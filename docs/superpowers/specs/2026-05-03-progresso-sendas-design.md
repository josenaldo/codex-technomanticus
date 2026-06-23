---
title: "Spec — Tracking de progresso nas sendas"
date: 2026-05-03
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Tracking de progresso nas sendas

## 1. Contexto e motivação

O Codex Technomanticus organiza o conhecimento em quatro zonas operacionais (`01-Pergaminhos`, `02-Glosas`, `03-Dominios`, `04-Sendas`). As **Sendas** são, conceitualmente, mapas de leitura sobre os Domínios — caminhos curatoriais que sequenciam notas de domínio em trilhas de estudo orientadas a um objetivo.

Hoje, ao percorrer uma senda, o usuário não tem visibilidade de **onde está**: o que já foi estudado, o que está em curso, o que pausou, o que ainda é horizonte. A Senda IA tem 19 KB de conteúdo (fases, checkpoints, notas de apoio); a Senda Java tem 23 KB. Quando o usuário retoma o estudo depois de algumas semanas, refaz o trabalho de localização.

Falta também um modelo conceitual nítido sobre o que **deve** estar em cada zona. As sendas atuais misturam material que pertence aos domínios (links externos contextualizados, exercícios, checkpoints conceituais), violando a metáfora "estante × fluxograma de faculdade".

Esta spec resolve as duas lacunas em um único movimento: define o modelo canônico de senda (apenas wikilinks ordenados pra notas dos domínios), introduz o campo `progresso` no frontmatter das notas, e estabelece convenções de agregação que permitem responder "onde estou nessa senda?" automaticamente.

## 2. Objetivo

Entregar:

1. Um **modelo de dados** simples — um único campo `progresso` no frontmatter — que serve como fonte da verdade do estado de estudo.
2. Um **template canônico de senda** com duas variantes (lista plana e fases) que reforça o modelo conceitual "domínios = estantes, sendas = fluxograma".
3. Uma **convenção de convite** (`[!convite]`) que define onde materiais externos vivem dentro do pipeline (em notas de domínio, como aprofundamento opcional, não nas sendas).
4. **Bloco dataview de agregação** dentro de cada senda, exibindo progresso item-a-item e totais.
5. **Atualizações nos templates** existentes pra incorporar o novo campo + convenção.
6. **CSS** do callout `convite` no repo do site (Quartz).
7. **Piloto na Senda Frontend**, demonstrando o sistema completo com uma senda real.

## 3. Escopo

### Em escopo

- Documentação do modelo conceitual no `00-Meta/guia/`.
- Definição do campo `progresso` (valores, default, onde aplica).
- Atualização de `Template - Nota.md`, `Template - Glosa.md`, e substituição de `00-Meta/templates/trail.md` pelo novo template canônico.
- Definição da convenção `[!convite]` e exemplos.
- Bloco dataview de agregação na senda (versões `minimal` e `structured`).
- CSS do callout `convite` no `codex-technomanticus-site`.
- Migração da Senda Frontend ao novo formato (piloto).
- Criação das **estantes mínimas** que o piloto precisa referenciar — `03-Dominios/Tecnologia/Frontend/` (engenharia), `React/`, `TypeScript/`, e demais conforme §10.2 — com notas-stub. Não inclui migração das notas existentes em `03-Dominios/Tecnologia/JavaScript/Frontend/` para essas estantes (vide §13).
- Atualização de `docs/apocrypha-pendencias.md` com itens deferred.

### Fora de escopo (trabalho subsequente)

