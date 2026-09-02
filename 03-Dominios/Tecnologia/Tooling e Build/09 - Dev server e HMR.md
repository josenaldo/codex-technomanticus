---
title: "Dev server e HMR"
created: 2026-06-24
updated: 2026-06-25
type: concept
fase: iniciado
status: seedling
publish: true
tags:
  - tooling
  - dev-server
  - hmr
  - iniciado
  - entrevista
---

# Dev server e HMR

> [!abstract] TL;DR
> Dev e prod são **ambientes com objetivos opostos**: dev otimiza velocidade de feedback (você quer ver a mudança em milissegundos), prod otimiza tamanho e performance de download (você quer o menor bundle possível para o usuário). O Vite resolve essa tensão usando **motores diferentes para cada ambiente**: em dev, serve ESM nativo diretamente ao browser, convertendo deps CJS com Rolldown sob demanda — sem bundlar nada da sua aplicação; em build, o Rolldown (engine Rust, GA em 2026 com o Vite 8) produz um bundle otimizado. O **HMR (Hot Module Replacement)** é o mecanismo que faz mudanças aparecerem no browser sem reload — preservando estado de componentes — via WebSocket + grafo de módulos. **Source maps** fecham o ciclo: traduzem o JS transformado de volta ao seu código original no debugger. Entender esse modelo é o que diferencia um dev que "usa o Vite" de um que "entende o Vite".

---

## Por que dev e prod são ambientes fundamentalmente diferentes

Quando você escreve código, você está num loop de feedback. Você muda um arquivo, quer ver o resultado, corrige, muda de novo. A cadência é de segundos. Se o tooling demorar dez segundos a cada mudança, você perde o fio do raciocínio, abre outra aba, perde contexto. A latência do tooling afeta diretamente a qualidade do pensamento.

Em produção, o cenário é invertido. Seu usuário vai baixar o bundle uma vez e rodar muitas vezes. Cada kilobyte a mais no bundle é carregado novamente por todos que visitarem o site. O que importa é o tamanho final, a compatibilidade com browsers antigos, a separação de chunks para carregamento lazy. A velocidade de build no CI pode demorar minutos — isso é aceitável porque acontece uma vez, não a cada keypress.

Essa oposição de objetivos significa que **a estratégia certa para dev é ruim para prod, e vice-versa**.

```mermaid
graph LR
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    classDef falha fill:#FF6B6B24,stroke:#FF6B6B,color:#E9ECF2
    subgraph DEV["Ambiente de desenvolvimento"]
        D1["Objetivo: velocidade de feedback\n(ms por mudança)"]
        D2["Aceita: bundle grande, source maps inline,\nnão-minificado, sem tree-shaking"]
        D3["Estratégia: serve sob demanda,\ntransforma só o que mudou"]
        D1 --> D2 --> D3
    end

    subgraph PROD["Ambiente de produção"]
        P1["Objetivo: bundle mínimo\n(KB importam para o usuário)"]
        P2["Aceita: build mais lento, minificação,\ntree-shaking agressivo, chunks"]
        P3["Estratégia: analisa o grafo completo,\notimiza globalmente"]
        P1 --> P2 --> P3
    end

    class DEV neutro
    class PROD falha
```

> [!info] Leitura do diagrama
> As duas colunas não são o mesmo processo em velocidades diferentes — são estratégias arquiteturalmente distintas. Dev sacrifica tamanho e compatibilidade para ter velocidade de feedback. Prod sacrifica velocidade de build para ter performance em runtime. Tentar usar a mesma estratégia nos dois ambientes é o motivo pelo qual webpack ficou lento conforme as aplicações cresceram.

O webpack (e antes dele, o Browserify) tomou uma decisão que fazia sentido em 2012: bundlar tudo em um único arquivo. Browsers não entendiam módulos. Cada `require()` precisava ser resolvido estaticamente e embutido no bundle. O servidor de dev era um processo de build completo a cada mudança. Funcionava — mas à medida que os projetos cresceram para centenas de módulos, o cold start passou de segundos para dezenas de segundos.

**O que é um bundle?** Imagine que você tem cem arquivos `.js` — componentes, utilitários, bibliotecas. O browser, em 2012, não sabia carregar um arquivo e seguir seus `import`s para buscar os outros. A solução foi um passo de build que lê todos esses arquivos, resolve as dependências entre eles, e os concatena em um único arquivo — o **bundle**. O browser baixa um arquivo, tem tudo. **Bundlar** é executar esse processo. O problema: bundlar duzentos arquivos leva mais tempo que bundlar vinte — o tempo de build cresce com o projeto. E a cada mudança no dev, o bundle inteiro precisa ser reconstruído.

O Vite foi criado em 2021 por Evan You (criador do Vue) com uma observação simples: **browsers modernos já entendem ESM nativamente**. Se o browser consegue carregar `import { foo } from './utils.js'` diretamente, por que bundlar tudo durante o desenvolvimento? A resposta foi: não precisa.

---

## O modelo do Vite em dev: ESM sob demanda

O dev server do Vite não é um processo de build. É um **servidor HTTP especializado** que transforma arquivos conforme eles são requisitados pelo browser. A diferença é conceitual e tem consequências práticas enormes.

