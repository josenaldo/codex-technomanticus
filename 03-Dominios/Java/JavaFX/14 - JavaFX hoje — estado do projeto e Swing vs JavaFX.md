---
title: "JavaFX hoje — estado do projeto e Swing vs JavaFX"
created: 2026-06-06
updated: 2026-06-06
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - javafx
  - magus
  - sintese
  - openjfx
aliases:
  - "JavaFX hoje"
  - "Swing vs JavaFX"
  - "Estado do JavaFX"
---

# JavaFX hoje — estado do projeto e Swing vs JavaFX

> [!abstract] TL;DR
> **JavaFX está vivo, mas fora do JDK.** Desde o Java 11 ele vive no projeto **OpenJFX** (no OpenJDK), com repositório ativo em `github.com/openjdk/jfx`, **releases semestrais alinhadas à cadência do JDK** (a versão atual confirmada em openjfx.io é a **JavaFX 26**) e *stewardship* da **Gluon** mais a comunidade — a Gluon empacota builds (SDK, jmods, Maven Central), mantém o **Scene Builder** e vende **LTS comercial** (hoje 17, 21 e 25). Estar fora do JDK **não é morte**: é cadência própria. Do outro lado, **Swing não foi substituído** — continua *core Java SE* suportado enquanto o JDK for ([[03-Dominios/Java/Swing/12 - Swing hoje - estado atual|Swing hoje]]); "modo de manutenção" é jargão de comunidade, não termo oficial. Por isso **Swing vs JavaFX é decisão de contexto**, não de torcida: legado/ecossistema maduro/zero-dependência puxam pra Swing; reatividade/CSS/binding declarativo puxam pra JavaFX; e às vezes a resposta certa **não é nenhum dos dois — é web**. Responder com a tabela mental de 2014 ("JavaFX substituiu o Swing") ou de 2010 ("JavaFX morreu") **reprova igual**: as duas são fotografias velhas de um estado que mudou.

## O que é

Esta nota é a **capstone do Galho 6 (JavaFX)** e fecha, junto com a [[03-Dominios/Java/Swing/12 - Swing hoje - estado atual|capstone do Galho 5 (Swing)]], o **par desktop** da trilha Java. As notas 01–13 ensinam *como* operar JavaFX — scene graph, FXML, properties, threading, empacotamento. Esta ensina duas coisas que não são técnicas, são de **arquitetura**:

1. **O estado real do projeto JavaFX hoje** — quem o mantém, em que ritmo lança, onde mora o repositório, qual o papel da Gluon. Fatos verificáveis, com hedge onde a confirmação não foi possível.
2. **O framework de decisão Swing vs JavaFX (vs web)** — não "qual é melhor", mas "qual é o certo *para este projeto, este time, este momento*".

O salto de senioridade que uma entrevista internacional quer ver é exatamente esse: sair de "sei usar a ferramenta" para "sei decidir se a ferramenta é a certa — e defender a decisão por critérios, não por gosto". A resposta madura nunca é um veredito de torcida ("JavaFX é o futuro", "Swing é coisa de velho"); é um **frame de decisão**.

A calibração que esta nota persegue, espelhando a do Swing: nem "morto" (a foto de 2010) nem "o futuro que aposentou o Swing" (a foto de 2014), e sim **vivo, externo ao JDK, em cadência própria**. Manter os dois toolkits nessa faixa de "vivos, com nichos diferentes" — sem enterrar nem coroar nenhum — é a postura que uma entrevista sênior recompensa.

> [!note] Por que esta nota fecha o par desktop
> O Java oferece **duas** UIs desktop de primeira classe — Swing e JavaFX — e a pergunta que aparece em revisão de arquitetura e em entrevista não é "como funciona o scene graph?", é *"desktop Java em 2026, sério? Por quê este e não aquele — ou por que desktop em vez de web?"*. Responder bem exige conhecer o **estado dos dois lados** e ter um **critério explícito**. Esta nota e a [[03-Dominios/Java/Swing/12 - Swing hoje - estado atual|capstone do Swing]] são deliberadamente complementares e **não se contradizem**: Swing é *core Java SE* suportado; JavaFX é externo, vivo e em cadência própria. Nenhum dos dois está "morto" e nenhum dos dois "venceu".

## Por que importa

"Desktop Java em 2026?" é uma **pergunta real**, e o entrevistador a faz justamente porque ela separa o candidato que repete slogans do que pensa com contexto.

O candidato fraco responde com uma das duas **fotografias velhas**:

- A **foto de 2010**: *"JavaFX morreu, ninguém usa."* Era uma leitura plausível quando o JavaFX Script foi descontinuado e o futuro do toolkit parecia incerto — mas é falsa hoje, com OpenJFX lançando a cada seis meses e repositório ativo.
- A **foto de 2014**: *"JavaFX substituiu o Swing, Swing é legado morto."* Era o discurso da era em que o JavaFX vinha *bundled* no JDK 8 e a Oracle o posicionava como sucessor — mas Swing **nunca foi removido**, continua *core Java SE*, e o JavaFX **saiu** do JDK em 2011/Java 11.

Ambas reprovam, e reprovam **igual**, porque ambas trocam o estado atual por um instantâneo congelado. O que diferencia o sênior não é saber qual toolkit é "melhor" — é **decidir por contexto**: o app precisa ser desktop? É legado ou greenfield? Que time você tem? Que ecossistema de terceiros o projeto depende? A resposta cai naturalmente de critérios, não de preferência. E uma honestidade que vale ouro em entrevista: às vezes a melhor resposta para "qual UI desktop Java?" é **"nenhuma — o requisito é web"**.

Há ainda um motivo prático de a pergunta importar: decisões de UI desktop são **caras de reverter**. Escolher errado entre Swing, JavaFX e web não é um detalhe de implementação que se troca num *refactor* de tarde — é arquitetura que arrasta anos de código, contratação e manutenção. Por isso o entrevistador valoriza tanto o **frame de decisão**: ele revela se o candidato pensa no custo de longo prazo da escolha ou só na empolgação com a tecnologia da moda.

## Como funciona

### Governança e releases (Oracle → OpenJFX; github.com/openjdk/jfx; cadence; papel da Gluon)

**O fato central da governança.** JavaFX nasceu na **Oracle** (JavaFX 2.0, 2011, substituindo o antigo JavaFX Script — ver [[01 - JavaFX — o que é e como chega ao projeto]]) e foi *bundled* no JDK 8 da Oracle. No **Java 11 (2018)** foi **desacoplado do JDK** e passou a viver como o projeto **OpenJFX**, dentro do **OpenJDK**, sob a mesma licença do OpenJDK (**GPL com Classpath Exception** — confirmado em openjfx.io). A consequência arquitetural: JavaFX deixou de ser "parte da instalação Java" e virou **dependência externa** com **ciclo de vida próprio**.

A transição de governança em três marcos:

| Quando | Quem governa | Como chega | Significado |
|--------|--------------|------------|-------------|
| 2011 | Oracle | API standalone (substitui JavaFX Script) | JavaFX nasce como produto Oracle |
| JDK 8 (2014) | Oracle | *bundled* no JDK da Oracle | `import javafx.*` sem dependência externa |
| Java 11 (2018) → hoje | **OpenJFX (OpenJDK) + Gluon + comunidade** | dependência externa (Maven/SDK/jmods) | cadência própria, fora do JDK |

A leitura sênior dessa tabela: a mudança de 2018 **não foi um downgrade** — foi a passagem de "controlado por um vendor, preso ao ciclo do JDK" para "projeto open-source com vendor comercial de suporte e cadência própria". É o mesmo movimento que o OpenJDK fez, e ninguém diz que o Java morreu por isso.

**O repositório.** O desenvolvimento do OpenJFX acontece em **`github.com/openjdk/jfx`** — o fato de estar sob a organização `openjdk` no GitHub é coerente com ser um projeto formal do OpenJDK.

> [!warning] Hedge — confirmação do repositório
> Confirmei via openjfx.io que o projeto é **OpenJFX, livre, GPL+Classpath Exception, parte do ecossistema OpenJDK** e distribuído via SDK, jmods e Maven Central. **Não consegui validar diretamente** a página `github.com/openjdk/jfx` nesta sessão (sem acesso autenticado/render do repositório). O caminho `openjdk/jfx` é o canônico e bate com a organização `openjdk` no GitHub; trato a existência e a atividade do repositório como **altamente provável, mas não verificada nesta sessão**. Em entrevista, é honesto dizer "the OpenJFX sources live in the OpenJDK org on GitHub" — e, se cobrado em número de commits ou atividade recente, dizer que confirmaria na fonte em vez de inventar.

**A cadência.** O OpenJFX lança **alinhado ao JDK — uma release a cada seis meses**, e a numeração **espelha o JDK** correspondente (JavaFX 21 ↔ JDK 21, JavaFX 24 ↔ JDK 24, etc. — cravado na [[01 - JavaFX — o que é e como chega ao projeto]]). A versão atual confirmada em openjfx.io é a **JavaFX 26**.

> [!info] Hedge — cadência semestral explícita
> A página inicial de openjfx.io **não reafirma em texto** a frase "uma release a cada seis meses" de forma literal; confirma a numeração 26 e a natureza desacoplada/externa do projeto. A cadência semestral alinhada ao JDK está cravada na nota 01 deste galho e é coerente com o modelo de release do OpenJDK. Trato como **fato estabelecido pela trilha**, com a numeração 26 verificada nesta sessão.

