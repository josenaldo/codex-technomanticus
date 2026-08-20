---
title: "Compressão e minificação"
created: 2026-07-06
updated: 2026-07-06
type: concept
status: seedling
fase: adepto
tags:
  - web-performance
  - carregamento
  - compressão
  - brotli
publish: true
---

# Compressão e minificação

> [!abstract] TL;DR
> Todo recurso de texto — HTML, CSS, JS, SVG, JSON — deve viajar comprimido. **Minificação** remove o que é redundante *para humanos* (espaços, comentários, nomes longos) antes de servir; **compressão** (gzip ou **Brotli**) reduz os bytes *na transferência*, e o browser descomprime. As duas são complementares e se somam: você minifica **e** comprime. O Brotli bate o gzip em ~15–25% para texto e é suportado por todos os browsers modernos. Assets estáticos devem ser pré-comprimidos no nível máximo em build; conteúdo dinâmico, comprimido on-the-fly num nível mais leve. Imagens e vídeo **não** entram aqui — já são formatos comprimidos (nota 04).

## O problema: você está enviando ar pela rede

Um bundle de JavaScript "de verdade" tem indentação, comentários, nomes de variáveis descritivos, quebras de linha — tudo essencial para *você ler*, e completamente inútil para o *browser executar*. Servir esse arquivo cru é enviar, literalmente, megabytes de espaços em branco e comentários pela rede do usuário.

Pior: mesmo depois de tirar o supérfluo, o texto que sobra tem enorme redundância estatística (a palavra `function`, `const`, `return` se repete milhares de vezes). Enviar isso sem compressão é desperdiçar banda que o usuário no celular paga em tempo — e o tempo vira LCP e FCP altos. Duas técnicas independentes atacam os dois desperdícios.

## Minificação: remover o que é para humanos

**Minificar** é reescrever o código para a menor forma equivalente antes de servir: remove espaços, quebras de linha e comentários; encurta nomes de variáveis locais (`usuarioAtual` → `u`); elimina código morto. O resultado é ilegível para humanos, mas **idêntico em comportamento** para o browser.

```js
// Antes (o que você escreve)
function calcularTotal(itens) {
  // soma os preços
  return itens.reduce((acc, item) => acc + item.preco, 0);
}

// Depois (o que você serve)
function calcularTotal(t){return t.reduce((e,r)=>e+r.preco,0)}
```

Ferramentas de build fazem isso automaticamente (esbuild, Terser, SWC para JS; cssnano para CSS). Esse é o território de [[03-Dominios/Tecnologia/Tooling e Build/17 - Otimização de bundle|Tooling 17 — Otimização de bundle]], que cobre também tree-shaking e code-splitting. Aqui, o ponto é: **minificação é pré-requisito, não opcional** — nenhum texto deve ir para produção sem passar por ela.

## Compressão: reduzir a redundância na transferência

A **compressão** age numa camada diferente: o servidor comprime o arquivo (já minificado) antes de enviar, o browser descomprime ao receber, transparentemente. É negociada via cabeçalhos HTTP: o browser diz o que aceita (`Accept-Encoding: gzip, br`), o servidor responde com o que usou (`Content-Encoding: br`).

Dois algoritmos dominam:

| Algoritmo | Ganho em texto | Suporte | Nota |
|-----------|----------------|---------|------|
| **gzip** | referência | universal | o piso; sempre disponível |
| **Brotli** (`br`) | ~15–25% melhor que gzip | todos os browsers modernos | primeira escolha para texto |

O Brotli é o padrão moderno para recursos de texto — melhor compressão pelo mesmo (ou menor) custo de descompressão. gzip continua como fallback universal.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
graph LR
    A[código-fonte] -->|minifica em build| B[minificado]
    B -->|comprime em build/servidor| C["Brotli (ou gzip)"]
    C -->|Content-Encoding: br| D[Browser]
    D -->|descomprime| E[executa]
    style B fill:#4A90D9,color:#fff
    style C fill:#4A90D9,color:#fff
    style E fill:#F5A623,color:#000
