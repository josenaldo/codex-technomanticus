---
title: "Polymorphic components com as prop"
created: 2026-04-26
updated: 2026-04-26
type: concept
status: seedling
publish: true
tags: [typescript, react, typescript-react, frontend, polymorphic, as-prop, forwardRef, advanced]
aliases:
  - Polymorphic components React
  - as prop tipada
---

# Polymorphic components com as prop

> [!abstract] TL;DR
> `<Box as="a" href="..." />` precisa que o TS mude as props aceitas conforme `as`. A solução é um generic component que recebe `as: ElementType` e combina com `React.ComponentPropsWithoutRef<typeof as>` para herdar as props nativas do elemento. Em React 18 e libs com `peerDeps` em React 18, o pattern combina com `forwardRef` (e paga o preço de um cast no final, porque `forwardRef` não preserva generics naturalmente). Em React 19, `ref` virou prop normal — `forwardRef` é opcional e a implementação fica mais limpa. O pattern é a base de design systems modernos (Mantine, Radix, MUI).

## O que é

Um *polymorphic component* é um componente que aceita uma prop especial — convencionalmente chamada `as` (Mantine, Chakra) ou `component` (MUI) — que controla **qual elemento HTML ou componente** será renderizado. A magia em TypeScript é que essa prop muda **tanto a tag renderizada quanto o tipo das demais props aceitas** no call site:

- `<Box as="div">` aceita props de `<div>` (`onClick`, `className`, `id`, `style`, ...)
- `<Box as="a">` aceita props de `<a>`, incluindo `href`, `target`, `rel`
- `<Box as="button">` aceita props de `<button>`, incluindo `type="submit"`, `disabled`, `formAction`
- `<Box as={Link}>` (passando um componente externo, como `next/link`) aceita as props do `Link` — `href`, `prefetch`, `replace`, etc.

A `as` aceita dois tipos de valor: **strings** (uma chave de `React.JSX.IntrinsicElements`, ou seja, um nome de tag HTML) ou **componentes** (function/class component). O tipo `React.ElementType` é exatamente a união desses dois mundos — string literal de tag HTML + qualquer componente válido. É a primitiva sobre a qual o pattern todo é construído.

A inferência das props derivadas vem de `React.ComponentPropsWithoutRef<typeof as>` (ou `ComponentProps`, `ComponentPropsWithRef` quando ref entra na conversa): esse helper aceita um `ElementType` e devolve o objeto de props que aquele elemento aceita. Combinado com generic, o componente "transporta" o tipo do elemento escolhido até as props finais — o consumer escreve `<Box as="a" href="/x">` e o TS valida `href` contra `<a>`, não contra alguma interface fixa do `Box`.

## Por que importa

Design systems precisam de componentes reutilizáveis que **mantenham estilos, semântica de design e props customizadas** consistentes, mas variem o elemento HTML renderizado conforme o contexto. Um `<Button>` clicável é, em diferentes lugares, renderizado como:

- `<button type="submit">` — em forms (default)
- `<a href="/dashboard">` — quando navega para outra página (acessibilidade pede `<a>`, não `<button onClick={navigate}>`)
- `<Link to="/dashboard">` — quando o app usa client-side routing (React Router, Next.js, TanStack Router)

Sem polymorphic, três caminhos ruins: (1) reescrever `<Button>` como `<ButtonAsLink>` e `<ButtonAsRouterLink>` separados, duplicando estilos, hover states, focus rings e variantes; (2) renderizar sempre `<button>` e usar `onClick={() => navigate('/x')}`, quebrando acessibilidade e perdendo right-click/middle-click; (3) embrulhar manualmente cada caso (`<a><Button as="span" /></a>`), produzindo HTML inválido e duplicação de eventos.

Com polymorphic, **um** componente `<Button as="a" href="/x">Login</Button>` resolve: estilos do design system, semântica HTML correta, tipo das props validado pelo TS conforme o `as`. O consumer paga zero — escreve uma prop a mais, e o autocomplete do editor mostra `href`, `target`, `rel` quando `as="a"`. O ganho compõe quando o design system tem 30+ componentes — a alternativa "uma duplicata por tag possível" multiplica a superfície mantida em 3-5x sem ganho real.

