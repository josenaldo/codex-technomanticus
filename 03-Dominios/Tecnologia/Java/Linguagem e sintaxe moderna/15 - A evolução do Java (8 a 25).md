---
title: "A evolução do Java (8 a 25)"
created: 2026-06-02
updated: 2026-06-02
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - linguagem
  - magus
  - versoes
  - lts
aliases:
  - Evolução do Java
  - Features por versão
  - Java timeline
---

# A evolução do Java (8 a 25)

> [!abstract] TL;DR
> O Java adotou cadência de **6 meses** em 2017 (Java 9), liberando versões todo março e setembro. Versões **LTS** recebem suporte estendido: **8** (mar/2014), **11** (set/2018), **17** (set/2021), **21** (set/2023), **25** (set/2025). Features seguem o ciclo **preview → segunda preview → GA** antes de estabilizar; `--enable-preview` é obrigatório para usá-las antes da GA. A linha mestra do Java moderno: Java 8 inaugurou lambdas/Streams/Optional/Date-Time; Java 9 trouxe JPMS; Java 10 o `var`; Java 11 métodos de String; Java 14 switch expressions GA; Java 15 text blocks GA; Java 16 records e instanceof patterns GA; Java 17 sealed classes GA; Java 21 pattern matching for switch + record patterns + virtual threads — tudo GA. A **estratégia de migração canônica** para produção segue o caminho entre LTSs: 8 → 11 → 17 → 21 (→ 25 em breve).

## O que é

O Java saiu de uma linguagem verbosa e estática dos anos 2000 para uma das mais expressivas da JVM. Um senior que conhece apenas o "Java 8 clássico" está operando com uma fatia de uma linguagem que mudou radicalmente — features como records, sealed types, pattern matching e virtual threads não são adições cosméticas: elas mudam *como* se modela domínio e *como* se escreve concorrência.

Acompanhar a evolução importa por três razões diretas:

1. **Reconhecer o Java moderno** — saber que `record Point(int x, int y) {}` não é um framework externo, que `switch` com patterns e guards é GA desde Java 21, e que não é necessário um Reactor/Coroutine para concorrência massiva de I/O.
2. **Planejar migração** — entender qual versão é LTS, o que foi removido ou depreciado entre versões, e como `--enable-preview` funciona para avaliar o que vem a seguir.
3. **Falar em entrevista** — demonstrar que se acompanha o roadmap, que se distingue GA de preview, e que se entende o raciocínio por trás das features (não apenas a sintaxe).

## Por que importa

A distinção **GA vs preview** é crítica em código de produção. Uma feature preview exige `--enable-preview` em compilação e execução, e sua API/sintaxe pode mudar — ou até ser removida — antes de se tornar GA. O exemplo mais nítido: **String Templates** (`STR."..."`) foi preview no Java 21, continuou em revisão, e foi retirado para redesenho — código que dependia dela quebrou. Features GA, por outro lado, têm compatibilidade garantida para sempre para frente.

Para planejar migração, o padrão de uso em produção é:

- **Versões LTS** são a escolha óbvia para produção: suporte de 8 anos para a Oracle JDK, com suporte da comunidade OpenJDK.
- **Feature releases** (versões não-LTS) têm suporte por apenas 6 meses — até a próxima versão. Empresas raramente as usam em produção diretamente; servem para avaliar o que virá na próxima LTS.
- Reconhecer "Java moderno" significa ter como referência o Java 17 no mínimo, com Java 21 sendo o alvo natural para novos projetos em 2025/2026.

## Como funciona

### Modelo de releases (6 meses) e LTS

Desde o Java 9 (setembro de 2017), o Java segue uma **cadência time-based**: uma nova versão é lançada todo março e todo setembro, independentemente do volume de features incluídas. Se uma feature não está pronta, fica de fora. Isso substituiu o modelo anterior (Java 8 levou quase 3 anos para sair), tornando o planejamento previsível.

