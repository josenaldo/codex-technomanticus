---
name: enriquecer-nota
description: Enriquece uma nota do vault com lentes selecionáveis (profundidade, lacunas, novidade com fonte, conexões, mídia), filtradas por um subagente crítico calibrado pela fase da nota. Apresenta plano antes de executar. Fase 0 diagnostica a estrutura e ativa Modo A (incremental) ou Modo B (elevação). Use quando o usuário invocar /enriquecer-nota [path] [instrução], ou pedir pra "enriquecer", "aprofundar", "melhorar", "atualizar" ou "revisar" uma nota.
---

# Skill: enriquecer-nota

Enriquece uma nota do vault em 8 fases: **diagnosticar → identificar alvo → escolher lentes →
analisar → criticar → planejar → executar → reportar**. Nunca edita sem confirmação prévia.

O eixo é **fechar lacunas reais com fonte verificável**, não decorar a nota. Um subagente crítico
calibrado pela fase poda candidatos óbvios antes de você ver o plano.

**Dois modos:** Modo A (incremental) para notas bem estruturadas; Modo B (elevação) para notas
com estrutura fraca — reconstrói o esqueleto antes de enriquecer o conteúdo.

## Invocação

```
/enriquecer-nota [path] [instrução complementar]
```

- **Sem `path`:** pergunta qual nota enriquecer.
- **Com `path`:** usa o arquivo indicado (relativo à raiz do vault).
- **Instrução complementar:** texto livre como contexto (foco temático, URLs a incorporar). Pode
  pré-selecionar lentes (ex: "só profundidade e conexões").

## Modo `--auto` (não-interativo)

Ativado por `--auto` no comando:

```
/enriquecer-nota [path] --auto ["instrução"]
```

### Com instrução/plano explícito (uso pelo `enriquecer-galho`)

Quando acompanhado de uma instrução concreta (ex: vinda do `roadmap.md` do galho):

- **Pula Fase 2** (menu de lentes) — lentes e ações derivadas diretamente da instrução.
- **Pula Fase 4** (subagente crítico) — o plano do roadmap já é a lista vetada pelo diagnóstico; não há novo gate.
- **Pula Fase 5** (confirmação) — plano pré-aprovado; aplica e grava direto.
- Aplica exatamente as mudanças descritas na instrução, seguindo o Registro Feynman e os formatos de seção da Fase 3.
- Fase 7 (relatório) executa normalmente e indica `(modo --auto)` no cabeçalho do resumo.

### Sem instrução (uso avulso pelo usuário)

Quando `--auto` é usado sem instrução complementar:

- Roda a higiene baseline + as lentes inferidas do diagnóstico da Fase 0 (score + gaps do `/verificar-nota`).
- Aplica os candidatos sobreviventes sem gate de confirmação.
- **Não dispara o subagente crítico** — evita fan-out aninhado, pois este caminho é tipicamente invocado de dentro de outro subagente.
- Fase 7 indica `(modo --auto, sem instrução)`.

---

## Referências (ler antes de executar)

- `references/lentes.md` — as lentes, seus motores, higiene baseline, schema do candidato,
  e o **Registro Feynman** que governa todo conteúdo gerado.
- `references/critico.md` — prompt do subagente crítico (I/O + rubrica por fase).
- `references/proveniencia.md` — quais lentes exigem fonte e como registrar.

## Quando NÃO usar

| Situação | Resposta |
| -------- | -------- |
| Criar nota nova | Use `/escrever-nota` |
| Só adicionar um verbete | Use `/verbete` diretamente |
| Reescrever a nota do zero | Fora de escopo; reescrita aqui é cirúrgica (trecho a trecho, com diff) |
| Só adicionar vídeo/podcast | Use `/adicionar-midia` diretamente |

---

## Fase 0 — Diagnóstico estrutural

Antes de qualquer enriquecimento, audita a nota com `/verificar-nota`.

1. Roda `/verificar-nota <path>` internamente e lê o relatório de score.
2. Contabiliza o score de aprovação e os itens `✗` por seção.
3. Decide o modo de operação:

| Score | Modo | Descrição |
|-------|------|-----------|
| ≥9/12 ✓ | **Modo A — Incremental** | Nota bem estruturada; enriquece conteúdo via lentes |
| 6-8/12 ✓ | **Modo A — Incremental** | Estrutura parcial; lentes podem preencher seções ausentes |
| <6/12 ✓ | **Modo B — Elevação** | Nota estruturalmente fraca; reconstrói esqueleto antes de enriquecer |

Apresenta o diagnóstico ao usuário antes de prosseguir:

```
DIAGNÓSTICO — <título>   (fase: <Adepto>)   <N> linhas
Score: 4/12 ✓ → MODO B (elevação estrutural)

Seções críticas ausentes: E3 (diagrama), E6 (inglês), E7 (PT↔EN),
E8 (armadilhas), P2 (mecanismo), L2 (fontes)
```

### Modo B — Elevação estrutural

Ativado quando score <6/12. Executa **antes** das Fases 1-7 e reconstrói as seções
ausentes com o **Registro Feynman** de `references/lentes.md`.

