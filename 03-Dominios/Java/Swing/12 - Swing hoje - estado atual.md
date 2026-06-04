---
title: "Swing hoje: estado atual"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - swing
  - magus
  - estado-atual
  - arquitetura
aliases:
  - Swing hoje
  - Estado atual do Swing
---

# Swing hoje: estado atual

> [!abstract] TL;DR
> **Swing é tecnologia core e suportada do Java SE — não está deprecada nem marcada para remoção.** A Oracle, no *Java Client Roadmap Update* (março de 2018, atualizado em maio de 2020), afirma que **Swing e AWT permanecem "core Java SE technologies"**, seguem recebendo *bug fixes* e atualizações nas releases LTS e na mainline, e serão suportadas **enquanto o JDK for suportado**. O que mudou foi o ritmo de evolução: na prática a API recebe **poucas features novas**. O rótulo **"modo de manutenção" é jargão da comunidade, não termo oficial da Oracle** — convém citar a declaração oficial e a leitura de-facto como duas coisas distintas. Enquadre Swing como **decisão de arquitetura honesta**: ainda é a escolha certa para um nicho bem definido — ferramentas internas/admin, IDEs (IntelliJ IDEA, NetBeans, Eclipse), apps desktop offline e legados, embedded — e a escolha errada para um app moderno com UI rica/animada, web ou mobile. Para esses casos o Java oferece **JavaFX (planejado, Galho 6)** ou stacks web. E uma honestidade técnica: **virtual threads** (Galho 4) melhoram o trabalho de **background**, mas **não mudam a natureza single-thread da EDT** — não a "consertam" nem a substituem.

## O que é

Esta nota fecha o galho com uma leitura honesta do **estado atual** da API Swing — não um obituário, não um panfleto. A pergunta que ela responde é a que aparece em entrevista e em revisão de arquitetura: *"em 2026, ainda faz sentido escolher Swing?"*. A resposta madura não é "sim" nem "não", é **"depende do nicho — e, antes de tudo, não confunda 'pouca evolução' com 'morto'"**.

O estado real tem duas camadas que precisam ser separadas com cuidado, porque a comunidade tende a fundi-las:

1. **O status oficial** — declaração formal da Oracle sobre suporte e ciclo de vida. Aqui há fato verificável, com fonte e data.
2. **O consenso de-facto** — a leitura prática da comunidade sobre o ritmo de evolução e o posicionamento de mercado. Aqui há opinião amplamente compartilhada, mas **não números oficiais de adoção** — e esta nota não inventa nenhum.

Tratar Swing como **suportado mas estável** (em vez de "morto" ou "vivíssimo") é a postura correta. O resto da nota detalha onde isso aterrissa em decisões concretas.

> [!note] Por que esta nota fecha o galho
> As notas 01–11 ensinam *como* usar Swing — modelo, componentes, EDT, models, *look and feel*, pintura customizada. Esta, a capstone, ensina *quando* usá-lo. É a passagem de "sei operar a ferramenta" para "sei decidir se a ferramenta é a certa" — exatamente o salto de senioridade que uma entrevista internacional quer ver. A resposta não é técnica, é **de arquitetura**: pesar status, nicho e alternativas com honestidade, sem torcida.

## Como funciona

### O status oficial vs o consenso da comunidade

**O fato oficial (fonte + data).** No *Java Client Roadmap Update*, publicado pela **Oracle em março de 2018** e **atualizado em maio de 2020**, a Oracle declara que **Swing e AWT permanecem "core Java SE technologies"** — parte da especificação Java SE — e que **continuarão recebendo *bug fixes* e atualizações** nas releases LTS suportadas e na mainline, conforme a evolução dos sistemas operacionais o exija. A consequência direta dessa declaração: enquanto o JDK for suportado, **Swing e AWT são suportados junto**. Não há *deprecation*, não há JEP de remoção, não há data de fim.

