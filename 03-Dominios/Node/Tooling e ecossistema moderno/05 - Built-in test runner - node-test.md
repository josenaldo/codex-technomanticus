---
title: "Built-in test runner - node:test"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: seedling
progresso: andamento
publish: false
tags:
  - node
  - testing
  - node-test
  - tooling
  - javascript
aliases:
  - node:test
  - node test runner
---

# Built-in test runner - node:test

> [!abstract] TL;DR
> O `node:test` (Node 18 experimental, estável no Node 20+) oferece `test`, `describe`, `it`, hooks (`before`/`after`/`beforeEach`/`afterEach`) e mocking nativo (`t.mock.fn`, `t.mock.method`, `t.mock.timers`) sem dependências externas.
> É competitivo com Vitest para projetos simples, bibliotecas e CLIs. `node --test --watch` (Node 18.13+/19.2+) e `--test-reporter=spec` (Node 19.9+/20.3+) completam o setup básico.
> Para Testing Library, JSDOM, snapshot testing ou cobertura via istanbul, ainda use Vitest ou Jest.

## O que é

Antes do Node 18, qualquer projeto JavaScript que precisasse de testes dependia obrigatoriamente de ferramentas externas: Jest, Mocha, Jasmine, AVA ou similares. Cada uma trazia dezenas (ou centenas) de dependências transitivas, aumentando o `node_modules`, o tempo de instalação e a superfície de ataque de segurança.

O Node 18 introduziu o módulo `node:test` como experimental, fornecendo um corredor de testes integrado ao próprio runtime. A motivação principal foi dupla: reduzir a barreira de entrada para testes em projetos novos e permitir que utilitários e bibliotecas de infraestrutura escrevam testes sem forçar uma dependência de framework em quem as consome.

No Node 20, o módulo tornou-se estável e passou a ser a opção padrão para novos projetos que não precisam de recursos avançados. No ecossistema atual, o `node:test` ocupa uma posição intermediária: mais robusto que um script de testes manual, mais leve que o Jest, e levemente inferior ao Vitest em termos de ergonomia e ecossistema de plugins — mas com a vantagem de não adicionar nenhuma dependência.

## Como funciona

### Funções básicas: test, describe e it

A API central do `node:test` expõe três funções de declaração de testes:

- `test(name, fn)` — declara um teste individual com callback síncrono ou assíncrono.
- `it(name, fn)` — alias exato de `test`, existe por compatibilidade com a sintaxe BDD familiar de Mocha/Jest.
- `describe(name, fn)` — agrupa testes relacionados em uma suíte.

Cada função aceita modificadores para controlar a execução:

- `test.skip(name, fn)` ou `it.skip(...)` — pula o teste e registra como *skipped*.
- `test.todo(name)` — marca o teste como pendente (sem implementação).
- `test.only(name, fn)` — executa apenas os testes marcados com `only` na suíte.
- `t.skip('reason')` — pula o teste de dentro do callback (útil para skip condicional).

```js
import { test, describe, it } from 'node:test';
import assert from 'node:assert/strict';

describe('Calculadora', () => {
  it('soma dois números positivos', () => {
    assert.equal(2 + 3, 5);
  });

  it('subtrai corretamente', async () => {
    const resultado = await Promise.resolve(10 - 4);
    assert.equal(resultado, 6);
  });

  test.skip('multiplicação por zero (ainda não implementado)', () => {
    // será implementado na próxima sprint
  });

  test.todo('divisão por zero deve lançar erro');

  test('só eu rodo com --test-only', { only: true }, (t) => {
    // executado apenas quando node --test --test-only
    assert.ok(true);
  });
});
```

### Asserções com node:assert

O `node:test` não inclui uma biblioteca de asserções própria — em vez disso, usa o módulo nativo `node:assert` (ou `node:assert/strict` para o modo estrito por padrão).

As asserções mais relevantes para o dia a dia:

| Asserção | O que verifica |
|---|---|
| `assert.equal(a, b)` | `a == b` (coerção de tipo) |
| `assert.strictEqual(a, b)` | `a === b` (sem coerção) |
| `assert.deepEqual(a, b)` | igualdade profunda com coerção |
| `assert.deepStrictEqual(a, b)` | igualdade profunda sem coerção |
| `assert.ok(value)` | valor truthy |
| `assert.throws(fn, pattern)` | função lança erro correspondente ao padrão |
| `assert.rejects(asyncFn, pattern)` | promise rejeita com erro correspondente |
| `assert.match(str, regex)` | string corresponde à expressão regular |
| `assert.doesNotThrow(fn)` | função NÃO lança erro |

