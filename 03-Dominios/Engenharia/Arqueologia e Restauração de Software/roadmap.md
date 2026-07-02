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
| ✅ escritas | 8 |
| ⬜ não escritas | 20 |
| 🔄 rascunho | 0 |
| % escrito | 29% |

**Por fase:** Iniciado 7/7 ✅ (COMPLETA) · Adepto 1/9 🔄 · Magus 0/12 ⬜.

## Tabela-resumo (enriquecimento das escritas)

| Métrica | Valor |
|---------|-------|
| Escritas | 8 |
| ✅ enriquecidas | 0 |
| ⬜ pendentes (só M1/mídia) | 8 |
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

### Adepto (8-16) — em andamento 🔄 (1/9)

#### 08 - Engenharia reversa e recuperação de arquitetura   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit 13b36e5)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 320 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T2 isento (320 < 400, padrão capítulo)
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre reflexion models / architecture reconstruction / ArchUnit / dependency graphs
- **Resultado:** fragmentos → mapa formal; 2 braços (extração/grafo + validação/reflexion model Murphy-Notkin); erosão & desvio (Perry-Wolf); top-down↔bottom-up (OORP); DSM; ferramentas por stack (jdeps/ArchUnit/madge/import-linter); 2 cenários (due diligence núcleo cíclico / resgate divergência)

#### 09 - Forense de software   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Adepto
- **Plano de execução:** método de Tornhill (*Your Code as a Crime Scene* 2ª ed 2024): hotspots (complexidade × mudança), acoplamento temporal, bus factor quantificados. Aprofunda o faro introduzido na 07.
- **Resultado:** —

#### 10 - A rede de segurança primeiro   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Adepto
- **Plano de execução:** characterization tests — testes que revelam o comportamento atual (não o "correto"). Fronteira com galho `Testes`.
- **Resultado:** —

#### 11 - Approval e Golden Master testing   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Adepto
- **Plano de execução:** pôr código intocável sob teste rápido (Bache & Falco); approval testing, golden master.
- **Resultado:** —

#### 12 - Seams e quebra de dependência   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Adepto
- **Plano de execução:** os pontos de intervenção; o legacy change algorithm (Feathers); tipos de seam.
- **Resultado:** —

#### 13 - Técnicas cirúrgicas   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Adepto
- **Plano de execução:** Sprout/Wrap method & class, micro-committing, exploratory refactoring.
- **Resultado:** —

#### 14 - Refactoring em terreno hostil   [substantivo]
- **Escrita:** ⬜ não escrita
- **Enriquecimento:** ➖ n/a
- **Estado:** — · fase: Adepto
- **Plano de execução:** o catálogo de Fowler aplicado a código que resiste (sem rede, com acoplamento).
- **Resultado:** —

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

1. **Escrever a nota 09** (Forense de software) — método de Adam Tornhill (*Your Code as a Crime Scene* 2ª ed 2024): hotspots (complexidade × mudança), acoplamento temporal, *bus factor* quantificados. Aprofunda o faro introduzido na 07 e a intensidade que falta ao mapa estático da 08.
2. Seguir o roster 10→28, uma por vez, commitando por nota (ou par), atualizando **este roadmap** (escrita ✅ + commit) a cada nota fechada.
3. **Rodada de mídia (M1)** das 7 notas de Iniciado quando o galho amadurecer — buscar 1 vídeo/podcast por nota (skill `/adicionar-midia`), fechando o único gap recorrente.
4. Ao concluir cada fase, atualizar a linha "Por fase" e as duas tabelas-resumo.
