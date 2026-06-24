---
title: "O runtime como ferramenta de DX"
created: 2026-06-24
updated: 2026-06-24
type: concept
fase: adepto
status: seedling
publish: true
tags:
  - tooling
  - dx
  - node
  - tsx
  - adepto
  - entrevista
---

# O runtime como ferramenta de DX

> [!abstract] TL;DR
> Durante anos, rodar TypeScript no Node exigia uma cadeia de ferramentas fora do runtime: `ts-node` pra executar, `nodemon` pra reiniciar, `dotenv` pra carregar variáveis. Em 2026 o Node absorveu as três funções. `--watch` substitui o nodemon para a maioria dos casos; `--env-file` elimina a dependência de dotenv; e o **type stripping nativo** (padrão desde Node 23.6, estável no Node 24) deixa você rodar arquivos `.ts` diretamente — sem compilar, sem instalar nada. Entenda o que cada flag faz, o que ela **não** faz, e quando `tsx` ainda vale mais do que confiar no runtime puro.

---

## O problema que o tooling externo resolve — e resolve mal

Existe um gap entre o que você escreve e o que o Node consegue executar. O gap clássico é o TypeScript: o Node só entende JavaScript, então `.ts` precisa virar `.js` antes de rodar. Mas há outros atritos menores que somam:

- Você muda um arquivo e precisa matar e reiniciar o servidor manualmente.
- Você precisa carregar variáveis de ambiente de um `.env` sem commitar credenciais.
- Você quer rodar um script utilitário escrito em TypeScript sem criar um pipeline de build só pra isso.

A solução da comunidade foi instalar ferramentas externas pra cada um: `nodemon` pra watch, `dotenv` pra env files, `ts-node` (ou `tsx`) pra TypeScript. Funciona — mas são três dependências, três configurações e três fontes de quebra potencial.

A tendência de 2024-2026 é diferente: **o runtime absorve a responsabilidade**. Não porque as ferramentas externas eram ruins, mas porque a plataforma amadureceu o suficiente pra cobrir os 90% mais comuns sem dependência adicional.

```mermaid
timeline
    title A absorção de DX pelo Node.js
    2023 : Node 20.6.0 — --env-file (experimental)
         : Node 20.13.0 — --watch estável
    2024 : Node 22.6.0 — --experimental-strip-types
         : Node 22.7.0 — --experimental-transform-types
         : Node 22.21.0 — --env-file estável
    2025 : Node 23.6.0 — type stripping como padrão (unflagged)
         : Node 24 LTS — type stripping default, --env-file stable
    2026 : Node 24 Active LTS — stack nativo completo
         : Node 26 — --experimental-transform-types removido
```

Cada linha desse timeline representa uma dependência que você pode não precisar mais instalar.

---

## `--watch`: o nodemon que vem no box

O `nodemon` nasceu de uma dor real: toda vez que você salva um arquivo, precisa reiniciar o servidor Node manualmente. O nodemon resolveu isso monitorando o sistema de arquivos e reiniciando o processo automaticamente. Funcionou tão bem que se tornou onipresente — qualquer tutorial de Node de 2015 a 2023 começa com `npm install -g nodemon`.

A flag `--watch` do Node.js entrou em modo experimental no Node 18.11.0 e se tornou **estável no Node 20.13.0**. O princípio é idêntico ao nodemon: quando um arquivo importado pelo processo muda, o Node reinicia automaticamente.

```bash
# Antes: dependência externa, configuração separada
npm install --save-dev nodemon
# nodemon.json ou package.json "scripts": { "dev": "nodemon src/server.js" }
nodemon src/server.js

# Depois: zero dependência, zero configuração
node --watch src/server.js

# Com TypeScript (usando tsx, ver adiante):
node --watch --import tsx src/server.ts
```

O mecanismo é mais simples do que parece: o Node monitora todos os arquivos que foram `import`ados ou `require`d durante a execução. Quando qualquer um deles muda no disco, o processo é encerrado e reiniciado com os mesmos argumentos.

