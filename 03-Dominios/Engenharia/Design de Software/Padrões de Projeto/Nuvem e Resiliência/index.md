---
title: "Nuvem e Resiliência"
created: 2026-07-31
updated: 2026-07-31
type: moc
status: evergreen
publish: true
tags:
  - moc
  - design-de-software
  - resiliencia
  - cloud
  - falhas
aliases:
  - Nuvem e Resiliência
  - Cloud Design Patterns
  - Padrões de resiliência
  - Stability patterns
  - Galho - Nuvem e Resiliência
---

# Nuvem e Resiliência

> [!abstract] TL;DR
> Os padrões que administram a **falha parcial** — o estado que só existe em sistemas distribuídos, onde
> o sistema não está no ar nem fora dele, e sim *meio* no ar. Sexta e **última** família do galho-pai
> [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/index|Padrões de Projeto]]. O inimigo não
> é a dependência que cai: é a que fica **lenta**, porque a lentidão retém seus recursos até você parar
> também. A lente aqui é o trade-off explícito: **todo padrão de resiliência é uma escolha sobre o que
> sacrificar para não cair inteiro — e sobre quem paga a conta**.

## Sobre esta família

Catálogo de consulta, com notas autocontidas e **Armadilhas** pesando no *quando não usar*.

**Esta é a família mais coberta do vault, e escrevê-la foi decisão deliberada** — um catálogo de padrões
precisa ter uma entrada para "Circuit Breaker", não um ponteiro. Por isso **toda nota abre declarando o
recorte**: o que ela trata, e para onde ir atrás de escala, afinação ou serviço gerenciado.

| Galho | Pergunta que responde |
| --- | --- |
| [[03-Dominios/Engenharia/Arquitetura/System Design/3 - Padrões recorrentes/index\|System Design]] | *quanto aguenta?* — escala, números, a resposta de entrevista |
| [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/index\|Operação]] | *como tunar e operar?* — thresholds, orçamento, mesh, teste |
| [[03-Dominios/Tecnologia/Cloud/20 - Resiliência e continuidade/index\|Cloud]] | *qual serviço faz isso?* — HA, multi-region, DR |
| [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index\|Arqueologia]] | *como migrar com isso?* — Strangler Fig e ACL como método |
| **Esta família** | ***o que se sacrifica, e quem paga?*** |

## Iniciado — falhar bem: os fundamentos

1. [[01 - Panorama da resiliência]] — falha parcial e cascata; o mapa dos padrões e a soma dos sacrifícios.
2. [[02 - Timeout]] — o default infinito é a configuração que derruba sistemas; a versão adulta é o prazo propagado.
3. [[03 - Retry]] — o único padrão que **piora** o incidente quando errado; backoff, jitter e orçamento.
4. [[04 - Circuit Breaker]] — parar de bater numa porta que não abre; a aposta e seus dois erros opostos.
5. [[05 - Bulkhead]] — o acoplamento não está no código, está no recurso compartilhado.

## Adepto — conter e degradar

6. [[06 - Fallback e degradação graciosa]] — a pergunta que os outros não respondem, e que é de produto.
7. [[07 - Rate Limiting e Load Shedding]] — os dois modos de dizer não: por cota e por pressão.
8. [[08 - Cache-Aside]] — cache quente é defesa, cache frio é dívida que vence de uma vez.
9. [[09 - Health Endpoint Monitoring]] — liveness × readiness; o erro é semântico, não de código.
10. [[10 - Leader Election]] — quando redundância é o problema; lease, split-brain e fencing token.

## Magus — topologia, fronteira e migração

11. [[11 - Ambassador + Sidecar]] — tirar a resiliência do código; o argumento real é poliglota e legado.
12. [[12 - Gatekeeper + Valet Key]] — interpor onde se decide, sair da frente onde se transporta.
13. [[13 - Anti-Corruption Layer + Strangler Fig]] — conviver com o legado enquanto ele morre.
14. [[14 - Escolher o padrão de resiliência (capstone)]] — **fecha a família e o galho-pai**: mapa por sintoma, quem paga cada conta, ordem de composição, e a síntese das seis famílias.

> [!tip] Atalho para a hora do incidente
> A [[14 - Escolher o padrão de resiliência (capstone)|nota 14]] começa com uma tabela **sintoma → padrão**
> ("a dependência está lenta", "uma funcionalidade opcional derrubou uma essencial", "um job roda N vezes
> numa frota de N") e traz a **ordem de composição** — timeout dentro de retry dentro de breaker dentro
> de bulkhead — que é o que evita as três somas que causam incidentes.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Nuvem e Resiliência"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/index|Padrões de Projeto]] — o galho-pai e as seis famílias.
- [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/06 - Resiliência operacional|Resiliência operacional]] — a mesma matéria pela ótica de quem opera.
- [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Arquitetura de Eventos/index|Arquitetura de Eventos]] — a família anterior.
- [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index|Arqueologia e Restauração de Software]] — o método de migração por trás da nota 13.
