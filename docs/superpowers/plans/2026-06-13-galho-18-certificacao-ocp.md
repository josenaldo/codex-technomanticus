# Galho 18 — Certificação Java OCP — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir o Galho 18 (Certificação Java OCP) — 17 notas atômicas + MOC mapeando o syllabus oficial (1Z0-830/1Z0-831) aos galhos 1-4 da trilha, colher e podar o tronco legado, integrar índice central e Dicionário.

**Architecture:** Pasta `03-Dominios/Tecnologia/Java/Certificação OCP/` com 17 notas + `index.md` (MOC). Espinha = 10 domínios oficiais; cada nota de domínio mapeia para notas exatas dos galhos via wikilink (linka, não re-explica). Grupos de certificação (não 3 fases). Subagentes write-only; controller commita nominal por fase.

**Tech Stack:** Obsidian Flavored Markdown, wikilinks, callouts, frontmatter YAML, Dataview. Skill `verificar-wikilinks` para validação.

---

## Notas operacionais (ler antes de executar)

- **Spec:** `docs/superpowers/specs/2026-06-13-galho-18-certificacao-ocp-design.md` — fonte de verdade. Este plano operacionaliza.
- **Subagentes write-only:** cada tarefa de nota = 1 subagente que CRIA o arquivo. O subagente recebe no prompt: o skeleton da nota, os fatos obrigatórios, e **os wikilinks-alvo EXATOS** (copiar de §7 do spec — NUNCA deixar o subagente inventar título de nota).
- **Controller commita:** `git add <arquivos específicos>` — **NUNCA `git add -A`** (bot do Obsidian Git roda no timer). Sem `Co-Authored-By`.
- **Direto na main**, sem branch. Sem push (manual pelo usuário).
- **Validação por fase:** após cada fase de notas, rodar grep dos wikilinks contra arquivos reais. Validação final completa via `verificar-wikilinks` na Fase 6.
- **Voz de plano:** onde colher 1ª pessoa do tronco, reescrever como preparação ("meu plano é…", "estou me preparando…") — nunca afirmar prova feita/credencial obtida.
- **Fonte de colheita:** tronco legado `03-Dominios/Tecnologia/Java/Core/Certificação Java OCP.md` (878 linhas). Mapa de seções:
  - L19-38 (o que é / vantagens / desvantagens) → nota 01
  - L42-57 (versões + OCA) → nota 02
  - L61-100 (formato + online vs físico) → nota 03
  - L104-294 (12 tópicos) → notas de domínio 05-14 (reorganizar p/ 10 oficiais)
  - L296-398 (novidades Java 21) → dobrar nas notas de domínio relevantes
  - L402-629 (armadilhas clássicas) → nota 15
  - L633-697 (estratégia de estudo) → nota 16
  - L701-749 (tips + depois) → nota 17
  - L753-804 (Na prática / How to explain) → reformular em voz de plano, distribuir
  - L821-866 (recursos) → notas 02/16

---

## Convenções de wikilink (copiar exato)

Formato: `[[03-Dominios/Tecnologia/Java/<Pasta>/<arquivo sem .md>|<rótulo>]]`. Lista canônica de títulos exatos dos galhos 1-4 e G6·13 está em **§7 do spec** — é a fonte. Exemplos:
- `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/02 - Tipos, variáveis e operadores|Tipos, variáveis e operadores (G1)]]`
- `[[03-Dominios/Tecnologia/Java/Collections e Streams/12 - I-O moderno com java.nio.file|I/O moderno com java.nio.file (G2)]]`
- `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads (G4)]]`

Wikilinks internos do galho: `[[03-Dominios/Tecnologia/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|o mapa objetivo → galho]]`.

---

## File Structure

```
03-Dominios/Tecnologia/Java/Certificação OCP/
├── index.md                                  (MOC do galho)
├── 01 - A certificação OCP — o que é, por que (e por que não) fazer.md
├── 02 - Qual prova mirar — Java 21 (1Z0-830) vs Java 25 (1Z0-831).md
├── 03 - Formato, logística e mecânica da prova.md
├── 04 - O mapa objetivo → galho — revisar a trilha pra prova.md
├── 05 - Domínio 1 — Datas, texto, números e booleanos.md
├── 06 - Domínio 2 — Controle de fluxo.md
├── 07 - Domínio 3 — Orientação a objetos.md
├── 08 - Domínio 4 — Exceções.md
├── 09 - Domínio 5 — Arrays e coleções.md
├── 10 - Domínio 6 — Streams e lambdas.md
├── 11 - Domínio 7 — Empacotamento, deployment e módulos.md
├── 12 - Domínio 8 — Concorrência.md
├── 13 - Domínio 9 — I/O.md
├── 14 - Domínio 10 — Localização.md
├── 15 - O catálogo de pegadinhas clássicas.md
├── 16 - Estratégia de estudo e recursos.md
└── 17 - O dia da prova e depois.md
```
Também tocados: `Core/Certificação Java OCP.md` (poda), `index.md` central, `Dicionário de Java.md`.

---

