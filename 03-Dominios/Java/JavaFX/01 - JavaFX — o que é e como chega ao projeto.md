---
title: "JavaFX — o que é e como chega ao projeto"
created: 2026-06-06
updated: 2026-06-06
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - javafx
  - iniciado
  - openjfx
aliases:
  - "JavaFX"
  - "OpenJFX"
  - "Primeira aplicação JavaFX"
---

# JavaFX — o que é e como chega ao projeto

> [!abstract] TL;DR
> JavaFX é o toolkit de UI desktop moderno do ecossistema Java: scene graph declarativo, FXML, data binding e CSS. **Não vem no JDK** — foi desacoplado no Java 11 e vive hoje no projeto **OpenJFX**, com stewardship de Gluon e da comunidade. Chega ao projeto via Maven (`org.openjfx:javafx-controls`) ou Gradle. **Swing não foi substituído** — continua como parte do core Java SE e ambos coexistem. Entender o setup atual é o que a entrevista cobra; a tabela mental de 2014 (JavaFX = bundled no JDK) já não vale.

## O que é

JavaFX é um toolkit de interface gráfica desktop para Java, baseado em **scene graph** — uma árvore de nós que representa a hierarquia visual da janela. Oferece suporte a FXML (layouts declarativos em XML), data binding bidirecional, animações e estilização via CSS.

### Linha do tempo honesta

| Período | O que aconteceu |
|---------|-----------------|
| 2011 | JavaFX 2.0 lançado pela Oracle — substitui o JavaFX Script, API Java pura |
| JDK 8 (2014) | JavaFX bundled no JDK da Oracle — era possível importar sem dependência externa |
| Java 11 (2018) | JavaFX **desacoplado** do JDK → projeto **OpenJFX** no OpenJDK; passa a ser dependência externa |
| Hoje | OpenJFX 26 (versão atual confirmada em openjfx.io) — ciclo de release alinhado ao JDK (6 meses) |

> Na era do JDK 8, `import javafx.*` funcionava sem adicionar nenhuma dependência ao pom.xml porque o runtime era parte da instalação da Oracle JDK. Esse comportamento não existe em nenhum JDK atual.

### JavaFX não substituiu o Swing

O framing de "JavaFX é o substituto do Swing" é impreciso. Swing permanece parte do **core Java SE** — presente em qualquer JDK, sem dependência externa, sem plano de remoção. JavaFX é uma biblioteca independente, com modelo diferente (scene graph vs. componentes AWT). Os dois coexistem. Para o estado atual do Swing: [[03-Dominios/Java/Swing/12 - Swing hoje - estado atual|Swing hoje]].

## Por que importa

O setup do projeto é a **primeira pegadinha** do galho. Dev que abriu um tutorial de 2013 no YouTube vai tentar `import javafx.scene.Scene` e tomar um erro de compilação — porque no JDK atual essa dependência não existe até você declará-la explicitamente.

Em entrevista de sênior, a pergunta não é "o que JavaFX faz" — é "como você sabe onde JavaFX vive e como chega ao build?". Demonstrar que conhece a separação JDK/OpenJFX e o mecanismo de distribuição (Maven Central, SDK standalone, jmods) é o que diferencia resposta de sênior de resposta de pleno.

## Como funciona

### De onde vem — OpenJFX, cadência e papel da Gluon

O **OpenJFX** é o projeto que desenvolve e mantém JavaFX como software livre (GPL + Classpath Exception, igual ao OpenJDK). Gluon é a empresa que lidera o desenvolvimento e fornece distribuições e suporte comercial; a comunidade contribui com patches e validação.

O ciclo de releases segue a cadência do JDK — uma release a cada 6 meses. A versão atual é **JavaFX 26** (confirmada em openjfx.io). O número de versão espelha o JDK correspondente: JavaFX 21 = LTS alinhado ao JDK 21, JavaFX 24 = alinhado ao JDK 24, e assim por diante.

O runtime está disponível em três formas:
- **Maven Central** — artifacts por módulo (forma recomendada para projetos Maven/Gradle)
- **SDK standalone** — download em openjfx.io, útil para experimentos fora de build tool
- **jmods** — para uso com `jlink` (empacotamento customizado — ver [[13 - Empacotamento — módulos, jlink e jpackage]])

O papel da Gluon no ecossistema mais amplo (GraalVM native image para JavaFX, suporte mobile) é tema da [[14 - JavaFX hoje — estado do projeto e Swing vs JavaFX]].

