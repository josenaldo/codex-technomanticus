---
name: enriquecer-galho
description: >
  Coordena o enriquecimento de um galho inteiro, nota a nota, com governança de tokens via
  ccusage e memória permanente em disco (roadmap.md). Roda em Opus/opusplan (é coordenação
  pura — nunca enriquece notas diretamente). Use quando o usuário pedir "enriquecer galho",
  "enriquecer o galho X", "rodar enriquecimento do galho", "continuar enriquecimento de
  <pasta>", ou "retomar enriquecer-galho".
---

# Skill: enriquecer-galho

Coordenador de enriquecimento de galho. Recebe o caminho de uma pasta de galho e decide:
ou gera o diagnóstico (se ainda não existe `roadmap.md`) ou executa o loop nota a nota.

**Este coordenador roda em Opus (opusplan).** É tarefa de coordenação — mantém estado da
sessão, governa tokens, despacha subagentes. Nunca enriquece notas por conta própria.

---

## Invocação

```
/enriquecer-galho <path-do-galho>
```

- `<path-do-galho>`: caminho absoluto (ou relativo à raiz do vault) da pasta do galho.
  Ex: `03-Dominios/Tecnologia/IA/Anatomia dos LLMs`

---

## Roteamento de entrada

Antes de qualquer ação, cheque se `<path>/roadmap.md` existe:

```bash
ls "<path-absoluto-do-galho>/roadmap.md" 2>/dev/null
```

### Caso A — roadmap.md NÃO existe

Invoque `diagnosticar-galho <path>` e **PARE**.

Informe o usuário:

```
roadmap.md não encontrado em <path>.
Invocando /diagnosticar-galho para gerar o diagnóstico.

<output do diagnosticar-galho>

Diagnóstico pronto. Revise o roadmap.md antes de prosseguir.
Quando aprovado, rode novamente: /enriquecer-galho <path>
```

Não entre no loop de execução. A revisão humana do diagnóstico é pré-condição.

### Caso B — roadmap.md existe

Entre no **loop de execução** (seção abaixo).

---

## Loop de execução

O loop é o coração desta skill. Repete até que não haja mais `⬜` ou até uma parada forçada.

### Passo 1 — Releitura do roadmap

Leia `<path>/roadmap.md` na íntegra. Colete as notas com estado `⬜ pendente`.

Ignore `✅ feita`, `➖ não precisa` e `🔄 em andamento` — estas nunca são retocadas nesta
rodada. `🔄` em particular indica subagente despachado em sessão anterior que não concluiu;
trate como `⬜` (re-despache), já que o subagente não está mais ativo.

### Passo 2 — Verificação de conclusão

Se **zero `⬜`** (e zero `🔄`):

```
Galho <nome> concluído — todas as notas enriquecidas ou dispensadas.
roadmap.md: <N> ✅ feita · <M> ➖ não precisa · 0 ⬜ pendente · 0 🔄 em andamento
```

Encerre a skill. Não há mais trabalho.

### Passo 3 — Governança pré-onda

Execute a checagem de tokens **antes** de cada onda. Veja a seção "Governança de tokens"
abaixo. Se a checagem indicar pausa → escreva o aviso no chat e encerre a skill sem erro.
Não forme onda, não despache nenhum subagente.

### Passo 4 — Formação da onda

Selecione as próximas **≤3 notas `⬜`** (em ordem de aparição no roadmap).

Para cada nota da onda, **antes de despachar o subagente**, marque o estado no roadmap:

```
- **Enriquecimento:** ⬜ pendente
```
→
```
- **Enriquecimento:** 🔄 em andamento
```

Use `Edit` com substituição exata do bloco da nota (old_string = linha `Enriquecimento` com `⬜`,
new_string = linha com `🔄`). Grave no disco antes de avançar. Isso protege contra
re-despacho concorrente: se a sessão for interrompida agora, a nota não reaparece como `⬜`.

