---
title: "Roadmap — Complexidade de Software"
created: 2026-07-31
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Complexidade de Software

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`.

**Galho:** `03-Dominios/Engenharia/Complexidade de Software`
**Diagnóstico:** 2026-07-31
**Última execução:** 2026-07-31 — enriquecimento completo, 17/17

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (iniciado/adepto/magus)
**Piso de linhas:** ver ajuste 3 abaixo — **não aplicado como gap**

### Ajustes de régua para este galho

O checklist genérico **sub-avalia este galho**, porque foi calibrado para notas de tecnologia
(ferramenta, código, produção) e este é o galho mais **teórico** do vault — Brooks, Naur,
Hickey, Parnas, Ousterhout, Lehman, Meadows, Conway. Quatro ajustes, decididos com o autor
em 2026-07-31:

1. **E4 (Casos práticos) só onde o caso ilustra de verdade.** Critério do autor: *"se houver
   casos práticos relevantes, que ilustrem os conceitos, sim; se for apenas criação pra cumprir
   agenda, não."* Em 11 das 16 notas o material ilustrativo já existe **embutido na prosa**
   (é assim que capítulo de livro funciona) e extraí-lo para uma seção `## Casos práticos`
   seria pior. E4 fica **N/A** nessas. Nas 5 em que há casos de verdade — e apenas
   desagrupados (06 ecossistemas · 10 reconhecimento/falência · 13 manifestações ·
   15 arquétipos · 16 Vista/Mozilla/Amazon/Spotify) — E4 conta como **✅**.

