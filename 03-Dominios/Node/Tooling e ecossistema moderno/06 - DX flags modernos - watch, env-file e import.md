---
title: "DX flags modernos - watch, env-file e import"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: seedling
progresso: andamento
publish: false
tags:
  - node
  - dx
  - flags
  - watch
  - env-file
  - tooling
aliases:
  - node --watch
  - node --env-file
---

# DX flags modernos - watch, env-file e import

> [!abstract] TL;DR
> O Node 18-22 introduziu flags que eliminam ferramentas externas comuns: `--watch` substitui o nodemon, reiniciando o processo quando arquivos importados mudam.
> `--env-file` carrega variáveis de ambiente a partir de um arquivo `.env` sem instalar o dotenv, e `--import` pré-carrega um módulo ESM antes do script principal, substituindo loaders manuais para registrar hooks de módulo.
> `--inspect` e `--inspect-brk` ativam o depurador V8 via WebSocket, dispensando dependências de depuração externas. Conhecer essas flags é um diferencial em entrevistas — demonstra domínio do runtime sem overhead de dependências.

## O que é

Há alguns anos, configurar um projeto Node.js para desenvolvimento exigia um conjunto previsível de dependências: `nodemon` para reiniciar o servidor ao salvar, `dotenv` para carregar variáveis de ambiente a partir de arquivos `.env`, e `ts-node` (ou um loader manual) para pré-carregar transformadores de módulo. Cada uma dessas ferramentas resolve um problema real, mas também adiciona pacotes, aumenta a superfície de configuração e introduz possíveis pontos de falha.

Entre o Node 18 e o Node 22, o runtime passou por um movimento de "menos é mais": absorver internamente as funcionalidades mais comuns que antes dependiam de pacotes externos. O resultado é um conjunto de flags de linha de comando que cobrem os casos de uso mais frequentes de DX sem nenhuma instalação adicional.

Essa filosofia não é nova — ela ecoa o movimento de consolidação que já ocorreu em outras camadas do ecossistema (por exemplo, o `node:test` substituindo Jest/Mocha para casos simples, o `fetch` nativo substituindo o `node-fetch`). As flags de DX são a manifestação desse movimento na camada de operação do processo.

## Como funciona

### --watch (Node 18.11.0+, estável no Node 22)

O flag `--watch` instrui o Node a monitorar os arquivos importados pelo script e reiniciar o processo automaticamente quando qualquer um deles sofrer alteração no sistema de arquivos.

O mecanismo é baseado no grafo de módulos: o Node rastreia quais arquivos foram carregados via `import` ou `require` durante a execução e registra watchers para todos eles. Quando um arquivo monitorado muda, o processo é encerrado e reiniciado do zero.

**Diferenças em relação ao nodemon:**

- O `--watch` não monitora `node_modules` por padrão (o nodemon também evita isso, mas exige configuração explícita).
- O `--watch` não possui arquivo de configuração próprio — o que simplifica a setup, mas limita a personalização.
- O `--watch` monitora apenas arquivos **já presentes no grafo de módulos no momento da inicialização**; novos arquivos criados enquanto o processo está rodando não são detectados automaticamente (ver Armadilhas comuns).
- O nodemon permite configurar extensões de arquivo, padrões de ignore e delays via `nodemon.json`; o `--watch` não tem essa granularidade.
- `--watch-path` (Node 22+) permite adicionar diretórios extras ao monitoramento, compensando parcialmente a limitação de novos arquivos.

```bash
# Monitorar app.js e todos os módulos que ele importa
node --watch app.js

# Monitorar app.js E o diretório ./src inteiro (Node 22+)
node --watch --watch-path=./src app.js

# Combinar com --env-file para desenvolvimento completo
node --watch --env-file=.env app.js
```

O `--watch` foi introduzido como experimental no Node 18.11.0 e estabilizado no Node 22. Em Node 18 e 20, pode exibir avisos experimentais que podem ser suprimidos com `--no-warnings`.

### --env-file (Node 20.6.0+)

O flag `--env-file` carrega variáveis de ambiente a partir de um arquivo de texto no formato `KEY=VALUE` (compatível com o formato `.env` popularizado pelo pacote `dotenv`) diretamente no `process.env`, sem necessidade de instalar ou chamar `require('dotenv').config()`.