### Passo 5 — Despacho dos subagentes

Despache os subagentes da onda em paralelo (uma única mensagem com N tool calls).

**Classificação → modelo do subagente:**

| Classificação | Modelo | effort |
|---------------|--------|--------|
| `[mecânico]` | Haiku | low |
| `[substantivo]` | Sonnet | (padrão) |

Nunca force Opus em subagente — Opus é reservado ao coordenador.

**Prompt de cada subagente (LITERAL — substitua os valores entre `<>`):**

```
Você é um executor de enriquecimento do vault Codex Technomanticus.

## Tarefa

Enriqueça a nota abaixo usando exatamente o plano de execução do roadmap.
Não improvise, não adicione itens fora do plano, não interaja.

## Dados

- **Nota:** `<path-absoluto-da-nota>`
- **Plano de execução (extraído do roadmap):**
<cole aqui o bloco "Plano de execução" da entrada desta nota no roadmap>

## Como executar

Invoque:
  /enriquecer-nota <path-absoluto-da-nota> --auto "<plano de execução acima>"

O modo --auto aplica o plano sem menu de lentes, sem subagente crítico e sem gate de
confirmação. Aplique tudo e relate o que foi feito.

## Relatório esperado

Ao concluir, responda com um resumo de 2-4 linhas:
- O que foi feito (ações executadas do plano)
- Score /verificar-nota pós-enriquecimento (se disponível)
- Qualquer desvio ou item do plano que não pôde ser aplicado e por quê
```

### Passo 6 — Recepção e gravação por nota

**Não espere a onda inteira.** Conforme cada subagente conclui:

1. **Grave `✅` no roadmap imediatamente:**
   - Localize a entrada da nota no roadmap.
   - Substitua `🔄 em andamento` por `✅ feita (<YYYY-MM-DD>)`.
   - Substitua `**Resultado:** —` pelo resumo do subagente (2-4 linhas).
   - Use `Edit` com old_string exato; não edite outros blocos.

2. **Incremente o contador de sessão** (variável interna do coordenador: inicia em 0 nesta
   sessão; não persiste no roadmap — a parada das 15 é por sessão, não por galho).

3. **Execute a governança pós-nota** (seção "Governança de tokens"). Se pausar → encerre.

4. Se o contador atingiu **15** → parada dura (seção "Parada das 15").

5. Caso contrário, volte ao **Passo 1** após a última nota da onda concluir.

---

## Governança de tokens (ccusage)

> `ccusage` lê os JSONL locais do Claude Code — é legível via Bash. O `/usage` é só UI
> e **não é legível pelo modelo**; não o use para esta checagem.
>
> `ccusage` mede a **sessão inteira** (coordenador + todos os subagentes). Por isso, quando
> o trabalho principal (fora do enriquecimento) estiver consumindo tokens, esta checagem
> já reflete isso e cede automaticamente. O enriquecimento é **baixa prioridade**.

### Comando

```bash
ccusage blocks --active --offline --json -t max
```

- `--offline` evita chamada de rede a cada check.
- `--active` retorna só o bloco de 5h em curso.
- **`-t max` é obrigatório:** sem ele o JSON NÃO traz o teto do bloco. Com ele, o JSON ganha
  o objeto `tokenLimitStatus` com `limit`, `projectedUsage` e `percentUsed`.

Extração robusta (evita hand-parse) — o coordenador deve rodar:

```bash
ccusage blocks --active --offline --json -t max \
  | jq '.blocks[0] | {rem: .projection.remainingMinutes, used: .totalTokens, limit: .tokenLimitStatus.limit, projPct: .tokenLimitStatus.percentUsed}'
```

### Parse do resultado (schema REAL do ccusage 18.x)

Sob `.blocks[0]`:

- `.projection.remainingMinutes` → tempo restante do bloco de 5h, em minutos.
- `.totalTokens` → tokens consumidos no bloco até agora (a SESSÃO inteira: main + subagentes).
- `.tokenLimitStatus.limit` → teto do bloco (ex: 207.108.614; derivado do máximo histórico).
- `.tokenLimitStatus.percentUsed` → **projeção** ao fim do bloco como % do teto (já é projeção÷teto).
- `.tokenLimitStatus.projectedUsage` → projeção do total em tokens absolutos.

`usoPct` (uso atual) = `.totalTokens / .tokenLimitStatus.limit × 100`.

### Filosofia: USAR a janela, não desperdiçá-la

O objetivo é **consumir o bloco de 5h**, não economizá-lo — a janela **não acumula**, então terminar
o bloco em 50% = metade desperdiçada. Projeção de 80–95% é **bom** (boa utilização). O único limite
real: **não estourar 100% ANTES do bloco resetar**. Como o ccusage mede a sessão inteira, se o
trabalho principal esquentar a projeção sobe e o enriquecimento cede sozinho — sem teto artificial baixo.

### Critérios de pausa (QUALQUER um)

| Critério | Condição | Razão |
|----------|----------|-------|
| Projeção estoura | `.tokenLimitStatus.percentUsed >= 95` | No ritmo atual o bloco esgota ANTES do reset — aí sim para |
| Tempo baixo | `.projection.remainingMinutes < 15` | Perto do fim do bloco; não iniciar onda que seria cortada |

**NÃO** pause por uso atual alto nem por projeção entre 50–90% — isso é uso saudável da janela, é o
que queremos. O `95` é knob ajustável (deixa margem pro "peak hours: 3–5× faster").

> **Não use `.totalTokens` cru como gate.** Ele soma `cacheReadInputTokens`, que numa sessão longa
> infla muito (o modelo relê o contexto a cada turno) mas é barato/descontado no faturamento real —
> foi o que causou um falso-alarme a 92% projetado quando o uso real era ~42%. Use
> `.tokenLimitStatus.percentUsed` (projeção já ponderada) e/ou `.costUSD`. O `usoPct` cru é só informação.
>
> **Limite de 7 dias:** o `ccusage blocks` só enxerga o bloco de 5h. Se o painel/usuário indicar que
> o **limite semanal** está apertado (>~85%), pause independente do bloco — o semanal é o gargalo
> binário até o reset.

### Ação de pausa

Ao detectar qualquer critério, escreva no chat:

```
[enriquecer-galho] Pausando — governança de tokens ativada.

Snapshot do bloco:
  Usado: <used> / <limit> (<usoPct>%)
  Projeção: <projPct>% do teto
  Tempo restante: <rem> min

Motivo: <cite o critério disparado>

O enriquecimento é baixa prioridade e cede ao trabalho principal da sessão.
Estado gravado no roadmap — retome no próximo bloco/sessão com:
  /enriquecer-galho <path>
```

Encerre a skill sem erro. O roadmap já tem tudo gravado; a retomada é segura.

### Quando rodar a checagem

- **Pré-onda** (Passo 3): antes de despachar qualquer subagente da onda.
- **Pós-nota** (Passo 6, item 3): logo após gravar `✅` de cada nota.

### Falha da ferramenta = PAUSA (fail-safe)

Se o ccusage não estiver disponível, retornar erro, ou o JSON não trouxer `tokenLimitStatus`
(ex: esqueceu o `-t max`, ou o schema mudou), **PAUSE** — não continue às cegas. A governança
de tokens é a razão de existir deste fluxo; rodar sem ela é o pior caso (foi o que queimou a
janela de 5h antes). Avise no chat que a governança não pôde ser lida e que o enriquecimento
parou por segurança; o usuário decide como prosseguir.

---

## Parada dura das 15 (inegociável)

Ao atingir **15 notas enriquecidas na sessão** (contador interno):

