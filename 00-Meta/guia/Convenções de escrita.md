---
title: "Convenções de escrita"
created: 2026-04-28
updated: 2026-04-28
type: how-to
status: seedling
tags:
  - guia
  - meta
publish: false
---

# Convenções de escrita

Regras práticas de como escrever notas no Codex. O objetivo é que qualquer nota, criada hoje ou em 5 anos, siga o mesmo padrão e seja recuperável.

## Atomicidade — uma ideia por nota

Cada nota em `03-Dominios/` cobre **uma única ideia evergreen**. Se você está descrevendo dois conceitos relacionados, faça duas notas e linke uma na outra.

Sinais de que a nota deveria virar duas:

- O título usa "e" ou vírgula (`X e Y`, `X, Y, Z`)
- A nota tem dois H2s que poderiam viver sem o outro
- Você se pega escrevendo "veja a outra parte desta nota" — separe

Exceções legítimas: MOCs (índices), Sendas (curadoria) e Interview Notes bilíngues.

## Filename

| Tipo de nota               | Convenção                                                                                          |
| -------------------------- | -------------------------------------------------------------------------------------------------- |
| Domínio (notas atômicas)   | `Nome do Conceito.md` — Title Case, espaços normais (não kebab-case)                               |
| MOC                        | Mesmo nome da pasta (`Java/Java.md`, `Arquitetura/Arquitetura.md`)                                 |
| Glosa                      | `<ano>-<slug-kebab-case>.md` (ex: `2026-ai-now-writes-97-of-my-code.md`); colisão usa `-2`, `-3`   |
| Senda                      | `Senda <Tema>.md` em `04-Sendas/` (flat, sem subpastas)                                            |
| Mestre                     | `Nome do Mestre.md` em `00-Meta/mestres/`                                                          |

A regra geral: o filename deve casar com o `title` do frontmatter. Wikilinks `[[Nome]]` resolvem por filename, então mudar o filename quebra links — Obsidian atualiza wikilinks em renomeações automaticamente, mas só dentro do vault.

## Frontmatter

Mínimo obrigatório em qualquer nota:

```yaml
---
title: "Nome da Nota"
created: 2026-04-28
updated: 2026-04-28
type: <tipo>
status: <status>
tags:
  - 
publish: false
---
```

### `type`

Quem é a nota. Tipos em uso:

- `concept` — nota atômica de um conceito (Domínios)
- `glosa` — fichamento de artigo
- `moc` — índice de área (Map of Content)
- `how-to` — passo-a-passo
- `til` — Today I Learned, aprendizado pontual
- `reference` — material de referência (cheatsheet, tabela)
- `trail` — Senda (curadoria)
- `note` — uso geral (template Templater padrão)

### `status`

Em que fase de cultivo a nota está:

- `seedling` — recém-criada, incompleta, em rascunho. Default de novas notas.
- `evergreen` — madura, revisada, pronta pra ser referenciada. Promova quando a nota for sólida e você confiaria nela numa entrevista.
- `lido` — usado só em Glosas, indica que o artigo foi lido (independe de ter sido processado em Domínio).

Não invente status novos sem registrar em [[Decisões do vault]].

### `publish`

- `publish: false` — default. Não vai pro site Quartz.
- `publish: true` — explicitamente publicado. MOCs e notas evergreen consolidadas.

Detalhes em [[Publicação]].

### `tags`

Tags são complementares aos Domínios — use pra cortes transversais (ex: `interview`, `senior-skills`, `performance`). Evite duplicar a pasta (`#java` numa nota dentro de `Java/` é redundante).

Convenções:

- Lowercase, kebab-case (`design-patterns`, não `DesignPatterns`)
- Hierarquia com `/` quando útil (`carreira/entrevista`)
- Sem caracteres especiais nem acentos

## Estilo de escrita

- **PT-BR** em todo conteúdo autoral. Exceção: seções "How to explain in English" das Interview Notes e citações verbatim em Glosas.
- **Frase direta**. Sujeito + verbo + complemento. Sem rodeios acadêmicos.
- **Voz ativa**. "O Spring injeta o bean" em vez de "o bean é injetado pelo Spring".
- **Negrito** pra termos-chave na primeira menção; depois texto corrido.
- **Code spans** (`backticks`) pra nomes de arquivo, comandos, identificadores de código, e nomes de classes/funções.

## Promoção de status

Quando uma nota merece ir de `seedling` pra `evergreen`:

- Foi revisada pelo menos 2 vezes
- Tem exemplos concretos (não só teoria)
- Tem pelo menos um wikilink saindo dela e um chegando nela
- Você se sentiria confortável citando ela numa entrevista ou conversa técnica

Atualize o campo `updated` quando promover.

## Veja também

- [[Wikilinks e MOCs]] — boas práticas de linking
- [[workflow]] — fluxo entre as zonas
- [[Manutenção do vault]] — quando e como revisar
