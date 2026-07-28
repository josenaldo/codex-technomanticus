---
title: "UX"
type: moc
publish: true
created: 2026-07-28
updated: 2026-07-28
status: seedling
tags:
  - moc
  - ux
  - design
  - usabilidade
  - design-system
aliases:
  - UX
  - User Experience
  - Experiência do Usuário
---

# UX

> [!abstract] TL;DR
> UX não é "a camada de tela" — é a disciplina de **decidir o que construir, para quem, e por quê**, antes de qualquer pixel. Este domínio existe para o *fractional engineer* full-cycle: quem colhe requisito com o cliente, define o problema, desenha a solução, constrói, mede e sustenta — sozinho. Não forma um especialista de UX; dá **profundidade real do mínimo necessário** para exercer bem o ofício sem um time de design ao lado, e para sustentar conversa de nível sênior/staff em entrevista internacional.

Dois recortes atravessam todo o domínio, porque definem o público-alvo:

- **Cliente ≠ usuário.** Em consultoria/B2B, quem paga e aprova quase nunca é quem usa o sistema. Otimizar para a satisfação de quem assina o contrato produz produto que os usuários reais rejeitam.
- **Escala de um.** Boa parte do cânone de UX pressupõe time, orçamento e tráfego. Cada nota separa o que é praticável sozinho do que exige estrutura — e nomeia honestamente o segundo grupo em vez de fingir que dá para fazer sem ele.

O domínio se organiza **por disciplina de UX** (pesquisa, arquitetura de informação, interação, linguagem visual, writing, métricas, ética) — não pelo ciclo do produto. A lente full-cycle entra **dentro** de cada nota: toda nota responde "o que eu, sozinho, faço com isso na segunda-feira".

---

## Política de mídia (M1 obrigatório)

> [!info] Mídia verificada é obrigatória em toda nota (2026-07-28)
> Diferente do padrão default de `verificar-nota` — que isenta M1 (vídeo/podcast embutido)
> na fase Iniciado — este domínio segue o padrão de [[03-Dominios/Tecnologia/Acessibilidade/index|Tecnologia/Acessibilidade]]
> (vídeo verificado em 21 de 21 notas): **M1 é obrigatório em toda nota, de qualquer fase**.
> Isso sobrepõe tanto a isenção de fase da skill `verificar-nota` quanto a regra de
> `diagnosticar-galho` que fecharia uma nota em `➖` só por score alto sem mídia. Uma nota
> sem mídia verificada **não fecha**.
>
> "Verificada" significa que a URL foi de fato conferida (WebFetch ou `yt-dlp`, lendo
> transcrição/descrição) e que o conteúdo corresponde ao que a nota afirma — nunca um link
> plausível, não conferido. Preferência por vídeo (YouTube); podcast/talk é aceitável quando
> não há vídeo bom e verificável para o tema. Ver a skill `.claude/skills/adicionar-midia/SKILL.md`
> para o formato do callout.
>
> **Exceção deliberada:** se, após busca extensiva, nenhuma mídia boa e verificável for
> encontrada, a nota fica sem mídia e o roadmap do sub-galho registra isso explicitamente
> como buraco honesto — nunca forçar um link fraco só para fechar o gate. Ver
> [[03-Dominios/Engenharia/UX/Descoberta e Pesquisa/roadmap|roadmap de SG2]], nota 06, para
> um exemplo real dessa exceção.

## Sub-galhos

