---
title: "Testes em JavaScript"
created: 2026-04-11
updated: 2026-04-11
type: concept
status: evergreen
tags:
  - javascript
  - testes
  - entrevista
publish: false
---

# Testes em JavaScript

Deep dive em estratégias, ferramentas e patterns de teste na stack JavaScript/TypeScript moderna (2026). Para fundamentos gerais de testes, ver [[Testes]]. Para Java testing, ver [[Testes em Java]]. Para React specifically, ver [[React]].

## O que é

Testar em JavaScript em 2026 é radicalmente diferente de 2020. **Vitest** está comendo o market share do Jest, **Testing Library** substituiu Enzyme, **Playwright** dominou E2E, e **MSW** resolveu o problema de mockar HTTP. Para um senior, o stack moderno é:

```
┌─────────────────────────────────────────┐
│           Stack de testes JS            │
├─────────────────────────────────────────┤
│ Vitest / Jest          — unit + integ   │
│ Testing Library        — component      │
│ MSW (Mock Service Worker) — HTTP mocks  │
│ Playwright / Cypress   — E2E            │
│ Storybook              — component dev  │
│ Chromatic / Percy      — visual         │
└─────────────────────────────────────────┘
```

Em entrevistas, o que diferencia um senior em testes JS:

1. **Saber escolher a ferramenta** — Vitest vs Jest, Playwright vs Cypress
2. **Testing Library philosophy** — "test what users see, not implementation"
3. **MSW** — mockar HTTP no nível de rede, não do fetch
4. **Cobertura não é meta** — entender métricas e suas armadilhas
5. **Test pyramid** — muitas unit, menos integration, poucas E2E
6. **Fake timers, clock, fetch** — controle total de side effects
7. **Strategy para components** — user-event, fire-event, renderHook
8. **E2E patterns** — page object model, fixtures, parallelization
9. **Flakiness** — como detectar e evitar

---

## Vitest vs Jest

Em 2026, **Vitest é o default para novos projetos**. Jest ainda domina projetos legacy (especialmente CRA/Next.js), mas Vitest está ganhando rápido.

### Comparação

| Aspecto | Jest | Vitest |
| --- | --- | --- |
| **Ano** | 2014 (Facebook) | 2021 (Vitest team) |
| **Performance** | Médio | **3-10x mais rápido** |
| **ESM** | Suporte parcial, doloroso | **Nativo** |
| **TypeScript** | ts-jest (lento) ou SWC | **Nativo via Vite** |
| **API** | `describe`, `it`, `expect` | **Compatível com Jest** |
| **Watch mode** | Bom | **Excelente** (HMR) |
| **UI dashboard** | ❌ | **✅ built-in** |
| **Configuração** | Verbosa | **Herda do Vite** |
| **Mocking** | `jest.mock()` | `vi.mock()` (compatível) |
| **Snapshots** | ✅ | ✅ |
| **Coverage** | ✅ (v8 ou babel) | ✅ (v8 native) |

**Regra prática em 2026:**

- **Projeto novo** → Vitest
- **Projeto Vite/Next.js 14+** → Vitest
- **Projeto Jest existente funcionando bem** → fique no Jest até ter razão para migrar

### Vitest — setup básico

```bash
npm install -D vitest @vitest/ui
```

```javascript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
    test: {
        globals: true,           // usa describe/it/expect sem import
        environment: 'jsdom',    // ou 'node', 'happy-dom'
        setupFiles: ['./tests/setup.ts'],
        coverage: {
            provider: 'v8',
            reporter: ['text', 'html', 'lcov'],
            exclude: ['**/node_modules/**', '**/dist/**', '**/*.config.*']
        }
    }
});
```

```json
// package.json
{
    "scripts": {
        "test": "vitest",
        "test:ui": "vitest --ui",
        "test:coverage": "vitest run --coverage",
        "test:ci": "vitest run"
    }
}
```

---

## Vitest — API essencial

