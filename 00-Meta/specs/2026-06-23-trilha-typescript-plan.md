---
title: "Plano — Trilha TypeScript"
type: spec
created: 2026-06-23
updated: 2026-06-23
status: in_progress
tags:
  - spec
  - trilha
  - typescript
---
# Plano — Trilha TypeScript (3 fases)

## Visão

Transformar o domínio `Tecnologia/TypeScript` (hoje: 1 monólito `TypeScript.md` de 1514 ln + 2 stubs) numa **trilha 3-fases** (Iniciado/Adepto/Magus) de notas atômicas estilo capítulo (~440-540 ln, diagramas Mermaid), no padrão das trilhas maduras. Alvo: prep pra entrevistas internacionais, eixo frontend-web.

A tese da trilha: **TypeScript é um sistema de tipos *estrutural* e *gradual* colado sobre o JavaScript, que some em runtime.** Essas três propriedades (estrutural, gradual, erased) explicam quase toda decisão de design e toda armadilha. A trilha vai do modelo mental até type-level programming e a fronteira type↔runtime.

## Fonte e método

- **Tronco a minerar:** `TypeScript.md` (1514 ln) cobre ~90% do material em forma de monólito. Cada nota da trilha **minera a seção correspondente** e a aprofunda ao nível capítulo (exemplo trabalhado, divulgação progressiva, Mermaid, registro Feynman). **Decisão: o monólito é APOSENTADO** (deletado) quando 100% absorvido — não vira tronco-com-callouts. Garantir que cada seção tenha destino numa nota antes de remover; redirecionar os inbound de `[[TypeScript]]` pro `index` (ou nota específica).
- **Biblioteca:** `Biblioteca de TypeScript.md` é **artefato próprio do domínio** (recursos externos curados, par do Dicionário — ver [[project_artefatos_dominio]]). **Mantida**, atualizada se necessário; nunca absorvida na trilha.
- **MOC:** `index.md` vira o MOC agrupado por fase.
- Notas numeradas `01..NN` flat em `Tecnologia/TypeScript/`, frontmatter `fase: Iniciado|Adepto|Magus`, tag `typescript` + fase + `entrevista`; MOC agrupado por fase (padrão [[project_trilhas_fases_aprendizado]]).

## Fronteiras (anti-duplicação — crítico)

| Tema | Dono | A trilha TS faz |
|------|------|-----------------|
| TS **aplicado a React** (props, hooks, Context, forms tipados) | `React/TypeScript com React/` (15 notas, **já existe**) | **NÃO duplicar** — linkar. A trilha TS para na linguagem |
| **Teoria** de sistemas de tipos (estrutural×nominal como conceito, ADTs) | `Ciência/Paradigmas/13 Sistemas de tipos` + `10 Tipos algébricos` | Cobre a implementação CONCRETA do TS; linka a teoria |
| **Inferência** como teoria (Hindley-Milner) | `Ciência/Compiladores/10 Análise semântica` | Cobre a inferência do TS na prática; linka a teoria |
| Libs de **validação runtime** (Zod/Yup/Joi) | `Tecnologia/JavaScript/Validação/` | Cobre o *conceito* da fronteira type↔runtime; linka as libs |
| **Build/transpilação** (esbuild, swc, bundling) | `Tecnologia/Tooling e Build` | Dona do `tsconfig` enquanto **type-checker**; defere a transpilação/bundle |
| Base da **linguagem JS** (closures, async, protótipos) | `Tecnologia/JavaScript/JavaScript Fundamentals` | Pressupõe; linka, não reensina |
| TS em **Node/backend** (Express/Fastify) | `Tecnologia/Node` | Menção leve em padrões; defere framework specifics |

## Roster por fase (granular — 27 notas)

