# Lentes de enriquecimento — enriquecer-nota

Cada lente é um analisador focado com um *motor* próprio. O usuário escolhe quais rodar (Fase 2 da
SKILL). Cada lente produz **candidatos** no schema abaixo.

## Schema do candidato

```yaml
- id: C1                       # C1, C2, ... (sequencial global)
  lente: profundidade          # profundidade | lacunas | novidade | conexoes
  tipo: adicao                 # adicao | reescrita | link | verbete
  local: "§Nome da Seção"      # ou "após §X" | "fim da nota" | "frontmatter"
  conteudo: "<texto rascunho>" # para tipo: reescrita, é o texto "depois"
  antes: "<trecho original>"   # SÓ quando tipo: reescrita
  fonte: { tipo: url, ref: "https://..." }   # tipo: url | nota | geral
```

## Registro do conteúdo gerado (método Feynman)

Todo candidato `tipo: adicao|reescrita` é redigido como quem **ensina**, não como quem cataloga.
Exemplo canônico do registro: `03 - A janela de contexto.md` (seção prefill/decode/KV cache).
Anti-exemplo: prosa enciclopédica neutra — tecnicamente correta, mas que não antecipa a dúvida do leitor.

- **Analogia concreta** quando o mecanismo for abstrato (holofote pra atenção diluída, chef/despensa
  pra banda de memória). Uma por conceito; analogia decorativa é ruído.
- **Pergunta retórica do leitor** antes de responder ("Por que isso é o gargalo?") — espelha a dúvida
  que surgiria na leitura corrida.
- **Camadas explícitas** — separar *sintoma* de *causa*, *o que é* de *por que importa*.
- **Callouts pedagógicos** (`> [!info]`, `> [!question]-`, `> [!example]`) pra apartes, comparações
  lado a lado e FAQs; colapsáveis (`-`) quando longos.
- **Fechar seção densa** com resumo em uma linha (callout `[!summary]` ou frase final).
- **Visuais:** mindmap pra mapear o argumento de uma seção longa; graph pra mecanismo/fluxo.
- O registro **não afrouxa a proveniência**: fonte continua obrigatória e vai em `## Referências`.

## Lente: Profundidade

- **Objetivo:** ir além do óbvio — trade-offs, edge cases, gotchas, o detalhe que separa júnior de sênior.
- **Motor (query-and-file):**
  1. Liste as *perguntas em aberto* que um leitor da fase-alvo (ou acima) faria à nota.
  2. Para cada pergunta sem resposta na nota, pesquise (WebSearch dirigido) e componha uma resposta curta.
  3. Cada resposta vira um candidato `tipo: adicao` (ou `reescrita` se aprofunda trecho raso existente).
- **Exige fonte:** sim (ver `proveniencia.md`).
- **Web:** sim.

## Lente: Lacunas

- **Objetivo:** sub-tópicos que a nota deveria cobrir e não cobre.
- **Motor:**
  1. Monte o outline de cobertura esperada do tema no nível da nota (o que uma nota completa teria).
  2. Faça diff com as seções/conteúdo atuais.
  3. Cada item faltante vira candidato `tipo: adicao`, `local: "fim da nota"` ou seção apropriada.
- **Exige fonte:** preferível; `geral` aceito para cobertura estrutural.
- **Web:** às vezes.

## Lente: Novidade c/ fonte

- **Objetivo:** fatos líquidos-novos que o leitor-alvo provavelmente não sabe.
- **Motor:**
  1. Pesquisa dirigida (WebSearch) por desenvolvimentos/dados/nuances recentes ou pouco conhecidos.
  2. Descarte na origem qualquer fato sem fonte verificável.
  3. Cada fato com fonte vira candidato `tipo: adicao`.
- **Exige fonte:** sim (sem fonte = descartado antes do crítico).
- **Web:** sim.

## Lente: Conexões

- **Objetivo:** densidade de grafo — wikilinks pro dicionário do domínio + notas/trilhas relacionadas.
- **Motor (lógica herdada da v1):**
  1. Para cada termo técnico não-linkado no corpo: `grep` por `### <Termo>` no dicionário do domínio.
     - Encontrado → candidato `tipo: link`, `conteudo: "[[Dicionário#Termo|texto original]]"`.
     - Ausente → candidato `tipo: verbete` (cria verbete via lógica `/verbete` + wikilink).
  2. `grep` no vault por notas relacionadas (tags/título) → candidatos `tipo: link` com `fonte.tipo: nota`
     (entram em `## Veja também`).
- **Exige fonte:** N/A (links internos).
- **Web:** não.
- **Bypassa o crítico.**

## Higiene baseline (sempre roda)

Independente das lentes, sempre roda um passe barato, apresentado em grupo próprio e **fora do crítico**:

- **Frontmatter:** `status: seedling → growing`; `updated: → hoje`; `progress: in_progress` se ausente e aplicável.
  Nunca regride `growing`/`mature`.
- **Typos / erros gramaticais óbvios** (correção cirúrgica).
- **Estrutura:** TL;DR (`> [!abstract] TL;DR`) e parágrafo de introdução presentes? Se não, propor.
