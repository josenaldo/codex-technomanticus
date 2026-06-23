---
name: colher-duvidas
description: >-
  Colhe dúvidas de leitura (callouts `> [!duvida]`) de uma nota ou galho e
  transforma cada uma em melhoria de texto — consertando o fluxo (essencial) ou
  promovendo a um `> [!question]` polido (tangente). É a ponta que RESOLVE
  dúvidas; quem as PLANTA proativamente é a /plantar-duvidas.
---

# Skill: colher-duvidas

Fecha o loop **capturar → colher → evoluir** do padrão [[feedback-padrao-capitulo-livro|capítulo de livro]].
A dúvida real do leitor (um `> [!duvida]` largado no ponto exato em que ele travou) vira combustível
para o texto — não scaffolding jogado fora. É a versão sistematizada de "tirar dúvida no chat e usar
pra evoluir a nota".

O eixo é a **decisão editorial**, não responder por responder: dúvida sobre algo *essencial* conserta o
fluxo; dúvida *tangente* vira conversa permanente (`[!question]`). Nunca remendar conceito load-bearing
num FAQ.

## Invocação

```
/colher-duvidas [path] [dúvidas soltas]
```

- **Sem `path`:** pergunta a nota/galho.
- **`path` de nota:** processa aquela nota.
- **`path` de pasta (galho):** varre todas as notas do galho.
- **Dúvidas soltas (texto livre):** dúvidas ditas na conversa entram no pool junto com os marcadores do
  texto (rota conversacional — você não precisa ter marcado no arquivo).

> [!note] Para PLANTAR dúvidas, use a [[plantar-duvidas|/plantar-duvidas]]
> Esta skill só **resolve** dúvidas que já existem (marcadas no texto ou ditas na conversa). Para uma
> leitura cética que **encontra e planta** os pontos confusos antes de você travar, rode a
> `/plantar-duvidas` primeiro — e depois colha aqui.

## Os dois callouts (regra rígida)

| Callout | Papel | Publica? |
| ------- | ----- | -------- |
| `> [!duvida]` | **matéria-prima** — a confusão crua, estado de trabalho | **Não** (limpar antes de deploy) |
| `> [!question]` | **produto** — a conversa que fica, dúvida + resposta | Sim |

Formato do marcador de captura:

```md
> [!duvida] <a pergunta, como o leitor a faria>
> <opcional: o que exatamente confundiu / "parece lista de ingredientes aqui">
```

> [!warning] `[!duvida]` é transitório
> Marcadores `[!duvida]` não devem sobreviver a um `git push`/deploy — eles renderizam no site. Rode a
> colheita antes de publicar. Quem controla o deploy é o usuário (push manual).

---

## Fases

### Fase 1 — Localizar alvo
1. Valida `path`. Se for pasta, lista as notas (`*.md`, exceto MOC/index).
2. Lê a(s) nota(s) inteira(s) e o frontmatter (`fase:` calibra a régua — default Magus).

### Fase 2 — Coletar dúvidas
Monta o pool a partir de:
- **Marcadores no texto:** todo bloco `> [!duvida]` (com nota + localização da seção).
- **Dúvidas soltas** passadas na invocação.
- **(Opcional) Arcana:** se o usuário citar cards reprovados, cada um vira uma dúvida.

Se o pool estiver vazio e não houver dúvidas soltas → sugere rodar `--cetico` e encerra.

### Fase 3 — Resolver
Para cada dúvida: responde com precisão. Se precisar de fato externo, faz **WebSearch dirigido** e guarda
a fonte ([[feedback-enriquecimento-feynman|registro Feynman]] na redação). Cruza com o resto do galho
para não duplicar ([[feedback-redundancia-entre-notas|redundância é reforço]] — linkar, não podar).

### Fase 4 — Decisão editorial (o coração da skill)
Classifica cada dúvida resolvida:

| Classe | Sinal | Ação |
| ------ | ----- | ---- |
| **Essencial** | É sobre algo que o leitor *precisa* entender pra seguir; a confusão nasceu de um salto/peça-solta no fluxo principal | **Conserta o fluxo**: reescreve o trecho, adiciona o passo de encaixe ou um exemplo trabalhado. O `[!duvida]` é removido (curado). |
| **Tangente** | É um "você deve estar se perguntando" legítimo, interessante mas não load-bearing | **Promove a `[!question]`** (dúvida + resposta) no ponto certo. |
| **Já coberta** | A resposta já está no texto, o leitor só não conectou | Pequeno ajuste de sinalização/transição; remove o `[!duvida]`. |

Regra de ouro: **callout é para o que é interessante saber; o fluxo é para o que é preciso saber.**
Na dúvida entre as duas classes, prefira consertar o fluxo.

### Fase 5 — Plano
Apresenta agrupado por nota, com **diff antes→depois** para reescritas e o texto do novo `[!question]`
para tangentes. Cada item marca a classe e a fonte (se houver). Confirmação obrigatória.

### Fase 6 — Execução
Relê o arquivo antes de cada edição. Para cada item aprovado: aplica a reescrita **ou** insere o
`[!question]`, e **remove o `[!duvida]` correspondente**. Atualiza `updated:` no frontmatter.

### Fase 7 — Relatório
```
COLHIDO — <nota/galho>
✓ <n> dúvidas resolvidas → <a> consertos de fluxo, <b> novos [!question], <c> já cobertas
✓ <k> fontes adicionadas
– <m> dúvidas adiadas (sem resolução clara) — marcadas, ficam no texto
```

---

## Convenções rígidas

- **Confirmação antes de executar** — nenhuma edição sem plano aprovado.
- **Essencial → fluxo; tangente → `[!question]`.** Nunca remendar conceito central num FAQ colapsado.
- **Aditivo + reescrita-com-diff** — não reorganiza a nota inteira; reescrita só via diff aprovado item a item.
- **Nunca remove um `[!duvida]` sem resolvê-lo** (ou sem o usuário mandar adiar).
- **Proveniência** para fatos novos (fonte na seção Referências, nunca no corpo).
- **Não cria notas novas** — exceto quando a decisão for "isto virou um broto" (aí segue
  [[project-broto-galho-convention]]) e o usuário aprovar.
- Casa com `/enriquecer-nota` (pode encadear), com o padrão [[feedback-padrao-capitulo-livro]] e o
  registro [[feedback-enriquecimento-feynman]].

## Edge cases

| Caso | Comportamento |
| ---- | ------------- |
| Nenhum `[!duvida]` e sem dúvidas soltas | Sugere rodar `/plantar-duvidas`; encerra |
| Dúvida sem resolução confiável | Não inventa; mantém o `[!duvida]`, reporta como adiada |
| Reescrita: trecho `antes` não casa exato | Pula o item, avisa; não edita às cegas |
| WebSearch offline | Resolve com o que dá; marca o que ficou sem fonte |
| Dúvida revela que a nota cobre 2 assuntos | Propõe split/broto ([[project-broto-galho-convention]]); não força no FAQ |
| `path` é MOC/index | Avisa que MOC não recebe `[!duvida]`; pede a nota de conteúdo |
