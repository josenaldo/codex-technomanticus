---
title: "Empacotamento — módulos, jlink e jpackage"
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
  - jpackage
  - jpms
aliases:
  - "Empacotamento JavaFX"
  - "jpackage"
  - "jlink"
  - "module-path"
---

# Empacotamento — módulos, jlink e jpackage

> [!abstract] TL;DR
> JavaFX é um conjunto de **módulos JPMS que vivem FORA do JDK**. Em desenvolvimento, o `--module-path` resolve esses módulos e a aplicação roda. Para **distribuir** ao usuário final, duas ferramentas do JDK entram em cena: **`jlink`** monta um runtime image enxuto (só os módulos que você usa, JavaFX inclusos) e **`jpackage`** (JEP 392) gera um **instalador nativo** por plataforma (`deb`/`rpm`, `msi`/`exe`, `dmg`/`pkg`) com esse runtime embarcado. O resultado: ninguém mais pede "instale o Java" pro usuário final — o runtime exato viaja dentro do pacote.

## O que é

Esta nota cobre o caminho que vai do **código** ao **executável distribuível**: como uma aplicação JavaFX, que roda lisa na IDE, vira um instalador que um usuário não-técnico clica e usa, sem nunca tocar numa linha de comando ou instalar um JDK.

JavaFX torna esse assunto **obrigatório** de entender por um motivo estrutural: ele **não está no JDK** (desacoplado no Java 11 — ver [[01 - JavaFX — o que é e como chega ao projeto]]). Em Swing puro, o toolkit é parte do core Java SE; qualquer JRE/JDK o tem. JavaFX, não. Os módulos `javafx.*` são dependências externas que precisam estar presentes em **tempo de execução** — e o launcher do JavaFX checa isso explicitamente. Distribuir uma app JavaFX é, antes de tudo, garantir que esses módulos cheguem junto.

As três peças:

- **Módulos JPMS** — JavaFX é entregue como módulos nomeados (`javafx.controls`, `javafx.fxml`, ...). A mecânica do JPMS (o que é `module-info`, `requires`, delegação de leitura) é do Galho 3: [[03-Dominios/Java/JVM/08 - JPMS — o sistema de módulos|JPMS (Galho 3)]]. Aqui **aplicamos** ao JavaFX, sem re-explicar.
- **`jlink`** — ferramenta do JDK que cria um *runtime image* customizado: um mini-Java contendo só os módulos necessários (os seus + os do JavaFX), em vez do JDK inteiro.
- **`jpackage`** — ferramenta do JDK (JEP 392, produção no Java 16) que pega seu app + um runtime e produz um **pacote nativo** da plataforma alvo.

## Por que importa

"Roda na IDE, não roda fora" é o **rito de passagem** do empacotamento JavaFX. A IDE (ou o `javafx-maven-plugin`) monta o `--module-path` por você silenciosamente; no momento em que você tenta `java -jar app.jar` ou um duplo-clique, o andaime some e o launcher do JavaFX aborta com a mensagem famosa:

```text
Error: JavaFX runtime components are missing, and are required to run this application
```

Em entrevista de sênior, **esse erro É a pergunta**. Quem sabe explicar *por que* ele acontece (o launcher checa os módulos JavaFX no boot) e *como* resolver para os dois mundos — rodar localmente (`--module-path`/`--add-modules`) e distribuir (jlink + jpackage) — demonstra que entende a fronteira JDK/OpenJFX e o ciclo de vida de distribuição, não só a API de UI.

E há o lado do produto: **app desktop profissional se distribui com runtime embarcado**. Pedir "baixe e instale o Java 21" pro usuário final em 2026 é fricção inaceitável e fonte de bugs por versão errada. O padrão moderno é o instalador autocontido — e é exatamente o que `jpackage` produz.

## Como funciona

### JavaFX como módulos JPMS

JavaFX é distribuído como um grafo de módulos nomeados. Os principais:

| Módulo | Papel | Depende de (requires) |
|--------|-------|-----------------------|
| `javafx.base` | Fundação: properties, binding, collections observáveis, eventos | — (raiz) |
| `javafx.graphics` | Scene graph, render, animação, geometria, CSS, Application/Stage/Scene | `javafx.base` |
| `javafx.controls` | Controles de UI (Button, TableView, ...) e layouts | `javafx.graphics` (→ `javafx.base`) |
| `javafx.fxml` | Carregamento de layouts FXML (`FXMLLoader`) | `javafx.base` (+ usa `javafx.graphics`/controls em runtime) |
| `javafx.media` | Áudio e vídeo | `javafx.graphics` |
| `javafx.web` | `WebView` (engine web embarcada) | `javafx.controls`, `javafx.media` |
| `javafx.swing` | Interop com Swing (`SwingNode`, `JFXPanel`) | `javafx.graphics` |

O ponto prático: **`javafx.controls` puxa `javafx.graphics`, que puxa `javafx.base`**. Então declarar `javafx.controls` já traz a cadeia transitiva — você não precisa listar `graphics` e `base` à mão. Mas `javafx.fxml` **não** vem junto: se a app usa FXML, esse módulo precisa entrar **explicitamente**.

A mecânica de como o JPMS resolve esse grafo (root modules, leitura, `requires transitive`, o module path vs. o classpath) é do Galho 3 — ver [[03-Dominios/Java/JVM/08 - JPMS — o sistema de módulos|JPMS (Galho 3)]]. Aqui basta a regra de aplicação: **liste no `--add-modules` todo módulo JavaFX que você usa diretamente**, deixando o resolver completar o transitivo.

### Por que `java -jar app.jar` falha

A classe principal de uma app JavaFX normalmente estende `javafx.application.Application`. Quando a JVM tenta lançar uma subclasse de `Application` como main class, o **launcher do JavaFX** roda primeiro e verifica que os módulos do JavaFX estão presentes e corretamente carregados. Se eles não estão no module path, ele aborta com:

```text
Error: JavaFX runtime components are missing, and are required to run this application
```

Há **duas saídas**:

1. **Fornecer os módulos** — invocar com `--module-path` apontando pros jars/jmods do JavaFX e `--add-modules` listando os módulos usados. É o que o `javafx-maven-plugin` faz por baixo dos panos.
2. **Classe launcher separada** — uma classe que **não** estende `Application`, com um `main` estático que apenas chama `Application.launch(MinhaApp.class, args)`. Como a main class não é uma `Application`, o checador estrito do launcher não dispara da mesma forma — padrão clássico para "fat jars" no classpath. (Continua exigindo os módulos JavaFX disponíveis; só contorna o aborto precoce.)

### App modular vs. não-modular

| | **Modular** (com `module-info.java`) | **Não-modular** (sem `module-info`) |
|--|--------------------------------------|-------------------------------------|
| Declaração de deps | `requires javafx.controls;` no `module-info` | nada — jars no classpath ou module path |
| `jlink` | **Funciona** — exige mundo modular | **Não funciona** direto (automatic modules) |
| `jpackage` | via `--module` | via `--input` + `--main-jar` |
| Encapsulamento | forte (JPMS); precisa `opens` p/ FXML/reflection | nenhum |
| Trade-off | mais cerimônia, mas habilita runtime enxuto | mais simples, mas perde jlink |

A escolha tem consequência direta no empacotamento: **se você quer `jlink`, precisa ser modular**. Se ficar não-modular, ainda dá pra distribuir com `jpackage` — mas o runtime embarcado tende a ser maior (ou você gera o runtime à parte com jlink só dos módulos da plataforma + JavaFX e passa via `--runtime-image`).

### jlink — runtime image enxuto

`jlink` monta uma imagem de runtime contendo **apenas** os módulos que sua aplicação precisa — os seus módulos mais os do JavaFX mais os do JDK que eles transitivamente exigem. Em vez de um JDK de centenas de MB, você fica com um runtime sob medida.

Exige **mundo modular**: todos os módulos no grafo precisam ser módulos nomeados de verdade (não automatic modules derivados de jars sem `module-info`). Flags de redução confirmadas na man page do JDK 21:

