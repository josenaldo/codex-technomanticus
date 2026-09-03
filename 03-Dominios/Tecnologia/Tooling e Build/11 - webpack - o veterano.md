---
title: "webpack - o veterano"
created: 2026-06-24
updated: 2026-06-25
type: concept
fase: adepto
status: seedling
publish: true
tags:
  - tooling
  - webpack
  - bundler
  - adepto
  - entrevista
---

# webpack — o veterano

> [!abstract] TL;DR
> webpack é o bundler que definiu o que significa "configurar build de frontend": entry point, loaders que transformam qualquer coisa em módulo, plugins que orquestram o output, e SplitChunksPlugin que divide o bundle de forma inteligente. Dominou a era 2015–2021 por ser o primeiro a fazer tudo isso junto num único sistema coerente. Em 2026, ainda roda com ~30M+ downloads semanais e é irreplaceable em dois nichos — Apps legados grandes que custam demais pra migrar, e Module Federation (micro-frontends em runtime). Mas para projetos novos, quase ninguém escolhe webpack: o dev server é lento, a config é verbosa, e Vite entrega DX comparável com zero atrito. Saber webpack hoje significa entender o padrão que todos os bundlers modernos replicam ou reagem contra.

---

## O que era o problema em 2014

Para entender o webpack, você precisa se lembrar do que existia antes dele.

Em 2014, o ecosistema frontend tinha dois mundos que não se falavam. No mundo dos task runners (Grunt, Gulp), você escrevia pipelines de transformação de arquivos: concatenar JS, minificar CSS, copiar imagens, rodar sass. Funcionava, mas era frágil — você geria dependências entre tarefas manualmente, e a ordem importava de forma não-óbvia.

No mundo dos module bundlers, havia Browserify: ele resolvia o problema de rodar código CommonJS no browser, mas era rígido. CSS? Você precisava de plugins. Imagens? Outro pipeline. O Browserify resolvia módulos JS e parava por aí.

O que nenhum dos dois resolvia de forma integrada era isso: **tratar absolutamente tudo como módulo**. Em uma aplicação React em 2014, você tinha:

```js
// O que o dev queria escrever
import styles from './Button.module.css';
import logo from './logo.svg';
import Button from './Button.jsx';
```

Três tipos de asset, três ferramentas diferentes, três pipelines separados que você precisava sincronizar. Se o CSS mudasse, o hash do JS mudava errado. Se a imagem mudasse, o manifest ficava desatualizado. Era um pesadelo de orquestração.

webpack resolveu isso com uma tese radical: **tudo é um módulo**. CSS, imagens, fontes, JSON, WASM — qualquer coisa que você `import`a pode ser processada, transformada, e integrada no grafo de dependências. E um único sistema cuida de todo esse grafo, do entry point ao output final.

Essa tese, mais a capacidade de configurar com código JS em vez de YAML, mais o HMR (Hot Module Replacement) que ele popularizou — foi o que fez o webpack dominar de 2015 até o início dos anos 2020.

---

## O modelo mental central: entry → loaders → plugins → output

Antes de ver config, você precisa ter o mapa mental do webpack. Ele tem quatro conceitos centrais, e a confusão entre eles é a maior fonte de frustração para iniciantes.

```mermaid
flowchart TD
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    classDef marca fill:#8855DF33,stroke:#8855DF,color:#E9ECF2
    subgraph INPUT["Entrada"]
        E["Entry point(s)\n(src/index.js, src/admin.js...)"]
    end

    subgraph RESOLVE["Resolução + Grafo"]
        G["Module Graph\n(todos os imports seguidos recursivamente)"]
    end

    subgraph TRANSFORM["Transformação"]
        L["Loaders\n(por módulo, na cadeia certa)\ncss-loader → style-loader\nbabel-loader → js\nfile-loader → asset"]
    end

    subgraph ORCHESTRATE["Orquestração"]
        P["Plugins\n(sobre o ciclo inteiro de build)\nHtmlWebpackPlugin\nMiniCssExtractPlugin\nSplitChunksPlugin\nModuleFederationPlugin"]
    end

    subgraph OUTPUT["Saída"]
        O["Chunks de output\n(dist/main.[hash].js\ndist/vendor.[hash].js\ndist/chunk-editor.[hash].js)"]
    end

    E --> G --> L --> P --> O

    class INPUT neutro
    class RESOLVE destaque
    class TRANSFORM destaque
    class ORCHESTRATE marca
    class OUTPUT marca
```

> [!note] Leitura do diagrama
> O fluxo é linear mas as responsabilidades são distintas. Entry define onde começa o grafo. Loaders transformam módulos individualmente (cada arquivo passa pelos loaders relevantes). Plugins operam no ciclo de build inteiro — não num módulo, mas na compilação. Output define como os chunks resultantes são emitidos.

A diferença entre **loader** e **plugin** é o que mais confunde. Vale gravar:

> [!tip] Loader vs. Plugin — a distinção definitiva
> **Loader** = transforma um arquivo específico. É uma função que recebe o conteúdo de um módulo e retorna o conteúdo transformado. Roda por arquivo, na resolução do módulo. **Plugin** = observa (e modifica) o **ciclo de build inteiro**. Tem acesso ao `compiler` e ao `compilation`, pode emitir arquivos extras, modificar o grafo, injetar código no runtime. Roda em hooks do ciclo de build.
>
> Analogia: loader é como um tradutor de idioma (transforma cada arquivo). Plugin é como um diretor de produção (organiza todo o processo).

---

## Entry: onde o grafo começa

O entry point é o módulo raiz a partir do qual o webpack começa a construir o grafo. Você pode ter um, ou múltiplos.

```js
// webpack.config.js — entry simples (SPA)
module.exports = {
  entry: './src/index.js',
};

// entry múltiplo (MPA — multi-page app)
module.exports = {
  entry: {
    home: './src/pages/home.js',
    checkout: './src/pages/checkout.js',
    admin: './src/pages/admin.js',
  },
};
```

Com múltiplos entry points, o webpack gera um chunk principal para cada um, mais chunks compartilhados entre eles (via `SplitChunksPlugin`). Isso é o fundamento de apps multi-página onde cada rota tem seu próprio bundle inicial, mas compartilham vendors.

```mermaid
graph TD
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    HOME_E["entry: home.js"]
    CHECK_E["entry: checkout.js"]
    ADMIN_E["entry: admin.js"]

    HOME_C["home.[hash].js"]
    CHECK_C["checkout.[hash].js"]
    ADMIN_C["admin.[hash].js"]
    VENDOR_C["vendor.[hash].js\n(React, lodash — compartilhados)"]

    HOME_E --> HOME_C
    CHECK_E --> CHECK_C
    ADMIN_E --> ADMIN_C

    HOME_C -.->|"depende de"| VENDOR_C
    CHECK_C -.->|"depende de"| VENDOR_C
    ADMIN_C -.->|"depende de"| VENDOR_C

    class VENDOR_C neutro
```

> [!note] Leitura do diagrama
> Cada entry gera seu próprio chunk inicial. Módulos compartilhados entre múltiplos entry points são extraídos pelo `SplitChunksPlugin` num chunk de vendor separado. O browser carrega `vendor.[hash].js` uma vez e o reutiliza em cache para todas as páginas.

---

## Loaders: quando tudo vira módulo

Loaders são o coração da filosofia "tudo é módulo". Sem loaders, webpack só processa JavaScript. Com loaders, ele processa qualquer coisa que você declarar.

A lógica é simples: quando o webpack encontra um `import` de um tipo de arquivo, ele verifica as regras de `module.rules` e aplica os loaders correspondentes, em ordem (da direita pra esquerda, ou de baixo pra cima).

```js
// webpack.config.js — seção de loaders
module.exports = {
  module: {
    rules: [
      // Regra 1: TypeScript e TSX
      {
        test: /\.(ts|tsx)$/,                 // regex que casa com o arquivo
        exclude: /node_modules/,
        use: [
          { loader: 'babel-loader' },        // 2º: babel aplica presets
          { loader: 'ts-loader' },           // 1º: ts-loader compila TS→JS (ordem: direita→esquerda)
        ],
      },

      // Regra 2: CSS com CSS Modules
      {
        test: /\.module\.css$/,
        use: [
          MiniCssExtractPlugin.loader,       // 3º: extrai CSS para arquivo separado (em prod)
          {
            loader: 'css-loader',            // 2º: resolve @import e url(), aplica CSS Modules
            options: { modules: true },
          },
          'postcss-loader',                  // 1º: PostCSS (autoprefixer, etc.)
        ],
      },

      // Regra 3: Imagens como assets (webpack 5 nativo — não precisa de file-loader)
      {
        test: /\.(png|jpg|gif|svg)$/i,
        type: 'asset/resource',              // emite o arquivo em dist/ e retorna a URL
        generator: {
          filename: 'images/[hash][ext]',
        },
      },

      // Regra 4: Fontes
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/i,
        type: 'asset/resource',
        generator: {
          filename: 'fonts/[hash][ext]',
        },
      },
    ],
  },
};
```

