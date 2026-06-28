---
title: "Guia de implementação do zero"
created: 2026-04-26
updated: 2026-06-28
type: concept
fase: Iniciado
progress: backlog
status: seedling
publish: true
tags:
  - memoria-agentes
  - guia
  - implementacao
  - hands-on
  - llm-wiki-pattern
aliases:
  - Guia LLM Wiki
  - Implementar memória de agentes
  - LLM Wiki howto
---

# Guia de implementação do zero

> [!abstract] TL;DR
> Existem dois caminhos práticos para implementar memória de agentes baseada no LLM Wiki Pattern: **(1) minimal seguindo o gist do Karpathy** — pasta `raw/` + `wiki/` + `CLAUDE.md` montada manualmente em cerca de 30 minutos; **(2) pronto via basic-memory MCP** — Obsidian + Claude com integração nativa em cerca de 10 minutos. Esta nota guia ambos passo a passo, mostra um template de `CLAUDE.md` reutilizável e fornece critério para decidir quando ir além do mínimo. A escolha não é "qual é melhor" e sim "qual encaixa no objetivo": aprender o pattern por dentro vs. produzir resultado rápido com ferramenta madura.

> [!question]- Dúvidas e lacunas desta nota
> - Dúvida gerada pelo conteúdo: o template de `CLAUDE.md` apresentado aqui é genérico — como adaptar as seções de "operações" para domínios altamente especializados (ex: jurídico, médico) sem tornar o schema tão denso que o agente ignore partes dele? Existe pesquisa ou prática consolidada sobre o tamanho ideal de um `CLAUDE.md`?
> - Lacuna potencial: a nota descreve a estrutura de pastas e as operações mas não aprofunda como lidar com conflitos de schema — quando o agente interpreta uma regra de forma inesperada, qual processo iterativo (testar → observar desvio → ajustar regra) funciona melhor na prática?

## O que é

Esta nota apresenta **dois caminhos práticos** para sair do conceitual e ter uma base de memória de agente rodando no mesmo dia. O **Caminho A** é didático: monta a estrutura mínima descrita no [[06 - O LLM Wiki Pattern (gist do Karpathy)|gist do Karpathy]], escreve o `CLAUDE.md` à mão e roda as primeiras operações (`ingest`, `query`, `lint`) com Claude Code. Ele ensina o pattern por dentro — quem termina o Caminho A entende exatamente por que cada peça existe.