- **Migração das outras sendas**: cada senda existente (Backend, Cloud, Devops, Entrevistas, Fullstack, Go, IA, Java, JS-TS, Python) será migrada quando o usuário retomar o estudo correspondente. Idealmente, **vira uma skill `/migrar-senda <nome>`** que automatiza a quebra do conteúdo "ofensivo" (presente na senda mas que pertence ao domínio) em notas atômicas no domínio + aplica o template canônico.
- **Refatoração da Senda IA**: a Senda IA tem volume grande de conteúdo factual misturado (capítulos, checkpoints, projetos). Sua migração é trabalho dedicado posterior, não cabe neste piloto.
- **Dashboard agregado consolidado**: visão cross-senda com totalizadores globais ("47 notas estudadas em IA este mês"). Mora no apocrypha — vide `docs/apocrypha-pendencias.md`.
- **Nota "o que estudar hoje?"**: depende de definição de ordem global e prioridade. Apocrypha.
- **Journal de estudo**: registro de processo de aprendizagem (não de estado factual). Aceito conceitualmente, mas o usuário ainda não tem daily notes do Obsidian no pipeline. Vide `docs/perguntas-abertas.md` (bloco "Daily notes do Obsidian").
- **Pipeline glosa → domínio**: o critério e o ato concreto de promoção de uma glosa a uma nota de domínio ainda não estão claros. Vide `docs/perguntas-abertas.md` (bloco "Glosa → Domínio").
- **Cross-vault awareness** (`cta` como tomo irmão de `ct`): pendência geral do apocrypha.

## 4. Modelo conceitual (canon)

### 4.1 As quatro zonas e o pipeline

| Zona | Papel |
|---|---|
| `01-Pergaminhos/` | Captura inicial: inbox, links soltos, ideias cruas. |
| `02-Glosas/` | Fichamentos de materiais externos consumidos. |
| `03-Dominios/` | Corpus do conhecimento. **Centro gravitacional do vault**. Notas amadurecidas, organizadas por domínio. |
| `04-Sendas/` | Mapas de leitura. Wikilinks ordenados pra notas dos domínios. **Apenas isso**. |

**Pipeline de alimentação**: pergaminho → glosa → nota de domínio. Materiais externos consumidos viram glosas; glosas amadurecem e dão origem a notas de domínio.

### 4.2 Domínios = estantes; sendas = fluxograma

- **Domínios** são estantes de livros: corpus de conhecimento sobre um tema. Notas, materiais externos contextualizados (via callout `[!convite]`), exercícios, projetos — tudo aqui.
- **Sendas** são fluxogramas de faculdade: indicam a ordem de leitura das notas (livros) das estantes. Não contêm conhecimento próprio; apenas referenciam.

Uma senda **não** contém:

- Texto explicativo de conceitos (vai pra nota do domínio).
- Links externos a artigos, vídeos, livros, cursos (vão pra notas de domínio, dentro de callouts `[!convite]`, ou viram glosas).
- Exercícios, projetos, checkpoints conceituais (vão pro domínio).
- Wikilinks pra headings internos do próprio arquivo.

Uma senda **contém**:

- Frontmatter com metadados (vide §6.1).
- Descrição curta da senda (pra quem é, qual o destino).
- Pré-requisitos (wikilinks pra notas de outros domínios).
- Sequência ordenada de wikilinks pra notas do domínio principal (forma plana ou em fases).
- Bloco dataview de agregação de progresso.

### 4.3 Organização dos domínios (modelo de estantes)

Cada domínio é uma estante coerente: uma área de conhecimento com vocabulário próprio, comunidade própria, ferramental próprio. Tecnologias maiores merecem estante própria; áreas de disciplina (cross-tech) também.

Modelo adotado:

- **Linguagens próprias**: `JavaScript/` (apenas core: closures, prototypes, async, ESNext), `TypeScript/`, `HTML/`, `CSS/` (incluindo Sass/Less), além das já existentes (`Java/`, `Python/`, `Go/`).
- **Bibliotecas/frameworks grandes como estantes**: `React/`, `Vue/`, `Svelte/`, `HTMX/`. Bibliotecas menores moram como notas dentro do domínio mais relevante (ex.: MUI, Mantine como notas em `React/`).
- **Disciplinas (cross-tech)**: `Frontend/` deixa de ser agrupador de tecnologias e vira estante de **engenharia frontend** — arquitetura, performance, acessibilidade, padrões, responsividade. Cross-tech por natureza.
- **Ferramentas**: `Ferramentas/` (já existente) abriga tooling cross-tech (Vite, bundlers, monorepos).

