---
name: processar-vaga
description: >
  Processa uma vaga de emprego a partir de URL pública em nota canônica em `03-Dominios/Inglês/Entrevistas/Vagas/` seguindo o padrão da Mappa 3276 (10 seções: BLUF, briefing da empresa, briefing da vaga, match analysis, pitch adaptado, prováveis perguntas em 6 fases, histórias do banco mapeadas, cheat sheet de vocabulário, logística/checklist, próximas ações, histórico). Aciona com "/processar-vaga <url>", "processa essa vaga", "ficha essa vaga", "vaga: <url>", "registra essa vaga", ou colando uma URL com pedido de processamento. Lê dossiê do candidato (Narrativa Profissional + Roadmap GCA) pra compor Match Analysis, pitch e mapeamento de histórias. Cross-linka com Sessions GCA (01-05) sistematicamente. NÃO inventa dados da empresa — onde faltar informação, marca explicitamente "(a confirmar no Recruiter Call)" ou "(a pesquisar)".
---

# processar-vaga

## O que faz

Transforma uma URL de vaga em **uma nota canônica de preparação de entrevista** em `03-Dominios/Inglês/Entrevistas/Vagas/`. A nota tem 10 seções estruturadas que cobrem:

- **Diagnóstico da vaga** (empresa, stack, senioridade, sinais culturais).
- **Match analysis** (pontos fortes do candidato + gaps com mitigação).
- **Pitch adaptado** (Tell me about yourself + Why this role customizados pra vaga).
- **Prováveis perguntas em 6 fases** (Recruiter, Hiring Manager, Tech Deep Dive, System Design, Cultural Fit, Logística), cada uma com estratégia de resposta.
- **Histórias do banco mapeadas** (cenários típicos → história do candidato → BLUF de abertura).
- **Cheat sheet de vocabulário** (power verbs, glossário pt/en, kill list).
- **Logística + Smart Questions** pra cada persona da entrevista.

Padrão de referência: `03-Dominios/Inglês/Entrevistas/Vagas/Mappa 3276 - Senior Platform Lead Java-Kotlin.md`.

## Quando usar

- Slash command: `/processar-vaga <url>`
- Linguagem natural: "processa essa vaga: \<url\>", "ficha essa vaga", "registra essa vaga", "preparação pra essa vaga: \<url\>"
- Compartilhar URL de uma vaga + pedido de processamento.

## Inputs aceitos

| Forma | Exemplo | Comportamento |
|---|---|---|
| URL como argumento | `/processar-vaga https://...` | Usa direto |
| URL em mensagem livre | "processa essa vaga: https://..." | Extrai URL e processa |
| Sem URL | `/processar-vaga` | Pergunta a URL |

## Inputs esperados (do contexto)

- **URL pública da vaga** (obrigatório). Páginas com paywall/login → falha graciosamente.
- **Template** em `00-Meta/templates/Template - Vaga.md` (obrigatório).
- **Dossiê do candidato** (opcional mas crítico pra qualidade):
  - `03-Dominios/Inglês/Entrevistas/Minha Narrativa Profissional.md` (se existir)
  - `03-Dominios/Inglês/GCA/Roadmap.md` (campo `## Dossiê do Aluno` traz perfil, cenário, gargalo, estratégia)
  - Sessions GCA processadas em `03-Dominios/Inglês/GCA/Sessions/` (01-Foundation, 02-Manager of One, 03-BLUF, 04-Resilience, 05-AI Workflow)

Sem dossiê → seções de Pitch e Histórias do banco ficam mais genéricas, marcadas pra refinamento manual.

## Steps

### 1. Obter URL

- Se URL no argumento → usa.
- Se sem argumento → pergunta: "Cole a URL da vaga, por favor."
- Validar formato (`https?://`).

### 2. Fetch da URL

Usar `WebFetch` com prompt estruturado pedindo extração de:

- Nome da empresa + breve descrição (missão, setor, tamanho).
- Posição + senioridade.
- Modalidade (remote/hybrid/onsite) + timezone.
- Tipo de contrato (full-time/PJ/contractor) + restrições geográficas.
- Faixa salarial (se divulgada).
- Idioma requerido.
- Stack técnica obrigatória.
- Stack nice-to-have.
- Responsabilidades.
- Benefícios.
- Deadline de aplicação.
- Processo de entrevista.
- Valores culturais.
- Sinais sobre estágio/funding/tamanho do time.

**Se URL falha** (404, paywall, JS-heavy SPA sem SSR): reporta erro e pede ao usuário colar manualmente o texto da vaga. NÃO inventa dados.

### 3. Pesquisa complementar (best-effort)

Se o nome da empresa for público (não-anônimo), tentar enriquecer:

- **LinkedIn da empresa** (página pública): estágio, tamanho do time, geografia da sede.
- **Site oficial**: produto, missão real, casos de uso.
- **Glassdoor** (se acessível sem login): faixa salarial real, reviews de cultura.

Empresas anônimas (marketplaces tipo Mappa.ai com disclosure só pós-Recruiter Call) → marcar `empresa: Anônima` e populizar `## Briefing da empresa` com o pitch declarado no listing.

### 4. Inferir filename canônico

Formato base: `<Plataforma|Empresa> [job_id] - <Posição curta>.md`

Exemplos:
- Com plataforma intermediária e ID: `Mappa 3276 - Senior Platform Lead Java-Kotlin.md`
- Sem ID, vaga direta: `Codelitt - Senior Fullstack Java Engineer.md`
- ID na URL slug: `Codelitt mByg2FsH0l - Senior Fullstack Java Engineer.md` (opcional)

Slug rules:
- Substituir `/` por `-` (problema em filenames).
- Manter capitalização da posição.
- Limitar a ~70 caracteres totais.

### 5. Verificar conflito

- Arquivo já existe → confirmação simples: "Nota da vaga já existe. Sobrescrever (perde edições manuais)?"
- Usuário disse não → aborta limpo.

### 6. Ler dossiê do candidato

Em paralelo:

- `Minha Narrativa Profissional.md` (extrair: timeline, projetos canônicos, métricas, posicionamento).
- `Roadmap.md` do GCA (extrair: perfil do aluno, gargalo atual, ancoragem salarial, estratégia).
- Sessions GCA processadas (extrair: princípios BLUF, regras Kill List, defesa do gap, narração da IA).

Se algum arquivo ausente → segue com placeholders nas seções que dependeriam dele, marcados explicitamente.

### 7. Compor frontmatter

Resolver placeholders Templater do `Template - Vaga.md`:

```yaml
title: <auto do filename>
created, updated: <data atual>
type: vaga
status: seedling
empresa: <nome ou "Anônima (oculta na listagem)">
plataforma: <nome plataforma intermediária ou empresa direta>
url: <URL original>
job_id: <ID se houver>
posicao: <título da vaga>
senioridade: junior | pleno | senior | staff | lead | principal
modalidade: remote | hybrid | onsite
contrato: full-time | contractor | pj | eor
salario_min: <número ou vazio>
salario_max: <número ou vazio>
moeda: USD | BRL | EUR | etc.
idioma_requisito: en-advanced | en-fluent | en-intermediate | pt-br
dominio: <setor: healthcare, fintech, wealth tech, devtools, etc.>
stack: [Java, Spring, etc.]
fase_aplicacao: prospeccao | aplicado | recruiter | hiring-manager | tech | system-design | offer | nao-aprovado
prioridade: alta | media | baixa
data_aplicacao: <vazio ou data>
deadline: <vazio ou data se divulgado>
data_publicacao: <data de publicação se divulgada>
tags: [entrevista, vaga, <stack>, <dominio>, remoto-internacional se aplicável]
publish: false
```

### 8. Compor seções do corpo (10 seções do padrão Mappa)

#### Seção 0 — BLUF (callout `> [!info] BLUF — Por que esta vaga`)

Uma frase: match principal + faixa salarial + alavanca de carreira (por que esta vaga vale o esforço de preparação).

#### Seção 1 — Briefing da empresa

- `> [!abstract] O que sabemos` — lista do extraído (empresa, setor, modelo de trabalho, stack confirmada, banda salarial, skills listadas, pitch da empresa).
- `> [!warning] Sinais de alerta da listagem` — observações sobre vagueness, anonimato, título ambíguo, escopo expandido, etc.
- `> [!question] Perguntas obrigatórias para o Recruiter Call` — bullets com perguntas críticas pra qualificar a vaga.
- `> [!note] Sinais culturais detectados` — pistas no texto da vaga (jargão, valores expressos, missão, tom).

#### Seção 2 — Briefing da vaga

- `### Stack confirmada` — bullet do que está textualmente na descrição.
- `### Stack provável (inferida)` — o que toda empresa nesse setor/stack costuma usar (frameworks, DB, cloud, mensageria, CI/CD, compliance — citando o motivo da inferência).
- `### Responsabilidades inferidas` — em vagas vagas, inferir do título + setor + senioridade.
- `### Sinais de senioridade` — o que o título sugere sobre escopo (IC vs gestão, ownership).

#### Seção 3 — Match Analysis

- **Tabela `### Pontos fortes (onde brilho)`**: Requisito da vaga × Minha experiência × História/Case do banco.
- **Tabela `### Gaps (onde tenho que posicionar bem)`**: Gap × Mitigação/Como enquadrar.
- **Posicionamento estratégico**: 1-2 frases em estilo executivo de como o candidato se apresenta nesta vaga especificamente.

#### Seção 4 — Pitch adaptado

