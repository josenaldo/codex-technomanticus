---
title: "Onboarding de time — introduzir Claude Code sem caos"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - onboarding
  - time
  - adocao
---

# Onboarding de time — introduzir Claude Code sem caos

> [!abstract] TL;DR
> Introduzir Claude Code num time não é só instalar a CLI — é definir convenções, treinar uso responsável, e estabelecer feedback loops. A adoção falha quando cada dev usa de forma diferente e o agente produz output inconsistente. A adoção tem sucesso quando o time desenvolve hábitos compartilhados: quais skills usar, quando confiar no agente, quando revisar manualmente.

## Os três estágios de adoção

```
1. Indivíduo isolado     → Um dev usa, time não sabe
   ↓
2. Time experimentando   → Vários devs usam, sem padrão
   ↓
3. Time integrado        → Convenções compartilhadas, workflows reproduzíveis
```

A maioria dos times trava no estágio 2 — cada dev tem seu jeito, e o agente vira ruído ao invés de alavanca. Onboarding intencional acelera a transição para o estágio 3.

## Pré-requisitos antes do onboarding

Antes de introduzir Claude Code no time, prepare o ambiente:

1. **CLAUDE.md do projeto** com convenções, arquitetura, comandos
2. **Pelo menos 2-3 skills** que cobrem workflows comuns (review, deploy, debugging)
3. **MCP servers** essenciais configurados (DB staging, GitHub)
4. **Hooks de guardrail** para operações destrutivas
5. **Política de permissões** documentada

Sem isso, o onboarding ensina o uso da ferramenta mas não o uso dentro do projeto.

## Sessão de onboarding (1 hora)

Estrutura sugerida para introduzir o time:

```
1. (10 min) O que é Claude Code e quando faz sentido usar
   - Não é substituto de pensamento
   - É alavanca para tarefas repetitivas e exploratórias

2. (10 min) Demo de uso real no projeto
   - Mostra uma sessão acontecendo
   - Destaca uso de skills do projeto

3. (15 min) Hands-on: cada dev configura
   - Instalação da CLI
   - Setup do .claude/settings.json
   - Configuração das API keys

4. (15 min) Walkthrough das convenções do time
   - Onde fica o CLAUDE.md
   - Quais skills existem e quando usar cada
   - O que nunca deixar o agente fazer

5. (10 min) Q&A e próximos passos
   - Canal de Slack para dúvidas
   - Como reportar problemas com skills
   - Quando trazer feedback à revisão
```

## Documento de onboarding

Crie um documento de referência que novos devs leem antes de usar Claude Code:

```markdown
# Claude Code neste projeto

## Setup
1. Instalar: `npm install -g @anthropic-ai/claude-code`
2. Configurar API key: `export ANTHROPIC_API_KEY=...` (pedir ao tech lead)
3. Clonar o repo — as configurações em `.claude/` vêm com o clone

## Workflows do time
- Para code review: `/review` antes de pedir aprovação no GitHub
- Para implementar feature: `/tdd` + `/convencoes`
- Para debugar bug em produção: `/bug-triage`

## O que o agente pode fazer
[Lista do CLAUDE.md, repetida aqui para visibilidade]

## O que o agente nunca deve fazer
[Lista do CLAUDE.md, repetida aqui]

## Quando NÃO usar
- Decisões arquiteturais críticas — converse com o time primeiro
- PRs urgentes em produção — revisão humana é obrigatória
- Modificação de migrations já aplicadas
- Lógica de domínio que envolve regras de negócio sutis

## Onde pedir ajuda
- Canal #claude-code no Slack
- Tech lead: @nome
- Documentação completa: docs/claude-code/
```

## Workflows compartilhados

A força do time não está em cada dev usar Claude Code — está em todos usarem da mesma forma. Defina e documente workflows:

### Workflow: Review de PR

```markdown
1. Crie o PR no GitHub normalmente
2. Localmente, na branch do PR:
   /review
   Revise o diff contra origin/main
3. Endereça os feedbacks que fazem sentido
4. Marque o PR para review humano só depois disso
```

### Workflow: Implementar feature de issue

```markdown
1. Leia a issue com o time (não pula o entendimento)
2. Em uma branch nova:
   /convencoes
   /tdd
   Implementa a feature descrita na issue #N
3. O agente vai seguir TDD com as convenções do projeto
4. Revise os testes gerados antes de prosseguir
5. Crie o PR e siga o workflow de review acima
```

