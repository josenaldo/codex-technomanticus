---
title: "Refactoring multi-arquivo"
created: 2026-05-24
updated: 2026-05-24
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - workflow
  - magus
  - refactoring
  - playbook
aliases:
  - Refactoring multi-file
  - rg quickfix LSP
---

# Refactoring multi-arquivo

> [!abstract] TL;DR
> Playbook para refactor que toca 10+ arquivos. Pipeline: `rg <padrão>` pra mapear ocorrências → carregar em nvim quickfix → `:cdo s/X/Y/gc` pra editar em lote OU LSP rename pra refactor type-aware. Validar com `:cnext`/`:cprev`. Cuidado: `:cdo` quando mudanças invalidam matches subsequentes. LSP rename é seguro pra símbolos; rg+quickfix é flexível mas requer atenção.

## O que é / Como funciona

### Por que refactor multi-arquivo merece técnica

Find/replace global no IDE parece simples mas é caro mentalmente: você perde controle fino de quais ocorrências mudar, não tem como confirmar match a match sem parar o fluxo, e o histórico de undo fica fragmentado por arquivo. O nvim quickfix resolve exatamente isso — uma lista centralizada de matches navegável e editável em lote.

A estratégia ótima combina três ferramentas:

- **rg** (ripgrep): descoberta rápida — o que existe, onde, quantas vezes
- **nvim quickfix + `:cdo`**: edição em lote com controle fino (confirm por match)
- **LSP rename**: segurança semântica — renomeia símbolo rastreando todas as referências no grafo do projeto

Nenhuma ferramenta substitui as outras. LSP rename não toca comentários ou strings; rg não entende escopo; o quickfix não sabe se um match é falso positivo. Combinados, você tem cobertura total.

### Quickfix — o que é

O quickfix é uma lista global do nvim de "localizações": cada entrada contém `file:line:col + texto`. Funciona como fila de trabalho persistente durante a sessão.

Como é populado:
- `:grep <padrão>` / `:vimgrep` — busca no projeto
- `:make` — erros de compilação
- LSP diagnostics — erros e warnings do language server
- Telescope (`<C-q>`) — envia seleção do live_grep pro quickfix

Como navegar:
- `:copen` — abre janela do quickfix
- `:cclose` — fecha
- `:cnext` / `:cprev` — próximo / anterior match
- `:cfirst` / `:clast` — primeiro / último

Como editar em lote:
- `:cdo <cmd>` — executa `<cmd>` em cada match da lista (um por um)
- `:cfdo <cmd>` — executa `<cmd>` uma vez por arquivo da lista (mais seguro pra substituições)

### Três fluxos principais

| Fluxo | Quando usar | Cobertura |
|---|---|---|
| **rg + quickfix + `:cdo`** | Strings, comentários, logs, qualquer texto | Qualquer arquivo, qualquer texto |
| **LSP rename** | Renomear função, variável, tipo, método | Só símbolos reconhecidos pelo LSP |
| **Telescope live_grep + quickfix** | Quando precisa pré-filtrar matches visualmente antes de editar | Qualquer arquivo, com curadoria manual |

### Quando usar cada fluxo

- **Renomear função/variável/tipo** → LSP rename (`<leader>rn`): semântico, seguro, instantâneo
- **Mudar string/comentário/log message em N arquivos** → rg + quickfix + `:cdo s/X/Y/gc`
- **Refactor estrutural (mudar shape de objeto, migrar API)** → manual nvim com substituições Telescope-driven ou quickfix por etapas
- **Cross-language refs** (TypeScript renomeia mas JSON/YAML ainda tem o nome antigo) → rg + quickfix pra varredura residual após LSP rename

---

## Na prática

### Fluxo rg + quickfix

```bash
# Fora do nvim — exploratório
rg "OldName" --stats
rg "OldName" --files-with-matches

# Dentro do nvim
:grep "OldName"               # carrega matches no quickfix (usa ripgrep se configurado)
:copen                        # abre janela quickfix
:cdo s/OldName/NewName/gc     # substitui com confirmação em CADA match
:cfdo update                  # salva todos arquivos modificados (só salva se mudou)
```

Flags do `s///gc`:
- `g` — todas as ocorrências na linha (não só a primeira)
- `c` — pede confirmação: `y` (sim), `n` (não), `a` (todos restantes), `q` (parar)

### Fluxo LSP rename

```text
# Cursor posicionado sobre o símbolo
<leader>rn        (LazyVim default)
# Digite novo nome → Enter
# Todos os usos no projeto são atualizados imediatamente
```

Funciona melhor em projetos com LSP bem configurado (tsserver, pyright, rust-analyzer, etc.). Abre um buffer de rename — você digita o novo nome e confirma.

### Fluxo Telescope live_grep + quickfix

```text
:Telescope live_grep
# Buscar o padrão
# Selecionar matches desejados com <Tab>
# <C-q> → envia seleção pro quickfix
:copen
:cdo s/OldName/NewName/gc
```

Útil quando o padrão de busca retorna muitos false positives e você quer escolher manualmente quais matches processar antes de rodar o `:cdo`.

### Pipeline avançado: rg → fzf → quickfix

```bash
# Selecionar matches manualmente via fzf antes de abrir no nvim
rg "padrão" --vimgrep | fzf -m | nvim -q /dev/stdin

# Alternativa: salvar lista filtrada e carregar no nvim
rg "padrão" --vimgrep | fzf -m > /tmp/matches.txt
nvim -q /tmp/matches.txt
```

