---
title: "Roadmap — Testes"
created: 2026-08-01
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Testes

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`.

**Galho:** `03-Dominios/Engenharia/Testes`
**Diagnóstico:** 2026-08-01
**Última execução:** 2026-08-01 — ondas 1-2 (notas 01-06)
**Spec do passe:** [[00-Meta/specs/2026-08-01-galho-testes-fechamento-design|passe de fechamento]]

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado 01-04 · Adepto 05-11 · Magus 12-16)
**Piso de linhas:** **APLICADO** (Iniciado ≥300 · Adepto ≥400 · Magus ≥500) — decisão do usuário, 2026-08-01.

### Ajustes de régua (registrados, não compensados)

Herdados da lição de Complexidade de Software: o checklist genérico sub-avalia galho
conceitual/estratégico. Registrar o ajuste é obrigatório; preencher seção pra cumprir
agenda é proibido.

1. **Piso de linhas — APLICADO.** ⚠️ **Decisão do usuário em 2026-08-01: o piso vale.** Isto
   revoga a suspensão provisória usada durante o diagnóstico. O passe deixa de ser só casca e
   passa a incluir **expansão real de conteúdo**. Piso: Iniciado ≥300 · Adepto ≥400 · Magus ≥500.

   Medição e déficit por nota (linhas reais em 2026-08-01):

   | Nota | Fase | Hoje | Piso | Déficit |
   |------|------|------|------|---------|
   | 01 | Iniciado | 301 | 300 | ✅ — |
   | 02 | Iniciado | 245 | 300 | +55 |
   | 03 | Iniciado | 285 | 300 | +15 |
   | 04 | Iniciado | 322 | 300 | ✅ — |
   | 05 | Adepto | 298 | 400 | +102 |
   | 06 | Adepto | 270 | 400 | +130 |
   | 07 | Adepto | 240 | 400 | +160 |
   | 08 | Adepto | 310 | 400 | +90 |
   | 09 | Adepto | 330 | 400 | +70 |
   | 10 | Adepto | 257 | 400 | +143 |
   | 11 | Adepto | 239 | 400 | +161 |
   | 12 | Magus | 260 | 500 | +240 |
   | 13 | Magus | 322 | 500 | +178 |
   | 14 | Magus | 311 | 500 | +189 |
   | 15 | Magus | 333 | 500 | +167 |
   | 16 | Magus | 286 | 500 | +214 |

   **Como fechar o déficit — nesta ordem:**
   1. **A casca já entrega boa parte.** `## Casos práticos`, `## O que vem a seguir`,
      `## Armadilhas comuns`, `## Fontes`, tabela PT↔EN e o `[!tip]` de mídia somam tipicamente
      **60–120 linhas**. Em 02, 03, 08 e 09 isso sozinho pode fechar o piso.
   2. **O resto é conteúdo técnico NOVO e sourced** — ângulo, mecanismo, exemplo trabalhado,
      diagrama Mermaid que carrega semântica. Nota substancial mora em ~440–540 linhas.
   3. **PROIBIDO padding.** Nada de reformular o mesmo parágrafo em outras palavras, listar
      ferramentas sem raciocínio, ou inflar callout para ganhar linha. Se o piso só fechar com
      enchimento, **declare o déficit** no roadmap em vez de encher — o registro honesto vale
      mais que o número batido.
   4. **Redundância entre notas é reforço** — linkar, nunca podar assunto repetido.
2. **E4 (Casos práticos)** só onde o caso é real. O galho carrega 5 experiências reais do
   usuário (MedEspecialista, TDD/comissão, tela de 30 campos, mock→fake, Awaitility,
   Testcontainers×H2), mapeadas no spec de origem. **Nunca fabricar** caso novo.
3. **E6/E7 (Inglês / PT↔EN)** — a nota 16 é a consolidação canônica de vocabulário do galho;
   ela é **exceção declarada**, não gap.
4. **E8 (Armadilhas)** — os `[!warning]` já existem espalhados no corpo (1–5 por nota). A ação
   correta é **mover**, não duplicar. A nota 16 já tem `## 7. Armadilhas consolidadas`:
   exceção declarada.
5. **`## Em entrevista`** conta como seção-lente local do galho (presente em 15/16).

### Diretriz de fronteira (decidida no galho, executada por nota)

O galho é o **hub stack-agnóstico** de um cluster grande, mas o outbound é cego: cita só
`[[Testes em Java]]` (20×) e `[[Testes em JavaScript]]` (8×). Zero menções a Testes JS (18
notas), Python/Testes (9), Go/15, Arqueologia, Operação e Acessibilidade — todas nascidas
depois de 2026-06-18. O inbound, esse, é forte. A lente Conexões **executa o alvo abaixo**;
não sai descobrindo vizinho (modo de falha do galho de Go).

> [!danger] Paths verificados — copiar LITERAL, não reconstruir de memória
> Os paths abaixo foram conferidos com `ls` em 2026-08-01. O subagente da nota 06 **já alucinou
> dois deles** (escreveu `Engenharia/Testes JS` — a pasta é `Tecnologia/Testes JS` — e
> `11 - Testes de caracterização`, que não existe; o arquivo é `11 - Approval e Golden Master
> testing`). **Copie o path exato desta tabela.** Se um alvo não estiver aqui, confira com `ls`
> antes de escrever o wikilink. Nunca reconstrua nome de arquivo por memória.

| Nota | Alvo de despacho — path exato |
|------|-------------------------------|
| 01 | `03-Dominios/Engenharia/Arqueologia e Restauração de Software/01 - O que é código legado` · `.../10 - A rede de segurança primeiro` |
| 02 | `03-Dominios/Tecnologia/Testes JS/01 - O cenário de testes JS` · `03-Dominios/Engenharia/Operação/index` |
| 04 | `03-Dominios/Tecnologia/Python/Testes/01 - pytest fundamentos — anatomia, discovery e assert introspection` · `03-Dominios/Tecnologia/Go/15 - Testes/02 - Table-driven tests` · `03-Dominios/Tecnologia/Testes JS/04 - Organização e ciclo de vida` |
| 05 | `03-Dominios/Tecnologia/Testes JS/06 - Mocking com Vitest` · `03-Dominios/Tecnologia/Python/Testes/04 - Mocking com unittest.mock e pytest-mock` · `03-Dominios/Tecnologia/Testes JS/09 - MSW - mockando a rede` · `03-Dominios/Tecnologia/Go/15 - Testes/04 - Test doubles — interfaces e mocks` |
| 06 | `03-Dominios/Tecnologia/Testes JS/07 - Testing Library - filosofia e queries` · `03-Dominios/Engenharia/Arqueologia e Restauração de Software/11 - Approval e Golden Master testing` |
| 07 | `03-Dominios/Tecnologia/Python/Testes/05 - Testando a API REST — TestClient e dependency overrides` · `03-Dominios/Tecnologia/Python/Testes/06 - Testando a camada de persistência — banco de teste e rollback` · `03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes` · `03-Dominios/Tecnologia/Go/15 - Testes/05 - Testes de integração` |
| 08 | `03-Dominios/Tecnologia/Python/Testes/08 - TDD na prática com pytest` |
| 09 | `03-Dominios/Tecnologia/Python/Testes/08 - TDD na prática com pytest` · `03-Dominios/Engenharia/Arqueologia e Restauração de Software/14 - Refactoring em terreno hostil` |
| 10 | `03-Dominios/Ciência/Matemática para Computação/05 - Técnicas de prova` · `03-Dominios/Tecnologia/Go/15 - Testes/07 - Fuzzing` |
| 11 | `03-Dominios/Tecnologia/Testes JS/16 - Testes flaky em JS` |
| 12 | `03-Dominios/Tecnologia/Testes JS/12 - Cobertura no ecossistema JS` · `03-Dominios/Tecnologia/Python/Testes/07 - Coverage — pytest-cov e o que ele não mede` · `03-Dominios/Tecnologia/Java/Testes/17 - Mutation testing — PIT e cobertura honesta` |
| 13 | `03-Dominios/Tecnologia/Testes JS/11 - Snapshot testing` · `03-Dominios/Tecnologia/Acessibilidade/Auditar e Testar/14 - Testes de a11y no código` · `03-Dominios/Engenharia/Arqueologia e Restauração de Software/11 - Approval e Golden Master testing` · `03-Dominios/Tecnologia/Java/Testes/20 - Contract testing — Pact` |
| 14 | `03-Dominios/Engenharia/Operação/index` · `03-Dominios/Tecnologia/Web Performance/index` · `03-Dominios/Tecnologia/Java/Testes/18 - Performance — JMH e microbenchmarks` |
| 15 | `03-Dominios/Tecnologia/Testes JS/17 - Testes na CI` · `03-Dominios/Tecnologia/Python/Testes/09 - Capstone — a suíte de testes da API de Tarefas` · `03-Dominios/Engenharia/Operação/index` |
| 16 | tabela consolidada conceito → ferramenta, por stack (Java · JS/TS · Python · Go) |

