---
title: "Convenções de escrita"
created: 2026-04-28
updated: 2026-08-19
type: how-to
status: seedling
tags:
  - guia
  - meta
publish: false
---

# Convenções de escrita

Regras práticas de como escrever notas no Codex. O objetivo é que qualquer nota, criada hoje ou em 5 anos, siga o mesmo padrão e seja recuperável.

## Atomicidade — uma ideia por nota

Cada nota em `03-Dominios/` cobre **uma única ideia evergreen**. Se você está descrevendo dois conceitos relacionados, faça duas notas e linke uma na outra.

Sinais de que a nota deveria virar duas:

- O título usa "e" ou vírgula (`X e Y`, `X, Y, Z`)
- A nota tem dois H2s que poderiam viver sem o outro
- Você se pega escrevendo "veja a outra parte desta nota" — separe

Exceções legítimas: MOCs (índices), Sendas (curadoria) e Interview Notes bilíngues.

## Filename

| Tipo de nota               | Convenção                                                                                          |
| -------------------------- | -------------------------------------------------------------------------------------------------- |
| Domínio (notas atômicas)   | `Nome do Conceito.md` — Title Case, espaços normais (não kebab-case)                               |
| MOC                        | Mesmo nome da pasta (`Java/Java.md`, `Arquitetura/Arquitetura.md`)                                 |
| Glosa                      | `<ano>-<slug-kebab-case>.md` (ex: `2026-ai-now-writes-97-of-my-code.md`); colisão usa `-2`, `-3`   |
| Senda                      | `Senda <Tema>.md` em `04-Sendas/` (flat, sem subpastas)                                            |
| Mestre                     | `Nome do Mestre.md` em `00-Meta/mestres/`                                                          |

A regra geral: o filename deve casar com o `title` do frontmatter. Wikilinks `[[Nome]]` resolvem por filename, então mudar o filename quebra links — Obsidian atualiza wikilinks em renomeações automaticamente, mas só dentro do vault.

## Frontmatter

Mínimo obrigatório em qualquer nota:

```yaml
---
title: "Nome da Nota"
created: 2026-04-28
updated: 2026-04-28
type: <tipo>
status: <status>
tags:
  - 
publish: false
---
```

### `type`

Quem é a nota. Tipos em uso:

- `concept` — nota atômica de um conceito (Domínios)
- `glosa` — fichamento de artigo
- `moc` — índice de área (Map of Content)
- `how-to` — passo-a-passo
- `til` — Today I Learned, aprendizado pontual
- `reference` — material de referência (cheatsheet, tabela)
- `trail` — Senda (curadoria)
- `note` — uso geral (template Templater padrão)

### `status`

Em que fase de cultivo a nota está:

- `seedling` — recém-criada, incompleta, em rascunho. Default de novas notas.
- `evergreen` — madura, revisada, pronta pra ser referenciada. Promova quando a nota for sólida e você confiaria nela numa entrevista.
- `lido` — usado só em Glosas, indica que o artigo foi lido (independe de ter sido processado em Domínio).

Não invente status novos sem registrar em [[Decisões do vault]].

### `publish`

- `publish: false` — default. Não vai pro site Quartz.
- `publish: true` — explicitamente publicado. MOCs e notas evergreen consolidadas.

Detalhes em [[Publicação]].

### `tags`

Tags são complementares aos Domínios — use pra cortes transversais (ex: `interview`, `senior-skills`, `performance`). Evite duplicar a pasta (`#java` numa nota dentro de `Java/` é redundante).

Convenções:

- Lowercase, kebab-case (`design-patterns`, não `DesignPatterns`)
- Hierarquia com `/` quando útil (`carreira/entrevista`)
- Sem caracteres especiais nem acentos

## Estilo de escrita

- **PT-BR** em todo conteúdo autoral. Exceção: seções "How to explain in English" das Interview Notes e citações verbatim em Glosas.
- **Frase direta**. Sujeito + verbo + complemento. Sem rodeios acadêmicos.
- **Voz ativa**. "O Spring injeta o bean" em vez de "o bean é injetado pelo Spring".
- **Negrito** pra termos-chave na primeira menção; depois texto corrido.
- **Code spans** (`backticks`) pra nomes de arquivo, comandos, identificadores de código, e nomes de classes/funções.

