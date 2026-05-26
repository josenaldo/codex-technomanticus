---
name: sintetizar-glosas
description: >
   Consolida várias glosas em UMA nota nova de domínio. Cria nota com `## Fontes` populada com wikilinks pras N glosas selecionadas, move cada glosa pra `02-Glosas/Promovidas/<ano>/`, e atualiza `promovida_em` em cada uma. Use quando o usuário invocar `/sintetizar-glosas <criterio>` ou pedir pra "sintetizar glosas sobre X", "consolidar essas glosas em uma nota", "criar nota a partir de várias glosas".
---

# Skill: sintetizar-glosas

Cria UMA nota nova de domínio sintetizando VÁRIAS glosas relacionadas a um tema. A skill prepara o esqueleto da nota com a seção `## Fontes` populada com wikilinks pras glosas selecionadas; o usuário escreve a síntese em prosa própria — a skill **não** gera a síntese textual automaticamente.

## Quando usar

- Usuário invoca `/sintetizar-glosas tag:<X>` (filtro por tag).
- Usuário invoca `/sintetizar-glosas <assunto>` (busca textual).
- Usuário invoca `/sintetizar-glosas` sem argumento (modo interativo).
- Usuário diz "sintetizar glosas sobre X", "consolidar essas glosas em uma nota", "criar nota a partir de várias glosas".

## Quando NÃO usar

- Usuário quer promover apenas UMA glosa: use `/promover-glosa`.
- Usuário quer apenas listar glosas sobre um tema: skill futura `/glosas-list` ou dataview manual.

## Argumentos

| Forma                          | Comportamento                                    |
| ------------------------------ | ------------------------------------------------ |
| `/sintetizar-glosas tag:<X>`   | Filtra glosas (raiz + Promovidas) com tag `<X>`. |
| `/sintetizar-glosas <assunto>` | Busca textual em `title`, `aliases`, `tags`.     |
| `/sintetizar-glosas`           | Modo interativo: pergunta filtro.                |

## Fluxo de execução

1. **Filtrar candidatas.**
   - Se `tag:<X>`: usar Glob/Grep em `02-Glosas/**/*.md` pra encontrar arquivos com a tag (verificar frontmatter).
   - Se `<assunto>`: busca textual em `title`, `aliases`, `tags` de cada glosa.
   - Se modo interativo: pergunta filtro ao usuário.

2. **Apresentar lista pra seleção.** Cada candidata: slug, título curto, tags, status (raiz vs Promovidas).
   - Default: todas marcadas pra incluir.
   - Usuário pode tirar itens.
   - Se 0 candidatas: avisar e abortar.
   - Se 1 candidata: sugerir usar `/promover-glosa` em vez disso.

3. **Ler conteúdo de cada glosa selecionada** (TL;DR + tags + título). Use `Read` tool em cada arquivo.

4. **Sugerir domínio + nome da nota:**
   - **Domínio**: interseção das tags das glosas mapeadas pra domínios. Se múltiplos candidatos, pedir escolha.
   - **Nome**: derivar do tema comum (heurística simples — pode usar a tag mais frequente ou o assunto buscado).
   - Pedir confirmação ao usuário.

5. **Verificar se a nota já existe.** Mesma lógica de `/promover-glosa`.

6. **Criar a nota nova** em `03-Dominios/<X>/<Nome>.md`:

   ```markdown
   ---
   title: "<Nome da nota>"
   created: <hoje YYYY-MM-DD>
   updated: <hoje YYYY-MM-DD>
   type: concept
   status: seedling
   progresso: andamento
   tags:
     - <tags-consolidadas-das-glosas>
   publish: true
   ---

   # <Nome da nota>

   <!-- Síntese a partir das glosas listadas em ## Fontes. -->
   <!-- Escreva aqui a sua interpretação consolidada. -->

   ## O que é

   <!-- Definição clara e objetiva -->

   ## Como funciona

   <!-- Mecanismo, funcionamento, detalhes relevantes -->

   ## Quando usar

   <!-- Casos de uso, contexto adequado -->

   ## Armadilhas comuns

   <!-- O que evitar, erros frequentes -->

   ## Fontes

   - [[02-Glosas/Promovidas/<ano>/<slug-1>|<title-1>]]
   - [[02-Glosas/Promovidas/<ano>/<slug-2>|<title-2>]]
   - <... outras glosas selecionadas ...>

   ## Aprofundamento

   <!-- Vide Template - Nota.md -->

   ## Veja também

   -
   ```

   **Importante:** NÃO popular as outras seções com texto extraído das glosas. Síntese é voz própria do usuário; deixar comentários como guia.

7. **Mover cada glosa selecionada que ainda esteja na raiz** pra `02-Glosas/Promovidas/<ano-atual>/`. Use `git mv`. Pular glosas já em Promovidas.

8. **Atualizar `promovida_em` em cada glosa** (append do novo wikilink). Atualizar `updated` pra hoje.

9. **Reportar ao usuário:**

   ```
   Síntese criada: 03-Dominios/<X>/<Nome>.md (<N> fontes)
   Glosas movidas pra Promovidas/<ano>/:
     - <slug-1>
     - <slug-2>
     - ...
   Glosas que já estavam em Promovidas (frontmatter atualizado):
     - <slug-N>
   ```

## Edge cases

| Caso                                  | Comportamento                                           |
| ------------------------------------- | ------------------------------------------------------- |
| 0 candidatas                          | Avisar e abortar                                        |
| 1 candidata                           | Sugerir `/promover-glosa` em vez disso                  |
| Tags inconsistentes                   | Apresentar interseção; se vazia, união como sugestão    |
| Domínio destino não existe            | Mesma lógica de `/promover-glosa` (perguntar se cria)   |
| Nota já existe                        | Perguntar anexar/outro nome/cancelar                    |
| Mistura de glosas (raiz + Promovidas) | OK; mover só as da raiz; atualizar frontmatter de todas |
| Conflito de nome no destino           | Abortar com erro                                        |

## Convenções

- **Skill NÃO escreve a síntese textual.** Apenas prepara `## Fontes` e o esqueleto. Síntese é voz própria.
- **Confirmação humana** antes de mover/criar.
- **`git mv`** pra preservar histórico.
- **`updated` em todas as glosas tocadas**.
