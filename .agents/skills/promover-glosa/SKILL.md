---
name: promover-glosa
description: >
   Promove uma glosa em `02-Glosas/` para uma nota nova em `03-Dominios/`. Cria a nota usando Template - Nota, popula `## Fontes` com wikilink pra glosa, move a glosa pra `02-Glosas/Promovidas/<ano>/`, e atualiza o frontmatter da glosa com `promovida_em`. Use quando o usuário invocar `/promover-glosa <slug>`, falar em "promover glosa", "criar nota a partir dessa glosa", "esta glosa merece nota", ou pedir explicitamente pra fazer essa transição.
---

# Skill: promover-glosa

Promove **uma** glosa para o status de fonte de uma nota nova de domínio. A glosa permanece como artefato de leitura (movida pra subpasta de promovidas); a nota nasce nova com a TL;DR da glosa como ponto de partida.

## Quando usar

- Usuário invoca `/promover-glosa <slug>` (slug ou wikilink da glosa).
- Usuário invoca `/promover-glosa` sem argumento (modo interativo).
- Usuário diz "promover esta glosa", "criar nota a partir dessa glosa", "esta glosa merece nota de domínio".

## Quando NÃO usar

- Usuário quer consolidar VÁRIAS glosas em UMA nota: use `/sintetizar-glosas` em vez disso.
- Usuário quer apenas marcar glosa como lida (`progress: done`): edição manual ou skill futura.

## Argumentos

| Forma                        | Comportamento                                                                                 |
| ---------------------------- | --------------------------------------------------------------------------------------------- |
| `/promover-glosa <slug>`     | Promove a glosa especificada (slug do nome de arquivo, sem extensão).                         |
| `/promover-glosa <wikilink>` | Aceita wikilink (`[[<slug>]]` ou `[[02-Glosas/<slug>]]`).                                     |
| `/promover-glosa`            | Modo interativo: lista glosas em raiz com `progress: done` ou `in_progress`|`done`, usuário escolhe. |

## Fluxo de execução

1. **Resolver a glosa.**
   - Se argumento explícito: localizar arquivo em `02-Glosas/` (raiz) ou `02-Glosas/Promovidas/<ano>/`. Se não existir, abortar com erro.
   - Se modo interativo: listar candidatas (em `02-Glosas/` raiz com `progress` em `in_progress` ou `done`), apresentar pra escolha.

2. **Ler a glosa** com `Read` tool. Extrair:
   - `title` (do frontmatter).
   - `tags` (lista do frontmatter).
   - TL;DR (texto da seção `## TL;DR`).
   - `promovida_em` (lista atual; se já tiver itens, será incrementada).

3. **Sugerir domínio destino.** Heurística:
   - Mapear cada tag pra um domínio candidato olhando `03-Dominios/`. Ex.: tag `react` → `03-Dominios/React/`. Tag `validacao` → `03-Dominios/Frontend/Validação/`.
   - Apresentar a sugestão com a tag correspondente. Se múltiplas tags casam com domínios diferentes, listar todas e pedir escolha.
   - Permitir o usuário corrigir/digitar outro caminho.

4. **Sugerir nome da nota.** Default: derivar do `title` da glosa. Ex.: glosa "DESIGN.md — A format specification for describing a visual identity to coding agents — google-labs-code" → sugerir `DESIGN.md` ou `Design Spec for AI Agents`. Pedir confirmação.

5. **Verificar se a nota já existe** em `03-Dominios/<X>/<Nome>.md`:
   - Se SIM: perguntar (a) anexar a glosa às fontes da nota existente, (b) escolher outro nome, (c) cancelar.
   - Se NÃO: prosseguir.

6. **Criar a nota nova** com `Write` tool em `03-Dominios/<X>/<Nome>.md`. Conteúdo:

   ```markdown
   ---
   title: "<Nome da nota>"
   created: <hoje YYYY-MM-DD>
   updated: <hoje YYYY-MM-DD>
   type: concept
   status: seedling
   progress: in_progress
   tags:
     - <tags-da-glosa>
     - <tag-do-domínio se houver convenção>
   publish: true
   ---

   # <Nome da nota>

   <!-- Ponto de partida da glosa: -->
   <!-- <TL;DR da glosa, como comentário, pra você expandir em prosa própria> -->

   ## O que é

   <!-- Definição clara e objetiva -->

   ## Como funciona

   <!-- Mecanismo, funcionamento, detalhes relevantes -->

   ## Quando usar

   <!-- Casos de uso, contexto adequado -->

   ## Armadilhas comuns

   <!-- O que evitar, erros frequentes -->

   ## Fontes

   - [[02-Glosas/Promovidas/<ano-decisão>/<slug-da-glosa>|<title-da-glosa>]]

   ## Aprofundamento

   <!-- Vide Template - Nota.md -->

   ## Veja também

   -
   ```

7. **Mover a glosa** (apenas se ainda na raiz):

   ```bash
   mkdir -p "02-Glosas/Promovidas/<ano-atual>"
   git mv "02-Glosas/<slug>.md" "02-Glosas/Promovidas/<ano-atual>/<slug>.md"
   ```

   Use `git mv` em vez de `mv` para preservar histórico do git.

   Se a glosa já estava em `02-Glosas/Promovidas/<ano>/`, NÃO mover de novo (idempotência).

8. **Atualizar frontmatter da glosa** com `Edit` tool:
   - `promovida_em`: append `[[03-Dominios/<X>/<Nome>]]` (lista cresce; preserva itens anteriores).
   - `updated`: hoje.
   - `progress`: se atual é `in_progress`|`done`, mudar pra `in_progress`|`done`.

9. **Reportar ao usuário:**

   ```
   Glosa promovida: <slug>.
   Nota criada: 03-Dominios/<X>/<Nome>.md
   Glosa movida pra: 02-Glosas/Promovidas/<ano>/<slug>.md
   ```

   Se a glosa já estava promovida (apenas append no `promovida_em`):

   ```
   Glosa <slug> já estava em Promovidas/<ano>/.
   Nova nota criada: 03-Dominios/<X>/<Nome>.md
   Glosa agora referencia <N> notas.
   ```

## Edge cases

| Caso                                         | Comportamento                                                                           |
| -------------------------------------------- | --------------------------------------------------------------------------------------- |
| Glosa não existe                             | Erro claro com sugestão de listar glosas existentes                                     |
| Glosa já em Promovidas/                      | Append em `promovida_em`, não move; cria nota normalmente                               |
| Domínio destino não existe                   | Pergunta se cria. Se sim, criar `03-Dominios/<X>/index.md` mínimo antes de criar a nota |
| Nota já existe                               | Perguntar (a) anexar fonte, (b) outro nome, (c) cancelar                                |
| Conflito de nome em Promovidas               | Avisar e abortar (nome de arquivo é único por construção)                               |
| Tags da glosa não mapeiam pra nenhum domínio | Listar TODOS os domínios disponíveis e pedir escolha                                    |
| TL;DR vazia ou ausente                       | Criar nota sem comentário-TL;DR; ainda popular `## Fontes`                              |
| Glosa sem tags                               | Pedir tags pro usuário antes de criar a nota                                            |

## Convenções

- **Nota nasce com `progress: in_progress` e `status: seedling`** — ponto de partida, não produto pronto.
- **`updated` da glosa é atualizado** em toda interação.
- **`git mv` em vez de `mv`** pra preservar histórico.
- **Nunca deletar a glosa** — sempre mover (perda zero).
- **Confirmação humana** para nome da nota e domínio destino (antes de criar arquivos).
