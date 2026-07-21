---
title: "Evolução da Engenharia de IA"
type: moc
publish: true
tags:
  - evolucao-engenharia-ia
  - ia
  - moc
created: 2026-07-20
updated: 2026-07-20
aliases:
  - Evolução da Engenharia de IA
  - Camadas da Engenharia de IA
  - Prompt Context Loop Graph
  - History of AI Engineering
---

# Evolução da Engenharia de IA

Em dezoito meses, o discurso técnico anunciou a morte de três disciplinas e o nascimento de outras tantas: prompt engineering morreu, context engineering morreu, loop engineering morreu, viva o graph engineering. Quem trabalha com IA em produção precisa decidir, a cada anúncio, se aquilo é uma camada nova de verdade ou o mesmo trabalho com nome novo — e decidir rápido, porque a decisão vira arquitetura.

Este galho é a **historiografia desse capítulo**. Não é a defesa de nenhuma camada, e não é profecia. É o registro de como a engenharia em torno de LLMs se organizou entre 2022 e 2026, com datas, autoria, mecanismo e — em cada nota — o ceticismo que a bolha não conta.

> [!info] O critério que atravessa o galho
> A pergunta que separa camada de rebranding é: **qual é a unidade de design?** A menor coisa que você projeta, versiona e depura. A frase → o fluxo → a janela → o ambiente → o ciclo → a rede. Se a unidade não mudou, o nome mudou sozinho.

> [!warning] Capítulo em curso, não conclusão
> Este galho documenta o estado do campo em **julho de 2026**. Boa parte do material das notas 06 e 07 é discurso quente, de dias atrás, ainda não decantado por evidência. Quando a próxima camada aparecer — e vai — ela entra como nota 09 e o resto continua válido. O que envelhece bem aqui é o critério, não a lista.

## O que este galho NÃO é

Cada camada já tem galho próprio no vault, com a mecânica completa. Aqui o ângulo é exclusivamente historiográfico: **por que** cada camada surgiu quando surgiu, o que ela deslocou, e o que ficou pelo caminho.

| Para a mecânica de… | Vá para |
|---|---|
| técnicas de prompting | [[03-Dominios/Tecnologia/IA/Prompt Engineering/index\|Prompt Engineering]] |
| montagem e compressão de contexto | [[03-Dominios/Tecnologia/IA/Context Engineering/index\|Context Engineering]] |
| eval → diff → ship, champion-challenger | [[03-Dominios/Tecnologia/IA/Improvement Loop/index\|Improvement Loop]] |
| anatomia e arquitetura de agentes | [[03-Dominios/Tecnologia/IA/Anatomia de Agents/index\|Anatomia de Agents]] |
| spec como artefato de entrada | [[03-Dominios/Tecnologia/IA/Spec-Driven Development/index\|Spec-Driven Development]] |
| a vista de cima das camadas de sistema | [[03-Dominios/Tecnologia/IA/AI Engineering Stack/index\|AI Engineering Stack]] |

## As notas

### Fase Iniciado — o critério e o primeiro ciclo completo

- [[03-Dominios/Tecnologia/IA/Evolução da Engenharia de IA/01 - A escada de abstração — qual é a unidade de design\|01 - A escada de abstração]] — o critério que separa camada nova de rebranding, e a linha do tempo completa com datas e autoria. Comece aqui.
- [[03-Dominios/Tecnologia/IA/Evolução da Engenharia de IA/02 - Prompt engineering — o que morreu e o que sobrou\|02 - Prompt engineering]] — o cargo sumiu, a skill triplicou. O mecanismo da morte dos truques de fraseado, e a lição que se repete em toda camada: **absorção não é extinção**.

### Fase Adepto — as camadas do meio

- [[03-Dominios/Tecnologia/IA/Evolução da Engenharia de IA/03 - Flow engineering — o precursor que ninguém cita\|03 - Flow engineering]] — o AlphaCodium já tinha nome para "gerar → testar → corrigir" em janeiro de 2024. A ideia sobreviveu, o nome não. A diferença real entre flow e loop: quem decide a próxima etapa.
- [[03-Dominios/Tecnologia/IA/Evolução da Engenharia de IA/04 - Context e harness — o ambiente vira o produto\|04 - Context e harness]] — o que o agente vê e o que ele pode fazer, duas camadas irmãs. Karpathy, Hashimoto, e a estranheza estrutural de loop engineering aparecer como *sub*-disciplina do harness.
- [[03-Dominios/Tecnologia/IA/Evolução da Engenharia de IA/05 - Loop engineering — o motor de 4 tempos e as 4 traições\|05 - Loop engineering]] — o motor que você já conhece (termostato, dieta, eval loop) e as quatro maneiras de ele te trair: Goodhart, cegueira para o alvo, conflito, decay.

### Fase Magus — a fronteira e a leitura do ciclo

- [[03-Dominios/Tecnologia/IA/Evolução da Engenharia de IA/06 - Graph engineering — a confiabilidade mora nas arestas\|06 - Graph engineering]] — a rede de loops como resposta às quatro traições, o duplo grafo (org vs work), e a pergunta honesta: o que muda num DAG quando os nós são estocásticos?
- [[03-Dominios/Tecnologia/IA/Evolução da Engenharia de IA/07 - Grounded vs ungrounded — tocar a realidade\|07 - Grounded vs ungrounded]] — um grafo internamente perfeito e externamente falso. As três âncoras, e por que este é um corte **transversal** às camadas, não a camada seguinte.
- [[03-Dominios/Tecnologia/IA/Evolução da Engenharia de IA/08 - Hype, ceticismo e mercado — lendo o próximo ciclo\|08 - Hype, ceticismo e mercado]] — a anatomia do ciclo destilada, as perguntas de triagem para a próxima camada anunciada, e o que os dados de mercado realmente dizem.

## A linha do tempo em uma tela

| Camada | Unidade de design | Quando | Marco |
|---|---|---|---|
| Prompt engineering | a frase | 2022–2024 | CoT, few-shot, ToT |
| Flow engineering | o fluxo test-driven | jan/2024 | AlphaCodium (Codium/Qodo) |
| Context engineering | a janela | 2025 | Karpathy: "LLM = CPU, contexto = RAM" |
| Harness engineering | o ambiente executável | 2026 | Mitchell Hashimoto |
| Loop engineering | o ciclo | jun/2026 | Addy Osmani, Peter Steinberger |
| Graph engineering | a rede de loops | jul/2026 | Steinberger, Santiago Valdarrama |

E, atravessando todas elas: **grounded vs ungrounded** — a máquina de melhoria toca a realidade que diz melhorar, ou só a si mesma?

## Como percorrer

> [!tip] Três caminhos
> - **Sequencial (01 → 08)** se quer a história inteira. As notas se referenciam em cadeia: as traições da 05 são respondidas pelas arestas da 06, que são questionadas pela 07.
> - **Direto na 05 e 06** se o que você precisa é decidir arquitetura de agentes agora. Volte para a 01 depois, pelo critério.
> - **01 e 08** se o que você quer é só o método de leitura — como avaliar a próxima camada quando ela for anunciada. São as duas pontas do mesmo argumento.

## Crédito das ilustrações

Os quatro diagramas embutidos nas notas 05, 06 e 07 são de **Carlos E. Perez** ([@IntuitMachine](https://x.com/IntuitMachine)), de um thread publicado em julho de 2026. Eles carregam o argumento do motor de quatro tempos, das quatro traições, das arestas e do corte grounded/ungrounded.