```mermaid
sequenceDiagram
    participant Browser
    participant ViteServer as Vite Dev Server
    participant FS as Sistema de Arquivos

    Browser->>ViteServer: GET /index.html
    ViteServer->>FS: lê index.html
    ViteServer-->>Browser: index.html (injeta /@vite/client)

    Browser->>ViteServer: GET /src/main.ts
    ViteServer->>FS: lê main.ts
    ViteServer->>ViteServer: transforma: TS→JS, injeta import.meta.hot
    ViteServer-->>Browser: main.js (ESM)

    Browser->>ViteServer: GET /src/components/Button.tsx
    ViteServer->>FS: lê Button.tsx
    ViteServer->>ViteServer: transforma: TSX→JS, injeta HMR
    ViteServer-->>Browser: Button.js (ESM)

    Note over Browser,ViteServer: Módulos de /node_modules já estão\npré-bundlados em /.vite/deps/
```

> [!info] Leitura do diagrama
> O browser faz requests HTTP normais para cada módulo da sua aplicação. O Vite intercepta cada request, lê o arquivo, transforma (TS→JS, JSX→JS, etc.) e responde. Não há bundle sendo construído em background — cada arquivo é processado na hora em que o browser pede.

Esse modelo tem uma propriedade fundamental: **o tempo de cold start não cresce com o tamanho da aplicação**. Com webpack, bundlar 500 módulos demora mais que bundlar 100. Com o Vite, o servidor inicia em menos de um segundo independentemente do tamanho — porque não está processando nada até o browser pedir.

### O problema das dependências: pré-bundling com Rolldown

Porém, tem um problema. A maioria das bibliotecas do npm foi publicada como CommonJS (`module.exports = ...`), não como ESM. E mesmo as que são ESM, como o lodash-es, podem ter centenas de arquivos internos — o que significa centenas de requests HTTP separados apenas para carregar uma biblioteca.

**CommonJS vs ESM — por que dois sistemas?** O JavaScript não tinha sistema de módulos nativo até o ES2015 (ES6). O Node.js, criado em 2009, precisava de uma forma de carregar arquivos, então inventou o **CommonJS**: `require()` para importar, `module.exports = ...` para exportar. Isso funcionava no Node, mas o browser nunca entendeu `require()` — por isso os bundlers precisavam resolver tudo estaticamente. O **ESM** (ECMAScript Modules) é o padrão oficial da linguagem, com a sintaxe `import`/`export` que você conhece. Browsers modernos (Chrome, Firefox, Safari) entendem ESM nativamente desde 2018. O npm acumulou uma dívida histórica: millions de pacotes publicados antes do ES2015 usam CommonJS, porque era o único padrão disponível. Quando o Vite faz pré-bundling, uma das suas tarefas centrais é converter esses pacotes CommonJS para ESM, para que o browser possa carregá-los diretamente.

O Vite resolve isso com o **pré-bundling de dependências**: antes de iniciar o servidor, ele analisa quais pacotes você usa, converte cada um para um único arquivo ESM, e armazena em `.vite/deps/`. Isso acontece uma vez, na primeira inicialização (ou quando o `package.json` muda).

```mermaid
flowchart TD
    classDef ok fill:#4ADE8021,stroke:#4ADE80,color:#E9ECF2
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    START["vite dev\n(primeira vez)"]
    CRAWL["Rolldown varre seu código\n(descoberta de imports bare)"]
    PREBUNDLE["Pré-bundling de deps\nRolldown converte CJS→ESM\nagrupa arquivos internos"]
    CACHE[".vite/deps/\n(cache persistente)"]
    SERVER["Servidor HTTP iniciado\n(< 1s)"]

    CHANGE["node_modules muda?"]
    REBUILD["Rolldown repré-bundla"]

    START --> CRAWL --> PREBUNDLE --> CACHE --> SERVER
    CHANGE -->|sim| REBUILD --> CACHE
    CHANGE -->|não| SERVER

    class CACHE ok
    class SERVER neutro
```

> [!info] Leitura do diagrama
> O pré-bundling acontece uma vez no cold start e é cacheado. Seu próprio código da aplicação nunca é pré-bundlado — é servido diretamente como ESM. Apenas as dependências do `node_modules` passam por esse processo.

> [!note] Vite 7 vs Vite 8: a troca de motor
> Nas versões do Vite até a 7, o pré-bundling de dependências era feito com **esbuild** (bundler em Go, extremamente rápido). Com o Vite 8 (lançado em março de 2026), o motor mudou para **Rolldown** — um bundler escrito em Rust, desenvolvido pela VoidZero. A troca traz 10–30x de speedup nos builds de produção e uma arquitetura unificada: o mesmo motor serve tanto o pré-bundling em dev quanto o build de produção. A **nota [[07 - O grafo de módulos e o que é bundling]]** entra em mais detalhes sobre o grafo de dependências.

O resultado para o usuário é transparente: você importa `import { useState } from 'react'` e o browser recebe um único arquivo `.vite/deps/react.js` em vez de dezenas de módulos internos do React.

---

## HMR: Hot Module Replacement

Live reload é simples: quando um arquivo muda, o servidor avisa o browser e o browser faz um reload completo. Funciona, mas você perde todo o estado — o formulário que o usuário estava preenchendo, a posição do scroll, o estado de autenticação em memória. Para ciclos de desenvolvimento rápidos, isso é insuportável.

**HMR (Hot Module Replacement)** resolve isso: quando um arquivo muda, **apenas aquele módulo é substituído na memória**, sem recarregar a página. O estado dos módulos não afetados é preservado.

### O ciclo de uma atualização HMR

