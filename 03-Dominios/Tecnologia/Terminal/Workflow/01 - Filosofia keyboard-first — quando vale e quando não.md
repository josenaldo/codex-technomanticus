---
title: "Filosofia keyboard-first — quando vale e quando NÃO"
created: 2026-05-24
updated: 2026-05-24
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - workflow
  - iniciado
  - keyboard-first
aliases:
  - Keyboard-first
  - Filosofia keyboard-first
---

# Filosofia keyboard-first — quando vale e quando NÃO

> [!abstract] TL;DR
> Keyboard-first é um modelo onde o teclado é primário e o mouse é opcional — não "sem mouse". Ele compensa pra texto, código e navegação repetitiva, onde consistência e ergonomia importam mais que velocidade pura. **Não compensa** pra graphics, ER design e browsing visual, onde gestos contínuos superam saltos discretos. O custo de aprendizado é real (semanas a meses) e o ganho principal não é digitar mais rápido: é menos contexto-switch, menos RSI e mais consistência entre ferramentas.

## O que é / Como funciona

### O que é keyboard-first

Keyboard-first é um modelo de interação onde o teclado é o dispositivo primário para navegação, edição e emissão de comandos. O mouse existe e é usado, mas é opcional — acionado quando faz sentido, não como padrão reflexo.

A origem está em editores modais (vi, Emacs) e na tradição Unix de composição de ferramentas via texto. Terminais não tinham mouse; tudo era teclado. Esse legado virou filosofia: interfaces bem projetadas devem ser completamente operáveis via teclado, com mouse como complemento.

### Princípios

- **Atalhos hierárquicos (leader keys, prefix):** em vez de memorizar centenas de combinações isoladas, usa-se um tecla inicial (leader no Vim, `<C-a>` no tmux, `<C-b>` no Zellij) que abre um namespace de atalhos. Isso reduz colisões e torna o sistema mais expansível.
- **Modos vs modelos:** editores modais (vi/Vim/Neovim) trocam o modo da interface inteira (normal, insert, visual, command). Emacs usa meta-combinações em modo único. Modos permitem teclas simples como `d`, `y`, `p` fazerem coisas poderosas sem modificadores.
- **Consistência cross-tool (Vim grammar):** o mesmo vocabulário (`hjkl`, `/` pra buscar, `gg`/`G`) reaparece em Neovim, `less`, `bat`, `man`, `zsh vi-mode`, `fzf`. Aprende-se uma vez, funciona em múltiplos contextos.
- **Pequenos gestos, alta frequência:** keyboard-first não é sobre teclas exóticas. É sobre tornar as 50 ações mais frequentes do dia tão rápidas que se tornam reflexo.

### Quando keyboard-first compensa

- **Texto e código:** domínio natural — toda interação é textual; mouse não adiciona precisão.
- **Navegação repetitiva:** alternar entre arquivos, buffers, abas, splits — ações feitas dezenas de vezes por hora.
- **Composição de comandos:** encadear `rg | fzf | xargs` ou operações Vim (`ci"`, `va{`) é inerentemente textual.
- **Operações reversíveis:** desfazer (`u`, `Ctrl-Z`) é trivial; o custo de errar é baixo.
- **Ambientes sem mouse confiável:** SSH remoto, terminal headless, tmux em servidor.

### Quando NÃO compensa

- **Graphics e design:** Figma, Photoshop, Inkscape — a interação fundamental é posicionar, arrastar, pintar. Atalhos de teclado existem mas são auxiliares.
- **ER diagrams e diagramação:** ferramentas como draw.io, Lucidchart ou dbdiagram.io envolvem posicionamento espacial que mouse resolve em segundos.
- **Browsing visual e exploração de mídia:** rolar uma página com imagens, explorar um dashboard, comparar dois layouts visualmente.
- **Onde gestos contínuos superam saltos discretos:** qualquer tarefa onde precisão de posição no espaço 2D importa mais que velocidade de sequência de comandos.
- **Colaboração imediata com não-praticantes:** pair programming com alguém que usa VS Code + mouse — forçar keyboard-first cria atrito na colaboração.

### Custo real

