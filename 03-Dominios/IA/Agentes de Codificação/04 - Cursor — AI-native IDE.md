---
title: "Cursor — AI-native IDE"
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
  - Cursor IDE
  - Cursor Composer
  - .cursorrules
---

# Cursor — AI-native IDE

> [!abstract] TL;DR
> [[Dicionário de IA#Cursor|Cursor]] é um fork do VS Code que transforma o editor em um ambiente AI-native — não é uma extensão, é a arquitetura inteira reprojetada para IA. Composer faz edições multi-file coerentes, Agent Mode planeja e executa autonomamente, Background Agents trabalham enquanto você faz outra coisa, e .cursorrules define o "sistema operacional" do AI no seu projeto. Em 2026, é considerado o padrão da indústria para codificação agentic em IDE.

## O que é

**Cursor** é um IDE AI-native baseado no VS Code que integra capacidades de [[Dicionário de IA#LLM (Large Language Model)|LLM]] diretamente na experiência de edição. Diferente de extensões como Copilot que se plugam ao VS Code, Cursor é um fork que controla o editor inteiro — permitindo interações mais profundas entre AI e código.

## Por que importa

Cursor é o IDE onde a maioria dos engenheiros AI-first trabalha em 2026. Saber configurá-lo e usá-lo é equivalente a saber usar o VS Code em 2020 — competência base.

## Como funciona

### Features principais

| Feature                | O que faz                                            | Quando usar                   |
| ---------------------- | ---------------------------------------------------- | ----------------------------- |
| **Tab (autocomplete)** | Completa código inline                               | Digitação diária, boilerplate |
| **Chat**               | Conversa sobre código com contexto do projeto        | Perguntas, debugging          |
| **Composer**           | Edição multi-file coordenada com diffs               | Refactoring, features novas   |
| **Agent Mode**         | Planejamento + execução + iteração autônoma          | Tarefas complexas multi-step  |
| **Background Agents**  | Agentes rodando em background enquanto você trabalha | Tarefas longas, paralelas     |

### Composer — o diferencial

Composer é o que separa Cursor de autocomplete. Em vez de sugerir uma linha, ele:

1. Analisa a instrução em linguagem natural
2. Identifica todos os arquivos afetados
3. Gera diffs coordenados mantendo coerência entre arquivos
4. Apresenta preview para review antes de aplicar

**Exemplo de instrução:**
> "Refatore o módulo de autenticação para usar JWT em vez de sessões. Atualize o middleware, os testes, e a documentação."

O Composer geraria diffs em 5-8 arquivos, mantendo consistência entre o middleware, os handlers, os testes, e os tipos.

### Agent Mode

Agent Mode eleva o Composer para autonomia:

1. **Plan** — analisa a tarefa e propõe um plano
2. **Execute** — implementa o plano gerando código
3. **Run** — executa comandos (testes, lint)
4. **Observe** — analisa resultados
5. **Fix** — corrige problemas e repete

### .cursorrules — configuração essencial

```markdown
# .cursorrules

## Linguagem e estilo
- Use TypeScript strict mode em todos os arquivos
- Prefira functional components com hooks
- Nomeie arquivos com kebab-case

## Padrões
- Use Zod para validação de schemas
- Error handling com Result pattern, não try/catch
- Testes com Vitest, não Jest

## Proibições
- NUNCA delete arquivos de configuração sem confirmação
- NUNCA modifique testes existentes para fazê-los passar
- NUNCA use any em TypeScript
- NUNCA instale dependências sem listar no chat

## Contexto do projeto
- Este é um SaaS Next.js 15 com App Router
- Backend usa tRPC com Drizzle ORM
- Auth via Clerk
```

### Model selection

Cursor permite trocar o modelo base:

| Modelo            | Quando usar                       | Custo |
| ----------------- | --------------------------------- | ----- |
| Claude Sonnet     | Coding diário, equilíbrio         | Médio |
| Claude Opus       | Refactoring complexo, arquitetura | Alto  |
| GPT-4.1           | Alternativa para raciocínio geral | Médio |
| Cursor Small/Fast | Autocomplete rápido               | Baixo |

## Configuração

### Setup inicial recomendado

1. Criar `.cursorrules` na raiz do projeto
2. Configurar `.cursorignore` (equivalente ao .gitignore para contexto AI)
3. Selecionar modelo padrão (Sonnet para maioria)
4. Configurar atalhos de teclado para Composer e Chat

### .cursorignore

```
node_modules/
dist/
build/
.next/
coverage/
*.lock
*.log
```

Exclui diretórios irrelevantes do contexto AI, economizando [[Dicionário de IA#Token|tokens]] e melhorando qualidade.

## Armadilhas

- **Não configurar .cursorrules** — usar Cursor sem rules é como usar um IDE sem settings. O AI vai gerar código no estilo dele, não no seu.
- **Ignorar .cursorignore** — sem ele, o AI pode tentar processar node_modules e desperdiçar tokens em contexto irrelevante.
- **Aceitar tudo do Composer sem review** — Composer é poderoso mas não infalível. Sempre revise os diffs antes de aplicar.
- **Usar Agent Mode para tudo** — para edições simples de 1 arquivo, Chat ou Tab são mais rápidos e baratos.
- **Não trocar de modelo** — usar Opus para autocomplete é desperdício. Use Cursor Small/Fast para tab completion.

## Veja também

- [[05 - Claude Code — terminal-first agent]] — alternativa terminal para quem prefere CLI
- [[07 - Windsurf e Cascade]] — concorrente com proposta de valor em custo
- [[14 - agents.md e configuração de projeto]] — configuração cross-tool

## Referências

- **Cursor** — *Documentation* (cursor.com/docs). Referência oficial.
- **Dev.to** — *Cursor Rules Best Practices 2026*. Guia comunitário de .cursorrules.
