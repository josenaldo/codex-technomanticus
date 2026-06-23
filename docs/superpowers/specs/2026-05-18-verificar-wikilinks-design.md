---
title: "Skill `verificar-wikilinks` — design"
created: 2026-05-18
status: spec
domain: ferramentas-do-vault
related:
  - "[[03-Dominios/Tecnologia/IA/index.md]]"
  - ".agents/skills/deadlink/"
  - ".agents/skills/obsidian-markdown/"
---

# Spec — Skill `verificar-wikilinks`

## Motivação

A MOC `03-Dominios/Tecnologia/IA/index.md` contém wikilinks como `[[Anatomia dos LLMs]]`, `[[MCP]]`, `[[Context Engineering]]` que apontam para **pastas** sem `index.md`. No Obsidian funcionam (resolução por basename pula folders); no site gerado pelo Quartz **quebram**, porque Quartz não converte `[[Pasta]]` em `[[Pasta/index]]` quando a pasta não tem arquivo de índice.

Esse padrão deve estar replicado em outras MOCs do vault. Precisamos de uma ferramenta para:

1. **Detectar** wikilinks e links markdown internos quebrados, aplicando a regra do Quartz.
2. **Corrigir** as quebras com auxílio do histórico do git (arquivos renomeados/movidos) e geração opcional de `index.md`.

Ferramentas existentes avaliadas:

- **Deadlink** (BytesAgain, MIT-0): só varre URLs `http(s)://`. Não detecta wikilinks. Fica como ferramenta complementar para auditar referências externas, **não substitui** esta skill.
- **kepano/obsidian-skills**: instalado (defuddle, json-canvas, obsidian-bases, obsidian-cli, obsidian-markdown). Nenhuma das 5 sub-skills cobre detecção de links quebrados.

## Objetivos da v1

- Detectar wikilinks (`[[…]]`), embeds de markdown (`![[…]]` com extensão `.md`) e links markdown internos (`[texto](caminho.md)`) quebrados em uma pasta do vault.
- Aplicar a regra do Quartz: `[[Pasta]]` é quebrado se a pasta não tiver `index.md`.
- Gerar relatório JSON estruturado.
- Corrigir as quebras com aprovação do usuário, usando histórico do git para detectar renames.
- Zero dependências externas (Python stdlib only).
- Preservar isolamento público/apocrypha (regra de memória).

## Não-objetivos da v1

- Verificação de URLs HTTP/HTTPS (Deadlink faz).
- Verificação de assets binários (imagens, PDFs, `.canvas`).
- Detecção de wikilinks em propriedades Dataview/Bases.
- Modo watch / hook de pre-commit.
- Paralelização por subagentes.
- Suporte a outros geradores estáticos (regra Quartz hardcoded).

## Arquitetura

Divisão em duas camadas:

### Camada 1 — Script Python (detecção determinística)

Localização: `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`

Responsabilidades:

- Indexar o vault (uma vez por execução).
- Parsear arquivos `.md` da pasta-alvo extraindo wikilinks, embeds e links markdown internos.
- Resolver cada link aplicando regras do Quartz.
- Produzir JSON com lista de quebras e estatísticas.

Pure função: sem efeitos colaterais além do JSON de saída. Sem alucinação.

### Camada 2 — Skill `SKILL.md` (orquestração pelo agente)

Localização: `.agents/skills/verificar-wikilinks/SKILL.md`

Responsabilidades:

- Invocar o script no path solicitado.
- Ler JSON, agrupar quebras por motivo.
- Para cada quebra, decidir correção: `git log --follow` em caso de rename, criar `index.md` em caso de folder-sem-index, ou pedir desambiguação.
- Aplicar edições via tool `Edit` apenas após aprovação do usuário.
- Re-rodar script para verificar zero quebras (verification-before-completion).

## Componentes

### `scripts/check_wikilinks.py`

**Interface CLI**:

```
python check_wikilinks.py <pasta-alvo> [--vault-root <path>] [--output <json-path>] [--respect-public-only]
```

**Algoritmo**:

1. **Indexação do vault** (uma vez):
   - Walk `<vault-root>` (auto-detectado subindo até achar `.obsidian/` ou usando cwd) coletando `.md`.
   - Ignora `.obsidian/`, `.git/`, `node_modules/`, `.agents/`.
   - Constrói:
     - `files_by_basename: dict[str, list[Path]]` (basename sem `.md` → caminhos)
     - `files_by_relpath: set[Path]` (paths relativos ao vault root)
     - `folders: dict[str, list[Path]]` (basename de pasta → caminhos)
     - `folders_with_index: set[Path]` (subset de `folders` que têm `index.md`)

