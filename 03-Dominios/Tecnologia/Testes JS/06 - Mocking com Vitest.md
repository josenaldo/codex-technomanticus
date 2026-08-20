---
title: "Mocking com Vitest"
created: 2026-07-06
updated: 2026-07-06
type: concept
status: seedling
fase: Adepto
tags:
  - testes
  - javascript
  - vitest
  - mocking
publish: true
---

# Mocking com Vitest

> [!abstract] TL;DR
> `vi` é o namespace de mocking do Vitest (o `jest` do Jest). **`vi.fn()`** cria uma função-mock que registra chamadas e pode fingir retornos (`mockReturnValue`, `mockResolvedValue`, `mockImplementation`). **`vi.spyOn(obj, 'metodo')`** espiona um método real — observando-o e, opcionalmente, substituindo-o. **`vi.mock('./modulo')`** substitui um módulo inteiro (é **içado** para o topo do arquivo, o que exige `vi.hoisted` para variáveis usadas na factory). A disciplina que evita vazamento entre testes: **resete os mocks** (`clearAllMocks` no `afterEach`, ou `clearMocks: true` na config). A teoria dos doubles está em Engenharia/Testes 05; aqui é a mecânica.

## O problema: testar uma unidade sem arrastar o mundo junto

Você quer testar uma função que envia um e-mail ao criar um pedido. Rodar o teste de verdade mandaria um e-mail real, chamaria a API de pagamento, gravaria no banco — lento, frágil e com efeitos colaterais reais. Você precisa **isolar** a unidade sob teste, substituindo suas dependências por dublês controláveis. Isso é *mocking*.

A teoria — dummy, stub, spy, mock, fake, e quando usar cada um — vive em [[03-Dominios/Engenharia/Testes/05 - Test doubles - dummy, stub, spy, mock, fake|Engenharia/Testes 05]]. Esta nota é a **mecânica no Vitest**: como criar cada tipo de dublê com o namespace `vi`, e como não deixá-los vazarem entre os testes (o erro que mais gera flaky de mocking).

## `vi.fn()`: a função-mock

`vi.fn()` cria uma função que **registra tudo** que aconteceu com ela e pode **fingir** comportamento:

```ts
import { vi, test, expect } from 'vitest';

test('registra chamadas', () => {
  const cb = vi.fn();
  [1, 2, 3].forEach(cb);

  expect(cb).toHaveBeenCalledTimes(3);
  expect(cb).toHaveBeenCalledWith(2, 1, [1, 2, 3]); // 2º arg do forEach é o índice
  expect(cb).toHaveBeenLastCalledWith(3, 2, [1, 2, 3]);
});
```

Para fingir retornos (transformando o spy num **stub**):

```ts
const getPreco = vi.fn();
getPreco.mockReturnValue(10);              // sempre retorna 10
getPreco.mockResolvedValue(10);            // Promise.resolve(10) — para async
getPreco.mockImplementation((id) => id * 2); // lógica customizada
getPreco.mockReturnValueOnce(99);          // só na próxima chamada
```

Os matchers de asserção sobre mocks — `toHaveBeenCalled`, `toHaveBeenCalledWith`, `toHaveBeenCalledTimes` — são o vocabulário do teste **baseado em interação** (verificar *que* algo foi chamado), que a [[03-Dominios/Engenharia/Testes/06 - Testar comportamento, não implementação|Engenharia/Testes 06]] contrasta com o baseado em estado.

## `vi.spyOn()`: espiar o método real

`vi.spyOn(objeto, 'metodo')` embrulha um método **existente** num spy. Por padrão ele ainda **chama o original** (só observa); você pode substituí-lo encadeando um `mock*`:

```ts
const logger = { salvar: (msg: string) => { /* grava no disco */ } };

const spy = vi.spyOn(logger, 'salvar');           // observa (ainda executa o real)
processar(logger);
expect(spy).toHaveBeenCalledWith('processado');

const spy2 = vi.spyOn(logger, 'salvar').mockImplementation(() => {}); // substitui (não grava)
```

`spyOn` é ideal quando você quer verificar (ou neutralizar) **um** método de um objeto real, sem substituir o objeto inteiro — por exemplo, espiar `console.error` ou `Date.now`.

## `vi.mock()`: substituir um módulo inteiro

Quando a dependência é um **módulo importado** (um cliente de API, uma lib), `vi.mock('./caminho')` substitui o módulo todo:

```ts
import { buscarCep } from './cep';      // o módulo real
import { criarEndereco } from './endereco';

vi.mock('./cep');                       // substitui ./cep por mocks automáticos

test('monta endereço a partir do CEP', async () => {
  vi.mocked(buscarCep).mockResolvedValue({ cidade: 'Recife', uf: 'PE' });

  const end = await criarEndereco('50000-000');
  expect(end.cidade).toBe('Recife');
  expect(buscarCep).toHaveBeenCalledWith('50000-000');
});
```