```

## Estático vs dinâmico: o nível de compressão importa

Comprimir custa CPU, e o custo cresce com o nível. A estratégia certa depende de *quando* você comprime:

- **Assets estáticos** (o seu bundle JS/CSS, que não muda entre requisições): comprima **uma vez, em build, no nível máximo** (Brotli nível 11). O custo de CPU é pago uma vez; todo usuário recebe o menor arquivo possível. Servidores e CDNs servem o `.br` pré-gerado.
- **Conteúdo dinâmico** (HTML gerado por requisição): comprima **on-the-fly, num nível mais leve** (Brotli 4–5 ou gzip). Aqui você não pode gastar o nível 11 a cada requisição — a latência de CPU comeria o ganho de banda.

> [!warning] Comprimir o que já é comprimido
> **O que acontece:** o time habilita compressão gzip/Brotli para *tudo*, incluindo imagens, vídeos e fontes `woff2`, e ganha ~0% — às vezes os arquivos até incham um pouco. **Por quê:** JPEG, PNG, AVIF, WebP, MP4 e `woff2` **já são formatos comprimidos**. Passar um compressor de propósito geral por cima não acha mais redundância; só gasta CPU. **Como evitar:** comprima apenas recursos de **texto** (HTML, CSS, JS, SVG, JSON, `.ico` em alguns casos). Deixe os formatos binários já otimizados em paz — a otimização deles é a da [[03-Dominios/Tecnologia/Web Performance/Performance de Carregamento/04 - Otimização de imagens|nota 04]].

> [!question]- Se eu minifico, ainda preciso comprimir? E vice-versa?
> Sim, as duas — elas atacam redundâncias diferentes e se somam. **Minificação** remove o que é redundante *semanticamente* (comentários, espaços, nomes longos): reduz o texto antes de qualquer coisa. **Compressão** remove redundância *estatística* (padrões repetidos de bytes) no momento da transferência. Um arquivo minificado ainda comprime muito bem, porque `function`/`return`/`const` continuam se repetindo. Minificar sem comprimir deixa banda na mesa; comprimir sem minificar envia comentários comprimidos. Faça as duas.

**Compressão e minificação em uma frase:** minifique todo texto em build (remove o que é para humanos) e comprima-o com Brotli (fallback gzip) na transferência — estático no nível máximo pré-gerado, dinâmico num nível leve on-the-fly —, deixando de fora os formatos binários que já são comprimidos.

## Como explicar em inglês

> "Every text resource should travel compressed, and it's two complementary steps. **Minification** strips what's there for humans — whitespace, comments, long variable names — at build time. **Compression** — gzip or Brotli — removes statistical redundancy during transfer, and the browser decompresses transparently via `Content-Encoding`. Brotli beats gzip by roughly 15–25% on text and is supported everywhere modern. For static assets I pre-compress at max level once in build; for dynamic HTML I compress on the fly at a lighter level. And I never compress images or fonts — they're already compressed formats."

| PT | EN |
|----|----|
| Minificação | Minification |
| Compressão | Compression |
| Nível de compressão | Compression level |
| Pré-comprimido | Pre-compressed |
| Negociação de conteúdo | Content negotiation |
| Código morto | Dead code |

## O que vem a seguir

Comprimir reduz o *tamanho* de cada download. A próxima vitória é ainda mais radical: **não baixar de novo** o que o usuário já tem. Cache HTTP e CDN transformam a segunda visita (e a navegação entre páginas) em quase instantâneas.

- [[03-Dominios/Tecnologia/Web Performance/Performance de Carregamento/07 - Cache e CDN|07 — Cache e CDN]] — `Cache-Control`, immutable, hashing de assets e edge.
- [[03-Dominios/Tecnologia/Tooling e Build/17 - Otimização de bundle|Tooling 17]] — minificação, tree-shaking e code-splitting no build, como reforço.

## Fontes

- **web.dev (Google)** — [*Reduce network payloads using text compression*](https://web.dev/articles/reduce-network-payloads-using-text-compression) — gzip vs Brotli e como habilitar.
- **MDN Web Docs** — [*Content-Encoding*](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Encoding) — a negociação de compressão via HTTP.
- **web.dev (Google)** — [*Minify JavaScript / CSS*](https://web.dev/articles/reduce-network-payloads-using-text-compression) — minificação como pré-passo da compressão.
