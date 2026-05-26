---
title: "pipeline vs pipe: error handling"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - pipeline
  - error-handling
aliases:
  - pipe antipattern
  - stream/promises
  - finished
---

# pipeline vs pipe: error handling

> [!abstract] TL;DR
> `.pipe()` é antipattern moderno: não propaga erros — se um Transform falhar no meio da cadeia, o source continua aberto, o destination continua aberto, e você tem um leak silencioso de file descriptors e memória. `pipeline()` (callback ou `stream/promises` async) destrói todos os streams da cadeia ao primeiro erro, propaga o erro ao chamador, e suporta `AbortSignal` para cancelamento. Use `pipeline` por default em todo código novo; `.pipe()` apenas em código legacy onde não vale a pena refatorar.

---

## O que é

Node.js tem duas APIs para conectar streams em sequência:

### `.pipe()` — a API clássica (Node 0.x)

```javascript
readable.pipe(writable);
// ou em cadeia:
source.pipe(transform).pipe(destination);
```

`.pipe()` retorna a stream de destino, permitindo encadeamento. É a API original de streams, disponível desde Node.js 0.x. Funciona passando chunks do Readable para o Writable conforme o consumer pede, com gestão básica de backpressure.

### `stream.pipeline()` — a API moderna (Node 10+)

```javascript
// Versão callback — node:stream
import { pipeline } from 'node:stream';

pipeline(source, transform, destination, (err) => {
  if (err) console.error('Pipeline falhou:', err);
  else console.log('Pipeline concluído.');
});
```

```javascript
// Versão promise — node:stream/promises (Node 15+, idioma 2026)
import { pipeline } from 'node:stream/promises';

await pipeline(source, transform, destination);
```

`pipeline()` aceita qualquer número de streams, AsyncIterables e funções geradoras. Gerencia a conexão entre elas, backpressure, cleanup e propagação de erros de forma unificada.

### `stream.finished()` — helper para stream única

```javascript
import { finished } from 'node:stream/promises';

await finished(stream); // resolve quando stream termina, rejeita se errar
```

Útil quando você precisa aguardar o término de uma stream isolada, sem estar dentro de um `pipeline()`.

---

## Por que importa

`.pipe()` em código novo é **red flag de code review**.

Não é questão de estilo — é uma questão de corretude. O problema concreto: `.pipe()` **não propaga erros**. A documentação oficial do Node.js afirma explicitamente:

> "If the `Readable` stream emits an error during processing, the `Writable` destination is not closed automatically. If an error occurs, it will be necessary to manually close each stream in order to prevent memory leaks."

Isso significa que em qualquer cadeia com `.pipe()`, um único erro em qualquer stream deixa **todas as demais abertas**. Em código de produção que processa arquivos, conexões de banco ou sockets de rede, isso resulta em:

- File descriptors abertos que nunca fecham.
- Buffers em memória que nunca liberam.
- Writable streams que nunca emitem `'finish'`.
- Processos que lentamente acumulam recursos até atingir limites do OS.

O erro não aparece em desenvolvimento com cenários simples. Aparece em produção, em condições de falha parcial — exatamente quando você mais precisa que o cleanup funcione.

`pipeline()` resolve todos esses problemas automaticamente.

---

## Como funciona

### 1. `.pipe()` clássico — o problema

```javascript
// PROBLEMÁTICO — não propaga erros
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';

const source      = createReadStream('input.tar');
const compress    = createGzip();
const destination = createWriteStream('output.tar.gz');

source.pipe(compress).pipe(destination);

// Se compress emitir 'error':
//   → destination NÃO é destruída automaticamente
//   → source NÃO para automaticamente
//   → o erro não vai a lugar nenhum (unhandled 'error' → crash)
//   → file descriptors de source e destination ficam abertos
```

Para fazer `.pipe()` corretamente, você precisaria registrar listeners de erro em **cada stream** individualmente e chamar `.destroy()` em todas — exatamente o que `pipeline()` faz internamente, de forma robusta e testada.

### 2. `pipeline()` — versão callback

```javascript
import { pipeline } from 'node:stream';
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';

pipeline(
  createReadStream('input.tar'),
  createGzip(),
  createWriteStream('output.tar.gz'),
  (err) => {
    if (err) {
      console.error('Pipeline falhou:', err);
      // Todas as streams já foram destruídas pelo runtime
    } else {
      console.log('Compressão concluída.');
    }
  }
);
```