> [!info] O que "suportado" significa aqui
> "Suportado como core Java SE" quer dizer: faz parte da especificação, vem no JDK sem dependência externa, recebe correções de bug e adaptações a mudanças de SO (novas versões de Windows/macOS/Linux, HiDPI, etc.). **Não** quer dizer "recebe features novas no mesmo ritmo de uma API em desenvolvimento ativo". As duas coisas são compatíveis: uma API pode ser suportada e, ao mesmo tempo, evoluir devagar.

**O consenso de-facto (leitura da comunidade).** Na prática, Swing recebe **poucas features novas** — o investimento de novas capacidades de UI desktop da Oracle foi para o JavaFX, e Swing entrou num regime de estabilidade. A comunidade costuma chamar esse regime de **"modo de manutenção"** (*maintenance mode*). 

> [!warning] "Modo de manutenção" é jargão da comunidade, não termo oficial
> A Oracle **não** usa a expressão "maintenance mode" para Swing nos documentos oficiais; o termo oficial é **"core Java SE technologies"** que continuam suportadas. "Modo de manutenção" é uma **leitura da comunidade** do ritmo de evolução, não uma declaração da Oracle. Em entrevista, separe as duas: *"officially, Oracle calls Swing a core Java SE technology supported as long as the JDK is supported; the 'maintenance mode' label is the community's de-facto read of how little it evolves, not Oracle's wording."* Confundir as duas é a primeira armadilha (abaixo).

**Como ler o roadmap em termos práticos.** O *Java Client Roadmap Update* amarra o suporte de Swing/AWT ao **ciclo de vida das releases do JDK**: enquanto uma release (em especial as **LTS** — Long-Term Support) estiver dentro da janela de suporte da Oracle, Swing e AWT recebem correções junto. Não há um "fim de vida do Swing" separado do fim de vida do JDK — eles morrem juntos, e nenhuma release de JDK suportada hoje tem isso no horizonte. Para a janela concreta de cada release, a referência é o [Oracle Java SE Support Roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html). Em decisão de arquitetura, a leitura é simples: **escolher Swing não cria risco de "ficar sem suporte"** num horizonte previsível — o risco real é outro (pouca evolução de features, ajuste cultural do time), e é esse que deve pesar.

E uma honestidade sobre dados: **esta nota não cita estatística de adoção** ("X de cada Y empresas usam Swing"). Não há fonte oficial com esses números, e inventá-los seria fabricação. O que se pode afirmar **qualitativamente** é o que vem a seguir: onde Swing ainda aparece e onde não aparece.

### Onde Swing ainda faz sentido

Qualitativamente, Swing segue sendo uma escolha defensável — às vezes a melhor — num conjunto de cenários:

- **Ferramentas internas e telas de admin.** Apps de linha-de-negócio, dashboards operacionais, ferramentas de back-office que rodam dentro da empresa. UI funcional importa mais que UI deslumbrante; *time-to-market* e baixo custo de manutenção importam muito.
- **IDEs e ferramentas de desenvolvimento.** O exemplo mais forte: **IntelliJ IDEA** e **NetBeans** têm UI construída em **Swing**; o **Eclipse** usa **SWT** (toolkit nativo diferente, mas igualmente desktop-Java). São aplicações enormes, maduras e amplamente usadas — prova viva de que Swing escala para UIs complexas e de longa vida.
- **Apps desktop offline / legados.** Software que precisa rodar sem rede, com acesso direto ao filesystem e a hardware local, ou bases de código já em Swing onde reescrever não se paga.
- **Embedded e ambientes controlados.** Quiosques, painéis industriais, sistemas onde se controla a JVM e o SO e não se quer arrastar um runtime de UI externo.
- **Zero dependência externa pesada.** Swing **vem no JDK**. Não há que adicionar JavaFX standalone, nem um runtime web, nem empacotar Chromium. Para um app pequeno que precisa só funcionar, isso é uma vantagem real.

