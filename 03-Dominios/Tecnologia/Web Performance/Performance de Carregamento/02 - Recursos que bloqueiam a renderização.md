---
title: "Recursos que bloqueiam a renderização"
created: 2026-07-06
updated: 2026-07-06
type: concept
status: seedling
fase: iniciado
tags:
  - web-performance
  - carregamento
  - render-blocking
  - critical-css
publish: true
---

# Recursos que bloqueiam a renderização

> [!abstract] TL;DR
> Dois tipos de recurso travam o Critical Rendering Path: **CSS** (bloqueia o *paint* — nada aparece até o CSSOM ficar pronto) e **JavaScript síncrono** (bloqueia o *parse* do DOM — o browser congela ao encontrar um `<script>`). As armas para desarmá-los: em JS, `defer` (executa depois do parse, na ordem) e `async` (executa assim que baixa, fora de ordem); em CSS, extrair o **critical CSS** (o mínimo para a dobra) inline e carregar o resto de forma assíncrona. Regra de ouro: **só o que a primeira tela precisa deve bloquear; todo o resto espera.**

## O problema: o HTML chegou, mas a tela está branca

Na [[03-Dominios/Tecnologia/Web Performance/Performance de Carregamento/01 - O Critical Rendering Path|nota anterior]] vimos que o browser lê o HTML incrementalmente — então, em tese, o conteúdo deveria aparecer quase na hora. Na prática, uma folha de estilo de 200 KB no `<head>` e três `<script>` de analytics no meio do `<body>` transformam esse fluxo numa tela em branco de vários segundos.

Por quê? Porque esses recursos **bloqueiam** o caminho. E aqui está a boa notícia: *quais* recursos bloqueiam, e *como* impedi-los de bloquear, é algo que você controla com poucas mudanças de altíssimo impacto. Esta é a otimização de carregamento com melhor relação esforço/retorno que existe.

## CSS: o bloqueador do paint

O browser **não pinta nada** enquanto não tiver o CSSOM completo. A razão é sensata: se ele pintasse com o CSS pela metade, você veria um flash de página crua (o famoso FOUC — Flash of Unstyled Content) e depois um pulo quando o estilo chegasse. Para evitar isso, o CSS é tratado como **render-blocking** por padrão.

O custo: cada arquivo CSS no `<head>` adia o **primeiro pixel** (o FCP) até baixar e ser processado. Um `<link rel="stylesheet">` para um framework de 300 KB é um pedágio que *toda* renderização paga.

A solução tem duas frentes:

**1. Critical CSS inline.** Extraia o CSS mínimo necessário para renderizar a **primeira tela** (a "dobra") e coloque-o inline, num `<style>` no `<head>`. Assim o browser pinta a parte visível **sem esperar nenhuma requisição de rede**.

**2. Carregue o resto de forma assíncrona.** O CSS não-crítico (rodapé, modais, telas abaixo da dobra) é carregado sem bloquear, com um truque de `media`:

```html
<!-- Bloqueia: o CSS crítico da dobra, inline -->
<style>/* ...critical css... */</style>

<!-- Não bloqueia: carrega assíncrono e "liga" quando chega -->
<link rel="stylesheet" href="/resto.css" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="/resto.css"></noscript>
```

O truque `media="print"` faz o browser baixar o arquivo sem tratá-lo como render-blocking (ele acha que é só para impressão); o `onload` troca para `all` assim que chega, aplicando os estilos. O `<noscript>` garante o fallback sem JS.

> [!question]- Se eu colocar todo o CSS inline, resolvo de vez o bloqueio?
> Não — você troca um problema por outro. CSS inline não é cacheável entre páginas (vai junto do HTML toda vez) e infla o tamanho do HTML, o que atrasa o próprio parse do DOM. O certo é o **crítico** inline (pequeno, só a dobra) e o resto em arquivo externo cacheável, carregado assíncrono. É um equilíbrio: inline demais engorda o HTML; externo demais bloqueia o paint. O critical CSS é a linha entre os dois.

## JavaScript: o bloqueador do parse

Quando o browser, montando o DOM, encontra um `<script>` **sem atributo**, ele para tudo: pausa a construção do DOM, baixa o script, executa, e só então retoma. A razão histórica é que o script pode conter `document.write` e alterar o próprio HTML que está sendo lido — então o browser não ousa continuar.

O resultado é brutal: um `<script src>` de terceiros lento no `<head>` pode segurar a página inteira por segundos. A solução são dois atributos que dizem ao browser "não me espere":

