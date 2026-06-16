---
title: "Galho Complexidade de Software — design (Fundamentos, galho 12)"
created: 2026-06-16
type: spec
status: draft
publish: false
tags:
  - meta
  - spec
  - fundamentos
  - complexidade-de-software
---

# Galho Complexidade de Software — design

## Contexto

Primeiro galho a ser construído do domínio Fundamentos, conforme o meta-plano
`00-Meta/specs/2026-06-15-fundamentos-meta-planejamento-design.md` (galho 12, Camada C).
É o galho mais autoral do domínio: cruza com o cluster `IA/O Lado Sombrio da IA` e com o
material de blog sobre débito cognitivo.

**Espinha (teste de inclusão):** *isso ajuda a entender ou gerenciar a complexidade do
software?* Se não responde, não entra. Esse teste impede o galho de virar "gaveta de
Engenharia de Software" — daí o nome **Complexidade de Software** (e não "Engenharia de
Software", que prometia demais).

**Audiência:** dev senior. Diferente dos galhos Java, a relevância de entrevista aqui é
*parcial* — o valor primário é formação conceitual e articulação de trade-offs. Registro
didático Feynman (analogias, perguntas retóricas, callouts, resumo em 1 linha), conforme
a prática cravada na skill `enriquecer-nota`.

## Fronteiras

- **Com `IA/O Lado Sombrio da IA` (os débitos):** o mesmo tópico vive nos *dois* galhos sob
  *perspectivas diferentes* — Lado Sombrio trata os débitos sob a lente da IA (aceleração,
  agentes, custos humanos); Complexidade de Software trata sob a lente do desenvolvimento
  *em geral* (atemporal, stack-agnóstico). Cross-linkados; divergem com o tempo. Isto é
  aplicação deliberada do princípio *redundância entre notas é reforço* (linkar, não podar).
  **Nada é movido de IA pra cá.** A nota `Débito cognitivo` (IA, `publish: true`) permanece;
  ganha link para a nota conceitual `11 - Dívida cognitiva` deste galho.
- **Com `Arquitetura`:** Design Patterns, Arquitetura de Software, System Design ficam em
  `Arquitetura/` (regra anti-duplicação do meta-plano). Este galho no máximo linka pra lá.

## Migrações (da raiz de Fundamentos para a pasta do galho)

Duas notas existentes na raiz de `03-Dominios/Fundamentos/` viram notas-âncora do galho:

| Nota atual (raiz) | Vira | Fase |
| --- | --- | --- |
| `O programa como teoria.md` | `04 - O programa como teoria` | Iniciado |
| `Abstrações que vazam.md` | `06 - Abstrações que vazam` | Adepto |

Wikilinks por nome continuam resolvendo após a mudança de pasta. O MOC do domínio
(`Fundamentos/index.md` e `Fundamentos.md`) é atualizado: remove as duas da raiz, adiciona
callout/entrada do galho.

**Atenção ao alias "Teoria do sistema":** hoje é alias da nota do Naur. Ele migra para a
nota `15 - Pensamento sistêmico` (que é o que "teoria do sistema" de fato designa). A nota
do Naur mantém os demais aliases (theory building, etc.).

## Estrutura do galho

- Pasta: `03-Dominios/Fundamentos/Complexidade de Software/`
- Notas atômicas `NN - Título.md`, flat, com frontmatter incluindo `fase: iniciado|adepto|magus`
  e tags com a fase + `complexidade-de-software` + `fundamentos`.
- `index.md` (`type: moc`) no padrão do vault: TL;DR, "Sobre este galho" (com o que **não**
  cobre), seções Iniciado/Adepto/Magus com lista numerada, "Rotas alternativas", dataview
  `TABLE fase, status, updated`, "Veja também".
- **Dicionário de Fundamentos:** novos verbetes conforme os termos surgem (complexidade
  essencial/acidental, abstração vazada — já existe —, débito técnico/cognitivo/intenção,
  carga cognitiva, entropia de software, Lei de Conway, Lei de Hyrum) via `/verbete`.
- **Tronco:** entrada do galho no MOC do domínio Fundamentos.

## As 16 notas

### Iniciado — o problema (por que software é difícil)

1. `01 - A complexidade como problema central` — complexidade como a dificuldade-raiz do
   software; visão geral; Brooks, *No Silver Bullet*.
2. `02 - Complexidade essencial vs. acidental` — a distinção de Brooks; *Out of the Tar Pit*
   (Moseley & Marks) e a complexidade vinda do estado.
3. `03 - Simplicidade não é facilidade` — Hickey, *Simple Made Easy* (simple ≠ easy;
   complecting).
4. `04 - O programa como teoria` — **(migra)** Naur, theory-building; conhecimento tácito
   (Polanyi); knowing-that × knowing-how (Ryle).