### Workflow: Debugging de bug em staging

```markdown
1. Reproduza o bug em staging
2. /bug-triage
   Bug observado: [descrição]
   Log do erro: [paste]
3. O agente vai consultar o banco staging via MCP, identificar a causa,
   e propor correção
4. Revise a proposta antes de implementar
```

Workflows escritos no CLAUDE.md ou em `docs/claude-code/workflows.md` garantem reprodutibilidade.

## Feedback loop nas primeiras semanas

Nas primeiras 2-4 semanas, colete feedback ativamente:

- **Daily ou weekly check-in**: o que funcionou, o que não funcionou, surpresas
- **Compartilhar bons prompts**: quando alguém encontra um prompt que funciona bem, compartilhar para o time aprender
- **Identificar skills faltantes**: tarefa repetitiva que o time faz mas o agente não está ajudando → criar skill
- **Identificar skills tóxicas**: skill que o agente segue mas produz resultado ruim → revisar ou remover

## Métricas de adoção saudável

Como saber se a adoção está funcionando?

| Indicador | Bom sinal | Mau sinal |
|-----------|-----------|-----------|
| Uso por dev | Crescente e estável | Cai depois das primeiras semanas |
| Tipos de tarefa | Variedade aumenta com o tempo | Só uso para coisas triviais |
| Skills do projeto | Time adiciona e mantém | Nunca tocadas após criação |
| Reviews de PR | Tempo de review reduz | PRs precisam mais correções pós-merge |
| Qualidade do output | Time confia em cenários definidos | Devs revertem mudanças do agente |

## Anti-padrões comuns

### "Manda o Claude fazer"

Time delega tarefas sem entender o que está sendo feito. O agente vira caixa preta. Sintoma: PRs que ninguém consegue explicar. Correção: revisar a saída antes de aceitar, sempre.

### "O Claude vai pegar"

Time relaxa em qualidade de issue, especificação, ou pensamento prévio assumindo que o agente vai inferir. Sintoma: prompts vagos com resultados inconsistentes. Correção: tratar o agente como um dev junior — quanto melhor o briefing, melhor o resultado.

### Skills paralelas em conflito

Cada dev cria suas próprias skills em `~/.claude/skills/` que duplicam ou contradizem as do projeto. Sintoma: comportamento inconsistente entre devs. Correção: skills do projeto em `.claude/skills/`, revisão obrigatória.

### Sem revisão de output

Time aceita output do agente sem ler. Sintoma: PRs com bugs ou code smells passando despercebidos. Correção: code review humano permanece obrigatório, sempre.

## O papel do tech lead

Em qualquer adoção de Claude Code no time, alguém precisa ser o owner:

- Mantém o CLAUDE.md atualizado
- Revisa skills antes de adicionar ao projeto
- Treina novos devs no setup e workflows
- Coleta feedback e itera nas convenções
- Decide quando uma skill foi superada e deve ser removida

Sem esse papel definido, as convenções degradam rapidamente.

## Armadilhas

**Onboarding apenas técnico**: ensinar a instalar a CLI sem ensinar as convenções do time gera caos. O setup é 20% do onboarding; os 80% restantes são "como usamos aqui".

**Sem CLAUDE.md ao introduzir**: introduzir Claude Code antes de ter convenções escritas é como contratar dev sem onboarding — cada um inventa o próprio jeito.

**Adotar tudo de uma vez**: tentar adotar headless, CI, MCP, skills, hooks ao mesmo tempo sobrecarrega o time. Comece com uso interativo + 1-2 skills + CLAUDE.md básico. Adicione complexidade conforme o time absorve.

**Sem feedback structured**: se ninguém pergunta o que está funcionando, problemas viram folclore — "ah, eu nunca consigo fazer X funcionar, mas o Y consegue". Crie espaço para essa conversa.

## Veja também

- [[03-Dominios/IA/Claude Code/Time e Automação/04 - CLAUDE.md compartilhado|04 - CLAUDE.md compartilhado]] — base da convenção do projeto
- [[03-Dominios/IA/Claude Code/Time e Automação/06 - Segurança organizacional|06 - Segurança organizacional]] — política de permissões
- [[03-Dominios/IA/Claude Code/Skills e MCP/08 - Skills em time|08 - Skills em time]] — manter skills vivas
- [[03-Dominios/IA/Claude Code/Time e Automação/08 - Avaliando qualidade|08 - Avaliando qualidade]] — quando confiar no agente
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — índice do galho