> [!info] webpack 5 e Asset Modules
> webpack 4 exigia `file-loader`, `url-loader` e `raw-loader` para assets. webpack 5 introduziu **Asset Modules** nativos: `asset/resource` (emite arquivo), `asset/inline` (base64 inline), `asset/source` (texto puro), `asset` (decide automaticamente por tamanho). Elimina a necessidade de instalar três loaders para assets básicos.

A cadeia de loaders para um arquivo `.module.css` fica assim:

```mermaid
flowchart LR
    classDef marca fill:#8855DF33,stroke:#8855DF,color:#E9ECF2
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    CSS["Button.module.css\n(arquivo original)"]
    POSTCSS["postcss-loader\n(autoprefixer, nesting)\n↓\n.btn { color: red }"]
    CSSLOADER["css-loader\n(resolve imports, CSS Modules)\n↓\nJS com objeto de classes\n{ btn: '_abc123_btn' }"]
    EXTRACT["MiniCssExtractPlugin.loader\n(separa CSS do JS)\n↓\nCSS vai pra styles.[hash].css\nJS exporta o objeto de classes"]
    IMPORT["seu componente\nimport s from './Button.module.css'\ns.btn === '_abc123_btn'"]

    CSS --> POSTCSS --> CSSLOADER --> EXTRACT --> IMPORT

    class CSS neutro
    class IMPORT marca
```

> [!note] Leitura do diagrama
> Cada loader recebe o output do anterior. A ordem de execução é da direita para a esquerda no array `use` (postcss-loader primeiro, depois css-loader, depois MiniCssExtractPlugin.loader). O CSS sai do pipeline como dois artefatos: um arquivo `.css` separado (para o `<link>` no HTML) e um objeto JS com os nomes de classes mapeados (para usar no componente).

---

## Tapable: o coração dos plugins

Antes de entender plugins de verdade, você precisa entender Tapable — a biblioteca de hooks que o webpack usa internamente para expor seu ciclo de build. Tapable não é um detalhe de implementação obscuro; é o que torna o ecossistema de plugins do webpack tão poderoso e extensível.

> [!abstract] Tapable em uma linha
> Tapable é um sistema de hooks tipados que permite registrar callbacks (taps) em pontos específicos do ciclo de build e garantir a ordem e o tipo de execução entre eles.

Existem três famílias principais de hooks:

| Tipo | Comportamento | Uso típico |
|---|---|---|
| `SyncHook` | Síncrono, sem retorno | Notificação simples (ex: `compiler.hooks.done`) |
| `SyncBailHook` | Síncrono, para se algum tap retornar não-undefined | Decisões de curto-circuito |
| `SyncWaterfallHook` | Síncrono, passa resultado de um tap pro próximo | Transformações em cadeia |
| `AsyncSeriesHook` | Assíncrono, taps rodam em série | I/O (ex: `compiler.hooks.emit`) |
| `AsyncParallelHook` | Assíncrono, taps rodam em paralelo | Otimizações independentes |

```mermaid
flowchart TD
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    classDef marca fill:#8855DF33,stroke:#8855DF,color:#E9ECF2
    subgraph COMPILER["compiler (ciclo de build inteiro)"]
        C1["hooks.beforeRun\n(SyncHook)"]
        C2["hooks.run\n(AsyncSeriesHook)"]
        C3["hooks.make\n(AsyncParallelHook)\n← aqui o compilation começa"]
        C4["hooks.emit\n(AsyncSeriesHook)\n← aqui os assets são escritos em disco"]
        C5["hooks.done\n(AsyncSeriesHook)\n← build completo"]
    end

    subgraph COMPILATION["compilation (um build específico)"]
        D1["hooks.buildModule\n(SyncHook)\n← cada módulo sendo processado"]
        D2["hooks.seal\n(SyncHook)\n← grafo fechado, nenhum módulo novo"]
        D3["hooks.optimize\n(SyncHook)\n← otimizações (tree-shaking, split)"]
        D4["hooks.processAssets\n(AsyncSeriesHook)\n← assets prontos pra emissão"]
    end

    C3 --> D1 --> D2 --> D3 --> D4 --> C4 --> C5

    class COMPILER neutro
    class COMPILATION marca
```

> [!note] Leitura do diagrama
> `compiler` representa o processo de build inteiro — ele persiste entre builds em modo watch. `compilation` representa um build específico (cada rebuild gera uma nova compilation). Plugins se registram em hooks de ambos: `compiler.hooks.emit` para emitir arquivos adicionais ao final; `compilation.hooks.processAssets` para manipular assets já gerados; `compilation.hooks.optimize` para otimizações pós-seal.

Um plugin mínimo que demonstra o sistema Tapable:

```js
// webpack.config.js — plugin customizado mínimo
class TimingPlugin {
  apply(compiler) {
    let start;

    // tap: registra callback síncrono no hook
    compiler.hooks.run.tapAsync('TimingPlugin', (compiler, callback) => {
      start = Date.now();
      callback(); // obrigatório em hooks async
    });

    compiler.hooks.done.tap('TimingPlugin', (stats) => {
      const duration = Date.now() - start;
      console.log(`Build completed in ${duration}ms`);
    });
  }
}

module.exports = { plugins: [new TimingPlugin()] };
```

> [!tip] Tap vs TapAsync vs TapPromise
> - `tap(name, fn)` — callback síncrono, sem espera
> - `tapAsync(name, (args..., callback) => ...)` — callback-style assíncrono; você chama `callback()` quando terminar
> - `tapPromise(name, (...args) => Promise)` — Promise-style; o hook espera a Promise resolver
>
> O tipo de hook determina quais variantes são permitidas. `SyncHook` só aceita `tap`. `AsyncSeriesHook` aceita os três.

---

## Plugins: orquestração do ciclo de build

Se loaders transformam módulos, plugins observam e controlam o build inteiro. O webpack expõe um sistema de hooks baseado em Tapable (a lib de hooks interna do webpack) em cada fase do ciclo de compilação. Um plugin se registra em algum desses hooks e executa lógica customizada.

Os plugins mais usados em qualquer config de produção:

```js
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

// webpack.config.js — seção de plugins
plugins: [
  // Gera o index.html injetando automaticamente os <script> e <link> certos
  new HtmlWebpackPlugin({
    template: './public/index.html',
    // Em MPA, uma instância por página:
    // new HtmlWebpackPlugin({ template: '...', filename: 'home.html', chunks: ['home', 'vendor'] }),
  }),

  // Extrai todo CSS dos módulos em arquivos .css separados (vs. inlinear no JS)
  new MiniCssExtractPlugin({
    filename: 'css/[name].[contenthash:8].css',
    chunkFilename: 'css/[id].[contenthash:8].css',
  }),

  // Analisador de bundle — gera visualização treemap do que está dentro do bundle
  // (útil pra debugar por que seu bundle está grande)
  new BundleAnalyzerPlugin({ analyzerMode: 'static', openAnalyzer: false }),
],

// Minimizadores — também são plugins, mas ficam em optimization.minimizer
optimization: {
  minimizer: [
    '...', // mantém o TerserPlugin padrão para JS
    new CssMinimizerPlugin(), // adiciona minificação de CSS
  ],
},
```

> [!tip] O ciclo de build e os hooks do webpack
> O webpack expõe dezenas de hooks no `compiler` (ciclo de build inteiro: `run`, `emit`, `done`) e no `compilation` (ciclo de um build específico: `buildModule`, `seal`, `optimize`). Um plugin pode interceptar qualquer um desses momentos. `HtmlWebpackPlugin`, por exemplo, se registra no hook `emit` para injetar os hashes corretos no HTML depois que os chunks foram finalizados — não antes, porque só então os hashes são conhecidos.

---

## Code splitting com SplitChunksPlugin

`SplitChunksPlugin` é o plugin interno do webpack que divide chunks automaticamente com base em heurísticas. Ele resolve um problema real: se você tem três páginas que importam React e lodash, sem splitting você teria React + lodash duplicados em cada chunk de página.

```js
// webpack.config.js — optimization completo
module.exports = {
  optimization: {
    // Extrai o "runtime" do webpack (o código que carrega outros chunks) em arquivo separado
    runtimeChunk: 'single',

    splitChunks: {
      chunks: 'all',               // 'async' (padrão), 'initial', ou 'all' (recomendado)
      minSize: 20_000,             // só extrai se o módulo tiver > 20KB
      maxAsyncRequests: 30,
      maxInitialRequests: 30,
      cacheGroups: {
        // Vendors: todo código de node_modules vai pra chunk separado
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendor',
          chunks: 'all',
          priority: -10,
        },
        // React especificamente num chunk próprio (muda raramente = cache longo)
        react: {
          test: /[\\/]node_modules[\\/](react|react-dom|react-router)[\\/]/,
          name: 'react-vendor',
          chunks: 'all',
          priority: 20,            // prioridade maior que 'vendor' → esse grupo vence quando ambos casam
        },
        // Código compartilhado entre ≥2 chunks do seu app (não de node_modules)
        common: {
          minChunks: 2,            // módulo deve ser importado por pelo menos 2 chunks
          name: 'common',
          chunks: 'all',
          priority: -20,
          reuseExistingChunk: true,
        },
      },
    },
  },
};
```