```js
import assert from 'node:assert/strict';

// Igualdade estrita
assert.strictEqual(1 + 1, 2);
assert.strictEqual('hello'.toUpperCase(), 'HELLO');

// Igualdade profunda em objetos e arrays
assert.deepStrictEqual({ a: 1, b: [2, 3] }, { a: 1, b: [2, 3] });

// Verificar lançamento de erro síncrono
assert.throws(
  () => JSON.parse('{ inválido }'),
  { name: 'SyntaxError' }
);

// Verificar rejeição de promise
await assert.rejects(
  async () => { throw new Error('falhou'); },
  { message: 'falhou' }
);

// Verificar que corresponde a regex
assert.match('node@20.0.0', /node@\d+\.\d+\.\d+/);

// Verificar que NÃO lança erro
assert.doesNotThrow(() => JSON.parse('{"ok": true}'));
```

### Hooks: before, after, beforeEach, afterEach

O `node:test` oferece quatro hooks de ciclo de vida para configuração e limpeza:

- `before(fn)` — executado **uma vez** antes de todos os testes da suíte.
- `after(fn)` — executado **uma vez** após todos os testes da suíte.
- `beforeEach(fn)` — executado **antes de cada** teste individual.
- `afterEach(fn)` — executado **após cada** teste individual.

Os hooks aceitam callbacks assíncronos e recebem o mesmo contexto `t` que os testes.

```js
import { describe, before, after, beforeEach, afterEach, it } from 'node:test';
import assert from 'node:assert/strict';

// Simulação de conexão com banco de dados
let db;

describe('Repositório de usuários', () => {
  before(async () => {
    // Conecta ao banco de testes uma vez para toda a suíte
    db = await criarConexaoTesteBD();
    await db.migrate();
  });

  after(async () => {
    // Fecha a conexão ao final de todos os testes
    await db.close();
  });

  beforeEach(async () => {
    // Limpa os dados antes de cada teste para isolamento
    await db.query('DELETE FROM usuarios');
    await db.query("INSERT INTO usuarios (id, nome) VALUES (1, 'Alice')");
  });

  afterEach(async () => {
    // Limpeza adicional após cada teste (logs, locks, etc.)
    await db.query('DELETE FROM logs_auditoria');
  });

  it('lista todos os usuários', async () => {
    const usuarios = await db.query('SELECT * FROM usuarios');
    assert.equal(usuarios.length, 1);
    assert.equal(usuarios[0].nome, 'Alice');
  });

  it('insere um novo usuário', async () => {
    await db.query("INSERT INTO usuarios (id, nome) VALUES (2, 'Bob')");
    const usuarios = await db.query('SELECT * FROM usuarios');
    assert.equal(usuarios.length, 2);
  });
});
```

### Mocking: t.mock.fn e t.mock.timers

O sistema de mocking do `node:test` está disponível através do objeto `t` (contexto de teste) e oferece espias de função, substituição de métodos em objetos e controle de temporizadores.

**`t.mock.fn(original?)`** — cria uma espiã de função. Rastreia chamadas, argumentos e valores de retorno. Opcionalmente recebe a implementação original ou substituta.

**`t.mock.method(objeto, 'nomeMetodo', implementacao?)`** — substitui um método em um objeto existente, rastreando suas chamadas.

**`t.mock.timers.enable({ apis: ['setTimeout', 'setInterval'] })`** — intercepta os temporizadores do Node, permitindo avançar o tempo manualmente. Disponível desde o Node 20.4.0.

**`t.mock.reset()`** — reseta os rastreadores de todas as mocks do contexto.

**`t.mock.restore()`** — restaura todos os métodos substituídos aos originais.

