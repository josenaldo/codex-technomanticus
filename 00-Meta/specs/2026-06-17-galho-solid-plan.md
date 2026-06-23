---
title: "Galho SOLID — design e plano (Fundamentos, Camada A)"
created: 2026-06-17
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - solid
---

# Galho SOLID — design e plano

## Contexto
Galho **spin-off do galho Orientação a Objetos** (`2026-06-17-galho-orientacao-a-objetos-plan.md`),
aprovado pelo usuário em 2026-06-17: SOLID sai do galho OO e vira galho próprio, irmão sob
`03-Dominios/Ciência/`. Isso **altera o meta-plano**: a Camada A passa de 6 → 7 galhos
(ED, Algoritmos, OO, **SOLID**, Banco, Redes, Testes). Interview-critical (★).

A semente de conteúdo é a seção **SOLID** do monólito `Orientação a Objetos.md` (os 5 princípios já
escritos, com exemplos Java). O monólito só é removido depois que ESTE galho e o galho OO estiverem
ambos migrados.

## Fronteiras (rígido)
- **Acoplamento e coesão** fica no galho OO (nota 08, `Acoplamento e coesão`) — é design-OO
  fundacional, anterior a SOLID. Este galho **forward-linka** pra lá (SRP↔coesão, DIP↔acoplamento),
  não duplica.
- **SOLID aplicado à arquitetura** já existe em `[[Arquitetura de Software]]` (seção própria). Este
  galho é dono do SOLID **nível-objeto/classe**; o capstone (08) linka pra Arquitetura para o
  nível-módulo/serviço. Regra anti-duplicação: linka, não copia.
- **Design Patterns** → o OCP e o DIP usam patterns como exemplo (Strategy, Factory); **linkar**
  `[[Design Patterns]]`, não ensinar o catálogo.
- **DI/IoC e Spring** → a nota 07 trata DI/IoC como conceito OO-agnóstico de framework; o container
  Spring entra como exemplo, linkando a estante Java/Spring (`[[Spring Boot]]` / `[[Spring]]`) sem
  duplicar a mecânica de beans.

## Preservação (rígido)
Experiência REAL do usuário, relocada do monólito ([[feedback-no-fabrication]]):
- **MedEspecialista — NotificationSender**: interface com implementações email/SMS/push; adicionar
  WhatsApp foi classe nova (zero mudança no consumidor = OCP); `FakeSender` em memória deixou a
  suíte rápida e determinística (DIP testável). → **nota 07 (DIP na prática: DI e IoC)**, com
  referência cruzada do OCP (nota 03).

## Roster de notas (8 base; pode crescer/encolher por split)

### Iniciado — o princípio e os dois primeiros
1. **O que é SOLID** — cinco heurísticas (não dogma), história (Robert C. Martin / Uncle Bob),
   o acrônimo, a meta comum (baixo acoplamento + alta coesão, código flexível/testável/evolutivo);
   "não são regras religiosas — são heurísticas cujas exceções você deve conhecer". Forward-link
   `[[Acoplamento e coesão]]` (galho OO).
2. **SRP — Responsabilidade Única** — "uma única razão para mudar"; eixos de mudança (persistência
   ≠ negócio ≠ notificação); não é "uma classe, uma função"; relação com coesão.
3. **OCP — Aberto/Fechado** — aberto para extensão, fechado para modificação; o switch que cresce
   vs polimorfismo (cada caso = nova classe); linka `[[Design Patterns]]` (Strategy). *(referencia a
   exp NotificationSender da nota 07 como OCP na prática)*

### Adepto — os três últimos
4. **LSP — Substituição de Liskov** — subtipos substituíveis sem quebrar comportamento esperado;
   design by contract (pré/pós-condições, invariantes); Rectangle/Square; sinais de violação
   (`UnsupportedOperationException`, checagem de tipo concreto, Refused Bequest).
5. **ISP — Segregação de Interfaces** — nenhum cliente depende de métodos que não usa; várias
   interfaces pequenas (capacidades) vs uma grande; relação com coesão de interface.
6. **DIP — Inversão de Dependência** — módulos de alto e baixo nível dependem de abstrações; a
   inversão da seta de dependência; abstração não pertence a quem implementa, e sim a quem consome.

### Magus — aplicação e crítica
7. **DIP na prática: DI e IoC** — injeção de dependência (constructor/setter/field), Inversão de
   Controle, containers (Spring como exemplo, link à estante Java); por que torna testável (fakes/
   mocks). *(recebe exp REAL: MedEspecialista NotificationSender)*
8. **SOLID em xeque (capstone)** — quando SOLID atrapalha: over-engineering, interface com uma só
   implementação "pro futuro" (YAGNI), SOLID vs simplicidade (crítica de Ousterhout, *A Philosophy
   of Software Design*: muitas classes pequenas podem aumentar complexidade); SOLID aplicado à
   arquitetura (link `[[Arquitetura de Software]]`); em entrevista ("como aplicou DIP recentemente?")
   + frases em inglês + vocabulário; cheat-sheet dos 5.

## Padrão por nota (idêntico ao galho OO)
- Feynman didático, profundo à medida do tema; teto 2400 (permissão, código não conta).
- **Diagramas Mermaid** onde ajudam (seta de dependência invertida no DIP, hierarquia LSP, switch→
  polimorfismo no OCP, interface gorda→segregada no ISP). Lead-in + "leitura do diagrama". **Sem
  `xychart-beta`.** Símbolos literais na prosa; entidades HTML só em rótulos Mermaid entre aspas.
- **Seção "Em entrevista"** (interview-critical) — frases em inglês + vocabulário.
- Fontes verificadas; callout "Lastro".
- Atomicidade: linka vizinhas em vez de duplicar. `NN - Título.md` flat.
- `publish: false` nas notas; `publish: true` só no `index.md`. Frontmatter `fase:`, tags.

## Tronco e MOC
- Pasta `03-Dominios/Engenharia/SOLID/` com `index.md` (MOC, `type: moc`, `publish: true`,
  agrupado por fase, rota de entrevista, dataview, "Veja também").
- Alias do `index.md`: **"SOLID"** (+ "Princípios SOLID", "SOLID Principles") para resolver links de
  entrada (Arquitetura de Software, Java, etc. referenciam SOLID).
- A entrada SOLID entra no MOC do domínio (`Fundamentos/index.md` e `Fundamentos.md`).

## Convenções de execução
- Subagent-driven, um subagente por nota, escrita em UMA chamada Write.
- Commits direto na main, SEM push, SEM Co-Authored-By ([[feedback-commits]]).

## Sequência de construção
1. (Após o galho OO) Scaffold `SOLID/index.md` + alias.
2. Registrar a entrada SOLID no MOC do domínio.
3. Escrever as notas Iniciado (1–3), Adepto (4–6), Magus (7–8), uma por subagente. Migrar os 5
   princípios do monólito; relocar a exp NotificationSender → 07.
4. Remover o monólito `Orientação a Objetos.md` (ambos os galhos migrados); `verificar-wikilinks`;
   fechar MOCs; atualizar memória.