### 🟢 Iniciado (júnior — modelo mental e o sistema de tipos do dia a dia) — 10 notas
1. **O que é TypeScript: gradual, estrutural, apagado** — por que tipos; TS como camada sobre JS; *structural typing* (o conceito que diferencia de Java/C#); erase-at-runtime; o compilador como type-checker. Liga JS Fundamentals + Paradigmas.
2. **Tipos primitivos, literais e a inferência** — tipos básicos; deixar o TS inferir vs anotar; literal types; widening/narrowing de literais.
3. **Arrays, tuplas e `as const`** — arrays vs tuplas; readonly arrays; `as const` e seu efeito; tuplas nomeadas.
4. **`any`, `unknown` e `never`** — o buraco do `any`; `unknown` como `any` seguro; `never` e seu papel; soundness e onde o TS abre mão dela de propósito.
5. **`strictNullChecks`: null, undefined e optional** — o erro de um bilhão de dólares; `?` vs `| undefined`; optional chaining/nullish no nível de tipo.
6. **Objetos: `interface` vs `type`** — quando cada um; extending; index signatures; optional/readonly; excess property checking.
7. **Union e intersection types** — `|` e `&`; modelar "ou"/"e"; perigos de intersection; narrowing de union (intro).
8. **Discriminated unions e exhaustiveness** — o pattern central: tagged unions pra modelar estado; checagem exaustiva com `never`.
9. **Type narrowing e type guards** — `typeof`/`instanceof`/`in`; discriminant; control flow analysis; custom type guards; assertion functions; `!`.
10. **Tipando funções: assinaturas, overloads, contextual typing** — parâmetros/retorno, optional/rest, overloads, tipando callbacks, `this`.

### 🟡 Adepto (pleno — type-level programming e configuração) — 10 notas
11. **Generics: funções e constraints** — o coração da reutilização tipada; `extends` como constraint; inferência de type args.
12. **Generics: defaults, classes e interfaces genéricas** — default type params; classes/interfaces genéricas; variância na prática.
13. **Conditional types** — tipos condicionais; distributive conditionals; padrões comuns.
14. **`infer` e extração de tipos** — `infer`; extrair de funções/arrays/promises; reconstruir `ReturnType`/`Awaited`.
15. **`keyof`, `typeof` e indexed access types** — operadores de tipo; `T[K]`; derivar tipos de valores.
16. **Mapped types e key remapping** — mapear sobre keys; `+/-readonly`, `+/-?`; key remapping (TS 4.1+) com `as`.
17. **Template literal types** — strings no nível de tipo; `Uppercase`/etc.; padrões (rotas tipadas, keys derivadas).
18. **Utility types — e como reconstruí-los** — `Partial`/`Required`/`Pick`/`Omit`/`Record`/`Parameters`/`NonNullable`; reconstruir a partir de mapped+conditional (consolida 13-16).
19. **Enums, `const` objects e modelagem de constantes** — por que evitar `enum`; union de literais (recomendado); `as const` object pattern.
20. **`tsconfig` e strict mode a fundo** — o que cada flag de `strict` protege; `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`; `module`/`target`/`moduleResolution` na ótica de TIPOS. (Fronteira: build → Tooling e Build.)

### 🔴 Magus (senior — fronteiras, runtime, escala, produção) — 7 notas
21. **Modules: ESM, CJS e type-only imports** — ESM×CJS no TS; `import type`/`export type`; `verbatimModuleSyntax`; resolução de módulos.
22. **Declaration files (`.d.ts`) e o ecossistema de tipos** — `.d.ts`; ambient declarations; DefinitelyTyped/`@types`; declaration merging a fundo; tipando libs sem tipos.
23. **A fronteira type↔runtime: parse, don't validate** — tipos somem em runtime; o gap nos boundaries (API, env, form); *parse-don't-validate*. Linka `Validação` (Zod).
24. **Type-driven design: branded types, Result e estados impossíveis** — making impossible states unrepresentable; branded/nominal types; Result/Either; domain modeling com tipos.
25. **TypeScript em escala: performance do compilador e project references** — por que a checagem fica lenta; `incremental`; project references; monorepo. (Fronteira: bundling → Tooling.)
26. **Lendo o compilador: erros comuns e como decifrar mensagens** — anatomia de um erro de tipo; armadilhas frequentes; estratégias de debugging de tipos.
27. **TypeScript em entrevista** — capstone: frases-chave, vocabulário PT→EN, perguntas comuns (structural typing, `unknown` vs `any`, generics, narrowing, parse-don't-validate), mapa de revisão.

**Total: 27 notas** (10/10/7). Range das trilhas maduras: 13-24; TS é linguagem profunda → mais granular justifica.

## Sequência de execução

> **Status:** ✅ **Iniciado (1-10) FEITO** (2026-06-23, commit 07c9730) — 10 notas ~415-685 ln, 3-5 Mermaid cada, MOC por fase. Monólito mantido. Próximo: Adepto (11-20).

1. **Iniciado (1-10)** primeiro — base que o resto pressupõe; minerar as seções do monólito.
2. **Adepto (11-20)** — type-level; a nota 18 (utility types) consolida 13-16.
3. **Magus (21-27)** — fronteiras e produção; 23 coordena com `Validação`.
4. Conforme escrevo, **garantir destino de cada seção do `TypeScript.md`** e **aposentá-lo** (deletar) ao fim, redirecionando inbound de `[[TypeScript]]`; construir o **MOC `index.md`** agrupado por fase; manter `Biblioteca de TypeScript.md` (atualizar se houver recurso novo das notas).
5. Revisão entre fases (não despejar as 27 de uma vez).

## Decisões fechadas (2026-06-23)

- **Granularidade:** roster granular de **27 notas** (10/10/7) — aprovado "mais notas".
- **Monólito `TypeScript.md`:** **aposentado** (deletado) quando 100% absorvido; não vira tronco-com-callouts.
- **`Biblioteca de TypeScript.md`:** **mantida** como artefato de domínio ([[project_artefatos_dominio]]); atualizar se necessário, nunca absorver.

## Âncoras
- Padrões aplicados: [[project_trilhas_fases_aprendizado]], [[feedback_padrao_capitulo_livro]], [[feedback_notas_profundas_diagramas]], [[feedback_enriquecimento_feynman]], [[project_artefatos_dominio]].
