---
title: "Material UI"
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

# Material UI

Biblioteca de componentes React baseada no Material Design do Google — a mais popular do ecossistema React.

## O que é

Material UI (MUI) é uma biblioteca de componentes React que implementa o Material Design. Oferece 50+ componentes prontos, sistema de temas, CSS-in-JS (Emotion/styled-components), e é altamente customizável.

## Como funciona

### Componentes básicos

```tsx
import { Button, TextField, Card, CardContent, Typography } from '@mui/material';

function PatientForm() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5">Novo Paciente</Typography>
        <TextField label="Nome" fullWidth margin="normal" />
        <TextField label="Email" type="email" fullWidth margin="normal" />
        <Button variant="contained" color="primary">Salvar</Button>
      </CardContent>
    </Card>
  );
}
```

### Sistema de temas

```tsx
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: { main: '#2563eb' },
    secondary: { main: '#7c3aed' },
  },
  typography: {
    fontFamily: '"Inter", sans-serif',
  },
  shape: { borderRadius: 8 },
});

// Envolve a app inteira
<ThemeProvider theme={theme}>
  <App />
</ThemeProvider>
```

### Layout com MUI

- **Box:** div com system props (`sx`, `m`, `p`, `display`)
- **Stack:** flex column/row com spacing
- **Grid2:** grid responsivo (similar ao Bootstrap)
- **Container:** largura máxima responsiva

```tsx
<Stack direction="row" spacing={2} alignItems="center">
  <Avatar src={doctor.photo} />
  <Typography>{doctor.name}</Typography>
</Stack>
```

### `sx` prop

```tsx
<Box sx={{
  display: 'flex',
  gap: 2,
  p: 3,
  bgcolor: 'background.paper',
  borderRadius: 1,
  '&:hover': { bgcolor: 'action.hover' }
}}>
```

### Data Display

- **DataGrid (@mui/x-data-grid):** tabelas avançadas com sort, filter, pagination, edit
- **DatePicker (@mui/x-date-pickers):** seleção de data/hora
- **Charts (@mui/x-charts):** gráficos integrados

## Quando usar

- **Aplicações React com design system:** dashboard, admin, SaaS
- **Equipes que querem produtividade:** componentes prontos, acessíveis, responsivos
- **Projetos que seguem Material Design:** ou que precisam de uma base sólida para customizar

## Armadilhas comuns

- **Bundle size:** MUI é grande. Usar tree-shaking e imports nomeados
- **Over-customization:** se lutando contra o Material Design, considerar outra lib
- **Performance com DataGrid:** datasets grandes precisam de virtualização (built-in no DataGrid Pro)
- **sx prop vs styled:** `sx` para one-off, `styled()` para componentes reutilizáveis

## Na prática (da minha experiência)

> No MedEspecialista, o frontend usa MUI como base de componentes. O DataGrid é usado extensivamente para listagens de pacientes e agendamentos. O sistema de temas permite manter consistência visual com customizações mínimas — mudando `createTheme`, todos os componentes se adaptam.

## How to explain in English

"Material UI is my primary component library for React applications. I appreciate its comprehensive set of accessible, well-tested components and the powerful theming system. For data-heavy applications, the DataGrid component handles sorting, filtering, and pagination out of the box, which saves significant development time. I customize the theme to match brand guidelines while keeping the UX patterns that users expect from Material Design."

### Key vocabulary

- biblioteca de componentes → component library
- sistema de temas → theming system
- design system → design system
- CSS-in-JS → CSS-in-JS: estilos escritos em JavaScript

## Recursos

- [MUI Docs](https://mui.com/material-ui/) — documentação oficial
- [MUI X](https://mui.com/x/) — componentes avançados (DataGrid, DatePicker)

## Veja também

- [[HTML e CSS]]
- [[React]]
- [[Bootstrap]]
- [[03-Dominios/JavaScript/Frontend/Mantine]]
