---
title: "05 - Few-shot examples — exemplos como contrato"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - prompt-engineering
  - ia
  - few-shot
publish: true
aliases:
  - Few-shot prompting
  - In-context learning
  - Exemplos no prompt
---

# 05 - Few-shot examples — exemplos como contrato

> [!abstract] TL;DR
> Few-shot é o ato de incluir **exemplos de input → output** no prompt antes da tarefa real. Funciona porque mostrar é semanticamente denso: o modelo extrai padrão de estilo, formato, profundidade e critério de sucesso a partir de 2-5 exemplos com muito mais precisão do que da descrição em prosa. Mas é também o lugar onde o prompt **envenena** com mais facilidade: exemplos inconsistentes entre si, exemplos que contradizem as instruções escritas, ou exemplos demais do mesmo tipo arruínam o output. Esta nota cobre por que funciona, princípios anti-poison, e um template prático.

## Por que exemplos batem instruções abstratas

Descrever "tom direto" é vago. Mostrar três exemplos de tom direto define **o que conta** com precisão que nenhuma instrução em prosa alcança. O modelo está treinado pra continuar padrões; few-shot dá ao modelo o padrão exato a continuar.

Três razões mais específicas:

1. **Densidade semântica.** Um exemplo curto codifica simultaneamente formato, vocabulário, profundidade, postura. Descrever esses quatro vetores em palavras leva parágrafos — e ainda fica ambíguo.
2. **In-context learning.** O modelo aprendeu, no treino, a usar exemplos no contexto pra inferir tarefa. Few-shot ativa essa habilidade diretamente. O paper *Language Models are Few-Shot Learners* (GPT-3, 2020) cunhou o termo justamente porque o efeito é desproporcional ao número de exemplos.
3. **Compressão.** Três exemplos de 100 tokens cada (300 tokens total) frequentemente sobem qualidade mais do que 500 tokens de instrução em prosa. ROI por token é altíssimo.

## A regra prática: 3 a 5 exemplos

A literatura empírica e a prática convergem nessa faixa:

- **1 exemplo:** o modelo pode tratar como caso especial, não generalizar.
- **2-3 exemplos:** ponto de inflexão — o modelo identifica padrão sem overfit.
- **3-5 exemplos:** zona ideal pra maioria das tarefas.
- **6+ exemplos:** rendimento decrescente. Tokens caros, e variação entre exemplos vira ruído.
- **10+ exemplos:** considere fine-tuning em vez de prompt.

Exceção: tarefas de classificação com muitas classes podem precisar de exemplos por classe — aí a contagem cresce e o trade-off muda.

## Princípios anti-poison

Few-shot é o mecanismo onde o prompt envenena mais fácil. Quatro princípios pra não estragar:

### 1. Consistência entre exemplos

Todos os exemplos devem demonstrar o **mesmo** padrão. Variação inconsistente confunde o modelo: ele começa a alternar entre estilos e formatos.

```
RUIM:
Exemplo 1: bullets curtos
Exemplo 2: parágrafo único
Exemplo 3: bullets com sub-bullets

(o modelo agora não sabe se a tarefa pede bullets ou parágrafo)

BOM:
Exemplo 1: 3 bullets de uma linha
Exemplo 2: 3 bullets de uma linha
Exemplo 3: 3 bullets de uma linha

(padrão claro: 3 bullets de uma linha)
```

### 2. Exemplos não contradizendo instruções

Se o prompt diz *"sem listas numeradas"* mas dois dos três exemplos usam listas numeradas, o modelo segue os exemplos — eles são mais concretos que a instrução. **Exemplo vence prosa.** Se houver conflito, o output vai pro lado do exemplo.

Regra: depois de escrever exemplos, releia as instruções e elimine qualquer cláusula que os exemplos violem. Ou ajuste os exemplos.

### 3. Cobertura, não repetição

Os 3-5 exemplos devem cobrir **a variação esperada** dos inputs reais, não repetir o mesmo caso. Se todos os exemplos têm input curto e output curto, o modelo pode falhar com input longo.

Estratégia: pense em 2-3 *tipos* de input que vão chegar em produção. Inclua um exemplo de cada tipo.

### 4. Sem labels enviesados

