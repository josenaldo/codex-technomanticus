---
title: "Powerlevel10k"
created: 2026-05-19
updated: 2026-05-19
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - shell
  - zsh
  - adepto
  - powerlevel10k
  - prompt
aliases:
  - Powerlevel10k
  - P10k
---

# Powerlevel10k

> [!abstract] TL;DR
> Powerlevel10k é um theme externo pra Zsh com prompt rico (status git, tempo de comando, exit code, etc.) e o famoso `instant prompt`. Configurado pelo wizard `p10k configure` ou editando `~/.p10k.zsh`. Em modo manutenção desde 2024 (atividade do autor caiu drasticamente), mas plugin segue funcional.

---

## O que é / Como funciona

Powerlevel10k (P10k) é um theme pra Zsh criado por Roman Perepelitsa (`romkatv`). O nome é referência ao predecessor Powerlevel9k, do qual mantém compatibilidade retroativa de variáveis de config (`POWERLEVEL9K_*`). O foco do P10k é **velocidade**, **customização** e **out-of-the-box experience** — o prompt é responsivo mesmo com 70+ segmentos ativos.

O P10k não substitui o Zsh nem o Oh-My-Zsh: é um theme que sobrescreve as variáveis `PROMPT` e `RPROMPT`. Pode ser carregado via OMZ (como `ZSH_THEME`) ou manualmente (via `source`). A instalação manual via clone direto é a recomendada pelo projeto — dá controle total de versão e evita conflitos com o sistema de themes do OMZ.

O P10k inclui mais de 70 segmentos built-in: diretório atual, status git (branch, dirty, commits à frente/atrás, stash), exit code do último comando, tempo de execução do comando, versão de linguagens (Python, Node, Go, Rust, Java, etc.), contexto AWS/GCP/Azure, Kubernetes context, hora, carga do sistema, bateria, e mais. Todos os segmentos são opcionais e configurados por arrays no `~/.p10k.zsh`.

> [!warning] Modo manutenção desde 2024-07
> O projeto tem suporte muito limitado: sem novas features, maioria dos bugs não será corrigida. A última release ativa foi em julho de 2024. O plugin segue funcional, mas não evolui. Alternativas ativas: **Starship** (cross-shell, escrito em Rust) e **Pure** (minimalista, Sindre Sorhus).

### Instalação canônica

```zsh
# Clone (uma vez)
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k

# No .zshrc, source depois de OMZ (ou no lugar de ZSH_THEME)
source ~/powerlevel10k/powerlevel10k.zsh-theme

# O wizard cria ~/.p10k.zsh; source para aplicar
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
```

O `--depth=1` faz um clone raso (shallow clone) — traz apenas o commit mais recente, sem todo o histórico. É suficiente para uso e economiza espaço em disco e tempo de download.

A alternativa via OMZ theme (`ZSH_THEME="powerlevel10k/powerlevel10k"`) existe — e exige clonar pra `~/.oh-my-zsh/custom/themes/powerlevel10k/`. Mas misturar os dois mecanismos duplica o carregamento — decidir um caminho e manter apenas ele.

> [!tip] Ordem de source no `.zshrc`
> O bloco do instant prompt vai no topo. O source do OMZ (`source $ZSH/oh-my-zsh.sh`) vem depois. O source do P10k (`source ~/powerlevel10k/powerlevel10k.zsh-theme`) vem depois do OMZ. O `source ~/.p10k.zsh` vem por último — carrega a configuração gerada pelo wizard.

### Instant prompt

O instant prompt é o diferencial de performance do P10k. Funciona cacheando o prompt renderizado na sessão anterior e exibindo-o **antes** de o `.zshrc` terminar de carregar. O efeito: o prompt aparece imediatamente ao abrir o terminal, enquanto plugins continuam inicializando em background.

O cache fica em `${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-<usuario>.zsh`. Na primeira vez que você abre o terminal após instalar ou reconfigurar o P10k, não há cache — o prompt normal é exibido. A partir da segunda abertura, o cache é usado e o prompt aparece em milissegundos.