O resultado em disco de uma app com essa config:

```
dist/
  runtime.[hash].js          → ~2KB: bootstrap do webpack (carrega outros chunks)
  react-vendor.[hash].js     → React + ReactDOM + React Router (~140KB gzipped)
  vendor.[hash].js           → lodash, date-fns, etc. (muda raramente)
  common.[hash].js           → utilitários compartilhados do seu código
  home.[hash].js             → código específico da home page
  checkout.[hash].js         → código específico do checkout
  chunk-editor.[hash].js     → chunk lazy (import() dinâmico do editor)
```

> [!info] Por que `runtimeChunk: 'single'` importa
> O runtime do webpack é o bootstrap que, em runtime no browser, sabe quais chunks existem e como carregá-los sob demanda. Esse bootstrap **contém um mapa de todos os chunks** (nomes, hashes, URLs) que o app usa. Sem extraí-lo, ele fica embutido dentro de cada chunk inicial — incluindo `vendor.js`.
>
> O problema é que esse mapa muda toda vez que qualquer chunk muda de hash. Se você edita `home.js` e o hash do chunk `home` muda, o mapa interno do runtime precisa refletir o hash novo — mas esse mapa está gravado dentro de `vendor.js`. Resultado: o *conteúdo* de `vendor.js` muda (porque o mapa embutido mudou), o hash de `vendor.js` muda, e o browser invalida o cache do vendor, mesmo que nenhuma dependência vendorizada tenha mudado.
>
> Extraindo com `runtimeChunk: 'single'`, o mapa de chunks fica só em `runtime.[hash].js` (~2KB). Quando `home.js` muda, só `runtime.js` e `home.js` têm hash novo — `vendor.js` permanece idêntico, cache intacto.

---

## Cache persistente: o maior ganho do webpack 5

Um dos features mais subestimados do webpack 5 é o **filesystem cache** — uma cache que persiste entre builds em disco. Em projetos grandes, isso transforma "rebuild de 40 segundos" em "rebuild de 2-3 segundos" nos builds subsequentes.

```js
// webpack.config.js — cache persistente
module.exports = {
  cache: {
    type: 'filesystem',              // persiste em disco (vs 'memory', default em dev)
    cacheDirectory: path.resolve(__dirname, '.webpack_cache'),
    buildDependencies: {
      // invalida o cache se qualquer um desses arquivos mudar
      config: [__filename],          // próprio webpack.config.js
      tsconfig: [path.resolve(__dirname, 'tsconfig.json')],
    },
    // Versão do cache — incrementar força invalidação total (útil em CI)
    version: '1.0',
    // Compressão automática (gzip) dos artefatos de cache
    compression: 'gzip',
  },
};
```

> [!info] Como o cache filesystem funciona
> O webpack serializa o estado interno de cada módulo (código processado por loaders, metadados de resolução, resultado de tree-shaking parcial) para arquivos binários em `.webpack_cache/`. No próximo build, antes de reprocessar um módulo, ele verifica se o hash do arquivo-fonte + todos os loaders + dependências de config mudou. Se não mudou, usa o resultado em cache. O ganho é mais dramático nos primeiros builds após o cold start — e é cumulativo: quanto mais estável o código, mais o cache funciona.

```mermaid
flowchart LR
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    subgraph "Build 1 (cold)"
        B1_SRC["src/**\n(600 módulos)"]
        B1_PROC["processamento completo\nbabel, ts, css, assets"]
        B1_CACHE["serialização\n→ .webpack_cache/\n~50-100MB"]
        B1_TIME["⏱ 35s"]
        B1_SRC --> B1_PROC --> B1_CACHE
    end

    subgraph "Build 2 (warm cache)"
        B2_SRC["src/**\n(2 arquivos mudaram)"]
        B2_CHECK["verifica hash\n598 cache hits\n2 misses"]
        B2_PROC["reprocessa só\nos 2 módulos alterados"]
        B2_TIME["⏱ 2-3s"]
        B2_SRC --> B2_CHECK --> B2_PROC
    end

    B1_CACHE -.->|"cache read"| B2_CHECK

    class B1_TIME destaque
    class B2_TIME neutro
```

> [!note] Leitura do diagrama
> O ganho de cache não é incremental proporcional — é quase constante. Dois módulos mudados ou duzentos módulos mudados, o overhead base de "verificar hashes" é similar. O que varia é o tempo de reprocessar os módulos que deram miss. Em projetos estáveis (maioria do código não muda entre builds), o filesystem cache é o equivalente a ter um build de produção em 3 segundos.

> [!warning] Cache filesystem em CI
> O cache filesystem funciona melhor quando persiste entre runs de CI. Em GitHub Actions, use `actions/cache` para restaurar `.webpack_cache/` com chave baseada em `package-lock.json`. Sem isso, cada run começa cold e o ganho some. Com isso, builds de CI caem de 5 minutos para 45-60 segundos em projetos médios.

---

## `mode` e o que ele ativa automaticamente

`mode` é uma das adições mais úteis do webpack 4 que muita gente não explora além de `'development'` vs `'production'`. Saber exatamente o que cada mode faz evita configuração redundante e explica comportamentos que parecem mágica.

```js
// Os três modes possíveis
module.exports = { mode: 'production' }  // | 'development' | 'none'
```

O que cada mode configura automaticamente:

| Configuração | `development` | `production` | `none` |
|---|---|---|---|
| `process.env.NODE_ENV` | `'development'` | `'production'` | (não define) |
| `devtool` | `eval` | `false` | `false` |
| Tree-shaking | desativado | ativado (`usedExports`, `sideEffects`) | desativado |
| Minificação (Terser) | desativado | ativado | desativado |
| `optimization.moduleIds` | `named` (legível) | `deterministic` (hashes) | `natural` |
| `optimization.chunkIds` | `named` | `deterministic` | `natural` |
| `cache.type` | `memory` | `memory` | `memory` |
| Scope hoisting | desativado | ativado (`concatenateModules`) | desativado |

> [!info] O que é scope hoisting (e por que só em production)
> Sem scope hoisting, o webpack envolve cada módulo em uma função separada para isolar seu escopo. Com 200 módulos, o bundle tem 200 funções aninhadas. Isso tem dois custos: tamanho (o código de wrapping ocupa espaço) e performance de runtime (o motor JS precisa criar 200 closures).
>
> `concatenateModules` (o scope hoisting) resolve isso: quando módulos ESM são relacionados de forma estática e simples, o webpack os *concatena* num único escopo plano, eliminando as funções de wrapper. O resultado é um bundle menor e mais rápido de executar — em projetos grandes, o ganho de tamanho chega a 10-15%.
>
> Só funciona com ESM puro (análise estática necessária) e em production porque em development os módulos com `named` IDs e source maps separados por módulo são mais úteis para debugging do que o bundle concatenado.

> [!tip] `DefinePlugin` implícito no mode
> `mode: 'production'` implicitamente adiciona `new webpack.DefinePlugin({ 'process.env.NODE_ENV': JSON.stringify('production') })`. Isso significa que código guardado por `if (process.env.NODE_ENV !== 'production')` é eliminado pelo Terser em produção — é assim que React remove seus warnings de dev sem code splitting manual.

Se você precisar de um DefinePlugin explícito (para injetar outras variáveis de build):

```js
const webpack = require('webpack');

plugins: [
  new webpack.DefinePlugin({
    // NÃO usar process.env.NODE_ENV aqui se já usa mode — seria duplicado
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    __BUILD_DATE__: JSON.stringify(new Date().toISOString()),
    __FEATURE_FLAG_EDITOR__: JSON.stringify(process.env.FEATURE_EDITOR === 'true'),
  }),
],
```

No código, essas constantes são substituídas em tempo de build:

```js
// Antes do build (fonte):
if (__FEATURE_FLAG_EDITOR__) {
  import('./Editor').then(m => render(m.Editor));
}

// Depois de mode: 'production' + Terser (se FEATURE_EDITOR=false):
// Bloco inteiro eliminado — nem o dynamic import existe no bundle
```

---

## `externals` e `resolve`: além do básico

Duas configurações que aparecem em configs de produção sérios mas raramente são explicadas com profundidade.

### `externals` — excluir deps do bundle

`externals` diz ao webpack "não inclua esse módulo no bundle — ele vai estar disponível no ambiente de runtime (global ou CDN)". Usado em dois cenários principais:

**Cenário 1: Libs entregues via CDN (bibliotecas de UI em legado)**

```html
<!-- index.html -->
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
```

```js
// webpack.config.js
module.exports = {
  externals: {
    // Quando o código faz `import React from 'react'`,
    // webpack resolve como `window.React` em vez de incluir no bundle.
    react: 'React',
    'react-dom': 'ReactDOM',
  },
};
```

**Cenário 2: Bibliotecas sendo criadas (não apps)**

Ao criar uma lib que vai ser publicada no npm, você nunca deve incluir React (ou outras peer deps) no bundle — o consumidor já tem. `externals` garante que o bundle da lib não carregue React de novo:

```js
// webpack.config.js de uma lib
module.exports = {
  externals: {
    react: { commonjs: 'react', commonjs2: 'react', amd: 'React', root: 'React' },
    'react-dom': { commonjs: 'react-dom', commonjs2: 'react-dom', amd: 'ReactDOM', root: 'ReactDOM' },
  },
  output: { library: { name: 'MyLib', type: 'umd' } },
};
```

> [!info] Por que externals de lib usa objeto `{commonjs, commonjs2, amd, root}`
> A forma string `{ react: 'React' }` funciona quando você sabe exatamente em qual ambiente o bundle será executado: no browser, `React` é uma variável global — ponto final. Mas uma lib publicada no npm precisa ser usada em *múltiplos* ambientes ao mesmo tempo (isso é exatamente o que `output.library.type: 'umd'` declara).
>
> UMD (Universal Module Definition) gera um bundle que detecta em qual ambiente está e se registra de forma diferente:
> - **`root`**: browser sem sistema de módulos → espera `window.React`
> - **`commonjs` / `commonjs2`**: Node.js ou bundler CJS → espera `require('react')`
> - **`amd`**: ambiente AMD (RequireJS) → espera `define(['react'], ...)`
>
> O objeto de externals mapeia *como o React deve ser resolvido em cada contexto do UMD*. Sem isso, o bundle UMD tentaria empacotar React dentro da lib — o que quebraria quem já tem React instalado e usaria duas instâncias. Em resumo: string simples = um ambiente; objeto UMD = todos os ambientes simultâneos.

### `resolve` — como módulos são encontrados

`resolve` vai além de alias. Configurações úteis que aparecem em projetos reais:

```js
resolve: {
  // Extensões: webpack tenta cada uma em ordem ao importar sem extensão
  extensions: ['.tsx', '.ts', '.jsx', '.js', '.json'],

  // Alias: atalhos de caminho (evita '../../../')
  alias: {
    '@': path.resolve(__dirname, 'src'),
    '@tests': path.resolve(__dirname, 'tests'),
    // Alias condicional: troca uma implementação por outra
    'lodash-es': 'lodash', // força CJS lodash em ambientes que não suportam ESM
  },

  // mainFields: ordem de campos do package.json que webpack prefere ao importar uma lib
  // Default pra targets web: ['browser', 'module', 'main']
  // Isso explica por que importar 'react' pega o CJS — o package.json do React não tem 'module'
  mainFields: ['browser', 'module', 'main'],

  // fallback: polyfills para módulos Node em ambientes browser (webpack 5 não polyfilla automaticamente)
  fallback: {
    buffer: require.resolve('buffer/'),   // libs que usam Buffer no browser
    crypto: false,                        // 'false' = não polyfilla, apenas ignorar o import
    path: require.resolve('path-browserify'),
  },
},
```

> [!info] Por que webpack 5 quebrou muitas bibliotecas com "Buffer is not defined"
> webpack 4 incluía polyfills para módulos Node (`buffer`, `crypto`, `path`, `stream`, etc.) automaticamente. webpack 5 removeu isso — se uma lib de terceiros usa `require('crypto')`, você precisa explicitamente configurar `resolve.fallback`. Isso foi intencional (não faz sentido empacotar polyfills que 90% das apps não usam), mas causou quebras na migração de projetos que usavam libs de Node no frontend sem perceber.

---

## Dev server e HMR — o legado mais importante

webpack-dev-server foi o primeiro dev server com HMR (Hot Module Replacement) que funcionava de verdade em um projeto JS de escala. O HMR é a técnica que permite que uma mudança num arquivo seja "injetada" no browser **sem recarregar a página inteira**, preservando o estado da aplicação.

```mermaid
sequenceDiagram
    participant DEV as Dev (você)
    participant FS as Sistema de arquivos
    participant WDS as webpack-dev-server
    participant BROWSER as Browser
    participant APP as App em memória

    DEV->>FS: edita Button.jsx
    FS->>WDS: evento de mudança (watch)
    WDS->>WDS: recompila apenas o módulo alterado\n+ dependentes (graph analysis)
    WDS->>BROWSER: WebSocket: "módulo X mudou, hash novo"
    BROWSER->>WDS: HTTP: GET /hot-update/[hash].json (manifest)
    BROWSER->>WDS: HTTP: GET /hot-update/[hash].js (patch do módulo)
    BROWSER->>APP: aplica o patch: substitui Button no registry
    APP->>APP: React Fast Refresh re-renderiza\nsem perder estado do componente
    Note over BROWSER,APP: Página não recarregou.\nEstado (form preenchido, modal aberto) persiste.
```

> [!note] Leitura do diagrama
> O ciclo HMR tem três fases: detecção (webpack-dev-server via watch no FS), propagação (WebSocket do server para o browser), e aplicação (o browser baixa só o patch do módulo alterado, não o bundle inteiro). O React Fast Refresh — integrado via `babel-plugin-react-refresh` — garante que componentes sejam substituídos sem perder estado local.

O HMR do webpack foi o padrão da indústria por anos. Vite e outros ferramentas modernas implementam HMR também, mas com uma arquitetura diferente: em vez de recompilar o módulo alterado em webpack e enviar o patch, o Vite serve o módulo como ESM nativo e instrui o browser a reimportá-lo diretamente. O resultado em HMR speed é favorável ao Vite (50–500ms vs alguns segundos no webpack em projetos grandes), mas o conceito de "injetar só o que mudou sem recarregar" nasceu no ecosystem do webpack.

---

## Um webpack.config.js real e comentado

Este é um config realista para um projeto React + TypeScript em produção, com comentários explicando cada decisão:

```js
// webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

const isDev = process.env.NODE_ENV !== 'production';

module.exports = {
  // ──────────────────────────────────────────────────────────────────
  // MODE: ativa otimizações automáticas. 'production' liga tree-shaking,
  // minificação com Terser, e define process.env.NODE_ENV='production'.
  // ──────────────────────────────────────────────────────────────────
  mode: isDev ? 'development' : 'production',

  // ──────────────────────────────────────────────────────────────────
  // ENTRY: ponto de partida do grafo de módulos.
  // ──────────────────────────────────────────────────────────────────
  entry: './src/index.tsx',

  // ──────────────────────────────────────────────────────────────────
  // OUTPUT: como os chunks são emitidos em disco.
  // contenthash garante que só o chunk que mudou tem hash novo.
  // ──────────────────────────────────────────────────────────────────
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: isDev ? '[name].js' : '[name].[contenthash:8].js',
    chunkFilename: isDev ? '[id].chunk.js' : '[id].[contenthash:8].chunk.js',
    clean: true,          // webpack 5: limpa dist/ antes de cada build (substitui CleanWebpackPlugin)
    publicPath: '/',      // URL base para os assets (importante para routing em SPA)
  },

  // ──────────────────────────────────────────────────────────────────
  // RESOLVE: como o webpack encontra módulos ao seguir imports.
  // ──────────────────────────────────────────────────────────────────
  resolve: {
    extensions: ['.tsx', '.ts', '.js', '.jsx'],  // testa essas extensões na ordem ao importar sem extensão
    alias: {
      '@': path.resolve(__dirname, 'src'),        // import '@/components/Button' em vez de '../../../components/Button'
    },
  },

  // ──────────────────────────────────────────────────────────────────
  // LOADERS: transformações por tipo de arquivo.
  // ──────────────────────────────────────────────────────────────────
  module: {
    rules: [
      // TypeScript e TSX via SWC (mais rápido que ts-loader + babel-loader)
      {
        test: /\.(ts|tsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'swc-loader',     // usa SWC (Rust) em vez de Babel — 5-20x mais rápido
          options: {
            jsc: {
              parser: { syntax: 'typescript', tsx: true },
              transform: { react: { runtime: 'automatic' } },
            },
          },
        },
      },

      // CSS Global (não-modularizado)
      {
        test: /\.css$/,
        exclude: /\.module\.css$/,
        use: [
          isDev ? 'style-loader' : MiniCssExtractPlugin.loader,
          // Em dev, style-loader injeta CSS via <style> (mais rápido, suporta HMR de CSS).
          // Em prod, MiniCssExtractPlugin extrai para .css separado (melhor cache, sem FOUC).
          'css-loader',
          'postcss-loader',
        ],
      },

      // CSS Modules (arquivos *.module.css)
      {
        test: /\.module\.css$/,
        use: [
          isDev ? 'style-loader' : MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {
              modules: {
                localIdentName: isDev
                  ? '[local]__[hash:base64:5]'   // dev: legível ([name]__[hash])
                  : '[hash:base64:8]',            // prod: só hash (menor, não expõe nomes de classe)
              },
            },
          },
          'postcss-loader',
        ],
      },

      // Assets (webpack 5 nativo — sem file-loader)
      {
        test: /\.(png|jpg|gif|webp|avif)$/i,
        type: 'asset',               // 'asset': abaixo de 8KB vira inline base64; acima, emite arquivo
        parser: { dataUrlCondition: { maxSize: 8 * 1024 } },
        generator: { filename: 'images/[hash:8][ext]' },
      },
      {
        test: /\.svg$/i,
        issuer: /\.[jt]sx?$/,
        use: ['@svgr/webpack'],      // importar SVG como componente React: import Logo from './logo.svg'
      },
    ],
  },

  // ──────────────────────────────────────────────────────────────────
  // PLUGINS: orquestração do build inteiro.
  // ──────────────────────────────────────────────────────────────────
  plugins: [
    // Gera index.html com os <script> e <link> corretos injetados
    new HtmlWebpackPlugin({
      template: './public/index.html',
      minify: !isDev,
    }),

    // Em prod: extrai CSS em arquivos separados
    ...(isDev ? [] : [
      new MiniCssExtractPlugin({
        filename: 'css/[name].[contenthash:8].css',
        chunkFilename: 'css/[id].[contenthash:8].css',
      }),
    ]),
  ],

  // ──────────────────────────────────────────────────────────────────
  // OPTIMIZATION: code splitting e minificação.
  // ──────────────────────────────────────────────────────────────────
  optimization: {
    runtimeChunk: 'single',          // extrai o bootstrap do webpack em arquivo separado
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        // React e libs de UI em chunk separado (muda raramente)
        react: {
          test: /[\\/]node_modules[\\/](react|react-dom|react-router-dom|scheduler)[\\/]/,
          name: 'react-vendor',
          chunks: 'all',
          priority: 20,
        },
        // Todo o resto de node_modules
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendor',
          chunks: 'all',
          priority: -10,
        },
      },
    },
    minimizer: [
      '...', // mantém TerserPlugin (minificação de JS — ativado por mode: 'production')
      new CssMinimizerPlugin(),
    ],
  },

  // ──────────────────────────────────────────────────────────────────
  // DEV SERVER: config do webpack-dev-server.
  // ──────────────────────────────────────────────────────────────────
  devServer: {
    port: 3000,
    hot: true,                         // HMR ativado
    historyApiFallback: true,          // SPA: serve index.html para qualquer rota (client-side routing)
    open: true,
    static: { directory: path.join(__dirname, 'public') },
    // proxy: útil para evitar CORS em dev (redireciona /api para o backend)
    proxy: [
      { context: ['/api'], target: 'http://localhost:8080', changeOrigin: true },
    ],
  },

  // SOURCE MAPS: modo rápido em dev, source-map completo em prod
  devtool: isDev ? 'eval-cheap-module-source-map' : 'source-map',
};
```

> [!warning] A armadilha do config crescente
> Este config já tem ~100 linhas e ainda não inclui SVG, workers, internacionalização, análise de bundle, ou Module Federation. Um config de produção real em codebase grande chega facilmente a 300-500 linhas, frequentemente dividido em `webpack.common.js`, `webpack.dev.js` e `webpack.prod.js` com `webpack-merge`. Essa é exatamente a complexidade que Vite e outros ferramentas eliminaram com defaults sensatos e zero-config.

---

## Module Federation: o diferencial que sobrevive

Module Federation é a feature do webpack 5 (2020) que justifica continuar estudando webpack mesmo que você nunca escreva um `webpack.config.js` do zero. É genuinamente diferente de tudo que existia antes.

**O problema que resolve:** micro-frontends em runtime. Em vez de uma empresa ter um único app monolítico frontend, ela tem múltiplos times cada um dono de sua fatia da UI — time de checkout, time de catálogo, time de perfil. O problema clássico é: como você junta isso no browser sem que cada time dependa do build do outro?

A solução pré-Module Federation era iframe (funciona mas é preso) ou build em monorepo compartilhado (funciona mas cria acoplamento de deploy). Module Federation resolve de forma diferente: cada app é buildado e deployado de forma independente, e em runtime eles **carregam código uns dos outros** via URL.

```mermaid
flowchart LR
    classDef marca fill:#8855DF33,stroke:#8855DF,color:#E9ECF2
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    subgraph "Shell App (container)"
        SHELL["shell/\n(entry do usuário)\nwww.empresa.com"]
        SHELL_MF["ModuleFederationPlugin\nremotes:\n  checkout: 'checkout@https://checkout.empresa.com/mf.js'\n  catalog: 'catalog@https://catalog.empresa.com/mf.js'"]
    end

    subgraph "Checkout App (remote)"
        CHECK_MF["ModuleFederationPlugin\nexposes:\n  './CheckoutWidget': './src/CheckoutWidget.jsx'"]
        CHECK_BUILD["dist/mf.js\n(manifest de módulos expostos)\ndist/checkout.[hash].js\ndist/react-vendor.[hash].js\n(shared: react@18)"]
    end

    subgraph "Catalog App (remote)"
        CAT_MF["ModuleFederationPlugin\nexposes:\n  './ProductCard': './src/ProductCard.jsx'"]
        CAT_BUILD["dist/mf.js\ndist/catalog.[hash].js"]
    end

    SHELL -->|"import('@checkout/CheckoutWidget')\nem runtime, lazy"| CHECK_BUILD
    SHELL -->|"import('@catalog/ProductCard')\nem runtime, lazy"| CAT_BUILD
    CHECK_BUILD -.->|"shared react@18\n(se shell já carregou, reutiliza)"| SHELL

    class SHELL neutro
    class CHECK_BUILD marca
    class CAT_BUILD marca
```

> [!note] Leitura do diagrama
> O shell não tem o código de checkout ou catálogo em seu bundle. Em runtime, quando o usuário navega para o checkout, o browser baixa `checkout.empresa.com/mf.js` (o manifest de módulos expostos pelo time de checkout), descobre quais chunks contêm o `CheckoutWidget`, e os carrega. Se React já foi carregado pelo shell, o remote o reutiliza (shared deps) em vez de carregar de novo.

O config de Module Federation fica assim:

```js
// webpack.config.js do Checkout App (remote)
const { ModuleFederationPlugin } = require('webpack').container;

plugins: [
  new ModuleFederationPlugin({
    name: 'checkout',             // nome único deste remote
    filename: 'mf.js',           // manifest que o host vai buscar
    exposes: {
      './CheckoutWidget': './src/CheckoutWidget.jsx',
      './CheckoutPage': './src/pages/CheckoutPage.jsx',
    },
    shared: {
      react: { singleton: true, requiredVersion: '^18.0.0' },
      'react-dom': { singleton: true, requiredVersion: '^18.0.0' },
      // singleton: true garante que só uma instância de React rode no browser,
      // mesmo se shell e remote trouxerem versões diferentes (desde que compatíveis)
    },
  }),
],

// webpack.config.js do Shell App (host)
plugins: [
  new ModuleFederationPlugin({
    name: 'shell',
    remotes: {
      checkout: 'checkout@https://checkout.empresa.com/mf.js',
      catalog: 'catalog@https://catalog.empresa.com/mf.js',
    },
    shared: {
      react: { singleton: true },
      'react-dom': { singleton: true },
    },
  }),
],
```

No código React do shell:

```jsx
// src/pages/CheckoutRoute.jsx
import React, { lazy, Suspense } from 'react';

// import lazy de remote — carregado em runtime, não em build time
const CheckoutWidget = lazy(() => import('checkout/CheckoutWidget'));

export function CheckoutRoute() {
  return (
    <Suspense fallback={<div>Carregando checkout...</div>}>
      <CheckoutWidget />
    </Suspense>
  );
}
```

### Module Federation 2.0 — o que mudou

Em 2024, Module Federation ganhou versão 2.0, que chegou a estável em abril de 2026, e desacoplou o runtime do webpack completamente:

- **Cross-bundler**: MF 2.0 funciona com webpack, Rspack, Rollup, Rolldown, Rsbuild e Vite. Times diferentes podem usar bundlers diferentes e ainda trocar módulos em runtime.
- **TypeScript nativo**: tipos dos remotes são compartilhados automaticamente — você consome `import('checkout/CheckoutWidget')` com type-safety, sem manter pacotes de tipos manualmente.
- **Node.js support**: módulos federados podem ser consumidos em SSR e em microserviços Node — não só no browser.
- **Dev tools**: Chrome DevTools extension para inspecionar quais remotes foram carregados e com quais versões.