**Comportamento de precedência importante:** o `--env-file` **não sobrescreve** variáveis já definidas no ambiente do processo. Se `NODE_ENV=production` já estiver definido no shell antes de invocar o node, o valor do `.env` é ignorado para essa variável. Esse comportamento é diferente do `dotenv` por padrão, que também não sobrescreve — mas o `dotenv` expõe `dotenv.config({ override: true })` para forçar a sobrescrita, algo que o `--env-file` não oferece.

**Múltiplos arquivos:** é possível especificar vários arquivos `--env-file`. Eles são processados da esquerda para a direita; o mesmo princípio de não-sobrescrita se aplica — a primeira definição de uma variável prevalece.

```bash
# Carregar .env básico
node --env-file=.env app.js

# Carregar .env base e sobrepor com valores locais
# .env.local é processado depois, mas NÃO sobrescreve variáveis já definidas por .env
node --env-file=.env --env-file=.env.local app.js

# Exemplo de .env compatível
# DATABASE_URL=postgres://localhost:5432/mydb
# PORT=3000
# NODE_ENV=development
```

```js
// app.js — após node --env-file=.env app.js
console.log(process.env.DATABASE_URL); // 'postgres://localhost:5432/mydb'
console.log(process.env.PORT);         // '3000'
console.log(process.env.NODE_ENV);     // 'development'

// Todas as variáveis chegam como strings — sempre converta explicitamente
const port = Number(process.env.PORT); // 3000 (number)
```

### --import (Node 12+, prático para hooks desde Node 20.6.0)

O flag `--import` pré-carrega um módulo ESM **antes** de o script principal ser executado. É o equivalente ESM do antigo `--require` (que pré-carregava módulos CJS).

O caso de uso mais comum é registrar hooks de módulo via a API `module.register()` (introduzida no Node 20.6.0). Esses hooks permitem interceptar a resolução e o carregamento de módulos — tornando possível, por exemplo, suporte a TypeScript, aliases de path ou outros transformadores sem modificar o código-fonte.

**`--import` vs `--require`:**

| Aspecto | `--require` | `--import` |
|---|---|---|
| Sistema de módulos | CJS | ESM |
| Quando executa | Antes do script | Antes do script |
| Sintaxe do arquivo pré-carregado | `require()` / CJS | `import` / ESM |
| Suporte a hooks ESM | Limitado | Nativo (via `module.register()`) |

```bash
# Pré-carregar um módulo de registro de hooks ESM
node --import ./register.mjs app.mjs

# Registrar ts-node/esm como loader TypeScript (legado)
node --import ts-node/esm src/index.ts

# Combinar com outros flags
node --import ./register.mjs --env-file=.env --watch app.mjs
```

```js
// register.mjs — exemplo de arquivo de registro de hooks
import { register } from 'node:module';
import { pathToFileURL } from 'node:url';

// Registra um loader customizado que intercepta imports .ts
register('./typescript-loader.mjs', pathToFileURL('./'));
```

A partir do Node 20.6.0, `module.register()` é a API canônica para registrar loaders ESM. Ela substitui a abordagem experimental anterior de `--loader` (que permanece funcional, mas com aviso de depreciação em versões mais recentes).

### --inspect e --inspect-brk (V8 Inspector)

O V8 Inspector Protocol é uma interface de depuração baseada em WebSocket que expõe o estado interno do processo Node (call stack, heap, variáveis locais, breakpoints) para ferramentas externas como o Chrome DevTools e o VS Code.

**`--inspect`** abre o servidor WebSocket do inspector no endereço `127.0.0.1:9229` (padrão) e o processo continua executando normalmente. O cliente de depuração pode se conectar a qualquer momento.

**`--inspect-brk`** faz o mesmo, mas **pausa a execução na primeira linha** do script (antes de qualquer código do usuário rodar). É indispensável para depurar código de inicialização que executa muito cedo — imports de nível de módulo, por exemplo.

**Como conectar no Chrome DevTools:**

1. Executar `node --inspect app.js`
2. Abrir `chrome://inspect` no Chrome
3. Clicar em "Open dedicated DevTools for Node" ou no link do processo listado