**O papel da Gluon.** A **Gluon** é a empresa que faz a *stewardship* prática do OpenJFX e fecha a cadeia entre "projeto open-source" e "coisa que você consegue usar e suportar em produção":

- **Builds / distribuições.** A Gluon empacota e publica o runtime JavaFX — **SDK por plataforma, jmods e artifacts no Maven Central** (Linux x64, Windows x64, macOS x64 e macOS aarch64 entre as plataformas padrão). É de onde, na prática, sai o JavaFX que você baixa em `gluonhq.com`.
- **LTS comercial.** A Gluon vende um serviço de **Long-Term Support** para JavaFX. Confirmado nesta sessão: hoje as versões com designação **LTS são 17, 21 e 25**. Isso preenche a lacuna do projeto open-source, que (como o OpenJDK upstream) não dá garantias de suporte longo de graça.
- **Scene Builder.** A Gluon **mantém o Scene Builder**, o editor visual de FXML — ver [[06 - FXML e Scene Builder]]. É a peça de tooling que torna o desenvolvimento declarativo de UI viável sem escrever XML na mão.
- **Ecossistema mais amplo.** Gluon **Mobile** (JavaFX em iOS/Android), **GluonFX / GraalVM native image** (compilar JavaFX para binário nativo), Gluon Embedded e consultoria. O detalhe mobile/native é mencionado adiante, sem aprofundar.

> [!info] O modelo mental certo de governança
> JavaFX hoje é **OpenJFX (código, no OpenJDK) + Gluon (builds, tooling, LTS comercial) + comunidade (patches, validação)**. Esse arranjo é *normal* para um projeto open-source maduro de infraestrutura — não é sinal de fragilidade. Estar fora do JDK significa **cadência própria**, não abandono; ter um vendor comercial por trás (Gluon) é o que viabiliza adoção corporativa com suporte. É exatamente o oposto de "morto".

### Sinais de vitalidade honestos (releases, repositório, vendors — sem números de adoção)

Como saber se um projeto está "vivo" **sem inventar estatística**? Olhando para **sinais verificáveis**, não para market share:

- **Release atual confirmado.** Há uma **JavaFX 26** atual (confirmada em openjfx.io, com Javadoc 26 publicado — cravado na nota 01). Projeto morto não publica release nova e numerada acompanhando o JDK.
- **Cadência mantida.** Releases **semestrais alinhadas ao JDK**, numeração espelhando o JDK. Um cronograma vivo e previsível é, por si só, um sinal de saúde.
- **Repositório no OpenJDK.** O código vive sob a organização **`openjdk` no GitHub** (`openjdk/jfx`) — projeto formal, não fork abandonado num canto.
- **Vendor empacotando ativamente.** A **Gluon** publica builds por plataforma, mantém o Scene Builder e vende **LTS (17, 21, 25)**. Ninguém vende suporte longo para tecnologia que não tem demanda.

E, por honestidade intelectual, o teste inverso: **o que falsificaria "JavaFX está vivo"?** Se as releases parassem (sem versão nova acompanhando o JDK por vários ciclos), se o repositório no OpenJDK ficasse sem commits por muito tempo, ou se a Gluon encerrasse builds e LTS. Hoje **nenhum** desses sinais negativos está presente — e é justamente por enumerar o que *derrubaria* a tese que a afirmação "está vivo" deixa de ser torcida e vira leitura defensável.

> [!warning] Por que NÃO citamos market share / "% de desenvolvedores"
> Você vai ver blogs afirmando "X% dos devs Java usam JavaFX" ou "JavaFX tem Y% de adoção". **Não existe fonte oficial e confiável com esse número** — ninguém mede de forma censitária quem usa qual toolkit desktop. Repetir esses números é **propagar fabricação**, e é exatamente o tipo de afirmação que um entrevistador técnico derruba pedindo a fonte. A postura honesta é falar de **sinais verificáveis** (releases datadas, repositório, vendors empacotando, LTS à venda) e dizer com todas as letras: *"I don't have reliable adoption numbers — nobody does — but the project ships releases on a JDK-aligned cadence, the sources live in the OpenJDK org, and Gluon sells commercial LTS, which are concrete signs it's alive."* Isso vale mais do que qualquer porcentagem inventada. (A capstone do Swing aplica a mesma regra: nada de "X de cada Y empresas usam Swing".)

### Swing vs JavaFX — a decision matrix

Comparação **justa**: cada linha diz **quem vence** e, principalmente, **por quê** — porque o vencedor muda conforme o critério, e é a leitura linha a linha que demonstra senioridade.

