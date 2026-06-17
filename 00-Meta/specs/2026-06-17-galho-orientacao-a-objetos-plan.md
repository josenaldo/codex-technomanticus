---
title: "Galho Orientação a Objetos — design e plano (Fundamentos, Camada A)"
created: 2026-06-17
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - orientacao-a-objetos
---

# Galho Orientação a Objetos — design e plano

## Contexto
Terceiro galho da **Camada A** do meta-plano de Fundamentos
(`00-Meta/specs/2026-06-15-fundamentos-meta-planejamento-design.md`): refatorar o monólito
`03-Dominios/Fundamentos/Orientação a Objetos.md` (554 linhas) numa sub-trilha de notas atômicas
em 3 fases. Interview-critical (★, Fase 1 da Senda Entrevistas). Mesmo padrão tronco/galhos dos
galhos Complexidade de Software, Estruturas de Dados (ED) e Algoritmos.

**Spin-off aprovado:** SOLID **sai do galho OO e vira galho próprio** (irmão sob `Fundamentos/`).
Ver `2026-06-17-galho-solid-plan.md`. Consequência: o meta-plano passa de 6 → 7 galhos na Camada A,
e a experiência real "MedEspecialista NotificationSender (DIP+OCP+FakeSender)" do monólito vai para
o galho SOLID, não para OO.

## Decisões deste galho (2026-06-17)

1. **4 linguagens NÃO é obrigação (decisão do usuário, revertendo ED).** Diferente de ED (coluna
   Java/TS/Python/Go em toda estrutura), aqui **cada nota usa a linguagem que melhor ilustra o
   conceito** — Python para MRO e duck typing, Go para embedding e interfaces estruturais, Java
   para `equals`/`hashCode` e o OO clássico, TS para tipagem estrutural e `#`. Sem coluna-de-4
   forçada; sem padding. A nota 11 ("Como o modelo OO difere entre linguagens") existe porque o
   *tema* é a divergência cross-language (não como síntese de um thread mecânico).
2. **Teto de prosa = 2400 linhas SÓ NESTE GALHO** (permissão, não alvo; código NÃO conta) — igual
   ED/Algoritmos, por consistência. Com o 4-lang desobrigado, as notas aterrissam naturalmente
   ~400–900 de prosa; herança, interfaces e a nota cross-language podem ir mais fundo. Teto é
   liberdade pra aprofundar onde o tema pede, nunca licença pra padding.
3. **Fronteiras (rígido):**
   - **Design Patterns** → OO ensina o *material bruto* (composição+polimorfismo = Strategy;
     hook de herança = Template Method) e **linka** `[[Design Patterns]]`; NUNCA o catálogo GoF.
   - **DDD** → corte limpo. OO fica com a **modelagem tática de objeto**: Entity vs Value Object
     (identidade/igualdade), imutabilidade, Rich vs Anemic, Tell Don't Ask. O **DDD estratégico**
     (Aggregate, Bounded Context, Ubiquitous Language, Domain Event, Repository-como-pattern) mora
     em `[[Arquitetura de Software]]` (já existe lá) — OO só forward-linka. A seção DDD grande do
     monólito é **partida**: metade tática fica (notas 09–10), metade estratégica vira link.
   - **SOLID** → galho próprio (`2026-06-17-galho-solid-plan.md`). OO mantém `Acoplamento e coesão`
     (nota 08, design-OO fundacional anterior a SOLID); o galho SOLID forward-linka pra ela.
   - **Paradigmas (galho 7, futuro)** → seam. Galho 7 = *por que* escolher OO vs FP vs procedural
     vs lógico (survey comparativo). Galho OO = *como fazer OO bem* (assume você já está em OO). O
     ponto "OO é ferramenta, não religião / às vezes uma função pura é melhor" fica **leve no
     capstone (13)** com forward-link a galho 7; a comparação FP↔OO completa mora no galho 7.