```bash
# Abre debugger; execução começa normalmente
node --inspect app.js

# Pausa na primeira linha (aguarda cliente conectar antes de continuar)
node --inspect-brk app.js

# Porta customizada (útil para múltiplos processos simultâneos)
node --inspect=9230 worker.js
```

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug app.js",
      "program": "${workspaceFolder}/app.js",
      "runtimeArgs": ["--inspect-brk"],
      "autoAttachChildProcesses": true,
      "skipFiles": ["<node_internals>/**"]
    },
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to running Node",
      "port": 9229,
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```

O flag `--inspect` está disponível desde o Node 6.3.0 e o `--inspect-brk` desde o Node 7.6.0 — são as flags de depuração mais antigas e estáveis desta lista.

### Outras flags úteis

Além das quatro principais, o runtime expõe um conjunto de flags adicionais que cobrem cenários frequentes de produção e profiling:

**`--max-old-space-size=N`** — define o tamanho máximo do heap V8 (geração antiga) em megabytes. O padrão varia por plataforma (tipicamente 1.4 GB em 64-bit). Útil para processos que manipulam grandes volumes de dados em memória.

**`--enable-source-maps`** — ativa o suporte a sourcemaps nos stack traces do Node. Quando o código foi transpilado (TypeScript, Babel), os erros mostram as linhas do código-fonte original em vez do JavaScript gerado.

**`--no-warnings`** — suprime avisos de features experimentais no stderr. Útil em ambientes de produção ou scripts onde os avisos poluem logs estruturados.

**`--heap-prof`** — habilita o profiler de heap do V8, gerando um arquivo `.heapprofile` ao final da execução. O arquivo pode ser carregado no Chrome DevTools (Memory tab) para análise de alocações.

| Flag | Substitui / complementa | Disponível desde |
|---|---|---|
| `--watch` | nodemon | Node 18.11.0 (exp), estável Node 22 |
| `--watch-path` | nodemon (padrão de diretório) | Node 22.0.0 |
| `--env-file` | dotenv | Node 20.6.0 |
| `--import` | `--require` (para ESM) + loaders manuais | Node 12.0.0 (hooks: Node 20.6.0) |
| `--inspect` | ndb, `node-inspector` (legado) | Node 6.3.0 |
| `--inspect-brk` | breakpoints externos | Node 7.6.0 |
| `--max-old-space-size` | variável `NODE_OPTIONS` com mesmo flag | Node muito antigo |
| `--enable-source-maps` | `source-map-support` (pacote npm) | Node 12.12.0 |
| `--no-warnings` | filtros manuais de stderr | Node 6.0.0 |
| `--heap-prof` | heapdump (pacote npm) | Node 12.0.0 |

## Quando usar

A escolha de qual flag ativar depende do estágio do ciclo de vida do projeto e do contexto de execução:

**Em desenvolvimento:**

- Use `--watch` para qualquer servidor ou script que precise de reload automático. Para projetos simples sem configuração complexa de diretórios, é a substituição direta do nodemon com zero dependências.
- Use `--env-file=.env` em vez de chamar `dotenv.config()` no código — isso mantém a configuração fora do código e deixa o arquivo `app.js` mais limpo.
- Use `--inspect-brk` quando precisar depurar código de inicialização ou entender o fluxo de carregamento de módulos. Use `--inspect` (sem `--brk`) quando quiser conectar o debugger depois que o servidor já está rodando.

**Em testes:**

- `node --test --watch` (combina o runner de testes com o watch mode) é suficiente para a maioria dos projetos sem configuração extra.
- `--env-file=.env.test` isola as variáveis de ambiente de teste das de desenvolvimento.

**Em produção:**

- Nunca use `--watch` — o overhead de monitoramento de arquivos é desnecessário e pode causar reinícios indesejados.
- Nunca use `--inspect` ou `--inspect-brk` — expõe uma porta de depuração que permite execução remota de código arbitrário.
- `--max-old-space-size` pode ser necessário para processos com carga de memória alta (ETL, processamento de grandes JSONs).
- `--enable-source-maps` é recomendado em produção junto com o código compilado, para que logs de erro sejam legíveis.
- `--no-warnings` pode ser usado para suprimir avisos de features estabilizadas recentemente que ainda exibem avisos em versões de transição.

**Resumo por ambiente:**

| Flag | Dev | Teste | Produção |
|---|---|---|---|
| `--watch` | Sim | Sim (com `--test`) | Nunca |
| `--env-file` | Sim | Sim | Opcional (preferir variáveis de ambiente do sistema) |
| `--import` | Sim (loaders) | Sim | Sim (se necessário) |
| `--inspect` | Sim | Ocasional | Nunca |
| `--inspect-brk` | Sim (debug profundo) | Raramente | Nunca |
| `--enable-source-maps` | Opcional (tsx faz melhor) | Opcional | Sim |
| `--max-old-space-size` | Raramente | Raramente | Conforme necessário |

## Armadilhas comuns

### Armadilha 1: --env-file não expande variáveis no estilo bash

O `--env-file` implementa um parser simples de `KEY=VALUE` — ele **não** executa expansão de variáveis do shell. Referências como `$HOME`, `${DATABASE_HOST}` ou `${PORT:-3000}` são lidas literalmente como strings, não como variáveis expandidas.

```js
// ❌ Problema: esperar expansão de variáveis no .env
// Conteúdo do .env:
// BASE_DIR=$HOME/app
// DATABASE_URL=postgres://${DB_HOST}:5432/mydb