```mermaid
sequenceDiagram
    participant Dev as Você (editor)
    participant Watcher as File Watcher
    participant ViteServer as Vite Server
    participant WS as WebSocket
    participant Client as HMR Client (browser)
    participant App as Aplicação rodando

    Dev->>Watcher: salva Button.tsx
    Watcher->>ViteServer: file change event
    ViteServer->>ViteServer: invalida Button no grafo de módulos
    ViteServer->>ViteServer: propaga invalidação para importadores
    ViteServer->>WS: envia HMR payload (tipo + módulo afetado)
    WS->>Client: mensagem WebSocket
    Client->>ViteServer: GET /src/components/Button.tsx?t=1234
    ViteServer-->>Client: Button.js transformado (versão nova)
    Client->>App: substitui módulo Button na memória
    App->>App: re-renderiza componentes afetados
    Note over App: Estado de outros módulos\npreservado intacto
```

> [!info] Leitura do diagrama
> O caminho crítico é: mudança no disco → file watcher → invalidação no grafo → WebSocket → browser busca apenas o módulo mudado → substitui na memória. A página não recarrega. O estado dos outros módulos (formulários preenchidos, autenticação, variáveis em memória) sobrevive.

### Por que o Vite é mais rápido que o webpack no HMR

Com o webpack, HMR significa: re-bundlar o chunk que contém o módulo modificado, mais todas as suas dependências internas. Quanto maior o chunk, mais lento. Em apps grandes, um HMR podia demorar 3–10 segundos.

Com o Vite, o browser só precisa buscar **um único arquivo** — o módulo que mudou. Sem re-bundling. Sem re-processamento de dependências. O único trabalho é transformar aquele arquivo e enviar. Isso leva dezenas de milissegundos independentemente do tamanho da aplicação.

```mermaid
graph LR
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    classDef ok fill:#4ADE8021,stroke:#4ADE80,color:#E9ECF2
    subgraph WEBPACK["HMR no webpack"]
        W1["Arquivo muda"]
        W2["Re-bundla chunk\n(arquivo + dependências)"]
        W3["Envia bundle atualizado\n(pode ser 100KB+)"]
        W4["Browser substitui módulo"]
        W1 --> W2 --> W3 --> W4
    end

    subgraph VITE["HMR no Vite"]
        V1["Arquivo muda"]
        V2["Transforma só\no módulo mudado"]
        V3["Browser faz GET\nnesse módulo (1 arquivo)"]
        V4["Browser substitui módulo"]
        V1 --> V2 --> V3 --> V4
    end

    class WEBPACK destaque
    class VITE ok
```

### A HMR API: `import.meta.hot`

O HMR automático funciona para a maioria dos casos — frameworks como Vue e React (via plugins do Vite) já sabem como substituir componentes sem perder estado. Mas quando você quer controle explícito, existe a **HMR API** exposta em `import.meta.hot`.

```ts
// Módulo que quer aceitar suas próprias atualizações
if (import.meta.hot) {
  // import.meta.hot só existe em dev — em prod é undefined (tree-shaken)

  // 1. accept(): este módulo sabe se atualizar sozinho
  import.meta.hot.accept((newModule) => {
    // newModule é o módulo recém-carregado
    // aqui você decide o que fazer com a nova versão
    console.log('Módulo atualizado:', newModule)
  })

  // 2. dispose(): limpeza ANTES de ser substituído
  // Essencial para setInterval, event listeners, conexões WebSocket
  import.meta.hot.dispose((data) => {
    clearInterval(myInterval) // evita memory leaks ao re-substituir
    data.count = currentCount  // passa estado para o próximo hot update
  })

  // 3. accept() com dependências: aceita atualizações de outros módulos
  import.meta.hot.accept(['./dep1.ts', './dep2.ts'], ([newDep1, newDep2]) => {
    // chamado quando dep1 ou dep2 mudar
  })

  // 4. invalidate(): sinaliza que este módulo não consegue se atualizar
  // força o Vite a propagar a invalidação para os importadores
  import.meta.hot.invalidate('módulo não sabe se recuperar desse estado')
}
```

> [!tip] O guard `if (import.meta.hot)`
> Sempre envolva o código HMR nesse guard. Em produção, `import.meta.hot` é `undefined` e o Vite remove o bloco inteiro via tree-shaking (dead code elimination). Se você não usar o guard, o código HMR vai parar em produção e quebrar.

A maioria dos desenvolvedores nunca escreve `import.meta.hot` diretamente — frameworks fazem isso nos plugins (o `@vitejs/plugin-react` injeta HMR para componentes React automaticamente). Mas entender a API explica por que o HMR **preserva estado**: é porque os módulos declaram o que sabem fazer durante uma atualização. Se um componente React tiver Fast Refresh habilitado, o plugin sabe re-renderizar sem desmontar — o estado do hook (`useState`) sobrevive.

> [!question] Mas o que acontece quando o HMR não consegue atualizar?
> Se o grafo de invalidação chega até um módulo que não aceitou HMR (não tem `import.meta.hot.accept`), o Vite faz um **full reload** automático. Você vê no terminal: `page reload src/main.ts`. É o fallback seguro. Em projetos bem configurados (com plugins de framework), isso raramente acontece para mudanças em componentes — apenas para mudanças em arquivos de configuração ou de bootstrapping da aplicação.

### HMR boundaries: onde a propagação para

Quando você salva um arquivo, o Vite precisa responder a uma pergunta: "quem mais precisa saber que este módulo mudou?" Ele faz isso percorrendo o grafo de importações para cima (dos importados para os importadores) até encontrar um **HMR boundary** — um módulo que declarou `import.meta.hot.accept()`, dizendo "eu sei me atualizar".

```mermaid
graph TD
    classDef ok fill:#4ADE8021,stroke:#4ADE80,color:#E9ECF2
    A["App.tsx\n(não tem accept())"]
    B["Layout.tsx\n(não tem accept())"]
    C["Counter.tsx\n✓ self-accepting\n(plugin React injetou accept())"]
    D["utils.ts\n(sem accept())"]

    A --> B
    B --> C
    C --> D

    class C ok
```

