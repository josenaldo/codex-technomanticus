---
title: "Tipando data fetching"
created: 2026-04-26
updated: 2026-04-26
type: concept
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, data-fetching, react-query, tanstack, suspense, server-actions]
aliases:
  - Data fetching tipado
  - useQuery TanStack TS
---

# Tipando data fetching

> [!abstract] TL;DR
> `useQuery<TData, TError>` infere de `queryFn`. Validação runtime com Zod no boundary (TS é compile-time only). `use()` em React 19 desembrulha Promise com Suspense. Server Actions em Next 16 são funções tipadas chamadas direto do client. Result type pattern dá erros explícitos quando o caller precisa lidar com falhas como dados.

## O que é

Data fetching em React com TypeScript em 2026 não é mais uma escolha única. Três modelos coexistem em produção, e a decisão de qual usar depende de onde o componente vive (client puro, RSC, edge), do tipo de cache que se quer (cliente com invalidação fina, RSC com revalidação por tag, sem cache) e da forma de orquestrar loading e erro (estado discriminado no render, Suspense + error boundary, formulário com server action). A nota cobre os três e o ponto comum entre eles — validação runtime no boundary.

**Modelo 1: client-side com TanStack Query (`useQuery` / `useMutation`).** É a escolha default em SPAs e em Next/Remix quando o componente roda no cliente e precisa de cache compartilhado entre componentes. `useQuery({ queryKey, queryFn })` infere o tipo dos dados a partir do retorno de `queryFn`, expõe um campo `status` que é uma discriminated union (`'pending' | 'success' | 'error'` — ver [[09 - Tipando reducers e state machines]]) e gerencia cache, refetch, deduplicação, revalidação em janela e otimistic updates. `useMutation` cobre o lado de escrita (POST, PUT, DELETE) com a mesma forma.

**Modelo 2: Suspense-driven com `use()` (React 19).** O hook `use()` aceita uma `Promise<T>` e retorna `T` diretamente — sem `undefined`, sem `isLoading`, sem `isError` no call site. Quando a Promise está pendente, o componente "suspende" e o `<Suspense fallback>` mais próximo na árvore exibe o estado de loading; quando rejeita, o `<ErrorBoundary>` mais próximo captura. O tipo do consumer fica radicalmente mais simples (`const user = use(promise)` é `User`, não `User | undefined`), mas o custo é arquitetural: a Promise tem que ser estável entre renders (idealmente criada em Server Component e passada como prop), e os boundaries de loading/erro vivem **acima** do componente, não dentro dele.

**Modelo 3: Server Actions (Next.js 16).** Uma função marcada com `'use server'` no topo do arquivo (ou de um bloco) vira um endpoint RPC tipado. Do client component, ela é importada e chamada como função normal — `await updateUser({ id, name })` —, mas Next/React serializam os argumentos, fazem POST para o servidor, executam a função no Node e devolvem o resultado serializado. O tipo da assinatura no client **é** o tipo da assinatura no server: a inferência cruza a fronteira de rede sem ferramenta de codegen. O modelo cobre mutações (formulários, ações pontuais) e composição com `<form action={...}>` para progressive enhancement.

O denominador comum é o boundary de rede. Independentemente do modelo, dados que chegam de fora do programa entram como `unknown` e precisam ser validados em runtime antes de serem tratados como o tipo declarado — caso contrário o tipo é uma promessa não verificada.

## Por que importa

TypeScript é estritamente compile-time. No momento em que o código JavaScript roda, todos os tipos foram apagados — não há `User`, não há `string`, não há discriminated union. Para dados internos ao programa, isso é fine: o compilador garante que nenhum caminho do código atribui valor incompatível com o tipo declarado. Para dados que vêm da rede, o compilador não tem como saber: `fetch` retorna `Response`, `await res.json()` retorna `Promise<any>`, e o `any` se propaga silenciosamente para qualquer lugar que use o resultado. Anotar `: User` na variável é uma asserção de fé — o programa diz "trate isso como User", mas em runtime pode ser literalmente qualquer coisa.

