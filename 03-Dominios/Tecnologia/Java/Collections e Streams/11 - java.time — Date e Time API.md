---
title: "java.time — Date e Time API"
created: 2026-06-04
updated: 2026-06-04
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - collections
  - adepto
  - datetime
  - java-time
aliases:
  - "java.time"
  - "LocalDate"
  - "Date Time API"
---

# java.time — Date e Time API

> [!abstract] TL;DR
> `java.time` (JSR-310, Java 8) é a API moderna de datas e horas: imutável, thread-safe e semanticamente precisa. Use `LocalDate`/`LocalTime`/`LocalDateTime` quando timezone não importa, `ZonedDateTime` quando importa e `Instant` para persistência e logging (sempre UTC). `Duration` mede intervalos de tempo (horas, minutos, segundos); `Period` mede intervalos de calendário (anos, meses, dias). `DateTimeFormatter` formata e faz parsing — também imutável e thread-safe. Nunca use `Date`, `Calendar` ou `SimpleDateFormat` em código novo.

## O que é

`java.time` é o pacote de data e hora introduzido no Java 8 sob a especificação [JSR-310](http://jcp.org/en/jsr/detail?id=310). Ele substitui as classes problemáticas `java.util.Date` e `java.util.Calendar`, que acumulavam décadas de falhas de design: mutabilidade, falta de clareza entre instante e data local, meses indexados em zero e formatação não thread-safe via `SimpleDateFormat`.

A API é construída em torno de dois princípios centrais confirmados pelo Javadoc do Java 21:

- **Imutabilidade:** todos os tipos (`LocalDate`, `LocalDateTime`, `Instant`, `Duration`, `Period`, `DateTimeFormatter` etc.) são `final` e imutáveis. Cada operação de manipulação retorna uma nova instância — o objeto original nunca é alterado.
- **Thread-safety:** como consequência direta da imutabilidade, todas as instâncias são seguras para uso concorrente sem sincronização explícita.

O pacote segue o calendário proleptico gregoriano (ISO-8601) e divide os conceitos em tipos distintos, eliminando a ambiguidade que havia em `Date` (que representava ao mesmo tempo um instante e uma data local dependendo de como era usado).

## Por que importa

Datas e horas aparecem em praticamente todo sistema de software: timestamps de auditoria, agendamentos, cálculo de prazos, relatórios, serialização de dados. O legado `Date`/`Calendar` transformava tarefas simples em fontes de bugs sutis:

- `java.util.Date` é mutável — passá-la como parâmetro ou retorná-la de um método expõe o estado interno a modificações externas.
- `SimpleDateFormat` não é thread-safe — compartilhá-la entre threads em um pool gera condições de corrida silenciosas.
- `Calendar.MONTH` começa em zero — `Calendar.JANUARY == 0`, uma armadilha que persiste por décadas de código legado.

Com `java.time`, essas classes de problema desaparecem. Além disso, entrevistas para posições sênior cobram com frequência a distinção entre `Instant` e `LocalDateTime` para persistência, e a regra de qual tipo usar em cada cenário — dominar essa escolha é um diferencial concreto.

## Como funciona

### Tipos sem timezone (`LocalDate` / `LocalTime` / `LocalDateTime`)

Esses três tipos representam datas e horas "de parede" — sem informação de timezone ou offset UTC. O Javadoc os descreve como os tipos preferidos quando timezone não é parte do domínio.

```java
// LocalDate: apenas a data (ano, mês, dia)
LocalDate hoje       = LocalDate.now();
LocalDate nascimento = LocalDate.of(1990, 3, 15);
LocalDate parsed     = LocalDate.parse("2026-04-01");

// LocalTime: apenas o horário (hora, minuto, segundo, nanosegundo)
LocalTime abertura   = LocalTime.of(9, 0);
LocalTime fechamento = LocalTime.of(18, 30);

// LocalDateTime: data + horário, sem timezone
LocalDateTime reuniao = LocalDateTime.of(hoje, LocalTime.of(14, 30));
LocalDateTime inicio  = LocalDateTime.now();

// Manipulação — todas as operações retornam nova instância
LocalDate proximaSemana   = hoje.plusWeeks(1);
LocalDate primeiroDomes   = hoje.withDayOfMonth(1);
LocalDate mesPassado      = hoje.minusMonths(1);

// Comparação
boolean anterior = nascimento.isBefore(hoje); // true
boolean posterior = nascimento.isAfter(hoje);  // false
```

**Regra:** use `LocalDate` para datas puras (aniversários, feriados, datas de contrato), `LocalTime` para horários puros (horário de funcionamento, alarme), e `LocalDateTime` para data+hora quando o contexto é sempre o mesmo timezone (relatórios internos, agendas locais).

### Tipos com timezone (`ZonedDateTime` / `OffsetDateTime`) e `Instant` (UTC, persistência)

Quando o timezone importa, os tipos sem timezone são insuficientes. A API oferece três opções com informação temporal completa.

```java
// ZonedDateTime: data + hora + regras de timezone (DST incluído)
ZonedDateTime sp  = ZonedDateTime.now(ZoneId.of("America/Sao_Paulo"));
ZonedDateTime utc = ZonedDateTime.now(ZoneId.of("UTC"));

// Conversão entre zonas — não perde o instante, muda a representação
ZonedDateTime paris = sp.withZoneSameInstant(ZoneId.of("Europe/Paris"));

// OffsetDateTime: data + hora + offset fixo (sem regras de DST)
// Ideal para persistência em banco e protocolos de rede (XML, JSON)
OffsetDateTime comOffset = OffsetDateTime.now(ZoneOffset.ofHours(-3));

// Instant: ponto absoluto na linha do tempo, sempre em UTC
// Equivalente moderno de java.util.Date para timestamps
Instant agora      = Instant.now();                        // "2026-06-04T15:30:00.123Z"
Instant fromMillis = Instant.ofEpochMilli(System.currentTimeMillis());
long    epoch      = agora.toEpochMilli();                 // volta para milissegundos

// Conversão Instant → ZonedDateTime (para exibição)
ZonedDateTime exibicao = agora.atZone(ZoneId.of("America/Sao_Paulo"));
```

**Regra de ouro (da especificação Oracle):**

| Situação | Tipo recomendado |
|---|---|
| Data pura (sem hora/timezone) | `LocalDate` |
| Hora pura (sem data/timezone) | `LocalTime` |
| Data + hora, timezone implícito | `LocalDateTime` |
| Data + hora + timezone com DST | `ZonedDateTime` |
| Persistência / logging / timestamps | `Instant` |
| Protocolo de rede / banco de dados | `OffsetDateTime` |

### `Duration` (tempo) vs `Period` (datas)

`Duration` e `Period` representam quantidades de tempo, mas em domínios distintos — confundi-los é uma armadilha clássica.

```java
// Duration: intervalo baseado em tempo (horas, minutos, segundos, nanossegundos)
Instant inicio = Instant.now();
// ... processamento ...
Instant fim    = Instant.now();
Duration elapsed = Duration.between(inicio, fim);

System.out.println(elapsed.toSeconds());    // total em segundos
System.out.println(elapsed.toMillis());     // total em milissegundos
System.out.println(elapsed.toMinutes());    // total em minutos

// Criação direta
Duration trintaMin = Duration.ofMinutes(30);
Duration duasHoras = Duration.ofHours(2);
Duration timeout   = Duration.ofSeconds(30);

// Period: intervalo baseado em calendário (anos, meses, dias)
LocalDate contratacao = LocalDate.of(2020, 6, 1);
LocalDate hoje2       = LocalDate.now();
Period tempo = Period.between(contratacao, hoje2);

System.out.println(tempo.getYears());   // anos completos
System.out.println(tempo.getMonths());  // meses restantes
System.out.println(tempo.getDays());    // dias restantes

// Adicionar Period a uma data
LocalDate vencimento = LocalDate.now().plus(Period.ofMonths(3));
```

**Distinção crítica:** `Duration.ofDays(1)` sempre significa 86.400 segundos. `Period.ofDays(1)` adicionado a uma `LocalDate` em um dia de transição de horário de verão pode resultar em 23 ou 25 horas reais — porque `Period` opera sobre o calendário, não sobre o tempo físico.

### Formatação e parsing (`DateTimeFormatter`)

`DateTimeFormatter` é o ponto central para converter entre objetos `java.time` e `String`. Assim como todos os tipos da API, é **imutável e thread-safe** — pode e deve ser armazenado como constante estática.

```java
// Padrão personalizado (ofPattern)
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");

LocalDateTime reuniao = LocalDateTime.of(2026, 6, 15, 14, 30);
String texto   = reuniao.format(fmt);                        // "15/06/2026 14:30"
LocalDateTime  parsed = LocalDateTime.parse(texto, fmt);     // de volta ao objeto

// Constantes ISO predefinidas
DateTimeFormatter isoDate     = DateTimeFormatter.ISO_LOCAL_DATE;     // "2026-06-15"
DateTimeFormatter isoDateTime = DateTimeFormatter.ISO_LOCAL_DATE_TIME; // "2026-06-15T14:30:00"
DateTimeFormatter isoInstant  = DateTimeFormatter.ISO_INSTANT;         // "2026-06-15T14:30:00Z"

String dataFormatada = LocalDate.now().format(DateTimeFormatter.ISO_LOCAL_DATE);

// Locale-aware (para exibição ao usuário)
DateTimeFormatter localeBR = DateTimeFormatter
    .ofLocalizedDate(FormatStyle.LONG)
    .withLocale(new Locale("pt", "BR"));
// Saída: "15 de junho de 2026"

// Instant requer timezone para formatação local
Instant agora2 = Instant.now();
String exibivel = agora2.atZone(ZoneId.of("America/Sao_Paulo"))
                        .format(fmt);
```

Os símbolos de padrão mais usados: `dd` (dia com zero), `MM` (mês com zero), `yyyy`/`uuuu` (ano), `HH` (hora 0-23), `mm` (minuto), `ss` (segundo). Literais no padrão devem ser delimitados por aspas simples: `"'Início:' dd/MM/yyyy"`.

### Imutabilidade (operações retornam nova instância)

Todas as operações que parecem modificar um objeto `java.time` retornam, na verdade, uma nova instância. O objeto original permanece inalterado. Isso é garantido pela especificação do Java 21 para toda a hierarquia do pacote.

```java
LocalDate base = LocalDate.of(2026, 1, 1);

// CORRETO: capturar o retorno
LocalDate fim  = base.plusMonths(6);   // base = 2026-01-01, fim = 2026-07-01

// ERRO SILENCIOSO: ignorar o retorno
base.plusMonths(6);  // base continua 2026-01-01 — a nova instância foi descartada
System.out.println(base); // "2026-01-01" — nada mudou

// O mesmo se aplica a todos os tipos
Duration d1 = Duration.ofHours(2);
Duration d2 = d1.plusMinutes(30); // d1 continua PT2H; d2 é PT2H30M

LocalDateTime dt = LocalDateTime.now();
LocalDateTime  dtUtc = dt.atZone(ZoneId.of("UTC")).toLocalDateTime(); // dt inalterado
```

Essa garantia torna os objetos `java.time` seguros para compartilhamento entre threads e para uso como chaves em coleções — o estado não muda após a criação.

## Na prática

```java
// Calcular próxima semana a partir de hoje
LocalDate hoje        = LocalDate.now();
LocalDate proximaSemana = hoje.plusWeeks(1);
System.out.println("Vencimento: " + proximaSemana); // "2026-06-11"

// Medir tempo de execução
Instant antes  = Instant.now();
realizarProcessamento();
Instant depois = Instant.now();
Duration tempo = Duration.between(antes, depois);
System.out.printf("Processamento: %d ms%n", tempo.toMillis());

// Formatar data para exibição
DateTimeFormatter br = DateTimeFormatter.ofPattern("dd/MM/yyyy");
String exibir = LocalDate.now().format(br); // "04/06/2026"

// Tempo de casa de um funcionário
LocalDate admissao = LocalDate.of(2019, 3, 10);
Period   tempoCasa = Period.between(admissao, LocalDate.now());
System.out.printf("%d anos, %d meses%n",
    tempoCasa.getYears(), tempoCasa.getMonths());

// Timestamp de auditoria (para persistir no banco)
Instant  criadoEm = Instant.now();           // salvar como TIMESTAMP WITH TIME ZONE
long     epochMs  = criadoEm.toEpochMilli(); // ou como BIGINT

// Converter timestamp armazenado de volta para exibição local
Instant  restaurado = Instant.ofEpochMilli(epochMs);
ZonedDateTime local = restaurado.atZone(ZoneId.of("America/Sao_Paulo"));
System.out.println(local.format(DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm z")));
```

## Armadilhas

**1. Usar `Date` / `Calendar` / `SimpleDateFormat` (legado, mutável, não thread-safe)**

```java
// ERRADO — legado e perigoso
SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy");
// Compartilhar sdf entre threads é uma condição de corrida

Date data = new Date();
data.setTime(System.currentTimeMillis() + 86_400_000); // mutável, frágil

// CORRETO — java.time
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("dd/MM/yyyy"); // thread-safe
LocalDate amanha = LocalDate.now().plusDays(1);                    // imutável
```

`SimpleDateFormat` não é thread-safe: se dois threads chamarem `format()` ou `parse()` ao mesmo tempo sobre a mesma instância, o resultado é indefinido. `DateTimeFormatter` elimina esse problema por design.

**2. Confundir `Duration` com `Period`**

```java
// ERRADO — usar Duration para datas de calendário
Duration errado = Duration.between(
    LocalDate.of(2026, 1, 1).atStartOfDay(),
    LocalDate.of(2026, 12, 31).atStartOfDay()
);
// Retorna PT8736H — tecnicamente correto em segundos, mas não é o que se quer

// CORRETO — Period para intervalos de calendário
Period correto = Period.between(
    LocalDate.of(2026, 1, 1),
    LocalDate.of(2026, 12, 31)
);
System.out.println(correto.getMonths()); // 11 (meses e dias, não segundos)

// CORRETO — Duration para intervalos de tempo real
Instant t1 = Instant.parse("2026-06-04T10:00:00Z");
Instant t2 = Instant.parse("2026-06-04T12:30:00Z");
Duration intervalo = Duration.between(t1, t2); // PT2H30M
```

**3. Usar `LocalDateTime` para timestamp persistido (perde timezone)**

```java
// ERRADO — LocalDateTime não carrega timezone
// Se o servidor mudar de timezone, o valor muda de significado
LocalDateTime criadoEm = LocalDateTime.now();
// Persistido como "2026-06-04T15:30:00" — em qual timezone?

// CORRETO — Instant é sempre UTC, sem ambiguidade
Instant criadoEm2 = Instant.now();
// Persistido como "2026-06-04T18:30:00Z" — inequívoco

// Ou OffsetDateTime para preservar o offset original no banco
OffsetDateTime comOffset = OffsetDateTime.now(ZoneOffset.ofHours(-3));
// "2026-06-04T15:30:00-03:00" — data + hora + offset preservados
```

Essa distinção é especialmente crítica em sistemas distribuídos: se o serviço roda em múltiplos servidores em diferentes regiões, `LocalDateTime` produz valores inconsistentes. `Instant` garante um único ponto de referência global.

## Em entrevista

### Frase pronta (inglês)

"The `java.time` package, introduced in Java 8 under JSR-310, replaces the legacy `Date` and `Calendar` classes with an immutable, thread-safe API. The core design rule is straightforward: use `LocalDate`, `LocalTime`, or `LocalDateTime` when timezone is not part of your domain, `ZonedDateTime` when you need full timezone semantics including DST rules, and `Instant` for persistence and logging since it always represents a UTC timestamp with no ambiguity. `Duration` measures time-based intervals with nanosecond precision, while `Period` measures calendar-based intervals in years, months, and days — they are not interchangeable. `DateTimeFormatter` is immutable and thread-safe, so it should be stored as a static constant and reused. A common interview mistake is using `LocalDateTime` for database timestamps: it silently drops timezone information, which breaks correctness in distributed systems."

### Vocabulário

| Termo | Definição curta |
|---|---|
| **immutable** | objeto cujo estado não pode ser alterado após a criação |
| **thread-safe** | seguro para acesso simultâneo por múltiplas threads sem sincronização |
| **epoch** | ponto de referência `1970-01-01T00:00:00Z` (Unix epoch) |
| **UTC** | Coordinated Universal Time — referência de tempo global sem offset |
| **DST** | Daylight Saving Time — horário de verão; `ZonedDateTime` lida com isso automaticamente |
| **ISO-8601** | padrão internacional para representação de datas e horas (ex: `2026-06-04T15:30:00Z`) |
| **JSR-310** | Java Specification Request que definiu o `java.time` API |
| **temporal adjuster** | função que ajusta uma data (`TemporalAdjuster`, ex: `lastDayOfMonth()`) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#LocalDate / LocalDateTime|LocalDate / LocalDateTime]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Instant|Instant]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Duration / Period|Duration / Period]]

## Referências

- [java.time — Package Summary (Java 21 Javadoc)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/package-summary.html)
- [LocalDate (Java 21 Javadoc)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/LocalDate.html)
- [Instant (Java 21 Javadoc)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/Instant.html)
- [Duration (Java 21 Javadoc)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/Duration.html)
- [DateTimeFormatter (Java 21 Javadoc)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/format/DateTimeFormatter.html)
- [Date and Time (Oracle Java Tutorial)](https://docs.oracle.com/javase/tutorial/datetime/index.html)
- [JSR-310: Date and Time API](http://jcp.org/en/jsr/detail?id=310)