O bloco do instant prompt **deve ficar no TOPO do `.zshrc`**, antes de qualquer outra linha:

```zsh
# Bloco do instant prompt — DEVE ser a primeiríssima coisa do .zshrc
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi
```

Valores da variável `POWERLEVEL9K_INSTANT_PROMPT`:

| Valor | Comportamento |
|---|---|
| `verbose` (default) | Ativa instant prompt e avisa se algo no `.zshrc` produz output antes do prompt |
| `quiet` | Ativa instant prompt, sem avisos |
| `off` | Desliga instant prompt (use quando init produz output legítimo e inevitável) |

### Wizard `p10k configure`

O wizard é a forma oficial de configurar o P10k. Executa uma sequência de perguntas visuais, com preview ao vivo de como o prompt vai ficar após cada escolha:

1. **Charset** — o wizard testa se o terminal renderiza Powerline glyphs e Nerd Font v3. Você confirma o que viu. Se a fonte não suporta, sugere instalar MesloLGS NF.
2. **Style** — rainbow / lean / classic / pure (preview de cada opção)
3. **Unicode version** — v1 ou v3 (Nerd Fonts v3 tem mais glyphs mas exige font mais recente)
4. **Prompt color** — light, dark ou varia com o terminal
5. **Time format** — 12h, 24h, ou sem horário no prompt
6. **Separators** — tipo de divisor entre segmentos (powerline ``, round ``, blunt `|`, etc.)
7. **Prompt heads/tails** — estilo das pontas dos segmentos
8. **Lines** — 1 ou 2 linhas (prompt 2-linha libera mais espaço pro comando)
9. **Frame** — nenhum, top, bottom, ou full (bordas decorativas)
10. **Connection** — estilo de conexão entre segmentos multi-linha
11. **Icons** — muitos, poucos, ou nenhum
12. **Prompt flow** — compact ou dispersed (espaçamento entre segmentos)
13. **Transient prompt** — se ativa ou não; se sim, qual modo
14. **Instant prompt** — se ativa ou não; se sim, `verbose` ou `quiet`

Output: `~/.p10k.zsh`, arquivo de ~1800 linhas comentadas. Rodar `p10k configure` novamente sobrescreve o arquivo.

> [!info] O wizard testa o terminal
> Antes de cada pergunta de glyph/charset, o wizard exibe o símbolo e pergunta "Does this look like X?". Isso garante que as opções escolhidas vão funcionar no terminal específico — não é apenas estética, é compatibilidade.

### Estrutura do `~/.p10k.zsh`

O arquivo gerado pelo wizard tem estrutura previsível e ~1800 linhas — a maioria são comentários que explicam cada opção. É seguro editá-lo diretamente; o wizard sobrescreve tudo se você rodar `p10k configure` novamente.

- **Header** — comentários com instruções e disclaimer gerado pelo wizard; avisa que o arquivo é gerado e pode ser sobrescrito
- **Elementos do prompt:**
  ```zsh
  typeset -g POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(
    dir                    # diretório atual
    vcs                    # status git
    newline                # quebra de linha (prompt 2-linha)
    prompt_char            # caractere de prompt (❯ ou similar)
  )
  typeset -g POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(
    status                 # exit code do último comando
    command_execution_time # tempo de execução
    background_jobs        # jobs em background
    time                   # horário atual
  )
  ```
- **Cores por segmento** — variáveis `POWERLEVEL9K_<SEG>_BACKGROUND` e `POWERLEVEL9K_<SEG>_FOREGROUND` aceitam valores ANSI 0-255. `typeset -g` garante que são globais, disponíveis mesmo em subshells.
- **Thresholds de segmento** — ex: `POWERLEVEL9K_COMMAND_EXECUTION_TIME_THRESHOLD=3` exibe o tempo de execução só se o comando levou mais que 3 segundos
- **Condicionais de contexto** — `POWERLEVEL9K_<SEG>_SHOW_ON_COMMAND` mostra um segmento só quando certo comando está ativo (ex: mostrar versão do Python só ao rodar scripts Python)
- **Funções custom** — `prompt_<nome>()` pra segmentos personalizados, adicionados ao array de elements