## Registro de escrita: Técnica Feynman

O registro autoral do Codex segue a **Técnica Feynman**: escrever como quem ensina, não como quem cataloga. O teste: *"se você não consegue explicar de forma simples, você não entendeu bem o suficiente."*

Regras de registro — aplicam-se a todo conteúdo de domínio, em especial às notas de trilha:

| Princípio | Aplicação |
|-----------|-----------|
| **Problema-primeiro** | Abre com o problema/cenário que o conceito resolve; nunca começa com definição ("X é um...") |
| **Analogia antes da técnica** | Quando o mecanismo for abstrato, 1 analogia concreta antes de explicar (decorativa = ruído) |
| **Por que, não só o quê** | Explica o mecanismo causal — anti-padrão: "X faz Y" sem dizer como/por quê |
| **Pergunta do leitor** | Antes de responder algo não-óbvio, escreve a pergunta que o leitor faria: `> [!question]-` |
| **Camadas explícitas** | Separa sintoma de causa, o quê de por quê, caso normal de edge case |
| **Resumo em 1 linha** | Ao fim da seção principal: "X em uma frase: ..." |
| **Anti-padrão** | Prosa enciclopédica neutra — tecnicamente correta, mas que não antecipa a dúvida do leitor |

O Registro Feynman é o eixo das skills `/escrever-nota` e `/enriquecer-nota`. O critério de auditoria vive na constraint-skill `/verificar-nota` (item P2: "mecanismo explicado"). Referência canônica de como fica bem aplicado: nota `03 - A janela de contexto.md` do galho Anatomia dos LLMs.

## Notas de trilha como capítulo de livro

As notas das trilhas de aprendizado (galhos em fases Iniciado/Adepto/Magus) seguem um padrão mais alto que uma nota de referência: **devem ler como um capítulo de livro que pega o leitor pela mão.** O teste de dois usos define a régua:

1. O autor **consulta** quando esquece o tópico.
2. O autor **entrega a um colega** para aprender o conceito do zero.

O segundo uso é o que exige padrão de livro. A pergunta de aceite: *"este capítulo ensina o conceito do zero, sem buracos, numa ordem de dependência que facilita o aprendizado, e consolida no fim?"*

**Comprimento não é meta — é consequência.** Um capítulo é tão longo quanto o conceito precisa. Mas isso não dispensa o piso: escreva pela necessidade do conceito e **depois** confira o piso — se a nota ficou curta, o diagnóstico correto é quase sempre que o capítulo tem buraco (falta o exemplo trabalhado, falta a divulgação progressiva, falta a armadilha), não que ele estava pronto e curto.

> [!important] Piso de linhas — vigente desde 2026-08-01
> Uma suspensão provisória do piso circulou entre junho e agosto de 2026 e **foi revogada**. O piso vale, por fase: **Iniciado ≥300 · Adepto ≥400 · Magus ≥500** linhas. É o critério T da [[verificar-nota]].
>
> Cruzar o piso com padding é falha pior que ficar abaixo dele. Ficar abaixo é gap registrado no `roadmap.md` do galho, com plano de expansão substantiva nomeado; inflar com prosa vazia corrompe a nota e engana a auditoria. Quando um galho justificar desvio, registre o desvio — não mude a régua em silêncio.

### O smell "lista de ingredientes"

O modo de falha mais comum: conceitos enfileirados sem que as peças se encaixem — o leitor sente que lê uma lista de ingredientes sem a receita. Antídoto obrigatório:

- **≥1 exemplo trabalhado que usa as peças juntas** (não basta explicar cada ingrediente isolado).
- **Divulgação progressiva**: ensine a versão simplificada funcionando primeiro, depois adicione nuance.
- **Transições de encaixe explícitas**: "guarde X, porque o próximo passo precisa dele".

### Exigências de um capítulo