```mermaid
sequenceDiagram
    participant Dev as Desenvolvedor
    participant Node as node --watch
    participant FS as Sistema de Arquivos
    participant Proc as Processo

    Dev->>Node: node --watch src/server.js
    Node->>Proc: fork do processo
    Proc->>FS: importa server.js, db.js, routes.js
    Node->>FS: registra watch em server.js, db.js, routes.js

    Dev->>FS: edita routes.js
    FS-->>Node: evento de mudança em routes.js
    Node->>Proc: SIGTERM (encerra)
    Node->>Proc: fork novo processo
    Proc-->>Dev: servidor reiniciado
```

### `--watch-path`: watch sem seguir imports

Às vezes você quer observar um diretório inteiro — inclusive arquivos que o processo não importa diretamente, como templates HTML ou arquivos de configuração carregados por leitura de arquivo (`fs.readFile`). Para isso existe `--watch-path`:

```bash
# Observa o diretório src/ inteiro
node --watch-path=./src src/server.js

# Múltiplos caminhos
node --watch-path=./src --watch-path=./templates src/server.js
```

> [!warning] `--watch-path` desativa o rastreamento automático de imports
> Quando você usa `--watch-path`, o Node **para de rastrear** os módulos importados automaticamente. Você assume o controle total de quais caminhos observar. Se esquecer de listar um arquivo que muda, o processo não reinicia. É uma troca explícita: cobertura manual em vez de descoberta automática.

> [!warning] `--watch-path` só funciona em macOS e Windows
> O `--watch-path` depende de APIs de watch nativas do SO (`kqueue` no macOS, `ReadDirectoryChangesW` no Windows) e **não está disponível no Linux**. No Linux, use `--watch` sem path (rastreamento por import) ou recorra ao nodemon para casos avançados.

### O que `--watch` não faz (que o nodemon faz)

O nodemon acumulou uma década de features opcionais. O `--watch` nativo não tem:

- **Delay configurável** antes de reiniciar (debounce).
- **Extensões customizáveis** (`--ext ts,json,env`).
- **Padrões de ignore** granulares (`.gitignore`-style).
- **Execução de script de pré/pós-restart**.
- **Restart manual via `rs`** digitado no terminal.

Para scripts simples e servidores de desenvolvimento, `--watch` é suficiente. Para projetos com muitas extensões, templates ou configuração por arquivo externo, nodemon ainda é a escolha mais confortável.

---

## `--env-file`: o dotenv que vem no box

O `dotenv` foi um dos pacotes mais instalados da história do npm. Ele resolve um problema universal: você quer guardar configuração sensível (URLs de banco, secrets de API) fora do código, num arquivo `.env` que vai no `.gitignore`. O `dotenv` carregava esse arquivo e populava `process.env`.

O Node.js 20.6.0 trouxe a flag `--env-file` que faz exatamente o mesmo. O flag ficou estável em duas versões: **Node 22.21.0 e Node 24.10.0** (os dois LTS ativos em 2026).

```bash
# Antes: dependência de dotenv, require no topo do código
# require('dotenv').config()
# Ou dotenv/config no import:
node -r dotenv/config src/app.js

# Depois: flag nativa, zero dependência, zero código
node --env-file=.env src/app.js

# Múltiplos arquivos (o último tem precedência)
node --env-file=.env --env-file=.env.local src/app.js

# Variante silenciosa: não falha se o arquivo não existir
# (landed em Node 22.9.0)
node --env-file-if-exists=.env.local --env-file=.env src/app.js
```

O padrão de uso com múltiplos arquivos segue a convenção de frameworks modernos (Next.js, Vite):

```bash
# Hierarquia de precedência (mais específico sobrescreve o mais geral)
node --env-file=.env \
     --env-file=.env.local \
     --env-file=.env.development.local \
     src/app.js
```

### O que `--env-file` não faz (que o dotenv faz)

Há duas limitações importantes que fazem o `dotenv` (com `dotenv-expand`) ainda ser necessário em alguns projetos:

**1. Sem expansão de variáveis (`${VAR}`):**

```bash
# .env com expansão — funciona com dotenv-expand, FALHA com --env-file
BASE_URL=https://api.exemplo.com
API_ENDPOINT=${BASE_URL}/v1   # --env-file vai ler literalmente "${BASE_URL}/v1"
```

**2. Sem cascata de arquivos automática:**

