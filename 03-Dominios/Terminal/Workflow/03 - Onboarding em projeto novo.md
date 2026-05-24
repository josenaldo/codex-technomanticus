---
title: "Onboarding em projeto novo"
created: 2026-05-24
updated: 2026-05-24
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - workflow
  - iniciado
  - onboarding
  - playbook
aliases:
  - Onboarding projeto novo
  - Onboarding playbook
---

# Onboarding em projeto novo

> [!abstract] TL;DR
> Playbook para chegar em um repo desconhecido e ter um mapa mental em 30 minutos. Fluxo: clone + `cd` (zoxide aprende o caminho) → `eza --tree` para ver a estrutura macro → `rg "TODO|FIXME"` + `bat README.md` para contexto → Telescope `live_grep` para localizar entry points → `lazygit log` para entender o contexto recente. Anote perguntas em um scratch file; não tente entender tudo na primeira passada.

## O que é / Como funciona

### Por que onboarding merece playbook

A tendência ruim é abrir a IDE, navegar pela árvore de diretórios por horas e se perder em detalhes sem contexto. Horas depois, você sabe o nome dos arquivos mas não o propósito do sistema.

A tendência melhor é bater o terreno com ferramentas exploratórias rápidas: varredura de estrutura, busca por padrões, leitura de histórico. Trinta minutos focados valem mais do que três horas dispersas. O objetivo não é entender 100% — é ter o mapa mental mínimo para começar a contribuir com segurança.

### Fluxo macro

O playbook divide os 30 minutos em quatro fases sequenciais:

| Fase | Duração | Foco |
|------|---------|------|
| 1 — Contexto | 5 min | README, estrutura de pastas, CONTRIBUTING |
| 2 — Entry points | 10 min | Fluxos críticos, ponto de entrada da aplicação |
| 3 — Histórico recente | 10 min | Últimos commits, branches ativos, tendências |
| 4 — Anotar perguntas | 5 min | Scratch file com dúvidas para a próxima conversa |

Cada fase tem um entregável claro. Se uma fase estourar o tempo, avance assim mesmo — você volta com mais contexto depois.

### O que você quer no fim dos 30 minutos

Ao final do playbook, você deve conseguir responder:

- Qual diretório contém o entry point principal da aplicação?
- Qual(is) linguagem(ns) e framework(s) o projeto usa?
- Quais são os 2–3 fluxos críticos de negócio?
- Quais 5–10 perguntas você precisa fazer ao time antes de tocar em código de produção?

Se não conseguir responder pelo menos três dessas questões, repita as Fases 1 e 2 com foco diferente ou consulte alguém do time.

## Na prática

### Receita completa (30min)

```bash
# Fase 1 — Contexto (5min)
cd ~/repos/myproj              # zoxide aprende o caminho
eza --tree -L 2 --git-ignore   # estrutura macro (ignora vendor/node_modules)
bat README.md                  # leitura com syntax highlight
bat CONTRIBUTING.md 2>/dev/null
ls -la docs/ 2>/dev/null

# Fase 2 — Entry points (10min)
rg "main|entry|bootstrap" -t lua -t js -t py -t go | head -20
rg "TODO|FIXME|XXX" --stats | head
# Dentro do nvim:
# :Telescope find_files
# :Telescope live_grep "config|database|main"

# Fase 3 — History (10min)
lazygit
# log: ler últimos 20 commits, ver branches ativos
# Q pra sair
git log --oneline --all --decorate -20

# Fase 4 — Anotar perguntas (5min)
nvim ~/scratch/myproj.md
# Lista: arquitetura, deps externas, testing strategy, deploy pipeline
```

O bloco é sequencial. Não pule fases; comprima-as se necessário, mas execute-as todas.

### Adaptar ao tamanho do repo

Nem todo repo tem o mesmo perfil. Ajuste o playbook conforme o porte:

**Repo pequeno** (< 10 k linhas): pule a Fase 3. Com tão pouco código, o histórico importa menos do que entender a estrutura. Use o tempo extra na Fase 2 para ler mais entry points.

**Repo grande** (> 500 k linhas): na Fase 2, foque em **um** submódulo ou pacote por vez. Tentar mapear tudo de uma vez é armadilha. Escolha o submódulo mais relevante para a tarefa que você recebeu.

**Monorepo**: na Fase 1, mapeie quais `packages/` ou `apps/` existem antes de descer em qualquer um. O `eza --tree -L 3` ajuda. Entenda o grafo de dependências entre pacotes antes de mergulhar em código.

### Sinais ruins — volte ao README ou pergunte ao time

Alguns sinais indicam que o repo está em estado problemático e o playbook sozinho não basta:

- Não achou entry point óbvio após 10 minutos na Fase 2
- README com último commit há mais de 2 anos e sem build instructions
- Ausência de scripts de build ou test (`package.json`, `Makefile`, `pyproject.toml`, etc.)
- Arquivo de dependências vazio, corrompido ou sem lock file

Nesses casos, pare o playbook e pergunte ao time. Continuar explorando sem contexto humano vai custar mais tempo do que uma conversa de 5 minutos com `alice` ou `bob`.