`vi.mocked(fn)` é um helper de tipos: diz ao TypeScript que `buscarCep` agora é um mock, liberando `.mockResolvedValue`. Para mockar **parte** de um módulo (manter o resto real), use a factory com `importActual`:

```ts
vi.mock('./mat', async (importActual) => {
  const real = await importActual<typeof import('./mat')>();
  return { ...real, aleatorio: vi.fn(() => 0.5) }; // só aleatorio é mockado
});
```

> [!warning] Usar uma variável externa na factory do `vi.mock` (hoisting)
> **O que acontece:** você define `const fake = vi.fn()` e usa dentro de `vi.mock('./x', () => ({ f: fake }))` — e recebe `ReferenceError: Cannot access 'fake' before initialization`. **Por quê:** o Vitest **iça (hoists)** as chamadas `vi.mock` para o **topo do arquivo**, antes dos imports e das declarações. Na hora que a factory roda, `fake` ainda não existe. **Como evitar:** declare a variável dentro de **`vi.hoisted`**, que é içado junto: `const { fake } = vi.hoisted(() => ({ fake: vi.fn() }))`. Aí ela existe quando a factory do mock roda.

## A disciplina: resetar entre testes

Mocks acumulam estado — o histórico de chamadas e as implementações fingidas persistem entre testes se você não limpar. É a causa clássica de "o teste passa sozinho mas falha na suíte".

```ts
import { afterEach, vi } from 'vitest';
afterEach(() => vi.clearAllMocks());   // limpa histórico de chamadas entre testes
// ou, na config: test: { clearMocks: true }
```

| Método | Limpa histórico | Remove implementação | Restaura original (spyOn) |
|--------|:---------------:|:--------------------:|:-------------------------:|
| `clearAllMocks` | ✅ | ❌ | ❌ |
| `resetAllMocks` | ✅ | ✅ | ❌ |
| `restoreAllMocks` | ✅ | ✅ | ✅ |

> [!question]- Qual eu uso: clear, reset ou restore?
> Regra prática: **`clearMocks: true`** (ou `clearAllMocks` no `afterEach`) como default — zera o histórico de chamadas entre testes, evitando que um `toHaveBeenCalledTimes` conte chamadas de testes anteriores. Use **`restoreAllMocks`** quando usa `vi.spyOn`, para devolver o método original (senão o spy vaza para outros testes e para o objeto real). `resetAllMocks` (que também apaga as implementações fingidas) é mais raro — útil quando você quer recriar o comportamento do zero em cada teste. O default seguro na maioria dos projetos: `clearMocks: true` + `restoreMocks: true` na config, e você quase não pensa nisso.

**Mocking com Vitest em uma frase:** `vi.fn()` cria funções-mock que registram e fingem, `vi.spyOn` observa/substitui um método real, `vi.mock` troca um módulo inteiro (içado — use `vi.hoisted` para variáveis da factory), e a disciplina inegociável é resetar mocks entre testes (`clearMocks`/`restoreMocks`) para não vazar estado.

## Em entrevista

> "`vi` is Vitest's mocking namespace. `vi.fn()` creates a mock function that records calls and can fake returns with `mockReturnValue` or `mockResolvedValue`. `vi.spyOn` wraps a real method — observing it and optionally replacing it. And `vi.mock` replaces a whole module, but it's **hoisted** to the top of the file, so if the factory needs a variable I declare it in `vi.hoisted`. The discipline that prevents flaky tests is resetting mocks between tests — I set `clearMocks` and `restoreMocks` in the config so call history and spies don't leak across tests."

| PT | EN |
|----|----|
| Função-mock | Mock function |
| Espião | Spy |
| Içamento (hoisting) | Hoisting |
| Vazamento de estado | State leakage |
| Baseado em interação | Interaction-based |
| Resetar mocks | Reset mocks |

## O que vem a seguir

Mockar funções e módulos cobre a lógica. Mas testar **UI** pede uma abordagem própria — e ela começa por uma filosofia (testar como o usuário usa) e um conjunto de queries. É a Testing Library.

- [[03-Dominios/Tecnologia/Testes JS/07 - Testing Library - filosofia e queries|07 — Testing Library: filosofia e queries]] — queries user-centric.
- [[03-Dominios/Engenharia/Testes/06 - Testar comportamento, não implementação|Engenharia/Testes 06]] — estado vs. interação, a teoria por trás dos mocks.

## Fontes

- **Vitest** — [*Mocking (`vi.fn`, `vi.spyOn`, `vi.mock`)*](https://vitest.dev/guide/mocking.html) — o guia oficial de mocking.
- **Vitest** — [*Vi API (`vi.hoisted`, `vi.mocked`, `clearAllMocks`)*](https://vitest.dev/api/vi.html) — helpers e reset.
- **Engenharia/Testes** — [[03-Dominios/Engenharia/Testes/05 - Test doubles - dummy, stub, spy, mock, fake|Test doubles]] — a taxonomia conceitual que esta nota instrumenta.