## Preservação (rígido)
A seção **"Na prática (da minha experiência)"** do monólito tem experiências REAIS do usuário.
**Relocar, NUNCA refazer/fabricar** ([[feedback-no-fabrication]]):
- **MedEspecialista — NotificationSender** (interface com email/SMS/push, WhatsApp = classe nova,
  FakeSender em testes; DIP+OCP) → **vai pro galho SOLID, nota 07 (DI/IoC)**.
- **Anemic → Rich** (início de carreira: services gigantes + entidades anêmicas; hoje regra
  "pedido só aprova se pendente e dentro do limite" dentro de `Pedido.aprovar()`) → **nota 10
  (Rich vs Anemic Domain Model)**.
- **Digidados — hierarquia de 4 níveis de `Report`** virou pesadelo → refatorada para composição
  (`ReportBuilder` com `HeaderStrategy`/`BodyStrategy`/`FooterStrategy`) → **nota 07 (Composição
  sobre herança)**.

O bloco **"How to explain in English"** + frases de pivô + vocabulário bilíngue do monólito →
**capstone (13)**. Recursos (livros/artigos) → capstone (13) + por nota onde couber.

## Roster de notas (13 base; pode crescer por split)

### Iniciado — objetos, classes e os pilares
1. **O que é Orientação a Objetos** — objeto (estado/comportamento/identidade), mensagens (Alan Kay)
   vs classes (mainstream Java/C++), classe/objeto/instância, OO como *um* paradigma (forward-link
   galho 7). *(intro mais leve)*
2. **Encapsulamento** — esconder estado, interface pública, invariantes, getter/setter como
   anti-encapsulamento (encapsulamento falso). Visibilidade onde ilustra (Java `private`/`protected`,
   Python `_`/`__` name mangling, TS `#`, Go por pacote/capitalização).
3. **Abstração** — modelar pelo que faz, não como; níveis de abstração; ADT; abstração ≠ interface.
   *(mais leve; flag: fundir com 02 se ficar fina)*
4. **Herança** — is-a, super/subclasse, override, fragile base class, acoplamento forte; hierarquias
   rasas. Python MRO/C3 + `super()` e Go embedding (não-herança) onde ilustram. *(candidata a split:
   conceito + variações por linguagem)*
5. **Polimorfismo** — subtipo/late binding (dynamic dispatch, vtable), paramétrico (generics),
   ad-hoc (overload). Duck typing (Python) e interfaces estruturais (Go) onde ilustram.

### Adepto — interfaces, composição e design
6. **Interfaces e classes abstratas** — contrato vs implementação parcial; tabela comparativa;
   **tipagem nominal vs estrutural** (conceito-âncora: Java/Python nominal, Go/TS estrutural;
   Python ABC/Protocol).
7. **Composição sobre herança** — has-a vs is-a, delegação, por que herança é perigosa, quando
   herança serve (template method, hierarquia de domínio estável, frameworks); Go embedding. Linka
   `[[Design Patterns]]` (Strategy/Decorator). *(recebe exp REAL: Digidados Report 4-níveis → Strategy)*
8. **Acoplamento e coesão** — coupling/cohesion (queremos baixo/alta), tipos de acoplamento, Law of
   Demeter, Tell Don't Ask, Feature Envy. Forward-link ao galho SOLID (SRP↔coesão, DIP↔acoplamento).

### Magus — modelagem rica, paradigma e síntese
9. **Identidade, igualdade e imutabilidade** — Entity vs Value Object (identidade), contrato
   equals/hashCode (e `__eq__`/`__hash__`, `==` em Go), imutabilidade (Java `record`, Python frozen
   dataclass, TS `readonly`); vantagens (thread-safe, raciocínio, hashable estável).
10. **Rich vs Anemic Domain Model** — comportamento junto dos dados; Anemic como procedural
    disfarçado; Tell Don't Ask aplicado; forward-link DDD estratégico → `[[Arquitetura de Software]]`.
    *(recebe exp REAL: fat services → Rich Domain Model)*
11. **Como o modelo OO difere entre linguagens** — Go composition-only (sem herança, interfaces
    implícitas), Python múltipla herança + MRO, JS class-based vs prototype-based, nominal vs
    estrutural; tabela de contrastes. *(o tema é a divergência; pega o leitor senior de surpresa)*