# FASE 0 — Scaffolding (MOC esqueleto)

### Task 0.1: Criar a pasta e o MOC esqueleto

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Certificação OCP/index.md`

- [ ] **Step 1: Criar o MOC** com frontmatter + estrutura completa, listando os 17 títulos como wikilinks (o esqueleto fica pronto; as notas serão preenchidas depois).

Frontmatter:
```yaml
---
title: "Certificação Java OCP"
created: 2026-06-13
updated: 2026-06-13
type: moc
status: growing
publish: true
tags:
  - java
  - certificacao-ocp
  - moc
aliases:
  - "Certificação OCP"
  - "Galho 18 - Certificação OCP"
  - "OCP Java SE"
  - "1Z0-830"
  - "1Z0-831"
---
```

Corpo (seções, nesta ordem):
1. `# Certificação Java OCP`
2. `> [!abstract] TL;DR` — galho atípico: não re-ensina linguagem, é guia da prova OCP mapeado aos galhos 1-4. Cobre 2 provas vigentes (Java 21/1Z0-830 e Java 25/1Z0-831), os 10 domínios oficiais, pegadinhas e estratégia. 17 notas em 3 grupos de certificação. Último galho da trilha.
3. `## Sobre este galho` — a tese atípica + **fronteira-assinatura**: este galho LINKA, não re-explica. Galho 1 (linguagem), Galho 2 (collections/streams/IO/time), Galho 3 (JVM/módulos), Galho 4 (concorrência), Galho 6 (jlink/jpackage). A mecânica vive lá; aqui só o ângulo de prova.
4. `## Sobre a prova` — wikilinks notas 01-04.
5. `## Os domínios do exame` — wikilinks notas 05-14.
6. `## Pegadinhas, estratégia e dia da prova` — wikilinks notas 15-17.
7. `## Rotas alternativas`:
   - **Completa:** 01→…→17 em ordem.
   - **Reta-final (pré-prova):** 04 (mapa) → 15 (pegadinhas) → 03 (formato) → 17 (dia da prova).
   - **Só-pegadinhas:** 15 → domínios com mais armadilhas (07, 10, 12).
   - **Por-domínio:** 04 → escolher domínio fraco → nota de domínio → galho mapeado.
   - **Decidir a prova:** 01 → 02 → 03.
8. `## Veja também` — `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]`, galhos 1-4, `[[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]`, tronco `[[03-Dominios/Tecnologia/Java/Core/Certificação Java OCP|Certificação OCP (tronco legado)]]`.
9. `## Notas do galho` — bloco dataview:
````
```dataview
TABLE fase, status
FROM "03-Dominios/Tecnologia/Java/Certificação OCP"
WHERE type = "concept"
SORT file.name ASC
```
````

Os wikilinks das notas 01-17 usam o path completo `[[03-Dominios/Tecnologia/Java/Certificação OCP/<arquivo sem .md>|<rótulo curto>]]` com os nomes de arquivo exatos da File Structure acima.

- [ ] **Step 2: Validar** que o arquivo existe e os 17 wikilinks internos apontam para nomes de arquivo idênticos aos da File Structure.

Run: `ls "03-Dominios/Tecnologia/Java/Certificação OCP/"` (deve mostrar só index.md por ora).

- [ ] **Step 3: Commit**
```bash
git add "03-Dominios/Tecnologia/Java/Certificação OCP/index.md"
git commit -m "feat(java): scaffolding do Galho 18 (Certificação OCP) — MOC esqueleto"
```

---

# FASE 1 — Sobre a prova (notas 01-04)

> Cada nota: subagente write-only com o skeleton abaixo + fatos do §3 do spec. Controller commita as 4 juntas ao fim da fase.

### Task 1.1: Nota 01 — A certificação OCP (o que é / por que)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Certificação OCP/01 - A certificação OCP — o que é, por que (e por que não) fazer.md`

- [ ] **Step 1: Criar a nota.** Frontmatter `fase: sobre-a-prova`, tags `[java, certificacao-ocp, sobre-a-prova]`, aliases `["Certificação OCP", "Por que fazer OCP"]`.

Seções:
- `> [!abstract] TL;DR` — 1 linha.
- `## O que é a OCP` — Oracle Certified Professional Java SE; credencial oficial que valida domínio da linguagem + APIs core; reconhecida internacionalmente (Europa/Ásia em vagas senior). Colher L19-29.
- `## Por que fazer` — credencial internacional, forcing function (fecha gaps), disciplina de estudo, salary bump em algumas empresas. Colher L23-29.
- `## Por que talvez não` — conhecimento acadêmico (corner cases de bytecode ≠ arquitetura), não substitui experiência, custo (USD 245), versão fica datada. Colher L31-38. **Honesto.**
- `## OCA acabou` — desde Java 11 prova OCP única, sem OCA separada (ver nota 02). Colher L55-57.
- `## Em entrevista` — frase EN demonstrando *por que* a pessoa busca a cert (forcing function), **voz de preparação** (não "I have", e sim "I'm pursuing / preparing for"). Vocabulário PT/EN (certificação→certification, forcing function, credencial→credential).
- `## Veja também` — notas 02, 03, 16 do galho; `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]`.
- `## Referências` — `https://education.oracle.com/java-certification`.

