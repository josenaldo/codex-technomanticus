---
name: acordar-glosas
description: >
   Reativa glosas previamente arquivadas em `02-Glosas/Arquivadas/<ano>/`. Move pra raiz `02-Glosas/`, reseta `progresso: andamento`, atualiza `updated`. Aceita filtro por slug, tag, ou assunto. Use quando o usuário invocar `/acordar-glosas <criterio>` ou pedir pra "reativar glosas sobre X", "tirar glosas do arquivo", "acordar glosas pra estudar X".
---

# Skill: acordar-glosas

Move glosas de `02-Glosas/Arquivadas/**` de volta pra raiz `02-Glosas/`, com confirmação. Útil pra retomar trabalho em um assunto previamente arquivado.

## Quando usar

- Usuário invoca `/acordar-glosas <slug>` (uma glosa específica).
- Usuário invoca `/acordar-glosas tag:<X>` (todas com tag).
- Usuário invoca `/acordar-glosas <assunto>` (busca textual).
- Usuário invoca `/acordar-glosas` (modo interativo).
- Usuário diz "reativar glosas sobre X", "tirar glosas do arquivo", "acordar glosas pra estudar X".

## Quando NÃO usar

- Usuário quer reativar glosa que foi PROMOVIDA (em `Promovidas/`): glosas promovidas são histórico imutável; edite-as in-place sem mover. Esta skill **não** mexe em `Promovidas/`.

## Argumentos

| Forma                       | Comportamento                                       |
| --------------------------- | --------------------------------------------------- |
| `/acordar-glosas <slug>`    | Reativa a glosa especificada (slug).                |
| `/acordar-glosas tag:<X>`   | Reativa todas as glosas em `Arquivadas/` com a tag. |
| `/acordar-glosas <assunto>` | Busca textual em `title`, `aliases`, `tags`.        |
| `/acordar-glosas`           | Modo interativo: pergunta filtro.                   |

## Fluxo de execução

1. **Filtrar candidatas em `02-Glosas/Arquivadas/**`** (recursivo, todos os anos).
   - Se `<slug>`: localizar arquivo. Erro se não existir.
   - Se `tag:<X>`: percorrer arquivos, ler frontmatter, filtrar por tag.
   - Se `<assunto>`: busca textual em `title`, `aliases`, `tags`.
   - Se modo interativo: perguntar filtro.

2. **Listar candidatas pro usuário:**

   ```
   Candidatas a acordar:
   1. <slug-1>  |  arquivada: 2025/  |  tags: [react, ui]   |  updated: 2025-08-12
   2. <slug-2>  |  arquivada: 2026/  |  tags: [ai, rag]     |  updated: 2026-02-03
   ...

   Acordar todas? (s)im / (n)ão / (e)scolher quais
   ```

3. **Pedir confirmação:**
   - "s": acordar todas.
   - "n": cancelar.
   - "e": desselecionar.

4. **Para cada confirmada:**

   ```bash
   git mv "02-Glosas/Arquivadas/<ano>/<slug>.md" "02-Glosas/<slug>.md"
   ```

   Verificar conflito: se `02-Glosas/<slug>.md` já existe na raiz, abortar com erro pra esta glosa específica e seguir com as demais.

5. **Atualizar frontmatter de cada glosa acordada:**
   - `progresso`: resetar pra `andamento`.
   - `updated`: hoje.

6. **Reportar ao usuário:**

   ```
   Acordadas <N> glosas (movidas pra raiz com progresso: andamento):
     - <slug-1>
     - <slug-2>
     ...
   ```

   Se houve conflitos:

   ```
   Conflitos (não foi possível acordar):
     - <slug-X>: já existe arquivo de mesmo nome em 02-Glosas/. Inspecionar manualmente.
   ```

## Edge cases

| Caso                     | Comportamento                                                |
| ------------------------ | ------------------------------------------------------------ |
| Glosa não está arquivada | Erro claro com sugestão de listar arquivadas                 |
| 0 candidatas             | "Nenhuma glosa arquivada com esse critério"                  |
| Conflito de nome na raiz | Abortar pra esta glosa, seguir com outras; reportar conflito |
| Glosa em `Promovidas/`   | Ignorar (skill só atua em `Arquivadas/`); explicar           |

## Convenções

- **Skill atua APENAS em `Arquivadas/`** — `Promovidas/` é histórico imutável.
- **Reset de `progresso: andamento`** ao acordar (assume que vai trabalhar).
- **`updated` atualizado** pra registrar evento.
- **`git mv`** pra preservar histórico.
- **Confirmação humana obrigatória.**
