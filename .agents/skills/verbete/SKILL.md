---
name: verbete
description: >
   Adiciona um verbete (termo + definição) a um glossário de domínio do vault. Use quando o usuário invocar /verbete, pedir pra "adicionar termo ao dicionário/glossário", "criar verbete", "registrar termo", "novo verbete", ou similares. Localiza o glossário pelo frontmatter `type: glossary` e insere em ordem alfabética na seção correta. Se a definição não for fornecida, ativa modo pesquisa (busca + propõe definição pra confirmação).
---

# Skill: verbete

Adiciona um verbete a um glossário do vault (`type: glossary`). Suporta dois modos:

- **Modo manual**: usuário fornece termo + definição → skill insere direto.
- **Modo pesquisa**: usuário fornece só o termo → skill pesquisa, propõe definição, confirma com o usuário antes de inserir. **Este é o caso de uso mais comum** — usuário aprende ao mesmo tempo em que registra.

## Quando usar

Ative quando o usuário:

- Invoca `/verbete <termo>[: <definição>]`
- Pede "adicionar X ao dicionário/glossário"
- Pede "criar verbete pra X", "registrar termo X", "novo verbete: X"
- Compartilha um termo técnico isolado e pede pra catalogar

## Quando NÃO usar (e o que fazer)

| Situação                              | Resposta                                                                           |
| ------------------------------------- | ---------------------------------------------------------------------------------- |
| Usuário pede pra criar glossário novo | Esta skill só adiciona a glossários existentes; sugira usar `Template - Glossário` |
| Termo já existe no glossário          | Aborte; mostre a definição existente; sugira edição manual                         |
| Nenhum glossário encontrado no vault  | Avise; sugira criar um a partir do template                                        |

## Fluxo de execução

### 1. Parse do input

Extrai `termo` e (opcionalmente) `definição` do input do usuário. Formatos suportados:

- `/verbete <termo>: <definição>` — modo manual
- `/verbete <termo>` — modo pesquisa
- "adiciona <termo> ao dicionário de <X>" — modo pesquisa, com hint de glossário
- "novo verbete <termo>: <definição>" — modo manual

Se o termo é ambíguo (ex.: "agent" pode ser IA ou vendas), peça contexto antes de prosseguir.

### 2. Localizar o glossário-alvo

Estratégia em ordem de prioridade:

1. **Hint explícito do usuário** (ex.: "ao dicionário de IA"): faça `grep -l "type: glossary"` em todo o vault, então filtre por `title:` ou filename matching o hint (case-insensitive, sem acento).
2. **Domínio inferido pelo CWD**: se o usuário está em `03-Domínios/<X>/`, procure `type: glossary` na mesma pasta.
3. **Sem hint nem CWD útil**: liste todos os arquivos com `type: glossary` no vault e pergunte ao usuário.

Comando de descoberta:

```bash
grep -rl "^type: glossary$" --include="*.md" /caminho/do/vault
```

Se 1 resultado → usa direto. Se vários → lista títulos + pergunta. Se 0 → aborta com aviso.

### 3. Validar o alvo

Confirme que o arquivo encontrado tem `type: glossary` no frontmatter. Se não tiver, aborte com erro claro (não escreva no arquivo errado).

### 4. Checar conflito

Leia o arquivo. Se já existe um `### <Termo>` (case-insensitive, ignorando acento) em qualquer seção:

- Aborte sem modificar.
- Mostre ao usuário a definição existente e a seção onde está.
- Sugira: "Edite manualmente ou use outro termo."

### 5. Modo pesquisa (se definição vazia)

5a. **Detectar idioma do glossário:**

- Lê `lang:` do frontmatter.
- Se ausente: infira pelas 2-3 primeiras definições existentes.
- Se vazio (glossário novo sem verbetes): pergunte ao usuário e persista no frontmatter.

5b. **Pesquisar:**

- Use conhecimento geral primeiro (suficiente pra maioria dos termos técnicos consolidados).
- Para termos recentes/obscuros (lançamento do mês passado, paper específico, framework novo), use `WebSearch`.
- Se ambos falharem (termo desconhecido): aborte e peça definição manual ao usuário.

5c. **Compor proposta:**

- **Definição**: 1 a 3 frases, no idioma do glossário (respeitando `lang:`), estilo conciso e direto. Mantenha termos técnicos em inglês apenas quando consolidados no mercado (ex: embeddings, tokens, fine-tuning). Não acadêmico-prolixo. Sem citações no corpo.
- **Seção sugerida**: lê todas as `## H2` do arquivo + escolhe a melhor com base no significado do termo. Se nenhuma se encaixa bem, propõe criar nova seção.
- **Fonte consultada**: link, nome do paper, ou "conhecimento geral" — pra mostrar no relatório (não vai no corpo da definição).

5d. **Apresentar pro usuário:**

```
Termo: <Termo>
Glossário: <título do glossário>
Seção sugerida: <Nome da Seção>
Definição proposta:
  <definição em 1-3 frases>

Fonte consultada: <link ou descrição>

[c] confirmar e inserir
[e] editar definição
[s] mudar seção
[x] cancelar
```

Aguarde resposta do usuário antes de inserir.

### 6. Modo manual (definição fornecida)

Pula o modo pesquisa. Vai direto pra escolha de seção:

- Se usuário mencionou seção no input → usa (case-insensitive match contra H2 existentes).
- Se não → lista seções existentes + opção "nova seção", pergunta.
- Se seção não existe e usuário quer criar → confirma uma vez antes de criar.

Não precisa de confirmação da definição (o usuário já forneceu).

### 7. Inserir o verbete

Insere `### <Termo>\n<definição>\n\n` em posição **alfabética** dentro da seção escolhida:

- Comparação case-insensitive, ignora acento (`Á` = `a`).
- Se o termo começa com símbolo (ex.: `#tag`), trata o símbolo como prefixo e ordena pela primeira letra alfabética.
- Se a seção não existe ainda, cria no fim do arquivo (antes de qualquer rodapé tipo `---` ou `## Veja também` final).
- Insere uma linha em branco antes e depois do bloco do verbete pra preservar legibilidade.

### 8. Atualizar frontmatter

Bumpa o campo `updated:` pra hoje (formato `YYYY-MM-DD`). Se o campo não existir, cria.

### 9. Reportar ao usuário

Mensagem de sucesso única, no formato:

```
Verbete "<Termo>" adicionado em <título do glossário> → seção "<Seção>".
[Modo pesquisa] Fonte consultada: <fonte>
```

A linha de fonte só aparece se foi modo pesquisa.

## Edge cases

| Caso                                        | Comportamento                                                          |
| ------------------------------------------- | ---------------------------------------------------------------------- |
| Definição vazia                             | Modo pesquisa (não é erro — é o caso de uso mais comum)                |
| Termo já existe no glossário                | Aborta; mostra definição existente + seção; sugere edição manual       |
| Glossário ambíguo (vários matches)          | Lista títulos + pergunta qual                                          |
| Glossário não encontrado                    | Lista todos `type: glossary` do vault + pergunta                       |
| Vault sem nenhum glossário                  | Aborta; sugere criar um a partir de `Template - Glossário.md`          |
| Arquivo alvo sem `type: glossary`           | Aborta com erro claro (proteção contra escrever no arquivo errado)     |
| Termo ambíguo (significa coisas diferentes) | Pede contexto ao usuário antes de pesquisar                            |
| WebSearch falha / sem rede                  | Tenta só conhecimento geral; se também falhar, pede definição manual   |
| Termo desconhecido (não existe)             | Aborta; sugere fornecer definição manual ou verificar grafia           |
| Seção pedida não existe                     | Pergunta se quer criar antes de inserir                                |
| Glossário sem `lang:` e sem definições      | Pergunta idioma uma vez; persiste no frontmatter                       |
| Termo com caracteres Markdown (`#`, `[`)    | Escape correto pra heading válido; preserve no display                 |
| Definição muito longa (>5 frases)           | Em modo pesquisa, condense; em modo manual, aceite e avise gentilmente |

## Convenções rígidas

- **Ordem alfabética** sempre dentro de cada seção (case-insensitive, sem acento).
- **Idioma da definição** = `lang:` do glossário-alvo (não traduza se o usuário forneceu manualmente em outro idioma — só avise).
- **Modo pesquisa sempre confirma** antes de inserir. Modo manual insere direto.
- **`updated:`** sempre bumpado.
- **Fonte vai no relatório**, nunca no corpo da definição (mantém glossário limpo).
- **Não fabrica seção** — usa existente ou confirma criação antes.
- **Não fabrica definição em modo manual** — só pesquisa em modo pesquisa.
- **Não modifica verbetes existentes** — só adiciona. Edição é manual.

## Exemplos

### Exemplo 1 — modo manual com seção explícita

```
Usuário: /verbete chunking: dividir um documento em pedaços menores antes de gerar embeddings, equilibrando granularidade de retrieval e contexto preservado. Adiciona em RAG and Vector Databases do dicionário de IA.

Skill:
1. Localiza Dicionário de IA.md
2. Verifica que "chunking" não existe ainda
3. Insere "### chunking\n<definição>\n" em posição alfabética dentro de "RAG and Vector Databases" (entre BM25 e dense retrieval)
4. Bumpa updated: 2026-05-03
5. Reporta: Verbete "chunking" adicionado em Dicionário de IA → seção "RAG and Vector Databases".
```

### Exemplo 2 — modo pesquisa (caso comum)

```
Usuário: /verbete reranking ao dicionário de IA

Skill:
1. Localiza Dicionário de IA.md (lang: pt)
2. Verifica que "reranking" não existe ainda
3. Pesquisa (conhecimento geral suficiente)
4. Apresenta:

   Termo: reranking
   Glossário: Dicionário de IA
   Seção sugerida: RAG and Vector Databases
   Definição proposta:
     Uma etapa de pontuação de segundo estágio em pipelines de recuperação que
     reordena um conjunto inicial de candidatos usando um modelo mais caro (tipicamente
     um cross-encoder) para melhorar a qualidade dos principais resultados (top-K)
     passados para o LLM.

   Fonte consultada: conhecimento geral

   [c] confirmar  [e] editar  [s] mudar seção  [x] cancelar

5. Usuário responde "c"
6. Insere alfabeticamente em RAG and Vector Databases (entre hybrid search e retrieval)
7. Bumpa updated
8. Reporta: Verbete "reranking" adicionado em Dicionário de IA → seção "RAG and Vector Databases". [Modo pesquisa] Fonte consultada: conhecimento geral.
```

### Exemplo 3 — modo pesquisa com seção nova

```
Usuário: /verbete LoRA

Skill:
1. Localiza glossário (CWD em 03-Domínios/IA/)
2. Pesquisa LoRA
3. Apresenta:

   Termo: LoRA
   Seção sugerida: Fine-tuning (nova seção)
   Definição proposta:
     Low-Rank Adaptation: a parameter-efficient fine-tuning technique that
     freezes the base model weights and trains small low-rank matrices injected
     into attention layers, dramatically reducing memory and storage cost.
   ...

4. Usuário: "s, coloca em LLMs Anatomy"
5. Skill confirma e insere em LLMs Anatomy (entre inference e parameters/weights)
```
