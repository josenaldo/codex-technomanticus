---
title: "Matemática para Computação"
created: 2026-06-20
updated: 2026-06-20
type: moc
status: growing
publish: true
tags:
  - fundamentos
  - matematica-para-computacao
  - entrevista
  - moc
aliases:
  - Matemática para Computação
  - Matemática Discreta
  - Discrete Mathematics
  - Math for CS
  - Galho - Matemática para Computação
---

# Matemática para Computação

> [!abstract] TL;DR
> A matemática **discreta** é o ferramental que a Ciência da Computação usa o tempo todo sem parar pra
> ensinar: a **lógica** que sustenta toda condição e invariante, as **provas** (com a indução, que é a
> corretude da recursão escrita em matemática), os **conjuntos/funções/relações** que modelam dados, a
> **combinatória** que conta o espaço de estados, a **teoria dos números** por trás de hashing e
> criptografia, os **grafos** como objeto matemático, e a **probabilidade** que faz o Bloom filter e o
> quicksort randomizado funcionarem. Este galho é a **dona** dessas ferramentas — os outros galhos as usam
> e linkam de volta pra cá.

## Sobre este galho
Se a [[03-Dominios/Fundamentos/Teoria da Computação/index|Teoria da Computação]] é a *teoria sobre os
limites do computável*, a Matemática para Computação é a **caixa de ferramentas** que torna essa teoria (e
quase todo o resto da CC) escrevível. Aqui mora o discreto — o mundo de estados, passos e estruturas
contáveis em que o software vive —, em oposição ao contínuo do cálculo.

**Fronteiras (linka, não duplica):**
- **Análise assintótica (Big-O), recorrências e Teorema Mestre** → [[03-Dominios/Fundamentos/Algoritmos/index|Algoritmos]]. Aqui (nota 08) mora a **base** matemática: logaritmos, somatórios, crescimento e a resolução geral de recorrências.
- **Grafos como estrutura de dados e algoritmos (BFS/DFS/Dijkstra)** → [[03-Dominios/Fundamentos/Estruturas de Dados/11 - Grafos - travessia e algoritmos|Estruturas de Dados]]. Aqui (notas 16–18) é o **lado matemático**: definições, Euler/Hamilton, planaridade, coloração, matching, árvore como objeto.
- **Diagonalização e o incomputável** → [[03-Dominios/Fundamentos/Teoria da Computação/10 - Decidível, reconhecível e a máquina universal|Teoria da Computação]]. Aqui (nota 13) mora a **cardinalidade** (contável × incontável) e a diagonalização de Cantor que aquela teoria *usa*.
- **Criptografia, hashing e segurança aplicados** → futuro galho de Segurança Conceitual. Aqui (notas 14–15) é a **teoria dos números** (Euclides, modular, Fermat/Euler); RSA aparece só em prosa.
- **Lógica digital e circuitos** → futuro galho de Organização de Computadores. Aqui a lógica é tratada pelo ângulo **matemático** (tabelas-verdade, prova), não de hardware.

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção "Em entrevista"
com frases prontas em inglês e vocabulário técnico PT→EN. (O tema cai *raramente* em entrevista, mas a
indução, o Big-O/logaritmos, a probabilidade de hashing e os grafos aparecem o tempo todo na prática.)

## Iniciado — a linguagem da prova (lógica e conjuntos)
1. [[01 - O que é matemática para computação]] — discreto × contínuo; por que a CS é matemática discreta; o mapa do galho; matemática (ferramenta) × teoria da computação (limites).
2. [[02 - Lógica proposicional]] — conectivos, tabelas-verdade, equivalências, De Morgan, contrapositiva; booleanos, `if`, `WHERE` do SQL.
3. [[03 - Lógica de predicados e quantificadores]] — ∀/∃, negação, aninhamento; invariantes, asserções, pré/pós-condições, specs.
4. [[04 - Teoria dos conjuntos]] — operações, potência, produto cartesiano, Venn, leis; tipos como conjuntos, set ops em SQL.

