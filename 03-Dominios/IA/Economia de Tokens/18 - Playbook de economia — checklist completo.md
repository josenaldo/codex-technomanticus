---
title: "Playbook de economia — checklist completo"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - economia-tokens
  - ia
  - custos
aliases:
  - Playbook economia tokens
  - Token optimization checklist
---

# Playbook de economia — checklist completo

> [!abstract] TL;DR
> Este é o checklist mestre de economia de tokens. Aplicando todas as técnicas desta trilha, é possível reduzir custos em 60-85% mantendo (ou melhorando) a qualidade. A ordem importa: monitore primeiro, depois aplique as técnicas de maior impacto (caching, pruning, routing), e por fim as de ajuste fino.

## O checklist

### Fase 0: Monitoramento (ANTES de otimizar)

- [ ] Instalar monitoramento (ccusage, Helicone, ou Langfuse)
- [ ] Registrar baseline de custo diário/semanal
- [ ] Identificar TOP 3 categorias de gasto

### Fase 1: Quick wins (impacto imediato)

- [ ] **Prompt caching:** mover conteúdo estático para início do prompt + `cache_control`
- [ ] **Context pruning:** configurar .cursorignore, excluir node_modules/dist/coverage
- [ ] **Higiene de sessão:** usar `/clear` ao trocar de tarefa e `/compact` proativo quando o contexto passar de ~100k
- [ ] **Interface de economia:** instalar **Serena** (redução agressiva) e usar `/statusline` para monitorar uso em tempo real
- [ ] **Respostas concisas:** adicionar instruções de concisão no system prompt
- [ ] **Modelo correto:** usar budget model para autocomplete, mid-tier para coding

### Fase 2: Otimizações estruturais

- [ ] **Compactação de histórico:** ativar/configurar context compaction automática
- [ ] **Filtragem de output:** usar **RTK** (Ex: `rtk git status`) para filtrar saídas verbosas de ferramentas
- [ ] **Sub-agentes eficientes:** delegar para sub-agente `Explore` (read-only) em buscas e `general-purpose` apenas para escrita/lógica
- [ ] **Tool compression:** comprimir descriptions de tools
- [ ] **Thinking budget:** limitar thinking tokens por tipo de tarefa
- [ ] **Retrieval seletivo:** enviar trechos de arquivo (usando offset/limit), não arquivos inteiros
- [ ] **Higiene de projeto:** manter `CLAUDE.md` enxuto e evitar deixar muitos arquivos abertos/sem commit no Git

### Fase 3: Ajuste fino

- [ ] **Batch API:** usar para tarefas assíncronas em volume
- [ ] **Semantic caching:** cachear respostas para perguntas frequentes
- [ ] **Model cascading:** implementar fallback budget → standard → flagship
- [ ] **Orçamento:** definir budget mensal com alertas

### Fase 4: Manutenção contínua

- [ ] Revisar dashboard semanalmente
- [ ] Ajustar budget trimestralmente
- [ ] Atualizar tabela de preços quando providers mudam pricing
- [ ] Aplicar [[21 - Hacks de trincheira — Claude, Gemini e Copilot em 2026|hacks específicos do motor]] em uso
- [ ] Treinar time em práticas de economia

## Impacto acumulado estimado

| Técnica | Redução | Acumulado |
|---------|---------|-----------|
| Baseline (sem otimização) | — | $100/mês |
| + Prompt caching | -40% | $60/mês |
| + Context pruning | -20% | $48/mês |
| + Respostas concisas | -15% | $41/mês |
| + Model routing | -25% | $31/mês |
| + Compactação de histórico | -15% | $26/mês |
| + Thinking budget | -10% | $23/mês |
| **Total** | **~77%** | **$23/mês** |

## Veja também
- Todas as notas desta trilha (01-12) para detalhes de cada técnica
- [[19 - Planos e tiers — Max, Pro, API, Enterprise]]
- [[20 - O futuro — tokens cada vez mais baratos]]

## Referências
- Compilado de todas as referências das notas 01-12 desta trilha.