> [!info] Leitura do diagrama
> Se `utils.ts` mudar, o Vite percorre para cima: `Counter.tsx` tem `accept()` → propagação para aqui. O `Layout.tsx` e o `App.tsx` nunca ficam sabendo. Se `Layout.tsx` mudar, o Vite sobe até `App.tsx` — e `App.tsx` não tem `accept()`, então faz full reload.

A estrutura interna do Vite define uma interface `PropagationBoundary` com três campos: `boundary` (o nó do grafo que aceitou), `acceptedVia` (o módulo que acionou a atualização) e `isWithinCircularImport` (se o caminho cruzou uma importação circular). Quando há importação circular no grafo, o Vite marca isso e usa heurísticas conservadoras — geralmente preferindo full reload para evitar estado inconsistente.

**O que é uma importação circular?** É quando dois módulos importam um do outro — formando um ciclo: `A.ts` importa de `B.ts`, e `B.ts` importa de `A.ts`. Em tempo de execução, isso cria um problema de ordem de inicialização: para executar `A`, o motor precisa de `B`; mas para executar `B`, precisa de `A`. JavaScript resolve isso com um mecanismo de referências "ao vivo" — cada módulo recebe uma referência para o outro antes de qualquer um terminar de executar, então alguns valores ficam `undefined` momentaneamente. Para o HMR, isso é especialmente problemático: quando o Vite propaga uma invalidação num grafo com ciclos, ele pode passar pelo mesmo nó mais de uma vez e entrar em loop, ou invalidar módulos na ordem errada, deixando o estado do aplicativo inconsistente. Por isso o Vite prefere o fallback seguro: full reload, garantindo que o ciclo seja "quebrado" do zero.

> [!warning] O módulo que não tem `accept()` bloqueia o HMR
> Se a propagação chegar a um módulo que não declarou `accept()` e não há nenhum ancestral que aceite, o Vite cai no full reload. Você vê no terminal: `[vite] page reload src/main.ts`. A solução típica é garantir que os módulos de entrada (entry points) — aqueles que o browser carrega primeiro — estejam fora do grafo de invalidação, ou que os componentes de framework sejam self-accepting via plugin.

### React Fast Refresh: as regras de preservação de estado

O `@vitejs/plugin-react` usa a biblioteca **React Fast Refresh** (originalmente desenvolvida pela equipe do React Native, depois adotada em React DOM). O plugin injeta automaticamente `import.meta.hot.accept()` em cada componente — mas com regras específicas sobre quando o estado é preservado e quando é descartado.

**Quando o estado É preservado:**
- `useState` e `useRef` mantêm seus valores anteriores, desde que a ordem dos hooks não mude.
- Adicionar, remover ou editar o corpo de um componente funcional — sem mudar os hooks.

**Quando o estado É descartado (remount completo):**
- A ordem das chamadas de hook muda (ex: você adiciona um hook no meio da lista).
- O arquivo exporta algo além de componentes React (ex: uma constante ou função utilitária). Se o módulo mistura exportações React e não-React, o Fast Refresh não consegue identificar o boundary com segurança e força reload.
- Componentes de classe (`class MyComp extends Component`) — Fast Refresh só preserva estado em componentes funcionais.

```ts
// ✗ PROBLEMA: arquivo misturando componente e exportação não-React
export function Button() { return <button /> }
export const MAX_RETRIES = 3  // isso impede preservação de estado!

// ✓ SOLUÇÃO: separar em dois arquivos
// constants.ts → export const MAX_RETRIES = 3
// Button.tsx   → export function Button() { return <button /> }
```

> [!tip] O pragma `@refresh reset`
> Você pode forçar um remount completo a cada edição adicionando `// @refresh reset` em qualquer lugar do arquivo. Útil para componentes que dependem de estado inicial não reproduzível — por exemplo, animações de entrada que você quer ver do zero a cada mudança.

**O comportamento especial de `useEffect`:** hooks com dependências como `useEffect`, `useMemo` e `useCallback` **sempre re-executam** durante um Fast Refresh — mesmo que o array de dependências seja `[]`. Isso é intencional: garante que efeitos colaterais sejam "re-sincronizados" após uma atualização. Se você tem um `useEffect(() => { fetchData() }, [])` e salva o arquivo, o fetch vai rodar de novo.

### Comunicação bidirecional: `import.meta.hot.send()`

A nota mencionou WebSocket como canal de comunicação, mas omitiu a direção inversa: o **browser pode enviar eventos para o servidor Vite**, não só receber. Isso habilita fluxos avançados de dev tooling:

```ts
if (import.meta.hot) {
  // Enviar evento customizado do browser para o servidor
  import.meta.hot.send('meu-plugin:evento', { dados: 'payload' })

  // Receber resposta do servidor
  import.meta.hot.on('meu-plugin:resposta', (data) => {
    console.log('Servidor respondeu:', data)
  })
}
```

No lado do servidor (plugin Vite):
```ts
// vite plugin — servidor escuta eventos do browser
export function meuPlugin(): Plugin {
  return {
    name: 'meu-plugin',
    configureServer(server) {
      server.hot.on('meu-plugin:evento', (data, client) => {
        // data: payload enviado pelo browser
        // client: o cliente WebSocket específico
        client.send('meu-plugin:resposta', { ok: true })
      })
    }
  }
}
```

