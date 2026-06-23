---
title: "07 - Geração de diagramas e ilustrações técnicas"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - image-prompting
  - prompt-engineering
  - ia
  - technical-illustration
  - limits
publish: true
aliases:
  - Diagramas com IA
  - Geração de ilustração técnica
---

# 07 - Geração de diagramas e ilustrações técnicas

> [!abstract] TL;DR
> Em 2026, modelos de imagem ainda **não** geram diagramas técnicos precisos de forma confiável. Texto em caixinhas erra; setas conectam errado; org charts viram bagunça; ER diagrams são fantasia. Onde funcionam bem: ilustração conceitual de arquitetura (metáfora visual de "sistema de filas", "RAG como bibliotecário"), hero images pra posts técnicos, icon sets temáticos. Onde não funcionam: flowchart real, diagrama de classes, schema de DB, org chart, qualquer coisa com texto preciso em múltiplas caixas. Padrão híbrido pra 2026: LLM-de-texto gera Mermaid/PlantUML spec → modelo de imagem gera hero conceitual de apoio. Use cada ferramenta no que ela faz bem.

## O estado honesto em 2026

Modelos de imagem evoluíram bastante em texto-na-imagem entre 2023 e 2026 (Ideogram, Imagen 4, FLUX dev lideram). Mas **diagrama técnico** é categoria diferente de "imagem com texto":

- Diagrama exige **precisão semântica**: a seta vai *daqui pra ali*, esse texto está *naquela caixa específica*, essa relação é *one-to-many*.
- Diagrama exige **estrutura discreta**: número exato de elementos, conexões exatas, alinhamento.
- Diagrama exige **legibilidade em zoom**: texto pequeno em múltiplas caixas tem que estar correto, não "parecer correto".

Modelos generativos atuais são contínuos por natureza — não pensam em "essa caixa" como objeto discreto. Pra eles, é distribuição de pixels que se parece com diagrama.

Resultado: diagrama gerado tem aparência de diagrama, mas:
- Texto nas caixas: errado ou ilegível
- Setas: conectam coisas que não deveriam conectar
- Hierarquia: invertida ou ausente
- Símbolos: misturados (UML + ER + flowchart no mesmo desenho)

Avanço marginal de versão pra versão, mas em 2026 ainda não dá pra confiar.

## Onde modelos de imagem funcionam em conteúdo técnico

Apesar do limite acima, há casos onde modelos de imagem entregam valor em contexto técnico:

### Ilustração conceitual de arquitetura

Não é o diagrama exato — é a **metáfora visual** que ancora o conceito.

- "Sistema de mensageria como rede de tubos pneumáticos"
- "RAG como bibliotecário digital em estante infinita"
- "Microservices como ilha-arquipélago conectada por pontes"
- "Cache como antessala da biblioteca"

Modelo bom: Midjourney (qualidade artística), FLUX dev. Output vira hero de post técnico, capa de talk, slide de keynote.

### Hero image pra post técnico

Como nota [[05 - Templates por entregável — poster, infográfico, mockup, thumbnail]] já cobriu, o hero não precisa ser o diagrama — é a peça visual que abre o post. "Post sobre RAG" → hero com metáfora visual de RAG, sem ser o diagrama do pipeline. O diagrama vem no meio do post, feito em Mermaid/Excalidraw.

### Icon set temático

Conjunto de ícones consistentes pra deck, doc, ou UI. Usa `--sref` (Midjourney) ou IP-Adapter (SD) pra manter consistência. Modelo gera o "tema" do ícone (linha fina, cor específica, mesma vibe), você re-prompta com cada conceito.

Exemplo: deck sobre as 11 camadas do AI Engineering Stack — 11 ícones em estilo consistente, um por camada.

### Wallpaper / background técnico

Background pra slide, sessão de hero em landing page, capa de podcast técnico. Abstrato, evocativo, mas técnico. Modelos de imagem entregam bem.

## Onde modelos de imagem **não** funcionam

Lista de "não tente, vai dar errado":

### Flowchart preciso

`if condition → branch A → loop → end`. Modelo gera algo que parece flowchart, com palavras inventadas e setas erradas. **Use:** Mermaid (`graph LR` ou `flowchart TD`), Excalidraw, Draw.io.

### Diagrama UML / classes

Hierarquia de classe, relacionamentos, métodos. Modelo confunde notação. **Use:** PlantUML, Mermaid (`classDiagram`).

### Schema de banco de dados (ER)

Tabelas, colunas, relações N:N. Modelo inventa colunas. **Use:** DBdiagram.io, Mermaid (`erDiagram`), dbml.

### Org chart

Hierarquia organizacional. Modelo erra reportes. **Use:** Mermaid (`flowchart TD`), tools de RH.

