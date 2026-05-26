---
title: "Mantine"
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

# Mantine

Biblioteca de componentes React moderna — hooks-first, tipagem forte, e design limpo sem opinionismo excessivo.

## O que é

Mantine é uma biblioteca React com 100+ componentes, 50+ hooks, sistema de temas, e formulários integrados. Diferente do MUI (Material Design), Mantine tem um design visual neutro e mais fácil de customizar. Usa CSS Modules nativamente (v7+).

## Como funciona

### Componentes

```tsx
import { Button, TextInput, Card, Group, Stack, Text } from '@mantine/core';

function PatientForm() {
  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Stack>
        <Text size="lg" fw={500}>Novo Paciente</Text>
        <TextInput label="Nome" placeholder="Nome completo" />
        <TextInput label="Email" placeholder="email@exemplo.com" />
        <Group justify="flex-end">
          <Button>Salvar</Button>
        </Group>
      </Stack>
    </Card>
  );
}
```

### Hooks

```tsx
import { useDisclosure } from '@mantine/hooks';
import { useDebouncedValue } from '@mantine/hooks';
import { useForm } from '@mantine/form';

// Modal control
const [opened, { open, close }] = useDisclosure(false);

// Debounce para busca
const [debounced] = useDebouncedValue(searchTerm, 300);

// Forms com validação
const form = useForm({
  initialValues: { name: '', email: '' },
  validate: {
    email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Email inválido'),
  },
});
```

### Temas

```tsx
import { MantineProvider, createTheme } from '@mantine/core';

const theme = createTheme({
  primaryColor: 'blue',
  fontFamily: 'Inter, sans-serif',
  defaultRadius: 'md',
});

<MantineProvider theme={theme}>
  <App />
</MantineProvider>
```

### Diferenciais vs MUI

| Aspecto     | Mantine                 | MUI                          |
| ----------- | ----------------------- | ---------------------------- |
| Design      | Neutro, flexível        | Material Design (opinionado) |
| Estilização | CSS Modules (v7)        | Emotion / styled             |
| Hooks       | 50+ hooks utilitários   | Poucos                       |
| Forms       | @mantine/form integrado | Sem solução oficial          |
| Bundle      | Menor                   | Maior                        |
| Maturidade  | Mais novo (2021)        | Mais maduro (2014)           |

## Quando usar

- **Projetos React que querem flexibilidade visual:** sem ficar preso ao Material Design
- **Aplicações com muitos formulários:** @mantine/form é excelente
- **Quando hooks utilitários agregam valor:** useDisclosure, useDebouncedValue, useLocalStorage
- **Projetos novos:** menor vendor lock-in que MUI

## Armadilhas comuns

- **Migração entre major versions:** Mantine v6→v7 teve breaking changes significativos (CSS-in-JS → CSS Modules)
- **Ecossistema menor:** menos componentes third-party que MUI
- **Documentação:** boa mas menos exemplos que MUI

## How to explain in English

"Mantine is a React component library I use when I want more design flexibility than Material UI provides. It has a clean, neutral aesthetic that's easier to customize for different brands. What sets it apart is the collection of 50+ utility hooks — things like `useDisclosure` for modals, `useDebouncedValue` for search, and a built-in form management solution. For new projects where I don't need to follow Material Design, Mantine is my preferred choice."

### Key vocabulary

- biblioteca de componentes → component library
- hooks utilitários → utility hooks
- gerenciamento de formulários → form management
- design neutro → neutral design / unopinionated design

## Recursos

- [Mantine Docs](https://mantine.dev/) — documentação oficial
- [Mantine UI](https://ui.mantine.dev/) — templates e exemplos prontos

## Veja também

- [[HTML e CSS]]
- [[React]]
- [[Material UI]]
- [[Bootstrap]]
