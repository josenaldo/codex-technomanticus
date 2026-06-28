---
title: "SEO técnico e metadados"
created: 2026-06-27
updated: 2026-06-27
type: note
fase: Magus
tags:
  - html
  - frontend
  - web
  - seo
  - metadados
  - entrevista
publish: true
---

# SEO técnico e metadados

> [!abstract] TL;DR
> SEO técnico é o que os mecanismos de busca enxergam antes de renderizar CSS ou JS: o HTML cru, o `<head>`, os metadados estruturados, e os sinais de rastreabilidade (`robots.txt`, `sitemap.xml`, `canonical`). Conteúdo de qualidade ainda é o fator dominante, mas erros técnicos — título duplicado, canonical errado, marcação de schema mal-formada — podem sabotar qualquer esforço editorial.

---

## O `<head>`: o que o crawler vê primeiro

O `<head>` é invisível para o usuário mas é a primeira coisa que um crawler lê. Ele define identidade, rastreabilidade, idioma e como o conteúdo será representado em buscadores e redes sociais.

```mermaid
mindmap
  root("`**\<head\>**`")
    Identidade
      "`\<title\>`"
      "`\<meta name=description\>`"
      "`\<link rel=canonical\>`"
    Rastreabilidade
      "`\<meta name=robots\>`"
      "`robots.txt`"
      "`sitemap.xml`"
    Aparência social
      "`Open Graph (og:)`"
      "`Twitter Card`"
    Internacionalização
      "`\<html lang\>`"
      "`\<link rel=alternate hreflang\>`"
    Performance
      "`\<link rel=preload\>`"
      "`\<link rel=preconnect\>`"
    Técnico
      "`\<meta charset\>`"
      "`\<meta name=viewport\>`"
```

---

## `<title>` — o elemento mais importante para SEO on-page

```html
<title>Como usar ARIA em formulários — Guia Prático | MeuSite</title>
```

Regras de ouro:
- **50–60 caracteres** — o Google trunca acima disso na SERP
- **Palavra-chave principal no início** — mais peso na relevância
- **Único por página** — títulos duplicados confundem crawlers e usuários
- **Descreve a página, não o site** — o nome do site pode ficar no final (separado por `|` ou `–`)

O que evitar:
```html
<!-- ❌ Muito longo — truncado na SERP -->
<title>Aprenda tudo sobre acessibilidade web em HTML5 com exemplos práticos e exercícios avançados</title>

<!-- ❌ Keyword stuffing -->
<title>HTML, HTML5, HTML semântico, acessibilidade HTML, aprender HTML</title>

<!-- ❌ Título padrão que aparece em todas as páginas -->
<title>MeuSite - Home</title>
```

---

## `<meta name="description">` — o texto do snippet

```html
<meta
  name="description"
  content="Aprenda ARIA: roles, states, properties e live regions. Com exemplos práticos e padrões do WAI-ARIA APG para formulários e widgets customizados."
>
```

- **150–160 caracteres** — Google pode exibir mais, mas trunca na mobile
- **Não é fator de ranking direto** — mas influencia CTR (click-through rate)
- **Pode ser ignorada** — o Google frequentemente substitui por trecho do conteúdo da página que considera mais relevante para a query
- **Única por página** — meta descriptions duplicadas reduzem CTR por parecer conteúdo replicado

> [!info] Google gera seus próprios snippets
> O Google usa a meta description como candidato mas frequentemente a ignora em favor de um trecho da página que considera mais relevante para a query específica. Isso não significa que a meta description não importa — importa para outros buscadores e para redes sociais.

---

## `<link rel="canonical">` — evitar conteúdo duplicado

O canonical declara a URL "oficial" de uma página. Essencial quando o mesmo conteúdo é acessível por múltiplas URLs:

```html
<!-- Na versão canônica e em todas as variantes -->
<link rel="canonical" href="https://meusite.com/artigo/aria-em-formularios">
```

Casos de uso comuns:

| Situação | Problema | Solução |
|---|---|---|
| `?utm_source=` em URL | `artigo.html?utm_source=newsletter` e `artigo.html` indexados separados | Canonical aponta para URL limpa |
| HTTP e HTTPS | Versões duplicadas | Canonical + redirect 301 para HTTPS |
| `www` e sem `www` | Versões duplicadas | Canonical + redirect 301 para versão preferida |
| Paginação | `/lista` e `/lista?page=2` | Canonical para a primeira página (ou `rel="next"/"prev"` — deprecated mas ainda usado) |
| Print/mobile versions | `/artigo` e `/artigo?print=1` | Canonical para a versão principal |

```html
<!-- Página 1 de uma lista paginada -->
<link rel="canonical" href="https://meusite.com/blog">

<!-- Página 2 — aponta para a primeira -->
<!-- (estratégia simplificada: consolidar link juice na página 1) -->
<link rel="canonical" href="https://meusite.com/blog">

<!-- Alternativa: cada página tem canonical para si mesma -->
<link rel="canonical" href="https://meusite.com/blog?page=2">
```

---

## `<meta name="robots">` — controlar rastreamento e indexação

```html
<!-- Índice a página, siga os links (padrão — não precisa declarar) -->
<meta name="robots" content="index, follow">

<!-- Não indexe mas siga links (ex: página de login, área privada) -->
<meta name="robots" content="noindex, follow">

<!-- Não indexe e não siga links -->
<meta name="robots" content="noindex, nofollow">

<!-- Não exiba snippet na SERP (respeito a LGPD/GDPR) -->
<meta name="robots" content="nosnippet">

<!-- Máximo de caracteres no snippet -->
<meta name="robots" content="max-snippet:160">

<!-- Não use imagem em destaque no snippet -->
<meta name="robots" content="noimageindex">
```

Diferença entre `<meta robots>` e `robots.txt`:
- `robots.txt` bloqueia o **acesso** ao arquivo — o crawler não rastreia
- `<meta robots>` instrui o que fazer **após** rastrear — o crawler acessa, lê, mas não indexa
- Para páginas que não devem aparecer na busca: use `<meta name="robots" content="noindex">`
- Para bloquear rastreamento de recursos pesados (CSS, imagens): `robots.txt` (evita uso de crawl budget)

---

## Dados estruturados — Schema.org e JSON-LD

Dados estruturados permitem que buscadores entendam o conteúdo de forma semântica e exibam **rich results** (estrelas de avaliação, FAQ expandida, breadcrumb, receitas, eventos).

**JSON-LD é o formato preferido do Google** — fica em um `<script>` separado, sem interferir no HTML:

```html
<!-- Artigo com autor e data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Como usar ARIA em formulários",
  "author": {
    "@type": "Person",
    "name": "João Silva"
  },
  "datePublished": "2026-06-27",
  "dateModified": "2026-06-27",
  "image": "https://meusite.com/imagens/aria-formularios.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "MeuSite",
    "logo": {
      "@type": "ImageObject",
      "url": "https://meusite.com/logo.png"
    }
  }
}
</script>

<!-- FAQ — gera rich result expandido na SERP -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "O que é ARIA?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "ARIA (Accessible Rich Internet Applications) é uma especificação de atributos HTML que melhora a acessibilidade para tecnologias assistivas."
      }
    },
    {
      "@type": "Question",
      "name": "Quando usar role='button'?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Somente quando não é possível usar um elemento <button> nativo."
      }
    }
  ]
}
</script>

<!-- BreadcrumbList -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://meusite.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Tecnologia",
      "item": "https://meusite.com/tecnologia"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "HTML"
    }
  ]
}
</script>
```

> [!tip] Microdata e RDFa
> Existem outros formatos (Microdata inline no HTML, RDFa), mas JSON-LD é recomendado pelo Google para novos projetos — é mais fácil de manter, não polui o HTML e pode ser gerado dinamicamente.

---

