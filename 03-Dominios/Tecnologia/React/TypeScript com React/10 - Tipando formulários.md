---
title: "Tipando formulários"
created: 2026-04-26
updated: 2026-04-26
type: concept
progress: backlog
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, forms, validation, react-hook-form, zod]
aliases:
  - Formulários tipados em React
  - RHF + Zod
---

# Tipando formulários

> [!abstract] TL;DR
> Schema-driven typing: declare schema Zod, derive tipo TS via `z.infer<typeof schema>`. Integre com React Hook Form via `zodResolver`. Erros viram um objeto tipado em `formState.errors` com a mesma forma do schema. Controlled inputs usam `value`/`onChange`; uncontrolled (mais idiomático em RHF) usam `register`. O schema vira a *single source of truth* — runtime validation + tipo TS derivado.

## O que é

Um formulário em React é a interseção de três fontes de tipo distintas que precisam permanecer sincronizadas. **A primeira é o schema**: o contrato que descreve quais campos existem, quais tipos têm e quais regras de validação se aplicam (email tem que ser email, password tem mínimo de 8 caracteres, age é opcional). **A segunda são os event handlers**: o `onChange` de um `<input>` recebe `React.ChangeEvent<HTMLInputElement>` e expõe `e.target.value: string`, mas formulários ricos têm checkbox (`boolean`), select (string com union de literais), radio (literal), file (`FileList`). **A terceira é o state**: o lugar onde os valores vivem entre renders — pode ser `useState` por campo, um único `useState` com um objeto, um `useReducer`, ou totalmente abstraído por uma biblioteca.

Tipar um form do zero significa declarar o tipo TS dos valores, declarar separadamente as regras de validação (frequentemente como `if`s manuais ou um schema de outra biblioteca), e manter os dois alinhados manualmente. Cada vez que um campo é adicionado, removido ou renomeado, o programador precisa lembrar de atualizar **dois** lugares — o tipo e a validação. Esquecer um deles gera bugs silenciosos: o TS continua compilando porque o tipo declarado não mudou, mas o schema valida algo diferente, e a UI mostra erros que não correspondem aos campos reais.

A solução idiomática em 2026 é **schema-driven typing**: declare um schema Zod, e derive o tipo TS dele via `z.infer<typeof schema>`. O schema vira a única fonte de verdade — runtime validation e tipo TS saem do mesmo objeto, e por construção não podem divergir. React Hook Form (RHF) integra esse modelo via `zodResolver`: o resolver chama o schema na submissão, e os erros aparecem em `formState.errors` com a mesma forma do schema. Adicione um campo no schema, o tipo TS atualiza, o resolver passa a validar, e o objeto `errors` ganha a entrada correspondente — tudo em uma edição.

## Por que importa

TypeScript é um sistema de tipos estritamente compile-time. No momento em que o código roda, todos os tipos foram apagados — o JavaScript executado não sabe o que era um `User`, o que era `string` ou o que era `'admin' | 'user' | 'guest'`. Para dados que vêm de fora do programa (input de usuário em formulários, resposta de API, `localStorage`, query params), o tipo declarado é uma **expectativa**, não uma garantia. Se o usuário digitar texto onde o tipo declara `number`, ou se um campo obrigatório vier vazio, o programa entra em estado inválido sem que o compilador tenha como avisar.

A consequência prática é que formulários precisam de duas coisas distintas que muitos times tratam como uma só: um **tipo** TS para o valor (que dá autocomplete e checagem estática) e uma **validação runtime** que confirma a forma do dado quando ele chega. Sem validação runtime, o `data` que sai de `handleSubmit` é uma asserção de fé — o TS diz que é `UserForm`, mas em runtime pode ser qualquer coisa. Adicionar validação manual (com um pacote separado, ou ifs no submit) introduz o problema oposto: o tipo declarado e o validador são objetos independentes, e mudar um sem mudar o outro é silencioso.

A duplicação de contrato é o problema concreto. Considere um form com 8 campos: declarar `type UserForm = { ... }` e separadamente um `userValidator = { email: validateEmail, password: validateLength(8), ... }` cria duas estruturas que precisam combinar campo a campo. Adicionar um nono campo exige edição em dois lugares; renomear um campo exige edição em dois lugares; mudar um tipo de `string` para `'a' | 'b'` exige edição em dois lugares. Cada esquecimento é um bug — e o tipo de bug que não aparece em compile time porque o TS só sabe da declaração, não da validação.