| Versão | Data de release | LTS? | Observação |
|--------|----------------|------|------------|
| 8  | Mar/2014 | **LTS** | Cadência antiga; ainda muito usada em projetos legados |
| 9  | Set/2017 | — | Primeiro da cadência nova; JPMS (módulos) |
| 10 | Mar/2018 | — | `var` para inferência local |
| 11 | Set/2018 | **LTS** | Primeira LTS da cadência nova; HTTP Client API |
| 12 | Mar/2019 | — | Switch expressions (preview) |
| 13 | Set/2019 | — | Switch expressions (2ª preview); Text blocks (preview) |
| 14 | Mar/2020 | — | Switch expressions **GA**; Text blocks (2ª preview); Records (preview) |
| 15 | Set/2020 | — | Text blocks **GA**; Records (2ª preview); Sealed classes (preview) |
| 16 | Mar/2021 | — | Records **GA**; instanceof pattern **GA** |
| 17 | Set/2021 | **LTS** | Sealed classes **GA**; Pattern matching for switch (preview) |
| 18 | Mar/2022 | — | Pattern matching for switch (2ª preview) |
| 19 | Set/2022 | — | Pattern matching for switch (3ª preview); Virtual threads (preview) |
| 20 | Mar/2023 | — | Pattern matching for switch (4ª preview); Virtual threads (2ª preview) |
| 21 | Set/2023 | **LTS** | Pattern matching for switch **GA**; Record patterns **GA**; Virtual threads **GA** |
| 22 | Mar/2024 | — | Unnamed variables (preview); Statements before super() |
| 23 | Set/2024 | — | Primitive types in patterns (preview) |
| 24 | Mar/2025 | — | Stream Gatherers **GA**; Scoped Values **GA** |
| 25 | Set/2025 | **LTS** | Structured Concurrency **GA**; Primitive Patterns **GA**; Module imports **GA** |

**O que LTS significa na prática:** uma versão LTS da Oracle JDK recebe atualizações de segurança e correções de bugs por 8 anos no mínimo (Premier Support). No ecossistema OpenJDK, distribuidores como Adoptium/Eclipse Temurin, Amazon Corretto, Azul Zulu e Microsoft Build of OpenJDK também garantem suporte estendido para as mesmas versões LTS. Para produção, LTS é o critério mínimo — feature releases são adequadas para desenvolvimento/avaliação, não para sistemas em operação contínua.

---

### Preview features e `--enable-preview`

O mecanismo de **preview features** permite que o Java Ship features novas em estado "candidato a GA" para que a comunidade as experimente em código real e dê feedback — antes do compromisso de estabilidade para sempre. O ciclo padrão:

```text
Preview (versão N)  →  Segunda preview (N+1)  →  GA (N+1 ou N+2)
```

Para compilar e executar código que usa uma preview feature, ambos os passos precisam da flag:

```bash
# Compilar com preview habilitado
javac --release 23 --enable-preview Foo.java

# Executar com preview habilitado
java --enable-preview Foo
```

> [!warning] Preview não é GA
> Uma preview feature pode **mudar de sintaxe**, **mudar de semântica** ou até ser **removida** entre versões. O caso de String Templates (preview no Java 21, retirado para redesenho) é o exemplo mais visível. Nunca faça deploy em produção de código que depende de `--enable-preview` sem entender claramente que a feature pode mudar na próxima versão de 6 meses. Em código de produção, use apenas features GA.

Em entrevista e em revisão de código, quando alguém menciona uma feature, vale verificar: é GA, ou ainda é preview? Qual versão e qual JEP?

---

### Timeline das features que importam

A tabela abaixo mapeia as features das outras notas deste galho às suas versões de introdução (GA) e, quando relevante, quando foi preview primeiro.