## Open Graph e Twitter Cards — redes sociais

Quando uma URL é compartilhada, redes sociais leem as meta tags OG (Open Graph) para montar o preview:

```html
<!-- Open Graph — Facebook, LinkedIn, WhatsApp, Slack, Telegram -->
<meta property="og:type" content="article">
<meta property="og:title" content="Como usar ARIA em formulários">
<meta property="og:description" content="Guia prático com exemplos de roles, states e live regions.">
<meta property="og:image" content="https://meusite.com/og/aria-formularios.jpg">
<meta property="og:url" content="https://meusite.com/artigo/aria-em-formularios">
<meta property="og:site_name" content="MeuSite">
<meta property="og:locale" content="pt_BR">

<!-- Twitter Cards (independente do OG, mas aproveita og: como fallback) -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@meusite">
<meta name="twitter:creator" content="@joaosilva">
<meta name="twitter:title" content="Como usar ARIA em formulários">
<meta name="twitter:description" content="Guia prático com exemplos de roles, states e live regions.">
<meta name="twitter:image" content="https://meusite.com/og/aria-formularios.jpg">
```

Dimensões recomendadas para `og:image`:
- **1200×630px** — padrão para `summary_large_image`
- **Mínimo 600×315px** — fallback para previews menores
- **Formato**: JPG ou PNG, sem texto importante nas bordas (crop em algumas plataformas)

---

## `hreflang` — internacionalização e SEO multilíngue

Quando o mesmo conteúdo existe em múltiplos idiomas/regiões, `hreflang` informa ao Google qual versão exibir para cada usuário:

```html
<!-- Declarar em TODAS as versões (cada uma aponta para todas as outras) -->

<!-- Versão em português do Brasil -->
<link rel="alternate" hreflang="pt-BR" href="https://meusite.com/pt-br/artigo">

<!-- Versão em português de Portugal -->
<link rel="alternate" hreflang="pt-PT" href="https://meusite.com/pt-pt/artigo">

<!-- Versão em inglês -->
<link rel="alternate" hreflang="en" href="https://meusite.com/en/article">

<!-- Fallback para idiomas não especificados -->
<link rel="alternate" hreflang="x-default" href="https://meusite.com/en/article">
```

> [!warning] `hreflang` é bidirecional
> Cada versão deve declarar as outras. Se a versão `pt-BR` aponta para `en` mas a versão `en` não aponta para `pt-BR`, o Google ignora o sinal. Essa é a causa mais comum de hreflang não funcionar.

---

## `robots.txt` e `sitemap.xml` — rastreabilidade

Esses dois arquivos vivem na raiz do domínio e comunicam diretamente com crawlers:

```text
# robots.txt — https://meusite.com/robots.txt

User-agent: *          # Aplica a todos os crawlers
Disallow: /admin/      # Bloqueia o diretório /admin/
Disallow: /private/    # Bloqueia /private/
Allow: /admin/public/  # Mas permite esta subpasta

User-agent: Googlebot  # Regras específicas para o Googlebot
Disallow: /staging/

Sitemap: https://meusite.com/sitemap.xml
```

```xml
<!-- sitemap.xml — lista todas as URLs indexáveis -->
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://meusite.com/</loc>
    <lastmod>2026-06-27</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://meusite.com/artigo/aria-em-formularios</loc>
    <lastmod>2026-06-27</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

---

## `<html lang>` — idioma da página

```html
<html lang="pt-BR">  <!-- Português do Brasil -->
<html lang="pt-PT">  <!-- Português de Portugal -->
<html lang="en">     <!-- Inglês (genérico) -->
<html lang="en-US">  <!-- Inglês americano -->
```

Impacto duplo:
1. **Acessibilidade**: leitores de tela usam para selecionar o engine de síntese de voz correto
2. **SEO**: buscadores usam para localização e matching de queries

Trechos em idioma diferente:
```html
<p>
  O princípio do ARIA em inglês é:
  <q lang="en">No ARIA is better than bad ARIA.</q>