A consequência aparece nos pontos de contato com a API. `const user = await res.json()` com `user: User` declarado dá autocomplete em `user.name`, mas se a API mudar a chave para `fullName`, o TS continua compilando, o autocomplete continua funcionando, e em runtime `user.name` é `undefined` — bug silencioso que só aparece quando alguém testa aquele fluxo. Multiplique por dezenas de endpoints, por mudanças de schema durante desenvolvimento, por respostas de erro com shape diferente do sucesso, e o sistema de tipos perde valor exatamente nos pontos onde mais importava.

A solução em 2026 é a mesma que para formulários (ver [[10 - Tipando formulários]]): **validação runtime no boundary**. Defina um schema Zod descrevendo a forma esperada da resposta; derive o tipo TS via `z.infer<typeof schema>`; valide a resposta com `schema.parse(json)` (ou `safeParse`) antes de devolver. O tipo deixa de ser uma asserção e passa a ser uma garantia: se `parse` retornou, o dado bate com o schema; se não bate, lança um `ZodError` que o error boundary captura e o usuário vê uma mensagem de erro em vez de um crash silencioso na renderização.

A integração com `useQuery` é natural. O `queryFn` é a função que faz o fetch — ali dentro, a validação acontece, e o tipo do retorno do `queryFn` se torna o tipo do `data` que o hook expõe. O caller do `useQuery` consome `data: User | undefined`, e se a promessa de schema foi cumprida, `User` é o que está lá quando `data` não é `undefined`. O mesmo pattern serve a `use()` (a Promise interna valida) e a Server Actions (validação no servidor antes de retornar).

A discriminated union de `status` na TanStack Query é a outra metade da equação. Em vez de três flags paralelas (`isLoading`, `isError`, `isSuccess`) que permitiriam estados impossíveis (loading com data populado, error com data presente — ver a discussão em [[09 - Tipando reducers e state machines]]), o status é um único valor literal e `data` / `error` são opcionais ou não conforme o variant. Um `switch (query.status)` narroweia automaticamente: dentro do `case 'success'`, `query.data` é `T` (não `T | undefined`); dentro do `case 'error'`, `query.error` é `Error` (não `Error | null`). A discriminação no tipo elimina renderizações inválidas em compile time.

## Como funciona

### Sample 1 — `useQuery` com inferência de `queryFn`

```typescript
import { useQuery } from '@tanstack/react-query';

declare function fetchUser(id: string): Promise<User>;

function UserView({ id }: { id: string }) {
  const { data, error, isLoading, isError } = useQuery({
    queryKey: ['user', id],
    queryFn: () => fetchUser(id),
  });
  // data: User | undefined  (inferido do return de queryFn)
  // error: Error | null     (default da TanStack)
  // isLoading: boolean

  if (isLoading) return <Spinner />;
  if (isError) return <ErrorMessage error={error} />;
  if (!data) return null;

  return <UserCard user={data} />;
}
```

`useQuery` é genérico em duas posições: `useQuery<TData, TError, TSelectFn, TQueryKey>`. Em 99% dos casos não declaramos generics manualmente — TanStack infere `TData` do tipo de retorno do `queryFn` e usa `Error` como default para `TError`. Por isso o ponto crítico é tipar o `queryFn` corretamente: se `fetchUser` retorna `Promise<User>`, `data` é `User | undefined`. Se a função retorna `Promise<any>` (caso comum quando se chama `fetch` direto sem validar), `data` vira `any` e a tipagem do componente desmorona silenciosamente.

A presença de `undefined` no tipo de `data` não é gratuita: enquanto a query está pendente, ainda não há dado. As três flags (`isLoading`, `isError`, `isSuccess`) servem como discriminadores manuais — checá-las narroweia `data` para `User` no ramo de sucesso. O Sample 3 mostra a forma idiomática usando `status` direto, que é a abordagem recomendada da própria TanStack.

### Sample 2 — Validação runtime com Zod no boundary

```typescript
import { z } from 'zod';

const userSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
});

type User = z.infer<typeof userSchema>;

async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const json: unknown = await res.json();
  return userSchema.parse(json);  // throws se shape inválido — error boundary tipado
}

// Em useQuery:
const { data } = useQuery({ queryKey: ['user', id], queryFn: () => fetchUser(id) });
// data: User | undefined  (User vem do schema, não de cast manual)
```