Fora da tabela, o `index.md` recebe a seção "Fronteiras" reescrita (hoje lista só Java e JS).

### Trava de mídia (M1)

ID de YouTube só entra na nota se o `uvx yt-dlp` **baixou legenda de fato**. Download que
falha vira buraco declarado — nunca vídeo "provável".

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 16 |
| ⬜ pendente | 10 |
| ➖ não precisa | 0 |
| ✅ feita | 6 |
| % concluído | 38% |
| Classe `[substantivo]` | 16 |
| Classe `[mecânico]` | 0 — reclassificada após o piso voltar a valer |
| Score médio | ~5,7 |

> Tabela preenchida ao final do diagnóstico (Fase 3).

---

## Notas

#### 01 - O que são testes e por que testar   [substantivo]
- **Enriquecimento:** ✅ feita (2026-08-01)
- **Estado:** 301 linhas reais · fase: iniciado · status: evergreen
- **Núcleo/gaps:** E2 (abre pela definição — "Comece pela definição mais crua possível. Um teste automatizado é código" — não por problema/cenário) · E4 (sem `## Casos práticos`; não há caso real evidente na nota) · E5 (sem `## O que vem a seguir`; existe `## Veja também`, que é lista, não ponte narrativa) · E8 (3 `[!warning]` espalhados no corpo, sem seção `## Armadilhas comuns`) · L2 (callout `[!info] Lastro` cita livros/paper em prosa, sem URL clicável; não há seção `## Fontes`) · M1 (5 callouts `[!tip]` presentes, nenhum com link de vídeo/podcast)
- **Score:** 7/12
- **Plano de execução:**
  - Reabrir o corpo com um cenário/problema concreto (ex.: o teste manual que não escala) antes de qualquer definição → ativa E2
  - Mover os 3 `[!warning]` existentes (Dijkstra/prova vs. amostragem; confiança frágil; falácia "não temos tempo") para nova seção `## Armadilhas comuns`, sem duplicar → ativa E8
  - Adicionar `## O que vem a seguir` com ponte narrativa, despachando para `[[03-Dominios/Engenharia/Arqueologia e Restauração de Software/01 - O que é código legado]]` e `[[03-Dominios/Engenharia/Arqueologia e Restauração de Software/10 - A rede de segurança primeiro]]` (alvos confirmados existentes) conforme diretriz de fronteira do galho → ativa E5 e quita o despacho pendente
  - Avaliar se há caso real do usuário aplicável a esta nota introdutória para `## Casos práticos`; se não houver, manter o gap declarado — não fabricar → ativa E4 (condicional)
  - Pesquisar e citar ≥1 URL externa verificável (ex.: o relatório NATO 1969 de Dijkstra, ou o paper/relatório do IBM Systems Sciences Institute) em nova seção `## Fontes`, substituindo/complementando o callout `Lastro` em prosa → ativa L2
  - Pesquisar vídeo/podcast relevante (ex.: motivação para testar, TDD de Kent Beck) e embutir como `[!tip]` só se `uvx yt-dlp` baixar legenda de fato (trava de mídia) → ativa M1
- **Resultado:** 319 linhas (era 301). E2 reaberto pelo cenário do teste manual que não escala · E8 os 3 `[!warning]` movidos para `## Armadilhas comuns` · E5 ponte para Arqueologia/01 e /10 (despacho de fronteira quitado) · L2 `## Fontes` com o relatório NATO 1969 verificado (PDF baixado, citação de Dijkstra conferida) e ressalva de proveniência sobre o número do IBM Systems Sciences Institute · M1 Kent Beck no The Engineering Room (`guycIP56YeY`, legenda baixada e ID reconferido). **E4 = buraco declarado:** nenhum caso real do usuário cabe nesta nota introdutória.

#### 02 - A pirâmide de testes e suas variações   [substantivo]
- **Enriquecimento:** ✅ feita (2026-08-01)
- **Estado:** 245 linhas reais · fase: iniciado · status: evergreen
- **Núcleo/gaps:** E1 (TL;DR tem só 1 linha, não ≥3) · E4 (sem `## Casos práticos`) · E5 (sem `## O que vem a seguir`, só `## Veja também`) · E7 (Vocabulário é lista, não tabela) · E8 (só 1 `[!warning]` no corpo, abaixo do piso de 3, sem seção dedicada) · L2 (fontes em callout `Lastro`, não seção `## Fontes`, URLs sem link clicável) · M1 (nenhum vídeo/podcast embutido)
- **Score:** 5/11 (P1 N/A — nota conceitual sem código)
- **Plano de execução:**
  - Expandir o `[!abstract]` de 1 para ≥3 linhas densas, cobrindo pirâmide, troféu e a pergunta de ouro → ativa E1
  - Avaliar se existe caso real de produção do usuário aplicável (ex.: decisão pirâmide vs troféu em algum projeto real); se não houver, não fabricar e manter o gap registrado → avalia E4
  - Adicionar seção `## O que vem a seguir` com ponte narrativa até os alvos já decididos na Diretriz de fronteira (Testes JS/01 e Operação — "a pirâmide na esteira") → ativa E5
  - Converter a lista `### Vocabulário` numa tabela PT ↔ EN → ativa E7
  - Mover o `[!warning]` existente (linha 154, "A ampulheta tem uma defesa parcial") para uma seção `## Armadilhas comuns`; registrar que só há 1 disponível no corpo, abaixo do piso de 3, sem fabricar novas → ativa E8 parcialmente
  - Reformular o callout `[!info] Lastro` como seção `## Fontes`, com as mesmas URLs em formato de link markdown clicável → ativa L2
  - Pesquisar vídeo/podcast sobre pirâmide de testes ou Testing Trophy com legenda baixável via `yt-dlp` e embutir como `[!tip]` → ativa M1
- **Resultado:** 312 linhas (era 245; piso 300 atingido). E1 TL;DR para 5 linhas · E5 pontes para Testes JS/01 e Operação/index · E7 Vocabulário virou tabela PT↔EN · E8 o `[!warning]` da ampulheta movido + 2 derivadas do conteúdo técnico (dogma numérico; ambiguidade de "teste de integração" entre times), com `[!info]` declarando qual tem lastro original · L2 `## Fontes` com URLs verificadas · M1 Testing Trophy de Kent C. Dodds (`RHKkEiQ58N0`, legenda baixada e ID reconferido). Déficit fechado com conteúdo novo e sourced — taxonomia small/medium/large do Google Testing Blog + exemplo trabalhado —, não padding. **E4 = lacuna consciente** registrada em callout.