| Critério | Vence | Por quê |
|----------|-------|---------|
| Ecossistema / 3rd-party maduro | **Swing** | Décadas de bibliotecas, exemplos, Stack Overflow e ferramentas; UIs gigantes em produção (IntelliJ IDEA, NetBeans em Swing). JavaFX tem ecossistema bom, porém menor e mais novo. |
| Look nativo do SO | **Empate / depende** | Nenhum dos dois renderiza widgets nativos de verdade (isso é o SWT). Swing tem L&F que *imita* o SO; JavaFX **não persegue** o look nativo — aposta em theming próprio via CSS. Se "parecer exatamente o SO" é requisito duro, nenhum é ideal. |
| Theming / CSS | **JavaFX** | CSS de primeira classe, declarativo, com seletores e *pseudo-classes* ([[09 - CSS em JavaFX]]). Em Swing você depende de L&F de terceiros (FlatLaf) para algo moderno. |
| Binding / reatividade | **JavaFX** | `Property` observável + `bind`/`bindBidirectional` ([[07 - Properties e binding]]) é o diferencial estrutural do JavaFX; é a base do MVVM ([[11 - Arquitetura — MVC, MVVM e injeção de dependência]]). Swing não tem binding nativo — você sincroniza model/view na mão. |
| Threading (EDT vs FX thread) | **Empate técnico** | Mesma regra dos dois lados: **uma única thread de UI**, todo update de componente nela, trabalho lento vai pro background e reentra via marshaling. Swing: EDT + `invokeLater`. JavaFX: FX Application Thread + `Platform.runLater`/`Task`/`Service` ([[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]]). Quem entende um, entende o outro. |
| Empacotamento | **Depende** | **Swing vem no JDK** — zero dependência de UI. JavaFX é **externo (JPMS, fora do JDK)** e exige `--module-path`/plugin em dev e `jlink`/`jpackage` pra distribuir ([[13 - Empacotamento — módulos, jlink e jpackage]]). Vantagem Swing na simplicidade de baseline; mas `jpackage` nivela a distribuição final (instalador nativo dos dois jeitos). |
| Legado / contratação | **Swing** | Há muito mais código Swing instalado e mais gente que já manteve Swing. Para *manter legado* e *contratar rápido*, Swing tem massa crítica maior. |
| Tooling / Scene Builder | **JavaFX** | O **Scene Builder** (mantido pela Gluon) dá edição visual de FXML ([[06 - FXML e Scene Builder]]); Swing não tem um editor visual oficial vivo equivalente. |

Resumindo o placar da matrix: **Swing** leva ecossistema/3rd-party, legado/contratação e baseline de empacotamento; **JavaFX** leva theming/CSS, binding/reatividade e tooling/Scene Builder; **empate** em look nativo (nenhum é nativo de verdade) e em threading (mesma regra de single-thread de UI). Nenhum lado "ganha de goleada" — cada um domina um terço da tabela.

> [!info] Como ler a matrix
> Repare que **nenhuma coluna vence todas as linhas** — e é esse o ponto. Swing ganha em ecossistema, legado e baseline de empacotamento; JavaFX ganha em CSS, binding e tooling visual; threading é empate conceitual. Um candidato que diz "JavaFX é melhor" sem qualificar **não leu a matrix**. A resposta certa é sempre *"melhor para quê?"*. E a matrix inteira pressupõe que **desktop já é a resposta** — se não for, ela nem se aplica (próxima seção).

> [!warning] A linha de threading que confunde
> A linha "threading" da matrix é **empate técnico**, e isso costuma surpreender quem espera que JavaFX tenha "resolvido" o problema da thread única do Swing. Não resolveu — nem precisava. JavaFX tem a **FX Application Thread**, single-thread, com a **mesma regra** da EDT do Swing: todo update de UI nela, trabalho lento no background, reentrada via `Platform.runLater`/`Task`/`Service` ([[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]]). Quem entende a EDT do Swing já entende a FX thread — e vice-versa. O modelo de threading **não é** um critério de desempate entre os dois.

### Quando nenhum dos dois — a opção web (e os concorrentes reais)

A pergunta antes da matrix é mais fundamental: **precisa mesmo ser desktop Java?** Em muitos casos de 2026, a resposta honesta é não.

