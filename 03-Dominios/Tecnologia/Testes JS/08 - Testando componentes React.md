---
title: "Testando componentes React"
created: 2026-07-06
updated: 2026-07-06
type: concept
status: seedling
fase: Adepto
tags:
  - testes
  - javascript
  - react
  - testing-library
publish: true
---

# Testando componentes React

> [!abstract] TL;DR
> O fluxo é: **`render(<Componente />)`** monta num DOM (jsdom), você busca elementos com as queries do `screen` (nota 07), simula a interação com **`user-event`** e afirma o resultado visível. Use **`userEvent.setup()`** (não o `fireEvent`) porque ele simula interações reais — foco, teclas, eventos na ordem certa. Interações e efeitos são assíncronos, então **`await`** os `userEvent` e use **`findBy`** para o que aparece depois. Teste **comportamento** (o que o usuário vê e faz), não props/estado interno. `render` limpa sozinho entre testes na config moderna.

## O problema: como testar um botão que abre um menu?

Você tem um componente: clica no botão, um menu aparece; clica num item, um callback dispara. Como testar isso sem abrir um browser? E, mais sutil: como testar **sem** amarrar o teste aos detalhes internos (o state `isOpen`, o nome do handler), para ele sobreviver a refatorações?

A resposta junta as duas notas anteriores: renderizar o componente num DOM simulado, interagir como um usuário (via Testing Library), e afirmar sobre o que fica visível. Esta nota é o fluxo concreto — o gesto que você repete em todo teste de componente.

## O fluxo básico: render → interagir → afirmar

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect, test } from 'vitest';
import { Contador } from './Contador';

