
# Usar o comando `ccusage`

# RTK

# Caveman

# Configurar skills

# CLAUDE.md menor

Não deixar arquivos demais abertos no git, sem commit

Não deixar a conversa ficar longa demais



## Diagnóstico

**A foto geral:** 47.2M tokens em 32 dias, 73.3% em **Opus 4.7**. Opus custa ~5x Sonnet e ~25x Haiku. Só esse mix já é o multiplicador principal.

## Top 5 causas, em ordem de impacto

### 1. RTK quase não está rodando — ~2.1M tokens vazando (impacto alto, fix trivial)

`23.908 comandos Bash` e só **65 (0.3%)** passaram por RTK. O hook do Claude Code que reescreve `git status` → `rtk git status` claramente **não está ativando** na maioria das sessões. Quando funciona (4927 comandos), você economizou 85.6%. Fora dele, está sangrando:

- `git log` (4025x) → 639K tokens
- `grep -rn` (2545x) → 376K
- `find` (1368x) → 230K
- `ls -la` (1460x) → 111K
- `tail -30` (1095x) → 265K

**Ação:** verifica o hook agora. Provável que o `settings.json` do projeto api esteja sem o hook RTK ou ele esteja falhando silenciosamente:

```bash
rtk --version && which rtk
cat ~/.claude/settings.json | grep -i rtk
cat /home/josenaldo/repos/medespecialista/api/.claude/settings.json 2>/dev/null | grep -i rtk
```

### 2. Sessões de 8+ horas — 88% do uso de hoje

Sessões longas custam mesmo com cache, porque cada turno relê 150k+ de contexto. Você tem `Auto-compact: true`, mas auto-compact dispara tarde.

**Ação:**

- `/clear` ao trocar de tarefa (nem sempre você precisa do histórico anterior)
- `/compact` proativo quando o contexto passa de ~100k, não esperar o auto
- Background loops (você tem skill `loop` configurada): revisar se algum está rodando esquecido — `loop` em modo dynamic dorme caro

### 3. Subagentes — 54% do uso, `general-purpose` sozinho = 8%

Cada subagente é uma chamada Claude separada com contexto próprio. `general-purpose` é Sonnet/Opus por padrão e infla rápido.

**Ação:**

- Pra **buscas de código**, usar `Explore` (read-only, mais barato) em vez de `general-purpose`
- Pra **investigação simples**, usar Bash/Grep direto em vez de delegar
- Reservar `general-purpose` pra investigações genuinamente multi-passo
- Subagentes `superpowers:*` (19% do uso!): cada skill carrega instruções pesadas + roda agentes próprios. Use só quando realmente precisar do framework — não pra tarefa simples

### 4. Modelo: 73.3% em Opus 4.7

Seu CLAUDE.md já diz "Standard (Sonnet) é default, Opus só pra refactor arquitetural/ADR". Mas a prática está invertida. Provável que sessões antigas em Opus estão sendo continuadas por inércia.

**Ação:**

- `/model sonnet` como default em sessões novas
- Manter Opus pra: ADRs, decisões cross-layer, debugging difícil, planejamento complexo
- Tarefas que **não** precisam de Opus: testes, lint, docs, JSDoc, traduções, fix de import, criar componente seguindo padrão

### 5. Contexto >150k em 85% do uso

Casado com #2. O cache atenua, mas não zera — toda saída de tool re-entra no contexto e infla a próxima rodada.

**Ação:**

- Pra `Read` em arquivos grandes: usar `offset`/`limit` em vez de ler 2000 linhas
- Pra comandos com saída grande (test runs, find, git log): usar `rtk` (que filtra) ou `head`/`tail` específico
- Pra investigações que vão gerar muita saída: delegar pra `Explore` agent (saída fica isolada, retorna só o resumo)

## Plano de economia, por ROI

|#|Ação|Esforço|Economia estimada|
|---|---|---|---|
|1|Reativar hook RTK em todas as sessões|5min|~2.1M tokens/30 dias|
|2|Default `/model sonnet`, Opus sob demanda|0min|~40-60% por sessão típica|
|3|`/clear` ao trocar tarefa, `/compact` proativo|hábito|~30% em sessões longas|
|4|Trocar `general-purpose` por `Explore` em buscas|hábito|~5-8% direto|
|5|Reduzir paralelismo (queue 4+ sessões)|hábito|~36% suavizado|
|6|Auditar plugin `superpowers` — qual skill realmente vale?|30min|até 19%|

## Sobre os 4+ sessões em paralelo (36%)

Você está rodando "várias sessões hoje desde de manhã" e isso aparece nos números. **Todas dividem o mesmo limite semanal.** Se você não precisa delas simultâneas (ex: uma está esperando você revisar enquanto outra implementa), preferir serial — mesmo trabalho, custo distribuído mais uniformemente, e cache de prompt é melhor aproveitado.

## Próximo passo concreto

A correção mais barata e maior impacto é o **#1 (RTK hook)**. Quer que eu verifique agora se o hook está configurado corretamente nos seus `settings.json`?

## Serena
- Instalem Serena (reduz seus tokens absurdamente, sem palhacada de caveman, isso salva token de vdd): https://github.com/oraios/serena
## statusline
- Usem /statusline, voce consegue visualizar em tempo real o uso da sessao, tempo, tokens, modelo, etc, de forma limpa e nativa. Vou deixar abaixo o meu statusline setup caso alguem queira dar uma testada. Ajuda bastante na hora de saber quando compactar a sessao ou nao.