O ponto-chave é a anotação `const json: unknown = await res.json()`. Sem ela, `json` seria `any` e qualquer cast subsequente passaria silenciosamente. Com `unknown`, o TS recusa qualquer acesso a propriedade até que o tipo seja narrowed — e a única forma idiomática de narrow é validar runtime (Zod, Valibot, ou um type guard escrito à mão). `userSchema.parse(json)` faz exatamente isso: lança `ZodError` se o shape não bater, ou retorna o valor tipado como `User` se bater.

O `User` derivado por `z.infer<typeof userSchema>` é a mesma fonte que o `useQuery` enxerga. Adicionar um campo no schema (`avatar: z.string().url()`) atualiza automaticamente o tipo `User`, atualiza o tipo de `data` em todo lugar que consome a query, e atualiza a validação runtime — sem três edições manuais e sem possibilidade de divergência. Esse é o ganho que justifica adotar Zod no projeto inteiro: o schema vira a fonte única, exatamente como em [[10 - Tipando formulários]].

O `throw` dentro do `queryFn` é o canal que TanStack Query usa para popular `query.error`. A validação Zod participa naturalmente desse mecanismo: schema inválido lança `ZodError`, que vira `query.error`, que pode ser checado e renderizado como erro no componente — sem código de plumbing.

### Sample 3 — Status discriminado da TanStack Query

```typescript
const query = useQuery({
  queryKey: ['user', id],
  queryFn: () => fetchUser(id),
});

// query.status: 'pending' | 'success' | 'error'
// query.fetchStatus: 'idle' | 'fetching' | 'paused'

switch (query.status) {
  case 'pending': return <Spinner />;
  case 'error':   return <ErrorMessage error={query.error} />;  // narrowed
  case 'success': return <UserCard user={query.data} />;        // narrowed: data é User (não User | undefined)
}
```

`query` é tipado como uma discriminated union: cada valor de `status` corresponde a um variant onde `data` e `error` têm tipos diferentes. No `case 'success'`, o TS sabe que `data` está populado e estreita o tipo para `User` (sem `| undefined`). No `case 'error'`, `error` é estreitado para `Error` (sem `| null`). No `case 'pending'`, ambos são opcionais.

O `switch` exhaustivo sobre `query.status` é a forma idiomática recomendada pela própria documentação da TanStack — equivalente ao pattern de state machine descrito em [[09 - Tipando reducers e state machines]] aplicado a fetching. A diferença em relação a checar `isLoading`/`isError`/`isSuccess` separadamente é prática: o switch força o desenvolvedor a tratar todos os casos, o TS narroweia automaticamente em cada ramo, e adicionar um exhaustiveness check com `default: const _: never = query` aponta em compile time qualquer caso esquecido se a TanStack adicionar um novo `status` no futuro.

Vale notar a separação entre `status` e `fetchStatus`. O `status` descreve o resultado da query (temos dado? temos erro? estamos esperando o primeiro?); o `fetchStatus` descreve a operação de rede no momento (estamos buscando? pausados por offline?). Uma query pode estar em `status: 'success'` (já temos dados em cache) e `fetchStatus: 'fetching'` (estamos revalidando em background). A discriminada do `status` cobre o caso comum; quando precisar do detalhe, `fetchStatus` está disponível.

### Sample 4 — `use()` com Suspense (React 19)

```typescript
import { Suspense, use } from 'react';

declare function fetchUser(id: string): Promise<User>;

function UserProfile({ promise }: { promise: Promise<User> }) {
  const user = use(promise);  // user: User (não User | undefined — Suspense lida com loading)
  return <h1>{user.name}</h1>;
}

function App() {
  const userPromise = fetchUser('42');  // Promise<User>
  return (
    <Suspense fallback={<Spinner />}>
      <UserProfile promise={userPromise} />
    </Suspense>
  );
}
```

O hook `use()` aceita `Promise<T>` e retorna `T` diretamente. Não há `undefined` no tipo de retorno: se a Promise está pendente, o componente suspende e o `<Suspense>` mais próximo na árvore renderiza o `fallback`; se rejeita, o error boundary mais próximo captura. O componente que chama `use()` só é renderizado quando os dados estão prontos, então `user` é `User`, ponto.