- [ ] **Step 2: Validar** wikilinks internos (notas 02/03/16 + trilha) batem com nomes de arquivo.

### Task 1.2: Nota 02 — Qual prova mirar (21 vs 25)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Certificação OCP/02 - Qual prova mirar — Java 21 (1Z0-830) vs Java 25 (1Z0-831).md`

- [ ] **Step 1: Criar a nota.** Frontmatter `fase: sobre-a-prova`, aliases `["1Z0-830", "1Z0-831", "OCP Java 21 vs 25"]`.

Seções:
- `> [!abstract] TL;DR`.
- `## As versões vigentes` — tabela: 1Z0-830 (Java SE 21, consolidada, livro Sybex existe) | 1Z0-831 (Java SE 25, lançada 01/mai/2026, sem livro Sybex ainda). Ambas válidas. **Oracle não anunciou aposentadoria do 830** (afirmar só isso). Colher/atualizar L42-53 (a tabela do tronco está desatualizada — adicionar a 25).
- `## A linhagem (OCA→OCP único)` — 1Z0-815+816 → 1Z0-819 (ago/2020) → 1Z0-829 → 1Z0-830 → 1Z0-831. Java 8 ainda exigia OCA. Colher L55-57.
- `## Os 10 domínios são quase iguais` — callout/tabela com os dois conjuntos de títulos oficiais (copiar a tabela do §3 do spec). Mensagem: o mapeamento objetivo→galho (nota 04) serve as duas provas.
- `## Qual escolher` — recomendação honesta por perfil: 21 se quer material maduro (Sybex/Enthuware), 25 se quer a LTS mais nova e já estudou Java 25 features pela trilha. Sem dogma.
- `## Veja também` — nota 04 (mapa), nota 03, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/15 - A evolução do Java (8 a 25)|A evolução do Java (G1)]]`.
- `## Referências` — as 4 URLs do §3 do spec (Oracle 830/831 + Enthuware 290/297).

### Task 1.3: Nota 03 — Formato, logística e mecânica

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Certificação OCP/03 - Formato, logística e mecânica da prova.md`

- [ ] **Step 1: Criar a nota.** Frontmatter `fase: sobre-a-prova`, aliases `["Formato da prova OCP", "Online proctored"]`.

Seções:
- `> [!abstract] TL;DR`.
- `## Formato` — 50 questões, nota de corte ~68%, múltipla escolha (single + multi-answer). **Duração: registrar a divergência** — "fontes secundárias divergem entre 90 e 120 min; confirme na página oficial do seu exame". Preço USD 245 (varia por região). Colher L61-76 mas **corrigir** (tronco dizia 90 min fixo).
- `## Características traiçoeiras` — multi-answer sem crédito parcial, "Select two/three", código real (o que imprime/compila/lança), marcador de revisão. Colher L77-84.
- `## Online proctored vs centro` — prós/contras de cada; **nota:** o 1Z0-830 migrou da Pearson VUE para agendamento via `oracle.com/education` (marcar como *fonte secundária — verificar*). Colher L86-100 + fato do §3.
- `## Veja também` — notas 02, 17, 16.
- `## Referências` — páginas oficiais 830/831.

### Task 1.4: Nota 04 — O mapa objetivo → galho (NOTA-CORAÇÃO)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova.md`

- [ ] **Step 1: Criar a nota.** Frontmatter `fase: sobre-a-prova`, aliases `["Mapa objetivo galho", "Revisar a trilha pra OCP"]`. **Esta é a nota mais importante — o hub de revisão.**

Seções:
- `> [!abstract] TL;DR` — "se você já fez a trilha, esta é a sua porta: cada domínio do exame → as notas exatas que o cobrem."
- `## Como usar este mapa` — orientação: identifique domínio fraco, vá às notas linkadas, revise, volte às pegadinhas (nota 15).
- `## O mapa` — **tabela grande**, uma linha por domínio (1-10), colunas: Domínio | Notas da trilha (wikilinks exatos) | Nota de domínio deste galho | Cobertura (Cheia/Parcial). Os wikilinks de cada domínio seguem o mapeamento do §4 do spec. **Usar os títulos exatos do §7 do spec.** Exemplo da linha do Domínio 8:
  - Concorrência | `[[…/Concorrência e paralelismo/02 - Threads e seu ciclo de vida|…]]`, `[[…/08 - Executors e thread pools|…]]`, `[[…/10 - CompletableFuture e composição assíncrona|…]]`, `[[…/12 - Virtual Threads e Project Loom|…]]` | `[[…/Certificação OCP/12 - Domínio 8 — Concorrência|Domínio 8]]` | Cheia
- `## Os três domínios que a trilha não cobre por inteiro` — destacar Domínios 7 (empacotamento), 9 (I/O), 10 (localização); apontar para as notas 11/13/14 que carregam o gap. **Seam de honestidade.**
- `## Veja também` — todas as notas de domínio (05-14), nota 15.
- `## Referências` — Enthuware 290/297.