- `--module-path` / `-p` — onde achar os módulos (default: `$JAVA_HOME/jmods`).
- `--add-modules` — os módulos raiz a incluir.
- `--output` — onde gravar o runtime image gerado.
- `--strip-debug` — remove informação de debug da imagem.
- `--no-header-files` — exclui header files (`.h` de JNI).
- `--no-man-pages` — exclui man pages.
- `--compress=0|1|2` — `0` sem compressão, `1` *constant string sharing*, `2` ZIP.

### jpackage — instalador nativo (JEP 392)

`jpackage` empacota a aplicação Java num pacote específico da plataforma, incluindo todas as dependências necessárias. Entregue como **produção no Java 16** (JEP 392), depois de incubar no Java 14–15 (JEP 343).

Modos de saída, via `--type` / `-t` (valores confirmados na man page: `app-image`, `exe`, `msi`, `rpm`, `deb`, `pkg`, `dmg`):

- **`app-image`** — um diretório com a app + runtime, sem instalador (bom pra zipar ou pra debug).
- **Instalador nativo por plataforma:**
  - **Linux** → `deb` (Debian/Ubuntu) ou `rpm` (Fedora/RHEL)
  - **Windows** → `msi` ou `exe`
  - **macOS** → `dmg` ou `pkg`

> Cada formato só é gerado **na plataforma correspondente** — `jpackage` não faz cross-build. Para gerar `.msi`, rode num Windows; para `.dmg`, num macOS.

Funciona com app **não-modular também**: aí você usa `--input` (diretório com os jars) + `--main-jar` (o jar com a main) + `--main-class`. Para app modular, usa `--module modulo/classe`. Flags-chave (man page JDK 21):

- `--input` / `-i` — diretório de entrada com os arquivos a empacotar (modo não-modular).
- `--main-jar` — jar principal, relativo ao `--input` (mutuamente exclusivo com `--module`).
- `--main-class` — classe main qualificada (só com `--main-jar`).
- `--module` / `-m` — módulo principal `[/main-class]` (mutuamente exclusivo com `--main-jar`).
- `--module-path` / `-p` — paths de módulos.
- `--add-modules` — módulos a adicionar (repassado ao jlink como `--add-modules`).
- `--icon` — ícone do pacote.
- `--app-version` — versão da aplicação/pacote.
- `--runtime-image` — runtime image predefinido a copiar pra dentro do pacote. **Se omitido, `jpackage` roda `jlink` automaticamente** pra criar o runtime.

Esse último é a ponte com o jlink: você gera o runtime enxuto com `jlink`, depois passa via `--runtime-image` pro `jpackage`, controlando exatamente o que viaja.

### Native image

Há um caminho ainda mais agressivo: compilar a app a um binário nativo único (sem JVM), via GraalVM Native Image e Gluon Substrate, com tempo de startup quase instantâneo e footprint reduzido. É o que viabiliza JavaFX em mobile e ambientes restritos. O conceito de native image é tratado no [[03-Dominios/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|Galho 17 (nota 08)]], embora o alvo lá seja serviços server-side, não o destino desktop/mobile do Gluon Substrate.

## Na prática

### (a) O erro de runtime e o fix mínimo

O erro completo ao tentar rodar a classe `Application` sem o module path:

```text
Error: JavaFX runtime components are missing, and are required to run this application
```

O fix manual — supondo `$PATH_TO_FX` apontando pro diretório `lib` do JavaFX SDK:

```bash
# Linux/macOS — $PATH_TO_FX = .../javafx-sdk-21/lib
java \
  --module-path "$PATH_TO_FX" \
  --add-modules javafx.controls,javafx.fxml \
  -jar app.jar
```

Os módulos no `--add-modules` são os que a app usa **diretamente**: `javafx.controls` (UI) e `javafx.fxml` (carregamento de FXML). O resolver completa `graphics` e `base` por transitividade.

### (b) jlink de app modular — runtime enxuto

Pré-requisito: app modular (tem `module-info.java`), JavaFX disponível como **jmods**.

```bash
jlink \
  --module-path "$JAVA_HOME/jmods:$PATH_TO_FX_JMODS" \
  --add-modules com.exemplo.app \
  --output runtime/ \
  --strip-debug \
  --no-header-files \
  --no-man-pages \
  --compress=2
```