| Feature | Preview desde | GA desde | Nota do galho |
|---------|--------------|----------|---------------|
| Lambdas e interfaces funcionais | — | **Java 8** (mar/2014) | [[02 - Tipos, variáveis e operadores]] |
| Streams API | — | **Java 8** (mar/2014) | [[02 - Tipos, variáveis e operadores]] |
| Optional | — | **Java 8** (mar/2014) | [[02 - Tipos, variáveis e operadores]] |
| Date-Time API (`LocalDate`, `Instant`...) | — | **Java 8** (mar/2014) | [[02 - Tipos, variáveis e operadores]] |
| Módulos JPMS | — | **Java 9** (set/2017) | [[02 - Tipos, variáveis e operadores]] |
| `var` (inferência local) | — | **Java 10** (mar/2018) | [[02 - Tipos, variáveis e operadores]] |
| String methods (`isBlank`, `strip`, `lines`) | — | **Java 11** (set/2018) | [[04 - Strings e text blocks]] |
| Switch expressions | Java 12 | **Java 14** (mar/2020) | [[03 - Estruturas de controle e fluxo]] |
| Text blocks | Java 13 | **Java 15** (set/2020) | [[04 - Strings e text blocks]] |
| Records | Java 14 | **Java 16** (mar/2021) | [[13 - Records e record patterns]] |
| Pattern matching `instanceof` | Java 14 | **Java 16** (mar/2021) | [[14 - Sealed classes e pattern matching]] |
| Sealed classes | Java 15 | **Java 17** (set/2021) | [[14 - Sealed classes e pattern matching]] |
| Pattern matching for `switch` | Java 17 | **Java 21** (set/2023) | [[14 - Sealed classes e pattern matching]] |
| Record patterns | Java 19 | **Java 21** (set/2023) | [[13 - Records e record patterns]] |
| Virtual Threads | Java 19 | **Java 21** (set/2023) | [[Java Fundamentals]] |
| Primitive types in patterns | Java 23 | **Java 25** (set/2025) | [[14 - Sealed classes e pattern matching]] |
| Structured Concurrency | incubating Java 19 | **Java 25** (set/2025) | — |

---

### Estratégia de migração entre versões

O caminho canônico para sistemas em produção é migrar entre LTSs:

```text
Java 8  →  Java 11  →  Java 17  →  Java 21  (→ Java 25)
```

Pular versões é possível, mas cada pulo acumula breaking changes. Os pontos de atenção por trecho:

**8 → 11**
- **JPMS (módulos):** mesmo que o projeto não use módulos explicitamente, o Java 9+ encapsula internals da JDK. Reflexão ilegal (`--illegal-access`) foi depreciada no 9, restrita no 16 e removida no 17. Frameworks que usavam reflexão em internals da JDK (Hibernate, alguns Spring internals, geração de bytecode) precisam de atualização.
- **APIs removidas:** `javax.xml.bind` (JAXB), `javax.activation`, `javax.transaction` foram movidas para módulos separados e depois removidas do JDK base — precisam ser adicionadas como dependências.
- **Ferramenta:** `jdeps` analisa o projeto e aponta uso de APIs internas.

**11 → 17**
- **JEP 396 (Java 16) / JEP 403 (Java 17):** encapsulamento forte de internals. `--add-opens` pode contornar no curto prazo, mas a solução correta é atualizar as libs.
- **GC:** o G1 tornou-se o default no Java 9; no 17, ZGC e Shenandoah estão mais maduros.
- **APIs depreciadas/removidas:** Security Manager (depreciado no 17, removido no 18), Applet API (removida no 17).

**17 → 21**
- **Virtual Threads:** disponíveis, mas exigem revisão de uso de `ThreadLocal` e de pools de conexão (conexões de banco de dados usam thread pinning em versões antigas de drivers).
- **Sequenced Collections:** nova interface na hierarquia (`SequencedCollection`, `SequencedMap`); pode afetar assinaturas de método que retornam `List`/`Map`.
- **Record patterns e switch patterns:** GA — é hora de refatorar código legado de `instanceof`+cast.

**Check rápido antes de migrar:**

1. Versão mínima das dependências críticas (Spring Boot, Hibernate, etc.) compatível com o JDK alvo.
2. Build tool atualizada (Maven Compiler Plugin 3.13+, Gradle 8.x+).
3. `jdeps --jdk-internals` para detectar usos de APIs internas.
4. Testes de compatibilidade com o flag `--release N` no compilador.
5. Se usando preview features: avaliar se a feature foi GA ou mudou na versão alvo.

## Na prática

Checklist de migração de versão — o que verificar antes de mudar o JDK do projeto:

**Antes de iniciar**
- [ ] Identificar a versão de destino (preferencialmente uma LTS: 17, 21, 25)
- [ ] Verificar as release notes e JEPs da versão alvo
- [ ] Consultar a matriz de compatibilidade das libs críticas (Spring, Hibernate, Quarkus, Micronaut)

