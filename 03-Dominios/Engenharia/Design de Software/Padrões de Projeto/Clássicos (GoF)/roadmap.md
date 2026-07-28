---
title: "Roadmap — Clássicos (GoF)"
created: 2026-07-28
type: meta
publish: false
tags:
  - meta
  - roadmap
  - design-de-software
  - design-patterns
  - gof
---

# Roadmap — Clássicos (GoF) (galho-folha, construção)

Roadmap da família `03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Clássicos (GoF)`. Galho-**folha em modo construção**: uma entrada por nota **a escrever** (não é diagnóstico de notas existentes). Pai: [[Padrões de Projeto/roadmap|Padrões de Projeto]]. Matéria-prima: o monólito [[Design Patterns]] (631 ln).

## Escopo desta família

Os **23 padrões do Gang of Four** (Gamma, Helm, Johnson, Vlissides, 1994), organizados como catálogo de consulta com a **lente cross-linguagem** (Java · TypeScript · Python · Go) e peso no **quando NÃO usar**. Os 4 padrões genuinamente raros (Bridge, Flyweight, Memento, Interpreter) vão numa nota única. Padrões de acesso a dados, integração, apresentação, eventos e nuvem **não** entram aqui — são famílias irmãs (ver roadmap-pai).

## Anatomia de cada nota de padrão

Padrão "capítulo de livro" (nota que pega o leitor pela mão; ~substancial com Mermaid; sem padding):

1. **TL;DR** `[!abstract]` (1-3 linhas: o que resolve).
2. **Abertura-problema** — o cenário que dói *antes* do padrão.
3. **A ideia** — o mecanismo, com **Mermaid** (classe/sequência) onde ajuda.
4. **Os 4 idiomas lado a lado** — Java · TS · Python · Go. Exemplo trabalhado, não snippet solto.
5. **Como a linguagem muda o padrão** — recursos que encolhem/dissolvem (funções 1ª classe, structural typing, embedding, enums/records, pattern matching, sealed types).
6. **Quando a linguagem torna o padrão desnecessário** — o "não precisa disso aqui".
7. **Armadilhas** `[!warning]` **(seção recheada)** — quando NÃO usar · os usos mais equivocados · o custo de aplicar cedo demais · abstração prematura.
8. **Como explicar em inglês** — quote + tabela PT↔EN.
9. **O que vem a seguir** — ponte pra próxima nota da sequência.
10. **Fontes** — GoF, Refactoring Guru, Effective Java, docs das 4 linguagens (com URL).

**Esquema de `fase:`:** COM fase, por **centralidade/frequência** do padrão (não gate de aprendizado). Iniciado = os que todo dev encontra primeiro; Adepto = catálogo de trabalho; Magus = situacionais + síntese sênior.
**Piso de linhas:** flexível — o padrão capítulo substitui o piso rígido; padrões simples podem ser mais curtos, sustentados pela comparação cross-linguagem.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Notas de conteúdo | 23 |
| Iniciado | 6 |
| Adepto | 12 |
| Magus | 5 |
| ✅ escritas | 6 |
| ⬜ pendentes | 17 |
| % concluído | 26% |
| Scaffolding | index.md criado (2026-07-28) |

---

## Notas — Iniciado (fundamentos + criacionais)

#### 01 - O que são Design Patterns   [substantivo]
- **Estado:** ✅ escrita (2026-07-28) · fase: iniciado · 224 linhas
- **Escopo:** vocabulário (não código pra copiar); GoF 1994; as 3 categorias; patterns num mundo de frameworks; **a lente do galho** (4 idiomas + "quando a linguagem dissolve o padrão"); como usar o catálogo. Mermaid do mapa das 3 categorias.
- **Resultado:** verificar-nota 10/12 aplicáveis ✓ (E4/P1 N/A; M1 opcional Iniciado); Mermaid ok; tese ilustrada com exemplo Strategy nos 4 idiomas; tabela-fronteira das 6 famílias; 3 armadilhas. Aprovada no padrão-capítulo (T1 cede à régua de qualidade).

#### 02 - Singleton   [substantivo]
- **Estado:** ✅ escrita (2026-07-28) · fase: iniciado · 222 linhas
- **Escopo:** instância única; **o mais controverso** (estado global disfarçado). Java: enum idiomático vs static final. Python/Go: **module/package-level var** (o idioma já dá singleton). Framework: `@Service` scope. **Armadilha central:** singleton mutável = estado global; esconde dependências; mata testabilidade → prefira DI.
- **Resultado:** 4 idiomas (enum/holder Java · módulo Python/TS · sync.Once Go); Mermaid do contraste dep-escondida×injeção; 4 armadilhas; DI como substituto. Aprovada no padrão-capítulo.