> [!note] Prefixo `POWERLEVEL9K_`
> Todas as variáveis do P10k usam o prefixo `POWERLEVEL9K_` (com 9, não 10) — herança do Powerlevel9k. Isso garante retrocompatibilidade: configs do Powerlevel9k funcionam no P10k sem alteração.

### Modos visuais

| Modo | Característica |
|---|---|
| **rainbow** | Backgrounds coloridos por segmento — visual mais chamativo; cada segmento tem sua própria cor de fundo |
| **lean** | Sem backgrounds, texto colorido apenas — visual limpo e moderno |
| **classic** | Único background neutro — estilo powerline tradicional; separadores angulares |
| **pure** | Imita o tema Pure (Sindre Sorhus) — minimalista, sem ícones, sem backgrounds |

Todos os modos (exceto pure) são funcionalmente equivalentes: mostram as mesmas informações com visual diferente. O modo `pure` é deliberadamente mais limitado em informação — segue a filosofia do Pure original.

Os separadores entre segmentos (` `, `│`, `>`, `⟩`, etc.) são configuráveis independentemente do style. O wizard oferece opções de separadores mas você pode trocar editando `POWERLEVEL9K_LEFT_SEGMENT_SEPARATOR` e `POWERLEVEL9K_RIGHT_SEGMENT_SEPARATOR` no `~/.p10k.zsh`.

### Transient prompt

Com transient prompt ativo, ao pressionar Enter, o prompt da linha atual "encolhe" pra uma versão mínima — só o caractere de prompt e o comando. Os prompts anteriores no scrollback também são reduzidos. Libera espaço visual considerável em prompts de duas linhas.

O prompt encolhido mantém apenas o símbolo de prompt (`❯`) e o comando digitado — sem path, sem git, sem tempo, sem ícones. Em prompts de duas linhas, o efeito é especialmente marcante: ao invés de cada comando ocupar 2 linhas no scrollback, ocupa apenas 1.

Configuração via `POWERLEVEL9K_TRANSIENT_PROMPT`:

- `off` (default) — sem transient prompt; cada prompt permanece com a forma completa no scrollback
- `same-dir` — encolhe prompts de outros diretórios; quando você está no mesmo diretório, mantém detalhado
- `always` — encolhe todos os prompts anteriores sem exceção

> [!warning] `always` e o scrollback
> Com `always`, o scrollback perde contexto: não dá mais pra ver em qual diretório cada comando foi executado. Para sessões longas com navegação entre pastas, `same-dir` é mais útil.

### Nerdfont

Nerd Fonts são fonts patched com glyphs adicionais: ícones de Git, distros Linux, dev tools (Python, Node, Docker, Kubernetes), devicons. O projeto Nerd Fonts pega fontes existentes e inclui milhares de glyphs extras na faixa Unicode privada (PUA — Private Use Area, U+E000 a U+F8FF e extensões).

O P10k recomenda **MesloLGS NF** — versão customizada do Meslo LGS patched especificamente pra P10k, com glyphs alinhados pra funcionar bem com os separadores e ícones do tema.

Sem nerdfont configurada no terminal, o P10k tenta exibir glyphs que o terminal não consegue renderizar, resultando em caixas `□` ou `?` no lugar dos ícones.

Download: as 4 variantes (Regular, Bold, Italic, Bold Italic) disponíveis no repo do P10k em `font/`. Instalação:

```zsh
# Criar diretório de fonts locais (se não existir)
mkdir -p ~/.local/share/fonts

# Copiar as 4 variantes baixadas
cp MesloLGS\ NF\ *.ttf ~/.local/share/fonts/

# Atualizar cache de fonts (Linux)
fc-cache -fv
```