O dotenv com `dotenv-flow` ou configurado pelo framework faz a cascata `.env` → `.env.local` → `.env.development` automaticamente. Com `--env-file`, você declara explicitamente cada arquivo na linha de comando. É mais verboso, mas mais previsível — sem "de onde veio esse valor?".

> [!tip] Regra de decisão simples
> Se o seu `.env` não usa `${VAR}` e você não precisa de cascata automática, `--env-file` é suficiente. Se você usa expansão de variáveis (comum em projetos com URLs compostas ou conexões de banco parameterizadas), mantenha `dotenv-expand`. Para scripts e utilitários, a flag nativa é sempre a escolha mais simples.

---

## Type stripping nativo: rodando TypeScript sem compilar

Esta é a mudança mais significativa dos últimos anos na DX do ecossistema Node. Entender o que ela faz — e o que ela deliberadamente não faz — é fundamental para não ser pego de surpresa.

### O que acontece quando você roda um `.ts` com Node 23.6+

A partir do Node 23.6.0, o type stripping é **ativado por padrão** para arquivos `.ts` e `.tsx`. Você não precisa de nenhuma flag:

```bash
# Node 23.6+ e Node 24+: funciona diretamente
node meu-script.ts

# Antes de 23.6: precisava de flag explícita
node --experimental-strip-types meu-script.ts
```

O mecanismo é deliberadamente simples: o Node lê o arquivo `.ts`, substitui cada anotação de tipo por **espaços em branco** (whitespace), e executa o JavaScript resultante. Por que espaços e não remoção? Para preservar os números de linha e colunas nas stack traces — um erro na linha 42 do `.ts` ainda aparece como linha 42.

```mermaid
flowchart LR
    TS["meu-script.ts\n\nfunction soma(a: number, b: number): number {\n  return a + b\n}"]
    STRIP["Type Stripper\n(whitespace replacement)"]
    JS["JavaScript resultante\n\nfunction soma(a        , b        )         {\n  return a + b\n}"]
    V8["V8 Engine"]
    RUN["Execução"]

    TS --> STRIP --> JS --> V8 --> RUN
```

O resultado é um TypeScript "sem os tipos" que o V8 executa normalmente. **Nenhum tipo é checado. Nenhum erro de tipo é reportado.** O Node não conhece nem se importa com a semântica dos tipos — eles são literalmente apagados antes do código chegar ao engine.

### O que o type stripping executa

Praticamente toda sintaxe TypeScript que é **apenas anotação** funciona:

```ts
// Tudo isso roda com node meu-arquivo.ts no Node 24:

// Tipos e interfaces (apagados completamente)
type ID = string | number;
interface Usuario {
  id: ID;
  nome: string;
}

// Anotações de tipo em variáveis, parâmetros, retorno
const id: ID = 42;
function buscarUsuario(id: ID): Promise<Usuario> {
  return fetch(`/api/users/${id}`).then(r => r.json());
}

// Generics
function identidade<T>(valor: T): T {
  return valor;
}

// Type assertions e satisfies
const config = { porta: 3000 } satisfies { porta: number };
const raw = JSON.parse(texto) as Record<string, unknown>;

// Non-null assertion
const elemento = document.getElementById("app")!;
```

### O que o type stripping NÃO consegue executar (sem flag extra)

Aqui está o ponto crítico: algumas construções TypeScript **geram código JavaScript**. Não são anotações — são sintaxe que o TypeScript inventou e que produz lógica real em runtime. O type stripping não pode simplesmente apagar essas — ele precisaria transformá-las, o que é uma operação diferente.

```ts
// FALHA com node puro (type stripping): enums geram código JavaScript
enum Direcao {
  Norte,
  Sul,
  Leste,
  Oeste
}
// TypeScript compila isso para:
// var Direcao;
// (function (Direcao) {
//   Direcao[Direcao["Norte"] = 0] = "Norte";
//   ...
// })(Direcao || (Direcao = {}));
// Isso não é uma anotação — é lógica de runtime.

// FALHA: namespaces instanciados (namespace com código)
namespace Matematica {
  export function somar(a: number, b: number) { return a + b; }
}

// FALHA: parameter properties no constructor (sintaxe TS que gera atribuição)
class Servico {
  constructor(
    private readonly db: Database,  // isso gera this.db = db no JS
    public nome: string              // isso gera this.nome = nome
  ) {}
}

// FALHA: decorators legados (experimentalDecorators: true)
// (NestJS, TypeORM, Angular pré-standalone usam isso)
@Injectable()
class MeuServico {}
```