#### 03 - Anatomia de um bom teste   [substantivo]
- **Enriquecimento:** ✅ feita (2026-08-01)
- **Estado:** 285 linhas reais · fase: iniciado · status: evergreen
- **Núcleo/gaps:** E1 (TL;DR tem só 1 linha, não ≥3) · E4 (sem "Casos práticos"; nenhum dos 5 casos reais do spec de origem mapeia pra esta nota) · E5 (sem "O que vem a seguir"; "Veja também" é lista pura, não ponte narrativa) · E8 (sem seção "Armadilhas comuns"; só 1 `[!warning]` solto no corpo) · L1 (todos os wikilinks apontam pra dentro da própria pasta Testes; sem alvo cross-galho) · M1 (sem vídeo/podcast embutido)
- **Score:** 7/12
- **Plano de execução:**
  - Expandir o TL;DR `[!abstract]` (linha 18) pra ≥3 linhas densas → ativa E1
  - Avaliar se existe caso real do usuário aplicável a esta nota (nenhum dos 5 casos do spec de origem — MedEspecialista, comissão, tela 30 campos, mock→fake, Awaitility, Testcontainers×H2 — cobre "anatomia de um bom teste"); se não houver, manter como buraco declarado, nunca fabricar → avalia E4
  - Adicionar seção `## O que vem a seguir` com ponte narrativa (a "## Veja também" atual vira ou complementa essa seção) → ativa E5
  - Mover os callouts existentes (`[!warning] Nomes que não dizem nada`, linha 123; `[!danger] O mito da "uma assertion por teste"`, linha 157) para uma seção dedicada `## Armadilhas comuns`; avaliar se cabe um terceiro item real sem fabricar → ativa E8
  - A diretriz de fronteira do galho não lista alvo de despacho pra nota 03 (tabela cobre 01,02,04-07,10-16, não 03); avaliar candidato plausível na Fase de execução ou registrar como buraco declarado — não inventar wikilink → avalia L1
  - Pesquisar vídeo/podcast sobre anatomia de um bom teste (AAA, F.I.R.S.T, nomenclatura) e embutir via `uvx yt-dlp` só se a legenda baixar de fato → ativa M1
- **Resultado:** 311 linhas (era 285; piso 300 atingido). E1 TL;DR para 3 linhas · E5 `## O que vem a seguir` bifurcando para as notas 04 e 06 · E8 os 2 callouts movidos + 1 terceiro derivado da própria seção "Sem lógica no teste" · L1 fechado com Java/Testes/02 e Testes JS/03 (paths verificados) · M1 PyCon UK 2016 sobre AAA (`GGw5T1mw9vU`, legenda baixada e ID reconferido). **E4 = buraco declarado** em callout. **Ressalva:** E8 tem 3 armadilhas mas 2 são `[!warning]` e 1 é `[!danger]` (o original foi movido, não reclassificado). L2 não constava como gap no diagnóstico desta nota — divergência entre auditores, conferir no passe final.

#### 04 - Testes unitários   [substantivo]
- **Enriquecimento:** ✅ feita (2026-08-01)
- **Estado:** 322 linhas · fase: iniciado · status: evergreen
- **Núcleo/gaps:** E1 (TL;DR `[!abstract]` tem só 1 linha de conteúdo, não ≥3) · E4 (sem `## Casos práticos`; nenhum dos 5 casos reais do spec de origem — MedEspecialista, TDD/comissão, tela de 30 campos, mock→fake, Awaitility, Testcontainers×H2 — mapeia claramente pra "testes unitários" em si) · E5 (sem `## O que vem a seguir`; existe `## Veja também`, lista pura, não ponte narrativa) · E7 (`### Vocabulário`, linha 291, é lista, não tabela PT↔EN) · E8 (3 `[!warning]` espalhados no corpo — linhas 81, 158, 240 — sem seção `## Armadilhas comuns`) · L2 (callout `[!info] Lastro`, linha 306, tem URLs clicáveis mas não é seção `## Fontes`) · M1 (2 `[!tip]` presentes — linhas 87 e 280 — nenhum com link de vídeo/podcast)
- **Score:** 5/12
- **Plano de execução:**
  - Expandir o `[!abstract]` (linha 18-19) pra ≥3 linhas densas, cobrindo a definição, a guerra Londres×Detroit e F.I.R.S.T → ativa E1
  - Avaliar se há caso real do usuário aplicável a esta nota (nenhum dos 5 casos do spec de origem cobre diretamente escolas de teste unitário/factories/object mother/determinismo); se não houver, manter o gap declarado — não fabricar → avalia E4
  - Adicionar `## O que vem a seguir` com ponte narrativa, despachando para `[[03-Dominios/Tecnologia/Python/Testes/01 - pytest fundamentos — anatomia, discovery e assert introspection]]`, `[[03-Dominios/Tecnologia/Python/Testes/02 - Fixtures — escopos, yield e conftest.py]]`, `[[03-Dominios/Tecnologia/Python/Testes/03 - Parametrização e organização de suíte]]`, `[[03-Dominios/Tecnologia/Go/15 - Testes]]` e `[[03-Dominios/Tecnologia/Testes JS/02 - Vitest - setup e o primeiro teste]]`–`[[03-Dominios/Tecnologia/Testes JS/04 - Organização e ciclo de vida]]` (alvos confirmados existentes) conforme diretriz de fronteira do galho → ativa E5 e quita o despacho pendente
  - Converter `### Vocabulário` (linha 291-304) numa tabela PT ↔ EN → ativa E7
  - Mover os 3 `[!warning]` existentes (trade-off isolamento×acoplamento linha 81; fixture compartilhada linha 158; lado escuro da object mother linha 240) para nova seção `## Armadilhas comuns`, sem duplicar → ativa E8
  - Reformular o callout `[!info] Lastro` (linha 306-309) como seção `## Fontes`, preservando as mesmas URLs em formato de link markdown clicável → ativa L2
  - Pesquisar vídeo/podcast sobre escola de Londres × Detroit (mockist vs classicist testing) ou object mother e embutir como `[!tip]` só se `uvx yt-dlp` baixar legenda de fato (trava de mídia) → ativa M1
- **Resultado:** 342 linhas (era 322; piso 300 já atendido). E1 TL;DR para 3 linhas (definição + Londres×Detroit + F.I.R.S.T) · E5 ponte para Python/Testes 01-03, Go/15/index e Testes JS 02/04 — despacho de fronteira quitado, com `/index` correto no alvo de pasta · E7 Vocabulário virou tabela PT↔EN · E8 os 3 `[!warning]` movidos, com referência cruzada nos pontos originais · L2 `## Fontes` com 3 URLs clicáveis · M1 Codemanship, "London School AND Classic TDD" (`uVHGt2qbjXI`, legenda baixada e ID reconferido). **E4 = buraco declarado:** nenhum caso real cobre escolas/factories/object mother.

