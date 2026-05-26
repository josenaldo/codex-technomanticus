---
title: "Bootstrap"
created: 2026-04-01
updated: 2026-04-01
type: concept
status: seedling
tags:
  - javascript
  - frontend
  - ui-library
  - entrevista
publish: true
---

# Bootstrap

Framework CSS mais popular do mundo — grid system, componentes prontos e prototipagem rápida.

## O que é

Bootstrap é um framework CSS open-source (Twitter, 2011) que fornece um sistema de grid responsivo, componentes de UI pré-estilizados, e utilities CSS. Ideal para prototipagem rápida e projetos que não precisam de design custom.

## Como funciona

### Grid System (12 colunas)

```html
<div class="container">
  <div class="row">
    <div class="col-md-8">Conteúdo principal</div>
    <div class="col-md-4">Sidebar</div>
  </div>
</div>
```

Breakpoints: `xs` (<576px), `sm` (≥576px), `md` (≥768px), `lg` (≥992px), `xl` (≥1200px), `xxl` (≥1400px).

### Componentes principais

- **Navbar, Breadcrumb, Pagination** — navegação
- **Card, Modal, Accordion, Tabs** — conteúdo
- **Button, Form, Input Group** — interação
- **Alert, Toast, Badge** — feedback
- **Table, Spinner, Progress** — dados e loading

### Utilities

```html
<div class="d-flex justify-content-between align-items-center p-3 mb-2 bg-primary text-white rounded">
  Utility classes: display, spacing, colors, borders
</div>
```

### Bootstrap com React

```tsx
// react-bootstrap
import { Button, Card, Container, Row, Col } from 'react-bootstrap';

function Dashboard() {
  return (
    <Container>
      <Row>
        <Col md={8}><Card>...</Card></Col>
        <Col md={4}><Card>...</Card></Col>
      </Row>
    </Container>
  );
}
```

## Quando usar

- **Prototipagem rápida:** resultado visual aceitável em minutos
- **Admin panels / back-office:** onde design custom não é prioridade
- **Projetos sem designer:** Bootstrap fornece um design system razoável out-of-the-box
- **Equipes que já conhecem:** curva de aprendizado baixa

## Armadilhas comuns

- **Override excessivo:** se está sobrescrevendo 80% do Bootstrap, use outra solução
- **Design genérico:** sites "cara de Bootstrap" — customizar variáveis Sass ajuda
- **Bundle grande:** importar tudo quando usa poucos componentes. Usar imports seletivos

## How to explain in English

"Bootstrap is a CSS framework I use for rapid prototyping and admin interfaces. Its 12-column grid system and pre-built components let me create functional UIs quickly. For production applications with custom design requirements, I prefer more flexible solutions like Material UI or Mantine."

### Key vocabulary

- sistema de grid → grid system
- componente pré-construído → pre-built component
- ponto de quebra → breakpoint
- prototipagem → prototyping

## Recursos

- [Bootstrap Docs](https://getbootstrap.com/docs/)
- [React Bootstrap](https://react-bootstrap.netlify.app/)

## Veja também

- [[HTML e CSS]]
- [[Material UI]]
- [[03-Dominios/JavaScript/Frontend/Mantine]]
- [[React]]
