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
| ✅ escritas | 28 |
| ⬜ não escritas | 0 |
| 🔄 rascunho | 0 |
| % escrito | 100% |

**Por fase:** Iniciado 7/7 ✅ (COMPLETA) · Adepto 9/9 ✅ (COMPLETA) · Magus 12/12 ✅ (COMPLETA). **GALHO COMPLETO NA ESCRITA.** Notas 19-28 escritas em fan-out (workflow, 10 subagentes Sonnet, 2026-07-03); pendente rodada de enriquecimento nota a nota.

## Tabela-resumo (enriquecimento das escritas)

| Métrica | Valor |
|---------|-------|
| Escritas | 28 |
| ✅ enriquecidas | 0 |
| ⬜ pendentes (só M1/mídia) | 28 |
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

### Adepto (8-16) — COMPLETA ✅

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
- **Escrita:** ✅ 2026-07-02 (commit 28d4d55)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 321 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T2 isento (321 < 400)
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre The Mikado Method / prerequisite graph refactoring
- **Resultado:** Ellnestam & Brolund (*The Mikado Method*, Manning 2014); a hidra (conserta-um-quebram-três, branch que incha); analogia pega-varetas; ciclo tentar→observar-o-que-quebra→anotar-pré-requisito→REVERTER (git reset --hard)→atacar folha; grafo Mikado (folhas seguras→raiz/objetivo, sempre partindo do verde); por que reverter é genial (sempre-entregável, liga a Strangler 18); 4 armadilhas (não-reverter, raiz-antes-das-folhas, grafo-só-na-cabeça, compilou≠seguro)

#### 16 - IA como acelerador e seus riscos   [substantivo]
- **Escrita:** ✅ 2026-07-02 (commit dc148da) — **FECHA a fase Adepto**
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 349 linhas · fase: Adepto · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T2 isento (349 < 400)
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre AI coding agents legacy / automation bias / characterization before AI
- **Resultado:** onde a IA acelera (compreensão/08+06, docs/07, caracterização/10-11, refatoração/12-14); REGRA DE OURO = rede de caracterização ANTES de deixar a IA mudar (velocidade sem rede = quebrar mais rápido); riscos com mecanismo (alucinação de comportamento/API, perda da teoria/Chesterton-02/07, contexto-limitado vs acoplamento-temporal-09, automation bias, vazamento de código do cliente); fluxo seguro (entender→caracterizar→IA-propõe→rede-valida→revisão→micro-commit); fronteira IA `Agentes de Codificação` (link confirmado resolve); fontes NIST/OWASP LLM Top 10 (sem dados fabricados); absorveu candidato C5 da nota 01

### Magus (17-28) — COMPLETA ✅ (12/12)

#### 17 - Frameworks de decisão   [substantivo]
- **Escrita:** ✅ 2026-07-03 (commit 3732632)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 353 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T3 500 isento (353); **P3 COBRADO e atendido** (seção Fundamento teórico)
- **Score:** 11/12 (gap único = M1)
- **Plano de execução:** buscar vídeo sobre application portfolio rationalization / TIME model / rewrite vs refactor (Spolsky)
- **Resultado:** ABRE a Magus (virada mudar-com-segurança → decidir-o-destino). 7 R's (Gartner 2010 5R → AWS/Orban 2016 6R → 7º Relocate) como cardápio de invasividade, mapeados nos 4 verbos do consultor (manter/restaurar/substituir/aposentar); TIME (valor×qualidade, 4 quadrantes) como lente de portfólio — Migrate é o território do restaurador; fluxo 2 etapas (TIME classifica → R dentro do Migrate); rewrite vs incremento (Spolsky/Netscape "pior erro estratégico"; código feio = bug consertado = teoria de Naur; quando rewrite se justifica: teoria perdida/plataforma morta/domínio mudou — sempre via Strangler, nunca big-bang); P3 = teoria de portfólio + falácia custo-afundado/tela-em-branco + leis de Lehman (mudança contínua/complexidade crescente) + valor de opção da reversibilidade; 2 casos trabalhados (faturamento Migrate→Refactor; relatório "morto" que era Retain por compliance). Sem dados fabricados. Fronteiras linkadas: Strangler(18)/dados(20)/política(23)/compliance(27).