2. **Parser de links** (regex + pós-processamento):
   - Wikilinks: `\[\[([^\]\n]+?)\]\]` — captura `alvo|alias`, `alvo#section`, `pasta/alvo`.
   - Embeds: `!\[\[…\]\]` (mesma regex, flag `embed=True`). Filtrar embeds não-`.md` (assets) na v1.
   - Markdown internos: `\[([^\]]+)\]\(([^)]+)\)` filtrado para targets que terminam em `.md` (com ou sem anchor) e que não são URLs.
   - **Pular** linhas dentro de code fences (` ``` `) e spans inline (`` ` ``).
   - **Marcar** `in_frontmatter: true` para links dentro do bloco YAML inicial.

3. **Resolução** (aplica regras do Quartz):
   - Match por basename exato → ok (alvo é arquivo `.md`).
   - Target é nome de pasta → ok se a pasta tem `index.md`; senão `reason: folder_without_index`.
   - Target tem path explícito (`pasta/nota`) → resolve diretamente.
   - Múltiplos matches ambíguos → `reason: ambiguous` com lista de candidatos.
   - Sem match → `reason: target_not_found` com sugestões via `difflib.get_close_matches` (cutoff=0.6).
   - Para `[[Nota#Seção]]`: também valida seção. Se arquivo resolve mas seção não existe → `reason: anchor_not_found`.

4. **Saída JSON**:

```json
{
  "scanned_at": "2026-05-18T14:32:00Z",
  "vault_root": "/home/josenaldo/repos/personal/codex-technomanticus",
  "target_folder": "03-Dominios/Tecnologia/IA",
  "stats": {
    "files_scanned": 47,
    "links_total": 312,
    "links_broken": 12,
    "by_reason": {
      "folder_without_index": 8,
      "target_not_found": 2,
      "ambiguous": 2
    }
  },
  "broken": [
    {
      "file": "03-Dominios/Tecnologia/IA/index.md",
      "line": 42,
      "raw": "[[Anatomia dos LLMs]]",
      "target": "Anatomia dos LLMs",
      "alias": null,
      "anchor": null,
      "type": "wikilink",
      "in_frontmatter": false,
      "reason": "folder_without_index",
      "candidates": [
        "03-Dominios/Tecnologia/IA/Anatomia dos LLMs/01 - O que é um LLM.md"
      ]
    }
  ],
  "warnings": [
    {"file": "x.md", "msg": "encoding error, skipped"}
  ]
}
```

### `SKILL.md`

**Frontmatter**:

```yaml
---
name: verificar-wikilinks
description: "Detecta e corrige wikilinks/links markdown quebrados em um vault Obsidian, aplicando a regra do Quartz (folder-link exige index.md). Use quando o usuário invocar /verificar-wikilinks <pasta>, pedir 'checar links quebrados', 'auditar wikilinks', 'consertar links da MOC'."
---
```

**Fluxo conversacional descrito no corpo**:

1. Receber pasta-alvo do usuário (default: pasta atual se invocado sem argumento, com confirmação).
2. Rodar `python .agents/skills/verificar-wikilinks/scripts/check_wikilinks.py <pasta>`.
3. Ler o JSON gerado.
4. Apresentar **resumo agrupado** ao usuário:
   - "Encontrei N quebras em M arquivos. Plano:"
   - Lista por motivo (`folder_without_index` → criar index.md; `target_not_found` → git log; etc.).
5. Pedir aprovação explícita ("aprovar?", "sim/não/ajustar").
6. Aplicar correções via tool `Edit` (sequencial, agrupadas por arquivo, linhas em ordem decrescente para preservar offsets).
7. Re-rodar script. Reportar resultado final.

## Fluxo de dados

```
usuário /verificar-wikilinks 03-Dominios/IA
        ↓
script Python → /tmp/wikilinks-report-<timestamp>.json
        ↓
agente lê JSON, agrupa por reason
        ↓
agente apresenta plano agrupado
        ↓
[GATE] usuário aprova
        ↓
agente aplica Edits + cria index.md onde necessário
        ↓
script Python re-roda → 0 quebras ou lista resíduo
        ↓
agente reporta status final
```

## Estratégia por tipo de quebra

| Motivo | Diagnóstico | Correção |
|---|---|---|
| `folder_without_index` | `[[X]]` aponta para pasta `…/X/` sem `index.md` | **Default**: criar `index.md` mínimo (frontmatter `created`/`type: moc`, título `# X`, lista dos `.md` da pasta). **Alternativa**: trocar wikilink para arquivo específico. |
| `target_not_found` (renomeado) | `git log --diff-filter=R --follow -- '*<basename>*'` retorna match | Atualizar wikilink para novo caminho/nome automaticamente. |
| `target_not_found` (apagado) | git histórico mostra delete sem rename | Listar para usuário decidir (manter, remover, criar stub). |
| `ambiguous` | Múltiplos arquivos com mesmo basename | Mostrar candidatos, pedir escolha por wikilink. |
| `anchor_not_found` | Arquivo resolve, seção `#Seção` não existe | Listar seções existentes do destino, pedir escolha. |
| `markdown_broken_path` | `[t](caminho/x.md)` inválido | Mesma lógica de `target_not_found`, reconstrói o `[texto](novo-caminho)`. |