// resultado: process.env.BASE_DIR === '$HOME/app'  (literal!)
// resultado: process.env.DATABASE_URL === 'postgres://${DB_HOST}:5432/mydb' (literal!)
console.log(process.env.BASE_DIR);      // '$HOME/app' — NÃO é /home/user/app
console.log(process.env.DATABASE_URL);  // string com ${DB_HOST} não expandido
```

```js
// ✅ Fix: compor valores dinamicamente no código
// .env deve conter apenas valores literais:
// DB_HOST=localhost
// DB_PORT=5432
// DB_NAME=mydb

// Composição no código:
const dbUrl = `postgres://${process.env.DB_HOST}:${process.env.DB_PORT}/${process.env.DB_NAME}`;

// Ou: usar dotenv + dotenv-expand se expansão for necessária:
// import 'dotenv/config';
// import 'dotenv-expand/config';
```

### Armadilha 2: --watch não detecta novos arquivos criados após a inicialização

O `--watch` registra watchers apenas para os arquivos **presentes no grafo de módulos no momento em que o processo sobe**. Se um novo arquivo for criado no disco depois que o servidor está rodando, o `--watch` não o detecta e não reinicia o processo.

```js
// ❌ Problema: novo arquivo adicionado ao projeto enquanto --watch está ativo
// routes/products.js é criado durante o desenvolvimento
// O --watch não percebe mudanças em routes/products.js
// até que o arquivo já esteja no grafo de módulos (i.e., após restart manual)
import './routes/products.js'; // este import não existia no startup original
```

```js
// ✅ Fix: usar --watch-path para monitorar diretórios inteiros (Node 22+)
// node --watch --watch-path=./routes --watch-path=./src app.js
// Qualquer mudança em ./routes/ ou ./src/ dispara restart,
// independente de o arquivo estar no grafo de módulos original

// Para Node 18/20 sem --watch-path: usar nodemon para projetos
// com estrutura de diretórios dinâmica
// npx nodemon --watch routes --watch src app.js
```

### Armadilha 3: --inspect ativo em produção expõe porta de execução remota

O servidor WebSocket do inspector permite que qualquer cliente com acesso à porta execute código arbitrário no processo Node com as mesmas permissões do processo. Deixar `--inspect` ativo em produção é uma vulnerabilidade crítica de segurança.

```js
// ❌ Problema: --inspect no processo de produção
// Dockerfile ou script de start com:
// CMD ["node", "--inspect", "app.js"]

// Resultado: porta 9229 aberta
// Qualquer pessoa com acesso à rede pode conectar ao inspector
// e executar código arbitrário com acesso total ao processo,
// variáveis de ambiente (incluindo secrets) e sistema de arquivos
```

```js
// ✅ Fix: nunca usar --inspect em produção
// Para debugging de emergência em produção, ativar via SIGUSR1:
// kill -SIGUSR1 <pid>   ← ativa o inspector em runtime
// Depois tunelar via SSH para acessar a porta localmente:
// ssh -L 9229:localhost:9229 user@servidor

