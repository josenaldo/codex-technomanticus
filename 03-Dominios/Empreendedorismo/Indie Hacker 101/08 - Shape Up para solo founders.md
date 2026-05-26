---
title: "Shape Up para solo founders"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - indie-hacker
  - empreendedorismo
  - produto
  - shape-up
  - metodologia
aliases:
  - Shape Up
  - Appetite
  - Fixed time variable scope
---

# Shape Up para solo founders

> [!abstract] TL;DR
> Shape Up é a metodologia de produto do Basecamp: ciclos fixos de 6 semanas com escopo variável, seguidos de 2 semanas de cooldown. Para solo founders, a adaptação principal é: ciclos menores (2 semanas), shaping como pensamento individual (não reunião de equipe), e betting table como decisão pessoal semanal. O conceito mais poderoso é **appetite** — em vez de estimar "quanto tempo leva?", defina "quanto tempo estou disposto a gastar nisso?" e corte escopo para caber. Shape Up é o antídoto mais prático contra scope creep.

## O que é

Shape Up foi desenvolvido por Ryan Singer no Basecamp e publicado como livro gratuito em basecamp.com/shapeup. É uma metodologia de desenvolvimento de produto que rejeita tanto o waterfall clássico quanto o Agile baseado em sprints e backlogs infinitos.

Os princípios centrais:

1. **Fixed time, variable scope.** O tempo é fixo (6 semanas no Basecamp; 2 semanas para solo founder). O escopo varia para caber no tempo. Se não cabe, corta — não estende.
2. **Appetite, not estimates.** Em vez de perguntar "quanto tempo leva para construir X?", pergunte "quanto tempo estou disposto a gastar em X?". A resposta define o que é possível construir nesse tempo.
3. **Shaping before building.** Antes de codificar, pense no problema, nos limites, nos riscos ("rabbit holes") e no que explicitamente NÃO será feito ("no-gos"). Esse pensamento é o "shaping".
4. **Betting, not backlogging.** Não mantenha um backlog infinito de ideias. A cada ciclo, escolha ("aposte") no que importa agora. Se uma ideia não foi escolhida, descarte-a — se ainda for relevante, ela volta naturalmente.
5. **Cooldown.** Após cada ciclo de build, 1-2 semanas sem compromisso: bugs, housekeeping, exploração livre. Previne burnout.

## Por que importa

O problema mais prático do solo founder não é técnico — é gerencial: **como decidir no que trabalhar, quanto tempo gastar, e quando parar?**

Sem metodologia, o padrão é: começa feature A → distrai com feature B → descobre bug C → volta para A → percebe que D é urgente → 3 meses depois, nada está completo.

Shape Up resolve isso com um framework simples que funciona para 1 pessoa tão bem quanto para 10.

## Como funciona

### Adaptação para solo founder

| Conceito original (Basecamp, 6 pessoas) | Adaptação solo (1 pessoa) |
|----------------------------------------|--------------------------|
| Ciclo de 6 semanas | **Ciclo de 2 semanas** (manter urgência) |
| Cooldown de 2 semanas | **Cooldown de 2-3 dias** |
| Shaping por seniors em sala | **Shaping como exercício escrito solo** (30-60 min) |
| Betting table com CEO + CTO | **Decisão pessoal semanal** (15 min) |
| Time de 2-3 devs por projeto | **Você** |

### 1. Shaping (antes de cada ciclo)

Escreva um mini-pitch para cada trabalho candidato ao próximo ciclo. Formato:

```markdown
## [Nome do trabalho]

**Problema:** O que está errado / faltando
**Appetite:** Quanto tempo estou disposto a gastar (ex: 3 dias, 1 semana, 2 semanas)
**Solução rough:** Como resolver (esboço, não spec detalhada)
**Rabbit holes:** Riscos que podem explodir o tempo
**No-gos:** O que explicitamente NÃO fazer neste ciclo
```

O shaping não precisa ser longo. 5-10 linhas por pitch bastam. O valor está no ato de pensar nos limites antes de codificar.

### 2. Betting (início do ciclo)

Olhe todos os pitches shaped e escolha 1-2 para o ciclo de 2 semanas. Critérios:

- Qual tem maior impacto no usuário/receita?
- Qual cabe no appetite definido?
- Qual tem menos rabbit holes?

**Descarte o resto.** Não vá para um backlog. Se a ideia for realmente boa, ela volta.

### 3. Building (durante o ciclo)

- Trabalhe apenas nos pitches escolhidos
- Se descobrir que o escopo não cabe, **corte escopo** — não estenda tempo
- Use hill charts mentais: "estou subindo a colina (descobrindo) ou descendo (executando)?"
- Não aceite interrupções externas ("feature request urgente de usuário") — vão para o próximo shaping

### 4. Cooldown (após o ciclo)

2-3 dias sem compromisso de delivery:
- Corrigir bugs encontrados no ciclo
- Atualizar docs/README
- Explorar ideia nova sem pressão
- Descansar (sério — burnout mata mais indie hackers que concorrência)

### O conceito de appetite na prática

Appetite é a inversão do estimativa:

| Pergunta tradicional | Pergunta Shape Up |
|---------------------|------------------|
| "Quanto tempo leva para fazer dark mode?" | "Estou disposto a gastar 2 dias em dark mode?" |
| "Resposta: 3 semanas" → aceita | "Se leva mais que 2 dias, não vale agora" → corta |

Isso muda fundamentalmente a relação com escopo. Em vez de construir o que "precisa", você constrói o que cabe. O resultado é: features menores, mais focadas, entregues com mais frequência.

## Na prática

Um ciclo típico de 2 semanas para solo founder:

| Dia | Atividade |
|-----|-----------|
| **Seg (início)** | Shaping + betting (1h). Escolher 1-2 trabalhos. |
| **Seg-Sex (semana 1)** | Building. Foco nos trabalhos escolhidos. |
| **Seg-Qua (semana 2)** | Building. Cortar escopo se necessário. |
| **Qui-Sex (semana 2)** | Cooldown. Bugs, docs, descanso. |
| **Dom** | Review: o que aprendeu? O que muda no próximo ciclo? |

## Armadilhas

- **Tratar Shape Up como Agile com nome diferente.** Shape Up não tem sprints, não tem backlog, não tem daily standup. Se você está mantendo um backlog, está fazendo Agile, não Shape Up.

- **Não respeitar o appetite.** Se definiu "2 dias para dark mode" e levou 5, o problema não é a estimativa — é o escopo. Corte, não estenda.

- **Pular o cooldown.** "Não preciso de cooldown, estou empolgado." Burnout não avisa. O cooldown é prevenção, não recompensa.

- **Shaping demais.** O pitch não é um PRD de 10 páginas. São 5-10 linhas que definem problema, solução rough, limites e riscos. Se está escrevendo mais, está fazendo spec, não shaping.

- **Nunca descartar ideias.** O backlog infinito é a antítese do Shape Up. Se uma ideia não foi escolhida em 2 ciclos seguidos, provavelmente não é importante o suficiente. Delete.

## Veja também

- [[07 - O que é realmente um MVP]] — escopo mínimo para validação
- [[02 - O conceito de enough — Company of One]] — por que não construir tudo
- [[09 - Stack de custo zero]] — infraestrutura para o ciclo

## Referências

- **Singer, Ryan** — *Shape Up: Stop Running in Circles and Ship Work that Matters*. Livro gratuito: basecamp.com/shapeup. O framework completo com exemplos do Basecamp.
- **Fried, Jason & DHH** — *Rework* e *It Doesn't Have to Be Crazy at Work*. Filosofia de trabalho calmo que fundamenta o Shape Up.
