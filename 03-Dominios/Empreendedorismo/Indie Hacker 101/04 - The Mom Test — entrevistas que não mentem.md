---
title: "The Mom Test — entrevistas que não mentem"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - indie-hacker
  - empreendedorismo
  - validacao
  - mom-test
  - customer-discovery
aliases:
  - Mom Test
  - Customer Discovery
  - Entrevistas de validação
---

# The Mom Test — entrevistas que não mentem

> [!abstract] TL;DR
> *The Mom Test* (Rob Fitzpatrick) ensina que a maioria das "validações de ideia" não valida nada — porque as perguntas estão erradas. Se você pergunta "você usaria isso?", a resposta é sempre "sim" — porque pessoas são educadas, não honestas. As três regras: (1) fale sobre a vida deles, não sobre sua ideia; (2) pergunte sobre o passado, não sobre o futuro; (3) fale menos, ouça mais. O sinal real não está em opiniões — está em comportamento: a pessoa já paga por uma solução ruim? Já tentou resolver sozinha? Oferece dinheiro antes de você pedir?

## O que é

O nome do livro vem de uma premissa: até sua mãe mentiria para você sobre sua ideia de startup — não por maldade, mas por amor. Ela vai dizer "que ideia incrível, filho!" porque quer te apoiar, não porque analisou seu TAM. O mesmo vale para amigos, colegas e potenciais clientes em conversas casuais.

O Mom Test é um framework para fazer perguntas que produzem informação real — perguntas tão boas que nem sua mãe consegue mentir na resposta. A mecânica é simples: **nunca pergunte sobre sua ideia; sempre pergunte sobre a vida da pessoa**.

## Por que importa

A causa mais comum de morte de projetos indie hacker não é falta de habilidade técnica — é construir algo que ninguém precisa. E a razão pela qual constroem algo que ninguém precisa é que "validaram" a ideia fazendo perguntas erradas para pessoas erradas que deram respostas educadas.

Validação feita corretamente (com Mom Test) separa indie hackers que constroem para o mercado de indie hackers que constroem para si mesmos.

## Como funciona

### As três regras de ouro

**1. Fale sobre a vida deles, não sobre sua ideia.**

| ❌ Pergunta ruim | ✅ Pergunta boa |
|-----------------|----------------|
| "Eu estou construindo um app de estudo. O que acha?" | "Me conta como você organiza seus estudos hoje." |
| "Você usaria uma ferramenta que cria flashcards automaticamente?" | "Na última vez que precisou revisar algo que estudou semanas atrás, como fez?" |
| "Você acha que devs precisam de ferramentas melhores de estudo?" | "Você comprou alguma ferramenta ou curso nos últimos 6 meses? Qual? Quanto pagou?" |

**2. Pergunte sobre o passado, não sobre o futuro.**

Hipotéticos ("você faria X?") não produzem informação confiável. Comportamento passado é o melhor preditor de comportamento futuro.

- ❌ "Você pagaria $10/mês por isso?" → resposta sempre "talvez"
- ✅ "Quanto você gastou com ferramentas de estudo no último ano?" → resposta concreta
- ✅ "Qual foi a última vez que você parou de usar uma ferramenta de estudo? Por quê?" → revela churn real

**3. Fale menos, ouça mais.**

Se você está falando mais de 30% do tempo, está fazendo pitch, não entrevista. O objetivo é extrair informação, não convencer. Silêncio é ferramenta — deixe a pessoa preencher o silêncio com detalhes que você nunca pensou em perguntar.

### As armadilhas de "bad data"

Fitzpatrick identifica três tipos de dados inúteis que parecem validação:

| Tipo | Exemplo | Por que é inútil |
|------|---------|-----------------|
| **Elogios** | "Que ideia legal!" | Não indica intenção de compra, apenas educação social |
| **Fluff** | "Eu com certeza usaria isso se tivesse tempo" | Hipotético condicional = zero compromisso |
| **Wishlists** | "Seria legal se tivesse feature X, Y e Z" | Feature requests sem contexto de dor real |

### Sinais fortes vs fracos

