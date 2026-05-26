---
title: "STAR Method"
created: 2026-04-01
updated: 2026-04-22
type: concept
status: seedling
tags:
  - entrevista
  - behavioral
  - inglês
  - star
  - pitch
publish: true
---

# STAR Method

Framework para estruturar respostas em entrevistas behavioral — Situation, Task, Action, Result.

## O que é

STAR é um framework para contar histórias profissionais de forma estruturada e impactante. Cada resposta tem 4 partes que guiam o entrevistador pela sua experiência.

## Como funciona

### Time-box rígido

| Etapa      | % do tempo | ~segundos | Foco                                       |
| ---------- | ---------- | --------- | ------------------------------------------ |
| Situation  | 10%        | ~12s      | Mínimo contexto pro stake fazer sentido    |
| Task       | 10%        | ~12s      | Responsabilidade isolada + maior restrição |
| **Action** | **60%**    | **~72s**  | **O coração — Power Verbs e "why"**        |
| Result     | 20%        | ~24s      | Outcome de negócio com dados duros         |

> [!warning] Tempo total alvo: **2 minutos**.
> Se passar disso, está vendendo demais o contexto e de menos a execução. Recrutadores globais cortam por tempo, não por mérito.

### S — Situation (Contexto)

Onde e quando? Qual era o cenário? Mantenha breve (2-3 frases).

> "At Muvz, I joined a project to modernize a major newspaper's legacy system. The existing architecture was a Java EJB monolith, and the project was already 3 months behind schedule."

- ✅ Nomeie a crise de negócio específica. Mantenha **sob 15 segundos**.
- ❌ Não conte a história inteira da empresa nem liste todo framework usado.

### T — Task (Desafio)

O que precisava ser feito? Qual era o seu papel específico?

> "My task was to lead the migration from the monolith to a microservices architecture using Spring Boot and Kafka, while mentoring the team on modern practices."

- ✅ Declare a responsabilidade isolada ("As the sole / lead developer..."). Destaque a restrição (deadline, equipe júnior, codebase caótico).
- ❌ Não misture Task com Action. Não reclame de devs anteriores.

### A — Action (O que você fez)

O que VOCÊ fez? Seja específico sobre suas ações, decisões e por que.

> "I started by mapping the bounded contexts using Event Storming to identify natural service boundaries. Then I led the team in building 5 Spring Boot microservices, introduced Kafka for event-driven communication between services, and implemented Hexagonal Architecture to keep the business logic independent from infrastructure."