`z.infer` resolve isso por construção. O schema Zod é um valor JS que descreve a forma e as regras; `z.infer<typeof schema>` é uma operação puramente type-level que extrai o tipo TS correspondente sem custo de runtime. Adicione um campo ao schema e o tipo derivado ganha esse campo automaticamente; remova um campo e o tipo perde aquela entrada; mude `z.string()` para `z.string().email()` e o tipo continua `string` (porque o tipo TS não distingue email de string qualquer), mas a validação runtime passa a checar o formato. **O contrato vive uma vez, em um lugar.**

## Como funciona

### Sample 1 — Schema Zod + `z.infer`

```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  age: z.number().int().positive().optional(),
  role: z.enum(['admin', 'user', 'guest']),
});

type UserForm = z.infer<typeof userSchema>;
// {
//   email: string;
//   password: string;
//   age?: number;
//   role: 'admin' | 'user' | 'guest';
// }
// — derivado do schema, não declarado manualmente
```

Pontos a notar:

- `z.infer<typeof userSchema>` é uma operação type-level: zero custo em runtime, apenas extrai o tipo do schema.
- `z.string().email()` continua sendo `string` no tipo TS (TS não tem tipo "email"), mas a validação runtime checa o formato. O tipo é mais permissivo que o validador — o oposto seria pior.
- `.optional()` adiciona `?` no tipo derivado; `.enum([...])` produz uma union de literais; `.int().positive()` continua sendo `number` no tipo (essas são checagens runtime).
- Mudanças no schema (adicionar/remover/renomear/retipar campos) propagam automaticamente para `UserForm`. Não há possibilidade de divergência.

### Sample 2 — Setup RHF + zodResolver

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

function UserFormComponent() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<UserForm>({
    resolver: zodResolver(userSchema),
    defaultValues: {
      email: '',
      password: '',
      role: 'user',
    },
  });

  const onSubmit = (data: UserForm) => {
    // data é tipado como UserForm — garantido pelo resolver
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="password" {...register('password')} />
      {errors.password && <span>{errors.password.message}</span>}

      <select {...register('role')}>
        <option value="admin">Admin</option>
        <option value="user">User</option>
        <option value="guest">Guest</option>
      </select>
      {errors.role && <span>{errors.role.message}</span>}

      <button type="submit" disabled={isSubmitting}>Submit</button>
    </form>
  );
}
```

`useForm<UserForm>` parametriza o hook com o tipo dos valores. A partir desse generic, `register` aceita apenas nomes de campo válidos (`'email' | 'password' | 'age' | 'role'` — typo é compile error), `errors` ganha a forma derivada de `UserForm`, e o `data` recebido em `onSubmit` é tipado como `UserForm`. O `resolver: zodResolver(userSchema)` conecta a validação runtime: antes de chamar `onSubmit`, RHF roda o schema; se falhar, popula `errors` em vez de submeter.

### Sample 3 — Errors como objeto tipado

```typescript
// errors tem tipo derivado:
// {
//   email?: { message?: string; type: string; ... };
//   password?: { message?: string; type: string; ... };
//   age?: { ... };
//   role?: { ... };
// }
// Cada campo é opcional — só aparece quando há erro

// Acesso seguro com optional chaining:
errors.email?.message     // string | undefined
errors.password?.message  // string | undefined
errors.age?.message       // string | undefined
errors.role?.message      // string | undefined

// Typo é erro de compilação, não silêncio:
errors.emial?.message     // ERRO: Property 'emial' does not exist on type ...
```

A forma do `errors` espelha a forma do `UserForm`: cada campo do form vira uma entrada opcional em `errors`, contendo (entre outros) `message` (string preenchida pelo schema) e `type` (qual regra falhou). Como cada entrada é opcional, o acesso idiomático é via optional chaining (`errors.email?.message`), que retorna `string | undefined`. Renderizar isso em JSX (`{errors.email?.message}`) é seguro: `undefined` não vira nada na árvore.

Para schemas aninhados (`z.object({ address: z.object({ city: z.string() }) })`), `errors.address?.city?.message` segue a mesma estrutura. Para arrays (`z.array(z.string())`), `errors.tags?.[0]?.message` indexa por posição.

### Sample 4 — Controlled vs uncontrolled (e quando cada faz sentido)

```typescript
// Controlled — useState manual, value+onChange
function ControlledInput() {
  const [value, setValue] = useState('');
  return (
    <input
      value={value}
      onChange={(e: React.ChangeEvent<HTMLInputElement>) => setValue(e.target.value)}
    />
  );
}

// Uncontrolled (RHF idiomático) — register, sem useState
function UncontrolledInput() {
  const { register } = useForm<{ name: string }>();
  return <input {...register('name')} />;
}

// RHF prefere uncontrolled porque:
// - Menos re-renders (input mantém estado próprio no DOM)
// - APIs mais simples (sem useState manual)
// - Performance: form com 50 campos não re-renderiza tudo a cada keystroke

