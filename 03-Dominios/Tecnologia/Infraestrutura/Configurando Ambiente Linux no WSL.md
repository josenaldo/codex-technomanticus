- [[#Windows Terminal]]
    - [[#Instalar Windows Terminal]]
    - [[#Configurar temas do Windows Terminal]]
    - [[#Temas do Windows Terminal]]
- [[#Instalar WSL, Ubuntu e Docker]]
    - [[#WSL (Windows Subsystem for Linux) - Ultimate Tutorial e últimas novidades]]
    - [[#Melhorando a velocidade da internet do Linux dentro do WSL]]
        - [[#Instalar pacotes básicos]]
    - [[#Lidando com painéis do Windows Terminal]]
- [[#ZSH]]
    - [[#Instalando fontes Fira Code]]
    - [[#Instalar ZSH]]
    - [[#Instalar Oh My ZSH]]
    - [[#Instalar PowerLevel10k]]
    - [[#Instalar plugins do ZSH]]
        - [[#zsh-autosuggestions]]
        - [[#zsh-syntax-highlighting]]
        - [[#zsh-fast-syntax-highlighting]]
        - [[#zsh-autocomplete]]
        - [[#Habilitar plugins]]
- [[#Git]]
- [[#Stacks]]
    - [[#Node]]
        - [[#Instalar NVM]]
    - [[#Go]]
        - [[#Instalar o Go]]
    - [[#Configurar Go no ZSH]]
    - [[#Java]]
- [[#Editores]]
    - [[#Neovim]]
        - [[#Instalar Neovim]]
    - [[#VS Code]]
        - [[#Instalar Code]]
        - [[#Extensões]]
- [[#Pacotes extras]]
    - [[#Para trabalhar com gRPC em Go]]
- [[#Backup]]

# Windows Terminal

## Instalar Windows Terminal

> [!info] Instalação do Terminal do Windows  
> Saiba como instalar e configurar o Terminal do Windows.  
> [https://learn.microsoft.com/pt-br/windows/terminal/install](https://learn.microsoft.com/pt-br/windows/terminal/install)  

## Configurar temas do Windows Terminal

> [!info] Esquemas de cores do Terminal do Windows  
> Saiba como criar esquemas de cores para o Terminal do Windows.  
> [https://learn.microsoft.com/pt-br/windows/terminal/customize-settings/color-schemes](https://learn.microsoft.com/pt-br/windows/terminal/customize-settings/color-schemes)  

  

## Temas do Windows Terminal

Pegue o tema Monokai Pro no [https://windowsterminalthemes.dev/](https://windowsterminalthemes.dev/).

> [!info] Windows Terminal Themes  
> Browse and copy hundreds of themes for Windows Terminal  
> [https://windowsterminalthemes.dev/](https://windowsterminalthemes.dev/)  

No Windows Terminal, abra o arquivo JSON

![[Untitled.png]]

No arquivo de configurações, acrescente o código do tema à lista de `schemes`.  

![[Untitled 1.png]]

Abra os perfis que quiser e selecione o tema acrescentado.

![[Untitled 2.png]]

# Instalar WSL, Ubuntu e Docker

Esse guia ensina como:

- Instalar o WSL2

- Instalar um Linux, como o Ubuntu

- Configurar o WSL

https://github.com/codeedu/wsl2-docker-quickstart

https://github.com/josenaldo/wsl2-docker-quickstart

## **WSL (Windows Subsystem for Linux) - Ultimate Tutorial e últimas novidades**

[https://www.youtube.com/watch?v=-oxnRGhA9Mg](https://www.youtube.com/watch?v=-oxnRGhA9Mg)

## Melhorando a velocidade da internet do Linux dentro do WSL

Se, dentro do Linux, a instalação de pacotes e os downloads estiverem lentos, execute o procedimento abaixo:  
  
1-Press the Windows Key and type “Control Panel” and hit enter  
2- Click “Network and Internet”  
3- Click “View network status and tasks”  
4- Click “Change adapter settings”  
5- Find the “vEthernet (WSL)” adapter and click properties  
6- Click “configure” and open the advanced tab  
Select “Large Send Offload Version 2 (IPv4)” and change the drop-down to disabled. To the same for “Large Send Offload Version 2 (IPv6)”.  
Once this is done click “OK” and you are all done. You may experience a slight downtime in connection while this is saved.  
  
Fonte: [https://answers.microsoft.com/en-us/windows/forum/all/low-internet-speed-in-wsl-2/21524829-18be-4611-bb5f-cabccd2cae31](https://answers.microsoft.com/en-us/windows/forum/all/low-internet-speed-in-wsl-2/21524829-18be-4611-bb5f-cabccd2cae31)

### Instalar pacotes básicos

Instale pacotes básicos

```Bash
sudo apt-get install -y gcc sqlite3
```

## Lidando com painéis do Windows Terminal

> [!info] Painéis do Terminal do Windows  
> Saiba como dividir painéis no Terminal do Windows.  
> [https://learn.microsoft.com/pt-br/windows/terminal/panes](https://learn.microsoft.com/pt-br/windows/terminal/panes)  

# ZSH

## Instalando fontes Fira Code

> [!info] How to Install Nerd Fonts on Ubuntu - Linuxspin  
> In this article, you will learn how to install nerd fonts on Ubuntu and applied them to your favorite application like code editor or terminal emulator.  
> [https://linuxspin.com/install-nerd-fonts-on-ubuntu/](https://linuxspin.com/install-nerd-fonts-on-ubuntu/)  

## Instalar ZSH

> [!info] Installing ZSH  
> 🙃 A delightful community-driven (with 2,200+ contributors) framework for managing your zsh configuration.  
> [https://github.com/ohmyzsh/ohmyzsh/wiki/Installing-ZSH](https://github.com/ohmyzsh/ohmyzsh/wiki/Installing-ZSH)  

```Bash
sudo apt-get install zsh
```

## Instalar Oh My ZSH

> [!info] Home  
> 🙃 A delightful community-driven (with 2,200+ contributors) framework for managing your zsh configuration.  
> [https://github.com/ohmyzsh/ohmyzsh/wiki](https://github.com/ohmyzsh/ohmyzsh/wiki)  

## Instalar PowerLevel10k

https://github.com/romkatv/powerlevel10k

## Instalar plugins do ZSH

Lembre-se de instalar os plugins sempre como plugins do oh-my-zsh.

### zsh-autosuggestions

https://github.com/zsh-users/zsh-autosuggestions

```Bash
git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions
```

### zsh-syntax-highlighting

https://github.com/zsh-users/zsh-syntax-highlighting

```Bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
```

### zsh-fast-syntax-highlighting

https://github.com/zdharma-continuum/fast-syntax-highlighting

```Bash
git clone https://github.com/zdharma-continuum/fast-syntax-highlighting.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/fast-syntax-highlighting
```

### zsh-autocomplete

https://github.com/marlonrichert/zsh-autocomplete

```Bash
git clone --depth 1 -- https://github.com/marlonrichert/zsh-autocomplete.git $ZSH_CUSTOM/plugins/zsh-autocomplete
```

### Habilitar plugins

Abra o .zshrc

```Bash
nvim ~/.zshrc
```

Encontre a linha que contém `plugins=(git)` e substitua os essa linha por:

```Bash
plugins=(
        git
        zsh-autosuggestions
        zsh-autocomplete
        fast-syntax-highlighting
        zsh-syntax-highlighting
)
```

# Git

Configurar email e nome do usuário

```Shell
git config --global user.email "josenaldo@gmail.com"

git config --global user.name "Josenaldo de Oliveira Matos Filho"
```

# Stacks

## Node

### Instalar NVM

https://github.com/nvm-sh/nvm

## Go

### Instalar o Go

> [!info] Download and install - The Go Programming Language  
> Don't see your operating system here?  
> [https://go.dev/doc/install](https://go.dev/doc/install)  

## Configurar Go no ZSH

No arquivo `~/zshrc`, atualize o PATH:

```Bash
export PATH=$PATH:/usr/local/go/bin
```

## Java

Instale o OpenJDK 17

```Bash
sudo apt install openjdk-17-jdk openjdk-17-jre
```

# Editores

## Neovim

### Instalar Neovim

```Bash
sudo apt-get install neovim
```

## VS Code

### Instalar Code

```Bash
code .
```

### Extensões

- GraphQL: Language Feature Support: [https://marketplace.visualstudio.com/items?itemName=GraphQL.vscode-graphql](https://marketplace.visualstudio.com/items?itemName=GraphQL.vscode-graphql)

- DotENV: [https://marketplace.visualstudio.com/items?itemName=mikestead.dotenv](https://marketplace.visualstudio.com/items?itemName=mikestead.dotenv)

# Pacotes extras

## Para trabalhar com gRPC em Go

Instale o `protobuf-compiler`

```Bash
sudo apt install -y protobuf-compiler
```

No arquivo `~/zshrc`, atualize o path, de modo a permitir que o `protoc` encontre os plugins.

```Bash
export PATH="$PATH:$(go env GOPATH)/bin"
```

1. Instale os plugins do `protocol compiler` para Go

```Bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

  

# Backup

Para fazer backup do Ubuntu, use o comando:

```Bash
wsl --export Ubuntu c:\wsl-backup\ubuntu.tar
```