---
name: verificar-wikilinks
description: "Detecta e corrige wikilinks/links markdown quebrados em um vault Obsidian, aplicando a regra do Quartz (folder-link exige index.md). Use quando o usuário pedir /verificar-wikilinks <pasta>, 'checar links quebrados', 'auditar wikilinks', 'consertar links da MOC'."
---

# verificar-wikilinks

Detecta e corrige wikilinks quebrados em pastas do vault, aplicando a regra do
Quartz: `[[Pasta]]` só funciona se a pasta tiver `index.md`.

## Quando usar

- Usuário invoca `/verificar-wikilinks <pasta>` (ex: `03-Dominios/IA`).
- Usuário pede para "checar links quebrados", "auditar wikilinks", "consertar
  links da MOC".
- Após renomear/mover notas, antes de publicar no site Quartz.

## Fluxo

### 1. Receber pasta-alvo

Se o usuário não passou pasta, peça confirmação (sugira a pasta atual). Não
assuma.

### 2. Rodar o detector

```bash
python3 .agents/skills/verificar-wikilinks/scripts/check_wikilinks.py \
  <pasta> --respect-public-only
```

O script imprime o caminho do JSON gerado em `/tmp/wikilinks-report-*.json`.

### 3. Ler o JSON e agrupar por motivo

Leia o JSON. Apresente ao usuário um resumo:

```
Encontrei N quebras em M arquivos. Plano de correção:

folder_without_index (K):
  - [[Anatomia dos LLMs]] em 03-Dominios/IA/index.md:42
    → criar 03-Dominios/IA/Anatomia dos LLMs/index.md
  - [...]

target_not_found (K):
  - [[Velho Nome]] em ...:15
    → git log sugere renomeado para "Novo Nome.md"; atualizar wikilink

ambiguous (K):
  - [[Notas]] tem candidatos:
      1. A/Notas.md
      2. B/Notas.md
    Qual deve ser usado?

anchor_not_found (K):
  - [[Nota#Inexistente]]
    Seções existentes: ... Escolha uma ou peça remoção do anchor.
```

### 4. Estratégia por motivo

| Motivo | Ação default |
|---|---|
| `folder_without_index` | Criar `index.md` na pasta (frontmatter mínimo + título + lista do conteúdo). Alternativa: trocar wikilink para arquivo específico. |
| `target_not_found` | Rodar `git log --diff-filter=R --follow -- '*<basename>*'`. Se houver rename, atualizar automaticamente. Senão, perguntar. |
| `ambiguous` | Perguntar ao usuário qual candidato usar (uma vez por basename). |
| `anchor_not_found` | Listar seções existentes do destino, pedir escolha (ou remover anchor). |
| `markdown_broken_path` | Mesma lógica de `target_not_found`. Atualizar o `[texto](caminho)` inteiro. |
| `malformed` | Não auto-corrigir. Listar e pedir intervenção manual. |

### 5. Pedir aprovação do plano

Espere "sim/aprovado/proceda" antes de qualquer Edit. O usuário pode pedir
ajustes ("não crie index.md para X, troque o wikilink").

### 6. Aplicar correções

- Agrupe Edits por arquivo.
- Aplique em ordem decrescente de linha (preserva offsets).
- Se a mesma quebra aparece N vezes no mesmo arquivo, use `replace_all=true` no
  Edit.
- Para `folder_without_index`, crie o `index.md` com:

  ```markdown
  ---
  title: "<Nome da pasta>"
  created: <YYYY-MM-DD>
  type: moc
  ---

  # <Nome da pasta>

  - [[arquivo-1]]
  - [[arquivo-2]]
  ```

### 7. Verificação — re-rodar o script

Após aplicar tudo, rode o detector de novo. Reporte:

```
Zero quebras restantes em <pasta>.
```

Se ainda houver, liste os resíduos (provavelmente decisões manuais não tomadas).

## Restrições

- **Não escrever no apocrypha**. Se uma correção exigir, bloqueie e reporte.
- **Não auto-corrigir** quando `reason` for `ambiguous`, `anchor_not_found` ou
  `malformed` — exigem decisão humana.
- **Não criar `index.md` automaticamente** se a pasta tem README.md (pode
  haver intenção explícita) — pergunte.

## Arquivos

- Script: `scripts/check_wikilinks.py`
- Testes: `scripts/test_check_wikilinks.py` (`python3 -m unittest`)
- Spec: `docs/superpowers/specs/2026-05-18-verificar-wikilinks-design.md`