> [!warning] O destino de `--experimental-transform-types`
> O Node 22.7 introduziu `--experimental-transform-types` para lidar com exatamente esses casos — enums, namespaces, parameter properties. O Node 26 **removeu essa flag** inteiramente. O motivo: a equipe do Node entendeu que a responsabilidade de transformar sintaxe TS complexa pertence a ferramentas dedicadas (tsx, tsc, swc), não ao runtime. Se você tem enums ou decorators legados, use `tsx` ou compile com `tsc`/`swc` antes de rodar.

```mermaid
flowchart TD
    ARQUIVO["Arquivo .ts"]
    TEM_ENUM{"Tem enum, namespace\ninstanciado, parameter\nproperties ou\ndecorators legados?"}
    SIMPLE["Só anotações de tipo\n(interfaces, generics,\nassertions, satisfies...)"]
    NODE["node arquivo.ts\n(Node 23.6+ ou 24+)\n✓ funciona"]
    PRECISA_TSX["tsx arquivo.ts\nou\ntsc + node build/arquivo.js\n✓ funciona"]

    ARQUIVO --> TEM_ENUM
    TEM_ENUM -->|não| SIMPLE --> NODE
    TEM_ENUM -->|sim| PRECISA_TSX
```

### Verificando o tipo de arquivo e `.mts`/`.cts`

O type stripping se comporta de forma diferente dependendo do contexto de módulo:

```bash
# .ts — interpretado como ESM se "type": "module" no package.json
# ou como CJS caso contrário (padrão)
node arquivo.ts

# .mts — sempre ESM (equivalente a .mjs)
node arquivo.mts

# .cts — sempre CJS (equivalente a .cjs)
node arquivo.cts
```

> [!info] TypeScript com `"type": "module"` e imports
> Se o `package.json` tem `"type": "module"`, os imports relativos em `.ts` **precisam incluir a extensão `.js`** (não `.ts`), porque é o que o TypeScript especificou como regra de resolução para ESM. Parece estranho, mas é o padrão que o Node e o tsc seguem. O tsx tem um modo que resolve isso automaticamente — mais um motivo para usá-lo quando ESM puro é crítico.

```ts
// No modo ESM nativo com TypeScript, imports ficam assim:
import { buscarUsuario } from './usuarios.js'; // .js mesmo sendo .ts no disco
```

---

## tsx: o wrapper que vai além do stripping

O `tsx` (TypeScript eXecute) é um wrapper fino em torno do **esbuild** que permite rodar TypeScript com transformação completa, não só stripping. Criado por Hiroki Osame (`@hirokiosame`), é hoje a ferramenta recomendada para rodar TypeScript em Node quando o runtime nativo não é suficiente.

```bash
# Instalação
npm install --save-dev tsx

# Uso básico
npx tsx script.ts
# ou com global install:
tsx script.ts

# Com watch (reinicio automático)
tsx watch script.ts

# Como loader do Node (--import)
node --import tsx/esm src/server.ts
```

O motivo pelo qual o tsx existe — e vai continuar existindo mesmo com o stripping nativo do Node — é a transformação completa:

| Recurso | `node` (strip) | `tsx` |
|---------|:--------------:|:-----:|
| Anotações de tipo | ✓ | ✓ |
| Enums | ✗ | ✓ |
| Namespaces instanciados | ✗ | ✓ |
| Parameter properties | ✗ | ✓ |
| Decorators (legacy e TC39) | ✗* | ✓ |
| JSX/TSX | ✗ | ✓ |
| Transpilação de target (downlevel) | ✗ | ✓ |
| Path aliases (`tsconfig.paths`) | ✗ | ✓ |
| Checagem de tipos | ✗ | ✗ |

*Node 26 removeu `--experimental-transform-types`; decorators TC39 Stage 3 funcionavam antes disso.

