# Próxima sessão — Spec + Plano + Execução do Galho 2 (Shell) da trilha Terminal

> **Este arquivo é descartável.** Apagar quando a sessão começar — é só o prompt-bootstrap pra retomar o trabalho.

---

## Prompt pra próxima sessão

Cole isto no início da próxima sessão de Claude Code:

---

Continue a trilha **Terminal** do Codex. **Galho 1 (Editor)** foi entregue em 2026-05-19 (commits `703f303` até `8704df1`). Agora **Galho 2 — Shell** (Zsh + Oh-My-Zsh + Powerlevel10k).

### Roadmap relevante (já existem)

- `docs/superpowers/specs/2026-05-18-trilha-terminal-design.md` — roadmap macro da trilha (7 galhos, 3 fases por galho, padrão tronco/galho)
- `docs/superpowers/specs/2026-05-19-terminal-editor-design.md` — spec do galho 1 (Editor) — use como **referência de formato** (seções, rubrica de nota, dicionário, etc.)
- `docs/superpowers/plans/2026-05-19-terminal-editor-execution.md` — plano que executei pro galho 1 (21 tasks, formato proven)
- `03-Dominios/Terminal/index.md` — tronco da trilha (já tem wikilink ativo pro Editor; outros galhos como bullet de texto)
- `03-Dominios/Terminal/Dicionário do Terminal.md` — dicionário trilha-wide (42 verbetes do Editor; vai crescer com Shell)
- `03-Dominios/Terminal/Editor/` — exemplo concreto de galho entregue (14 arquivos)

### Mapa das 8 notas do galho 2 (do roadmap §Galho 2)

**Iniciado (3 notas)**

| # | Nota |
|---|------|
| 01 | Zsh vs Bash — o que muda, por que migrar |
| 02 | Zsh essencial — aliases, funções, opts (setopt) |
| 03 | Oh-My-Zsh — anatomia + plugins essenciais (git, z, fzf-tab, autosuggestions, syntax-highlighting) |

**Adepto (3 notas)**

| # | Nota |
|---|------|
| 04 | Powerlevel10k — instant prompt, config wizard, customização |
| 05 | Completion system (compsys) — modelo mental |
| 06 | ZLE — Zsh Line Editor, key bindings, widgets |

**Magus (2 notas)**

| # | Nota |
|---|------|
| 07 | Globbing avançado e parameter expansion |
| 08 | Plugins, themes e custom no OMZ — escrevendo o seu |

Total: 8 notas + MOC + atualizações no Dicionário do Terminal (verbetes próprios do Shell). Pasta destino: `03-Dominios/Terminal/Shell/`.

### Fluxo esperado (igual ao galho 1)

1. **Brainstorming** — `superpowers:brainstorming` para alinhar escopo, fontes primárias por nota, "Em inglês", versões assumidas (Zsh 5.9+? OMZ master? P10k atual). Importante: cobrir setup real do user — perguntar se ele já usa OMZ + P10k ou se a config é vanilla.
2. **Spec** — salvar em `docs/superpowers/specs/YYYY-MM-DD-terminal-shell-design.md` seguindo o formato do spec do Editor (seções 1-15). Tamanho-alvo: ~500-700 linhas.
3. **Pedir review** — usuário aprova antes do plano.
4. **Writing-plans** — `superpowers:writing-plans` produz `docs/superpowers/plans/YYYY-MM-DD-terminal-shell-execution.md`. Tasks: Task 0 pré-flight → esqueletos (Shell/index.md + atualizar Dicionário se houver bloco novo) → 8 tasks de nota → finalização → ativar wikilink no tronco → validação. Total esperado: ~12-15 tasks, ~1800-2000 linhas.
5. **Execução** — `superpowers:subagent-driven-development`. Sequential (dicionário é estado compartilhado). Cada nota: implementer sonnet → spot-check pelo controller → commit.

### Restrições absolutas (memórias do user — verificar antes)

- **Sem fabricação** — nada de "eu uso isto no meu projeto X". Use "padrão observado na comunidade Zsh", hipotéticos explícitos, etc.
- **Sem `Co-Authored-By: Claude`** em commits. Sem `--no-verify`.
- **Isolamento público** — Shell é público, nenhuma menção a apocrypha.
- **Não remover `index.md` do Quartz** — tronco `Terminal/index.md` é editado (ativar wikilink Shell), nunca removido.

### Pontos abertos pra perguntar no brainstorm

- Setup atual do user: OMZ + P10k? Ou outra coisa (starship, prezto)? **Importante pra calibrar o caminho primário** — se ele usa OMZ+P10k, esse é o foco. Se está em prezto, repensar.
- Versão de Zsh: macOS bundle (5.9) ou Linux package (varia)?
- O dicionário do Terminal recebe novos verbetes — possíveis: shell, builtin, alias, function, glob, parameter expansion, compsys, ZLE, widget, prompt, instant prompt, theme, plugin OMZ, etc.

### Critério de pronto

- 9 arquivos em `03-Dominios/Terminal/Shell/` (8 notas + index)
- ≥10 verbetes novos no Dicionário do Terminal
- Tronco `Terminal/index.md` com wikilink ativo pro Shell
- Todos `publish: true`
- Build local do site passa (ou validação manual via Obsidian)
- Commits sem `Co-Authored-By`

### Galho subsequente

Após Shell, o roadmap (`§Ordem sugerida de execução`) recomenda **galho 3 — Multiplexer (Zellij)**. Mas o usuário pode pular ordem.

---

**Quando começar:** apague este arquivo (`docs/superpowers/specs/PROXIMA-SESSAO-galho-2-shell.md`), inicie a nova sessão e cole o prompt acima.