> [!info] Swing e SWT não são a mesma coisa
> Ao citar IDEs, vale a precisão: **IntelliJ IDEA e NetBeans usam Swing**; **Eclipse usa SWT** (*Standard Widget Toolkit*), um toolkit de UI desktop-Java que, ao contrário do Swing, é **heavyweight** — usa *widgets* nativos do SO via JNI, na linha do antigo AWT. Os dois são "desktop em Java", mas com filosofias opostas (Swing lightweight, pintado em Java; SWT nativo). Um detalhe de precisão: o NetBeans é construído sobre a **NetBeans Platform**, um framework para aplicações Swing — sua UI é Swing via essa camada de plataforma, enquanto o IntelliJ usa Swing mais diretamente (com o JetBrains Runtime). O ponto comum, para esta nota, é que **UIs de IDE de larga escala continuam sendo construídas em Java desktop** — Swing inclusive. É a evidência mais forte de que Swing aguenta complexidade real.

### Onde Swing NÃO faz sentido

Com a mesma honestidade, há cenários onde escolher Swing hoje é arquitetura ruim:

- **App moderno com UI rica/animada.** Transições fluidas, *theming* sofisticado por CSS, gráficos vetoriais, *data binding* declarativo — JavaFX e stacks web entregam isso de forma muito mais natural. Reproduzir em Swing custa caro.
- **Web.** Se o requisito é rodar no navegador, sem instalação, Swing não compete — é desktop por construção.
- **Mobile.** Swing não tem história em Android/iOS. Fora de escopo.
- **Time sem experiência desktop.** Um time que vive em React/web pagará uma curva de aprendizado (EDT, *layout managers*, *look and feel*) que talvez não se justifique se o produto não exige desktop nativo.

> [!warning] A armadilha do "mas é só uma telinha"
> O custo escondido de escolher Swing num time sem cultura desktop aparece **depois** do protótipo. A primeira janela é fácil; o que custa é a manutenção sob a *single-thread rule* — cada chamada de I/O num *listener* que congela a UI, cada `setText` fora da EDT que corrompe a tela de forma intermitente. Um time que não internalizou o modelo da [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|EDT]] vai acumular esses bugs e culpar o "Swing velho", quando o problema é falta de fluência no modelo. Em decisão de arquitetura, **fluência do time é um critério de primeira classe**, não um detalhe.

### Swing × virtual threads

Aqui mora a armadilha técnica mais sutil, e a nota a trata **sem hype**.

As **virtual threads** (Galho 4, GA no Java 21 — veja [[03-Dominios/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]) são threads leves multiplexadas pela JVM, ótimas para trabalho **I/O-bound** e alta concorrência. Num app Swing, elas melhoram o lado do **background**: a tarefa lenta que antes ocupava uma *platform thread* cara pode agora rodar numa virtual thread barata, e você pode ter muitas delas.

**O que elas NÃO fazem:** mudar a EDT. A **Event Dispatch Thread continua sendo uma única thread** (veja [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|A Event Dispatch Thread (EDT)]]). A **single-thread rule do Swing permanece intacta**: todo acesso a componente ainda tem de ocorrer na EDT, e você ainda reentra nela via `SwingUtilities.invokeLater`. Virtual threads não tornam o Swing thread-safe, não paralelizam a pintura, não "consertam" o congelamento de UI — a UI congela exatamente do mesmo jeito se você bloquear a EDT.

> [!example] O que muda e o que não muda
> ```java
> // ANTES: background numa platform thread
> new Thread(() -> {
>     var dados = consultarServico();                 // I/O lento, fora da EDT
>     SwingUtilities.invokeLater(() -> label.setText(dados)); // reentra na EDT
> }, "bg").start();
>
> // DEPOIS (Java 21+): background numa virtual thread — mais barata em escala
> Thread.ofVirtual().start(() -> {
>     var dados = consultarServico();                 // I/O lento, fora da EDT
>     SwingUtilities.invokeLater(() -> label.setText(dados)); // a EDT é a MESMA
> });
> ```
> O `invokeLater` continua obrigatório. A EDT é a mesma single-thread de sempre. Virtual threads só barateiam o lado de fora — nada mais.

Há ainda um ponto fino que separa o candidato sênior: a EDT **não deve** ser uma virtual thread, e não é. A EDT é uma *platform thread* dedicada, de vida longa, que faz trabalho de UI contínuo — exatamente o perfil **errado** para virtual threads, que brilham em tarefas de vida curta e *I/O-bound* que bloqueiam e desmontam. As virtual threads entram do lado de **fora** da UI (as tarefas que você dispara a partir de um *listener*), nunca como a thread de despacho. Se alguém propuser "rodar a EDT como virtual thread", a resposta é não — é uma incompreensão tanto do modelo da EDT quanto do caso de uso de virtual threads.