- `### Tell me about yourself (60-90s) — versão customizada`: callout `> [!quote] Draft v1 (a refinar com [[Coaching]])` com pitch customizado pra stack + setor da vaga.
- Lista **Aplicar**: Session 02 (Manager of One), Session 03 (BLUF), Power verbs, Kill list, Cadência.
- `### Why this role / why this company (30-45s)`: callout `> [!quote]` com 2 razões concretas (domínio + escopo).

#### Seção 5 — Prováveis perguntas

Subseções por fase, cada `> [!question]` com **Strategy** explicando a abordagem:

- **Fase 1 — Recruiter Screen**: Tell me about yourself; Why looking; Salary expectation (ancorar acima da banda); English level (responder com evidência de uso, não nível); Currently employed; Other interviews; Defesa do gap (`Session 04 - Resilience Architecture`).
- **Fase 2 — Hiring Manager Fit**: BLUF drills com casos de plataforma owned, technical disagreement, debt vs feature delivery, domínio do setor.
- **Fase 3 — Technical Deep Dive**: stack-specific (Java migration, event-driven, data quality, quality engineering, ferramentas-chave da vaga, AI workflow).
- **Fase 4 — System Design**: Think Aloud Protocol — clarifying questions → high-level → trade-offs → edge cases → compliance.
- **Fase 5 — Cultural Fit**: liderança sem hierarquia, async, conflito com peer, handle being wrong, why this company.
- **Fase 6 — Logística / Closing**: quando pode começar, smart questions.

#### Seção 6 — Histórias do banco mapeadas para esta vaga

Tabela: Cenário típico × História a usar × Primeira frase BLUF (rascunho).

Cenários canônicos (~9):

1. Legacy modernization
2. Tight deadline delivery
3. Technical disagreement
4. Production incident
5. Translating tech to non-tech
6. Mentoring / leading
7. Proactive optimization
8. Manager of One
9. AI workflow

Cada linha popular usando histórias do dossiê (Muvz, MedEspecialista, syllabus module, CI/CD, agentes IA, etc.).

#### Seção 7 — Cheat sheet de vocabulário

- `### Power verbs prioritários para esta vaga` (categorizados: Plataforma / Modernização / Qualidade / Liderança / Domínio-específico).
- `### Vocabulário do domínio (en)` — tabela pt-BR ↔ en pra termos críticos do setor (ex: prontuário eletrônico → EHR; conformidade → compliance).
- `### Kill list para esta entrevista` — vícios pessoais a evitar (basically, I think, like/you know, I helped to, sort of, kind of, a little bit of, stuff).

#### Seção 8 — Logística & checklist

- `### Antes do Recruiter Call`: aplicar, salvar PDF, pesquisar empresa, gravar pitch, lista de perguntas, setup técnico, disponibilidade.
- `### Logo após o Recruiter Call`: nome da empresa, stack completa, processo, Glassdoor, produto, refinar este documento.
- `### Perguntas para fazer no final de cada etapa (Smart Questions)`: bullets por persona (Recruiter, Hiring Manager, Tech Panel, C-Level).

#### Seção 9 — Próximas ações

Checklist concreto: aplicar, estudar stack-specific, refinar pitch com `/coaching`, gravar e medir WPM, ensaiar defesa do gap, adaptar CV.

#### Seção 10 — Histórico

Tabela: Data × Etapa × Notas × Próximo passo. Primeira linha já preenchida com data de descoberta da vaga.

### 9. Veja também

Lista de wikilinks:
- `[[Minha Narrativa Profissional]]` — pitch base
- `[[03-Dominios/Inglês/GCA/Roadmap|Roadmap GCA]]`
- `[[Session 01 - Foundation]]` — STAR + Power Verbs
- `[[Session 02 - Manager of One]]` — Pitch + cadência
- `[[Session 03 - BLUF Framework]]` — Kill list + drills
- `[[Session 04 - Resilience Architecture]]` — Defesa do gap
- `[[Session 05 - Narrating the AI Workflow]]` — IA executiva

### 10. Validação final

Buscar `<% ` ou ` %>` no output — qualquer residual = bug de mapeamento → aborta antes de salvar.

### 11. Salvar

Em `03-Dominios/Inglês/Entrevistas/Vagas/<filename>.md`.

### 12. Reportar

```
Processado: <Empresa> [<id>] - <Posição>
Arquivo: 03-Dominios/Inglês/Entrevistas/Vagas/<filename>.md

Dados extraídos:
  • Empresa: <nome ou "Anônima">
  • Modalidade: <remote/hybrid/onsite>
  • Banda salarial: <range ou "Não divulgada">
  • Stack: <lista>
  • Idioma: <nível>

Match analysis:
  • Pontos fortes mapeados: <N> requisitos
  • Gaps identificados: <M>

Cross-links GCA: <K> Sessions referenciadas.

Próximos passos sugeridos no documento:
  • Aplicar à vaga (registrar data no frontmatter)
  • Pesquisar empresa em LinkedIn/Glassdoor
  • Refinar pitch com /coaching
  • Gravar pitch e medir WPM
```