### Anatomia de um teste

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('PatientService', () => {

    let service: PatientService;

    beforeEach(() => {
        service = new PatientService();
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    describe('create', () => {
        it('should create a patient with valid data', () => {
            // Arrange
            const input = { name: 'Maria', email: 'maria@test.com' };

            // Act
            const patient = service.create(input);

            // Assert
            expect(patient.id).toBeDefined();
            expect(patient.name).toBe('Maria');
        });

        it('should throw when email is invalid', () => {
            expect(() => service.create({ name: 'X', email: 'invalid' }))
                .toThrow('Invalid email');
        });
    });
});
```

**AAA Pattern** (Arrange-Act-Assert) é universal. Torna testes legíveis em segundos.

**Nomes descritivos:**

```typescript
// RUIM
it('works', () => { ... });

// BOM
it('should return 404 when patient not found', () => { ... });
it('should send welcome email on successful registration', () => { ... });
```

### Assertions comuns

```typescript
// Equality
expect(value).toBe(5);                    // Object.is
expect(obj).toEqual({ name: 'Maria' });   // deep equality
expect(obj).toStrictEqual(other);          // deep + type check

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();
expect(value).toBeNaN();

// Numbers
expect(n).toBeGreaterThan(5);
expect(n).toBeGreaterThanOrEqual(5);
expect(n).toBeLessThan(10);
expect(n).toBeCloseTo(0.3, 5);            // float tolerance

// Strings
expect(str).toMatch(/regex/);
expect(str).toContain('substring');
expect(str).toHaveLength(10);

// Arrays
expect(arr).toContain(item);
expect(arr).toContainEqual({ id: 1 });    // deep
expect(arr).toHaveLength(3);

// Objects
expect(obj).toHaveProperty('nested.field');
expect(obj).toHaveProperty('name', 'Maria');
expect(obj).toMatchObject({ name: 'Maria' });  // partial

// Exceptions
expect(() => fail()).toThrow();
expect(() => fail()).toThrow('specific message');
expect(() => fail()).toThrow(CustomError);
await expect(asyncFail()).rejects.toThrow();

// Async
await expect(fetchUser(1)).resolves.toEqual(user);
await expect(fetchUser(999)).rejects.toThrow('not found');
```

### Parametrização — test.each

```typescript
describe('classify age', () => {
    it.each([
        [17, 'minor'],
        [18, 'adult'],
        [65, 'senior'],
        [0,  'baby']
    ])('classify(%i) should return %s', (age, expected) => {
        expect(classify(age)).toBe(expected);
    });
});
```

Com objetos para clareza:

```typescript
it.each([
    { input: 'hello', expected: 'HELLO' },
    { input: 'Foo',   expected: 'FOO' },
    { input: '',      expected: '' }
])('uppercase($input) → $expected', ({ input, expected }) => {
    expect(uppercase(input)).toBe(expected);
});
```

### Hooks

```typescript
beforeAll(() => { /* uma vez no início */ });
afterAll(() => { /* uma vez no fim */ });
beforeEach(() => { /* antes de cada teste */ });
afterEach(() => { /* depois de cada teste */ });
```

**Regra:** `beforeEach` é mais previsível que `beforeAll` porque cada teste começa em estado limpo. Use `beforeAll` apenas para setups caros e compartilháveis.

### Skip, only, todo

```typescript
it.skip('pending feature', () => { });     // pula
it.only('focus', () => { });                 // só este no file
it.todo('later');                            // planejado
describe.skip('pending suite', () => { });
```

**Cuidado:** `it.only` em commit bloqueia CI se não for detectado. Use ESLint `no-only-tests`.

### Concurrent

```typescript
describe.concurrent('group', () => {
    it.concurrent('test 1', async () => { ... });
    it.concurrent('test 2', async () => { ... });
    it.concurrent('test 3', async () => { ... });
});
// Rodam em paralelo (cuidado com shared state)
```

---

## Mocks em Vitest (vi)

### vi.fn() — criar mock

```typescript
const fn = vi.fn();
fn('a');
fn('b', 2);

expect(fn).toHaveBeenCalled();
expect(fn).toHaveBeenCalledTimes(2);
expect(fn).toHaveBeenCalledWith('a');
expect(fn).toHaveBeenLastCalledWith('b', 2);
expect(fn).toHaveBeenNthCalledWith(1, 'a');

// Configurar retorno
fn.mockReturnValue(42);
fn.mockReturnValueOnce(1).mockReturnValueOnce(2);
fn.mockResolvedValue('async');
fn.mockRejectedValue(new Error('fail'));
fn.mockImplementation((x) => x * 2);
```

### vi.spyOn — espiar método existente

```typescript
const spy = vi.spyOn(console, 'log').mockImplementation(() => {});
service.log('hello');
expect(spy).toHaveBeenCalledWith('hello');
spy.mockRestore();  // volta ao normal
```

### vi.mock — mockar módulo inteiro

```typescript
// test file
import { sendEmail } from './email';
import { createUser } from './user-service';

vi.mock('./email', () => ({
    sendEmail: vi.fn().mockResolvedValue({ sent: true })
}));

describe('createUser', () => {
    it('should send welcome email', async () => {
        await createUser({ name: 'Maria', email: 'maria@test.com' });
        expect(sendEmail).toHaveBeenCalledWith(
            'maria@test.com',
            expect.stringContaining('welcome')
        );
    });
});
```

### Parcial mock — keep original + override

```typescript
vi.mock('./utils', async (importOriginal) => {
    const actual = await importOriginal<typeof import('./utils')>();
    return {
        ...actual,
        getCurrentTime: vi.fn().mockReturnValue(new Date('2026-04-11'))
    };
});
```

### Auto mock

```typescript
vi.mock('./api');  // todas as exports viram mocks vazios

// Use __mocks__/api.ts para comportamento default
```

### Clear vs reset vs restore

```typescript
vi.clearAllMocks();   // limpa call history, mantém implementações
vi.resetAllMocks();   // limpa history + implementações (volta a retornar undefined)
vi.restoreAllMocks(); // restaura implementações originais (usado com spyOn)
```

**Regra:** `afterEach(() => vi.restoreAllMocks())` é um default seguro.

### Mock de timer

```typescript
it('should wait before sending', async () => {
    vi.useFakeTimers();

    const cb = vi.fn();
    setTimeout(cb, 1000);

    expect(cb).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1000);  // "avança" o tempo
    expect(cb).toHaveBeenCalled();

    vi.useRealTimers();
});
```

**Operações comuns:**

```typescript
vi.advanceTimersByTime(ms);              // avança N ms
vi.runAllTimers();                        // executa todos os timers pendentes
vi.runOnlyPendingTimers();                // só os pendentes atuais
vi.setSystemTime(new Date('2026-04-11')); // fixa data/hora
```

### Mock de fetch

```typescript
// Manual — apenas para casos simples
global.fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ id: 1, name: 'Maria' })
});