Sendas atravessam estantes naturalmente: `Senda Frontend`, por exemplo, é fluxograma transversal cruzando `JavaScript/` (core), `HTML/`, `CSS/`, `React/`, `TypeScript/`, `Frontend/` (engenharia), `Ferramentas/`.

**Implicação pra esta spec**: a reorganização completa dos domínios atuais (especialmente migrar `03-Dominios/Tecnologia/JavaScript/Backend/` e `03-Dominios/Tecnologia/JavaScript/Frontend/` pras novas estantes) é **trabalho separado** — pode virar spec própria. Esta spec faz **o mínimo necessário pro piloto rodar**: cria as estantes que a Senda Frontend piloto vai referenciar, com notas-stub, sem migrar tudo o que já existe em `JavaScript/Frontend/`. A migração completa dessas notas é trabalho subsequente, vide §13.

### 4.4 Materiais externos: o convite

Materiais externos (artigos, vídeos, cursos, livros) são apresentados dentro de notas de domínio como **convites a aprofundamento**:

```markdown
> [!convite] Aprofundamento — attention mechanism
> - [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — Jay Alammar
> - [3Blue1Brown — Neural Networks series](https://www.3blue1brown.com/topics/neural-networks)
>
> Consumiu? Faça uma glosa em `02-Glosas/` e amadureça pro domínio quando fizer sentido.
```

Convite é convite: opcional, não-bloqueante, sem `progresso` próprio. O `progresso` aparece quando o usuário consome o material e cria uma glosa.

## 5. Modelo de dados

### 5.1 Frontmatter `progresso`

Um único campo no frontmatter da nota:

```yaml
progresso: pendente | andamento | feito | pausado | abandonado
```

| Valor | Significado |
|---|---|
| `pendente` | Ainda não comecei. Default quando o campo está ausente. |
| `andamento` | Estou estudando ativamente. |
| `feito` | Concluí o estudo dessa nota; conteúdo absorvido. |
| `pausado` | Comecei e parei intencionalmente; pretendo retomar. |
| `abandonado` | Decidi não estudar; fora do meu radar. |

### 5.2 Default e ausência

A ausência do campo é tratada como `pendente` nas queries dataview (`default(progresso, "pendente")`). Não é necessário pré-popular as ~500 notas existentes.

### 5.3 Onde aplica

- **Notas de `03-Dominios/`**: sim. Toda nota de domínio é candidata a estudo.
- **Glosas em `02-Glosas/`**: sim. Glosa nasce com `progresso: andamento` (o ato de glosar é "estou consumindo este material"); evolui pra `feito` quando a leitura termina.
- **Pergaminhos em `01-Pergaminhos/`**: não. Pergaminho é captura inicial, não conhecimento para estudo.
- **Sendas em `04-Sendas/`**: não. Senda agrega; não tem progresso próprio. (O `status: active | done | archived` da senda continua sendo metadado de senda, separado.)
- **Notas de `00-Meta/`**: não.

### 5.4 Ortogonalidade com `status`

`status` (template existente: `seedling`, `budding`, `evergreen`) é maturidade do conteúdo da nota — quanto a nota foi desenvolvida. `progresso` é o **estado de estudo** do usuário em relação à nota. São ortogonais:

- Nota `evergreen` (madura) com `progresso: pendente` (ainda não comecei a estudar): possível.
- Nota `seedling` (stub) com `progresso: feito` (consumi o material, anotei o essencial, não pretendo aprofundar): possível.

## 6. Convenções e templates

### 6.1 Template canônico de senda