Após instalar, apontar o terminal pra "MesloLGS NF" nas preferências. Em caso de dúvida sobre a font, o wizard `p10k configure` testa o rendering com glyphs de referência antes de pedir a escolha de charset.

### `.zshrc` — ordem de carregamento

Um `.zshrc` bem ordenado com P10k tem esta sequência canônica:

```zsh
# 1. Instant prompt — PRIMEIRO de tudo
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# 2. Variáveis de ambiente e exports simples (não produzem output)
export EDITOR=nvim
export PATH="$HOME/bin:$PATH"

# 3. Oh-My-Zsh (se em uso)
export ZSH="$HOME/.oh-my-zsh"
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
source $ZSH/oh-my-zsh.sh

# 4. Ferramentas que produzem output (NVM, ASDF, etc.) — depois do instant prompt
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"

# 5. Source do P10k theme (depois do OMZ)
source ~/powerlevel10k/powerlevel10k.zsh-theme

# 6. Config do P10k — por último
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
```

> [!warning] Ferramentas com output e instant prompt
> NVM, ASDF, SDKMan e similares frequentemente printam mensagens ao inicializar. Se ficarem entre o bloco do instant prompt e o final do `.zshrc`, o P10k avisa (com `verbose`) ou silencia (com `quiet`). A solução mais limpa é colocar essas linhas o mais tarde possível no `.zshrc`, ou silenciar o output delas.

### gitstatus — o motor por trás do git info

O segmento `vcs` do P10k usa o `gitstatus` — uma biblioteca em C++ (com bindings Zsh) que consulta o estado do repositório git de forma assíncrona e sem bloquear o prompt. É por isso que o prompt do P10k permanece rápido mesmo em repos grandes: o status git é calculado em background e o prompt é atualizado quando a resposta chega.

O binário `gitstatusd` fica em `~/.cache/gitstatus/` e é baixado automaticamente na primeira vez que o P10k é carregado. Se o binário não existir ou for incompatível com a arquitetura, o P10k recorre ao `git` tradicional (mais lento).

---

## Na prática

### Editar segmento de cor

Abrir `~/.p10k.zsh`, localizar a variável do segmento (ex: `POWERLEVEL9K_DIR_BACKGROUND`), mudar o valor (número ANSI 0-255). Aplicar sem abrir novo shell:

```zsh
source ~/.p10k.zsh
```

Dica: `POWERLEVEL9K_DIR_BACKGROUND=4` usa o azul do esquema de cores do terminal. Valores 0-7 são cores ANSI padrão; 8-255 são cores da paleta extendida 256-color. Para ver a paleta 256-color no terminal:

```zsh
for i in {0..255}; do print -Pn "%K{$i}  %k%F{$i}${(l:3::0:)i}%f " ${${(M)$((i%6)):#3}:+$'\n'}; done
```

### Adicionar segmento custom

Definir a função no `~/.p10k.zsh` (ou em arquivo separado sourced antes):

```zsh
function prompt_meu_segmento() {
  local info='alguma informação'
  [[ -n $info ]] && p10k segment -f 3 -t "$info"
}
```

Adicionar `meu_segmento` ao array `POWERLEVEL9K_LEFT_PROMPT_ELEMENTS` ou `POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS`. O prefixo `prompt_` é obrigatório — o P10k busca funções com esse padrão.

O `p10k segment` recebe flags: `-f <cor>` (foreground), `-b <cor>` (background), `-t <texto>` (conteúdo), `-i <ícone>` (glyph). Se a função não chamar `p10k segment`, o segmento não aparece — é como um `return` implícito que omite o segmento.

### Ocultar ou exibir segmento condicionalmente

Muitos segmentos têm variáveis `_SHOW_ON_COMMAND` que ativam o segmento apenas quando certos comandos estão rodando. Exemplo: mostrar versão do Go apenas quando estiver em projetos Go:

```zsh
# No ~/.p10k.zsh — ocultar go por default, mostrar só quando relevante
typeset -g POWERLEVEL9K_GO_VERSION_PROJECT_ONLY=true
```

