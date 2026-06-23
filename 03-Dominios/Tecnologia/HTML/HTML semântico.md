---
title: "HTML semântico"
created: 2026-04-01
updated: 2026-06-23
type: concept
status: evergreen
tags:
  - html
  - frontend
  - web
  - entrevista
publish: true
aliases:
  - HTML
---

# HTML semântico

> [!nota] Nota-semente
> Conteúdo migrado do antigo "HTML e CSS" na reorganização em camadas. Cobre **HTML semântico moderno**. Será expandida numa trilha 3-fases (Iniciado/Adepto/Magus) no Batch 5. A parte de estilo vive em [[03-Dominios/Tecnologia/CSS/index|CSS]].

**HTML (HyperText Markup Language)** é a linguagem de marcação que estrutura documentos na web — estrutura e semântica, separada da apresentação ([[03-Dominios/Tecnologia/CSS/index|CSS]]) e do comportamento ([[JavaScript Fundamentals]]). Em entrevista, o que diferencia um senior: usar o elemento certo (`<button>`, `<nav>`, `<main>`, `<article>` — não `<div>` genérico), acessibilidade (ARIA, navegação por teclado, contraste) e SEO que vêm de graça da semântica correta.

## HTML semântico

HTML semântico **significa usar elementos pelo significado**, não pela aparência. `<div>` é o último recurso.

### Elementos estruturais (HTML5)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minha página</title>
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/about">About</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <article>
            <header>
                <h1>Título do artigo</h1>
                <time datetime="2026-04-11">11 de abril de 2026</time>
            </header>
            <section>
                <h2>Seção</h2>
                <p>Conteúdo...</p>
            </section>
            <aside>
                <h3>Relacionado</h3>
                <ul>...</ul>
            </aside>
            <footer>
                <p>Autor: Maria</p>
            </footer>
        </article>
    </main>

    <footer>
        <p>&copy; 2026 MedEspecialista</p>
    </footer>
</body>
</html>
```

**Principais tags estruturais:**

| Tag         | Uso                                           |
| ----------- | --------------------------------------------- |
| `<header>`  | Cabeçalho de página OU de seção/artigo        |
| `<nav>`     | Navegação principal                           |
| `<main>`    | Conteúdo principal (1 por página)             |
| `<article>` | Conteúdo auto-contido (post, card, notícia)   |
| `<section>` | Agrupamento temático com heading              |
| `<aside>`   | Conteúdo relacionado mas secundário (sidebar) |
| `<footer>`  | Rodapé de página OU de seção/artigo           |

### Elementos inline importantes

```html
<strong>importante</strong>        <!-- mais forte que <b> -->
<em>ênfase</em>                     <!-- mais forte que <i> -->
<mark>destacado</mark>              <!-- highlight -->
<code>código</code>
<kbd>Ctrl+C</kbd>                   <!-- teclado -->
<samp>output</samp>                  <!-- saída de programa -->
<var>x</var>                         <!-- variável matemática -->
<abbr title="HyperText Markup Language">HTML</abbr>
<cite>Título de obra</cite>
<q>citação curta</q>
<blockquote cite="https://...">citação longa</blockquote>
<time datetime="2026-04-11T10:00">11 de abril às 10h</time>
<address>
    <a href="mailto:contact@example.com">contact@example.com</a>
</address>
```

### Formulários

```html
<form action="/submit" method="POST">
    <fieldset>
        <legend>Dados pessoais</legend>

        <div>
            <label for="name">Nome</label>
            <input type="text" id="name" name="name" required autocomplete="name">
        </div>

        <div>
            <label for="email">Email</label>
            <input type="email" id="email" name="email" required autocomplete="email">
        </div>

        <div>
            <label for="password">Senha</label>
            <input
                type="password"
                id="password"
                name="password"
                required
                minlength="8"
                autocomplete="new-password"
            >
        </div>

        <div>
            <label for="birth">Nascimento</label>
            <input type="date" id="birth" name="birth">
        </div>

        <div>
            <label for="role">Função</label>
            <select id="role" name="role" required>
                <option value="">Selecione...</option>
                <option value="patient">Paciente</option>
                <option value="doctor">Médico</option>
            </select>
        </div>

        <div>
            <label>
                <input type="checkbox" name="terms" required>
                Aceito os termos
            </label>
        </div>
    </fieldset>

    <button type="submit">Enviar</button>
    <button type="button">Cancelar</button>