> [!important] Module Federation ainda depende de webpack?
> Para MF 1.x: sim, todos os apps envolvidos precisam ser buildados com webpack 5. Para MF 2.0: não necessariamente — o runtime foi extraído em `@module-federation/runtime` (pacote independente), e plugins para Vite, Rollup e Rspack estão disponíveis. A história ainda está evoluindo: suporte a Vite é considerado experimental em alguns aspectos (2026), mas a tendência é consolidação cross-bundler.

---

## Por que webpack dominou 2015–2021

A dominância do webpack não foi acidente. Ele chegou com um pacote de features que nenhuma ferramenta tinha combinado antes:

**1. Tudo em um lugar.** Antes do webpack, você precisava de Browserify para modules, Grunt/Gulp para tasks, outro plugin para CSS, outro para imagens. webpack unificou em um config (por mais verboso que seja).

**2. Code splitting real com dynamic import.** O `import()` dinâmico + code splitting automático foi revolucionário para SPAs. Sem isso, bundlar uma app grande significava jogar tudo numa única mega-query de 2MB.

**3. Dev server com HMR.** Hot Module Replacement mudou o loop de desenvolvimento. Editar um componente e ver a mudança em 100ms sem perder o estado — algo que Grunt e Gulp simplesmente não ofereciam.

**4. Ecossistema.** O npm logo foi dominado por loaders e plugins para webpack. Cada lib JS de UI tinha seu loader correspondente. Essa densidade de ecossistema criou lock-in produtivo.

**5. Adotado pelos frameworks.** Create React App (2016) e Angular CLI (2016) usavam webpack internamente. Quem usava React ou Angular estava usando webpack, mesmo sem saber. Isso garantiu dezenas de milhões de instalações.

```mermaid
timeline
    title webpack: ascensão e declínio relativo
    2014 : webpack 1.0 — nasce o conceito de "tudo é módulo"
    2015 : adoção inicial na comunidade React
    2016 : Create React App usa webpack\nAngular CLI usa webpack\n(começa a era de ouro)
    2018 : webpack 4 — modo automático\n(tree-shaking, mode production/development)
    2020 : webpack 5 — Module Federation\nAsset Modules nativos\nPersistent Caching
    2021 : Vite 2.0 — HMR 10-50x mais rápido\nmuitos projetos novos migram
    2023 : React recomenda Vite/Next oficial\nAngular 17 migra para esbuild+Vite default\nNext.js anuncia Turbopack
    2024 : Module Federation 2.0 (cross-bundler)\nRspack ganha tração como substituto drop-in
    2026 : webpack 5.107+ (latest)\n~30M downloads/sem (ainda enorme)\nRoadmap v6 em andamento\nTurbopack é padrão no Next.js dev
```

---

## Por que webpack perde espaço

86% dos devs ainda usam webpack (State of JS 2025), mas apenas 14% dizem que gostam. Esse gap entre uso e satisfação é raro em ferramentas maduras — e sinaliza uma situação de lock-in, não de preferência genuína.

Os problemas são estruturais, não de implementação:

### 1. Velocidade de desenvolvimento

webpack processa tudo através de um grafo de módulos bundlado antes de servir. Em projetos grandes (500+ módulos), o cold start do dev server pode chegar a 30-60 segundos. HMR também degrada: quando o grafo fica grande, o webpack precisa reanalisar dependências do módulo alterado antes de enviar o patch.

Vite resolve de forma diferente: em dev, não faz bundle. Serve módulos como ESM nativo, o browser faz as requisições individualmente. Cold start é quase instantâneo porque não tem bundling. HMR é sempre O(1) — só o módulo alterado é retransformado, independente do tamanho do projeto.

```mermaid
xychart-beta
    title "Cold Start comparativo (projeto ~500 módulos)"
    x-axis ["webpack 5", "Vite 5", "Rspack 1.x", "Turbopack"]
    y-axis "segundos" 0 --> 45
    bar [35, 2, 8, 3]
```

> [!warning] Benchmarks são indicativos
> Os tempos acima são representativos de reportes da comunidade em 2025-2026 (projetos React médio-grandes). Variam muito com hardware, tamanho real do projeto, e configuração. O ponto qualitativo — webpack é dramaticamente mais lento em dev que as alternativas — é consistente.

### 2. Complexidade de configuração

A flexibilidade do webpack tem um preço: não há defaults para apps modernas. Você precisa configurar explicitamente loaders para TypeScript, JSX, CSS, assets; plugins para HTML, extração de CSS, análise; optimization para splitting inteligente. O config cresce.

Vite tem defaults para TypeScript + JSX + CSS + assets **sem instalar nenhum pacote extra**. Você começa com um arquivo de ~5 linhas.

### 3. Arquitetura limitada pelo JavaScript

O core do webpack é JavaScript single-threaded. Tree-shaking, resolução de módulos, serialização de cache — tudo corre no mesmo processo V8. Ferramentas como esbuild (Go), Turbopack (Rust) e Rspack (Rust) exploram paralelismo real e tipagem estática de linguagem para atingir 5-100x mais velocidade em operações de I/O e CPU.

O webpack até pode paralelizar alguns loaders via `thread-loader`, mas é uma solução de contorno — o gargalo é arquitetural.

---

## Onde webpack ainda é a resposta certa

Honestidade obriga: existem contextos onde webpack não é legado que você quer migrar, mas a ferramenta certa.

### Apps grandes legados

Um app React com 800K linhas de código, 15 anos de loaders customizados, plugins internos, configurações para dezenas de features flags, e uma equipe de 200 devs familiarizados com o ecossistema webpack — migrar para Vite ou Turbopack tem custo real e risco real. O webpack nesses casos não é escolha de ingenuidade; é decisão de engenharia: o ROI da migração não compensa até que a dor de produtividade exceda o custo de transição.

### Module Federation (micro-frontends em runtime)

Se você precisa de micro-frontends com deploys independentes e compartilhamento de deps em runtime — e especialmente se você já tem times em webpack — Module Federation ainda é o caminho mais maduro. MF 2.0 está expandindo para cross-bundler, mas em 2026 o suporte mais completo e estável ainda é webpack + webpack.

### Next.js (em produção)

Turbopack é o default de dev no Next.js 15/16, mas o **build de produção** do Next.js ainda usa webpack por padrão. Turbopack para prod está em beta em 2026. Se você está em Next.js hoje, está usando webpack para seus builds de CI/CD, querendo ou não.

### Angular (projetos legados)

Angular 17+ usa esbuild + Vite como default para novos projetos. Mas projetos Angular pré-17 usam webpack, e a migração não é automática. Muitos apps Angular corporativos vão rodar em webpack-based browser builder por anos ainda.

> [!success] A regra de ouro
> Escolha webpack quando: (1) você tem uma codebase existente e grande demais para migrar sem ROI claro, (2) você precisa de Module Federation 1.x especificamente, ou (3) você está em Next.js e ainda não migrou o build de produção para Turbopack. Para qualquer projeto novo em 2026: use Vite.

---

## Rspack: webpack sem a lentidão

Vale mencionar aqui (com fronteira clara para a [[15 - Turbopack, Rspack e a corrida Rust-Go]]): Rspack é uma reimplementação de webpack em Rust, criada pela ByteDance, com compatibilidade quase total com a API do webpack.

O que isso significa na prática: você pode trocar `webpack` por `rspack` no `package.json` e em `webpack.config.js` trocar `require('webpack')` por `require('@rspack/core')` — e a maioria dos projetos funciona sem mais mudanças, com cold start 5-10x mais rápido.

ByteDance migrou 100.000+ módulos internos de webpack para Rspack e mede melhorias de 7-10x em tempo de build. Para times presos no webpack que não podem (ou não querem) mudar paradigma (Vite é diferente o suficiente para requerer ajustes), Rspack é o caminho pragmático.

```
# Migração de webpack para Rspack — minimal
npm remove webpack webpack-cli webpack-dev-server
npm add @rspack/core @rspack/cli

# webpack.config.js — mudança mínima
- const webpack = require('webpack');
+ const rspack = require('@rspack/core');
```

Rspack em profundidade fica na [[15 - Turbopack, Rspack e a corrida Rust-Go]].

---

## Como explicar em inglês

**webpack** is a module bundler for JavaScript applications. Its core idea is that *everything is a module*: JavaScript, CSS, images, fonts — anything you `import` can be processed by the bundler through a unified dependency graph starting at one or more **entry points**.

The build pipeline has four main concepts. **Loaders** transform individual files — `babel-loader` transpiles JSX, `css-loader` resolves CSS imports, `ts-loader` (or `swc-loader`) handles TypeScript. Each file matching a `rule` passes through the configured loader chain, right to left. **Plugins** operate on the entire compilation lifecycle — they can generate HTML files (`HtmlWebpackPlugin`), extract CSS into separate files (`MiniCssExtractPlugin`), or split the bundle intelligently (`SplitChunksPlugin`). **Output** defines how the generated chunks land on disk, with content hashes enabling long-lived browser caching.