## Tratamento de erros

| Cenário | Comportamento |
|---|---|
| URL inválida (não-https/http) | Erro com exemplo de formato esperado |
| WebFetch falha (paywall, 404, JS-only SPA) | Reporta limitação; pede ao usuário colar texto da vaga manualmente |
| Template `Template - Vaga.md` ausente | Aborta com path explícito |
| Pasta `Vagas/` ausente | Cria automaticamente |
| Arquivo já existe | Confirmação reforçada (perde edições manuais) |
| Dossiê do candidato ausente | Segue, marca seções dependentes com placeholder "(refinar manualmente — dossiê não encontrado)" |
| Sintaxe Templater (`<% %>`) restando no output | Aborta antes de salvar |
| Empresa anônima (marketplace tipo Mappa) | Marca `empresa: Anônima`; popula com pitch declarado; adiciona perguntas obrigatórias pra revelar nome no Recruiter Call |

## Não fazer

- **Não inventar dados de empresa** — Glassdoor/LinkedIn só se realmente acessíveis. Onde faltar, marcar "(a pesquisar)" ou "(a confirmar no Recruiter Call)".
- **Não fingir conhecer stack** além do que a vaga declara — usar "Stack provável (inferida)" pra projeções, sempre com motivo da inferência.
- **Não fabricar histórias do banco** que não estão no dossiê do candidato — se não houver dossiê, marcar tabela como "refinar manualmente".
- **Não copiar verbatim** textos longos da descrição da vaga — parafrasear pros sumários.
- **Não substituir o trabalho cognitivo do candidato** — pitch é DRAFT v1 explicitamente marcado pra refinar com `/coaching`.
- **Não modificar vagas já existentes** sem confirmação reforçada.
- **Não vazar info sensível** — se a vaga revela nome em "after-login" e o candidato compartilhou, OK; senão, respeitar opacidade da plataforma.

## Convenções de output

- **Filename:** `<Plataforma|Empresa> [job_id] - <Posição>.md` (capitalização da posição preservada, `/` substituído por `-`).
- **Frontmatter completo** conforme template; campos sem dado = vazio (não invenção).
- **Conteúdo em PT-BR** para meta-instruções (Strategy, comentários), **EN para drafts de pitch/respostas** (idioma de entrevista).
- **Wikilinks padrão** pras Sessions GCA, Narrativa Profissional, Roadmap.
- **Callouts Obsidian apropriados:**
  - `> [!info]` BLUF
  - `> [!abstract]` o que sabemos sobre a empresa
  - `> [!warning]` sinais de alerta
  - `> [!question]` perguntas pra fazer / perguntas prováveis
  - `> [!note]` sinais culturais
  - `> [!quote]` drafts de pitch (sempre marcados "Draft v1")
- **Tabelas Markdown** pras matrizes (Pontos fortes, Gaps, Histórias, Vocabulário, Histórico).
- **Power verbs prioritários** sempre customizados pra stack + setor da vaga (não copy-paste genérico).

## Notas técnicas

### Pra empresas anônimas (Mappa, marketplaces de talento)

Mappa.ai (e marketplaces similares) escondem o nome da contratante até o Recruiter Call. Nesses casos:

- Marcar `empresa: Anônima (oculta na listagem da Mappa)` no frontmatter.
- Usar `plataforma: Mappa` (ou nome da plataforma intermediária).
- Na `## 1. Briefing da empresa`, focar no pitch declarado pelo marketplace + skills listadas + faixa salarial.
- Adicionar `> [!question]` com perguntas pra revelar nome no Recruiter Call (`"Qual o nome da empresa contratante e onde fica a sede?"`).
- Após Recruiter Call, atualizar o documento com nome real + pesquisa LinkedIn/Glassdoor.

### Pra empresas com vaga rica em detalhe

Quando a descrição já traz responsabilidades + stack expandida + processo de entrevista:

- Reduzir `## Stack provável (inferida)` a só o que NÃO está declarado.
- Expandir `## 5. Prováveis perguntas` com cases stack-specific declarados na vaga.
- `## 8. Logística` lista o processo declarado em vez de inferido.

### Pra vagas onde o candidato já tem cases diretos

Quando o dossiê (Narrativa Profissional + Sessions GCA) contém múltiplos cases relevantes pro domínio da vaga:

- Tabela `## 6. Histórias do banco` pesada (>9 linhas se aplicável).
- Pitch adaptado com 3-4 frases de impacto concreto em vez de 2.
- Match analysis com 7-8 linhas de pontos fortes em vez de 3-4.