**Build e dependências**
- [ ] Atualizar `pom.xml` / `build.gradle`: `<java.version>21</java.version>` e `sourceCompatibility`/`targetCompatibility`
- [ ] Atualizar Maven Compiler Plugin (≥ 3.13) ou Gradle (≥ 8.x)
- [ ] Verificar dependências que usam internals da JDK: rodar `jdeps --jdk-internals --multi-release 21 app.jar`
- [ ] Verificar se há dependências com versões depreciadas ou removidas (ex.: JAXB standalone se 8→11+)

**Reflexão e encapsulamento (principalmente 8→11+ e 11→17)**
- [ ] Identificar `--add-opens` e `--add-exports` temporários no projeto — são sinais de libs que precisam de update
- [ ] Atualizar as libs responsáveis por esses acessos para versões compatíveis

**APIs removidas**
- [ ] `SecurityManager` (removido no 18) — substituir por alternativa da aplicação
- [ ] `Applet` API — não aplicável para novos projetos
- [ ] `finalize()` (depreciado para remoção) — revisar overrides

**Preview features (se aplicável)**
- [ ] Identificar qualquer uso de `--enable-preview` no projeto
- [ ] Verificar se a feature virou GA na versão alvo ou mudou de sintaxe
- [ ] Remover a flag `--enable-preview` se a feature virou GA; atualizar sintaxe se mudou

**Após a atualização**
- [ ] Executar suite completa de testes
- [ ] Verificar métricas de GC (o GC default pode ter mudado)
- [ ] Em migração para Java 21: avaliar se Virtual Threads são aplicáveis nos thread pools I/O-bound

## Armadilhas

### (1) Usar preview feature em produção sem entender o risco de mudança

**O problema:** uma preview feature exige `--enable-preview` em compilação e execução. Ela não tem garantia de estabilidade — pode mudar de sintaxe, mudar de semântica ou ser removida inteiramente antes de virar GA. O caso concreto mais impactante: **String Templates** (`STR."Hello \{name}"`) foi preview no Java 21 e continuou em revisão no Java 22 e Java 23, sendo **retirada do Java 23** para redesenho completo. Todo código que a usava em produção precisou ser reescrito.

```java
// ❌ Dependia de String Templates — preview Java 21/22, removida no Java 23
// Compilava com: javac --release 22 --enable-preview Foo.java
String msg = STR."Olá, \{name}! Você tem \{count} mensagens.";

// ✅ Alternativa GA (disponível em qualquer versão Java 8+)
String msg = "Olá, %s! Você tem %d mensagens.".formatted(name, count);
// Ou (Java 15+, GA)
String msg = """
        Olá, %s! Você tem %d mensagens.""".formatted(name, count);
```

**Fix:** use preview features apenas em ambientes de desenvolvimento/experimentação. Em produção, apenas features GA. Se precisar avaliar uma preview, isole em um branch/módulo separado e documente explicitamente o status e a versão do JDK. Antes de um release, verifique se a feature virou GA ou mudou entre as versões.

---

### (2) Confundir feature release com LTS no planejamento de produção

**O problema:** a cadência de 6 meses cria a ilusão de que todas as versões são equivalentes para produção. Versões não-LTS recebem suporte por apenas **6 meses** — até o próximo release. Usar Java 22 ou Java 23 em produção significa que, em 6 meses, a versão não terá mais patches de segurança. Equipes que não monitoram isso ficam presas em versões sem suporte, ou forçadas a atualizações urgentes a cada 6 meses — exatamente o problema que a cadência LTS foi criada para resolver.

```text
Situação real problemática:

  Projeto vai para produção com Java 22 (março/2024)
  Java 23 sai setembro/2024 → Java 22 perde suporte em setembro/2024
  Java 24 sai março/2025   → Java 23 perde suporte em março/2025
  
  Seis meses após o deploy, o projeto está em versão sem suporte de segurança.
  Para corrigir: migrar para Java 21 LTS (já disponível desde set/2023)
               ou esperar Java 25 LTS (set/2025)
```