Substitui `00-Meta/templates/trail.md`:

```markdown
---
type: trail
title: "Senda <Nome>"
domain: "[[03-Dominios/<Domínio>/index]]"
maturity: minimal      # ou: structured
status: active         # active | done | archived (metadado de senda, não de progresso)
publish: true
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
tags:
  - senda
---

# Senda <Nome>

> Pra quem é, qual o destino, em quanto tempo.

## Pré-requisitos

- [[...]]

## Sequência

<!-- Versão minimal: lista plana ordenada -->

1. [[03-Dominios/<Domínio>/<Nota A>]]
2. [[03-Dominios/<Domínio>/<Nota B>]]
3. [[03-Dominios/<Domínio>/<Nota C>]]

<!-- Versão structured: substituir "## Sequência" pelos blocos abaixo -->

<!--
## Fase 0 — <Tema>

1. [[03-Dominios/<Domínio>/<Nota A>]]
2. [[03-Dominios/<Domínio>/<Nota B>]]

## Fase 1 — <Tema>

1. [[03-Dominios/<Domínio>/<Nota C>]]
-->

## Progresso

(bloco dataview — vide §6.3)
```

Regras:

- A senda escolhe **uma** das duas formas (`Sequência` plana ou `Fases`) conforme `maturity`.
- Apenas wikilinks pra notas de `03-Dominios/`. Sem links externos, código, exercícios.
- Texto livre permitido apenas em "Pré-requisitos" e descrição inicial.

### 6.2 Atualizações em outros templates

**`Template - Nota.md`** (notas de domínio):

- Adicionar `progresso: pendente` no frontmatter.
- Adicionar seção opcional `## Aprofundamento` no fim do template, com exemplo de callout `[!convite]` comentado, pra incentivar o uso da convenção.

**`Template - Glosa.md`** (glosas):

- Adicionar `progresso: andamento` no frontmatter (glosa nasce em andamento; vira `feito` quando lida).

### 6.3 Bloco dataview de agregação

Inserido no fim da senda, sob `## Progresso`.

**Versão `minimal`** (lista plana):

````markdown
## Progresso

```dataview
TABLE WITHOUT ID
  file.link AS "Nota",
  default(progresso, "pendente") AS "Status"
FROM outgoing([[]])
WHERE file.path != this.file.path AND contains(file.path, "03-Dominios/")
SORT file.name ASC
```

**Resumo:**

```dataview
TABLE WITHOUT ID
  length(rows) AS "Total",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "feito")) AS "Feitas",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "andamento")) AS "Em andamento",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "pausado")) AS "Pausadas",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "pendente")) AS "Pendentes"
FROM outgoing([[]])
WHERE file.path != this.file.path AND contains(file.path, "03-Dominios/")
GROUP BY true
```
````

**Versão `structured`** (com fases): a agregação por fase exige identificar a fase de cada wikilink na senda. Duas abordagens possíveis, em ordem de preferência:

1. **Por seção da senda usando Dataview JS** (preferida): script lê o markdown da própria senda, identifica os headings `## Fase N — ...`, e agrupa os links por seção. Implementação concentrada em um único bloco no fim da senda.
2. **Fallback simples**: agregação total da senda inteira (igual à versão `minimal`), sem desagregar por fase. Aceitável se Dataview JS for custoso ou pouco confiável.

A spec adota o **fallback simples como mínimo viável**, e abre a possibilidade de evoluir pra Dataview JS quando o piloto rodar e o trabalho extra se justificar. O piloto usa fallback simples.

### 6.4 Callout `[!convite]`

Tipo customizado de callout do Obsidian, usado dentro de notas de domínio:

```markdown
> [!convite] <Título do aprofundamento>
> - [<Texto do link>](<url>) — <autor/origem>
> - <outro item>
>
> Consumiu? Faça uma glosa em `02-Glosas/` e amadureça pro domínio quando fizer sentido.
```

