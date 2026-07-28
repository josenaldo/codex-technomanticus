---
title: "Domínio UX — design"
created: 2026-07-28
type: design
status: draft
publish: false
tags:
  - meta
  - design
  - ux
  - usabilidade
  - design-system
  - ux-writing
---

# Domínio UX — design

## Contexto

O vault não tem cobertura de UX. Um levantamento em 2026-07-28 confirmou: não existe
domínio, senda nem tag sistemática (só duas notas usam `ux` como tag —
`Java/Swing/09 - Look and Feel` e `React/Ícones`). UX aparece hoje apenas como **lente
dentro de domínios técnicos**: `HTML/06 - Formulários II` (única nota com UX no título),
`Segurança/03 - Economia e fator humano` (maior densidade de "usabilidade" do vault),
`Web Performance/Medição e Core Web Vitals`, `Auth e Identidade` (UX de login) e o domínio
de IA (UX de produto de IA). Quase todo arquivo com "design" no nome é *design de
software*, não design de interface.

O vizinho mais próximo é **Acessibilidade** — domínio completo desde 2026-07-28, 21 notas,
que cobre a camada técnica de a11y mas não a camada de decisão de design que a precede.

**Público-alvo:** o *fractional engineer* full-cycle — profissional que assume ownership
total do projeto: colhe requisito com o cliente, define o problema, desenha a solução,
constrói e coloca em produção, mede e sustenta. **Não é especialista de UX e não vai
virar um.** Precisa do mínimo com profundidade real para exercer bem o ofício sozinho, e
para sustentar conversa de nível sênior/staff em entrevista internacional.

Esse público define dois recortes que atravessam todo o domínio e aparecem
independentemente em múltiplas fatias da pesquisa:

- **Cliente ≠ usuário.** Em consultoria/B2B, quem paga e aprova quase nunca é quem usa o
  sistema. Otimizar para a satisfação do stakeholder produz produto que os usuários reais
  rejeitam.
- **Escala de um.** Boa parte do cânone de UX pressupõe time, orçamento e tráfego. Cada
  nota precisa separar o que é praticável sozinho do que exige estrutura — e nomear
  honestamente o segundo grupo em vez de fingir que dá.

## Decisões de design

Tomadas no brainstorming de 2026-07-28:

1. **Eixo:** decomposição **por disciplina de UX** (research, AI, IxD, linguagem visual,
   writing, métricas, ética). Escolhido pelo usuário sobre a alternativa "ciclo do produto".
   *Mitigação do risco de virar enciclopédia:* a lente full-cycle entra **dentro** de cada
   nota — toda nota responde "o que eu, sozinho, faço com isso na segunda-feira".
2. **Escala:** domínio grande, de primeira classe (porte de React), não um galho enxuto.
   Resultado: **48 notas + capstone** em `Engenharia/UX/` e **9 notas** em
   `Tecnologia/Ferramentas de Design/`.
3. **Colocação:** split estável/volátil. O ofício mora em `Engenharia/UX/`; as ferramentas
   concretas e perecíveis moram em `Tecnologia/Ferramentas de Design/`. Segue a regra
   declarada em `Engenharia/index.md`: *"a fundamentação fica aqui; cada tecnologia linka
   pra cá e cuida das suas particularidades"*. Alternativas rejeitadas: tudo em
   `Tecnologia/UX` (mistura ofício durável com ferramenta de ciclo de 18 meses); nova
   camada de topo `Produto/` (mudança estrutural maior do que o ganho justifica agora).
4. **Ritmo:** galho a galho, ponta a ponta — fecha-se um sub-galho (semear + enriquecer
   até ✅) antes de abrir o próximo. Mantém o contexto leve por sessão.
5. **Primeira versão assumidamente imperfeita.** O usuário registrou que o galho será
   aprimorado com o tempo; esta spec fixa a espinha, não a palavra final.

## Arquitetura

### `03-Dominios/Engenharia/UX/`

- **`index.md`** (`type: moc`): TL;DR + tabela dos 8 sub-galhos + roster agrupado por fase
  + fronteiras.
- **`roadmap.md`** (galho-pai): mapa de estado recursivo (raiz → sub-galho → nota), no
  `Template - Roadmap`.
- **8 sub-pastas**, cada uma com `index.md` e `roadmap.md`.

### `03-Dominios/Tecnologia/Ferramentas de Design/`

Galho único (sem sub-galhos), com `index.md` e `roadmap.md`.

## Roster — `Engenharia/UX/` (48 + capstone)

