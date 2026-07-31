---
title: "Roadmap — Entrevistas"
created: 2026-07-31
type: meta
publish: false
tags:
  - meta
  - roadmap
  - carreira
  - entrevistas
---

# Roadmap — Entrevistas (galho-folha, construção)

Roadmap do galho `03-Dominios/Carreira/Entrevistas`. **Construção nova** (2026-07-31), aproveitando o método das 5 notas antigas (2026-05) e descartando o resto. Fontes canônicas: literatura de contratação técnica e negociação (Bock, Voss, McDowell), documentação pública de processos seletivos de empresas remotas, e as convenções do próprio vault.

## Escopo: teoria compartilhável, e só

Este galho é **conhecimento geral sobre o processo de entrevista técnica sênior** — o que vale para qualquer candidato. Ele é `publish: true` e vive num repositório público.

> [!danger] O que NUNCA entra neste galho
> **Nenhum dado pessoal do autor.** Nome de empregador, métrica interna de projeto, história própria, resposta própria, currículo, vaga específica, nome de mentoria ou de colegas. Nem em exemplo, nem em citação ilustrativa.
> **Motivo prático:** as notas antigas deste galho traziam nome de empregador atual e métricas internas dele num repositório **público** — exposição que ninguém escolheu conscientemente. A reforma existe também para desfazer isso.
> **Exemplos nas notas** devem ser **genéricos e claramente fictícios** ("uma fintech de 40 pessoas", "um time que herdou um monólito"), nunca casos reais reconhecíveis.

> [!warning] Material de terceiros
> Mentorias pagas, cursos e transcrições de terceiros **não podem ser republicados nem parafraseados de perto** aqui — é repositório público, e a questão é de direito autoral, não só de privacidade. Escrever a partir de fontes citáveis (livros, artigos, documentação pública), sempre.

## A lente deste galho: o que a etapa está realmente avaliando

Todo material de preparação ensina **o que responder**. A lente aqui é outra, e é a que serve a um sênior:

> **Cada etapa e cada pergunta existe para medir alguma coisa — e quase nunca é o que a pergunta literalmente diz.** "Fale sobre você" não pede biografia: mede se você sabe editar. "Conte um conflito" não pede o conflito: mede como você fala de quem discordou de você quando ele não está na sala.

Quem entende o critério improvisa bem sob pergunta nova; quem decora respostas quebra na primeira variação. Daí a seção-lente obrigatória em toda nota: **O que isto está medindo**.

## Fronteiras (cravadas 2026-07-31)

O vault já cobre partes deste assunto, e este galho **não as repete**:

| Tema | Casa canônica | O que fica lá |
| --- | --- | --- |
| Conteúdo **técnico** por domínio em entrevista | ~30 notas `X em entrevista` (CSS 13 · TypeScript 27 · Banco de Dados 16 · Redes 15 · SO 14 · Go 21 · OO 13 · Testes 16 · a11y 20 · Plataforma Web × 7 · React × 4 …) | o que perguntam **sobre aquele tema** e como responder tecnicamente |
| **System design** em entrevista | [[03-Dominios/Engenharia/Arquitetura/System Design/index\|System Design]] — 4 sub-galhos + [[03-Dominios/Engenharia/Arquitetura/System Design/Conduzindo a entrevista completa\|capstone]] | o framework inteiro: clarificar, estimar, diagramar, aprofundar |
| **Inglês** — fluência, vocabulário, articulação | [[03-Dominios/Carreira/Inglês/index\|Carreira/Inglês]] | idioma; aqui só o que é específico de entrevista |
| **Ofício de legado** (tema recorrente em entrevista sênior) | [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index\|Arqueologia]] | o método real, que alimenta as respostas |

**Regra:** este galho trata do processo, do comportamental, da comunicação e da negociação — **nunca** do conteúdo técnico de um domínio.

## Anatomia de cada nota

1. **Cenário** — a situação concreta de entrevista
2. **A ideia / o mecanismo** — o framework ou a dinâmica, com Mermaid onde couber
3. **O que isto está medindo** ← *seção-lente obrigatória*
4. **Armadilhas (reforçada)** — ≥3, com peso no que o sênior erra
5. **Como soa em inglês** — o registro da entrevista internacional + tabela PT↔EN
6. **O que vem a seguir** + **Fontes**

Registro Feynman. Escrever direto, sem gate por nota. Exemplos sempre genéricos.

**`fase:`** por centralidade: Iniciado = o terreno e o funil; Adepto = os formatos e como se estrutura uma resposta; Magus = o que decide no nível sênior.

## Aproveitamento das 5 notas antigas