Regras:

- Vai dentro da nota de domínio, em seção `## Aprofundamento` ou intercalado no texto onde o aprofundamento faz sentido.
- Lista links externos relevantes ao tema da nota.
- Convida o usuário a fazer uma glosa, sem obrigatoriedade.
- Não tem `progresso` próprio (ele aparece na glosa que eventualmente nasce do convite).

No Obsidian, callouts customizados funcionam por padrão (renderiza como `[!convite]` se reconhecido, ou cai no estilo genérico). No Quartz, requer CSS — vide §8.

## 7. Privacy e split público × apocrypha

A spec respeita a separação rígida público × apocrypha do projeto:

- **Estado factual** (campo `progresso`): vai no público, junto com a nota. Não é dado sensível — é apenas seu estado de leitura. Já há precedente no público (campo `status` que indica seu juízo de maturidade da nota).
- **Visão consolidada / agregada / narrativa**: vai no apocrypha. Dashboard cross-senda, journal de estudo, "o que estudar hoje?" são experiências pessoais que cruzam dados do público com reflexão.

Esta spec não toca no apocrypha. O apocrypha tem outra sessão de edição em andamento; pendências relacionadas estão em `docs/apocrypha-pendencias.md`.

## 8. Visibilidade no Quartz (site)

O bloco dataview **não roda no Quartz v4** (Quartz não executa Dataview). Comportamento esperado no site:

- A senda renderiza com frontmatter, descrição, pré-requisitos e sequência (lista de wikilinks). Tudo visível.
- O bloco `## Progresso` aparece no markdown bruto (visitante vê o código `dataview` inline) — solução pragmática: configurar o Quartz pra **omitir** a seção `## Progresso` na renderização, ou inserir um marcador HTML `<!-- omit -->` que o Quartz respeite.
- Decisão: omitir a seção `## Progresso` no site. O tracking é experiência local do Obsidian; visitantes só querem o caminho.

**CSS do callout `[!convite]`**: precisa ser adicionado no Quartz pra renderizar com estilo dedicado (cor, ícone, semântica visual de "convite"). Sem CSS, o callout cai no estilo genérico do Quartz — funcional, mas sem identidade. Trabalho pequeno: adicionar uma regra no SCSS do tema.

## 9. Repos afetados

| Repo | O quê |
|---|---|
| `codex-technomanticus` (público) | Templates, campo `progresso`, callout `[!convite]`, queries dataview, documentação no guia, piloto Senda Frontend |
| `codex-technomanticus-site` (Quartz) | CSS do callout `[!convite]`, omissão da seção `## Progresso` na renderização |
| `codex-technomanticus-apocrypha` (privado) | **Não tocar nesta spec**. Pendências em `docs/apocrypha-pendencias.md` |

## 10. Piloto: Senda Frontend

A Senda Frontend é escolhida como piloto porque o usuário está estudando frontend ativamente — feedback imediato sobre a utilidade do sistema.

### 10.1 Estado atual

Senda Frontend tem 4.1 KB e é **100% conteúdo "ofensivo"**: o arquivo é um sumário interno (`[[#React]]`, `[[#Frameworks]]`, etc., wikilinks pra headings do próprio arquivo) seguido de seções com links externos pros sites/artigos/docs (React, TanStack, NextJS, MUI, Mantine, etc.). **Zero wikilinks pra notas de domínio**.

Pelo modelo de estantes (§4.3), a Senda Frontend é **transversal**: aponta pra notas em múltiplos domínios — `JavaScript/` (core), `TypeScript/`, `HTML/`, `CSS/`, `React/`, `Frontend/` (engenharia), `Ferramentas/`. Essas estantes ainda não existem nesse formato; o conhecimento frontend hoje está principalmente em `03-Dominios/Tecnologia/JavaScript/Frontend/` (subpasta agrupadora a desfazer no trabalho subsequente §13).