Para remover completamente um segmento: deletar o nome do array `POWERLEVEL9K_LEFT_PROMPT_ELEMENTS` ou `POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS` no `~/.p10k.zsh`.

### Trocar de modo visual

Rodar `p10k configure` e passar pelo wizard novamente. Não há variável única que troca o "style" sem reconfigurar — o wizard reescreve o arquivo inteiro com todas as variáveis coerentes pro estilo escolhido.

> [!tip] Backup antes de reconfigurar
> O wizard sobrescreve `~/.p10k.zsh` sem aviso. Se você tem customizações manuais, faça backup antes: `cp ~/.p10k.zsh ~/.p10k.zsh.bak`

### Diagnosticar problemas de performance

```zsh
p10k diagnose
```

Gera relatório de diagnóstico com tempos de cada segmento, configurações ativas e potenciais problemas. Útil quando o prompt parece mais lento que o esperado — identifica qual segmento está demorando.

Para ver o tempo de cada segmento individualmente em modo verboso:

```zsh
p10k diagnose --verbose
```

### Recarregar configuração sem fechar o terminal

```zsh
source ~/.p10k.zsh
```

Aplica mudanças feitas diretamente no `~/.p10k.zsh` sem precisar abrir novo shell. O `source` do P10k recarrega as variáveis e redesenha o prompt imediatamente.

> [!tip] Verificar variável atual
> Para checar o valor atual de uma variável do P10k antes de editar:
> ```zsh
> echo $POWERLEVEL9K_DIR_BACKGROUND
> ```
> Se retornar vazio, a variável usa o valor default interno do tema.

### Comparar a config gerada com o default

Quando você quer saber o que o wizard adicionou ou mudou, é útil ter uma cópia baseline. Uma estratégia:

```zsh
# Antes de configurar: salvar o default gerado pelo wizard
cp ~/.p10k.zsh ~/.p10k.zsh.default

# Após customizações:
diff ~/.p10k.zsh.default ~/.p10k.zsh
```

Isso facilita reverter para o estado do wizard se customizações manuais gerarem problemas.

### Trocar a font no terminal

Depende do emulador:

- **GNOME Terminal:** Preferences → Profile → Text → Custom Font → "MesloLGS NF"
- **Kitty / Alacritty:** variável `font_family = MesloLGS NF` no arquivo de config
- **iTerm2 (macOS):** Preferences → Profiles → Text → Font → "MesloLGS NF"
- **VS Code integrated terminal:** `terminal.integrated.fontFamily: "MesloLGS NF"` no `settings.json`

### Status git no P10k — símbolos de referência

O segmento `vcs` exibe símbolos para cada estado do repositório:

| Símbolo | Significado |
|---|---|
| `⇣N` | N commits atrás do remote |
| `⇡N` | N commits à frente do remote |
| `*N` | N stashes |
| `~N` | N merge conflicts |
| `+N` | N arquivos staged |
| `!N` | N modificações unstaged |
| `?N` | N arquivos untracked |

---

## Armadilhas

### Armadilha 1 — P10k em modo manutenção desde julho de 2024

**Causa:** O autor reduziu drasticamente a atividade no projeto. O suporte do autor ficou muito limitado; contributors ocasionais fazem fixes pontuais, mas o projeto não evolui ativamente.

**Sintoma:** PRs e issues ficam sem resposta; bugs conhecidos não têm previsão de fix; sem novas features.

**Como detectar:** Verificar a data do último commit no branch `master` do repositório e a nota "THE PROJECT HAS VERY LIMITED SUPPORT" no README.

**Solução:** Para quem quer um theme em evolução ativa, as alternativas são:
- **Starship** — cross-shell (Bash, Zsh, Fish, PowerShell e mais), escrito em Rust, configurado por `~/.config/starship.toml`. Evolução ativa, comunidade grande.
- **Pure** — Zsh-only, minimalista, foco em velocidade e simplicidade, por Sindre Sorhus. Sem wizard, sem segmentos — prompt deliberadamente enxuto.