| Nota antiga | Destino |
| --- | --- |
| `STAR Method.md` | **método aproveitado** (time-box 10/10/60/20, do/don't, power verbs) → nota 06; **exemplos pessoais descartados** |
| `Behavioral Questions.md` | taxonomia aproveitada → nota 07; seção "da minha experiência" **removida** |
| `Communicating Trade-offs.md` | estrutura aproveitada → nota 11; caso pessoal **removido** |
| `Coding Challenges Strategy.md` | aproveitada → nota 08 |
| `System Design Practice.md` | **descartada** — duplica a trilha de System Design; vira a ponte da nota 09 |

Ao fim: as 5 são **removidas** e os inbound (`README.md`, `index.md` da raiz, `04-Sendas/Senda Entrevistas.md`) reapontados para o novo `index.md`.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Notas de conteúdo | 14 |
| Iniciado | 5 |
| Adepto | 5 |
| Magus | 4 |
| ✅ escritas | 10 (Iniciado + Adepto) |
| ⬜ pendentes | 4 (bloco Magus) |
| % concluído | 71% |
| Scaffolding | roadmap.md criado (2026-07-31); index.md ao fechar |

---

## Notas — Iniciado (o terreno e o funil)

#### 01 - O que uma entrevista sênior avalia   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: iniciado · 145 linhas
- **Escopo:** a mudança de critério de júnior para sênior — deixa-se de avaliar **se você sabe** e passa-se a avaliar **julgamento, escopo de impacto e como você opera com outras pessoas**. Por que candidatos tecnicamente fortes são reprovados. O conceito de *signal* (o que o entrevistador está tentando extrair) × *noise*. A lente do galho e o mapa das etapas. Fronteira com as ~30 notas técnicas do vault.

#### 02 - A anatomia do funil internacional   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: iniciado · 145 linhas
- **Escopo:** as fases típicas de um processo remoto internacional — triagem/recruiter screen · hiring manager · deep dive técnico/projetos passados · system design ou painel técnico · cultural/cross-functional · executive round e oferta. Quem conduz cada uma, **o que cada uma decide** e o que a reprova. Mermaid do funil. Por que a mesma história precisa de versões de tamanhos diferentes por etapa.

#### 03 - Fale sobre você — o pitch de abertura   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: iniciado · 141 linhas
- **Nota de nome:** sem aspas no filename — aspas em nome de arquivo quebram slug do Quartz e complicam wikilinks.
- **Escopo:** a pergunta mais previsível e a mais desperdiçada. Ela não pede biografia — mede **edição**: o que você escolhe deixar de fora. A estrutura presente/passado/futuro; o time-box de 2 minutos; a diferença entre a versão para recruiter e a para hiring manager. **Armadilhas:** narrativa cronológica desde a faculdade; listar tecnologias; terminar sem dizer o que se procura.

#### 04 - Contratação remota internacional   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: iniciado · 148 linhas
- **Escopo:** o que muda quando o empregador está em outro país. Modalidades (contrator PJ · EOR/employer of record · CLT local de subsidiária) e o que cada uma implica em estabilidade, benefícios e impostos. Fuso e sobreposição de horário como critério real de seleção. Faixas de comp e a assimetria LATAM↔EUA/Europa. **Sem aconselhamento jurídico ou fiscal** — o galho descreve o terreno e aponta o que perguntar a um contador.

#### 05 - Currículo e LinkedIn como artefatos de triagem   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: iniciado · 126 linhas
- **Escopo:** os dois documentos existem para passar por um filtro, não para contar sua vida. Como ATS e recrutador leem (segundos, por palavra-chave e por métrica). A linha de bullet como unidade: verbo de ação + o que foi feito + resultado mensurável. Por que "responsável por" é a construção mais fraca do gênero. Fecha o bloco Iniciado.

## Notas — Adepto (os formatos e a estrutura da resposta)

#### 06 - STAR e suas variantes   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: adepto · 151 linhas
- **Escopo:** o framework de resposta comportamental e o **time-box** que quase ninguém respeita: Situation 10% · Task 10% · **Action 60%** · Result 20%, alvo de 2 minutos. Por que a Action é o coração (é onde o julgamento aparece) e por que o Result sem número não fecha. Variantes: **STAR-L** (com *Learning*, obrigatória em pergunta de fracasso), PAR, CAR. Uso de "eu" × "nós". **Aproveita o método da nota antiga; exemplos refeitos genéricos.**

#### 07 - A taxonomia das perguntas comportamentais   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: adepto · 129 linhas
- **Escopo:** as famílias — conflito/desacordo · fracasso e erro · liderança sem autoridade · priorização sob restrição · ambiguidade · influência de stakeholder · aprendizado. **O que cada família mede** (a de conflito não mede o conflito: mede como você fala de quem discordou de você). Como uma mesma história serve a várias famílias com ênfase diferente. **Armadilhas:** o fracasso que é humblebrag; culpar terceiros; a história sem sua decisão dentro.

#### 08 - A entrevista técnica - os três formatos   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: adepto · 145 linhas
- **Escopo:** **live coding** (o que se avalia é o processo, não a solução — pensar em voz alta, clarificar antes de escrever, testar), **take-home** (o que realmente diferencia: README, decisões documentadas, escopo respeitado) e **pair programming/debugging ao vivo**. Como pedir ajuda sem parecer perdido. **Armadilhas:** silêncio prolongado; otimizar antes de funcionar; take-home com over-engineering; ignorar o time-box sugerido.

#### 09 - System design em entrevista — a ponte   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: adepto · 89 linhas
- **Escopo:** **nota curta e deliberadamente incompleta.** O que a etapa de system design avalia num sênior (julgamento sob ambiguidade, trade-offs explícitos, saber o que **não** construir) e como ela se encaixa no funil — e então **remete à trilha completa**, que tem framework de 5 notas, building blocks, padrões, 8 walkthroughs e capstone. Existe para o galho não ter um buraco, não para competir.

#### 10 - O banco de histórias   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: adepto · 160 linhas
- **Escopo:** o **método** de construir e indexar um repertório de histórias — sem nenhuma história dentro. Como inventariar (varrer projetos por decisão tomada, não por tecnologia usada); como indexar por **família de pergunta** em vez de por projeto; a regra de cobertura (toda família precisa de ao menos uma); como manter (registrar enquanto acontece, não na véspera). Por que 6-8 histórias bem trabalhadas batem 30 rasas. Fecha o bloco Adepto.

## Notas — Magus (o que decide no nível sênior)

#### 11 - Comunicar trade-offs sob pressão   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** a habilidade que mais separa sênior de pleno na avaliação. A estrutura: opções consideradas → critério de decisão → escolha → **o que se perdeu** → como o custo foi mitigado. Por que admitir o custo **aumenta** a credibilidade. **BLUF** (bottom line up front) como formato de abertura para audiência executiva. Adaptar profundidade à audiência (engenheiro × HM × executivo). **Armadilhas:** apresentar decisão sem alternativa; esconder o custo; profundidade errada para a audiência.

#### 12 - Red flags que sêniores produzem sem perceber   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** o inverso do resto do galho — não o que fazer, mas o que **desqualifica** alguém tecnicamente forte. Falar mal de empregador ou colega; "nós" que esconde a sua parte; não ter perguntas ao fim; rigidez tecnológica ("X é sempre melhor"); não saber dizer o que faria diferente; desprezar o produto ou os usuários; excesso de certeza sobre um sistema que não conhece. **Cada uma com o que o entrevistador infere daquilo.**

#### 13 - A entrevista reversa   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** as suas perguntas são avaliadas — e são a única parte do processo que você controla inteiramente. Perguntas que revelam senioridade (sobre processo de decisão técnica, dívida, on-call, o que mudou depois do último incidente) × perguntas que revelam desinteresse. Como ler as respostas: sinais de disfunção organizacional que aparecem quando se pergunta sobre release, postmortem e prioridade. Também: como avaliar **se você quer o emprego**.

#### 14 - Negociação de oferta (capstone)   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** **FECHA O GALHO.** Por que a negociação começa antes da oferta (a pergunta de expectativa salarial e como não ancorar contra si). **BATNA** e o poder real de ter alternativa. A estrutura da comp além do salário-base (bônus, equity, benefícios, orçamento de equipamento e de aprendizado, dias de férias). Ancoragem e a assimetria LATAM↔hemisfério norte. Como pedir tempo e como recusar sem queimar a ponte. Encerra com o **mapa do galho** — as 14 notas por etapa do funil — e a síntese da lente (o que cada etapa mede).

---

## Próximos passos

1. ✅ Bloco **Iniciado** (01-05) escrito — 2026-07-31. Zero dado pessoal (verificado por grep). Seção-lente presente em todas. A nota 04 leva aviso explícito de que não é aconselhamento jurídico/fiscal.
2. ✅ Bloco **Adepto** (06-10) escrito — 2026-07-31. A 09 é curta de propósito (89 linhas, sem Mermaid): situa a etapa e remete à trilha de System Design, sem competir. A 10 ensina o método do repertório sem conter nenhuma história — o banco de cada pessoa é material privado.
3. ⬜ Escrever o bloco **Magus** (11-14) — a 14 fecha o galho.
4. ⬜ `index.md` novo (MOC por fase + fronteiras).
5. ⬜ **Aposentar as 5 notas antigas** e reapontar os 3 inbound (`README.md`, `index.md` da raiz, `04-Sendas/Senda Entrevistas.md`).
6. ⬜ Atualizar [[00-Meta/Roadmap]] central (Tier 3).

## Disciplina

- Escrita sequencial, uma nota por vez. **Sem fan-out massivo**.
- **Zero dado pessoal.** Exemplos genéricos e fictícios, sempre.
- **Zero paráfrase de material de terceiros.** Fontes citáveis apenas.
- Validar Mermaid: `node .agents/skills/verificar-nota/scripts/validar-mermaid.mjs "<nota>"` (da raiz do repo).
- Frontmatter: `fase:` lowercase, `type: concept`, `publish: true` (é teoria compartilhável — diferente do padrão do galho de Padrões, que era `false`).
- **Git:** stage de paths explícitos e estreitos. Sem `Co-Authored-By`.
