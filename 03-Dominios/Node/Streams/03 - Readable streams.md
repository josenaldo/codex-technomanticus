---
title: "Readable streams"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - readable
aliases:
  - Readable
  - Modo flowing
  - Modo paused
---

# Readable streams

> [!abstract] TL;DR
> Readable tem 2 modos: **flowing** (listener de `'data'` → chunks empurrados automaticamente) e **paused** (`.read()` puxa chunk a chunk; default em Node moderno). Eventos principais: `data`, `end`, `error`, `close`, `readable`. Implementação custom: subclasse `Readable` + `_read(size)` + `push(chunk)` / `push(null)` (sinal de fim). `Readable.from(iterable)` é o atalho moderno para criar Readable em produção sem subclasse. Em 2026, o idioma canônico de consumo é `for await...of` — veja `[[08 - Async iteration de streams]]`.

---

## O que é

`Readable` é a classe base de Node.js para **fontes de dados**. Qualquer coisa que produz bytes ou objetos para consumo downstream é uma Readable: `fs.createReadStream`, HTTP response no lado do cliente, `process.stdin`, resultado de `zlib.createGunzip()` lido após inflate.

A classe vive em `node:stream` e pode ser:

- **Usada diretamente** via `Readable.from(iterable)` — o caminho moderno.
- **Subclassificada** para implementar fontes customizadas via `_read(size)`.
- **Consumida** via eventos (`'data'`, `'readable'`), `.pipe()`, ou `for await...of`.

A propriedade `readable.readableFlowing` expõe o estado interno como três valores possíveis:

| Valor | Significado |
|-------|-------------|
| `null` | Nenhum mecanismo de consumo ainda; stream não gera dados |
| `false` | Pausado explicitamente (backpressure ou `.pause()`) |
| `true` | Em flowing; emitindo dados ativamente |

---

## Por que importa

Escolher o modo errado de consumo introduz bugs que não aparecem em desenvolvimento mas explodem em produção:

- **Perda de chunks**: stream entra em flowing antes do listener estar registrado.
- **Vazamento de memória**: stream em paused sem ninguém chamar `.read()` enche o buffer interno indefinidamente.
- **Deadlock silencioso**: `'end'` nunca dispara porque o dado nunca é consumido.
- **Backpressure ignorado**: produtor mais rápido que consumidor sem controle de fluxo.

Entender os dois modos e quando cada um aplica é pré-requisito para trabalhar com qualquer stream em Node — inclusive abstrações de alto nível como `pipe()` e `for await...of` usam esses mecanismos internamente.

---

## Como funciona

### Estado interno e a transição de modos

Toda Readable começa em `readableFlowing === null`. O stream **não produz dados** enquanto nenhum mecanismo de consumo estiver ativo. A transição acontece assim:

```
null  →  true   : on('data', ...)  /  .resume()  /  .pipe()
null  →  false  : .pause()  /  .unpipe()
true  →  false  : .pause()
false →  true   : .resume()  /  on('data', ...)
```

### Flowing mode — listener de `'data'`

Adicionar um listener de `'data'` é suficiente para colocar o stream em flowing. Os chunks chegam empurrados pelo runtime assim que estão disponíveis no buffer interno:

```javascript
import { createReadStream } from 'node:fs';

const readable = createReadStream('./arquivo.txt', { encoding: 'utf8' });

readable.on('data', (chunk) => {
  // chunk chega empurrado; você não controla o ritmo
  process(chunk);
});

readable.on('end', () => {
  // Disparado UMA vez, depois que o último chunk foi consumido
  console.log('Leitura concluída');
});

readable.on('error', (err) => {
  // SEMPRE trate 'error' — não tratar é fatal em Node 22+
  console.error('Erro na leitura:', err);
});
```

> [!warning] Regra: sempre registre `'error'`
> Em Node 22+, um `'error'` sem listener lança uma exceção não capturada e derruba o processo. Não existe Readable "segura" sem handler de erro.

### Paused mode — evento `'readable'` + `.read()`

No modo paused, o runtime avisa via `'readable'` que há dados disponíveis no buffer interno. Você puxa com `.read(size)` até receber `null` (buffer vazio):

```javascript
import { createReadStream } from 'node:fs';

const readable = createReadStream('./arquivo.txt');

readable.on('readable', () => {
  let chunk;
  // Loop de pull: puxa até esvaziar o buffer
  while ((chunk = readable.read()) !== null) {
    process(chunk);
  }
});

readable.on('end', () => {
  console.log('Fim do stream');
});

readable.on('error', (err) => {
  console.error(err);
});
```

`.read(size)` aceita um argumento opcional que especifica quantos bytes retornar. Se o buffer interno tiver menos do que `size` bytes, retorna `null` mesmo que ainda hajam dados a vir — o próximo `'readable'` chegará quando o buffer atingir `size`.