O tsx não checa tipos — essa responsabilidade fica com `tsc --noEmit`, rodado separadamente (em CI, em pre-commit, ou no editor). O tsx só transforma e executa. Esse design intencional o torna 25× mais rápido que o `ts-node` clássico no startup.

### tsx vs ts-node: o estado em 2026

O `ts-node` foi por anos a única opção séria para rodar TypeScript no Node. Hoje está em declínio:

```mermaid
graph LR
    subgraph "Era ts-node (2016–2023)"
        TSN["ts-node\n• Roda tsc internamente\n• Startup ~500ms\n• ESM: historicamente difícil\n• 8M downloads/semana\n  (legado + inércia)"]
    end

    subgraph "Era tsx (2022–hoje)"
        TSX["tsx\n• Wrapper esbuild\n• Startup ~20ms\n• ESM: suporte nativo\n• Drop-in replacement\n  para ts-node\n• Recomendado em 2026"]
    end

    subgraph "Node nativo (2023–hoje)"
        NODE["node --strip-types\n• Zero dependência\n• Startup igual ao JS\n• Só anotações (sem enums)\n• Default Node 23.6+/24"]
    end

    TSN -->|"substituído por"| TSX
    TSN -->|"casos simples"| NODE
    TSX -->|"casos simples"| NODE
```

O ts-node ainda tem ~8 milhões de downloads semanais — mas esse número reflete inércia e ferramentas existentes que dependem dele (jest com ts-jest, frameworks mais antigos), não projetos novos. Para novos projetos, a recomendação em 2026 é clara: não use ts-node.

---

## Rodando um script TypeScript de 3 formas: o exemplo real

Imagine um script utilitário que migra dados de banco — uma tarefa pontual que você quer rodar em desenvolvimento sem criar um pipeline de build:

```ts
// scripts/migrar-usuarios.ts
import { readFileSync } from 'fs';
import { Pool } from 'pg';

enum StatusMigracao {
  Pendente = 'pendente',
  Concluido = 'concluido',
  Erro = 'erro',
}

interface UsuarioLegado {
  id: number;
  email: string;
  nome_completo: string;
}

async function migrar(): Promise<void> {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });
  const dados = JSON.parse(
    readFileSync('./dados/usuarios-legados.json', 'utf-8')
  ) as UsuarioLegado[];

  let status: StatusMigracao = StatusMigracao.Pendente;

  for (const usuario of dados) {
    try {
      await pool.query(
        'INSERT INTO usuarios (email, nome) VALUES ($1, $2) ON CONFLICT DO NOTHING',
        [usuario.email, usuario.nome_completo]
      );
    } catch (err) {
      status = StatusMigracao.Erro;
      console.error(`Falha ao migrar ${usuario.email}:`, err);
    }
  }

  status = StatusMigracao.Concluido;
  console.log(`Migração: ${status}`);
  await pool.end();
}

migrar();
```

**Forma 1: `tsx` (recomendado — suporta enum)**

```bash
npx tsx --env-file=.env scripts/migrar-usuarios.ts
```

Funciona completamente. O enum `StatusMigracao` é transformado pelo esbuild antes de chegar ao Node. O `--env-file` carrega o `DATABASE_URL`. Startup em ~20ms.

**Forma 2: `node` nativo (falha com enum)**

```bash
node --env-file=.env scripts/migrar-usuarios.ts
# SyntaxError: The requested module does not provide an export named 'StatusMigracao'
# (ou similar — o enum gera código, não pode ser stripped)
```

Se você remover o enum do script (substituindo por um objeto constante ou um tipo union), aí funciona:

```ts
// Sem enum — compatível com node nativo
const STATUS_MIGRACAO = {
  Pendente: 'pendente',
  Concluido: 'concluido',
  Erro: 'erro',
} as const;
type StatusMigracao = typeof STATUS_MIGRACAO[keyof typeof STATUS_MIGRACAO];
```

**Forma 3: `ts-node` (funciona, mas lento)**

```bash
npx ts-node --require dotenv/config scripts/migrar-usuarios.ts
# Funciona, mas: startup ~500ms, requer dotenv manual, mais config
```