webpack popularized **Hot Module Replacement (HMR)**: when you edit a file, only that module's patch is sent to the browser over WebSocket, without a full page reload — preserving application state during development.

**Module Federation** (webpack 5, 2020; v2.0 stable 2026) is webpack's most unique contribution: it allows independently built and deployed applications to share code *at runtime*, loading remote modules from a URL without a shared build step. This is the foundation of micro-frontend architectures where separate teams own separate parts of the UI.

webpack dominated frontend tooling from 2015 to ~2021, but its JavaScript architecture becomes a bottleneck at scale — cold starts can take 30+ seconds in large apps. Tools like Vite (native ESM in dev, no bundling) and Rspack (webpack-compatible Rust rewrite) have largely replaced webpack for new projects, while webpack persists in large legacy codebases, Next.js production builds, and Module Federation deployments.

### Vocabulário-chave

| Português | English |
|---|---|
| ponto de entrada | entry point |
| saída | output |
| transformador | loader |
| plugin | plugin |
| divisão de bundle | code splitting / chunk splitting |
| fragmento | chunk |
| fragmento inicial | initial chunk |
| fragmento assíncrono | async chunk / lazy chunk |
| substituição de módulo a quente | Hot Module Replacement (HMR) |
| federação de módulos | Module Federation |
| remoto | remote (the app exposing modules) |
| hospedeiro / shell | host / shell (the app consuming remotes) |
| deps compartilhadas | shared dependencies / singletons |
| hash de conteúdo | content hash |
| servidor de desenvolvimento | dev server |
| config verboso | verbose config / boilerplate-heavy config |
| bundler compatível | drop-in compatible bundler |
| micro-frontend | micro-frontend |

---

## Armadilhas comuns

> [!bug] "O HMR não está funcionando — a página recarrega inteira"
> O HMR requer que o módulo (ou algum módulo na cadeia de acima) implemente a interface `module.hot.accept()`. Para React, isso é feito automaticamente pelo `ReactRefreshWebpackPlugin` + `babel-plugin-react-refresh`. Sem esse setup, o webpack detecta a mudança mas não sabe como "aplicar" o módulo novo sem recarregar, então desce para full reload. Solução: adicionar `ReactRefreshWebpackPlugin` ao config e `@pmmmwh/react-refresh-webpack-plugin` como dependência.

> [!bug] "Meu bundle tem React duplicado"
> Você tem dois pacotes no `node_modules` resolvendo para versões diferentes de React (ou dois paths físicos diferentes, como em workspaces sem hoisting correto). `SplitChunksPlugin` não deduplica se as instâncias são tecnicamente diferentes. Solução: `resolve.alias: { react: path.resolve('./node_modules/react') }` para forçar uma única instância. Em Module Federation: garanta `shared: { react: { singleton: true } }`.

> [!bug] "Cada build gera hashes diferentes mesmo sem mudar o código"
> O webpack inclui metadados (como IDs de módulo e IDs de chunk) nos bundles. Se a ordem de descoberta de módulos muda entre builds, os IDs mudam, os hashes mudam. Solução: `optimization.moduleIds: 'deterministic'` e `optimization.chunkIds: 'deterministic'` (padrão no webpack 5 em mode production, mas às vezes precisa ser explícito).

> [!bug] "Module Federation: remote carrega mas dá erro de versão de React"
> Sintoma: `Error: Minified React error #321` ou conflito de contexto de React. Causa: shell e remote carregaram duas instâncias de React (versões diferentes ou não-singleton). Solução: `shared: { react: { singleton: true, requiredVersion: '^18.0.0' }, 'react-dom': { singleton: true } }` em **ambos** os configs (host e remote). O `singleton: true` diz ao MF runtime para nunca carregar duas instâncias — ele usa a primeira que foi carregada e avisa se houver incompatibilidade de versão.

> [!bug] "Build de prod funciona, dev quebra com imports de CSS"
> Em prod com `MiniCssExtractPlugin.loader` + `css-loader`, o CSS é extraído para arquivo separado. Em dev com `style-loader`, o CSS é injetado como `<style>`. O comportamento de CSS Modules (nomes de classes gerados) é o mesmo, mas se você tem side effects globais que dependem de ordem de carregamento de CSS, pode diferir. Sempre teste `npm run build && serve dist` antes de assumir que prod está ok.

> [!bug] "webpack está lento — cold start de 40 segundos"
> Para webpack legado que não pode migrar, há algumas alavancas: (1) `cache: { type: 'filesystem' }` (webpack 5) — builds seguintes usam cache persistente em disco, caindo de 40s para 5-8s; (2) `swc-loader` em vez de `babel-loader` + `ts-loader` — SWC (Rust) é 5-20x mais rápido que Babel para transpilação; (3) `thread-loader` antes de loaders pesados — paraleliza em worker threads; (4) excluir `node_modules` em todos os loaders com `exclude: /node_modules/`. Se nada disso for suficiente, considere Rspack (nota [[15 - Turbopack, Rspack e a corrida Rust-Go]]).

---

## Tree-shaking no webpack: o que funciona e o que não funciona

Tree-shaking (eliminação de código morto baseado em análise estática de exports/imports) é um dos recursos mais importantes de `mode: 'production'`, mas tem limitações que todo dev webpack precisa conhecer.

### O que o webpack analisa

webpack usa dois mecanismos complementares:

1. **`usedExports`** (ativado por mode production): marca quais exports de cada módulo são realmente usados. Terser então elimina os não-usados.
2. **`sideEffects`** (lê do `package.json` da lib): se `"sideEffects": false`, webpack pode eliminar módulos inteiros que só são importados para side effects mas cujos exports não são usados.

```js
// Exemplo: você importa só uma função de lodash-es
import { debounce } from 'lodash-es';

// Com sideEffects: false no package.json do lodash-es:
// webpack elimina os outros 200 módulos do lodash-es que você não usou.
// Sem sideEffects: false:
// webpack inclui o módulo inteiro por segurança.
```

### Limitações estruturais do tree-shaking no webpack

| Situação | Resultado |
|---|---|
| Módulo ESM com exports estáticos | Tree-shaking funciona bem |
| Módulo CJS (`module.exports = ...`) | Tree-shaking NÃO funciona — exports são dinâmicos |
| Re-export de barrel file (`export * from '...'`) | Pode funcionar, mas barrels grandes degradam o tree-shaking |
| Side effects em módulos (ex: auto-registro de plugins) | `sideEffects: false` quebraria o comportamento — não declare |
| Dynamic import com variável (`import(variable)`) | webpack não pode analisar estaticamente — inclui tudo |
| Classe com métodos não usados | Terser elimina o método, mas webpack inclui a classe |

```js
// Anti-padrão comum: barrel file que quebra tree-shaking
// src/components/index.ts
export { Button } from './Button';
export { Modal } from './Modal';
export { Table } from './Table';
// ... 50 exports

// O problema: mesmo que você importe só Button, o webpack precisa
// processar o grafo completo do barrel pra saber que os outros não têm side effects.
// Com 50 exports, isso cria 50 módulos no grafo mesmo que 48 sejam eliminados depois.

// Solução: import direto (mais verboso, mas otimizado)
import { Button } from './components/Button'; // não passa pelo barrel
```

> [!warning] CJS e tree-shaking: o elefante na sala
> A maioria das libs de UI no npm ainda publica CJS como formato principal (mesmo em 2026). `react`, `lodash`, `moment`, e muitas outras usam CJS — e webpack não consegue fazer tree-shaking em CJS. A solução de longo prazo é que libs publiquem ESM (via campo `"exports"` no package.json). Enquanto isso: use alternativas ESM-first quando disponíveis (lodash-es em vez de lodash, date-fns em vez de moment).

---

## webpack em 2026: onde está e para onde vai

A percepção de que "webpack está morto" é errada — ele está em manutenção ativa e tem um roadmap ambicioso. O que mudou é o contexto: ele não é mais a escolha default para projetos novos, mas continua sendo um player importante.

### Estado atual: webpack 5.107+ (junho 2026)

webpack 5 está em versão `5.107+` no momento desta escrita (junho 2026). As adições mais significativas desde o lançamento do 5.0 (2020):

- **Asset Modules nativos** (5.0): substituiu file-loader, url-loader, raw-loader
- **Module Federation 1.x** (5.0): micro-frontends em runtime
- **Persistent Cache filesystem** (5.0): cache em disco, invalidação inteligente
- **Improved tree-shaking** (5.x): `sideEffects` mais preciso, inner-module tree-shaking
- **Real Content Hash** (5.x): content hash agora é baseado no conteúdo real do asset, não no conteúdo intermediário — evita invalidação desnecessária
- **Lazy Compilation** (experimental, 5.x): em dev, compila entry points e chunks assíncronos só quando são acessados pela primeira vez — reduz cold start em MPAs grandes