// Quando controlled ainda faz sentido:
// - Componentes externos que só aceitam value/onChange (date pickers, comboboxes
//   de UI libraries que não respeitam refs) — RHF expõe <Controller /> para isso.
// - Validação ou formatação síncrona durante a digitação (mascarar telefone,
//   normalizar caixa).
// - Quando o valor de um campo precisa renderizar partes diferentes da UI
//   instantaneamente (toggle que mostra/esconde outro campo).
```

A diferença não é estilística. Em **controlled**, cada keystroke vira `setState`, que vira re-render. Em um form pequeno, é trivial. Em forms com 30-50 campos, ou com validação síncrona pesada, o custo aparece. Em **uncontrolled**, o `<input>` mantém o valor próprio no DOM, e RHF lê via `ref` apenas quando precisa (no submit, ou em watches específicos). A consequência: digitar em um campo não re-renderiza os outros 49.

`<Controller />` é a ponte oficial: dentro dele, o componente filho recebe `value` e `onChange` (estilo controlled) mas o valor continua gerenciado por RHF. É o jeito certo de integrar componentes de UI library (Material UI, Mantine, Radix) que não expõem ref ou que insistem em controlled.

### Sample 5 — Schema compartilhado com backend

```typescript
// shared/schemas/user.ts
import { z } from 'zod';

export const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});
export type User = z.infer<typeof userSchema>;

// Frontend (React Hook Form)
import { userSchema, type User } from '@shared/schemas/user';
const form = useForm<User>({ resolver: zodResolver(userSchema) });

// Backend (Express, Fastify, Hono — qualquer um)
import { userSchema } from '@shared/schemas/user';
app.post('/users', (req, res) => {
  const result = userSchema.safeParse(req.body);
  if (!result.success) return res.status(400).json(result.error);
  // result.data é User (tipo idêntico ao do frontend)
  saveUser(result.data);
  res.status(201).json({ ok: true });
});