### SG1 — Fundamentos e modelo mental · *Iniciado* (5)

1. **UX não é tela — o ofício e seus limites** — o que a disciplina abrange, o que o
   engenheiro full-cycle faz sozinho, e o sinal de que é hora de chamar um especialista
2. **Affordances e signifiers** — Norman (1988/2013); por que "adicionar um tooltip" quase
   nunca é a correção certa
3. **As 10 heurísticas de Nielsen** — Nielsen & Molich (1990, refinadas 1994); uma
   violação e uma correção por heurística
4. **Leis de UX** — Fitts (1954), Hick & Hyman (1952), Jakob, Miller, Peak-End; curadoria
   de Yablonski (2020)
5. **Gestalt aplicada a UI** — proximidade, similaridade, fechamento, continuidade,
   figura-fundo

### SG2 — Descoberta e pesquisa · *Iniciado/Adepto* (9)

6. **Generativa vs avaliativa** — as duas fases da pesquisa; pular a generativa é a causa
   raiz mais comum de "construímos a coisa errada"
7. **Entrevista de descoberta — as regras do Mom Test** — Fitzpatrick; falar do passado
   concreto, nunca de opinião sobre o futuro
8. **Cliente não é usuário — a armadilha do B2B/consultoria** — nota central do domínio
   para este público
9. **Jobs To Be Done — as duas escolas** — Christensen/Moesta (qualitativa) vs
   Ulwick (outcome-driven); saber que divergem já sinaliza profundidade
10. **Opportunity Solution Tree de bolso** — Torres (2021) sem trio de produto
11. **Assumption mapping** — Bland & Osterwalder (2019); importância × evidência
12. **Proto-persona vs persona de verdade** — Gothelf & Seiden (2013); hipótese explícita
    vs dado pesquisado
13. **Teste de usabilidade guerrilha com 5 usuários** — Nielsen (2000) e Krug (2010), com
    o caveat honesto das 3 rodadas
14. **Personas sintéticas e síntese por IA** — estado 2026 com ceticismo: útil para
    ideação e triagem, perigoso como substituto de dado primário

### SG3 — Arquitetura de informação · *Adepto* (4)

15. **Os 4 sistemas da AI** — organização, rotulação, navegação, busca
    (Rosenfeld/Morville/Arango, 4ª ed. 2015)
16. **Schema de banco não é estrutura de navegação** — taxonomia vs navegação; o usuário
    não pensa em JOIN, pensa em tarefa
17. **Card sorting e tree testing de guerrilha** — validar taxonomia antes de comprometer
    a estrutura
18. **Navegação e wayfinding** — onde estou, de onde vim, para onde posso ir

### SG4 — Design de interação · *Adepto* (7)

19. **Do fluxo antes da tela** — user flow como máquina de estados; o equivalente a
    desenhar o diagrama de estados antes de codificar
20. **Os 5 estados de tela** — vazio, carregando, erro, parcial, sucesso; `if (loading)`
    é sub-modelagem do espaço de estados
21. **Progressive disclosure** — e a armadilha do "mostrar mais" que decepciona
22. **Modal vs página vs drawer** — critério de decisão e o anti-padrão do modal empilhado
23. **Undo vs confirmação** — reversibilidade barata contra alert fatigue
24. **Design de formulários — defaults** — coluna única, label acima, validação no blur,
    erro específico, opcional marcado
25. **Latência percebida e feedback** — Miller (1968), Card/Moran/Newell (1983); skeleton
    vs spinner, com a ressalva de que a superioridade do skeleton não é consenso

### SG5 — Linguagem visual e design system · *Adepto/Magus* (7)

26. **Hierarquia visual** — uma ação primária por tela; o mínimo para a tela não parecer
    amadora (Refactoring UI, 2018)
27. **Escalas de tipografia, espaçamento e densidade** — escala modular, base 4/8,
    densidade por perfil de usuário
28. **Cor de produto: OKLCH e paleta semântica** — Ottosson (2020); por que HSL mente
    sobre luminosidade percebida
29. **Design tokens como sistema** — hierarquia primitivo → semântico → componente e o
    formato W3C DTCG (primeira versão estável em out/2025, ainda Community Group Report,
    não padrão W3C)
30. **Atomic Design — o que ainda vale** — Frost (2013/2016) e a crítica corrente: a
    metáfora sobrevive, a taxonomia rígida virou debate de nomenclatura
31. **Component API design** — boolean explosion, enum de variant, composição sobre
    configuração
