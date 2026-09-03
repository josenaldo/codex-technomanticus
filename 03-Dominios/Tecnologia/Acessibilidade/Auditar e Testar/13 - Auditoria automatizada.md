---
title: "Auditoria automatizada"
created: 2026-07-27
updated: 2026-07-27
type: concept
status: seedling
fase: adepto
tags:
  - acessibilidade
  - a11y
  - auditoria
  - axe
publish: true
---

# Auditoria automatizada

> [!abstract] TL;DR
> Ferramentas automáticas — **axe** (o motor por trás da maioria), **Lighthouse** e **WAVE** — varrem uma página e apontam violações de WCAG em segundos. São indispensáveis: pegam o grosso das falhas mecânicas (contraste, `alt` faltando, campo sem label) sem esforço humano. Mas têm um **teto** que você precisa gravar: a automação detecta apenas **cerca de um terço a metade** dos problemas de acessibilidade. Ela verifica o que é *computável* ("existe um `alt`?"), não o que exige *julgamento* ("o `alt` descreve a imagem?"). Tratar "passou no axe" como "é acessível" é o erro que a nota 01 já avisava — a ferramenta é rede de segurança, não método.

O SG2 ensinou a construir. O SG3 ensina a **provar**. E o primeiro instinto — rodar uma ferramenta — é certo, desde que você saiba exatamente o que ela vê e o que ela é cega para ver. Começar pela automação é inteligente: é barata, rápida e pega os erros mais comuns do mundo (lembre dos seis que concentram 96% das falhas, na nota 01 — quase todos automaticamente detectáveis). Mas terminar na automação é o erro que produz sites "aprovados" e inutilizáveis.

## O que a automação vê bem

Ferramentas automáticas são excelentes no que é **verificável por regra**. Elas leem o DOM e a árvore de acessibilidade (nota 02) e checam condições objetivas:

- **Contraste de cor** — calculam a razão (nota 11) e sinalizam o que fica abaixo de 4.5:1. Fazem isso em massa, algo impossível de conferir a olho num site grande.
- **Atributos faltando** — imagem sem `alt`, campo sem label associado, botão sem nome acessível, `<html>` sem `lang`.
- **ARIA inválido** — um `role` que não existe, um `aria-*` mal escrito, um `aria-labelledby` apontando para um id inexistente.
- **Estrutura básica** — hierarquia de headings quebrada (h1→h3), landmarks ausentes, listas malformadas.

Nada disso exige julgamento humano — é presença/ausência, válido/inválido, número acima/abaixo do limiar. É exatamente onde a máquina supera o humano em velocidade e consistência.

## As três ferramentas que você vai usar

O mercado convergiu em torno de poucas ferramentas, e a maioria compartilha o **mesmo motor**:

| Ferramenta | O que é | Melhor para |
|-----------|---------|-------------|
| **axe-core** (Deque) | O *engine* open source de auditoria. Roda embutido em incontáveis outras ferramentas. | Ser a base de tudo — extensão, CI, testes de código |
| **axe DevTools** | Extensão de browser sobre o axe-core | Auditoria manual rápida durante o desenvolvimento |
| **Lighthouse** | Auditoria do Chrome (perf + a11y + SEO); a parte de a11y **usa axe-core** | Um score rápido no DevTools; visão geral |
| **WAVE** (WebAIM) | Extensão que **sobrepõe ícones** na própria página, mostrando onde estão os problemas | Ver os erros *no contexto visual* da página; ótimo didaticamente |

O ponto a interiorizar: **axe-core é o denominador comum**. A aba Accessibility do Lighthouse é axe por baixo; muitas ferramentas comerciais são axe por baixo. Isso é bom (um padrão de fato, bem mantido) e é um alerta (rodar Lighthouse *e* axe DevTools não te dá duas opiniões independentes — é o mesmo motor duas vezes). O WAVE é o mais diferente na apresentação: em vez de uma lista, ele desenha os problemas sobre a página, o que ajuda a *ver* a estrutura.

## O teto: por que a automação não basta

Agora o coração desta nota. A pesquisa da própria Deque — criadora do axe — e da comunidade converge num número desconfortável: testes automáticos detectam apenas em torno de **um terço a metade** dos problemas de acessibilidade de WCAG. A metade que falta não é obscura; é frequentemente a que **mais importa para o usuário**.

Por quê? Porque a máquina verifica o *computável*, não o *significativo*:

```mermaid
graph TD
    classDef marca fill:#8855DF33,stroke:#8855DF,color:#E9ECF2
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    A[Imagem] --> B{Tem alt?}
    B -->|não| C["❌ axe detecta:<br/>'imagem sem alt'"]
    B -->|sim| D["✅ axe aprova"]
    D --> E{"O alt DESCREVE<br/>a imagem?"}
    E -->|"alt='imagem123.jpg'"| F["😱 axe não vê:<br/>alt inútil, mas presente"]
    E -->|"alt='gráfico de vendas subindo'"| G[de fato acessível]
    class C marca
    class F destaque
    class G neutro
```

