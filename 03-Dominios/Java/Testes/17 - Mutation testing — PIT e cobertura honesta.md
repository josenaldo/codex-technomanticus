---
title: "Mutation testing — PIT e cobertura honesta"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - testes
  - magus
  - pit
aliases:
  - "mutation testing"
  - "PIT"
  - "Pitest"
---

# Mutation testing — PIT e cobertura honesta

> [!abstract] TL;DR
> **Line coverage** mede só "o código executou" — não "o teste pega bug". É possível ter 100% de cobertura de linha com zero asserções que validem o resultado. **Mutation testing** (via **PIT/Pitest**) ataca esse ponto cego: muta o *bytecode* (troca `>` por `>=`, remove um `return`, nega uma condição) e roda a suíte contra cada mutante. Se nenhum teste falha, o mutante **sobrevive** e revela um teste fraco; se um teste falha, o mutante é **morto** e o teste provou que pega aquela regressão. **Mutation coverage** é a métrica honesta — mas é cara, então roda no nightly, não em cada commit.

## O que é

Mutation testing é uma técnica que mede a **qualidade dos testes**, não a quantidade de código executado. A ideia: introduzir pequenos defeitos artificiais ("mutações") no código de produção e verificar se a suíte de testes os detecta. Cada defeito é um **mutante** — uma cópia do programa com uma alteração mínima e plausível.

**PIT** (também chamado **Pitest**) é o sistema de mutation testing de referência no ecossistema JVM. A documentação oficial o descreve como "state of the art mutation testing system, providing gold standard test coverage for Java and the jvm". Diferente das ferramentas acadêmicas antigas (que levavam horas ou dias), PIT é rápido o suficiente para uso real: opera direto sobre o **bytecode** compilado, não sobre o código-fonte.

O fluxo, segundo a própria documentação, tem três passos:

1. **Mutação** — defeitos são semeados automaticamente no código.
2. **Execução** — os testes rodam contra cada versão mutada.
3. **Avaliação** — se algum teste falha, o mutante foi *killed* (bom); se todos passam, o mutante *lived* (sobreviveu — sinal de teste fraco).

A métrica final, **mutation coverage**, é o percentual de mutantes mortos.

## Por que importa

Em fase magus, a pergunta não é "meus testes existem?", mas "meus testes **valem alguma coisa?**". Times de verdade caem numa armadilha silenciosa: perseguem uma meta de line coverage (80%, 90%, 100%) e, no esforço de bater o número, escrevem testes que **executam** o código sem **verificar** nada. O resultado é uma suíte verde e falsa — passa sempre, inclusive quando o código quebra.

Mutation testing fecha esse buraco porque, como diz a documentação oficial, "is actually able to detect whether each statement is meaningfully tested". Um mutante sobrevivente é a prova material de que existe uma regressão que sua suíte deixaria passar despercebida. Em entrevista senior, demonstrar que você entende a diferença entre *executar* e *verificar* linha — e que conhece a ferramenta que mede isso — separa quem decora "coverage" de quem entende garantia de qualidade.

## Como funciona

### Line coverage mente (100% sem asserção é inútil)

Cobertura de linha (e de branch) instrumenta o código e marca cada linha que foi tocada durante a execução dos testes. O problema é o que ela **não** mede: se o resultado daquela linha foi efetivamente comparado contra um valor esperado.

```java
// Código de produção
int desconto(int valor) {
    if (valor > 100) {
        return valor / 10;
    }
    return 0;
}

// Teste com 100% de line coverage e ZERO valor
@Test
void executaDesconto() {
    desconto(150);  // toca todas as linhas... e não verifica NADA
    desconto(50);
}
```

Esse teste reporta 100% de cobertura de linha. Mas se alguém trocar `valor / 10` por `valor / 5`, ou `> 100` por `>= 100`, o teste continua verde. A linha foi *executada*, nunca foi *testada*. Line coverage é um **limite superior**: mede o máximo que seus testes *poderiam* pegar, não o que realmente pegam.

### Mutation testing: PIT muta o bytecode e mede se os testes pegam

PIT opera depois do `test-compile`, direto sobre os `.class`. Para cada ponto mutável, ele gera uma variante do bytecode e roda os testes que cobrem aquela linha. Os **mutadores** (mutation operators) aplicam transformações pequenas e realistas — o tipo de erro que um humano cometeria:

- **Conditionals Boundary** — troca `<` por `<=`, `>` por `>=` (erros de off-by-one).
- **Negate Conditionals** — inverte `==` para `!=`, `>` para `<=`.
- **Math** — troca `+` por `-`, `*` por `/`.
- **Increments** — troca `i++` por `i--`.
- **Void Method Calls / Return Values** — remove uma chamada de método ou altera o valor retornado (ex: troca `return x` por `return 0`).

Rodar todos os mutantes contra a suíte inteira seria proibitivo, então PIT usa cobertura de linha para selecionar **apenas os testes que tocam a linha mutada**. Por isso é "fast (minutes vs. days)" — minutos contra os dias das ferramentas acadêmicas antigas.

### Mutante sobrevivente = teste fraco; mutante morto = teste bom

Esse é o coração da técnica, e a terminologia importa em entrevista:

- **Killed (morto)** — pelo menos um teste **falhou** quando o mutante foi injetado. Ótimo: o teste detectou o defeito artificial, logo detectaria a regressão real equivalente.
- **Survived / Lived (sobreviveu)** — **nenhum** teste falhou apesar da mutação. Péssimo: existe um defeito plausível que sua suíte não pega. É exatamente a classe de bug que escaparia em produção.
- **No coverage** — nenhum teste sequer executou aquela linha (problema anterior, de line coverage).

A **mutation coverage** é `mutantes mortos / mutantes totais`. Diferente da line coverage, ela só sobe quando você escreve uma **asserção** que efetivamente verifica o comportamento — porque é a asserção que faz o teste *falhar* diante do mutante. É a cobertura honesta.

### Custo: rodar no nightly, não em cada build

PIT é rápido *para mutation testing*, mas ainda é ordens de magnitude mais lento que rodar a suíte uma vez: ele recompila/reroda a suíte parcial para cada mutante, e um módulo médio gera centenas ou milhares de mutantes. Colocar PIT no caminho crítico de cada `push` ou cada PR mata a produtividade do time.

A prática estabelecida: rodar PIT em um **job agendado** (nightly, ou semanal num CI agendado), tratando a mutation coverage como uma métrica de saúde da suíte que se observa ao longo do tempo — não como gate de cada commit. O build rápido roda testes + line coverage; o nightly roda PIT e reporta os sobreviventes.

## Na prática

Plugin no `pom.xml`, com o engine de JUnit 5 declarado **dentro** do bloco do plugin (não no classpath do projeto):

```xml
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <version>1.18.2</version>
  <dependencies>
    <dependency>
      <groupId>org.pitest</groupId>
      <artifactId>pitest-junit5-plugin</artifactId>
      <version>1.2.2</version>
    </dependency>
  </dependencies>
  <configuration>
    <targetClasses>
      <param>com.exemplo.dominio.*</param>
    </targetClasses>
    <targetTests>
      <param>com.exemplo.dominio.*</param>
    </targetTests>
  </configuration>
</plugin>
```

Rodando a análise de mutação manualmente (ou no job do nightly):

```bash
mvn test-compile org.pitest:pitest-maven:mutationCoverage
```

O relatório HTML sai em `target/pit-reports/<timestamp>/`, com cada mutante marcado como killed, survived ou no-coverage.

Exemplo concreto de um mutante e por que um teste fraco não o pega:

```text
Código original:
    if (x > 10) { aprovar(); }

Mutante gerado (Conditionals Boundary):
    if (x >= 10) { aprovar(); }   // > vira >=

Teste fraco (passa pelo mutante — mutante SOBREVIVE):
    @Test
    void aprovaQuandoMaiorQue10() {
        processar(15);   // 15 > 10 E 15 >= 10 -> aprova nos dois casos
        // sem asserção sobre o caso de borda x == 10
    }

Por que sobrevive:
    O teste nunca exercita x == 10, o único valor onde > e >= divergem.
    Com x = 15, original e mutante se comportam igual -> nenhum teste falha
    -> PIT marca o mutante como SURVIVED.

Teste que mata o mutante:
    @Test
    void naoAprovaQuandoIgualA10() {
        assertFalse(processar(10));  // 10 > 10 é false, 10 >= 10 é true
    }                                // a asserção falha sob o mutante -> KILLED
```

