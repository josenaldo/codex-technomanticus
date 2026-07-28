---
title: "Mídia e movimento"
created: 2026-07-27
updated: 2026-07-27
type: concept
status: seedling
fase: Adepto
tags:
  - acessibilidade
  - a11y
  - midia
  - movimento
publish: true
---

# Mídia e movimento

> [!abstract] TL;DR
> Todo conteúdo que não é texto precisa de uma **alternativa em texto ou controle equivalente**: vídeo precisa de **legendas** (para quem não ouve) e, idealmente, **transcrição** e **audiodescrição** (para quem não vê); áudio precisa de transcrição; nada com som pode depender só do som. E o **movimento** tem duas exigências firmes: animações longas ou automáticas precisam poder ser **pausadas** (2.2.2), e você deve respeitar `prefers-reduced-motion` de quem pediu menos movimento — porque para pessoas com desordens vestibulares, uma transição exuberante causa náusea real, não só incômodo. Acima de tudo: **nada pode piscar mais de 3 vezes por segundo** (2.3.1), sob risco de desencadear convulsões.

Última parada do SG2, e a que sai do território de texto e widgets para o de vídeo, som e animação. É onde a acessibilidade encontra o conteúdo mais rico — e onde a exclusão pode ser não só frustrante, mas fisicamente perigosa. Vamos do vídeo ao pixel que pisca.

## A regra-mãe: toda mídia precisa de alternativa

O princípio **Perceptível** do POUR (nota 04) tem um mandamento central: se a informação chega por um sentido, precisa haver um caminho para quem não dispõe daquele sentido. Traduzido para mídia:

| Mídia | Quem fica de fora sem alternativa | Alternativa necessária |
|-------|-----------------------------------|------------------------|
| Vídeo com fala | Surdos, ambiente sem som | **Legendas** (captions) sincronizadas |
| Vídeo com informação visual | Cegos, baixa visão | **Audiodescrição** + transcrição |
| Áudio / podcast | Surdos | **Transcrição** em texto |
| Imagem informativa | Cegos | Texto alternativo (`alt`, nota já vista no HTML) |

O WCAG detalha isso na diretriz 1.2 (critérios 1.2.1 a 1.2.5), mas a régra prática cabe numa frase: **nenhuma informação essencial pode existir só numa forma que exclua um sentido**.

## Legendas não são transcrição (e não são iguais entre si)

Três termos que os times confundem, e a confusão gera entrega errada:

- **Legendas (captions)** — texto **sincronizado** com o vídeo, sobreposto na hora certa. *Legendas para surdos e ensurdecidos (SDH/closed captions)* incluem não só a fala mas também sons relevantes ("[música tensa]", "[porta batendo]") — porque quem não ouve precisa saber que houve um som significativo, não só o que foi dito. Diferem das *legendas de tradução*, que só vertem a fala de um idioma para outro e presumem que você ouve o resto.
- **Transcrição** — o texto **completo** do conteúdo, num bloco à parte, **não** sincronizado. Serve para ler no lugar de assistir, para buscar (Ctrl+F), e é a única alternativa viável para conteúdo **só de áudio** (podcast). Beneficia também quem prefere ler a ouvir — *curb-cut effect*.
- **Audiodescrição** — uma faixa de narração que descreve o que acontece **visualmente** nas pausas do diálogo ("ela abre a carta e empalidece"), para quem não vê a tela. É a alternativa mais trabalhosa e a mais esquecida.

> [!question]- Legenda automática do YouTube já não resolve?
> Ajuda, mas não basta sozinha para conteúdo essencial. As legendas automáticas (ASR) erram nomes, termos técnicos, pontuação, e não marcam quem fala nem os sons não-verbais — e uma legenda errada pode ser pior que nenhuma, porque transmite informação falsa com aparência de confiável. Para conteúdo importante (um curso, um vídeo institucional, uma aula), a legenda automática é o **rascunho**, não a entrega: alguém revisa. Para conteúdo casual, a automática é um piso aceitável. A régua é a mesma de sempre — proporcional à criticidade do conteúdo.

No HTML, o elemento `<track>` embute legendas num `<video>` nativo:

```html
<video controls>
  <source src="aula.mp4" type="video/mp4">
  <track kind="captions" src="aula-pt.vtt" srclang="pt" label="Português" default>
</video>
<!-- + link para a transcrição completa em texto, próximo ao vídeo -->
```

## Movimento que pode ser pausado

Passando do conteúdo para a **interface animada**. Carrosséis que giram sozinhos, banners que deslizam, textos que rolam automaticamente — tudo que se move, pisca ou rola por mais de **5 segundos** e começa **automaticamente** cai no critério **2.2.2 (Pausar, Parar, Ocultar, nível A)**: o usuário precisa poder **parar** o movimento.