Quando `createGzip()` errar (ou qualquer outra stream):
1. O runtime destrói o Readable de origem.
2. O runtime destrói todos os Transforms intermediários.
3. O runtime destrói o Writable de destino.
4. O erro é passado ao callback como primeiro argumento.

Nenhum recurso fica aberto. Nenhum tratamento manual é necessário.

### 3. `pipeline()` async — o idioma de 2026

```javascript
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';

async function comprimir(input, output) {
  try {
    await pipeline(
      createReadStream(input),
      createGzip(),
      createWriteStream(output),
    );
    console.log('Concluído.');
  } catch (err) {
    // Todas as streams já foram destruídas
    console.error('Falha na compressão:', err);
  }
}

await comprimir('input.tar', 'output.tar.gz');
```

A versão promise integra naturalmente com `async/await`, elimina callback hell e permite uso de `try/catch` para tratamento de erro — o mesmo padrão usado para qualquer outra operação assíncrona.

### 4. Múltiplos transforms na pipeline

```javascript
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';
import { Transform } from 'node:stream';

// Cada Transform é uma etapa de processamento
const splitLines  = new Transform({ /* ... */ });
const parseCsv    = new Transform({ /* ... */ });
const toJsonLines = new Transform({ /* ... */ });

await pipeline(
  createReadStream('dados.csv'),
  splitLines,   // 'linha1\nlinha2' → ['linha1', 'linha2']
  parseCsv,     // 'campo1,campo2' → { campo1, campo2 }
  toJsonLines,  // { campo1, campo2 } → '{"campo1":...}\n'
  createWriteStream('dados.jsonl'),
);
// Se parseCsv lançar erro em um registro malformado:
//   → createReadStream para
//   → splitLines é destruída
//   → parseCsv é destruída
//   → toJsonLines é destruída
//   → createWriteStream é destruída (arquivo parcial fechado)
//   → await rejeita com o erro
```

A cadeia pode ter qualquer número de etapas. O cleanup é sempre total.

### 5. `AbortSignal` para cancelamento

```javascript
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';

const controller = new AbortController();

// Cancela automaticamente após 5 segundos
const timeout = setTimeout(() => controller.abort(), 5_000);

try {
  await pipeline(
    createReadStream('arquivo-grande.tar'),
    createGzip(),
    createWriteStream('arquivo-grande.tar.gz'),
    { signal: controller.signal }, // AbortSignal no objeto de opções
  );
  clearTimeout(timeout);
} catch (err) {
  if (err.name === 'AbortError') {
    console.error('Pipeline cancelado por timeout.');
  } else {
    console.error('Erro na pipeline:', err);
  }
  // Em ambos os casos, todas as streams já foram destruídas
}
```

Quando o sinal é abortado:
- `destroy()` é chamado em todas as streams da cadeia com um `AbortError`.
- A promise rejeita com o `AbortError`.
- Nenhum recurso fica aberto.

> [!warning] `signal` vai dentro de um objeto de opções
> A assinatura é `pipeline(source, ...transforms, destination, { signal })`.
> Passar `signal` diretamente como quinto argumento — `pipeline(a, b, c, signal)` — não funciona. O signal precisa estar dentro de um objeto `{ signal }`. Esse é um dos erros mais comuns com `AbortSignal`.

### 6. `finished()` para aguardar stream única

```javascript
import { finished } from 'node:stream/promises';
import { createReadStream } from 'node:fs';

const stream = createReadStream('dados.bin');
stream.resume(); // coloca em flowing mode para drenar

try {
  await finished(stream);
  console.log('Stream concluída.');
} catch (err) {
  console.error('Stream falhou:', err);
}
```

`finished()` é o helper correto quando você precisa aguardar o término de uma stream que você não controla completamente — por exemplo, uma stream que já está em andamento em outro lugar, ou uma `Response` de fetch que você precisa drenar antes de prosseguir.

> [!info] `cleanup: false` por padrão
> `finished()` deixa event listeners (`'error'`, `'end'`, `'finish'`, `'close'`) no stream após resolver — previne crashes por eventos tardios de implementações incorretas. Use `cleanup: true` quando você controla o ciclo de vida da stream e quer limpeza imediata.

---

## Na prática