```
[enriquecer-galho] Parada das 15 — limite de sessão atingido.

15 notas enriquecidas nesta sessão. Hora de revisar e limpar o contexto.

Próximos passos:
  1. git diff — revise as mudanças e reverta o que não aprovar
  2. /clear — limpa o contexto da sessão (evita imposto de cache-read gigante)
  3. /enriquecer-galho <path> — continua da primeira ⬜ no próximo bloco

O roadmap está atualizado. Não há perda de trabalho.
```

Encerre a skill sem erro. O loop é resumível por design: a próxima invocação relê o roadmap
e continua da primeira `⬜`.

---

## Como cada problema anterior é resolvido

| Problema | Mecanismo |
|----------|-----------|
| Double-work (mesma nota 2×) | Máquina de estados: loop só toca `⬜`; `🔄` protege contra re-despacho concorrente |
| Galho-falso (galho marcado como feito sem ter sido) | Galho só "feito" com zero `⬜` e zero `🔄`; estado por nota gravado em disco após cada execução |
| Fan-out explosivo | Teto de ≤3 concorrentes por onda · `--auto` sem subagente crítico aninhado · governança ccusage pré-onda e pós-nota · parada dura das 15 |

---

## Convenções rígidas

1. **Teto de 3 concorrentes** — nunca mais de 3 subagentes de execução por onda.
2. **Estado por nota antes de avançar** — gravar `🔄` antes de despachar; gravar `✅` antes
   de passar para a próxima nota. Nunca pular esta gravação.
3. **Coordenador só orquestra** — não usa `enriquecer-nota` diretamente sobre nota alguma.
   Toda aplicação de mudança é delegada a subagente.
4. **Nunca marcar galho como "feito" com `⬜` ou `🔄` restantes** — a conclusão do galho
   é uma observação derivada da leitura do roadmap, não uma flag a setar.
5. **Commits são do usuário ou do coordenador** — subagentes de execução não commitam.
   O coordenador pode commitar ao final de uma onda se o usuário combinou isso previamente;
   caso contrário, deixa o staging para o usuário.
6. **Não fabricar dados do usuário** — se o plano do roadmap mencionar exemplos ou projetos
   específicos, não inventar substitutos; se o subagente não tiver como executar um item,
   ele reporta o desvio e segue o restante.
7. **Redundância entre notas é reforço** — não propor deduplicação de conteúdo repetido
   entre notas; linkar em vez de podar.

---

## Modelo dos agentes (opusplan)

| Agente | Modelo | Justificativa |
|--------|--------|---------------|
| Coordenador (`enriquecer-galho`) | **Opus** | Coordenação, governança, estado da sessão |
| Subagente `[mecânico]` | **Haiku, effort low** | Correção barata, sem pesquisa |
| Subagente `[substantivo]` | **Sonnet** | Expansão de conteúdo, pesquisa web |

Subagentes herdam modelo via `CLAUDE_CODE_SUBAGENT_MODEL`. Não forçar Opus em subagente
sem necessidade explícita — Opus é ~5× o custo do Sonnet e é reservado ao coordenador.

---

## Edge cases

| Caso | Comportamento |
|------|---------------|
| `roadmap.md` não existe | Invoca `diagnosticar-galho` e PARA (Roteamento Caso A) |
| `roadmap.md` já existe mas tem `🔄` de sessão anterior | Trata `🔄` como `⬜` — re-despacha o subagente |
| Subagente falha / timeout | Mantém `🔄` no roadmap; avisa no chat; não incrementa contador; prossegue com as demais notas da onda |
| ccusage não instalado / erro de JSON | Avisa no chat que governança está inativa; continua o loop |
| Zero `⬜` no primeiro passo | Reporta conclusão e encerra (Passo 2) |
| Contador chega a 15 no meio de uma onda | Aguarda as notas em voo da onda concluírem (grava ✅), depois aplica a parada |
| Path inválido / pasta não encontrada | Aborta com erro claro; não cria roadmap.md |