```html
<!-- ❌ Bloqueia o parse do DOM até baixar E executar -->
<script src="app.js"></script>

<!-- ✅ defer: baixa em paralelo, executa DEPOIS do DOM pronto, na ORDEM -->
<script src="app.js" defer></script>

<!-- ✅ async: baixa em paralelo, executa ASSIM QUE CHEGA, fora de ordem -->
<script src="analytics.js" async></script>
```

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
graph TB
    subgraph SYNC["&lt;script&gt; (síncrono)"]
        S1[Parse DOM] --> S2[⏸ PARA] --> S3[baixa+executa] --> S4[retoma parse]
    end
    subgraph DEFER["defer"]
        D1[Parse DOM segue] -.baixa em paralelo.-> D2[executa após DOM, na ordem]
    end
    subgraph ASYNC["async"]
        A1[Parse DOM segue] -.baixa em paralelo.-> A2[executa ao chegar, fora de ordem]
    end
    style S2 fill:#D0021B,color:#fff
    style D1 fill:#4A90D9,color:#fff
    style A1 fill:#4A90D9,color:#fff
```

Como escolher:

| Atributo | Baixa | Executa | Ordem preservada | Use para |
|----------|-------|---------|------------------|----------|
| (nenhum) | bloqueando | na hora, bloqueando | sim | quase nada — evite |
| **`defer`** | em paralelo | após o DOM pronto | **sim** | scripts da sua app que dependem do DOM ou uns dos outros |
| **`async`** | em paralelo | assim que baixa | **não** | scripts independentes (analytics, tags) que não dependem de nada |

Na dúvida, **`defer` é o padrão seguro**: não bloqueia, roda com o DOM pronto, e mantém a ordem. `async` é para o que é genuinamente independente. Um `type="module"` já é `defer` por padrão.

> [!warning] Usar `async` em scripts com dependências
> **O que acontece:** você marca `jquery.js` e `usa-jquery.js` ambos como `async`, e a página quebra intermitentemente com "$ is not defined". **Por quê:** `async` executa **na ordem de chegada**, não na ordem do HTML. Se o segundo script baixar antes do primeiro, ele roda antes — e a dependência não existe ainda. A falha é de corrida, então aparece "às vezes", o que a torna traiçoeira. **Como evitar:** use `defer` (preserva a ordem) para qualquer conjunto de scripts com dependência entre si. Reserve `async` para o que é ilhado.

> [!warning] "Colocar o script no fim do body resolve"
> **O que acontece:** o time move os `<script>` para antes de `</body>` e considera o problema resolvido. **Por quê:** ajuda (o DOM já está quase pronto quando o script roda), mas o script no fim do body **ainda é síncrono** — ele bloqueia o parse do pouco que resta e, sobretudo, só *começa a baixar* quando o parser chega nele, tarde. Com `defer`, o download começa cedo, em paralelo, e a execução espera o fim — melhor dos dois mundos. **Como evitar:** prefira `defer` no `<head>` a `<script>` síncrono no fim do body.

**Recursos render-blocking em uma frase:** CSS bloqueia o paint e JS síncrono bloqueia o parse, então você inlina o critical CSS e adia o resto, e marca seus scripts com `defer` (dependentes, na ordem) ou `async` (independentes) — deixando bloquear apenas o mínimo que a primeira tela realmente precisa.

## Como explicar em inglês

> "Two things block the rendering path. **CSS is render-blocking** — the browser won't paint until the CSSOM is ready — so I inline the **critical CSS** for above-the-fold content and load the rest asynchronously. And **synchronous JavaScript is parser-blocking** — the browser stops building the DOM when it hits a plain `<script>`. The fix is `defer` or `async`: `defer` downloads in parallel and runs after the DOM is ready, in order — that's my default; `async` runs as soon as it arrives, out of order, which is fine only for independent scripts like analytics."

| PT | EN |
|----|----|
| Bloqueia a renderização | Render-blocking |
| Bloqueia o parser | Parser-blocking |
| CSS crítico | Critical CSS |
| Acima da dobra | Above the fold |
| Adiar / diferir | To defer |
| Flash de conteúdo não-estilizado | Flash of Unstyled Content (FOUC) |

## O que vem a seguir

Desarmar os bloqueadores acelera o *começo* do carregamento. Mas há um passo além do "não me atrapalhe": você pode dizer ao browser, proativamente, **o que buscar antes** e **com que prioridade** — abrir conexões cedo, pré-carregar a imagem do LCP, subir a prioridade do que importa. São os resource hints.

- [[03-Dominios/Tecnologia/Web Performance/Performance de Carregamento/03 - Resource hints e prioridade|03 — Resource hints e prioridade]] — `preconnect`, `preload`, `prefetch`, `fetchpriority`.
- [[03-Dominios/Tecnologia/CSS/12 - Performance CSS|CSS 12 — Performance CSS]] — o custo de renderização do próprio CSS, como reforço.

## Fontes

- **web.dev (Google)** — [*Render-blocking resources*](https://web.dev/articles/render-blocking-resources) — CSS e JS que travam o caminho e como mitigar.
- **web.dev (Google)** — [*Defer non-critical CSS*](https://web.dev/articles/defer-non-critical-css) — o padrão de critical CSS inline + carregamento assíncrono.
- **MDN Web Docs** — [*`<script>`: async e defer*](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#attr-async) — semântica exata dos dois atributos.
