---
title: "Plano — Galho: Currículo"
created: 2026-08-20
type: meta
publish: false
tags:
  - meta
  - spec
  - plano
  - curriculo
  - carreira
---

# Plano de implementação — Galho: Currículo

> **Para quem executa:** SUB-SKILL OBRIGATÓRIA — use `superpowers:subagent-driven-development` (recomendado) ou `superpowers:executing-plans` para executar tarefa a tarefa. Os passos usam checkbox (`- [ ]`) para rastreio.

**Objetivo:** escrever o galho `03-Dominios/Carreira/Currículo/` — 26 notas + 1 broto + MOC + roadmap — ensinando a montar currículo de profissional de TI do estagiário ao staff, organizado pela peça do documento e atravessado pela lente do caminho de entrada no mercado.

**Arquitetura:** três fases (Iniciado 01-09, Adepto 10-19 + broto 18a, Magus 20-26). Cada nota é um arquivo atômico no padrão capítulo de livro. `roadmap.md` é a memória em disco que permite retomar o trabalho entre sessões. A nota 04 é escrita primeiro e serve de gate factual para todas as demais.

**Ferramental:** Obsidian Flavored Markdown, Mermaid, skills do vault `/escrever-nota`, `/verificar-nota`, `/adicionar-midia`, `/plantar-duvidas`, `/verificar-wikilinks`.

**Spec:** `00-Meta/specs/2026-08-20-galho-curriculo-design.md` — o plano argumenta a partir dela; leia as duas.

## Restrições globais

Valem para **toda** tarefa deste plano. Não repetidas em cada uma.

- **Sem quebra manual de linha.** Um parágrafo é uma linha só, por mais longa. Vale dentro de callout, item de lista e célula de tabela. Quebra manual parte wikilinks e quebra o render em tela estreita.
- **Padrão capítulo de livro.** A nota pega o leitor pela mão, com exemplo trabalhado e divulgação progressiva. Não é referência nem lista. O smell a evitar é a "lista de ingredientes".
- **Profundidade.** Faixa alvo ~440-540 linhas por nota, com diagrama Mermaid onde ele mostra mecanismo (não como enfeite). Nota curta é sinal de pesquisa preguiçosa. Capstone e brotos são exceção — o broto é isento do piso.
- **Frontmatter obrigatório:** `title`, `created: 2026-08-20`, `updated`, `type: concept`, `status: seedling`, `fase: iniciado | adepto | magus`, `tags` (incluindo `carreira` e `curriculo`), `publish: true`, `aliases`.
- **Etiqueta de dado, sem exceção.** Todo exemplo carrega `> [!example] Caso real` (com link verificável) ou `> [!example] Caso fictício` (persona declarada).
- **Nada do apocrypha.** Nenhum wikilink, caminho, nome de arquivo ou dado privado de `codex-technomanticus-apocrypha`. Só princípios genéricos, reescritos com palavras próprias.
- **Nunca inventar dado sobre o usuário ou terceiros.** Se faltar contexto, perguntar. Números do autor entram só se públicos no site, no repositório ou num commit.
- **Nenhum data broker como fonte.** RocketReach, ZoomInfo e similares estão proibidos, inclusive como citação.
- **Fonte comercial é declarada como tal.** Ao citar Jobscan, Enhancv, Teal e afins, dizer que vendem otimização de currículo e têm interesse no assunto.
- **Inline code nunca começa com `=`** — quebra o render do Dataview.
- **Título de nota nunca contém `/`** — vira subpasta no Obsidian.
- **Commits sem `Co-Authored-By`.** Stage de caminhos explícitos e conferência de `git diff --cached` antes de commitar; a working tree tem trabalho paralelo do usuário.

## Estrutura de arquivos

```
03-Dominios/Carreira/Currículo/
  index.md                    MOC, três fases
  roadmap.md                  memória em disco, rastreio nota a nota
  01 - Para que serve um currículo.md
  02 - As portas de entrada no mercado.md
  03 - Os seis níveis e o que muda entre eles.md
  04 - Quem lê o seu currículo — e o que a evidência diz.md
  05 - Formato e legibilidade de máquina.md
  06 - Cabeçalho e identidade.md
  07 - O sumário profissional.md
  08 - Formação, cursos e certificações.md
  09 - Habilidades técnicas.md
  10 - Inventário de evidência.md
  11 - A linha de bullet.md
  12 - XYZ, CAR e PAR — e as críticas.md
  13 - Responsabilidade, realização e alavancagem.md
  14 - Números que você pode defender.md
  15 - Quando não há número.md
  16 - A seção de experiência profissional.md
  17 - Projetos, portfólio e GitHub depois da IA.md
  18 - Adaptar por vaga sem reescrever.md
  18a - A carta de apresentação.md
  19 - Declarar lacuna.md
  20 - A âncora.md
  21 - O brag document.md
  22 - O currículo como pipeline.md
  23 - LinkedIn — o par que responde a busca.md
  24 - Mercados, e o Brazilian Cultural Bug.md
  25 - IA nos dois lados.md
  26 - Seis currículos, uma carreira.md
```

Fora da pasta, dois arquivos são modificados no fim: `03-Dominios/Carreira/Entrevistas/05 - Currículo e LinkedIn como artefatos de triagem.md` (podada para ponte), `03-Dominios/Carreira/index.md` (registra o domínio novo) e `00-Meta/Roadmap.md` (registra o galho).

## O gate de cada nota

O equivalente ao ciclo de teste. **Toda** tarefa de nota termina assim, e os passos não são repetidos em cada tarefa abaixo:

- [ ] **G1.** Rodar `/verificar-nota <caminho>` e ler o relatório.
- [ ] **G2.** Corrigir o que o relatório apontar em ESTRUTURA, SINTAXE, PROFUNDIDADE, TAMANHO, LINKS e MÍDIA. Se a régua do checklist não couber no tema da nota, **ajustar a régua e registrar no roadmap — nunca preencher seção para cumprir agenda**.
- [ ] **G3.** Conferir na mão as três restrições que o checklist não pega: nenhuma linha quebrada manualmente, toda etiqueta `[!example]` presente, nenhum vazamento do apocrypha.
- [ ] **G4.** Atualizar a linha da nota em `roadmap.md` (estado, data, o que ficou pendente).
- [ ] **G5.** Commitar com caminhos explícitos, conferindo `git diff --cached` antes.

---

## Bloco A — Andaime e gate factual

### Tarefa 1: Pasta, MOC e roadmap

**Arquivos:**
- Criar: `03-Dominios/Carreira/Currículo/index.md`
- Criar: `03-Dominios/Carreira/Currículo/roadmap.md`
- Modificar: `03-Dominios/Carreira/index.md`

**Interfaces:**
- Produz: os wikilinks canônicos que todas as notas seguintes usam para "Veja também"; a tabela de fronteiras replicada nas notas de borda; o formato de linha do roadmap que o gate G4 atualiza.

- [ ] **Passo 1.** Ler `03-Dominios/Carreira/Entrevistas/index.md` e `03-Dominios/Carreira/Entrevistas/roadmap.md` inteiros. São o molde: o `index.md` novo copia a estrutura (frontmatter `type: moc`, TL;DR em `[!abstract]`, seção "Sobre este galho", tabela de fronteiras, três blocos de fases numerados), e o `roadmap.md` copia o modo de galho-folha de `00-Meta/templates/Template - Roadmap.md`.

- [ ] **Passo 2.** Criar `index.md`. TL;DR declara a tese — *o currículo é a saída de um sistema de evidência, não um documento* — e as duas lentes. A seção "Sobre este galho" declara os seis níveis e as dez portas. A tabela de fronteiras é exatamente a da seção 5 da spec. Os 26 itens entram agrupados em Iniciado / Adepto / Magus, cada um com uma linha de uma frase dizendo o que a nota decide.

- [ ] **Passo 3.** Criar `roadmap.md` com uma entrada por nota: número, título, fase, estado (`pendente`), tarefa correspondente neste plano, e uma coluna de pendências. É a memória que permite retomar o galho em outra sessão.

- [ ] **Passo 4.** Acrescentar a linha do galho novo em `03-Dominios/Carreira/index.md`, na seção "Domínios", junto de Entrevistas, Inglês e Empreendedorismo.

- [ ] **Passo 5.** Rodar `/verificar-wikilinks 03-Dominios/Carreira/Currículo` — nesta altura vai acusar os 26 alvos ainda inexistentes, e isso é esperado. Registrar a contagem no roadmap como linha de base; ela precisa chegar a zero na Tarefa 30.

- [ ] **Passo 6.** Commit.

```bash
git add "03-Dominios/Carreira/Currículo/index.md" "03-Dominios/Carreira/Currículo/roadmap.md" "03-Dominios/Carreira/index.md"
git commit -m "feat(curriculo): abre o galho com MOC e roadmap"
```

### Tarefa 2: Nota 04 — Quem lê o seu currículo, e o que a evidência diz

Escrita **antes** de todas as outras porque estabelece o que o galho pode e não pode afirmar. Toda nota posterior que tocar em ATS, tempo de leitura ou triagem se ancora nesta.

**Arquivos:**
- Criar: `03-Dominios/Carreira/Currículo/04 - Quem lê o seu currículo — e o que a evidência diz.md`
- Modificar: `roadmap.md`

**Interfaces:**
- Produz: os wikilinks de ancoragem que as notas 05, 09, 17, 23 e 25 usam ao invés de repetir as fontes; o vocabulário de três categorias (evidência sólida / plausível não medido / caixa-preta) usado no galho inteiro.

- [ ] **Passo 1.** Reler a seção 8 da spec inteira. Ela já traz as fontes, os mitos e os limites; esta nota é a prosa que os organiza.

- [ ] **Passo 2.** Escrever a nota com esta espinha: os três leitores em sequência (a máquina, a varredura humana, a leitura técnica) → **de onde vem o que você ouviu** (a contaminação comercial, nominal) → os três mitos derrubados um a um, cada um com o que a evidência de fato diz → o que sobrevive → o que é caixa-preta declarada.

  Conteúdo obrigatório, com fonte no corpo do texto:
  - **Não existe rejeição automática por score** na maioria dos casos; o que existe é *knockout question*. Declarar que a fonte deste número é fraca.
  - **"PDF quebra o ATS" é falso como regra.** O que quebra o parsing é a complexidade do documento — duas colunas (o extrator segue ordem de desenho, não ordem visual, e atravessa as colunas), texto dentro de imagem, contato em cabeçalho ou rodapé, tabelas.
  - **Os "6 segundos"** vêm do estudo Ladders 2018, n=30, nunca publicado com revisão por pares, critérios de seleção não divulgados. O padrão de leitura em F sobrevive; o número exato, não.
  - **Texto branco escondido** é extraído normalmente e lido como desonestidade — a ponte para a nota 25.
  - **Caixa-preta declarada:** não há documentação oficial de engenharia do LinkedIn sobre o Recruiter Search, e não há fonte neutra com metodologia pública sobre market share de ATS.

- [ ] **Passo 3.** Diagrama Mermaid dos três leitores em sequência, marcando em cada etapa **o que ela de fato decide** e **qual é a qualidade da evidência** que temos sobre ela. É o diagrama que carrega a tese da nota.

