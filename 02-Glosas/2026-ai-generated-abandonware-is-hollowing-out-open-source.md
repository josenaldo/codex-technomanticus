---
title: "AI-generated abandonware is hollowing out open source"
aliases: ["AI-generated abandonware is hollowing out open source"]
source: https://leaddev.com/software-quality/ai-generated-abandonware-is-hollowing-out-open-source
author: Charles Humble
site: LeadDev
published: 2026-05-20
read: 2026-05-25
type: glosa
progress: backlog
status: lido
tags: [open-source, ia-generativa, abandonware, manutencao-software, sustentabilidade-oss]
lang: en
publish: false
---

# AI-generated abandonware is hollowing out open source — Charles Humble

## TL;DR

A IA generativa derrubou a barreira para publicar software, gerando uma enxurrada de abandonware de baixa qualidade. Pior: os workflows com IA curto-circuitam os loops de engajamento (leitura de docs, fóruns, pull requests) que sustentam economicamente o open source — secando tráfego, receita e novos mantenedores, ao mesmo tempo em que soterram os mantenedores atuais em "AI slop".

## Pontos-chave

- Abandonware sempre existiu, mas a IA agrava o problema: tornou trivial transformar qualquer ideia passageira em software ("created fast is abandoned fast") e tende a gerar código difícil de manter.
- O autor identifica três forças simultâneas: (1) temos menos apego a código que não escrevemos, (2) código de IA feito sem cuidado é difícil de manter, e (3) a IA quebra silenciosamente o modelo econômico do open source.
- Dados do OSSRA 2026 (Black Duck, 947 codebases): 93% das bases contêm componentes sem atividade de desenvolvimento nos últimos 2 anos e só 7% rodam a versão mais recente — o problema dos "zombie components", que vira risco de segurança composto.
- O paper "Vibe Coding Kills Open Source" (Koren, Békés, Hinz, Lohmann, jan/2026) mostra que agentes montam pacotes sem ler docs nem participar de fóruns, curto-circuitando o loop de engajamento que dá retorno aos mantenedores (reputação, consultoria, receita, contribuidores).
- Evidências do colapso: Tailwind CSS teve tráfego de docs caindo ~40% desde 2023 e receita ~80%; o Stack Overflow caiu ~25% em seis meses após o ChatGPT.
- Sobrecarga dos mantenedores: o curl recebeu 37 submissões de "AI slop" em 2025 (contra 2 em 2023) sem um único relatório de segurança válido; o Electron viu o dobro de propostas, boa parte ruído gerado por IA.
- Para líderes de engenharia: avaliar histórico de commits e bus factor (não só estrelas), auditar a árvore de dependências, e nomear explicitamente nas políticas de review o uso de IA sem revisão humana antes de submeter contribuições.

## Citações

> "The barrier to shipping software has collapsed. With AI code generation, any fleeting idea can become a reality almost instantly. But there's a catch: software that is created fast is often abandoned fast."

> "A staggering 93% of codebases contained components with no development activity in the last two years."

> "Together, these patterns suggest that AI mediation can divert interaction away from the surfaces where OSS projects monetize and recruit contributors."

> "We still have not seen a single valid security report done with AI help."

> "When everyone can build, the scarce resource is maintainers. That scarcity was already real before AI made it worse. The question now is whether the industry will treat it as the infrastructure problem it is, or wait for the next Log4j to remind us."

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

-
