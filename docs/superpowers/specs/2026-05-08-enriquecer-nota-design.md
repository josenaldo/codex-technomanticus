# Spec: Skill `enriquecer-nota`

**Data:** 2026-05-08
**Status:** aprovado

---

## Objetivo

Codificar o processo de enriquecimento de notas do vault Codex em uma skill invocável, aplicando análise de conteúdo, linkagem com o dicionário do domínio, criação de verbetes ausentes, busca de referências externas e atualização de frontmatter — tudo com confirmação antes de executar.

---

## Invocação

```
/enriquecer-nota [path] [instrução complementar]
```

- **Sem `path`:** A skill pergunta ao usuário qual nota deve ser enriquecida.
- **Com `path`:** Usa o arquivo indicado diretamente.
- **Instrução complementar:** Qualquer texto adicional é tratado como contexto livre — ex: foco temático, links de referência a incorporar, ênfase em determinada seção.

Exemplos:

```
/enriquecer-nota
/enriquecer-nota 03-Dominios/IA/Economia de Tokens/02 - Anatomia.md
/enriquecer-nota 03-Dominios/IA/02 - Anatomia.md foca na parte de reasoning
/enriquecer-nota 03-Dominios/IA/02 - Anatomia.md https://example.com/artigo
```

---

## Fase 1 — Identificar nota-alvo

1. Se `path` foi fornecido, valida que o arquivo existe.
2. Se não foi fornecido, pergunta ao usuário o path ou título da nota.
3. Lê o arquivo inteiro (frontmatter + corpo).
4. Identifica o **domínio** da nota pelo path (ex: `03-Dominios/IA/` → domínio IA).
5. Localiza o **dicionário do domínio**: arquivo com `type: glossary` na mesma pasta de domínio (ou pai mais próximo). Se houver mais de um, lista e pergunta.

---

## Fase 2 — Análise

A skill examina a nota em cinco dimensões:

### 2a. Frontmatter
- `status: seedling` → marcar para atualizar para `growing`
- `updated:` → marcar para bumpar para hoje
- `progresso:` → verificar se existe; se ausente e `status` for `growing`, sugerir adicionar `progresso: andamento`
- Outros campos faltantes relativos ao `type` da nota (ex: `publish`, `aliases`)

### 2b. Estrutura
- TL;DR (`> [!abstract] TL;DR`) está presente?
- Existe parágrafo de introdução logo após o TL;DR (antes do primeiro `##`)?
- Seção `## Veja também` existe?

### 2c. Conteúdo
- Typos e erros gramaticais óbvios
- Frases ambíguas que podem ser reescritas com clareza cirúrgica
- Lacunas de conteúdo sinalizadas pela instrução complementar (se houver)
- Se instrução complementar trouxer URLs: busca web nesses links para extrair informação relevante

### 2d. Termos técnicos — varredura única
Para cada termo técnico identificado no corpo da nota:

1. **Busca no dicionário do domínio** (grep por `### <Termo>` case-insensitive).
2. **Se encontrado no dicionário** → marcar para adicionar wikilink `[[Dicionário#Termo|texto original]]` na nota. Não cria verbete.
3. **Se não encontrado** → marcar para (a) criar verbete no dicionário via lógica da skill `/verbete` + (b) adicionar wikilink na nota após a criação.

Termos já linkados (`[[...]]`) são ignorados — não duplicar links existentes.

### 2e. Referências externas e notas relacionadas
- Busca web por artigos, papers ou docs oficiais relevantes ao tema da nota (usando instrução complementar como guia quando presente)
- Grep no vault por notas com tags ou títulos relacionados
- Candidatos para a seção `## Veja também`

---

## Fase 3 — Plano

Apresenta ao usuário um plano categorizado antes de qualquer edição:

```
PLANO — <título da nota>

FRONTMATTER
[ ] status: seedling → growing
[ ] updated: → 2026-05-08
[ ] progresso: → andamento

ESTRUTURA
[ ] Adicionar parágrafo de introdução após TL;DR

CONTEÚDO
[ ] Corrigir typo: 'estatégia' → 'estratégia'
[ ] Reescrever frase: "o modelo pode ou não..." → <proposta>

LINKS — termos já no dicionário (wikilink a adicionar na nota)
[ ] [[Dicionário de IA#Reasoning tokens|reasoning tokens]] — ocorrência em §Reasoning Tokens
[ ] [[Dicionário de IA#Prompt caching|estratégia de caching]] — ocorrência em §Input Tokens

DICIONÁRIO — termos ausentes (criar verbete + adicionar wikilink)
[ ] speculative decoding

REFERÊNCIAS
[ ] Seção "Veja também": adicionar nota relacionada [[05 - Prompt caching na prática]]
[ ] Seção "Veja também": adicionar link externo https://...

[c] confirmar tudo  [x] cancelar  [e] editar item N
```

Se o usuário editar um item (`[e] 3`), a skill apresenta o item e permite ajuste antes de continuar.

---

## Fase 4 — Execução

Ordem determinística após confirmação:

1. **Frontmatter** — atualiza `status`, `updated`, `progresso` e demais campos
2. **Estrutura** — adiciona TL;DR e/ou intro se ausentes
3. **Conteúdo** — aplica correções cirúrgicas (typos, reescritas)
4. **Wikilinks inline** — insere `[[Dicionário#Termo|texto original]]` nos pontos identificados
5. **Verbetes** — cria verbetes ausentes no dicionário (lógica da skill `/verbete`, alfabeticamente na seção correta); depois insere wikilinks correspondentes na nota
6. **Seção "Veja também"** — cria ou atualiza com notas internas e links externos

---

## Relatório final

```
CONCLUÍDO — <título da nota>

✓ Frontmatter atualizado (status, updated, progresso)
✓ Introdução adicionada
✓ 1 typo corrigido
✓ 2 wikilinks adicionados (termos já no dicionário)
✓ 1 verbete criado: speculative decoding → Dicionário de IA
✓ Seção "Veja também" criada com 2 entradas
```

---

## Convenções

- **Nível de intervenção:** moderado — corrige typos e reescreve frases ambíguas, nunca reescreve seções inteiras nem remove conteúdo existente.
- **Wikilink format:** `[[NomeDoDicionário#Termo|texto original da nota]]` — preserva o texto exato que estava na nota.
- **Verbetes:** seguem as mesmas regras da skill `/verbete` (ordem alfabética dentro da seção, idioma do glossário, `updated:` bumpado).
- **"Veja também":** se a seção já existe, adiciona entradas sem remover as existentes.
- **Instrução complementar:** não substitui a análise padrão, apenas orienta prioridades e fornece contexto adicional.
- **Termos já linkados** na nota são ignorados na varredura (não duplica links).

---

## Fora de escopo

- Não reorganiza seções existentes
- Não apaga conteúdo
- Não cria notas novas (só edita a nota-alvo e o dicionário)
- Não muda `status` de `growing` para `mature` (progressão de maturidade é decisão do usuário)