- **Curva de aprendizado de semanas a meses:** antes de ficar neutro em velocidade, você é mais lento. Isso é esperado e não indica falha.
- **Customização que envelhece mal:** configs crescem, o autor original esquece por que escreveu cada linha; migrar pra nova máquina vira trabalho.
- **Lock-in cognitivo:** depois de anos em Neovim + Zellij, colaborar em VS Code com mouse parece alienígena. O custo existe.
- **RSI invertido:** postura ruim no teclado também causa lesão. Teclado ergonômico inadequado + horas de digitação intensa = mesmo resultado que mouse intensivo. Keyboard-first não é imunidade automática contra RSI.

## Na prática

### Auto-teste honesto: vale pra você?

Antes de começar, responda:

1. **Mais de 80% do dia é texto/código?** Se sim, o investimento compensa. Se você passa metade do dia em reuniões, Figma e spreadsheets, o ROI cai drasticamente.
2. **Muda de máquina com frequência?** Portabilidade do conhecimento (não da config) é um argumento real para keyboard-first.
3. **Tem deadline em 2 semanas?** Espere. Adotar keyboard-first em sprint crítico é receita para desastre.
4. **Sente fadiga no pulso/cotovelo após longas sessões?** Esse é o argumento mais honesto — teclado ergonômico + keyboard-first pode ser terapêutico.

### Como NÃO entrar errado

- **Não copie a config de um senior sem entender.** A config deles é acúmulo de anos; a sua precisa começar menor.
- **Não desabilite o mouse forçado.** Remover o mouse do sistema cria frustração desnecessária em tarefas visuais.
- **Não meça produtividade em "comandos por minuto".** A métrica certa é: consegue fazer o que precisa sem sair do fluxo?
- **Aprenda 1 atalho por dia** — não 20 de uma vez. Repetição cria músculo; volume cria confusão.
- **Mantenha o mouse à mão.** Keyboard-first não é uma competição de pureza.

### Caminho mínimo viável

Uma progressão realista para quem parte do zero:

- **Dia 1:** instalar Neovim com uma distro (LazyVim) e aprender a abrir, editar e salvar um arquivo. Só isso.
- **Semana 1–2:** `hjkl`, modos (normal/insert/visual), busca com `/`, e Telescope para arquivos. Ainda lento — normal.
- **Mês 1:** `rg` + `fzf` no shell para busca; leader keys no editor; prefix do Zellij para splits. Começar a sentir o fluxo.
- **Mês 2+:** customização própria, baseada em fricção real observada — não em vídeos de "minha config definitiva".

A regra prática: uma ferramenta nova por semana, consolidada antes de adicionar outra.

## Armadilhas

1. **"Keyboard-first é mais rápido" como argumento principal**

**Causa:** vídeos de demonstração medem segundos por micro-tarefa. A conclusão "ele é 3x mais rápido" não sobrevive ao contexto real de trabalho com interrupções, buscas, leitura de docs e comunicação.

**Sintoma:** desânimo intenso após 2–3 semanas — você ainda é mais lento do que era com a IDE anterior, e o argumento que te motivou não está se confirmando.

**Como detectar:** compare o tempo de tasks reais completas (implementar uma feature pequena, revisar um PR), não de micro-benchmarks isolados como "deletar uma linha".

**Solução:** reframe o objetivo. O ganho real de keyboard-first é consistência (menos contexto-switch entre mouse e teclado), ergonomia (menos tensão no punho) e portabilidade do conhecimento entre ferramentas. Velocidade aparece como subproduto após meses, não como causa.

---

2. **Forçar adoção 100% em todas as tarefas**

**Causa:** purismo doutrinário. "Se eu usar o mouse, estou traindo o método."

**Sintoma:** frustração crescente em tasks visuais — arrastar colunas no Excel, posicionar elementos no Figma, browsing de imagens. O método está atrapalhando o trabalho, não ajudando.

**Como detectar:** se uma tarefa específica leva consistentemente mais de 2x o tempo que levava antes, e isso não melhora após 2 semanas, é sinal de ferramenta errada para aquela task.

**Solução:** keyboard-first é prioridade, não dogma. Mouse para graphics, browsing visual e drag-drop intencional não é derrota — é pragmatismo. A filosofia diz "teclado quando compensa", não "teclado sempre".

---

3. **Customizar tudo antes de aprender o default**