Em resumo honesto: virtual threads são uma boa notícia para o **trabalho de background** de apps Swing, e **irrelevantes** para o modelo de threading da própria UI. Quem disser em entrevista que "virtual threads modernizam a EDT" está errado.

### O ecossistema vivo

"Pouca evolução na API do JDK" não é o mesmo que "ecossistema parado". Há ferramentas *third-party* ativas que mantêm Swing visualmente atual e produtivo:

- **FlatLaf** — um *Look and Feel* moderno (flat, com *dark mode* e temas tipo IntelliJ) que tira o "cara de 2005" de um app Swing com poucas linhas. É o exemplo mais citado de que Swing pode parecer moderno hoje. Veja [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel e temas]].
- **Builders e bibliotecas de componentes** mantidos pela comunidade, que cobrem lacunas de produtividade.

A leitura honesta: o **núcleo** evolui devagar, mas o **ecossistema** ao redor mantém Swing utilizável e até agradável para os nichos onde ele faz sentido. Essas ferramentas são *third-party* — não fazem parte do JDK — e essa dependência precisa entrar na conta da decisão de arquitetura.

Há uma tensão honesta aqui: o argumento "Swing vem no JDK, zero dependência" enfraquece um pouco quando, na prática, você adiciona FlatLaf e mais um par de bibliotecas para chegar a uma UI moderna. A conta continua leve comparada a empacotar um runtime web, mas deixou de ser estritamente "zero dependência". Vale ser preciso sobre isso em vez de vender o JDK puro como se bastasse para um app polido.

Outra peça do "Swing hoje" do lado de **distribuição**: o `jpackage` (ferramenta do JDK) empacota uma app desktop Java — Swing inclusive — como **instalador nativo** (`.msi`/`.dmg`/`.deb`) com um runtime embarcado, sem exigir que o usuário tenha Java instalado. Isso responde a uma crítica antiga ("apps Java desktop são chatos de distribuir") e é parte do motivo de Swing seguir viável para apps que precisam chegar à máquina do usuário final como um app comum.

### E o JavaFX?

A outra opção de UI desktop do Java é o **JavaFX**: mais novo, com *theming* por CSS, *data binding* declarativo, animação e gráficos vetoriais de primeira classe. Um detalhe arquitetural relevante: **a partir do Java 11, o JavaFX foi desacoplado do JDK** — deixou de vir empacotado e passou a ser um módulo standalone (OpenJFX), adicionado como dependência. Swing e AWT, ao contrário, **continuam dentro do JDK**.

A comparação detalhada — quando preferir JavaFX a Swing, o modelo de *scene graph*, *properties* e *binding* — é assunto do **Galho 6 (JavaFX, planejado)**, não desta nota. Aqui o JavaFX entra só como **gancho**: saiba que existe, que é a alternativa desktop "moderna" do Java, e que vive fora do JDK desde o Java 11.

Um esclarecimento que evita um mal-entendido comum em entrevista: **JavaFX estar fora do JDK não significa "abandonado"** — significa que evolui no seu **próprio ciclo** (OpenJFX), desacoplado do JDK, podendo lançar mais rápido. E **Swing continuar no JDK não significa "preferido"** — significa que faz parte da especificação Java SE e é mantido como tal. São dois modelos de empacotamento diferentes, não um ranking de qualidade. A escolha entre eles é de *fit* com o projeto, não de "qual a Oracle gosta mais".

## Na prática

A decisão concreta cabe numa **árvore de decisão**: *"devo usar Swing neste projeto?"*