- **Gancho de entrada e de saída autorais** — abrir recapitulando o necessário do capítulo anterior; fechar com a ponte narrativa para o próximo (não só uma lista "Veja também").
- **Essencial fora de callouts colapsados** — o leitor de livro não clica para expandir. O que é *preciso saber* fica no fluxo; o callout é para o que é *interessante saber*.
- **"Veja também" / "Ver mais" são rodapé**, não muleta para o que devia estar no corpo.
- **Ordem de dependência auditada** — cada conceito merecido antes de usado.
- **Consolidação no fim** (um resumo, ou "o conceito em uma frase").
- **Densidade uniforme** entre capítulos do mesmo galho.

### Reconciliação com o uso-referência

Atomicidade (uma ideia por nota) e leitura-de-livro parecem brigar, mas a convenção **broto → galho** resolve: o núcleo numerado é o capítulo linear que ensina; sub-tópicos avançados viram **brotos** (notas `Xa`/`Xb`, `fase: magus`) que servem de profundidade consultável. Núcleo que guia + brotos que aprofundam. Ver [[Decisões do vault]].

### 15 práticas estruturais

Estas práticas emergem da evolução de 4 galhos do vault (Org. de Computadores → Segurança Conceitual → Compiladores e Linguagens → TypeScript). Cada galho adicionou uma camada nova; o padrão atual é a soma de todas. São auditadas pela constraint-skill `/verificar-nota`.

**Abertura e TL;DR**

1. **TL;DR callout denso** — `> [!abstract] TL;DR` com ≥3 linhas que funcionam standalone (não copiar a intro).
2. **Abertura com problema** — 1ª seção ou intro abre com cenário real; nunca começa com definição.

**Estrutura visual**

3. **Diagrama Mermaid com semântica cromática** — azul `#4A90D9` = ok, âmbar `#F5A623` = atenção, vermelho `#D0021B` = erro/impossível. Sempre para mostrar fluxo, contraste ou estrutura — nunca decorativo.
4. **Casos práticos com ≥2 cenários de produção** — não basta 1 exemplo genérico; cada cenário tem contexto e consequência.

**Navegação e síntese**

5. **"O que vem a seguir" como ponte narrativa** — explica por que o próximo conceito importa dado o que acabamos de ver; não é só lista de links.
6. **"X em uma frase"** — síntese Feynman ao final da seção principal ("este mecanismo em uma frase: ...").

**Internacionalização**

7. **Seção "Como explicar em inglês"** — 2-3 frases em inglês natural, prontas para entrevista técnica.
8. **Tabela PT↔EN** — vocabulário técnico do tema mapeado.

**Honestidade técnica**

9. **Código com falha** — mostra o problema antes da solução; nunca só o caminho feliz.
10. **Mecanismo explicado** — por que funciona assim (causalidade), não só o quê.
11. **Armadilhas comuns com `[!warning]` individuais** — cada armadilha em callout próprio (≥3), não lista bullet.

**Profundidade progressiva**

12. **`[!question]-` para perguntas do leitor** — dúvidas que o leitor faria, colapsadas; resolvidas no callout ou no fluxo.
13. **Teoria subjacente (fase Magus)** — conecta ao fundamento formal ou conceitual para notas sênior.
14. **Wikilinks cross-galho** — conecta ao vocabulário de outros domínios, não só ao galho atual.

**Mídia como reforço**

15. **Vídeo/podcast embutido como `[!tip]`** — referência multimídia com transcrição lida; acompanhado de 1-2 frases explicando o que acrescenta que o texto não cobre. Adicionado pela skill `/adicionar-midia`.

## Dúvidas de leitura: `[!duvida]` e `[!question]`

O texto evolui a partir da dificuldade **real** de leitura — não do palpite do autor sobre o que confunde. Dois callouts, com papéis rígidos:

| Callout | Papel | Publica? |
| ------- | ----- | -------- |
| `> [!duvida]` | **Matéria-prima** — a confusão crua, largada no ponto exato em que você travou. Estado de trabalho. | **Não** — limpe antes do deploy |
| `> [!question]` | **Produto** — a conversa que fica: a dúvida + a resposta, no ponto certo do texto. | Sim |

Formato de captura, no calor do momento:

```md
> [!duvida] <a pergunta, como o leitor a faria>
> <opcional: o que exatamente confundiu>
```

O loop **capturar → colher → evoluir** é operado por um par de skills (ver [[skills]] e [[Como usar este vault]]): `/plantar-duvidas` lê como iniciante e **planta** os `[!duvida]` nos pontos confusos (prevenção); `/colher-duvidas` os **colhe** e, para cada um, decide entre **consertar o fluxo** (quando a dúvida é sobre algo essencial) ou **promover a `[!question]`** (quando é uma tangente legítima). A regra de ouro: *callout é para o que é interessante saber; o fluxo é para o que é preciso saber* — nunca remende um conceito central num FAQ. Marcadores `[!duvida]` são transitórios e não devem sobreviver a um `git push`.

## Promoção de status

Quando uma nota merece ir de `seedling` pra `evergreen`:

- Foi revisada pelo menos 2 vezes
- Tem exemplos concretos (não só teoria)
- Tem pelo menos um wikilink saindo dela e um chegando nela
- Você se sentiria confortável citando ela numa entrevista ou conversa técnica

Atualize o campo `updated` quando promover.

## Grafo de skills: o raciocínio por trás do pipeline

O pipeline de escrita do vault usa três tipos de skill:

- **Micro-skills** (atômicas): fazem uma coisa com entrada/saída claras.
- **Meta-skills** (orquestradoras): coordenam micro-skills em fluxo mais longo.
- **Constraint-skills** (verificadoras): auditam sem editar — servem de gate compartilhado.

### O grafo

```
Criação:        /escrever-nota  →  /verificar-nota (gate automático)
                        ↓
Enriquecimento: /enriquecer-nota
                  Fase 0: /verificar-nota → Modo A ou Modo B
                  Lente Mídia: /adicionar-midia
                  Lente Conexões: /verbete
                        ↓
Dúvidas:        /plantar-duvidas → /colher-duvidas
                        ↓
Higiene:        /verificar-wikilinks
```

### Por que não um template fixo?

Templates fixos impõem a mesma estrutura para todos os temas — uma nota sobre álgebra de tipos tem necessidades radicalmente diferentes de uma sobre protocolo de rede. A solução adotada é **núcleo mínimo + menu de seções opcionais**: o núcleo garante coerência mínima; o menu permite que cada tema escolha as seções pertinentes. A constraint-skill `/verificar-nota` audita o resultado sem ter imposto o caminho.

### Por que Modo A e Modo B no `/enriquecer-nota`?

O enriquecimento incremental (Modo A) parte da premissa de que a estrutura já existe — adiciona profundidade, lacunas e novidade. Mas notas antigas do vault (~74 linhas, sem diagrama, sem seção de inglês) têm um **problema estrutural**, não de conteúdo. Para elas, enriquecer conteúdo sem antes construir o esqueleto seria como pintar uma casa sem paredes. O Modo B diagnostica isso via `/verificar-nota` e reconstrói as seções ausentes antes de enriquecer.

### Por que o Registro Feynman está explícito nas skills?

Sem uma linguagem de registro explícita, o conteúdo gerado tende ao modo enciclopédico: correto, mas que não antecipa a dúvida do leitor. O Registro Feynman (problema-primeiro, analogia antes da técnica, mecanismo explicado) é o antídoto — e precisa estar **nomeado** nas skills para que possa ser verificado e exigido, não apenas aspirado.

### Por que mídia tem skill própria?

A análise de vídeo/podcast exige um fluxo distinto do conteúdo textual: download de legendas, análise de relevância (score 0-10), decisão editorial sobre trecho âncora. Separar em `/adicionar-midia` deixa o `/enriquecer-nota` focado em texto e delega a operação de mídia a uma skill especializada — que pode ser invocada diretamente quando o usuário só quer embutir um vídeo sem enriquecer o restante.

## Veja também

- [[Wikilinks e MOCs]] — boas práticas de linking
- [[workflow]] — fluxo entre as zonas
- [[skills]] — catálogo completo das skills do vault
- [[Manutenção do vault]] — quando e como revisar
