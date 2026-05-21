---
title: "Skills de processo vs skills de domínio"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - skills
  - processo
  - dominio
  - classificacao
---

# Skills de processo vs skills de domínio

> [!abstract] TL;DR
> Processo = como fazer. Domínio = o que é. Skills de processo ensinam o agente a seguir um workflow (TDD, code review, debugging). Skills de domínio ensinam o agente sobre o contexto do projeto (arquitetura, convenções, regras de negócio). A distinção importa porque processo e domínio têm ciclos de vida, invocação e manutenção diferentes.

## A distinção fundamental

**Skills de processo** ensinam o agente *como fazer* algo:
- "Para implementar uma feature, siga: teste → implementação → refactor"
- "Para revisar código, verifique: segurança, performance, legibilidade, testes"
- "Para debugar, comece pela reprodução mínima"

**Skills de domínio** ensinam o agente *o que é* algo no contexto do projeto:
- "Este projeto usa domain-driven design. Entidades ficam em `src/domain/`, serviços em `src/application/`"
- "A tabela `orders` usa soft delete — nunca DELETE, sempre `deleted_at = NOW()`"
- "O módulo de pagamentos usa filas assíncronas para tudo acima de R$ 1000"

## Quando usar cada tipo

### Use skill de processo quando:

- O workflow tem passos definidos que o agente deveria seguir em sequência
- A tarefa se repete com o mesmo padrão (toda feature segue o mesmo ciclo)
- O processo é transferível para outros projetos com ajuste mínimo
- Você quer garantir que certas verificações sempre aconteçam (o agente não "esquece" o processo)

Exemplos de skills de processo boas:
```
tdd.md          — red/green/refactor com commits por fase
code-review.md  — checklist de revisão estruturado
debugging.md    — metodologia de isolamento de bugs
deploy.md       — checklist de verificação antes de push
```

### Use skill de domínio quando:

- O agente precisa de contexto que não está óbvio no código
- Há convenções não-padrão que o agente violaria sem instrução
- Regras de negócio críticas precisam ser respeitadas
- A arquitetura tem decisões que parecem erradas sem o histórico

Exemplos de skills de domínio boas:
```
arquitetura.md      — mapa dos módulos e responsabilidades
convencoes.md       — padrões de nomenclatura, organização de arquivos
regras-negocio.md   — invariantes do domínio que não podem ser violadas
stack.md            — versões, bibliotecas preferidas, o que evitar
```

## Ciclos de vida diferentes

**Processo**: muda quando o time decide mudar como trabalha. Muda raramente — uma vez que o TDD workflow funciona, ele permanece estável por meses.

**Domínio**: muda quando o projeto muda. Toda vez que a arquitetura evolui, uma nova regra de negócio surge, ou uma convenção é adotada, a skill de domínio precisa ser atualizada. Perde valor rapidamente se não for mantida.

## Combinações comuns

Processo e domínio frequentemente trabalham juntos:

```
/tdd → agente segue o processo de TDD
/convencoes → agente entende as convenções do projeto antes de escrever código
```

Você pode invocar múltiplas skills na mesma sessão:
```
/convencoes
/tdd
Implementa o serviço de notificações
```

## Exemplo: skill de processo

```markdown
---
name: tdd
description: Guia o agente através do ciclo TDD — red, green, refactor com commits por fase
metadata:
  type: process
  tags: [tdd, testing]
---

# TDD — Test-Driven Development

## Ciclo obrigatório

Para cada unidade de comportamento novo:

1. **Red**: Escreva o teste que falha primeiro. Rode e confirme que falha pelo motivo certo.
2. **Green**: Escreva o mínimo de código para o teste passar. Sem otimizar.
3. **Refactor**: Melhore o código mantendo os testes verdes. Commit após cada refactor.

## Regras

- Nunca escreva código de implementação sem um teste falhando primeiro
- O teste deve falhar pela razão certa (não por erro de sintaxe)
- Commit ao final de cada ciclo completo
```

## Exemplo: skill de domínio

```markdown
---
name: arquitetura-pedidos
description: Arquitetura do módulo de pedidos — onde fica cada coisa e regras de integridade
metadata:
  type: domain
  tags: [orders, architecture, domain]
---

# Módulo de Pedidos — Arquitetura

## Estrutura de diretórios

- `src/domain/orders/` — entidades e regras de domínio (sem dependências externas)
- `src/application/orders/` — use cases, orquestra domínio + infra
- `src/infra/orders/` — repositórios, adaptadores de banco

## Invariantes críticas

- Um pedido não pode ir de CANCELADO para qualquer outro estado
- `total_amount` é sempre calculado — nunca salvo diretamente do input do usuário
- Todo item de pedido deve ter `product_id` válido verificado antes de inserir
```

## Armadilhas

**Misturar os dois tipos numa skill**: uma skill que explica a arquitetura E define o processo de desenvolvimento é difícil de manter e o agente tende a priorizar as últimas instruções lidas.

**Skill de domínio desatualizada**: é pior do que não ter skill — o agente vai seguir convencoes que o projeto abandonou. Skills de domínio precisam de owner e revisão periódica.

**Skill de processo muito rígida**: se o processo tem muitas exceções, o agente vai travar tentando segui-lo. Inclua "quando pular esta etapa" explicitamente.

## Veja também

- [[03-Dominios/IA/Claude Code/Skills e MCP/01 - Anatomia de uma skill|01 - Anatomia de uma skill]] — estrutura e frontmatter
- [[03-Dominios/IA/Claude Code/Skills e MCP/03 - Criar sua primeira skill|03 - Criar sua primeira skill]] — walkthrough com exemplos reais
- [[03-Dominios/IA/Claude Code/Skills e MCP/08 - Skills em time|08 - Skills em time]] — manutenção de skills em equipe
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — índice do galho