- **Requisito é navegador → web.** Se o app precisa rodar no browser, sem instalação, distribuído por URL, atualizado no servidor — **nem Swing nem JavaFX competem**. São desktop por construção. A resposta é uma stack web.
- **Precisa de web *e* desktop → avalie web-first.** Quando o roadmap tem as duas formas, começar por web costuma cobrir o desktop "de graça" (via empacotadores), enquanto começar por desktop Java deixa o web descoberto. Avaliar **web-first** antes de comprometer com desktop nativo é a leitura madura.
- **Electron / Tauri são concorrentes reais do desktop Java.** Para apps desktop multiplataforma com UI rica, **Electron** (web stack + Chromium embarcado) e **Tauri** (web frontend + runtime nativo enxuto) competem de frente com Swing/JavaFX — e times que já vivem em web entregam mais rápido neles. Ignorar essa concorrência ao defender "desktop Java" é ingênuo.
- **Mobile → Gluon Mobile existe, mas é outra conversa.** JavaFX *roda* em iOS/Android via **Gluon Mobile** (e GraalVM native image). É uma menção honesta de que o caminho existe — **não** é o foco desta nota nem, na maioria dos casos, a escolha óbvia frente a nativo/cross-platform mobile dedicado.

Os concorrentes do desktop Java, lado a lado:

| Opção | Stack | Quando faz sentido |
|-------|-------|--------------------|
| Swing | Java desktop, no JDK | Legado, ferramentas internas, zero-dependência |
| JavaFX | Java desktop, OpenJFX externo | Greenfield com UI reativa/CSS/binding, time desktop |
| Web (puro) | HTML/CSS/JS no navegador | Requisito é browser, distribuição por URL |
| Electron | Web + Chromium embarcado | Desktop multiplataforma, time já web, UI rica |
| Tauri | Web + runtime nativo enxuto | Desktop multiplataforma com footprint menor que Electron |

A linha que muitos esquecem: as três últimas **não são desktop Java** — e ainda assim competem de frente quando o requisito real é "app multiplataforma com UI rica" e o time vive em web.

> [!tip] A pergunta que vem antes da matrix
> Antes de comparar Swing e JavaFX, pergunte: *"isto precisa ser desktop?"*. Se a resposta for "não" ou "não necessariamente", a matrix Swing-vs-JavaFX é a discussão errada — a discussão certa é desktop-vs-web. Pular essa pergunta é o erro de quem já decidiu a tecnologia antes de entender o requisito.

> [!info] E o SWT? (a terceira via desktop-Java)
> A capstone do Swing lembra que há um terceiro toolkit desktop-Java: o **SWT** (*Standard Widget Toolkit*), que move o **Eclipse**. Ao contrário de Swing (lightweight, pintado em Java) e JavaFX (scene graph próprio, theming por CSS), o SWT usa **widgets nativos do SO via JNI** — é a opção que de fato entrega *look nativo de verdade*. Esta nota foca o **par Swing × JavaFX** porque é o que a trilha cobre, mas em entrevista vale saber que SWT existe e ocupa um nicho distinto (look nativo a qualquer custo). Não é parte da especificação Java SE nem do OpenJDK — é projeto da Eclipse Foundation.

### O que o senior responde — o frame de três perguntas

A resposta sênior não é um veredito, é um **frame** que resolve qualquer caso concreto por contexto:

1. **Precisa ser desktop?** Se o requisito é navegador, é **web** — encerra. Se "talvez web no futuro", avalie **web-first**. Só se desktop for genuinamente necessário a conversa continua.
2. **Legado ou greenfield?** **Legado em Swing** → continue em Swing; migrar sem requisito de produto é custo sem payoff. **Greenfield** → a inércia não decide; compare pelos critérios da matrix.
3. **Que time você tem?** Um time fluente em desktop Java e em MVVM tira proveito do binding/CSS do JavaFX. Um time só-web talvez entregue melhor em Electron/Tauri. **Fluência do time é critério de primeira classe**, não detalhe.

O mesmo frame como árvore de decisão:

```text
Precisa ser desktop? ──não──► web (Electron/Tauri se quiser companheiro desktop)
   │
   sim
   ▼
Já existe base Swing (legado)? ──sim──► continue em Swing
   │                                    (migrar sem requisito = custo sem payoff)
   não (greenfield)
   ▼
Precisa de UI reativa / CSS / binding declarativo? ──sim──► JavaFX
   │                                                         (se o time tiver fluência desktop)
   não
   ▼
Ecossistema 3rd-party / contratação / baseline simples pesam? ──sim──► Swing é defensável
   │
   ▼
Decida pelo time: fluência desktop-Java → JavaFX/Swing; só-web → reavalie web/Electron/Tauri.
```

O denominador comum: a decisão **cai dos critérios**, nunca da preferência. É assim que se defende numa revisão de arquitetura — e numa entrevista.

