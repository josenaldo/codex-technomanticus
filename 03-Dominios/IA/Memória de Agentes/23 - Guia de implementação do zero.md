---
title: "Guia de implementação do zero"
created: 2026-04-26
updated: 2026-04-26
type: concept
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

## O que é

Esta nota apresenta **dois caminhos práticos** para sair do conceitual e ter uma base de memória de agente rodando no mesmo dia. O **Caminho A** é didático: monta a estrutura mínima descrita no [[06 - O LLM Wiki Pattern (gist do Karpathy)|gist do Karpathy]], escreve o `CLAUDE.md` à mão e roda as primeiras operações (`ingest`, `query`, `lint`) com Claude Code. Ele ensina o pattern por dentro — quem termina o Caminho A entende exatamente por que cada peça existe.

O **Caminho B** é direto: instala [[13 - basic-memory — MCP nativo Obsidian|basic-memory]], aponta para um vault Obsidian e em poucos minutos tem Claude lendo e escrevendo markdown estruturado via MCP. Pula a etapa de schema porque a ferramenta já traz convenções razoáveis. Útil para quem quer testar o pattern em um problema real antes de investir tempo em customização.

## Por que importa

Sem implementação, o conhecimento das notas anteriores (RAG, taxonomia, panorama, comparativos) fica abstrato. A diferença entre ler sobre o LLM Wiki Pattern e ter uma `wiki/` com 20 páginas geradas, lintada e versionada é qualitativa — só na prática aparecem os atritos reais (drift, contradições, índice desatualizado, schema vago).

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

A intuição é simples: `raw/` é o **acervo** (fontes que entram no sistema e nunca são editadas pelo agente); `wiki/` é o **conhecimento processado** (páginas interlinkadas que o LLM mantém). O `CLAUDE.md` na raiz é o contrato que ensina o agente como operar entre os dois.

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

Pontos de atenção no schema:

- **Operações nomeadas** (`Ingest`, `Query`, `Lint`) viram vocabulário compartilhado: você diz "lint" e o agente sabe o procedimento.
- **Append-only log** em `wiki/log.md` é barato e funciona como diário do agente — útil para entender o que mudou e quando.
- **Limite de palavras por página** força subdivisão. Sem isso, o LLM tende a inflar páginas até virarem inúteis.
- **Cláusula "perguntar antes"** é um freio explícito: sem ela, o agente toma decisões irreversíveis em silêncio.

## Caminho B — basic-memory MCP (pronto)

> [!warning] Quando escolher este caminho
> Este é o caminho para quem quer **resultado rápido com ferramenta madura**. Ao final, você tem Claude lendo e escrevendo markdown em um vault Obsidian via MCP, sem precisar projetar schema. Bom para validar o pattern em um problema real antes de decidir se vale construir do zero.

### Passo a passo

1. **Instalar basic-memory:**

   ```bash
   pip install basic-memory
   ```

   Para isolamento, prefira ambiente virtual ou Docker (ver [[13 - basic-memory — MCP nativo Obsidian|13 - basic-memory]] para alternativas).

2. **Configurar MCP server** no Claude Desktop ou Claude Code. Edite o arquivo de configuração MCP do cliente e adicione:

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

- **Volume cresce além de ~500 documentos:** busca textual simples começa a degradar; considere hybrid search (BM25 + vector). Implementações de referência em [[10 - LLM-knowledge-base (Wendel) — direto do gist|LLM-knowledge-base]].
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

- **Esquecer o lint.** Wiki rot é inevitável sem health check periódico — páginas órfãs, links quebrados, índice desatualizado. Trate `lint` como rotina, não como conserto.
- **`CLAUDE.md` vago demais.** Schema impreciso produz output ruim. Itere o schema baseado nos erros — quando o agente desvia, é sinal de que falta uma regra explícita.
- **Não revisar páginas geradas pelo LLM.** Drift, alucinação e contradições silenciosas são reais. Revisão humana periódica é parte do pattern, não opcional.
- **Misturar `raw/` com `wiki/`.** Editar fontes em `raw/` ou pedir ao agente que escreva lá quebra a auditabilidade. A separação é o que torna o pattern confiável.
- **Esperar resultado out-of-the-box.** O pattern requer 2-3 iterações no schema antes de funcionar bem. Quem desiste depois da primeira passagem perde o efeito.
- **Confiar cegamente em estatísticas auto-reportadas** de framework. Benchmarks de fornecedor frequentemente são otimizados para o caso ideal — ver [[22 - Críticas, limitações e armadilhas]] para auditoria honesta dos números mais citados.

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
