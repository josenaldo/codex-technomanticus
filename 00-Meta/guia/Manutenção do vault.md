---
title: "Manutenção do vault"
created: 2026-04-28
updated: 2026-04-28
type: how-to
status: seedling
tags:
  - guia
  - meta
publish: false
---

# Manutenção do vault

Sem rotina de manutenção, o pipeline trava: Pergaminhos vira buraco negro, Glosas acumulam sem virar Domínio, MOCs ficam mentindo. Este guia define o ritmo mínimo pra manter o Codex saudável.

## Frequências

| Cadência   | Atividade                                                |
| ---------- | -------------------------------------------------------- |
| Semanal    | Processar `01-Pergaminhos/entradas.md`                   |
| Quinzenal  | Revisar Glosas com **Meu comentário** vazio              |
| Mensal     | Atualizar MOCs e revisar status `seedling` candidatas    |
| Trimestral | Auditar Sendas, links quebrados e tags soltas            |

Não precisa ser rígido — são alvos, não obrigações. Mas se passou 2x da cadência, é sinal de débito.

## Rotina semanal — processar Pergaminhos

`01-Pergaminhos/entradas.md` é onde links coletados moram antes de virar Glosas. Se cresce sem parar, vira ruído.

**Passos:**

1. Abrir `entradas.md` e ver o tamanho. Mais de ~20 links pendentes? Pause leitura nova.
2. Pra cada link prioritário: ler → invocar `/glosa <url>` → conferir a Glosa gerada → preencher **Meu comentário**.
3. Pra links que perderam relevância: deletar diretamente. Não tudo merece virar Glosa.
4. Pra links que viraram Glosa: a skill `/glosa` já remove de `entradas.md` automaticamente.

## Rotina quinzenal — Glosas órfãs

Glosa sem **Meu comentário** preenchido é metade-feita: tem o resumo mas não tem sua reação.

**Identificar:**

```dataview
LIST
FROM "02-Glosas"
WHERE !contains(file.content, "## Meu comentário\n\n*Escreva")
  AND !contains(file.content, "## Meu comentário\n\n[A-Za-z]")
```

(O bloco acima é uma aproximação — ajuste conforme o placeholder real do template.)

**Decisão binária:**

- Vale a pena? → preencha **Meu comentário** e considere extrair pra Domínio.
- Não vale? → delete a Glosa. Fichamento sem reação não tem valor de longo prazo.

## Rotina mensal — MOCs e promoção de status

### Atualizar MOCs

Pra cada MOC de Domínio (`Java.md`, `Arquitetura.md`, ...):

1. Comparar a lista manual do MOC com o conteúdo real da pasta (o bloco Dataview ajuda).
2. Adicionar wikilinks pras notas novas que apareceram.
3. Reorganizar seções se o tema cresceu o bastante pra justificar subdivisão.
4. Remover wikilinks pra notas que foram deletadas (links vermelhos no MOC = mau cheiro).

### Promover seedlings

Identificar candidatas a `evergreen`:

```dataview
LIST
FROM "03-Dominios"
WHERE status = "seedling"
  AND file.mtime < date(today) - dur(30 days)
SORT file.mtime ASC
```

Pra cada uma: aplicar os critérios de promoção descritos em [[Convenções de escrita#Promoção de status]]. Se passou nos critérios → mude `status: evergreen` e atualize `updated`. Se não passou → ou aprofunde agora ou deixe pra próxima revisão.

## Rotina trimestral — auditoria geral

### Sendas estagnadas

Sendas são roteiros — se há checkboxes não-marcados há meses, ou:

- Você abandonou aquela trilha (delete a Senda)
- A Senda está mal-desenhada (refaça)
- Você só não estudou (decida se vai voltar)

### Links quebrados

Obsidian mostra links não-resolvidos no painel "Unresolved Links". Resolva:

- Se o destino deveria existir → crie a nota.
- Se foi typo → conserte o link.
- Se a ideia mudou → remova o link.

### Tags zumbi

Use o painel de Tags do Obsidian. Tags com 1 ou 2 ocorrências geralmente são erro de digitação ou ideias que não decolaram. Decida: consolidar (renomear pra tag existente) ou remover.

## Sinais de alerta

- `entradas.md` com 50+ links → backlog crítico.
- Mais de 10 Glosas com `status: lido` mas sem **Meu comentário** → fila de processamento bloqueada.
- MOC com mais de 30% das notas da pasta faltando → MOC mentiroso.
- Senda com 0 checkboxes marcados há 3+ meses → Senda morta.

## Veja também

- [[workflow]] — fluxo normal entre zonas
- [[Convenções de escrita]] — critérios de promoção
- [[Wikilinks e MOCs]] — anatomia de MOC vivo
