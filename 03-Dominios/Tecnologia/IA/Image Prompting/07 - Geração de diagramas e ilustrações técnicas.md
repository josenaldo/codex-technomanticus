---
title: "07 - Geração de diagramas e ilustrações técnicas"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
fase: Iniciado
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

> [!question]- Qual a diferença entre "ilustração conceitual" e "diagrama técnico"? Onde está a fronteira?
> A fronteira está na **precisão semântica necessária**. Ilustração conceitual comunica a essência de um sistema — "esse componente alimenta aquele, há um buffer no meio" — sem exigir que o texto seja exato, as setas numeradas, ou a hierarquia verificável. Diagrama técnico é **especificação visual**: alguém precisa implementar a partir dele, ou auditá-lo, ou rastrear um bug usando a arquitetura desenhada. Regra prática: se um desenvolvedor vai olhar e tomar decisão técnica com base no visual → diagrama técnico, use ferramentas declarativas. Se vai olhar, entender o conceito e seguir em frente → ilustração conceitual, modelo de imagem funciona.

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

Exemplo: deck sobre as 11 camadas do AI Engineering Stack — 11 ícones em estilo consistente, um por camada. Processo: gera o primeiro ícone com descrição completa de estilo → salva o URL como `--sref` pra Midjourney → gera os 10 restantes referenciando o primeiro → consistência visual garantida sem esforço manual.

### Wallpaper / background técnico

Background pra slide, sessão de hero em landing page, capa de podcast técnico. Abstrato, evocativo, mas técnico. Modelos de imagem entregam bem.

Pra série de slides com branding consistente: gere o background uma vez (16:9, paleta fixa, estilo fixo), salve em alta resolução, reutilize em todos os slides da série. O modelo de imagem resolve o problema de "preciso de background premium sem comprar stock". Uma geração bem-feita serve a toda a série.

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

O padrão híbrido tem outro benefício: **manutenção**. Spec Mermaid no vault Obsidian pode ser editada com um PR; o hero de imagem raramente precisa mudar junto. Separar o visual precisos do visual evocativo cria independência entre os dois fluxos de trabalho.

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

Uma tendência concreta que já aparece em 2026: modelos com **code execution** (GPT-5, Gemini com Code Execution) podem gerar Python que usa `graphviz`, `matplotlib`, ou `networkx` pra desenhar diagramas programaticamente. O modelo não gera a imagem diretamente — gera o *código* que gera a imagem. Resultado é mais preciso que geração direta. Ainda não é "modelo de imagem gerando diagrama", mas é um step intermediário útil: você pede "gere código Python que desenhe o flowchart do pipeline RAG usando matplotlib + networkx", executa o código, recebe um SVG/PNG preciso. Mais trabalhoso que Mermaid, mas às vezes o controle é necessário.

## Código: gerando Mermaid via LLM

O padrão híbrido (LLM gera spec → renderizador converte) funciona melhor com um prompt estruturado pro LLM:

```python
import anthropic

client = anthropic.Anthropic()

MERMAID_SYSTEM = """Você é um especialista em Mermaid.js. Quando solicitado, gera
APENAS o bloco Mermaid sem explicação. Siga essas regras:
- Comece sempre com o tipo de diagrama na primeira linha (graph LR, sequenceDiagram, erDiagram, etc.)
- Use IDs ASCII simples sem espaços (UserService, não "User Service")
- Texto em labels pode ter português mas sem caracteres especiais problemáticos
- Máximo 20 nós pra legibilidade
- Valide mentalmente que as setas fazem sentido antes de responder
"""

def generate_mermaid(description: str, diagram_type: str = "flowchart") -> str:
    type_hints = {
        "flowchart": "graph LR ou flowchart TD/LR",
        "sequence": "sequenceDiagram",
        "class": "classDiagram",
        "er": "erDiagram",
        "state": "stateDiagram-v2",
    }
    hint = type_hints.get(diagram_type, "graph LR")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=MERMAID_SYSTEM,
        messages=[{
            "role": "user",
            "content": (
                f"Gere um diagrama Mermaid do tipo '{hint}' para: {description}\n"
                "Retorne APENAS o bloco mermaid, sem markdown fences nem explicação."
            ),
        }],
    )
    return response.content[0].text.strip()


# Uso
mermaid_spec = generate_mermaid(
    description="Pipeline RAG: usuário faz query → embedding → busca vetorial → "
                "recupera chunks relevantes → monta contexto → LLM gera resposta",
    diagram_type="flowchart",
)
print(mermaid_spec)
# Cole em https://mermaid.live/ ou use no Obsidian diretamente (bloco ```mermaid)
```

O Obsidian renderiza Mermaid nativo — cole o spec em ```` ```mermaid ```` no vault. Quartz (o site gerado) também renderiza automaticamente.

