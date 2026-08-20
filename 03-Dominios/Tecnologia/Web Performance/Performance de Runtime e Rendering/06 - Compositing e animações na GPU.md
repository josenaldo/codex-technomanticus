---
title: "Compositing e animações na GPU"
created: 2026-07-06
updated: 2026-07-06
type: concept
status: seedling
fase: adepto
tags:
  - web-performance
  - runtime
  - compositing
  - gpu
publish: true
---

# Compositing e animações na GPU

> [!abstract] TL;DR
> O browser pode dividir a página em **camadas de composição** e desenhá-las separadamente, combinando-as no fim pela **GPU**. Uma camada que só muda por `transform`/`opacity` é animada inteiramente na GPU, sem tocar a main thread nem disparar layout/paint — daí a fluidez a 60 fps. Você promove um elemento a camada com `will-change: transform` (ou `transform: translateZ(0)`). Mas camada tem custo de memória: **cada uma consome VRAM**, e promover elementos demais (ou deixar `will-change` fixo em tudo) degrada em vez de ajudar. A arte é promover **só o que anima**, e só enquanto anima.

## O problema: por que a animação suave às vezes fica granulada

Você aplicou `transform` na animação (lição da [[03-Dominios/Tecnologia/Web Performance/Performance de Runtime e Rendering/04 - Reflow, repaint e o custo do layout|nota 04]]) e ficou lisa. Empolgado, adicionou `will-change: transform` em dezenas de elementos "para acelerar tudo". Resultado: a página ficou mais lenta, o scroll começou a travar, e no celular a aba às vezes recarrega sozinha (o SO matou a página por memória).

O que aconteceu? Você entrou no mundo das **camadas de composição** — a ferramenta que torna as animações fluidas, mas que cobra memória e vira uma faca de dois gumes quando usada sem critério. Entender como o browser cria camadas, e o custo delas, é o que separa "animação a 60 fps" de "página que engasga por excesso de camadas".

## O que é uma camada de composição

Pense na página como um desenho feito de **transparências empilhadas** (como as antigas transparências de retroprojetor). Em vez de repintar a página inteira quando um elemento se move, o browser pode desenhar esse elemento numa **camada própria** e depois só **reposicionar a transparência** sobre as outras — trabalho que a **GPU** faz muito bem e muito rápido.

Esse passo de "combinar as transparências na imagem final" é o **compositing**, a etapa mais barata do pipeline de rendering. Quando um elemento está na própria camada e você anima apenas seu `transform` ou `opacity`, o browser **não recalcula layout nem repinta nada** — só a GPU recompõe as camadas. Por isso essas animações rodam a 60 fps mesmo com a main thread ocupada: elas nem passam por ela.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
graph TB
    subgraph SEM["Sem camada própria"]
        A[muda posição] --> B[repinta a região<br/>na main thread]
    end
    subgraph COM["Com camada de composição"]
        C[muda transform] --> D[GPU recompõe<br/>as camadas]
        D --> E[✓ 60fps, fora da main thread]
    end
    style B fill:#F5A623,color:#000
    style E fill:#4A90D9,color:#fff