| # | Sub-galho | O quê | Fase |
|---|-----------|-------|------|
| 1 | [[03-Dominios/Engenharia/UX/Fundamentos e Modelo Mental/index\|SG1 — Fundamentos e Modelo Mental]] | affordances e signifiers, as 10 heurísticas de Nielsen, leis de UX, Gestalt aplicada a UI | Iniciado |
| 2 | [[03-Dominios/Engenharia/UX/Descoberta e Pesquisa/index\|SG2 — Descoberta e Pesquisa]] | generativa vs avaliativa, Mom Test, cliente ≠ usuário, JTBD, Opportunity Solution Tree, personas, teste de usabilidade guerrilha, personas sintéticas | Iniciado/Adepto |
| 3 | [[03-Dominios/Engenharia/UX/Arquitetura de Informação/index\|SG3 — Arquitetura de Informação]] | os 4 sistemas da AI, taxonomia vs navegação, card sorting e tree testing, wayfinding | Adepto |
| 4 | [[03-Dominios/Engenharia/UX/Design de Interação/index\|SG4 — Design de Interação]] | fluxo antes da tela, os 5 estados de tela, progressive disclosure, modal vs página vs drawer, undo vs confirmação, formulários, latência percebida | Adepto |
| 5 | [[03-Dominios/Engenharia/UX/Linguagem Visual e Design System/index\|SG5 — Linguagem Visual e Design System]] | hierarquia visual, escalas de tipografia/espaçamento, cor em OKLCH, design tokens, Atomic Design, component API design, adotar vs construir | Adepto/Magus |
| 6 | [[03-Dominios/Engenharia/UX/UX Writing e Content Design/index\|SG6 — UX Writing e Content Design]] | voz e tom, microcopy, erros e recuperação, estados vazios como conteúdo, i18n quebrando layout | Adepto |
| 7 | [[03-Dominios/Engenharia/UX/Medir, Validar e Sustentar/index\|SG7 — Medir, Validar e Sustentar]] | HEART/GSM, SUS/UMUX-Lite/SUPR-Q/SEQ, NPS e North Star, event taxonomy, quando A/B não se aplica, session replay, UX debt, defender decisão com número | Magus |
| 8 | [[03-Dominios/Engenharia/UX/Ética e Ofício/index\|SG8 — Ética e Ofício]] | dark patterns e regulação, UX no ciclo de dev, UX em entrevista sênior/staff | Magus |
| — | **Capstone — Do requisito ao produto validado** *(a criar)* | ciclo completo: descobrir com o cliente, definir, desenhar, construir, instrumentar, medir, priorizar a dívida | Magus |

> **Estado (2026-07-28):** domínio recém-estruturado (scaffold). 0/48 + capstone escritas. Ver [[00-Meta/specs/2026-07-28-dominio-ux-design|design do domínio]], o plano em `00-Meta/.superpowers/sdd/2026-07-28-dominio-ux-plano/` e o [[03-Dominios/Engenharia/UX/roadmap|roadmap]].

---

## Roster agrupado por fase

### SG1 — Fundamentos e modelo mental · *Iniciado* (5)
1. UX não é tela — o ofício e seus limites
2. Affordances e signifiers
3. As 10 heurísticas de Nielsen
4. Leis de UX
5. Gestalt aplicada a UI

### SG2 — Descoberta e pesquisa · *Iniciado/Adepto* (9)
6. Generativa vs avaliativa
7. Entrevista de descoberta — as regras do Mom Test
8. Cliente não é usuário — a armadilha do B2B/consultoria
9. Jobs To Be Done — as duas escolas
10. Opportunity Solution Tree de bolso
11. Assumption mapping
12. Proto-persona vs persona de verdade
13. Teste de usabilidade guerrilha com 5 usuários
14. Personas sintéticas e síntese por IA

### SG3 — Arquitetura de informação · *Adepto* (4)
15. Os 4 sistemas da AI
16. Schema de banco não é estrutura de navegação
17. Card sorting e tree testing de guerrilha
18. Navegação e wayfinding

### SG4 — Design de interação · *Adepto* (7)
19. Do fluxo antes da tela
20. Os 5 estados de tela
21. Progressive disclosure
22. Modal vs página vs drawer
23. Undo vs confirmação
24. Design de formulários — defaults
25. Latência percebida e feedback

### SG5 — Linguagem visual e design system · *Adepto/Magus* (7)
26. Hierarquia visual
27. Escalas de tipografia, espaçamento e densidade
28. Cor de produto: OKLCH e paleta semântica
29. Design tokens como sistema
30. Atomic Design — o que ainda vale
31. Component API design
32. Adotar vs construir, e governança mínima para um time de um

### SG6 — UX writing e content design · *Adepto* (5)
33. Voz e tom
34. Microcopy, labels de ação e jargão interno
35. Erros: fluxo de recuperação e mensagem que não culpa
36. Estados vazios como conteúdo
37. i18n quebra layout