- [ ] **Step 2: Validar TODOS os wikilinks da tabela** contra arquivos reais (grep — ver Fase 6, mas rodar parcial aqui dado o volume de links desta nota).

### Task 1.5: Commit da Fase 1
- [ ] Review das 4 notas (controller lê cada uma; checa voz de plano na 01, divergência de duração na 03, wikilinks na 04).
```bash
git add "03-Dominios/Tecnologia/Java/Certificação OCP/01 - A certificação OCP — o que é, por que (e por que não) fazer.md" \
        "03-Dominios/Tecnologia/Java/Certificação OCP/02 - Qual prova mirar — Java 21 (1Z0-830) vs Java 25 (1Z0-831).md" \
        "03-Dominios/Tecnologia/Java/Certificação OCP/03 - Formato, logística e mecânica da prova.md" \
        "03-Dominios/Tecnologia/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova.md"
git commit -m "feat(java): Galho 18 — grupo 'Sobre a prova' (notas 01-04, mapa objetivo→galho)"
```

---

# FASE 2 — Domínios cheios (notas 05, 06, 07, 08, 09, 10, 12)

> **Estrutura comum de nota de domínio** (todas as notas 05-14). Subagente recebe: skeleton + sub-objetivos oficiais + wikilinks exatos do domínio (§7 spec) + pegadinhas do domínio. Frontmatter `fase: dominios`, tags `[java, certificacao-ocp, dominios]`.
>
> Seções: `> [!abstract] TL;DR` → `> [!info] Títulos oficiais` (os dois títulos 21/25 do §3) → `## O que a Oracle cobra` (sub-objetivos) → `## Mapa de revisão` (wikilinks exatos das notas dos galhos) → `## Pegadinhas deste domínio` (linka nota 15 quando transversal) → `## Em entrevista` (frase EN do domínio, leve) → `## Veja também` → `## Referências`.

### Task 2.1: Nota 05 — Domínio 1 (Datas, texto, números, booleanos)
**Files:** Create `…/05 - Domínio 1 — Datas, texto, números e booleanos.md`
- [ ] **Step 1: Criar.** Cobertura **Cheia**.
  - O que a Oracle cobra: primitivos/wrappers/autoboxing, literais numéricos (`100_000`,`0b`,`0x`,`L`,`f`), operadores/precedência/short-circuit, String (imutabilidade/pool/equals vs ==/text blocks), StringBuilder, `java.time` (LocalDate/Time/DateTime/ZonedDateTime/Instant/Duration/Period), DateTimeFormatter, BigDecimal/RoundingMode. Colher L108-118.
  - Mapa de revisão (wikilinks exatos): `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/02 - Tipos, variáveis e operadores|Tipos, variáveis e operadores]]`, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/04 - Strings e text blocks|Strings e text blocks]]`, `[[03-Dominios/Tecnologia/Java/Collections e Streams/11 - java.time — Date e Time API|java.time — Date e Time API]]`.
  - Pegadinhas do domínio: Integer cache (-128..127), BigDecimal vs float p/ dinheiro. Linka nota 15.

### Task 2.2: Nota 06 — Domínio 2 (Controle de fluxo)
**Files:** Create `…/06 - Domínio 2 — Controle de fluxo.md`
- [ ] **Step 1: Criar.** Cobertura **Cheia**.
  - O que a Oracle cobra: if/else, switch statement vs switch expression, pattern matching em switch (Java 21), loops (for/enhanced/while/do-while), labels (`break label`), return/break/continue. Colher L122-130.
  - Mapa: `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/03 - Estruturas de controle e fluxo|Estruturas de controle e fluxo]]`, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/14 - Sealed classes e pattern matching|Sealed classes e pattern matching]]`.
  - Pegadinhas: switch fall-through (statement) vs sem fall-through (arrow), exaustividade com sealed/`yield`. Linka nota 15.

### Task 2.3: Nota 07 — Domínio 3 (Orientação a objetos)
**Files:** Create `…/07 - Domínio 3 — Orientação a objetos.md`
- [ ] **Step 1: Criar.** Cobertura **Cheia**. (Domínio mais denso.)
  - O que a Oracle cobra: classes/objetos/construtores/ordem de init, métodos/varargs/covariância, encapsulamento/modificadores, herança/`@Override`/polimorfismo/dynamic dispatch, casting/`instanceof`/pattern matching, abstratas vs interfaces, default methods/diamond, static/final, inner classes (static nested/inner/local/anonymous), enums, records (compact constructor), sealed classes. Colher L134-148 + L298-326 (records/sealed).
  - Mapa (wikilinks exatos): `06 - Classes, objetos e encapsulamento`, `07 - Herança e polimorfismo`, `08 - Interfaces e classes abstratas`, `09 - Enums`, `11 - Annotations`, `12 - Generics em profundidade`, `13 - Records e record patterns`, `14 - Sealed classes e pattern matching` (todos `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/<arquivo>|<rótulo>]]`).
  - Pegadinhas: ordem de init (static→instance→constructor), static hiding ≠ override, enum constructor private, record component final, generics type erasure. Linka nota 15.

