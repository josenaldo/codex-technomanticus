---
title: "Domínio 10 — Localização"
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
  - "Domínio 10 OCP"
  - "Localização na OCP"
---

# Domínio 10 — Localização

> [!abstract] TL;DR
> Este é o domínio de **menor peso** na prova — mas cai. E aqui mora uma armadilha: a trilha Java quase não cobre o assunto. DateTimeFormatter você já viu (em java.time, G2); o resto — `Locale`, `ResourceBundle`, `NumberFormat` — exige **estudo à parte**. Não dá pra confiar só na trilha. Trate este domínio como uma ilha isolada: pequena, mas com pegadinhas próprias.

> [!info] Títulos oficiais
> - **1Z0-830 (Java 21):** *Implementing Localization*
> - **1Z0-831 (Java 25):** *Developing Applications with Localization Support*

## O que a Oracle cobra

A Oracle desdobra este domínio em quatro famílias de API. Pense nelas como camadas: você primeiro decide **quem é o usuário** (Locale), depois **o que dizer a ele** (ResourceBundle) e finalmente **como formatar números e datas** no jeito dele (NumberFormat, DateTimeFormatter).

- **Locale** — criação de instâncias, `Locale.getDefault`, `Locale.Builder`, e o formato `language-country` (ex.: `pt-BR`, `en-US`). É a "identidade cultural" que todo o resto consome.
- **ResourceBundle** — leitura de mensagens a partir de *properties files*, a **hierarquia de fallback** (do mais específico ao mais genérico), e o método `getBundle`. É como você externaliza textos pra fora do código.
- **NumberFormat** — formatação e *parsing* de moeda (`currency`), porcentagem (`percent`) e números genéricos, sempre sensível ao Locale.
- **DateTimeFormatter** — `FormatStyle` em quatro tamanhos (`SHORT`, `MEDIUM`, `LONG`, `FULL`) e os métodos `localizedBy` / `withLocale` pra amarrar o formatador a um Locale.

## Mapa de revisão

- [[03-Dominios/Tecnologia/Java/Collections e Streams/11 - java.time — Date e Time API|java.time — Date e Time API (G2)]] — cobre DateTimeFormatter (parte do domínio).

## Pegadinhas deste domínio

São poucas, mas concentradas. Decore o mecanismo de fallback — é o que a prova mais explora.

**(1) ResourceBundle: a cascata de fallback.** Pedindo `messages` com locale `pt_BR`, o Java procura nesta ordem, do mais específico ao mais genérico:

```text
messages_pt_BR.properties   →   messages_pt.properties   →   messages.properties
```

Se a chave não existir em nenhum desses, ele ainda tenta a cadeia do **default locale** antes de estourar `MissingResourceException`. A regra de ouro: cai sempre pro mais genérico, e por fim pro `messages.properties` base.

**(2) Locale é "language_COUNTRY".** O idioma vem em minúsculas, o país em maiúsculas:

```java
Locale brasil = new Locale("pt", "BR");   // legado, ainda compila
Locale moderno = Locale.of("pt", "BR");   // Java 19+, forma preferida
```

A partir do Java 19, o construtor `new Locale(...)` foi *deprecated* em favor de `Locale.of(...)`. Na prova da 1Z0-831 (Java 25), prefira `Locale.of`.

**(3) NumberFormat troca símbolo E separadores.** `getCurrencyInstance(locale)` não muda só o símbolo da moeda — muda também os separadores de milhar e decimal:

```java
double valor = 1234.56;
NumberFormat.getCurrencyInstance(Locale.US).format(valor);          // $1,234.56
NumberFormat.getCurrencyInstance(Locale.of("pt","BR")).format(valor); // R$ 1.234,56
```

Repare: ponto e vírgula trocam de papel entre `en-US` e `pt-BR`. Cuidado com questões que misturam o símbolo de um locale com os separadores de outro.

Veja mais armadilhas transversais no [[03-Dominios/Tecnologia/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas|catálogo de pegadinhas]].

## Lacuna da trilha

> [!warning] Seam de honestidade
> A trilha Java Senior cobre **DateTimeFormatter** (dentro de java.time, G2), mas **NÃO cobre** `Locale`, `ResourceBundle` nem `NumberFormat`. Ou seja: quase todo este domínio é território não-mapeado pela trilha. Aqui vai o mínimo autocontido pra você não chegar cru na prova — mas reserve estudo à parte.

### 1. Locale

O `Locale` carrega idioma + país (e, opcionalmente, variante/script). Tudo que formata texto culturalmente sensível consome um `Locale`.

```java
Locale atual = Locale.getDefault();           // o locale da JVM/SO
Locale ptBR = Locale.of("pt", "BR");          // Java 19+
Locale enUS = Locale.US;                       // constante pronta

// alimentando um formatador:
NumberFormat nf = NumberFormat.getInstance(ptBR);
```

`Locale.getDefault()` reflete o ambiente onde a JVM roda — por isso testes que dependem do default locale são frágeis. A boa prática (e a resposta certa na prova) é **sempre passar o Locale explicitamente** aos formatadores.

### 2. ResourceBundle

É o mecanismo de externalização de mensagens. Você cria um arquivo `.properties` por locale e o Java escolhe o certo em tempo de execução.

```properties
# messages.properties (base/default)
greeting=Hello

# messages_pt_BR.properties
greeting=Olá
```

```java
ResourceBundle bundle = ResourceBundle.getBundle("messages", Locale.of("pt","BR"));
String texto = bundle.getString("greeting");   // "Olá"
```

A `getBundle` aplica a cascata de fallback descrita nas pegadinhas: do `_pt_BR` ao `_pt`, ao base, e em último caso à cadeia do default locale. Se a chave não for encontrada em lugar nenhum, `getString` lança `MissingResourceException`.

### 3. NumberFormat

A fábrica de formatadores numéricos. Três variantes principais, todas aceitando um `Locale`:

```java
Locale ptBR = Locale.of("pt", "BR");

NumberFormat.getInstance(ptBR).format(1234.5);          // 1.234,5
NumberFormat.getCurrencyInstance(ptBR).format(1234.5);  // R$ 1.234,50
NumberFormat.getPercentInstance(ptBR).format(0.75);     // 75%

// parsing (o caminho inverso) lança ParseException (checked):
Number n = NumberFormat.getInstance(ptBR).parse("1.234,5");
```

Atenção ao `parse`: ele é o inverso do `format` e lança `ParseException` (checada) — precisa de try/catch ou `throws`. A prova adora cobrar isso.

> [!tip] Estude à parte
> Este é o domínio mais provável de você nunca ter tocado no trabalho. Reserve uma sessão dedicada com o **Sybex OCP Study Guide** (capítulo de Localization) e a **documentação oficial** de `ResourceBundle` e `NumberFormat`. É pouco conteúdo, mas com mecânica própria — não dá pra adivinhar.

## Em entrevista

Frase curta, sem reivindicar credencial:

> *"Java handles internationalization through `ResourceBundle`, which resolves message keys from the most specific `.properties` file down to a default fallback — so you externalize strings per locale instead of hardcoding them."*

Vocabulário PT | EN:

- localização | localization
- pacote de recursos | resource bundle
- formato de moeda | currency format
- idioma e país | language and country (locale)

## Veja também

- [[03-Dominios/Tecnologia/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|O mapa objetivo → galho]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas|O catálogo de pegadinhas clássicas]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/index|Certificação OCP (MOC do galho)]]

## Referências

- ResourceBundle docs: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ResourceBundle.html
- Enthuware 21: https://enthuware.com/oca-ocp-java-certification-resources/290-ocp-java-21-exam-syllabus