test('incrementa ao clicar', async () => {
  const user = userEvent.setup();          // 1. prepara a simulação de usuário
  render(<Contador />);                     // 2. monta no jsdom

  const botao = screen.getByRole('button', { name: /incrementar/i });
  expect(screen.getByText('Total: 0')).toBeInTheDocument();

  await user.click(botao);                  // 3. interage (assíncrono!)

  expect(screen.getByText('Total: 1')).toBeInTheDocument(); // 4. afirma o visível
});
```

As quatro peças:

- **`render(jsx)`** monta o componente num DOM (o `environment: 'jsdom'` da nota 02). Retorna utilidades, mas prefira o **`screen`** global para as queries.
- **`screen.getByRole(...)`** encontra os elementos pelo que o usuário percebe (nota 07).
- **`userEvent`** simula a interação.
- **`expect(...).toBeInTheDocument()`** — matcher do `@testing-library/jest-dom`, que estende o `expect` com asserções de DOM (`toBeVisible`, `toHaveValue`, `toBeDisabled`...).

## `user-event` vs `fireEvent`: use `user-event`

Há duas formas de simular interação, e a escolha importa:

| | `fireEvent` | `userEvent` |
|-|-------------|-------------|
| O que faz | dispara **um** evento DOM cru (`click`) | simula a **interação completa** do usuário |
| Realismo | baixo (só o evento pedido) | alto (hover → focus → keydown → keyup → click, na ordem) |
| Digitar | `fireEvent.change` seta o valor de uma vez | `userEvent.type` dispara tecla por tecla |
| Recomendação | evite | **padrão** |

```tsx
const user = userEvent.setup();
await user.type(screen.getByLabelText('E-mail'), 'ana@ex.com'); // tecla por tecla
await user.click(screen.getByRole('button', { name: /entrar/i }));
await user.keyboard('{Enter}');
```

`userEvent` é mais fiel porque um clique real não é só um evento `click` — é uma cascata (mousedown, focus, mouseup, click) que seu componente pode depender. `fireEvent` pula isso e pode passar num teste que falharia com um usuário de verdade.

> [!warning] Esquecer o `await` no `userEvent`
> **O que acontece:** você faz `user.click(botao)` sem `await`, e a asserção seguinte falha porque a UI ainda não atualizou — ou o teste vira flaky. **Por quê:** desde a v14, os métodos do `userEvent` são **assíncronos** (retornam promise), para simular a interação de forma realista incluindo atualizações de estado. Sem `await`, você afirma antes da UI reagir. **Como evitar:** **sempre** `await` os métodos do `userEvent` (e por isso o teste é `async`). Também não esqueça o `userEvent.setup()` no início — a API v14 exige.

## UI assíncrona: `findBy` e `waitFor`

Componentes que carregam dados (um fetch no `useEffect`) mostram o conteúdo *depois*. Aí entra o `findBy` (nota 07), que espera o elemento aparecer:

```tsx
test('mostra os pedidos após carregar', async () => {
  render(<ListaPedidos />);

  // enquanto carrega:
  expect(screen.getByText(/carregando/i)).toBeInTheDocument();

  // findBy espera o elemento surgir (após o fetch resolver):
  expect(await screen.findByText('Pedido #42')).toBeInTheDocument();

  // e o "carregando" sumiu:
  expect(screen.queryByText(/carregando/i)).not.toBeInTheDocument();
});
```

`findBy` (para "apareceu") e `waitFor` (para "esta asserção passa a valer em algum momento") cobrem o assíncrono de UI. De onde vêm os dados desse fetch num teste? De um mock de rede — o assunto da próxima nota (MSW).

> [!question]- O que eu devo (e não devo) testar num componente?
> **Teste o comportamento que o usuário observa:** renderiza o conteúdo certo dadas as props? responde à interação (clique, digitação) mudando o que aparece? mostra estados de loading/erro/vazio? chama os callbacks certos (`onSubmit`) com os dados certos? **Não teste implementação:** o valor de um `useState`, se um `useEffect` rodou, nomes de handlers, estrutura de markup irrelevante. O teste da [[03-Dominios/Engenharia/Testes/06 - Testar comportamento, não implementação|Engenharia/Testes 06]] vale integralmente aqui — se você renomear um state ou trocar `useState` por `useReducer` sem mudar o que o usuário vê, o teste deve continuar verde. Se ele quebra, estava testando a coisa errada. Uma boa heurística: se a asserção menciona algo que o usuário não consegue perceber, reconsidere.

**Testando componentes React em uma frase:** `render` monta no jsdom, `userEvent.setup()` + `await user.click/type` simula a interação real, as queries do `screen` acham os elementos pelo que o usuário vê, `findBy` espera a UI assíncrona, e você afirma sempre sobre o **comportamento visível** — nunca sobre state ou props internos.

## Em entrevista

> "The flow is render, interact, assert. I `render` the component into jsdom, query elements with `screen` by role or label, simulate interaction with `userEvent` — not `fireEvent`, because `userEvent` reproduces the full real interaction, focus, keystrokes, in order. Since v14 those methods are async, so I `await user.click`. For UI that loads data I use `findBy`, which waits for the element to appear. And I test behavior — what the user sees and does — never internal state or props, so the test survives refactors like swapping `useState` for `useReducer`."

| PT | EN |
|----|----|
| Renderizar | To render |
| Evento de usuário | User event |
| Interação completa | Full interaction |
| UI assíncrona | Async UI |
| Estado de carregamento | Loading state |
| Comportamento observável | Observable behavior |

## O que vem a seguir

O teste de componente com fetch precisa de dados vindos "da rede" — e chamá-la de verdade é lento e frágil. A solução moderna é interceptar a rede na camada certa, com o MSW.

- [[03-Dominios/Tecnologia/Testes JS/09 - MSW - mockando a rede|09 — MSW: mockando a rede]] — interceptar HTTP em testes.
- [[03-Dominios/Tecnologia/Testes JS/10 - Testando hooks e estado|10 — Testando hooks e estado]] — testar a lógica fora do componente.

## Fontes

- **Testing Library** — [*React Testing Library — `render`*](https://testing-library.com/docs/react-testing-library/api/) — montar componentes.
- **Testing Library** — [*user-event*](https://testing-library.com/docs/user-event/intro) — `setup()` e a simulação realista.
- **Testing Library** — [*jest-dom matchers*](https://github.com/testing-library/jest-dom) — `toBeInTheDocument`, `toHaveValue`, etc.