### Task 2.4: Nota 08 — Domínio 4 (Exceções)
**Files:** Create `…/08 - Domínio 4 — Exceções.md`
- [ ] **Step 1: Criar.** Cobertura **Cheia**.
  - O que a Oracle cobra: hierarquia (Throwable/Error/Exception/RuntimeException), checked vs unchecked, try/catch/finally/multi-catch, try-with-resources (AutoCloseable/suppressed/ordem de close), throws/overriding rules, custom exceptions, assertions. Colher L158-165.
  - Mapa: `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros|Exceções e tratamento de erros]]`.
  - Pegadinhas: try/finally com return, try-with-resources ordem reversa, multi-catch com exceções relacionadas (não compila), override não adiciona checked. Linka nota 15.

### Task 2.5: Nota 09 — Domínio 5 (Arrays e coleções)
**Files:** Create `…/09 - Domínio 5 — Arrays e coleções.md`
- [ ] **Step 1: Criar.** Cobertura **Cheia**.
  - O que a Oracle cobra: arrays (decl/init/multi-dim/Arrays.sort/binarySearch), List/Set/Map/Queue + implementações, ArrayList vs LinkedList, HashMap/TreeMap/LinkedHashMap, Deque/Stack/Queue ops, Iterator/Iterable (fail-fast vs fail-safe), Comparable/Comparator, imutáveis (List.of/unmodifiableList — view vs cópia), ConcurrentModificationException, SequencedCollection. Colher L186-194 + L357-364.
  - Mapa (wikilinks exatos): `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/05 - Arrays e varargs|Arrays e varargs]]`, `01 - O Collections Framework`, `02 - Listas, conjuntos e filas`, `03 - Mapas`, `06 - Comparable e Comparator`, `14 - SequencedCollection e SequencedMap` (estes 5 em `[[03-Dominios/Tecnologia/Java/Collections e Streams/<arquivo>|…]]`).
  - Pegadinhas: `Arrays.asList` tamanho fixo (UnsupportedOperationException no add), init de arrays (0/null/false), view vs cópia. Linka nota 15.

### Task 2.6: Nota 10 — Domínio 6 (Streams e lambdas)
**Files:** Create `…/10 - Domínio 6 — Streams e lambdas.md`
- [ ] **Step 1: Criar.** Cobertura **Cheia**.
  - O que a Oracle cobra: lambda syntax/effectively final, method references, interfaces funcionais (Function/Predicate/Consumer/Supplier/BiFunction/UnaryOperator + primitivas), stream creation, intermediate ops (filter/map/flatMap/distinct/sorted/peek/limit/skip/takeWhile/dropWhile), terminal ops (forEach/toList/collect/reduce/count/min/max/find/match), Collectors (toMap/groupingBy/partitioningBy/joining/…), Optional, parallel streams, Gatherers. Colher L201-211.
  - Mapa (wikilinks exatos, `[[03-Dominios/Tecnologia/Java/Collections e Streams/<arquivo>|…]]`): `04 - Lambdas e interfaces funcionais`, `05 - Introdução à Stream API`, `07 - Operações de Stream — intermediárias e terminais`, `08 - Collectors e agrupamento`, `09 - Streams primitivos`, `10 - Optional`, `13 - Composição funcional e funções de alta ordem`, `15 - Collectors customizados e Gatherers`.
  - Pegadinhas: stream one-shot (IllegalStateException), peek lazy, `Optional.orElse` sempre executa vs `orElseGet`, `Collectors.toMap` chave duplicada. Linka nota 15.

### Task 2.7: Nota 12 — Domínio 8 (Concorrência)
**Files:** Create `…/12 - Domínio 8 — Concorrência.md`
- [ ] **Step 1: Criar.** Cobertura **Cheia**.
  - O que a Oracle cobra: thread creation (Thread vs Runnable, start vs run), thread states, lifecycle (sleep/join/interrupt), synchronized/volatile/wait-notify, ExecutorService (fixed/single/cached/scheduled + **newVirtualThreadPerTaskExecutor**), Callable/Future, CompletableFuture, atomics, concurrent collections, Virtual Threads (Java 21), locks (ReentrantLock/ReadWriteLock). Colher L230-246.
  - Mapa (wikilinks exatos, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/<arquivo>|…]]`): `02 - Threads e seu ciclo de vida`, `03 - Exclusão mútua com synchronized`, `06 - Atômicos e operações lock-free`, `07 - Concurrent collections`, `08 - Executors e thread pools`, `10 - CompletableFuture e composição assíncrona`, `11 - Java Memory Model em profundidade`, `12 - Virtual Threads e Project Loom`, `15 - Parallel streams e fork-join`.
  - Pegadinhas: `t.run()` não cria thread (roda no caller), `t.start()` sim. Linka nota 15.

### Task 2.8: Commit da Fase 2
- [ ] Review das 7 notas (controller checa wikilinks contra arquivos reais).
```bash
git add "03-Dominios/Tecnologia/Java/Certificação OCP/05 - Domínio 1"*.md \
        "03-Dominios/Tecnologia/Java/Certificação OCP/06 - Domínio 2"*.md \
        "03-Dominios/Tecnologia/Java/Certificação OCP/07 - Domínio 3"*.md \
        "03-Dominios/Tecnologia/Java/Certificação OCP/08 - Domínio 4"*.md \
        "03-Dominios/Tecnologia/Java/Certificação OCP/09 - Domínio 5"*.md \
        "03-Dominios/Tecnologia/Java/Certificação OCP/10 - Domínio 6"*.md \
        "03-Dominios/Tecnologia/Java/Certificação OCP/12 - Domínio 8"*.md
