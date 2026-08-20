---
title: "Roadmap — Segurança e Guardrails"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Segurança e Guardrails

Diagnóstico migrado de guia/roadmap - ia.md (28/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Segurança e Guardrails`

> [!warning] Diagnóstico de 28/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho. ⚠️ Este galho tem alerta regulatório adicional: a nota 11 (EU AI Act) tem prazo de caducidade em 2026-08-02 — checar se ainda reflete "lei ainda não aplicável" ou se precisa virar "lei já aplicável".

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado · P4 Exemplo com número |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado) **Piso de linhas:** aplicável — Iniciado ≥300 · Adepto ≥400 · Magus ≥500 (decisão do usuário, 2026-08-01)

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 13 |
| ⬜ pendente | 0 |
| ➖ não precisa | 0 |
| ✅ feita | 13 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

> [!note] Nota 13 acrescentada em 2026-08-16 — o galho passou a ter dois escopos
> As notas 01-12 cobrem a segurança do **código gerado por IA**. A nota 13 abre o **Bloco 5**: segurança de **runtime** da feature de IA (prompt injection), que não tinha dono no vault — o tema aparecia disperso em 01, 07 e em `Context Engineering/12`, apesar de o index do domínio listá-lo entre os 8 erros recorrentes. Lacuna identificada na comparação com o board *IA do Zero ao Sênior* ([[2026-ia-do-zero-ao-senior-trilha-visual]]). Se o Bloco 5 crescer para ~5 notas, considerar graduá-lo a galho próprio conforme a convenção broto → galho.

> [!success] Galho enriquecido 2026-07-06 — 12/12 notas via fan-out ≤3 verificado (4 ondas). **Caducidade regulatória resolvida:** a pesquisa da nota 11 revelou que o Digital Omnibus on AI (mai/2026) já ADIOU as obrigações high-risk do EU AI Act (Anexo III→02/12/2027, Anexo I→02/08/2028); GPAI + Art. 50 permanecem em 02/08/2026. Nota 11 reflete o estado real. Reavaliar após 02/08/2026 (primeiras multas GPAI, texto final do Omnibus). Desvio menor: nota 10 ficou em 296 linhas (4 abaixo do piso 300) — sem padding por design.

---

## Notas

#### 01 - Código gerado por IA é untrusted   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 201 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L2
- **Score:** 10/12
- **Plano de execução:**
  - Expandir "A janela de risco" com exemplos reais de incidentes, expandir "Onde a indústria está", ou adicionar seção "Como montar um pipeline mínimo" para atingir ≥300 linhas
  - Adicionar URLs reais às referências (Veracode, BusinessWire, Help Net Security)
- **Resultado:** 301 linhas. Expandiu "A janela de risco" com incidentes reais (CVE-2025-8217 Amazon Q, CVE-2025-53773 Copilot, Vibe Security Radar); nova seção "Como montar um pipeline mínimo" (4 gates); "Onde a indústria está" com dado GitGuardian; subseção "Refinamento iterativo piora" (arXiv 2506.11022). Todas as refs com URL real verificada + 4 fontes novas. status→growing.

#### 02 - Slopsquatting — o ataque via alucinação   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 251 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar seção "Impacto real — o que os estudos medem" (dados USENIX) e/ou aprofundar "Por que LLMs alucinam tanto pacote" para atingir ≥300 linhas
  - Adicionar URLs reais às referências (Trend Micro, Socket.dev, Snyk, Aikido, Mend.io, USENIX, Cloudsmith)
- **Resultado:** 301 linhas. Nova seção "Impacto real" com dados USENIX 2025 (Spracklen et al., 576k amostras, 5,2%/21,7% taxa) + 3 callouts (huggingface-cli, conversão 20-35%, frontier 2026). Aprofundou "Por que LLMs alucinam pacote" (confusão de ecossistema, RAG/Self-Refinement 83% redução). 8 refs com URL real. status→growing.

#### 03 - Alucinações em código — APIs fantasma e parâmetros inexistentes   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 283 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário concreto antes de "Os 5 tipos" (ativa E2 e sobe o piso)
  - Adicionar URLs reais às referências (Veracode 2025, Trend Micro, OWASP LLM Top 10, Pydantic docs)
- **Resultado:** Parágrafo de abertura com cenário concreto (`auto_validate=True` absorvido por `**kwargs`) antes de "Os 5 tipos" (ativa E2). 4 refs com URL real (Veracode 2025, Trend Micro, OWASP LLM Top 10, Pydantic). Plano aplicado integralmente, sem desvios.

#### 04 - A pirâmide de validação AI   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 250 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar seção "Casos reais de falha na pirâmide" com 2-3 exemplos de incidentes por camada ausente, ou expandir "Anti-patterns" com 2 itens adicionais
  - Adicionar URLs reais às referências (Veracode 2025, DryRun Security, NVIDIA blog, Anthropic engineering blog, OWASP LLM Top 10)
- **Resultado:** Anti-patterns expandido com 2 itens (coverage% como proxy; guardrails camada-2 sem review). 5 refs com URL real verificada. Desvio: optou por expandir Anti-patterns em vez da seção "Casos reais" para evitar fabricar incidentes sem fonte por camada.

#### 05 - SAST e SCA para código AI   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 291 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2, E3
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário concreto (ativa E2 e sobe piso)
  - Adicionar URLs reais às referências (DryRun Security, Veracode 2025, Semgrep docs, Socket.dev, OWASP LLM Top 10)
  - Adicionar diagrama Mermaid (pipeline CI/CD SAST+SCA ou árvore de decisão de ferramentas) — ativa E3 e contribui para o piso
- **Resultado:** 335 linhas. Abertura com cenário concreto (path traversal via open(), PR aprovado, pentest 3 semanas depois) ativa E2. Mermaid novo (flowchart pipeline SAST+SCA com gate bloqueante) ativa E3. 5 URLs reais. status→growing. Score ~10/12.

#### 06 - Permissões e sandboxing   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 324 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs reais às referências (Anthropic Claude Code docs, Truefoundry blog, Adversa AI CVE post, NVIDIA whitepaper, Docker docs, Startup Fortune)
  - Opcional: snippet mostrando o resultado de deny rule contornada (bubblewrap Permission denied)
- **Resultado:** 336 linhas. 6 refs com URL real (Anthropic eng+docs, Truefoundry, Adversa AI, NVIDIA, Docker, Startup Fortune). Snippet opcional aplicado (deny rule contornada → `Permission denied` via `--ro-bind /etc/`, CVE-2026-25723). Desvio menor: "The Menon Lab" sem URL verificável, mantido só texto.

#### 07 - Security-focused prompting   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 306 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L2, E2
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar URLs reais às referências (Veracode 2025, Anthropic Best Practices, OWASP LLM Top 10 2025, Augment Code docs, Microsoft Security blog)
  - Adicionar parágrafo de abertura com cenário concreto entre o TL;DR e "O que NÃO funciona"
- **Resultado:** 5 refs com URL real (Veracode, Anthropic, OWASP, Augment Code, Microsoft), cada uma anotada com o ponto que sustenta. Parágrafo de abertura com cenário concreto (prompt genérico→validação superficial→PR aprovado→pentest) ativa E2. Plano integral.

#### 08 - Code review de código AI — o que muda   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 285 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário concreto antes do `[!abstract]`
  - Adicionar URLs reais às referências (Anthropic Best Practices, GitHub AI code review post, Augment Code docs, Atlassian AI assistants blog, Plus8Soft Comprehension Gate)
- **Resultado:** Abertura com cenário concreto (tech lead com 47 PRs na fila, aprovação por inércia, race condition em cobrança descoberta 3 semanas depois) ativa E2. 5 refs com URL real (Anthropic, GitHub, Augment, Atlassian, Plus8Soft). Plano integral.

#### 09 - Testes imutáveis — a barreira que o agente não pode reescrever   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 322 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs reais às referências (Anthropic Best Practices, Augment Code docs, Martin Fowler Spec by Example, GitHub Spec Kit)
  - P1 (código-com-falha) inaplicável para nota de prática/guardrail — não forçar
- **Resultado:** 4 refs com URL real (Anthropic, Augment Code, Martin Fowler SpecByExample, GitHub Spec Kit), cada uma com frase de contexto. P1 corretamente marcado inaplicável (nota de prática/guardrail). Plano integral.

#### 10 - Métricas de qualidade AI — defect escape rate, rework ratio   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 281 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs reais às referências (dora.dev, GitClear AI impact on code quality, METR, Veracode State of Software Security)
  - Adicionar Mermaid mostrando evolução temporal das 5 métricas (xychart ou timeline antes/depois de intervenção) para atingir o piso
- **Resultado:** 4 refs com URL real (dora.dev, GitClear 2025, METR RCT, Veracode 2025); Augment sem URL pública. Mermaid `timeline` da história dos dashboards (6 marcos, semana 1→16) ativa E3. Desvio menor: 296 linhas (4 abaixo do piso 300) — não fez padding por design; T1 pode fechar depois com lente Lacunas/Casos práticos.

#### 11 - Governance as architecture — EU AI Act, GDPR, licenças   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** 237 linhas reais · fase: Iniciado · status: seedling ⚠️ caducidade regulatória
- **Núcleo/gaps:** E1, L2
- **Score:** 9/12
- **Plano de execução:**
  - Expandir "Para code generation especificamente", "High-risk AI systems" e "Para times brasileiros" (status do PL 2338/2023, comparativo LGPD × GDPR × AI Act) — meta +65 linhas para atingir o piso
  - Quebrar o TL;DR em ≥3 linhas distintas: deadline/impacto imediato, obrigações práticas para code generation, consequência de não fazer (€35M / 7% de faturamento global) — ativa E1
  - Adicionar URLs reais às referências (digital-strategy.ec.europa.eu, artificialintelligenceact.eu)
  - ⚠️ Caducidade regulatória: prazo "2 de agosto de 2026" vence em ~33 dias (a partir de 2026-06-30) — adicionar `[!warning]` de caducidade avisando que após 2026-08-02 a nota precisa ser atualizada para o modo "lei já aplicável" (enforcement, primeiras multas, comunicados da Comissão Europeia)
- **Resultado:** 237→382 linhas (+69). TL;DR em 3 linhas (E1). **Descoberta via web: o Digital Omnibus on AI (acordo mai/2026) ADIOU obrigações high-risk — Anexo III→02/12/2027, Anexo I→02/08/2028; GPAI+Art.50 permanecem 02/08/2026.** Refletido em datas, novo Mermaid timeline e seção High-risk. Callout [!warning] recalibrado. Expandiu code-gen (tabela metadados/PR), Brasil (PL 2338/2023 + comparativo LGPD×GDPR×AI Act). 6 refs com URL real. status→growing.

#### 12 - O roadmap de segurança para times   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-06)
- **Estado:** ~316 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs reais às 5 referências (Veracode 2025 GenAI Report, DryRun Security SAST Tools 2026, Anthropic Best Practices for Claude Code, NVIDIA Sandboxing Guidance, EUR-Lex EU AI Act)
- **Resultado:** 5/5 refs com URL real (Veracode 2025, DryRun 2026, Anthropic, NVIDIA, EUR-Lex Reg. UE 2024/1689). Plano integral, sem desvios.

#### 13 - Prompt injection — quando o dado vira instrução   [substantivo]
- **Enriquecimento:** ✅ feita (2026-08-19)
- **Estado:** 403 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** — (T2, M1 e P1 fechados na expansão)
- **Score:** ~10/13 (checklist já com o novo item P4)
- **Plano de execução:**
  - `/adicionar-midia` — talk sobre prompt injection (Simon Willison tem palestras gravadas sobre o tema) → resolve M1
  - Bloco de código com falha: montagem de prompt concatenando retorno de ferramenta sem tag nem sanitização, e a versão com tag + allowlist de domínio na renderização → resolve P1
  - **Expansão real de conteúdo até o piso de 400** (déficit +185): terceiro e quarto cenário prático (agente de código lendo issue hostil; MCP server de terceiro devolvendo payload), seção sobre detecção (classificadores XPIA e por que falham isolados), e aterrissagem dos 6 padrões num exemplo trabalhado ponta a ponta. Expansão substantiva, nunca padding.
  - Verificar após 02/08/2026 se o EU AI Act cria obrigação específica sobre injection que valha citar na nota 11
- **Resultado:** 215→403 linhas, fecha o piso Adepto sem padding. Acrescentado: TL;DR em 3 blocos (E1); 2 vídeos verificados via oEmbed — RedMonk e Heavybit/Generationship, ambos com Simon Willison (M1); seção "O bug que a camada 1 sozinha não pega" com montagem de prompt concatenando retorno de tool cru + versão taggeada e resumida (P1); seção "Detectar não é defender" (classificador XPIA, por que o EchoLeak passou por ele, assimetria do falso negativo); "A terceira forma: quando o ataque fica" (injeção persistente — memória, índice do RAG, arquivos de instrução); Cenário 3 (agente de código lendo issue hostil, CVE-2025-53773 desarmando a camada 4) e Cenário 4 (MCP server de terceiro, com a distinção server-malicioso vs server-honesto-repassando-terceiros e a descrição de tool como vetor); "Um exemplo trabalhado" aplicando Plan-Then-Execute + Context-Minimization + Map-Reduce a um agente de suporte, com o custo subindo a cada degrau; seção "Como testar o seu sistema" (eval adversarial, 4 famílias incluindo falso positivo, critério = ação não ocorre); checklist de revisão pré-deploy; 5ª armadilha (modelo novo não resolveu); callout `[!question]-` sobre por que a indústria segue lançando agentes.