// PREFERIDO — MSW (abaixo)
```

---

## MSW (Mock Service Worker)

**A maneira certa de mockar HTTP em JavaScript moderno.** MSW intercepta requests no nível da rede (Service Worker no browser, interceptador no Node), sem mockar `fetch` ou `axios`.

### Por que MSW

**Antes:**

```typescript
// Ruim — mockando a biblioteca
vi.mock('axios', () => ({
    default: { get: vi.fn().mockResolvedValue({ data: {...} }) }
}));
```

**Problemas:**

- Se trocar de `axios` para `fetch`, os testes quebram
- Mock é diferente do comportamento real (headers, serialization)
- Impossível simular erros de rede reais

**Com MSW:**

```typescript
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
    http.get('/api/users/:id', ({ params }) => {
        return HttpResponse.json({ id: params.id, name: 'Maria' });
    }),

    http.post('/api/users', async ({ request }) => {
        const body = await request.json();
        return HttpResponse.json({ id: 42, ...body }, { status: 201 });
    })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Seu código chama fetch normalmente, MSW intercepta
it('should fetch user', async () => {
    const res = await fetch('/api/users/1');
    const user = await res.json();
    expect(user.name).toBe('Maria');
});
```

### Handlers dinâmicos

```typescript
it('should handle 500 error', async () => {
    server.use(
        http.get('/api/users/:id', () => {
            return new HttpResponse(null, { status: 500 });
        })
    );

    const res = await fetch('/api/users/1');
    expect(res.status).toBe(500);
});
```

### MSW também funciona em dev

```typescript
// mocks/browser.ts
import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

export const worker = setupWorker(...handlers);

// src/main.tsx
if (process.env.NODE_ENV === 'development') {
    const { worker } = await import('./mocks/browser');
    await worker.start();
}
```

Permite desenvolver frontend sem backend rodando. **Um dos maiores ganhos de produtividade dos últimos anos.**

---

## Testing Library — testes de componentes

**A filosofia:** "test what users see, not implementation details".

Em vez de testar "state", "props" ou métodos internos, Testing Library encoraja testar:

1. **Comportamento visível** — o que aparece na tela
2. **Interação do usuário** — clicks, typing, form submit
3. **Acessibilidade** — encontra elementos por role, label, text

### Instalação

```bash
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

```typescript
// tests/setup.ts
import '@testing-library/jest-dom/vitest';  // adiciona toBeInTheDocument, etc.
```

### Teste básico de componente React

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {

    it('should render email and password fields', () => {
        render(<LoginForm onSubmit={() => {}} />);

        expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /log in/i })).toBeInTheDocument();
    });

    it('should call onSubmit with form data', async () => {
        const user = userEvent.setup();
        const onSubmit = vi.fn();

        render(<LoginForm onSubmit={onSubmit} />);

        await user.type(screen.getByLabelText(/email/i), 'maria@test.com');
        await user.type(screen.getByLabelText(/password/i), 'secret');
        await user.click(screen.getByRole('button', { name: /log in/i }));

        expect(onSubmit).toHaveBeenCalledWith({
            email: 'maria@test.com',
            password: 'secret'
        });
    });

    it('should show error when password is too short', async () => {
        const user = userEvent.setup();
        render(<LoginForm onSubmit={() => {}} />);

        await user.type(screen.getByLabelText(/password/i), '12');
        await user.tab();  // blur

        expect(await screen.findByText(/at least 6 characters/i)).toBeInTheDocument();
    });
});
```

### Queries — como encontrar elementos

**Prioridade (Testing Library recomenda nesta ordem):**

1. **`getByRole`** — acessível por leitores de tela. **Sua primeira escolha.**

    ```typescript
    screen.getByRole('button', { name: /submit/i })
    screen.getByRole('heading', { level: 1 })
    screen.getByRole('textbox', { name: /email/i })
    ```

2. **`getByLabelText`** — form fields

    ```typescript
    screen.getByLabelText(/password/i)
    ```

3. **`getByPlaceholderText`** — quando não há label (evite, prefira label)

4. **`getByText`** — texto visível

    ```typescript
    screen.getByText(/welcome/i)
    screen.getByText('Exact text')
    ```

5. **`getByDisplayValue`** — valor atual de form field

6. **`getByAltText`** — imagens

    ```typescript
    screen.getByAltText(/logo/i)
    ```

7. **`getByTitle`** — `title` attribute

8. **`getByTestId`** — `data-testid`. **Último recurso.**

### Variantes

| Método | Retorna | Throws se não achar |
| --- | --- | --- |
| `getBy...` | Element | Sim |
| `queryBy...` | Element ou null | Não |
| `findBy...` | Promise<Element> | Sim (após timeout) |
| `getAllBy...` | Element[] | Sim (se vazio) |
| `queryAllBy...` | Element[] | Não |
| `findAllBy...` | Promise<Element[]> | Sim |

**Quando usar cada:**

- **`getBy`** — elemento que deve existir agora (teste falha se não existir)
- **`queryBy`** — para verificar que **não existe** (`expect(queryByText(...)).toBeNull()`)
- **`findBy`** — elemento que aparece assincronamente (espera até encontrar ou timeout)

### user-event vs fireEvent

**`userEvent`** simula interações reais: focus, typing, tab order, modifiers. **Preferido.**

```typescript
import userEvent from '@testing-library/user-event';