#### 05 - Test doubles - dummy, stub, spy, mock, fake   [substantivo]
- **Enriquecimento:** ✅ feita (2026-08-01)
- **Estado:** 298 linhas reais · fase: adepto · status: evergreen
- **Núcleo/gaps:** E1 (TL;DR tem só 1 linha densa, não ≥3) · E4 (sem `## Casos práticos`; nenhum dos 5 casos reais do spec de origem está mapeado explicitamente pra esta nota — avaliar se "mock→fake" se aplica) · E5 (sem `## O que vem a seguir`; existe `## Veja também`, que é lista, não ponte narrativa) · E8 (só 2 callouts disponíveis — `[!warning]` linha 62 e `[!danger]` linha 214 —, abaixo do piso de 3, sem seção `## Armadilhas comuns` dedicada) · P1 (todos os exemplos de código são caminho feliz; o sintoma de overmocking é descrito só em prosa no `[!danger]`, sem exemplo de código-problema) · L2 (callout `[!info] Lastro`, linha 285, tem URLs clicáveis mas não está em seção `## Fontes`) · M1 (callout `[!tip]` na linha 205 é dica textual, sem link de vídeo/podcast)
- **Score:** 6/12
- **Plano de execução:**
  - Expandir o `[!abstract]` (linhas 18-19) de 1 para ≥3 linhas densas, cobrindo a analogia do dublê, a divisão alimenta/verifica e a distinção mock×stub → ativa E1
  - Avaliar se o caso real "mock→fake" (mapeado no spec de origem do galho) se aplica a esta nota para `## Casos práticos`; se sim, adicionar sem fabricar; se não, manter o gap declarado → avalia E4
  - Adicionar `## O que vem a seguir` com ponte narrativa despachando para `[[Testes JS/06 - ...|Testes JS/06]]` (Vitest), `[[Python/Testes/04 - ...|Python/Testes/04]]` (`unittest.mock`) e `[[Testes JS/09 - ...|Testes JS/09]]` (MSW), conforme diretriz de fronteira do galho (verificar títulos exatos antes de linkar) → ativa E5 e quita o despacho pendente
  - Mover os 2 `[!warning]`/`[!danger]` existentes (linha 62 "Cuidado com o vocabulário do dia a dia"; linha 214 "Sintoma de overmocking") para nova seção `## Armadilhas comuns`, sem duplicar; registrar que só há 2 disponíveis, abaixo do piso de 3, sem fabricar novo → ativa E8 parcialmente
  - Acrescentar um trecho de código-problema (ex.: teste com `when(...)`/`verify(...)` em excesso e nenhuma asserção real sobre resultado) ilustrando o sintoma de overmocking já descrito em prosa → ativa P1
  - Reformular o callout `[!info] Lastro` (linhas 285-288) como seção `## Fontes`, mantendo as mesmas URLs em formato de link markdown clicável → ativa L2
  - Pesquisar vídeo/podcast sobre test doubles / mocks vs. stubs e embutir como `[!tip]` só se `uvx yt-dlp` baixar legenda de fato (trava de mídia) → ativa M1
- **Resultado:** 402 linhas (era 298; **piso 400 atingido**). E1 TL;DR para 3 linhas · E5 ponte para Testes JS/06, Python/Testes/04, Testes JS/09 e Go/15/04 · E8 os 2 callouts movidos + 1 derivada do texto (ambiguidade do `mock()` que cria os dois tipos) · P1 código-problema de overmocking (`when`/`verify` sem asserção real) vs. versão corrigida · L2 `## Fontes` + Freeman & Pryce citado como origem do TDD mockista · M1 Keploy, "Stubs vs Mocks vs Fake" (`4AxXWjBSIdY`, legenda `en-orig` baixada e ID reconferido). Déficit fechado com conteúdo novo e sourced: seção das duas escolas (Fowler / Freeman-Pryce) + exemplo trabalhado com três dublês juntos. **E4:** o caso mock→fake foi deixado para a nota 06 (casa correta), com gap declarado aqui em vez de duplicar.

#### 06 - Testar comportamento, não implementação   [substantivo]
- **Enriquecimento:** ✅ feita (2026-08-01)
- **Estado:** 270 linhas reais · fase: adepto · status: evergreen
- **Núcleo/gaps:** E1 (TL;DR tem só 1 linha, não ≥3) · E4 (sem `## Casos práticos`; existe 1 caso real — migração `@Mock UserRepository` → `InMemoryUserRepository` com `HashMap` — mas só como callout `[!example]`, não em seção dedicada, e é só 1 cenário, não ≥2) · E5 (sem `## O que vem a seguir`; existe `## Veja também`, lista pura sem ponte narrativa) · E7 (`### Vocabulário` é lista com `→`, não tabela PT↔EN) · E8 (sem seção `## Armadilhas comuns`; os `[!warning]` (over-mocking) e `[!danger]` (under-mocking) estão espalhados no corpo) · L2 (callout `[!info] Lastro` tem 3 URLs já clicáveis, mas não é uma seção `## Fontes`)
- **Score:** 6/12
- **Plano de execução:**
  - Expandir o `[!abstract]` de 1 para ≥3 linhas densas, cobrindo a regra de ouro, state-based×interaction-based e fake>mock → ativa E1
  - Formalizar em `## Casos práticos` o caso real já presente (callout `[!example]` "Da prancheta ao prato", migração `@Mock UserRepository` → `InMemoryUserRepository`); não fabricar segundo cenário — se só houver 1, registrar gap parcial → avalia E4
  - Adicionar `## O que vem a seguir` com ponte narrativa despachando para `[[03-Dominios/Tecnologia/Testes JS/07 - Testing Library - filosofia e queries]]` e `[[03-Dominios/Engenharia/Arqueologia e Restauração de Software/11 - Approval e Golden Master testing]]` (**paths verificados em 2026-08-01**; os dois alvos que o diagnóstico havia escrito estavam errados — `Testes JS` fica em `Tecnologia`, não `Engenharia`, e a nota 11 de Arqueologia chama-se `Approval e Golden Master testing`), conforme diretriz de fronteira do galho para a nota 06 → ativa E5
  - Converter `### Vocabulário` de lista para tabela PT ↔ EN → ativa E7
  - Mover (não duplicar) os callouts `[!warning]` (Sinais de over-mocking, linha 111) e `[!danger]` (O perigo do under-mocking, linha 139) para nova seção `## Armadilhas comuns`; registrar que restam só 2 blocos, abaixo do piso de 3 individuais, sem fabricar novo → ativa E8 parcialmente
  - Reformular o callout `[!info] Lastro` (linha 267) como seção `## Fontes`, preservando os 3 links clicáveis já existentes (Fowler, Dodds, Khorikov) → ativa L2
  - Pesquisar vídeo/podcast sobre testar comportamento vs. implementação (ou mocks vs. fakes) com legenda baixável via `uvx yt-dlp` e embutir como `[!tip]` só se a legenda baixar de fato (trava de mídia) → ativa M1
- **Resultado:** 397 linhas (era 270). **Piso 400 NÃO atingido — faltam 3 linhas, déficit declarado em vez de preenchido com enchimento** (comportamento correto sob a regra anti-padding). E1 TL;DR para 3 linhas · E4 `## Casos práticos` formaliza o caso real `@Mock`→`InMemoryUserRepository`; segundo cenário não fabricado, gap consciente em callout · E5 ponte para Testes JS/07 e Arqueologia/11 (os dois paths que o diagnóstico errara, agora corretos) · E7 tabela PT↔EN com 16 termos · E8 os 2 callouts movidos + 1 derivada ("mockar por preguiça") · L2 `## Fontes` com Fowler/Dodds/Khorikov · M1 PyCon Greece, Kalaitzis (`QQUwZQvuFCQ`, legenda baixada e ID reconferido). Conteúdo novo: os quatro pilares de Khorikov, diagrama de decisão fake×mock×stub e exemplos Java genéricos.

#### 07 - Testes de integração   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 240 linhas reais · fase: adepto · status: evergreen
- **Núcleo/gaps:** E1 (TL;DR `[!abstract]`, linha 18-19, tem só 1 linha densa, não ≥3) · E4 (sem `## Casos práticos`; o caso real do spec de origem — Testcontainers vs H2 — está presente só como callout `[!example]` "Como isso mudou meu fluxo", linha 147-148, 1 único cenário, não em seção dedicada) · E5 (sem `## O que vem a seguir`; existe `## Veja também`, linha 232, lista pura, não ponte narrativa) · E8 (só 2 callouts disponíveis — `[!danger]` linha 105 "Por que o drift te trai exatamente quando dói" e `[!warning]` linha 186 "Rede externa = flaky garantido" —, abaixo do piso de 3, sem seção `## Armadilhas comuns` dedicada) · L2 (callout `[!info] Lastro`, linha 227-230, já tem 3 URLs clicáveis, mas não está em seção `## Fontes` — gap de formato) · M1 (2 `[!tip]` presentes — linha 64 e linha 180 — nenhum com link de vídeo/podcast)
- **Score:** 6/11 (P1 N/A — nota conceitual, sem bloco de código, só diagramas)
- **Plano de execução:**
  - Expandir o `[!abstract]` (linha 18-19) de 1 para ≥3 linhas densas, cobrindo a definição de fiação/cola, o drift de ambiente e o espectro narrow×broad → ativa E1
  - Formalizar em `## Casos práticos` o caso real já presente (callout `[!example]` "Como isso mudou meu fluxo", Testcontainers substituindo o Postgres local "de teste" que drift-ava de produção); não fabricar segundo cenário — registrar que só há 1 disponível, abaixo do mínimo de 2 → avalia E4 parcialmente
  - Adicionar `## O que vem a seguir` com ponte narrativa despachando para `[[03-Dominios/Tecnologia/Python/Testes/05 - Testando a API REST — TestClient e dependency overrides]]`, `[[03-Dominios/Tecnologia/Python/Testes/06 - Testando a camada de persistência — banco de teste e rollback]]`, `[[03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes]]` e `[[03-Dominios/Tecnologia/Go/15 - Testes/05 - Testes de integração]]` (paths da Diretriz de fronteira; conferir existência com `ls` antes de escrever o wikilink) → ativa E5 e quita o despacho pendente
  - Mover (não duplicar) os callouts `[!danger]` (linha 105) e `[!warning]` (linha 186) para nova seção `## Armadilhas comuns`; registrar que restam só 2 blocos, abaixo do piso de 3 individuais, sem fabricar novo → ativa E8 parcialmente
  - Reformular o callout `[!info] Lastro` (linhas 227-230) como seção `## Fontes`, preservando os 3 links clicáveis já existentes (Fowler, Testcontainers, Hauer) → ativa L2
  - Pesquisar vídeo/podcast sobre Testcontainers ou environment drift em testes de integração e embutir como `[!tip]` só se `uvx yt-dlp` baixar legenda de fato (trava de mídia) → ativa M1