> [!info] `'readable'` vs `'data'`
> Quando ambos os listeners existem no mesmo stream, `'readable'` assume controle do fluxo e `'data'` só emite quando `.read()` é chamado. Não misture os dois estilos na mesma instância.

### Implementação custom: subclasse + `_read`

Para criar uma fonte de dados que não existe como arquivo ou socket — gerador de sequências, paginação de API, dados sintéticos — você subclassifica `Readable` e implementa `_read(size)`:

```javascript
import { Readable } from 'node:stream';

class CounterReadable extends Readable {
  constructor(max, options = {}) {
    super(options);
    this.i = 0;
    this.max = max;
  }

  _read(/* size é um hint; pode ser ignorado */) {
    if (this.i >= this.max) {
      // push(null) sinaliza fim do stream — OBRIGATÓRIO
      this.push(null);
    } else {
      // push retorna false quando o buffer está cheio (backpressure)
      // _read não será chamado novamente até o consumidor drenar
      this.push(`${this.i++}\n`);
    }
  }
}

// Uso:
const counter = new CounterReadable(5);
counter.on('data', (chunk) => process.stdout.write(chunk));
counter.on('end', () => console.log('FIM'));
// Saída: 0, 1, 2, 3, 4, FIM
```

**Contrato de `_read`:**

- É chamado pelo runtime quando o consumidor precisa de mais dados (buffer abaixo de `highWaterMark`).
- Deve chamar `this.push(chunk)` uma ou mais vezes, OU `this.push(null)` para sinalizar fim.
- **Não deve** chamar `this.push()` depois de já ter feito `this.push(null)` — o stream estará encerrado.
- O argumento `size` é um hint (quantos bytes o consumidor quer); pode ser ignorado com segurança.

### `Readable.from(iterable)` — o atalho moderno

Em código de produção, criar uma subclasse raramente é necessário. `Readable.from()` converte qualquer iterable ou async iterable em Readable:

```javascript
import { Readable } from 'node:stream';

// A partir de um array
const fromArray = Readable.from(['chunk1\n', 'chunk2\n', 'chunk3\n']);

// A partir de um generator síncrono
function* counter(max) {
  for (let i = 0; i < max; i++) yield `${i}\n`;
}
const fromGenerator = Readable.from(counter(5));

// A partir de um async generator — o caso mais poderoso
async function* fetchPages(baseUrl, pages) {
  for (let page = 1; page <= pages; page++) {
    const response = await fetch(`${baseUrl}?page=${page}`);
    yield await response.text();
  }
}
const fromAsyncGen = Readable.from(fetchPages('https://api.example.com/data', 3));

// Consumo com for await...of (idioma canônico em 2026)
for await (const chunk of fromAsyncGen) {
  console.log(chunk);
}
```

`Readable.from()` sempre cria um stream em **object mode por padrão** quando o iterable produz valores que não são strings ou Buffers. Para forçar binary mode, passe `{ objectMode: false, encoding: 'utf8' }`.

### Object mode

Por padrão, Readable streams processam `Buffer`, `string`, `TypedArray` e `DataView`. Ativar `objectMode: true` permite qualquer valor JavaScript — objetos, números, `null` não é mais sinal de EOF (EOF é apenas `push(null)` internamente; o objeto `null` é bloqueado):

```javascript
import { Readable } from 'node:stream';

const objectStream = new Readable({
  objectMode: true,
  read() {}
});

objectStream.push({ id: 1, nome: 'Alice' });
objectStream.push({ id: 2, nome: 'Bob' });
objectStream.push(null); // fim

objectStream.on('data', (obj) => {
  // obj é um plain object, não Buffer
  console.log(obj.nome);
});
```

> [!warning] Object mode é irreversível
> Não é possível alternar `objectMode` de uma instância existente. Defina na construção. Streams em object mode têm `highWaterMark` contado em **número de objetos**, não bytes.

---

## Na prática

Padrão observado em codebases Node modernas (2024–2026):

| Cenário | Abordagem recomendada |
|---------|----------------------|
| Criar Readable de lista/generator | `Readable.from(iterable)` |
| Consumir qualquer Readable | `for await...of` (veja nota 08) |
| Pipe para Writable/Transform | `.pipe()` ou `stream.pipeline()` |
| Implementar fonte custom rara | Subclasse + `_read` |
| Modo paused com `.read()` | Apenas em libs internas de baixo nível |

**`Readable.from(iterable)` é o default.** Você raramente precisa de subclasse — bibliotecas maduras (drivers de banco, HTTP clients) já expõem Readable prontas. Subclasse aparece em entrevistas como teste de conhecimento do contrato interno, não como padrão de produção.

**Modo paused com `.read()`** está presente em código legado e em implementações de parsers de protocolo. Em código de aplicação, `for await...of` oferece o mesmo controle de pull com sintaxe muito mais clara.