```text
É um app desktop? ──não──► Swing está fora.
   │                       (web → stack web; mobile → Android/iOS nativo)
   sim
   │
   ▼
Já existe base Swing / é manutenção de legado? ──sim──► Swing (continue; não reescreva sem ganho claro)
   │
   não (greenfield)
   │
   ▼
É ferramenta interna / admin / IDE-plugin / embedded,
UI funcional, offline, zero-dependência-externa? ──sim──► Swing é defensável (talvez a melhor escolha)
   │
   não
   │
   ▼
Precisa de UI rica/animada, theming sofisticado,
data binding declarativo? ──────────────────────sim──► Avalie JavaFX (planejado) ou web; Swing custa caro aqui
   │
   não / indiferente
   │
   ▼
Time tem experiência desktop-Java? ──não──► Pese a curva (EDT, layouts, L&F) vs alternativa que o time já domina
   │
   sim
   ▼
Swing segue sendo uma escolha pragmática.
```

Resumido em uma tabela de cenário → veredito:

| Cenário | Swing hoje? |
|---------|-------------|
| Ferramenta interna / tela de admin | Sim, defensável |
| Plugin/UI de IDE, app maduro em Swing | Sim (é o terreno natural) |
| Desktop offline / acesso a hardware local | Sim |
| Legado em Swing (manutenção) | Sim — não reescreva sem ganho claro |
| Greenfield com UI rica/animada | Não — avalie JavaFX (planejado) ou web |
| Aplicação web | Não (Swing é desktop) |
| Mobile | Não (fora de escopo) |
| Time só-web, sem cultura desktop | Provavelmente não — pese a curva |

A regra-mestra: **a inércia não é argumento**. "Já sabemos Swing" justifica continuar um legado; **não** justifica iniciar um greenfield moderno sem antes comparar com as alternativas.

### Um exemplo de aplicação da árvore

Para ver a árvore funcionando, três cenários concretos:

- **"Ferramenta de operações que roda na intranet, lê arquivos locais, sem UI sofisticada, time já em Java backend."** → desktop sim → greenfield → ferramenta interna/offline/zero-dep → **Swing é defensável**. Some FlatLaf para não parecer datado e siga. A *single-thread rule* é o único custo de aprendizado, e é bem documentada.
- **"App de produto com UI animada, gráficos, terá versão web no roadmap, time vem de front-end web."** → desktop talvez, mas web no horizonte → UI rica → time só-web → **Swing está fora**: avalie uma stack web (que cobre o futuro web de graça) ou, se desktop nativo for mandatório, **JavaFX (planejado)**.
- **"Sistema legado de 200 telas em Swing, em manutenção, com bugs ocasionais de EDT."** → desktop sim → legado → **continue em Swing**; reescrever 200 telas raramente se paga. O esforço melhor investido é treinar o time no modelo da EDT e adotar `SwingWorker`/FlatLaf incrementalmente.

O denominador comum dos três: a decisão saiu de **critérios** (desktop? legado? nicho? time?), não de gosto. É assim que se defende a escolha numa revisão de arquitetura — ou numa entrevista.

## Armadilhas

São armadilhas **de raciocínio** — erros de leitura do estado atual, não bugs de código.

### (1) Tratar Swing como "morto" ou "deprecado"

**Descrição.** Afirmar, em entrevista ou em decisão de arquitetura, que "Swing está morto / foi deprecado / vai ser removido". É **factualmente errado**: a Oracle declara Swing e AWT como **"core Java SE technologies"** suportadas enquanto o JDK for suportado, sem *deprecation* nem data de remoção. Quem diz isso perde credibilidade na hora — basta o entrevistador conhecer o roadmap.

**Raciocínio correto.** Declare o status com precisão e cite a fonte: *"Swing isn't deprecated — Oracle's Java Client Roadmap (2018, updated 2020) calls Swing and AWT core Java SE technologies, supported as long as the JDK is. What's true is that it evolves slowly; the 'maintenance mode' label is the community's read, not Oracle's term."* Distinga **status oficial** (suportado) de **ritmo de evolução** (lento). As duas coisas convivem.

---

### (2) Escolher Swing por inércia para um greenfield moderno

**Descrição.** Iniciar um projeto **novo** com UI rica/animada em Swing **só porque o time já conhece Swing** — sem comparar com as alternativas. A inércia ("é o que sabemos") é um argumento legítimo para **manter legado**, mas fraco para **decidir greenfield**. O resultado costuma ser reproduzir trabalhosamente em Swing o que JavaFX ou uma stack web entregariam de graça (animação, CSS, *binding*).