> [!note] O que o frame protege contra
> Cada pergunta do frame neutraliza uma armadilha clássica. "Precisa ser desktop?" mata o reflexo de resolver tudo com a tecnologia que se domina. "Legado ou greenfield?" separa *manter* (onde inércia é argumento legítimo) de *iniciar* (onde não é). "Que time você tem?" impede a escolha puramente técnica que ignora quem vai escrever e manter o código. O frame não diz a resposta — ele garante que a resposta venha das **perguntas certas, na ordem certa**. É essa disciplina, e não o conhecimento de qual toolkit tem mais features, que sinaliza senioridade de arquitetura.

## Na prática

Três **cenários hipotéticos** (genéricos, neutros — nenhuma referência a pessoa, cliente ou caso real) mostrando o frame funcionando. O ponto não é o veredito, é o **raciocínio** que leva até ele.

### (a) ERP em Swing de 15 anos, estável → fica em Swing

Um ERP corporativo construído em Swing há ~15 anos, em produção, estável, com bugs ocasionais mas sem dor de UI. Aplicando o frame: **desktop? sim** (é um app instalado). **Legado ou greenfield? legado.** Não há **requisito de produto** que exija a UI reativa/CSS do JavaFX — o sistema funciona. Veredito: **continua em Swing**. Reescrever as telas em JavaFX seria **custo e risco sem payoff nomeável** — exatamente coerente com a [[03-Dominios/Java/Swing/12 - Swing hoje - estado atual|capstone do Galho 5]]: migração sem requisito não se paga. Investimento melhor: modernizar incrementalmente (FlatLaf, fluência na EDT) onde dói.

### (b) Ferramenta interna NOVA de dados com dashboards → JavaFX

Uma ferramenta interna **greenfield** para análise operacional: tabelas grandes, dashboards que reagem a filtros em tempo real, gráficos, tema corporativo. Frame: **desktop? sim** (precisa de acesso local, roda na intranet, sem requisito de navegador). **Legado ou greenfield? greenfield.** Aqui o **binding** ([[07 - Properties e binding]]), o padrão **MVVM** ([[11 - Arquitetura — MVC, MVVM e injeção de dependência]]) e o **CSS** ([[09 - CSS em JavaFX]]) do JavaFX são vantagem estrutural: o dashboard reativo sai natural, a UI testável, o tema declarativo. Veredito: **JavaFX**, *se* o time tiver (ou puder construir) fluência desktop. Se o requisito de navegador surgir, a conversa volta pra web.

### (c) Produto SaaS multiplataforma → web (desktop nem entra)

Um produto SaaS vendido para muitos clientes, acessível de qualquer máquina, atualizado continuamente no servidor. Frame: **desktop? não** — o requisito é navegador, distribuição por URL, zero instalação. A matrix Swing-vs-JavaFX **nem se aplica**: a resposta é **web**. Insistir em desktop Java aqui seria resolver o problema errado. Se mais tarde surgir necessidade de um app desktop companheiro, **Electron/Tauri** (reaproveitando o frontend web) entram na frente do desktop Java.

Os três cenários lado a lado, para fixar que o veredito é função do contexto:

| Cenário | Desktop? | Legado/Green | UI reativa? | Veredito |
|---------|----------|--------------|-------------|----------|
| (a) ERP Swing de 15 anos | sim | legado | não exigida | **fica Swing** |
| (b) ferramenta interna nova de dados | sim | greenfield | sim (dashboards) | **JavaFX** |
| (c) SaaS multiplataforma | não | greenfield | sim, mas no browser | **web** |

> [!info] O fio que liga os três
> Em nenhum dos três a decisão veio de "gosto de X". Veio do frame: **desktop? → legado/greenfield? → que time?**. Os vereditos divergem (Swing, JavaFX, web) justamente porque os **contextos** divergem. Isso é decidir por contexto — o oposto de torcer por uma tecnologia. Troque um fator de qualquer cenário (o ERP ganha um requisito de dashboard reativo; o SaaS vira uma ferramenta offline de intranet) e o veredito muda — porque a decisão sempre seguiu os critérios, não a tecnologia.

## Armadilhas

Armadilhas **de raciocínio** — erros de leitura do estado atual e da decisão, não bugs de código.

### (1) "JavaFX morreu quando saiu do JDK"

**Descrição.** Concluir que, por não vir mais *bundled* no JDK desde o Java 11, o JavaFX foi abandonado. É confundir **desacoplamento de empacotamento** com **fim de projeto**. Desacoplar significou ganhar **cadência própria** (OpenJFX, releases alinhadas ao JDK), não morrer.

**Raciocínio correto.** **Cheque os sinais antes de afirmar.** Há **JavaFX 26** atual, cadência semestral, repositório no OpenJDK (`openjdk/jfx`) e **vendor (Gluon) vendendo LTS** (17, 21, 25) e empacotando builds. Esses são sinais verificáveis de vida. Em entrevista: *"decoupling from the JDK at Java 11 wasn't death — it gave JavaFX its own JDK-aligned release cadence; there's a current release, an OpenJDK repo, and Gluon selling commercial LTS."*

