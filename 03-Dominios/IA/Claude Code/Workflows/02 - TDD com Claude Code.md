---
title: "TDD com Claude Code — test-first workflow"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - workflows
  - tdd
  - testes
---

# TDD com Claude Code — test-first workflow

> [!abstract] TL;DR
> TDD com Claude Code funciona melhor quando você instrui o agente a seguir o ciclo Red/Green/Refactor explicitamente — não quando você espera que ele faça isso sozinho. O padrão: peça os testes primeiro, rode-os para confirmar falha, depois peça a implementação. O agente tende a escrever testes e implementação juntos se não for guiado.

## O problema padrão

Sem instrução explícita, o agente tende a:

1. Ler o código existente
2. Implementar a feature
3. Escrever testes para a implementação que acabou de criar

Isso é test-after, não TDD. Os testes ficam enviesados pela implementação — testam o que o código faz, não o que deveria fazer.

## O ciclo correto com Claude Code

### Red — escreva o teste que falha

```
você: "Escreva os testes para a função calculateTax(amount, category)
      em tests/services/taxCalculator.test.ts.

      Requisitos:
      - Produtos eletrônicos: 15% de imposto
      - Alimentos: 0% de imposto
      - Outros: 10% de imposto
      - amount negativo deve lançar InvalidAmountError
      - amount zero deve retornar 0

      NÃO implemente calculateTax ainda. Só os testes."
```

Depois de o agente escrever os testes:

```
você: "Rode npm test tests/services/taxCalculator.test.ts e
      confirme que todos os testes estão falhando."
```

Confirmar a falha é crucial — se algum teste passa sem implementação, ele está testando algo errado.

### Green — implementação mínima

```
você: "Agora implemente calculateTax em src/services/taxCalculator.ts
      para fazer todos os testes passarem. Implementação mínima —
      não adicione nada além do que os testes exigem."
```

Verificação:

```
você: "Rode npm test tests/services/taxCalculator.test.ts"
```

### Refactor — melhore sem quebrar

```
você: "Os testes estão passando. Refatore calculateTax para:
      - usar um mapa de categoria → alíquota em vez de if/else
      - extrair a validação de amount para validateAmount()
      Rode os testes depois para confirmar que continuam passando."
```

## Prompt de TDD em um bloco

Para quem prefere dar a instrução completa de uma vez:

```
"Implemente calculateTax(amount: number, category: Category): number
seguindo TDD:

1. Escreva os testes em tests/services/taxCalculator.test.ts cobrindo:
   - Eletrônicos: 15%, Alimentos: 0%, Outros: 10%
   - amount negativo → InvalidAmountError
   - amount zero → retorna 0

2. Rode os testes e confirme que falham.

3. Implemente src/services/taxCalculator.ts com o mínimo para passar.

4. Rode os testes e confirme que passam.

5. Refatore se necessário, rodando os testes novamente."
```

## Quando TDD com Claude Code brilha

**Feature nova com requisitos claros**: você sabe o comportamento esperado, o agente implementa. Os testes são a especificação executável.

**Bug fix**: escreva primeiro um teste que reproduz o bug. Depois peça ao agente para corrigir o bug até o teste passar. Garante que o bug não volta.

```
"Temos um bug: calculateTax lança TypeError quando category é undefined
em vez de usar a alíquota padrão (10%).

1. Escreva um teste que reproduz esse bug.
2. Rode o teste e confirme que falha.
3. Corrija calculateTax.
4. Confirme que o teste passa."
```

**Refactoring com confiança**: a suite de testes existente garante que o comportamento não mudou. Instrua o agente a não modificar os testes durante o refactor.

## Cobertura guiada

Depois de TDD, peça análise de cobertura:

```
"Rode npm test -- --coverage para src/services/taxCalculator.ts.
Identifique branches não cobertos e adicione testes para eles."
```

## Armadilhas

**"Escreva testes e implemente"**: o agente escreve tudo junto, sem o ciclo Red/Green. Separe explicitamente as etapas.

**Não confirmar a falha (Red)**: se o agente escreve um teste que já passa (porque testou a função existente, por exemplo), você não descobriu um comportamento — confirmou uma implementação existente.

**Testes que testam detalhes de implementação**: "deve chamar o método getRate() internamente" não é um teste de comportamento. Corrija: "deve retornar 15 para amount=100 com category='electronics'".

**Over-specification nos testes**: pedir ao agente para escrever testes para cada variação possível antes de implementar atrasa o ciclo. Comece com os casos críticos, adicione edge cases no refactor.

## Veja também

- [[03-Dominios/IA/Claude Code/Workflows/01 - Plan Mode|01 - Plan Mode]] — planejar a estrutura de testes antes de escrever
- [[03-Dominios/IA/Claude Code/Workflows/03 - Refactoring pesado|03 - Refactoring pesado]] — TDD como rede de segurança em refactors
- [[03-Dominios/IA/Claude Code/Workflows/09 - Prompting para Claude Code|09 - Prompting para Claude Code]] — precisão no prompt para TDD funcionar
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows]] — índice do galho