## Ferramentas de diagrama em 2026

| Ferramenta | Tipo | Melhor para | Integração Obsidian |
|---|---|---|---|
| **Mermaid** | Declarativo (texto) | Flowchart, sequence, ER, class, state | Nativo (renderiza inline) |
| **PlantUML** | Declarativo (texto) | UML completo, mais expressivo que Mermaid | Plugin Obsidian |
| **Excalidraw** | Mão livre | Arquitetura ad-hoc, sketch de sistema | Plugin Obsidian (excelente) |
| **Draw.io (diagrams.net)** | GUI drag-drop | Diagramas formais com muitos elementos | Plugin Obsidian |
| **dbml + DBdiagram** | Declarativo (schema) | ER diagrams, schema de banco | Externo (export PNG/SVG) |
| **D2** | Declarativo (texto) | Alternativa ao Mermaid com layout mais sofisticado | Externo |
| **Graphviz/DOT** | Declarativo (texto) | Grafos, dependências de pacotes, call graphs | Externo (via CLI) |

Para vault Obsidian: Mermaid (nativo) + Excalidraw (plugin) cobrem 95% dos casos. PlantUML para UML formal. Externo (Draw.io exportado como PNG) para diagramas muito complexos.

## Armadilhas comuns

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

## Armadilhas comuns

> [!warning] Iterar 5+ vezes tentando "consertar o texto" do diagrama gerado — beco sem saída
> Quando o modelo gera um diagrama com "Datbase" em vez de "Database" ou seta indo pra lugar errado, o instinto é iterar: "corrija o texto da caixa da direita para 'Database'". O modelo produz variação semelhante com o mesmo erro em lugar diferente. Essa iteração não converge porque o problema não é de prompt — é de natureza: modelos de geração de imagem não têm representação discreta de "essa caixa de texto específica". A saída do beco é largar o modelo de imagem e abrir Mermaid ou Excalidraw. Regra prática: se após 3 iterações o diagrama ainda tem erro semântico, pare.

> [!warning] Usar DALL-E pra gerar org chart de uma empresa real — nomes de pessoas errados e relações inventadas
> Um modelo generativo não tem acesso ao org chart real e vai gerar nomes plausíveis-mas-errados, hierarquias inventadas, e conectar pessoas que não se conhecem. Além de inútil, é potencialmente problemático (gerar informação falsa sobre pessoas reais). Org charts são dados estruturados, não visuais livres — use ferramentas de HR ou spreadsheet + automação pra gerar o diagrama real.

> [!warning] Confundir "parece diagrama" com "é diagrama" — enganar audiência com visual impreciso
> Uma ilustração conceitual de arquitetura que parece um diagrama de sistema pode enganar a audiência: ela vai assumir que aquele "diagrama" é preciso, que aquela seta representa o fluxo real, que aquela caixa é o componente real. Se o visual vai aparecer em documentação técnica, README de projeto, ou pitch técnico, deixe claro que é ilustração conceitual — "representação aproximada para comunicação" — não especificação. Uma legenda "Representação conceitual (ver Excalidraw pra diagrama preciso)" resolve ambiguidade.

## Como explicar em inglês

**Interview quote:** *"Image generation models are not reliable for precise technical diagrams in 2026 — text in boxes comes out garbled, arrows connect wrong elements, and structure isn't discrete. The hybrid pattern that works: use an LLM to generate Mermaid or PlantUML spec (rendered natively in Obsidian/Quartz), and use an image model for the conceptual illustration or hero — the evocative visual that opens the post, not the precise diagram in the middle of it."*