A complexidade do pattern não é gratuita: a UX do **consumer** é excelente, mas a UX do **mantenedor** do design system é desafiadora — o tipo é um dos mais densos da estrutura React+TS, mensagens de erro ficam barulhentas, e refatoração exige cuidado. É um custo concentrado em poucos arquivos da lib que paga em dezenas de call sites simplificados — o cálculo geralmente fecha.

## Como funciona

### Sample 1 — Versão ingênua (sem inferência correta)

```typescript
// Versão ingênua — bug: aceita href mesmo com as="div"
type BoxProps = {
  as?: React.ElementType;
  children: React.ReactNode;
} & React.HTMLAttributes<HTMLElement>;

function Box({ as: Component = 'div', children, ...rest }: BoxProps) {
  return <Component {...rest}>{children}</Component>;
}

// PROBLEMA:
<Box as="div" href="/foo">conteúdo</Box>  // TS aceita, mas <div> não tem href em runtime
<Box as="a" target="_blank">link</Box>     // TS reclama: 'target' não está em HTMLAttributes<HTMLElement>
```

A versão ingênua falha por dois lados ao mesmo tempo: aceita props inválidas (`href` em `<div>`) e rejeita props válidas (`target` em `<a>`, porque `target` não está em `HTMLAttributes` genérico — é específico de `<a>`). O motivo é que o tipo das props (`HTMLAttributes<HTMLElement>`) é **fixo**, independente do `as` passado. A correção exige que o tipo das props **dependa** do `as` — e é aí que generics entram.

### Sample 2 — `ComponentPropsWithoutRef` resolve a inferência

```typescript
type BoxProps<E extends React.ElementType> = {
  as?: E;
  children?: React.ReactNode;
} & Omit<React.ComponentPropsWithoutRef<E>, 'as' | 'children'>;

// React.ComponentPropsWithoutRef<'a'>      = props nativas de <a>
// React.ComponentPropsWithoutRef<'button'> = props nativas de <button>
// React.ComponentPropsWithoutRef<typeof Link> = props do componente Link

function Box<E extends React.ElementType = 'div'>({
  as,
  children,
  ...rest
}: BoxProps<E>) {
  const Component = as || 'div';
  return <Component {...rest}>{children}</Component>;
}

// AGORA:
<Box as="a" href="/foo">Link</Box>            // ok — href válido em <a>
<Box as="div" href="/foo">Div</Box>           // ERRO — 'href' não existe em props de <div>
<Box as="button" type="submit">Submit</Box>   // ok — type válido em <button>
<Box>conteúdo</Box>                           // ok — default 'div', sem href, sem type
```

Três peças sustentam essa versão. Primeiro, o **type parameter** `E extends React.ElementType` declara que o componente é parametrizado por um elemento — `'div'`, `'a'`, `typeof MyLink`, qualquer coisa que React saiba renderizar. Segundo, `React.ComponentPropsWithoutRef<E>` é o helper que extrai as props do `E` escolhido: é um lookup tipado sobre `JSX.IntrinsicElements` quando `E` é string, ou inferência das props quando `E` é componente. Terceiro, `Omit<..., 'as' | 'children'>` remove a colisão — `as` e `children` são propriedades do próprio `BoxProps`, e sem `Omit` o tipo final teria duplicatas que confundem o checker. O default no generic (`= 'div'`) garante que `<Box>conteúdo</Box>` (sem `as`) compile sem o consumer precisar passar `<Box<'div'>>`.

### Sample 3 — Versão com `forwardRef` (React 18 / lib retrocompatível)