```

## Como promover um elemento a camada

O browser cria camadas automaticamente em alguns casos (vídeos, `<canvas>`, elementos com certas propriedades). Para pedir explicitamente, o jeito moderno é o **`will-change`**:

```css
/* Diz ao browser: este elemento vai mudar de transform — prepare uma camada */
.card-animado {
  will-change: transform;
}
```

O `will-change` avisa o browser **com antecedência** que a propriedade vai mudar, para ele promover o elemento a camada *antes* da animação começar (evitando um soluço no primeiro frame). O truque antigo `transform: translateZ(0)` (ou `translate3d(0,0,0)`) força o mesmo efeito abusando da aceleração 3D — ainda funciona, mas `will-change` é a forma correta e legível.

## O custo: memória e o perigo do excesso

Aqui está a parte que quase todo mundo aprende errado: **camada não é grátis**. Cada camada de composição ocupa **memória de vídeo (VRAM)** — o browser precisa guardar o bitmap daquele elemento separadamente. Poucas camadas para o que anima: ótimo. Centenas de camadas porque você pôs `will-change` em tudo: a memória estoura, e gerenciar tantas camadas custa mais do que economiza.

> [!warning] `will-change` permanente em muitos elementos
> **O que acontece:** o dev adiciona `will-change: transform` no CSS de todos os cards, botões e imagens "para deixar tudo acelerado". A página fica mais lenta e consome muito mais memória, e no mobile chega a ser morta pelo SO. **Por quê:** `will-change` promove cada elemento a uma **camada permanente**, cada uma comendo VRAM. O browser passa a gerenciar dezenas ou centenas de camadas o tempo todo, mesmo sem nada animando. O tiro sai pela culatra: a otimização vira o gargalo. **Como evitar:** use `will-change` **cirurgicamente** — só nos poucos elementos que realmente animam, e idealmente **só enquanto animam** (adicione via JS/`:hover` antes da animação, remova depois). A regra oficial: "não aplique `will-change` a muitos elementos" e "não o deixe ligado indefinidamente".

> [!question]- Se camada é cara, por que não deixar o browser decidir sozinho quando criar?
> Na maioria dos casos, **deixe** — o browser é bom nisso e promove automaticamente o que precisa. Você só intervém com `will-change` quando há um problema concreto: uma animação que soluça no primeiro frame (porque a camada é criada tarde) ou um elemento que anima repetidamente e você quer garantir que ele fique numa camada estável. `will-change` é um remédio para um sintoma medido, não um tempero para espalhar. Aplicá-lo preventivamente em tudo é como manter o pé no acelerador e no freio ao mesmo tempo: você paga o custo sem o benefício. Meça (painel Layers do DevTools), promova o que precisa, remova quando não precisar mais.

**Compositing e GPU em uma frase:** o browser desenha elementos em camadas separadas e as combina na GPU, então animar só `transform`/`opacity` de uma camada roda a 60 fps fora da main thread — mas cada camada custa VRAM, então promova (com `will-change`) apenas o que anima, e só enquanto anima.

## Como explicar em inglês

> "The browser can split the page into **compositor layers** and combine them on the **GPU**. A layer that only changes via `transform` or `opacity` is animated entirely on the GPU — no layout, no paint, not even the main thread — which is why those animations hit 60 fps even under load. I promote an element to its own layer with `will-change: transform`. But layers cost **GPU memory**, so promoting everything backfires — the page gets slower and can be killed on mobile for memory. The rule is surgical: promote only what actually animates, and ideally only while it's animating."

| PT | EN |
|----|----|
| Camada de composição | Compositor layer |
| Aceleração por GPU | GPU acceleration |
| Promover a camada | Promote to a layer |
| Memória de vídeo | GPU / video memory (VRAM) |
| Explosão de camadas | Layer explosion |
| Cirúrgico | Surgical |

## O que vem a seguir

Você domina o custo de layout e de composição. Falta o outro Core Web Vital que vive em runtime: o **CLS** disparado *depois* do carregamento — conteúdo que é injetado, banners que aparecem, elementos que expandem e empurram o que o usuário está lendo. É um problema de estabilidade que as técnicas de imagem/fonte do Galho 2 não cobrem.

- [[03-Dominios/Tecnologia/Web Performance/Performance de Runtime e Rendering/07 - CLS em runtime|07 — CLS em runtime]] — deslocamentos pós-carregamento e como preveni-los.
- [[03-Dominios/Tecnologia/CSS/12 - Performance CSS|CSS 12 — Performance CSS]] — `contain`, `content-visibility` e custo de CSS, como reforço.

## Fontes

- **web.dev (Google)** — [*Stick to compositor-only properties and manage layer count*](https://web.dev/articles/stick-to-compositor-only-properties-and-manage-layer-count) — camadas, GPU e o custo de memória.
- **MDN Web Docs** — [*will-change*](https://developer.mozilla.org/en-US/docs/Web/CSS/will-change) — uso correto e os avisos contra o excesso.
- **Chrome for Developers** — [*Analyze rendering with the Layers panel*](https://developer.chrome.com/docs/devtools/rendering/) — inspecionar camadas de composição no DevTools.