## Armadilhas

### (1) Tratar line coverage como meta de PR

Definir "X% de line coverage" como gate de merge incentiva o comportamento errado: o desenvolvedor escreve testes que **tocam** o código para bater o número, sem **verificar** nada. Você pode ter 100% de cobertura de linha e zero garantia.

```java
// Bate a meta de coverage, garante zero
@Test
void cobreOMetodo() {
    calculadora.somar(2, 3);  // executa a linha, não assere o resultado
}
```

**Fix**: tratar line coverage como sinal *negativo* apenas (cobertura baixa = teste faltando), nunca como prova de qualidade. Usar mutation coverage como a métrica que de fato exige asserções para subir, e medi-la no nightly.

### (2) Rodar PIT em cada build

PIT gera centenas ou milhares de mutantes por módulo e reroda a suíte para cada um. Plugá-lo no pipeline de cada `push` ou PR transforma um build de 2 minutos em um de 40, e o time aprende a odiar (e ignorar) a ferramenta.

```bash
# Anti-padrão: no estágio de PR, bloqueando cada commit
mvn test-compile org.pitest:pitest-maven:mutationCoverage
```

**Fix**: mover PIT para um job **agendado** (nightly ou semanal). O pipeline de PR roda testes + line coverage (rápido); o nightly roda PIT e publica o relatório de sobreviventes para o time revisar no dia seguinte.

### (3) Ignorar mutantes sobreviventes

Rodar PIT, ver "72% mutation coverage" e arquivar o relatório é desperdício. Os mutantes **sobreviventes** não são ruído estatístico — cada um é um defeito plausível e específico que sua suíte deixa passar. São, literalmente, o catálogo dos bugs que vão escapar para produção.

```text
SURVIVED  ValidadorPedido.java:42  -> negated conditional (== virou !=)
SURVIVED  CalculoFrete.java:88     -> replaced return value with 0
```

**Fix**: tratar a lista de sobreviventes como backlog acionável. Para cada um, decidir: escrever a asserção que o mata, ou justificar conscientemente por que aquele mutante é equivalente/irrelevante. O número agregado importa menos que zerar os sobreviventes em código crítico.

## Em entrevista

### Frase pronta (inglês)

> Line coverage only tells you a statement was *executed*, never that it was *verified* — you can hit 100% with no assertions at all. That's why I rely on mutation testing with PIT for the parts of the system that matter: it mutates the bytecode — flipping a conditional boundary, negating a condition, stripping a return value — and reruns the tests against each mutant. A surviving mutant is hard evidence of a weak test, because a plausible bug slipped through; a killed mutant proves the assertion actually catches that regression. Because it's expensive, I run it on a nightly job rather than on every build, and I treat the surviving mutants as an actionable backlog, not just a percentage.

### Vocabulário

| Termo (EN)             | Tradução / sentido                                              |
| ---------------------- | -------------------------------------------------------------- |
| mutation testing       | teste de mutação — mede se os testes pegam defeitos semeados   |
| mutant                 | mutante — variante do código com uma alteração mínima          |
| killed mutant          | mutante morto — um teste falhou e detectou o defeito (bom)     |
| survived / lived mutant| mutante sobrevivente — nenhum teste falhou (teste fraco)       |
| mutation coverage      | cobertura de mutação — % de mutantes mortos; a métrica honesta |
| line coverage          | cobertura de linha — só mede execução, não verificação         |
| mutator / mutation operator | mutador — a transformação aplicada (ex: negate conditional) |
| equivalent mutant      | mutante equivalente — mutação que não muda o comportamento     |

## Veja também

- [[03-Dominios/Java/Testes/18 - Performance — JMH e microbenchmarks|Performance — JMH]]
- [[03-Dominios/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno|O que é testar em Java]]
- [[03-Dominios/Java/Testes/21 - Capstone — a estratégia de testes de uma app Spring production-grade|Capstone de testes]]
- [[03-Dominios/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]] (verbetes mutation testing / PIT (Pitest))

## Referências

- PIT — site oficial: https://pitest.org/
- PIT — Maven quickstart: https://pitest.org/quickstart/maven/
- pitest-junit5-plugin (suporte a JUnit 5): https://github.com/pitest/pitest-junit5-plugin