### Sequência (sequence diagram)

Múltiplos atores trocando mensagens em ordem. Modelo embaralha ordem. **Use:** Mermaid (`sequenceDiagram`), PlantUML.

### Tabela de dados

Linhas e colunas com números/texto. Modelo erra valores. **Use:** Markdown table, HTML, Figma.

### Arquitetura precisa de sistema

Você quer mostrar "API → Worker → Queue → DB" com nomes reais de serviço. Modelo erra os nomes e as conexões. **Use:** Excalidraw (mão livre estilizado), Draw.io, AWS/GCP/Azure diagram tools.

## O padrão híbrido: text-model + image-model

Padrão produtivo em 2026:

1. **LLM gera a especificação textual do diagrama** em formato declarativo (Mermaid, PlantUML, DOT, dbml).
2. **Renderizador textual** (Mermaid Live, PlantUML server, Quartz nativo) converte spec em SVG/PNG.
3. **Modelo de imagem gera hero conceitual** que abre o post / slide / doc, dando vida visual ao tema (sem ser o diagrama em si).

Exemplo concreto:

> Post sobre "Cache como antessala da biblioteca":
> - **Hero (FLUX/Midjourney):** ilustração abstrata de antessala de biblioteca com fluxo de luz das prateleiras
> - **No corpo do post (Mermaid):** `flowchart LR: Client --> Cache --> DB`
> - **Diagrama detalhado se necessário (Excalidraw):** mão livre

Cada peça é feita pela ferramenta certa. O modelo de imagem entrega a parte estética; o renderizador textual entrega a parte precisa.

## Quando o engenheiro tenta usar modelo de imagem pra diagrama (anti-padrões)

Sintomas comuns de "tentei e me arrependi":

- Você gerou um "diagrama" pro README e ninguém entende
- O diagrama do post tem palavras tipo "Servreve" e "Datbase"
- A seta entre componentes vai pra lugar nenhum
- Você passou 2h iterando e ainda está pior que se tivesse aberto o Excalidraw

Sinais de que você deveria parar:

- Você está iterando há mais de 3 vezes tentando "consertar" o texto
- Você está tentando que o modelo gere "exatamente N caixas"
- Você se viu pensando "se eu descrever melhor a topologia..."

Mude pra Mermaid/Excalidraw. Volte ao modelo de imagem só pro hero.

## O state em 2026 e o que vem pela frente

Em 2026, estamos a 6-12 meses (estimativa) de modelos conseguirem gerar **flowcharts reais** com confiabilidade. Direções de pesquisa que apontam pra isso:

- Modelos com **layout-aware generation** (entendem grid, alinhamento, hierarquia)
- Modelos **multimodais que aceitam spec textual + imagem** (você passa Mermaid, ele renderiza estilizado)
- Edição **estrutural-aware** (mover caixa preserva conexões)

Até lá, o padrão híbrido é o caminho. Honesto sobre limite economiza tempo.

## Recapitulação rápida

| Tipo de visual técnico | Use modelo de imagem? | Use o quê? |
|------------------------|----------------------|------------|
| Hero conceitual / metáfora arquitetural | **Sim** | Midjourney, FLUX dev, DALL-E |
| Icon set temático consistente | **Sim** | Midjourney `--sref`, SD IP-Adapter |
| Wallpaper / background | **Sim** | Qualquer modelo |
| Flowchart preciso | **Não** | Mermaid, Excalidraw, Draw.io |
| UML / class diagram | **Não** | PlantUML, Mermaid |
| ER diagram / schema DB | **Não** | DBdiagram, Mermaid, dbml |
| Sequence diagram | **Não** | Mermaid, PlantUML |
| Org chart | **Não** | Mermaid, ferramentas de RH |
| Arquitetura precisa de sistema | **Não** | Excalidraw, Draw.io |
| Tabela de dados | **Não** | Markdown, HTML |

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #16 (Image Prompting). Limites apresentados.
- **Mermaid** — *Documentation* ([docs](https://mermaid.js.org/)). Renderizador declarativo de diagramas em texto.
- **Excalidraw** — *Site* ([excalidraw.com](https://excalidraw.com/)). Mão livre estilizado pra diagramas.
- **PlantUML** — *Documentation* ([docs](https://plantuml.com/)). UML declarativo.

## Veja também

- [[05 - Templates por entregável — poster, infográfico, mockup, thumbnail]] — hero image (onde modelo de imagem brilha em contexto técnico)
- [[06 - Iteração visual — controlled changes]] — antídoto pra "iterando há 2h tentando consertar texto"
- [[03 - Modelos de imagem 2026 — DALL-E, Imagen, Midjourney, FLUX, SD]] — Ideogram/Imagen pra quando texto é viável