### Adepto — os mecanismos (como gerenciamos complexidade e onde falha)

5. `05 - Abstração: a ferramenta central` — o que é abstração; information hiding (Parnas);
   esconder decisões voláteis.
6. `06 - Abstrações que vazam` — **(migra)** Spolsky, Lei das Abstrações Vazadas; Lei de
   Hyrum como extremo lógico.
7. `07 - Módulos profundos e rasos` — Ousterhout, *A Philosophy of Software Design*; deep
   vs. shallow modules; complexidade incremental.
8. `08 - Carga cognitiva e legibilidade` — cognitive load no código; princípio da menor
   surpresa; obscuridade; ressalva sobre métricas (complexidade ciclomática).
9. `09 - As três dívidas do software` — Triple Debt Model de Storey: técnica/cognitiva/intenção;
   as três independentes e interagentes.
10. `10 - Dívida técnica` — Cunningham (a metáfora original); juros, atalhos estruturais no código.
11. `11 - Dívida cognitiva` — conceito geral (erosão do entendimento compartilhado);
    cross-link com `IA/O Lado Sombrio da IA/Débito cognitivo` (perspectiva IA).
12. `12 - Dívida de intenção` — Storey/Osmani/Fowler; ausência de rationale externalizado;
    specs/ADRs/AGENTS.md como ledger de intenção.

### Magus — gerir no tempo e no todo

13. `13 - Entropia de software e decaimento` — bit rot, broken windows, big ball of mud.
14. `14 - Manutenção e evolução` — legado como gestão de complexidade no tempo; *make the
    hard change easy* (Beck).
15. `15 - Pensamento sistêmico` — feedback, emergência, parte vs. todo (alias "Teoria do
    Sistema").
16. `16 - Lei de Conway` — complexidade organizacional ↔ arquitetural; inverse Conway maneuver.

## Fontes

**Glosas no vault (já criadas):**
- `02-Glosas/2026-from-technical-debt-to-cognitive-and-intent-debt.md` — Storey (arXiv), fonte
  primária do Triple Debt Model
- `02-Glosas/2026-the-intent-debt.md` — Addy Osmani
- `02-Glosas/2026-fowler-fragments-triple-debt-model.md` — Martin Fowler
- `02-Glosas/2026-intent-debt-the-ai-era-debt-nobody-is-tracking.md` — Developers Digest
- `02-Glosas/2026-cognitive-debt-hidden-risk-ai-driven-software-development.md` — Storey (DX)
- `02-Glosas/2026-cognitive-surrender.md` — Osmani
- (verificar) glosas de comprehension debt / deskilling já referenciadas em Lado Sombrio

**Canônicos a citar (com verificação adversarial onde houver dado factual):**
- Brooks — *No Silver Bullet* e *The Mythical Man-Month*
- Ousterhout — *A Philosophy of Software Design*
- Moseley & Marks — *Out of the Tar Pit*
- Hickey — *Simple Made Easy* (palestra)
- Parnas — *On the Criteria To Be Used in Decomposing Systems into Modules* (1972)
- Naur — *Programming as Theory Building* (1985)
- Cunningham — a metáfora original de dívida técnica
- Conway — *How Do Committees Invent?* (1968)

## Anatomia de cada nota

- TL;DR (callout `abstract`), "O que é", desenvolvimento em registro didático, "Armadilhas
  comuns" quando couber, "Referências", "Veja também".
- Seção **"Em entrevista"** apenas nas notas onde o tema realmente cai (ex.: dívida técnica,
  trade-offs de abstração) — não forçar nas notas teóricas/filosóficas.
- Honestidade epistêmica: distinguir o que passou por verificação de fonte do que é leitura
  interpretativa (padrão já usado em `Abstrações que vazam`).

## Fora de escopo

- Processos/metodologia (scrum, estimativa, requisitos) — não é a espinha do galho.
- As manifestações AI-specific dos débitos — ficam em `IA/O Lado Sombrio da IA`.
- Design Patterns e estilos arquiteturais — ficam em `Arquitetura/`.

## Sequência de construção sugerida

1. Criar a pasta + `index.md` (MOC) com as 16 entradas como esqueleto.
2. Migrar e renumerar as duas notas-âncora (04 Naur, 06 Spolsky); ajustar aliases e o MOC
   do domínio.
3. Escrever as notas Iniciado (01–03), depois Adepto (05, 07–12), depois Magus (13–16).
4. Atualizar `Débito cognitivo` (IA) e o índice do Lado Sombrio com os cross-links.
5. Verbetes no Dicionário de Fundamentos.
6. `verificar-wikilinks` na pasta antes de fechar.