#### 18 - Strangler Fig   [substantivo]
- **Escrita:** ✅ 2026-07-03 (commit 852e068)
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 327 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T3 500 isento (327); P3 COBRADO e atendido (seção Fundamento teórico)
- **Score:** 11/12 (gap único = M1)
- **Plano de execução:** buscar vídeo sobre Strangler Fig pattern / legacy displacement / monolith to microservices (Fowler, Thoughtworks, GOTO/NDC talks)
- **Resultado:** a execução do quadrante Migrate (nota 17). Metáfora da figueira de Queensland (Fowler 2004, StranglerApplication→StranglerFigApplication); anatomia em 5 passos (interceptar via facade de roteamento → construir ao lado → migrar função a função → repetir → remover); facade/proxy/API gateway como coração do padrão (o interruptor de desvio por rota). As 2 estratégias de Fowler: **event interception** (desviar só os eventos das funções migradas, não todos) e **asset capture** (mover a posse de um subconjunto de ativos por vez); as duas se amarram (capturar ativo exige interceptar seus eventos). Strangler vs big-bang cutover (a aposta de tudo-ou-nada; separar fluxo×dado evita o bug de dois donos do mesmo dado). **P3:** valor de opção da reversibilidade (opções reais, liga à 17§4) + redução de risco por tamanho de lote (small batches) + entrega incremental de valor/feedback curto + Lehman (não congela evolução). Parentesco explícito com Mikado (15). 2 casos (monólito→serviços canônico; faturamento na borda com parallel run→21). Fronteiras linkadas: 17(decisão)/19(Branch by Abstraction nível-código)/20(asset capture=dados)/21(parallel run). Sem dados fabricados.

#### 19 - Branch by Abstraction e Anti-Corruption Layer   [substantivo]
- **Escrita:** ✅ 2026-07-03 (commit 098c29d) — fan-out
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 366 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T3 500 isento; P3 atendido
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre Branch by Abstraction / trunk-based development / Anti-Corruption Layer (Hammant, Fowler, DDD)
- **Resultado:** duas técnicas de coexistência complementares ao Strangler. BRANCH BY ABSTRACTION (Hammant/Fowler/Humble&Farley): trocar implementação no nível do CÓDIGO quando não há borda de rede pra facade — 5 passos (introduzir abstração → migrar chamadores → construir nova impl → alternar via flag → remover velha), trunk sempre verde (contraste irônico com "branch"). ANTI-CORRUPTION LAYER (Evans, DDD): camada de tradução que protege o modelo novo da contaminação conceitual do legado. **P3:** information hiding (Parnas 1972) + DIP/SOLID + bounded contexts (Evans) + reversibilidade/opções reais. Fronteira EXPLÍCITA: Strangler=nível requisição/sistema vs BbA=nível código. 2 casos (motor de frete in-process / serviço de precificação vs CRM legado).

#### 20 - Migração de dados e schema   [substantivo]
- **Escrita:** ✅ 2026-07-03 (commit 29b61b5) — fan-out
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 352 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T3 500 isento; P3 atendido
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre expand-contract / online schema migration / gh-ost / zero-downtime data migration
- **Resultado:** o asset capture (18) aprofundado no nível dos DADOS. EXPAND-CONTRACT (Fowler/Sato ParallelChange) em 3 fases (expand schema aditivo → migrate dual writes+backfill+migrar leituras → contract remove velho); shadow tables (gh-ost) p/ tabelas grandes sem lock; DATA ARCHAEOLOGY (escavar significado real de colunas legadas sujas — status codes reaproveitados — antes de migrar). **P3:** dado tem estado/código não (revert de dado não é trivial) + Kleppmann (dual writes não-atômicas, CDC/single-writer) + Ambler&Sadalage transition period + Naur aplicado ao dado. Fronteira: parallel run que compara dados → empurrado à 21. 2 casos (faturamento expand-contract / cadastro de cargas arqueologia).

#### 21 - Validação em produção   [substantivo]
- **Escrita:** ✅ 2026-07-03 (commit d233a88) — fan-out
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 366 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T3 500 isento; P3 atendido
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre feature flags / GitHub Scientist / dark launch / canary release
- **Resultado:** escada de exposição crescente pra validar mudanças no legado em produção: feature flags/release toggles (Hodgson), dark launch, PARALLEL RUN (GitHub Scientist — fecha o laço aberto na 18: rodar velho+novo, retornar o velho como fonte da verdade, comparar silenciosamente), canary/gradual rollout, e INSTRUMENTAR o legado (dar olhos a um sistema inobservável). **P3:** observabilidade formal (Kálmán 1960, teoria de controle — legado sem instrumentação é literalmente inobservável) + falsificação de Popper (parallel run busca refutação, não confirmação) + gap teoria-reconstruída-vs-realidade. Fronteira: linka `Operação` (disciplina de SRE/observabilidade mora lá). 2 casos (faturamento parallel run+canary / reconciliação sem instrumentação).

