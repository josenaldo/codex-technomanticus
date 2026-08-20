---
title: "Transições de contexto"
created: 2026-05-24
updated: 2026-05-24
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - terminal
  - workflow
  - magus
  - contexto
  - meta
aliases:
  - Transições contexto
  - Context switching
---

# Transições de contexto

> [!abstract] TL;DR
> Deep work (trabalho focado cognitivamente exigente) e shallow tasks (tarefas rasas) exigem contextos diferentes. Cada troca entre eles tem custo cognitivo real: 10-30min pra "voltar" ao estado mental anterior. Estratégia: políticas explícitas — uma tab = um contexto, sessões persistentes pra deep work e efêmeras pra shallow, focus mode quando precisar isolamento. Como fechar contextos sem perder estado: detach + `:mksession` no nvim + notas TODO em scratch file por projeto.

## O que é / Como funciona

### Deep work vs shallow tasks

**Deep work** é atividade focada e cognitivamente exigente, sustentada por 1-4h, que produz valor único e difícil de replicar. Termo cunhado por Cal Newport no livro homônimo. Exemplos: implementar feature complexa, desenhar arquitetura, depurar bug elusivo, escrever documentação técnica densa.

**Shallow tasks** são atividades logísticas ou repetitivas — emails, tickets pequenos, syncs, code reviews curtos — tipicamente reativas, com duração de minutos cada e baixa profundidade cognitiva por unidade.

A maioria dos devs opera 80% do tempo em shallow e 20% em deep. A tese central de Newport: inverter essa proporção (ou pelo menos atingir 60/40) é o que diferencia performance mediocre de performance de elite.

### Switching cost cognitivo

Voltar ao estado mental de uma tarefa pesada após interrupção custa 10-30min de "reaquecimento" — o cérebro precisa recarregar working memory, retomar o contexto, religar os fios do raciocínio.

Isso não é mito: pesquisa em neurociência documenta o fenômeno como **attention residue** (Sophie Leroy, 2009) — parte da atenção permanece na tarefa anterior mesmo depois de você "mudar" para outra. 5 switches por dia = 1h+ desperdiçada só em reaquecimento.

Implicação prática: **blocos longos ininterruptos são exponencialmente mais produtivos** do que muitos blocos curtos do mesmo tempo total.

### Sessions efêmeras vs persistentes — política por contexto

| Tipo | Quando usar | Comportamento ao fechar |
|---|---|---|
| **Efêmera** | Shallow tasks one-shot | Some ao kill/detach final |
| **Persistente** | Deep work, projetos contínuos | Preserva estado indefinidamente |

O erro clássico: usar sessão efêmera pra deep work. O contexto some; amanhã você recomeça do zero.

A política: nomeie sessões de deep work (`zellij -s myproj-core`); deixe shallow tasks em sessões anônimas que não merecem ser preservadas.

### Uma tab = um contexto

Cada tab tem um papel fixo — não misturar:

| Tab | Papel | O que roda |
|---|---|---|
| `code` | Lê e edita código | nvim, editor |
| `server` | App em execução | processo rodando, logs |
| `test` | Suites de teste | `npm test`, watch mode |
| `git` | Operações git | lazygit, `git log` |

Violação típica: rodar testes na tab `code` porque "é só um `npm test` rápido". O efeito: a tab perde identidade, você perde a localização mental.

### Focus mode em deep work

Zellij: `Alt-f` esconde status bar e tabs bar, maximizando a área de código. É mais do que estética — é um sinal explícito pro cérebro: **"entramos em modo de trabalho profundo"**.

Complementar com: DND no OS, Slack pausado, notificações silenciadas. O ritual importa — o cérebro aprende a associar o estado visual com o estado mental.

## Na prática

### Política diária

```text
08h-10h:   Deep work bloco 1 (sessão persistente, focus mode)
10h-11h:   Shallow / emails / tickets (sessões efêmeras)
11h-13h:   Deep work bloco 2
13h-14h:   Almoço (away from keyboard — pausa real)
14h-15h:   Code review (cf. nota 05)
15h-17h:   Deep work bloco 3 OU continuation
17h-18h:   Tear-down + planning amanhã (cf. nota 04)
```

Hábito: colocar no calendário e honrar. Comunicar ao time os blocos de deep work com antecedência.

### Como fechar contexto sem perder estado

O objetivo: amanhã você abre o terminal e em 2 minutos está no mesmo ponto de ontem.

**nvim — salvar sessão:**

```bash
# dentro do nvim, antes de fechar:
:mksession ~/.sessions/myproj.vim

# restaurar amanhã:
nvim -S ~/.sessions/myproj.vim
```

**Zellij — detach (preserva tudo):**

```bash
# detach sem matar sessão:
zellij d
# ou: Ctrl-G d (se leader key for Ctrl-G)

# amanhã, reconectar:
zellij a -n myproj-core
```

**Scratch file por projeto:**

```bash
# anotar próximo passo antes de sair:
nvim ~/scratch/myproj-todo.md
```

Linha de exemplo no scratch:

```text
2026-05-24 EOD: continuar de src/auth.ts:142 — falta caso edge de token expirado
próximo: escrever teste pra esse edge case antes de implementar
```

Quando voltar: lê o scratch antes de abrir o código. Contexto reconstruído em <5min.

### Quando aceitar shallow vs adiar

