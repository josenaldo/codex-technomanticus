---
title: "Debugging complexo — diagnosticar, não só corrigir"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - workflows
  - debugging
  - troubleshooting
---

# Debugging complexo — diagnosticar, não só corrigir

> [!abstract] TL;DR
> O erro mais comum ao debugar com Claude Code é pedir a correção antes de ter a causa raiz. O agente aplica um fix plausível que resolve o sintoma mas não o problema real. O padrão correto: descreva o comportamento observado vs. esperado, deixe o agente formar e testar hipóteses, confirme a causa antes de aceitar o fix.

## O anti-padrão

```
você: "O endpoint POST /api/orders está retornando 500.
      Corrija."

agente: [olha o stack trace, adiciona try/catch em volta do código,
        o erro para de aparecer]

resultado: o erro foi silenciado, não corrigido.
```

## O padrão correto

### 1. Descreva o comportamento, não o fix desejado

```
"O endpoint POST /api/orders retorna 500 com esta payload:
{
  'customerId': 'c123',
  'items': [{'productId': 'p456', 'quantity': 2}]
}

Comportamento esperado: criar o pedido e retornar 201 com o id.
Comportamento observado: 500 Internal Server Error.

Stack trace nos logs:
TypeError: Cannot read properties of undefined (reading 'price')
at calculateTotal (src/services/pricing.ts:47)

Analise a causa raiz antes de sugerir qualquer fix."
```

### 2. Hipóteses e evidências

Instrue o agente a trabalhar como detetive:

```
"Antes de corrigir, forme hipóteses sobre por que `price` seria
undefined. Para cada hipótese, indique qual evidência confirmaria
ou descartaria. Depois adicione logging para coletar essas
evidências."
```

Agente:
```
Hipóteses:
1. productId 'p456' não existe no banco → price vem como undefined
   Confirmar: logar o resultado da query getProduct('p456')

2. getProduct retorna o produto mas sem o campo price
   Confirmar: logar os campos do objeto retornado

3. Race condition: produto existe mas foi deletado entre o
   fetch e o cálculo
   Confirmar: verificar se há soft-delete em produtos

Adicionando logging temporário para coletar evidências...
```

### 3. Coletar evidências antes de corrigir

```
"Adicione o logging de diagnóstico. Depois vou reproduzir o erro
e te mostrar o output dos logs. Não modifique a lógica ainda."
```

Depois de reproduzir:
```
"Output dos logs:
getProduct('p456') retornou: { id: 'p456', name: 'Monitor' }
— sem campo 'price'

Com isso, qual hipótese é confirmada e qual o fix correto?"
```

### 4. Fix direcionado

Com a causa confirmada:
```
agente: "Hipótese 2 confirmada: getProduct não está retornando
o campo price. O fix correto é atualizar a query SQL em
src/db/queries/products.ts para incluir o campo price no SELECT.

Fix:"
```

## Debugging com testes

A abordagem mais robusta: escreva um teste que reproduz o bug antes de corrigir.

```
"Antes de corrigir, escreva um teste em tests/services/pricing.test.ts
que reproduz o bug: calculateTotal com um produto que tem price=undefined
deve lançar ProductPriceError, não TypeError.

1. Escreva o teste.
2. Rode-o para confirmar que falha (e que falha pelo motivo certo).
3. Corrija o bug.
4. Confirme que o teste passa."
```

Benefício: o teste vira documentação do bug e prevenção de regressão.

## Bugs intermitentes

Para bugs que não acontecem toda vez:

```
"O bug acontece ~20% das requisições sob carga. Não tenho stack
trace consistente. Suspeito de race condition ou problema de
conexão com o banco.

Estratégia:
1. Adicione logging com timestamp e request ID em cada etapa
   de OrderService.createOrder()
2. Adicione métricas de tempo de resposta do banco
3. Identifique se há chamadas concorrentes ao mesmo recurso

Não corrija ainda — preciso de dados para confirmar a causa."
```

## Debugging com contexto insuficiente

Quando você não tem o stack trace completo:

```
"Não tenho o stack trace — o erro acontece apenas em produção
e os logs estão incompletos.

Com base nos sintomas (500 no POST /api/orders, apenas quando
o pedido tem mais de 10 itens), quais são as 3 causas mais
prováveis? Para cada uma, quais logs adicionaríamos para
confirmar?"
```

## Armadilhas

**Dar o fix direto sem diagnóstico**: `"adicione null check"` pode resolver o TypeError mas não explica por que price é undefined. O bug voltará de outra forma.

**Stack trace sem contexto**: mostrar apenas a linha do erro sem o estado do programa (o que foi passado, o que foi buscado no banco) deixa o agente adivinhando.

**Corrigir o sintoma mais imediato**: `Cannot read properties of undefined` — o agente adiciona `if (product?.price)`. O erro some, mas pedidos sem preço são processados silenciosamente.

**Sessão de debugging sem commits**: se o debugging gerar adição de logging, commite como `debug: add temporary logging for order creation bug`. Fácil de reverter depois.

## Veja também

- [[03-Dominios/IA/Claude Code/Workflows/02 - TDD com Claude Code|02 - TDD com Claude Code]] — teste que reproduz o bug antes do fix
- [[03-Dominios/IA/Claude Code/Workflows/09 - Prompting para Claude Code|09 - Prompting para Claude Code]] — descrever o problema com precisão
- [[03-Dominios/IA/Claude Code/Mental Model/08 - Como o agente decide|08 - Como o agente decide]] — por que o agente escolhe o fix errado sem diagnóstico
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows]] — índice do galho