Comentário de cada flag:

- `--module-path` — junta os jmods do JDK com os jmods do JavaFX.
- `--add-modules com.exemplo.app` — o módulo raiz da aplicação; o resolver puxa `javafx.controls`, `javafx.fxml` e o transitivo a partir do `requires` do `module-info`.
- `--output runtime/` — diretório do runtime image gerado.
- `--strip-debug` / `--no-header-files` / `--no-man-pages` — removem o que não serve em produção.
- `--compress=2` — compressão ZIP dos recursos.

> Ilustrativo: um runtime image enxuto de uma app JavaFX típica fica na casa de poucas dezenas de MB, contra centenas de MB de um JDK completo. O número exato depende dos módulos e da plataforma — trate como ordem de grandeza, não promessa.

### (c) jpackage — gerando o instalador

**Variante modular** (usa `--module`):

```bash
jpackage \
  --type deb \
  --name MinhaApp \
  --app-version 1.0.0 \
  --icon assets/app.png \
  --module-path "$PATH_TO_FX_JMODS:out/modules" \
  --module com.exemplo.app/com.exemplo.app.Main \
  --runtime-image runtime/
```

**Variante não-modular** (usa `--input` + `--main-jar`):

```bash
jpackage \
  --type msi \
  --name MinhaApp \
  --app-version 1.0.0 \
  --icon assets/app.ico \
  --input dist/ \
  --main-jar app.jar \
  --main-class com.exemplo.app.Launcher
```

Notas:

- `--type` escolhe o formato; troque por `rpm`/`exe`/`dmg`/`pkg` conforme a plataforma alvo (rodando **naquela** plataforma).
- `--runtime-image runtime/` (variante modular) reutiliza o runtime do passo (b); sem ela, `jpackage` roda `jlink` sozinho.
- Na variante não-modular, `--main-class` aponta pra uma classe **launcher** que chama `Application.launch(...)`, não pra uma `Application` direta.

## Armadilhas

### (1) `java -jar` com JavaFX no classpath

**O problema:** colocar os jars do JavaFX no classpath e rodar a `Application` diretamente. O launcher do JavaFX checa os módulos e aborta:

```text
Error: JavaFX runtime components are missing, and are required to run this application
```

**Fix:** ou fornecer os módulos via `--module-path "$PATH_TO_FX" --add-modules javafx.controls,...`, ou usar uma **classe launcher separada** com `main` estática que chama `Application.launch(MinhaApp.class, args)` — a main class deixa de ser uma `Application` e o aborto precoce não dispara.

```java
public class Launcher {                 // NÃO estende Application
    public static void main(String[] args) {
        MinhaApp.main(args);            // ou Application.launch(MinhaApp.class, args)
    }
}
```

---

### (2) Esquecer `javafx.fxml` no `--add-modules`

**O problema:** a app usa FXML, mas o `--add-modules` lista só `javafx.controls`. Compila, mas em **runtime** o `FXMLLoader` quebra:

```text
java.lang.module.FindException / NoClassDefFoundError: javafx/fxml/FXMLLoader
... javafx.fxml.LoadException ...
```

`javafx.fxml` **não** é puxado transitivamente por `javafx.controls`.

**Fix:** listar **todos** os módulos JavaFX usados diretamente:

```bash
--add-modules javafx.controls,javafx.fxml
# + javafx.media / javafx.web se a app os usar
```

---

### (3) jlink com app não-modular ou automatic modules

**O problema:** rodar `jlink` sobre uma app sem `module-info.java`. Os jars viram *automatic modules*, e `jlink` recusa:

```text
Error: ... is not a modular JAR / automatic modules are not allowed in the image
```

`jlink` exige um grafo **totalmente modular**.

**Fix:** ou **modularizar** a app (adicionar `module-info.java` com `requires javafx.controls; requires javafx.fxml;`), ou **pular o jlink** e gerar o runtime à parte só dos módulos JavaFX + JDK, passando-o ao `jpackage` via `--runtime-image`:

```bash
# runtime só dos módulos da plataforma + JavaFX (não depende do app ser modular)
jlink --module-path "$JAVA_HOME/jmods:$PATH_TO_FX_JMODS" \
      --add-modules javafx.controls,javafx.fxml \
      --output runtime/
# depois: jpackage --runtime-image runtime/ --input dist/ --main-jar app.jar ...
```

---

### (4) Pedir "instale o Java" pro usuário final em 2026

**O problema:** distribuir só o jar e instruir o usuário a baixar e instalar um JDK/JRE. Não existe mais um JRE standalone confiável e universal; a versão errada (ou ausente, ou um JDK sem JavaFX) quebra a app de formas difíceis de diagnosticar à distância.

```text
# Suporte recebe: "abri e não acontece nada" / "deu erro de versão"
```

**Fix:** `jpackage` **embarca o runtime exato** dentro do instalador nativo. O usuário instala um `.deb`/`.msi`/`.dmg` e roda — sem Java pré-instalado, sem versão para gerenciar.

## Em entrevista

### Frase pronta (inglês)

> "Because JavaFX was decoupled from the JDK at Java 11, its modules — `javafx.controls`, `javafx.fxml`, and so on — are external JPMS modules that have to be present at runtime, which is why running an `Application` subclass with plain `java -jar` fails with 'JavaFX runtime components are missing': the JavaFX launcher checks for those modules at boot. Locally you fix it by putting them on the module path with `--module-path` and `--add-modules`. For distribution, I don't ask users to install Java at all — I use `jlink` to build a trimmed runtime image containing only the modules the app needs, including the JavaFX ones, and then `jpackage` (the production packaging tool since Java 16, JEP 392) to produce a native installer per platform — `deb`/`rpm` on Linux, `msi`/`exe` on Windows, `dmg`/`pkg` on macOS — with that runtime embedded. `jpackage` even works with non-modular apps via `--input` and `--main-jar`, and you can feed it a pre-built runtime with `--runtime-image`."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| caminho de módulo | module path (`--module-path`) |
| adicionar módulos | add modules (`--add-modules`) |
| runtime enxuto / imagem de runtime | trimmed runtime / runtime image |
| instalador nativo | native installer |
| runtime embarcado | embedded runtime |
| classe lançadora | launcher class |
| app autocontido | self-contained app |
| módulos automáticos | automatic modules |

## Veja também

- [[01 - JavaFX — o que é e como chega ao projeto]]
- [[11 - Arquitetura — MVC, MVVM e injeção de dependência]]
- [[14 - JavaFX hoje — estado do projeto e Swing vs JavaFX]]
- [[03-Dominios/Java/JVM/08 - JPMS — o sistema de módulos|JPMS — o sistema de módulos (Galho 3)]]
- [[03-Dominios/Java/JavaFX/index|JavaFX (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#jlink|jlink (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#jpackage|jpackage (Dicionário)]]

## Referências

- [jpackage — man page (JDK 21, Oracle)](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jpackage.html) — confirmou os valores de `--type` (`app-image`, `exe`, `msi`, `rpm`, `deb`, `pkg`, `dmg`) e as flags `--input`, `--main-jar`, `--main-class`, `--module`, `--module-path`, `--add-modules`, `--icon`, `--app-version`, `--runtime-image` (e que omitir `--runtime-image` faz o jpackage rodar jlink).
- [jlink — man page (JDK 21, Oracle)](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jlink.html) — confirmou `--module-path`, `--add-modules`, `--output`, `--strip-debug`, `--no-header-files`, `--no-man-pages`, `--compress=0|1|2`.
- [JEP 392: Packaging Tool — openjdk.org](https://openjdk.org/jeps/392) — jpackage promovido de incubadora a **produção no Java 16**; formatos nativos por plataforma (msi/exe, pkg/dmg, deb/rpm); aceita app como jars ou módulos.
- [JEP 343: Packaging Tool (Incubator) — openjdk.org](https://openjdk.org/jeps/343) — jpackage como ferramenta em incubação no Java 14 (e 15), antecessor do JEP 392.
- [OpenJFX docs — openjfx.io/openjfx-docs/](https://openjfx.io/openjfx-docs/) — estrutura de projetos modular/não-modular, runtime images e o erro "JavaFX runtime components are missing".
