---
title: "Promise-based core APIs"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: seedling
progresso: andamento
publish: false
tags:
  - node
  - promises
  - async
  - core-apis
  - tooling
aliases:
  - fs/promises
  - timers/promises
  - stream/promises
---

# Promise-based core APIs

> [!abstract] TL;DR
> Node.js expõe versões Promise-based dos módulos core via submódulos `node:fs/promises`, `node:stream/promises`, `node:timers/promises`, `node:readline/promises` e `node:dns/promises` — use-os sempre que escrever código async/await em vez de misturar callbacks no meio de promises.
> `stream/promises.pipeline()` é a forma correta de encadear streams sem vazar listeners em caso de erro; `.pipe()` manual não faz cleanup automático.
> O prefixo `node:` nos imports é recomendado desde Node 14.18.0 para distinguir módulos core de pacotes npm com o mesmo nome.

## O que é

O Node.js nasceu com um modelo de I/O baseado em callbacks (padrão `(err, data) => {}`). Com a popularização de `async/await` no ES2017+, usar callbacks diretamente em código moderno cria incompatibilidades de fluxo de controle, exige wrappers (`util.promisify`) e torna o tratamento de erros mais verboso.

Para resolver isso sem quebrar compatibilidade retroativa, o Node.js adicionou **submódulos promise-based** aos módulos core existentes — acessíveis como `node:fs/promises`, `node:timers/promises`, etc. Estes submódulos expõem as mesmas operações que os módulos originais, mas com uma interface baseada em `Promise` (e, em alguns casos, async generators ou `AsyncIterable`).

**Por que isso importa:**
- Evita instalar pacotes externos (`graceful-fs`, `p-timeout`, `readline-sync`) para operações que o core já cobre.
- Permite usar `try/catch` para tratamento de erros em I/O, em vez de verificar `err` em callbacks.
- Integra naturalmente com `async/await` e `for await...of`.
- `util.promisify` ainda funciona, mas é mais verboso e não suporta recursos avançados como `FileHandle`.

## Como funciona

### node:fs/promises

Disponível como `fs.promises` desde Node 10.1.0 (experimental), estável em Node 11.14.0/10.17.0; o subpath `node:fs/promises` foi adicionado em Node 14.0.0. Cobre operações de arquivo e diretório com interface promise.

**Operações principais:** `readFile`, `writeFile`, `appendFile`, `unlink`, `rename`, `mkdir`, `rm`, `stat`, `access`, `readdir`, `copyFile`, `open`.

```js
import { readFile, writeFile, mkdir, rm } from 'node:fs/promises';

// leitura com encoding (retorna string)
const content = await readFile('./config.json', 'utf8');
const config = JSON.parse(content);

// escrita atômica: escreve no temp, renomeia — evita arquivo corrompido em crash
await writeFile('./output.json', JSON.stringify(config, null, 2), 'utf8');

// criação recursiva de diretório (não lança se já existe)
await mkdir('./logs/2026/05', { recursive: true });

// remoção recursiva (equivalente a rm -rf)
await rm('./tmp', { recursive: true, force: true });
```

**FileHandle API** — para leitura/escrita granular sem carregar o arquivo inteiro na memória:

```js
import { open } from 'node:fs/promises';

const fh = await open('./data.bin', 'r');
try {
  const buf = Buffer.alloc(128);
  const { bytesRead } = await fh.read(buf, 0, 128, 0);
  console.log('bytes lidos:', bytesRead);
} finally {
  await fh.close();  // sempre fechar em finally
}
```

### node:stream/promises

Disponível desde Node 15.0.0. Dois utilitários críticos: `pipeline` e `finished`.

**`pipeline(...streams)`** — encadeia streams com cleanup automático. Se qualquer stream emitir `'error'`, todos os outros são destruídos e a promise rejeita. O `.pipe()` manual não faz isso: um erro no meio da cadeia pode deixar streams anteriores rodando indefinidamente, vazando memória.

```js
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';
import { pipeline } from 'node:stream/promises';

// ✅ pipeline: cleanup automático em erro, promise-based
await pipeline(
  createReadStream('./arquivo-grande.log'),
  createGzip(),
  createWriteStream('./arquivo-grande.log.gz')
);

// Se createGzip() lançar um erro, createReadStream() é destruído automaticamente
// Sem vazamento de file descriptor
```

**`finished(stream)`** — aguarda um stream terminar (`'end'`/`'finish'`) ou errar (`'error'`/`'close'`). Útil quando você apenas quer saber quando um stream terminou sem encadeá-lo com `pipeline`.

```js
import { finished } from 'node:stream/promises';
import { createWriteStream } from 'node:fs';

const ws = createWriteStream('./output.txt');
ws.write('linha 1\n');
ws.write('linha 2\n');
ws.end();

await finished(ws);  // aguarda o flush completo para o disco
console.log('arquivo gravado com sucesso');
```

### node:timers/promises