- [ ] **Passo 4.** Seção `## Fontes` com Wilson & Caliskan (AAAI/ACM AIES 2024, arXiv 2407.20371), Duke/USENIX 2026 sobre prompt injection, o PDF do Ladders 2018, e o relatório da Greenhouse — cada um com uma linha dizendo **o que ele mede e onde ele não alcança**.

- [ ] **Passo 5.** Rodar o gate G1-G5.

---

## Bloco B — Iniciado

Ordem de execução: 01, 02, 03, 05, 06, 07, 08, 09. A 04 já foi feita na Tarefa 2.

### Tarefa 3: Nota 01 — Para que serve um currículo

- [ ] Escrever. Espinha: o objetivo único (gerar uma conversa, não relatar uma vida) → os três enquadramentos errados (autobiografia, lista de tudo, vitrine gráfica) → o currículo como peça de comunicação para um leitor apressado e cético cujo trabalho é encontrar motivo para descartar → a formulação que fecha: **remove motivo de descarte e cria motivo de conversa**.
- [ ] Absorver do post do blog a abertura ("alguém tem um template?") e o enquadramento dos três filtros, remetendo à 04 para a evidência.
- [ ] Fechar com o contrapeso honesto que dá crédito ao galho: o currículo te coloca na fila; quem te tira dela costuma ser uma pessoa. Gancho para a 20 e para a 26.
- [ ] Gate G1-G5.

### Tarefa 4: Nota 02 — As portas de entrada no mercado

A nota mais original do bloco. Nenhum guia do mercado a tem.

- [ ] Escrever as dez portas da seção 3.4 da spec, cada uma com: o requisito de acesso, o que ela te dá de evidência, e a dúvida que ela desperta no leitor do currículo.
- [ ] Cravar a tese: **estágio e trainee não são níveis de senioridade — são portas com requisito formal**, e por isso o autodidata entra direto como júnior, competindo com quem já acumulou dois anos de estágio.
- [ ] Usar os dados verificados na fonte, com artigo citado: Lei 11.788/2008 — estágio exige matrícula e frequência regular atestadas pela instituição (Art. 3º, I); não cria vínculo empregatício (Art. 3º); teto de 6h diárias e 30h semanais no ensino superior (Art. 10, II); máximo de 2 anos na mesma parte concedente (Art. 11); bolsa e auxílio-transporte compulsórios no estágio não obrigatório (Art. 12); recesso de 30 dias a partir de 1 ano (Art. 13).
- [ ] Destacar o achado que sustenta a porta 3: o **Art. 2º, § 3º**, na redação dada pela **Lei nº 14.913, de 2024**, equipara extensão, monitoria, **iniciação científica** e intercâmbio no exterior ao estágio quando previstos no projeto pedagógico do curso.
- [ ] Trainee: declarar que **não tem lei própria** — é contratação CLT com todos os direitos, programas tipicamente de 12 a 24 meses, para recém-formados ou com até ~2 anos de formação. Marcar como prática de mercado apurada em fonte secundária (Exame, Serasa Experian, UBES), não como norma.
- [ ] Diagrama Mermaid das dez portas convergindo para os primeiros níveis, mostrando **quais portas cada perfil alcança e quais lhe são fechadas**.
- [ ] `[!example] Caso real` com a trajetória do autor, que atravessa três portas encadeadas: 1999 (virou dev por dentro, aprendendo Access no trabalho) → 2000 (entra na graduação, motivado pela experiência) → 2003 (bolsa de IC no Labbi/UESC, que ele considera sua primeira experiência profissional) → nov/2003 (CEPEDI como Java Júnior, pelo orientador do Labbi, que era diretor) → 2005/2006 (PROPP, com o mesmo orientador, então pró-reitor) → retorno ao CEPEDI. A lição: **as portas se compõem, e quem as abre costuma ser uma pessoa**.
- [ ] `[!example] Caso real` com a trajetória da Cassiana Gabriela Lima Barreto para a porta 2 e a porta 7 — só o que é público nesta nota; o detalhe fica na 26.
- [ ] Gate G1-G5.

### Tarefa 5: Nota 03 — Os seis níveis e o que muda entre eles

Nota-mapa. Ensina a ler o galho e fixa o vocabulário que as 23 notas seguintes usam.

- [ ] Escrever os seis níveis (estagiário, trainee, júnior, pleno, sênior, staff), com o que o leitor do currículo procura em cada um.
- [ ] Explicar o que **sobe** com a senioridade (impacto organizacional, liderança técnica sem cargo de gestão, decisão de arquitetura, mentoria) e o que **desce** (stack linha a linha, tarefa de dia a dia, certificação básica).
- [ ] Regra de páginas por nível, **declarada como convenção de mercado e não como estudo** — a pesquisa não achou fonte primária. Registrar que comprimir currículo de staff em uma página é lido como sinal de que o candidato não percebeu que as regras mudaram.
- [ ] Tabela-mapa: nível × o que o documento precisa provar × onde no galho isso é tratado. É o índice funcional do galho.
- [ ] Gate G1-G5.

### Tarefa 6: Nota 05 — Formato e legibilidade de máquina