// Mesma source of truth — schema vive uma vez, tipo é derivado dos dois lados
```

Esse é o ganho que justifica o custo de adotar Zod em primeiro lugar. O frontend valida o input no submit; o backend valida o body recebido (porque clientes hostis ou bugados existem); e os dois validam **a mesma coisa**. Adicionar um campo no schema atualiza o form, atualiza o tipo `User` em todos os lugares que importam, e atualiza o validador do endpoint — em uma edição. O contrato é enforced end-to-end, não via documentação.

`safeParse` retorna `{ success: true, data: T } | { success: false, error: ZodError }` — uma discriminated union (ver [[09 - Tipando reducers e state machines]]) que força o consumer a checar `success` antes de acessar `data` ou `error`. Em runtimes onde lançar exceções é caro (edge functions, RSC), `safeParse` é preferível a `parse`. Em scripts de desenvolvimento ou onde o erro é fatal, `parse` é mais conciso.

## Na prática

A configuração que mais escala em projetos médios e grandes é **schema em arquivo separado, importado pelo form e pelo backend**. O schema mora em `shared/schemas/<dominio>.ts` (ou um pacote `@org/schemas` em monorepo), exporta tanto o objeto Zod quanto o tipo derivado, e é a única origem de ambos. Forms importam o schema para o `zodResolver`; mutações importam o tipo para tipar o body; endpoints importam o schema para validar o input. Quando o domínio cresce, schemas se compõem (`userSchema.extend({ ... })`, `z.intersection`, `z.discriminatedUnion`) e os tipos derivados continuam alinhados.

**TanStack Form** (também conhecido como `@tanstack/react-form`) é uma alternativa moderna a RHF que ganhou tração desde 2024. O design parte de um princípio diferente: em vez de delegar tipos para um generic em `useForm<T>`, TanStack Form infere o tipo a partir do `defaultValues` e do schema, sem precisar declarar o tipo separadamente. Para schemas aninhados profundos ou unions complexas, a inferência do TanStack Form costuma ser mais granular que a do RHF. RHF continua sendo a escolha mais popular em 2026 pela base de adoção e pela quantidade de integrações prontas; TanStack Form é uma escolha defensável para projetos novos que querem inferência mais agressiva.

Forms multi-step (wizards, checkout em fases) merecem tratamento específico: cada step tem campos diferentes, validações diferentes e transições explícitas (avançar, voltar, pular). Modelar o fluxo de steps como state machine — a abordagem da [[09 - Tipando reducers e state machines]] — separa a lógica de "qual step está ativo" da lógica de "valores do form". Cada step vira um sub-schema (`step1Schema`, `step2Schema`), o schema final é a interseção (`step1Schema.merge(step2Schema)`), e a state machine controla a navegação. RHF expõe `trigger` para validar campos sob demanda (útil ao avançar de step), e `getValues` para inspecionar valores atuais sem causar re-render.

## Armadilhas

- **Declarar tipos manuais em vez de `z.infer`.** O padrão tentador é escrever `type UserForm = { email: string; password: string; ... }` e separadamente um `userSchema` Zod com as mesmas chaves. O tipo declarado e o schema viram dois objetos independentes que precisam combinar campo a campo, e qualquer mudança em um sem o outro é silenciosa em compile time. A regra: se existe um schema, o tipo é `z.infer<typeof schema>` — sempre, sem exceção. Tipo declarado manualmente só faz sentido quando não existe schema (forms triviais sem validação runtime).

- **`register` com nome errado vira string sem detecção de TS.** `register('emial')` em vez de `register('email')` pode passar silenciosamente se o `useForm` não estiver parametrizado com o generic. RHF declara `register` aceitando `Path<TFieldValues>` — sem o generic, `TFieldValues` é `FieldValues` (qualquer coisa) e qualquer string passa. **Sempre** parametrize: `useForm<UserForm>({ ... })`. Com o generic, `register` só aceita os nomes válidos do tipo, e o typo vira erro de compilação imediato.

- **Usar Yup em vez de Zod em projetos novos.** Yup foi a escolha dominante até ~2022, mas a inferência de tipos é menos precisa que a de Zod (especialmente com schemas aninhados ou condicionais), e exige declarar tipos manualmente em muitos casos. Em 2026, Zod é a escolha padrão para TS, com Valibot como alternativa quando bundle size importa muito. Yup só faz sentido em projetos legados que já o usam — adotar Yup hoje significa abrir mão da inferência mais forte sem ganho compensatório.

- **Misturar controlled e uncontrolled no mesmo form sem critério.** Inputs nativos com `register` (uncontrolled) e date pickers de UI library com `useState + onChange` (controlled) coexistem se necessário, mas o estado fica espalhado: parte em RHF, parte em useState locais. Submeter exige juntar manualmente; resetar exige resetar nos dois lugares. A regra: use `<Controller />` para os campos que precisam ser controlled, mantendo todo o estado dentro do RHF. Se o form todo precisa ser controlled (caso raro), considere se RHF é a ferramenta certa — pode ser que `useState` direto seja mais simples.

- **Esquecer `defaultValues` no RHF.** Sem `defaultValues`, campos uncontrolled começam como `undefined`, o que gera o warning clássico do React: "A component is changing an uncontrolled input to be controlled". A regra: declare `defaultValues` cobrindo **todos** os campos do form, mesmo que com strings vazias e zeros. Para schemas com campos opcionais, ainda assim defina o default (`age: undefined` é explícito, `''` para strings opcionais costuma ser mais simples). Sem isso, debug fica frustrante porque o warning não aponta o campo culpado.

- **Validar no `onChange` em vez do `onSubmit` por padrão.** RHF aceita `mode: 'onChange'` (validar a cada digitação), mas o default é `'onSubmit'` (validar só ao submeter) por boa razão: validar enquanto o usuário ainda está preenchendo gera erros prematuros ("email inválido" antes do usuário terminar de digitar). O modo `'onTouched'` ou `'onBlur'` costuma ser o ponto certo: valida quando o usuário sai do campo, sem incomodar durante a digitação. `onChange` só faz sentido após o primeiro erro daquele campo (RHF chama isso de `reValidateMode: 'onChange'`).

## Em entrevista

> "For forms in React with TypeScript, my pattern is schema-driven: declare a Zod schema, derive the TypeScript type with `z.infer<typeof schema>`, and integrate with React Hook Form via `zodResolver`. The schema becomes the single source of truth — runtime validation and the type both come from the same place, so they can't drift apart. Errors live in `formState.errors` as an object that mirrors the schema shape, and I access individual messages via optional chaining like `errors.email?.message`. RHF prefers uncontrolled inputs via `register` — fewer re-renders than controlled, and the API is simpler. The same schema can live in a shared package and validate the same payload on the server, so the form's contract is enforced end-to-end."

**Vocabulário-chave:** *schema-driven typing*, *`z.infer`*, *resolver*, *uncontrolled input*, *single source of truth*.

## Veja também

- [[06 - Tipando event handlers]] — quando você precisa de `onChange` manual (controlled inputs, `<Controller />`)
- [[09 - Tipando reducers e state machines]] — multi-step forms como state machine
- [[11 - Tipando data fetching]] — submit de form via mutação tipada
- [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]] — seção "Runtime validation — Zod"