```typescript
type PolymorphicProps<E extends React.ElementType, P = {}> = P & {
  as?: E;
} & Omit<React.ComponentPropsWithoutRef<E>, keyof P | 'as'>;

type PolymorphicRef<E extends React.ElementType> =
  React.ComponentPropsWithRef<E>['ref'];

type BoxOwnProps = { padding?: number };

type BoxProps<E extends React.ElementType> = PolymorphicProps<E, BoxOwnProps>;

const Box = React.forwardRef(
  <E extends React.ElementType = 'div'>(
    { as, padding, children, ...rest }: BoxProps<E>,
    ref: PolymorphicRef<E>,
  ) => {
    const Component = as || 'div';
    return (
      <Component ref={ref} style={{ padding }} {...rest}>
        {children}
      </Component>
    );
  },
) as <E extends React.ElementType = 'div'>(
  props: BoxProps<E> & { ref?: PolymorphicRef<E> },
) => React.ReactElement | null;

// Uso (React 18):
const linkRef = useRef<HTMLAnchorElement>(null);
<Box as="a" href="/foo" ref={linkRef} padding={8}>Link</Box>
```

Esta é a versão que você encontra em libs com `peerDependencies: { react: ">=18" }` — Mantine 7, MUI v5, Chakra UI v2. Três detalhes merecem atenção. (1) `PolymorphicProps<E, P>` é o helper reutilizável que combina own-props (`P`, ex: `{ padding?: number }`) com props do elemento (`E`), removendo colisões com `Omit<..., keyof P | 'as'>`. (2) `PolymorphicRef<E>` extrai o tipo do ref correto via `ComponentPropsWithRef<E>['ref']` — em `<a>`, o ref é `Ref<HTMLAnchorElement>`; em `<button>`, é `Ref<HTMLButtonElement>`; em `Link`, é o que o componente expõe. (3) O **cast no final** (`as <E extends ...>(...) => ReactElement | null`) é o "preço" do pattern em React 18 — `forwardRef` foi tipado quando generics em components ainda não existiam de forma robusta, e o tipo de retorno do `forwardRef` "achata" o generic do componente interno. Sem o cast, o consumer escreveria `<Box as="a" href="/x">` e receberia `Box` não-genérico, com `as: ElementType` e props de elemento perdidas. O cast restaura a forma genérica que o TS já entende internamente — é um *type assertion* que diz "eu sei que é assim, confia".

### Sample 4 — Versão React 19 (sem `forwardRef`)

```typescript
// React 19: ref é prop normal — sem forwardRef, sem cast
type BoxProps<E extends React.ElementType = 'div'> = {
  as?: E;
  padding?: number;
  ref?: React.ComponentPropsWithRef<E>['ref'];
} & Omit<React.ComponentPropsWithoutRef<E>, 'as' | 'padding' | 'ref'>;

function Box<E extends React.ElementType = 'div'>({
  as,
  padding,
  ref,
  children,
  ...rest
}: BoxProps<E>) {
  const Component = (as || 'div') as React.ElementType;
  return (
    <Component ref={ref} style={{ padding }} {...rest}>
      {children}
    </Component>
  );
}

// Uso (React 19):
const linkRef = useRef<HTMLAnchorElement>(null);
<Box<'a'> as="a" href="/foo" ref={linkRef} padding={8}>Link</Box>
// ref tipo: RefObject<HTMLAnchorElement>
```