// No package.json, separar claramente os scripts:
// "start": "node app.js",                    // produção: sem inspect
// "dev": "node --inspect --watch app.js",    // dev: com inspect
// "debug": "node --inspect-brk app.js"       // debug pontual
```

## Em entrevista

**Q: What is the `--watch` flag in Node.js and how does it compare to nodemon?**

The `--watch` flag, introduced as experimental in Node 18.11.0 and stabilized in Node 22, tells the runtime to monitor the files in the module graph and automatically restart the process when any of them change. It works without any configuration file or additional packages — you simply add the flag to your `node` invocation. Compared to nodemon, `--watch` is more minimal: it does not watch `node_modules` by default, it does not support the rich configuration options in `nodemon.json` (like file extension filtering or custom restart delays), and it only monitors files that were loaded during the initial startup, not newly created files. For simple servers and scripts where the file structure is stable, `--watch` is a zero-dependency replacement for nodemon; for projects with complex directory structures or dynamic file creation, nodemon or `--watch-path` (Node 22+) is still the better choice.

**Q: How does `--env-file` work and what are its limitations compared to the dotenv package?**

The `--env-file` flag, available since Node 20.6.0, reads a `.env`-formatted file and populates `process.env` with its key-value pairs before the script starts executing, without any code in the application itself. You can pass multiple `--env-file` flags to load several files in sequence. The most important behavioral difference from dotenv is that `--env-file` does not support shell variable expansion — values like `$HOME` or `${DB_HOST}` are treated as literal strings, not evaluated. Additionally, like dotenv's default behavior, `--env-file` does not override variables already present in the process environment, so system environment variables always take precedence. For production deployments, injecting secrets via system environment variables rather than `.env` files is still the recommended practice; `--env-file` is primarily a development convenience.

**Q: What is the `--import` flag and when would you use it over `--require`?**

The `--import` flag pre-loads an ES module before the main script runs, making it the ESM counterpart of the older `--require` flag which worked only with CommonJS modules. The primary use case in modern Node.js is registering custom module hooks using the `module.register()` API introduced in Node 20.6.0 — for example, to enable TypeScript support, path alias resolution, or custom loaders without modifying the application code. You would use `--import` over `--require` whenever the loader or hook is written as an ESM module, or whenever the project uses `"type": "module"` in `package.json`, because `--require` cannot load ES modules. A practical example is replacing the older `node --loader ts-node/esm` pattern with `node --import ts-node/esm` in projects migrating away from the deprecated `--loader` flag.

**Q: Why is `--inspect` dangerous in production and what is the safe alternative for emergency debugging?**

The `--inspect` flag opens a WebSocket server on port 9229 that implements the Chrome DevTools Protocol, which allows any connecting client to execute arbitrary JavaScript inside the running process with full access to memory, file system, environment variables, and network. In production, if this port is reachable, it represents a remote code execution vulnerability that bypasses all application-level authentication. The safe alternative for emergency production debugging is to send `SIGUSR1` to the running process (`kill -SIGUSR1 <pid>`), which activates the inspector at runtime only when needed, and then access it exclusively through an authenticated SSH tunnel (`ssh -L 9229:localhost:9229 user@server`) rather than exposing the port directly. This way the inspector is never persistently enabled, and access is gated by SSH authentication rather than being open by default.

## Vocabulário

| Português | Inglês |
|---|---|
| Modo de observação | Watch mode |
| Arquivo de variáveis de ambiente | Environment file / `.env` file |
| Pré-carregamento de módulo | Module preloading |
| Depurador | Debugger |
| Ponto de interrupção | Breakpoint |
| Tamanho do heap | Heap size |
| Grafo de módulos | Module graph |
| Expansão de variáveis | Variable expansion |
| Porta de depuração | Debug port |
| Túnel SSH | SSH tunnel |
| Reinicialização automática | Auto-restart / hot restart |
| Hook de módulo | Module hook / loader hook |

## Fontes

- [Node.js Docs — CLI flags reference](https://nodejs.org/api/cli.html) — referência completa de todas as flags de linha de comando, com versões e descrições
- [Node.js 18.11.0 Changelog — --watch introduced](https://nodejs.org/en/blog/release/v18.11.0) — anúncio oficial do flag `--watch` como experimental
- [Node.js 20.6.0 Changelog — --env-file introduced](https://nodejs.org/en/blog/release/v20.6.0) — anúncio do `--env-file` e do `module.register()`
- [Node.js Docs — module.register() API](https://nodejs.org/api/module.html#moduleregisterspecifier-parenturl-options) — documentação da API de registro de hooks ESM usada com `--import`
- [V8 Inspector Protocol — Chrome DevTools](https://chromedevtools.github.io/devtools-protocol/) — especificação do protocolo WebSocket que `--inspect` implementa

## Veja também

- [[Tooling e ecossistema moderno]] — índice do galho 7
- [[05 - Built-in test runner - node-test]] — nota anterior no galho
- [[07 - Single Executable Apps (SEA)]] — próxima nota no galho
- [[Node.js]] — tronco da trilha Node Senior
- [[03-Dominios/Node/index|Node.js (MOC central)]] — visão geral de todos os galhos da trilha Node Senior