- ✅ Use "**I**", não "we" — você está vendendo sua execução.
- ✅ Foque no **"why" por trás do "what"** (decisão arquitetural, trade-off).
- ✅ Aplique [[#Power Verbs|Power Verbs]] no lugar de Junior English.
- ❌ Sem technobabble linha-por-linha. Sem perder-se em bugs menores.

### R — Result (Resultado)

Qual foi o impacto? Use números sempre que possível.

> "We improved system performance by over 40%, eliminated the 3-month delay, and delivered on time. The team adopted DDD and Hexagonal Architecture as standard practices for future projects."

- ✅ Dados duros sempre ("3,000+ tests", "1h → 2min", "+40% performance").
- ✅ Amarre o resultado **de volta à crise** mencionada no Situation.
- ❌ Não termine sem outcome concreto. Não seja modesto — **own the impact**.

## Quando usar

- **Behavioral questions clássicas**: "Tell me about a time when...", "Describe a situation where...", "Give me an example of..."
- **Perguntas técnicas com contexto humano**: "How did you handle a tough trade-off?", "Walk me through a hard decision."
- **Cover letters e LinkedIn About** que destacam realizações concretas.
- **1-on-1 com gestor / performance review** — vender impacto de ciclo.
- **Auto-avaliação** — escrever histórias STAR força clareza sobre o próprio impacto.

### Liderança técnica — Kafka na Muvz

- **S:** Projeto de modernização de sistema legado para um grande jornal. Monolito Java EJB.
- **T:** Liderar migração para microserviços e introduzir mensageria assíncrona.
- **A:** Event Storming para mapear bounded contexts. 5 microserviços Spring Boot. Proof-of-concept com Kafka. Setup do cluster Kafka em Kubernetes com DevOps. Mentoria da equipe.
- **R:** Performance +40%. 3 meses de atraso eliminados. Equipe adotou DDD e Hexagonal como padrão.

### CI/CD — MedEspecialista

- **S:** Plataforma de educação médica com deploys manuais e lentos.
- **T:** Automatizar pipeline de entrega e modernizar a stack frontend.
- **A:** GitHub Actions para CI/CD completo. Migração de CRA para Vite + TypeScript. TanStack Query para data fetching. BullMQ para processamento assíncrono.
- **R:** Deploy de 1 hora → 2 minutos. Trabalho manual reduzido em 97%. Lead time de 2 semanas → 1 semana.

### Mentoria — Arquitetura na Muvz

- **S:** Equipe de desenvolvedores trabalhando sem padrões consistentes.
- **T:** Elevar o nível técnico da equipe mantendo produtividade.
- **A:** Code reviews focados em princípios (SOLID, DDD). Sessões de pair programming. Documentação de decisões arquiteturais. Exemplos práticos no código.
- **R:** Equipe internalizou práticas de arquitetura limpa. Menos bugs. Código mais consistente.

## Armadilhas comuns

- **Situation muito longa:** máximo 2-3 frases / ~15 segundos. O entrevistador quer saber o que VOCÊ fez.
- **Misturar Task com Action:** primeiro o objetivo, depois a execução — não os dois embolados.
- **Action vaga:** "eu trabalhei com a equipe para resolver" — especifique SUA contribuição.
- **Action sem "why":** descrever o que fez sem justificativa de design vira recital de tarefas, não de senioridade.
- **Sem números no Result:** "ficou melhor" vs "melhorou 40%". Números são mais impactantes.
- **"We" no lugar de "I":** dilui ownership e sinaliza dependência. Você está vendendo SUA execução.
- **Junior English:** "I did", "I made", "I helped", "I worked on" → vocabulário de executor, não de senior. Ver [[#Power Verbs|Power Verbs]].
- **Technobabble:** explicar lógica de código linha-a-linha em entrevista comportamental é bandeira vermelha.
- **Esquecer o aprendizado:** para histórias de fracasso, adicione o que aprendeu (STAR + L).
- **Não preparar histórias de fracasso:** recrutadores experientes pedem; sem exemplo de falha + aprendizado, parece performance.

## Power Verbs

Substituir Junior English por verbos de senioridade. Lista canônica:

| Categoria       | Power Verb       | Em vez de          | Exemplo                                                        |
| --------------- | ---------------- | ------------------ | -------------------------------------------------------------- |
| Execution       | **Orchestrated** | I worked on        | "I orchestrated the migration to a decoupled architecture."    |
| Leadership      | **Spearheaded**  | I helped lead      | "I spearheaded the adoption of Clean Architecture."            |
| Strategy        | **Leveraged**    | I used             | "I leveraged AI agents to accelerate the TDD workflow."        |
| Risk Management | **Mitigated**    | I avoided problems | "I mitigated deployment risks with a robust CI/CD pipeline."   |
| Problem Solving | **Overhauled**   | I rewrote          | "I overhauled the 'Big Ball of Mud' into a scalable platform." |
| Optimization    | **Streamlined**  | I improved         | "I streamlined the development lifecycle."                     |

> [!tip] Sinônimos para variar
> Coordinated, Synchronized · Led, Pioneered · Utilized, Capitalized on · Alleviated, Reduced · Revamped, Rebuilt · Optimized, Simplified.

## How to explain in English

"I structure my behavioral answers using STAR. Let me give you an example:

**Situation:** At Muvz, I joined a project to modernize a major newspaper's legacy Java EJB system. The project was already three months behind schedule.

**Task:** I was responsible for leading the migration to a microservices architecture and getting the project back on track.

**Action:** I started with Event Storming to identify bounded contexts and natural service boundaries. Then I built a Kafka proof-of-concept to demonstrate event-driven communication. We split the monolith into five Spring Boot microservices following Hexagonal Architecture. I also mentored the team on DDD and SOLID principles through code reviews and pair programming.

**Result:** We improved performance by over 40%, eliminated the three-month delay, and delivered on time. The team adopted these architectural practices as their standard going forward."

### Key vocabulary

- situação → situation / context
- tarefa → task / challenge
- ação → action: o que você fez
- resultado → result / outcome / impact
- impacto mensurável → measurable impact
- lições aprendidas → lessons learned

## Veja também

- [[Behavioral Questions]] — categorias de perguntas e como se preparar
- [[Communicating Trade-offs]] — como explicar decisões técnicas sob pressão