### Regra de ouro — quando usar cada API

| Situação | API recomendada |
|----------|----------------|
| Conectar 2+ streams em sequência | `await pipeline(...)` de `node:stream/promises` |
| Lógica entre chunks que precisa de `break` ou condicional | `for await...of` (ver nota 08) |
| Aguardar stream única em andamento | `await finished(stream)` de `node:stream/promises` |
| Integração com biblioteca que só usa `.pipe()` | `.pipe()` com listeners de erro manuais em cada stream |
| Código legado que não vale refatorar | `.pipe()` com listeners de erro manuais |

Para 90% dos casos em código Node moderno, a resposta é `await pipeline(...)`. A exceção são cenários onde você precisa iterar sobre os chunks com lógica de controle de fluxo — nesses casos, `for await...of` sobre um Readable é mais expressivo.

### Padrão para operações de arquivo

```javascript
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';

// Compressão de arquivo — padrão idiomático
export async function gzip(inputPath, outputPath) {
  await pipeline(
    createReadStream(inputPath),
    createGzip(),
    createWriteStream(outputPath),
  );
}
```

Três linhas. Sem listeners de erro. Sem cleanup manual. Sem file descriptors abertos em caso de falha.

### `.pipe()` com tratamento mínimo correto

Se por algum motivo você precisar usar `.pipe()`, o mínimo necessário é registrar um listener de `'error'` em **cada stream** e chamar `.destroy(err)` em todas. `pipeline()` faz isso — mais tratamento de casos edge — em 3 linhas.

---

## Armadilhas

### 1. `.pipe()` sem error handler em cada stream → leak silencioso

```javascript
// ERRADO — bug clássico que parece correto
const rs = createReadStream('input.csv');
const transform = createCsvParser();
const ws = createWriteStream('output.json');

rs.pipe(transform).pipe(ws);

// Se createCsvParser emitir 'error':
//   → rs fica aberto (file descriptor não fechado)
//   → ws fica aberto (arquivo parcialmente escrito, fd aberto)
//   → o erro vai para o handler de 'uncaughtException' ou trava o processo
//   → em produção: file descriptor leak até atingir limite do OS (EMFILE)
```

O comportamento EMFILE ("too many open files") é a manifestação clássica desse bug em produção. O processo funciona normalmente por horas, depois começa a falhar ao abrir qualquer arquivo.

### 2. `pipeline()` async sem `await` → unhandledRejection

```javascript
// ERRADO — promise rejeitada ignorada
pipeline(
  createReadStream('input.txt'),
  transform,
  createWriteStream('output.txt'),
); // sem await, sem .catch()

// Se a pipeline falhar:
//   → UnhandledPromiseRejection
//   → Em Node 15+: processo termina com código de saída 1
//   → Em Node 14 e anteriores: warning, mas processo continua — o pior cenário
```

```javascript
// CORRETO
await pipeline(...);
// ou
pipeline(...).catch(handleError);
```

### 3. `AbortSignal` sem objeto de opções → erro silencioso

```javascript
const ctrl = new AbortController();

// ERRADO — signal passado diretamente, não em { signal }
await pipeline(source, transform, destination, ctrl.signal);
// ctrl.signal é tratado como stream adicional na pipeline
// → TypeError obscuro ou comportamento indefinido

// CORRETO
await pipeline(source, transform, destination, { signal: ctrl.signal });
```

### 4. Misturar `.pipe()` e `pipeline()` na mesma cadeia

```javascript
// ERRADO — ambíguo e perigoso
const partial = source.pipe(transform); // .pipe() retorna transform
await pipeline(partial, destination);   // pipeline tenta gerenciar partial

// O pipeline() não tem visibilidade sobre source.
// Se source errar, pipeline() não o destroi.
// LEAK.
```

Escolha uma API para toda a cadeia. Nunca misture.

### 5. `finished()` sem `cleanup: true` em streams reutilizáveis

```javascript
// Atenção: listeners acumulam se cleanup: false (padrão)
for (const stream of muitasStreams) {
  await finished(stream); // acumula listeners 'error'/'end'/'finish'/'close'
}

// CORRETO para uso em loop
for (const stream of muitasStreams) {
  await finished(stream, { cleanup: true });
}
```

Para uma stream usada uma única vez, o padrão `cleanup: false` é inofensivo. Em loops ou reutilização, use `cleanup: true`.

