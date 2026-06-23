---
title: "Modelo de Maturidade AI - Steve Yegge"
created: 2026-05-05
updated: 2026-05-06
type: concept
status: growing
progress: in_progress
tags:
  - IA
  - EngenhariaDeSoftware
  - Carreira
  - Produtividade
publish: true
---
# Modelo de Maturidade AI - Steve Yegge

O modelo de maturidade de Steve Yegge (ex-Google, ex-Amazon, Sourcegraph) descreve a evolução da relação entre engenheiros de software e IA generativa: de rejeição defensiva, passando por autocomplete e chat, até workflows agênticos onde o humano especifica intenção, valida qualidade e coordena execução.

O ponto central não é que "a IA substitui programadores", mas que o locus do trabalho muda. O desenvolvedor deixa de ser principalmente operador de sintaxe e passa a ser designer de problemas, curador de contexto, avaliador de qualidade e orquestrador de sistemas parcialmente autônomos.

> [!important] Correção de leitura
> A nota inicial tratava o framework como 8 níveis numerados de 0 a 7. Em *Welcome to Gas Town*, Yegge apresenta a escala como **8 estágios numerados de 1 a 8**. A estrutura abaixo preserva o espírito da versão anterior, mas corrige a numeração e explicita melhor as transições.

## Tese

Yegge argumenta que a indústria está entrando numa fase em que a produtividade diferencial entre desenvolvedores não depende só de "saber programar", mas de saber **programar através de IA**. O programador maduro não terceiriza julgamento; ele terceiriza trabalho mecânico, exploração inicial, geração de alternativas e execução controlada.

Esse modelo conversa com três mudanças maiores:

- **De edição para direção:** o valor migra de escrever cada linha para descrever comportamento, restrições, testes e arquitetura.
- **De prompt para contexto:** o resultado depende menos de frases mágicas e mais de arquivos, testes, documentação, histórico, convenções e artefatos que o agente consegue ler.
- **De assistente para agente:** a IA deixa de apenas responder e passa a navegar no repositório, chamar ferramentas, rodar testes, modificar arquivos e iterar.

## Genealogia do Argumento

Yegge desenvolveu a tese em uma sequência de posts:

- **The Death of the Stubborn Developer**: alerta contra o desenvolvedor que rejeita IA por orgulho, identidade profissional ou apego ao modo antigo de trabalhar.
- **Revenge of the Junior Developer**: inverte a narrativa de que IA mata juniors; juniors adaptáveis podem ganhar alavancagem rapidamente porque têm menos identidade presa ao velho workflow.
- **Welcome to Gas Town**: apresenta a escala de maturidade em 8 estágios e descreve a passagem de chat/autocomplete para workflows agenticos.
- **Welcome to Gas City**: expande a visão para um ecossistema maior de desenvolvimento mediado por IA, no qual tools, agents, memória, contexto e infraestrutura moldam a nova prática.

## Os 8 Estágios

### Estágio 1: O Cético

O desenvolvedor vê IA como hype, brinquedo, risco jurídico ou ameaça ao ofício. Pode até ter bons argumentos sobre alucinação, segurança e qualidade, mas usa esses riscos como justificativa para não experimentar.

**Sinal típico:** "isso só serve para código ruim".

**Limite:** a crítica pode estar correta em casos específicos, mas sem prática real ela não vira discernimento; vira distância.

### Estágio 2: O Usuário de Autocomplete

A IA aparece como sugestão inline no editor. O fluxo mental ainda é tradicional: o humano decide a próxima linha, a IA acelera digitação e boilerplate.

**Ferramentas típicas:** GitHub Copilot em modo completion, autocomplete do Cursor, sugestões de IDE.

**Ganho:** reduz fricção em código local, nomes, blocos repetitivos e APIs familiares.

**Limite:** melhora velocidade de digitação, mas não muda muito a unidade de trabalho.

### Estágio 3: O Chat como Stack Overflow

O desenvolvedor usa chat para tirar dúvidas, gerar snippets, explicar erros e comparar abordagens. A IA vira um mecanismo de consulta interativo.

**Sinal típico:** "explique esse erro", "como faço X em framework Y?", "me dê um exemplo".

**Ganho:** acelera aprendizado e reduz tempo de busca.

**Limite:** o contexto do projeto ainda fica majoritariamente fora da conversa. O humano copia, cola, adapta e integra manualmente.

> [!warning] A Grande Fenda
> A transição crítica é entre usar IA como **oráculo** e usá-la como **executor delegado**. Antes da fenda, você pede respostas. Depois dela, você define tarefas, critérios e contexto.