> [!info] Por que WebSocket e não SSE (Server-Sent Events)?
> SSE (Server-Sent Events) é unidirecional: só o servidor envia, o cliente só recebe. Para HMR simples (servidor avisa browser de mudança) isso bastaria. Mas o Vite usa WebSocket porque precisa de comunicação bidirecional: o browser envia eventos customizados de volta para o servidor via `import.meta.hot.send()`. Plugins de dev tools, como visualizadores de roteamento e inspecionadores de estado, dependem dessa capacidade. O protocolo real é um WebSocket na mesma porta do dev server (configurável em `server.ws`).

### HMR events: o que o browser pode ouvir

Além de `import.meta.hot`, a aplicação pode escutar eventos globais de HMR para reagir ao ciclo de atualização:

```ts
// Eventos globais do ciclo HMR — úteis para logging, analytics de dev
if (import.meta.hot) {
  import.meta.hot.on('vite:beforeUpdate', (payload) => {
    console.log('HMR: atualização chegando', payload.type)
  })

  import.meta.hot.on('vite:afterUpdate', () => {
    console.log('HMR: atualização aplicada')
  })

  import.meta.hot.on('vite:beforeFullReload', () => {
    console.log('HMR: não foi possível hot update, recarregando página')
  })

  import.meta.hot.on('vite:error', (payload) => {
    console.error('HMR: erro no servidor', payload.err)
  })
}
```

---

## Source maps: debugando o código que você não escreveu

O browser está rodando JavaScript transformado. Seu TypeScript com JSX virou JavaScript sem tipos, sem JSX, talvez minificado, com nomes de variáveis encurtados. Quando o debugger para numa exceção, a linha que ele aponta é no arquivo transformado — não no seu source.

**Source maps** são arquivos de mapeamento que dizem ao browser: "a linha 12, coluna 4 do arquivo transformado corresponde à linha 45, coluna 8 do arquivo original `src/components/Button.tsx`". Com isso, o DevTools mostra seu código original, com nomes de variáveis originais, breakpoints nas linhas certas.

### A anatomia de um source map

Um source map é um arquivo `.js.map` (JSON) referenciado pelo arquivo transformado:

```js
// Button.js (arquivo transformado pelo Vite)
function Button({ onClick, children }) {
  return React.createElement("button", { onClick }, children);
}
//# sourceMappingURL=Button.js.map
```

```json
// Button.js.map (simplificado — na prática é VLQ-encoded)
{
  "version": 3,
  "sources": ["src/components/Button.tsx"],
  "sourcesContent": ["export function Button({ onClick, children }: ButtonProps) {\n  return <button onClick={onClick}>{children}</button>;\n}"],
  "mappings": "AAAA,SAAS,OAAO,EAAE,OAAO,EAAE,QAAQ..."
}
```

O campo `mappings` usa o formato **VLQ Base64** (Variable Length Quantity) — uma codificação compacta que mapeia cada posição no output para uma posição no source. O DevTools lê isso e executa o mapeamento transparentemente.

**Como o DevTools detecta e usa source maps automaticamente.** O browser não carrega source maps durante a execução normal da página — isso seria desperdício de banda para o usuário. Quando você abre o DevTools (F12), o browser verifica se o arquivo JavaScript possui um comentário `//# sourceMappingURL=...` no final. Se tiver, o DevTools faz um request separado para buscar o `.map`. Com source maps inline (padrão em dev no Vite), o mapeamento já vem embutido no próprio arquivo como uma string base64 — sem request adicional. Você não precisa configurar absolutamente nada: basta ter o DevTools aberto, e as abas Sources/Debugger vão mostrar seu TypeScript/JSX original em vez do JavaScript transformado. Breakpoints definidos no arquivo original funcionam diretamente. O único requisito é que a opção "Enable JavaScript source maps" esteja habilitada no DevTools — ela vem ativada por padrão em todos os browsers modernos.

### Os três tipos de source maps

```mermaid
graph TD
    classDef ok fill:#4ADE8021,stroke:#4ADE80,color:#E9ECF2
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    subgraph INLINE["Inline\n(devSourcemap: true — Vite dev default)"]
        I1["O source map é embutido\nno próprio .js como base64"]
        I2["▶ Um request só\n▶ Ótimo para dev"]
        I3["✗ Arquivo grande\n✗ Ruim para prod"]
        I1 --> I2
        I1 --> I3
    end

    subgraph EXTERNAL["Externo\n(sourcemap: true — Vite build)"]
        E1["Arquivo .js.map separado\nreferenciado pelo .js"]
        E2["▶ Bundle menor\n▶ Só baixado quando DevTools abre"]
        E3["✗ Dois requests\n✗ Expõe source ao usuário"]
        E1 --> E2
        E1 --> E3
    end

    subgraph HIDDEN["Hidden\n(sourcemap: 'hidden')"]
        H1["Arquivo .js.map separado\nSEM referência no .js"]
        H2["▶ Bundle limpo\n▶ Sourcemap para Sentry/error tracking"]
        H3["✗ Usuário não consegue debugar\n(intencionalmente)"]
        H1 --> H2
        H1 --> H3
    end

    class INLINE ok
    class EXTERNAL neutro
    class HIDDEN destaque
```

> [!info] Leitura do diagrama
> Três estratégias, três trade-offs. Em dev, inline é o padrão — sem deploy de arquivos extras, sem segundo request. Em prod, hidden é o padrão para times sérios: o `.js.map` é gerado mas não referenciado, enviado só para o sistema de error tracking (Sentry, Datadog) — o usuário nunca vê seu source.

### Source maps no Vite