## Armadilhas

1. **Tentar entender 100% antes de tocar código**
   **Causa:** Ansiedade de "não saber o suficiente" — medo de errar por ignorância.
   **Sintoma:** Três dias depois você ainda está lendo docs sem ter rodado o app nenhuma vez.
   **Como detectar:** Você marcou 30 minutos no timer mas já estorou para 2 horas e ainda não abriu o editor.
   **Solução:** Time-box rígido. Ao bater 30 minutos, mude o objetivo para "rodar o app local" — mesmo entendendo apenas 40% do código. O restante se aprende fazendo, com o contexto prático que só a execução dá.

2. **Pular `bat README.md` por achar que README é sempre inútil**
   **Causa:** Experiência acumulada com READMEs desatualizados cria viés de descarte automático.
   **Sintoma:** Você descobre um conceito básico do domínio (ex.: o que é um "pedido" naquele sistema) apenas na semana 2, por acidente.
   **Como detectar:** O README tem 5 ou mais linhas e você não leu nenhuma delas.
   **Solução:** Sempre leia o README na Fase 1. Mesmo que seja trash, dá o vocabulário que o time usa — e vocabulário errado em PR comments cria atritos desnecessários.

3. **Ignorar `lazygit log` / `git log` (Fase 3 pulada)**
   **Causa:** "O código atual basta para entender o sistema."
   **Sintoma:** Você faz um refactor com um pressuposto que foi explicitamente removido dois commits atrás, gerando regressão.
   **Como detectar:** Você não consegue responder "onde o time está pensando agora?" — só "onde o código está agora?"
   **Solução:** Fase 3 é obrigatória, não opcional. O histórico recente revela intenção e direção — o que o time está construindo, não apenas o que já construiu.

4. **Não anotar nada (Fase 4 esquecida)**
   **Causa:** "Vou lembrar" — confiança excessiva na memória de curto prazo.
   **Sintoma:** Na semana seguinte você faz o mesmo onboarding mental novamente, com as mesmas dúvidas, sem ter avançado.
   **Como detectar:** Abre `~/scratch/myproj.md` na semana 2 — está vazio ou inexistente.
   **Solução:** Fase 4 é inegociável. Mesmo 3 bullets já bastam. O scratch file vira fonte para a retrospectiva de onboarding e para orientar o próximo dev que entrar no mesmo projeto.

5. **Pular a Fase 2 e ir direto para leitura linear de arquivos**
   **Causa:** Querer mergulhar no código antes de mapear a topologia — parece "mais produtivo".
   **Sintoma:** Você leu 10 arquivos sem entender como eles se conectam nem qual deles é chamado primeiro.
   **Como detectar:** Ao final, você não consegue desenhar o fluxo de uma requisição típica do app do início ao fim.
   **Solução:** Use `rg` e Telescope **antes** de qualquer leitura linear. Identifique `main`, `index` ou `app` primeiro. Só depois desça para os módulos que esses arquivos importam.

## Em inglês

- **onboarding** — *onboarding*. "O onboarding de um dev novo no projeto pode levar dias se não houver playbook."
- **entry point** — *entry point*. "O entry point da aplicação fica em `src/main.go`."
- **codebase** — *codebase*. "Antes de tocar na codebase, leia o README e o histórico de commits."
- **scratch file** — *scratch file*. "Abri um scratch file para anotar as perguntas antes da reunião com o time."
- **time-box** — *time-box*. "Faça um time-box de 30 minutos para a fase de exploração; depois comece a rodar o código."
- **exploration** — *exploration*. "A fase de exploration serve para mapear o terreno, não para entender tudo."
- **repository** — *repository*. "Clone o repository e use `eza --tree` para ver a estrutura antes de abrir qualquer arquivo."
- **build script** — *build script*. "Se o projeto não tem build script, pergunte ao time antes de continuar."
- **dependency** — *dependency*. "Leia o arquivo de dependency (`package.json`, `go.mod`, `pyproject.toml`) na Fase 1."
- **contribution guide** — *contribution guide*. "O contribution guide (`CONTRIBUTING.md`) descreve o fluxo de trabalho esperado pelo time."

## Veja também

- [[02 - Anatomia da sessão de trabalho]]
- [[05 - Code review no terminal]]
- [[08 - Refactoring multi-arquivo]]
- [[03-Dominios/Terminal/Editor/04 - LazyVim — instalação, tour, navegação|LazyVim — Telescope (galho 1)]]
- [[03-Dominios/Terminal/TUIs/01 - Lazygit — overview|Lazygit overview (galho 4)]]
- [[03-Dominios/Terminal/CLI Utils/02 - ripgrep e fd — buscar conteúdo e nomes|ripgrep (galho 6)]]
- [[03-Dominios/Terminal/CLI Utils/04 - eza — ls moderno|eza (galho 6)]]
- [[03-Dominios/Terminal/CLI Utils/05 - zoxide — cd inteligente com frecency|zoxide (galho 6)]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]

## Referências

Sem referências externas. Esta é uma nota de playbook que compõe e aplica os comandos apresentados nos galhos 1–6 da trilha Terminal.