32. **Adotar vs construir, e governança mínima para um time de um** — decisão de produto,
    não comparação técnica de API (essa já existe em React/Ecossistema)

### SG6 — UX writing e content design · *Adepto* (5)

*Território 100% novo no vault — nenhuma cobertura hoje.*

33. **Voz e tom** — voz constante do produto, tom que varia com o estado emocional do
    usuário
34. **Microcopy, labels de ação e jargão interno** — verbo + objeto específico; o nome da
    tabela do banco vazando para a interface
35. **Erros: fluxo de recuperação e mensagem que não culpa** — o que aconteceu, por quê,
    o que fazer agora
36. **Estados vazios como conteúdo** — "sem dados ainda" vs "sem resultados" vs "erro"
37. **i18n quebra layout** — expansão de string, pluralização, RTL, truncamento

### SG7 — Medir, validar e sustentar · *Magus* (8)

38. **HEART + Goals-Signals-Metrics** — Rodden et al. (Google, ~2010); Happiness é a única
    dimensão atitudinal
39. **SUS, UMUX-Lite, SUPR-Q, SEQ** — qual questionário quando; SUS 68 é benchmark
    empírico, não meio de escala
40. **NPS e North Star — promessa, crítica e Goodhart** — por que os dois números mais
    citados do mercado são os mais contestados
41. **Instrumentação: event taxonomy e tracking plan** — object-action, snake_case,
    governança; taxonomia sem dono apodrece
42. **Quando A/B não se aplica** — tráfego baixo, B2B, cliente único; alternativas
    legítimas (feature flag como desenho experimental mínimo, micro-conversões,
    qualitativo como método de primeira classe). Recorte crítico para este público.
43. **Session replay e heatmap** — o que provam, o que não provam, e o recorte de
    privacidade (consentimento, mascaramento de PII)
44. **UX debt e matriz severidade × esforço** — priorizar retrabalho de usabilidade com
    critério
45. **Defender decisão de UX com número** — e a atribuição causal frágil que torna todo
    ROI de UX uma estimativa, não um fato

### SG8 — Ética e ofício · *Magus* (3)

46. **Dark patterns e regulação** — taxonomia dos padrões enganosos e o cenário
    regulatório (EU DMA em vigor; EU Digital Fairness Act ainda em tramitação — verificar
    status na data de escrita; ações da FTC). Deixou de ser questão estética e virou risco
    legal e de carreira.
47. **UX no ciclo de dev** — Definition of Done que inclui UX, revisão de UX no code
    review, gates de CI
48. **UX em entrevista sênior/staff** — articular trade-off explícito, vocabulário
    compartilhado com design, e o custo de engenharia de cada opção de interface

### Capstone

49. **Do requisito ao produto validado** — um ciclo completo: descobrir com o cliente,
    definir, desenhar, construir, instrumentar, medir, priorizar a dívida

## Roster — `Tecnologia/Ferramentas de Design/` (9)

1. **Figma para o engenheiro** — Dev Mode, variables/modes, auto layout; e o que é
   território de designer profissional que dá para ignorar com segurança
2. **Figma MCP Server + Code Connect** — contexto de design estruturado para o agente, em
   vez de screenshot
3. **Claude Design e o handoff bundle** — research preview da Anthropic Labs (17/abr/2026,
   sobre Opus 4.7); linka para a skill `handoff-design` já existente em vez de duplicá-la
4. **Geradores de UI por IA** — v0, Lovable, Bolt, Subframe: onde ajudam, onde produzem
   lixo, como avaliar a saída
5. **Estética genérica de IA e como escapar** — o fingerprint reconhecível e a causa raiz
   (convergência do modelo para o estatisticamente seguro)
6. **Protótipo em código** — quando o componente real é o protótipo mais barato e a
   ferramenta de design é etapa dispensável
7. **Excalidraw e tldraw** — baixa fidelidade, e tldraw como SDK embutível
8. **Pipeline de tokens** — Figma Variables → Style Dictionary → CSS custom properties,
   com Git como fonte de verdade
9. **Loop visual com Playwright MCP e visual regression** — accessibility tree como
   feedback estruturado; snapshot nativo do Playwright antes de plataforma cloud

## Fronteiras (linkar, nunca reescrever)

