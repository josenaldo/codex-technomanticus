---
title: "React Red Flag Manual"
created: 2026-04-24
updated: 2026-04-24
type: manual
status: evergreen
tags:
  - javascript
  - frontend
  - react
  - code-smells
  - anti-patterns
  - entrevista
  - manual
publish: true
sources:
  - https://www.frontendjoy.com/p/29-react-codebase-red-flags-from-a-senior-frontend-developer
  - https://react.dev/learn/you-might-not-need-an-effect
  - https://blog.logrocket.com/15-common-useeffect-mistakes-react/
  - https://blog.sentry.io/react-js-performance-guide/
  - https://itnext.io/6-common-react-anti-patterns-that-are-hurting-your-code-quality-904b9c32e933
  - https://medium.com/@sureshdotariya/reactjs-jsx-anti-patterns-you-must-avoid-in-2025-f58e44d08abf
---

# React Red Flag Manual

Catálogo autoral, em português, dos **sinais de alerta** mais relevantes em codebases React — para code review, entrevistas de senior/staff e auditoria de arquitetura. Consolidado a partir de múltiplas fontes (ver [[#Bibliografia]]), com comentários próprios e exemplos adaptados. Para fundamentos de React, ver [[React]]. Para TS, ver [[TypeScript]]. Para testes, ver [[Testes em JavaScript]].

> [!info] Como usar este manual
> Cada item segue o padrão: **problema → exemplo ruim → solução com exemplo → nuances e exceções → fonte**. Callouts `[!info]-` colapsáveis trazem definições de conceitos de apoio (shim, polyfill, focus trap, discriminated union, etc.) pra leitura autocontida. A numeração é contínua (1–56) para facilitar citação ("red flag #33"). Use os capítulos como índice e o [[#Checklist para code review]] como ferramenta rápida.

> [!quote] Filosofia
> "Red flag" não é regra absoluta — é **sinal de que vale parar e pensar**. Todo padrão tem contraexemplo. O valor está em reconhecer, nomear e justificar a escolha.

---

## Índice

- **Capítulo 1** — [[#Cap. 1 — Dependências e tooling]] (#1–3)
- **Capítulo 2** — [[#Cap. 2 — Organização de código]] (#4–7)
- **Capítulo 3** — [[#Cap. 3 — Componentes e composição]] (#8–11)
- **Capítulo 4** — [[#Cap. 4 — Estado e refs]] (#12–17)
- **Capítulo 5** — [[#Cap. 5 — Memoização]] (#18–21)
- **Capítulo 6** — [[#Cap. 6 — TypeScript e hooks]] (#22–26)
- **Capítulo 7** — [[#Cap. 7 — Listas e keys]] (#27)
- **Capítulo 8** — [[#Cap. 8 — useEffect, o abismo]] (#28–36)
- **Capítulo 9** — [[#Cap. 9 — Data fetching, erros e estados de UI]] (#37–40)
- **Capítulo 10** — [[#Cap. 10 — Performance e bundle]] (#41–46)
- **Capítulo 11** — [[#Cap. 11 — Acessibilidade]] (#47–50)
- **Capítulo 12** — [[#Cap. 12 — Legibilidade]] (#51–53)
- **Capítulo 13** — [[#Cap. 13 — Arquitetura e manutenibilidade]] (#54–56)
- [[#Checklist para code review]]
- [[#Bibliografia]]

---

## Cap. 1 — Dependências e tooling

### 1. Usar libs para tarefas que o JS nativo resolve

**O problema.** Muita codebase acumula dependências que existiam por boa razão há 5 anos, mas que hoje são redundantes porque a plataforma evoluiu. Cada dep extra tem custo real: peso no bundle (afeta [LCP](https://web.dev/articles/lcp) e INP), mais uma superfície de CVEs pra auditar, mais uma API pra sua equipe aprender, mais um candidato a `peer dependency` conflict quando você subir versão do React.

O caso clássico é `lodash`. A lib foi essencial quando o JS não tinha `Array.prototype.flat`, `Object.entries`, `??` (nullish coalescing), spread em objetos. Hoje, quase tudo que `lodash` oferece tem equivalente nativo — e frequentemente **mais performático**, porque o engine V8 otimiza as built-ins.

**Mapa de substituições nativas.**

| Lib / uso comum       | Substituto nativo                                          | Desde  |
| --------------------- | ---------------------------------------------------------- | ------ |
| `_.cloneDeep(obj)`    | `structuredClone(obj)`                                     | 2022   |
| `_.groupBy(arr, fn)`  | `Object.groupBy(arr, fn)` / `Map.groupBy`                  | 2024   |
| `_.last(arr)`         | `arr.at(-1)`                                               | 2022   |
| `_.isEmpty(obj)`      | `Object.keys(obj).length === 0`                            | sempre |
| `_.uniq(arr)`         | `[...new Set(arr)]`                                        | sempre |
| `_.flatten(arr)`      | `arr.flat()`                                               | 2019   |
| `_.pick(obj, keys)`   | `Object.fromEntries(keys.map(k => [k, obj[k]]))`           | 2019   |
| `_.debounce(fn, 300)` | `AbortController` + `setTimeout`, ou hook próprio          | —      |
| `uuid` (lib)          | `crypto.randomUUID()`                                      | 2022   |
| `classnames` / `clsx` | Template literal + `&&` (ou mantenha — `clsx` é 239 bytes) | —      |

> [!warning] "Nativo" tem asterisco
> `Object.groupBy` é ES2024 — precisa de Node 21+ ou browsers recentes. Se seu alvo inclui Safari antigo, cheque [caniuse.com/?search=Object.groupBy](https://caniuse.com/?search=Object.groupBy) **antes** de remover o polyfill. Regra: adote nativo quando o alvo de suporte cobre, senão mantenha o shim.

> [!info]- O que é um Shim e um Pollyfill?
> Shim: uma função que implementa API moderna usando recursos antigos. Exemplo:
>
> ```ts
> function structuredCloneShim(obj: any) {
  > return JSON.parse(JSON.stringify(obj));
> }
> ```
>
> Pollyfill: um pacote que detecta se a API nativa existe e, se não, registra o shim globalmente. Exemplo:
>
> ```ts
> if (!('structuredClone' in window)) {
>   (window as any).structuredClone = structuredCloneShim;
> }
> ```

**Exemplo — substituindo `lodash.cloneDeep`**:

```ts
// antes — 24KB gzipped de lodash só pra isso
import cloneDeep from 'lodash/cloneDeep';
const copy = cloneDeep(state);

// depois — 0KB, e lida com Map/Set/Date nativamente
const copy = structuredClone(state);
```

> [!tip] Antes de `npm install`: cheque [caniuse](https://caniuse.com/) e [MDN](https://developer.mozilla.org/). Se a feature que você precisa está lá e cobre seu alvo, pense duas vezes antes de adicionar a dep.

**Quando a lib ainda vale.** `debounce`/`throttle` com edge cases (leading, trailing, maxWait) é não-trivial — `lodash.debounce` isolado ou hooks dedicados (`useDebounce`, `useDebouncedCallback`) são ok. Utilitários de imutabilidade complexa (Immer) continuam ganhando do manual. O ponto não é "zero deps", é **deps justificadas**.

**Fonte**: [1]

### 2. Deps pesadas quando existem alternativas leves

**O problema.** Algumas libs populares são pesadas por razões históricas (arquitetura não tree-shakable, features legadas). Se existe alternativa moderna de tamanho 10x menor que resolve o seu caso, a troca é quase sempre positiva — especialmente se for dep de primeira camada (carregada no bundle inicial).

**Suspeitos clássicos.**

- **`moment.js`** — ~70KB gzipped, não tree-shakable, [mantido em modo de manutenção pelos próprios autores](https://momentjs.com/docs/#/-project-status/). Alternativas:
  - **`date-fns`** (~13KB se tree-shakable, import por função): `import { format, addDays } from 'date-fns'`
  - **`dayjs`** (~2KB, API compatível com moment): drop-in replacement
  - **`Intl.DateTimeFormat`** nativo: zero dep pra formatação básica
  - **`Temporal`** (proposta ES, polyfill disponível): o futuro

- **`axios`** (~13KB gzipped) onde `fetch` nativo resolve. `axios` ainda tem valor em casos reais (interceptors, retry, progress) — mas pra 90% dos fetches simples, `fetch` + pequeno wrapper basta.

- **`uuid`** — ~5KB pra gerar IDs quando `crypto.randomUUID()` é uma linha.

- **`react-icons`** completo em vez de ícones individuais (`lucide-react` com tree-shaking, ou SVG inline).

**Exemplo — substituindo `moment` por `Intl.DateTimeFormat`**:

```ts
// antes
import moment from 'moment';
const formatted = moment(date).format('DD/MM/YYYY HH:mm');
// ❌ 70KB no bundle só pra isso

// depois
const formatter = new Intl.DateTimeFormat('pt-BR', {
  dateStyle: 'short',
  timeStyle: 'short',
});
const formatted = formatter.format(date);
// ✅ 0KB, e respeita locale do usuário automaticamente
```

**Ferramentas pra decidir.**

- [bundlephobia.com](https://bundlephobia.com/) — tamanho de qualquer pacote npm com gráfico histórico
- [pkg-size.dev](https://pkg-size.dev/) — inclui análise de exports individuais
- [bundle analyzer](https://github.com/btd/rollup-plugin-visualizer) — visualiza o que tá pesando **no seu bundle real**

> [!tip] Regra de bolso
> Se uma dep ocupa mais de 5% do bundle inicial e você usa menos de 20% da API dela, investigue alternativa.

**Fonte**: [1]

### 3. Sem linter nem formatter

**O problema.** Sem ferramenta automática garantindo estilo e qualidade, cada PR vira discussão de vírgula, ponto-e-vírgula, `const` vs `let`. Pior: bugs reais passam despercebidos porque o ruído cognitivo do review é alto demais pra ver os problemas que importam. Lint não é preferência estética — é **automação de code review**.

**O que linter (ESLint/Biome) pega que um humano cansado não pega:**

- Variável não usada → pode ser sinal de import errado ou código morto
- `useEffect` sem deps corretas (`react-hooks/exhaustive-deps`) — **principal defesa contra stale closure** (ver #26)
- `any` implícito (`@typescript-eslint/no-explicit-any`)
<!-- markdownlint-disable-next-line MD033 -->
- <code>==</code> em vez de <code>===</code>
- Regras de acessibilidade (`jsx-a11y/*`)
- Ordem de imports, console.log esquecido, código inalcançável

**Stack sugerida (2026):**

```jsonc
{
  "devDependencies": {
    "eslint": "^9",
    "@typescript-eslint/eslint-plugin": "^8",
    "eslint-plugin-react": "^7",
    "eslint-plugin-react-hooks": "^5",
    "eslint-plugin-jsx-a11y": "^6",
    "prettier": "^3",
    "husky": "^9",
    "lint-staged": "^15"
  }
}
```

**Alternativa moderna: [Biome](https://biomejs.dev/).** Formatter + linter em Rust, 10-50x mais rápido que ESLint + Prettier, config única. Se tá começando projeto novo, considere.

**Integração obrigatória.**

1. **Editor** — ESLint/Biome rodando on-save. Feedback imediato.
2. **Pre-commit** — `husky` + `lint-staged` bloqueia commit que fere regras. Exemplo:

   ```jsonc
   // package.json
   "lint-staged": {
     "*.{ts,tsx}": ["eslint --fix", "prettier --write"]
   }
   ```

3. **CI** — última linha de defesa. Build quebra se lint falhar. Impede bypass via `git commit --no-verify`.

> [!warning] Não desligue regras por conveniência
> `// eslint-disable-next-line` pra calar o linter é red flag em si (ver #23). Se a regra tá errada pro seu caso, **configure a regra** no `.eslintrc` explicando por quê — documentado, versionado, revisável. Comentário inline é dívida invisível.

**Fonte**: [1]

---

## Cap. 2 — Organização de código

### 4. Estrutura de pastas inconsistente

**O problema.** Metade dos componentes em `src/components/`, metade em `src/ui/`, alguns em `src/views/`, feature nova em `src/features/`. Cada PR negocia onde as coisas vão. Desenvolvedor novo gasta a primeira semana arqueologizando o layout do repo em vez de produzir. Pior: arquivos "órfãos" se escondem em diretórios esquecidos e ninguém sabe se podem deletar.

Isso não é questão estética — **estrutura consistente é navegação**. Em repo bem organizado, você consegue adivinhar onde um arquivo mora antes de abrir o VSCode.

**Duas convenções viáveis.**

```text
# Feature-based (o que mais escala em SPAs médias/grandes)
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api.ts
│   │   └── types.ts
│   ├── checkout/
│   └── dashboard/
├── shared/        ← código genuinamente reusável entre features
│   ├── ui/        ← Button, Input, Modal...
│   └── lib/       ← date, string, http...
└── app/           ← rotas, providers, entry point
```

```text
# Domain-based (mais comum em backends; usado em frontends com modelos fortes)
src/
├── users/
├── orders/
├── products/
└── shared/
```

> [!info]- O que é "feature-based" vs "domain-based"?
> **Feature-based**: organiza por _funcionalidade do produto_ (auth, checkout, dashboard). Cada feature é auto-contida. Boa pra SPAs cujas funcionalidades são relativamente independentes.
>
> **Domain-based**: organiza por _entidade do modelo de negócio_ (users, orders, products). Herdada de arquitetura DDD. Boa quando o app é CRUD sobre entidades bem definidas — múltiplas features operam sobre as mesmas entidades.
>
> Não são excludentes: pode ter `features/checkout/` que consome `domain/orders/`. Mas **escolha uma como raiz** e documente.

**Regra prática.** Escolha uma convenção, documente no `README.md` com exemplos, e passe review rigoroso nos primeiros 10 PRs pra segurar. Depois vira cultura.

**Sinal de piora silenciosa.** Se você tem `components/`, `views/`, `ui/`, `widgets/`, `pages/` **todos ao mesmo tempo** — pare. A equipe não tem modelo mental compartilhado do que é o quê.

**Fonte**: [1]

### 5. `utils.ts` como gaveta de tranqueiras

**O problema.** `utils.ts` (ou `helpers.ts`, ou `lib.ts`) começa com `formatDate`. Seis meses depois tem `formatDate`, `slugify`, `parseCurrency`, `debounce`, `getUserInitials`, `isValidEmail`, `truncate`, `deepEqual`, `classNames`, `sleep`, `retry`, `randomId`. Vira o _junk drawer_ do repo:

- **Hotspot de merge conflict** — todo mundo edita o mesmo arquivo.
- **Sem coesão** — funções sem relação entre si, nenhum tema unificador.
- **Difícil de descobrir** — ninguém procura `formatCurrency` em `utils.ts`; cada dev reimplementa.
- **Import cascata** — `utils.ts` importa de 30 lugares, e bundlers menos espertos acabam puxando mais código do que precisam.

**Solução — particionar por domínio.**

```text
src/shared/lib/
├── date.ts          ← formatDate, parseDate, addBusinessDays
├── string.ts        ← slugify, truncate, getInitials
├── currency.ts      ← parseCurrency, formatCurrency
├── validation.ts    ← isEmail, isCPF, isStrongPassword
├── array.ts         ← chunk, groupBy, unique
└── async.ts         ← sleep, retry, withTimeout
```

Cada arquivo tem **uma razão pra existir**. Quando você precisa de `formatCurrency`, sabe que está em `currency.ts`. Merge conflicts diminuem porque trabalho de domínios diferentes toca arquivos diferentes.

> [!tip] Teste do arquivo utils
> Abra seu `utils.ts`. Se não conseguir escolher **um nome curto** (2 palavras) que descreva o conteúdo todo, o arquivo tá fazendo coisas demais. Divida.

**Quando `utils.ts` ainda vale.** Protótipos, scripts, projetos de um-só-dev. O problema aparece quando o repo tem mais de 2 pessoas editando ativamente.

**Fonte**: [1]

### 6. Arquivos relacionados não colocalizados

**O problema.** Convenção herdada de projetos antigos: separação por _tipo de arquivo_ em vez de _feature_.

```text
src/
├── components/UserCard/UserCard.tsx
├── __tests__/UserCard.test.tsx
├── styles/UserCard.module.css
├── hooks/useUserCard.ts
└── types/UserCard.types.ts
```

Pra entender _uma_ feature, você pula entre 4 pastas. Pra **renomear** `UserCard` → `MemberProfile`, tem que lembrar de cada uma. Código relacionado parece não-relacionado porque está fisicamente distante. Quando deleta a feature, quase sempre esquece arquivos órfãos.

**Solução — colocalize tudo que muda junto.**

```text
src/features/members/UserCard/
├── UserCard.tsx
├── UserCard.test.tsx
├── UserCard.module.css
├── useUserCard.ts           ← hook específico desta feature
├── UserCard.types.ts
└── index.ts                  ← re-exporta o componente público
```

**Princípio.** Arquivos que mudam juntos **moram juntos**. É o mesmo raciocínio por trás do princípio de [colocalização](https://kentcdodds.com/blog/colocation) do Kent C. Dodds: "o que muda junto, fica junto". Quando for deletar a feature, `rm -rf UserCard/` e pronto.

> [!info]- E testes? Ficam junto do código?
> Sim — `Component.tsx` + `Component.test.tsx` na mesma pasta. Duas razões:
>
> 1. **Descoberta**: quem edita o componente _vê_ que existe teste e, idealmente, atualiza.
> 2. **Coesão**: teste sem componente é órfão; componente sem teste é visível.
>
> A exceção são **testes E2E** (Playwright, Cypress) que testam jornadas inteiras — esses ficam numa pasta própria (`e2e/`, `tests/e2e/`) porque não pertencem a nenhum componente específico.

**Quando separar faz sentido.** `shared/ui/` genuinamente usado por todas as features, gerador de código (OpenAPI → `src/generated/`), assets públicos (`public/`). Esses podem ficar em pastas globais — a regra de colocalização é pro _código de feature_.

**Fonte**: [1]

### 7. Barrel files com `export *`

**O problema.** Barrel file é um `index.ts` que reexporta o conteúdo de arquivos irmãos pra permitir imports limpos:

```ts
// src/shared/ui/index.ts
export * from './Button';
export * from './Input';
export * from './Modal';
// ... 40 linhas assim
```

Permite escrever `import { Button } from '@/shared/ui'` em vez de `from '@/shared/ui/Button'`. Parece elegante, mas tem custos reais:

- **Quebra tree-shaking em vários bundlers.** Quando você importa `{ Button }` do barrel, bundlers menos agressivos incluem o código de `Modal`, `Input`, etc. no bundle final. Vite e Rollup modernos costumam dar conta; Webpack antigo ou combinações de plugins estranhos, não.
- **Hot-reload mais lento.** Qualquer edição em qualquer arquivo que o barrel reexporta invalida _todo mundo que importa do barrel_. Dev server trava.
- **Ciclos de import invisíveis.** `A/index.ts` exporta `A1`, que importa `B` do barrel `B/index.ts`, que exporta `B1`, que importa `A` do barrel... ciclo. Roda o app e dá erro esotérico `Cannot access 'X' before initialization`.
- **"Go to definition" vai pro barrel**, não pro arquivo real. +1 clique em cada navegação.
- **Refactor ferra.** Renomear `Button` → `SolidButton` via IDE pode ou não pegar o reexport genérico `export * from './Button'`.

> [!info]- O que é tree-shaking?
> Processo do bundler que **remove código não usado** do bundle final. Funciona analisando os `import`/`export` estáticos: se você importou só `format` de `date-fns`, o bundler não inclui `parseISO`, `addDays`, etc.
>
> Tree-shaking depende de: (1) módulos ES (`import`/`export`, não CommonJS `require`), (2) ausência de side effects declarados (`"sideEffects": false` no `package.json`), (3) bundler que faz análise estática agressiva (Rollup > Vite > esbuild > Webpack > antigos).
>
> Barrel files podem interferir porque o bundler tem que seguir `export *` e inferir o que cada arquivo exporta — trabalho extra, nem sempre bem feito.

**Solução.**

1. **Evite barrels desnecessários.** Import direto é melhor: `import { Button } from '@/shared/ui/Button'`.
2. **Se precisar de barrel** (API pública de um pacote, por exemplo), use **exports nomeados explícitos**, não `export *`:

   ```ts
   // bom — explícito, tree-shakable, grepável
   export { Button } from './Button';
   export { Input } from './Input';
   export { Modal } from './Modal';

   // ruim
   export * from './Button';
   export * from './Input';
   export * from './Modal';
   ```

3. **Marque `"sideEffects": false`** no `package.json` (ou em arquivos específicos) pra sinalizar ao bundler que tree-shaking é seguro.

**Quando barrels valem.** Bibliotecas publicadas no npm (a API pública precisa ser um ponto único). Módulos pequenos (< 5 exports) onde o custo é mínimo. Features internas com interface pública clara (`features/checkout/index.ts` exportando só `CheckoutPage`, escondendo o resto).

**Fonte**: [1]

---

## Cap. 3 — Componentes e composição

### 8. God components

**O problema.** Componente de 800 linhas que faz fetch de dados, filtra, ordena, paginação, renderiza tabela com linhas expansíveis, abre modal de edição, contém form com 12 campos, valida form, submete, trata erros, atualiza cache. Tudo num arquivo só, tudo num componente só.

Sintomas:

- **Qualquer mudança é alto risco** — adicionar coluna na tabela pode quebrar o form, porque state local está entrelaçado.
- **Testes impossíveis** — pra testar validação do form, você tem que mockar o fetch, o modal, o roteador e o toast.
- **Reuso zero** — a tabela dali não serve em outro lugar porque está acoplada ao state do pai.
- **Medo de refatorar** — ninguém entende o arquivo inteiro, então ninguém toca.

God component é quase sempre consequência de crescer sem extrair: cada feature nova foi "mais uma função aqui, mais um estado ali", e após 18 meses você tem um monstro.

**Solução — três cortes clássicos.**

**1. Extrair sub-componentes por responsabilidade visual.**

```tsx
// antes — tudo num arquivo
function Dashboard() {
  // 80 linhas de state, fetch, filtros...
  return (
    <div>
      {/* 200 linhas de header */}
      {/* 300 linhas de tabela */}
      {/* 150 linhas de modal */}
      {/* 100 linhas de form */}
    </div>
  );
}

// depois — composição clara
function Dashboard() {
  return (
    <DashboardLayout>
      <DashboardHeader />
      <UserTable />
      <EditUserModal />
    </DashboardLayout>
  );
}
```

**2. Extrair lógica em custom hooks.**

```tsx
// antes — lógica misturada com JSX
function UserTable() {
  const [users, setUsers] = useState([]);
  const [sortKey, setSortKey] = useState('name');
  const [filter, setFilter] = useState('');
  useEffect(() => { /* fetch */ }, []);
  const sorted = useMemo(() => /* ... */, [users, sortKey]);
  const filtered = useMemo(() => /* ... */, [sorted, filter]);
  return <table>{/* ... */}</table>;
}

// depois — hook isolável, testável sem DOM
function useUserTable() {
  // toda lógica aqui — retorna dados + handlers
  return { rows, sortBy, filterBy, isLoading };
}

function UserTable() {
  const { rows, sortBy, filterBy, isLoading } = useUserTable();
  return <table>{/* só JSX */}</table>;
}
```

**3. Padrão container/presenter (quando faz sentido).**

```tsx
// UserTableContainer.tsx — busca dados, lida com estado
function UserTableContainer() {
  const { data, isLoading, error } = useUsers();
  if (isLoading) return <Skeleton />;
  if (error) return <ErrorState error={error} />;
  return <UserTableView users={data} />;
}

// UserTableView.tsx — só renderiza, fácil de testar no Storybook
function UserTableView({ users }: { users: User[] }) {
  return <table>{/* ... */}</table>;
}
```

> [!info]- Container vs Presenter — ainda vale?
> Padrão popularizado em 2015 (Dan Abramov), hoje menos rígido. A essência é: **separar quem busca dados de quem desenha pixels**. O presenter é puro (só props in, JSX out) e vira "material pronto" pro Storybook, testes visuais e reuso.
>
> Hooks customizados frequentemente substituem o container. Não force o padrão — use quando a separação clareia, ignore quando vira burocracia.

**Limite prático.** Se o arquivo passou de ~300 linhas, pare e avalie. Raro um componente React honesto precisar de mais que isso. Se precisa, provavelmente são responsabilidades distintas disfarçadas.

**Fonte**: [1]

### 9. Passar objeto inteiro quando só precisa de campos

**O problema.** Quando você passa um objeto enorme como prop porque o filho usa 2 campos, três coisas quebram:

1. **Acoplamento excessivo.** O filho agora depende da _forma_ completa do objeto. Renomear `user.avatarUrl` pra `user.profile.avatar` te obriga a mudar o filho, mesmo que ele só use o nome.
2. **Re-render desnecessário.** Se o pai atualizar qualquer campo de `user` (mesmo um que o filho não usa), o filho re-renderiza. Com `React.memo`, a comparação default é shallow — objeto diferente = render.
3. **Tipagem vaga.** `Avatar` dizendo "eu preciso de um `User` inteiro" é menos preciso que "eu preciso de `name` e `imageUrl`".

**Exemplo.**

```tsx
// ruim — Avatar agora depende da estrutura inteira de User
function Avatar({ user }: { user: User }) {
  return <img src={user.avatarUrl} alt={user.name} />;
}
<Avatar user={user} />

// bom — props mínimas, contrato explícito
function Avatar({ name, imageUrl }: { name: string; imageUrl: string }) {
  return <img src={imageUrl} alt={name} />;
}
<Avatar name={user.name} imageUrl={user.avatarUrl} />
```

**Benefício colateral: reusabilidade.** `Avatar({ name, imageUrl })` serve pra usuário, produto, empresa, qualquer coisa com nome e imagem. `Avatar({ user })` só serve pra coisa com `User`.

**Quando passar objeto inteiro faz sentido.**

- **Entity components** — `<UserCard user={user} />` onde o componente representa conceitualmente _aquela entidade_ e usa vários campos.
- **Formulários** — `<UserForm initialValues={user} onSubmit={...} />` onde o form opera sobre a entidade inteira.
- **Quando a lista de campos passaria de 5–6 props** — ponto em que a explosão de props piora a legibilidade. Considere o objeto inteiro ou agrupar em sub-objetos (`<Chart data={chartData} config={chartConfig} />`).

Regra: pense no componente como contrato público. Se o contrato "o que eu preciso?" é pequeno, props pequenas. Se é grande e conceitualmente unificado, objeto faz sentido.

**Fonte**: [1]

### 10. Definir componente dentro de outro componente

**O problema.** Parece um refactor inocente — "`Child` só é usado aqui, vou defini-lo dentro do `Parent`". Mas React **identifica componentes por referência de função**. Toda vez que `Parent` renderiza, `function Child(...)` cria uma _função nova_ na memória — e pra React, "função nova" significa "tipo de componente diferente".

Consequências em cascata:

- **`Child` remonta a cada render do `Parent`.** State interno (`useState`) é zerado, effects (`useEffect`) re-executam do zero, refs perdem referência.
- **Foco perdido em inputs.** Input que tem state interno (controlado ou não) _pisca_ — perde foco, seleção, valor digitado a meio.
- **Animações reiniciam.** Enter/exit animations disparam a cada render.
- **Performance degrada.** Mesmo sem state, é trabalho gratuito: desmontar nó do DOM e montar de novo.

**Exemplo mostrando o bug.**

```tsx
// ruim — Child é redefinido a cada render de Parent
function Parent() {
  const [count, setCount] = useState(0);

  function Child() {
    const [text, setText] = useState('');
    return <input value={text} onChange={e => setText(e.target.value)} />;
  }

  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
      <Child />
      {/* digita no input, clica no botão → input zera. Por quê?
          Porque `Child` é uma função nova, então React desmonta o
          input antigo e monta um novo, com state zerado. */}
    </div>
  );
}
```

**Solução.** Definir `Child` **fora** do `Parent`:

```tsx
// bom
function Child() {
  const [text, setText] = useState('');
  return <input value={text} onChange={e => setText(e.target.value)} />;
}

function Parent() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
      <Child />
    </div>
  );
}
```

Se `Child` precisa de dados do `Parent`, passe via props. Se é _tão_ específico que não merece ser componente, inline o JSX direto:

```tsx
// alternativa — se realmente é só um pedaço do Parent, não vire componente
function Parent() {
  return (
    <div>
      <span>{/* o que seria o Child */}</span>
    </div>
  );
}
```

> [!warning] O linter pega isso
> A regra `react/no-unstable-nested-components` (do `eslint-plugin-react`) detecta esse padrão. Se não está habilitada no seu projeto, habilite.

**Quando é ok — nunca.** Genuinamente não há caso em que definir componente dentro de componente seja a resposta certa. Se precisa de fechamento sobre variáveis do pai, extraia pra fora e passe via props.

**Fonte**: [5]

### 11. Prop drilling excessivo

**O problema.** "Prop drilling" é passar uma prop por vários níveis da árvore só pra chegar num descendente profundo que precisa dela. Cada componente intermediário carrega uma prop que **não usa**, só repassa.

```tsx
// cinco níveis pra o user chegar no Avatar
function App() {
  const [user] = useUser();
  return <Layout user={user} />;
}
function Layout({ user }) { return <Header user={user} />; }
function Header({ user }) { return <Nav user={user} />; }
function Nav({ user }) { return <UserMenu user={user} />; }
function UserMenu({ user }) { return <Avatar user={user} />; }
```

Problemas:

- **Acoplamento em cascata.** Mudar a forma de `user` força mudar 5 componentes.
- **Componentes intermediários poluídos.** `Layout`, `Header`, `Nav` carregam uma prop que não é problema deles.
- **Testes mais pesados.** Cada intermediário precisa receber `user` mock pra renderizar.
- **Refactor assustador.** Adicionar `theme` ao fluxo exige tocar todos eles de novo.

**Soluções, em ordem de preferência.**

**1. Composição via `children` (solução mais elegante quando cabe).**

Em vez de passar o dado pelos níveis, deixe o nível que _tem_ o dado renderizar o nível que _precisa_ dele.

```tsx
function App() {
  const [user] = useUser();
  return (
    <Layout>
      <Header>
        <Nav>
          <UserMenu>
            <Avatar user={user} />
          </UserMenu>
        </Nav>
      </Header>
    </Layout>
  );
}
// Layout, Header, Nav, UserMenu não sabem nada de user.
```

**2. Context (quando o dado é "ambiental" — usado em muitos lugares).**

```tsx
const UserContext = createContext<User | null>(null);

function App() {
  const [user] = useUser();
  return (
    <UserContext.Provider value={user}>
      <Layout />
    </UserContext.Provider>
  );
}

function Avatar() {
  const user = useContext(UserContext);
  return <img src={user.avatarUrl} alt={user.name} />;
}
```

Cuidados com Context (ver [[#15. Um Context gigante re-renderizando meia app]]):

- Um Context por domínio (`UserContext`, `ThemeContext`, `CartContext`), não um mega-context.
- Memoize o `value` (ver [[#19. Não memoizar `value` de Context]]).

**3. Store dedicado (Zustand, Jotai, Redux) — quando o estado é global de verdade.**

```tsx
// Zustand — simples e poderoso
const useUser = create<UserState>((set) => ({
  user: null,
  login: (user) => set({ user }),
}));

function Avatar() {
  const user = useUser(state => state.user);
  return <img src={user.avatarUrl} alt={user.name} />;
}
```

Store faz sentido quando: (1) dado é compartilhado entre **muitas** partes da árvore, (2) mutações acontecem de **vários lugares**, (3) você precisa de persistência (localStorage), devtools, time-travel, etc.

> [!info]- Quando Context não é suficiente?
> Context re-renderiza **todos os consumidores** quando o `value` muda — mesmo os que só usam um pedaço. Se você tem 50 componentes lendo de um Context e o valor muda 20 vezes por segundo, é re-render demais.
>
> Stores (Zustand, Jotai, Redux) permitem **seletores**: cada consumidor re-renderiza só quando o pedaço que ele observa muda. Pra state compartilhado de alto tráfego (cursor, drag-and-drop, animações), stores ganham.

**Regra prática.** 2 níveis de prop drilling é ok. 3 níveis é alerta. 4+ níveis é refactor. Não sirva Context pra tudo — só quando o dado é genuinamente "ambiental" (usuário logado, tema, locale), não pra evitar pensar em composição.

**Fonte**: [5][6]

---

## Cap. 4 — Estado e refs

### 12. Guardar valor derivado em state

**O problema.** Guardar em `useState` um valor que pode ser **calculado** a partir de outro state ou prop. O valor vira uma cópia sincronizada manualmente — e sincronizar é uma das fontes mais comuns de bug em React.

```tsx
// ruim — duas fontes de verdade pra mesma informação
function UserCard({ firstName, lastName }) {
  const [fullName, setFullName] = useState(`${firstName} ${lastName}`);
  // ... e agora? quem atualiza fullName quando firstName muda?
  // você vai querer um useEffect — e aí já está em terreno pantanoso
  return <h1>{fullName}</h1>;
}
```

Consequências:

- **Stale values.** Props mudam, state fica pra trás até algum effect atualizar — passa render desatualizado.
- **Cascata de effects.** Pra sincronizar, você escreve `useEffect(() => setFullName(...), [firstName, lastName])` — e cria render extra a cada mudança (ver [[#28. Transformar dados em Effect em vez de derivar no render]]).
- **Inconsistência.** Se dois lugares atualizam `firstName` mas só um lembra de atualizar `fullName`, bug.

**Solução — derive no render.**

```tsx
// bom — uma fonte de verdade, sempre atualizado
function UserCard({ firstName, lastName }) {
  const fullName = `${firstName} ${lastName}`; // cálculo puro
  return <h1>{fullName}</h1>;
}
```

Render em React é barato. A cada render, `fullName` é recalculado — e isso é **o que você quer**.

**E se o cálculo for caro?** Aí sim: `useMemo`.

```tsx
function Table({ items, filter }) {
  // heavy() custa caro — memoize com base nas entradas reais
  const filtered = useMemo(() => heavy(items, filter), [items, filter]);
  return <ul>{filtered.map(/* ... */)}</ul>;
}
```

Mas **comece sem `useMemo`**. Só adicione quando profiling mostrar que aquele cálculo é o gargalo. Memoização prematura é custo (memória, complexidade de deps) sem benefício.

**Regra de ouro.** Se o valor pode ser calculado de state/props, **ele não é state**. É um cálculo.

> [!info]- "Fonte única da verdade" (single source of truth)
> Princípio: cada peça de dado tem **um lugar canônico** onde vive. Cópias derivadas sempre se calculam a partir desse lugar, nunca guardam cópia.
>
> Em React: state local, Context, store (Zustand/Redux), ou props vindo do pai são fontes. Tudo mais é **derivado** — calcule no render, não copie pra outro state.

**Fonte**: [1][2]

### 13. Usar state quando deveria ser ref

**O problema.** Nem todo valor que muda precisa causar re-render. State (`useState`) **causa re-render**. Ref (`useRef`) **não causa**. Usar state pra valores que o render não precisa "ver" é desperdício e pode gerar render infinito.

**O que deveria ser ref, não state:**

- **Timer IDs** (`setTimeout`, `setInterval`) — você precisa lembrar pra limpar, mas UI não depende disso.
- **Valor anterior de uma prop/state** (pra comparar com o atual).
- **Flag "já montou"** ou "já executou uma vez".
- **Referência a elemento DOM** — `ref={meuRef}` é ref, não state.
- **Cache de valor computado** que você controla manualmente.
- **Instância de classe** — `new Map()`, `new IntersectionObserver()`, WebSocket, AbortController.

**Exemplo — debounce ID.**

```tsx
// ruim — state pra algo que UI nem renderiza
function Search() {
  const [timeoutId, setTimeoutId] = useState<number | null>(null);
  const handleChange = (e) => {
    if (timeoutId) clearTimeout(timeoutId);
    const id = setTimeout(() => fetch(e.target.value), 300);
    setTimeoutId(id); // ← re-render inútil
  };
}

// bom — ref
function Search() {
  const timeoutRef = useRef<number | null>(null);
  const handleChange = (e) => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => fetch(e.target.value), 300);
  };
}
```

**Exemplo — instância mutável que persiste entre renders.**

```tsx
// bom — AbortController vive na ref, não recria a cada render
function useFetchOnMount(url: string) {
  const controllerRef = useRef<AbortController | null>(null);
  useEffect(() => {
    controllerRef.current = new AbortController();
    fetch(url, { signal: controllerRef.current.signal });
    return () => controllerRef.current?.abort();
  }, [url]);
}
```

> [!info]- Quando usar `useRef` vs `useState`
> **Pergunta chave**: _a mudança desse valor deve re-renderizar o componente?_
>
> - **Sim** → `useState`. (Contador que aparece na tela, texto digitado, item selecionado.)
> - **Não** → `useRef`. (Timer ID, flag interna, referência a DOM, contador de cliques que só é lido num handler.)
>
> Casos de fronteira: se o valor afeta outros _effects_ mas não o JSX, ainda é state (deps são reativos a state, não a ref).

**Refs não são "state preguiçoso".** Mudanças em `ref.current` não disparam re-render. Se você mudar a ref e esperar que a UI reflita, nada acontece até algum outro gatilho renderizar.

**Fonte**: [1]

### 14. Jogar tudo num store global

**O problema.** Uma vez que o projeto instala Zustand/Redux/Jotai, a equipe tende a jogar _tudo_ lá. Em 6 meses, você tem 40 slices — e metade é estado que só um componente usa. Problemas:

- **Acoplamento global artificial.** Estado que era local agora é parte da "API" global do app.
- **Testes mais pesados.** Componente que deveria ser testável isoladamente precisa configurar store mock.
- **Performance.** Qualquer subscriber mal configurado re-renderiza em mudança de campo não relacionado.
- **Navegação piora.** Pra entender de onde vem um valor, você caça redutores/slices em vez de subir a árvore de componentes.

**Hierarquia do estado** (do mais local ao mais global):

1. **State derivado** — calcule no render. Não é estado.
2. **`useState` / `useReducer` local** — default para estado de UI.
3. **"Lift state up"** — mover pra ancestral comum quando 2+ filhos compartilham.
4. **Context** — quando o estado é "ambiental" e lido de vários lugares da árvore.
5. **Server state** (React Query, SWR) — estado vindo do servidor tem cache, dedup, revalidação — **não é seu** estado, é cache do servidor.
6. **Store global** (Zustand, Redux, Jotai) — quando realmente é global e muitas fontes mutam.

**Regra prática.** Comece em 2 (state local). Suba na hierarquia apenas quando houver pressão real: múltiplos consumidores distantes, persistência necessária, devtools/time-travel valiosos, performance de re-render (seletores granulares do store).

> [!tip] Server state ≠ client state
> Antes de colocar dados de API num store global, considere [[React Query|React Query/TanStack Query]] ou SWR. Eles resolvem cache, dedup, revalidação, paginação, mutation — coisas que você _vai_ implementar mal no Redux.

**Fonte**: [1]

### 15. Um Context gigante re-renderizando meia app

**O problema.** Context é reativo ao `value` inteiro — se o value muda, **todos os consumidores re-renderizam**, mesmo quem só usa uma parte. Então:

```tsx
// ruim — mudar theme faz quem só consome user re-renderizar
type AppContext = {
  user: User;
  theme: Theme;
  settings: Settings;
  cart: Cart;
};

<AppContext.Provider value={{ user, theme, settings, cart }}>
  {children}
</AppContext.Provider>;
```

Se o carrinho tem 20 mudanças por segundo (item sendo arrastado, por exemplo), o `ThemeToggle` re-renderiza 20 vezes por segundo sem motivo.

**Solução — divida por domínio.**

```tsx
// bom — um Context por preocupação
<UserContext.Provider value={userValue}>
  <ThemeContext.Provider value={themeValue}>
    <CartContext.Provider value={cartValue}>
      <SettingsContext.Provider value={settingsValue}>
        {children}
      </SettingsContext.Provider>
    </CartContext.Provider>
  </ThemeContext.Provider>
</UserContext.Provider>
```

Agora mudanças no cart só afetam quem consome `CartContext`. A árvore cresce um pouco, mas normalmente você cria um componente `<AppProviders>{children}</AppProviders>` que agrupa.

**Segunda otimização — split entre state e dispatch.**

Padrão usado por libs (e pelo próprio Context do React em exemplos avançados): **dois contexts** — um pro valor, outro pros updaters.

```tsx
const ThemeValueContext = createContext<Theme>('light');
const ThemeDispatchContext = createContext<(t: Theme) => void>(() => {});

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState<Theme>('light');
  return (
    <ThemeValueContext.Provider value={theme}>
      <ThemeDispatchContext.Provider value={setTheme}>
        {children}
      </ThemeDispatchContext.Provider>
    </ThemeValueContext.Provider>
  );
}

// Quem só quer TROCAR tema (não ler) não re-renderiza quando o tema muda:
function ThemeToggle() {
  const setTheme = useContext(ThemeDispatchContext);
  return <button onClick={() => setTheme('dark')}>Dark</button>;
}
```

**Terceira otimização — memoize o `value`.** Ver [[#19. Não memoizar `value` de Context]].

> [!info]- Por que Context re-renderiza "meia app"?
> Todo componente que chama `useContext(X)` está "inscrito" em `X`. Quando o Provider muda `value` (comparação `Object.is`), React re-renderiza **todos** esses componentes — ignorando `React.memo` no caminho.
>
> `Object.is` é referência pra objetos. Se você passar `{ user, theme }` inline no Provider, é objeto novo a cada render **do Provider**, então `Object.is` dá `false` e todos os consumidores re-renderizam. Por isso memoizar o value é crítico.

**Fonte**: [1][4]

### 16. Resetar state manualmente em vez de usar `key`

**O problema.** Você tem um componente `<Profile userId={...} />` com state interno (comentário rascunhado, tab selecionada, scroll position). Quando `userId` muda, você quer zerar esse state. O instinto é usar `useEffect`:

```tsx
// ruim — reset via effect
function Profile({ userId }) {
  const [comment, setComment] = useState('');
  const [selectedTab, setSelectedTab] = useState('overview');

  useEffect(() => {
    setComment('');
    setSelectedTab('overview');
  }, [userId]);

  // ...
}
```

Problemas:

- **Stale flash.** React renderiza com valores antigos **primeiro**, depois o effect roda e chama `setState`, o que dispara **segundo render** com valores corretos. O usuário pode ver o comentário anterior por um frame.
- **Esquecer um state.** Você tem 4 `useState`s? Precisa lembrar de zerar todos. Adicionou um quinto? Fácil esquecer.
- **Esforço mental.** Toda vez que adiciona state, precisa pensar "preciso zerar isso também?".

**Solução — `key` prop.** React usa `key` pra identificar instâncias. Quando `key` muda, React **desmonta e remonta** o componente — state é zerado naturalmente, effects re-executam, é como se fosse primeira vez.

```tsx
// bom — key força remount, todo state interno reseta
<Profile userId={userId} key={userId} />
```

```tsx
function Profile({ userId }) {
  // state começa "zerado" sempre que a key muda — sem nenhum effect extra
  const [comment, setComment] = useState('');
  const [selectedTab, setSelectedTab] = useState('overview');
  // ...
}
```

**Onde esse padrão brilha:**

- **Form de edição de entidade** — `<EditForm itemId={id} key={id} />`. Mudar de item reseta tudo.
- **Modal que reabre** — `<Modal key={openCount}>` pra garantir estado limpo a cada abertura.
- **Páginas de detalhe** — `<UserProfile key={userId} />` faz roteamento cliente funcionar como se fosse full page reload (em termos de state).

**Cuidado — `key` tem custo.** Remount **desmonta o DOM** e monta de novo. Se o componente é pesado (gráfico grande, mapa), isso pode piscar. Na dúvida, meça. Pra casos pesados, considere state local condicional mesmo.

> [!info]- `key` não é só pra listas
> Conhecida no contexto de `array.map(item => <Row key={item.id} />)`, mas funciona em qualquer componente. `key` **identifica a instância** — quando muda, React trata como componente diferente.

**Fonte**: [2]

### 17. Ajustar state baseado em props via Effect

**O problema.** Variação do #16 e do #28. Você precisa que "quando `items` mudar, `selection` volte pra null" (ou pro primeiro item, etc). Cai no padrão:

```tsx
// ruim — effect pra sincronizar state derivado
function List({ items }) {
  const [selection, setSelection] = useState<Item | null>(null);

  useEffect(() => {
    setSelection(null);
  }, [items]);

  // ...
}
```

Mesmos problemas: render extra, stale flash, acoplamento sutil.

**Três soluções, em ordem de preferência.**

**1. Calcule no render (se `selection` é derivável).**

```tsx
// se a seleção é "o primeiro item", derive
function List({ items }) {
  const selection = items[0] ?? null;
  return /* ... */;
}
```

**2. `key` pra remount (se a "identidade" do componente muda quando `items` muda).**

```tsx
// se items mudando significa "lista diferente", use key
<List items={items} key={listId} />
```

**3. Guarde ID em state, derive o objeto no render.**

```tsx
// bom — state guarda apenas ID (primitivo, estável)
function List({ items }: { items: Item[] }) {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  // se o selectedId não existe mais em items, é null (derivado, sem effect)
  const selected = items.find(i => i.id === selectedId) ?? null;

  return (
    <ul>
      {items.map(item => (
        <li key={item.id} onClick={() => setSelectedId(item.id)}>
          {item.name}
        </li>
      ))}
    </ul>
  );
}
```

Esse padrão (**guardar ID, derivar objeto**) é poderoso:

- Se o item sumiu de `items` (foi deletado), `selected` vira `null` automaticamente.
- Se o item foi atualizado (mesmo ID, nome novo), `selected` reflete o novo dado.
- Zero effects. Zero sincronização.

> [!tip] Heurística de decisão
> Sempre que sentir vontade de escrever `useEffect(() => setX(...), [y])`, pare e pergunte: **"existe uma fórmula que derive `x` de `y`?"** Quase sempre existe.

**Fonte**: [2]

---

## Cap. 5 — Memoização

> [!info]- Fundamento — por que memoização importa em React
> React compara props com **referência** (`Object.is`), não valor. Se a prop é `{ x: 1 }` hoje e `{ x: 1 }` amanhã mas são objetos diferentes na memória, React considera "mudou" e re-renderiza.
>
> `useMemo`, `useCallback` e `React.memo` existem pra **preservar referência** entre renders quando o conteúdo não mudou. Sem isso, quebra otimizações (`React.memo`), dispara effects sem razão (deps instáveis), re-renderiza árvores grandes.
>
> **React 19 Compiler** promete automatizar muito disso — mas ainda não é default em todo projeto. Até lá, entender memoização manual é obrigatório pra perf de verdade.

### 18. Memoização quebrada por default inline

**O problema.** Defaults escritos inline são recriados a cada render — e quando usados como dep de `useMemo`/`useEffect`, **destroem a memoização**.

```tsx
// ruim — `items ?? []` cria array novo a cada render
function Table({ items }: { items?: Item[] }) {
  const rows = useMemo(() => process(items ?? []), [items ?? []]);
  //                                                ^^^^^^^^^^^
  //               array novo a cada render → useMemo nunca cacheia
  return /* ... */;
}
```

Aqui `[items ?? []]` é uma expressão avaliada a cada render. Se `items` é `undefined`, o fallback `[]` é um **array literal novo**, referência diferente, memo inválida. A função `process` roda toda vez.

**Solução 1 — default fora do componente.**

```tsx
// bom — referência estável, memoizada uma vez só
const EMPTY: readonly Item[] = [];

function Table({ items = EMPTY }: { items?: readonly Item[] }) {
  const rows = useMemo(() => process(items), [items]);
  return /* ... */;
}
```

`EMPTY` é criado **uma vez** quando o módulo carrega. Mesma referência em todos os renders.

**Solução 2 — default no parâmetro da função.**

```tsx
// também bom — JS avalia default só quando `items` é undefined
function Table({ items = [] as Item[] }: { items?: Item[] }) {
  // ainda assim, o `[]` é novo a cada render — então:
  const rows = useMemo(() => process(items), [items]);
  // funciona **se** items vier sempre do pai (estável).
  // Mas se o pai passar undefined e o default criar novo []...
  // bug sutil.
}
```

Prefira a **solução 1** — constante fora do componente. Tira ambiguidade.

> [!warning] Mesma armadilha com objetos
> `const user = props.user ?? {}` dentro do componente cria objeto novo quando `props.user` é `undefined`. Se `user` é dep de effect, effect roda toda vez.

**Fonte**: [1]

### 19. Não memoizar `value` de Context

**O problema.** O `value` de um Provider é objeto recriado a cada render do Provider. Se você escrever `value={{ user, setUser }}`, esse objeto é **novo todo render** — e todos os consumidores re-renderizam, mesmo quando `user` e `setUser` não mudaram.

```tsx
// ruim — objeto novo a cada render
function UserProvider({ children }) {
  const [user, setUser] = useState<User | null>(null);
  return (
    <UserContext.Provider value={{ user, setUser }}>
      {/*                   ^^^^^^^^^^^^^^^^^^^^^  */}
      {/*                   novo objeto → todos re-renderizam */}
      {children}
    </UserContext.Provider>
  );
}
```

**Solução — memoize.**

```tsx
// bom — referência estável enquanto user não mudar
function UserProvider({ children }) {
  const [user, setUser] = useState<User | null>(null);

  const value = useMemo(
    () => ({ user, setUser }),
    [user], // setUser é estável (vem de useState), não precisa declarar
  );

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}
```

Agora `value` só muda quando `user` muda. Consumidores que só usam `setUser` ainda re-renderizam (limitação fundamental de Context unificado) — pra resolver isso, split state/dispatch (ver [[#15. Um Context gigante re-renderizando meia app]]).

> [!info]- Por que `setUser` é "estável"?
> React garante que a função retornada por `useState` (o setter) tem **referência estável** entre renders. Mesmo princípio pra `useReducer`'s dispatch. Por isso setters não precisam ser declarados em deps — o linter `react-hooks/exhaustive-deps` reconhece isso.

**Regra.** Todo Provider deve ter `value` memoizado. Não é otimização prematura — é **corretude** (pra não cancelar efeitos de `React.memo` na árvore).

**Fonte**: [1]

### 20. Passar objetos/arrays inline como props

**O problema.** Sempre que você escreve `<Component prop={{ key: value }} />`, esse objeto literal é **criado a cada render do pai**. Se `Component` é envolto em `React.memo` (pra evitar re-renders quando props não mudaram), a comparação shallow dá "diferente" e o memo vira inútil.

```tsx
// ruim — objeto novo a cada render
const GridItem = React.memo(function GridItem({ options }: { options: Options }) {
  return <div style={{ gap: options.spacing }}>{/* ... */}</div>;
});

function Parent() {
  return <GridItem options={{ spacing: 8 }} />;
  //                         ^^^^^^^^^^^^^
  //                 novo objeto → memo não ajuda
}
```

**Soluções.**

**1. Constante fora do componente (quando o valor é estático).**

```tsx
const GRID_OPTIONS = { spacing: 8 } as const;

function Parent() {
  return <GridItem options={GRID_OPTIONS} />;
}
```

**2. `useMemo` (quando o valor depende de algo do render).**

```tsx
function Parent({ spacing }: { spacing: number }) {
  const options = useMemo(() => ({ spacing }), [spacing]);
  return <GridItem options={options} />;
}
```

**3. Passar primitivos (quando possível).**

```tsx
// em vez de passar objeto, passe campos individuais
<GridItem spacing={8} />
// primitivos são comparados por valor, sempre estáveis
```

> [!tip] Quando vale a pena se preocupar
> Objeto inline em prop de componente **leve** (um `<button>` simples, `<span>`): irrelevante. React render é barato pra JSX primitivo.
>
> Objeto inline em prop de componente **pesado** (tabela virtualizada, gráfico, árvore grande): crítico. É aí que memoização entrega valor real.

**Fonte**: [5][6]

### 21. Funções novas a cada render passadas pra filhos memoizados

**O problema.** Funções inline (`onClick={() => doStuff(id)}`) são **criadas a cada render**. Mesma lógica do objeto inline: quebra `React.memo`, dispara effects em filhos que recebem a função como dep.

```tsx
// ruim — handleClick é função nova a cada render do Parent
const MemoButton = React.memo(function Button({ onClick, children }) {
  console.log('Button renderizou');
  return <button onClick={onClick}>{children}</button>;
});

function Parent({ id }: { id: string }) {
  return (
    <MemoButton onClick={() => doStuff(id)}>
      {/*       ^^^^^^^^^^^^^^^^^^^^^^^^^^^  */}
      {/*       função nova → MemoButton re-renderiza sempre */}
      Click
    </MemoButton>
  );
}
```

**Solução — `useCallback`.**

```tsx
function Parent({ id }: { id: string }) {
  const handleClick = useCallback(() => doStuff(id), [id]);
  return <MemoButton onClick={handleClick}>Click</MemoButton>;
}
```

Agora `handleClick` só muda quando `id` muda. `MemoButton` só re-renderiza nessas ocasiões.

**Quando `useCallback` não vale a pena.**

- **Filho não é memoizado.** Se não tem `React.memo`, a função estável não impede nada (filho re-renderiza com o pai de qualquer jeito).
- **Função não é passada a ninguém.** Se é handler inline do próprio componente (`<button onClick={...}>`), esqueça — nada consome a "estabilidade".
- **Overhead do próprio `useCallback`** passa a ser perceptível em árvores gigantes com centenas de callbacks. Raro, mas possível.

**Padrão que funciona mesmo com pai que muda muito — `useRef` pra handler "ambulante".**

```tsx
// quando o handler muda de definição mas você quer referência estável
function Parent({ id, data }) {
  const handlerRef = useRef(() => {});
  handlerRef.current = () => doStuff(id, data); // atualiza a cada render

  // exposto como função estável
  const stableHandler = useCallback(() => handlerRef.current(), []);

  return <MemoButton onClick={stableHandler} />;
}
```

Padrão avançado — use com moderação. React 19 tem `useEvent` (estável como ref, mas sempre "vê" os valores atuais) pra esse caso.

> [!info]- React Compiler — memoização automática
> O [React Compiler](https://react.dev/reference/react-compiler/) (React 19+) analisa seu código e insere memoização **automaticamente** onde for benéfico. Em projetos onde está habilitado, `useMemo`/`useCallback` manuais tornam-se desnecessários em muitos casos.
>
> Mas: (1) ainda é opt-in, nem todo projeto usa; (2) não cobre 100% dos casos (funções passadas pra libs externas, por exemplo); (3) entender o **porquê** da memoização continua sendo habilidade de senior.

**Fonte**: [4][5]

---

## Cap. 6 — TypeScript e hooks

### 22. Higiene de TypeScript fraca

**O problema.** TypeScript é ferramenta de _garantir invariantes em compile-time_. Quando você escreve `any` toda hora, faz `as unknown as Foo` pra "convencer" o compilador, ou duplica types ("tem um `User` aqui e outro lá, quase iguais"), está **jogando fora o benefício**. Código passa a ter tipos decorativos — não catch real de bug.

**Padrões que diferenciam senior.**

**1. Discriminated unions pra estados (em vez de flags booleanas).**

```ts
// ruim — estados impossíveis representáveis
type FetchState<T> = {
  isLoading: boolean;
  data: T | null;
  error: Error | null;
};
// o que é { isLoading: true, data: dados, error: erro } ? inválido mas tipado.

// bom — discriminated union: exatamente um dos estados
type FetchState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

// uso — narrowing automático
function render(state: FetchState<User>) {
  if (state.status === 'loading') return <Spinner />;
  if (state.status === 'error') return <Error error={state.error} />;
  if (state.status === 'success') return <UserView user={state.data} />;
  return <Idle />;
}
```

Aqui o TypeScript sabe que dentro do `if (state.status === 'success')`, `state.data` existe e é `User`. Sem cast.

**2. Exhaustive checks com `never` no switch default.**

```ts
function handle(state: FetchState<User>) {
  switch (state.status) {
    case 'idle': return /* ... */;
    case 'loading': return /* ... */;
    case 'success': return /* ... */;
    case 'error': return /* ... */;
    default:
      // se alguém adicionar um novo estado e esquecer de tratar,
      // TS falha aqui em compile-time
      const _exhaustive: never = state;
      return _exhaustive;
  }
}
```

**3. `unknown` em vez de `any` quando o tipo é realmente incerto.**

```ts
// ruim — any desliga o typecheck completamente
function parse(json: any) {
  return json.user.name; // sem erro em compile-time, bomba em runtime
}

// bom — unknown força você a validar antes de usar
function parse(json: unknown) {
  if (typeof json === 'object' && json !== null && 'user' in json) {
    // agora TS sabe que existe `user` em `json`
  }
}

// melhor — use uma lib de runtime validation
import { z } from 'zod';
const UserSchema = z.object({ user: z.object({ name: z.string() }) });
const parsed = UserSchema.parse(json); // valida + tipa
```

**4. Type guards em vez de `as`.**

```ts
// ruim — cast cego, pode estar errado
const user = data as User;

// bom — type guard testa de verdade
function isUser(x: unknown): x is User {
  return typeof x === 'object' && x !== null && 'id' in x && 'name' in x;
}
if (isUser(data)) {
  // TS sabe que data é User aqui
}
```

> [!info]- O que é "narrowing" em TypeScript?
> Mecanismo do TS que **restringe** o tipo de uma variável dentro de um bloco, baseado em checks no código. Exemplos:
>
> - `if (typeof x === 'string')` → dentro, `x` é `string`.
> - `if ('field' in obj)` → dentro, `obj` tem `field`.
> - `if (x instanceof Error)` → dentro, `x` é `Error`.
> - Discriminated unions + check do discriminador.
>
> Senior bom escreve código de forma que o TS **narrow-se naturalmente** — sem `as`, sem `!`, sem `any`. Cast só em fronteiras reais (ex: deserializar JSON).

**Sinais de alerta em code review.**

- `any` explícito ou implícito (`no-implicit-any` no tsconfig ajuda a pegar).
- `as` em mais de 1–2 pontos do arquivo.
- Types duplicados (`UserDTO` no frontend, `User` no form, `UserData` no list) — consolide ou derive (`Pick<User, 'id' | 'name'>`).
- `!` (non-null assertion) espalhado — se é sempre não-nulo, por que o tipo diz que pode ser null?

**Fonte**: [1]

### 23. Silenciar `exhaustive-deps`

**O problema.** `react-hooks/exhaustive-deps` é o **principal linter de corretude** pra hooks. Ele garante que toda variável usada dentro do effect/callback está declarada nas deps — o que evita [[#26. Deps faltando → stale values|stale values]].

Quando aparece warning, o instinto ruim é silenciar:

```tsx
// ruim — escondendo bug
useEffect(() => {
  doStuff(value); // usa `value`, mas...
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, []); // ...não declarou — effect vai usar `value` congelado no momento do mount
```

Isso cria **closure stale**: `value` vale o que valia no primeiro render para sempre. Quando prop mudar, effect continua chamando `doStuff` com o valor antigo.

**Soluções reais, em ordem de preferência.**

**1. Incluir a dep (resposta óbvia — o linter está certo).**

```tsx
useEffect(() => {
  doStuff(value);
}, [value]);
```

**2. Extrair pra `useCallback` (se o problema é a função no deps).**

```tsx
const stableFn = useCallback(() => doStuff(value), [value]);
useEffect(() => {
  stableFn();
}, [stableFn]);
```

**3. Refatorar (se incluir a dep causa loop ou comportamento errado).**

Significa que seu effect não é só "reagir a mudanças" — há lógica de evento misturada (ver [[#30. Lógica de evento dentro de Effect]]).

**4. `useRef` (se o valor não deve triggar re-execução).**

```tsx
const valueRef = useRef(value);
useEffect(() => {
  valueRef.current = value;
});

useEffect(() => {
  doStuff(valueRef.current); // usa valor mais recente, mas não reage a mudança
}, []); // deps vazios de propósito — ref não precisa estar aqui
```

**5. `useEffectEvent` (React 19.2+).**

```tsx
// pra lógica não-reativa que deve ver valores atuais
const onUpdate = useEffectEvent(() => doStuff(value));
useEffect(() => {
  onUpdate();
}, []); // sem deps; onUpdate sempre vê `value` atual
```

> [!warning] `eslint-disable` é confissão
> Toda vez que você escreve `// eslint-disable-next-line react-hooks/exhaustive-deps`, está admitindo: "não sei explicar corretamente pro React quando esse effect deve rodar". Ou ignore com **comentário explicando por quê** (raramente válido), ou refatore.

**Fonte**: [1]

### 24. Hook quando função pura bastaria

**O problema.** Hook vem com regras: só pode ser chamado no topo de componente ou outro hook, não dentro de loops/if/callbacks. Se seu "hook" não usa `useState`/`useEffect`/`useContext`/`useRef`/outros hooks, **não é hook** — é função pura mascarada, e você paga o custo de regras sem ganhar nada.

```tsx
// ruim — "hook" que não usa hooks
function useFormatPrice(value: number, currency: string) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency,
  }).format(value);
}

// uso
function Product({ price }) {
  const formatted = useFormatPrice(price, 'BRL'); // só roda no topo!
  if (price > 100) {
    // não posso chamar useFormatPrice aqui ← regras de hooks
  }
  return <span>{formatted}</span>;
}
```

**Solução — função pura.**

```tsx
// bom — função pura, chamável em qualquer lugar
function formatPrice(value: number, currency: string) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency,
  }).format(value);
}

function Product({ price }) {
  // chama onde precisar, incluindo dentro de condicional
  return <span>{price > 100 ? formatPrice(price, 'BRL') : 'Barato'}</span>;
}
```

**Regra de decisão.**

- Usa `useState`/`useEffect`/`useRef`/`useContext`/outro hook? → É hook. Nome começa com `use`.
- Só processa entrada e retorna saída? → Função pura. Nome sem `use`.

**Quando um "hook" sem hooks ainda vale.** Nunca. Se você sente que faz sentido, provavelmente está preparando pra adicionar `useMemo` mais tarde — mas adicione quando precisar, não profilaticamente.

**Fonte**: [1]

### 25. Deps instáveis (objetos/funções criados no render)

**O problema.** Variação do #18 e #20. Se você coloca no array de deps algo que é **recriado a cada render**, o effect/callback/memo roda **todo render** — como se as deps fossem `[Math.random()]`.

```tsx
// ruim — options é objeto novo cada render → effect roda sempre
function Widget({ userId }: { userId: string }) {
  const options = { userId, includeAvatar: true };
  //              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  //              novo objeto em cada render

  useEffect(() => {
    api.fetch(options);
  }, [options]); // ← effect roda a cada render; você queria roda só quando userId mudar
}
```

**Soluções.**

**1. Memoizar o objeto.**

```tsx
const options = useMemo(
  () => ({ userId, includeAvatar: true }),
  [userId],
);
useEffect(() => { api.fetch(options); }, [options]);
```

**2. Melhor — passar primitivos no array de deps.**

```tsx
useEffect(() => {
  api.fetch({ userId, includeAvatar: true });
}, [userId]); // só primitivo — sempre estável
```

Essa é a **solução preferida** quando o objeto é construído dentro do effect. Os valores primitivos que compõem o objeto são o que realmente importa.

**3. Envolver função em `useCallback`.**

```tsx
const fetchData = useCallback(() => api.fetch({ userId }), [userId]);
useEffect(() => { fetchData(); }, [fetchData]);
```

**Fonte**: [3]

### 26. Deps faltando → stale values

**O problema.** Omitir prop/state do array de deps parece simplificar — "esse effect só precisa rodar no mount" — mas cria **closure stale**: o effect/callback captura os valores do momento em que foi criado, e nunca vê as atualizações.

```tsx
// ruim — closure com `userId` congelado no primeiro render
function UserProfile({ userId }) {
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, []); // ← userId faltando!

  // quando userId mudar (nova rota, por exemplo), effect não roda de novo
  // — usuário continua vendo dados do primeiro userId
}
```

**Por que é traiçoeiro.** O bug **não aparece no desenvolvimento inicial** — quando userId não muda, funciona bem. Aparece meses depois, quando alguém implementa navegação interna pra perfis de outros usuários.

**Solução.**

**1. Confie no linter.** `react-hooks/exhaustive-deps` pega isso. Se não ativou, ative agora.

```tsx
// bom — deps corretas
useEffect(() => {
  fetchUser(userId).then(setUser);
}, [userId]);
```

**2. Se realmente quer "só no mount, independente de props", reconsidere.** Geralmente significa que o componente não deveria re-renderizar para outro `userId`, mas sim **remount** — use `key`:

```tsx
<UserProfile userId={userId} key={userId} />
```

**3. `useRef` + efeito de sincronização** (quando quer valor atual sem disparar re-execução — raro e delicado, ver #23).

> [!tip] Regra de três segundos
> Toda vez que quiser omitir uma dep, pare 3 segundos e pergunte: "O que acontece quando essa variável muda?" Se a resposta é "nada deveria acontecer", você provavelmente quer `useRef` (ou refatorar). Se a resposta é "o effect deveria rodar de novo", declare a dep.

**Fonte**: [3]

---

## Cap. 7 — Listas e keys

### 27. Usar `index` como `key`

**O problema.** Quando você renderiza uma lista, React usa `key` pra saber **qual JSX corresponde a qual linha da lista entre renders**. Isso permite preservar estado interno, animações, foco de input, etc.

Quando você usa `index` como key, qualquer mudança na ordem da lista (remover do meio, reordenar, filtrar) faz o React associar o JSX errado às linhas erradas.

**O bug clássico.** Lista com inputs internos por linha:

```tsx
// ruim — index como key
function List({ items }: { items: string[] }) {
  return (
    <ul>
      {items.map((item, i) => (
        <Row key={i} label={item} />
      ))}
    </ul>
  );
}

function Row({ label }: { label: string }) {
  const [note, setNote] = useState('');
  return (
    <li>
      {label} <input value={note} onChange={e => setNote(e.target.value)} />
    </li>
  );
}
```

Cenário que bomba:

1. Lista é `['A', 'B', 'C']`. Usuário digita "obs A" no input da linha A, "obs B" na linha B.
2. Usuário deleta a linha A. Lista vira `['B', 'C']`.
3. **O que acontece**: React vê `key=0` → ainda existe (antes era A, agora é B). React pensa "ah, a linha 0 continua aí, só mudou o label". Reusa o `<Row>` antigo (que tinha `note='obs A'`), só troca o label pra `'B'`.
4. Usuário vê: linha B com note "obs A". Linha C com note "obs B". **Estado vazou entre linhas.**

**Solução — ID estável.**

```tsx
// bom — ID da entidade
items.map(item => <Row key={item.id} label={item.label} />);
```

Agora, quando você remove o item com id="a", React vê `key="a"` sumir — desmonta aquela `<Row>` inteira, incluindo o state. Linhas remanescentes continuam identificadas por `"b"` e `"c"`, state preservado corretamente.

**E se a API não retornar ID?**

- **Sempre tente adicionar no backend.** É o lugar certo.
- Se não for possível, gere ID estável **no ponto de entrada** do dado no sistema (assim que chega no frontend):

  ```tsx
  const withIds = data.map(item => ({ ...item, id: crypto.randomUUID() }));
  // guarde withIds no state — IDs persistem entre renders
  ```

- **Nunca gere ID no render.** `items.map(item => <Row key={crypto.randomUUID()} />)` gera ID novo a cada render — **pior** que index, porque toda linha remonta toda vez.

> [!info]- Quando `index` como key é aceitável
> Quando a lista é **genuinamente estática** e **não tem state interno por item**:
>
> - Lista de opções de menu que nunca muda de ordem.
> - Lista de labels sem interação.
> - Lista de ícones decorativos.
>
> Mesmo assim, ID estável é melhor — só é indiferente quando garantidamente não vai dar problema. Como garantia "nunca" é difícil no mundo real, o hábito correto é **sempre usar ID estável**.

**Nunca use `Math.random()` nem `Date.now()` como key.** Pelo mesmo motivo de `crypto.randomUUID()` no render: geram valor novo a cada render, forçando desmontagem/remontagem constantes. Animações piscam, foco de input some, performance despenca.

**Fonte**: [1][6]

---

## Cap. 8 — useEffect, o abismo

**Regra geral.** `useEffect` deve ser **exceção, não default**. Existe pra sincronizar React com **sistemas externos** (DOM manual, APIs de browser, sockets, listeners, libs de terceiros). Pra tudo mais — derivar dados, reagir a eventos de usuário, passar dados pra cima — há caminho melhor.

> [!info]- Quando `useEffect` é a ferramenta certa
>
> - **Sincronizar com APIs do browser**: `IntersectionObserver`, `ResizeObserver`, `window.addEventListener`.
> - **Subscribir em stores externos**: WebSocket, Firebase, Redux externo (mas `useSyncExternalStore` costuma ser melhor).
> - **Integrar libs não-React**: inicializar um mapa (Mapbox), chart (D3), editor (Monaco, Quill).
> - **Efeitos colaterais depois do paint**: analytics "página vista", focar primeiro input.
>
> **Não é ferramenta certa pra**: derivar dados, reagir a clique/input, notificar o pai, transformar props em state.

### 28. Transformar dados em Effect em vez de derivar no render

**O problema.** Clássico. Mesmo bug do [[#12. Guardar valor derivado em state]], mas com a armadilha extra do effect: cria **render duplo** (render inicial com valor velho, effect atualiza, render de novo).

```tsx
// ruim — effect só pra derivar
function Form({ firstName, lastName }) {
  const [fullName, setFullName] = useState('');

  useEffect(() => {
    setFullName(firstName + ' ' + lastName);
  }, [firstName, lastName]);
  // fluxo: props mudam → render (fullName velho) → effect → setState → render de novo

  return <h1>{fullName}</h1>;
}

// bom — cálculo no render, um render só
function Form({ firstName, lastName }) {
  const fullName = firstName + ' ' + lastName;
  return <h1>{fullName}</h1>;
}
```

Se o cálculo é caro, `useMemo` (ver [[#12. Guardar valor derivado em state]]).

**Fonte**: [2]

### 29. Encadear Effects (cascatas de setState)

**O problema.** Cada effect dispara o próximo por setState — e você tem **N renders sequenciais** pra uma única interação. Código fica frágil (ordem de effects importa), testes ficam lentos, React precisa reconciliar árvore N vezes.

```tsx
// ruim — cascata de renders
function Game({ card }) {
  const [goldCount, setGoldCount] = useState(0);
  const [round, setRound] = useState(1);
  const [isGameOver, setIsGameOver] = useState(false);

  useEffect(() => { setGoldCount(c => c + 1); }, [card]);        // render 2
  useEffect(() => { setRound(r => r + 1); }, [goldCount]);       // render 3
  useEffect(() => {
    if (round > 5) setIsGameOver(true);
  }, [round]);                                                    // render 4
}
```

**Solução — calcule tudo no handler do evento original.**

```tsx
// bom — uma função, um render
function Game() {
  const [state, setState] = useState({
    goldCount: 0, round: 1, isGameOver: false,
  });

  function playCard(card: Card) {
    setState(prev => {
      const goldCount = prev.goldCount + 1;
      const round = prev.round + 1;
      const isGameOver = round > 5;
      return { goldCount, round, isGameOver };
    });
  }
}
```

Alternativamente, `useReducer` pra lógica mais complexa:

```tsx
function gameReducer(state: GameState, action: GameAction) {
  switch (action.type) {
    case 'PLAY_CARD': {
      const goldCount = state.goldCount + 1;
      const round = state.round + 1;
      return { ...state, goldCount, round, isGameOver: round > 5 };
    }
  }
}
```

> [!tip] Pergunta diagnóstica
> Se você tem `useEffect(() => setX(...), [y])` e `useEffect(() => setZ(...), [x])`, **pare**. Isso é cascata. Mova pra um handler ou reducer.

**Fonte**: [2]

### 30. Lógica de evento dentro de Effect

**O problema.** Effects rodam **quando as deps mudam** — mas não sabem _o que_ causou a mudança. Se você coloca um "side effect de ação" (toast, analytics, som) num effect, ele dispara em situações que não deveriam ser consideradas a "ação":

- Primeira carga da página (se a condição já é verdadeira).
- Re-render por motivo não relacionado.
- Hot-reload em desenvolvimento.
- Strict Mode (em dev, React roda effects duas vezes propositalmente).

```tsx
// ruim — toast dispara mesmo quando a página carrega com o item já no carrinho
function Product({ product }) {
  useEffect(() => {
    if (product.isInCart) {
      showToast(`Added ${product.name} to cart!`);
    }
  }, [product.isInCart]);
}
```

Usuário recarrega a página com o item já no carrinho → toast inesperado.

**Solução — coloque a lógica no handler que _causou_ a mudança.**

```tsx
// bom — toast só dispara quando o usuário clica
function Product({ product }) {
  function handleAddToCart() {
    addToCart(product);
    showToast(`Added ${product.name} to cart!`);
  }

  return <button onClick={handleAddToCart}>Add to cart</button>;
}
```

**Regra.** Effects reagem a **dados**; handlers reagem a **ações**. Se a lógica só faz sentido quando o usuário clicou/submeteu/digitou, ela pertence ao handler.

**Fonte**: [2][3]

### 31. Inicialização global dentro de Effect

**O problema.** Você precisa inicializar uma lib (SDK de analytics, Sentry, Mermaid, Facebook Pixel) **uma vez**, quando o app carrega. Cai no instinto:

```tsx
// ruim — vários problemas
function App() {
  useEffect(() => {
    initFacebookPixel();
    loadFromLocalStorage();
    checkAuthToken();
  }, []);

  return /* ... */;
}
```

Problemas:

- **Strict Mode roda 2x em dev**, então `initFacebookPixel()` é chamado duas vezes. Se a função não é idempotente, bugs em dev.
- Se o componente `<App>` remontar (em testes, HMR, rotas), init repete.
- Roda **depois** do primeiro paint — auth check chega tarde, conteúdo "pisca" entre estados.

**Solução 1 — module-level init (roda uma vez quando o módulo é importado).**

```tsx
// bom — roda uma vez, na carga do bundle
if (typeof window !== 'undefined') {
  initFacebookPixel();
  checkAuthToken();
}

export function App() {
  return /* ... */;
}
```

> [!info]- Por que o `typeof window !== 'undefined'`?
> Se o app tem SSR (Next.js, Remix), o arquivo também executa no servidor, onde `window` não existe. O guard evita crash em server-side. Em SPA puro (Vite + React Router client-side), não é necessário.

**Solução 2 — flag de guarda.**

```tsx
let initialized = false;
function initOnce() {
  if (initialized) return;
  initialized = true;
  initFacebookPixel();
  checkAuthToken();
}

function App() {
  useEffect(() => { initOnce(); }, []);
  return /* ... */;
}
```

**Solução 3 — em meta-frameworks, use o arquivo raiz.** Next.js tem `app/layout.tsx`; Remix tem `root.tsx`; Vite+React Router tem `main.tsx`. Inits globais moram no _topo_ do entry point.

**Fonte**: [2]

### 32. Notificar pai via Effect

**O problema.** Componente filho tem state interno (`isOn`) e precisa avisar o pai quando muda. Instinto ruim:

```tsx
// ruim — effect atualiza o pai
function Toggle({ onChange }: { onChange: (v: boolean) => void }) {
  const [isOn, setIsOn] = useState(false);

  useEffect(() => {
    onChange(isOn);
  }, [isOn]);
  // problemas:
  // - dispara em mount (avisa o pai que está "false" sem usuário fazer nada)
  // - render do filho acontece ANTES do pai saber
  // - se pai re-renderizar baseado em isOn, há pass extra

  return <button onClick={() => setIsOn(v => !v)}>{isOn ? 'On' : 'Off'}</button>;
}
```

**Solução 1 — atualize ambos no mesmo handler.**

```tsx
// bom — sincronia imediata
function Toggle({ onChange }: { onChange: (v: boolean) => void }) {
  const [isOn, setIsOn] = useState(false);

  function toggle() {
    const next = !isOn;
    setIsOn(next);
    onChange(next); // mesmo evento → mesmo render
  }

  return <button onClick={toggle}>{isOn ? 'On' : 'Off'}</button>;
}
```

**Solução 2 (melhor) — faça o componente _controlled_.**

```tsx
// bom — pai é dono do state, sem duplicação
function Toggle({ isOn, onChange }: { isOn: boolean; onChange: (v: boolean) => void }) {
  return <button onClick={() => onChange(!isOn)}>{isOn ? 'On' : 'Off'}</button>;
}

function Parent() {
  const [isOn, setIsOn] = useState(false);
  return <Toggle isOn={isOn} onChange={setIsOn} />;
}
```

Componentes controlled são mais previsíveis, testáveis, compostos. Use quando o state é relevante pro pai.

**Fonte**: [2]

### 33. Race conditions em fetch

**O problema.** Effects disparam fetches async. Se a dep muda rápido (usuário digitando busca), múltiplos fetches ficam em voo. A **ordem de resposta não é garantida** — resposta do query antigo pode chegar _depois_ da resposta do query novo, sobrescrevendo com dados desatualizados.

```tsx
// ruim — race condition
function SearchResults({ query }: { query: string }) {
  const [results, setResults] = useState<Result[]>([]);

  useEffect(() => {
    fetchResults(query).then(setResults);
    // usuário digita "re" → fetch A começa
    // usuário digita "rea" → fetch B começa
    // fetch B responde primeiro (rápido) → results = B
    // fetch A responde depois (lento) → results = A ← bug: mostra resultado do query antigo
  }, [query]);
}
```

**Solução 1 — flag `ignore`.**

```tsx
// bom — resposta velha é ignorada se o effect já foi "limpado"
useEffect(() => {
  let ignore = false;

  fetchResults(query).then(data => {
    if (!ignore) setResults(data);
  });

  return () => {
    ignore = true; // quando a dep mudar ou componente desmontar
  };
}, [query]);
```

**Solução 2 — `AbortController` (melhor: cancela a requisição HTTP).**

```tsx
useEffect(() => {
  const controller = new AbortController();

  fetch(`/api/search?q=${query}`, { signal: controller.signal })
    .then(r => r.json())
    .then(setResults)
    .catch(err => {
      if (err.name !== 'AbortError') throw err;
    });

  return () => controller.abort();
}, [query]);
```

**Solução 3 (recomendada em prod) — use [[React Query|TanStack Query]] ou SWR.**

```tsx
// bom — lib lida com tudo: dedup, cache, cancelamento, revalidação
function SearchResults({ query }: { query: string }) {
  const { data } = useQuery({
    queryKey: ['search', query],
    queryFn: () => fetchResults(query),
  });
  return <Results data={data} />;
}
```

Race conditions são _resolvidas_ (não mitigadas) por libs de data fetching. Ver [[#37. Camada de data fetching caseira]].

**Fonte**: [2][3]

### 34. Falta de cleanup (timers, listeners, subscriptions)

**O problema.** Recursos criados em effects (listeners, timers, sockets, subscriptions) **persistem depois do componente desmontar** se você não limpa. Consequências:

- **Memory leak.** Closures vivas mantendo referência a props/state de componentes que deveriam ter ido embora.
- **Handlers disparando no vazio.** `resize` chama `setState` em componente desmontado → warning do React + possível bug.
- **Conexões abertas.** WebSocket fica ativo, consumindo banda, gerando eventos pra nada.

```tsx
// ruim — listener nunca removido
useEffect(() => {
  window.addEventListener('resize', handleResize);
}, []);
```

**Solução — toda criação de recurso em effect precisa da função de cleanup.**

```tsx
// bom — cleanup removido quando componente desmonta ou deps mudam
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

**Padrões de cleanup.**

```tsx
// timer
useEffect(() => {
  const id = setTimeout(() => {...}, 1000);
  return () => clearTimeout(id);
}, []);

// interval
useEffect(() => {
  const id = setInterval(() => {...}, 1000);
  return () => clearInterval(id);
}, []);

// subscription (ex: store externo, Firebase)
useEffect(() => {
  const unsubscribe = store.subscribe(callback);
  return unsubscribe; // já é função, só retornar
}, []);

// observer
useEffect(() => {
  const observer = new IntersectionObserver(callback);
  observer.observe(ref.current);
  return () => observer.disconnect();
}, []);

// WebSocket
useEffect(() => {
  const ws = new WebSocket(URL);
  return () => ws.close();
}, []);
```

> [!tip] Regra simples
> Se o effect **abre/cria/registra** algo, ele **fecha/destrói/remove** no cleanup. Sempre.

**Fonte**: [3]

### 35. `useEffect` onde `useLayoutEffect` deveria

**O problema.** `useEffect` roda **depois do browser pintar**. `useLayoutEffect` roda **antes do pintar**, sincronamente após mutações do DOM.

Se você precisa **ler layout** (tamanho, posição) ou **escrever estilo/DOM baseado em layout**, `useEffect` causa **flicker**: o browser pinta o estado "errado", depois o effect ajusta, e pinta de novo.

```tsx
// ruim — tooltip piscando
function Tooltip({ target, children }) {
  const ref = useRef<HTMLDivElement>(null);
  const [pos, setPos] = useState({ top: 0, left: 0 });

  useEffect(() => {
    // 1. browser pinta tooltip em (0, 0) ← flicker
    const rect = target.getBoundingClientRect();
    setPos({ top: rect.bottom, left: rect.left });
    // 2. browser pinta tooltip na posição correta
  }, [target]);

  return <div ref={ref} style={pos}>{children}</div>;
}

// bom — sem flicker, ajuste pré-paint
function Tooltip({ target, children }) {
  const ref = useRef<HTMLDivElement>(null);
  const [pos, setPos] = useState({ top: 0, left: 0 });

  useLayoutEffect(() => {
    const rect = target.getBoundingClientRect();
    setPos({ top: rect.bottom, left: rect.left });
  }, [target]);

  return <div ref={ref} style={pos}>{children}</div>;
}
```

**Quando usar o quê.**

| Cenário                                            | Hook                   |
| -------------------------------------------------- | ---------------------- |
| Fetch, analytics, timers, listeners                | `useEffect`            |
| Medir DOM (`getBoundingClientRect`, `offsetWidth`) | `useLayoutEffect`      |
| Ajustar estilo/posição baseado em layout           | `useLayoutEffect`      |
| Subscribir em store externo                        | `useSyncExternalStore` |
| Scroll position restore                            | `useLayoutEffect`      |

**Cuidado — `useLayoutEffect` bloqueia o paint.** Código lento dentro dele faz a UI travar (usuário espera pelo ajuste antes de ver qualquer pixel). Use só pro necessário; tudo que puder ficar em `useEffect`, fique.

> [!info]- `useSyncExternalStore` — quando usar
> Hook dedicado a subscribir em **stores externos** (fora do React). Resolve problemas que `useEffect` tem com concurrent rendering (suspense, transições). Libs modernas (Zustand, Redux) já usam por baixo — você só escreve manual se estiver integrando store próprio/legado.

**Fonte**: [3]

### 36. Loop infinito por deps mal configuradas

**O problema.** Effect que chama `setState` + deps mal configuradas = loop infinito. CPU a 100%, browser travando, console cuspindo warnings.

**Causa 1 — sem array de deps.**

```tsx
// ruim — effect roda TODO render → setState → novo render → loop
useEffect(() => {
  setCount(c => c + 1);
});
```

Sem deps, o effect roda após cada render. Effect chama setState, dispara novo render, roda de novo.

**Causa 2 — objeto/função inline em deps.**

```tsx
// ruim — options é objeto novo a cada render → deps "mudam" sempre → loop
function Widget({ userId }: { userId: string }) {
  const options = { userId };
  useEffect(() => {
    fetch('/api', options).then(setData);
  }, [options]);
}
```

`options` é `{ userId: 'abc' }` no render 1, `{ userId: 'abc' }` no render 2 — **mesmo conteúdo, referência diferente**. React compara com `Object.is`, detecta "mudou", roda effect, que chama `setData`, dispara render, `options` é novo objeto, effect roda de novo... ver [[#25. Deps instáveis (objetos/funções criados no render)]].

**Causa 3 — setState sem updater function, dep faltando.**

```tsx
// ruim — precisa de count na dep, mas setar count ativa o effect
useEffect(() => {
  setCount(count + 1);
}, []); // linter avisa, você inclui count no deps... e entra em loop
```

**Soluções.**

1. **Se o effect só deve rodar no mount**: `[]` (vazio) e certifique-se que os valores lidos dentro não mudam (ou usar updater function).
2. **Se o effect deve reagir a algo**: declare `[algo]`, e esse algo deve ser **estável** (primitivo ou memoizado).
3. **setState com updater**: `setCount(c => c + 1)` em vez de `setCount(count + 1)` — não precisa de `count` na dep.
4. **Objetos em dep**: memoize com `useMemo`, ou passe só primitivos.

> [!warning] Se o browser travou no dev
> Provavelmente é loop de effect. Comente os `useEffect`s recentes, destrave, diagnostique um por um.

**Fonte**: [3]

---

## Cap. 9 — Data fetching, erros e estados de UI

### 37. Camada de data fetching caseira

**O problema.** "Vou só escrever um wrapper em `fetch`." Seis meses depois, você tem 600 linhas de código lidando com:

- Retry com backoff exponencial
- Deduplicação (2 componentes pedindo o mesmo endpoint ao mesmo tempo)
- Cache (não repetir fetch se dado ainda é fresco)
- Revalidação (refetch quando janela volta ao foco, em intervalos, em navegação)
- Cancelamento de fetch anterior quando o novo começa
- Loading states, error states
- Infinite scroll / paginação
- Optimistic updates em mutations
- Invalidação de cache em mutations
- SSR / streaming

É **projeto por si só**, com tests, edge cases, regressões. E você vai fazer mal — porque não é o foco do produto.

**Solução — use lib madura.**

**[[React Query|TanStack Query]]** (`@tanstack/react-query`) — padrão de facto pra client-side.

```tsx
// queries
function Users() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(r => r.json()),
    staleTime: 5 * 60_000, // fresh por 5min
  });

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorState error={error} />;
  return <UserList users={data} />;
}

// mutations com invalidação
function EditUser() {
  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: (user: User) => fetch('/api/users', { method: 'PUT', body: JSON.stringify(user) }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] }); // re-fetch lista
    },
  });
  return <button onClick={() => mutation.mutate(user)}>Save</button>;
}
```

**SWR** (`swr`) — mais leve, filosofia "stale-while-revalidate" (mostra cache enquanto revalida).

**Nativo de meta-framework.**

- **Next.js App Router**: `fetch` server-side com cache integrado, Server Actions pra mutations.
- **Remix / React Router 7**: `loader`/`action` pra dados e mutations.
- **TanStack Start**: loaders + queries integrados.

Pra apps SSR modernos, preferir o mecanismo do framework — já lida com caching, streaming, hydration.

> [!tip] Quando `fetch` puro ainda serve
> Scripts, protótipos, fetches únicos sem interação (fetch-and-forget). Não adicione React Query pra um `fetch()` que roda uma vez no mount sem reuso. Mas assim que houver 2+ consumidores do mesmo endpoint, ou necessidade de refetch, migre.

**Fonte**: [1][4]

### 38. Zero error boundaries

**O problema.** JavaScript é dinâmico — um `undefined.map()` ou `null.name` em qualquer componente crash o React. Sem error boundaries, o crash **derruba a árvore inteira** e o usuário vê tela branca. Sem telemetria, você nem fica sabendo.

Error boundaries são componentes especiais que **capturam erros em renders de filhos** e permitem mostrar fallback.

```tsx
// ruim — um bug na tabela derruba o app todo
function App() {
  return (
    <Layout>
      <Dashboard />        {/* se isso quebrar... */}
      <UserTable />        {/* ...tudo desaparece */}
      <Sidebar />
    </Layout>
  );
}

// bom — isolamento por seção
function App() {
  return (
    <Layout>
      <ErrorBoundary fallback={<DashboardError />}>
        <Dashboard />
      </ErrorBoundary>

      <ErrorBoundary fallback={<TableError />}>
        <UserTable />
      </ErrorBoundary>

      <ErrorBoundary fallback={<SidebarError />}>
        <Sidebar />
      </ErrorBoundary>
    </Layout>
  );
}
```

Agora, se a `UserTable` crashar, o resto do app continua funcional.

**Onde colocar error boundaries.**

- **Raiz do app** — fallback final pra erros catastróficos.
- **Por rota** — erro em uma página não derruba o resto.
- **Por seção relevante** — widgets independentes (dashboard com múltiplos cards).
- **Volta de recursos pesados** — um gráfico que depende de dados opcionais.

**Implementação — use a lib, não escreva do zero.**

```tsx
import { ErrorBoundary } from 'react-error-boundary';

<ErrorBoundary
  FallbackComponent={ErrorFallback}
  onError={(error, info) => logToSentry(error, info)}
  onReset={() => queryClient.invalidateQueries()}
>
  <MyComponent />
</ErrorBoundary>;
```

**Error boundaries não pegam tudo.** Não capturam: erros em event handlers, em effects async, em setTimeout, em código fora do React. Pra esses, `try/catch` tradicional + log pra telemetria.

> [!info]- Por que error boundaries são classes?
> Historicamente, React só tinha API de `componentDidCatch` em classes. Hoje existe a hook `useErrorBoundary` em libs como `react-error-boundary`, mas por baixo ainda é classe (limitação do React até 19).

**Fonte**: [1]

### 39. `catch {}` vazio

**O problema.** Bloco catch sem conteúdo (ou só com `console.log`). O erro é **engolido** — não loga, não notifica o usuário, não vai pra telemetria. Quando o bug aparece em prod, não tem rastro.

```tsx
// ruim — erro some
try {
  const data = await fetchData();
  setState(data);
} catch {
  // silêncio
}
```

**Por que acontece.**

- Dev queria suprimir o erro em dev, esqueceu de voltar.
- Erro "acontece às vezes" e o dev não sabe de onde vem, então "esconde" pra continuar.
- Copy-paste de exemplo de internet.

**Consequências.**

- **Bugs silenciosos.** Estado inconsistente, UI estranha, ninguém sabe o porquê.
- **Dificuldade de reproduzir.** Sem stack trace, sem contexto.
- **Confiança na telemetria.** Se você não loga, não aparece no Sentry/Datadog — cria falsa sensação de "está tudo bem".

**Solução mínima — loga com contexto.**

```tsx
try {
  const data = await fetchData();
  setState(data);
} catch (error) {
  console.error('Failed to fetch user data', { userId, error });
  throw error; // se quer propagar pro error boundary
}
```

**Solução ideal — telemetria + UX.**

```tsx
try {
  const data = await fetchData();
  setState(data);
} catch (error) {
  Sentry.captureException(error, {
    tags: { feature: 'user-fetch' },
    extra: { userId },
  });
  toast.error('Não foi possível carregar. Tente novamente.');
  setErrorState(error);
}
```

**Quando catch vazio é ok — nunca.** Se você genuinamente quer ignorar, **comente o porquê**:

```tsx
try {
  analytics.track('pageview');
} catch {
  // ignorar — analytics não deve quebrar a página, e já temos fallback no provider
}
```

Mas isso é raro. Em 95% dos casos, você quer saber que deu erro.

**Fonte**: [1]

### 40. Sem loading / error / empty states

**O problema.** Componente que faz fetch mas não cobre os quatro estados possíveis:

1. **Loading** — dados ainda não chegaram.
2. **Error** — fetch falhou.
3. **Empty** — fetch OK, mas resultado é vazio.
4. **Success** — dados chegaram e existem.

Sintomas comuns de cobertura incompleta:

- **Tela branca** em fetch lento (sem loading) — usuário acha que app travou.
- **Tela branca ou crash** em falha (sem error) — usuário perdido.
- **"Nenhum resultado"** mostrado **durante** loading (sem distinguir loading de empty) — usuário clica em "nova busca" achando que não funcionou.

**Padrão mínimo — early returns por estado.**

```tsx
function Users() {
  const { data, isLoading, error } = useQuery({ queryKey: ['users'], queryFn: fetchUsers });

  if (isLoading) return <UsersSkeleton />;
  if (error) return <UsersError error={error} onRetry={() => refetch()} />;
  if (!data || data.length === 0) return <UsersEmpty onCreate={openCreateModal} />;
  return <UsersList users={data} />;
}
```

**Cada estado merece atenção.**

- **Loading** — **skeleton** (placeholder do layout final) é melhor que spinner genérico, porque sinaliza o _que_ está vindo.
- **Error** — mensagem humana + **ação** ("Tentar de novo", "Reportar"). Nunca jogar o stack trace na cara do usuário.
- **Empty** — visual distinto de loading. Idealmente com **call-to-action** ("Criar primeiro cliente").
- **Success** — o conteúdo.

**Teste com DevTools throttling.** No Chrome DevTools > Network > "Slow 3G", você vê o loading. Em dev-local o fetch é instantâneo e você nem percebe. Teste devagar uma vez por feature.

> [!info]- Stale-while-revalidate
> Padrão onde, em refetches subsequentes, você **mostra o dado antigo** enquanto atualiza em background. Evita flash de loading toda vez que o usuário navega de volta. Libs como SWR e React Query fazem isso por padrão.

**Fonte**: [1]

---

## Cap. 10 — Performance e bundle

> [!info]- Core Web Vitals — o vocabulário do capítulo
> Métricas que o Google (e usuários) cobram. Afetam SEO e percepção de qualidade.
>
> - **LCP** (Largest Contentful Paint): tempo até o maior elemento visível renderizar. Meta: < 2.5s.
> - **INP** (Interaction to Next Paint): tempo entre interação (click/input) e próximo paint. Meta: < 200ms.
> - **CLS** (Cumulative Layout Shift): quanto conteúdo "pula" durante carregamento. Meta: < 0.1.
> - **FCP** (First Contentful Paint): primeira renderização de qualquer conteúdo. Meta: < 1.8s.
> - **TTFB** (Time to First Byte): tempo até primeiro byte de resposta do server. Meta: < 0.8s.
>
> Medir com [PageSpeed Insights](https://pagespeed.web.dev/), Chrome DevTools > Lighthouse, ou `web-vitals` npm package em prod.

### 41. Sem code splitting / lazy routes

**O problema.** Bundle único de 2MB no primeiro load. Usuário só quer ver a página de login, mas o browser baixa código de `/admin/reports` + `/checkout` + dependências gigantes que nem são usadas ainda.

Consequências:

- **LCP ruim.** Quanto maior o JS, mais tempo até a página ser interativa.
- **INP ruim.** Parse + execute de JS bloqueia o main thread.
- **Banda/dados do usuário.** Mobile em 4G pagando por código que ele não vai usar.

**Solução — dividir o bundle em chunks carregados sob demanda.**

**Por rota (80% do ganho):**

```tsx
// ruim — tudo importado estaticamente, tudo no bundle inicial
import Home from './pages/Home';
import Admin from './pages/Admin';
import Checkout from './pages/Checkout';

// bom — lazy load por rota
import { lazy, Suspense } from 'react';

const Home = lazy(() => import('./pages/Home'));
const Admin = lazy(() => import('./pages/Admin'));
const Checkout = lazy(() => import('./pages/Checkout'));

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/admin" element={<Admin />} />
        <Route path="/checkout" element={<Checkout />} />
      </Routes>
    </Suspense>
  );
}
```

Cada `lazy()` gera um **chunk separado**, baixado só quando a rota é visitada.

**Por componente pesado:**

```tsx
// editor rich-text de 300KB — carregar só quando o usuário abre o modal
const RichTextEditor = lazy(() => import('./RichTextEditor'));

function Page() {
  const [editing, setEditing] = useState(false);
  return (
    <>
      <button onClick={() => setEditing(true)}>Editar</button>
      {editing && (
        <Suspense fallback={<Spinner />}>
          <RichTextEditor />
        </Suspense>
      )}
    </>
  );
}
```

**Ferramentas pra descobrir o que pesa.**

- **`rollup-plugin-visualizer`** (Vite) — árvore visual do bundle.
- **`webpack-bundle-analyzer`** — equivalente pra Webpack.
- **Chrome DevTools > Coverage** — mostra quanto % do JS baixado é **realmente executado** numa página.

**Meta-frameworks.** Next.js, Remix e similares fazem code splitting por rota **automaticamente**. Se você está usando, já tem o básico.

> [!tip] Medindo impacto
> Antes: rode Lighthouse, anote LCP, tamanho do bundle inicial. Implemente splitting. Meça de novo. Se reduziu pouco, é porque o bundle não era o gargalo — foque em outra coisa.

**Fonte**: [4]

### 42. Imagens não otimizadas

**O problema.** PNG/JPG gigantes (1920x1080 do designer) exibidos como thumbnails de 100x100. Sem `loading="lazy"`, o browser baixa **tudo** no load. Sem formato moderno, arquivos 3–5x maiores que o necessário.

Consequências: LCP alto (imagem grande bloqueia "conteúdo principal"), banda desperdiçada, bateria (mobile).

**Solução — checklist.**

**1. Formatos modernos.**

- **WebP**: ~30% menor que JPG, suporte universal desde 2020.
- **AVIF**: ~50% menor que JPG, suporte em ~95% dos browsers (2026).
- Fallback pra JPG/PNG só pra cobrir legado extremo.

**2. Responsive images.**

```html
<picture>
  <source srcset="hero-2000.avif 2000w, hero-1000.avif 1000w" type="image/avif" />
  <source srcset="hero-2000.webp 2000w, hero-1000.webp 1000w" type="image/webp" />
  <img
    src="hero-1000.jpg"
    srcset="hero-2000.jpg 2000w, hero-1000.jpg 1000w"
    sizes="(max-width: 768px) 100vw, 50vw"
    alt="..."
    width="1000"
    height="600"
  />
</picture>
```

Browser escolhe o melhor formato + tamanho baseado em viewport e DPR (retina).

**3. `loading="lazy"` pra off-screen.**

```html
<img src="..." loading="lazy" alt="..." />
```

Browser só baixa quando a imagem chega perto do viewport. **Não coloque `lazy` em hero image** (imagem acima do fold) — afeta LCP.

**4. Dimensões fixas (`width`, `height`) pra evitar CLS.** Ver [[#46. CLS alto por falta de reserva de espaço]].

**5. CDN de imagem.** Em vez de servir do seu backend, use serviço que otimiza on-the-fly:

- **Cloudinary, Imgix, ImageKit** — transformações por URL.
- **`next/image`** (Next.js), **`@unpic/react`** (framework-agnóstico) — componentes que integram com CDN.

**6. SVG pra ícones/logos.** Texto, escalável, leve — nunca PNG pra elementos vetoriais.

> [!info]- Por que AVIF > WebP > JPG?
> Compressão de imagem evolui por décadas. JPEG (1992) usa DCT; WebP (2010, baseado em VP8) adiciona predição; AVIF (2019, baseado em AV1) usa redes neurais + predição intra-frame avançada. Cada geração dá mais qualidade por byte.
>
> Trade-off: AVIF codifica mais devagar no servidor. CDNs modernas resolvem cacheando.

**Fonte**: [4]

### 43. Listas longas sem virtualização

**O problema.** Renderizar 10.000 linhas num `<table>` trava o navegador. Mesmo com React.memo, são 10.000 componentes no DOM — scroll fica laggy, INP ruim, memória alta.

O insight: **o usuário só vê ~20 linhas de cada vez**. Renderizar 10.000 é desperdício.

**Solução — virtualização.** Renderiza só as linhas visíveis no viewport (+ buffer). Quando scrollar, remove as que saíram e monta as que entraram.

**Libs recomendadas.**

- **[`@tanstack/react-virtual`](https://tanstack.com/virtual/)** — moderna, flexível, mantida pelo time do TanStack.
- **`react-window`** — mais simples, API enxuta.
- **`react-virtualized`** — legada, mais features mas maior.

**Exemplo com `@tanstack/react-virtual`:**

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function UserList({ users }: { users: User[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: users.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // altura em px de cada linha
    overscan: 5,            // renderiza 5 a mais fora de vista pra scroll suave
  });

  return (
    <div ref={parentRef} style={{ height: 600, overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize(), position: 'relative' }}>
        {virtualizer.getVirtualItems().map(item => (
          <div
            key={item.key}
            style={{
              position: 'absolute',
              top: item.start,
              height: item.size,
              width: '100%',
            }}
          >
            {users[item.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

**Quando virtualizar.**

- **~500 linhas ou mais** — threshold empírico; abaixo disso, React render é rápido o suficiente.
- **Linhas com DOM complexo** (imagens, inputs) — menor pode já justificar.
- **Mobile** — threshold ainda menor, devices mais fracos.

**Tradeoffs.**

- **Ctrl+F não encontra** o que não foi renderizado. Use busca própria.
- **Alturas variáveis** complicam — precisa re-medir on-the-fly (libs modernas lidam bem).
- **Scrollbar pode ficar imprecisa** inicialmente se a estimativa de altura tá longe da real.

**Fonte**: [4]

### 44. Sem debounce/throttle em eventos caros

**O problema.** Eventos de input disparam **a cada keystroke**. Eventos de scroll/resize disparam **a 60+ vezes por segundo**. Se cada um faz fetch ou cálculo pesado, o app trava.

```tsx
// ruim — fetch a cada tecla digitada
<input onChange={e => fetchResults(e.target.value)} />
// digita "react" → 5 fetches (r, re, rea, reac, react)
```

**Soluções.**

**Debounce — espera N ms sem novas chamadas antes de executar.** Ideal pra inputs (busca, autocomplete).

```tsx
import { useDebouncedCallback } from 'use-debounce';

function Search() {
  const debouncedFetch = useDebouncedCallback((q: string) => {
    fetchResults(q);
  }, 300);

  return <input onChange={e => debouncedFetch(e.target.value)} />;
  // usuário digita "react" em 300ms — 1 fetch no final, com "react"
}
```

**Throttle — garante no máximo N chamadas por segundo.** Ideal pra scroll/resize.

```tsx
import { throttle } from 'lodash-es';

const handleScroll = throttle(() => {
  updateVisiblePosition();
}, 100);

useEffect(() => {
  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}, []);
```

**Heurísticas de delay.**

- **Input de busca**: 250–400ms (sensação de "estou digitando").
- **Input normal** (validação em tempo real): 100–200ms.
- **Scroll handler**: 16ms (60fps) ou 100ms (aceitável).
- **Resize**: 100–250ms (nunca faz sentido reagir a cada pixel).

> [!info]- Debounce vs Throttle — diferença mental
> **Debounce**: "só execute se ficar quieto por N ms". Usuário digita 10 letras em rajada → 1 execução, depois do último `keystroke`.
>
> **Throttle**: "no máximo 1 execução por N ms". Scroll dispara 1000 eventos → executa 1x a cada 100ms, ignora os entre.
>
> Debounce pra "quero valor final". Throttle pra "quero amostra regular".

**Cuidado com `useMemo(() => debounce(...), [...])`.** Criar novo debounce a cada render quebra tudo. Use `useCallback` pra estabilizar, ou hooks de lib como `useDebouncedCallback`.

**Fonte**: [4]

### 45. Computação CPU-heavy no main thread

**O problema.** JavaScript no browser roda em **um único thread** (o main thread) — o mesmo que renderiza UI, processa cliques, aplica layouts. Se você pôr algo pesado (parse de 10MB de JSON, geração de PDF, processamento de imagem, algoritmo de grafo) nesse thread, **tudo congela** até terminar.

Sintomas: scroll trava, cliques não respondem, animação pula, INP arruinado.

**Solução — Web Workers.** Threads de verdade, separados do main. Executam JavaScript em paralelo, trocam dados por mensagens.

**Exemplo básico:**

```ts
// worker.ts
self.onmessage = (e) => {
  const result = heavyComputation(e.data);
  self.postMessage(result);
};
```

```tsx
// Component.tsx
function Analyzer({ data }: { data: BigData }) {
  const [result, setResult] = useState(null);

  useEffect(() => {
    const worker = new Worker(new URL('./worker.ts', import.meta.url));
    worker.postMessage(data);
    worker.onmessage = (e) => setResult(e.data);
    return () => worker.terminate();
  }, [data]);

  if (!result) return <Processing />;
  return <Chart data={result} />;
}
```

Main thread fica livre, UI responsiva enquanto worker processa.

**Lib que torna ergonômico — `comlink`.**

```ts
// worker.ts
import { expose } from 'comlink';

expose({
  async analyze(data) {
    return heavyComputation(data);
  },
});
```

```tsx
// Component.tsx
import { wrap } from 'comlink';
import AnalyzerWorker from './worker?worker';

const analyzer = wrap(new AnalyzerWorker());

async function process(data) {
  const result = await analyzer.analyze(data); // parece chamada normal
  setState(result);
}
```

**Quando vale Web Worker.**

- Operação CPU-heavy que ultrapassa **~50ms** (bloqueio perceptível).
- Exemplos reais: parse de JSON grande, geração de PDF no cliente (jsPDF), image processing (canvas manipulation), crypto em volume (hashing, encryption), árvore de decisão grande (big tree traversal).

**Quando não vale.**

- Setup do worker tem custo (~10ms). Pra operações < 50ms, não compensa.
- Comunicação main ↔ worker serializa dados (`postMessage`) — transferir 100MB vai demorar também. `Transferable` objects (ArrayBuffer) ajudam.

> [!info]- Long tasks e INP
> "Long task" no browser = operação > 50ms no main thread. Cada uma bloqueia UI por aquele tempo. INP mede o pior caso. Meta pra INP: < 200ms. Se uma função sua tem > 50ms de execução, pense em Worker ou `requestIdleCallback`.

**Fonte**: [4]

### 46. CLS alto por falta de reserva de espaço

**O problema.** Conteúdo "pula" durante carregamento:

- Imagem carrega → conteúdo abaixo é empurrado.
- Anúncio aparece → layout shift.
- Fonte custom carrega e troca métrica → texto reflui.
- Embed de Twitter/YouTube carrega → espaço muda.

CLS alto não é só estética — **Google penaliza em SEO**, e usuário clica no botão errado porque pulou do lugar.

**Solução — reserve espaço antes do carregamento.**

**1. `width`/`height` em `<img>` (crítico).**

```html
<!-- ruim — browser não sabe tamanho até baixar -->
<img src="hero.jpg" alt="..." />

<!-- bom — browser reserva aspect ratio desde o início -->
<img src="hero.jpg" alt="..." width="1200" height="600" />
```

Com `width` e `height`, browser calcula `aspect-ratio` e reserva o espaço mesmo antes da imagem chegar.

**2. `aspect-ratio` em CSS pra containers.**

```css
.video-embed {
  aspect-ratio: 16 / 9;
  width: 100%;
}
```

**3. `font-display: optional` ou `font-display: swap` com match próximo.**

```css
@font-face {
  font-family: 'Inter';
  src: url(...) format('woff2');
  font-display: swap;
  /* fallback próximo minimiza shift quando troca */
}
```

**4. Skeletons de tamanho fixo.** Skeletons (loading placeholders) devem ocupar **exatamente o mesmo espaço** que o conteúdo final. Se o card real tem 200px de altura, skeleton tem 200px.

**5. Ads/embeds em container de tamanho reservado.**

```html
<div style="min-height: 250px"><!-- ad slot 300x250 --></div>
```

**Diagnóstico.** Chrome DevTools > Performance > grava carregamento da página > painel "Layout Shifts" lista o que pulou.

> [!info]- CLS — o que conta
> Fórmula: `impact fraction × distance fraction`. Shift pequeno num pedacinho da tela = CLS baixo; shift grande movendo conteúdo central = CLS alto.
>
> Shifts causados por **interação do usuário nos últimos 500ms** (ex: clique abre accordion) não contam — são "esperados". Shifts automáticos durante carregamento contam.

**Fonte**: [4]

---

## Cap. 11 — Acessibilidade

> [!quote] A11y não é feature — é qualidade mínima
> Um app que não é acessível é um app quebrado pra 15–20% dos usuários, além de risco jurídico em várias jurisdições (ADA nos EUA, EAA na UE a partir de 2025, LBI no Brasil).

**Tecnologias assistivas que você precisa conhecer.**

- **Screen reader**: lê a tela em voz alta. Principais: NVDA (Windows, grátis), JAWS (Windows, pago), VoiceOver (Mac/iOS, nativo), TalkBack (Android).
- **Navegação por teclado**: Tab pra navegar, Shift+Tab pra voltar, Enter/Space pra ativar, Esc pra fechar.
- **Zoom**: usuários com baixa visão aumentam fonte até 200%+.
- **Alto contraste / dark mode**: preferências `prefers-contrast`, `prefers-color-scheme`.
- **Reduced motion**: `prefers-reduced-motion` — desativa animações pra quem sente enjôo.

Teste mínimo: feche os olhos e navegue o app só com teclado + screen reader. Se não funcionar, está quebrado.

### 47. `<div onClick>` em vez de `<button>`

**O problema.** Desenvolvedores usam `<div>` com `onClick` porque "é mais fácil de estilizar". Mas `<div>` **não é semanticamente um botão** — e tecnologia assistiva trata como texto qualquer:

- Não é focável via Tab (a menos que você adicione `tabIndex={0}`).
- Não ativa com Enter ou Space (a menos que você implemente manualmente).
- Screen reader não anuncia "button" — lê só o texto.
- Não expõe estados (disabled, pressed) sem atributos ARIA.

**Tentar "ressemantizar" um `<div>` é recriar mal o que `<button>` já faz:**

```tsx
// ruim — só o olho de humano vê como botão
<div onClick={handleClick} className="btn">Salvar</div>

// ainda ruim — dando um jeito; agora falta estado de disabled, active, etc
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') handleClick(); }}
  aria-label="Salvar"
>
  Salvar
</div>

// bom — elemento certo pro trabalho
<button type="button" onClick={handleClick}>Salvar</button>
```

`<button>` já tem:

- `role="button"` implícito.
- Foco via Tab.
- Ativação via Enter **e** Space.
- Estado `:focus-visible` para estilizar foco.
- Atributo `disabled` semântico.
- Eventos de teclado consistentes com convenções do SO.

**"Mas o estilo default é feio."** Resete com CSS, não abandone o elemento:

```css
button.unstyled {
  all: unset; /* ou reset manual */
  cursor: pointer;
  /* aplicar estilos do design system */
}
```

**Regra simples.**

- Ação na **mesma página** (toggle, abrir modal, submeter form) → `<button>`.
- Navegação pra **outra URL** → `<a href="...">`.
- Toggle de estado com 2 opções → `<button aria-pressed="...">` ou `<input type="checkbox">`.
- Opção dentro de grupo → `<input type="radio">`.

> [!tip] Linter te protege
> `eslint-plugin-jsx-a11y` tem regra `click-events-have-key-events` — avisa quando você coloca `onClick` em `<div>` sem `onKeyDown`.

**Fonte**: [5][6]

### 48. Imagens sem `alt`

**O problema.** `<img>` sem atributo `alt` deixa screen readers confusos:

- **Sem `alt`**: screen reader fala o nome do arquivo (`"logo-final-v3-retina.png"`) ou pula — ambos ruins.
- **`alt=""`**: explicitamente marca como **decorativa** — screen reader pula, correto para imagens puramente estéticas.
- **`alt="descrição"`**: imagem **informativa** — screen reader lê.

**Regras de decisão.**

```tsx
// decorativa — pula no screen reader
<img src="/flourish.svg" alt="" />

// informativa — texto descreve a INFORMAÇÃO, não a aparência
<img src="/chart.png" alt="Vendas cresceram 40% no Q3 2025" />

// logo como marca da empresa
<img src="/logo.svg" alt="Acme Inc." />

// link com ícone
<a href="/settings">
  <img src="/gear.svg" alt="Configurações" />
</a>

// link com texto + ícone — ícone é decorativo
<a href="/settings">
  <img src="/gear.svg" alt="" />
  Configurações
</a>
```

**Regras gerais.**

- **Nunca repita texto visível no alt.** Se o botão já tem texto "Salvar", não coloque `alt="Salvar"` no ícone.
- **Alt não precisa dizer "imagem de..."**. Screen reader já anuncia "imagem" automaticamente. Escreva só o conteúdo: `alt="Gráfico de barras..."`.
- **Para gráficos complexos**, alt curto + descrição longa em elemento separado (`<figcaption>` ou `aria-describedby`).
- **Fotos de pessoas**: descreva o relevante (`alt="João Silva, CEO da Acme"`), não traços irrelevantes.

**Fonte**: [5][6]

### 49. Forms sem `<label>` associado

**O problema.** `<input>` sem `<label>` é um campo mudo pra screen reader. Usuário ouve "edit text, in" e tem que adivinhar o que é.

```tsx
// ruim — placeholder não é label
<input type="email" placeholder="E-mail" />

// ruim — label existe, mas não está associado ao input
<label>E-mail</label>
<input type="email" />

// bom — htmlFor liga ao id do input
<label htmlFor="email">E-mail</label>
<input id="email" type="email" />

// bom também — label envolve o input
<label>
  E-mail
  <input type="email" />
</label>
```

**Por que placeholder não substitui label.**

- **Desaparece quando o usuário digita** — usuário esquece o que era, tem que apagar pra ver de novo.
- **Contraste fraco** — muitos designs fazem placeholder cinza claro, difícil de ler.
- **Screen reader comporta diferente** — nem todos leem placeholder.
- **Usuários com déficits cognitivos** perdem contexto quando o rótulo some.

**Quando label visível não cabe no design — use `aria-label`.**

```tsx
// campo de busca sem label visível, mas acessível
<input type="search" aria-label="Buscar produtos" placeholder="Buscar..." />
```

**Ou `aria-labelledby`** apontando pra outro elemento:

```tsx
<h2 id="form-title">Edite seu perfil</h2>
<input type="text" aria-labelledby="form-title" />
```

**Associação completa (requisição, help, erro).**

```tsx
<label htmlFor="email">E-mail</label>
<input
  id="email"
  type="email"
  required
  aria-describedby="email-help email-error"
  aria-invalid={hasError}
/>
<span id="email-help">Nunca compartilharemos seu e-mail.</span>
{hasError && <span id="email-error" role="alert">E-mail inválido.</span>}
```

> [!info]- `aria-*` atributos mais comuns em forms
>
> - `aria-label` — rótulo invisível (quando não há texto visível).
> - `aria-labelledby` — id de outro elemento que rotula este.
> - `aria-describedby` — id de texto de ajuda/erro.
> - `aria-invalid` — marca campo com erro.
> - `aria-required` — indica obrigatório (redundante se já tem `required`).
> - `role="alert"` — anuncia mudança (como mensagem de erro aparecendo).

**Fonte**: [5][6]

### 50. Focus management ignorado em SPAs / modais

**O problema.** Em apps tradicionais (multi-page), cada navegação é page load — browser reseta foco pra top, screen reader anuncia o novo `<title>`. Em SPA, você só troca a URL e renderiza outra árvore — **foco permanece onde estava**.

Sintomas:

- **Navegação SPA**: screen reader não anuncia que chegou em outra página. Foco fica no link clicado, que agora nem existe mais.
- **Modal abre**: foco continua no botão que abriu. Usuário de teclado não está "dentro" do modal — tabs vão pro fundo da página atrás.
- **Modal fecha**: foco vai pra `document.body` (ou some). Usuário se perde.
- **Dropdown/menu/popover**: mesmo problema.

**Soluções.**

**1. Anunciar mudança de rota em SPAs.**

```tsx
// focar o h1 principal quando a rota mudar
function RouteAnnouncer() {
  const location = useLocation();
  const h1Ref = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    h1Ref.current?.focus();
  }, [location.pathname]);

  return null; // ou componente wrapping o h1
}
```

**2. Modal — focus trap + devolver foco ao trigger.**

```tsx
// ruim — modal sem gestão de foco
function Modal({ open, onClose, children }) {
  if (!open) return null;
  return createPortal(<div className="modal">{children}</div>, document.body);
}

// bom — foco move pro modal ao abrir, trava dentro, devolve ao fechar
import { Dialog } from '@radix-ui/react-dialog';

function EditModal() {
  return (
    <Dialog.Root>
      <Dialog.Trigger>Editar</Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay />
        <Dialog.Content>
          <Dialog.Title>Editar perfil</Dialog.Title>
          {/* Radix cuida de: focus move, focus trap, Esc, click outside, return focus */}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

**3. Dropdowns / menus / comboboxes — mesma lógica.** Use [Radix UI](https://www.radix-ui.com/), [React Aria](https://react-spectrum.adobe.com/react-aria/), [Headless UI](https://headlessui.com/) — libs que **fazem a a11y direito**. Não reimplemente.

> [!info]- O que é "focus trap"?
> Mecanismo que **impede o foco de escapar** de um contêiner até ele ser fechado. Quando modal está aberto, `Tab` circula entre elementos focáveis **do modal**; quando chega no último, volta pro primeiro. Essencial pra usuário de teclado não "sair" do modal sem querer.

**Cuidado — não use `autoFocus` cegamente.** Auto-focar um input ao montar funciona em alguns casos (campo principal de form) mas atrapalha em outros (page load com usuário rolando o header). Pense caso a caso.

**Checklist rápido de a11y.**

- [ ] Navegação completa só com Tab/Shift+Tab/Enter/Esc?
- [ ] Foco visível (outline/ring) em todos os elementos interativos?
- [ ] Modal: foco move ao abrir, trava dentro, devolve ao fechar?
- [ ] SPA: mudança de rota anunciada ao screen reader?
- [ ] Contraste mínimo AA (4.5:1 texto, 3:1 UI) — use [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/).
- [ ] `prefers-reduced-motion` respeitado em animações?

**Fonte**: [5][6]

---

## Cap. 12 — Legibilidade

### 51. Condicionais ilegíveis

**O problema.** Ternário aninhado é tecnicamente válido, semanticamente correto — e ilegível depois de 2 níveis.

```tsx
// sofrimento — precisa parsear mentalmente a árvore toda
return (
  <div>
    {isLoading ? (
      <Spinner />
    ) : error ? (
      <Error error={error} />
    ) : !data ? (
      <Empty />
    ) : data.length === 0 ? (
      <NoResults />
    ) : (
      <List data={data} />
    )}
  </div>
);
```

Pra entender o que é renderizado numa condição específica, o leitor precisa andar até o final do ternário, contando parênteses. Debug por bisect — não por leitura.

**Solução 1 — early returns.**

```tsx
// legível — uma condição por linha, chegou ao fim = sucesso
function List({ isLoading, error, data }) {
  if (isLoading) return <Spinner />;
  if (error) return <Error error={error} />;
  if (!data || data.length === 0) return <Empty />;
  return <List data={data} />;
}
```

Cada condição se explica, não há aninhamento, alteração futura não precisa se preocupar com a estrutura do ternário.

**Solução 2 — variáveis extraídas quando o condicional é pequeno.**

```tsx
const shouldShowBadge = user.role === 'admin' || user.hasFlag;
return <Card badge={shouldShowBadge && <Badge />} />;
```

**Solução 3 — componente dedicado a cada estado.**

```tsx
function UserList() {
  const { data, isLoading, error } = useUsers();
  if (isLoading) return <UserListLoading />;
  if (error) return <UserListError error={error} />;
  if (!data?.length) return <UserListEmpty />;
  return <UserListSuccess users={data} />;
}
```

Vantagem extra: cada estado vira um componente Storybook-able.

**Ternário simples continua sendo ok.**

```tsx
// aceitável — ternário de 1 nível
<Badge color={isActive ? 'green' : 'gray'} />

// aceitável — inline curto pra valor
<p>Olá, {user?.name ?? 'visitante'}!</p>
```

**Fonte**: [1]

### 52. Sem early returns

**O problema.** Código escrito em cascata de `if/else` aninhados quando inverter a condição e retornar cedo resolveria em 1 nível:

```tsx
// ruim — pirâmide de ifs
function process(user) {
  if (user) {
    if (user.active) {
      if (user.role === 'admin') {
        // lógica principal
        return doAdminStuff(user);
      } else {
        return 'não autorizado';
      }
    } else {
      return 'inativo';
    }
  } else {
    return 'sem usuário';
  }
}

// bom — guard clauses
function process(user) {
  if (!user) return 'sem usuário';
  if (!user.active) return 'inativo';
  if (user.role !== 'admin') return 'não autorizado';

  return doAdminStuff(user);
}
```

**Benefícios do early return.**

- **Uma condição por vez.** Leitor não precisa manter 4 ifs abertos na cabeça.
- **Intenção explícita.** "Se não passa nesse check, não continue" é mais direto que "se passa nesse check, aninhe tudo que vem depois".
- **Diff pequeno.** Adicionar um novo guard é +1 linha, não reformatar pirâmide.
- **Função "principal" visível.** O happy path (última linha, sem aninhamento) é o foco.

> [!tip] Regra prática
> Se a função tem `if/else/if/else` com mais de 2 níveis, inverta condições e retorne cedo. "Linked list of returns" > "binary tree of ifs".

**Exceção.** Em render de componentes com JSX, às vezes uma condição pequena inline é melhor que sair com early return (evita múltiplos `<>` fragmentos confusos). Use bom senso — o objetivo é legibilidade, não regra cega.

**Fonte**: [1]

### 53. Magic numbers

**O problema.** Números literais no código sem explicação do que significam. Leitor precisa caçar contexto, adivinhar, perguntar no Slack.

```ts
// ruim — o que é cada número?
if (retries > 3) throw new Error('fail');
setTimeout(pollStatus, 86400000);
if (user.age < 13) showParentalConsent();
const discount = total * 0.15;
```

Seis meses depois, alguém precisa trocar `3` por `5` — mas grep por `"3"` retorna milhares de matches. Alguém muda `86400000` pra `86_400_000` (um dia em ms, mas escrito menos confuso) e quebra se outro código esperava o valor exato.

**Solução — nomear constantes.**

```ts
// bom — intenção explícita, trocar é grep único
const MAX_RETRIES = 3;
const ONE_DAY_MS = 24 * 60 * 60 * 1000;
const MINIMUM_AGE_WITHOUT_CONSENT = 13;
const DEFAULT_DISCOUNT_RATE = 0.15;

if (retries > MAX_RETRIES) throw new Error('fail');
setTimeout(pollStatus, ONE_DAY_MS);
if (user.age < MINIMUM_AGE_WITHOUT_CONSENT) showParentalConsent();
const discount = total * DEFAULT_DISCOUNT_RATE;
```

**Onde colocar constantes.**

- **No topo do módulo** — se usadas em vários pontos do mesmo arquivo.
- **Arquivo dedicado** (`constants.ts` por domínio) — se usadas em vários lugares.
- **Config externo** — se devem mudar sem deploy (env vars, feature flags).

**Quando número literal é ok.**

- **0, 1, -1, 2** — valores tão universais que não precisam de nome (`arr[0]`, `x * 2`, `i + 1`).
- **Valores explicados pelo contexto imediato**: `<Grid columns={3} />` — "3 colunas" já é óbvio.
- **Matemática direta com significado universal**: `angle * Math.PI / 180` (radianos), `1024 * 1024` (1 MiB — aqui ainda vale uma const).

**Regra mental.** Se você tem que explicar o número em comentário, ele merece um nome em vez do comentário. `const MAX_RETRIES = 3` é auto-documentado.

> [!info]- Por que "magic"?
> Termo clássico de programação: número que "magicamente" tem significado que só quem escreveu conhece. A correção é **desmagicar** — dar nome ao significado.

**Fonte**: [1]

---

## Cap. 13 — Arquitetura e manutenibilidade

### 54. Mesma lógica condicional espalhada

**O problema.** Regra de negócio duplicada em 15 lugares. Quando a regra muda (e _vai_ mudar), você precisa caçar todas as ocorrências. Esquecer uma = bug sutil em produção.

```tsx
// espalhado pela codebase
// ProfilePage.tsx: if (user.role === 'admin' || user.role === 'superadmin') showEditButton();
// Sidebar.tsx:     if (user.role === 'admin' || user.role === 'superadmin') showAdminLink();
// UserList.tsx:    if (user.role === 'admin' || user.role === 'superadmin') showDeleteAction();
// ... +12 arquivos
```

No dia que o produto decide que "editor" também pode editar, você faz grep por `role === 'admin'`, acha 15 lugares, muda cada um, quer Deus que não tenha esquecido de nenhum. Test coverage não cobre todos os caminhos. Bug aparece semanas depois.

**Solução — centralize regras de negócio em funções nomeadas.**

```ts
// src/domain/permissions.ts
export const canEditUser = (user: User) =>
  user.role === 'admin' || user.role === 'superadmin';

export const canViewAdminPanel = (user: User) =>
  user.role === 'admin' || user.role === 'superadmin';

export const canDeleteUser = (user: User, target: User) =>
  canEditUser(user) && user.id !== target.id; // admin não deleta a si
```

Agora, regra muda em **um arquivo**:

```ts
export const canEditUser = (user: User) =>
  user.role === 'admin' || user.role === 'superadmin' || user.role === 'editor';
```

E os 15 lugares se atualizam automaticamente.

**Benefícios além de evitar bugs.**

- **Intenção documentada.** `canEditUser(user)` é auto-explicativo. `user.role === 'admin' || user.role === 'superadmin'` pede leitura.
- **Testável isoladamente.** Teste unitário na função de permissão, não em 15 componentes.
- **Consistência.** Impossível dois lugares implementarem a regra de forma sutilmente diferente.

**Quando criar o helper.**

- **2ª ocorrência**: considerar. A terceira ocorrência te machucou.
- **3ª ocorrência**: extrair, sem dúvida.
- **1ª ocorrência**: não antecipe. DRY tem custo (abstração prematura).

> [!info]- "Regra de negócio" vs "regra de apresentação"
> **Regra de negócio**: "admin pode editar" — fato sobre o domínio, muda quando o produto muda.
>
> **Regra de apresentação**: "mostrar botão em vermelho" — fato sobre UI, muda quando design muda.
>
> As de negócio são as que você deve centralizar com mais rigor. As de apresentação podem morar junto do componente sem drama.

**Fonte**: [1]

### 55. Sem abstração sobre libs third-party

**O problema.** Você escolhe uma lib de notifications (`react-toastify`) e importa ela direto em 80 componentes. Um ano depois, você quer trocar por `sonner` (mais leve, melhor UX). Resultado: refactor de mês, tocando 80 arquivos, cada commit uma revisão.

O mesmo acontece com:

- Logger (`winston` → `pino` → `axiom`)
- Analytics (`mixpanel` → `posthog`)
- Date lib (ver [[#2. Deps pesadas quando existem alternativas leves|#2]])
- HTTP client (`axios` → `fetch`)
- Modal lib (`react-modal` → `radix-ui`)

**Solução — wrap atrás de interface interna.**

```ts
// src/lib/notifications.ts — único lugar que sabe que é react-toastify
import { toast } from 'react-toastify';

export const notify = {
  success: (msg: string) => toast.success(msg),
  error: (msg: string) => toast.error(msg),
  info: (msg: string) => toast.info(msg),
  dismiss: () => toast.dismiss(),
};
```

```tsx
// em todo o app — acopla só à sua interface
import { notify } from '@/lib/notifications';

notify.success('Salvo!');
```

Trocar de lib agora é: editar `src/lib/notifications.ts` pra usar `sonner`. **Um arquivo**, 80 componentes continuam funcionando.

**Princípio — criar ponto de controle único.** Esse padrão é conhecido como [anti-corruption layer](https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer) em DDD: você protege seu código de peculiaridades da lib externa.

**Cuidado — overhead de abstração.** Nem toda lib merece wrapper.

- **Vale** quando a lib é usada em muitos lugares + é plausível trocar + a API é não-trivial.
- **Não vale** quando a lib é tão estabelecida que trocar nunca vai acontecer (React, TypeScript, Node built-ins). Wrap em cima do wrap em cima do wrap é anti-pattern chamado "lasanha arquitetural".

**Heurística.** Pergunte: "Se amanhã eu precisasse trocar essa lib, seria trivial, médio ou caro?" Se "caro", wrap. Se "trivial", não.

> [!info]- Abstração vs acoplamento
> Toda abstração adiciona camada. A camada tem custo (uma indireção a mais na leitura, um lugar a mais pra procurar bug). Só compensa quando protege de algo real. Abstrair `console.log` atrás de um `logger.debug` é overkill se você nunca vai trocar `console`.

**Fonte**: [1]

### 56. Arquivos gigantes que ninguém ousa refatorar

**O problema.** `LegacyDashboard.tsx` tem 3000 linhas. Sem testes. Lógica crítica. Cada um na equipe tem medo de tocar. Ele cresce mais um pouco a cada sprint, porque é o caminho de menor resistência ("o que estou mexendo já tá aqui, só vou adicionar mais 100 linhas").

Com o tempo, o arquivo vira **dívida técnica intransponível**: pra "reescrever" precisa de sprint dedicado, produto não prioriza, ninguém se voluntaria, então vai piorando.

**Estratégia incremental — a única que funciona.**

**1. Characterization tests primeiro.**

Antes de tocar uma linha, **capture o comportamento atual** (inclusive bugs conhecidos) com testes. Isso vira sua rede de segurança.

```tsx
// não importa se o código é feio — testa o que ELE FAZ hoje
test('LegacyDashboard renderiza tabela com dados filtrados por role', () => {
  const users = [...];
  render(<LegacyDashboard users={users} filter="admin" />);
  expect(screen.getAllByRole('row')).toHaveLength(3);
});

test('LegacyDashboard ignora filtro quando há erro — bug conhecido mas aceito', () => {
  // documenta o comportamento real, inclusive o errado
});
```

**2. Extraia uma função pura de cada vez.**

Pega um trecho de lógica (filtro, ordenação, formatação). Tira pra função pura fora do componente. Testa a função isolada. Substitui o trecho no legacy.

```tsx
// antes — inline no JSX
{users
  .filter(u => u.active && u.role === filter)
  .sort((a, b) => a.name.localeCompare(b.name))
  .map(u => /* ... */)}

// depois — função extraída + testada
const visibleUsers = getVisibleUsers(users, filter);
{visibleUsers.map(u => /* ... */)}

// src/lib/users.ts
export function getVisibleUsers(users: User[], filter: Role) { /* ... */ }
```

**3. Extraia sub-componentes pequenos.**

Tabela, modal, form — cada um pra componente próprio. Testes de snapshot/interaction pra cada um.

**4. Repita até o arquivo raiz ser razoável.**

Em 2–3 meses de trabalho incremental (alguns PRs por semana), um arquivo de 3000 linhas vira um de 300 + 10 arquivos pequenos. Cada PR é pequeno, revisável, reversível.

**Anti-pattern — "vou reescrever do zero em uma PR".**

- Leva 3 vezes mais tempo do que estimou.
- Diverge do mainline, merge conflicts infernais.
- Ninguém revisa direito (PR de 5000 linhas).
- No dia que subir, regressões que ninguém capturou.

> [!quote] Michael Feathers, _Working Effectively with Legacy Code_
> "Legacy code is simply code without tests."

A essência: o arquivo gigante é medonho porque você **não tem certeza do que ele faz**. Resolva a incerteza primeiro (characterization tests), aí o refactor vira mecânico.

> [!info]- Characterization test vs TDD
>
> - **TDD (test-driven development)**: escreve teste **antes** do código; teste define o que deveria fazer.
> - **Characterization test**: escreve teste **depois** do código, para o que ele **já faz** (inclusive possíveis bugs). Objetivo: ter rede de segurança pra refatorar sem quebrar.
>
> Ambos são rede de segurança. TDD pra código novo, characterization pra legado.

**Fonte**: [1]

---

## Checklist para code review

### Dependências e tooling

- [ ] Deps novas justificadas (bundle size checado)?
- [ ] Linter/formatter rodando em CI?

### Organização

- [ ] Estrutura consistente (feature-based ou domain-based)?
- [ ] Arquivos da feature colocalizados?
- [ ] Sem `export *` em barrels?

### Componentes

- [ ] Sem god components (> ~300 linhas)?
- [ ] Sem componente definido dentro de componente?
- [ ] Props mínimas (não passar objetos gigantes)?
- [ ] Prop drilling sob controle (< 3 níveis)?

### Estado

- [ ] Nada de state pra valor derivável?
- [ ] `useRef` pra valores que não afetam render?
- [ ] Context split por domínio, `value` memoizado?
- [ ] Reset de state via `key`, não via effect?

### Memoização

- [ ] Defaults definidos fora do componente?
- [ ] Objetos/arrays inline evitados em props críticas?
- [ ] `useCallback` em handlers passados pra filhos memoizados?

### TypeScript

- [ ] Zero `any`?
- [ ] Discriminated unions em estados assíncronos?
- [ ] `exhaustive-deps` respeitado?

### Listas

- [ ] Keys estáveis (nunca `index`)?

### useEffect

- [ ] Effect sincroniza com sistema externo (não deriva dados)?
- [ ] Sem encadeamento de effects?
- [ ] Lógica de evento nos handlers, não em effects?
- [ ] Cleanup em timers, listeners, fetches?
- [ ] Race conditions em fetch tratadas (flag/AbortController)?
- [ ] Escolha correta entre `useEffect`/`useLayoutEffect`?

### Data fetching e erros

- [ ] Usando lib de data fetching (React Query/SWR/framework)?
- [ ] Error boundary em seções críticas?
- [ ] Sem `catch {}` vazio?
- [ ] Loading + error + empty states cobertos?

### Performance

- [ ] Code splitting por rota?
- [ ] Imagens otimizadas (WebP/AVIF, lazy, responsive)?
- [ ] Listas longas virtualizadas?
- [ ] Debounce/throttle em eventos caros?
- [ ] CPU-heavy em Web Worker?
- [ ] CLS controlado (espaço reservado)?

### Acessibilidade

- [ ] `<button>` pra clicável (não `<div>`)?
- [ ] `alt` em todas as imagens?
- [ ] `<label>` em todo input?
- [ ] Focus management em navegação SPA e modais?

### Legibilidade

- [ ] Early returns em condicionais complexas?
- [ ] Magic numbers nomeados?

### Arquitetura

- [ ] Regras de negócio centralizadas (sem duplicação)?
- [ ] Libs third-party encapsuladas em wrapper?

---

## Bibliografia

Todas as fontes usadas na consolidação deste manual. Numeração citada no final de cada item.

1. **Frontend Joy** — [29 React Codebase Red Flags from a Senior Frontend Developer](https://www.frontendjoy.com/p/29-react-codebase-red-flags-from-a-senior-frontend-developer). Fonte principal da primeira versão desta nota; base dos capítulos 1–2, 7, 9, 12–13 e grande parte de 3–6.

2. **React Docs (oficial)** — [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect). Referência autoritativa do capítulo 8; origem dos itens sobre derivar dados no render, `key`-based reset, encadeamento de effects e race conditions.

3. **LogRocket Blog — David Omotayo** — [15 common useEffect mistakes to avoid in your React apps](https://blog.logrocket.com/15-common-useeffect-mistakes-react/). Complementa o capítulo 8 com stale values, cleanup de listeners, `useLayoutEffect` e `useEffectEvent`.

4. **Sentry Engineering Blog** — [React Performance: Common Problems & Their Solutions](https://blog.sentry.io/react-js-performance-guide/). Base do capítulo 10 (code splitting, imagens, virtualização, CLS, Web Workers).

5. **ITNEXT — Juntao Qiu** — [6 Common React Anti-Patterns That Are Hurting Your Code Quality](https://itnext.io/6-common-react-anti-patterns-that-are-hurting-your-code-quality-904b9c32e933). Componente-dentro-de-componente, props inline, prop drilling.

6. **Medium — Suresh Kumar Ariya Gowder** — [Reactjs JSX Anti-Patterns You Must Avoid](https://medium.com/@sureshdotariya/reactjs-jsx-anti-patterns-you-must-avoid-in-2025-f58e44d08abf). JSX e acessibilidade básica.

### Referências complementares

- [React Docs — Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks)
- [React Docs — Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)
- [React Docs — useLayoutEffect](https://react.dev/reference/react/useLayoutEffect)
- [Kent C. Dodds — Myths about useEffect](https://www.epicreact.dev/myths-about-useeffect)
- [web.dev — Core Web Vitals (CLS, LCP, INP)](https://web.dev/articles/vitals)
- [MDN — Web Workers API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [TanStack Query](https://tanstack.com/query/)
- [bundlephobia.com](https://bundlephobia.com/) · [pkg-size.dev](https://pkg-size.dev/)

---

## Notas relacionadas

- [[React]] — deep dive na biblioteca
- [[JavaScript Fundamentals]] — base de JS moderno
- [[TypeScript]] — tipagem e patterns
- [[Testes em JavaScript]] — characterization tests, Testing Library
- [[HTML e CSS]] — fundamentos de UI e semântica