---

### (2) "Swing está deprecado, tenho que migrar"

**Descrição.** Achar que Swing foi deprecado/marcado para remoção e que isso *obriga* a migrar para JavaFX. **Falso.** Swing é **core Java SE**, suportado enquanto o JDK for suportado, sem *deprecation* e sem data de remoção — cravado na [[03-Dominios/Java/Swing/12 - Swing hoje - estado atual|capstone do Galho 5]]. "Modo de manutenção" é **jargão da comunidade** sobre o ritmo de evolução, **não** termo oficial da Oracle.

**Raciocínio correto.** Migrar precisa de **motivo concreto** (um requisito de produto que Swing não atende bem), não de medo de "ficar sem suporte" — esse risco não existe num horizonte previsível. Sem requisito, **fica Swing**. Migração por medo é custo sem payoff.

---

### (3) Reescrever app Swing estável em JavaFX "pra modernizar"

**Descrição.** Propor reescrever uma aplicação Swing **estável** em JavaFX só "para modernizar a stack", sem nenhum requisito de produto puxando a mudança. É a armadilha (2) virada do avesso: não é medo de deprecação, é **estética de stack**.

**Raciocínio correto.** Toda reescrita carrega **custo e risco** (bugs novos, regressões, tempo de time). Esse custo precisa de um **payoff nomeável** — uma UI reativa que o produto exige, um CSS theming que o negócio pede, uma integração que só o JavaFX entrega bem. "Parecer moderno" não é payoff; é gosto. Sem payoff nomeável, a reescrita é prejuízo. (Coerente com o cenário (a) acima e com a capstone do Galho 5.)

---

### (4) Citar estatística de adoção de blog

**Descrição.** Sustentar "JavaFX está vivo/morto" com números do tipo *"X% dos devs usam JavaFX"* tirados de um blog ou pesquisa informal. **Ninguém tem esse dado** de forma confiável — não há censo de adoção de toolkit desktop. Repetir o número é propagar fabricação.

**Raciocínio correto.** Argumente com **sinais verificáveis**: releases datadas e numeradas (JavaFX 26), cadência alinhada ao JDK, repositório no OpenJDK, vendor (Gluon) empacotando e vendendo LTS. E seja explícito sobre a ausência do dado: *"I don't quote adoption percentages because there's no reliable source — I look at releases, the repo, and vendors instead."* Honestidade sobre o que **não** se sabe é sinal de maturidade.

## Em entrevista

### Frase pronta (inglês)

> "I treat JavaFX-versus-Swing as a context decision, not a winner. JavaFX is alive but lives outside the JDK: it was decoupled at Java 11 into the OpenJFX project under the OpenJDK, it ships on a JDK-aligned six-month cadence — the current release is JavaFX 26 — and it's stewarded by Gluon plus the community. Gluon packages the builds, maintains Scene Builder, and sells commercial LTS, currently for 17, 21, and 25. Decoupling from the JDK wasn't death — it gave JavaFX its own cadence. On the other side, Swing wasn't replaced: it's still core Java SE, supported as long as the JDK is, and 'maintenance mode' is the community's label, not Oracle's wording. So I decide by context: I'd keep a stable legacy app on Swing because migrating without a product requirement is cost with no payoff; I'd reach for JavaFX on a greenfield data tool that needs reactive dashboards, because binding, MVVM and CSS are first-class there; and if the requirement is the browser, honestly neither fits — I'd go web, where Electron or Tauri compete directly with Java desktop. One thing I'm careful about: I won't quote adoption percentages, because nobody has a reliable number — I point to releases, the OpenJDK repo, and Gluon's LTS as the real signs of life."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| desacoplado do JDK | decoupled / unbundled from the JDK |
| cadência de release alinhada ao JDK | JDK-aligned release cadence |
| stewardship / curadoria do projeto | project stewardship |
| suporte de longo prazo comercial | commercial long-term support (LTS) |
| sinais de vitalidade | signs of life / vitality signals |
| dados de adoção / market share | adoption numbers / market share |
| decisão de contexto / de arquitetura | context / architecture decision |
| projeto novo / do zero | greenfield project |
| custo sem retorno nomeável | cost with no nameable payoff |
| editor visual de FXML | visual FXML editor (Scene Builder) |
| binding / reatividade | data binding / reactivity |
| modo de manutenção (jargão) | maintenance mode (community jargon) |

### O erro que derruba o candidato