### Como chega ao projeto — Maven/Gradle

A dependência principal é `org.openjfx:javafx-controls`. Projetos reais frequentemente adicionam `javafx-fxml` (para layouts FXML) e outros módulos conforme a necessidade.

**Coordenadas Maven:**

```xml
<dependency>
    <groupId>org.openjfx</groupId>
    <artifactId>javafx-controls</artifactId>
    <version>21</version>
</dependency>
```

Para rodar sem configurar manualmente o module-path, usa-se o **javafx-maven-plugin**:

```xml
<plugin>
    <groupId>org.openjfx</groupId>
    <artifactId>javafx-maven-plugin</artifactId>
    <version>0.0.8</version>
    <configuration>
        <mainClass>hellofx.HelloFX</mainClass>
    </configuration>
</plugin>
```

O plugin cuida de montar o `--module-path` e `--add-modules` corretos na invocação da JVM — detalhe que, se feito na mão, é a segunda fonte mais comum de erro.

**Rodar:**

```bash
mvn javafx:run
```

> Para Gradle, o equivalente é `org.openjfx.javafxplugin` com a extensão `javafx { modules = ["javafx.controls"] }`.

### O lifecycle de Application

Toda aplicação JavaFX estende `javafx.application.Application`. O framework gerencia o ciclo de vida:

```text
main() chama Application.launch()
        │
        ▼
  init()         ← opcional; roda na thread principal (NÃO na JavaFX thread)
        │
        ▼
  start(Stage)   ← obrigatório; roda na JavaFX Application Thread
        │         Aqui você monta a cena e exibe o Stage
        ▼
  [aplicação rodando — event loop do JavaFX]
        │
        ▼
  stop()         ← opcional; chamado ao fechar a janela ou Platform.exit()
```

O ponto crítico: `start(Stage)` é o único método que roda **na JavaFX Application Thread** com garantia desde o início. Atualizar a UI fora dessa thread (ou sem `Platform.runLater()`) causa `IllegalStateException` — armadilha comum em integração com CompletableFuture.

### Stage e Scene — janela e conteúdo

- **Stage** — é a janela. O `primaryStage` é fornecido pelo framework no `start(Stage)`. É possível criar Stages adicionais para janelas secundárias (diálogos customizados, painéis flutuantes).
- **Scene** — é o conteúdo da janela; carrega a raiz do scene graph e define dimensões. Um Stage exibe uma Scene por vez.

O scene graph em si — nós, layouts, controles — é o tema de [[02 - Scene graph — stage, scene e nodes]].

## Na prática

### HelloFX completo

```java
package hellofx;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

public class HelloFX extends Application {

    @Override
    public void start(Stage stage) {
        String javaVersion   = System.getProperty("java.version");
        String javafxVersion = System.getProperty("javafx.version");

        Label label = new Label(
            "Hello, JavaFX " + javafxVersion + " — rodando em Java " + javaVersion
        );

        Scene scene = new Scene(new StackPane(label), 640, 480);
        stage.setTitle("HelloFX");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();          // delega ao framework; NÃO instancie HelloFX manualmente
    }
}
```

### pom.xml mínimo