A diferença de superfície em relação a `useQuery` é grande. No modelo de query hook, o componente convive com os três estados (`isLoading`, `isError`, `data | undefined`) e renderiza variações; no modelo Suspense, o componente é "puro" — assume que os dados existem e os boundaries de loading/erro vivem acima dele. A árvore vira mais declarativa, mas a coordenação de loading state é arquitetural: `<Suspense>` precisa estar na altura certa para que o fallback faça sentido (envolver muito gera flash global; envolver de menos quebra streaming).

O ponto crítico de tipagem é a estabilidade da Promise. `use()` lê a Promise por referência: se a função renderizar e criar uma nova Promise a cada render (`const promise = fetchUser(id)` dentro do componente), o componente entra em loop de suspensão. A forma idiomática é criar a Promise em Server Component e passá-la como prop — o RSC executa uma vez, a Promise serializa para o client, e o componente client a consome via `use()`. Em SPAs sem RSC, a Promise precisa vir de um cache (TanStack Query expõe `useSuspenseQuery` exatamente para esse caso) ou ser memoizada com cuidado.

`useSuspenseQuery` da TanStack Query é a ponte entre os dois modelos: API idêntica a `useQuery`, mas a Promise é gerenciada pelo cache da biblioteca, e o tipo de `data` é `T` (não `T | undefined`) porque o componente só renderiza após resolver. É o melhor dos dois mundos quando o app já usa TanStack e quer adotar Suspense.

### Sample 5 — Server Action tipada (Next.js 16)

```typescript
// app/actions/user.ts
'use server';

import { z } from 'zod';

const updateUserSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
});

export async function updateUser(input: z.infer<typeof updateUserSchema>) {
  const data = updateUserSchema.parse(input);  // validação runtime
  await db.user.update({ where: { id: data.id }, data: { name: data.name } });
  return { success: true };
}

// app/components/UserForm.tsx
'use client';

import { updateUser } from '@/app/actions/user';

function UserForm({ id }: { id: string }) {
  return (
    <form action={async (formData) => {
      const name = formData.get('name') as string;
      await updateUser({ id, name });  // tipo inferido da assinatura do server action
    }}>
      <input name="name" />
      <button type="submit">Save</button>
    </form>
  );
}
```

A diretiva `'use server'` no topo do arquivo marca todas as funções exportadas como Server Actions. No client component, `import { updateUser } from '@/app/actions/user'` traz uma referência tipada — Next/React substituem a função em build time por um stub que serializa argumentos, faz POST para o servidor e devolve o retorno serializado. Do ponto de vista do TypeScript, a chamada é igual a chamar uma função local: o tipo dos argumentos e o tipo do retorno são os declarados na função do servidor.

A inferência cruzar a fronteira cliente-servidor é o ganho principal. Sem Server Actions, o pattern era declarar manualmente o contrato (`POST /api/users/:id`, body `{ name: string }`, retorno `{ success: boolean }`) em três lugares — handler do servidor, código do client, eventual tipo compartilhado — e manter os três sincronizados. Com Server Action, há uma única função tipada; renomear o argumento ou adicionar campo atualiza ambos os lados em uma edição.

O detalhe que costuma escapar: **o tipo da assinatura não substitui validação runtime**. O TS confia que `input` é `{ id: string; name: string }`, mas o que chega no servidor é JSON deserializado de um POST — pode ter sido manipulado, pode ter campos a mais, pode ter tipos errados. `updateUserSchema.parse(input)` na primeira linha da função é o que transforma a confiança do tipo em garantia de runtime. Sem isso, um cliente hostil pode passar `id: 123` (number) e a função aceita até quebrar no Prisma.

A integração com `<form action={...}>` é a outra ponta. O atributo `action` aceita uma função assíncrona que recebe `FormData`; chamar a Server Action a partir dela funciona em progressive enhancement (o form submete via POST nativo se JS estiver desabilitado). Para forms mais ricos, `useActionState` (React 19) ou `useFormState` (deprecated alias) gerenciam o estado entre submissões, e `useFormStatus` expõe `pending` para feedback visual.

### Sample 6 — Result type pattern para erros explícitos

```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function fetchUserSafe(id: string): Promise<Result<User>> {
  try {
    const user = await fetchUser(id);
    return { ok: true, value: user };
  } catch (e) {
    return { ok: false, error: e instanceof Error ? e : new Error(String(e)) };
  }
}

// Caller é forçado a lidar com erro:
const result = await fetchUserSafe('42');
if (result.ok) {
  console.log(result.value.name);
} else {
  console.error(result.error.message);
}
// vs throw — caller pode esquecer try/catch
```

