---
title: "Roadmap — Arqueologia e Restauração de Software"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Arqueologia e Restauração de Software

Roadmap do galho `03-Dominios/Engenharia/Arqueologia e Restauração de Software`. Diferente dos galhos de IA (todos escritos, rastreiam enriquecimento), este galho está **em construção**: o eixo primário é **escrita** (quantas das 28 notas do roster já existem), e o enriquecimento (sobretudo mídia) é secundário, aplicado nota a nota depois. Fonte do roster: `index.md`.

## Régua de análise

Dois eixos de rastreio:

- **Escrita:** ⬜ não escrita · 🔄 rascunho · ✅ escrita+commitada (YYYY-MM-DD).
- **Enriquecimento:** ⬜ pendente · ➖ n/a (nota ainda não escrita) · ✅ enriquecida. Nas notas já escritas, o gap recorrente é **M1 (vídeo/mídia)** — obrigatório só na rodada de enriquecimento futura.

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado 1-7 / Adepto 8-16 / Magus 17-28).
**Piso de linhas:** aplicável em tese (Iniciado ≥300 / Adepto ≥400 / Magus ≥500) — **mas ISENTO na prática**: o galho segue o [[feedback_padrao_capitulo_livro|padrão capítulo-de-livro]], que substitui o piso. T1 aparece como ✗ nas notas curtas mas é aceito; não inflar.
**P1 (código-com-falha):** N/A na maioria — são notas conceituais de método/ofício, não de código executável.

## Tabela-resumo (escrita)

| Métrica | Valor |
|---------|-------|
| Total de notas (roster) | 28 |
| ✅ escritas | 14 |
| ⬜ não escritas | 14 |
| 🔄 rascunho | 0 |
| % escrito | 50% |

**Por fase:** Iniciado 7/7 ✅ (COMPLETA) · Adepto 7/9 🔄 · Magus 0/12 ⬜.

## Tabela-resumo (enriquecimento das escritas)

| Métrica | Valor |
|---------|-------|
| Escritas | 14 |
| ✅ enriquecidas | 0 |
| ⬜ pendentes (só M1/mídia) | 14 |
| Score médio verificar-nota | 11/12 (gap único = M1) |

---

## Notas

<!-- Escrita: ⬜ não escrita · 🔄 rascunho · ✅ (data). Enriquecimento: ⬜ · ➖ n/a · ✅.
     Custo do que falta: [mecânico] barato/sem pesquisa · [substantivo] pesquisa/redação. -->

### Iniciado (1-7) — COMPLETA ✅