Roda, mas é 25× mais lento no startup e exige mais boilerplate. Para um script pontual não é catastrófico, mas para um servidor dev que reinicia dezenas de vezes por hora, a diferença acumula.

```mermaid
graph TD
    SCRIPT["Script TypeScript\ntem enum, JSX ou\ndecorators?"]
    ENUM_SIM["tsx\nnpx tsx script.ts\n✓ Transforma tudo\n✓ ESM/CJS\n~20ms startup"]
    ENUM_NAO{"Só interfaces,\ntypes, generics?"}
    NODE_NAO["node nativo\nnode script.ts\n✓ Zero dependência\n✓ Startup nativo\nNode 23.6+ / 24"]
    TSNODE["ts-node\n(apenas legado)\nnpx ts-node script.ts\n⚠ 500ms startup\n⚠ ESM difícil"]

    SCRIPT -->|sim| ENUM_SIM
    SCRIPT -->|não| ENUM_NAO
    ENUM_NAO -->|sim| NODE_NAO
    ENUM_NAO -->|não certeza| ENUM_SIM
    ENUM_NAO -->|legado forçado| TSNODE
```

---

## A tendência: "menos tooling, mais runtime"

O que aconteceu com `--watch`, `--env-file` e type stripping é parte de uma tendência maior. O Deno e o Bun apontaram o caminho: runtimes com TypeScript nativo, env files embutidos, test runner integrado. O Node.js está respondendo.

```mermaid
flowchart LR
    subgraph "2018 — Dependências externas pra tudo"
        N1["nodemon\n+ ts-node\n+ dotenv\n+ jest\n+ babel-node"]
    end

    subgraph "2026 — Nativo onde possível"
        N2["node --watch\n+ node --env-file\n+ node (strip-types)\n+ node:test\n+ tsx (quando precisa de mais)"]
    end

    N1 -->|"absorção gradual"| N2
```

A pergunta que vale fazer antes de instalar qualquer ferramenta de dev é: **o Node já faz isso?** Frequentemente a resposta mudou de "não" para "sim" nos últimos dois anos.

Isso não significa que ferramentas externas vão desaparecer. O tsx ainda tem razão de existir para enums e transformações complexas. O nodemon ainda ganha em projetos com configuração avançada de watch. O dotenv ainda é necessário quando você precisa de expansão de variáveis. A diferença é que o caso de uso simples — o mais comum — agora tem resposta nativa.

---

## Como explicar em inglês

> "Node.js has been quietly absorbing DX responsibilities that used to require external tools. In 2026, three things stand out.
>
> First, **`--watch`** replaced nodemon for most use cases. Stable since Node 20.13, it monitors all imported files and restarts the process automatically when any of them changes. It's simpler than nodemon but lacks advanced configuration — no debounce, no glob ignores, no manual restart command. For a dev server, it's usually enough.
>
> Second, **`--env-file`** replaced dotenv for simple cases. Stable in Node 22.21 and 24.10, it loads a `.env` file and populates `process.env` with zero dependencies. The caveat: no variable expansion — `${VAR}` references aren't resolved. If you need that, dotenv-expand is still the answer.
>
> Third, and most interesting, **native type stripping**. Since Node 23.6, type annotations are stripped by default when you run a `.ts` file — no compilation step, no extra flags. But this only works for erasable syntax: interfaces, type aliases, generics, assertions. Enums, namespaces with code, and parameter properties in constructors generate actual JavaScript and can't be stripped. For those, `tsx` — which wraps esbuild — is the right tool.
>
> The practical rule in 2026: start with native Node flags. If you hit an enum or decorator, reach for `tsx`. Avoid `ts-node` on new projects — it's 25x slower at startup, ESM support is painful, and `tsx` is a drop-in replacement."

### Vocabulário-chave

| Português | English |
|-----------|---------|
| Experiência do desenvolvedor | Developer Experience (DX) |
| Reinicialização automática | Auto-restart / hot reload |
| Apagamento de tipos | Type stripping |
| Ferramenta de sintaxe TypeScript que gera código | TypeScript syntax that emits JavaScript |
| Variáveis de ambiente | Environment variables |
| Expansão de variáveis | Variable expansion / variable interpolation |
| Wrapper em torno de esbuild | esbuild wrapper |
| Inicialização do processo | Process startup |
| Tempo de startup | Startup time / cold start |
| Verificação de tipos (separada) | Type checking (separate pass) |
| Arquivo de ambiente | Environment file / `.env` file |
| Recurso apagável (TypeScript) | Erasable syntax |
| Recurso gerador de código | Code-emitting syntax |