12. **Anti-patterns de OO** — God Class, Anemic, Feature Envy, Primitive Obsession, Refused Bequest,
    Yo-yo, Shotgun Surgery, Circular Dependency, Leaky/Exposed Internals; sintoma → causa → correção.
13. **OO na prática e em entrevista (capstone)** — OO como ferramenta não religião (seam c/ galho 7,
    YAGNI/over-engineering), armadilhas de entrevista (recitar sem contexto, herança a qualquer
    custo, interface↔classe abstrata), "How to explain in English" + frases de pivô + vocabulário
    bilíngue, recursos (livros/artigos), cheat-sheet.

## Padrão por nota (herdado de Complexidade + ED + Algoritmos)
- Profunda, à profundidade que o assunto exigir; registro **Feynman** didático (analogias,
  perguntas retóricas, resumo em 1 linha). Teto 2400 (permissão), código não conta.
- **Diagramas Mermaid** (3–5 por nota) onde ajudam (hierarquia de classes, dispatch dinâmico,
  composição vs herança, fluxo de mensagens, nominal vs estrutural). Cada diagrama com lead-in +
  "leitura do diagrama". **NÃO usar `xychart-beta`** (não renderiza no Obsidian — usar tabela ou
  flowchart). Parênteses/símbolos LITERAIS na prosa; entidades HTML SÓ dentro de rótulos Mermaid,
  sempre entre aspas.
- **Seção "Em entrevista"** (galho interview-critical) — frases prontas em inglês + vocabulário.
- Fontes verificadas na web para afirmações factuais; callout "Lastro" de honestidade.
- **Atomicidade:** cada nota linka as vizinhas em vez de duplicar. Notas `NN - Título.md` flat.
- `publish: false` nas notas; `publish: true` só no `index.md` (convenção de Fundamentos).
- Frontmatter com `fase: iniciado|adepto|magus`, tags.

## Tronco e MOC
- Criar pasta `03-Dominios/Fundamentos/Orientação a Objetos/` com `index.md` (MOC, `type: moc`,
  `publish: true`, agrupado por fase, rotas alternativas, dataview, "Veja também").
- O `index.md` recebe **alias "Orientação a Objetos"** (+ "Orientação a objetos", "OO",
  "Object-Oriented Programming") para que os 13 links de entrada existentes resolvam (README,
  Senda Entrevistas, Senda Python, Helsinki MOOC, Java Fundamentals, Design Patterns, Arquitetura
  de Software, Testes, Complexidade/05/06/07, Fundamentos/index, Fundamentos.md, index raiz).
- Migrar o conteúdo do monólito para as notas atômicas; o monólito só é **removido** depois que
  AMBOS os galhos (OO e SOLID) estiverem migrados — a seção SOLID dele é a semente do galho SOLID.
- Atualizar o MOC do domínio (`Fundamentos/index.md` e `Fundamentos.md`): a entrada de Orientação a
  Objetos passa a apontar para o `index` do galho; adicionar entrada para o galho SOLID.

## Convenções de execução
- Feynman didático; fontes/honestidade onde houver afirmação factual.
- **Subagent-driven:** um subagente por nota (profundo, Feynman, diagramas), escrita em UMA chamada
  Write pra evitar timeout.
- Commits **direto na main**, **SEM push**, **SEM Co-Authored-By** ([[feedback-commits]]).

## Sequência de construção
1. Scaffold `index.md` do galho OO (MOC, esqueleto das 13 entradas) + alias.
2. Atualizar MOC do domínio para apontar ao galho OO (e registrar o galho SOLID).
3. Escrever as notas Iniciado (1–5), Adepto (6–8), Magus (9–13), uma por subagente.
4. Relocar as experiências reais (Digidados → 07, Anemic→Rich → 10; NotificationSender vai pro SOLID).
5. Construir o galho SOLID (spec próprio) na mesma sessão.
6. SÓ ENTÃO remover o monólito; `verificar-wikilinks`; fechar MOCs em `growing`; atualizar memória.
