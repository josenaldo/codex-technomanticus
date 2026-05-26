---
name: arquivar-glosas
description: >
   Move glosas inativas há mais de 30 dias em `02-Glosas/` raiz pra `02-Glosas/Arquivadas/<ano>/`. Inatividade = `hoje - max(updated, mtime) > 30 dias`. Aplica-se a TODAS as glosas na raiz, independente de `progresso`. Use quando o usuário invocar `/arquivar-glosas`, falar em "arquivar glosas antigas", "limpar glosas antigas", "arquivar glosas paradas".
---

# Skill: arquivar-glosas

Varre `02-Glosas/` raiz e move pra `02-Glosas/Arquivadas/<ano-atual>/` glosas que não foram modificadas nos últimos 30 dias. Pede confirmação antes de mover. Glosas em `Promovidas/` não são afetadas.

## Quando usar

- Usuário invoca `/arquivar-glosas`.
- Usuário diz "arquivar glosas antigas", "limpar glosas paradas", "arquivar glosas inativas".

## Quando NÃO usar

- Usuário quer DELETAR glosas: skill não suporta deleção (só move pra Arquivadas).
- Usuário quer reativar glosas arquivadas: use `/acordar-glosas`.

## Argumentos

Sem argumentos. A skill é uma varredura.

## Fluxo de execução

1. **Listar arquivos em `02-Glosas/` raiz.**
   - Use Glob ou `ls` em `02-Glosas/*.md`.
   - NÃO descer em `Promovidas/` ou `Arquivadas/`.
   - Excluir o `.gitkeep` se existir.

2. **Para cada glosa, calcular `idade_inativa`:**
   - Ler frontmatter, extrair `updated` (string `YYYY-MM-DD`).
   - Obter `mtime` do arquivo (use `stat` via `Bash`).
   - `data_referencia = max(parse(updated), mtime)` (a mais recente das duas).
   - `idade_inativa = hoje - data_referencia` em dias.
   - Se `updated` ausente, usar só `mtime`.

3. **Filtrar candidatas:** `idade_inativa > 30 dias`.

4. **Listar candidatas pro usuário:**

   ```
   Candidatas a arquivar (>30 dias inativas):
   1. <slug-1>  |  idade: 47d  |  tags: [react, ui]  |  progresso: feito
   2. <slug-2>  |  idade: 95d  |  tags: [ai, rag]    |  progresso: andamento
   ...
   N. <slug-N>  |  idade: 32d  |  tags: [...]        |  progresso: abandonado

   Arquivar todas? (s)im / (n)ão / (e)scolher quais
   ```

5. **Pedir confirmação:**
   - "s": arquiva todas.
   - "n": cancelar (sem ação).
   - "e": permitir desselecionar (lista de números a tirar).

6. **Mover cada confirmada** pra `02-Glosas/Arquivadas/<ano-atual>/`:

   ```bash
   mkdir -p "02-Glosas/Arquivadas/<ano-atual>"
   git mv "02-Glosas/<slug>.md" "02-Glosas/Arquivadas/<ano-atual>/<slug>.md"
   ```

   Para cada glosa movida, atualizar `updated` no frontmatter pra hoje. (Razão: registrar o evento; permite a `/acordar-glosas` filtrar por `updated` se desejado.)

7. **Reportar ao usuário:**

   ```
   Arquivadas <N> glosas em 02-Glosas/Arquivadas/<ano-atual>/:
     - <slug-1>
     - <slug-2>
     - ...
   ```

   Se nada foi arquivado: `Nenhuma glosa atendia ao critério (>30 dias inativas).`

## Edge cases

| Caso                                       | Comportamento                            |
| ------------------------------------------ | ---------------------------------------- |
| Sem candidatas                             | Avisar "nada a arquivar" e sair sem ação |
| Pasta `Arquivadas/<ano>/` ainda não existe | Criar com `mkdir -p`                     |
| Conflito de nome (improvável)              | Abortar com erro claro                   |
| `updated` no frontmatter inválido          | Cair no `mtime` puro                     |
| Glosa em `Promovidas/`                     | Ignorar (skill só varre raiz)            |

## Convenções

- **Critério: `idade_inativa = hoje - max(updated, mtime) > 30d`.**
- **Aplica-se a TUDO na raiz**, independente de `progresso` (`andamento`, `feito`, `abandonado` — todos são candidatos).
- **Confirmação humana obrigatória** antes de mover.
- **`git mv`** pra preservar histórico.
- **Atualiza `updated`** ao mover (registra o evento de arquivamento).