git commit -m "feat(java): Galho 18 — domínios de cobertura cheia (notas 05-10, 12)"
```
> Nota: o glob `"05 - Domínio 1"*.md` casa só o arquivo do galho 18 porque o controller roda do repo root e o path é específico. Conferir `git status` antes do commit para garantir que nada do bot entrou.

---

# FASE 3 — Domínios parciais (notas 11, 13, 14)

> Mesma estrutura de nota de domínio, **+ seção `## Lacuna da trilha`** (após Pegadinhas): o que o galho não cobre, conteúdo autocontido mínimo, fontes. Seam de honestidade.

### Task 3.1: Nota 11 — Domínio 7 (Empacotamento, deployment e módulos)
**Files:** Create `…/11 - Domínio 7 — Empacotamento, deployment e módulos.md`
- [ ] **Step 1: Criar.** Cobertura **Parcial**.
  - O que a Oracle cobra: JPMS (module-info: requires/exports/opens/uses/provides), tipos de módulo (named/unnamed/automatic), ServiceLoader, jlink, migração classpath→modulepath; jar/MANIFEST, jpackage, javac/java/classpath/modulepath, JShell, implicit classes & instance main methods. Colher L273-292.
  - Mapa: `[[03-Dominios/Tecnologia/Java/JVM/08 - JPMS — o sistema de módulos|JPMS — o sistema de módulos (G3)]]`, `[[03-Dominios/Tecnologia/Java/JavaFX/13 - Empacotamento — módulos, jlink e jpackage|Empacotamento — jlink e jpackage (G6)]]`, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/15 - A evolução do Java (8 a 25)|A evolução do Java (G1)]]` (p/ implicit classes/instance main).
  - `## Lacuna da trilha`: a trilha não tem nota dedicada a `jar`/`META-INF/MANIFEST.MF`, `jShell`, nem aos *implicit classes & instance main methods* como tópico de prova. Conteúdo autocontido mínimo desses 3 + fontes (docs Oracle). **JPMS pouco usado em produção mas cai muito** — estudar mesmo assim.

### Task 3.2: Nota 13 — Domínio 9 (I/O)
**Files:** Create `…/13 - Domínio 9 — I/O.md`
- [ ] **Step 1: Criar.** Cobertura **Parcial**.
  - O que a Oracle cobra: java.io (InputStream/OutputStream bytes, Reader/Writer chars), Buffered*, File*Stream/File*Reader/Writer, try-with-resources, java.nio.file (Path/Paths/Files/Files.lines/walk), serialization (Serializable/transient/serialVersionUID/ObjectI-O-Stream), Console. Colher L250-258.
  - Mapa: `[[03-Dominios/Tecnologia/Java/Collections e Streams/12 - I-O moderno com java.nio.file|I/O moderno com java.nio.file (G2)]]`.
  - `## Lacuna da trilha`: a trilha cobre `java.nio.file` mas **não** `java.io` clássico (byte/char streams, Buffered*), **nem serialização**, **nem Console** — tópicos de prova. Conteúdo autocontido mínimo dos 3 + fontes. Nota: serialização cai pouco (1-2 questões).

### Task 3.3: Nota 14 — Domínio 10 (Localização)
**Files:** Create `…/14 - Domínio 10 — Localização.md`
- [ ] **Step 1: Criar.** Cobertura **Parcial**.
  - O que a Oracle cobra: Locale (criação/getDefault), ResourceBundle (properties/fallback), NumberFormat (currency/percent/locale), DateTimeFormatter (FormatStyle SHORT/MEDIUM/LONG/FULL). Colher L221-226.
  - Mapa: `[[03-Dominios/Tecnologia/Java/Collections e Streams/11 - java.time — Date e Time API|java.time (G2)]]` (cobre DateTimeFormatter parcialmente).
  - `## Lacuna da trilha`: a trilha **não cobre** Locale/ResourceBundle/NumberFormat — domínio inteiro precisa de estudo à parte. Conteúdo autocontido mínimo + fontes. Menor peso na prova, mas cai.