- [ ] Escrever: coluna única, texto selecionável, cabeçalho e rodapé, tabelas, conteúdo essencial em imagem, nome do arquivo, idioma.
- [ ] Cravar a correção que o galho deve ao leitor: **"não use Canva" está certo pelo motivo errado.** O problema não é a ferramenta — é o layout de duas colunas e o conteúdo dentro de elemento gráfico. Um PDF de coluna única exportado do Canva passa; um DOCX de duas colunas falha. Ancorar na 04.
- [ ] Ensinar o teste operacional: copiar o texto do PDF e colar num editor de texto puro. Se sair embaralhado, o extrator leu embaralhado.
- [ ] `[!example] Caso real` do pipeline do autor (markdown → pandoc → ODT → PDF com `--reference-doc`), como demonstração de que formato é problema resolvível por ferramenta, com gancho para a 22.
- [ ] Gate G1-G5.

### Tarefa 7: Nota 06 — Cabeçalho e identidade

- [ ] Escrever: nome, e-mail profissional, telefone, LinkedIn com URL personalizada, GitHub, cidade e estado, site.
- [ ] O que não entra, e **por que isso varia por país** — remeter à 24 em vez de dar a regra brasileira como universal.
- [ ] Para vaga remota internacional: fuso e janela de sobreposição declarados explicitamente.
- [ ] `[!example] Caso real` do cabeçalho público do autor, que carrega cargo, âncora, stack, modalidade e fuso em quatro linhas — com gancho para a 20.
- [ ] Variação por nível: o que muda do estagiário ao staff.
- [ ] Gate G1-G5.

### Tarefa 8: Nota 07 — O sumário profissional

- [ ] Escrever: o sumário como trailer, 3 a 5 linhas, respondendo *quem é essa pessoa e por que continuar lendo*.
- [ ] Introduzir **BLUF** aqui: a primeira frase entrega conclusão e impacto; contexto técnico vem depois, e só se sustentar.
- [ ] Explicar por que o sumário substituiu o "objetivo profissional" — o objetivo servia para separar fisicamente currículos entregues na portaria; hoje ele é ruído, porque a vaga já é conhecida.
- [ ] Matar os clichês sem evidência ("comunicativo, proativo, trabalho bem em equipe") mostrando o teste: se todo candidato pode escrever a mesma frase, ela não diz nada.
- [ ] **Seis sumários lado a lado**, um por nível — o coração da lente principal.
- [ ] Gate G1-G5.

### Tarefa 9: Nota 08 — Formação, cursos e certificações

- [ ] Escrever: o que entra, o que não entra, formato da linha, e a posição no documento — sobe quando é o seu principal contexto, desce quando a experiência já fala.
- [ ] Curadoria: por que 30 linhas de curso passam impressão de acúmulo sem direção.
- [ ] Para quem estuda: declarar previsão de conclusão, porque isso informa planejamento de equipe.
- [ ] **Onde o caminho de entrada pesa mais** — a seção muda de peso conforme a porta. Tratar explicitamente bootcamp, curso livre, autodidata sem diploma, e o caso da pós/mestrado/doutorado em transição.
- [ ] Gate G1-G5.

### Tarefa 10: Nota 09 — Habilidades técnicas

- [ ] Escrever: a seção existe para dois leitores com necessidades diferentes — a busca por termo e a leitura humana rápida.
- [ ] Nomear os anti-padrões: a **"lista de ingredientes"** e a **"sopa de letrinhas"**; a barra de proficiência (o que significa "80% de React"?); a lista sem categorias.
- [ ] Usar os mesmos termos da descrição da vaga, não sinônimos — e explicar por que isso é comunicação eficaz, não trapaça.
- [ ] **A regra de lastro**, que é a mais importante da nota: não liste o que você não sustenta numa pergunta. `[!example] Caso real` — o autor removeu Kubernetes da seção de skills por não ter experiência própria, mantendo o bullet que diz "partnered with DevOps to run a Kafka cluster on Kubernetes", porque descreve parceria e é factualmente correto. A distinção entre as duas coisas é a nota inteira.
- [ ] Gate G1-G5.

---

## Bloco C — Adepto

### Tarefa 11: Nota 10 — Inventário de evidência

A ponte entre as duas lentes. Converte porta de entrada em material aproveitável.

- [ ] Para cada uma das dez portas: o que ela produziu de evidência, onde essa evidência costuma estar esquecida, e a dúvida específica que ela desperta no leitor.
- [ ] Tratar com seriedade o que os guias descartam: bolsa de IC, monitoria, extensão, TCC com implementação real, trabalho voluntário técnico, freelance informal, contribuição pequena a open source, automação feita no emprego anterior de outra área.
- [ ] Para transição de carreira, cravar a inversão: a experiência da área anterior é **ativo**, não passivo — e quase todo mundo a esconde.
- [ ] Fechar com o inventário como exercício executável, não como conceito. Gancho para a 21.
- [ ] Gate G1-G5.

### Tarefa 12: Nota 11 — A linha de bullet

- [ ] Escrever: a linha é a unidade de projeto, porque currículo é varrido em linhas, não lido em parágrafos.
- [ ] A fórmula: verbo de ação + o que foi feito + resultado.
- [ ] **"Responsável por" como a construção mais fraca do gênero** — informa o que estava no seu escopo, não o que aconteceu por sua causa. Duas pessoas com a mesma atribuição têm resultados opostos, e é essa diferença que o leitor procura.
- [ ] O teste linha a linha: *outra pessoa no mesmo cargo poderia escrever isto?* Se sim, a linha descreve o cargo, não você.
- [ ] Migrar o diagrama Mermaid da nota 05 de Entrevistas para cá.
- [ ] Tabela de power verbs: substituição cirúrgica de "helped", "participated", "tried", "worked on" pelas formas que declaram propriedade da decisão.
- [ ] `[!example] Caso real` — bullets públicos do autor, mostrando a fórmula operando.
- [ ] Gate G1-G5.

### Tarefa 13: Nota 12 — XYZ, CAR e PAR, e as críticas

