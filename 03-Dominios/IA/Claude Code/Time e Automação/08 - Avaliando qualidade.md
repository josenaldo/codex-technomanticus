---
title: "Avaliando qualidade do output — quando confiar, quando revisar"
type: concept
progress: backlog
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - qualidade
  - revisao
  - confianca
  - calibracao
---

# Avaliando qualidade do output — quando confiar, quando revisar

> [!abstract] TL;DR
> [[Dicionário de IA#Claude Code|Claude Code]] produz código que vai de excelente a sutilmente quebrado, e o nível de confiança depende do tipo de tarefa, do contexto fornecido, e do quanto você consegue verificar o resultado. Tarefas mecânicas e bem especificadas merecem mais autonomia; mudanças que afetam regra de negócio, dados, ou produção exigem revisão linha a linha. A calibração não é estática — ela melhora à medida que você acumula evidência de onde o agente acerta e onde erra.

## A gradação de confiança

O erro mais comum é tratar Claude Code como confiável ou não confiável de forma binária. A realidade tem nuance:

```
Alta confiança   ─── tarefas mecânicas em contexto bem especificado
                 ─── refatorações com testes existentes que passam
                 ─── geração de boilerplate, documentação, formatação
                 ─── ajustes de tipos, lint, formato

Confiança média  ─── implementação de features pequenas com TDD
                 ─── debugging de bugs com reprodução clara
                 ─── revisão de PRs (catch de erros óbvios)
                 ─── migrations de estrutura simples

Baixa confiança  ─── lógica de domínio com regras de negócio sutis
                 ─── decisões arquiteturais
                 ─── mudanças em código de pagamento, autenticação, dados
                 ─── operações irreversíveis em produção
```

Cada categoria pede um modo de revisão diferente. Tarefa mecânica: olhar o diff e confirmar que parece razoável. Lógica de domínio: ler linha por linha, executar manualmente, validar com testes.

## Sinais de output confiável

Quando o agente produz output que merece confiança, alguns sinais aparecem:

- **Testes incluídos e passando**: o agente escreveu testes que cobrem o novo comportamento, e eles passam
- **Mudanças focadas**: o diff toca só o necessário, sem refatorações paralelas
- **Comentários ausentes onde não precisam**: código autoexplicativo, sem narração redundante
- **Decisões justificadas no chat**: quando o agente fez uma escolha não-óbvia, explicou o porquê
- **Lida com casos de borda**: input vazio, null, lista única, valor extremo
- **Não introduz dependências novas sem motivo**: usa o que já existe no projeto

## Sinais de output suspeito

Inversamente, sinais que pedem revisão atenta:

- **Testes "fake"**: o agente afirma que testou, mas o teste não exercita o caminho relevante
- **Try/catch genérico engolindo erros**: `catch (e) { console.log(e) }` esconde problemas
- **Comentários explicando o óbvio**: sinal de que o agente está preenchendo espaço, não pensando
- **Variáveis renomeadas sem motivo**: refatoração paralela que aumenta área de superfície do PR
- **TODO genérico no meio do código**: "// TODO: handle this case" — vai ficar lá pra sempre
- **Soluções complexas para problemas simples**: três classes onde uma função basta
- **Mocks em testes de integração**: o teste passa mas não valida nada real
- **Dependências novas sem motivo**: adiciona biblioteca para o que poderia ser 5 linhas de código

## Estratégias de verificação por tipo de tarefa

### Refatoração

```
Pergunta-chave: o comportamento mudou?

Verificação:
1. Os testes existentes passam sem modificação?
2. Se testes foram modificados, por quê? (justificativa válida?)
3. O diff visual: faz sentido a mudança?
4. Spot check de 2-3 caminhos críticos manualmente
```

Refatoração com testes existentes que continuam passando é o caso mais seguro de delegação.

### Implementação de feature

```
Pergunta-chave: a feature funciona conforme especificado?

Verificação:
1. Os testes novos cobrem os casos esperados?
2. Casos de borda: lista vazia, input inválido, concorrência?
3. Caminho feliz manual: roda no dev server, exercita a feature
4. Caminho infeliz manual: o que acontece com input ruim?
5. Integração: a feature interage corretamente com o resto do sistema?
```

Tests passing não é suficiente — o [[Dicionário de IA#Agent|agente]] pode ter escrito testes incompletos. Manual testing complementa.

### Bug fix

```
Pergunta-chave: o bug foi corrigido sem introduzir outro?

Verificação:
1. Existe teste de regressão? Roda?
2. O fix é local ou tem efeitos colaterais?
3. A causa raiz está clara, ou é só sintoma sumido?
4. Reproduzir o bug manualmente antes e depois do fix
```

Cuidado especial: agentes às vezes "corrigem" um bug suprimindo a manifestação sem entender a causa. Sempre exija o teste de regressão.

### Lógica de domínio

```
Pergunta-chave: as regras de negócio estão corretas?

Verificação:
1. As regras estão documentadas em algum lugar (PRD, ticket, código existente)?
2. O agente teve acesso a essa documentação?
3. Walk-through linha a linha com a regra em mente
4. Cenários de teste cobrem todas as variações da regra
5. Revisão com alguém do produto/domínio
```

Lógica de domínio sutil é onde Claude Code mais falha — porque o agente não tem contexto que só existe na cabeça das pessoas.

### Mudança em produção

```
Pergunta-chave: o que acontece se isto estiver errado?

Verificação:
1. Existe rollback claro?
2. Mudança pode ser feita em staging primeiro?
3. Existe feature flag para desligar rapidamente?
4. Logs/alertas vão detectar problema rapidamente?
5. Revisão por outra pessoa do time
```

Para mudanças em produção, nunca aceite o output do agente sem revisão humana adicional. Independente de quão bem ele parece estar funcionando localmente.

## Calibrando confiança ao longo do tempo

Mantenha uma noção empírica de onde o agente acerta e onde erra no seu contexto específico:

| Domínio | Notas observadas |
|---------|-----------------|
| Boilerplate (DTOs, controllers) | Quase sempre correto |
| Validação de input | Mete `any` quando aperta — sempre revisar tipos |
| Queries SQL | Boa em CRUD; complica em agregações |
| Testes unitários | Boa estrutura; cobre casos óbvios, falha em borda |
| Concorrência | Frequentemente erra timing/race conditions |
| Configuração de CI | Boa quando há template; inventa quando não há |

Essa tabela é pessoal — cada projeto e estilo de prompt produz padrões diferentes. Vale anotar surpresas (boas e ruins) ao longo das primeiras semanas.

## Gates de qualidade por estágio

Defina quais checks são pré-requisito antes de aceitar output em cada estágio:

### Antes de commitar

- Type check passa
- Lint passa
- Testes locais passam
- Spot check visual do diff

### Antes de abrir PR

- Testes de integração passam
- Manual testing da feature na branch
- Diff revisado linha a linha
- CLAUDE.md ainda reflete o estado do projeto

### Antes de mergear

- CI passa
- Code review humano (não só agente)
- Para mudanças de risco: aprovação adicional do tech lead

### Antes de deploy em produção

- Deploy em staging
- Smoke tests em staging
- Feature flag pronto se aplicável

## Quando NÃO usar Claude Code

Reconhecer os limites é parte da calibração:

- **Quando você não consegue verificar o output**: se você não entende o código que o agente vai produzir, não dá pra revisar. Use para aprender, mas não para mergear cego.
- **Mudanças com requisitos ambíguos**: o agente vai inferir, e a inferência pode estar errada. Esclareça antes.
- **Decisões que envolvem stakeholders**: arquitetura, escolhas de tooling, mudanças de contrato — converse com o time antes.
- **Sistemas críticos sem boa cobertura de teste**: o agente vai parecer correto e ninguém vai pegar o bug até produção.
- **Lógica de domínio extremamente sutil**: regras de imposto, cálculo financeiro, conformidade legal — esses casos pedem expert humano dirigindo.

## O paradoxo da confiança crescente

Conforme você usa Claude Code mais, a tendência natural é confiar mais. Isso pode ser perigoso:

- O agente acerta 95% das vezes, então você começa a só revisar o diff superficialmente
- Mas é nos 5% que o bug entra — e a calibração relaxada permite que passe
- O bug em produção te lembra de revisar mais
- Aí você fica paranoico e revisa tudo linha a linha, perdendo a velocidade

A solução não é confiar mais ou menos — é manter ritual de revisão proporcional ao risco da mudança. Refatoração simples? Diff superficial é OK. Pagamento? Linha a linha sempre.

## Métricas para o time

Se o time quer entender saúde da adoção, alguns indicadores:

- **% de PRs gerados com Claude Code que precisam de correção pós-merge**: alta = revisão fraca
- **Tempo médio de PR review**: deve diminuir com adoção, mas não para zero
- **Cobertura de testes em PRs com Claude Code**: deve manter ou melhorar
- **Bugs em produção atribuídos a mudanças geradas pelo agente**: tracking simples descobre padrões
- **Confiança auto-relatada do time**: pergunte em retro: "você confia no output do agente quando revisa?"

## Armadilhas

**Confiar porque os testes passam**: testes podem ser superficiais. Verifique se cobrem o que importa.

**Revisar pouco porque "o agente faz bem"**: viés de confirmação. Você lembra das vezes que acertou, esquece das que precisou corrigir.

**Revisar tudo porque "não confio no agente"**: o oposto é igualmente custoso. Você perde a alavanca da ferramenta.

**Tratar revisão como formalidade**: passar o olho sem entender o diff não é revisão — é teatro de revisão.

**Não documentar padrões de erro**: se o agente sempre comete o mesmo tipo de erro no seu projeto, isso vai pro CLAUDE.md como restrição.

**Esperar perfeição**: Claude Code não substitui pensamento; complementa. Mesmo quando funciona, você precisa entender o resultado.

## Veja também

- [[03-Dominios/IA/Claude Code/Time e Automação/04 - CLAUDE.md compartilhado|04 - CLAUDE.md compartilhado]] — convenções que ajudam o agente a acertar
- [[03-Dominios/IA/Claude Code/Time e Automação/06 - Segurança organizacional|06 - Segurança organizacional]] — limites que reduzem risco
- [[03-Dominios/IA/Claude Code/Time e Automação/07 - Onboarding de time|07 - Onboarding de time]] — como o time desenvolve calibração compartilhada
- [[03-Dominios/IA/Claude Code/Workflows/05 - Code review|05 - Code review]] — usar o próprio agente para revisar
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — índice do galho
