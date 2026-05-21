---
title: "Zellij vs tmux vs screen"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - multiplexer
  - zellij
  - tmux
  - iniciado
aliases:
  - Zellij vs tmux
---

# Zellij vs tmux vs screen

> [!abstract] TL;DR
> Multiplexer divide 1 terminal em múltiplas sessions/panes que sobrevivem a detach. Zellij é o moderno (lançado ~2021), com modos discoverable (status bar mostra atalhos) e config declarativa em KDL. tmux é o padrão de facto (universal em servidores, ecossistema maduro). screen é o legado (lançado em 1987, sempre instalado, baixo nível). Zellij vence pra workstation de dev; tmux vence pra servidor remoto.

## O que é / Como funciona

### Multiplexer — o conceito

Um **terminal multiplexer** é um programa que roda como servidor em background e cria múltiplas "sessões" virtuais, cada uma com tabs e panes independentes. Você se conecta ao servidor (`attach`) e se desconecta (`detach`) à vontade — o servidor continua rodando, e os processos dentro das sessões continuam executando.

A diferença fundamental para "abrir várias abas no emulador de terminal":

- **Sobrevive a fechar o emulador** — o processo continua rodando no servidor
- **Sobrevive a queda de SSH** — conexão cai, sessão persiste no servidor remoto
- **Permite múltiplos clientes** — dois terminais podem se anexar à mesma sessão simultaneamente (colaboração em par)
- **Panes não são janelas do OS** — são divisões gerenciadas pelo multiplexer, visíveis em qualquer ambiente (SSH, tty, headless)

```
┌─────────────────────────────────────┐
│  Servidor do multiplexer (bg)       │
│  ┌──────────────┐ ┌──────────────┐  │
│  │  Sessão A    │ │  Sessão B    │  │
│  │  tab1 tab2   │ │  tab1        │  │
│  └──────────────┘ └──────────────┘  │
└─────────────────────────────────────┘
         ↑ attach / detach ↑
    cliente (emulador, SSH, etc.)
```

### Os 3 concorrentes

| Critério | Zellij | tmux | screen |
|---|---|---|---|
| Ano de lançamento | ~2021 (v0.1.0 em 2021) | 2007 | 1987 |
| Versão atual (2026) | 0.44.x | 3.5.x | 5.0.x |
| Discoverabilidade | Alta — status bar exibe atalhos contextuais | Baixa — requer decorar prefixo + tecla | Muito baixa — interface mínima |
| Config | KDL declarativo | arquivo `.tmux.conf` (DSL própria) | `.screenrc` (sintaxe arcaica) |
| Sessions persistentes | Sim | Sim | Sim |
| Plugin system | WASM (sandbox, multilíngue) | TPM (shell scripts, centenas de plugins) | Não |
| Performance | Boa (Rust) | Excelente (C) | Excelente (C) |
| Ubiquidade em servidores | Baixa | Alta (frequentemente pré-instalado) | Muito alta (sempre instalado) |
| Maturidade | Jovem (~5 anos) | Maduro (18+ anos) | Muito maduro (38+ anos) |
| Público-alvo primário | Dev workstation local | Uso geral, servidores remotos | Sysadmin, servidores embedded |

### Diferenciais do Zellij

**1. Status bar com hints de modo**

A barra inferior do Zellij mostra, em tempo real, os atalhos disponíveis para o modo ativo. Você nunca precisa lembrar `Ctrl-b ?` nem consultar cheatsheet — o multiplexer ensina à medida que você usa.

**2. Modos discoverable**

Zellij organiza ações em modos nomeados: `Normal`, `Locked`, `Resize`, `Pane`, `Tab`, `Scroll`, `Search`, `EnterSearch`, `RenameTab`, `RenamePane`, `Session`, `Move`, `Prompt`, `Tmux`. Cada modo tem um conjunto específico de atalhos exibidos na status bar — o "modelo mental" é explícito.