O Vite usa source maps inline em dev por padrão. Quando você transforma um `.tsx`, o arquivo servido ao browser já contém o mapeamento embutido. O DevTools detecta automaticamente e você debugga seu TypeScript original.

```ts
// vite.config.ts — controle de source maps
export default defineConfig({
  // Em dev, o padrão já é inline. Para desabilitar (raro):
  // server: { sourcemapIgnoreList: () => false },

  build: {
    sourcemap: true,    // gera arquivo .map externo (referenciado)
    // sourcemap: 'hidden', // gera .map sem referenciar — para Sentry
    // sourcemap: 'inline', // embutido no bundle — grande demais para prod
    // sourcemap: false,    // sem source map em prod (padrão)
  }
})
```

> [!warning] O custo real dos source maps em produção
> Source maps completos podem ser maiores que o próprio bundle — um bundle de 200KB pode ter um `.map` de 800KB. Isso aumenta o tempo de build e o espaço em disco/CDN. Em produção com `hidden`, esse custo não afeta usuários (o `.map` nunca é servido). Mas gerar source maps sempre adiciona latência ao pipeline de CI. Times de alta performance usam `sourcemap: 'hidden'` + upload automático para error tracking, sem servir o `.map` via CDN.

---

## Vite 8: o que mudou além do motor

O Vite 8 (lançado 2026-03-12) não trocou só o bundler de build — trouxe mudanças arquiteturais que afetam diretamente o dev server e o HMR.

### Oxc Transforms: transpilação em Rust

O Vite 8 adota o **Oxc** (The JavaScript Oxidation Compiler) para transpilação de TypeScript e JSX. Antes, esbuild (Go) era responsável por converter `.tsx` para `.js` a cada request. Agora, Oxc (Rust) faz isso — e é substancialmente mais rápido, especialmente em projetos com muitos arquivos TypeScript com decorators e tipos complexos.

> [!note] Oxc e Rolldown são projetos distintos
> Oxc é o transpilador (TS→JS, JSX→JS, transformações de sintaxe). Rolldown é o bundler (resolve grafo, agrupa módulos, tree-shaking). O Vite 8 usa ambos: Oxc transforma individualmente cada arquivo servido em dev, Rolldown bundla as dependências (pré-bundling) e produz o output de build. São componentes complementares da toolchain Rust da VoidZero.

### Bundled dev mode: HMR escalável para apps gigantes

O modelo ESM-sob-demanda tem um limite: em aplicações com milhares de componentes, o browser faz centenas de requests na inicialização. Em testes com apps de 10.000 componentes React, o cold start ficava lento por pura latência de HTTP.

O Vite 8 introduz um **bundled dev mode** opcional: em vez de servir cada módulo individualmente, o Rolldown agrupa módulos em chunks menores — mantendo HMR granular por módulo, mas reduzindo o número de requests de inicialização.

```ts
// vite.config.ts — Vite 8 bundled dev mode (experimental em 8.0)
export default defineConfig({
  dev: {
    bundleMode: 'bundle',  // 'module' é o padrão ESM-sob-demanda
  }
})
```

> [!note] Para a maioria dos projetos, `bundleMode: 'module'` é o default correto
> O bundled mode é útil em monorepos e apps com >1000 módulos onde o overhead de requests se torna perceptível. Para projetos normais (dezenas ou centenas de módulos), o modo ESM clássico é mais rápido no HMR porque o browser substitui exatamente um arquivo.

### Cloudflare e VoidZero

Em 2026, a Cloudflare adquiriu a **VoidZero** — a empresa fundada por Evan You para desenvolver Rolldown, Oxc e a próxima geração do Vite. Isso não mudou a governança open-source do Vite (que permanece na Vite Core Team), mas consolidou o financiamento e a infraestrutura de desenvolvimento da toolchain Rust subjacente.

---

## O trade-off dev↔prod no Vite 8: motores unificados

A tensão dev/prod que descrevemos tem uma história de ferramentas no Vite. Durante anos (Vite 1–7), a situação era:

- **Dev**: esbuild transforma arquivos individualmente (Go, rápido, mas não otimiza globalmente), serviço ESM sob demanda
- **Prod**: Rollup bundla (JS, mais lento, mas com tree-shaking e output formats completos)

O problema era **inconsistência**: features que funcionavam em dev podiam se comportar diferente em prod porque os dois motores tinham semânticas ligeiramente diferentes. E o esbuild não suportava todos os plugins do ecossistema Rollup.

Com o **Vite 8** (março de 2026), a VoidZero lançou o **Rolldown** como motor único:

```mermaid
graph LR
    classDef marca fill:#8855DF33,stroke:#8855DF,color:#E9ECF2
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    classDef ok fill:#4ADE8021,stroke:#4ADE80,color:#E9ECF2
    subgraph VITE7["Vite ≤ 7 (arquitetura dual)"]
        V7DEV["Dev:\nesbuild (Go)\n• pré-bundling de deps\n• transpila TS/JSX por request"]
        V7PROD["Prod:\nRollup (JS)\n• bundle completo\n• tree-shaking, code splitting\n• plugins do ecossistema"]
        V7DEV -.- V7PROD
        class V7DEV marca
        class V7PROD destaque
    end

    subgraph VITE8["Vite 8 (arquitetura unificada)"]
        V8["Rolldown (Rust)\n• pré-bundling de deps em dev\n• transpila TS/JSX em dev\n• bundle completo em prod\n• mesma semântica, mesma API\n• 10–30× mais rápido em build"]
        class V8 ok
    end
```

