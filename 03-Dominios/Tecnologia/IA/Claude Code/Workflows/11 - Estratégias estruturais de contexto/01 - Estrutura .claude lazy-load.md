---
title: "Estrutura .claude/ lazy-load — carga inicial enxuta, resto sob demanda"
type: concept
progress: backlog
publish: true
created: 2026-05-22
updated: 2026-05-22
status: seedling
fase: iniciado
tags:
  - claude-code
  - workflows
  - contexto
  - tokens
  - claude-md
  - lazy-load
aliases:
  - Lazy-load de .claude
  - .claudeignore
---

# Estrutura `.claude/` lazy-load — carga inicial enxuta, resto sob demanda

> [!abstract] TL;DR
> A cada `claude` aberto, o [[Dicionário de IA#Claude Code|Claude Code]] lê CLAUDE.md, `.claude/` e tudo que o `.claudeignore` *não* exclui. Em projetos com docs históricas e CLAUDE.md inflado, isso queima 8k–15k [[Dicionário de IA#Token|tokens]] *antes* da primeira pergunta. A solução estrutural é separar o que precisa estar visível no startup (instruções de comportamento, comandos diários, armadilhas críticas) do que pode estar disponível mas não carregado (sessões antigas, decisões, ADRs). Tudo continua acessível por menção explícita — só não custa nada até ser pedido.

## O que é

Lazy-load aplicado ao contexto inicial do Claude Code: organizar `.claude/` e os arquivos auto-incluídos para que o startup carregue um conjunto mínimo de **instruções vivas**, e qualquer outra coisa fique no repositório mas fora do contexto até ser explicitamente requisitada.

Três ingredientes:

1. **CLAUDE.md curto e estável** — instruções de comportamento que não mudam de sessão pra sessão (convenções, restrições, comandos canônicos).
2. **`.claude/` com 3–4 arquivos focados** — "quick start", "armadilhas comuns", "mapa da arquitetura". Coisas que o agente realmente precisa ver toda sessão.
3. **`.claudeignore` agressivo** — exclui `docs/archive/`, `.claude/sessions/`, `completions/`, tudo que é histórico ou efêmero.

O resto da documentação fica nas pastas habituais do projeto. O agente pode lê-las quando você mencionar — não custa nada até lá.

## Como funciona

### Estrutura típica

```
your-project/
├── CLAUDE.md                    # ~150–300 tokens, ~30 linhas
├── .claudeignore                # exclui histórico e ruído
│
├── .claude/
│   ├── COMMON_MISTAKES.md       # top 5 bugs que custaram >1h
│   ├── QUICK_START.md           # comandos do dia-a-dia
│   ├── ARCHITECTURE_MAP.md      # "onde mora X"
│   ├── sessions/                # NO .claudeignore (0 tokens)
│   └── completions/             # NO .claudeignore (0 tokens)
│
└── docs/
    ├── INDEX.md                 # carregado se mencionado
    ├── adr/                     # decisões — lidas sob demanda
    └── archive/                 # NO .claudeignore
```

### O `.claudeignore` carrega o peso

```gitignore
# Sessões e histórico de Claude
.claude/sessions/
.claude/completions/
.claude/archive/

# Docs históricas
docs/archive/
docs/old/

# Build e dependências
node_modules/
dist/
build/
coverage/

# Logs e dumps
*.log
*.dump
*.bak
```

O `.claudeignore` segue a sintaxe do `.gitignore`. Tudo que ele cobre é invisível ao agente *até* você passar o caminho explicitamente em um `Read`.

### Princípio "0 tokens até ser pedido"

A regra mental: **arquivo carregado por default custa tokens em toda sessão**; arquivo ignorado custa zero tokens até ser explicitamente lido. Tudo que não muda *seu* comportamento como agente em *toda* sessão deve estar fora do default.

Decisões de arquitetura de 6 meses atrás? `docs/adr/` — não vai por default, vai quando você falar "leia o ADR-0007".

Resumo da sessão de ontem? `.claude/sessions/2026-05-21.md` — fica no repo pra você consultar, mas não pra o agente carregar.

Lista de tarefas concluídas? `.claude/completions/` — fica pra história, custa zero contexto.

## Quando usar

Vale a pena adotar quando:

- **Projeto >3 meses** com docs acumuladas e CLAUDE.md crescido organicamente.
- **Monorepo** ou repo grande onde o agente "varre" o início da sessão.
- **Pipelines automatizados** (CI, sub-agents) onde toda sessão paga o startup.
- Você já notou que `/context` mostra >5k tokens consumidos *antes* de você pedir nada.

Não vale a pena para:

- Projeto novo ou repo pequeno onde o CLAUDE.md ainda é proporcional.
- Sessões one-off em projeto exploratório.
- Caso onde a estrutura `.claude/` já não existe — não invente burocracia sem motivo.

## Como medir o impacto

Antes de adotar, meça. O comando `/context` no Claude Code mostra a composição atual:

```
/context
```

Output (esquematizado):

```
Total context: 14,832 tokens
  CLAUDE.md:           8,210 tokens
  .claude/:            3,420 tokens
  System reminders:    1,892 tokens
  ...
```

Se CLAUDE.md + `.claude/` somam >5k tokens em um projeto de tamanho médio, há ganho a capturar. Refatore, rode `/context` de novo, compare.

## Armadilhas

**Mover tudo pra lazy "porque parece bom"**. Se você esvazia o CLAUDE.md, perde as instruções de comportamento que mantêm o agente alinhado. O ponto é separar **instruções vivas** (ficam) de **histórico** (sai). Convenções de código, restrições do projeto, comandos canônicos — ficam.

**`.claudeignore` mal configurado bloqueando arquivos legítimos**. Se você ignora `docs/` inteiro, mas o agente precisa ler um ADR específico que você mencionou, ele vai falhar. `.claudeignore` afeta também leitura sob demanda — teste depois de configurar.

**Cache miss em [[Dicionário de IA#Prompt caching|prompt cache]]**. CLAUDE.md grande mas estável é melhor do que CLAUDE.md pequeno mas mutável: o prompt cache da Anthropic só ativa quando o início do contexto é idêntico entre chamadas. Se você fica trocando CLAUDE.md de sessão pra sessão, anula o desconto de cache (~$0.30/MTok vs $3/MTok). Estabilidade > tamanho.

**Atualizar `.claude/COMMON_MISTAKES.md` toda hora**. Se vira diário de bugs, perde o efeito (e quebra cache). Limite a bugs que custaram >1h pra debugar. Se passou de 10–15 itens, é hora de arquivar os mais antigos.

**Esquecer que `.claudeignore` é honrado por leitura mas não por geração**. O agente ainda pode *criar* arquivos em paths ignorados se você mandar — o ignore só afeta leitura.

## Relação com outras abordagens deste galho

Esta é a abordagem **Iniciada** — zero infra externa, aplicável em qualquer projeto hoje. Se ela não basta (codebase grande, agente sempre relê o repo inteiro mesmo com CLAUDE.md enxuto), os próximos passos são [[02 - Sandboxing de tool output]] para output verboso, [[03 - Indexação semântica externa]] para busca em codebase grande, [[04 - Knowledge graph local com AST]] para impact analysis.

## Veja também

- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|CLAUDE.md anatomia]] — estrutura do arquivo principal
- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/03 - CLAUDE.md receitas|CLAUDE.md receitas]] — templates por stack
- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/07 - Pasta .claude|Pasta .claude]] — convenções de organização
- [[03-Dominios/Tecnologia/IA/Claude Code/Mental Model/07 - Tokens e custo|Tokens e custo]] — fundamentos econômicos
- [[03-Dominios/Tecnologia/IA/Claude Code/Workflows/11 - Estratégias estruturais de contexto/index|Tronco do sub-galho]]

## Aprofundamento

> [!convite] Referências externas
> - [nadimtuhin/claude-token-optimizer](https://github.com/nadimtuhin/claude-token-optimizer) — scaffolding via `npx` que cria a estrutura `.claude/` e `.claudeignore` para 13 frameworks (Express, Next.js, Vue, Django, Rails, Laravel, etc). MIT, idiomas claros. Útil como ponto de partida.
> - [drona23/claude-token-efficient](https://github.com/drona23/claude-token-efficient) — um único CLAUDE.md focado em reduzir verbosidade do *output* do Claude (corta "Sure!", "Great question!", restate de pergunta, etc). MIT. README honesto sobre o tradeoff (o arquivo carrega input tokens toda sessão; só compensa em alto volume de output). Métricas de stars do repo são suspeitas — leia pela técnica, não pela popularidade.
>
> Consumiu? Faça uma glosa em `02-Glosas/` se quiser destilar mais.