Por quê? Movimento automático prejudica vários grupos ao mesmo tempo: quem tem TDAH ou dificuldade de atenção é constantemente puxado pelo que se mexe; quem lê devagar não termina antes do carrossel trocar; quem usa leitor de tela pode ter o conteúdo mudando sob seus pés. Um carrossel sem botão de pausa é hostil a todos eles. A correção é banal — um botão pausa/play — e quase nunca implementada.

## `prefers-reduced-motion`: respeitando o sistema vestibular

Aqui está a exigência que mais surpreende quem nunca ouviu falar. Para pessoas com **desordens vestibulares**, movimento na tela — um *parallax* exuberante, um zoom brusco, uma transição de página que voa — pode causar **tontura, náusea e enxaqueca de verdade**, o mesmo mecanismo do enjoo de movimento. Não é preferência estética; é resposta fisiológica.

Os sistemas operacionais oferecem uma configuração de "reduzir movimento", e o navegador a expõe via *media query* `prefers-reduced-motion`. Respeitá-la é trivial e transforma a experiência de quem precisa:

```css
/* animação padrão, exuberante */
.card { transition: transform 300ms ease; }
.modal { animation: slide-in 400ms; }

/* para quem pediu menos movimento: corta ou reduz drasticamente */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

A boa prática de sistema: projete as animações como **enriquecimento** que pode ser removido sem quebrar a função. Se apagar todas as transições torna o app inutilizável, a animação estava carregando informação que deveria estar na estrutura. O critério relacionado **2.3.3 (Animação a partir de Interações, AAA)** formaliza isso, mas mesmo em nível AA respeitar a preferência é padrão de ofício hoje.

## O limiar perigoso: nada pisca acima de 3 Hz

Terminamos no critério mais sério de todo o WCAG, porque a falha aqui não é inconveniência — é **risco de saúde**. O critério **2.3.1 (Três Flashes ou Abaixo do Limiar, nível A)** proíbe qualquer conteúdo que **pisque mais de três vezes por segundo**, a menos que os flashes sejam pequenos e de baixo contraste.

O motivo é a **epilepsia fotossensível**: flashes rápidos, sobretudo em vermelho saturado e ocupando área grande da tela, podem **desencadear convulsões** em pessoas suscetíveis. Não é hipotético — há casos documentados de conteúdo web e até de ataques deliberados com GIFs piscantes contra pessoas com epilepsia.

> [!warning] Conteúdo que pisca acima de 3 vezes por segundo
> **O que acontece:** uma animação, GIF, vídeo ou efeito que pisca rápido (> 3 Hz) em área significativa da tela pode desencadear uma convulsão em quem tem epilepsia fotossensível.
> **Por quê:** o cérebro fotossensível responde a estímulos luminosos rápidos e rítmicos com atividade elétrica anormal. É um risco físico real, não um desconforto.
> **Como evitar:** não crie conteúdo que pisque acima de 3 vezes por segundo, ponto. Se receber mídia de terceiros (um anúncio, um GIF de usuário), teste com uma ferramenta como o **PEAT** (Photosensitive Epilepsy Analysis Tool) antes de publicar. Este é o critério onde "não sabíamos" não é desculpa aceitável.

**Mídia e movimento em uma frase:** toda mídia precisa de alternativa em texto (legenda, transcrição, audiodescrição), todo movimento automático precisa poder parar e respeitar `prefers-reduced-motion`, e nada — jamais — pode piscar mais de três vezes por segundo.

## O que vem a seguir

Com esta nota, o SG2 fecha: você sabe construir foco, formulários, os padrões APG, a11y em React, cor/contraste e mídia. Sabe *fazer* acessível. Falta o rigor de *provar* que fez — porque "acho que está acessível" não é auditoria. O SG3 é dedicado a isso: as ferramentas automáticas e seus limites, os testes de a11y no código, e a auditoria manual que pega o que a máquina não vê.

- [[03-Dominios/Tecnologia/Acessibilidade/Auditar e Testar/index|SG3 — Auditar e Testar]] — o próximo sub-galho: provar que funciona.
- [[03-Dominios/Tecnologia/Acessibilidade/Auditar e Testar/13 - Auditoria automatizada|13 — Auditoria automatizada]] — axe, Lighthouse, WAVE e o teto da automação.
- [[03-Dominios/Tecnologia/Acessibilidade/Construir Acessível/11 - Cor, contraste e visual acessível|11 — Cor e contraste]] — a nota irmã sobre o outro lado do visual.

## Fontes

- **W3C** — [*Understanding SC 1.2.2: Captions (Prerecorded)*](https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html) — a exigência de legendas e a distinção de audiodescrição (1.2.5).
- **W3C** — [*Understanding SC 2.3.1: Three Flashes or Below Threshold*](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html) — o limiar de flashes e a epilepsia fotossensível.
- **MDN Web Docs** — [*prefers-reduced-motion*](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) — a media query e a implementação de movimento reduzido.
- **WebAIM** — [*Captions, Transcripts, and Audio Descriptions*](https://webaim.org/techniques/captions/) — as diferenças práticas entre os três tipos de alternativa de mídia.