### SG7 — Medir, validar e sustentar · *Magus* (8)
38. HEART + Goals-Signals-Metrics
39. SUS, UMUX-Lite, SUPR-Q, SEQ
40. NPS e North Star — promessa, crítica e Goodhart
41. Instrumentação: event taxonomy e tracking plan
42. Quando A/B não se aplica
43. Session replay e heatmap
44. UX debt e matriz severidade × esforço
45. Defender decisão de UX com número

### SG8 — Ética e ofício · *Magus* (3)
46. Dark patterns e regulação
47. UX no ciclo de dev
48. UX em entrevista sênior/staff

### Capstone
49. Do requisito ao produto validado

---

## Fronteiras (linkar, nunca reescrever)

> [!info] Fronteiras
> Este domínio **linka** as notas abaixo como reforço, **nunca as reescreve** (redundância entre notas é reforço, não duplicação — mas reescrever uma fronteira inteira é duplicação). Regra: cada nova nota linka a fronteira em vez de reexplicá-la.
>
> | Fronteira existente | O que já está lá | O que é novo aqui |
> |---|---|---|
> | [[03-Dominios/Tecnologia/Acessibilidade/index\|Tecnologia/Acessibilidade]] (21 notas) | accessibility tree, WCAG 2.2, ARIA APG, foco em SPA, contraste, cor acessível | a camada de decisão que precede a implementação acessível. *"O botão tem contraste suficiente" é a11y; "por que existe um botão aqui e não um link, e por que ele domina a tela" é IxD.* |
> | [[03-Dominios/Tecnologia/CSS/07 - Custom properties e design tokens\|Tecnologia/CSS/07]] e [[03-Dominios/Tecnologia/CSS/06 - Design responsivo - media queries e container queries\|/06]] | custom properties, mecânica de tokens em CSS, responsivo | tokens como **sistema** (hierarquia, governança, padrão DTCG), não a sintaxe CSS |
> | [[03-Dominios/Tecnologia/React/Ecossistema/03 - Component libraries e design systems\|Tecnologia/React/Ecossistema/03]] | comparação técnica MUI/Radix/shadcn/Mantine com código | o **quando adotar** como decisão de produto |
> | [[03-Dominios/Tecnologia/React/Ecossistema/10 - Tabelas e data grids - TanStack Table\|Tecnologia/React/Ecossistema/10]], [[03-Dominios/Tecnologia/React/Ecossistema/11 - Data visualization - escolhendo libs de gráficos\|/11]] | tabelas, data grids, libs de gráficos | nada — apenas linkar |
> | [[03-Dominios/Tecnologia/Web Performance/index\|Tecnologia/Web Performance]] | INP, LCP, CLS, lab vs field, CrUX | métrica de UX (satisfação, sucesso de tarefa, retenção). Performance é **insumo** de UX, não a mesma coisa; vale uma nota-ponte curta |
> | [[03-Dominios/Tecnologia/Testes JS/14 - Playwright além do básico\|Tecnologia/Testes JS/14]] | Playwright além do básico | Playwright como loop de feedback **visual/de design** |
> | skill `dataviz` | paleta categórica/sequencial, heurística de forma | paleta de **produto/UI**, não de dados |
> | [[03-Dominios/Tecnologia/IA/Claude Code/index\|Tecnologia/IA/Claude Code]] + skill `handoff-design` | Claude Code, o fluxo de handoff | Claude Design como produto; a nota linka a skill |
> | [[03-Dominios/Tecnologia/Tooling e Build/index\|Tecnologia/Tooling e Build]] | pipeline de build | Style Dictionary é candidato natural a nota **lá**, não aqui |

---

## Veja também

- [[00-Meta/Roadmap|Roadmap de Trilhas]] — UX entra como construção nova em andamento (Tier 1).
- [[03-Dominios/Tecnologia/Ferramentas de Design/index|Ferramentas de Design]] — a metade volátil/tecnológica deste mesmo domínio.
- [[03-Dominios/Tecnologia/Acessibilidade/index|Acessibilidade]] — o vizinho mais próximo: a camada técnica que precede este domínio.
- [[00-Meta/specs/2026-07-28-dominio-ux-design|Design do domínio]] — decisões, roster completo e fronteiras.