### Estágio 4: O Delegador de Código

O desenvolvedor começa a pedir unidades completas de código: funções, testes, componentes, scripts, migrações pequenas. Ainda há muito micromanagement, mas a IA já produz artefatos que entram no repositório.

**Sinal típico:** "implemente essa função", "escreva os testes para esse caso", "refatore esse bloco".

**Ganho:** a unidade de delegação passa de linha/snippet para tarefa pequena.

**Limite:** sem contexto suficiente, a IA tende a produzir código plausível porém desalinhado com convenções locais.

### Estágio 5: O Diretor por Especificação

O desenvolvedor muda o centro do trabalho: em vez de pedir implementação diretamente, descreve comportamento, invariantes, casos de teste, interfaces e critérios de aceite.

**Prática-chave:** [[03-Dominios/IA/Spec-Driven Development/index|Spec-Driven Development]] e testes como contrato executável.

**Sinal típico:** "a feature deve passar estes testes", "preserve estes invariantes", "não altere este contrato público".

**Ganho:** a IA recebe um alvo verificável, e o humano pode avaliar resultado por comportamento, não por leitura linha a linha.

**Limite:** especificações ruins geram automação ruim. O estágio exige clareza de produto e arquitetura.

### Estágio 6: O Operador de Agente

A IA ganha acesso ao repositório e a ferramentas: ler arquivos, editar, rodar testes, investigar falhas, consultar docs, produzir diffs. O desenvolvedor deixa de interagir apenas por chat e passa a conduzir um [[Dicionário de IA#agentic loop|loop agentico]].

**Ferramentas típicas:** [[Dicionário de IA#Claude Code|Claude Code]], [[Dicionário de IA#Cursor|Cursor]] agent mode, GitHub Copilot Agents, Codex CLI, [[Dicionário de IA#Aider|Aider]], OpenCode.

**Conexões internas:** [[03-Dominios/IA/Agentes de Codificação/index|Agentes de Codificação]], [[03-Dominios/IA/Anatomia de Agents/index|Anatomia de Agents]], [[03-Dominios/IA/MCP/index|MCP]].

**Ganho:** o agente pode fechar o ciclo `planejar -> agir -> observar -> corrigir`.

**Limite:** a autonomia amplia tanto produtividade quanto blast radius. Permissões, sandboxing, revisão e testes deixam de ser opcionais.

### Estágio 7: O Orquestrador Multi-Agent

O desenvolvedor coordena múltiplos agentes, modelos ou sessões em paralelo: um investiga, outro implementa, outro revisa, outro escreve testes, outro atualiza documentação.

**Sinal típico:** dividir trabalho por ownership de arquivos, módulos ou hipóteses independentes.

**Ganho:** paralelismo cognitivo e operacional. O humano age como tech lead de trabalhadores digitais.

**Limite:** sem contratos claros, agentes entram em conflito, duplicam trabalho ou geram mudanças incompatíveis.

### Estágio 8: O Arquiteto de Sistemas AI-Native

O foco principal passa a ser desenhar o sistema de trabalho: contexto persistente, documentação viva, specs, avaliações, guardrails, memória, permissões, pipelines de revisão, métricas e integração com ferramentas.

**Sinal típico:** o repositório é organizado para ser legível tanto por humanos quanto por agentes.

**Ganho:** a equipe cria um ambiente em que agentes conseguem trabalhar com previsibilidade.

**Limite:** este estágio exige senioridade real. Quando o humano não entende arquitetura, segurança e produto, ele não consegue avaliar a produção da IA.

## Mapa Resumido

| Estágio | Papel da IA | Papel do humano | Unidade de trabalho |
| --- | --- | --- | --- |
| 1 | Ameaça ou hype | Rejeitar | Nenhuma |
| 2 | Autocomplete | Escrever código | Linha |
| 3 | Chat de consulta | Perguntar e adaptar | Snippet |
| 4 | Gerador de código | Delegar pequenas tarefas | Função/teste/componente |
| 5 | Executor guiado por spec | Definir comportamento | Feature pequena |
| 6 | Agente com ferramentas | Conduzir loop agentico | Issue/refactor/debug |
| 7 | Múltiplos agentes | Coordenar e integrar | Workstream paralelo |
| 8 | Substrato operacional | Arquitetar o sistema de trabalho | Organização inteira |

## O Que Muda na Engenharia

### 1. Expertise fica mais importante, não menos

Quanto mais você delega execução, mais precisa saber avaliar resultado. A IA reduz o custo de produzir código, mas aumenta o custo relativo de:

- definir o problema correto;
- reconhecer código plausível porém errado;
- proteger invariantes arquiteturais;
- decidir quando refazer em vez de remendar;
- saber quais testes e checks são evidência suficiente.

Esse é o paradoxo do modelo: iniciantes ganham velocidade, mas senioridade vira o gargalo de qualidade.

### 2. Testes viram linguagem de delegação

Em estágios altos, testes não são só rede de segurança. Eles são uma forma de escrever instruções executáveis para humanos e agentes.

Um bom teste:

- reduz ambiguidade;
- impede regressões invisíveis;
- permite que o agente se auto-corrija;
- torna revisão humana mais objetiva;
- cria memória persistente do comportamento esperado.

Ver [[03-Dominios/IA/Spec-Driven Development/index|Spec-Driven Development]] e [[03-Dominios/IA/Segurança e Guardrails/09 - Testes imutáveis — a barreira que o agente não pode reescrever|Testes imutáveis — a barreira que o agente não pode reescrever]].

### 3. Context engineering substitui prompt heroico

O prompt isolado perde importância quando o agente trabalha em codebase real. O que importa é o pacote completo de contexto:

- `README`, `AGENTS.md`, `CLAUDE.md`, docs de arquitetura;
- issues com escopo claro;
- testes e fixtures;
- ADRs e decisões registradas;
- exemplos de código canônico;
- scripts de verificação;
- permissões e limites operacionais.

Ver [[03-Dominios/IA/Context Engineering/index|Context Engineering]].

### 4. Code review muda de natureza

Revisar código AI-generated não é apenas procurar estilo ruim. É validar uma cadeia de delegação:

- a tarefa estava bem especificada?
- o agente leu os arquivos certos?
- a solução respeita contratos existentes?
- os testes cobrem o comportamento novo?
- houve alteração oportunista fora do escopo?
- dependências, licenças e segurança foram consideradas?

Ver [[03-Dominios/IA/Segurança e Guardrails/08 - Code review de código AI — o que muda|Code review de código AI — o que muda]].

### 5. O risco se desloca para workflow

Em estágios baixos, o risco está em aceitar uma resposta errada. Em estágios altos, o risco está em deixar um sistema autônomo operar sem limites suficientes.

Riscos recorrentes:

- **[[Dicionário de IA#Hallucination|alucinação]] de APIs e dependências**;
- **alterações fora do escopo**;
- **testes que confirmam implementação errada**;
- **remoção silenciosa de guardrails**;
- **exposição de segredos ou dados sensíveis**;
- **rework invisível por falta de critérios de aceite**.

Ver [[03-Dominios/IA/Segurança e Guardrails/index|Segurança e Guardrails]].

## Como Subir de Estágio

### De 2 para 3

Use chat para acelerar aprendizado, mas sempre peça explicação de tradeoffs, não só respostas. Bons prompts nessa fase:

- "Explique o erro e liste as 3 causas mais prováveis."
- "Compare duas abordagens para este problema no contexto de Spring/React/etc."
- "Mostre um exemplo mínimo e diga onde ele quebraria em produção."

### De 3 para 4

Pare de pedir "como fazer" e comece a pedir "faça esta unidade pequena". Dê arquivo, escopo e critério de aceite.

Exemplo:

```text
Implemente a função X em src/foo.ts.
Preserve a API pública.
Adicione testes para casos A, B e C.
Não altere arquivos fora de src/foo.ts e src/foo.test.ts.
```

### De 4 para 5

Escreva primeiro a especificação ou teste. O agente implementa contra o contrato.

Exemplo de mudança mental:

- Fraco: "adicione suporte a cupom".
- Forte: "um cupom válido aplica 10% antes do imposto; cupom expirado retorna erro X; cupom já usado retorna erro Y; preserve idempotência; adicione testes unitários e de integração".

### De 5 para 6

Use agent mode em um projeto real, mas com limites:

- trabalhe em branch separada;
- peça plano antes de edição grande;
- exija testes;
- revise diff antes de aceitar;
- mantenha permissões restritas;
- prefira tarefas com verificação objetiva.

### De 6 para 7

Divida por ownership claro:

- agente A investiga causa raiz;
- agente B implementa em módulo isolado;
- agente C escreve testes;
- agente D revisa segurança ou documentação.

O humano integra os resultados e resolve conflitos conceituais.

### De 7 para 8

Construa infraestrutura de maturidade:

- templates de issue e PR;
- instruções de agente versionadas;
- specs e ADRs;
- suite de testes confiável;
- linters, typecheck, SAST e SCA;
- ambientes sandbox;
- métricas de defeitos, retrabalho e custo de tokens;
- documentação voltada para humanos e agentes.

## Relação com Vibe Coding

O termo "[[Dicionário de IA#vibe coding|vibe coding]]", popularizado por [[Andrej Karpathy]], descreve um modo de programar em que o humano guia a IA por intenção, aceita sugestões e deixa o modelo carregar boa parte da implementação. Isso se conecta ao modelo de Yegge, mas há uma diferença importante:

- **vibe coding ingênuo:** confiar no fluxo, aceitar patches plausíveis e corrigir por tentativa;
- **vibe coding disciplinado:** usar IA intensamente, mas com specs, testes, revisão, contexto e guardrails.

O objetivo não é abandonar disciplina de engenharia. É tornar a disciplina mais explícita, porque ela vira a interface de controle dos agentes.

Ver [[03-Dominios/IA/Agentes de Codificação/02 - Vibe coding vs engenharia disciplinada|Vibe coding vs engenharia disciplinada]].

## Críticas e Limites do Modelo

### Pode superestimar produtividade universal

Ganhos de 5x ou mais podem ocorrer em tarefas com escopo claro, boa testabilidade e baixo acoplamento. Em sistemas legados, domínios regulados, incidentes de produção e decisões de produto ambíguas, o ganho é menor e o custo de revisão sobe.

### Pode romantizar multi-agent

Múltiplos agentes não são automaticamente melhores. Eles exigem decomposição correta, contratos e integração. Sem isso, apenas multiplicam ruído.

### Pode invisibilizar trabalho de manutenção

Código gerado rapidamente ainda precisa ser operado, monitorado, migrado, auditado e explicado. Produtividade de escrita não equivale a produtividade de ciclo de vida.

### Pode criar falsa senioridade

Um junior com IA pode produzir artefatos com aparência sênior. Isso é útil para aprendizado, mas perigoso se a organização confunde output com julgamento.

### Depende muito do ambiente

O mesmo desenvolvedor pode parecer estágio 6 em uma codebase com testes e docs, e estágio 3 em uma codebase opaca, sem scripts e sem convenções.

## Aplicação Pessoal

Para avaliar sua própria maturidade, observe comportamento real, não opinião:

- Quantas tarefas por semana você delega de ponta a ponta?
- Quantas têm critério de aceite antes da implementação?
- Você deixa o agente rodar testes e corrigir falhas?
- Você consegue revisar arquitetura sem reler cada linha?
- Seu repositório tem contexto persistente para agentes?
- Você mede retrabalho, defeitos e custo?
- Você sabe quando impedir a IA de continuar?

## Heurística

> [!tip] Regra prática
> Subir no modelo não significa "editar menos código" por vaidade. Significa **aumentar a unidade de delegação sem reduzir a qualidade do julgamento**.

## Referências

- Steve Yegge — [Welcome to Gas Town](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04)
- Steve Yegge — [Welcome to Gas City](https://steve-yegge.medium.com/welcome-to-gas-city-57f564bb3607)
- Steve Yegge — [The Death of the Junior Developer](https://webflow.sourcegraph.com/blog/the-death-of-the-junior-developer)
- Steve Yegge — [The Death of the Stubborn Developer](https://sourcegraph.com/blog/the-death-of-the-stubborn-developer)
- Steve Yegge — [Revenge of the Junior Developer](https://sourcegraph.com/blog/revenge-of-the-junior-developer)
- Andrej Karpathy — [vibe coding](https://x.com/karpathy/status/1886192184808149383)

## Veja também

- [[03-Dominios/IA/Agentes de Codificação/index|Agentes de Codificação]]
- [[03-Dominios/IA/Agentes de Codificação/02 - Vibe coding vs engenharia disciplinada|Vibe coding vs engenharia disciplinada]]
- [[03-Dominios/IA/Agentes de Codificação/12 - Multi-agent — workflows com múltiplos agentes|Multi-agent — workflows com múltiplos agentes]]
- [[03-Dominios/IA/Agentes de Codificação/17 - Human-in-the-loop — quando (não) confiar|Human-in-the-loop — quando (não) confiar]]
- [[03-Dominios/IA/Anatomia de Agents/index|Anatomia de Agents]]
- [[03-Dominios/IA/Context Engineering/index|Context Engineering]]
- [[03-Dominios/IA/Spec-Driven Development/index|Spec-Driven Development]]
- [[03-Dominios/IA/Segurança e Guardrails/index|Segurança e Guardrails]]
- [[03-Dominios/IA/Economia de Tokens/index|Economia de Tokens]]
-