P10k ainda é válido para quem já tem a configuração estabilizada — ele não vai quebrar por estar em manutenção.

### Armadilha 2 — `INSTANT_PROMPT=verbose` reclama de output no init

**Causa:** Ferramentas como NVM, SDKMan, Conda, ASDF e similares imprimem mensagens durante inicialização (`Now using node v20.x.x`, por exemplo). O instant prompt captura o estado do terminal antes dessas mensagens — quando elas chegam depois, o P10k detecta output inesperado e avisa.

**Sintoma:** Mensagem de aviso em vermelho no terminal ao abrir o shell, tipo `[powerlevel10k] instant prompt: ...`.

**Como detectar:** Ler a mensagem de aviso — ela indica qual parte do `.zshrc` produziu output. Alternativamente, `POWERLEVEL9K_INSTANT_PROMPT=off` e ver quais mensagens aparecem na ordem natural.

**Solução (escolher uma):**
- Mover as linhas que produzem output pra ANTES do bloco do instant prompt no `.zshrc`
- Silenciar a saída na fonte (ex: `export NVM_SILENT=true` ou redirecionar stderr/stdout)
- Usar `POWERLEVEL9K_INSTANT_PROMPT=quiet` — mantém instant prompt, sem avisos
- Usar `POWERLEVEL9K_INSTANT_PROMPT=off` — desliga o instant prompt completamente

### Armadilha 3 — Nerdfont não configurada no terminal

**Causa:** MesloLGS NF (ou outra nerdfont) não instalada, ou instalada mas não selecionada nas preferências do emulador de terminal.

**Sintoma:** Ícones do P10k aparecem como `□`, `?`, ou caracteres estranhos no lugar dos glyphs esperados.

**Como detectar:** Rodar `echo '❯'` no terminal. Se aparecer `❯`, UTF-8 está OK mas a font não tem o glyph — o problema é de font, não de locale. Se aparecer `❯` literal, o problema é de locale (UTF-8 não ativo).

**Solução:** Instalar MesloLGS NF (as 4 variantes do repo do P10k), apontar o terminal pra essa font nas preferências, reabrir o terminal. Rodar `p10k configure` e selecionar "Nerd Fonts v3" no passo de charset.

### Armadilha 4 — `TRANSIENT_PROMPT=always` confunde o scrollback

**Causa:** Com `always`, todos os prompts anteriores — inclusive de outros diretórios — são reescritos como prompt mínimo. Se você rodar um comando em `/projetos/foo`, scrollar pra cima e tentar identificar em qual diretório estava, o prompt não vai mostrar mais o path.

**Sintoma:** Scrollback fica uniforme — todos os prompts são idênticos (só `❯`), sem informação contextual.

**Como detectar:** Abrir o terminal, rodar alguns comandos em diretórios diferentes, pressionar Enter, scrollar pra cima — todos os prompts antigos viram `❯ ` sem context.

**Solução:** Usar `POWERLEVEL9K_TRANSIENT_PROMPT=same-dir` em vez de `always`. Com `same-dir`, prompts de diretórios diferentes mantêm o context completo; só encolhe quando o diretório atual é o mesmo. Alternativamente, `off` desliga completamente.

### Armadilha 5 — Duplicação ao misturar `ZSH_THEME` com `source` manual

**Causa:** Configurar `ZSH_THEME="powerlevel10k/powerlevel10k"` no `.zshrc` E fazer `source ~/powerlevel10k/powerlevel10k.zsh-theme` carrega o theme duas vezes — o OMZ faz o source pelo sistema de themes, e o `source` manual faz de novo.

**Sintoma:** Prompt pode piscar, variáveis de config são sobreescritas na ordem errada, comportamento imprevisível.

**Como detectar:** Procurar por `ZSH_THEME` e `source .*/powerlevel10k` no `.zshrc` — se ambos existem, há duplicação.

**Solução:** Escolher um mecanismo e remover o outro. A instalação manual via `source` (sem `ZSH_THEME`) é a recomendada pelo projeto para ter controle total de versão.