### Task 3.4: Commit da Fase 3
- [ ] Review (controller checa wikilinks + que a seção "Lacuna da trilha" existe nas 3).
```bash
git add "03-Dominios/Tecnologia/Java/Certificação OCP/11 - Domínio 7"*.md \
        "03-Dominios/Tecnologia/Java/Certificação OCP/13 - Domínio 9"*.md \
        "03-Dominios/Tecnologia/Java/Certificação OCP/14 - Domínio 10"*.md
git commit -m "feat(java): Galho 18 — domínios de cobertura parcial com 'Lacuna da trilha' (notas 11, 13, 14)"
```

---

# FASE 4 — Estratégia (notas 15, 16, 17)

### Task 4.1: Nota 15 — O catálogo de pegadinhas clássicas
**Files:** Create `…/15 - O catálogo de pegadinhas clássicas.md`
- [ ] **Step 1: Criar.** Frontmatter `fase: estrategia`, aliases `["Pegadinhas OCP", "Gotchas Java"]`.
  - Catálogo (colher L402-629, expandir): cada pegadinha = subseção `###` com código mínimo + explicação + link ao domínio/galho. Lista: Integer cache, String pool vs new String/intern, `var` ambíguo, autoboxing+null→NPE, final com objeto mutável, override/overload+autoboxing (ordem exact→widening→autoboxing→varargs), static hiding ≠ override, try/finally com return, try-with-resources ordem reversa, equals/hashCode contrato, view vs cópia, switch fall-through, stream one-shot, effectively final, init de arrays, enum constructor private, generics type erasure.
  - `## Veja também` — nota 04 (mapa), notas de domínio.
  - Domínios de exemplo neutros nos snippets.

### Task 4.2: Nota 16 — Estratégia de estudo e recursos
**Files:** Create `…/16 - Estratégia de estudo e recursos.md`
- [ ] **Step 1: Criar.** Frontmatter `fase: estrategia`.
  - `## Plano de estudo` — **voz de plano** (futuro/presente: "o plano é…", "pretendo…"), 3-4 meses, reformular L633-664 tirando qualquer "fiz". Pode usar 2ª pessoa/imperativo ("revise", "faça") como guia ao leitor.
  - `## Recursos essenciais` — livro Sybex (Boyarsky & Selikoff, ISBN 9781394286614, **só p/ 1Z0-830**), Enthuware (mocks), MyExamCloud/Whizlabs. Colher L666-686 + §3 spec.
  - `## Como usar mocks` — diagnóstico, revisar todas, caderno de erros, regra "3 mocks >80% antes de marcar". Colher L688-697.
  - `## Em entrevista` — como falar do *processo de preparação* em inglês (voz honesta: "I'm preparing for the OCP… the study process reinforced X"), **não** "I have the OCP". Reformular L786-804.
  - Sem 1ª pessoa afirmando prova feita. Remover/reformular o bloco "Na prática (da minha experiência)" L753-782 → voz de plano.

### Task 4.3: Nota 17 — O dia da prova e depois
**Files:** Create `…/17 - O dia da prova e depois.md`
- [ ] **Step 1: Criar.** Frontmatter `fase: estrategia`.
  - `## Antes` / `## Durante` / `## Gestão de tempo` (50q em 90-120min — coerente com a divergência da nota 03) / `## Mentalidade`. Colher L703-729.
  - `## Depois — se passar` (CertView/Credly/LinkedIn) / `## Depois — se reprovar` (14 dias, relatório de áreas fracas). Colher L734-749.
  - `## Veja também` — notas 03, 16.

### Task 4.4: Commit da Fase 4
- [ ] Review (controller checa **voz de plano** nas 16/17 — nenhuma afirmação de prova feita/credencial obtida).
```bash
git add "03-Dominios/Tecnologia/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas.md" \
        "03-Dominios/Tecnologia/Java/Certificação OCP/16 - Estratégia de estudo e recursos.md" \
        "03-Dominios/Tecnologia/Java/Certificação OCP/17 - O dia da prova e depois.md"
git commit -m "feat(java): Galho 18 — grupo estratégia (pegadinhas, estudo, dia da prova; voz de plano)"
```

---

# FASE 5 — Integração

### Task 5.1: Podar o tronco legado a stub-hub
**Files:** Modify `03-Dominios/Tecnologia/Java/Core/Certificação Java OCP.md`
- [ ] **Step 1:** Substituir o corpo (878 linhas) por um stub-hub curto. Manter frontmatter (`publish: false`), atualizar `updated: 2026-06-13`. Adicionar callout no topo:
  ```
  > [!info] Este tronco foi podado
  > O conteúdo virou o **Galho 18 — Certificação OCP**, em notas atômicas. Comece pelo MOC: [[03-Dominios/Tecnologia/Java/Certificação OCP/index|Certificação OCP (Galho 18)]].
  ```
  Corpo: 1 parágrafo + lista de atalhos pras notas-chave (01, 04, 15). Não deletar o arquivo.
- [ ] **Step 2: Commit**
```bash
git add "03-Dominios/Tecnologia/Java/Core/Certificação Java OCP.md"
git commit -m "refactor(java): poda do tronco legado de OCP — vira stub-hub do Galho 18"
```