| Fronteira existente | O que já está lá | O que é novo aqui |
|---|---|---|
| `Tecnologia/Acessibilidade` (21 notas) | accessibility tree, WCAG 2.2, ARIA APG, foco em SPA, contraste, cor acessível | a camada de decisão que precede a implementação acessível. *"O botão tem contraste suficiente" é a11y; "por que existe um botão aqui e não um link, e por que ele domina a tela" é IxD.* |
| `Tecnologia/CSS/07` e `/06` | custom properties, mecânica de tokens em CSS, responsivo | tokens como **sistema** (hierarquia, governança, padrão DTCG), não a sintaxe CSS |
| `Tecnologia/React/Ecossistema/03` | comparação técnica MUI/Radix/shadcn/Mantine com código | o **quando adotar** como decisão de produto |
| `Tecnologia/React/Ecossistema/10, /11` | tabelas, data grids, libs de gráficos | nada — apenas linkar |
| `Tecnologia/Web Performance` | INP, LCP, CLS, lab vs field, CrUX | métrica de UX (satisfação, sucesso de tarefa, retenção). Performance é **insumo** de UX, não a mesma coisa; vale uma nota-ponte curta |
| `Tecnologia/Testes JS/14` | Playwright além do básico | Playwright como loop de feedback **visual/de design** |
| skill `dataviz` | paleta categórica/sequencial, heurística de forma | paleta de **produto/UI**, não de dados |
| `Tecnologia/IA/Claude Code` + skill `handoff-design` | Claude Code, o fluxo de handoff | Claude Design como produto; a nota linka a skill |
| `Tecnologia/Tooling e Build` | pipeline de build | Style Dictionary é candidato natural a nota **lá**, não aqui |

Regra: cada nova nota linka a fronteira em vez de reexplicá-la. Redundância entre notas é
reforço e não deve ser deduplicada — mas **reescrever uma fronteira inteira** é duplicação,
não reforço.

## Convenções e qualidade

- Notas atômicas em 3 fases (Iniciado/Adepto/Magus) com `fase:` no frontmatter.
- Padrão capítulo de livro; registro Feynman no enriquecimento; diagramas Mermaid nas
  notas substanciais.
- Núcleo mínimo obrigatório: TL;DR · abertura-problema · corpo-mecanismo · O que vem a
  seguir · Fontes · frontmatter.
- `roadmap.md` por sub-galho antes do enriquecimento (pré-condição da `enriquecer-galho`).
- **Toda nota separa explicitamente o praticável sozinho do que exige time/orçamento.**
  Isso não é seção opcional — é a promessa do domínio ao seu público.

## Rigor de fontes

A pesquisa de 2026-07-28 devolveu itens que **não foram verificados** e que as notas
correspondentes devem marcar como tal, em vez de afirmar:

- O comando `/design-sync` do Claude Design (só em blog de terceiros, não na doc oficial).
- A data da integração bidirecional Figma ↔ Claude Code (fev/2026, apenas fonte
  secundária).
- Percentuais de adoção de IA em pesquisa (69%, 88%) — vêm de blogs de fornecedores de
  ferramentas, material promocional sem estudo primário acessível.
- A citação "cavalos mais rápidos" atribuída a Henry Ford — apócrifa, autenticidade
  contestada.
- A citação Forrester de ROI de UX ("$1 → $100") — estudo antigo, metodologia não visível.
- A superioridade de skeleton screens sobre spinners — contestada, não é consenso.
- A data da 2ª edição de *Strategic Writing for UX* (Podmajersky).
- Status do EU Digital Fairness Act — em tramitação; verificar na data de escrita.
- APCA **não** é padrão de conformidade: foi retirado do working draft de WCAG 3 em 2023.
  WCAG 2.2 segue vigente.

## Fora de escopo

- Reescrever acessibilidade técnica (vive em `Tecnologia/Acessibilidade`).
- Design gráfico, branding e identidade visual de marca.
- UX de mobile nativo (iOS/Android HIG) além de menção — foco é web.
- Formação de designer profissional: autoria avançada em Figma, gestão de biblioteca
  multi-time, governança formal de design system em organização grande.
- Design de software (SOLID, patterns) — já é domínio próprio e não se confunde com este.

## Ordem de execução

**SG1 → SG2 → SG4 → SG6 → SG5 → SG3 → SG7 → SG8 → Ferramentas de Design → capstone.**

Justificativa da ordem: SG2, SG4 e SG6 vêm cedo porque são o que se usa no próximo
projeto; SG7 vem depois porque é o que sustenta entrevista; Ferramentas vem por último
porque é a parte mais perecível — quanto mais tarde for escrita, mais tempo de validade
terá. Ao fechar o domínio, atualizar o `00-Meta/Roadmap.md`.
