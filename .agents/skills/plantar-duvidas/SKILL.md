---
name: plantar-duvidas
description: >-
  Lê uma nota ou galho como um iniciante confuso e planta callouts `> [!duvida]`
  nos pontos que travam o aprendizado (peças sem encaixe / "lista de
  ingredientes", saltos de dependência, essencial escondido em callout
  colapsado), antes do leitor travar de verdade. Par preventivo da
  /colher-duvidas, que depois resolve as dúvidas plantadas.
---

# Skill: plantar-duvidas

A ponta **preventiva** do loop de dúvidas do padrão [[feedback-padrao-capitulo-livro|capítulo de livro]].
Enquanto a `/colher-duvidas` resolve dúvidas que já existem, esta **encontra** os pontos de confusão
*antes* de você travar uma semana neles — lendo a nota como um iniciante leria, não como quem já sabe.

O eixo é o **olhar do iniciante**: o expert não enxerga o próprio salto (a "maldição do conhecimento").
Esta skill simula deliberadamente o leitor que ainda não tem o contexto e marca onde ele se perderia.

> [!note] Esta skill só PLANTA, não resolve
> Plantar dúvida e respondê-la são trabalhos diferentes (e a separação é proposital). Aqui só inserimos
> os marcadores `[!duvida]`. A resolução — consertar o fluxo ou virar `[!question]` — é da
> [[colher-duvidas|/colher-duvidas]], rodada em seguida.

## Invocação

```
/plantar-duvidas [path]
```

- **Sem `path`:** pergunta a nota/galho.
- **`path` de nota:** lê aquela nota.
- **`path` de pasta (galho):** varre todas as notas de conteúdo (exceto MOC/index).

## O que caça (os smells de "lista de ingredientes")

Lendo na pele de um iniciante **da fase da nota** (`fase:` no frontmatter calibra a régua — iniciante de
Iniciado ≠ iniciante de Magus), procura especificamente:

- **Peças sem encaixe** — conceitos enfileirados sem um exemplo que os use juntos ("ingredientes sem receita").
- **Salto de dependência** — termo/ideia usado antes de ser definido ou motivado.
- **Salto de raciocínio** — "...logo..." / "...portanto..." com o meio omitido.
- **Essencial escondido** — o que é *preciso saber* enterrado num callout colapsado (`[!...]-`).
- **Densidade irregular** — trecho que pula de explicação gentil para banquete denso sem transição.
- **Ponteiro sem ponte** — "como vimos" / "veja a outra nota" onde faltou a costura narrativa.

## Fases

### Fase 1 — Localizar alvo
1. Valida `path`. Se pasta, lista as notas de conteúdo.
2. Lê a(s) nota(s) inteira(s) + `fase:` (default Magus se ausente).

### Fase 2 — Ler como iniciante
Percorre o texto linearmente, **sem usar conhecimento externo para preencher lacunas** — se um passo só
faz sentido para quem já sabe, é um candidato. Acumula os pontos com: localização (seção/trecho), o smell
detectado, e a pergunta que o iniciante faria.

### Fase 3 — Formular na voz do iniciante
Cada dúvida é escrita **como o leitor confuso a faria** — concreta, ingênua, sem jargão de quem já
entendeu. "por que esse √d_k aparece do nada?" e não "discutir a normalização da variância do produto
escalar". A pergunta ruim ensina mal a `/colher-duvidas`.

### Fase 4 — Plano
Apresenta os pontos agrupados por nota: localização + smell + a pergunta proposta + por que um iniciante
travaria ali. Confirmação obrigatória — você desmarca o que for falso-positivo.

### Fase 5 — Plantar
Insere os `> [!duvida]` aprovados nos pontos exatos. **Não altera o conteúdo** — só adiciona marcadores.
Formato:

```md
> [!duvida] <a pergunta, na voz do iniciante>
> <opcional: que smell é — "peças não se encaixam", "termo usado antes de definido"…>
```

### Fase 6 — Relatório
```
PLANTADO — <nota/galho>
✓ <n> dúvidas plantadas (<a> peça-sem-encaixe, <b> salto de dependência, <c> essencial escondido, …)
→ próximo: /colher-duvidas <alvo> para resolver
```

## Convenções rígidas

- **Só planta, nunca resolve nem reescreve** — resolução é da [[colher-duvidas]].
- **Voz do iniciante**, não do expert.
- **Confirmação antes de gravar** — falso-positivo é desmarcado no plano.
- **Não toca o conteúdo** — apenas insere `[!duvida]`.
- **`[!duvida]` é transitório** — renderiza no site; deve ser colhido antes de `git push` ([[feedback-padrao-capitulo-livro]]).
- **Calibra pela fase** — não cobra de uma nota Iniciado o rigor de uma Magus, nem vice-versa.
- Pode ser despachada como **subagente "leitor-cético"** para um galho grande (respeitar o teto de
  fan-out; preferir sequencial em galhos pequenos).

## Edge cases

| Caso | Comportamento |
| ---- | ------------- |
| Nota já tem `[!duvida]` | Não duplica; foca em pontos ainda não marcados |
| Nenhum smell encontrado | Reporta "nada plantado" — a nota leu limpa para a fase |
| `path` é MOC/index | Avisa que MOC não recebe `[!duvida]`; pede a nota de conteúdo |
| Galho grande | Sugere processar nota a nota (ou subagente por nota, dentro do teto de fan-out) |