### Task 5.2: Ativar o galho no índice central
**Files:** Modify `03-Dominios/Tecnologia/Java/index.md`
- [ ] **Step 1:** Linha 54: trocar `18. Certificação Java OCP *(planejado)*` por:
  `18. [[03-Dominios/Tecnologia/Java/Certificação OCP/index|Certificação Java OCP]] — guia das provas OCP Java SE 21 (1Z0-830) e 25 (1Z0-831): os 10 domínios oficiais mapeados às notas dos galhos 1-4, pegadinhas clássicas, formato e estratégia de prova`
- [ ] **Step 2:** Linha 61: atualizar o item do tronco para indicar que virou o Galho 18 (apontar ao galho ativo, manter link ao tronco como legado).
- [ ] **Step 3:** Atualizar `updated: 2026-06-13` no frontmatter.
- [ ] **Step 4: Commit**
```bash
git add "03-Dominios/Tecnologia/Java/index.md"
git commit -m "feat(java): ativa Galho 18 (Certificação OCP) no MOC central — trilha completa"
```

### Task 5.3: Expandir o Dicionário de Java
**Files:** Modify `03-Dominios/Tecnologia/Java/Dicionário de Java.md`
- [ ] **Step 1: Grep cada termo candidato** antes de inserir (linkar se já existe, não duplicar):
  ```bash
  for t in OCP OCA "1Z0-830" "1Z0-831" "exam objective" "passing score" "online proctored" voucher Enthuware CertView Credly "Pearson VUE"; do
    echo "== $t =="; grep -in "$t" "03-Dominios/Tecnologia/Java/Dicionário de Java.md" | head -3
  done
  ```
- [ ] **Step 2:** Inserir os verbetes ausentes em ordem alfabética na seção da letra correta (formato `### Termo` + definição curta + wikilink ao galho/notas). Linkar verbetes a termos já existentes (ex.: Integer cache, type erasure provavelmente já existem — só referenciar).
- [ ] **Step 3:** Atualizar `updated: 2026-06-13`.
- [ ] **Step 4: Commit**
```bash
git add "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
git commit -m "feat(java): expande Dicionário com verbetes de certificação OCP (Galho 18)"
```

---

# FASE 6 — Validação

### Task 6.1: Validar wikilinks programaticamente
- [ ] **Step 1: Grep de cada wikilink de destino** das notas do galho contra arquivos reais. Para cada `[[03-Dominios/Tecnologia/Java/.../<arquivo>|...]]`, confirmar que `03-Dominios/Tecnologia/Java/.../<arquivo>.md` existe:
  ```bash
  cd /home/josenaldo/repos/personal/codex-technomanticus
  grep -rhoE '\[\[03-Dominios/Tecnologia/Java/[^|]+' "03-Dominios/Tecnologia/Java/Certificação OCP/" \
    | sed -E 's/^\[\[//' | sort -u \
    | while IFS= read -r p; do [ -f "${p}.md" ] || echo "QUEBRADO: $p"; done
  ```
  Expected: nenhuma linha "QUEBRADO". Corrigir os que aparecerem (provável causa: título alucinado — conferir contra §7 do spec).
- [ ] **Step 2: Rodar a skill `verificar-wikilinks`** na pasta `03-Dominios/Tecnologia/Java/Certificação OCP/` e no `index.md` central. Corrigir o que apontar.

### Task 6.2: Review final e commit de fechamento
- [ ] **Step 1:** Conferir: 17 notas + index existem; dataview do MOC lista as 17; nenhuma afirmação de prova feita; divergência de duração registrada; os 3 domínios parciais têm "Lacuna da trilha".
  ```bash
  ls "03-Dominios/Tecnologia/Java/Certificação OCP/" | wc -l   # esperado: 18 (17 notas + index)
  ```
- [ ] **Step 2:** Se houve correções nas Tasks 6.1, commit:
```bash
git add "03-Dominios/Tecnologia/Java/Certificação OCP/" "03-Dominios/Tecnologia/Java/index.md"
git commit -m "fix(java): corrige wikilinks do Galho 18 e fecha a trilha Java (18/18 galhos)"
```
- [ ] **Step 3:** Reportar ao usuário: trilha Java completa (18/18). **Não fazer push** (manual).

---

## Self-review (preenchido)

- **Cobertura do spec:** §2 decisões → Fases 0-6; §3 fatos → notas 02/03/05-14; §4 mapa de notas → Tasks 0.1-4.3; §5 estrutura → skeletons; §6 integração → Fase 5; §7 wikilinks → embutidos + Fase 6; §8 regras → Notas operacionais; §9 sequência → Fases. ✔
- **Placeholders:** skeletons referenciam fatos/linhas concretas do tronco e títulos exatos do §7; sem TBD. ✔
- **Consistência:** nomes de arquivo idênticos entre File Structure, wikilinks e comandos de commit; `fase:` consistente (sobre-a-prova/dominios/estrategia). ✔
- **Pendência conhecida (aceita):** snippets de código dentro das notas serão escritos pelos subagentes a partir do tronco (que já tem os exemplos) — o plano aponta as linhas-fonte em vez de repetir todo o código, dado o volume (17 notas). Aceitável para galho de conteúdo.