O `Result<T, E>` é uma discriminated union (mesmo pattern de [[09 - Tipando reducers e state machines]]) que torna o erro parte do tipo de retorno em vez de algo lançado. A diferença prática é que o caller **precisa** checar `result.ok` antes de acessar `result.value`: tentar `result.value` direto é erro de compilação porque a propriedade `value` só existe no variant `{ ok: true; ... }`. Comparado com `throw`, onde nada no tipo de retorno indica que a função pode falhar, o caller tem garantia em compile time de que tratou o caso de erro.

O custo é a verbosidade no caller (precisa do `if`/`switch` para narrow) e a perda da composição idiomática com `await throw` em chains de operações. O ganho aparece em camadas críticas: server actions que retornam para o client, hooks que expõem dados a múltiplos consumers, funções de domínio onde "pode falhar com erro X específico" é parte do contrato. TanStack Query usa internamente um modelo similar — `query.status === 'error'` é o narrow que dá acesso ao `error`, e `query.error` não existe no `case 'success'`.

A escolha entre `throw` e `Result` é arquitetural, não estilística. `throw` cabe quando o erro é genuinamente excepcional e não modelado no domínio (rede caiu, banco fora do ar); `Result` cabe quando o erro **é** parte do domínio (usuário não encontrado, validação falhou, permissão negada). Em React + TypeScript, server actions são os candidatos mais naturais para `Result` — o erro precisa cruzar a rede e ser apresentado ao usuário, então modelá-lo como dado é mais robusto que confiar no error boundary capturar uma exceção serializada.

## Na prática

O pattern mais robusto para data fetching em apps React + TypeScript em 2026 é **Zod schema no boundary do fetch**, com `useQuery` consumindo a função validada. O fluxo concreto: o schema vive em um arquivo compartilhado (`shared/schemas/user.ts` exportando `userSchema` e `type User = z.infer<typeof userSchema>`); a função de fetch (`fetchUser` em `api/user.ts`) chama `fetch`, anota o `await res.json()` como `unknown`, valida com `userSchema.parse` e retorna `User`; o `useQuery` no componente passa `fetchUser` como `queryFn` e recebe `data: User | undefined` automaticamente. Esse é o mesmo schema que o backend usa para validar input nas rotas, exatamente como em [[10 - Tipando formulários]] — uma fonte única, três consumidores (form, fetch client, validação server).

Para mutações, o equivalente é `useMutation`. A API espelha `useQuery`: `mutationFn` é a função que faz o POST/PUT/DELETE, `useMutation` retorna `{ mutate, mutateAsync, status, error, data }`, e o tipo de `data` vem do retorno da `mutationFn`. O pattern combinado com forms é `useForm` (RHF) chamando `mutate` no submit handler, com o mesmo schema Zod servindo `zodResolver` do form e validação do body no fetch. Em React 19 + Next 16, parte desses casos se desloca para Server Actions: forms simples (criar, editar, deletar) podem ir direto via `<form action={serverAction}>` sem `useMutation`. TanStack Query continua valendo quando há cache compartilhado, otimistic updates ou invalidação fina por chave.

A escolha entre `useQuery` e `use()` + Suspense não é exclusiva. TanStack expõe `useSuspenseQuery` que combina os dois: cache da biblioteca, mas o tipo de `data` é `T` em vez de `T | undefined`, e a renderização é gated por `<Suspense>`. O componente fica mais simples (sem checagens de loading), mas o fallback global precisa ser desenhado com cuidado para não regredir UX. A heurística pragmática: comece com `useQuery` (mais explícito sobre os estados); migre para `useSuspenseQuery` quando os boundaries naturais da árvore já existirem e o componente puder assumir os dados.

## Armadilhas

- **`data` é `T | undefined` em `useQuery` (loading), confundir com Suspense onde é sempre `T`.** No `useQuery` clássico, o componente é renderizado durante o loading e `data` é `undefined`. Tentar `data.name` direto é erro de TS (e crash em runtime). A regra: ou checa `isLoading`/`status === 'success'` antes, ou usa `useSuspenseQuery` que não retorna `undefined`. Isso vale também para `use()` em React 19: lá `user = use(promise)` é `User` direto. Misturar mentalmente os dois modelos gera bugs em que o desenvolvedor esquece de tratar `undefined` no caminho não-Suspense ou tenta tratar `undefined` que não existe no caminho Suspense.