</p>
```

---

## Headings e estrutura semântica como sinal de SEO

Os crawlers usam a hierarquia de headings para entender a estrutura do documento — não apenas para acessibilidade:

- **`<h1>`**: deve haver apenas um por página, correspondendo ao `<title>` (ou próximo a ele)
- **Hierarquia não deve pular níveis**: h1 → h2 → h3, não h1 → h3
- **Keywords nos headings**: o Google dá mais peso ao texto em heading do que ao corpo
- **`<h1>` ≠ `<title>`**: o `<title>` é o que aparece na SERP; o `<h1>` é o que o usuário vê na página — podem e frequentemente devem ser diferentes em extensão

```html
<!-- ✅ Estrutura semântica para SEO e acessibilidade -->
<h1>Guia de ARIA para desenvolvedores web</h1>
  <h2>O que é ARIA?</h2>
  <h2>Quando usar ARIA?</h2>
    <h3>Widgets customizados</h3>
    <h3>Live regions</h3>
  <h2>Anti-padrões mais comuns</h2>

<!-- ❌ Headings usados para estilo, sem hierarquia -->
<h3>Introdução</h3>
<h5>O que é ARIA?</h5>
<h2>Conclusão</h2>
```

---

## Checklist de `<head>` completo

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <!-- 1. Charset — sempre primeiro -->
  <meta charset="UTF-8">

  <!-- 2. Viewport — mobile-first -->
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- 3. Identidade -->
  <title>Guia de ARIA — MeuSite</title>
  <meta name="description" content="Aprenda ARIA com exemplos práticos.">

  <!-- 4. Canonical -->
  <link rel="canonical" href="https://meusite.com/artigo/aria">

  <!-- 5. Robots (só quando não-padrão) -->
  <!-- <meta name="robots" content="noindex, follow"> -->

  <!-- 6. Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="Guia de ARIA">
  <meta property="og:description" content="Aprenda ARIA com exemplos práticos.">
  <meta property="og:image" content="https://meusite.com/og/aria.jpg">
  <meta property="og:url" content="https://meusite.com/artigo/aria">

  <!-- 7. Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">

  <!-- 8. Favicon -->
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/png" href="/favicon.png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.json">

  <!-- 9. Fontes — preconnect antes do preload -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preload" href="/fonts/inter.woff2" as="font" crossorigin>

  <!-- 10. CSS crítico -->
  <link rel="stylesheet" href="/css/main.css">

  <!-- 11. Dados estruturados -->
  <script type="application/ld+json">
  { "@context": "https://schema.org", "@type": "Article", ... }
  </script>
</head>
```

---

> [!question] Para fixar
> 1. Qual o impacto da `meta description` no ranking do Google? E por que ainda importa?
> 2. Quando usar `<meta name="robots" content="noindex">` vs bloquear no `robots.txt`?
> 3. O que acontece se você configurar `hreflang` em apenas uma das versões de idioma?
> 4. Por que JSON-LD é preferido a Microdata para dados estruturados?
> 5. Qual a diferença entre `<title>` e `<h1>` em termos de SEO e quando eles devem divergir?
> 6. Cite três situações em que `<link rel="canonical">` é necessário.

---

## Veja também

- [[03-Dominios/Tecnologia/HTML/08 - ARIA - roles, states, properties e live regions|08 — ARIA]] — anterior
- [[03-Dominios/Tecnologia/HTML/10 - Performance em HTML - resource hints e critical path|10 — Performance em HTML]] — próxima (preload, prefetch, preconnect em profundidade)
- [[03-Dominios/Tecnologia/HTML/01 - O modelo mental do HTML - semântica, árvore e o browser|01 — O modelo mental do HTML]] — parsing e DOM (contexto de como crawlers interpretam)
- [[03-Dominios/Tecnologia/HTML/02 - Landmark elements e documento estruturado|02 — Landmark elements]] — estrutura de documento (h1, hierarquia de headings)