const user = userEvent.setup();
await user.click(button);
await user.type(input, 'hello');
await user.keyboard('{Enter}');
await user.tab();
await user.hover(element);
await user.selectOptions(select, 'option1');
await user.upload(fileInput, new File(['content'], 'file.txt'));
```

**`fireEvent`** dispara eventos DOM sintéticos diretamente. Mais baixo nível.

```typescript
import { fireEvent } from '@testing-library/react';

fireEvent.click(button);
fireEvent.change(input, { target: { value: 'hello' } });
```

**Regra:** use `userEvent` sempre. `fireEvent` só em casos específicos (ex.: disparar eventos customizados).

### Assertions com jest-dom

```typescript
expect(element).toBeInTheDocument();
expect(element).not.toBeInTheDocument();
expect(element).toBeVisible();
expect(element).toBeDisabled();
expect(element).toBeEnabled();
expect(element).toBeChecked();
expect(element).toHaveFocus();
expect(element).toHaveTextContent('text');
expect(element).toHaveValue('value');
expect(element).toHaveAttribute('href', '/home');
expect(element).toHaveClass('active');
expect(element).toHaveStyle({ color: 'red' });
expect(form).toHaveFormValues({ email: 'test@test.com', remember: true });
```

### Hooks — renderHook

```typescript
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

it('should increment', () => {
    const { result } = renderHook(() => useCounter());

    expect(result.current.count).toBe(0);

    act(() => {
        result.current.increment();
    });

    expect(result.current.count).toBe(1);
});
```

---

## Anti-patterns em Testing Library

### Não teste implementation details

```typescript
// RUIM — testa state interno
expect(wrapper.state('count')).toBe(1);

// RUIM — testa método interno
wrapper.instance().increment();

// BOM — testa comportamento visível
expect(screen.getByText('Count: 1')).toBeInTheDocument();
await user.click(screen.getByRole('button', { name: /increment/i }));
```

### Evite querySelector e getElementById

```typescript
// RUIM
const btn = container.querySelector('.submit-btn');

// BOM — baseado em acessibilidade
const btn = screen.getByRole('button', { name: /submit/i });
```

### Evite snapshots grandes

```typescript
// RUIM — snapshot enorme, ninguém revisa
expect(container).toMatchSnapshot();

// MELHOR — snapshots pequenos ou asserts específicos
expect(screen.getByTestId('user-card')).toMatchSnapshot();
```

### Não use act() manualmente

```typescript
// RUIM — act() manual
act(() => {
    fireEvent.click(btn);
});

// BOM — userEvent já envolve em act
await user.click(btn);
```

---

## E2E Testing — Playwright

**Playwright** (Microsoft) é o líder atual de E2E testing em 2026. Substituiu amplamente Cypress em projetos novos.

### Por que Playwright

| Aspecto | Playwright | Cypress |
| --- | --- | --- |
| **Browsers** | Chromium, Firefox, WebKit | Chromium (+ Firefox experimental) |
| **Linguagens** | JS, TS, Python, .NET, Java | JS, TS |
| **Multi-tab / iframe** | ✅ | ⚠️ limitado |
| **Paralelização** | ✅ nativa | ✅ paga ou custom |
| **API** | async/await | chainable |
| **Auto-wait** | ✅ excelente | ✅ |
| **Trace viewer** | ✅ excelente | ✅ |
| **Component testing** | ✅ experimental | ✅ |
| **Performance** | Muito rápido | Bom |

### Setup Playwright

```bash
npm init playwright@latest
```

### Teste básico

```typescript
import { test, expect } from '@playwright/test';

test('login flow', async ({ page }) => {
    // Navegar
    await page.goto('/login');

    // Interagir
    await page.getByLabel('Email').fill('maria@test.com');
    await page.getByLabel('Password').fill('secret123');
    await page.getByRole('button', { name: 'Log in' }).click();

    // Assert
    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText(/welcome, Maria/i)).toBeVisible();
});