- **`error` é `Error | null` (não throw) — caller precisa checar.** TanStack Query **não relança** o erro do `queryFn`: ela captura, popula `query.error` e expõe via render. O componente que assume `try/catch` em volta do `useQuery` está enganado — não há nada para capturar, porque o erro vira dado. Esquecer de checar `isError` ou `status === 'error'` faz o componente renderizar com `data: undefined` e nenhuma indicação de falha; o usuário vê o spinner sumir e nada aparecer. A regra: em todo `useQuery`, o render trata explicitamente os três casos (pending, error, success), idealmente via `switch (query.status)`.

- **Confundir `useQuery` com `useSuspenseQuery`.** As assinaturas são quase idênticas, mas `useSuspenseQuery` não retorna `undefined` em `data` (Suspense cuida do loading) e não retorna `error` (error boundary cuida da falha). Componentes que usam `useSuspenseQuery` mas ainda checam `isLoading` no render estão fazendo trabalho duplicado — pior, se os boundaries não existirem na árvore acima, o app trava no fallback raiz. A regra: ao escolher `useSuspenseQuery`, garanta `<Suspense>` e `<ErrorBoundary>` na altura adequada antes de remover as checagens manuais.

- **Não validar runtime — `fetch` + `await res.json()` retorna `any` se não anotar.** Esta é a armadilha mais comum e mais cara. `await res.json()` tem tipo `Promise<any>` no lib.dom — qualquer cast subsequente passa silenciosamente. Anotar `: User` na variável dá autocomplete falso e bug em produção quando a API muda. A regra inflexível: anote o resultado de `res.json()` como `unknown`, e o único caminho de saída é validação runtime (Zod, Valibot, type guard escrito à mão). O TS forçará o desenvolvedor a passar pela validação porque acessar propriedade em `unknown` é erro de compilação.

- **Server Actions em Next 16 ainda exigem validação runtime do input.** O tipo da assinatura (`function updateUser(input: { id: string; name: string })`) é compile-time only. O que chega no servidor é JSON deserializado de um POST — pode ter sido manipulado por cliente hostil, pode ter chegado com tipos errados. Confiar no tipo da assinatura sem validar com `schema.parse(input)` na primeira linha da função é deixar a porta aberta. A regra: toda Server Action começa com validação runtime do input, mesmo que o client "garante" enviar o formato certo — o servidor não confia no client.

- **Criar a Promise dentro do componente client e passar para `use()`.** `use(fetchUser(id))` chamado dentro do render cria uma nova Promise a cada render, e o componente entra em loop de suspensão. A regra: a Promise tem que ser estável entre renders. Em RSC + client, crie no Server Component e passe como prop; em SPA, use `useSuspenseQuery` (TanStack gerencia a estabilidade) ou memoize com `useMemo` cuidadoso considerando as dependências.

## Em entrevista

> "Data fetching in React with TypeScript has three patterns I use depending on the context. For client-side cached fetching, I use TanStack Query — `useQuery<TData>` infers from the `queryFn` return, and the discriminated `status` field forces narrowing in the render. For Suspense-driven fetching, the `use()` hook in React 19 unwraps a Promise — `data` becomes `T` directly, and the loading state is handled by `<Suspense>` higher up. For server-driven mutations, Server Actions in Next.js 16 are typed functions called directly from the client, with the type derived from the server function's signature. The critical thing across all three: TypeScript is compile-time only. Anything coming from the network — fetch responses, FormData, query params — needs runtime validation, usually with Zod, before I trust the type. The schema is the single source of truth: the runtime validates, and the type is derived from the schema, so they can't drift apart."

**Vocabulário-chave:** *queryFn inference*, *runtime validation*, *Suspense boundary*, *server action*, *result type*.

## Veja também

- [[07 - Tipando hooks customizados]] — useQuery é o exemplo canônico de hook genérico
- [[09 - Tipando reducers e state machines]] — discriminated `status` da TanStack Query
- [[10 - Tipando formulários]] — schema Zod compartilhado entre form e fetch
- [[TypeScript]] — seção "Runtime validation — Zod"