Disponível desde Node 15.0.0. Três funções: `setTimeout`, `setInterval` (async generator) e `setImmediate`.

```js
import { setTimeout, setInterval, setImmediate } from 'node:timers/promises';

// delay: espera 500ms e continua
await setTimeout(500);
console.log('500ms depois');

// delay com valor de retorno (útil para testes)
const result = await setTimeout(100, 'done');  // resolve com 'done' após 100ms
console.log(result);  // 'done'

// setImmediate: resolve na check phase da próxima iteração do event loop
await setImmediate();
console.log('após a check phase atual');
```

**`setInterval` como async generator** — gera ticks em intervalos regulares sem acumular callback hell:

```js
import { setInterval, setTimeout } from 'node:timers/promises';

const TIMEOUT_MS = 2000;
const start = Date.now();

// polling: verifica condição a cada 200ms, para com break ou timeout
for await (const _ of setInterval(200)) {
  const status = await verificarServico();  // função hipotética
  if (status === 'ready') {
    console.log('serviço pronto');
    break;
  }
  if (Date.now() - start > TIMEOUT_MS) {
    throw new Error('timeout aguardando serviço');
  }
}
// Nota: para cancelamento externo com AbortController, envolva em try/catch
// para capturar o AbortError que o generator lança ao ser abortado
```

### node:readline/promises

Disponível desde Node 17.0.0. Substitui `readline` callback-based para leitura de stdin e de arquivos linha a linha.

**Input interativo com `question()`:**

```js
import { createInterface } from 'node:readline/promises';
import { stdin, stdout } from 'node:process';

const rl = createInterface({ input: stdin, output: stdout });

const nome = await rl.question('Seu nome: ');
const idade = await rl.question('Sua idade: ');

console.log(`Olá, ${nome}! Você tem ${idade} anos.`);
rl.close();  // sempre fechar para o processo terminar
```

**Leitura de arquivo linha a linha sem carregar tudo na memória:**

```js
import { createInterface } from 'node:readline/promises';
import { createReadStream } from 'node:fs';

const rl = createInterface({
  input: createReadStream('./grande.csv'),
  crlfDelay: Infinity  // trata \r\n como uma única quebra de linha
});

let linhas = 0;
for await (const linha of rl) {
  linhas++;
  // processa cada linha individualmente — memória O(1), não O(n)
}
console.log(`Total de linhas: ${linhas}`);
```

### node:dns/promises

Disponível desde Node 10.6.0. Evita o padrão callback de `dns.lookup` e `dns.resolve`.

```js
import { lookup, resolve, resolve4, reverse } from 'node:dns/promises';

// lookup: usa o resolvedor do SO (considera /etc/hosts e nsswitch.conf)
const { address, family } = await lookup('nodejs.org');
console.log(`${address} (IPv${family})`);

// resolve4: consulta DNS diretamente (bypassa /etc/hosts)
const enderecos = await resolve4('nodejs.org');
console.log(enderecos);  // ['104.20.22.46', ...]

// reverse: PTR lookup
const hostnames = await reverse('8.8.8.8');
console.log(hostnames);  // ['dns.google']
```

## Quando usar

**Sempre prefira os submódulos promise-based** em código moderno com `async/await`. As versões callback ainda existem por compatibilidade retroativa, mas não há motivo para usá-las em código novo.

| Necessidade | Módulo recomendado | Evitar |
|---|---|---|
| Leitura/escrita de arquivo | `node:fs/promises` | `fs.readFile(cb)` |
| Encadeamento de streams | `node:stream/promises.pipeline` | `.pipe()` manual |
| Delay async | `node:timers/promises.setTimeout` | `new Promise(r => setTimeout(r, ms))` |
| Polling com intervalo | `node:timers/promises.setInterval` | `setInterval` + flag global |
| Input CLI interativo | `node:readline/promises` | `readline` + `question` callback |
| Resolução DNS | `node:dns/promises` | `dns.lookup(cb)` |

**Quando `util.promisify` ainda faz sentido:**
- Funções de terceiros que seguem o padrão `(err, result) => {}` e não têm equivalente promise nativo.
- Migração incremental de código callback legado.

## Armadilhas comuns

### Armadilha 1: Misturar `fs` callback com `async/await`

```js
// ❌ Problema: importar o módulo raiz em vez do submódulo promises
import fs from 'node:fs';

async function lerConfig() {
  // fs.readFile é callback-based — não retorna Promise
  // Isso não funciona como esperado
  const content = await fs.readFile('./config.json', 'utf8');
  return JSON.parse(content);
}
// TypeError implícito: await de undefined (readFile retorna void)
```

```js
// ✅ Fix: importar do submódulo /promises
import { readFile } from 'node:fs/promises';

async function lerConfig() {
  const content = await readFile('./config.json', 'utf8');
  return JSON.parse(content);
}
```

### Armadilha 2: Usar `.pipe()` em vez de `stream/promises.pipeline()`

