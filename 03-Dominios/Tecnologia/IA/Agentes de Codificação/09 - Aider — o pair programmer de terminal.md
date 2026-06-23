---
title: "Aider — o pair programmer de terminal"
created: 2026-05-02
updated: 2026-05-02
type: concept
progress: backlog
status: seedling
publish: true
tags:
  - agentes-codificacao
  - ia
  - ferramentas
aliases:
  - Aider
  - Aider chat
  - Terminal pair programmer
---

# Aider — o pair programmer de terminal

> [!abstract] TL;DR
> [[Dicionário de IA#Aider|Aider]] é uma ferramenta open-source (Apache 2.0) de terminal que funciona como pair programmer AI com foco em Git. Cada mudança vira um commit automático com mensagem descritiva. É model-agnostic (traz sua própria API key), suporta edição multi-file, e gera um "repository map" semântico para dar contexto ao LLM. Em 2026, é a escolha preferida de devs seniors que valorizam auditabilidade, controle granular, e independência de vendor.

## O que é

**Aider** é um assistente de codificação CLI que combina:

- **Git-first workflow** — cada edit vira um commit atômico
- **Model agnosticism** — use Claude, GPT, DeepSeek, ou modelos locais via Ollama
- **Repository map** — síntese semântica do codebase (assinaturas, tipos, dependências)
- **Open-source** — código aberto, sem lock-in

## Por que importa

Para devs que querem IA sem abrir mão de controle:

- Cada mudança é um commit — reversível com `git revert`
- Escolha livre de modelo — troque de provider sem trocar de ferramenta
- Transparência total — veja exatamente o que o [[Dicionário de IA#LLM (Large Language Model)|LLM]] vê e o que ele muda

## Como funciona

### Setup

```bash
# Instalar
pip install aider-chat

# Usar com Claude Sonnet
export ANTHROPIC_API_KEY=sk-ant-...
aider --model claude-sonnet-4.6

# Usar com modelo local (Ollama)
aider --model ollama/qwen2.5:14b
```

### Repository map

Aider gera automaticamente um mapa comprimido do repositório:

```
src/
  auth/
    auth.service.ts   - AuthService class: login(email, password), logout(), validateToken(token)
    auth.guard.ts     - AuthGuard: canActivate(context)
    auth.module.ts    - NestModule: imports [JwtModule, UserModule]
  user/
    user.entity.ts    - User class: id, email, name, role, createdAt
    user.service.ts   - UserService: findById(id), findByEmail(email), create(dto)
```

Esse mapa dá contexto estrutural sem enviar o conteúdo completo de cada arquivo.

### Workflow típico

```bash
$ aider src/auth/auth.service.ts src/auth/auth.guard.ts

> Add rate limiting to the login endpoint - max 5 attempts per IP per minute

# Aider gera diffs, aplica, e faz commit:
# "feat(auth): add rate limiting to login - 5 attempts/IP/minute"
```

### Comparativo

| Aspecto              | Aider                      | Claude Code      | Cursor          |
| -------------------- | -------------------------- | ---------------- | --------------- |
| **Licença**          | Apache 2.0                 | Proprietário     | Proprietário    |
| **Git integration**  | ★★★★★ (commit automático)  | ★★★              | ★★              |
| **Model choice**     | ★★★★★ (qualquer modelo)    | ★★ (Claude only) | ★★★★ (vários)   |
| **Agentic autonomy** | ★★★ (pair, não agente)     | ★★★★★            | ★★★★★           |
| **Filosofia**        | Pair programmer controlado | Agente autônomo  | IDE inteligente |

## Quando usar

- Refactoring sistemático com auditoria Git completa
- Projetos que exigem independência de vendor
- Devs que preferem terminal e controle granular
- Quando se quer combinar com modelos locais (DeepSeek, Qwen via Ollama)

## Armadilhas

- **Não é agente autônomo** — Aider é pair programmer, não agente. Não executa comandos nem itera autonomamente como Claude Code.
- **Commits automáticos podem poluir** — em sessões longas, o Git log fica com muitos commits incrementais. Use `git rebase -i` para limpar.
- **Repository map tem limites** — para codebases muito grandes, o mapa pode ficar incompleto. Adicione arquivos relevantes explicitamente.

## Veja também

- [[05 - Claude Code — terminal-first agent]] — alternativa com mais autonomia
- [[10 - OpenCode — o harness open source]] — outro open-source mais agentic
- [[11 - Comparativo — qual ferramenta para qual tarefa]] — decisão entre ferramentas

## Referências

- **Aider** — *Documentation* (aider.chat). Referência oficial.
- **Gauthier, Paul** — *Aider: AI Pair Programming in Your Terminal* (GitHub). Repositório open-source.