test('should show error on invalid credentials', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Email').fill('wrong@test.com');
    await page.getByLabel('Password').fill('wrong');
    await page.getByRole('button', { name: 'Log in' }).click();

    await expect(page.getByRole('alert')).toContainText(/invalid credentials/i);
});
```

### Locators

Playwright usa **locators** que se parecem com Testing Library queries:

```typescript
page.getByRole('button', { name: /submit/i })
page.getByLabel('Email')
page.getByText('Welcome')
page.getByPlaceholder('Search...')
page.getByAltText('Logo')
page.getByTitle('Close')
page.getByTestId('user-card')

// CSS (último recurso)
page.locator('.my-class')
page.locator('#my-id')

// Filtering
page.getByRole('listitem').filter({ hasText: 'Maria' })
page.getByRole('listitem').first()
page.getByRole('listitem').nth(2)
```

### Auto-wait

Playwright **espera automaticamente** por condições antes de agir. Não precisa `wait` manual na maioria dos casos.

```typescript
// Espera botão estar visible, enabled e no viewport antes de clicar
await page.getByRole('button').click();

// Se precisar esperar explicitamente
await page.waitForURL('/dashboard');
await page.waitForLoadState('networkidle');
await expect(page.getByText('Loaded')).toBeVisible();  // retry até visible
```

### Page Object Model

Organize testes com POM para evitar duplicação:

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
    readonly page: Page;
    readonly emailInput: Locator;
    readonly passwordInput: Locator;
    readonly submitButton: Locator;
    readonly errorMessage: Locator;

    constructor(page: Page) {
        this.page = page;
        this.emailInput = page.getByLabel('Email');
        this.passwordInput = page.getByLabel('Password');
        this.submitButton = page.getByRole('button', { name: 'Log in' });
        this.errorMessage = page.getByRole('alert');
    }

    async goto() {
        await this.page.goto('/login');
    }

    async login(email: string, password: string) {
        await this.emailInput.fill(email);
        await this.passwordInput.fill(password);
        await this.submitButton.click();
    }
}

// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test('login', async ({ page }) => {
    const login = new LoginPage(page);
    await login.goto();
    await login.login('maria@test.com', 'secret');
    await expect(page).toHaveURL('/dashboard');
});
```

### Fixtures customizadas

```typescript
// tests/fixtures.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

type MyFixtures = {
    loginPage: LoginPage;
    authenticatedPage: Page;
};

export const test = base.extend<MyFixtures>({
    loginPage: async ({ page }, use) => {
        await use(new LoginPage(page));
    },

    authenticatedPage: async ({ page }, use) => {
        // Setup: login
        await page.goto('/login');
        await page.getByLabel('Email').fill('test@test.com');
        await page.getByLabel('Password').fill('test');
        await page.getByRole('button', { name: 'Log in' }).click();
        await page.waitForURL('/dashboard');

        await use(page);
        // Teardown (opcional)
    }
});

export { expect } from '@playwright/test';
```

```typescript
// Uso
import { test, expect } from './fixtures';

test('should see profile', async ({ authenticatedPage: page }) => {
    await page.goto('/profile');
    await expect(page.getByRole('heading', { name: /profile/i })).toBeVisible();
});
```

### Parallelization

```typescript
// playwright.config.ts
export default defineConfig({
    workers: process.env.CI ? 4 : undefined,  // paralelização
    fullyParallel: true,
    projects: [
        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
        { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },
        { name: 'webkit',   use: { ...devices['Desktop Safari'] } },
        { name: 'mobile',   use: { ...devices['iPhone 14'] } }
    ]
});
```

### Trace viewer

Playwright gera **traces** com screenshots, snapshots DOM e network, navegáveis passo a passo:

```bash
npx playwright test --trace on
npx playwright show-trace trace.zip
```

**Debugging E2E nunca foi tão fácil.** Você vê exatamente o que o teste fez, cada frame, cada network call.

### Component testing (experimental)

Playwright pode testar componentes React/Vue/Svelte em isolamento:

```typescript
import { test, expect } from '@playwright/experimental-ct-react';
import { Button } from './Button';

test('Button click', async ({ mount }) => {
    let clicked = false;
    const component = await mount(
        <Button onClick={() => { clicked = true; }}>Click me</Button>
    );
    await component.click();
    expect(clicked).toBe(true);
});
```

---

## Cypress — alternativa

Ainda popular, especialmente em projetos existentes. API chainable:

```javascript
describe('login', () => {
    it('should login with valid credentials', () => {
        cy.visit('/login');
        cy.get('input[name="email"]').type('maria@test.com');
        cy.get('input[name="password"]').type('secret{enter}');
        cy.url().should('include', '/dashboard');
        cy.contains(/welcome/i).should('be.visible');
    });
});
```

**Em 2026, Playwright é a escolha mais comum em projetos novos.** Cypress ainda tem ecossistema grande mas tem perdido mindshare.

---

## Storybook — desenvolvimento de componentes

