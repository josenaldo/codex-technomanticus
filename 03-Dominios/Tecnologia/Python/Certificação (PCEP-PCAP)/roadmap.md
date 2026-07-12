---
title: "Roadmap — Python Certificação (PCEP/PCAP)"
created: 2026-07-12
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Certificação PCEP/PCAP (galho 19, ÚLTIMO da trilha)

Roadmap-folha do galho `Python/Certificação (PCEP-PCAP)`. Fase **Magus**. Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. Pendência transversal do roadmap-pai já cumprida: "pesquisar PCEP/PCAP no momento de abrir o galho, não antes" — pesquisa feita via WebSearch em 2026-07-12, ver fontes abaixo.

**Pesquisa PCEP/PCAP (2026-07-12, WebSearch, fontes pythoninstitute.org):**

- **PCEP-30-02** (Certified Entry-Level Python Programmer), status Live & Active. 30 itens, 4 blocos: (1) Computer Programming and Python Fundamentals — 7 itens/18%; (2) Control Flow – Conditional Blocks and Loops — 8 itens/29%; (3) Data Collections – Tuples, Dictionaries, Lists, and Strings — 7 itens/25%; (4) Functions and Exceptions — 8 itens/28%. Nota mínima: 70% cumulativo. Tempo de prova não confirmado na fonte oficial (fontes terceiras citam ~40-45min, não confiável).
- **PCAP-31-03** (Certified Associate in Python Programming), status Live & Active. 40 itens, 5 blocos: (1) Modules and Packages — 6 itens/12%; (2) Exceptions — 5 itens/14%; (3) Strings — 8 itens/18%; (4) Object-Oriented Programming — 12 itens/34% (MAIOR PESO); (5) Miscellaneous (list comprehensions, lambdas, closures, file I/O) — 9 itens/22%. Nota mínima: 70% cumulativo. Tempo não confirmado oficialmente (fontes terceiras citam ~65min+10min tutorial).
- Nenhuma nova versão de exame anunciada pra 2025/2026 nas fontes oficiais consultadas.

**Fronteira cravada:** este galho NÃO reensina Python — todo conteúdo técnico já está nos Galhos 1-6 (núcleo da linguagem). Aqui só mapeamos blocos oficiais do syllabus às notas já escritas, cobrimos o formato/estilo de questão da Python Institute, e fechamos com simulado.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ pendente | 0 |
| ✅ feita | 8 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

---

## Notas

#### 01 - Panorama — PCEP e PCAP, o que são e pra quem
- **Estado:** ✅ feita (140 linhas) · fase: Magus
- **Escopo:** o que é a Python Institute, diferença PCEP (entry-level) vs PCAP (associate, o alvo real de quem já fez os Galhos 1-6), formato de prova (múltipla escolha, "single-choice"/"multiple-choice"/"drag-and-drop"/"gap-fill" nos blocos oficiais), nota de corte 70% cumulativo, para quem faz sentido (currículo/certificação formal vs aprendizado real — honestidade de que a trilha já ensinou mais do que qualquer uma das duas certificações cobre).

#### 02 - PCEP na prática — fundamentos, controle de fluxo e coleções
- **Estado:** ✅ feita (320 linhas) · fase: Magus
- **Escopo:** os 4 blocos do PCEP-30-02 mapeados às notas dos Galhos 1-2 (interpretador/tipos/operadores → Core; if/while/for/break/continue → Core; listas/tuplas/dicts/strings → Collections e Comprehensions; funções/exceções → Core). Tabela bloco×peso×nota-fonte. Revisão dirigida aos pontos que mais aparecem em prova (não repete a explicação, aponta pra ela).

#### 03 - PCAP — módulos, exceções e strings
- **Estado:** ✅ feita (391 linhas) · fase: Magus
- **Escopo:** blocos 1-3 do PCAP-31-03 (Modules and Packages 12%, Exceptions 14%, Strings 18%) mapeados às notas correspondentes dos Galhos 1 e 3. Foco nos detalhes que a prova cobra e que às vezes passam batido no aprendizado orgânico (ex: diferença `import`/`from...import`/`as`, hierarquia exata de exceções built-in, métodos de string menos comuns).

#### 04 - PCAP — orientação a objetos, o bloco de maior peso
- **Estado:** ✅ feita (651 linhas) · fase: Magus
- **Escopo:** bloco 4 do PCAP-31-03 (Object-Oriented Programming, 34% — maior peso de todo o exame) mapeado ao Galho 3 (OO e Data Model). Ênfase nos pontos que a Python Institute testa pesado: encapsulamento/name mangling, herança/MRO, herança múltipla, polimorfismo, introspecção (`isinstance`/`issubclass`/`__class__`), construtores. Nota mais longa do galho dado o peso do bloco.

#### 05 - PCAP — miscellaneous, comprehensions, lambdas, closures e arquivos
- **Estado:** ✅ feita (447 linhas) · fase: Magus
- **Escopo:** bloco 5 do PCAP-31-03 (Miscellaneous, 22%) mapeado aos Galhos 2 (comprehensions) e 4 (lambdas, closures) — mais file I/O, que é território novo não coberto em profundidade nos Galhos 1-6 (breve introdução a `open()`/context manager de arquivo/modos de abertura, o suficiente pro exame).

#### 06 - Armadilhas comuns e o estilo de questão da Python Institute
- **Estado:** ✅ feita (388 linhas) · fase: Magus
- **Escopo:** o padrão de pegadinha característico da Python Institute — "o que este código imprime" com mutação inesperada, escopo (LEGB) armado como pegadinha, precedência de operadores, slicing com índices negativos, comportamento de `is` vs `==` com cache de inteiros pequenos, mutável como argumento default. Conecta de volta aos Galhos 1-6 mas com o ângulo específico de "isso é testado assim na prova".

#### 07 - Estratégia de prova e plano de estudo
- **Estado:** ✅ feita (240 linhas) · fase: Magus
- **Escopo:** como se preparar de fato — recursos oficiais (Python Institute practice tests, OpenEDG), gestão de tempo de prova, ordem de ataque das questões (deixar as de código longo por último), plano de estudo de 2-3 semanas cruzando os Galhos 1-6 com os blocos oficiais mapeados nas notas 02-05 deste galho.

#### 08 - Capstone — simulado comentado PCEP + PCAP
- **Estado:** ✅ feita (554 linhas) · fase: Magus
- **Escopo:** simulado com ~15-20 questões no estilo real da Python Institute (mistura PCEP+PCAP, pesos proporcionais aos blocos oficiais), cada questão com gabarito comentado explicando o raciocínio E linkando de volta pra nota-fonte do conceito (Galhos 1-6 ou notas deste galho). Fecha o galho 19 E A TRILHA PYTHON INTEIRA (19 galhos) — última nota da trilha, deve reconhecer isso explicitamente no fechamento.

## Decisões e fronteiras registradas

- Todo conteúdo técnico de Python → Galhos 1-6, nunca reexplicado aqui, só mapeado e revisado.
- PCEP-30-02 e PCAP-31-03 confirmados como versões ativas em 2026-07-12; sem indício de nova versão em preparação.
- Tempo de prova não confirmado oficialmente para nenhuma das duas certificações — notas devem mencionar isso honestamente em vez de citar números de fontes terceirizadas sem verificação como se fossem oficiais.
- Este é o ÚLTIMO galho da trilha Python (19/19) — o capstone (nota 08) fecha a trilha inteira.