O diagrama mostra o buraco. O axe verifica que o `alt` **existe**; ele não tem como saber se o `alt` **descreve** a imagem. `alt="DSC_0042.jpg"` passa na automação e é inútil para quem usa leitor de tela. Os casos que só o humano pega:

- **Qualidade do texto alternativo** — `alt` presente mas sem sentido, ou que descreve a coisa errada.
- **Ordem lógica** — a ordem de foco faz *sentido*? A leitura linear conta a história certa? A máquina vê que há uma ordem; não julga se ela é lógica.
- **Rótulos significativos** — um botão nomeado "clique aqui" tem nome acessível (passa no axe) e é inútil para quem navega por lista de links.
- **Se o teclado realmente funciona** — o axe checa se elementos são focáveis; não verifica se o *fluxo* de teclado do seu combobox faz sentido (nota 09).
- **Legendas corretas** — vê que há um `<track>`; não confere se a legenda está certa e sincronizada.

> [!warning] "Passou no Lighthouse com 100" = acessível
> **O que acontece:** o time celebra o score 100 de acessibilidade do Lighthouse e considera a a11y resolvida. Um usuário de leitor de tela, semanas depois, não consegue usar metade da interface. **Por quê:** o score do Lighthouse reflete só as verificações automáticas (axe-core) — a metade computável do problema. Um `alt="foto"` inútil, uma ordem de foco ilógica e um combobox de teclado quebrado passam todos com nota máxima. **Como evitar:** leia o próprio Lighthouse — ele *avisa* que testes manuais são necessários e lista itens "a verificar manualmente". Score alto é piso, não teto. A metade que falta é a auditoria manual da nota [[03-Dominios/Tecnologia/Acessibilidade/Auditar e Testar/15 - Auditoria manual|15]].

## Onde a automação brilha de verdade: escala e regressão

Se a automação pega só metade, por que ela é indispensável? Porque essa metade é **grande, mecânica e recorrente** — e a máquina a cobre em **escala** e **continuamente**, coisa que nenhum humano faz. Um humano não confere o contraste de 1.257 elementos por página, em 200 páginas, a cada deploy. O axe faz isso em segundos.

O maior valor da auditoria automatizada não é o relatório pontual — é **rodar sempre**, pegando **regressões** antes que cheguem à produção. Um campo que perdeu o label num refactor, um contraste que quebrou numa mudança de tema: a automação flagra na hora. É exatamente por isso que ela pertence ao **código e ao CI**, não só à extensão de browser — e é para lá que a próxima nota vai.

**Auditoria automatizada em uma frase:** axe (e o Lighthouse/WAVE que o embutem) pega em segundos a metade mecânica das falhas — contraste, atributos, ARIA inválido — mas é cega para tudo que exige julgamento, então é o piso da auditoria, jamais o teto.