```js
import { test, describe } from 'node:test';
import assert from 'node:assert/strict';

describe('Mock de fetch', () => {
  test('usa t.mock.fn para substituir fetch', async (t) => {
    // Substitui o fetch global por uma espiã
    const fetchMock = t.mock.fn(async () => ({
      ok: true,
      json: async () => ({ id: 42, nome: 'Alice' }),
    }));
    globalThis.fetch = fetchMock;

    // Código que usa fetch internamente
    const usuario = await buscarUsuario(42);

    // Verifica o resultado e as chamadas
    assert.equal(usuario.nome, 'Alice');
    assert.equal(fetchMock.mock.calls.length, 1);
    assert.equal(fetchMock.mock.calls[0].arguments[0], '/api/usuarios/42');
  });
});

describe('Mock de setTimeout', () => {
  test('usa t.mock.timers para controlar tempo', (t) => {
    // Habilita controle manual dos temporizadores (Node 20.4.0+)
    t.mock.timers.enable({ apis: ['setTimeout'] });

    let executado = false;

    setTimeout(() => {
      executado = true;
    }, 5000);

    // O callback ainda não executou (tempo real: ~0ms)
    assert.equal(executado, false);

    // Avança 5 segundos manualmente
    t.mock.timers.tick(5000);

    // Agora o callback executou
    assert.equal(executado, true);
  });
});

describe('Mock de método em objeto', () => {
  test('substitui método com t.mock.method', (t) => {
    const logger = {
      log: (msg) => console.log(msg),
    };

    // Substitui logger.log por uma espiã sem implementação real
    const logMock = t.mock.method(logger, 'log');

    logger.log('teste 1');
    logger.log('teste 2');

    assert.equal(logMock.mock.calls.length, 2);
    assert.equal(logMock.mock.calls[0].arguments[0], 'teste 1');

    // Restaura o método original ao final
    t.mock.restore();
  });
});
```

### Executando testes

O `node:test` é invocado através do flag `--test` do runtime — sem instalar nenhuma ferramenta extra.

**Descoberta automática de arquivos** (Node 18+): o flag `--test` sem argumentos procura por:
- `**/*.test.mjs`, `**/*.test.cjs`, `**/*.test.js`
- `**/test.mjs`, `**/test.cjs`, `**/test.js`
- `**/test/**/*.mjs`, `**/test/**/*.cjs`, `**/test/**/*.js`

```bash
# Roda todos os arquivos de teste descobertos automaticamente
node --test

# Roda arquivo específico
node --test src/utils.test.js

# Modo watch: re-executa ao detectar mudanças (Node 18.13+/19.2+, estável no Node 22)
node --test --watch

# Saída legível por humanos (Node 19.9+/20.3+)
node --test --test-reporter=spec

# Saída TAP para CI/CD (padrão em Node 18 e quando redirecionado)
node --test --test-reporter=tap

# Executa apenas testes marcados com test.only
node --test --test-only

# Paralelismo de arquivos (Node 18.19+/20.10+/21+)
node --test --test-concurrency=4

# Cobertura de código nativa (Node 22+, experimental)
node --test --experimental-test-coverage
```

> [!tip] Em Node 18 LTS, o output padrão é TAP. O `--test-reporter=spec` está disponível a partir do Node 19.9+/20.3+.

No `package.json`, o padrão recomendado para projetos que usam `node:test`:

```json
{
  "scripts": {
    "test": "node --test --test-reporter=spec",
    "test:watch": "node --test --watch --test-reporter=spec",
    "test:ci": "node --test --test-reporter=tap",
    "test:coverage": "node --test --experimental-test-coverage"
  }
}
```

### Comparação com Vitest

| Recurso | `node:test` | Vitest |
|---|---|---|
| Zero dependências | Sim | Não (Vite, esbuild, etc.) |
| Integrado ao runtime | Sim | Não |
| `describe`, `test`, `it` | Sim | Sim |
| Hooks de ciclo de vida | Sim | Sim |
| Mocking nativo | Sim (`t.mock`) | Sim (`vi.fn`, `vi.mock`) |
| Snapshot testing | Não | Sim |
| JSDOM / browser mode | Não | Sim |
| Testing Library | Não | Sim |
| Cobertura via istanbul | Não (nativa limitada) | Sim (`@vitest/coverage-v8`) |
| Watch mode | Sim (Node 18.13+/19.2+) | Sim (nativo, mais maduro) |
| TypeScript sem config | Não (< Node 22); nativo com strip-types (Node 22+) | Sim (com Vite pipeline) |
| Velocidade de startup | Muito rápida | Rápida (mas com overhead Vite) |
| Reporters customizados | Sim | Sim (mais ecossistema) |

**Quando escolher `node:test`:**
- Bibliotecas e utilitários sem DOM que precisam de zero dependências de teste.
- Scripts de CLI, ferramentas de build, módulos de infraestrutura.
- Projetos onde velocidade de startup e leveza são críticas.
- Ambientes com restrições de instalação de dependências.