- [ ] Apresentar a fórmula XYZ — *accomplished X as measured by Y by doing Z* — atribuindo a origem a **Laszlo Bock**, ex-SVP de People Operations do Google, em *Work Rules!* (2015). Dizer que a popularização como "a fórmula do Google" veio depois e por terceiros.
- [ ] Apresentar CAR e PAR como irmãs, e a relação com STAR (que é de entrevista, não de documento) — gancho para `Entrevistas/06`.
- [ ] **As quatro críticas**, que é o que falta em todo guia: força métrica onde ela não existe; a repetição mecânica denuncia quando todo bullet tem a mesma forma; convida ao arredondamento agressivo, e a credibilidade quebra na primeira pergunta; foi desenhada para a cultura de contratação de uma empresa específica e não transfere sem atrito.
- [ ] Fechar dizendo quando usar e quando abandonar — a fórmula é andaime, não gabarito.
- [ ] Gate G1-G5.

### Tarefa 14: Nota 13 — Responsabilidade, realização e alavancagem

A nota onde a senioridade fica mais nítida.

- [ ] A escada em três degraus: **atribuição** (descreve o cargo) → **realização** (descreve o que mudou por sua causa) → **alavancagem** (descreve o que passou a ser possível para outras pessoas).
- [ ] Nomear os perfis: *task-taker* × *owner* × *force multiplier*.
- [ ] Mostrar **o mesmo trabalho escrito nos três degraus** — é o exemplo trabalhado da nota.
- [ ] Explicar por que o terceiro degrau é o que separa sênior de staff, e por que vender esforço ("trabalhei o fim de semana inteiro") anda para trás enquanto vender sistema ("construí uma ferramenta que devolve N horas por semana ao time") anda para frente.
- [ ] Diagrama Mermaid da escada, com o mesmo fato subindo os três degraus.
- [ ] Gate G1-G5.

### Tarefa 15: Nota 14 — Números que você pode defender

Provavelmente o conteúdo mais original do galho. Nenhum guia de currículo ensina isto.

- [ ] Os três níveis de confiança, com o que cada um autoriza dizer: **medido** (extraído de git, CI ou suíte, com comando reproduzível — pode ser citado com segurança, e mostrar como se chegou lá fortalece); **contado** (contagem manual sobre registro existente — deve nomear a fonte na própria frase e declarar a limitação antes de perguntarem); **lembrado** (memória sem registro recuperável — só ordem de grandeza, e **nunca derive percentual disso**).
- [ ] **Par de números vale mais que percentual.** Um par bruto ("de ~X para ~Y") é uma medição; um percentual é uma afirmação. Percentual calculado sobre baseline lembrada é **falsa precisão** — e é assim que métrica inflada nasce sem ninguém mentir de propósito.
- [ ] **Números aposentados**: o registro de "nunca mais diga isso", e por que ele precisa existir separado.
- [ ] `[!example] Caso real` — o sistema do autor: a auditoria que encontrou o mesmo fato em seis redações divergentes espalhadas por 17 arquivos, e a guarda automatizada que aborta a geração do currículo quando um número aposentado aparece. Gancho para a 22.
- [ ] `[!example] Caso real` — "três codebases" corrigido para "dez repositórios" depois de levantamento na fonte; e o mesmo levantamento mostrando que contar diretórios ingenuamente inflaria o número em 90%. A lição: **verifique o dado difícil antes de escrevê-lo, não depois de ser perguntado**.
- [ ] Gate G1-G5.

### Tarefa 16: Nota 15 — Quando não há número

- [ ] Escrever: nem toda realização tem métrica, e inventar é a única coisa que pode custar a vaga **depois** de conquistada.
- [ ] Onde procurar antes de desistir: tempo (de deploy, de resposta a incidente, de onboarding), volume (requisição, usuário, registro), quantidade (serviço, time, integração), frequência (incidente por mês, release por semana).
- [ ] Quando não houver mesmo: servir **consequência** — o que passou a ser possível depois — em vez de superlativo vago.
- [ ] Tratar o caso de quem não tem experiência nenhuma: a métrica do projeto pessoal existe e quase ninguém a usa (usuários reais, tempo de execução antes e depois, cobertura, tamanho do dado processado).
- [ ] Gate G1-G5.

### Tarefa 17: Nota 16 — A seção de experiência profissional

- [ ] Estrutura da entrada, ordem cronológica inversa, e **densidade decrescente** — a experiência de dez anos atrás não merece o mesmo número de linhas que a atual.
- [ ] A linha de contexto sob o cargo (o que a empresa faz, qual era o escopo), que quase todo currículo esquece e que dá tamanho ao resultado.
- [ ] Tratar com honestidade o que os guias evitam: lacunas de emprego, passagens curtas, PJ e freelance, trabalho por agência ou body shop, e o mesmo empregador com vários cargos.
- [ ] Para quem tem pouca ou nenhuma experiência formal: o que conta, o que não conta, e a regra de não inventar — um currículo com projetos sólidos e sem experiência formal é honesto e funciona; um com experiência fabricada explode na primeira pergunta.
- [ ] Gate G1-G5.

### Tarefa 18: Nota 17 — Projetos, portfólio e GitHub depois da IA

- [ ] Estrutura da entrada de projeto: nome, link do repositório, link do deploy, o problema em uma linha, tecnologias, desafio técnico enfrentado, status.
- [ ] **A regra do README**: sem README que responda o que é, para que serve e como rodar, o projeto não existe para quem avalia.
- [ ] O que conta e o que não conta — repositório com um commit de "initial commit", projeto de tutorial copiado sem modificação, repositório sem README.
- [ ] **O que a IA mudou**, com a ressalva de que não há estudo quantitativo controlado sobre o peso atual — só leitura de mercado. O projeto genérico saturou como sinal; o que resta valendo é evidência de decisão de engenharia visível no histórico de commits e sistema com uso real.
- [ ] Ancorar a discussão da IA na 04 e na 25 em vez de repetir as fontes.
- [ ] Gate G1-G5.