### 10.2 Migração

Em ordem:

1. **Criar estantes mínimas** que a senda piloto vai referenciar:
   - `03-Dominios/Tecnologia/Frontend/` (engenharia frontend, disciplina)
   - `03-Dominios/Tecnologia/React/`
   - `03-Dominios/Tecnologia/TypeScript/`
   - `03-Dominios/HTML/` (se a senda abordar)
   - `03-Dominios/CSS/` (se a senda abordar)
   Cada estante nasce com seu próprio `index.md` (ou `README.md`, conforme padrão do vault). **Não** migrar agora as notas existentes em `JavaScript/Frontend/` para essas estantes — isso é trabalho subsequente (§13).
2. **Auditoria do conteúdo atual da senda**: enumerar os ~30 links externos e ~15 seções da Senda Frontend, mapear cada um pra qual estante nova ele pertencerá (React vai pra `React/`, padrões frontend vão pra `Frontend/`, etc.).
3. **Criar notas-stub** nas estantes apropriadas: para cada conceito identificado, uma nota mínima (frontmatter + esqueleto). Notas nascem como `status: seedling` com `progresso: pendente`.
4. **Mover links externos pra callouts `[!convite]`** dentro das notas de domínio correspondentes.
5. **Reescrever a Senda Frontend** seguindo o template canônico (§6.1) — apenas wikilinks ordenados pras notas das estantes. `maturity: minimal` na primeira versão; evolui pra `structured` quando o usuário identificar fases naturais. Frontmatter `domain` aponta pro domínio principal da senda — `[[03-Dominios/Tecnologia/Frontend/index]]`.
6. **Adicionar bloco dataview de progresso** (§6.3).
7. **Aplicar `progresso` em notas referenciadas** com base no estado real do usuário — `andamento` no que está estudando, `pendente` no resto.
8. **Validar**: abrir no Obsidian, verificar agregação. Construir o site (Quartz), verificar renderização e CSS do callout.

Nota: a migração da Senda Frontend é, na prática, **mais criação de domínios do que migração de senda**. Isso é honesto sobre o estado atual e serve como template pro tipo de trabalho que outras sendas exigirão (a skill `/migrar-senda` proposta em §13 deve incorporar esse fluxo, e a reorganização completa dos domínios JavaScript é spec própria).

### 10.3 Critério de sucesso do piloto

- Senda Frontend tem apenas wikilinks pra notas de `03-Dominios/Tecnologia/Frontend/`.
- Bloco dataview no Obsidian mostra contagens corretas.
- Nenhum link externo na senda; todos migrados a callouts `[!convite]` nas notas de domínio.
- Site Quartz renderiza a senda sem expor o bloco dataview ao visitante; callouts `[!convite]` têm estilo dedicado.
- O usuário valida subjetivamente: "ao abrir essa senda, sei imediatamente onde estou".

## 11. Plano de execução

Em ordem (independências entre passos permitem paralelismo, mas a ordem abaixo é mental):

1. Documentar modelo conceitual em `00-Meta/guia/sendas-e-dominios.md` (estrutura atual já tem `Como usar este vault.md`, `Convenções de escrita.md`, `Decisões do vault.md`, `Wikilinks e MOCs.md` — o novo arquivo adere ao mesmo padrão).
2. Atualizar `00-Meta/templates/trail.md` com o template canônico (§6.1).
3. Atualizar `Template - Nota.md` com `progresso: pendente` e seção `## Aprofundamento`.
4. Atualizar `Template - Glosa.md` com `progresso: andamento`.
5. Documentar a convenção `[!convite]` em `00-Meta/guia/`.
6. Aplicar piloto na Senda Frontend (§10) — inclui criar `03-Dominios/Tecnologia/Frontend/` se a decisão de §10.2 passo 1 for criar domínio dedicado.
7. Adicionar CSS do callout `[!convite]` no `codex-technomanticus-site`.
8. Verificar renderização do site após próximo deploy.
9. Self-review: abrir a Senda Frontend no Obsidian, confirmar agregação correta.