Em React 19, `ref` virou **prop normal** em function components — o release blog é explícito: *"Starting in React 19, you can now access `ref` as a prop for function components"* e *"New function components will no longer need `forwardRef`, and we will be publishing a codemod to automatically update your components to use the new `ref` prop. In future versions we will deprecate and remove `forwardRef`"* ([fonte](https://react.dev/blog/2024/12/05/react-19)). A consequência prática para polymorphic é grande: o cast cerimonioso do Sample 3 desaparece, `ref` entra como prop opcional dentro do mesmo objeto de props, e o componente é uma function plain — generics, defaults e inferência funcionam de forma natural. O pequeno cast residual (`(as || 'div') as React.ElementType`) é só para satisfazer o JSX parser, que em alguns casos perde o `E` específico ao passar para um `<Component>` dinâmico — não tem ônus de tipo no consumer.

### Sample 5 — Helper utilitário reutilizável

```typescript
// Tipo helper genérico — reutilizável para múltiplos componentes polymorphic
export type PolymorphicComponentProps<
  E extends React.ElementType,
  P = {},
> = P & {
  as?: E;
} & Omit<React.ComponentPropsWithoutRef<E>, keyof P | 'as'>;

// Aplicação em diferentes componentes do design system:
type TextOwnProps = { size?: 'sm' | 'md' | 'lg'; weight?: 'normal' | 'bold' };
type TextProps<E extends React.ElementType> =
  PolymorphicComponentProps<E, TextOwnProps>;

type ButtonOwnProps = {
  variant?: 'primary' | 'secondary' | 'ghost';
  loading?: boolean;
};
type ButtonProps<E extends React.ElementType> =
  PolymorphicComponentProps<E, ButtonOwnProps>;

type StackOwnProps = { gap?: number; direction?: 'row' | 'column' };
type StackProps<E extends React.ElementType> =
  PolymorphicComponentProps<E, StackOwnProps>;

// Cada componente do design system tem o mesmo shape genérico,
// trocando apenas o conjunto de own-props.
```

Centralizar `PolymorphicComponentProps` em um arquivo de tipos do design system é o passo que torna o pattern sustentável em escala. Sem o helper, cada componente reinventa a combinação `P & { as?: E } & Omit<...>` e qualquer correção (ex: incluir `'children'` na lista de chaves omitidas) precisa ser propagada manualmente em N arquivos. Com o helper, a evolução é centralizada — todos os componentes do design system herdam a correção. O pattern é exatamente o que Mantine, Chakra e shadcn/ui fazem internamente: um arquivo `polymorphic.ts` (ou similar) com 20-40 linhas de tipos helpers, importado por dezenas de componentes consumidores.

## Na prática

Polymorphic components são a coluna vertebral da camada de layout/typography em design systems modernos:

- **Mantine** — `<Box>`, `<Text>`, `<Group>` aceitam prop `component` (sinônimo do `as`). A documentação descreve explicitamente o pattern como "polymorphic component" e expõe o tipo helper `PolymorphicComponentProps` para devs que constroem em cima da lib.
- **MUI** — usa prop `component` (não `as`) por convenção histórica. `<Box component="a" href="...">` e `<Typography component="h2">` são padrões. A complexidade do tipo é tão grande que a MUI publica documentação separada sobre "How TypeScript inference works on polymorphic components" como aviso para mantenedores.
- **Radix UI Themes** — `<Box>` aceita prop `as` com domínio restrito (`"div" | "span"`, conforme [docs](https://www.radix-ui.com/themes/docs/components/box)). Restringir o domínio é uma decisão de design — Radix evita a cardinalidade alta do pattern fully polymorphic e expõe só os casos comuns.
- **Radix UI Primitives** — usa um pattern alternativo com `Slot` (`asChild` prop): em vez de `<Button as={Link}>`, é `<Button asChild><Link>...</Link></Button>` — o `Slot` clona o filho e injeta as props do `Button`. Tem trade-offs diferentes (não exige tipos densos, mas exige um único filho válido), aprofundamento em [[14 - Compound components, slots, render props|nota 14]].
- **Chakra UI** — `<Box as="...">` é o nome canônico do pattern; o helper de tipos é parte pública da API e usado por consumidores que estendem a lib.
- **shadcn/ui** — adota o `Slot` do Radix (componente `Slot` exposto como dependência) em vez de polymorphic via `as`, herdando a decisão de design do Radix Primitives.

A escolha entre `as`/`component` polymorphic e `Slot`/`asChild` é uma das decisões de arquitetura mais visíveis em um design system. Polymorphic via `as` é mais ergonômico para o consumer (uma prop só, autocomplete imediato) mas pesa nos tipos. `Slot`/`asChild` é mais leve em tipo mas exige convenção do consumer (sempre um único filho válido, props via cloneElement). Não há vencedor universal — Mantine/Chakra/MUI escolheram `as`, Radix/shadcn escolheram `Slot`.

## Armadilhas

- **`as` colidindo com props HTML.** Sem `Omit<React.ComponentPropsWithoutRef<E>, 'as'>`, o tipo final pode ter `as` declarado duas vezes (no objeto interno e na herança), confundindo o checker e produzindo mensagens de erro confusas. Sempre incluir `'as'` na lista de chaves omitidas, junto de qualquer own-prop que possa existir como atributo HTML (`type` em `<button>`, `value` em `<input>`, etc).

- **Ref tipo errado em `forwardRef` genérico.** O ref de `<a>` é `Ref<HTMLAnchorElement>`; o de `<button>` é `Ref<HTMLButtonElement>`. Sem `React.ComponentPropsWithRef<E>['ref']` (ou `PolymorphicRef<E>`), o ref vira `Ref<unknown>` ou `Ref<HTMLElement>` genérico, e o consumer não consegue acessar `.click()` específico de `<a>` ou `<button>` sem cast. O helper extrai o ref correto a partir do `E` escolhido — é a forma idiomática.

- **Performance: `as` como função inline.** Passar `as={() => <CustomComponent />}` em cada render cria um novo componente a cada chamada, que o React trata como um tipo diferente — desmonta e remonta a árvore inteira a cada render. Sintoma: estado interno do `CustomComponent` se perde a cada update do pai. Correção: passar referência estável (`as={CustomComponent}`, sem wrapping) ou definir o componente fora do escopo do render.

- **Em React 19, ainda usar `forwardRef` "por costume".** Code reviews de devs vindos de React 18 frequentemente sugerem embrulhar polymorphic com `forwardRef` mesmo em projetos React 19. É desnecessário — `ref` é prop normal em function components agora, e o cast cerimonioso do Sample 3 só existe por causa do `forwardRef`. Em código novo React 19, vá direto na versão do Sample 4.

- **Esquecer o default no generic (`E extends React.ElementType = 'div'`).** Sem default, o consumer precisa passar `<Box<'div'>>` toda vez que omite `as` — o TS reclama de "Generic type 'BoxProps' requires 1 type argument(s)". O default torna `<Box>conteúdo</Box>` válido sem cerimônia, mantendo a opção de override (`<Box as="a" href="/x">`).

## Em entrevista

> "Polymorphic components are the pattern behind design systems like Mantine and Radix — a single `<Box>` or `<Text>` that accepts an `as` prop and changes both the rendered element and the accepted props. The TypeScript machinery is built on three pieces. First, a generic type parameter — `E extends React.ElementType` — for the element. Second, `React.ComponentPropsWithoutRef<E>` to extract the props of that element, so when `as='a'`, the component accepts `href`, `target`, `rel`, etc. Third, `Omit` to remove `as` and any conflicting own-props from the inherited props. In React 18, you also need `forwardRef`, and the type machinery gets verbose because `forwardRef` doesn't preserve generics naturally — you usually end up with a type assertion at the end of the component definition just to restore the generic shape. In React 19, `ref` is a regular prop on function components, so the cast disappears and the implementation becomes much cleaner. The pattern is complex to maintain, but it produces a developer experience that's worth it for design systems with dozens of components — the alternative is duplicating each component for every possible HTML element."

**Vocabulário-chave:** *polymorphic*, *element type*, *ComponentPropsWithoutRef*, *forwardRef*, *type preservation*.

**Pergunta típica de senior interview:** *"How do you implement a `<Box as="...">` component where the props change based on the `as` value?"* — resposta defensiva: declare a generic `<E extends React.ElementType>` on the component, intersect `{ as?: E }` with `Omit<React.ComponentPropsWithoutRef<E>, 'as'>` so the consumer gets the props of the chosen element. Add a default (`E = 'div'`) so callers can omit `as`. In React 18 wrap with `forwardRef` and cast the final type to restore the generic. In React 19, skip `forwardRef` — `ref` is just another prop on the props object.

## Veja também

- [[01 - A tripla inferência - props, state, hooks]] — IntrinsicElements e ComponentPropsWithoutRef
- [[05 - Tipando state e refs]] — ref em React 19 como prop normal
- [[12 - Generic components]] — generics em React (mecânica base)
- [[14 - Compound components, slots, render props]] — Slot/asChild como alternativa
- [[TypeScript]] — seção "Generics" e "TypeScript em frontend (React)"
- [[React]] — seção "Componentes e JSX"