2. **E5 é gap real, mas o galho já resolve metade do problema por outra via.** Nenhuma nota
   tem `## O que vem a seguir`. Em compensação, **toda nota abre com uma ponte narrativa
   para trás**, retomando explicitamente a anterior ("A nota anterior fechou com uma
   promessa…", "A nota anterior terminou com uma sentença incômoda…"). A coesão da trilha
   existe e é forte — falta só a ponte **para frente**. Custo baixo, ganho real.

3. **Piso de linhas NÃO aplicado.** Vale a regra do vault de que o **padrão capítulo de livro
   substitui o piso**. As 16 leem como capítulo (abertura por cenário, divulgação progressiva,
   mecanismo explicado). Nove ficam abaixo do piso nominal da fase — 06, 07, 08, 09, 11
   (adepto <400) e **as quatro magus** 13-16 (<500) — e isso está registrado como observação,
   **não como gap**. Engordar nota que já cumpre a função seria padding.

4. **`## Em entrevista` é a seção-lente do galho.** Presente em **16/16**, com qualidade alta
   (frase de efeito, evidência empírica, limites da tese, armadilha de cargo cult). O checklist
   genérico não a prevê; ela é o equivalente local do "para que serve saber isso" e deve ser
   **preservada** em qualquer enriquecimento.

### O que o diagnóstico encontrou de verdade

O miolo conceitual é **forte e uniforme**: E1, E2, E3, P2 e L1 passam em **16/16** — TL;DR denso,
abertura por problema com ponte para a nota anterior, 4-5 diagramas Mermaid por nota, mecanismo
causal explicado (não só rótulo), e wikilink cross-galho. Quatro notas ancoram em glosas do
vault (04, 09, 11, 12) e **todas as 5 glosas referenciadas resolvem** — nenhum link quebrado.

O que falta é **casca padronizada**, não conteúdo: o galho foi escrito antes da anatomia atual
da nota. Três gaps são transversais (E5, E6, E7 em 16/16; M1 em 16/16) e dois são pontuais
(L2 em 4 notas; E8 em 15).

| Gap | Alcance no diagnóstico | Natureza | Estado |
|-----|------------------------|----------|--------|
| E5 ponte para frente | 16/16 | mecânico — o fio narrativo já existe, falta o fecho | ✅ 2026-07-31 |
| E6 seção de inglês | 16/16 | mecânico — o vocabulário EN já está inline, em itálico | ✅ 2026-07-31 |
| E7 tabela PT↔EN | 16/16 | mecânico — consolidar termos já usados | ✅ 2026-07-31 |
| E8 `## Armadilhas comuns` | 15/16 (só 05 passava) | mecânico — `[!warning]` existem, faltam seção e volume ≥3 | ✅ 2026-07-31 |
| L2 URL externa | 4/16 (07, 08, 09, 11) | **substantivo** — zero links externos nessas | ✅ 2026-07-31 |
| M1 vídeo/podcast | 17/17 | **substantivo** — passe transversal de pesquisa | ✅ 16/17 (ver abaixo) |

> [!warning] Os `[!tip]` que já existiam não eram mídia
> Todas as notas tinham callouts `[!tip]`, mas do tipo *"Como isso aparece numa entrevista"*.
> Nenhum linkava vídeo ou podcast — M1 falhava em 17/17 apesar da contagem alta de `[!tip]`.
> Os callouts de mídia inseridos em 2026-07-31 usam o título `[!tip] Assista — <vídeo>`, o que
> os distingue à vista e evita repetir o erro de contagem num diagnóstico futuro.

> [!info] M1: 16/17, e a exceção é deliberada
> A **nota 02 (Complexidade essencial vs. acidental) ficou sem vídeo**. Buscas por *No Silver
> Bullet* e *Out of the Tar Pit* só devolveram canais pequenos de qualidade duvidosa, e o único
> candidato de peso (uma sessão do Papers We Love) não teve o conteúdo confirmado. Vale o mesmo
> critério do autor para casos práticos: **melhor a ausência declarada do que preencher pra
> cumprir agenda.** Se aparecer uma palestra boa sobre Brooks ou a Tar Pit, é a única lacuna
> de mídia do galho.

### Pendências de galho (fora do nota-a-nota)

- ✅ **Capstone:** **escrito em 2026-07-31** — [[17 - Capstone - O diagnóstico diferencial da complexidade]].
  A nota 16 já trazia a **síntese conceitual** do galho ("E aqui o galho fecha…" + a frase sobre
  o org chart), então o capstone **não é um resumo**: é o **caso trabalhado** que o vault faz nos
  outros ~20 capstones. Recorte escolhido: **diagnosticar**, não tratar — o tratamento é de
  Arqueologia e Restauração, e a fronteira está declarada em callout `[!info]` na abertura.
  Fecha também a ponte que faltava: o capstone de Arqueologia já linkava para a nota 04 daqui,
  e a volta agora existe.
- ✅ **`publish`:** as 16 notas estavam `publish: false` (o `index.md` já era `true`).
  **Publicadas em 2026-07-31** (17/17, capstone incluído).
- ✅ **Roadmap central:** `00-Meta/Roadmap.md` descrevia este galho como "🟡 17 notas —
  consolidar", o que estava errado. **Corrigido em 2026-07-31** (🟡 → 🟢), na tabela de
  Engenharia e no item de Tier 2.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 17 |
| ⬜ pendente | 0 |
| ➖ não precisa | 0 |
| ✅ feita | 17 |
| % concluído | **100%** |

> [!success] Galho fechado em 2026-07-31 — escrito e enriquecido
> Diagnóstico, capstone, publicação e enriquecimento completo no mesmo dia. Execução em 6 blocos
> de ≤3 subagentes Sonnet (nunca fan-out massivo), mais um passe transversal de mídia feito
> centralmente para não deixar subagente inventar ID de YouTube.
>
> **Uma lacuna consciente:** M1 na nota 02 (ver callout acima). Nada mais pendente.
>
> Daqui em diante: consulta e manutenção.

---

## Notas

#### 01 - A complexidade como problema central   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 441 linhas · fase: iniciado · status: growing
- **Núcleo/gaps:** E5 · E6 · E7 · E8 (3 `[!warning]` existem, dispersos, sem seção) · M1. E4 N/A (conceitual)
- **Score:** 6/10
- **Plano de execução:**
  - Fecha com `## O que vem a seguir` — ponte narrativa para [[02 - Complexidade essencial vs. acidental]], entregando a distinção de Brooks como a pergunta que a nota deixa em aberto → ativa E5
  - Consolida os 3 `[!warning]` (falsa esperança da bala de prata · tactical tornado · erro do júnior) sob `## Armadilhas comuns` → ativa E8
  - Cria seção de inglês + tabela PT↔EN com os termos já em itálico no corpo: *complexity · change amplification · cognitive load · unknown unknowns · tactical/strategic programming · silver bullet* → ativa E6, E7
  - Embute `[!tip]` com vídeo/palestra sobre o argumento de Brooks ou a tese de Ousterhout → ativa M1
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 02 - Complexidade essencial vs. acidental   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 418 linhas · fase: iniciado · status: growing
- **Núcleo/gaps:** E5 · E6 · E7 · E8 (só 2 `[!warning]`, sem seção) · M1. E4 N/A (conceitual)
- **Score:** 6/10
- **Plano de execução:**
  - Fecha com `## O que vem a seguir` para [[03 - Simplicidade não é facilidade]] — a ponte natural é que reduzir o acidental exige saber o que é *simples*, e Hickey mostra que não é o que se pensa → ativa E5
  - Cria `## Armadilhas comuns` com os 2 `[!warning]` existentes (irredutibilidade do essencial · a linha não é régua absoluta) + um terceiro sobre confundir estado acidental de infraestrutura com estado essencial do negócio → ativa E8
  - Seção de inglês + tabela PT↔EN: *essential/accidental complexity · tar pit · mutable state · referential transparency · silver bullet* → ativa E6, E7
  - Embute vídeo sobre *No Silver Bullet* ou *Out of the Tar Pit* → ativa M1
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 03 - Simplicidade não é facilidade   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 457 linhas · fase: iniciado · status: growing
- **Núcleo/gaps:** E5 · E6 · E7 · E8 (3 `[!warning]` dispersos, sem seção) · M1. E4 N/A (conceitual)
- **Score:** 6/10
- **Plano de execução:**
  - Fecha com `## O que vem a seguir` para [[04 - O programa como teoria]] — a ponte é que *complecting* destrói algo que não está no texto do programa, e Naur nomeia esse algo → ativa E5
  - Consolida os 3 `[!warning]` sob `## Armadilhas comuns` → ativa E8
  - Seção de inglês + tabela PT↔EN: *simple ≠ easy · to complect · interleaving · braid · guardrails · incidental* → ativa E6, E7
  - Embute a gravação de *Simple Made Easy* (Hickey) — é o vídeo canônico da nota → ativa M1
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 04 - O programa como teoria   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 410 linhas · fase: iniciado · status: growing
- **Núcleo/gaps:** E5 · E6 · E7 · E8 (1 `[!warning]`, sem seção) · M1. E4 N/A (conceitual)
- **Score:** 6/10
- **Plano de execução:**
  - Fecha com `## O que vem a seguir` para [[05 - Abstração - a ferramenta central]] — a ponte é que, se a teoria não cabe no texto, a pergunta vira *o que o texto consegue carregar* → ativa E5
  - Cria `## Armadilhas comuns` com ≥3 `[!warning]`: confundir documentação com teoria · achar que onboarding transfere teoria por leitura · tratar rotatividade como problema de RH e não de erosão de teoria → ativa E8
  - Seção de inglês + tabela PT↔EN: *theory building · tacit knowledge · program revival · ryle's sense of theory* → ativa E6, E7
  - Embute vídeo/podcast sobre Naur e *Programming as Theory Building* → ativa M1
  - Preserva os links já corretos para a glosa de débito cognitivo e para O Lado Sombrio da IA — verificados, resolvem
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 05 - Abstração - a ferramenta central   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 510 linhas · fase: adepto · status: growing · **melhor nota do galho**
- **Núcleo/gaps:** E5 · E6 · E7 · M1. E4 N/A (conceitual). **E8 passa** (seção + 4 `[!warning]`)
- **Score:** 8/11
- **Plano de execução:**
  - Fecha com `## O que vem a seguir` para [[06 - Abstrações que vazam]] — a ponte é que toda a nota defendeu a abstração, e a próxima mostra onde a promessa quebra → ativa E5
  - Seção de inglês + tabela PT↔EN: *information hiding · deep/shallow module · interface vs. implementation · indirection · leaky abstraction* → ativa E6, E7
  - Embute vídeo de Ousterhout (*A Philosophy of Software Design*) ou palestra sobre Parnas → ativa M1
  - **Não mexer** em `## Armadilhas comuns`, `## Boas vs. más abstrações` nem nos exemplos de código — é a nota mais bem estruturada do galho e o modelo a seguir nas demais
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 06 - Abstrações que vazam   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 328 linhas · fase: adepto · status: growing · abaixo do piso nominal (ver ajuste 3 — não é gap)
- **Núcleo/gaps:** E5 · E6 · E7 · E8 (tem a seção, mas só 1 `[!warning]`) · M1. **E4 passa** (`## Exemplos por ecossistema`: TCP, GC, JIT, ORM)
- **Score:** 8/12
- **Plano de execução:**
  - Fecha com `## O que vem a seguir` para [[07 - Módulos profundos e rasos]] — a ponte é que, se abstração vaza, a pergunta vira quanto ela precisa cobrar de interface para valer a pena → ativa E5
  - Expande `## Armadilhas comuns` de 1 para ≥3 `[!warning]`, aproveitando material já presente em "Críticas e refinamentos" e "Como conviver com vazamentos" → ativa E8
  - Seção de inglês + tabela PT↔EN: *leaky abstraction · law of leaky abstractions · Hyrum's law · abstraction tax* → ativa E6, E7
  - Embute vídeo/podcast sobre a Lei de Hyrum ou o ensaio de Spolsky → ativa M1
  - **12 URLs externas já presentes** — L2 sólido, não precisa pesquisa
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 07 - Módulos profundos e rasos   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 385 linhas · fase: adepto · status: growing · abaixo do piso nominal (não é gap)
- **Núcleo/gaps:** **L2 (zero URLs externas — núcleo)** · E5 · E6 · E7 · E8 (nenhum `[!warning]`) · M1. E4 N/A
- **Score:** 6/11
- **Plano de execução:**
  - **Pesquisa e adiciona `## Referências` com URLs verificáveis** — Ousterhout (*A Philosophy of Software Design*, página do livro/Stanford) e o debate público Ousterhout × "Uncle Bob" sobre funções pequenas, que a nota já discute em prosa sem linkar → ativa L2 (núcleo)
  - Fecha com `## O que vem a seguir` para [[08 - Carga cognitiva e legibilidade]] — a ponte já está escrita no corpo ("a *cognitive load* que a nota 08 detalha"), só falta a seção → ativa E5
  - Cria `## Armadilhas comuns` com ≥3 `[!warning]`: classitis · confundir "muitas classes pequenas" com bom design · empurrar complexidade para cima em vez de para baixo — todos já tratados no corpo → ativa E8
  - Seção de inglês + tabela PT↔EN: *deep/shallow module · classitis · information leakage · define errors out of existence · pass-through method* → ativa E6, E7
  - Embute palestra de Ousterhout → ativa M1
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 08 - Carga cognitiva e legibilidade   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 371 linhas · fase: adepto · status: growing · abaixo do piso nominal (não é gap)
- **Núcleo/gaps:** **L2 (zero URLs externas — núcleo)** · E5 · E6 · E7 · E8 (nenhum `[!warning]`) · M1. E4 N/A
- **Score:** 5/10
- **Plano de execução:**
  - **Pesquisa e adiciona `## Referências` com URLs** — Sweller (cognitive load theory), Team Topologies (carga cognitiva de time, que a nota já usa) e a literatura de legibilidade → ativa L2 (núcleo)
  - Fecha com `## O que vem a seguir` para [[09 - As três dívidas do software]] — a ponte é que carga cognitiva alta e sustentada vira dívida, e a nota 09 dá o modelo → ativa E5
  - Cria `## Armadilhas comuns` com ≥3 `[!warning]`, aproveitando `## A armadilha das métricas` (complexidade ciclomática como proxy ruim) e a confusão carga-vs-dívida que a nota já separa → ativa E8
  - Seção de inglês + tabela PT↔EN: *cognitive load (intrinsic/extraneous/germane) · chunking · principle of least astonishment · obscurity* → ativa E6, E7
  - Embute vídeo sobre carga cognitiva em engenharia (Team Topologies é o filão óbvio) → ativa M1
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 09 - As três dívidas do software   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 395 linhas · fase: adepto · status: growing · abaixo do piso nominal (não é gap) · **nota-eixo** (abre o bloco 09-12)
- **Núcleo/gaps:** **L2 (zero URLs externas — núcleo; só há wikilinks para glosas)** · E5 · E6 · E7 · E8 (1 `[!warning]`) · M1. E4 N/A
- **Score:** 5/10
- **Plano de execução:**
  - **Adiciona URLs externas em `## Fontes`** — as 4 glosas linkadas (Fowler/triple-debt, from-technical-debt-to-cognitive-and-intent, intent-debt) já contêm as URLs originais; puxar de lá é barato e não exige pesquisa nova → ativa L2 (núcleo)
  - Fecha com `## O que vem a seguir` para [[10 - Dívida técnica]] — a ponte é que das três dívidas a técnica é a única com literatura madura, e é por onde se começa → ativa E5
  - Expande `## Como cada dívida é mal gerida` em `## Armadilhas comuns` com ≥3 `[!warning]` → ativa E8
  - Seção de inglês + tabela PT↔EN: *technical/cognitive/intent debt · triple debt model · debt interest · principal* → ativa E6, E7
  - Embute vídeo/podcast sobre o Triple Debt Model (Storey) → ativa M1
  - Verifica o embed de `triple-debt-model.jpg` — imagem presente na pasta
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 10 - Dívida técnica   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 460 linhas · fase: adepto · status: growing
- **Núcleo/gaps:** E5 · E6 · E7 · E8 (4 `[!warning]`, mas sem seção dedicada) · M1. **E4 passa** (`## Como se reconhece` + `## Falência e o mito do rewrite`)
- **Score:** 7/11
- **Plano de execução:**
  - Fecha com `## O que vem a seguir` para [[11 - Dívida cognitiva]] — a ponte é que a dívida técnica é a visível e mensurável, e a próxima trata da que ninguém consegue medir → ativa E5
  - Agrupa os 4 `[!warning]` existentes sob `## Armadilhas comuns` → ativa E8
  - Seção de inglês + tabela PT↔EN: *technical debt · principal and interest · prudent/reckless × deliberate/inadvertent · a mess is not a technical debt · bankruptcy · rewrite* → ativa E6, E7
  - Embute vídeo de Fowler (quadrante de dívida técnica) ou de Cunningham explicando a metáfora original → ativa M1
  - **7 URLs já presentes** — L2 sólido
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 11 - Dívida cognitiva   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 342 linhas · fase: adepto · status: growing · abaixo do piso nominal (não é gap)
- **Núcleo/gaps:** **L2 (zero URLs externas — núcleo)** · E5 · E6 · E7 · E8 (1 `[!warning]`) · M1. E4 N/A
- **Score:** 5/10
- **Plano de execução:**
  - **Adiciona URLs externas em `## Fontes`** — puxar da glosa `2026-from-technical-debt-to-cognitive-and-intent-debt` e da nota de Débito cognitivo em O Lado Sombrio da IA, ambas já linkadas → ativa L2 (núcleo)
  - Fecha com `## O que vem a seguir` para [[12 - Dívida de intenção]] — a ponte é que perder o entendimento é uma coisa, e nunca ter registrado a intenção é outra → ativa E5
  - Expande `## Sinais de alerta` em `## Armadilhas comuns` com ≥3 `[!warning]` → ativa E8
  - Seção de inglês + tabela PT↔EN: *cognitive debt · shared understanding · bus factor · theory loss* → ativa E6, E7
  - Embute vídeo/podcast sobre erosão de entendimento em times → ativa M1
  - **Preserva** `## A mesma ideia, sob a lente da IA` e o cross-link para O Lado Sombrio da IA — é a fronteira declarada do galho
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 12 - Dívida de intenção   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 471 linhas · fase: adepto · status: growing
- **Núcleo/gaps:** E5 · E6 · E7 · E8 (nenhum `[!warning]`) · M1. E4 N/A (conceitual). L2 magro (1 URL) mas passa
- **Score:** 6/10
- **Plano de execução:**
  - Fecha com `## O que vem a seguir` para [[13 - Entropia de software e decaimento]] — a ponte é que as três dívidas descrevem o estado, e agora entra o tempo → ativa E5. **É também a ponte entre blocos** (fim do Adepto → início do Magus); merece um parágrafo a mais
  - Cria `## Armadilhas comuns` com ≥3 `[!warning]` a partir de `## Como diagnosticar` e `## Como se paga` → ativa E8
  - Seção de inglês + tabela PT↔EN: *intent debt · rationale · cold start · ADR (architecture decision record) · shift to verification* → ativa E6, E7
  - Reforça `## Fontes` com as URLs das 4 glosas já linkadas (só 1 URL hoje) → fortalece L2
  - Embute vídeo/podcast sobre ADRs ou registro de decisão → ativa M1
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 13 - Entropia de software e decaimento   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 367 linhas · fase: magus · status: growing · abaixo do piso nominal (não é gap) · abre o bloco Magus
- **Núcleo/gaps:** E5 · E6 · E7 · E8 (2 `[!warning]`, sem seção) · M1. **E4 passa** (`## Como o decaimento se manifesta`)
- **Score:** 7/11
- **Plano de execução:**
  - Fecha com `## O que vem a seguir` para [[14 - Manutenção e evolução]] — a ponte já existe do outro lado (a nota 14 abre retomando esta); espelhar → ativa E5
  - Cria `## Armadilhas comuns` com ≥3 `[!warning]` a partir de `## O decaimento é o default` e `## Erosão e deriva arquitetural` → ativa E8
  - Seção de inglês + tabela PT↔EN: *bit rot · broken windows · big ball of mud · Lehman's laws · architectural erosion/drift · software gravity* → ativa E6, E7
  - Embute vídeo sobre Big Ball of Mud (Foote & Yoder) ou as leis de Lehman → ativa M1
  - **`## Em entrevista` desta nota é exemplar** (separa desgaste × decaimento, traz Lehman II, fecha com frase de efeito) — usar como modelo, não mexer
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 14 - Manutenção e evolução   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 306 linhas · fase: magus · status: growing · **a menor do galho** (não é gap, mas é a candidata mais forte a crescer)
- **Núcleo/gaps:** E5 · E6 · E7 · E8 (nenhum `[!warning]`) · M1. E4 N/A (conceitual)
- **Score:** 6/10
- **Plano de execução:**
  - Fecha com `## O que vem a seguir` para [[15 - Pensamento sistêmico]] — a ponte é que manter é agir sobre um sistema com feedback, e a próxima dá o instrumental → ativa E5
  - Cria `## Armadilhas comuns` com ≥3 `[!warning]`: tratar manutenção como atividade de segunda classe · regra do escoteiro virando refatoração oportunista sem teste · confundir "código legado" com "código velho" → todos já implícitos no corpo → ativa E8
  - Seção de inglês + tabela PT↔EN: *corrective/adaptive/perfective/preventive maintenance · legacy code · boy scout rule · make the change easy, then make the easy change · refactoring* → ativa E6, E7
  - Embute vídeo de Feathers (*Working Effectively with Legacy Code*) ou de Beck sobre a frase canônica → ativa M1
  - **Ponte de galho a criar:** esta nota é a fronteira natural com [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index|Arqueologia e Restauração de Software]], cujo capstone **já linka de volta** para a nota 04 deste galho. A volta não existe — adicionar
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 15 - Pensamento sistêmico   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 473 linhas · fase: magus · status: growing
- **Núcleo/gaps:** E5 · E6 · E7 · E8 (1 `[!warning]`) · M1. **E4 passa** (`## Arquétipos de sistema`)
- **Score:** 7/11
- **Plano de execução:**
  - Fecha com `## O que vem a seguir` para [[16 - Lei de Conway]] — a ponte é forte e vale explicitá-la: se o sistema é sócio-técnico, o org chart é parte do sistema → ativa E5
  - Cria `## Armadilhas comuns` com ≥3 `[!warning]` a partir de `## Pontos de alavancagem` (agir no ponto de baixa alavancagem) e dos arquétipos → ativa E8
  - Seção de inglês + tabela PT↔EN: *systems thinking · emergence · stocks and flows · feedback loop (reinforcing/balancing) · leverage points · system archetypes* → ativa E6, E7
  - Embute vídeo sobre Donella Meadows (*Thinking in Systems* / leverage points) → ativa M1
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 16 - Lei de Conway   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 443 linhas · fase: magus · status: growing · **nota de fecho conceitual do galho**
- **Núcleo/gaps:** E5 · E6 · E7 · E8 (tem a seção, mas só 2 `[!warning]`) · M1. **E4 passa** (Vista, Mozilla, Amazon, Spotify)
- **Score:** 7/11
- **Plano de execução:**
  - `## O que vem a seguir` aqui é **especial**: a nota já fecha o argumento do galho ("E aqui o galho fecha…" + a frase-síntese do org chart). A ponte não é para a nota 17, é para **fora** — o capstone (caso trabalhado) e os galhos vizinhos (Arquitetura, Arqueologia). Escrever como convite, não como "próxima aula" → ativa E5
  - Expande `## Armadilhas comuns` de 2 para ≥3 `[!warning]`, aproveitando o cargo cult do modelo Spotify e o diagnóstico errado do monólito distribuído, ambos já no corpo → ativa E8
  - Seção de inglês + tabela PT↔EN: *Conway's law · mirroring hypothesis · inverse Conway maneuver · socio-technical congruence · team topologies · two-pizza team · distributed monolith* → ativa E6, E7
  - Embute vídeo sobre Team Topologies ou a manobra inversa de Conway → ativa M1
  - **Não tocar** no bloco de fecho (linhas ~405-412) nem em `## Em entrevista` — são o melhor material do galho
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada

#### 17 - Capstone - O diagnóstico diferencial da complexidade   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-31)
- **Estado:** 326 linhas · fase: magus · status: growing · **escrita em 2026-07-31, já no padrão atual**
- **Núcleo/gaps:** — (só M1, o passe transversal de mídia). E4 N/A: a nota **inteira** é um caso trabalhado, extrair uma seção `## Casos práticos` seria redundante. P1 N/A (sem código)
- **Score:** 10/11
- **Plano de execução:**
  - — nenhuma. Nasce com E1, E2, E3 (3 Mermaid validados), E5, E6, E7, E8 (5 `[!warning]`), P2, L1, L2 e `## Em entrevista`. Entra no passe transversal de M1 junto com as demais
- **Resultado:** ✅ casca completa (E5/E6/E7/E8) + mídia verificada