> [!info] Leitura do diagrama
> O Vite 7 usava dois motores com semânticas diferentes — esbuild em dev, Rollup em prod. O Vite 8 usa Rolldown para ambos: mesmo motor, mesma semântica, mesma API de plugins. A inconsistência dev/prod desapareceu como classe de bug.

> [!note] O que o Vite 8 preservou do modelo ESM
> A troca de motor **não mudou o modelo de servir ESM sob demanda**. O Vite 8 ainda não bundla sua aplicação em dev. O Rolldown substituiu o esbuild no pré-bundling de dependências e na transformação individual de arquivos, mas o princípio de "serve sob demanda, browser faz os requests" permanece. A nota [[13 - Vite a fundo]] cobre a configuração e o ecossistema de plugins em detalhes.

### Linha do tempo do Vite/Rolldown (2021–2026)

| Ano | Marco |
|-----|-------|
| 2021 | Vite 1 lançado — ESM nativo + esbuild para dev |
| 2022 | Vite 3 — ecossistema de plugins explode; padrão de facto para SPA |
| 2024 | VoidZero fundada por Evan You; Rolldown e Oxc anunciados |
| mai/2025 | `rolldown-vite` preview técnico disponível |
| dez/2025 | Vite 8 beta com Rolldown como padrão |
| mar/2026 | **Vite 8 estável** — Rolldown + Oxc, motor único; HMR bundled mode |
| mai/2026 | Rolldown 1.0 estável lançado; Cloudflare adquire VoidZero |
| mai/2026 | **Vite 8.1** lançado — refinamentos do bundled dev mode, fixes de HMR |

---

## O que acontece quando você salva um arquivo com HMR ligado

Vamos percorrer o cenário completo para concretizar todos os conceitos:

```mermaid
sequenceDiagram
    participant Dev as Editor (VS Code)
    participant FS as Sistema de Arquivos
    participant Chokidar as File Watcher (chokidar)
    participant Graph as Grafo de Módulos (Vite)
    participant Rolldown as Rolldown (transforma)
    participant WS as WebSocket
    participant HMRClient as /@vite/client (browser)
    participant Browser as Browser (React app)

    Dev->>FS: salva src/components/Counter.tsx

    FS->>Chokidar: evento 'change'
    Chokidar->>Graph: Counter.tsx mudou
    Graph->>Graph: invalida Counter.tsx no grafo
    Graph->>Graph: propaga: quais módulos importam Counter?\n(Counter é self-accepting via plugin React? sim)
    Graph->>WS: payload: { type: 'update', updates: [{ path: '/src/components/Counter.tsx' }] }

    WS->>HMRClient: mensagem WebSocket com payload
    HMRClient->>Rolldown: GET /src/components/Counter.tsx?t=1718200000
    Rolldown->>FS: lê Counter.tsx
    Rolldown->>Rolldown: transforma TSX→JS + source map inline
    Rolldown-->>HMRClient: Counter.js (módulo novo)

    HMRClient->>Browser: chama handler de accept() do plugin React
    Browser->>Browser: React Fast Refresh substitui\ncomponente Counter na árvore
    Browser->>Browser: re-renderiza Counter com estado preservado
    Note over Browser: useState do Counter mantém seu valor\n(o count não voltou a zero)
```

> [!info] Leitura do diagrama
> Doze passos da tecla Save até o componente atualizado no browser — sem reload de página, sem perda de estado. O `?t=1718200000` no request é um timestamp (cache-busting) para forçar o browser a buscar a versão nova em vez de usar o cache HTTP.

O detalhe crítico é a linha "Counter é self-accepting via plugin React?". O `@vitejs/plugin-react` (que usa React Fast Refresh) injeta automaticamente `import.meta.hot.accept()` em cada componente. Quando o grafo de invalidação chega num módulo self-accepting, a propagação para. Se o grafo chegasse num módulo sem `accept()`, o Vite faria um full reload.

---

## Como explicar em inglês

The Vite dev server works by serving your application source code as native ES Modules directly to the browser, without bundling. The browser requests modules on demand via HTTP, and Vite transforms each file in-place — stripping TypeScript types, compiling JSX, and injecting HMR hooks — then responds with a plain JavaScript module. Dependencies from `node_modules` are pre-bundled by Rolldown into single ESM files in `.vite/deps/`, handling the CJS-to-ESM conversion and collapsing hundreds of internal sub-modules into a single request.

HMR — Hot Module Replacement — works through a WebSocket connection between the Vite server and a small client script injected into the browser. When you save a file, Vite walks the module import graph to find which modules are affected, then notifies the browser over WebSocket. The browser fetches only the changed module, and the HMR client replaces it in memory without a full page reload, preserving the application state. Frameworks like React integrate via the `import.meta.hot.accept()` API, which lets each module declare how it handles being replaced at runtime.

Source maps are JSON files that map positions in the transformed JavaScript back to their original source locations. Vite embeds them inline during development so DevTools can show your TypeScript/JSX source when debugging. In production, teams typically generate hidden source maps — separate `.map` files not referenced in the bundle — and upload them to error-tracking services.

Vite 8 (stable March 2026) unified the dev and build engines under Rolldown, a Rust-based bundler that replaces both esbuild (previously used for pre-bundling) and Rollup (previously used for production builds), delivering 10–30x faster builds with a single consistent plugin API.

### Vocabulário-chave

| Português | English |
|-----------|---------|
| servidor de desenvolvimento | dev server |
| módulos nativos do browser | native ES Modules / browser-native ESM |
| pré-bundling de dependências | dependency pre-bundling |
| substituição a quente de módulos | Hot Module Replacement (HMR) |
| módulo self-accepting | self-accepting module |
| grafo de módulos | module import graph |
| conexão em tempo real | WebSocket connection |
| mapa de origem | source map |
| source map inline | inline source map |
| source map oculto | hidden source map |
| cache-busting por timestamp | timestamp-based cache-busting |
| motor unificado | unified engine / single bundler |
| estado preservado | preserved state |
| recarregamento completo | full page reload |
| propagação de invalidação | invalidation propagation |