**3. Defaults sensatos**

Out-of-the-box, sem nenhuma configuração:
- Mouse habilitado (`mouse_mode true`)
- Status bar visível na parte inferior
- Copy-on-select ativo (selecionar texto com mouse copia automaticamente)
- Panes com borda e título visíveis
- Sem necessidade de `~/.config/zellij/config.kdl` pra ter uma experiência funcional

**4. Layouts em KDL**

Configuração e layouts escritos em [KDL](https://kdl.dev) — formato legível, declarativo e versionável em dotfiles:

```kdl
// ~/.config/zellij/layouts/myproject.kdl
layout {
    pane size=1 borderless=true {
        plugin location="zellij:tab-bar"
    }
    pane split_direction="horizontal" {
        pane command="nvim"
        pane split_direction="vertical" {
            pane command="zsh"
            pane command="zsh"
        }
    }
    pane size=2 borderless=true {
        plugin location="zellij:status-bar"
    }
}
```

**5. Plugin system em WASM**

Plugins são módulos WebAssembly — isolados em sandbox, sem acesso irrestrito ao sistema, e podem ser escritos em Rust (suporte oficial) ou outras linguagens que compilam para WASM (iniciativas da comunidade). A própria UI do Zellij (status bar, tab bar) é implementada como plugins internos.

**6. "Tmux mode" opcional**

Para quem quer migrar gradualmente ou prefere o modelo de keybindings do tmux, Zellij oferece um modo `Tmux` integrado que replica os padrões de prefixo do tmux.

### Quando tmux ainda ganha

- **Servidores remotos**: tmux está disponível em praticamente qualquer servidor Linux via package manager. Zellij requer instalação manual.
- **Ecossistema de plugins**: TPM (Tmux Plugin Manager) tem centenas de plugins maduros — `tmux-resurrect`, `tmux-continuum`, `tmux-sensible`, etc.
- **Performance em sessões pesadas**: tmux em C é marginalmente mais eficiente em cenários com muitos panes e conteúdo intenso.
- **Documentação madura**: 18+ anos de Q&A, tutoriais, Stack Overflow. Troubleshooting é mais fácil.
- **Integração com ferramentas**: Neovim, `fzf`, `vim-tmux-navigator` têm integrações tmux bem estabelecidas.

### Público-alvo de cada

**Zellij:**
Desenvolvedor usando workstation local, dotfiles modernos, prefere aprender sem decorar atalhos, quer layouts declarativos versionados, confortável com ferramentas novas.

**tmux:**
Qualquer pessoa que trabalha frequentemente em servidores remotos via SSH, equipes que precisam de plugin ecosystem maduro, quem já tem config estabelecida e não quer migrar.

**screen:**
Sysadmin em servidor com ambiente mínimo, casos onde apenas `screen` está disponível (container sem apt, sistema embedded), scripts legados que dependem de `screen -dmS`.

## Na prática

### Instalação rápida (Linux)

```bash
# Opção 1: binário estático via GitHub Releases (sem dependências)
curl -L https://github.com/zellij-org/zellij/releases/latest/download/zellij-x86_64-unknown-linux-musl.tar.gz \
  | tar -xz
sudo mv zellij /usr/local/bin/

# Verificar versão
zellij --version
# zellij 0.44.1

# Opção 2: via cargo (requer Rust toolchain)
cargo install --locked zellij

# Opção 3: via package manager (verificar versão disponível antes)
# Ubuntu/Debian — pode ter versão desatualizada:
# sudo apt install zellij
```

> [!warning] apt pode instalar versão muito antiga
> Dependendo da distribuição, `apt install zellij` pode entregar versões muito atrasadas. Prefira o binário estático ou `cargo install` para garantir a versão atual.

### Primeira sessão

```bash
# Abre Zellij — cria ou reutiliza sessão "main"
zellij

# Cria sessão com nome específico
zellij -s myproj

# Lista sessões ativas
zellij ls

# Anexa a sessão existente pelo nome
zellij attach myproj

# Mata sessão específica
zellij delete-session myproj

# Mata todas as sessões
zellij delete-all-sessions
```

**Atalhos essenciais do modo Normal (exibidos na status bar):**

| Ação | Tecla |
|---|---|
| Novo pane (dividir vertical) | `Alt n` |
| Navegar entre panes | `Alt ←↑↓→` |
| Entrar modo Pane | `Ctrl p` |
| Entrar modo Tab | `Ctrl t` |
| Entrar modo Session | `Ctrl o` |
| Detach da sessão | `Ctrl o` → `d` |
| Sair (fechar pane) | `Ctrl q` |

### Side-by-side com tmux (transição)

A coexistência entre Zellij e tmux no mesmo ambiente é simples e recomendada no período de transição:

- **tmux para SSH remoto**: mantenha tmux nos servidores; use Zellij só na workstation local
- **Zellij para dev local**: layouts KDL por projeto, sessions nomeadas, status bar com hints
- **Tmux mode**: se os keybindings do Zellij desorientam, ative o modo Tmux que replica o modelo de prefixo
- **Sem conflito de server**: os dois podem rodar simultâneamente — são processos independentes

```bash
# Zellij com tmux keybindings (modo compatibilidade)
# No config.kdl:
# keybinds { tmux { ... } }
# Ou via --config-dir flag apontando pra layout com tmux mode

# Alternativa rápida: iniciar direto no modo Tmux
zellij --config-dir ~/.config/zellij-tmux
```

## Armadilhas

### (1) Achar que Zellij é "tmux com UI melhor" — é uma ferramenta diferente

**Causa:** o marketing de "terminal workspace" e a comparação frequente com tmux leva a assumir que Zellij é um tmux mais bonito. Na prática, o modelo mental é diferente: Zellij tem modos, plugin system WASM, e config KDL — não é uma skin sobre tmux.

**Sintoma:** frustração ao tentar replicar workflows tmux diretamente, como `bind-key` customizations ou scripts que dependem de `tmux send-keys`.

**Como detectar:** tentar configurar Zellij usando conceitos tmux (ex: `set -g mouse on`, `bind-key`, `source-file`) e notar que nenhum deles existe.

**Solução:** ler a documentação do Zellij como ferramenta independente, não como "tmux alternativo". Começar pelo `zellij setup --dump-config` para ver o `config.kdl` default comentado.

---

### (2) Instalar via `apt` em distros com repositórios atrasados

**Causa:** Zellij ainda não está nos repositórios oficiais de todas as distros. Quando está, costuma ser uma versão significativamente mais antiga que o upstream.

**Sintoma:** `zellij --version` mostra `0.32.x` ou similar quando a versão atual é `0.44.x`; features documentadas (como determinados atalhos ou opções KDL) não existem.

**Como detectar:** `apt-cache show zellij | grep Version` — comparar com a versão atual em https://github.com/zellij-org/zellij/releases.

**Solução:** usar o binário estático do GitHub Releases (`zellij-x86_64-unknown-linux-musl.tar.gz`) ou `cargo install --locked zellij`. Remover a versão apt com `sudo apt remove zellij` antes.

---

### (3) Conflito entre modos do Zellij e keybindings do Vim/Neovim

**Causa:** Zellij usa letras como `p`, `t`, `n`, `d`, `h`, `j`, `k`, `l` nos seus modos de controle (Pane, Tab, etc.), que colidem com os keybindings normais do Vim/Neovim quando você está editando dentro de um pane.

**Sintoma:** pressionar `Ctrl p` dentro do Neovim abre o modo Pane do Zellij em vez de executar a ação do plugin (ex: Telescope). O Zellij intercepta a tecla antes do pane.

**Como detectar:** o atalho não chega ao Neovim — a status bar do Zellij muda de modo ao invés de o editor reagir.

**Solução:** usar o modo `Locked` do Zellij (`Ctrl g` pra entrar/sair) quando precisar passar atalhos diretamente ao aplicativo interno. Ou reconfigurara os keybindings do Zellij pra usar prefixos que não colidam, como `Ctrl b` (padrão tmux) via tmux mode.

---

### (4) Tentar usar Zellij via SSH em servidor que não tem instalado

**Causa:** diferentemente do tmux (frequentemente pré-instalado) e screen (quase sempre presente), Zellij precisa ser instalado explicitamente. Não existe em repositórios padrão da maioria dos servidores.

**Sintoma:** `zellij: command not found` ao conectar via SSH num servidor de produção ou ambiente compartilhado.

**Como detectar:** `which zellij` retorna vazio no servidor remoto.

**Solução:** usar tmux ou screen para sessões remotas — esta é a estratégia recomendada (Zellij local + tmux remoto). Se precisar de Zellij no servidor, copiar o binário estático via `scp` e instalar em `~/.local/bin/`.

---

### (5) Esperar ecosystem de plugins do tamanho do tmux

**Causa:** Zellij tem ~5 anos de vida vs ~18 do tmux. O ecossistema TPM do tmux acumula centenas de plugins maduros, enquanto o ecosystem WASM do Zellij ainda é pequeno.

**Sintoma:** procurar equivalente ao `tmux-resurrect` (salvar/restaurar sessões) ou ao `tmux-continuum` (autosave) e não encontrar solução madura equivalente para o Zellij.

**Como detectar:** buscar no repositório oficial da comunidade — https://github.com/zellij-org/zellij/wiki/Third-Party-Plugins — e notar que a lista é curta comparada ao TPM.

**Solução:** aceitar que o Zellij tem ecosystem jovem e complementar com funcionalidades nativas (layouts KDL, sessions built-in) onde possível. Contribuir com plugins WASM se necessário — o modelo WASM é mais acessível que os shell scripts do TPM. Para funcionalidades críticas que só existem no tmux, considerar usar tmux para esse caso de uso específico.

## Em inglês

- **multiplexer** — *multiplexer* (ou *terminal multiplexer*). "A terminal multiplexer lets you run multiple programs in a single terminal window."
- **sessão** — *session*. "Detach from a session and it keeps running in the background."
- **painel** — *pane*. "Split the current pane horizontally to open a second shell."
- **aba** — *tab*. "Each tab can contain multiple panes arranged in a layout."
- **desanexar** — *detach*. "Detach from the session before closing the laptop."
- **anexar** — *attach*. "Attach to a named session to resume your work."
- **layout** — *layout*. "Define your project layout in a KDL file and launch it with one command."
- **descobrível / descobribilidade** — *discoverable / discoverability*. "Zellij's status bar makes keybindings discoverable without memorization."
- **barra de status** — *status bar*. "The status bar at the bottom shows context-sensitive hints for the active mode."
- **plugin** — *plugin*. "Zellij plugins are compiled to WebAssembly and run in a sandboxed environment."

## Veja também

- [[02 - Modelo mental — sessions, tabs, panes]] — próxima nota: anatomia detalhada
- [[03 - Modos básicos e keybindings essenciais]] — modos são o diferencial-chave do Zellij
- [[06 - Modos avançados, plugins e copy-mode]] — tmux compat mode e plugin WASM
- [[03-Dominios/Terminal/Multiplexer/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Multiplexer|multiplexer]]

## Referências

- [Zellij — about](https://zellij.dev/about/)
- [Zellij — documentation](https://zellij.dev/documentation/)
- [Zellij — releases (GitHub)](https://github.com/zellij-org/zellij/releases)
- [tmux — repositório oficial](https://github.com/tmux/tmux)
- [GNU screen — Wikipedia](https://en.wikipedia.org/wiki/GNU_Screen)