| Situação | Resposta |
|---|---|
| DM: cliente, prod down, urgência real | Atender imediatamente |
| Email "quando puder" | Batch: responder 2x/dia, não no momento |
| Sync recorrente (14h) | Bloco fixo; não interrompe deep work |
| Notificação aleatória de Slack | Silenciar; responder no próximo batch |

A pergunta-chave: **"se eu não responder agora, algo quebra em produção ou alguém fica bloqueado por horas?"** Se não, pode esperar o próximo batch.

### Memória muscular — construir

Atalhos repetidos viram automáticos em 2-4 semanas de uso deliberado. Estratégia: 1 atalho por dia, usar 20+ vezes no dia. Não tente memorizar 50 atalhos numa semana — nenhum vai virar muscular.

## Armadilhas

1. **Confundir "estar ocupado" com deep work**
   - **Causa:** muitas tasks pequenas dão sensação de produtividade.
   - **Sintoma:** ao fim do dia, 8h trabalhadas e nada importante avançou.
   - **Como detectar:** escrever ao final do dia: "o que avancei substancialmente?" — se a lista é só tasks pequenas, foi shallow.
   - **Solução:** bloquear 2-4h/dia explicitamente pra deep work. Calendário; comunicar ao time; desligar notificações.

2. **Deep work sem mudança visível de contexto**
   - **Causa:** "Vou começar deep" sem ritual de entrada — mesma tab, mesma sessão, sem focus mode.
   - **Sintoma:** mente fica saltando pra emails e Slack nos primeiros 10min.
   - **Como detectar:** notar urgência de checar Slack em menos de 10min de "deep work".
   - **Solução:** abrir nova sessão Zellij nomeada + ativar focus mode. Sinal claro pro cérebro de que o modo mudou.

3. **Confundir descanso com mais shallow tasks**
   - **Causa:** "Vou descansar respondendo emails".
   - **Sintoma:** cansaço cumulativo; deep work do bloco 2 começa já comprometido.
   - **Como detectar:** energia ao fim do dia abaixo do esperado, apesar de "pouco trabalho pesado".
   - **Solução:** pausa real = away from keyboard. Caminhar, alongar, água. Não "checagem rápida".

4. **Não fechar contextos — abrir do zero cada vez**
   - **Causa:** sem ritual de tear-down (cf. nota 04).
   - **Sintoma:** segunda-feira reconstruindo mentalmente o que sexta deixou; 30-60min perdidos.
   - **Como detectar:** ao começar o dia, sentir que está "achando o lugar" em vez de continuar de onde parou.
   - **Solução:** scratch file por projeto + `:mksession` no nvim + detach Zellij. Próximo dia: abrir tudo, contexto reconstrói em minutos.

5. **Atender cada DM durante deep work**
   - **Causa:** "Vai ser rápido".
   - **Sintoma:** bloco de deep work fragmentado em intervalos de 5 minutos efetivos; switching cost acumulado.
   - **Como detectar:** contar quantas vezes abriu Slack/DM durante o bloco.
   - **Solução:** DND (do not disturb) explícito durante o bloco. Comunicar ao time: "estou em deep work até X horas". Emergências reais vão por canal de emergência — não DM casual.

6. **Usar sessão efêmera pra deep work**
   - **Causa:** abrir Zellij sem nomear a sessão.
   - **Sintoma:** estado da sessão perdido após fechar o emulator ou reboot.
   - **Como detectar:** tentar reconectar uma sessão de ontem e não encontrar.
   - **Solução:** sempre nomear sessões de deep work: `zellij -s myproj-core`. Sessões efêmeras são pra tasks descartáveis.

## Em inglês

- **Deep work** — *deep work*. "Vou bloquear a manhã pra deep work, sem interrupções."
- **Shallow task** — *shallow task*. "Responder emails é uma shallow task — pode ir pro batch da tarde."
- **Context switching** — *context switching*. "Cada context switching de tarefa pesada custa 10 minutos de reaquecimento."
- **Switching cost** — *switching cost*. "O switching cost entre deep e shallow é alto demais pra ignorar."
- **Attention residue** — *attention residue*. "A atenção residual da reunião de manhã ainda me atrapalha no código."
- **Focus mode** — *focus mode*. "Ativei o focus mode no Zellij e no OS pra bloquear notificações."
- **Do not disturb (DND)** — *do not disturb (DND)*. "Coloquei DND no Slack durante o bloco de deep work."
- **Scratch file** — *scratch file*. "Deixo o próximo passo anotado no scratch file antes de fechar."
- **Working memory** — *working memory*. "A working memory não aguenta múltiplos contextos simultâneos."
- **Time-boxing** — *time-boxing*. "Time-boxing os blocos de deep work ajuda a honrar o calendário."

## Veja também

- [[01 - Filosofia keyboard-first — quando vale e quando não]]
- [[02 - Anatomia da sessão de trabalho]]
- [[04 - Setup matinal e tear-down]]
- [[06 - Ergonomia das mãos]]
- [[03-Dominios/Tecnologia/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#deep work|deep work]]
- [[Dicionário do Terminal#shallow task|shallow task]]
- [[Dicionário do Terminal#switching cost|switching cost]]
- [[Dicionário do Terminal#context switching cost|context switching cost]]

## Referências

- [Context switch — Wikipedia](https://en.wikipedia.org/wiki/Context_switch)
- [Deep Work — Cal Newport (Wikipedia)](https://en.wikipedia.org/wiki/Deep_work)