#### 03 - Factory Method   [substantivo]
- **Estado:** ✅ escrita (2026-07-28) · fase: iniciado · 183 linhas
- **Escopo:** delegar *qual classe* instanciar. Funções de 1ª classe encolhem (Python/TS/Go passam função). Go: `func New...`. Spring: `Map<String,Impl>`. **Armadilha:** factory com um só tipo; factory que só chama construtor.
- **Resultado:** distinção Factory Method×Simple×Abstract; 4 idiomas (switch Java · dict Python · New Go · registry TS); Mermaid cliente→interface; Spring Map+OCP; 3 armadilhas. Aprovada.

#### 04 - Abstract Factory   [substantivo]
- **Estado:** ✅ escrita (2026-07-28) · fase: iniciado · 180 linhas
- **Escopo:** famílias de objetos relacionados. Raro em backend; onde sobrevive (temas de UI, drivers de banco, ambientes). **Armadilha:** fábrica-de-fábricas sem necessidade (YAGNI); confundir com Factory Method.
- **Resultado:** honesto sobre raridade em backend; 4 idiomas (interface Java/Go · módulo Python · objeto TS); Mermaid 2 famílias coerentes; fraqueza "novo produto quebra todas as fábricas"; 3 armadilhas. Aprovada.

#### 05 - Builder   [substantivo]
- **Estado:** ✅ escrita (2026-07-28) · fase: iniciado · 174 linhas
- **Escopo:** objeto complexo passo a passo; resolve o construtor de 10 parâmetros. Java: `@Builder`/`record` + `with`. Python: **kwargs/dataclass** (o idioma já resolve). TS: object literal + tipos. Go: **functional options**. **Armadilha:** builder pra objeto de 2 campos.
- **Resultado:** o caso mais didático da tese; 4 idiomas; Mermaid problema→(Builder | recurso da linguagem); 3 armadilhas (build() inválido, reinventar onde há named args). Aprovada.

#### 06 - Prototype   [substantivo]
- **Estado:** ✅ escrita (2026-07-28) · fase: iniciado · 164 linhas
- **Escopo:** criar clonando. **Shallow vs deep** em cada idioma: Java `clone()`/copy ctor, TS `structuredClone`/spread, Python `copy`/`deepcopy`, Go cópia de struct/manual. **Quase-obsoleto** com imutabilidade + `with...()`. **Armadilha:** clone raso silencioso.
- **Resultado:** foco raso×profundo (Mermaid referências compartilhadas×independentes); 4 idiomas; imutabilidade+`with` como substituto; 3 armadilhas (aliasing, Cloneable quebrado). Aprovada. **Fecha o bloco Iniciado (01-06).**

## Notas — Adepto (estruturais + comportamentais de trabalho)

#### 07 - Adapter   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** casar interfaces; ponte legado/terceiros; base de Ports & Adapters. **Structural typing** (Go/TS) muda a necessidade de declarar o adaptador. Exemplo: wrapper de SDK (Stripe). **Armadilha:** adapter que vaza o vocabulário que deveria esconder.
- **Resultado:** —

#### 08 - Decorator   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** comportamento em runtime por composição (vs herança). **Decorators nativos**: Python `@`, TS (experimental/stage 3). Go: **embedding**. Java: I/O streams. **Armadilha:** pilha profunda ilegível; confundir decorator de linguagem com o padrão.
- **Resultado:** —

#### 09 - Facade   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** API simplificada sobre subsistema; **todo `@Service` orquestrador é uma Facade** — o padrão mais usado sem se perceber. **Armadilha:** God Facade que vira God Object.
- **Resultado:** —

#### 10 - Proxy   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** controlar acesso (lazy/cache/log/remoto/segurança). AOP: `@Transactional`/`@Cacheable`; lazy JPA; JDK dynamic proxy vs CGLIB. Go: sem proxies dinâmicos → geração/wrappers explícitos. **Pegadinha clássica:** `@Transactional` em chamada interna (`this.m()`) não intercepta.
- **Resultado:** —

#### 11 - Composite   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** árvore parte-todo; cliente trata folha e composto igual. Casos: filesystem, UI, AST, expressões. **Armadilha:** aplicar onde recursão simples/lista basta.
- **Resultado:** —

#### 12 - Strategy   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** **o exemplo-ouro de "vira função"**. Java: interface ou lambda. Python/Go/TS: passar função de 1ª classe. Spring: `Map<String,Strategy>`. **Armadilha central:** interface Strategy com **uma só implementação** e nenhuma perspectiva de segunda = abstração prematura.
- **Resultado:** —

#### 13 - Observer   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** dependência 1-para-N; base de event-driven. Spring Events, Node `EventEmitter`, DOM, Reactive (Reactor/RxJS). **Armadilha:** listener sem unsubscribe = memory leak; evento síncrono na thread da transação.
- **Resultado:** —