#### 22 - Dependências, upgrades e segurança   [substantivo]
- **Escrita:** ✅ 2026-07-03 (commit 193c509) — fan-out
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 338 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T3 500 isento; P3 atendido. **Link corrigido pós-fan-out:** apontava pra `Fundamentos/Segurança Conceitual/index` (inexistente) → corrigido pra `03-Dominios/Engenharia/Segurança/index` (galho real).
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre dependency management / CVE / SBOM / framework major upgrade
- **Resultado:** o legado que apodrece por baixo mesmo sem tocar no código: EOL, CVEs acumulando, versões sem suporte. Due diligence de vulnerabilidades (SCA, SBOM, Dependabot/Renovate); migração de versão de framework/runtime (major incremental, transitive dependency hell); por que "Retain" (17) tem prazo de validade (dependência estável vira CVE crítica sozinha — o gatilho de reavaliação que a 17 prometeu). **P3:** dívida de dependência como juros compostos / leis de Lehman (risco cresce sozinho). Fontes OWASP A06:2025/Dependency-Check, NIST NVD, SBOM/CISA.

#### 23 - A dimensão política   [substantivo]
- **Escrita:** ✅ 2026-07-03 (commit c98590b) — fan-out
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 350 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T3 500 isento; P3 atendido
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre Bellotti Kill It with Fire / selling technical debt / modernization business case
- **Resultado:** nenhum framework técnico vale nada sem VENDER a decisão. Bellotti "o sistema em volta do sistema" (a organização/pessoas/incentivos são tão legado quanto o código). Business case (traduzir dívida técnica em risco/custo/receita), stakeholders, buy-in; early win (04) como capital político; vender incremento (Strangler) é politicamente mais fácil que big-bang. **P3:** fundamento organizacional/mudança (Kotter urgência+coalizão) + quadrantes de dívida técnica de Fowler. Complementa a 17 (frameworks técnicos ↔ venda da decisão). Fecha o laço da 04.

#### 24 - Conhecimento e documentação   [substantivo]
- **Escrita:** ✅ 2026-07-03 (commit d0c7051) — fan-out
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 347 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T3 500 isento; P3 atendido
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre ADR / C4 model (Simon Brown) / living documentation
- **Resultado:** o antídoto de longo prazo: externalizar a TEORIA (Naur) pra não se perder de novo — fecha o ciclo do galho. ADRs (Nygard: capturar o porquê, não o quê); living docs/C4 (Simon Brown); offboarding=onboarding; matar o bus factor (09) espalhando conhecimento tribal. **P3:** teoria de Naur como o ativo a preservar; conhecimento tácito→explícito. Referenciada pela 07 (registrar o porquê agora); liga ao bus factor da 09 (ação de espalhar, não medir).

#### 25 - Sustentabilidade humana   [substantivo]
- **Escrita:** ✅ 2026-07-03 (commit 8cfa1e3) — fan-out
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 350 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T3 500 isento; P3 atendido
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre developer burnout / software estimation / cone of uncertainty (McConnell)
- **Resultado:** o custo HUMANO do legado. Burnout específico (frustração crônica, medo de quebrar, trabalho invisível/ingrato); estimativa sob incerteza (spikes time-boxed — fecha o laço da 17; cone da incerteza de McConnell; faixas, não números; sub-prometer); ritmo sustentável (Beck/XP); pequenas vitórias (sempre-entregável do Strangler/Mikado combate o desânimo). **P3:** cone da incerteza (McConnell) + sustainable pace (XP) + pesquisa de burnout (Maslach). Fecha o laço da 17 (spike time-boxed).

#### 26 - Firefighting em produção   [substantivo]
- **Escrita:** ✅ 2026-07-03 (commit ecda2b6) — fan-out
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 378 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T3 500 isento; P3 atendido
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre incident response / blameless post-mortem / git bisect debugging
- **Resultado:** o modo RESGATE (03) aprofundado: incidente num sistema que você não entende. Triagem sob pressão (estancar o sangramento/mitigar ANTES de causa raiz); ferramentas do galho sob fogo (git bisect/blame 07, forense 09, observabilidade 21); playbook detectar→mitigar→diagnosticar→resolver→post-mortem blameless; como evitar chegar lá (caracterização 10-11, deploys pequenos/reversíveis 18/15). **P3:** MTTR vs MTBF / restaurar serviço ≠ corrigir bug; teoria de incident response. Fronteira: linka `Operação` (disciplina completa). Modo resgate da 03 aprofundado.