### Tarefa 19: Nota 18 — Adaptar por vaga sem reescrever

- [ ] A tese: adaptação é **cirúrgica**, não reescrita. O que rende é ter uma base sólida e ajustar duas coisas — o sumário e a ordem e ênfase dos bullets recentes.
- [ ] Usar os termos da descrição da vaga, não sinônimos.
- [ ] `[!example] Caso real` — a lição mais cara do repositório do autor: a reescrita completa do currículo para uma vaga foi **revertida**, e a variante voltou a ser idêntica à base exceto por um bullet. E o corolário: o que se prova geral sobe para a base.
- [ ] `[!example] Caso real` — a reordenação por analogia: promover ao topo a experiência que é o caso análogo ao problema da vaga.
- [ ] Ensinar o critério de parada: quanto de adaptação é adaptação, e a partir de onde vira currículo diferente que você não vai conseguir sustentar.
- [ ] Gate G1-G5.

### Tarefa 20: Broto 18a — A carta de apresentação

Broto sob a nota 18, `fase: magus`, **isento do piso de linhas**. Existe porque a evidência é genuinamente contraditória, e a nota serve para dizer isso com as fontes na mão.

- [ ] Apresentar os dados conflitantes sem escolher um lado: uma fonte de 2025 com 753 recrutadores indica que 89% esperam carta e 83% leem; outra (ResumeBuilder, 2024, 948 líderes nos EUA) indica que só 26% leem regularmente e 44% pulam; um estudo controlado com 7.287 candidaturas achou 53% mais callback com carta personalizada do que sem carta.
- [ ] Declarar que os números não batem, que nenhuma fonte é claramente mais autoritativa, e que a variável provavelmente é região, setor e nível.
- [ ] Dar a regra operacional que sobrevive à incerteza: o custo de escrever uma carta curta e específica é baixo; o custo de mandar carta genérica é negativo. Quando a vaga pede, escreva; quando não pede, escreva se tiver algo que o currículo não comporta.
- [ ] Gate G1-G5, com a régua ajustada para broto (registrar o ajuste no roadmap).

### Tarefa 21: Nota 19 — Declarar lacuna

- [ ] A tese: inflar competência custa a vaga **depois** de conquistada, que é o pior momento possível.
- [ ] **Onde declarar**: na conversa, não no documento. `[!example] Caso real` — o autor removeu do currículo a seção que declarava lacunas de Go, GCP e Terraform, porque a transparência já tinha sido feita por e-mail e a recrutadora respondeu bem; repetir no documento era redundância que custava uma página inteira.
- [ ] A distinção fina que a nota precisa ensinar: descrever parceria não é reivindicar operação. Retomar o caso do Kubernetes da nota 09 pelo outro lado.
- [ ] Como declarar sem se desqualificar: nomear a lacuna, dizer o adjacente que você domina, e dizer o prazo realista de rampa.
- [ ] Gate G1-G5.

---

## Bloco D — Magus

### Tarefa 22: Nota 20 — A âncora

- [ ] A tese: currículo, pitch, resposta comportamental e negociação são **quatro saídas da mesma âncora**. Sem ela, cada saída improvisa uma versão diferente e o leitor sente a inconsistência.
- [ ] O drill-down de quatro camadas, de baixo para cima: **ferramentas** (nenhuma vantagem — todo mundo tem) → **tipo de sistema** (descreve a caixa) → **o movimento que se repete** nos seus projetos → **o diferencial**, que é a âncora.
- [ ] Exercício executável: pegue seus três últimos trabalhos e ache o que se repete entre eles que não seja a stack.
- [ ] `[!example] Caso real` — a âncora pública do autor abrindo o sumário e organizando tudo abaixo dela.
- [ ] Variação por nível: o estagiário também tem âncora, e ela é diferente da do staff — não é conceito reservado a sênior.
- [ ] Diagrama Mermaid do drill-down, com um exemplo subindo as quatro camadas.
- [ ] Gate G1-G5.

### Tarefa 23: Nota 21 — O brag document

- [ ] A tese, na formulação que a justifica: **a nota registra o número, não o trabalho.** Quando chega a hora de escrever o currículo ou responder "me conte sobre um projeto difícil", o número está lá e a história não.
- [ ] A anatomia: **Cheguei** (o estado em que a coisa estava — o problema, não a tarefa; é o que dá tamanho ao resultado) · **Construí** (o que foi feito, com decisões, trade-offs e o que foi rejeitado) · **Resultado** (o que mudou, com o número embutido na frase) · **Evidência** (o comando, o link, o print — como provar quando perguntarem) · **Aprendizado** (opcional, só quando há trade-off que valha declarar).
- [ ] A separação em duas camadas, que é a decisão de desenho não óbvia: métrica de **conquista** (tem início, fim, antes e depois) vive na nota da iniciativa; métrica de **escopo** (muda sozinha com o tempo) vive no dossiê do engajamento. Numa nota de conquista, a de escopo mente no mês seguinte.
- [ ] **A inversão que fecha o galho:** a métrica deixa de ser autorada e passa a ser derivada da conquista. Ligação direta com a 14.
- [ ] Cravar que este é o hábito que quem está começando deveria adotar **hoje**, e não quando for sênior — é o conselho mais valioso do galho para quem lê no começo da carreira.
- [ ] Gate G1-G5.