Vale memorizar o **anti-padrão** que mais reprova, porque é simétrico ao do Swing. O candidato fraco entrega uma das duas fotografias velhas: *"JavaFX morreu, saiu do JDK"* (foto de 2010 — falso, há release atual e LTS comercial) ou *"JavaFX substituiu o Swing, Swing é legado morto"* (foto de 2014 — falso, Swing nunca foi removido). As duas reprovam **igual**, porque trocam o estado atual por um instantâneo congelado. A resposta sênior **recusa os dois extremos** e entrega a leitura calibrada: JavaFX vivo mas externo ao JDK (OpenJFX, releases JDK-aligned, Gluon com builds/Scene Builder/LTS), Swing vivo como core Java SE, e a escolha entre eles **decidida por contexto** — com a honestidade extra de que, às vezes, a resposta certa é **web**. Demonstrar essa calibração, e citar **sinais verificáveis** em vez de estatística inventada, é o que sinaliza maturidade de arquitetura.

## Cheatsheet do galho

Mapa "qual nota do galho JavaFX resolve qual problema" — para revisar o galho inteiro antes de uma entrevista:

| Preciso de… | Nota |
|-------------|------|
| Setup / lifecycle / de onde vem o JavaFX | [[01 - JavaFX — o que é e como chega ao projeto]] |
| Entender a árvore visual / coordenadas | [[02 - Scene graph — stage, scene e nodes]] |
| Posicionar componentes na tela | [[03 - Layout panes]] |
| Widgets prontos (botões, campos, listas) | [[04 - Controls essenciais]] |
| Tratar eventos (capturing, bubbling, handlers) | [[05 - Eventos — capturing, bubbling e handlers]] |
| View declarativa em XML | [[06 - FXML e Scene Builder]] |
| Reatividade / sincronizar estado e UI | [[07 - Properties e binding]] |
| Grid de dados com colunas e formatação | [[08 - TableView, cell factories e dados observáveis]] |
| Tema / estilização visual | [[09 - CSS em JavaFX]] |
| Não travar a UI com trabalho lento | [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]] |
| Arquitetura testável (MVC / MVVM / DI) | [[11 - Arquitetura — MVC, MVVM e injeção de dependência]] |
| UI custom / Canvas / charts | [[12 - Custom controls, Canvas e charts]] |
| Distribuir ao usuário final | [[13 - Empacotamento — módulos, jlink e jpackage]] |
| "JavaFX ou Swing ou web? Estado do projeto" | esta nota (14 — capstone) |

> [!tip] A resposta de 30 segundos
> *"JavaFX is alive but outside the JDK — OpenJFX, JDK-aligned releases, current is 26, Gluon does builds, Scene Builder and commercial LTS. Swing wasn't replaced; it's still core Java SE. So it's a context call: legacy and broad ecosystem lean Swing; reactive UI, CSS and binding lean JavaFX; and if the requirement is the browser, the honest answer is web. No adoption percentages — nobody has them; I look at releases, the repo, and vendors."*

## Veja também

- [[01 - JavaFX — o que é e como chega ao projeto]]
- [[07 - Properties e binding]]
- [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]]
- [[11 - Arquitetura — MVC, MVVM e injeção de dependência]]
- [[13 - Empacotamento — módulos, jlink e jpackage]]
- [[03-Dominios/Java/Swing/12 - Swing hoje - estado atual|Swing hoje (Galho 5)]]
- [[03-Dominios/Java/Swing/index|Swing (MOC do Galho 5)]]
- [[03-Dominios/Java/JavaFX/index|JavaFX (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#OpenJFX|OpenJFX (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#Gluon|Gluon (Dicionário)]]

## Referências

- [OpenJFX — openjfx.io](https://openjfx.io/) — confirmou nesta sessão: JavaFX 26 como release atual, projeto desacoplado/externo ao JDK (SDK, jmods, Maven Central), licença GPL+Classpath Exception.
- [Gluon — JavaFX (gluonhq.com/products/javafx)](https://gluonhq.com/products/javafx/) — confirmou nesta sessão: Gluon empacota builds por plataforma, mantém o Scene Builder, oferece LTS comercial (versões 17, 21 e 25), além de Gluon Mobile e GluonFX/GraalVM native image.
- OpenJFX no OpenJDK — `https://github.com/openjdk/jfx` — repositório canônico do projeto (organização `openjdk`); **não verificado diretamente nesta sessão** (ver hedge na seção de governança).
- [[01 - JavaFX — o que é e como chega ao projeto]] — linha do tempo cravada (desacoplado no Java 11, OpenJFX, cadência semestral alinhada ao JDK, JavaFX 26 atual).
- [[03-Dominios/Java/Swing/12 - Swing hoje - estado atual|Swing hoje (Galho 5)]] — base do fato "Swing é core Java SE suportado; 'modo de manutenção' é jargão de comunidade, não termo oficial".