- **Resultado:** —

#### 08 - TDD - o ciclo Red-Green-Refactor   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 310 linhas reais · fase: adepto · status: evergreen
- **Núcleo/gaps:** E1 (TL;DR `[!abstract]`, linha 19, tem só 1 linha densa, não ≥3) · E4 (sem `## Casos práticos`; os 5 casos reais do usuário mapeados no spec de origem pertencem à nota 09, não a esta — nenhum caso real aplicável aqui) · E5 (sem `## O que vem a seguir`; existe `## Veja também`, linha 303, lista pura de wikilinks, não ponte narrativa) · E8 (só 2 `[!warning]` no corpo — linha 37 "Um teste que nunca falhou é suspeito" e linha 220 "Erros comuns no ciclo", este último agrupando 4 armadilhas num único callout em vez de individuais —, abaixo do piso de 3 individuais, sem seção `## Armadilhas comuns` dedicada) · L2 (callout `[!info] Lastro`, linha 296, tem 5 URLs já clicáveis, mas não está em seção `## Fontes`) · M1 (4 `[!tip]` presentes — linhas 46, 162, 171, 214 — nenhum com link de vídeo/podcast)
- **Score:** 7/12
- **Plano de execução:**
  - Expandir o `[!abstract]` (linha 18-19) de 1 para ≥3 linhas densas, cobrindo o ciclo Red-Green-Refactor, as três estratégias de Green (Obvious/Fake It/Triangulação) e o teste como primeiro cliente da API → ativa E1
  - Não fabricar caso real: os 5 casos do spec de origem (MedEspecialista, TDD/comissão, tela de 30 campos, mock→fake, Awaitility, Testcontainers×H2) estão mapeados para a nota 09, não para esta; manter o gap declarado para `## Casos práticos` → avalia E4 (sem ação de conteúdo)
  - Adicionar `## O que vem a seguir` com ponte narrativa a partir do `## Veja também` atual (linha 303), despachando para `[[09 - TDD na prática]]` (já linkada no corpo) e para `[[03-Dominios/Tecnologia/Python/Testes/08 - TDD na prática com pytest]]` (path verificado com `ls` em 2026-08-01, conforme diretriz de fronteira do galho) → ativa E5 e quita o despacho pendente
  - Mover os 2 blocos existentes (`[!warning]` linha 37; `[!warning] Erros comuns no ciclo` linha 220, desmembrando seus 4 sub-itens em `[!warning]` individuais) para nova seção `## Armadilhas comuns`, sem duplicar; registrar que restam só 2 blocos-fonte (viram até 5 individuais ao desmembrar o agrupado), sem fabricar armadilha nova → ativa E8
  - Reformular o callout `[!info] Lastro` (linhas 296-301) como seção `## Fontes`, preservando as mesmas 5 URLs em formato de link markdown clicável → ativa L2
  - Pesquisar vídeo/podcast sobre TDD / Red-Green-Refactor (ex.: Kent Beck falando sobre TDD, ou TCR) com legenda baixável via `uvx yt-dlp` e embutir como `[!tip]` só se a legenda baixar de fato (trava de mídia) → ativa M1
- **Resultado:** —

#### 09 - TDD na prática   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 330 linhas reais · fase: adepto · status: evergreen
- **Núcleo/gaps:** E1 (TL;DR `[!abstract]`, linha 18-19, tem só 1 linha densa, não ≥3) · E4 (os dois casos reais exigidos — comissão com 5 condições, linha 44-47, e tela de 30 campos, linha 144-145 — estão presentes como `[!example]` embutidos nas seções, não em `## Casos práticos` dedicada) · E5 (sem `## O que vem a seguir`; existe `## Veja também`, linha 322, lista pura sem ponte narrativa) · E7 (`### Vocabulário PT → EN`, linha 290, é lista com `→`, não tabela) · E8 (3 `[!warning]` espalhados no corpo — linhas 175, 196, 245 — sem seção `## Armadilhas comuns` dedicada) · L1 (todos os wikilinks, linhas 21,69,141,142,176,184,324-329, apontam pra dentro da própria pasta Testes; sem alvo cross-galho) · L2 (callout `[!info] Lastro`, linhas 313-320, tem 7 URLs já clicáveis, mas não é seção `## Fontes`) · M1 (2 `[!tip]` presentes — linhas 64 e 280 — nenhum com link de vídeo/podcast)
- **Score:** 5/12
- **Plano de execução:**
  - Expandir o `[!abstract]` (linhas 18-19) de 1 para ≥3 linhas densas, cobrindo a analogia do GPS, a heurística design-incerto/lógica-complexa e o debate contexto-vs-dogma → ativa E1
  - Formalizar em `## Casos práticos` os dois casos reais já presentes e verificados — comissão com 5 condições (TDD salvou, linha 44-47) e tela de cadastro com 30 campos (test-after venceu, linha 144-145) — sem alterar os fatos nem fabricar terceiro cenário → ativa E4
  - Adicionar `## O que vem a seguir` com ponte narrativa despachando para `[[03-Dominios/Tecnologia/Python/Testes/08 - TDD na prática com pytest]]` e `[[03-Dominios/Engenharia/Arqueologia e Restauração de Software/14 - Refactoring em terreno hostil]]` (**paths verificados via `ls` em 2026-08-01**), conforme diretriz de fronteira do galho para a nota 09 → ativa E5, L1 e quita o despacho pendente
  - Converter `### Vocabulário PT → EN` (linha 290-311) de lista para tabela PT ↔ EN → ativa E7
  - Mover (não duplicar) os 3 `[!warning]` existentes (TDD não garante bom design, linha 175; honestidade sobre a evidência, linha 196; loop externo não substitui o interno, linha 245) para nova seção `## Armadilhas comuns` → ativa E8
  - Reformular o callout `[!info] Lastro` (linhas 313-320) como seção `## Fontes`, preservando as 7 URLs já clicáveis (DHH, Fowler, Quality Coding, Feathers, Nagappan et al., Turhan/Munir, Freeman & Pryce) → ativa L2
  - Pesquisar vídeo/podcast sobre TDD na prática (ex.: Kent Beck sobre quando não fazer TDD, ou a série "Is TDD Dead?") e embutir como `[!tip]` só se `uvx yt-dlp` baixar legenda de fato (trava de mídia) → ativa M1
- **Resultado:** —