**Plano de elevação (apresentado antes de executar):**

```
PLANO DE ELEVAÇÃO — <título>

[ ] TL;DR — expandir para ≥3 linhas densas (atual: <N> linhas)
[ ] Abertura — reescrever para abrir com problema, não definição
[ ] Seção "Como explicar em inglês" — criar do zero
[ ] Tabela PT↔EN — criar na seção de inglês
[ ] Seção "Armadilhas comuns" — criar com ≥3 [!warning] individuais
[ ] Diagrama Mermaid — criar diagrama de fluxo/comparação
[ ] Seção "O que vem a seguir" — criar ponte narrativa

[c] confirmar   [x] cancelar   [N] ajustar item N
```

**Execução da elevação:**

- Cada seção criada segue o Registro Feynman (problema-primeiro, analogia antes da técnica,
  mecanismo explicado, pergunta retórica do leitor).
- Insere as novas seções nos pontos naturais do fluxo — não reorganiza a nota inteira.
- Apresenta diff antes→depois para cada seção criada ou reescrita.
- Confirma antes de gravar cada bloco.

**Verificação pós-elevação:**

Roda `/verificar-nota` de novo. Se score ≥6/12 → passa para Modo A (Fases 1-7 normais).
Se ainda <6/12 → avisa e pergunta: continuar corrigindo ou forçar enriquecimento mesmo assim.

---

## Fase 1 — Identificar alvo

1. Valida `path` (`ls "<vault>/<path>"`); se ausente, pergunta o path/título.
2. Lê a nota inteira (frontmatter + corpo).
3. Infere o **domínio** pelo path (`03-Dominios/<X>/`). Fora de `03-Dominios/` → domínio indefinido
   (lente Conexões e verbetes desativados).
4. Localiza o **dicionário do domínio**: `grep -rl "^type: glossary$" --include="*.md" "<pasta_do_dominio>"`.
   1 resultado → usa; vários → pergunta; 0 → segue sem dicionário.
5. Lê **`fase:`** do frontmatter (Iniciado/Adepto/Magus). Se ausente: infere pelo conteúdo; default
   **Magus** (régua sênior, a mais estrita).

## Fase 2 — Escolher lentes

Apresenta menu multi-select:

```
Quais lentes rodar? (a higiene baseline sempre roda)
[ ] Profundidade — trade-offs, edge cases, o que separa júnior de sênior
[ ] Lacunas — sub-tópicos que faltam
[ ] Novidade c/ fonte — fatos novos com fonte verificável
[ ] Conexões — wikilinks pro dicionário + notas relacionadas
[ ] Mídia — buscar vídeo/podcast relevante pra embutir (delega pro /adicionar-midia)
```

Se a instrução complementar já indicou lentes, pré-seleciona e confirma. Pelo menos 1 lente.

**Lente Mídia:** não gera candidatos para o crítico. Quando selecionada, invoca `/adicionar-midia`
no final da Fase 6, após todas as edições de conteúdo.

## Fase 3 — Análise por lente

Para cada lente selecionada (exceto Mídia), roda o motor de `references/lentes.md` e acumula um
pool de **candidatos** (schema em `lentes.md`). Lentes que precisam de fora fazem WebSearch
dirigido e registram a fonte (`proveniencia.md`). Reescritas carregam `tipo: reescrita` + o texto `antes`.

A higiene baseline também roda aqui (frontmatter/typos/estrutura), em paralelo, mas seus itens NÃO
entram no pool do crítico.

**Registro Feynman obrigatório** em todos os candidatos de conteúdo: ver `references/lentes.md`
(analogias concretas, perguntas retóricas, camadas explícitas, resumo em 1 linha).

## Fase 4 — Crítica (subagente)

> **Modo `--auto`:** esta fase é PULADA. No fluxo do `enriquecer-galho`, o plano do roadmap já é a lista vetada pelo diagnóstico — não há segundo gate. No uso avulso `--auto` sem instrução, o subagente crítico também é omitido para evitar fan-out aninhado.

Despacha UMA vez o subagente de `references/critico.md` via Agent tool (`subagent_type: general-purpose`),
passando: `fase`, `nota` (título + corpo) e os candidatos de conteúdo (`tipo: adicao|reescrita` das
lentes profundidade/lacunas/novidade). Candidatos de Conexões, Mídia e a higiene **não** vão ao crítico.

Recebe `sobreviventes` (com novidade/profundidade/justificativa/confianca) e `descartados` (com motivo). O orquestrador **mantém o pool completo de candidatos em memória**; após a resposta do crítico, faz merge dos `sobreviventes` de volta nos candidatos por `id` para recuperar `lente`, `tipo`, `local` e `antes` — campos que o crítico não devolve mas que a Fase 6 usa.

## Fase 5 — Plano

Apresenta os sobreviventes **agrupados por lente** + Conexões + Higiene. Reescritas como **diff
antes→depois**. Lista de descartados recolhida (resgatável).