O **Caminho B** é direto: instala [[13 - basic-memory — MCP nativo Obsidian|basic-memory]], aponta para um vault Obsidian e em poucos minutos tem Claude lendo e escrevendo markdown estruturado via [[Dicionário de IA#MCP (Model Context Protocol)|MCP]]. Pula a etapa de schema porque a ferramenta já traz convenções razoáveis. Útil para quem quer testar o pattern em um problema real antes de investir tempo em customização.

## Por que importa

Sem implementação, o conhecimento das notas anteriores ([[Dicionário de IA#RAG (Retrieval-Augmented Generation)|RAG]], taxonomia, panorama, comparativos) fica abstrato. A diferença entre ler sobre o LLM Wiki Pattern e ter uma `wiki/` com 20 páginas geradas, lintada e versionada é qualitativa — só na prática aparecem os atritos reais (drift, contradições, índice desatualizado, schema vago).

Os dois caminhos foram escolhidos por terem **barreira de entrada baixa**: 30 minutos para o Caminho A, 10 minutos para o Caminho B. Esse custo cabe em uma sessão única e produz material para experimentar antes de decidir investir em framework de produção como [[15 - Mem0 — vetorial + grafo|Mem0]], [[14 - Letta (ex-MemGPT)|Letta]] ou [[16 - Zep e Graphiti — knowledge graph temporal|Zep]]. Em outras palavras: este guia é o **primeiro experimento controlado** antes de escolhas arquiteturais maiores.

## Caminho A — minimal seguindo o gist do Karpathy

> [!warning] Quando escolher este caminho
> Este é o caminho para quem quer **dominar o pattern**. Ao final, você entende cada peça (raw vs. wiki, schema, log append-only, lint), sabe o que customizar e por quê. É também o melhor ponto de partida para quem pretende, depois, evoluir para implementações como [[10 - LLM-knowledge-base (Wendel) — direto do gist|LLM-knowledge-base do Wendel]] ou [[12 - graphify — knowledge graph de raw|graphify]].

### Estrutura inicial

A estrutura mínima espelha a separação **raw imutável** vs. **wiki mantida pelo LLM** descrita por [[Andrej Karpathy|Karpathy]]:

```text
my-llm-wiki/
├── CLAUDE.md           # schema (regras)
├── raw/                # fontes brutas (immutable)
│   ├── articles/
│   ├── papers/
│   └── transcripts/
├── wiki/               # mantido pelo LLM
│   ├── index.md
│   ├── log.md
│   └── *.md
└── README.md
```

A intuição é simples: `raw/` é o **acervo** (fontes que entram no sistema e nunca são editadas pelo agente); `wiki/` é o **conhecimento processado** (páginas interlinkadas que o [[Dicionário de IA#LLM (Large Language Model)|LLM]] mantém). O `CLAUDE.md` na raiz é o contrato que ensina o agente como operar entre os dois.

### Passos

1. **Criar a estrutura** acima com `mkdir -p` e `touch` dos placeholders. `wiki/index.md` e `wiki/log.md` começam vazios — serão preenchidos pelo LLM. Inicialize git: `git init`.
2. **Escrever o `CLAUDE.md`** com regras claras (template no próximo bloco). Resista à tentação de deixar vago — schema vago produz wiki ruim.
3. **Adicionar primeiras 3-5 fontes** em `raw/`: artigos relevantes, transcrições, papers. Em markdown sempre que possível. Esse pequeno corpus vira o ponto de partida.
4. **Pedir ao Claude Code** a primeira operação: *"Faça primeira ingestão de `raw/articles/` em `wiki/`"*. O agente vai ler as fontes, extrair conceitos, criar páginas, popular `index.md` e adicionar entrada em `log.md`.
5. **Revisar o wiki gerado** com olhar crítico: páginas duplicadas? Wikilinks coerentes? Categorias que fazem sentido? Quando o LLM desviar do esperado, ajuste o `CLAUDE.md` — é onde o aprendizado acontece.
6. **Iterar** com mais fontes. A cada lote novo, rode `ingest` e periodicamente um `lint pass` para detectar contradições, páginas órfãs e índice desatualizado.
7. **Commit a cada operação importante.** Git é parte do pattern: cada `ingest`, `query` que cria página nova ou `lint` deve virar um commit. Histórico = auditabilidade.

> [!tip] Tempo realista
> A primeira passagem dos 7 passos cabe em 30 minutos se as fontes já estiverem em markdown. A iteração 2-3 (refinar schema baseado em onde o LLM desviou) é onde a maior parte do valor aparece — separe outra hora para isso.

### Template de `CLAUDE.md`

Este é um ponto de partida funcional. Copie, ajuste o tom para o domínio e itere conforme necessário:

````markdown
# Schema da minha LLM Wiki

## Estrutura
- `raw/` — fontes imutáveis. Nunca edite arquivos aqui.
- `wiki/` — wiki interlinkada. Você (Claude) mantém.
  - `index.md` — catálogo content-oriented
  - `log.md` — append-only log de operações
  - `concepts/` — páginas de conceito
  - `entities/` — pessoas, projetos, ferramentas
- `README.md` — meta

## Operações
- **Ingest [arquivo]:** ler, extrair conceitos/entidades, criar/atualizar páginas, adicionar entrada em `log.md`
- **Query [pergunta]:** buscar em wiki, sintetizar resposta com citações, criar nova página se valiosa
- **Lint:** detectar contradições, páginas órfãs, links quebrados, índice desatualizado

## Convenções
- Páginas em PT-BR
- Wikilinks `[[X]]` para tudo
- Frontmatter mínimo: `created`, `updated`, `tags`
- Citação inline: `[fonte: raw/articles/foo.md]`
- Cada página ≤ 1500 palavras (subdivida se passar)

## Quando perguntar antes de fazer
- Mudanças que afetem >5 páginas
- Nova categoria/pasta na wiki
- Quando detectar contradições não-triviais
````

### Por dentro do template — o que cada seção faz

Entender por que cada bloco existe é o que permite iterar o schema quando ele não funciona:

**Seção Estrutura:** estabelece o contrato de pastas. O agente precisa saber exatamente onde cada tipo de arquivo mora — sem isso, cria pastas ad hoc que quebram o pattern. A separação `concepts/` vs `entities/` não é estética: conceitos são abstrações (o que é RAG?), entidades são concretos (o que é o projeto Mem0?). Misturar os dois tipos produz páginas híbridas difíceis de navegar.

**Seção Operações:** nomeia os procedimentos. "Ingest", "Query" e "Lint" viram vocabulário compartilhado — você diz "faz um lint" e o agente sabe o que fazer. Sem isso, cada pedido exige descrição do zero. O `log.md` append-only é especialmente importante: sem ele, não há como reconstruir o que o agente fez em uma sessão passada — é o diário de auditoria do sistema.

**Seção Convenções:** os detalhes que parecem menores mas fazem diferença. O limite de 1500 palavras por página força subdivisão — sem ele o agente infla páginas até virarem paredes de texto. A citação inline `[fonte: raw/articles/foo.md]` resolve um problema real: sem rastreabilidade, você não sabe de onde veio um fato na wiki.

**Seção "Quando perguntar":** o freio mais importante. Sem ela, o agente reestrutura silenciosamente — move pastas, renomeia páginas, resolve contradições pela própria lógica. A cláusula ">5 páginas" é um limiar concreto que você calibra conforme ganha confiança no agente.

### Como iterar o schema efetivamente

A primeira versão do `CLAUDE.md` vai errar. Isso é esperado e é parte do método. O loop de melhoria funciona assim:

1. **Rodar operação** → observar onde o agente desviou do esperado
2. **Identificar a lacuna** no schema: faltou uma regra? A regra existente é ambígua?
3. **Adicionar ou clarificar** a regra no `CLAUDE.md`
4. **Repetir** com a mesma operação no mesmo corpus

Exemplos de desvios comuns e ajustes correspondentes:

- Agente cria página para cada entidade mencionada, mesmo secundárias → adicionar regra: "Crie página de entidade só se aparecer em ≥ 3 fontes ou tiver papel central em ≥ 1 fonte"
- Páginas de conceito ficam vagas demais → adicionar regra: "Cada página de conceito deve ter: definição em 1 parágrafo, exemplo concreto, links para conceitos relacionados"
- Índice fica desatualizado → adicionar regra: "Sempre que criar ou atualizar página de conceito, verifique se `index.md` a lista"

Após 3-4 iterações, o schema tende a estabilizar. A partir daí, desvios são sinais de edge case genuíno, não de schema vago.

## Caminho B — basic-memory MCP (pronto)

> [!warning] Quando escolher este caminho
> Este é o caminho para quem quer **resultado rápido com ferramenta madura**. Ao final, você tem Claude lendo e escrevendo markdown em um vault Obsidian via MCP, sem precisar projetar schema. Bom para validar o pattern em um problema real antes de decidir se vale construir do zero.

### Passo a passo

1. **Instalar basic-memory:**

   ```bash
   pip install basic-memory
   ```

   Para isolamento, prefira ambiente virtual ou Docker (ver [[13 - basic-memory — MCP nativo Obsidian|13 - basic-memory]] para alternativas).

2. **Configurar [[Dicionário de IA#MCP server|MCP server]]** no Claude Desktop ou Claude Code. Edite o arquivo de configuração MCP do cliente e adicione:

   ```json
   {
     "mcpServers": {
       "basic-memory": {
         "command": "python",
         "args": ["-m", "basic_memory.mcp_server"],
         "env": {"VAULT_PATH": "/path/to/obsidian/vault"}
       }
     }
   }
   ```

   Ajuste `VAULT_PATH` para o caminho absoluto do vault. Reinicie o cliente para carregar o MCP server.

3. **Apontar para vault Obsidian** existente ou novo. basic-memory escreve markdown na pasta indicada — qualquer vault Obsidian funciona, e nada impede de usar uma pasta solta sem Obsidian instalado.

4. **Pronto.** A partir daí, Claude lê e escreve markdown estruturado via MCP, e Obsidian renderiza paralelamente (se aberto). As operações ficam expostas como tools nativas — `write_note`, `search_notes`, `read_note` etc.

> [!warning] basic-memory não é plugin Obsidian
> A confusão é frequente em tutoriais editoriais. basic-memory é um **MCP server externo** que escreve em uma pasta — Obsidian apenas abre essa pasta como vault e renderiza. Não há acoplamento com plugins do Obsidian. Detalhes em [[13 - basic-memory — MCP nativo Obsidian]].

### O que você ganha e perde no Caminho B

**Ganha:** velocidade, convenções razoáveis prontas, integração MCP nativa, vocabulário de operações já desenhado.

**Perde:** controle fino do schema, entendimento profundo do pattern, possibilidade de customizar operações específicas do domínio. A ferramenta é boa, mas é a opinião dos autores dela sobre como organizar memória.

Quem começa pelo Caminho B e sente atrito no schema costuma migrar parte do trabalho para o Caminho A — não há contradição em usar os dois.

## Quando ir além do mínimo

Os dois caminhos cobrem casos de uso individuais e bem delimitados. Sinais claros de que vale escalar para framework de produção:

- **Volume cresce além de ~500 documentos:** busca textual simples começa a degradar; considere [[Dicionário de IA#hybrid search|hybrid search]] ([[Dicionário de IA#BM25|BM25]] + vector). Implementações de referência em [[10 - LLM-knowledge-base (Wendel) — direto do gist|LLM-knowledge-base]].
- **Multi-user concorrente:** vários agentes ou usuários escrevendo na mesma base exigem governance, locking e merge — território de [[15 - Mem0 — vetorial + grafo|Mem0]], [[14 - Letta (ex-MemGPT)|Letta]] e [[16 - Zep e Graphiti — knowledge graph temporal|Zep]].
- **Tasks de alto custo:** quando cada query custa caro (em latência ou tokens), entram tiering, caching e evaluation sistemática.
- **Compliance:** data residency, audit logs, retenção formal — Zep e Graphiti são mais sólidos nesse eixo.
- **Casos com KG denso:** se o domínio tem grafo de relações forte (entidades muito interconectadas, raciocínio multi-hop), considere [[12 - graphify — knowledge graph de raw|graphify]] ou Zep/Graphiti.

Para um mapa visual da escolha por critério, veja [[09 - Panorama de implementações (abril 2026)|09 - Panorama]] e [[21 - Comparativo crítico (LongMemEval)|21 - Comparativo]].

## Quando NÃO escalar

Pressão para escalar é constante na cultura de engenharia, mas frequentemente errada. Indicadores de que minimal/basic-memory continua sendo a escolha certa:

- **Volume abaixo de ~100 documentos.** Overhead de framework sofisticado não compensa; a wiki minimal é mais rápida e auditável.
- **Single user, single agent.** Sem concorrência, governance é trabalho desperdiçado.
- **Workflow estável.** Manutenção de framework é trabalho, não prêmio. Se o que existe funciona, mexer é dívida.

Em todos esses casos, o tempo gasto avaliando frameworks rende mais investido em **qualidade do schema** (`CLAUDE.md`) e **revisão das páginas geradas**.

## Armadilhas comuns

> [!warning] Armadilha 1: Esquecer o lint
> Wiki rot é inevitável sem health check periódico. Páginas órfãs acumulam silenciosamente, wikilinks quebram quando páginas são renomeadas, e o índice fica desatualizado após cada lote de ingestão. A diferença entre uma wiki útil após seis meses e uma wiki abandonada é um `lint` periódico — semanal em bases ativas, quinzenal em bases estáveis. Trate lint como rotina de manutenção, não como operação de emergência.

> [!warning] Armadilha 2: `CLAUDE.md` vago demais
> Schema impreciso é a causa mais comum de output inconsistente. Quando o agente cria páginas que misturam conceitos com entidades, ou quando o índice fica desatualizado mesmo após instrução explícita, o problema raramente é o modelo — é falta de regra clara. O diagnóstico correto é: "qual instrução faltou no `CLAUDE.md` para o agente ter feito a escolha certa?" Itere o schema baseado nos desvios, não nos outputs esperados.

> [!warning] Armadilha 3: Não revisar páginas geradas pelo LLM
> Drift, alucinação silenciosa e contradições entre páginas são reais e se acumulam. O agente pode extrair um fato ligeiramente errado de uma fonte ambígua, e esse fato se propaga para outras páginas via wikilink. Revisão humana periódica não é overhead — é o mecanismo de controle de qualidade que separa uma wiki confiável de uma wiki aparentemente organizada mas factualmente degradada.

> [!warning] Armadilha 4: Misturar `raw/` com `wiki/`
> Editar fontes em `raw/` ou pedir ao agente que escreva lá quebra a auditabilidade. A separação `raw/` (imutável) vs `wiki/` (mantida pelo LLM) é o que torna possível responder "de onde veio esse fato?" em qualquer momento. Sem ela, não há como distinguir o que entrou como fonte do que o LLM sintetizou — e alucinações se tornam indistinguíveis de fatos documentados.

> [!warning] Armadilha 5: Esperar resultado out-of-the-box
> O pattern requer 2-3 iterações no schema antes de funcionar bem. Na primeira ingestão, é normal que o agente crie páginas com granularidade errada, misture tipos de entidade ou use wikilinks inconsistentes. Isso não é falha do pattern — é calibração necessária. Quem desiste depois da primeira passagem perde exatamente o ciclo onde o schema se ajusta ao domínio e o output começa a convergir para o esperado.

## Como explicar em inglês

> [!tip] Interview quote
> "I implement the LLM Wiki Pattern in two steps: first a minimal setup with a `raw/` folder for immutable sources and a `wiki/` folder the LLM maintains, governed by a `CLAUDE.md` schema file; then I iterate the schema based on where the agent deviates from expected behavior."

| Português | Inglês |
|-----------|--------|
| Fontes brutas imutáveis | Immutable raw sources |
| Schema do agente | Agent schema / CLAUDE.md contract |
| Ingestão de fontes | Source ingestion |
| Páginas órfãs | Orphan pages |
| Lint periódico | Periodic lint / Health check |
| Índice desatualizado | Stale index |
| Drift de conteúdo | Content drift |
| Caminho didático vs direto | Hands-on path vs fast path |
| Wikilinks interlinkados | Interlinked wikilinks |
| Append-only log | Append-only operation log |

### Como usar em entrevista

Quando perguntarem sobre implementação de memória de agentes, a estrutura dual-path é concisa e mostra julgamento:

- "For prototyping, I use the minimal setup: a `CLAUDE.md` schema, a `raw/` folder for immutable sources, and a `wiki/` the LLM maintains. It takes 30 minutes and teaches you the pattern from the inside."
- "The key insight is that the schema file is the contract — vague schema produces inconsistent output. I iterate it based on deviations, not on wishful expectations."
- "Lint is the maintenance operation people skip and then wonder why their wiki decayed. I treat it as a weekly routine, not a one-time cleanup."

## Checklist de "pronto para produção"

Antes de considerar a implementação estável o suficiente para uso contínuo, verifique cada item:

- [ ] `CLAUDE.md` tem operações nomeadas explicitamente (`Ingest`, `Query`, `Lint`) com descrição de o que cada uma faz
- [ ] `raw/` e `wiki/` estão em pastas separadas e o schema proíbe edição de `raw/` pelo agente
- [ ] `wiki/log.md` existe e está sendo preenchido como append-only em cada operação
- [ ] Há pelo menos um commit por operação importante (git é parte do pattern)
- [ ] Foi executado pelo menos um `lint pass` após a primeira ingestão
- [ ] O schema tem limite de palavras por página para evitar páginas infladas
- [ ] Há cláusula "perguntar antes" para mudanças que afetem mais de N páginas
- [ ] Para basic-memory (Caminho B): `VAULT_PATH` aponta para caminho absoluto correto e o MCP server foi testado com pelo menos uma operação de escrita e leitura

Este checklist não garante qualidade — o schema ainda pode ser vago, o corpus pode ser pequeno demais para detectar problemas, e o lint pode não ter sido calibrado para o domínio. Mas garante que os fundamentos estruturais estão no lugar antes de investir em mais conteúdo.

## O que vem a seguir

Com o guia prático em mãos — dois caminhos concretos, um template de schema testável e as armadilhas que derrubam implementações em campo — a trilha fecha no plano econômico: o que há de valor comercial ao redor desse pattern, quem paga, quanto se observa em ofertas públicas comparáveis e quando recusar o trabalho. A dimensão de negócio não é apêndice opcional: saber monetizar o conhecimento técnico é o que transforma domínio do tema em carreira sustentável. Veja [[24 - Aplicações comerciais e modelo de negócio]].

## Veja também

- [[06 - O LLM Wiki Pattern (gist do Karpathy)]] — pattern original
- [[07 - Por que Obsidian e markdown como substrato]] — fundamentação do substrato
- [[10 - LLM-knowledge-base (Wendel) — direto do gist]] — implementação Python de referência
- [[13 - basic-memory — MCP nativo Obsidian|13 - basic-memory]] — ferramenta do Caminho B
- [[09 - Panorama de implementações (abril 2026)|09 - Panorama]] — quando ir além
- [[21 - Comparativo crítico (LongMemEval)|21 - Comparativo]] — escolha por critério
- [[22 - Críticas, limitações e armadilhas]] — auditoria honesta

## Referências

- **Karpathy, A.** *LLM Wiki gist.* `https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f` — fonte primária do Caminho A.
- **basic-memory documentation.** `https://docs.basicmemory.com/` — referência canônica do Caminho B (instalação, configuração MCP, convenções).
- **Notas da trilha:** [[06 - O LLM Wiki Pattern (gist do Karpathy)|06]], [[10 - LLM-knowledge-base (Wendel) — direto do gist|10]], [[13 - basic-memory — MCP nativo Obsidian|12]] — contexto conceitual e de implementação que esta nota assume.
- **Tutorials editoriais** (aimaker.substack, mattpaige68.substack, thetoolnerd, entre outros). Existem vários walkthroughs públicos sobre basic-memory + Obsidian; **a qualidade varia bastante** — alguns confundem basic-memory com plugin Obsidian, outros tratam o pattern como solução pronta sem mencionar lint nem revisão. Use como complemento, sempre conferindo contra a documentação oficial.
- **Git** — parte estrutural do Caminho A. `git init` na raiz do projeto + commit por operação é o que habilita auditabilidade. Sem histórico, não há como reconstruir o que o agente fez em sessões passadas ou desfazer uma ingestão ruim.
- **Claude Code** — o agente que executa as operações `Ingest`, `Query` e `Lint` no Caminho A. As operações definidas no `CLAUDE.md` são instruções para Claude Code — não para Claude Desktop ou API direta. A distinção importa: Claude Code tem acesso ao filesystem e ao git, o que é necessário para o pattern funcionar.
- **LLM-knowledge-base (Wendel).** `https://github.com/WendellLiu/llm-knowledge-base`. Implementação Python que segue o gist do Karpathy de perto. Boa referência para quem quer ver o Caminho A em código antes de escrever o próprio. Detalhado em [[10 - LLM-knowledge-base (Wendel) — direto do gist|nota 10]].
- **graphify.** Referenciado em [[12 - graphify — knowledge graph de raw|nota 12]]. Extensão do pattern que converte `raw/` em knowledge graph — passo intermediário entre o Caminho A minimal e frameworks de produção como Zep/Graphiti. Relevante quando o domínio tem relações densas entre entidades que justificam grafo em vez de wiki flat.
- **[[22 - Críticas, limitações e armadilhas]]** — leitura obrigatória antes de adotar qualquer um dos dois caminhos. Arma o leitor com as perguntas certas antes de investir em implementação.
- **[[08 - Arquitetura de um sistema de memória]]** — aprofunda a diferença entre substrate (onde se guarda) e schema (o que se guarda e como). O `CLAUDE.md` desta nota é a implementação prática do "schema" discutido lá.
- **[[21 - Comparativo crítico (LongMemEval)|21 - Comparativo crítico]]** — contexto essencial sobre por que o Caminho A (minimal) às vezes supera frameworks sofisticados em workloads específicos. O argumento de "quando não escalar" desta nota é sustentado pelos dados daquele comparativo.
- **[[24 - Aplicações comerciais e modelo de negócio]]** — nota seguinte da trilha. Toma como dado que o leitor implementou (ou entendeu como implementar) e avança para o plano econômico: quem paga pelo pattern, em que formato e por quanto.
- **[[03-Dominios/Tecnologia/IA/Memória de Agentes/index]]** — MOC da trilha. Contexto completo de onde esta nota se situa na sequência de aprendizado e links para todas as outras notas do galho.
- **[[09 - Panorama de implementações (abril 2026)|09 - Panorama de implementações]]** — mapa de quais ferramentas existem e para qual perfil cada uma serve. Leitura complementar para quem, após o Caminho A ou B, quer entender em que ponto da paisagem cada solução se encaixa antes de escalar.
- **[[04 - RAG vs memória de longo prazo]]** — fundação conceitual que determina quando RAG basta e quando os caminhos desta nota fazem sentido. Se a distinção ainda não está clara, ler esta nota antes de implementar economiza a tentação de over-engineering.