#### 01 - O que é código legado   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit 36e6b5d)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 294 linhas · fase: Iniciado · status: growing
- **Núcleo/gaps:** M1 (vídeo Feathers já embutido — reavaliar); T1 isento
- **Score:** 11/12
- **Plano de execução:** — nenhuma (já tem vídeo Feathers Tech Lead Journal #195); revisar na rodada de mídia
- **Resultado:** duas definições (Feathers sem testes / Bellotti dono foi embora) + teoria de Naur; quadrante Domesticável

#### 02 - A mentalidade do restaurador   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit 36e6b5d)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 241 linhas · fase: Iniciado · status: growing
- **Núcleo/gaps:** M1 (vídeo); T1 isento
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre Chesterton's Fence / mentalidade de manutenção de legado
- **Resultado:** Cerca de Chesterton, legado-como-ativo, "humildade ativa", 3 armadilhas (Brooks second-system)

#### 03 - A lente do consultor   [substantivo]  **(espinha)**
- **Escrita:** ✅ 2026-07-02 (commit 2ceda8c)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 272 linhas · fase: Iniciado · status: growing
- **Núcleo/gaps:** M1 (vídeo); T1 isento
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre technical due diligence / assumir sistemas alheios
- **Resultado:** de-dentro-vs-de-fora; 3 modos (due diligence/herança/resgate) com diagrama+tabela; 3 armadilhas por modo

#### 04 - Os primeiros 30-60-90 dias   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit 3a67be4)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 270 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T1 isento
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre Watkins "The First 90 Days" / onboarding em legado
- **Resultado:** ponto de equilíbrio + imperativo da ação (Watkins); 3 arcos orientar/contribuir/independência; early win seguro

#### 05 - First Contact   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit 2928e8b)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 238 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T1 isento
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre reproducible builds / rodar legado / OORP
- **Resultado:** inventário técnico (buildar+rodar); cadáver vs vivo; padrões OORP; Interview during Demo

#### 06 - Lendo código que você não escreveu   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit ec5bbaf)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 239 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T1 isento
- **Score:** 11/12
- **Plano de execução:** buscar vídeo de Felienne Hermans (Programmer's Brain, InfoQ "Reading Code") ou scratch refactoring
- **Resultado:** memória de trabalho (Hermans, 2-6 chunks); top-down/bottom-up; tracing reverso; scratch refactoring

#### 07 - Arqueologia do histórico   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit 227bd3a)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 214 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T1 isento
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre git archaeology / git blame forense / git log pickaxe
- **Resultado:** código=o "como" / git=o "porquê"; blame -w/-M, pickaxe log -S; hotspots só introduzidos (defere à 09)

### Adepto (8-16) — em andamento 🔄 (7/9)

#### 08 - Engenharia reversa e recuperação de arquitetura   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit 13b36e5)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 320 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T2 isento (320 < 400, padrão capítulo)
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre reflexion models / architecture reconstruction / ArchUnit / dependency graphs
- **Resultado:** fragmentos → mapa formal; 2 braços (extração/grafo + validação/reflexion model Murphy-Notkin); erosão & desvio (Perry-Wolf); top-down↔bottom-up (OORP); DSM; ferramentas por stack (jdeps/ArchUnit/madge/import-linter); 2 cenários (due diligence núcleo cíclico / resgate divergência)

#### 09 - Forense de software   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit d7cebd4)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 319 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T2 isento
- **Score:** 11/12
- **Plano de execução:** buscar vídeo de Adam Tornhill / CodeScene / behavioral code analysis
- **Resultado:** método de Tornhill (*Your Code as a Crime Scene* 2ª ed 2024): hotspots (complexidade × frequência de mudança — nenhuma dimensão sozinha basta), acoplamento temporal (o que o mapa estático da 08 NÃO vê), bus factor/knowledge map; ferramenta-âncora CodeScene + open-source (code-maat, git-of-theseus); 3 diagramas (quadrante hotspot + estático×temporal)

#### 10 - A rede de segurança primeiro   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit cfdef1e)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 334 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T2 isento
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre characterization testing / Feathers / approval testing intro
- **Resultado:** PIVÔ entender→mudar-com-segurança; paradoxo galinha-e-ovo (Feathers); virada mental = caracterizar (comportamento ATUAL) ≠ especificar (correto); técnica "deixe o código confessar" (asserção que falha → valor real → pina); bug vira contrato documentado; código Java; delimita 10=manual/saída-pequena vs 11=ferramenta/saída-grande; fronteira galho Testes

#### 11 - Approval e Golden Master testing   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit c95f730)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 317 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T2 isento
- **Score:** 11/12
- **Plano de execução:** buscar vídeo de Emily Bache (approval testing / gilded rose) ou Llewellyn Falco
- **Resultado:** continuação direta da 10 (saída grande/opaca onde a caracterização manual não escala); golden master (congela saída p/ N inputs, muitas vezes gerados/aleatórios); approval testing (received vs approved, aprova snapshot em vez de asserção); ferramentas ApprovalTests (Falco), TextTest (Geoff Bache — correção de atribuição, Emily = divulgadora), Verify/.NET, jest snapshots; armadilhas aprovar-cegamente + não-determinismo/scrubbing; código Java

#### 12 - Seams e quebra de dependência   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit 7df5c72)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 468 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T2 OK (468 > 400 — a mais longa do galho, na faixa de profundidade preferida 440-540)
- **Score:** 11/12 (T2 ✓)
- **Plano de execução:** buscar vídeo sobre seams / breaking dependencies / Feathers legacy code
- **Resultado:** conceito de seam (alterar comportamento sem editar no lugar) + enabling point; 3 tipos (object/preprocessing/link); legacy change algorithm 5 passos (esta nota = passo 3, a 10 = passo 4); técnicas de quebra com código (Parameterize Constructor, Extract Interface, Extract and Override Call/Factory); paradoxo da testabilidade + "lean on the compiler"; delimita 12=abrir-seam-p/-testar-existente vs 13=costurar-novo-ao-lado

#### 13 - Técnicas cirúrgicas   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit 68c4209)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 388 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T2 OK (388 < 400 — isento pelo padrão capítulo)
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre Sprout Method / Wrap Method / adding features to legacy code
- **Resultado:** ADICIONAR sem abrir o velho (complemento da 12); Sprout Method/Class (brotar novo testado + 1 linha de chamada); Wrap Method/Class (renomear velho + interceptar); árvore de decisão sprout-vs-wrap; micro-commits reversíveis; scratch/exploratory refactoring só acenado (defere à 06); delimita 13=adiciona vs 14=reorganiza-existente

#### 14 - Refactoring em terreno hostil   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit d58c85a)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 405 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T2 OK (405 > 400)
- **Score:** 11/12 (T2 ✓)
- **Plano de execução:** buscar vídeo sobre Fowler refactoring / refactoring legacy code / Extract Method
- **Resultado:** definição estrita (estrutura sem comportamento — vital sem rede); micro-passo ainda menor no hostil; 4 receitas do catálogo com o perigo de cada (Extract Method/estado compartilhado, Rename/Naur, Extract Variable/número mágico, Extract Class/god class hotspot da 09); automated refactoring da IDE como aliado; tensão "alterna, não resolve"; quando NÃO refatorar (código estável); 4 armadilhas (misturar refactor+comportamento, sem rede, fora de escopo, Extract Class sem checkpoints)

#### 15 - O Método Mikado   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Adepto
- **Plano de execução:** grafo de pré-requisitos e revert agressivo para mudanças grandes.
- **Resultado:** —

#### 16 - IA como acelerador e seus riscos   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Adepto
- **Plano de execução:** LLM para engenharia reversa e docs; regra: characterization ANTES de deixar a IA mudar. Absorve o candidato C5 (retrospecto Feathers 2024 sobre FP/config/IA) cortado da nota 01. Fronteira com IA `Agentes de Codificação`.
- **Resultado:** —

### Magus (17-28) — não iniciada ⬜

#### 17 - Frameworks de decisão   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Magus
- **Plano de execução:** manter/restaurar/substituir/aposentar; os 6-7 R's, TIME (Gartner); rewrite vs. incremento.
- **Resultado:** —

#### 18 - Strangler Fig   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Magus
- **Plano de execução:** fazer o novo crescer em volta do velho, sempre entregável (Fowler).
- **Resultado:** —

#### 19 - Branch by Abstraction e Anti-Corruption Layer   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Magus
- **Plano de execução:** coexistência segura; proteger o novo do velho (DDD/Evans).
- **Resultado:** —

#### 20 - Migração de dados e schema   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Magus
- **Plano de execução:** expand-contract, dual writes, shadow tables, zero-downtime; data archaeology.
- **Resultado:** —

#### 21 - Validação em produção   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Magus
- **Plano de execução:** feature flags, dark launch, parallel run; instrumentar o legado com observabilidade. Fronteira com galho `Operação`.
- **Resultado:** —

#### 22 - Dependências, upgrades e segurança   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Magus
- **Plano de execução:** EOL/CVE, migração de versão de framework/runtime, due diligence de vulnerabilidades.
- **Resultado:** —

#### 23 - A dimensão política   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Magus
- **Plano de execução:** Bellotti "o sistema em volta do sistema"; vender modernização, stakeholders, business case. Já referenciada pela nota 04 (early win = capital de confiança).
- **Resultado:** —

#### 24 - Conhecimento e documentação   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Magus
- **Plano de execução:** ADRs (o *porquê*), living docs/C4, offboarding = onboarding, matar o bus factor. Já referenciada pela nota 07 (registrar o porquê agora).
- **Resultado:** —

#### 25 - Sustentabilidade humana   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Magus
- **Plano de execução:** burnout em legado, estimativa sob incerteza (spikes, time-boxing).
- **Resultado:** —

#### 26 - Firefighting em produção   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Magus
- **Plano de execução:** investigar e mitigar incidente num sistema que você não entende (o modo resgate da nota 03 aprofundado); e como evitar chegar lá. Fronteira com galho `Operação`.
- **Resultado:** —

#### 27 - Compliance e arqueologia legal   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Magus
- **Plano de execução:** por que certo código *não pode* ser deletado; desenterrar restrições legais antes de mexer.
- **Resultado:** —

#### 28 - Capstone - Assumindo um sistema legado do zero   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Magus
- **Plano de execução:** o playbook do consultor de ponta a ponta, num estudo de caso. Capstone — costura os três modos e as três fases. Atenção: capstones tendem a alucinar o próprio mapa do galho (lição do Compiladores) — verificar cada referência interna.
- **Resultado:** —

---

## Próximos passos

1. Faltam **2 notas para fechar a fase Adepto (8-16)**: a **15** e a **16**.
   - **Nota 15 — O Método Mikado**: grafo de pré-requisitos + revert agressivo para mudanças GRANDES/emaranhadas (onde puxar um fio quebra outros). A estratégia para o que as técnicas locais das notas 13-14 não dão conta sozinhas; 13 e 14 já apontam a 15 no handoff. Autores: Ola Ellnestam & Daniel Brolund (*The Mikado Method*, Manning 2014).
   - **Nota 16 — IA como acelerador e seus riscos** (FECHA a Adepto): LLM p/ engenharia reversa/docs; regra = characterization ANTES de deixar a IA mudar; absorve o candidato C5 cortado da nota 01. Fronteira com IA `Agentes de Codificação`.
2. Depois da 16, ABRE a fase **Magus (17-28)** pela nota 17 (Frameworks de decisão: manter/restaurar/substituir/aposentar; 6-7 R's, TIME Gartner). Magus pede piso T3 500 em tese (isento na prática) e P3 (teoria subjacente) passa a ser cobrado.
3. Seguir o roster 17→28, uma por vez, commitando por nota (ou par), atualizando **este roadmap** a cada nota fechada.
3. **Rodada de mídia (M1)** das 7 notas de Iniciado quando o galho amadurecer — buscar 1 vídeo/podcast por nota (skill `/adicionar-midia`), fechando o único gap recorrente.
4. Ao concluir cada fase, atualizar a linha "Por fase" e as duas tabelas-resumo.