#### 27 - Compliance e arqueologia legal   [substantivo]
- **Escrita:** ✅ 2026-07-03 (commit a501271) — fan-out
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 342 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T3 500 isento; P3 atendido
- **Score:** 11/12
- **Plano de execução:** buscar vídeo sobre data retention / GDPR right to erasure / compliance legacy
- **Resultado:** por que certo código NÃO PODE ser deletado (fecha o laço das 16/17 — o "if"/relatório que parece morto). Escavar restrições legais/regulatórias antes de mexer: retenção de dados, auditabilidade, a TENSÃO LGPD/GDPR (esquecimento vs. retenção), SOX/HIPAA/PCI-DSS; "ninguém usa" ≠ "pode deletar" (valor de conformidade não aparece nos logs); Retire (17) é o único R irreversível. **P3:** restrição exógena vs trade-off de engenharia (sobrepõe a decisão técnica da 17); a arqueologia (tese do galho) aplicada ao domínio legal. Fecha o quadrante Eliminate/Retire da 17.

#### 28 - Capstone - Assumindo um sistema legado do zero   [substantivo]
- **Escrita:** ✅ 2026-07-03 (commit 962553f) — fan-out (fase 2, após 19-27) — **FECHA a Magus e o galho**
- **Enriquecimento:** ⬜ pendente (M1)
- **Estado:** 330 linhas · fase: Magus · status: seedling
- **Núcleo/gaps:** M1 (vídeo); T3 500 isento; P3 atendido. **Refs internas VERIFICADAS contra filenames reais** (lição Compiladores) — todos os [[nota N]] batem; `[[index]]` ambíguo → path completo.
- **Score:** 11/12
- **Plano de execução:** rodada de mídia (vídeo panorâmico de "taking over a legacy system")
- **Resultado:** capstone integrativo (NÃO introduz conceito novo). Estudo de caso na plataforma de logística das 17/18: jornada completa due diligence→herança→resgate→volta (o diagrama de modos não-estanques da 03), costurando as 3 fases (Iniciado entender / Adepto mudar com segurança / Magus decidir e ser dono). **P3 sofisticado:** Naur (missão única = recuperar a teoria) + modelo de Dreyfus (5 estágios de perícia justificam a ordem Iniciado→Adepto→Magus; pular = novato decidindo como especialista) + Cynefin de Snowden (legado real é COMPLEXO → probe-sense-respond, não sense-analyze-respond; "entender antes de tocar" é exigência estrutural) + jornada como sequência de opções reais. Definição operacional de "dono confiante" = conhecimento não depender de uma cabeça só. Fontes-âncora reais (Naur, Feathers, Bellotti, Fowler, Tornhill, Dreyfus, Snowden). "O que vem a seguir" aponta pro index/01 (não há nota 29).

---

## Próximos passos

**ESCRITA COMPLETA — 28/28 notas (Iniciado 7/7 · Adepto 9/9 · Magus 12/12).** O eixo primário (escrita) fechou em 2026-07-03; as notas 19-28 foram escritas em fan-out (workflow, 10 subagentes Sonnet, fase 1 = 19-27 em paralelo + fase 2 = capstone). O eixo restante é **enriquecimento**.

1. **Rodada de mídia (M1)** — o único gap recorrente das 28 notas. Buscar 1 vídeo/podcast por nota (skill `/adicionar-midia`), começando pelas âncoras (01 já tem Feathers; priorizar 17/18 e o capstone 28).
2. **Enriquecimento nota a nota** (skill `/enriquecer-galho` + `/enriquecer-nota`) — as 10 notas do fan-out (19-28) são drafts de qualidade validada estruturalmente (11/12, gap único M1) mas ainda não passaram por enriquecimento manual; revisar profundidade/exemplos/diagramas onde couber. Diagramas Mermaid do fan-out usam `graph`/`sequenceDiagram` (seguros no Quartz).
3. **Verificação de publish:** confirmar que os diagramas Mermaid e wikilinks das 10 notas novas renderizam no Quartz (wikilinks quebrados por newline já corrigidos no pós-fan-out; link Segurança Conceitual já apontado pro path real `Engenharia/Segurança/index`).
4. **Manutenção do roster:** se surgir broto/sub-tópico Magus, seguir a convenção broto→galho.

> **Nota de processo (fan-out 2026-07-03):** 10 notas escritas por workflow com governança — 9 escritores paralelos (Sonnet/effort high) + capstone sequencial lendo os arquivos reais (evita alucinação de mapa). Pós-processamento manual do orquestrador: correção de wikilinks partidos por line-break, correção de path cross-galho, verificação de refs internas do capstone, commit nota a nota (stage explícito, sem assinatura). ~809k tokens de subagente.