## Adepto — provar, quantificar, contar
5. [[05 - Técnicas de prova]] — direta, contrapositiva, contradição, casos, contraexemplo; raciocinar sobre corretude.
6. [[06 - Indução matemática]] — fraca e forte; o efeito dominó; somatórios, corretude de recursão, loop invariants.
7. [[07 - Indução estrutural e definições recursivas]] — estruturas indutivamente definidas; A técnica de prova da CS; ADTs e funções recursivas.
8. [[08 - Somatórios, logaritmos e crescimento]] — Σ, logaritmos, crescimento de funções, recorrências; a base que Algoritmos defere.
9. [[09 - Funções]] — injetora/sobrejetora/bijetora, composição, inversa; hashing, mapeamentos, idempotência.
10. [[10 - Relações]] — propriedades, equivalência/classes, ordem parcial (Hasse), fechos; ordenação topológica, dependências.
11. [[11 - Combinatória - a arte de contar]] — soma/produto, permutações, combinações, binômio; espaço de estados, casos de teste.
12. [[12 - Princípios combinatórios - casa dos pombos e inclusão-exclusão]] — pigeonhole, inclusão-exclusão; colisão garantida de hash, contagem com sobreposição.
13. [[13 - Cardinalidade - contável e incontável]] — bijeção = "mesmo tamanho"; ℕ/ℤ/ℚ × ℝ; diagonalização de Cantor; o argumento que garante o incomputável.

## Magus — números, grafos e o acaso
14. [[14 - Teoria dos números - divisibilidade e primos]] — divisibilidade, primos, fatoração única, MDC, algoritmo de Euclides; hashing, checksums.
15. [[15 - Aritmética modular e Fermat-Euler]] — congruências, exponenciação modular, inverso, Fermat/Euler; RSA (em prosa), CRC, dígitos verificadores.
16. [[16 - Teoria dos grafos - o lado matemático]] — (V,E), grau, handshaking, conexidade, Euler × Hamilton (Königsberg); linka ED para o lado algorítmico.
17. [[17 - Grafos avançados - planaridade, coloração e matching]] — fórmula de Euler, 4 cores, matching/Hall; alocação de registradores, escalonamento, pareamento.
18. [[18 - Árvores como objeto matemático]] — caracterizações, enraizada × livre, fórmula de Cayley, spanning trees; fronteira com ED.
19. [[19 - Probabilidade discreta]] — espaço amostral, condicional, independência, Bayes; paradoxo do aniversário, colisão de hash.
20. [[20 - Variáveis aleatórias e esperança]] — VA, esperança, linearidade da esperança, variância, distribuições; quicksort randomizado, custo esperado de hashing.
21. [[21 - O acaso na computação - estruturas e algoritmos aleatorizados]] — Monte Carlo × Las Vegas, Bloom, hashing universal, skip list, power-of-two-choices; linka ED.
22. [[22 - A matemática na vida do dev]] — cada ramo → uso prático; cheat-sheet mestre; inglês; vocabulário; armadilhas.

## Rotas alternativas

### O essencial (a matemática que o dev usa toda semana)
06 → 08 → 09 → 11 → 19. Indução (corretude), logaritmos/somatórios (Big-O), funções (hash), contagem, probabilidade.

### A linguagem da prova (lógica e rigor)
02 → 03 → 04 → 05 → 06 → 07. Da lógica às técnicas de prova e às duas induções.

### Teoria dos números e o acaso (a matemática "escondida" da infra)
14 → 15 → 19 → 20 → 21. De Euclides ao RSA, da probabilidade às estruturas aleatorizadas.

### Grafos como matemática
16 → 17 → 18 + [[03-Dominios/Fundamentos/Estruturas de Dados/11 - Grafos - travessia e algoritmos|o lado algorítmico em ED]].

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Fundamentos/Matemática para Computação"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Fundamentos/index|Fundamentos (MOC do domínio)]]
- [[03-Dominios/Fundamentos/Algoritmos/index|Algoritmos]] — a base de logaritmos/somatórios/recorrências em uso
- [[03-Dominios/Fundamentos/Estruturas de Dados/index|Estruturas de Dados]] — grafos e estruturas aleatorizadas pelo lado algorítmico
- [[03-Dominios/Fundamentos/Teoria da Computação/index|Teoria da Computação]] — usa lógica, prova e diagonalização (que moram aqui)
- [[Dicionário de Fundamentos]]