## 12. Riscos e validações

| Risco | Mitigação |
|---|---|
| Bloco dataview lento em vault grande | Queries são restritas a `outgoing([[]])` (links saindo da própria senda) — escala com tamanho da senda, não do vault. |
| Versão `structured` com agregação por fase exige Dataview JS | Mínimo viável adota fallback (agregação total). Evoluir só se necessário. |
| Quartz expor o bloco dataview no site como código bruto | Config do Quartz pra omitir seção `## Progresso` (decisão validada na implementação do piloto). |
| Callout `[!convite]` quebrar em outros consumidores (tema do Obsidian sem suporte a callouts custom) | Callouts custom degradam graciosamente — fallback de estilo genérico. Aceitável. |
| Migração das outras sendas ficar parada por inércia | Sugerir skill `/migrar-senda` como trabalho subsequente; piloto valida o método antes de automatizar. |

## 13. Trabalhos subsequentes sugeridos

Em ordem de prioridade aproximada (não vinculante):

1. **Reorganização completa dos domínios JavaScript** (modelo §4.3): migrar `03-Dominios/Tecnologia/JavaScript/Backend/` pra novo `03-Dominios/Tecnologia/Node/` (ou `Backend/`); migrar `03-Dominios/Tecnologia/JavaScript/Frontend/` pras estantes específicas (`React/`, `Vue/`, etc., `Frontend/` disciplina); `JavaScript/` fica só com Core. Criar estantes faltantes (`HTML/`, `CSS/` se ainda não existirem em escala). Pode virar spec própria.
2. **Skill `/migrar-senda <nome>`**: automatiza a auditoria + migração de uma senda existente ao novo formato. Identifica conteúdo "ofensivo" (texto, links externos, exercícios), sugere quebra em notas atômicas nas estantes corretas, aplica template canônico. Reduz custo de migrar as 9 sendas restantes.
3. **Refatoração da Senda IA**: trabalho dedicado, provavelmente uma sessão inteira. Volume grande de conteúdo factual a mover pro domínio IA.
4. **Dashboard agregado no apocrypha**: visão consolidada de progresso cross-senda. Vide `docs/apocrypha-pendencias.md`.
5. **Daily notes do Obsidian**: integrar ao pipeline pra journal de estudo. Pendências em `docs/perguntas-abertas.md` (bloco "Daily notes do Obsidian").
6. **Pipeline glosa → domínio**: clarificar critério, ato e vínculos. Vide `docs/perguntas-abertas.md` (bloco "Glosa → Domínio").
7. **Ordem global e "o que estudar hoje?"**: depende de §3-5 acima.
8. **Cross-vault awareness** (`cta` como tomo irmão de `ct`): pendência geral do apocrypha.

## 14. Aceitação

A spec é considerada implementada quando:

- [ ] Templates atualizados em `00-Meta/templates/`.
- [ ] Documentação de modelo conceitual e convenção `[!convite]` em `00-Meta/guia/`.
- [ ] Senda Frontend reescrita seguindo template canônico, sem conteúdo "ofensivo".
- [ ] Bloco dataview de progresso na Senda Frontend rendendo agregação correta no Obsidian.
- [ ] Notas de `03-Dominios/Tecnologia/Frontend/` referenciadas pela senda têm o campo `progresso` com valor real (não placeholder).
- [ ] CSS do callout `[!convite]` aplicado no `codex-technomanticus-site` e validado em build local ou após deploy.
- [ ] Site renderiza a Senda Frontend sem expor bloco dataview; callouts `[!convite]` aparecem com estilo dedicado.
- [ ] `docs/apocrypha-pendencias.md` e `docs/perguntas-abertas.md` atualizados com itens deferred (já feito em sessão).