| Sinal forte ✅ | Sinal fraco ⚠️ |
|---------------|----------------|
| A pessoa já paga por solução ruim (Anki + planilhas + plugins) | "Parece útil" |
| A pessoa pergunta quando fica pronto | "Manda o link quando tiver" |
| A pessoa oferece dinheiro ou pre-order | "Eu pagaria se fosse barato" |
| A pessoa descreve o problema com emoção e detalhes | "Estudo é importante, sim" |
| A pessoa já tentou construir solução própria (scripts, automações) | "Seria legal ter algo assim" |

### O script de entrevista

Uma entrevista Mom Test típica de 20-30 minutos segue este fluxo:

1. **Contexto** (2-3 min): "Me conta o que você estuda/trabalha e como é sua rotina de aprendizado"
2. **Problema** (10-15 min): "Qual a parte mais frustrante? Quando foi a última vez que travou? O que fez?"
3. **Solução atual** (5 min): "O que você usa hoje? Quanto paga? O que funciona e o que não funciona?"
4. **Compromisso** (2-3 min): "Posso te mandar updates? Teria interesse em testar uma versão beta?"

**Não faça:** pitch do produto, demonstração, ou pedido de opinião sobre features.

### Onde encontrar pessoas para entrevistar

| Canal | Acesso | Qualidade |
|-------|--------|-----------|
| LinkedIn (devs que postam sobre estudo/certificações) | Direct message | Alta — contexto visível no perfil |
| Comunidades (Reddit, Discord de devs) | Participar primeiro, entrevistar depois | Alta — autofiltragem por interesse |
| Colegas e ex-colegas | Pedido direto | Média — podem ser educados demais |
| Twitter/X | Reply em threads relevantes | Média — volume baixo, ruído alto |
| Eventos presenciais / meetups | Conversa natural | Alta — contexto rico |

## Na prática

O volume mínimo para padrões confiáveis: **20 entrevistas**. Com menos, você vê anedotas; com 20+, começa a ver padrões repetidos. Quando 5 pessoas independentes descrevem o mesmo problema com as mesmas palavras, você tem sinal.

Documentação de cada entrevista deve registrar:
- Quem (persona, não nome — privacidade)
- Problema descrito
- Solução atual e custo
- Nível de dor (forte / médio / fraco)
- Compromisso obtido (email, pre-order, nada)

## Armadilhas

- **Fazer pitch disfarçado de entrevista.** Se você descreve o produto antes de ouvir o problema, a pessoa vai reagir ao produto, não ao problema. Resultado: validação falsa.

- **Entrevistar apenas amigos e família.** São as piores fontes de dados (Mom Test, literalmente). Busque estranhos que se encaixam na persona.

- **Parar na primeira confirmação.** 3 pessoas disseram que o problema existe ≠ validação. Padrões emergem com 15-20 entrevistas.

- **Confundir "interessante" com "dor".** Muitas coisas são "interessantes" mas ninguém paga para resolver. Dor verdadeira tem sintomas: tempo gasto, dinheiro gasto, frustração real, soluções gambiarras.

- **Não pedir compromisso.** Entrevista sem ask final (email, pre-order, meeting de follow-up) é conversa casual, não validação. Compromisso é o filtro que separa educação de interesse real.

## Veja também

- [[05 - Nicho vs mercado amplo]] — para quem entrevistar
- [[06 - Landing page de validação e sinais de demanda]] — o próximo passo após entrevistas
- [[01 - Bootstrapping vs venture capital]] — por que validação é crítica sem capital
- [[07 - O que é realmente um MVP]] — o que construir após validar

## Referências

- **Fitzpatrick, Rob** — *The Mom Test: How to Talk to Customers and Learn if Your Business is a Good Idea When Everyone is Lying to You*. O livro fundacional. Curto (~130 páginas), prático, sem fluff. Leitura obrigatória #1 desta trilha.
- **Walling, Rob** — *Start Small, Stay Small*. Blueprint para microSaaS que complementa o Mom Test com perspectiva de execução.
- **Kahl, Arvid** — *The Embedded Entrepreneur*. Imersão em comunidades antes de construir — complemento natural ao Mom Test.