```
PLANO — <título>   (fase-alvo: <Magus>)

HIGIENE
[x] status: seedling → growing
[x] updated: → <hoje>

PROFUNDIDADE
[x] +§<seção>: <rascunho>   — fonte: <url>   (crítico: "<justificativa>", alta)
[x] ~reescrever §<X> (raso): "<antes>" → "<depois>"   — fonte: <url>

LACUNAS
[x] +§<sub-tópico>: <rascunho>   — fonte: <url|geral>

NOVIDADE
[x] +<fato>   — fonte: <url>   (crítico: "<justificativa>", media)

CONEXÕES
[x] [[Dicionário#Termo|texto]] — §<Y>
[x] DICIONÁRIO: criar verbete <termo> + wikilink

MÍDIA (delegado pro /adicionar-midia ao final)
[→] Pesquisar vídeo/podcast sobre <tema>

DESCARTADOS PELO CRÍTICO (N) ▸ (expanda para resgatar)

[c] confirmar marcados   [x] cancelar   alternar item N   [e] editar item N
```

`[c]` executa só os itens marcados. O usuário pode desmarcar/marcar e resgatar descartados.

## Fase 6 — Execução

Ordem determinística (relê o arquivo antes de cada edição):

1. **Frontmatter** (higiene).
2. **Estrutura** — TL;DR/intro se aprovados.
3. **Adições de conteúdo** — insere blocos aprovados nos locais indicados.
4. **Reescritas (diffs)** — substituição EXATA do trecho `antes` pelo `depois` aprovado.
5. **Wikilinks inline** — `[[Dicionário#Termo|texto original]]`; 1ª ocorrência não-linkada por parágrafo.
   Dentro de tabela, escapar o pipe: `[[...\|...]]`.
6. **Verbetes** — lógica `/verbete` (alfabético na seção, idioma do glossário, bump do `updated:` do
   dicionário); depois insere o wikilink na nota.
7. **Referências** — fontes externas usadas (formato de `proveniencia.md`).
8. **Veja também** — notas internas relacionadas (sem remover existentes).
9. **Mídia** — se lente Mídia foi selecionada, invoca `/adicionar-midia <path>` ao final.

## Fase 7 — Relatório

```
CONCLUÍDO — <título>   (fase-alvo: <Magus>)
✓ Higiene: status, updated
✓ Profundidade: <n> adições + <m> trechos aprofundados (<k> fontes)
✓ Lacunas: <n> sub-tópicos
✓ Novidade: <n> fatos (<k> fontes)
✓ Conexões: <n> wikilinks, <m> verbetes criados
✓ Mídia: <n> vídeos/podcasts embutidos
– Crítico cortou <n> candidatos (óbvios para a fase)
Score /verificar-nota pós-enriquecimento: <X>/12 ✓
```

Itens pulados pelo usuário aparecem com `–`.

## Convenções rígidas

- **Confirmação antes de executar** — nenhuma edição sem plano aprovado. **Exceção: modo `--auto`**, em que o plano vem pré-aprovado (via instrução explícita do galho ou via diagnóstico da Fase 0) e é aplicado sem gate interativo.
- **Registro Feynman** — todo candidato de adição/reescrita segue o registro didático de
  `references/lentes.md`: analogias concretas, perguntas retóricas do leitor, camadas explícitas
  (sintoma/causa, o quê/por quê), resumo em 1 linha. Anti-padrão: prosa enciclopédica neutra.
- **Aditivo + reescrita-com-diff** — pode aprofundar trecho raso, mas só via diff antes→depois aprovado
  item a item. **Nunca remove em silêncio.** Não reorganiza a nota inteira.
- **Wikilink format:** `[[NomeDoDicionário#Termo|texto original]]`.
- **Verbetes seguem `/verbete`** (alfabético, idioma do glossário, `updated:` bumpado).
- **Proveniência obrigatória** para Profundidade/Novidade (`proveniencia.md`). Fonte vai na seção
  Referências, nunca no corpo.
- **Crítico é independente e calibrado pela fase.** Higiene, Conexões e Mídia não passam por ele.
- **Não cria notas novas** — só edita a nota-alvo e o dicionário.
- **Não progride `status` para `mature`** — decisão do usuário.
- **Modo B não reorganiza** — adiciona seções faltantes, não reestrutura o que já existe.

## Edge cases

| Caso | Comportamento |
| ---- | ------------- |
| Arquivo não encontrado | Aborta com erro claro |
| Nota sem domínio | Conexões/verbetes desativados; demais lentes seguem |
| Nota sem `fase:` | Infere; default Magus |
| Sem dicionário no domínio | Conexões e verbetes desativados |
| Crítico devolve 0 sobreviventes | Mostra só Higiene + Conexões; avisa que nada de conteúdo passou o gate |
| WebSearch falha / offline | Lentes que dependem de web reportam "sem candidatos"; segue com o resto |
| Todas as lentes vazias e higiene vazia | "Nota já está enriquecida"; encerra |
| Reescrita: `antes` não casa exato | Pula o item, avisa; não edita às cegas |
| Modo B: score ainda <6/12 após elevação | Avisa; pergunta se quer continuar corrigindo ou forçar Modo A |
| Lente Mídia selecionada + /adicionar-midia falha | Registra no relatório como `–`; não interrompe o restante |