### Tarefa 24: Nota 22 — O currículo como pipeline

- [ ] A tese: o currículo é a saída de um sistema, e tratá-lo como arquivo solto é o que produz as seis redações divergentes da nota 14.
- [ ] Os componentes: fonte única em texto puro e versionada · base reutilizável × variante por vaga · template que carrega só estilo · guardas automatizadas.
- [ ] **Variante enviada é registro histórico e imutável.** Reabrir a pasta de uma vaga daqui a um ano tem que mostrar exatamente o que o recrutador recebeu, não uma reconstrução que mudou junto com a base. Corrigir um dado exige tocar N arquivos, e os já enviados permanecem com os números antigos — isso é desenho, não descuido.
- [ ] **Guarda que falha em silêncio não é guarda.** `[!example] Caso real` — a verificação de números aposentados que aborta a geração, e o defeito que foi corrigido quando ela podia se desligar sozinha na falta de uma dependência.
- [ ] Escala honesta: o leitor iniciante não precisa de pandoc. Dar a versão mínima do mesmo princípio — um arquivo-fonte, um lugar só para os números, um changelog do que mudou.
- [ ] Diagrama Mermaid do pipeline, da conquista ao PDF entregue.
- [ ] Gate G1-G5.

### Tarefa 25: Nota 23 — LinkedIn, o par que responde a busca

- [ ] A tese: LinkedIn não é currículo em outra plataforma. Ele **responde a busca antes de responder a leitura**, porque é onde o recrutador procura ativamente, com filtro de cargo, tecnologia, localização e senioridade.
- [ ] O que isso muda na prática: o título e os termos determinam se você aparece; aparecer é pré-condição de ser lido.
- [ ] **Consistência com o currículo**: divergência de data ou cargo tem leitura desproporcional ao tamanho do erro. Tratar os dois como uma fonte com duas apresentações, e revisar os dois no mesmo dia.
- [ ] **A caixa-preta, declarada com todas as letras:** não existe documentação oficial de engenharia do LinkedIn sobre o funcionamento do Recruiter Search. Tudo que circula é inferência de terceiros comerciais. A nota diz isso em vez de repetir número de blog como fato.
- [ ] O que é observável e vale registrar como tal, separando do que é especulação.
- [ ] Gate G1-G5.

### Tarefa 26: Nota 24 — Mercados, e o Brazilian Cultural Bug

- [ ] Diferenças por mercado: foto (esperada em parte da Europa continental, desencorajada no Reino Unido, Holanda e EUA), dados pessoais, GDPR, Europass, referências. **Declarar a fragilidade das fontes** — a pesquisa não encontrou nenhuma fonte oficial europeia, só agregadores de blog de carreira.
- [ ] O pareado Brasil × padrão executivo global, que é o coração da nota: alto contexto e narrativa em espiral × BLUF; verbo passivo × verbo que declara propriedade; postura apologética × abrir pelo impacto; "nós" difuso × "eu" cravado; vender sacrifício × vender alavancagem; ancorar em custo de vida × ancorar em valor entregue.
- [ ] A formulação que evita o moralismo: **subestimar-se é lido como impostor, não como humildade** — a diferença é de código cultural, não de caráter, e por isso é aprendível.
- [ ] Idioma: currículo internacional escrito em inglês, não traduzido literalmente do português; construção calcada custa credibilidade.
- [ ] Gate G1-G5.

### Tarefa 27: Nota 25 — IA nos dois lados

- [ ] **Lado do recrutador.** O achado mais sólido do levantamento: Wilson & Caliskan (AAAI/ACM AIES 2024, 550+ currículos reais) — nomes associados a brancos preferidos em 85% dos casos, nomes masculinos em 52%, homens negros a categoria mais penalizada. E o follow-up da UW de nov/2025, sugerindo que humanos expostos a ranking enviesado de IA absorvem o viés. Tratar com a gravidade que o dado tem, sem transformar a nota em panfleto.
- [ ] **Lado do candidato.** Saturação do texto gerado; por que currículo de IA sem personalização é rejeitado; e por que a fonte desses números é frequentemente comercial.
- [ ] **Prompt injection**, com os três dados: Duke/ASU/Berkeley/UNC no USENIX Security de ago/2026, 200.000 currículos reais, ~1% com instrução oculta, incidência 7× maior entre jul/2024 e nov/2025; o gap da Greenhouse entre 41% de autorrelato e 1% de incidência real; e o achado da ACL 2026 de que a tática **funciona justamente enquanto poucos a usam** e se anula com a adoção.
- [ ] Registrar que os pesquisadores de Duke **deliberadamente não testaram** se a instrução influencia a decisão, por razão ética — é um dado sobre o limite do que sabemos, e a nota deve dizê-lo.
- [ ] Fechar com a posição do galho: a tática se anula sozinha, é lida como desonestidade, e está catalogada como risco de segurança. Não é conselho moral — é aritmética.
- [ ] Gate G1-G5.

---

## Bloco E — Capstone e fechamento

### Tarefa 28: Nota 26 — Seis currículos, uma carreira (capstone)

Peça mais cara do galho. Exceção declarada ao teto de linhas.

**Pré-condição:** o currículo da Cassiana precisa ter sido enviado pelo usuário. Ela já aprovou a citação em 2026-08-20. Se o arquivo não estiver disponível na hora de executar esta tarefa, **parar e pedir** — não reconstruir por inferência.