**Causa:** ansiedade de "deixar do meu jeito" antes de ter maturidade suficiente para saber o que precisa mudar.

**Sintoma:** configs com centenas de linhas após 1 semana, das quais 80% foram copiadas de vídeos do YouTube sem entender o propósito. Meses depois, abrir o config e não saber por que metade das linhas existe.

**Como detectar:** abra sua config e tente explicar, linha por linha, por que cada mapeamento existe. Se não consegue, está customizado demais cedo demais.

**Solução:** usar o default por 2–4 semanas inteiras. Customizar somente atalhos que você usa 10+ vezes por dia e onde o default causa fricção real. Cada linha nova no config deve ter um motivo documentado.

---

4. **Ignorar RSI até doer**

**Causa:** "ainda não dói, então está ok" — a ausência de dor é interpretada como prova de que a postura/setup está correto.

**Sintoma:** dor ou formigamento no pulso, cotovelo ou antebraço aparece de forma relativamente súbita após meses de uso intenso, muitas vezes após uma sessão longa ou período de stress.

**Como detectar:** qualquer tensão ou desconforto no pulso após 1 hora de digitação é um sinal precoce, não algo para ignorar. O problema real já está se desenvolvendo.

**Solução:** pausas ativas (Pomodoro 25/5 como mínimo), alongamentos de pulso e antebraço, teclado ergonômico (split keyboard ou ortolinear reduz desvio ulnar), e remapear CapsLock → Ctrl para evitar a contorção clássica da mão esquerda no `<C-x>`.

---

5. **Esperar que keyboard-first salve produtividade de problemas estruturais**

**Causa:** querer um atalho técnico para um problema que é organizacional, de processo ou de foco.

**Sintoma:** pensamento como "se eu dominasse Vim direito, entregaria o dobro de tasks". A ferramenta vira desculpa para não endereçar o real gargalo.

**Como detectar:** identifique onde o tempo realmente vai. Se o bottleneck é "não sei o que implementar", "reuniões demais", "PR em revisão há 3 dias" ou "código legado complexo" — nenhum atalho de teclado resolve isso.

**Solução:** keyboard-first amplifica produtividade existente — ele não a cria do zero. Se o processo, o design ou o foco estão quebrados, dominar Neovim não conserta. Resolva o problema real primeiro; depois otimize a ferramenta.

## Em inglês

- **keyboard-first** — *keyboard-first*. "Abordagem keyboard-first significa que o teclado é o dispositivo primário de interação."
- **modal editing** — *modal editing*. "Modal editing divide a interface em modos distintos, como normal e insert."
- **leader key** — *leader key*. "A leader key é uma tecla prefixo que abre um namespace de atalhos personalizados."
- **mouse-first** — *mouse-first*. "Fluxos mouse-first dependem de GUI para a maioria das interações."
- **RSI** — *Repetitive Strain Injury*. "RSI é uma lesão por esforço repetitivo comum em profissionais que digitam por horas."
- **ergonomia** — *ergonomics*. "Boa ergonomia de teclado inclui posição neutra do pulso e pausas regulares."
- **prefix key** — *prefix key*. "No Zellij, a prefix key padrão é `<C-a>`, usada para acessar comandos do multiplexer."
- **muscle memory** — *muscle memory*. "Depois de semanas de prática, muscle memory transforma atalhos em reflexo."
- **learning curve** — *learning curve*. "A learning curve de Neovim é real, mas se aplana após o primeiro mês."
- **lock-in** — *lock-in*. "Lock-in cognitivo significa que, depois de anos num editor modal, outros ambientes parecem lentos."

## Veja também

- [[02 - Anatomia da sessão de trabalho]]
- [[06 - Ergonomia das mãos]]
- [[03-Dominios/Tecnologia/Terminal/Editor/01 - Modal editing|Modal editing (galho 1)]]
- [[03-Dominios/Tecnologia/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#keyboard-first|keyboard-first]]
- [[Dicionário do Terminal#RSI|RSI]]

## Referências

- Modal editor (Wikipedia): https://en.wikipedia.org/wiki/Modal_editor
- Emacs FAQ — RSI: https://www.gnu.org/software/emacs/manual/html_node/efaq/RSI.html
