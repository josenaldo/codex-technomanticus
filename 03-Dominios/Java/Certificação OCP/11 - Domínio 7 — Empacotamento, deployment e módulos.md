---
title: "Domínio 7 — Empacotamento, deployment e módulos"
created: 2026-06-13
updated: 2026-06-13
type: concept
status: seedling
publish: true
fase: dominios
tags:
  - java
  - certificacao-ocp
  - dominios
aliases:
  - "Domínio 7 OCP"
  - "Empacotamento e módulos na OCP"
---

# Domínio 7 — Empacotamento, deployment e módulos

> [!abstract] TL;DR
> Este é um domínio de **cobertura parcial** na trilha: o sistema de módulos (JPMS) e as ferramentas `jlink`/`jpackage` já têm notas dedicadas nos galhos de JVM e JavaFX, mas três tópicos da prova — `jar`/MANIFEST, JShell e implicit classes/instance main — ainda não têm casa própria (veja a seção [[#Lacuna da trilha]]).
> Atenção redobrada com **JPMS**: é pouco usado em produção real (Spring e Jakarta EE não dependem dele agressivamente), mas **cai muito** na prova. Estude mesmo que você nunca vá escrever um `module-info.java` no trabalho.

> [!info] Títulos oficiais
> - **1Z0-830 (Java 21):** *Packaging and Deploying Java Code*
> - **1Z0-831 (Java 25):** *Packaging and Deploying Java Code*
>
> Os títulos são idênticos entre as duas versões da prova. O que muda é o estado de maturidade de recursos como implicit classes / instance main methods, que evoluíram de *preview* (Java 21) até estabilizar nas versões mais novas.

## O que a Oracle cobra

O domínio mistura o **sistema de módulos** com as **ferramentas de empacotamento e execução** da plataforma. Em linhas gerais:

- **JPMS — `module-info.java`** — diretivas `requires`, `exports`, `opens`, `uses`, `provides`.
- **Tipos de módulo** — *named module* (com `module-info`), *unnamed module* (classpath, sem `module-info`), *automatic module* (jar no modulepath sem `module-info`).
- **ServiceLoader** — `ServiceLoader.load()`, casado com `uses`/`provides` para descoberta de implementações em runtime.
- **jlink** — geração de runtime customizado (imagem só com os módulos necessários).
- **Migração** — passar uma aplicação de **classpath** para **modulepath**.
- **`jar` e META-INF/MANIFEST.MF** — empacotar classes em um jar, marcar `Main-Class:`, gerar jar executável.
- **`jpackage`** — instalador nativo da plataforma (Java 14+): `.deb`, `.msi`, `.dmg`, etc.
- **`javac` / `java`** — compilação e execução, com a distinção entre **classpath** (`-cp`) e **modulepath** (`-p` / `--module-path`).
- **JShell** (Java 9+) — REPL oficial da plataforma.
- **Implicit classes e instance main methods** — *preview* no Java 21, evoluindo até virar recurso final nas versões seguintes: permitem escrever scripts Java sem o boilerplate de `public static void main(String[])` e sem declaração explícita de classe.

## Mapa de revisão

A trilha cobre o coração deste domínio em três notas. Revise estas antes da prova:

- [[03-Dominios/Java/JVM/08 - JPMS — o sistema de módulos|JPMS — o sistema de módulos (G3)]] — todo o sistema de módulos: diretivas, tipos de módulo, ServiceLoader, migração.
- [[03-Dominios/Java/JavaFX/13 - Empacotamento — módulos, jlink e jpackage|Empacotamento — jlink e jpackage (G6)]] — jlink e jpackage na prática, com um app modular real.
- [[03-Dominios/Java/Linguagem e sintaxe moderna/15 - A evolução do Java (8 a 25)|A evolução do Java (G1)]] — contexto histórico de implicit classes e instance main methods (de preview a final).

## Pegadinhas deste domínio

Snippets curtos que a Oracle adora transformar em pegadinha:

1. **`exports` vs `opens`** — `exports pacote;` libera acesso ao pacote em **tempo de compilação** (a API pública do módulo). `opens pacote;` libera **reflexão em runtime** (frameworks como Spring/Hibernate que vasculham campos privados). São coisas distintas: um módulo pode `opens` sem `exports` e vice-versa.

   ```java
   module com.app {
       exports com.app.api;        // API pública, compile-time
       opens com.app.model;        // reflexão em runtime (JPA, Jackson...)
   }
   ```

2. **Automatic module deriva o nome do jar** — um jar sem `module-info` colocado no *modulepath* vira *automatic module*, e seu nome é **derivado do nome do arquivo jar** (ex.: `commons-lang3-3.12.jar` → `commons.lang3`). Isso é **frágil**: renomear o jar muda o nome do módulo e quebra os `requires` de quem depende dele.

3. **`requires transitive` repassa a dependência** — se o módulo A faz `requires transitive B`, então qualquer módulo que faça `requires A` **também enxerga** B automaticamente, sem precisar declarar `requires B`. Sem o `transitive`, B fica visível só dentro de A.

4. **Sem `module-info`, tudo cai no unnamed module** — código no **classpath** (não no modulepath) vive no *unnamed module*, que lê todos os outros módulos e exporta tudo. É o modo de compatibilidade pré-Java 9.

Mais armadilhas no [[03-Dominios/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas|catálogo de pegadinhas]].

## Lacuna da trilha

> [!warning] Seam de honestidade — cobertura parcial
> A trilha cobre **JPMS** (galho 3) e **jlink/jpackage** (galho 6) com profundidade, mas **não tem nota dedicada** a três tópicos que a prova cobra: `jar`/MANIFEST, JShell e implicit classes/instance main. Segue o conteúdo autocontido mínimo de cada um para você não chegar cru na prova. **Estude estes à parte** (livro Sybex da OCP / docs oficiais), pois aqui é só o esqueleto.

### 1. `jar` e MANIFEST.MF

A ferramenta `jar` empacota classes compiladas (e recursos) em um único arquivo `.jar` (que é, na prática, um zip com metadados em `META-INF/`).

```bash
# criar um jar executável apontando a classe main
jar --create --file app.jar --main-class com.app.Main -C build/classes .

# inspecionar o conteúdo
jar --list --file app.jar

# extrair
jar --extract --file app.jar
```

O arquivo **`META-INF/MANIFEST.MF`** carrega metadados do jar. A entrada-chave para a prova é:

```
Main-Class: com.app.Main
```

Quando o `Main-Class:` está presente, o jar é **executável** e roda com `java -jar app.jar` (sem precisar nomear a classe na linha de comando). A flag `--main-class` do `jar` grava essa entrada no manifesto automaticamente. Sem ela, `java -jar` falha com "no main manifest attribute".

### 2. JShell

REPL oficial da plataforma, disponível desde o **Java 9**. Você digita expressões e declarações e elas são avaliadas na hora — ótimo para **testar hipóteses de output** (justamente o tipo de coisa que a prova pergunta: "qual o resultado deste trecho?").

```text
$ jshell
jshell> int x = 2 + 3
x ==> 5
jshell> System.out.println("oi".repeat(3))
oioioi
```

Comandos básicos (começam com `/`):

- `/vars` — lista as variáveis declaradas na sessão.
- `/methods` — lista os métodos declarados.
- `/imports` — mostra os imports ativos (vários já vêm carregados por padrão).
- `/exit` — encerra a sessão.

### 3. Implicit classes e instance main methods

Desde o **Java 21** (como *preview*) e evoluindo até estabilizar nas versões seguintes, a plataforma permite escrever programas sem o boilerplate clássico. Dois ingredientes:

- **Instance main method** — o `main` pode ser **de instância** (sem `static`), e até sem o parâmetro `String[] args`.
- **Implicit class** — um arquivo `.java` **sem declaração de classe explícita**: o compilador embrulha tudo numa classe implícita.

O "Hello World" mínimo passa a ser:

```java
void main() {
    System.out.println("Olá!");
}
```

Não há `public class`, não há `static`, não há `String[] args`. Isso baixa drasticamente a barreira para scripts Java de aprendizado e protótipos. Na prova, o objetivo é **reconhecer a sintaxe** e saber que ela é válida nas versões em que está habilitada — não decorar a versão exata em que virou final.

> [!tip] Não pare por aqui
> Esses três tópicos merecem estudo à parte no **livro Sybex da OCP** (capítulo de módulos e ferramentas) e na **documentação oficial** das ferramentas (`jar`, `jshell`, `jpackage`). Esta seção é só uma rede de segurança, não a cobertura completa.

## Em entrevista

Uma frase que demonstra entendimento conceitual de módulos, sem reivindicar credencial:

> "In JPMS, `exports` exposes a package as part of the module's public API at compile time, while `opens` allows deep reflective access at runtime — that's what frameworks like Spring need to inspect private fields."

**Vocabulário PT | EN:**

| Português | English |
| --- | --- |
| módulo | module |
| exporta | exports |
| abre (reflexão) | opens |

## Veja também

- [[03-Dominios/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|O mapa objetivo → galho]]
- [[03-Dominios/Java/Certificação OCP/12 - Domínio 8 — Concorrência|Domínio 8 — Concorrência]]
- [[03-Dominios/Java/Certificação OCP/index|Certificação OCP (MOC do galho)]]

## Referências

- JPMS / ferramentas — docs oficiais (manual do `javac`): https://docs.oracle.com/en/java/javase/21/docs/specs/man/javac.html
- Enthuware — syllabus da OCP Java 21: https://enthuware.com/oca-ocp-java-certification-resources/290-ocp-java-21-exam-syllabus