**Quando escolher Vitest:**
- Projetos com componentes React/Vue/Svelte (precisa de JSDOM + Testing Library).
- Precisar de snapshot testing.
- Time já familiarizado com a sintaxe Jest (Vitest é quase drop-in replacement).
- Cobertura de código detalhada e integrada ao pipeline Vite.

**Quando escolher Jest:**
- Projetos legados já configurados com Jest.
- Ecossistema de plugins específicos do Jest que não têm equivalente no Vitest.
- Times com forte familiaridade com mocks do Jest (`jest.fn`, `jest.mock`, `jest.spyOn`).

## Quando usar

Siga este fluxo de decisão para escolher o corredor de testes adequado:

```
Precisa testar código com DOM / browser APIs?
├── Sim → Vitest (com JSDOM) ou Jest
└── Não ↓

Precisa de snapshot testing?
├── Sim → Vitest ou Jest
└── Não ↓

O projeto é uma biblioteca / utilitário / ferramenta CLI?
├── Sim → node:test (zero dependências, startup rápido)
└── Não ↓

O time já usa Vite no projeto?
├── Sim → Vitest (integração natural)
└── Não ↓

O projeto já tem Jest configurado e funcionando?
├── Sim → Manter Jest (custo de migração não compensa)
└── Não → node:test (projetos novos sem DOM) ou Vitest (projetos com mais necessidades)
```

> [!tip] Regra prática
> Para um novo servidor Node.js (API REST, CLI, worker), comece com `node:test`. Se em algum momento precisar de snapshot testing, Testing Library ou JSDOM, migre para Vitest — a sintaxe é intencionalmente parecida, reduzindo o atrito.

## Armadilhas comuns

### Armadilha 1: Executar o arquivo diretamente em vez de usar --test

Executar `node arquivo.test.js` diretamente parece funcionar — o código roda sem erros — mas os resultados dos testes não são reportados corretamente ao terminal, e o processo pode sair com código 0 mesmo quando há falhas.

```js
// ❌ Problema: arquivo executado diretamente
// node src/calculadora.test.js
// Saída: (silêncio) — os testes não são reportados

import { test } from 'node:test';
import assert from 'node:assert/strict';

test('soma', () => {
  assert.equal(2 + 2, 5); // assert falha, mas o comportamento do exit code não é confiável (pode variar por versão)
});
```

```js
// ✅ Fix: sempre executar via node --test, nunca diretamente
// node --test src/calculadora.test.js
// Saída: TAP ou spec com status correto e exit code 1 em caso de falha
```

> [!warning]
> Sem `--test`, o módulo `node:test` registra os testes mas não inicia o runner. Em CI/CD, isso significa que falhas passam despercebidas e o pipeline fica verde incorretamente.

### Armadilha 2: Confundir assert.deepEqual com assert.deepStrictEqual

O `assert.deepEqual` usa coerção de tipo (`==`) em comparações primitivas aninhadas em objetos. Isso pode mascarar bugs sutis de tipo onde um campo retorna `"42"` (string) quando deveria retornar `42` (número).

```js
// ❌ Problema: deepEqual usa == e aceita coerção de tipo
import assert from 'node:assert'; // sem /strict

assert.deepEqual({ id: '42', ativo: 1 }, { id: 42, ativo: true });
// Passa! '42' == 42 e 1 == true — bug mascarado
```

```js
// ✅ Fix: usar assert/strict ou deepStrictEqual explicitamente
import assert from 'node:assert/strict';

assert.deepStrictEqual({ id: 42, ativo: true }, { id: 42, ativo: true });
// Correto: '42' !== 42 causa falha imediata se os tipos não baterem
```

> [!tip]
> Prefira sempre `import assert from 'node:assert/strict'`. Isso torna todas as asserções do módulo estritas por padrão, evitando a armadilha sem precisar lembrar de usar `deepStrictEqual` explicitamente.

### Armadilha 3: Mocks não restaurados entre testes causam poluição de estado

Quando um teste substitui um método global (como `fetch`, `console.log` ou um método de objeto compartilhado) sem restaurar ao final, os testes seguintes herdam a versão mockada — podendo passar ou falhar por razões erradas.

```js
// ❌ Problema: mock global não restaurado
import { test } from 'node:test';
import assert from 'node:assert/strict';

// Teste 1: mocka fetch e nunca restaura
test('busca usuário', async (t) => {
  globalThis.fetch = t.mock.fn(async () => ({
    json: async () => ({ id: 1 }),
  }));

  const user = await buscarUsuario(1);
  assert.equal(user.id, 1);
  // ⚠️ Esqueceu de restaurar: fetch ainda é mock para o próximo teste
});

// Teste 2: depende do fetch real, mas recebe o mock do teste anterior
test('integração com API externa', async () => {
  const dados = await fetch('https://api.exemplo.com/dados'); // mock fantasma!
  assert.ok(dados.ok);
});
```

