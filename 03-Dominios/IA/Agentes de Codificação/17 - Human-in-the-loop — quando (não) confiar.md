---
title: "Human-in-the-loop — quando (não) confiar"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - agentes-codificacao
  - ia
  - ferramentas
aliases:
  - Human-in-the-loop
  - HITL
  - Supervisão de agentes
---

# Human-in-the-loop — quando (não) confiar

> [!abstract] TL;DR
> Human-in-the-loop (HITL) é o modelo de supervisão onde o humano autoriza ações do [[Dicionário de IA#Agent|agente]] em pontos críticos. Em 2026, a questão não é "sempre supervisionar ou nunca" — é calibrar ONDE no [[Dicionário de IA#agentic loop|loop]] colocar o humano. Ações de leitura são seguras para auto-approve. Edições em código de negócio precisam de review. Ações em produção (deploy, delete, git push) precisam de aprovação explícita SEMPRE. A arte é eliminar approval fatigue sem sacrificar segurança.

## O que é

HITL é um modelo de governança para agentes AI onde:

- **O agente opera autonomamente** na maioria das ações (leitura, análise, planejamento)
- **O humano intervém** em pontos de decisão críticos (edição de código, execução de comandos, deploy)

O espectro vai de "pede permissão para tudo" (seguro mas lento) a "faz tudo sozinho" (rápido mas perigoso).

## Como funciona

### Espectro de autonomia

| Nível             | Descrição                                       | Velocidade | Risco      |
| ----------------- | ----------------------------------------------- | ---------- | ---------- |
| **1 — Manual**    | Humano aprova CADA ação                         | ★          | Mínimo     |
| **2 — Semi-auto** | Auto para reads, manual para writes             | ★★★        | Baixo      |
| **3 — Whitelist** | Auto para ações whitelisted, manual para outras | ★★★★       | Médio      |
| **4 — Full auto** | Tudo auto, com hooks de segurança               | ★★★★★      | Alto       |
| **5 — Headless**  | Sem humano no loop                              | ★★★★★      | Muito alto |

### Configuração prática

```bash
# Claude Code: nível 2 (semi-auto)
claude config set permissions.allow "read_file,list_dir,grep_search,view_file"
claude config set permissions.allow "bash(npm test),bash(npm run lint)"
# Tudo que não está na whitelist pede permissão

# Claude Code: nível 4 (full auto com hooks)
claude config set auto_approve_edits true
# Hook de segurança:
# .claude/hooks.json — bloqueia rm -rf, git push --force
```

### Matriz de risco

| Ação                             | Risco         | Recomendação                   |
| -------------------------------- | ------------- | ------------------------------ |
| `read_file`, `list_dir`, `grep`  | ★ Nenhum      | Auto-approve                   |
| `write_file` (testes)            | ★★ Baixo      | Auto-approve com lint hook     |
| `write_file` (lógica de negócio) | ★★★ Médio     | Review humano                  |
| `write_file` (auth, pagamento)   | ★★★★★ Alto    | Review obrigatório             |
| `bash(npm test)`                 | ★ Nenhum      | Auto-approve                   |
| `bash(npm install)`              | ★★★ Médio     | Review (pode instalar malware) |
| `bash(git push)`                 | ★★★★ Alto     | SEMPRE pedir permissão         |
| `bash(rm -rf)`                   | ★★★★★ Crítico | BLOQUEAR via hook              |
| Deploy                           | ★★★★★ Crítico | SEMPRE humano                  |

### Approval fatigue — o inimigo silencioso

Quando o agente pede permissão para TUDO:

1. Humano começa revisando cuidadosamente
2. Após 20 approvals, começa a aprovar sem ler
3. Após 50, está no automático — rubber stamping
4. A única mudança perigosa da sessão é aprovada sem review

**Solução:** calibre o nível de autonomia para que as interrupções sejam RARAS e SIGNIFICATIVAS. Auto-approve ações seguras para que cada interrupção mereça atenção real.

## Quando usar cada nível

| Contexto                | Nível recomendado              |
| ----------------------- | ------------------------------ |
| Aprendendo a ferramenta | 1 (Manual)                     |
| Prototipagem/spike      | 3-4 (Whitelist/Full auto)      |
| Feature em produção     | 2-3 (Semi-auto/Whitelist)      |
| Infra/deploy/auth       | 1-2 (Manual/Semi-auto)         |
| CI/CD headless          | 5 (Headless) + hooks rigorosos |

## Armadilhas

- **"Sempre manual"** — máxima segurança mas mata a produtividade e causa approval fatigue.
- **"Sempre auto"** — máxima velocidade mas um `rm -rf /` não perdoa.
- **Não configurar hooks** — sem hooks, full auto é roleta russa.
- **Approval fatigue** — mais perigoso que full auto, porque você ACHA que está revisando.

## Veja também

- [[03 - O comprehension gate]] — o review que acontece DEPOIS da aprovação
- [[05 - Claude Code — terminal-first agent]] — configuração de permissions
- [[16 - O loop agentic — plan, act, observe]] — onde no loop o humano entra

## Referências

- **Anthropic** — *Permission System Documentation* (2026). Controle de autonomia.
- **claudefa.st** — *Reducing Approval Fatigue* (2026). Padrões práticos.
