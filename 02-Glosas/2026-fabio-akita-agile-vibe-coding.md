---
title: "Fabio Akita: Minha Experiência com Agile Vibe Coding"
aliases: ["Fabio Akita: Minha Experiência com Agile Vibe Coding"]
source: https://www.youtube.com/watch?v=U3bZavG8qQY
author: Tropical on Rails
site: YouTube
channel: Tropical on Rails
video_id: U3bZavG8qQY
duration: "58:50"
published: 2026-05-28
read: 2026-06-28
type: glosa
progress: backlog
status: lido
tags: [vibe-coding, ia, llm, agentes, engenharia-de-software]
lang: pt
publish: false
---

# Fabio Akita: Minha Experiência com Agile Vibe Coding — Tropical on Rails

> [!info] Vídeo
> ![https://www.youtube.com/watch?v=U3bZavG8qQY](https://www.youtube.com/watch?v=U3bZavG8qQY) 
> · 58:50 · Tropical on Rails
## TL;DR

Akita relata sua maratona de dois meses com Claude Code — 500 horas, 15+ projetos, ~300 mil linhas geradas — e propõe o "agile vibe coding" como síntese entre fundamentos técnicos sólidos e a nova era de agentes. O argumento central: a IA funciona como um acelerador multiplicador da sua competência atual, para o bem ou para o mal, então quem não domina os fundamentos continua sem resultado — apenas dez vezes mais rápido.

## Pontos-chave

- **A IA reflete quem você é**: profissionais sólidos são acelerados 5–10x; profissionais medíocres acumulam débito técnico na mesma proporção — o acelerador não tem juízo de valor.
- **LLMs são loot boxes**: geradores de texto estocásticos treinados para concordar com o usuário, não para ter razão; o modelo nunca é feito para dar a resposta certa, mas para te bajular — compreender isso é pré-requisito para usá-los bem.
- **A virada aconteceu em novembro de 2025**: a chegada do GPT-5.1 e do Opus 4.5 marcou o corte entre "promissor" e "viável em produção" para agentes de codificação.
- **Trate o Claude Code como programador júnior**: você é tech lead, gerente de produto e QA — não editor de arquivos; o método PILOTA (Planejar, Investigar, Lapidar, Operar, Testar, Ajustar) exige interação contínua, não um prompt único.
- **O CLAUDE.md é memória instrucional evolutiva**: adicione regras aos poucos à medida que você identifica padrões de erro; não comece com um arquivão de instruções que gasta contexto à toa.
- **Benchmark de 30 modelos**: apenas Claude Opus, GPT-X High e talvez Qwen 3.5-35B são práticos para trabalho real; DeepSeek tem falhas estruturais em prompt caching e tool calling — não use.
- **Senior que não sabe ensinar não é senior**: se você não consegue fazer uma IA fazer o que quer, provavelmente não conseguiria gerenciar um colega júnior; a IA explicita suas limitações de comunicação.

## Momentos-chave

- [00:00] — Introdução: contexto pós-YouTube, Akita no Tropical on Rails
- [01:36] — O pânico coletivo sobre IA substituir empregos (continuação da bolha de 2022)
- [05:27] — Caso Asami Arts: artista que vendia arte gerada por IA como sua própria
- [10:45] — LLMs explicados como "loot boxes" estocásticos
- [12:03] — Princípio central: "a IA reflete quem você é"
- [15:00] — Linha do tempo: 2025 como ano dos agentes; novembro como ponto de virada
- [16:06] — A maratona: 15–16 projetos, 500 horas, ~300 mil linhas de código
- [20:11] — O que 300 mil linhas significa em termos de projeto (pequeno a médio, ~2,5 anos solo)
- [24:24] — Mudança de mindset: "Let it go" do editor de texto, trate o LLM como júnior
- [25:54] — Método PILOTA apresentado
- [26:37] — Uso evolutivo do CLAUDE.md como memória de instruções do projeto
- [28:48] — Benchmark de 30 modelos open source e comerciais
- [35:15] — Por que DeepSeek não presta: sem prompt caching, tool calling fraco, deep thinking ruim
- [39:22] — Pricing: pare de economizar token; assinatura >> pay-per-token
- [46:21] — Senior que não sabe ensinar não é senior
- [48:27] — Só vai sobreviver quem souber fazer engenharia de verdade
- [51:27] — Demo ElevenLabs: 146 vídeos dublados em inglês em 3 dias por ~$2.000
- [58:27] — Conclusão: faça uma imersão de uma semana, "faça bullying com a IA"

## Citações

> "a IA reflete quem você é. Ela vai acelerar você. Então, se você for um excelente programador, um excelente artista, um excelente profissional, seja lá o que for, ele vai te acelerar dez vezes. Agora, se você for um péssimo profissional, um péssimo programador, um péssimo desenhista, ele vai acelerar o seu código ruim dez vezes." — [12:03]

> "na prática, uma LLM é um loot box. É um gerador de texto com parâmetros aleatórios, aonde a cada novo token que ele calcula, vem de um pool de tokens com probabilidades, aonde ele sorteia um, baseado em parâmetros como top K, top P, temperatura, etc." — [10:45]

> "Senior que não sabe ensinar não é senior. Sabe por quê? Porque se for só pra fazer código, o GPT faz. E vai me custar vinte dólares. E eu não preciso olhar pra sua cara feia." — [46:21]

> "Se você não tá conseguindo ter resultados com IA, é porque você não sabe gerenciar ninguém. Se você não consegue nem fazer uma IA fazer o que você quer, como que você vai gerenciar uma pessoa na sua equipe?" — [30:51]

> "para de tentar economizar token. É uma perda de tempo. Gaste todos os tokens aproveitando agora que ele tá hiper subsidiado e tá hiper barato." — [39:22]

## Meu comentário

> [!info] Qual a diferença entre mecanica de gacha e loot boxes nos games?
> Gacha e loot boxes são mecanismos de monetização por aleatoriedade, mas com diferenças importantes:
> 
> **Loot Box**
> 
> - Você compra uma caixa e recebe itens aleatórios
> - Cada abertura é independente — sem memória do histórico
> - Geralmente sem garantia de progressão para um item específico
> - Exemplo: caixas de CS:GO, pacotes de FIFA Ultimate Team
> 
> **Gacha**
> 
> - Derivado das máquinas "gachapon" japonesas
> - Tem sistemas de progressão embutidos:
> - Pity system: após N pulls sem o item raro, a probabilidade aumenta (ou o item é garantido)
> - Soft pity / hard pity: dois limiares de progressão
> - Frequentemente vem com banners temáticos (personagens/itens por tempo limitado)
> - Exemplo: Genshin Impact, Honkai Star Rail, FGO
> 
> **Diferença central**
> 
|                      | Loot Box  | Gacha                  |
| -------------------- | --------- | ---------------------- |
| Progressão garantida | Raramente | Sim (pity)             |
| Contexto cultural    | Ocidente  | Japão/Ásia             |
| Itens limitados      | Às vezes  | Quase sempre           |
| Pull individual      | Sim       | Sim + multi-pull (x10) |
> 
> Na prática, gacha é um subconjunto mais sofisticado do conceito de loot box — com mais camadas de design para manter o jogador engajado (e gastando) por mais tempo, por meio da ilusão de controle que o pity system oferece.
> 
> ❯ Então LLM é mais parecido com gacha do que com loot boxes, certo?
> 
> Boa analogia, mas é mais sutil do que parece.
> 
> **No nível bruto (token sampling), é mais loot box:**
> - Cada token é sorteado de uma distribuição de probabilidade independentemente
> - Sem "memória de falhas" — o modelo não sabe que já errou antes
> - `temperature=0` seria uma loot box com 100% de drop rate no item mais provável
> 
> **Mas o prompting cria um efeito gacha:**
> - Few-shot examples = você está manipulando o pool de drops antes de abrir a caixa
> - Chain-of-thought = construir progressivamente em direção ao output desejado, como acumular pity
> - System prompt = definir o banner (restringir o espaço de possibilidades)
> - RAG = injetar o item raro diretamente no contexto antes do sorteio
> 
> **A diferença filosófica real:**
> 
> No gacha, o sistema tem estado interno que evolui com suas ações (pity counter). No LLM, você é quem carrega o estado — no contexto. O "pity" não está no modelo, está na sua engenharia de prompt.
> 
> Então talvez a melhor analogia seja: LLM é uma loot box onde você pode hackear a tabela de drops em tempo real escrevendo o prompt certo. Gacha seria se o modelo aprendesse com suas interações anteriores e ficasse "mais próximo" do que você quer ao longo do tempo — que é o que o fine-tuning faz.

## Ver também

- [[02 - Vibe coding vs engenharia disciplinada]] <!-- sugestão; validar -->
- [[01 - O problema do vibe coding em produção]] <!-- sugestão; validar -->
- [[05 - Claude Code — terminal-first agent]] <!-- sugestão; validar -->
- [[14 - agents.md e configuração de projeto]] <!-- sugestão; validar -->