Storybook não é tecnicamente "testes", mas é parte essencial do workflow de UI moderno.

```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
    title: 'UI/Button',
    component: Button,
    args: {
        onClick: () => {}
    }
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
    args: {
        variant: 'primary',
        children: 'Click me'
    }
};

export const Disabled: Story = {
    args: {
        variant: 'primary',
        disabled: true,
        children: 'Disabled'
    }
};
```

**Storybook + interaction tests:**

```typescript
export const LoggedInSuccessfully: Story = {
    args: { onSubmit: () => {} },
    play: async ({ canvasElement }) => {
        const canvas = within(canvasElement);
        await userEvent.type(canvas.getByLabelText('Email'), 'maria@test.com');
        await userEvent.type(canvas.getByLabelText('Password'), 'secret');
        await userEvent.click(canvas.getByRole('button', { name: /log in/i }));
        await expect(canvas.getByText(/welcome/i)).toBeInTheDocument();
    }
};
```

Stories viram testes automaticamente via `test-storybook`.

**Chromatic** ou **Percy** fazem testes visuais — screenshots comparados entre commits, diffs visíveis.

---

## Estratégia de testes para projeto moderno

### Pirâmide adaptada para frontend

```
         ┌────────────┐
         │   E2E      │     Playwright
         │  (poucos)  │     5-10 fluxos críticos
         └────────────┘
       ┌────────────────┐
       │  Integration   │    Vitest + Testing Library + MSW
       │   (muitos)     │    componentes completos com rede mockada
       └────────────────┘
     ┌─────────────────────┐
     │   Component         │   Vitest + Testing Library
     │   (muitos)          │   componentes isolados
     └─────────────────────┘
   ┌──────────────────────────┐
   │  Unit (muitos)            │  Vitest
   │  functions puras, hooks   │
   └──────────────────────────┘
```

### Distribuição recomendada

- **60-70% unit tests** — funções puras, hooks, utilities, reducers
- **20-30% component tests** — Testing Library + MSW
- **5-10% E2E** — fluxos críticos de negócio

### Tempo de execução

- **Unit:** < 1s por teste, suite total < 30s
- **Component:** 100-500ms, suite < 2min
- **E2E:** 5-30s por teste, suite < 10min
- **CI total:** < 15min idealmente

### O que testar em cada nível

**Unit:**

- Utilities puras (formatação, validação, cálculo)
- Hooks customizados (useCounter, useDebounce)
- Redux/Zustand reducers e actions
- Funções de negócio

**Component:**

- Componente renderiza com props
- Interação do usuário muda estado visível
- Loading, error, empty states
- Formulários (validação, submit)

**Integration (dentro do Vitest):**

- Múltiplos componentes trabalhando juntos
- Com router, context, estado global
- Com rede mockada via MSW

**E2E:**

- Login/logout
- Fluxo crítico de conversão (checkout, registration)
- Integrações complexas (upload de arquivo, real-time)
- Smoke tests de deploy

---

## Cobertura de código — o que importa

```bash
vitest run --coverage
```

### Métricas

- **Lines** — quantas linhas foram executadas
- **Statements** — declarações executadas
- **Functions** — funções chamadas
- **Branches** — ramos de `if/else`, ternários

### Metas típicas

- **80% overall** — razoável, não é meta de qualidade
- **90%+ para lógica de negócio crítica**
- **100% é frequentemente waste** — código trivial ou ramos impossíveis

### Armadilhas

- **100% coverage não garante qualidade.** Testes sem asserts contam para coverage.
- **Coverage de tipos não existe em JS puro** — use TypeScript.
- **Coverage como meta** → devs escrevem testes ruins para bater número.
- **Branch coverage é mais importante que line coverage** — pega ramos não testados.
- **Use mutation testing** (Stryker) para avaliar **qualidade** dos testes.

### Stryker — mutation testing

```bash
npm install -D @stryker-mutator/core @stryker-mutator/vitest-runner
npx stryker init
npx stryker run
```

Altera bytecode/código (mutações) e verifica se testes pegam. Métrica real de qualidade, não só coverage.

---

## Flakiness — detectar e evitar

**Flaky test** = teste que às vezes passa, às vezes falha, sem mudança no código. Dívida técnica cara.

### Causas comuns

- **Timing** — race conditions, `setTimeout` vs `waitFor`
- **Shared state** — testes interferindo entre si
- **Ordem** — teste só passa se rodado numa ordem específica
- **Depêndencias externas** — rede, filesystem, relógio real
- **Async mal tratado** — `await` esquecido
- **CSS transitions** — E2E clica em elemento que ainda está animando

### Prevenção

1. **Isolamento total** — nada compartilhado entre testes
2. **Fake timers** em vez de sleep real
3. **MSW** em vez de rede real
4. **`findBy*`** em vez de `getBy*` + setTimeout
5. **Não confie em ordem** — `beforeEach`, não `beforeAll` com state
6. **Retry em E2E** — Playwright tem retry built-in

### Retry strategy