---

## Armadilhas comuns

**Confundir HMR com live reload.** Live reload recarrega a página inteira — você perde todo o estado. HMR substitui módulos em memória — o estado sobrevive. São mecanismos completamente diferentes. Vite usa HMR; só faz live reload como fallback quando não consegue fazer HMR.

**Esquecer o guard `if (import.meta.hot)`.**  Em produção, `import.meta.hot` é `undefined`. Se você chamar `.accept()` sem o guard, o código quebra em produção. Sempre envolva código HMR no guard — o Vite remove o bloco inteiro via tree-shaking quando o guard está presente.

**Assumir que source maps em produção são gratuitos.** Gerar source maps adiciona tempo de build e pode dobrar o tamanho dos artefatos. Em pipelines de CI grandes, isso importa. Use `sourcemap: 'hidden'` e suba os `.map` para seu error tracker — não os sirva via CDN.

**Editar arquivos em `node_modules` e esperar HMR.** O Vite monitora seu código-fonte, não `node_modules`. Mudanças em dependências exigem reiniciar o servidor (ou deletar `.vite/deps/` e reiniciar).

**Misturar exportações React e não-React no mesmo arquivo.** Se um arquivo exporta um componente React e também uma constante ou função utilitária, o React Fast Refresh não consegue garantir o boundary — ele descarta o estado e faz full reload. O aviso no terminal é: `"Fast refresh only works when a file only exports components"`. A solução é mover a constante para um arquivo separado.

**Assumir que `useEffect` não vai reexecutar durante Fast Refresh.** Todo `useEffect`, `useMemo` e `useCallback` re-executa sempre que Fast Refresh aplica uma atualização — independentemente do array de dependências. Se você tem um efeito com dependência vazia (`[]`) que faz uma chamada de API, ela vai disparar de novo toda vez que você salvar o arquivo. Em dev isso é intencional e geralmente inofensivo; mas se o efeito tem side effects pesados (ex: conectar a um WebSocket, inicializar um SDK), pode gerar comportamento confuso.

**Migrar para Vite 8 sem testar plugins.** A troca esbuild→Rolldown é transparente para a maioria dos casos, mas alguns plugins usavam APIs internas do esbuild. Verifique a lista de plugins do seu projeto antes de atualizar.

**Assumir que o modelo ESM do Vite funciona em produção sem bundler.** O Vite serve ESM sob demanda em dev porque o browser faz dezenas de requests individuais — aceitável em localhost. Em produção, você precisa do `vite build` para gerar um bundle otimizado; sem ele, o usuário faria centenas de requests HTTP.

---

## Referências

- [HMR API | Vite (oficial)](https://vite.dev/guide/api-hmr) — documentação da `import.meta.hot` API, incluindo `send()`, `on()`, `dispose()` e `invalidate()`
- [Vite 8.0 is out! | vite.dev](https://vite.dev/blog/announcing-vite8) — notas de lançamento do Vite 8 estável (2026-03-12); Rolldown + Oxc como motor unificado
- [Vite 8.1 is out! | vite.dev](https://vite.dev/blog/announcing-vite8-1) — refinamentos do bundled dev mode e fixes de HMR
- [Hot Module Replacement is Easy | Bjorn Lu](https://bjornlu.com/blog/hot-module-replacement-is-easy) — explicação profunda do algoritmo de propagação HMR; análise da `propagateUpdate` no código do Vite
- [Beyond HMR: Understanding React's Fast Refresh | Leapcell / Medium](https://leapcell.medium.com/beyond-hmr-understanding-reacts-fast-refresh-d6d80ef0fe4e) — regras de preservação de estado, comportamento de hooks e module boundary no Fast Refresh
- [Fast Refresh | React Native docs](https://reactnative.dev/docs/fast-refresh) — spec original do Fast Refresh; regras de reset de estado, `@refresh reset`
- [Architecture: Fast Refresh | Next.js](https://nextjs.org/docs/architecture/fast-refresh) — implementação do Fast Refresh no Next.js; edge cases de exportações mistas
- [Vite team boasts 10-30x faster builds with Rust-powered Rolldown | DevClass](https://www.devclass.com/development/2026/03/17/vite-team-boasts-10-30x-faster-builds-with-rust-powered-rolldown/5209472) — benchmarks do Vite 8 vs Vite 7

## Veja também

- [[07 - O grafo de módulos e o que é bundling]] — o grafo de imports que o HMR percorre ao propagar invalidações; o conceito de bundling que o dev server deliberadamente evita
- [[08 - Transpilação e targets]] — o que acontece na transformação individual de cada arquivo (TS→JS, JSX→JS) que o Vite executa por request; Oxc como novo transpilador no Vite 8
- [[13 - Vite a fundo]] — configuração detalhada, sistema de plugins, diferenças entre `vite.config.ts` e o comportamento do dev server; este aqui cobre o modelo conceitual
- [[14 - Rollup, esbuild e Rolldown]] — história e trade-offs dos três motores; por que Rolldown unificou o que esbuild e Rollup faziam separadamente
- [[15 - Turbopack, Rspack e a corrida Rust-Go]] — concorrentes do Vite em dev server e HMR; como Turbopack (Next.js) e Rspack implementam o mesmo ciclo com trade-offs diferentes