#### 10 - Técnicas de teste e edge cases   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 257 linhas reais · fase: adepto · status: evergreen
- **Núcleo/gaps:** E1 (TL;DR `[!abstract]`, linha 18-19, tem só 1 linha densa, não ≥3) · E4 (sem `## Casos práticos`; nenhum dos 5 casos reais do spec de origem — MedEspecialista, TDD/comissão, tela de 30 campos, mock→fake, Awaitility, Testcontainers×H2 — mapeia claramente pra técnicas de particionamento/BVA/tabelas de decisão/edge cases) · E5 (sem `## O que vem a seguir`; existe `## Veja também`, linha 249, lista pura de wikilinks, não ponte narrativa) · E7 (`### Vocabulário`, linha 224, é lista com `→`, não tabela PT↔EN) · E8 (3 `[!warning]` espalhados no corpo — linha 83 "A armadilha da partição de equivalência", linha 163 "O erro clássico", linha 214 "O esquecido que pega em produção" — sem seção `## Armadilhas comuns` dedicada) · L1 (todos os wikilinks — linhas 33, 124, 218, 251-257 — apontam pra dentro da própria pasta Testes; sem alvo cross-galho) · L2 (callout `[!info] Lastro`, linhas 244-247, tem 3 URLs já clicáveis, mas não é seção `## Fontes` — gap de formato) · M1 (4 `[!tip]` presentes — linhas 25, 114, 187, 217 (nota: 3 tips totais além do de mentalidade) — nenhum com link de vídeo/podcast)
- **Score:** 4/11 (P1 N/A — nota conceitual, sem bloco de código; diagramas Mermaid e tabelas ilustram as técnicas)
- **Plano de execução:**
  - Expandir o `[!abstract]` (linhas 18-19) de 1 para ≥3 linhas densas, cobrindo equivalence partitioning, boundary value analysis, decision tables/state-transition e o checklist de edge cases → ativa E1
  - Avaliar se há caso real do usuário aplicável a esta nota (nenhum dos 5 casos do spec de origem cobre diretamente particionamento/BVA/edge cases); se não houver, manter o gap declarado — não fabricar → avalia E4
  - Adicionar `## O que vem a seguir` com ponte narrativa, despachando para `[[03-Dominios/Ciência/Matemática para Computação/05 - Técnicas de prova]]` e `[[03-Dominios/Tecnologia/Go/15 - Testes/07 - Fuzzing]]` (paths literais da Diretriz de fronteira, linha 81 do roadmap; conferir existência com `ls` antes de escrever o wikilink) → ativa E5 e L1, e quita o despacho pendente
  - Converter `### Vocabulário` (linha 224-242) de lista com `→` para tabela PT ↔ EN → ativa E7
  - Mover (não duplicar) os 3 `[!warning]` existentes (linha 83 "A armadilha da partição de equivalência"; linha 163 "O erro clássico"; linha 214 "O esquecido que pega em produção") para nova seção `## Armadilhas comuns` → ativa E8
  - Reformular o callout `[!info] Lastro` (linhas 244-247) como seção `## Fontes`, preservando as 3 URLs já clicáveis (ISTQB syllabus, Myers, ISTQB BVA white paper) → ativa L2
  - Pesquisar vídeo/podcast sobre equivalence partitioning / boundary value analysis / edge case testing e embutir como `[!tip]` só se `uvx yt-dlp` baixar legenda de fato (trava de mídia) → ativa M1
- **Resultado:** —

#### 11 - Testes flaky   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 239 linhas reais · fase: adepto · status: evergreen
- **Núcleo/gaps:** E1 (TL;DR `[!abstract]`, linha 18-19, tem só 1 linha densa, não ≥3) · E4 (o caso real do spec de origem — os 3 flaky por race condition, `Thread.sleep(500)` mascarando até o CI lento falhar, solução `Awaitility.await().atMost(...)` — está presente como callout `[!example]` "Os três flaky por race condition (caso real)", linha 108-109, não em seção dedicada `## Casos práticos`; é só 1 cenário, não fabricar segundo) · E5 (sem `## O que vem a seguir`; existe `## Veja também`, linha 231, lista pura, não ponte narrativa) · E8 (3 callouts disponíveis — `[!danger]` linha 58 "O envenenamento é coletivo", `[!danger]` linha 103 "Nunca `Thread.sleep` num teste. Nunca.", `[!warning]` linha 198 "O custo cultural é o custo real" — espalhados no corpo, sem seção `## Armadilhas comuns` dedicada) · L2 (callout `[!info] Lastro`, linhas 226-229, tem 3 URLs em texto puro, não formatadas como link markdown clicável, e não está em seção `## Fontes` — gap de formato) · M1 (1 `[!tip]` presente, linha 145, sem link de vídeo/podcast)
- **Score:** 6/12
- **Plano de execução:**
  - Expandir o `[!abstract]` (linhas 18-19) de 1 para ≥3 linhas densas, cobrindo a definição de flaky, o mecanismo de erosão de confiança e a regra "nunca sleep em teste" → ativa E1
  - Formalizar em `## Casos práticos` o caso real já presente (callout `[!example]` "Os três flaky por race condition", linha 108-109: 3 testes flaky por race em código assíncrono, `Thread.sleep(500)` mascarando o problema até o CI lento falhar, solução `Awaitility.await().atMost(5, SECONDS).until(...)`, regra "nunca sleep em teste"); preservar os fatos exatamente como estão, não fabricar segundo cenário — registrar que só há 1 disponível, abaixo do mínimo de 2 → ativa E4 parcialmente
  - Adicionar `## O que vem a seguir` com ponte narrativa despachando para `[[03-Dominios/Tecnologia/Testes JS/16 - Testes flaky em JS]]` (path da Diretriz de fronteira, conferir existência com `ls` antes de escrever o wikilink) → ativa E5 e quita o despacho pendente
  - Mover (não duplicar) os 3 callouts existentes (`[!danger]` linha 58; `[!danger]` linha 103; `[!warning]` linha 198) para nova seção `## Armadilhas comuns`, individualizados → ativa E8
  - Reformular o callout `[!info] Lastro` (linhas 226-229) como seção `## Fontes`, convertendo as 3 URLs (Fowler, Google Testing Blog, Awaitility) em links markdown clicáveis → ativa L2
  - Pesquisar vídeo/podcast sobre testes flaky, race conditions em testes assíncronos ou Awaitility e embutir como `[!tip]` só se `uvx yt-dlp` baixar legenda de fato (trava de mídia) → ativa M1
- **Resultado:** —