</form>
```

**Input types modernos:**

| Type                               | Uso                                           |
| ---------------------------------- | --------------------------------------------- |
| `text`                             | Texto genérico                                |
| `email`                            | Valida formato email, teclado mobile adaptado |
| `tel`                              | Teclado numérico em mobile                    |
| `url`                              | Valida formato URL                            |
| `number`                           | Só números, com spinners                      |
| `date` / `time` / `datetime-local` | Date picker nativo                            |
| `month` / `week`                   | Seleção mês/semana                            |
| `color`                            | Color picker                                  |
| `range`                            | Slider                                        |
| `search`                           | Search com ícone nativo                       |
| `password`                         | Oculta input                                  |
| `file`                             | File picker                                   |
| `hidden`                           | Não visível, envia valor                      |
| `checkbox` / `radio`               | Escolhas                                      |

**Atributos de validação:**

```html
<input
    type="email"
    required
    minlength="5"
    maxlength="100"
    pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
    autocomplete="email"
    inputmode="email"
>
```

### Acessibilidade — ARIA e roles

```html
<!-- Landmark roles (implícitos via HTML5 semântico) -->
<nav role="navigation">          <!-- redundante, nav já é navigation -->
<main role="main">                <!-- redundante -->
<section role="region" aria-labelledby="title-1">
    <h2 id="title-1">Seção</h2>
</section>

<!-- Botão icon-only precisa de label -->
<button aria-label="Fechar modal" onClick={close}>
    <svg>...</svg>
</button>

<!-- Live regions -->
<div role="status" aria-live="polite">
    Item adicionado ao carrinho
</div>

<div role="alert" aria-live="assertive">
    Erro: conexão perdida
</div>

<!-- Formulário com erro -->
<input
    id="email"
    aria-invalid="true"
    aria-describedby="email-error"
>
<span id="email-error" role="alert">Email inválido</span>

<!-- Botão desativado semantically -->
<button aria-disabled="true">Disabled</button>
```

**Regras de ouro de a11y:**

1. **HTML semântico primeiro** — `<button>`, não `<div onClick>`
2. **Alt em imagens** — `alt=""` para decorativas, descritivo para conteúdo
3. **Labels em forms** — `<label for>` ou envolvendo o input
4. **Heading hierarchy** — h1 → h2 → h3, não pule níveis
5. **Keyboard navigation** — tudo interativo acessível por Tab
6. **Focus visible** — não esconda `:focus`
7. **Color contrast** — texto normal 4.5:1, large 3:1 (WCAG AA)
8. **Skip link** — `<a href="#main">Pular para conteúdo</a>`

### HTML APIs úteis

```html
<!-- Lazy loading de imagens -->
<img src="hero.jpg" alt="..." loading="lazy" decoding="async">

<!-- Srcset responsive -->
<img
    src="photo-800.jpg"
    srcset="photo-400.jpg 400w, photo-800.jpg 800w, photo-1600.jpg 1600w"
    sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1600px"
    alt="..."
>

<!-- Picture — arte direção -->
<picture>
    <source media="(max-width: 600px)" srcset="mobile.jpg">
    <source media="(max-width: 1200px)" srcset="tablet.jpg">
    <img src="desktop.jpg" alt="...">
</picture>

<!-- Dialog (modal nativo) -->
<dialog id="modal">
    <form method="dialog">
        <p>Confirmar ação?</p>
        <button value="cancel">Cancelar</button>
        <button value="confirm">OK</button>
    </form>
</dialog>
<script>
    document.getElementById('modal').showModal();
</script>

<!-- Details / summary -->
<details>
    <summary>Clique para expandir</summary>
    <p>Conteúdo escondido</p>
</details>

<!-- Popover (HTML5, 2024) -->
<button popovertarget="my-popover">Toggle</button>
<div id="my-popover" popover>Popover content</div>
```

---

## Veja também

- [[03-Dominios/Tecnologia/CSS/index|CSS]] — a apresentação visual
- [[03-Dominios/Tecnologia/Plataforma Web/index|Plataforma Web]] — as APIs do navegador
- [[React]] · [[JavaScript Fundamentals]]
