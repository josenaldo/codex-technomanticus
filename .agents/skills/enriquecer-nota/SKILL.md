---
name: enriquecer-nota
description: Enriquece uma nota do vault com lentes selecionáveis (profundidade, lacunas, novidade com fonte, conexões), filtradas por um subagente crítico calibrado pela fase da nota. Apresenta plano antes de executar. Use quando o usuário invocar /enriquecer-nota [path] [instrução], ou pedir pra "enriquecer", "aprofundar", "melhorar", "atualizar" ou "revisar" uma nota.
---

# Skill: enriquecer-nota

Enriquece uma nota do vault em 7 fases: identificar alvo → escolher lentes → analisar →
**criticar** → planejar → executar → reportar. Nunca edita sem confirmação prévia.

O eixo é **fechar lacunas reais com fonte verificável**, não decorar a nota. Um subagente crítico
calibrado pela fase poda candidatos óbvios antes de você ver o plano.

## Invocação

```
/enriquecer-nota [path] [instrução complementar]
```

- **Sem `path`:** pergunta qual nota enriquecer.
- **Com `path`:** usa o arquivo indicado (relativo à raiz do vault).
- **Instrução complementar:** texto livre como contexto (foco temático, URLs a incorporar). Pode
  pré-selecionar lentes (ex: "só profundidade e conexões").

## Referências (ler antes de executar)

- `references/lentes.md` — as 4 lentes, seus motores, higiene baseline, schema do candidato.
- `references/critico.md` — prompt do subagente crítico (I/O + rubrica por fase).
- `references/proveniencia.md` — quais lentes exigem fonte e como registrar.

## Quando NÃO usar

| Situação | Resposta |
| -------- | -------- |
| Criar nota nova | Esta skill só enriquece notas existentes; use o template |
| Só adicionar um verbete | Use `/verbete` diretamente |
| Reescrever a nota do zero | Fora de escopo; reescrita aqui é cirúrgica (trecho a trecho, com diff) |

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
```

Se a instrução complementar já indicou lentes, pré-seleciona e confirma. Pelo menos 1 lente.

## Fase 3 — Análise por lente

Para cada lente selecionada, roda o motor de `references/lentes.md` e acumula um pool de **candidatos**
(schema em `lentes.md`). Lentes que precisam de fora fazem WebSearch dirigido e registram a fonte
(`proveniencia.md`). Reescritas carregam `tipo: reescrita` + o texto `antes`.

A higiene baseline também roda aqui (frontmatter/typos/estrutura), em paralelo, mas seus itens NÃO
entram no pool do crítico.

## Fase 4 — Crítica (subagente)

Despacha UMA vez o subagente de `references/critico.md` via Agent tool (`subagent_type: general-purpose`),
passando: `fase`, `nota` (título + corpo) e os candidatos de conteúdo (`tipo: adicao|reescrita` das
lentes profundidade/lacunas/novidade). Candidatos de Conexões e a higiene **não** vão ao crítico.

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

## Fase 7 — Relatório

```
CONCLUÍDO — <título>   (fase-alvo: <Magus>)
✓ Higiene: status, updated
✓ Profundidade: <n> adições + <m> trechos aprofundados (<k> fontes)
✓ Lacunas: <n> sub-tópicos
✓ Novidade: <n> fatos (<k> fontes)
✓ Conexões: <n> wikilinks, <m> verbetes criados
– Crítico cortou <n> candidatos (óbvios para a fase)
```

Itens pulados pelo usuário aparecem com `–`.

## Convenções rígidas

- **Confirmação antes de executar** — nenhuma edição sem plano aprovado.
- **Aditivo + reescrita-com-diff** — pode aprofundar trecho raso, mas só via diff antes→depois aprovado
  item a item. **Nunca remove em silêncio.** Não reorganiza a nota inteira.
- **Wikilink format:** `[[NomeDoDicionário#Termo|texto original]]`.
- **Verbetes seguem `/verbete`** (alfabético, idioma do glossário, `updated:` bumpado).
- **Proveniência obrigatória** para Profundidade/Novidade (`proveniencia.md`). Fonte vai na seção
  Referências, nunca no corpo.
- **Crítico é independente e calibrado pela fase.** Higiene e Conexões não passam por ele.
- **Não cria notas novas** — só edita a nota-alvo e o dicionário.
- **Não progride `status` para `mature`** — decisão do usuário.

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