#### 14 - Command   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** requisição como objeto → enfileirar, logar, undo/redo. CQRS. Funções/closures encolhem em linguagens funcionais. **Armadilha:** cerimônia de Command onde um método direto basta.
- **Resultado:** —

#### 15 - Template Method   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** esqueleto + hooks via herança. **Go não tem herança** → embedding/funcs. Substituível por composição + lambdas no Java moderno. **Armadilha:** hierarquia rígida onde composição serviria melhor.
- **Resultado:** —

#### 16 - State   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** comportamento muda com estado interno. Vs máquina de estados com **enum**; **union types** (TS), **sealed** (Java 21). **Armadilha:** State pattern onde um enum + switch resolve; over-engineering de FSM simples.
- **Resultado:** —

#### 17 - Chain of Responsibility   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** cadeia de handlers; **a base de todo pipeline HTTP** (servlet filters, Spring Security, Express/Nest middleware). **Armadilha:** cadeia onde ninguém trata (buraco silencioso); ordem implícita frágil.
- **Resultado:** —

#### 18 - Iterator   [mecânico]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** acesso sem expor a interna; **nativo em toda linguagem moderna**: Java `Iterator`/`Iterable`, JS/TS `for...of`/`Symbol.iterator`, Python `__iter__`/generators, Go `range`-over-func (1.23). Raramente implementado à mão. **Armadilha:** reimplementar o que a linguagem já dá.
- **Resultado:** —

## Notas — Magus (situacionais + síntese sênior)

#### 19 - Mediator   [substantivo]
- **Estado:** ⬜ a escrever · fase: magus
- **Escopo:** encapsula interações N-para-N; reduz acoplamento direto. Command bus, MediatR (.NET), `ApplicationEventMulticaster`. **Armadilha:** o mediator vira **God Object** que sabe demais.
- **Resultado:** —

#### 20 - Visitor   [substantivo]
- **Estado:** ⬜ a escrever · fase: magus
- **Escopo:** **o caso-ouro da lente cross-linguagem.** Operações sobre estrutura sem tocar os tipos; double dispatch. **Pattern matching / sealed types matam o Visitor clássico**: Java 21+ `switch` sobre sealed, Kotlin `when`, Scala `match`, Python `singledispatch`/match, Go type switch. Onde sobrevive (AST/compiladores). **Armadilha:** Visitor cerimonioso onde o `switch` sobre tipo selado é mais claro.
- **Resultado:** —

#### 21 - Padrões raros (Bridge · Flyweight · Memento · Interpreter)   [substantivo]
- **Estado:** ⬜ a escrever · fase: magus
- **Escopo:** os 4 do GoF que o monólito só citou. O que são, **por que são raros hoje**, e onde ainda aparecem: Flyweight (pools, string interning, sprites), Memento (undo/snapshots, event sourcing encosta), Interpreter (DSLs, engines de regex/regra), Bridge (drivers, abstração×implementação). Nota-catálogo honesta, sem padding.
- **Resultado:** —

#### 22 - Reconhecer GoF nos frameworks   [substantivo]
- **Estado:** ⬜ a escrever · fase: magus
- **Escopo:** a tabela "onde você já usa" — `@Transactional`=Proxy, `@Service`=Facade, `@EventListener`=Observer, `JpaRepository`=Repository, `JdbcTemplate`=Template Method, DI=IoC. **Reconhecer > reimplementar.** Vale pra debugar (saber que é proxy, não mágica). *Pode graduar a capstone do galho-pai quando houver outras famílias (ver roadmap-pai).*
- **Resultado:** —

#### 23 - Quando NÃO usar: anti-patterns e discernimento sênior   [substantivo]
- **Estado:** ⬜ a escrever · fase: magus
- **Escopo:** síntese do "quando não usar" espalhado pelo galho — Pattern mania, Golden Hammer, abstração prematura, Singleton pra tudo, reimplementar o que o framework faz, confundir padrão com arquitetura. + **inglês/entrevista** consolidado (frases prontas, vocabulário PT↔EN, o "premature abstraction is as bad as no abstraction"). *Candidata a capstone do galho-pai.*
- **Resultado:** —

---

## Próximos passos

1. ⬜ Escrever 01 → 23 na ordem, via `/escrever-nota`. `/checkpoint` a cada bloco de fase (após 06, após 18, após 23).
2. ⬜ Criar `index.md` da família (MOC com seções por fase + rotas + dataview) — ao ter ≥ bloco Iniciado escrito.
3. ⬜ Ao fechar 23: podar o monólito [[Design Patterns]] (preservar 8 inbound links) e atualizar roadmap-pai + [[00-Meta/Roadmap]] central.