| Português | Inglês |
|---|---|
| Diagrama técnico preciso | Precise technical diagram |
| Ilustração conceitual | Conceptual illustration |
| Padrão híbrido (spec textual + hero visual) | Hybrid pattern (text spec + visual hero) |
| Spec declarativa (Mermaid, PlantUML) | Declarative spec (Mermaid, PlantUML) |
| Renderizador de diagrama | Diagram renderer |
| Herói de post técnico | Technical post hero image |
| Icon set temático consistente | Consistent themed icon set |
| Arquitetura precisa de sistema | Precise system architecture diagram |
| LLM gera a spec | LLM generates the spec |

## O que vem a seguir

Esta é a última nota do galho Image Prompting. Você agora tem: mentalidade engineering (nota 01), deliverable-first (nota 02), mapa de modelos (nota 03), anatomia do prompt (nota 04), templates por entregável (nota 05), iteração disciplinada (nota 06), e os limites honestos (esta nota). O próximo passo natural é o galho **Improvement Loop** — onde os mesmos princípios se aplicam na escala de múltiplas gerações e múltiplos assets, com avaliação sistemática e fine-tuning de estilo.

A lição mais importante desta nota para levar adiante: saber quando **não usar** uma ferramenta é tão valioso quanto saber como usá-la. Image prompting que sabe seus limites produz output melhor do que image prompting que tenta tudo. Diagramas em Mermaid produzem mais clareza em documentação técnica do que qualquer modelo de imagem em 2026.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #16 (Image Prompting). Limites apresentados.
- **Mermaid** — *Documentation* ([docs](https://mermaid.js.org/)). Renderizador declarativo de diagramas em texto.
- **Excalidraw** — *Site* ([excalidraw.com](https://excalidraw.com/)). Mão livre estilizado pra diagramas; plugin Obsidian.
- **PlantUML** — *Documentation* ([docs](https://plantuml.com/)). UML declarativo, mais expressivo que Mermaid.
- **DBdiagram.io** — [Site](https://dbdiagram.io/). Schema de banco em DBML, export PNG/SVG.
- **D2** — [d2lang.com](https://d2lang.com/). Alternativa moderna ao Mermaid com layout mais sofisticado.
- **Quartz** — *Mermaid support* ([docs](https://quartz.jzhao.xyz/)). Mermaid renderiza nativo no site gerado.
- **Obsidian** — *Mermaid plugin*. Diagramas Mermaid renderizam nativamente no vault sem plugin extra.

## Veja também

- [[01 - Image prompting como engenharia]] — quando NÃO usar geração de imagem (lista desta nota)
- [[03 - Modelos de imagem 2026 — DALL-E, Imagen, Midjourney, FLUX, SD]] — Ideogram/Imagen pra quando texto é viável
- [[05 - Templates por entregável — poster, infográfico, mockup, thumbnail]] — hero image (onde modelo de imagem brilha em contexto técnico)
- [[06 - Iteração visual — controlled changes]] — antídoto pra "iterando há 2h tentando consertar texto"
- [[Dicionário de IA#Mermaid|Dicionário: Mermaid]]
- [[Dicionário de IA#Ilustração conceitual|Dicionário: Ilustração conceitual]]
- [[Dicionário de IA#Diagrama técnico|Dicionário: Diagrama técnico]]
- [[Dicionário de IA#Padrão híbrido|Dicionário: Padrão híbrido (spec textual + hero visual)]]
- [[Dicionário de IA#ControlNet|Dicionário: ControlNet]] — útil pra ilustração conceitual com layout preciso
- [[03-Dominios/Tecnologia/Fundamentos/Compiladores e Linguagens/index|Galho Compiladores]] — especificações declarativas têm o mesmo princípio de separação (spec ≠ renderização)
- [[Dicionário de IA#Spec declarativa|Dicionário: Spec declarativa de diagrama]]
- [[Dicionário de IA#Layout-aware generation|Dicionário: Layout-aware generation]]