#### 12 - Coverage e mutation testing   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 260 linhas reais · fase: magus · status: evergreen
- **Núcleo/gaps:** E1 (TL;DR `[!abstract]`, linha 18-19, tem só 1 linha densa, não ≥3) · E4 (sem `## Casos práticos`; nenhum dos 5 casos reais do spec de origem — MedEspecialista, TDD/comissão, tela de 30 campos, mock→fake, Awaitility, Testcontainers×H2 — mapeia claramente pra coverage/mutation testing) · E5 (sem `## O que vem a seguir`; existe `## Veja também`, linha 252, lista pura, não ponte narrativa) · E7 (`### Vocabulário PT → EN`, linha 228, é lista com `→`, não tabela) · E8 (3 callouts disponíveis — `[!warning]` linha 94 "Coverage não vê asserções", `[!danger]` linha 141 "A meta de 100% é desperdício", `[!warning]` linha 199 "Mutation testing é caro" — atingem o piso de 3, mas sem seção `## Armadilhas comuns` dedicada) · L2 (callout `[!info] Lastro`, linhas 247-250, já tem URLs clicáveis, mas não está em seção `## Fontes` — gap de formato) · M1 (só o `[!tip]` da linha 74 "Configure a ferramenta para branch", sem link de vídeo/podcast)
- **Score:** 6/12
- **Plano de execução:**
  - Expandir o `[!abstract]` (linha 18-19) de 1 para ≥3 linhas densas, cobrindo a distinção coverage×mutation, os tipos de coverage e o mutation score → ativa E1
  - Avaliar se há caso real do usuário aplicável a esta nota (nenhum dos 5 casos do spec de origem cobre coverage/mutation testing diretamente); se não houver, manter o gap declarado — não fabricar → avalia E4
  - Adicionar `## O que vem a seguir` com ponte narrativa despachando para `[[03-Dominios/Tecnologia/Testes JS/12 - Cobertura no ecossistema JS]]`, `[[03-Dominios/Tecnologia/Python/Testes/07 - Coverage — pytest-cov e o que ele não mede]]` e `[[03-Dominios/Tecnologia/Java/Testes/17 - Mutation testing — PIT e cobertura honesta]]` (paths da Diretriz de fronteira; confirmar existência com `ls` antes de escrever o wikilink) → ativa E5 e quita o despacho pendente
  - Converter `### Vocabulário PT → EN` (linhas 228-246) de lista com `→` para tabela PT ↔ EN → ativa E7
  - Mover (não duplicar) os 3 callouts existentes (`[!warning]` linha 94 "Coverage não vê asserções"; `[!danger]` linha 141 "A meta de 100% é desperdício"; `[!warning]` linha 199 "Mutation testing é caro") para nova seção `## Armadilhas comuns` → ativa E8
  - Reformular o callout `[!info] Lastro` (linhas 247-250) como seção `## Fontes`, preservando os links clicáveis já existentes (Fowler, PITest/Baeldung, JAVAPRO) → ativa L2
  - Pesquisar vídeo/podcast sobre coverage vs. mutation testing (ex.: overview do PITest, ou talk sobre Goodhart's Law aplicada a métricas de teste) e embutir como `[!tip]` só se `uvx yt-dlp` baixar legenda de fato (trava de mídia) → ativa M1
- **Resultado:** —

#### 13 - Além do básico - property-based, snapshot, contract, smoke   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 322 linhas reais · fase: magus · status: evergreen
- **Núcleo/gaps:** E1 (TL;DR `[!abstract]`, linha 19, tem só 1 linha densa, não ≥3) · E4 (sem `## Casos práticos`; nenhum dos 5 casos reais do spec de origem — MedEspecialista, TDD/comissão, tela de 30 campos, mock→fake, Awaitility, Testcontainers×H2 — mapeia pra property-based/snapshot/contract/smoke) · E5 (sem `## O que vem a seguir`; existem só pontes inline soltas e uma `## Veja também` em lista) · E7 (`### Vocabulário`, linha 291-302, é lista com `—`, não tabela PT↔EN) · E8 (só 1 callout de armadilha no corpo — `[!danger] Snapshot fatigue`, linha 146-147 —, a mais pobre do galho; sem seção `## Armadilhas comuns` dedicada) · P1 (todos os exemplos de código — round-trip, snapshot, smoke — são caminho feliz; nenhum demonstra o caso-problema em código, só em prosa) · L2 (callout `[!info] Lastro`, linhas 304-309, tem 5 URLs já clicáveis, mas não está em seção `## Fontes` — gap de formato) · M1 (4 `[!tip]` presentes — linhas 33, 129, 169, 225, todos "Analogia" — nenhum com link de vídeo/podcast)
- **Score:** 5/12
- **Plano de execução:**
  - Expandir o `[!abstract]` (linha 18-19) de 1 para ≥3 linhas densas, cobrindo separadamente property-based (caça contraexemplo), snapshot (congela output), contract (acordo sem subir junto) e smoke (pulso pós-deploy) → ativa E1
  - Avaliar se há caso real do usuário aplicável (nenhum dos 5 casos do spec de origem cobre property-based/snapshot/contract/smoke diretamente); se não houver, manter o gap declarado em `## Casos práticos` — não fabricar → avalia E4
  - Adicionar `## O que vem a seguir` com ponte narrativa despachando para `[[03-Dominios/Tecnologia/Testes JS/11 - Snapshot testing]]`, `[[03-Dominios/Tecnologia/Acessibilidade/Auditar e Testar/14 - Testes de a11y no código]]`, `[[03-Dominios/Engenharia/Arqueologia e Restauração de Software/11 - Approval e Golden Master testing]]` e `[[03-Dominios/Tecnologia/Java/Testes/20 - Contract testing — Pact]]` (paths literais da Diretriz de fronteira, linha 84 do roadmap; conferir existência com `ls` antes de escrever o wikilink) → ativa E5 e quita o despacho pendente
  - Converter `### Vocabulário` (linha 291-302) de lista com `—` para tabela PT ↔ EN → ativa E7
  - Criar `## Armadilhas comuns` e mover o `[!danger] Snapshot fatigue` (linha 146-147) pra lá; como só há 1 callout de armadilha real no corpo (a mais pobre do galho), completar até 3 **derivando armadilhas do conteúdo técnico já presente na nota** — sem inventar experiência do usuário: (a) property-based com gerador mal definido/propriedade fraca vira "teste inútil" (já apontado na tabela-resumo, linha 261, e no texto "Não vale quando..." linha 117); (b) contract testing aplicado a monolito ou a terceiro que você não controla é esforço desperdiçado (linha 213, "Não vale pra um monolito, nem pra uma integração pontual..."); (c) smoke test inflado até virar suite e2e disfarçada, perdendo a velocidade que é sua única razão de existir (já é o `[!note]` da linha 244-245, que pode ser reclassificado como `[!warning]` individual) → ativa E8
  - Reformular o callout `[!info] Lastro` (linhas 304-309) como seção `## Fontes`, preservando as mesmas 5 URLs em formato de link markdown clicável → ativa L2
  - Pesquisar vídeo/podcast sobre property-based testing (QuickCheck/Hypothesis) ou consumer-driven contract testing (Pact) e embutir como `[!tip]` só se `uvx yt-dlp` baixar legenda de fato (trava de mídia) → ativa M1
- **Resultado:** —

#### 14 - Performance, carga, caos e segurança   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 311 linhas · fase: magus · status: evergreen
- **Núcleo/gaps:** E4 (sem `## Casos práticos`), E5 (sem `## O que vem a seguir` — há bridging em "Onde cada um entra" mas não a seção literal), E7 (Vocabulário é lista com `→`, não tabela), E8 (sem `## Armadilhas comuns`; só 2 `[!warning]` soltos — linha 69, 207 — mais 1 `[!danger]` linha 48, abaixo do piso de 3), L2 (só callout `[!info] Lastro`, não `## Fontes`), M1 (nenhum `[!tip]` com vídeo/podcast)
- **Score:** 7/12
- **Plano de execução:**
  - Adicionar `## O que vem a seguir` com ponte narrativa despachando para `[[03-Dominios/Engenharia/Operação/index]]`, `[[03-Dominios/Tecnologia/Web Performance/index]]` e `[[03-Dominios/Tecnologia/Java/Testes/18 - Performance — JMH e microbenchmarks]]` (paths literais da Diretriz de fronteira, linha 85 do roadmap, verificados com `ls`) → ativa E5 e quita o despacho pendente
  - Avaliar se há caso prático real (projeto/cliente do usuário) para `## Casos práticos`; se não houver, registrar o gap como buraco declarado — não fabricar caso → E4
  - Converter a seção `### Vocabulário` (lista com `→`) em tabela PT ↔ EN → E7
  - Criar `## Armadilhas comuns` e MOVER (não duplicar) os `[!warning]` existentes (linha 69, 207); avaliar se o `[!danger]` da linha 48 também migra; registrar que restam só 2-3 warnings, abaixo do piso de 3 — não fabricar novo → E8
  - Renomear/mover o callout `[!info] Lastro` para seção `## Fontes` com as URLs já presentes (linhas 294-301) → L2
  - Adicionar `[!tip]` com link de vídeo/podcast relevante (ex.: sobre chaos engineering, load testing ou JMH) → M1
- **Resultado:** —

#### 15 - Testes em CI-CD   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 333 linhas reais · fase: magus · status: evergreen
- **Núcleo/gaps:** E1 (TL;DR `[!abstract]`, linha 18-19, tem só 1 linha densa, não ≥3) · E4 (o caso real do spec de origem — stack MedEspecialista: JUnit 5 + AssertJ + Mockito + Testcontainers, ~800 testes em ~3 min no GitHub Actions, "PR sem teste não é revisado" — está presente como `[!example]` "No MedEspecialista", linha 233-236, embutido dentro de `## Não ignore os warnings`, não em seção dedicada `## Casos práticos`; é só 1 cenário, não fabricar segundo) · E5 (sem `## O que vem a seguir`; existe `## Veja também`, linha 325, lista pura de wikilinks, não ponte narrativa) · E8 (4 `[!warning]`/`[!danger]` espalhados no corpo — linha 35 "O mito do 'temos CI porque temos pipeline'", linha 149 "Fail fast", linha 175 "O trade-off honesto da seleção de teste", linha 213 "Retry mascara, não cura", linha 224 "Coverage theater" — ≥3 disponíveis, mas sem seção `## Armadilhas comuns` dedicada) · L2 (callout `[!info] Lastro`, linhas 316-323, tem 6 URLs já clicáveis, mas não está em seção `## Fontes` — gap de formato)
- **Score:** 6/11 (P1 N/A — nota conceitual, sem bloco de código-problema; diagramas Mermaid e tabelas ilustram os conceitos)
- **Plano de execução:**
  - Expandir o `[!abstract]` (linha 18-19) de 1 para ≥3 linhas densas, cobrindo a tese "teste só vale rodando na esteira", a distinção CI-como-prática × pipeline-como-ferramenta, e o orçamento de dez minutos → ativa E1
  - Formalizar em `## Casos práticos` o caso real já presente (callout `[!example]` "No MedEspecialista", linha 233-236: stack JUnit 5 + AssertJ + Mockito + Testcontainers, ~800 testes em ~3 min no GitHub Actions via paralelização, regra "PR sem teste não é revisado"); preservar os fatos exatamente como estão, não fabricar segundo cenário — registrar que só há 1 disponível, abaixo do mínimo de 2 → ativa E4 parcialmente
  - Adicionar `## O que vem a seguir` com ponte narrativa despachando para `[[03-Dominios/Tecnologia/Testes JS/17 - Testes na CI]]`, `[[03-Dominios/Tecnologia/Python/Testes/09 - Capstone — a suíte de testes da API de Tarefas]]` e `[[03-Dominios/Engenharia/Operação/index]]` (paths literais da Diretriz de fronteira, linha 86 do roadmap; Operação é a casa canônica da esteira de CI/CD — despacho obrigatório; confirmar existência com `ls` antes de escrever o wikilink) → ativa E5 e quita o despacho pendente
  - Mover (não duplicar) os 5 callouts existentes (`[!warning]` linha 35; `[!warning]` linha 149; `[!warning]` linha 175; `[!danger]` linha 213; `[!warning]` linha 224) para nova seção `## Armadilhas comuns`, individualizados → ativa E8
  - Reformular o callout `[!info] Lastro` (linhas 316-323) como seção `## Fontes`, preservando as URLs já clicáveis (Fowler ×3, GoCD, Humble & Farley, Octopus Deploy, Unleash, Harness, GitLab Docs) → ativa L2
  - Pesquisar vídeo/podcast sobre CI/CD, trunk-based development ou deployment pipeline (ex.: Martin Fowler falando sobre CI, ou talk sobre progressive delivery/canary) e embutir como `[!tip]` só se `uvx yt-dlp` baixar legenda de fato (trava de mídia) → ativa M1
- **Resultado:** —

#### 16 - Estratégia de testes em entrevista   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 286 linhas reais · fase: magus · status: evergreen
- **Núcleo/gaps:** E1 (o callout de abertura é `[!tip] Resumo em uma linha`, linha 18-19, não `[!abstract]`, e tem só 1 linha densa, não ≥3) · E4 (sem seção `## Casos práticos`; a nota é capstone de síntese e não há caso real do usuário mapeado no spec de origem aplicável aqui — não fabricar) · E5 (sem seção literal `## O que vem a seguir`; existe só `## Veja também`, linha 277, lista pura — e o gap real é de conteúdo, não só de rótulo: a Diretriz de fronteira do galho atribui à nota 16 a "tabela consolidada conceito → ferramenta, por stack (Java · JS/TS · Python · Go)", mas o despacho atual, tanto no `## Veja também` quanto no corpo, cita só `[[Testes em Java]]` e `[[Testes em JavaScript]]` — zero menção às vertentes Testes JS (18 notas), Python/Testes (9), Go/15 - Testes (8) e Java/Testes (21), todas nascidas depois de 2026-06-18) · L2 (existe `## 8. Recursos`, linha 210, com livros e URLs, mas as URLs estão em texto puro — ex. "kentcdodds.com/blog/..." — não como link markdown clicável, e a seção não se chama `## Fontes`; gap de formato) · M1 (nenhum dos `[!tip]` da nota tem link de vídeo/podcast — o único `[!tip]`, linha 18, é o resumo em uma linha)
- **Isenções aplicadas (não contam no denominador):** E6 e E7 — a nota já é a consolidação canônica de vocabulário do galho (`## 4. How to explain in English`, `## 5. Frases úteis em entrevista`, `## 6. Vocabulário PT→EN consolidado`); E8 — já existe `## 7. Armadilhas consolidadas`, consolidação das armadilhas do galho inteiro; P1 — nota conceitual pura, sem bloco de código (só diagramas Mermaid)
- **Score:** 4/8 (E2, E3, L1, P2 satisfeitos; E1, E4, E5, L2, M1 em gap; denominador = 12 − 3 isenções [E6,E7,E8] − 1 N/A [P1] = 8)
- **Plano de execução:**
  - Converter o callout de abertura (linha 18-19) de `[!tip]` para `[!abstract]` com ≥3 linhas densas, cobrindo a tese (gestão de risco, não cerimônia de ferramentas), o roteiro de sete passos e o fechamento do galho → ativa E1
  - Avaliar se há caso real do usuário aplicável para `## Casos práticos`; como capstone de síntese, se não houver caso novo (distinto dos já usados nas notas 01-15), manter o gap declarado — não fabricar → avalia E4
  - **Ação principal desta nota:** construir a tabela consolidada conceito → ferramenta por stack (Java · JS/TS · Python · Go) determinada pela Diretriz de fronteira do galho, e adicionar `## O que vem a seguir` com ponte narrativa para FORA do galho (é o fecho da trilha, não uma próxima nota interna), despachando para os quatro clusters hoje não citados — usar os índices já verificados como alvo: `[[03-Dominios/Tecnologia/Testes JS/index|Testes JS]]` (18 notas), `[[03-Dominios/Tecnologia/Python/Testes/index|Python/Testes]]` (9 notas), `[[03-Dominios/Tecnologia/Go/15 - Testes/index|Go/15 - Testes]]` (8 notas) e `[[03-Dominios/Tecnologia/Java/Testes/index|Java/Testes]]` (21 notas) — mantendo (não removendo) os links já existentes a `[[Testes em Java]]` e `[[Testes em JavaScript]]` como as notas mono-arquivo equivalentes → ativa E5
  - Reformular `## 8. Recursos` (linhas 210-228) como `## Fontes`, convertendo as URLs em texto puro (Testing Trophy, Mocks Aren't Stubs, Testcontainers, Awaitility, Testing Library) em links markdown clicáveis; os livros sem URL permanecem em prosa → ativa L2
  - Pesquisar vídeo/podcast sobre estratégia de testes em entrevista técnica (ex.: mock interview de system design de testes, ou talk sobre "how would you test this") e embutir como `[!tip]` só se `uvx yt-dlp` baixar legenda de fato (trava de mídia) → ativa M1
  - Também atualizar `index.md` do galho com a seção "Fronteiras" reescrita (hoje lista só Java e JS) — ação de escopo do galho, não desta nota isoladamente, mas dependente do mesmo levantamento de paths
- **Resultado:** —