---

## Em entrevista

### Frase pronta

> "`.pipe()` is an antipattern in modern Node code. The reason is concrete: it doesn't propagate errors. If a transform stream fails mid-pipeline, the source stream stays open, the destination stays open, and you leak file descriptors and memory — this is the classic EMFILE bug. The replacement is `pipeline()` — there's a callback version in `node:stream` and a promise version in `node:stream/promises`. The promise version is the 2026 idiom: `await pipeline(source, transform, destination)`. It automatically destroys all streams on error, propagates the error to the caller, and accepts an `AbortSignal` for cancellation. For waiting on a single stream to finish, `finished()` from the same module is the right tool."

### Perguntas frequentes e respostas diretas

**"Por que `.pipe()` não propaga erros?"**
Por design histórico: adicionado em Node 0.x, registra `'end'` para fechar a destination quando a source termina, mas não registra `'error'`. Refatorar quebraria compatibilidade retroativa.

**"Qual a diferença entre `pipeline` de `node:stream` e de `node:stream/promises`?"**
Comportamento idêntico. Só muda a interface: callback vs. Promise. Para código novo, prefira `stream/promises` — integra com `async/await` e `try/catch`.

**"O que `pipeline()` faz quando uma stream falha?"**
Chama `.destroy(err)` em **todas** as streams da cadeia — source, todos os transforms e destination. Depois invoca o callback ou rejeita a promise. Nenhum resource fica aberto.

**"Quando usar `finished()` em vez de `pipeline()`?"**
Quando você tem uma stream única já em andamento e precisa aguardar o término — não está conectando múltiplas streams. Ex.: aguardar fim de upload ou drenar body de `Request` HTTP.

**"Como cancelar uma pipeline em andamento?"**
`const ctrl = new AbortController()` → passe `{ signal: ctrl.signal }` como último argumento → `ctrl.abort()` destrói todas as streams com `AbortError` e rejeita a promise.

### Vocabulário PT-BR ↔ EN

| Português | English |
|-----------|---------|
| pipeline | pipeline |
| propagação de erro | error propagation |
| limpeza / cleanup | cleanup |
| sinal de aborto | AbortSignal |
| legado | legacy |
| vazamento de file descriptor | file descriptor leak |
| destruir stream | destroy stream |
| cadeia de streams | stream chain |
| cancelamento | cancellation |
| tratamento de erro | error handling |

---

## Rubric

| Critério | Status |
|----------|--------|
| TL;DR cobre `.pipe()` como antipattern com razão concreta | OK |
| `.pipe()` sem error handler: comportamento documentado | OK |
| `pipeline()` callback: assinatura e comportamento | OK |
| `pipeline()` async/await: idioma 2026 documentado | OK |
| Múltiplos transforms: exemplo com pipeline | OK |
| `AbortSignal`: assinatura correta `{ signal }` documentada | OK |
| `finished()`: uso correto com opções documentadas | OK |
| Regra de ouro: tabela quando usar cada API | OK |
| Armadilhas (5) com código e consequência real | OK |
| EMFILE como manifestação concreta do bug em produção | OK |
| Frase pronta para entrevista em EN | OK |
| Perguntas frequentes com respostas diretas | OK |
| Vocabulário PT-BR ↔ EN (10 termos) | OK |
| Veja também com wikilinks corretos | OK |
| Sem fabricação de dados reais | OK |

---

## Veja também

- `[[06 - Backpressure]]` — backpressure: o problema que `pipeline()` resolve automaticamente
- `[[08 - Async iteration de streams]]` — `for await...of` como alternativa a `pipeline()` quando há lógica entre chunks
- `[[10 - Padrões práticos]]` — padrões completos de uso de streams em produção
- `[[12 - Armadilhas, regras práticas, cheatsheet]]` — referência rápida de antipatterns e decisões
- `[[Node.js]]` — tronco: panorama do runtime

---

## Fontes

- [Node.js Docs — stream.pipeline()](https://nodejs.org/api/stream.html#streampipelinesource-transforms-destination-callback)
- [Node.js Docs — stream/promises.pipeline()](https://nodejs.org/api/stream.html#streampromisespipeline-source-transforms-destination-options)
- [Node.js Docs — stream.finished()](https://nodejs.org/api/stream.html#streamfinishedstream-options-callback)