## Decisões de UX

- **Aprovação em batch, não link-a-link**. Exceção: ambiguidades e anchor-not-found exigem escolha individual (sem default seguro).
- **Não-destrutivo no apocrypha**: flag `--respect-public-only` pula arquivos cujo path resolve fora do repo público.
- **Dry-run por default**: skill primeiro mostra plano; só edita após "sim/aprovado/proceda".
- **Sem subagentes na v1**: volume típico (dezenas de quebras) cabe em sequencial.

## Tratamento de erros

| Cenário | Comportamento |
|---|---|
| Pasta-alvo não existe | Exit code 2, mensagem clara, sem JSON. |
| `--vault-root` ausente | Auto-detecta: sobe diretórios até achar `.obsidian/`. |
| Arquivo `.md` com encoding inválido | Skip + warning em `warnings[]`, run continua. |
| `git` indisponível | Triagem cai em modo "sem histórico": `target_not_found` vira sempre decisão manual. |
| Permissão de escrita negada | Aborta arquivo, segue os demais, lista no final. |
| Wikilink em code fence | Ignorado por design. |
| Wikilink em frontmatter | Detectado mas marcado `in_frontmatter: true`; correção opcional. |
| Wikilink aninhado `[[a [[b]] c]]` | `reason: malformed`, listado para decisão manual. |
| Múltiplas quebras no mesmo arquivo | Edits aplicados em ordem decrescente de linha. |
| Mesmo wikilink quebrado repete N vezes | Agrupado em decisão única, Edit com `replace_all=true`. |
| Correção exigiria escrever no apocrypha | Bloqueia, reporta violação, deixa para usuário. |

## Testes

Suite em `scripts/test_check_wikilinks.py` (stdlib `unittest`, vault sintético via `tempfile.TemporaryDirectory()`).

Casos mínimos da v1:

1. `test_wikilink_resolves_exact_match`
2. `test_folder_link_without_index_breaks` *(o bug da MOC IA)*
3. `test_folder_link_with_index_resolves`
4. `test_alias_preserved_in_report`
5. `test_anchor_validation_existing_and_missing`
6. `test_markdown_link_internal_broken`
7. `test_ignores_wikilink_in_code_fence`
8. `test_ignores_http_urls_in_markdown_links`
9. `test_ambiguous_target_lists_candidates`
10. `test_fuzzy_suggestion_on_typo`

Comando: `python -m unittest scripts/test_check_wikilinks.py`. Roda em <1s.

A skill em si não tem testes automatizados; o teste funcional é rodar `/verificar-wikilinks 03-Dominios/IA` e validar manualmente.

## Critérios de aceite (v1)

- [ ] `python scripts/check_wikilinks.py 03-Dominios/IA` gera JSON válido.
- [ ] Detecta todas as quebras atuais da MOC IA conferidas manualmente.
- [ ] Tempo < 5s no vault inteiro.
- [ ] Zero dependências externas.
- [ ] `/verificar-wikilinks 03-Dominios/IA` corrige a MOC; re-run reporta zero quebras.
- [ ] Apocrypha intocado (verificável por `git status` no repo apocrypha).
- [ ] Suite de 10 testes passa.

## Estrutura de arquivos final

```
.agents/skills/verificar-wikilinks/
├── SKILL.md
├── scripts/
│   ├── check_wikilinks.py
│   └── test_check_wikilinks.py
└── README.md           (opcional: uso standalone)
```

## Riscos e mitigações

- **Falso-positivo do parser em sintaxe Obsidian exótica** → dry-run obrigatório; usuário aprova plano antes de qualquer Edit.
- **Criar `index.md` quebra layout existente** → template mínimo (só frontmatter + título + lista); usuário pode rejeitar e pedir alternativa.
- **Arquivos com mesmo basename em apocrypha e público** → `--respect-public-only` por default.
- **Wikilink em arquivo gerado** (ex: README auto-gerado) → fora de escopo; usuário deve excluir manualmente do scan.

## Próximos passos

1. Spec self-review (placeholders, contradições, ambiguidade, escopo).
2. User review desta spec.
3. Invocar `superpowers:writing-plans` para plano de implementação.
4. TDD: parser + testes → SKILL.md → dry-run na MOC IA → correção real → deploy Quartz.

## Decisões deferidas (v2+)

- Suporte a verificação de assets (`![[img.png]]`).
- Suporte a wikilinks dentro de Dataview/Bases.
- Modo watch ou hook pre-commit.
- Paralelização por subagentes (se relatórios passarem de ~50 quebras).
- Suporte a outros geradores (Hugo, MkDocs).