```js
// ✅ Fix: usar t.mock.method (restauração automática) ou restaurar explicitamente
import { test } from 'node:test';
import assert from 'node:assert/strict';

test('busca usuário', async (t) => {
  // t.mock.fn com escopo local — restaurado automaticamente ao fim do teste
  const fetchMock = t.mock.fn(async () => ({
    json: async () => ({ id: 1 }),
  }));

  // Substituir apenas localmente, guardando referência para restaurar
  const fetchOriginal = globalThis.fetch;
  globalThis.fetch = fetchMock;

  try {
    const user = await buscarUsuario(1);
    assert.equal(user.id, 1);
  } finally {
    // Garante restauração mesmo se o teste falhar
    globalThis.fetch = fetchOriginal;
  }
});
```

> [!important]
> Para mocks de métodos em objetos, prefira `t.mock.method(obj, 'metodo')` — o runner restaura automaticamente ao final do escopo do teste. Para globals, sempre use `try/finally` ou o hook `afterEach` para garantir a restauração.

## Em entrevista

**Q: What does `node:test` provide and when would you use it over Vitest?**

`node:test` is the built-in test runner introduced in Node 18 (experimental) and stabilized in Node 20, providing `test`, `describe`, `it`, hooks like `before`/`after`, and native mocking through `t.mock.fn` and `t.mock.timers` — all with zero external dependencies. I would choose it over Vitest when building a library, CLI tool, or backend utility where keeping the dependency footprint minimal is important, since the test runner ships with the runtime itself. However, when the project involves React components, JSDOM, Testing Library, or requires snapshot testing, Vitest is the better choice because `node:test` lacks those integrations entirely.

**Q: How does mocking work in `node:test`?**

Mocking in `node:test` is exposed through the `t` context object passed to each test callback. The three main APIs are `t.mock.fn(impl)` for creating standalone spy/stub functions that track calls and arguments, `t.mock.method(object, 'methodName', impl)` for replacing a method on an existing object while preserving the reference, and `t.mock.timers.enable({ apis: ['setTimeout'] })` (Node 20.4.0+) for intercepting timers and advancing them manually with `t.mock.timers.tick(ms)`. One important behavior is that mocks created via `t.mock.method` are automatically restored at the end of the test scope, but global replacements (like patching `globalThis.fetch`) require manual restoration using `try/finally` or an `afterEach` hook. The `t.mock.reset()` call resets call counters without removing the mock, while `t.mock.restore()` fully reverts the substitution.

**Q: What are the limitations of the built-in test runner?**

The most significant limitation is the absence of snapshot testing, which is a common pattern in frontend and component testing for detecting unintended UI changes. Additionally, `node:test` has no JSDOM integration, which means you cannot test browser DOM APIs or use libraries like Testing Library that rely on a simulated browser environment. Code coverage support exists as an experimental feature (`--experimental-test-coverage`) but it lacks the depth and configurability of istanbul-based solutions offered by Vitest (`@vitest/coverage-v8`) or Jest. Finally, TypeScript support requires an external tool like `tsx` or the Node 22+ native strip-types feature, whereas Vitest handles TypeScript out of the box through its Vite pipeline — making `node:test` more friction-heavy in TypeScript-first projects.

## Vocabulário

| Português | Inglês |
|---|---|
| Corredor de testes | Test runner |
| Duplo de teste | Test double |
| Espiã de função | Function spy |
| Gancho | Hook |
| Asserção | Assertion |
| Cobertura de código | Code coverage |
| Modo de observação | Watch mode |
| Suíte de testes | Test suite |
| Substituição de método | Method mocking |
| Isolamento de teste | Test isolation |

## Fontes

- [Node.js Docs — node:test](https://nodejs.org/api/test.html) — documentação oficial do módulo `node:test`, cobrindo todas as APIs, reporters e flags de linha de comando.

## Veja também

- `[[Tooling e ecossistema moderno]]` — índice do galho 7
- `[[06 - DX flags modernos - watch, env-file e import]]` — próxima nota no galho
- `[[03-Dominios/Node/index|Node.js (MOC central)]]` — visão geral de todos os galhos
- `[[Node.js]]` — tronco da trilha Node Senior