---

## Armadilhas

> [!danger] 1. Adicionar listener `'data'` tarde demais
> Se o stream já entrou em flowing (por exemplo, via `.resume()` ou `.pipe()`), adicionar `on('data')` depois que dados começaram a fluir **perde os chunks anteriores**. Sempre registre listeners antes de qualquer operação que ative o stream.
>
> ```javascript
> // ERRADO — possível perda de dados
> const r = createReadStream('./big.txt');
> r.resume(); // stream começa a fluir
> setTimeout(() => {
>   r.on('data', (chunk) => process(chunk)); // chunks iniciais já foram perdidos
> }, 100);
>
> // CORRETO — listener antes de qualquer ativação
> const r = createReadStream('./big.txt');
> r.on('data', (chunk) => process(chunk)); // registra ANTES de fluir
> ```

> [!danger] 2. Não tratar `'error'`
> Em Node 22+, um `'error'` sem listener é uma `uncaughtException` que derruba o processo. Sempre registre `on('error')` em toda Readable que você consume diretamente.

> [!danger] 3. Esquecer `push(null)` em `_read`
> Se `_read` nunca chama `push(null)`, o stream nunca emite `'end'`. O consumidor fica bloqueado indefinidamente esperando mais dados. Isso é especialmente sutil quando `push(null)` está atrás de uma branch condicional que nunca é atingida.
>
> ```javascript
> // BUG — 'end' nunca dispara se count > max
> _read() {
>   if (this.count < this.max) {
>     this.push(`${this.count++}`);
>   }
>   // esqueceu: else { this.push(null); }
> }
> ```

> [!danger] 4. `_read` síncrono que sempre tem dados sem yield
> Se `_read` chamar `push()` de forma completamente síncrona e nunca receber backpressure (porque o consumidor é rápido), o runtime chama `_read` novamente no mesmo tick em um loop. Em generators ou fontes infinitas, isso pode esgotar a stack ou monopolizar o event loop. Use `process.nextTick()` ou `setImmediate()` para yield:
>
> ```javascript
> _read() {
>   // Versão com yield para não bloquear o event loop
>   process.nextTick(() => {
>     this.push(`${this.i++}\n`);
>   });
> }
> ```

> [!caution] 5. Misturar estilos de consumo
> Usar `on('data')`, `on('readable')`, `.pipe()` e `for await...of` no mesmo stream leva a comportamento imprevisível. Escolha **um** mecanismo de consumo por instância.

---

## Em entrevista

**Frase pronta:**

> "A Readable stream is a source of chunks. It has two modes: flowing, where you attach a `'data'` listener and chunks are pushed to you; and paused, where you call `.read()` to pull. Modern Node code rarely uses either directly — `for await...of` is the canonical idiom in 2026, and it handles backpressure automatically. To create a Readable from an iterable, `Readable.from()` is the one-liner. To implement a custom Readable, subclass and define `_read(size)`, calling `push(chunk)` for each chunk and `push(null)` to signal end."

**Vocabulário para usar em inglês:**

| PT-BR | EN |
|-------|----|
| modo flowing | flowing mode |
| modo paused | paused mode |
| empurrar chunk | push a chunk |
| puxar chunk | pull a chunk |
| modo objeto | object mode |
| sinalizar fim | signal end-of-stream / EOF |
| limite de buffer | highWaterMark |
| contrapressão | backpressure |

**Perguntas frequentes e respostas curtas:**

- *"O que acontece se você não chamar `push(null)`?"* → O stream nunca emite `'end'`; consumidores ficam bloqueados.
- *"Qual a diferença entre `'readable'` e `'data'`?"* → `'data'` = flowing (push); `'readable'` = paused (pull). Não misture os dois.
- *"Quando usar subclasse vs `Readable.from()`?"* → `Readable.from()` para qualquer coisa baseada em iterable/generator. Subclasse apenas quando você precisa controlar `highWaterMark` manualmente ou integrar com uma fonte de I/O de baixo nível.
- *"`readableFlowing === null` vs `false`?"* → `null` = nenhum mecanismo de consumo ainda (stream não gera dados); `false` = pausado explicitamente após ter tido consumo.

---

## Veja também

- `[[02 - Os 4 tipos - Readable, Writable, Duplex, Transform]]` — onde Readable se encaixa no modelo geral
- `[[04 - Writable streams]]` — o lado destino do fluxo
- `[[06 - Backpressure]]` — como Readable e Writable negociam pressão
- `[[08 - Async iteration de streams]]` — `for await...of`, o idioma canônico de consumo
- `[[Node.js]]` — tronco do domínio Node

---

## Fontes

- [Node.js Docs — Stream: Readable Streams](https://nodejs.org/api/stream.html#readable-streams)