**Fix:** para sistemas em produção, use **exclusivamente versões LTS**. A estratégia de "usar a última feature release para ter as features mais novas" é adequada em desenvolvimento/experimentação, não em produção. O planejamento correto:

- Produção: Java 17 LTS (set/2021) → Java 21 LTS (set/2023) → Java 25 LTS (set/2025)
- Desenvolvimento/avaliação: pode usar feature releases para explorar o que virá na próxima LTS
- Regra de bolso: se um release não aparece como "LTS" na matriz do fornecedor da JDK, não vai para produção sem plano explícito de upgrade semestral

### Cheatsheet

Resumo compacto das features do galho mapeadas por versão GA e status de preview:

| Feature | Preview desde | GA desde | Foi preview? |
|---------|--------------|----------|:---:|
| Lambdas, Streams, Optional, Date-Time | — | Java 8 | Não |
| JPMS (módulos) | — | Java 9 | Não |
| `var` (inferência de tipo local) | — | Java 10 | Não |
| `String.isBlank()`, `.strip()`, `.lines()` | — | Java 11 | Não |
| Switch expressions | Java 12 | Java 14 | Sim (2 previews) |
| Text blocks | Java 13 | Java 15 | Sim (2 previews) |
| Records | Java 14 | Java 16 | Sim (2 previews) |
| `instanceof` pattern (binding variable) | Java 14 | Java 16 | Sim (2 previews) |
| Sealed classes | Java 15 | Java 17 | Sim (2 previews) |
| Pattern matching for `switch` | Java 17 | Java 21 | Sim (4 previews) |
| Record patterns | Java 19 | Java 21 | Sim (2 previews) |
| Virtual Threads | Java 19 | Java 21 | Sim (2 previews) |
| Sequenced Collections | — | Java 21 | Não |
| Stream Gatherers | Java 22 | Java 24 | Sim |
| Scoped Values | Java 20 | Java 24 | Sim |
| Primitive types in patterns | Java 23 | Java 25 | Sim |
| Structured Concurrency | incubating Java 19 | Java 25 | Sim |
| Module import declarations | Java 23 | Java 25 | Sim |

## Em entrevista

### Frase pronta (inglês)

> "Java moved to a 6-month release cadence in 2017 starting with Java 9, with LTS versions — 11, 17, 21, and 25 — being the only ones I'd target for production, since non-LTS releases lose support after just six months, which makes them impractical for anything beyond evaluation. The deliberate decision when adopting a new Java version is always to check whether the features I care about are GA or still behind `--enable-preview`, because preview features are explicitly unstable — String Templates were previewed in Java 21 and then pulled entirely for a redesign, which is the most concrete proof of that risk. The standard migration path I follow is LTS-to-LTS — 8 to 11, then 17, then 21 — and the key friction points at each hop are strong encapsulation of JDK internals, removed APIs like JAXB or the Security Manager, and ensuring that third-party libs are compatible before bumping the `--release` flag."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| cadência de releases | release cadence |
| suporte de longo prazo | long-term support (LTS) |
| versão de feature | feature release |
| feature em preview | preview feature |
| disponibilidade geral | general availability (GA) |
| encapsulamento de internals | strong encapsulation of JDK internals |
| migração de versão | version migration / upgrade path |
| caminho de migração | migration path |
| modularização | modularization / JPMS |
| thread virtual | virtual thread |

## Veja também

- [[01 - O modelo da linguagem Java]]
- [[03 - Estruturas de controle e fluxo]]
- [[13 - Records e record patterns]]
- [[14 - Sealed classes e pattern matching]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Fundamentals]]

## Referências

- [Java Platform Evolution — dev.java](https://dev.java/evolution/) — visão geral oficial da evolução da linguagem
- [Java Version History — Wikipedia](https://en.wikipedia.org/wiki/Java_version_history) — datas e features por versão
- [OpenJDK JEP Index](https://openjdk.org/jeps/0) — todas as JEPs por número
- [Oracle Java SE Release Notes](https://www.oracle.com/java/technologies/javase/jdk-relnotes-index.html) — notas de release oficiais
- [Java Language Updates — Oracle Docs](https://docs.oracle.com/en/java/javase/21/language/index.html) — guia de linguagem Java 21