```typescript
// Vitest
// vitest.config.ts
export default defineConfig({
    test: {
        retry: 1  // retry 1x em falha (máscara flakiness, use com cuidado)
    }
});

// Playwright
// playwright.config.ts
export default defineConfig({
    retries: process.env.CI ? 2 : 0
});
```

**Atenção:** retries mascaram flakiness. Use como safety net, não como solução.

### Detectar flakes

- **Run all tests 10x** em CI periódico
- **Stryker** — testes flaky falham nos "mutation runs"
- **Playwright trace** — inspeciona quando falha

---

## Armadilhas comuns

- **`it.only` commitado** — bloqueia CI. Use ESLint `no-only-tests`.
- **Coverage como meta em vez de ferramenta** — devs gaming o número
- **Mockar demais** — se metade do teste é mock, o design tem problemas
- **Testar implementação** — wrapper.state(), wrapper.instance()
- **querySelector em Testing Library** — prefira role/label/text
- **`getByText` com texto dinâmico** — regex mais seguro
- **async/await esquecido** — teste passa silenciosamente
- **`expect(1).toBe(1)`** — teste placeholder esquecido
- **Testes dependentes** — teste 2 só passa se teste 1 rodou
- **Mock global não limpo** — `vi.restoreAllMocks()` em afterEach
- **Real timers em testes de debounce** — use fake timers
- **Sleep real em E2E** — use waitFor/auto-wait
- **H2 em vez de Testcontainers** (backend) — ver [[Testes em Java]]
- **Testar bibliotecas de terceiros** — confie que React funciona
- **Não testar error paths** — só happy path
- **Snapshots enormes** — ninguém revisa
- **E2E para tudo** — pirâmide invertida, lento e frágil
- **Ignorar flakes** — "roda de novo que passa" é dívida
- **Shared context no beforeAll** — vaza state entre testes
- **`toHaveBeenCalled()` sem `toHaveBeenCalledWith`** — não valida argumentos

---

## Na prática (da minha experiência)

> **Stack de testes no MedEspecialista:**
>
> **1. Vitest + React Testing Library + MSW:**
> Stack default para frontend. Vitest roda em ~3s para ~800 testes, Jest demorava 20s. Watch mode instantâneo graças ao HMR do Vite. MSW mocka toda a API, testes não dependem de backend rodando.
>
> **2. Playwright para E2E:**
> Migrei do Cypress há um ano. Multi-browser (Chromium, Firefox, WebKit), paralelização nativa, trace viewer incrível. Debugging de falhas ficou 10x mais fácil.
>
> **3. MSW também em dev:**
> Frontend consegue rodar standalone com MSW servindo dados fake. Um desenvolvedor do frontend não precisa ter o backend Spring Boot rodando. Onboarding de novos devs ficou trivial.
>
> **4. Fixtures compartilhadas via factories:**
>
> ```typescript
> // tests/factories.ts
> export const makePatient = (overrides?: Partial<Patient>): Patient => ({
>     id: faker.number.int(),
>     name: faker.person.fullName(),
>     email: faker.internet.email(),
>     birthDate: faker.date.past({ years: 60 }),
>     ...overrides
> });
> ```
>
> Cada teste cria os objetos que precisa, sem depender de fixtures compartilhadas.
>
> **5. `data-testid` só em último caso:**
> 95% dos queries usam role, label ou text. `data-testid` é fallback para casos onde não há semântica natural.
>
> **6. Visual regression via Chromatic:**
> Componentes em Storybook, snapshots visuais em cada PR. Pega regressões de CSS invisíveis em code review.
>
> **Incidente memorável — race condition em teste:**
>
> Teste que fazia fetch e depois assert era flaky. Às vezes passava, às vezes falhava. Causa: o componente fazia 2 fetches (dados + user info), teste usava `getByText` que é síncrono e falhava no primeiro render. Solução: `findByText` (async) ou `waitFor`. Lição: queries assíncronas (`findBy*`) são default seguro quando há network.
>
> **Outro — Playwright flaky em CI:**
>
> Teste passava local, falhava em CI com "element not clickable". Causa: modal com transição CSS de 300ms. Playwright tentava clicar antes da animação terminar. Solução: `await expect(modal).toBeVisible()` que espera estabilização, ou `toBeInViewport()`. Playwright tem auto-wait, mas CSS transitions às vezes confundem.
>
> **Mutation testing:**
>
> Rodei Stryker num módulo crítico de cálculo de preços. Coverage dizia 92%, Stryker mostrou 67% de mutações sobreviveram. Testes validavam "rodou" mas não "resultado correto". Melhorei asserções baseado no relatório. Coverage é uma âncora, não um destino.
>
> **A lição principal:** testes são investimento com retorno composto. Uma suite rápida e confiável é o que permite refactoring agressivo sem medo. Invista em velocidade (Vitest), em isolamento (MSW, fixtures), e em cultura ("nunca commite `it.only`", "flake é bug").

---

## How to explain in English

