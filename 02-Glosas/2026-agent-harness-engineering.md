---
title: "Agent Harness Engineering"
aliases: ["Agent Harness Engineering"]
source: https://addyosmani.com/blog/agent-harness-engineering/
author: Addy Osmani
site: AddyOsmani.com
published: 2026-04-19
read: 2026-05-26
type: glosa
progress: backlog
status: lido
tags: [agent-harness, coding-agents, harness-engineering, agents-md, ai-development]
lang: en
publish: false
---

# Agent Harness Engineering — Addy Osmani

## TL;DR

Um agente de coding é o modelo *mais* tudo que se constrói ao redor dele — o **harness**. Osmani argumenta que tratar essa scaffolding (prompts, ferramentas, políticas de contexto, hooks, sandboxes, subagentes, loops de feedback, caminhos de recuperação) como um artefato real, endurecido a cada erro do agente, importa mais que a escolha do modelo: um modelo decente com um ótimo harness vence um ótimo modelo com um harness ruim.

## Pontos-chave

- **Agente = Modelo + Harness.** O harness é todo código, configuração e lógica de execução que não é o modelo: system prompts, `CLAUDE.md`/`AGENTS.md`, skills, ferramentas e MCP servers, infra (filesystem, sandbox, browser), orquestração, hooks e observabilidade. Um modelo bruto vira agente quando um harness lhe dá estado, execução de ferramentas, loops de feedback e restrições executáveis.
- **O "skill issue reframe":** harness engineering rejeita culpar o modelo pelas falhas. Elas costumam ser legíveis e endereçáveis no harness — não conhecia uma convenção? adiciona ao `AGENTS.md`; rodou comando destrutivo? cria um hook que bloqueia; se perdeu em tarefa longa? divide em planejador e executor. O gap entre o que os modelos conseguem e o que você os vê fazendo é, em grande parte, um gap de harness.
- **A catraca (ratchet):** todo erro vira regra permanente. Você só adiciona restrições *depois* de ver falhas reais — cada linha de um bom `AGENTS.md` deveria ser rastreável até algo específico que deu errado.
- **Working backwards:** parta do comportamento desejado para o design do componente. Se você não consegue nomear o comportamento que um componente existe para entregar, ele provavelmente não deveria estar lá. Componentes típicos: filesystem/Git (estado durável), bash (ferramenta geral), sandboxes, memória/busca (aprendizado contínuo), compressão de contexto, skills com divulgação progressiva, Ralph Loops (horizonte longo), hooks (enforcement) e `AGENTS.md` (rulebook).
- **Harnesses não encolhem, se movem:** melhorias do modelo não tornam o harness obsoleto — mudam *onde* a scaffolding é necessária. Cada componente codifica uma suposição sobre o que o modelo não consegue fazer sozinho; quando o modelo melhora nisso, o componente sai. Há um loop de feedback: primitivas úteis descobertas no harness são padronizadas, entram no treino da próxima geração e o modelo seguinte fica melhor em usá-las.
- **Harness-as-a-Service:** a indústria migra de "construir sobre LLM APIs" (que dão uma *completion*) para "construir sobre harness APIs" (que dão um *runtime*) — Claude Agent SDK, Codex SDK, OpenAI Agents SDK. O default passa a ser escolher um framework de harness, configurá-lo e investir esforço em design de prompt e ferramentas de domínio.
- **Para onde vai:** os agentes de coding top se parecem mais entre si do que seus modelos subjacentes — os padrões de harness estão convergindo. Problemas abertos: orquestrar muitos agentes em paralelo, agentes que analisam os próprios traces para corrigir falhas de harness, e harnesses que montam ferramentas *just-in-time* — ponto em que o harness deixa de ser config estático e começa a parecer um compilador.

## Citações

> "A decent model with a great harness beats a great model with a bad harness."

> "Agent = Model + Harness. If you're not the model, you're the harness." — Viv Trivedy

> "Every line in a good `AGENTS.md` should be traceable back to a specific thing that went wrong."

> "Every component in a harness encodes an assumption about what the model can't do on its own."

> "Success is silent, failures are verbose." — HumanLayer

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

-