```xml
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.example</groupId>
    <artifactId>hellofx</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <javafx.version>21</javafx.version>
        <maven.compiler.release>21</maven.compiler.release>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.openjfx</groupId>
            <artifactId>javafx-controls</artifactId>
            <version>${javafx.version}</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.openjfx</groupId>
                <artifactId>javafx-maven-plugin</artifactId>
                <version>0.0.8</version>
                <configuration>
                    <mainClass>hellofx.HelloFX</mainClass>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### Rodar

```bash
mvn javafx:run
```

> Se rodar com `java -jar hellofx.jar` ou `java hellofx.HelloFX` sem configurar o module-path, o erro será:
>
> ```text
> Error: JavaFX runtime components are missing, and are required to run this application
> ```
>
> Esse é exatamente o tema de [[13 - Empacotamento — módulos, jlink e jpackage]] — aqui não resolvemos, apenas reconhecemos a armadilha.

## Armadilhas

### (1) Achar que JavaFX vem no JDK

**O problema:** em qualquer JDK 11+ (Temurin, Corretto, Oracle JDK) o pacote `javafx.*` não existe no classpath por padrão. O compilador vai reclamar de cada import.

```text
error: package javafx.application does not exist
import javafx.application.Application;
```

**Fix:** declarar as dependências `org.openjfx:javafx-controls` (e outros módulos necessários) no `pom.xml` ou `build.gradle`.

---

### (2) Rodar `java HelloFX` direto e tomar o erro de runtime

**O problema:** mesmo depois de compilar com as dependências no classpath, invocar a classe diretamente sem o module-path configurado causa:

```text
Error: JavaFX runtime components are missing, and are required to run this application
```

**Fix:** usar `mvn javafx:run` (o plugin monta o module-path automaticamente) ou configurar `--module-path` e `--add-modules javafx.controls` manualmente. Empacotamento correto para distribuição: ver [[13 - Empacotamento — módulos, jlink e jpackage]].

---

### (3) Seguir tutorial da era JDK 8 (`jfxrt.jar`, sem dependência externa)

**O problema:** tutoriais anteriores a 2018 mostram JavaFX funcionando sem nenhuma dependência declarada — porque na época o `jfxrt.jar` era parte da Oracle JDK 8. Esse arquivo não existe em JDKs modernos.

```text
# Sinal de alerta no tutorial: menciona jfxrt.jar ou "não precisa de dependência"
# Sinal de alerta no pom.xml: <scope>system</scope> com path para jfxrt.jar
```

**Fix:** jogar fora o tutorial e seguir os docs atuais de openjfx.io. A versão mínima suportada hoje é JavaFX 11.

## Em entrevista

### Frase pronta (inglês)

> "JavaFX is the modern desktop UI toolkit for Java — it's built around a scene graph model, supports FXML for declarative layouts, data binding, and CSS styling. The key architectural fact is that it's no longer part of the JDK: it was decoupled at Java 11 and is now the OpenJFX project, led by Gluon and the open-source community. You pull it in as a Maven or Gradle dependency — `org.openjfx:javafx-controls` — and the official Maven plugin handles the module-path wiring so you don't have to configure it manually. The trade-off versus Swing is that JavaFX gives you a richer, more modern programming model with scene graph, animation, and CSS, but it's an external dependency with its own release cadence, which means you need to manage the version explicitly and think about packaging — especially if you need a self-contained executable, where you'd use jlink or jpackage. The caveat is that Swing was not replaced: it's still part of core Java SE with no removal plan, so the choice between them is architectural, not forced."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| gráfico de cena | scene graph |
| palco / janela | Stage |
| cena / conteúdo | Scene |
| nó (elemento visual) | Node |
| ciclo de vida da aplicação | Application lifecycle |
| desacoplado do JDK | unbundled / decoupled from JDK |
| dependência externa | external dependency |
| caminho de módulo | module path (`--module-path`) |

## Veja também

- [[02 - Scene graph — stage, scene e nodes]]
- [[13 - Empacotamento — módulos, jlink e jpackage]]
- [[14 - JavaFX hoje — estado do projeto e Swing vs JavaFX]]
- [[03-Dominios/Java/Swing/12 - Swing hoje - estado atual|Swing hoje (Galho 5)]]
- [[03-Dominios/Java/JavaFX/index|JavaFX (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#OpenJFX|OpenJFX (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#Stage / Scene|Stage / Scene (Dicionário)]]

## Referências

- [OpenJFX — openjfx.io](https://openjfx.io/) — confirmou JavaFX 26 como versão atual e o desacoplamento no Java 11
- [OpenJFX Getting Started Docs — openjfx.io/openjfx-docs/](https://openjfx.io/openjfx-docs/) — estrutura de seções Maven/Gradle modular e não-modular
- [openjfx/samples — HelloFX não-modular com Maven (GitHub)](https://github.com/openjfx/samples/blob/master/CommandLine/Non-modular/Maven/hellofx/) — coordenadas `org.openjfx:javafx-controls:21`, plugin `0.0.8`
- [javafx-maven-plugin — GitHub (openjfx)](https://github.com/openjfx/javafx-maven-plugin) — groupId `org.openjfx`, artifactId `javafx-maven-plugin`, versão `0.0.8`
- [JavaFX 24 Javadoc — openjfx.io/javadoc/24/](https://openjfx.io/javadoc/24/) — confirmou numeração de release
- [JavaFX 26 Javadoc — openjfx.io/javadoc/26/](https://openjfx.io/javadoc/26/) — confirmou JavaFX 26 como release existente