```js
// ❌ Problema: .pipe() não faz cleanup em erro
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';

const read = createReadStream('./input.log');
const gzip = createGzip();
const write = createWriteStream('./input.log.gz');

read.pipe(gzip).pipe(write);
// Se gzip emitir 'error', read e write continuam abertos
// → vazamento de file descriptor + arquivo de destino corrompido
```

```js
// ✅ Fix: stream/promises.pipeline destrói todos os streams em erro
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';

await pipeline(
  createReadStream('./input.log'),
  createGzip(),
  createWriteStream('./input.log.gz')
);
// Erro em qualquer etapa → todos os streams destruídos → sem vazamento
```

### Armadilha 3: Não fechar readline após uso

```js
// ❌ Problema: processo não termina porque readline mantém stdin aberto
import { createInterface } from 'node:readline/promises';
import { stdin, stdout } from 'node:process';

const rl = createInterface({ input: stdin, output: stdout });
const resposta = await rl.question('Nome: ');
console.log(`Olá, ${resposta}`);
// Processo fica suspenso — rl.close() não foi chamado
```

```js
// ✅ Fix: sempre fechar o interface após o último uso
import { createInterface } from 'node:readline/promises';
import { stdin, stdout } from 'node:process';

const rl = createInterface({ input: stdin, output: stdout });
try {
  const resposta = await rl.question('Nome: ');
  console.log(`Olá, ${resposta}`);
} finally {
  rl.close();  // libera stdin, permite que o processo termine
}
```

## Em entrevista

**Q: Why does Node.js have both callback-based and promise-based versions of its core modules, and which should you prefer?**

Node.js was designed around callbacks long before Promises existed in JavaScript, so the original core APIs (like `fs.readFile`) use the error-first callback convention. Rather than breaking those APIs — which would be a major semver-breaking change affecting millions of codebases — Node added parallel `promises` submodules accessible at paths like `node:fs/promises` and `node:timers/promises`. In modern code you should always prefer the promise-based submodules because they compose naturally with `async/await`, allow standard `try/catch` error handling, and avoid the callback pyramid of doom that makes async control flow hard to follow.

**Q: What is the difference between `stream/promises.pipeline()` and the manual `.pipe()` approach, and why does it matter in production?**

The core difference is error handling and resource cleanup. When you manually chain streams with `.pipe()`, an error emitted by a middle stream — like a gzip transform failing — does not automatically destroy the upstream readable or downstream writable streams. Those streams remain open, holding file descriptors and emitting events that nobody is listening to, which is a classic resource leak. `stream/promises.pipeline()` registers its own error handlers across all streams in the chain and ensures that if any stream fails, all others are properly destroyed before the returned promise rejects. In a long-running server that processes many files, a leak from manual `.pipe()` usage will accumulate open file handles until the process hits OS limits.

**Q: How does `node:timers/promises.setInterval` differ from the callback-based `setInterval`, and when would you use it?**

The callback-based `setInterval` fires a function repeatedly on a timer, but coordinating it with async operations requires external flags or promisification wrappers. `node:timers/promises.setInterval` returns an async generator that yields a value on each interval tick, which means you can use it directly in a `for await...of` loop and `await` async operations inside the loop body without worrying about overlapping ticks. You would use this for polling scenarios — checking an external service status, flushing a buffer periodically — where you want the simplicity of async/await without introducing a separate state machine or calling `clearInterval` explicitly (you just `break` from the loop).

## Vocabulário

| Português | Inglês |
|---|---|
| Módulo central | Core module |
| Submódulo de promessas | Promises submodule |
| Encadeamento de fluxos | Stream pipeline |
| Iterador assíncrono | Async iterator / async generator |
| Leitura de linha | Line-by-line reading / readline |
| Resolução de DNS | DNS resolution / DNS lookup |
| Vazamento de descritor de arquivo | File descriptor leak |
| Limpeza automática | Automatic cleanup / teardown |
| Interface de linha de comando | CLI interface |
| Promisificação | Promisification (via `util.promisify`) |

## Fontes

- [Node.js — fs/promises](https://nodejs.org/api/fs.html#promise-example)
- [Node.js — stream/promises](https://nodejs.org/api/stream.html#streampipelinestreams-options)
- [Node.js — timers/promises](https://nodejs.org/api/timers.html#timers-promises-api)
- [Node.js — readline/promises](https://nodejs.org/api/readline.html#promises-api)
- [Node.js — dns/promises](https://nodejs.org/api/dns.html#dnspromiseslookuphostname-options)

## Veja também

- [[Tooling e ecossistema moderno]]
- [[07 - Single Executable Apps (SEA)]]
- [[09 - Bun como runtime alternativo]]
- [[03-Dominios/Node/Streams/index|Streams (galho 3)]]
- [[Node.js]]
- [[03-Dominios/Node/index|Node.js (MOC central)]]