---

## Contexto: P10k vs Starship vs Pure

Se o P10k está em manutenção, vale comparar as alternativas ativas para decidir se migrar faz sentido:

| | **Powerlevel10k** | **Starship** | **Pure** |
|---|---|---|---|
| **Shell** | Zsh only | Bash, Zsh, Fish, PowerShell, e mais | Zsh only |
| **Linguagem** | Zsh script | Rust | Zsh script |
| **Config** | `~/.p10k.zsh` (gerado por wizard) | `~/.config/starship.toml` | `zstyle` no `.zshrc` |
| **Wizard** | Sim (`p10k configure`) | Não | Não |
| **Instant prompt** | Sim (built-in) | Não (shell init controls speed) | Não |
| **Nerdfont** | Necessária pra ícones | Necessária pra ícones | Não usa ícones |
| **Manutenção** | Limitada desde 2024-07 | Ativa | Ativa |
| **Filosofia** | Rico e configurável | Cross-shell, rápido, minimalista | Minimalista, "fique fora do caminho" |

Para quem quer migrar sem perder features: Starship. Para quem quer ir na direção oposta (menos prompt, mais foco): Pure.

---

## Em inglês

- **prompt** — *prompt*. "The shell's prompt is rendered before each command; P10k replaces `PROMPT` and `RPROMPT` with rich, configurable output."
- **instant prompt** — *instant prompt*. "Powerlevel10k's instant prompt caches the rendered prompt and displays it before `.zshrc` finishes loading, eliminating perceived startup lag."
- **transient prompt** — *transient prompt*. "When transient prompt is active, previously rendered prompts shrink to a minimal form on Enter, reducing scrollback clutter."
- **theme** — *theme*. "A Zsh theme overrides the `PROMPT` and `RPROMPT` variables; P10k is an external theme loaded independently of Oh-My-Zsh's theme system."
- **segmento** — *segment*. "Each segment is an independent unit in the P10k prompt (git status, directory, execution time); toggled by editing `POWERLEVEL9K_LEFT_PROMPT_ELEMENTS`."
- **font patched** — *patched font*. "Nerd Fonts are standard typefaces patched to include thousands of additional glyphs for developer tooling and terminal icons."
- **ícone** — *icon*. "Terminal icons in P10k are rendered as Unicode code points from the Nerd Fonts glyph range, typically U+E000–U+F8FF."
- **Unicode** — *Unicode*. "Unicode is the character encoding standard that assigns code points to every character; P10k uses Unicode glyphs for prompt symbols and icons."
- **glyph** — *glyph*. "A glyph is the visual representation of a character or symbol; Nerd Fonts add thousands of glyphs not present in standard typefaces."
- **customização** — *customization*. "P10k customization is done by editing `~/.p10k.zsh`—generated by the wizard—and reloading it with `source ~/.p10k.zsh`."
- **wizard** — *wizard*. "The `p10k configure` wizard guides prompt setup through a series of visual questions, generating a ready-to-use `~/.p10k.zsh` without manual editing."
- **shallow clone** — *shallow clone*. "A `git clone --depth=1` fetches only the latest commit without full history, used when installing P10k to reduce disk usage and download time."

---

## Veja também

- [[04 - Oh-My-Zsh — anatomia e plugins essenciais]] — OMZ vs theme externo
- [[10 - Plugins, themes e custom no OMZ]] — escrever theme próprio
- [[03-Dominios/Terminal/Shell/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Powerlevel10k|Powerlevel10k]], [[Dicionário do Terminal#Prompt|prompt]], [[Dicionário do Terminal#Instant prompt|instant prompt]], [[Dicionário do Terminal#Transient prompt|transient prompt]], [[Dicionário do Terminal#Nerdfont|nerdfont]]

---

## Referências

- P10k repo — <https://github.com/romkatv/powerlevel10k>
- Starship (alternativa cross-shell) — <https://starship.rs/>
- Pure (alternativa minimalista) — <https://github.com/sindresorhus/pure>