---

## Armadilhas comuns

> [!bug] Enums quebrando silenciosamente com node nativo
> O erro mais frequente ao migrar de tsx para node nativo: o script tem um enum TS e o Node 24 lança `SyntaxError` ou comportamento estranho. O type stripping não pode lidar com enums porque eles geram código JavaScript (o pattern `(function(Enum) { ... })(Enum || (Enum = {}))`). Solução: substituir enums por `const` objects com `as const` ou manter `tsx` pra esse arquivo.

> [!bug] `--watch-path` não funciona no Linux
> O `--watch-path` depende de APIs nativas de macOS e Windows. No Linux, usar `--watch-path` silenciosamente não faz nada ou lança erro dependendo da versão. Se o CI roda Linux, teste a flag lá antes de assumir que funciona. Alternativa: `--watch` puro (rastreia imports automaticamente) ou nodemon.

> [!bug] `--env-file` com `${VAR}` não faz o esperado
> Um `.env` herdado de um projeto que usava `dotenv-expand` pode ter referências como `API_URL=${BASE_URL}/v1`. O `--env-file` nativo lê isso **literalmente** — o valor de `API_URL` será a string `"${BASE_URL}/v1"`, não a URL expandida. O bug é silencioso: `process.env.API_URL` tem um valor, mas é o errado. Audite o `.env` antes de trocar dotenv por `--env-file`.

> [!bug] tsx não checa tipos — e isso pode enganar
> `tsx script.ts` executa mesmo com erros de tipo graves. Um `string` passado como `number` não gera erro em runtime se o JavaScript subjacente funcionar (e muitas vezes funciona, por coerção). Projetos que trocaram `ts-node` por `tsx` sem adicionar `tsc --noEmit` no CI ficaram sem checagem de tipos. Adicione `tsc --noEmit` como passo separado em CI ou em pre-push hook.

> [!bug] Imports com extensão `.js` no ESM + TypeScript
> No modo ESM com TypeScript, o padrão exige que imports relativos usem `.js` mesmo quando o arquivo no disco é `.ts`. Isso pega muita gente:
> ```ts
> import { algo } from './utils'; // ✗ — Node ESM não resolve sem extensão
> import { algo } from './utils.js'; // ✓ — correto (mesmo que o arquivo seja utils.ts)
> ```
> O tsx resolve isso automaticamente via path rewriting; o node nativo não. Com `tsc`, a config `"moduleResolution": "bundler"` ou `"node16"` aplica a regra correta.

> [!bug] `ts-node` e ESM: dor histórica
> Se você está mantendo um projeto que usa `ts-node` com `"type": "module"`, provavelmente já encontrou o labirinto de `esm: true` no `tsconfig`, `--esm` na linha de comando, e arquivos `.mts`. O ts-node nunca resolveu ESM de forma limpa. A migração para tsx leva geralmente 5 minutos e resolve todos esses problemas de uma vez.

---

## Veja também

- [[04 - Gerenciando versões de Node]] — como garantir que todos usam o Node 23.6+ ou 24 onde type stripping está disponível; versão como contrato de equipe.
- [[08 - Transpilação e targets]] — quando o stripping não é suficiente e você precisa de transformação real: downleveling, polyfills, targets de browser; o papel do esbuild, swc e tsc.
- [[20 - Bun como runtime e toolkit all-in-one]] — o runtime alternativo que tem TypeScript nativo, env files, watch mode e test runner desde o dia 1; como o Bun influenciou o Node a absorver essas features.
- [[03-Dominios/Tecnologia/Node/index|Node]] — runtime, event loop, APIs nativas: o que muda entre versões e por que a versão do Node importa pra DX.
- [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]] — a linguagem que gerou a necessidade de type stripping; enums, decorators e o que o TypeScript compila vs o que é apenas anotação.