Esse pipeline é útil em contexto de shell puro, sem Telescope. O formato `--vimgrep` (`file:line:col:text`) é diretamente consumível pelo quickfix via `-q`.

### Validar o refactor

```bash
# Após refactor, rodar testes
npm test        # ou pytest, cargo test, go test ./...

# Verificar que não sobrou nada do nome antigo
rg "OldName" --stats

# Ver diff total antes de commit
lazygit
```

Dentro do nvim, você pode também rodar `:grep OldName` de novo — se o quickfix voltar vazio, o refactor foi completo.

---

## Armadilhas

1. **`:cdo s/X/Y/g` sem flag `c`**
   - **Causa:** querer "terminar logo" leva a rodar `:cdo s/X/Y/g` sem confirmação.
   - **Sintoma:** todos os matches são trocados inclusive false positives (comentários com o nome em contexto diferente, strings que coincidem por acaso).
   - **Como detectar:** rodar `:grep OldName` antes e ver no `:copen` se há matches suspeitos.
   - **Solução:** **sempre usar flag `c`** em refactor não-trivial. O custo de confirmar um a um é baixo; o custo de reverter edições em 20 arquivos é alto.

2. **Match em contexto indesejado**
   - **Causa:** `rg "name"` encontra `oldname`, `filename`, `username` — qualquer substring.
   - **Sintoma:** variáveis não relacionadas são renomeadas, comentários explicativos ficam errados.
   - **Como detectar:** examinar os matches no `:copen` antes de rodar `:cdo`.
   - **Solução:** usar word boundary `\b` no rg: `rg "\bOldName\b"`. Ou ainda melhor: usar LSP rename quando o símbolo é reconhecido pelo language server.

3. **Mudanças invalidam matches subsequentes**
   - **Causa:** o quickfix carrega a lista de matches uma única vez; se a primeira substituição muda o número de linhas do arquivo, os matches seguintes para aquele arquivo podem apontar para linhas deslocadas.
   - **Sintoma:** algumas substituições aplicam no lugar certo, outras "pulam" ou aplicam em linha errada.
   - **Como detectar:** é sutil — percebe-se lendo cada confirmação com atenção.
   - **Solução:** usar `:cfdo` (por arquivo) em vez de `:cdo` (por match) é mais robusto. Ou recarregar o quickfix entre batches: rodar `:grep` novamente após cada rodada parcial.

4. **LSP rename não cobre refs cross-language**
   - **Causa:** LSP rename só conhece a linguagem configurada no buffer ativo; ao renomear uma função TypeScript, referências em `package.json`, arquivos `.yaml` de CI, schemas JSON ou documentação `.md` ficam intocadas.
   - **Sintoma:** após LSP rename, o nome antigo ainda aparece em configs e docs.
   - **Como detectar:** após LSP rename, rodar `rg "OldName" --stats` — se aparecem matches, são os residuais cross-language.
   - **Solução:** LSP rename pra símbolos + rg + quickfix pra varredura residual em configs e docs.

5. **Não ter baseline antes do refactor**
   - **Causa:** começar um refactor de larga escala com working tree sujo ou sem commit recente.
   - **Sintoma:** `:cdo` em escala ampla falha no meio, ou você percebe que foi longe demais, e reverter arquivo a arquivo manualmente é miserável.
   - **Como detectar:** `git status` antes de começar — se há modificações não commitadas, pause.
   - **Solução:** criar um commit pequeno antes do refactor: `git commit -m "chore: pre-refactor checkpoint"`. Se tudo der errado, `git reset --hard HEAD` resolve em segundos.

---

## Em inglês

- **refactoring** — *refactoring*. "Refactoring sem testes automatizados é andar num campo minado no escuro."
- **quickfix** — *quickfix list*. "O quickfix do nvim é uma lista centralizada de localizações para navegar e editar em lote."
- **location list** — *location list*. "A location list é como o quickfix, mas local a cada janela — cada split tem a sua."
- **find and replace** — *find and replace*. "Find and replace global sem word boundary pega substring onde você não quer."
- **language server** — *language server (LSP)*. "O language server entende o código semanticamente, não só como texto."
- **LSP rename** — *LSP rename*. "LSP rename é o caminho seguro pra renomear símbolos com rastreamento de referências."
- **regex** — *regular expression*. "Regex com word boundary `\b` evita matches parciais indesejados no ripgrep."
- **word boundary** — *word boundary*. "Word boundary `\b` garante que `name` não case com `filename` ou `username`."
- **batch edit** — *batch edit*. "Batch edit via `:cdo` aplica o mesmo comando em cada match do quickfix sequencialmente."
- **dry run** — *dry run*. "Dry run — rodar `rg --stats` antes de carregar o quickfix é o equivalente de ver o que vai mudar antes de mudar."

---

## Veja também

- [[03 - Onboarding em projeto novo]]
- [[05 - Code review no terminal]]
- [[09 - Transições de contexto]]
- [[03-Dominios/Tecnologia/Terminal/Editor/09 - LSP no Neovim|LSP no Neovim (galho 1)]]
- [[03-Dominios/Tecnologia/Terminal/Editor/11 - Workflow avançado|Quickfix avançado (galho 1)]]
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/02 - ripgrep e fd — buscar conteúdo e nomes|ripgrep (galho 6)]]
- [[03-Dominios/Tecnologia/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#quickfix|quickfix]]
- [[Dicionário do Terminal#LSP|LSP]]

---

## Referências

- nvim quickfix: <https://neovim.io/doc/user/quickfix.html>
- LazyVim keymaps: <https://www.lazyvim.org/keymaps>