Em tarefas de classificação, ordene labels aleatoriamente. Se os primeiros 3 exemplos são todos "positivo" e o quarto é "negativo", o modelo aprende uma frequência relativa que não existe na tarefa real.

## Template

Um esqueleto reutilizável:

```
Use os exemplos abaixo para aprender o padrão de estilo.
Padrão a preservar: <descrição curta do que generalizar>.
Não copie o wording dos exemplos — copie o padrão.

---
Exemplo 1
Input: <input concreto>
Output: <output desejado>
---
Exemplo 2
Input: <input concreto>
Output: <output desejado>
---
Exemplo 3
Input: <input concreto>
Output: <output desejado>
---

Agora aplique o mesmo padrão ao input real:

Input: <input real>
Output:
```

A linha *"Não copie o wording dos exemplos — copie o padrão"* é importante: sem ela, o modelo pode regurgitar frases dos exemplos no output. Com ela, o modelo é orientado a abstrair.

A linha *"Padrão a preservar"* dá ao modelo a chave de leitura — o que olhar nos exemplos. Sem ela, o modelo pode generalizar a dimensão errada (copiar comprimento quando você queria que copiasse tom).

## Quando few-shot não é a alavanca certa

- **Quando o output precisa ser único.** Few-shot tende a homogeneizar. Para geração criativa diversa, prefira role + temperature alta.
- **Quando a tarefa muda a cada chamada.** Se cada input é radicalmente diferente, exemplos podem confundir mais do que ajudar. Use zero-shot com instrução explícita.
- **Quando o ganho não compensa o custo.** Cada exemplo entra na janela de contexto. Em chamadas de alta frequência, considere fine-tuning.

## Few-shot vs CoT vs zero-shot — onde isso encaixa

Esta nota cobre o que faz few-shot **funcionar** em profundidade. Para a taxonomia mais larga das técnicas de prompting (zero-shot, few-shot, chain-of-thought, tree-of-thought), e quando escolher uma em vez de outra, ver [[03-Dominios/Tecnologia/IA/Context Engineering/15 - Técnicas de prompting — zero-shot, few-shot, CoT, ToT|Context Engineering — Técnicas de prompting]]. Aqui o foco é a disciplina específica: como montar exemplos que não envenenam.

## Pitfall: exemplo único como "exemplo"

Um exemplo só não é few-shot — é one-shot. E one-shot é frequentemente pior que zero-shot porque o modelo trata como caso particular. Se você vai colocar exemplo, coloque pelo menos dois (idealmente três). Um exemplo sozinho funciona como template a copiar, não como padrão a generalizar.

## Pitfall: vazamento de identificadores

Se os exemplos têm nomes, datas, IDs concretos, o modelo pode reaproveitar esses no output real. Sanitize:

- Trocar nomes por placeholders ("User A", "User B").
- Trocar datas por datas relativas ("D-7", "D").
- Remover IDs que pareçam reais.

Caso contrário, você arrisca o modelo cuspir um exemplo no output final como se fosse resposta verdadeira.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #4. Origem da framing "exemplos como contrato" e princípios anti-poison.
- **Brown et al.** — *Language Models are Few-Shot Learners* ([arxiv:2005.14165](https://arxiv.org/abs/2005.14165), 2020). Paper que cunhou o termo.
- **Schulhoff et al.** — *The Prompt Report* ([arxiv:2406.06608](https://arxiv.org/abs/2406.06608)), seção sobre few-shot e ordering effects.
- **Anthropic** — *Use examples (multishot prompting)* (docs.anthropic.com).

## Veja também

- [[03-Dominios/Tecnologia/IA/Context Engineering/15 - Técnicas de prompting — zero-shot, few-shot, CoT, ToT|Técnicas de prompting — taxonomia]] — onde few-shot mora dentro do catálogo maior
- [[02 - Especificidade — a primeira disciplina]] — exemplos só funcionam se a tarefa-base já é específica
- [[03 - Roles e personas — escolhendo o juízo do modelo]] — role estabelece juízo; exemplos estabelecem padrão
- [[06 - Constraints declarativas — boundaries como engenharia]] — quando exemplos contradizem constraints, constraints perdem