- [ ] Escrever a abertura explicando a composição e a honestidade dela: quatro peças de pessoas reais, uma persona fictícia, uma projeção. Cada peça declara sua natureza no topo.
- [ ] **Estagiário — `[!example] Caso fictício`.** Persona declarada, porque o autor nunca foi estagiário. Construir alguém coerente: graduação em andamento, sem experiência formal, com projeto de disciplina levado além do exercício.
- [ ] **Trainee — `[!example] Caso real`.** Cassiana Gabriela Lima Barreto: engenharia biomédica, mestrado, doutorado em Sistemas Computacionais e dispositivos aplicados à saúde na UFU (2020-2025), Python aprendido durante o doutorado por necessidade da pesquisa, depois banco de dados e dados; entrada na Dadosfera como trainee em 2024 e promoção a júnior pouco mais de um ano depois — **entrou no mercado antes de concluir o doutorado**. Fontes admitidas: LinkedIn, página de carreiras da Dadosfera (onde há depoimento público em primeira pessoa), UFU, DIO, publicações. **Nenhum data broker.** Confirmar com ela, antes de escrever, se a leitura correta é engenharia de dados ou ciência de dados, e a data e o título exatos da entrada como trainee.
- [ ] **Júnior — `[!example] Caso real`, reconstruído.** CEPEDI a partir de nov/2003, como Java Júnior — um júnior cuja única experiência anterior era bolsa de iniciação científica. É a peça mais rara do conjunto, porque essa situação é comum e não tem material publicado.
- [ ] **Pleno — `[!example] Caso real`, reconstruído.** O arco SWB → everis → TQI → Sankhya, a partir das experiências públicas do site.
- [ ] **Sênior — `[!example] Caso real`, atual.** O documento que existe hoje, público.
- [ ] **Staff — projeção declarada.** O degrau seguinte, não registro. Explicar que escrever o currículo do nível que se quer é técnica real, e que o capstone a está executando na frente do leitor.
- [ ] **Declarar reconstrução** em cada peça reconstruída: júnior e pleno não são documentos que existiram — são reconstruções feitas hoje a partir de registro público datado.
- [ ] Fechar com a leitura transversal: o que muda de peça em peça, e o que **não** muda. E o contrapeso honesto — nenhuma dessas seis portas se abriu por causa do documento sozinho.
- [ ] Gate G1-G5, com a régua de tamanho ajustada e o ajuste registrado no roadmap.

### Tarefa 29: Podar a nota 05 de Entrevistas para ponte

**Arquivos:**
- Modificar: `03-Dominios/Carreira/Entrevistas/05 - Currículo e LinkedIn como artefatos de triagem.md`
- Modificar: `03-Dominios/Carreira/Entrevistas/index.md`
- Modificar: `03-Dominios/Carreira/Entrevistas/roadmap.md`

- [ ] Ler `09 - System design em entrevista — a ponte.md` inteira antes de editar. É o molde de nota-ponte do vault, e a poda tem que produzir algo com a mesma forma e o mesmo tamanho (~90 linhas).
- [ ] Manter: o enquadramento de triagem dentro do funil, a TL;DR reescrita para apontar para fora, e o "Veja também".
- [ ] Remover, porque migrou para o galho novo: a fórmula da linha de bullet e o diagrama Mermaid (→ nota 11), os três `[!warning]` (→ notas 09, 11 e 23), as especificidades do processo internacional (→ nota 24), o `[!question]` sobre adaptar por vaga (→ nota 18), o bloco "Como soa em inglês" e a tabela PT/EN (→ notas 11 e 24).
- [ ] Substituir cada bloco removido por um callout curto remetendo à nota nova, com wikilink resolvível.
- [ ] Conferir que **nenhum wikilink de entrada quebrou** — a numeração de Entrevistas permanece intacta e os inbound continuam resolvendo.
- [ ] Atualizar a linha da nota 05 no índice e no roadmap de Entrevistas, registrando que virou ponte.
- [ ] Commit.

### Tarefa 30: Costura, verificação e registro

- [ ] Rodar `/verificar-wikilinks 03-Dominios/Carreira/Currículo` e levar a **zero** links quebrados. Comparar com a linha de base registrada na Tarefa 1.
- [ ] Rodar `/verificar-wikilinks 03-Dominios/Carreira/Entrevistas` para garantir que a poda da Tarefa 29 não quebrou nada.
- [ ] Conferir o inverso, que o verificador não pega: `grep -rn "apocrypha\|Apocrypha" 03-Dominios/Carreira/Currículo/` tem que voltar vazio.
- [ ] Conferir que toda nota tem `fase:` no frontmatter e aparece no bloco certo do `index.md`.
- [ ] Auditar a etiquetagem: cada `[!example]` do galho é `Caso real` ou `Caso fictício`, sem exceção, e todo `Caso real` tem link verificável.
- [ ] Fechar o `roadmap.md`: 26/26 escritas, com as pendências conscientes registradas (mídia, dúvidas plantadas, o que ficou fora).
- [ ] Registrar o galho em `00-Meta/Roadmap.md`, na camada Carreira, com a contagem de notas e a lente declarada.
- [ ] Commit final.

---

## Pendências deliberadas, para depois

Não são parte deste plano, e ficam registradas para não se perderem:

- **Enriquecimento de mídia** (`/adicionar-midia`) nas 26 notas — passe próprio, depois da escrita.
- **Dúvidas de leitura** (`/plantar-duvidas` seguido de `/colher-duvidas`) — passe próprio.
- **Revisão do post do blog** `como-escrever-o-seu-curriculo.md`, que repete parte do folclore de ATS derrubado na nota 04. O usuário fará em sessão separada, depois de o galho estar pronto.
- **Popular `cglima.github.io`**, hoje com as 13 experiências do autor em vez das da titular. Vem depois de o site do autor estar completo, por decisão do usuário.