> [!tip] Vídeo — Getting Started with the axe DevTools Browser Extension
> [**Getting Started with the axe DevTools Browser Extension**](https://www.youtube.com/watch?v=iRGB40c_YJc) (Deque Systems, 2 min) — direto da criadora do axe-core: mostra o fluxo real de rodar a extensão numa página e ler o relatório, o mesmo relatório que embasa a tabela e os limites descritos acima.

## Casos práticos

**Cenário 1 — Lighthouse 100, produto inutilizável.** Um squad sobe um checkout novo. O Lighthouse relata `Accessibility: 100`. Ninguém investiga mais. Semanas depois, o time de suporte recebe uma reclamação: um usuário de leitor de tela não consegue completar a compra — o combobox de forma de pagamento não anuncia as opções ao navegar por teclado, e o botão "Finalizar" só tem um ícone, sem nome acessível *significativo* (tem `aria-label="botão"`, o que passa no axe, mas não diz nada). O score 100 media só o computável; o combobox quebrado e o rótulo vazio de sentido ficaram nos itens "a verificar manualmente" que o próprio relatório listava — e que ninguém abriu.

**Cenário 2 — axe no CI pegando regressão de contraste.** Um PR muda a paleta de cores do design system: o cinza de texto secundário passa de `#595959` para `#8C8C8C` para "suavizar" a UI. O teste de acessibilidade automatizado no pipeline (nota [[03-Dominios/Tecnologia/Acessibilidade/Auditar e Testar/14 - Testes de a11y no código|14]]) roda o axe contra os componentes renderizados e falha: a nova cor caiu para 3.1:1 de contraste, abaixo do 4.5:1 mínimo (nota [[03-Dominios/Tecnologia/Acessibilidade/Construir Acessível/11 - Cor, contraste e visual acessível|11]]). O PR é bloqueado antes do merge — exatamente o caso de uso onde a automação vale mais: não achar um problema novo, mas impedir que um problema resolvido volte.

## Armadilhas comuns

> [!warning] Confundir "passou no axe" com "é acessível"
> **O que acontece:** zero violações reportadas vira sinônimo de "está tudo certo" na cabeça do time. **Por quê:** o axe só reporta o que consegue verificar por regra. Ausência de erro reportado não é ausência de erro — é ausência do que é *mecanicamente checável*. Um `alt` presente e sem sentido, uma ordem de foco absurda: zero violações, zero acessibilidade real. **Como evitar:** trate "zero violações do axe" como um checkpoint, não como a linha de chegada. A linha de chegada inclui a auditoria manual da nota [[03-Dominios/Tecnologia/Acessibilidade/Auditar e Testar/15 - Auditoria manual|15]].

> [!warning] Rodar Lighthouse e axe DevTools achando que são duas opiniões independentes
> **O que acontece:** o time roda os dois, os dois concordam, e isso é lido como "confirmação cruzada" — dupla checagem que aumenta a confiança. **Por quê:** como a tabela acima mostra, a aba Accessibility do Lighthouse *é* axe-core por baixo. Rodar os dois é rodar o mesmo motor duas vezes com uma casca de UI diferente — não é redundância que aumenta cobertura, é a ilusão de cobertura. **Como evitar:** para diversificar de verdade, combine axe com uma ferramenta de motor diferente (ex.: IBM Equal Access, ou a inspeção visual do WAVE) — ou, melhor ainda, com auditoria manual, que é onde a cobertura de fato aumenta.

> [!warning] Ignorar os itens "a verificar manualmente" do relatório
> **O que acontece:** o relatório do Lighthouse e do axe DevTools lista, separadamente das violações, uma seção de itens que a ferramenta **não conseguiu avaliar automaticamente** (ex.: "verifique se a ordem de leitura é lógica"). Times leem só o score e o contador de violações, e pulam essa seção. **Por quê:** essa seção é literalmente a ferramenta admitindo seu próprio teto — é o mapa do que falta, escrito pela própria Deque/Google. Ignorá-la é jogar fora a informação mais honesta do relatório. **Como evitar:** trate a seção "a verificar manualmente" como uma checklist obrigatória de revisão humana, não como rodapé opcional.

## Como explicar em inglês

In an interview, the sharpest way to frame automated accessibility testing is to name both its strength and its ceiling in the same breath. Something like: *"We run axe-core in CI as a regression gate — it catches contrast failures, missing labels, and invalid ARIA on every pull request, at scale, for free. But we don't treat a clean axe report as proof of accessibility. Deque's own research puts automated coverage at roughly a third to half of WCAG issues, and the gaps are exactly the ones that matter most to users: alt text that's present but meaningless, a focus order that technically exists but doesn't make sense. So automated testing is our floor, not our ceiling — it buys us confidence on the mechanical layer and frees up manual testing time for the judgment calls a machine can't make."* This framing signals seniority because it shows you understand *why* the ceiling exists (computable vs. meaningful), not just that a number exists.

| PT | EN |
|----|----|
| teste automatizado | automated testing |
| teto de cobertura | coverage ceiling |
| falsa sensação de segurança | false sense of security |
| motor (de auditoria) | engine |
| regressão | regression |
| checagem por regra | rule-based check |
| julgamento humano | human judgment |
| a verificar manualmente | needs manual review |
| rede de segurança | safety net |

## O que vem a seguir

A automação só entrega seu valor de regressão quando roda **sozinha, o tempo todo** — no seu pipeline de testes. A próxima nota leva o axe para dentro do código: testes de componente que falham quando a acessibilidade quebra, e testes E2E que auditam a página inteira.

- [[03-Dominios/Tecnologia/Acessibilidade/Auditar e Testar/14 - Testes de a11y no código|14 — Testes de a11y no código]] — jest/vitest-axe, Testing Library, Playwright.
- [[03-Dominios/Tecnologia/Acessibilidade/Auditar e Testar/15 - Auditoria manual|15 — Auditoria manual]] — a metade que a máquina não vê.
- [[03-Dominios/Tecnologia/Acessibilidade/Construir Acessível/11 - Cor, contraste e visual acessível|11 — Cor e contraste]] — o que a automação mais detecta.

## Fontes

- **Deque** — [*axe-core*](https://github.com/dequelabs/axe-core) — o motor open source de auditoria por trás da maioria das ferramentas.
- **Deque** — [*The automated accessibility coverage question*](https://www.deque.com/automated-accessibility-testing-coverage/) — a análise da própria criadora do axe sobre quanto a automação de fato cobre.
- **WebAIM** — [*WAVE Web Accessibility Evaluation Tool*](https://wave.webaim.org/) — a ferramenta que sobrepõe os problemas no contexto visual da página.
- **Google** — [*Lighthouse Accessibility scoring*](https://developer.chrome.com/docs/lighthouse/accessibility/scoring) — a documentação que explicita que o score cobre só o automatizável.