### Roadmap webpack v6 (publicado fev. 2026)

O roadmap oficial (publicado no blog do webpack em fevereiro de 2026) anuncia features que chegarão no webpack 6:

```
Roadmap webpack 6 (previsão 2026-2027):
├── Native CSS: processar CSS sem css-loader (como Asset Modules fez pra imagens)
│   → import './styles.css' funcionará sem nenhum loader instalado
├── Universal Target: um único target que funciona em browser, Node, Bun, Deno e Edge Workers
│   → elimina a necessidade de configs separados por ambiente
├── TypeScript transpilation builtin: transpilação TS nativa sem ts-loader ou swc-loader
│   → webpack core em TS → pode usar o próprio compilador internamente
└── Path to v6: API de plugin mais limpa, remoção de deprecated APIs do v4/v5
```

> [!info] Native CSS no webpack 6 vs. css-loader hoje
> Native CSS não elimina todas as funcionalidades do css-loader — CSS Modules, PostCSS, autoprefixer ainda precisam de processamento. O que elimina é a necessidade de loaders para o caso básico: `import './reset.css'` funcionará out-of-the-box, assim como já funciona no Vite. Para CSS Modules e PostCSS, ainda haverá configuração, mas mais simples.

### webpack vs. concorrentes em 2026: posicionamento real

```mermaid
quadrantChart
    title "Bundlers em 2026: Velocidade vs. Compatibilidade com ecossistema webpack"
    x-axis "Baixa compatibilidade" --> "Alta compatibilidade webpack"
    y-axis "Lento" --> "Rápido"
    quadrant-1 "Ideal para migração"
    quadrant-2 "Novo projeto"
    quadrant-3 "Legacy lock-in"
    quadrant-4 "Drop-in upgrade"
    "webpack": [0.9, 0.2]
    "Rspack": [0.85, 0.75]
    "Vite": [0.2, 0.85]
    "Turbopack": [0.5, 0.88]
    "esbuild": [0.15, 0.95]
    "Rollup": [0.2, 0.5]
```

> [!note] Leitura do quadrante
> webpack tem altíssima compatibilidade com seu próprio ecossistema (plugins, loaders, config) mas é o mais lento. Rspack é o único que combina alta compatibilidade com boa velocidade — daí sua proposta de "drop-in replacement". Vite e esbuild são rápidos mas requerem reaprender ou reconfigurar o ecossistema. Turbopack (Next.js) fica no meio: mais rápido que webpack, mas ainda longe de ser compatível com plugins webpack arbitrários.

### Downloads e saúde do ecossistema (2026)

| Ferramenta | Downloads semanais (aprox. jun. 2026) | Tendência |
|---|---|---|
| webpack | ~30M | estável (não cresce, não cai) |
| Vite | ~25M | crescimento acelerado |
| esbuild | ~40M | estável (usado por Vite internamente) |
| Rspack | ~2M | crescimento forte |
| Turbopack | incluído no Next.js | n/d |

> [!important] A leitura correta dos números
> webpack ter 30M downloads semanais não significa que 30M projetos novos/semana estão escolhendo webpack. Significa que 30M builds/semana acontecem em projetos existentes — muitos deles em CI de projetos legados, Next.js (que usa webpack em prod), e Angular pré-17. É uso inercial, não adoção nova. A diferença importa para entender o futuro.

---

## Veja também

- [[07 - O grafo de módulos e o que é bundling]] — o modelo mental de entry point, grafo de dependências, e o que um bundler faz antes de chegar no webpack especificamente
- [[06 - ESM e CJS e o sistema de módulos]] — por que CJS quebra tree-shaking e por que ESM é pré-requisito para análise estática de exports; essencial para entender as limitações do webpack com libs legadas
- [[08 - Transpilação e targets]] — babel-loader e swc-loader no contexto do webpack: o que transpilação faz, por que SWC é 5-20x mais rápido que Babel, e como `targets` determina o output
- [[09 - Dev server e HMR]] — o conceito de HMR em profundidade: como o protocolo WebSocket funciona, o papel do `module.hot.accept`, e como Vite implementa HMR diferente do webpack
- [[10 - Ferramentas legadas - Grunt, Gulp, Bower, Browserify e RequireJS]] — o contexto do "mundo antes do webpack": por que Browserify não era suficiente e o que o webpack resolveu que os task runners não resolviam
- [[12 - Create React App e a era dos scaffolders]] — como o CRA popularizou webpack sem expor a complexidade, criando uma geração de devs que usavam webpack sem saber configurá-lo
- [[13 - Vite a fundo]] — a alternativa moderna ao webpack para projetos novos: ESM nativo em dev, Rollup em prod, zero-config para TypeScript/JSX/CSS
- [[14 - Rollup, esbuild e Rolldown]] — as ferramentas que influenciaram Vite e que frequentemente aparecem como alternativas ao webpack em contextos de lib (Rollup) ou performance extrema (esbuild)
- [[15 - Turbopack, Rspack e a corrida Rust-Go]] — Rspack (drop-in replacement do webpack em Rust) e Turbopack (substituto do webpack no Next.js)
- [[17 - Otimização de bundle]] — tree-shaking a fundo, estratégias de code splitting, análise de bundle, e o que impede o webpack (e outros bundlers) de eliminar código morto
- [[21 - Monorepos - workspaces, Turborepo, Nx e changesets]] — como webpack se comporta em monorepos, o problema de resolução cross-workspace, e como ferramentas como Nx abstraem configs de webpack por cima

---

> [!info] Lastro
> 1. webpack — Documentação oficial, Concepts (entry, output, loaders, plugins, mode). Disponível em: https://webpack.js.org/concepts/
> 2. webpack — "Under The Hood" (documentação oficial). Descreve `ModuleGraph`, `ChunkGraph`, a hierarquia entry → chunk group → chunk → asset, e os tipos initial vs. non-initial. Disponível em: https://webpack.js.org/concepts/under-the-hood/
> 3. webpack — "Roadmap 2026" (blog oficial, fev. 2026). Native CSS support, universal target, TypeScript transpilation builtin, path to v6. Disponível em: https://webpack.js.org/blog/2026-02-04-roadmap-2026/
> 4. webpack — Documentação oficial, Tapable (Plugins API). Explica os tipos de hooks (SyncHook, AsyncSeriesHook, etc.), o sistema `tap`/`tapAsync`/`tapPromise`, e como escrever plugins customizados. Disponível em: https://webpack.js.org/api/plugins/
> 5. webpack — Documentação oficial, Cache (filesystem cache). Explica `cache.type: 'filesystem'`, `buildDependencies`, invalidação de cache e integração com CI. Disponível em: https://webpack.js.org/configuration/cache/
> 6. webpack — Documentação oficial, Externals. Explica como excluir dependências do bundle (CDN, peer deps de libs), incluindo as formas por target (UMD, CommonJS). Disponível em: https://webpack.js.org/configuration/externals/
> 7. webpack — Documentação oficial, Tree Shaking guide. Explica `usedExports`, `sideEffects`, e as limitações do tree-shaking com módulos CJS vs ESM. Disponível em: https://webpack.js.org/guides/tree-shaking/
> 8. InfoQ — "Module Federation 2.0 Reaches Stable Release with Wider Support outside of Webpack" (abr. 2026). Cross-bundler support (webpack, Rspack, Vite, Rolldown), TypeScript type sharing, Node.js runtime. Disponível em: https://www.infoq.com/news/2026/04/module-federation-2-stable/
> 9. InfoQ — "Webpack Publishes 2026 Roadmap with Native CSS Support, Universal Target, and Path to Version 6" (mar. 2026). Disponível em: https://www.infoq.com/news/2026/03/webpack-2026-roadmap/
> 10. PkgPulse — "Rspack vs Webpack in 2026: The Rust-Powered Drop-In Replacement" (2026). ByteDance migração de 100K+ módulos, benchmark comparativo. Disponível em: https://www.pkgpulse.com/blog/rspack-vs-webpack-2026
> 11. Tech Insider — "Vite vs Webpack 2026: 24x HMR Speed and 115M Downloads" (2026). Disponível em: https://tech-insider.org/vite-vs-webpack-2026-2/
> 12. DEV Community — "Native Federation vs Webpack Module Federation — Which Should You Choose in 2026?" (2026). Disponível em: https://dev.to/mhmoud_ashour_5547515422e/native-federation-vs-webpack-module-federation-which-should-you-choose-in-2026-109m
> 13. FrontScope — "Vite vs Webpack vs Rspack: The Build Tool Showdown (2026)" (2026). Disponível em: https://frontscope.dev/blog/vite-vs-webpack-vs-rspack-2026/