> "My JavaScript testing stack in 2026 is Vitest for unit and integration tests, React Testing Library for component tests, MSW for HTTP mocking, and Playwright for end-to-end. I migrated from Jest to Vitest over a year ago and the difference is dramatic — same API, but 3-10x faster, native ESM, and a proper UI dashboard.
>
> For component tests, I follow Testing Library's philosophy: test what users see, not implementation details. I use `getByRole` as my primary query because it aligns with accessibility, and I use `userEvent` to simulate real interactions like clicking, typing, and tabbing. I almost never use `data-testid` — that's a last resort.
>
> MSW is a game-changer. Instead of mocking `fetch` or `axios`, MSW intercepts at the network level. My tests don't care how the HTTP client works, and the same handlers can be used in development mode so the frontend can run without a backend. That alone is worth the setup cost.
>
> For E2E, I use Playwright. The auto-wait is reliable, the trace viewer makes debugging CI failures trivial, and parallelization across browsers is native. I organize tests with the Page Object Model and custom fixtures for authentication and common setups. I keep E2E tests minimal — only critical business flows, because they're slow and more prone to flakiness.
>
> My test distribution is roughly 70% unit, 25% component, 5% E2E. The pyramid, not the ice cream cone. I aim for sub-30-second unit suite and sub-10-minute CI total.
>
> I don't chase 100% coverage. I chase test quality. I run Stryker mutation testing occasionally on critical code — it reveals tests that execute code but don't actually verify behavior. Coverage is a floor, not a ceiling.
>
> Flakiness is dead debt. If a test is flaky, I fix it or delete it. Auto-retry in CI masks the problem. My rules: isolated tests, fake timers for anything timing-related, MSW for network, and `findBy*` for async-appearing elements."

### Frases úteis em entrevista

- "Vitest in 2026 — Jest is still valid for legacy, Vitest for new projects."
- "Testing Library philosophy: test what users see, not implementation."
- "MSW at the network level — not mocking fetch directly."
- "userEvent over fireEvent — simulates real user interaction."
- "`getByRole` first, `getByLabelText` second, `data-testid` last resort."
- "Playwright for E2E with trace viewer for debugging CI failures."
- "Page Object Model and custom fixtures keep E2E maintainable."
- "Fake timers for debounce, throttle, and any time-dependent logic."
- "Test pyramid — not the ice cream cone."
- "Mutation testing reveals test quality better than coverage."
- "Flaky tests are bugs. Auto-retry hides, doesn't fix."

### Key vocabulary

- teste unitário → unit test
- teste de componente → component test
- teste de integração → integration test
- teste de ponta a ponta → end-to-end test (E2E)
- regressão visual → visual regression
- simulação / mock → mock / stub / fake
- asserção → assertion
- correspondência → matcher
- consulta → query
- interceptor de rede → network interceptor
- temporizador falso → fake timer
- instantâneo → snapshot
- teste instável → flaky test
- cobertura → coverage
- teste de mutação → mutation testing
- pirâmide de testes → test pyramid
- interação do usuário → user interaction
- visualizador de rastros → trace viewer

---

## Recursos

### Documentação

- [Vitest](https://vitest.dev/)
- [Jest](https://jestjs.io/)
- [Testing Library](https://testing-library.com/docs/)
- [MSW](https://mswjs.io/)
- [Playwright](https://playwright.dev/)
- [Cypress](https://docs.cypress.io/)
- [Storybook](https://storybook.js.org/)

### Livros

- **Testing JavaScript** — Kent C. Dodds (curso + livro)
- **Test-Driven Development with Node.js** — Prince Abalogu
- **Unit Testing Principles, Practices, and Patterns** — Vladimir Khorikov (conceitos universais)

### Artigos

- [Kent C. Dodds Blog](https://kentcdodds.com/blog) — filosofia de Testing Library (ele escreveu)
- [Testing Trophy — Kent C. Dodds](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
- [Common mistakes with React Testing Library](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [Why MSW](https://mswjs.io/docs/philosophy)

### Vídeos

- Kent C. Dodds YouTube — Testing Library, Testing Trophy
- Playwright official YouTube — demos e tutoriais
- ["Testing Like the TSA" by Kent C. Dodds](https://kentcdodds.com/talks/#testing-like-the-tsa)

### Ferramentas

- [Stryker](https://stryker-mutator.io/) — mutation testing
- [Chromatic](https://www.chromatic.com/) — visual regression
- [Percy](https://percy.io/) — visual regression
- [BackstopJS](https://github.com/garris/BackstopJS) — visual regression
- [happy-dom](https://github.com/capricorn86/happy-dom) — alternativa ao jsdom, mais rápido
- [faker-js](https://fakerjs.dev/) — geração de dados de teste

---

## Veja também

- [[JavaScript Fundamentals]] — linguagem base
- [[TypeScript]] — tipagem em testes
- [[React]] — React-specific testing
- [[Node.js]] — backend testing
- [[Testes]] — fundamentos gerais
- [[Testes em Java]] — comparação com stack Java
- [[Full Stack Open - Guia de Revisão]] — partes 4, 5, 10 cobrem testes
- [[API Design]] — contract testing