**Raciocínio correto.** Para greenfield, faça a comparação explícita: o app precisa mesmo ser desktop? Se sim, **JavaFX (planejado)** entrega *theming* por CSS, *data binding* e animação como cidadãos de primeira classe; se o requisito for navegador, uma **stack web** vence. Escolha Swing por greenfield só quando o nicho o favorece (ferramenta interna, offline, zero-dependência, UI funcional) — não por hábito.

---

### (3) Achar que virtual threads "consertam" a natureza single-thread da EDT

**Descrição.** Supor que, com **virtual threads** (Java 21), o problema do *single-thread* do Swing "acabou" — que agora dá para tocar componentes de várias threads, ou que a UI não congela mais. Falso. Virtual threads aceleram/barateiam o **background**, mas **não alteram o modelo de threading da UI**: a **EDT continua single-thread**, a *single-thread rule* continua valendo, e bloquear a EDT continua congelando a tela exatamente como antes.

**Raciocínio correto.** Separe os dois mundos: virtual threads são para o **trabalho fora da UI** (I/O, alta concorrência); a **EDT é imutável** quanto a isso. Você ainda faz o trabalho lento numa thread de background (que *pode* ser virtual) e ainda reentra na EDT via `SwingUtilities.invokeLater`. Em entrevista: *"virtual threads improve the background side of a Swing app, but the EDT is still single-threaded — you still marshal updates back with `invokeLater`; they don't make Swing thread-safe."* Veja [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|A Event Dispatch Thread (EDT)]].

## Em entrevista

Esta é a nota que ancora a resposta "madura" sobre Swing: não vender nem enterrar, **enquadrar como decisão de arquitetura honesta** — quando sim, quando não, com o *caveat* de status correto.

### Frase pronta (inglês)

> "I treat Swing as an architecture decision, not as 'alive or dead'. Officially, Swing and AWT are core Java SE technologies — Oracle's Java Client Roadmap, from 2018 and updated in 2020, says they're supported as long as the JDK is supported; they're not deprecated and there's no removal date. What's true is that they evolve slowly, with few new features — the 'maintenance mode' label you hear is the community's de-facto read, not Oracle's wording. So I'd reach for Swing when the fit is right: internal and admin tools, IDE or developer tooling — IntelliJ and NetBeans are built on Swing, Eclipse on SWT — offline or embedded desktop apps, and legacy codebases. It ships in the JDK with zero external dependency, and the third-party ecosystem, like FlatLaf, keeps it looking modern. I'd avoid it for a greenfield app that needs a rich, animated UI, for the web, or for mobile — there JavaFX or a web stack fit better, and JavaFX has been decoupled from the JDK since Java 11. One nuance people get wrong: virtual threads from Java 21 help the background work in a Swing app, but they don't change the Event Dispatch Thread — it's still single-threaded, so you still marshal UI updates back with `invokeLater`. They don't make Swing thread-safe."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| tecnologia core do Java SE | core Java SE technology |
| suportado enquanto o JDK for suportado | supported as long as the JDK is supported |
| deprecado / marcado para remoção | deprecated / marked for removal |
| modo de manutenção (jargão) | maintenance mode (community jargon) |
| roadmap (de cliente Java) | (Java client) roadmap |
| ferramenta interna / de back-office | internal / back-office tool |
| app legado | legacy app |
| desacoplado do JDK | decoupled from the JDK |
| projeto novo / do zero | greenfield project |
| escolha por inércia | choice by inertia |
| natureza single-thread da EDT | single-threaded nature of the EDT |
| entregar atualizações de UI de volta à EDT | marshal UI updates back to the EDT |

### Cheatsheet do galho

Mapa rápido "qual nota do galho Swing resolve qual problema" — útil para revisar o galho inteiro antes de uma entrevista:

| Preciso de… | Nota |
|-------------|------|
| Fundamentos: o que é Swing, lightweight vs heavyweight, top-level containers | [[03-Dominios/Java/Swing/01 - O modelo do Swing\|01 – O modelo do Swing]] |
| Componentes e containers; layout; modelo de eventos | 02 – Componentes / 03 – Layout managers / 04 – Modelo de eventos |
| Threading / EDT: por que single-thread, `invokeLater`/`invokeAndWait` | [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread\|05 – EDT]] |
| Background work sem congelar a UI | 06 – SwingWorker |
| Models (MVC em Swing): `TableModel`, `ListModel`, separar dado de view | [[03-Dominios/Java/Swing/07 - MVC em Swing e os models\|07 – MVC e models]] |
| Renderizar/editar células de tabelas, listas, árvores | 08 – Renderers e editors |
| Aparência: Look and Feel, temas, FlatLaf, dark mode | [[03-Dominios/Java/Swing/09 - Look and Feel e temas\|09 – Look and Feel]] |
| Pintura customizada, componentes próprios | 10 – Custom painting |
| Atalhos de teclado, `Action` API, performance | 11 – Action API / key bindings |
| "Devo usar Swing? Status oficial, nichos, virtual threads" | esta nota (12 – capstone) |

> [!tip] A resposta de 30 segundos
> *"Supported core Java SE, not deprecated, but evolving slowly. Great for internal tools, IDEs, offline/legacy desktop, zero-dependency. Wrong for rich modern UIs, web, or mobile — there I'd look at JavaFX or a web stack. And virtual threads help the background, not the EDT."* — é isso, em uma respiração.

### O erro que derruba o candidato

Vale memorizar o **anti-padrão de resposta**, porque é o que mais reprova. O candidato fraco diz uma de duas coisas opostas e ambas erradas: ou *"Swing está morto, ninguém usa mais"* (falso — é suportado e move IntelliJ/NetBeans), ou *"Swing é ótimo, uso pra tudo"* (ingênuo — ignora web/mobile/UI rica). A resposta sênior **recusa os dois extremos** e entrega a leitura calibrada: suportado mas estável, certo para um nicho, errado para outro, com o *caveat* de que "modo de manutenção" é jargão e não termo oficial. Demonstrar essa calibração — e citar a fonte com data — é o que sinaliza maturidade de arquitetura.

## Veja também

- [[03-Dominios/Java/Swing/01 - O modelo do Swing|O modelo do Swing]]
- [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|A Event Dispatch Thread (EDT)]]
- [[03-Dominios/Java/Swing/07 - MVC em Swing e os models|MVC em Swing e os models]]
- [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel e temas]]
- [[03-Dominios/Java/Swing/index|Swing (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]
- [[03-Dominios/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]
- JavaFX — a alternativa desktop moderna do Java — é tema do **Galho 6 (JavaFX, planejado)**.

## Referências

- **[Java Client Roadmap Updates — Oracle Blogs (fonte oficial Oracle)](https://blogs.oracle.com/java/post/java-client-roadmap-updates)** — declara Swing e AWT como *core Java SE technologies*, suportadas enquanto o JDK for suportado; não deprecadas.
- **[Java Client Roadmap Update — White Paper (Oracle, março de 2018; fonte oficial Oracle)](https://www.oracle.com/docs/tech/java/javaclientroadmapupdate2018mar.pdf)** — documento original do roadmap; afirma o compromisso de continuar desenvolvendo Swing e AWT no Java SE e descreve o desacoplamento do JavaFX do JDK a partir do Java 11.
- **[Java Client Roadmap Update (Oracle, maio de 2020; fonte oficial Oracle)](https://www.oracle.com/technetwork/java/javase/javaclientroadmapupdatev2020may-6548840.pdf)** — atualização de 2020 do mesmo roadmap, reafirmando o status de Swing/AWT.
- **[Oracle Java SE Support Roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html)** — janelas de suporte das releases (LTS), que governam por quanto tempo Swing/AWT continuam suportados.
- **[dev.java](https://dev.java/)** — portal oficial de aprendizado Java; material de desktop/Swing e estado do Java atual.
- Cross-ref interno (Galho 4): [[03-Dominios/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]] — base do *caveat* de que virtual threads não alteram a EDT.
