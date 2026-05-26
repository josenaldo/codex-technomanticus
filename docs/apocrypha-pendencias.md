# Pendências do Apocrypha

Backlog de alterações que precisam ser aplicadas no `codex-technomanticus-apocrypha` quando a próxima sessão dedicada acontecer. Não tocar no apocrypha agora — outra sessão de edição está em andamento.

> **Resolvido pela spec [`2026-05-05-dashboards-apocrypha-design.md`](superpowers/specs/2026-05-05-dashboards-apocrypha-design.md)** (executada em 2026-05-05): cross-vault awareness via symlink relativo `Codex` → vault público; dashboards `Progresso agregado`, `O que estudar hoje`, `Cross-glosa` em `00-Meta/dashboards/` do apocrypha. Próximas pendências abaixo.

## Daily notes do Obsidian

**Decisão fechada:** daily notes vão no apocrypha (cunho pessoal demais pra publicar).

**Proposta detalhada (a refinar na sessão dedicada do apocrypha):**

### Estrutura de pastas

```
Diário/
└── <ano>/
    └── <YYYY-MM-DD>.md
```

`Diário/2026/2026-05-05.md`. Cap natural por ano evita pasta gigante quando o volume crescer.

### Plugin

Plugin core "Daily Notes" do Obsidian (já vem com Obsidian; ativar nas Settings → Core plugins). Configurar:
- **Date format:** `YYYY-MM-DD`
- **New file location:** `Diário/{{date:YYYY}}` (ou só `Diário` se preferir flat — decidir).
- **Template file location:** `00-Meta/templates/Template - Daily.md` (criar este template no apocrypha — não mexer no público).

Plugin Templater já está instalado no público; se for o caso, instalar/ativar no apocrypha também.

Plugin Calendar (community) é opcional — visualização mensal clicável das daily notes. Bom QoL.

### Template proposto (a criar em `Apocrypha/00-Meta/templates/Template - Daily.md`)

```markdown
---
title: "<% tp.date.now('YYYY-MM-DD') %>"
type: daily
created: <% tp.date.now('YYYY-MM-DD') %>
tags:
  - daily
publish: false
---

# <% tp.date.now('YYYY-MM-DD') %>

## Foco do dia

(o que pretende fazer hoje — objetivos prioritários)

## Estudei

(o que estudou; pode incluir wikilinks pra sendas/notas/glosas)

## Worklog

(decisões técnicas, código, problemas resolvidos)

## Capturas

(ideias soltas, links, fragmentos — candidatos a virar pergaminhos/glosas/notas)

## Reflexões

(journal — o que aprendi sobre meu processo, frustrações, retomadas)

## TODOs

- [ ] 

## Para amanhã

(o que ficou pendente; primeira coisa a olhar amanhã)
```

Seções podem ficar vazias — não tem obrigação de preencher tudo.

### Uso múltiplo (não só journal de estudo)

A daily note serve como container do dia, abrigando:

- **Worklog técnico** (decisões, código, debugging).
- **Journal de estudo** (o que aprendi, conexões, dúvidas).
- **Captura rápida** (similar a inbox; vira candidato a pergaminho público depois).
- **Reuniões** (notas de cada uma).
- **TODOs do dia** (checkbox).
- **Reflexões pessoais** (sentimentos, hábitos, observações).

Tudo num arquivo por dia. Se um aspecto crescer demais, pode "promover" pra arquivo dedicado.

### Ciclo de vida

Daily notes ficam **permanentes** — são histórico, não inbox. Não arquivar nem deletar. A subdivisão por ano (`Diário/<ano>/`) já organiza naturalmente.

Possível skill futura: `/daily-resumo-mensal <ano>-<mês>` que sumariza o mês a partir de N daily notes — útil pra retrospectivas.

### Promoção pra outras notas

Daily note funciona como **inbox temporal**:

- Capturou um link interessante → pode ir pra `01-Pergaminhos/entradas.md` (público) e depois virar glosa via `/glosa`.
- Anotou um insight de estudo → pode virar nota em `03-Dominios/<X>/` (público).
- Decisão técnica importante → vira nota dedicada (ADR ou similar).
- Reflexão pessoal → fica na daily mesmo (apocrypha é o lar dela).

A daily permanece como registro do "quando" — não some quando o conteúdo é promovido. Ela é cronológica; as notas promovidas são temáticas. Os dois coexistem.

Skill futura possível: `/daily-promover` que pesca um trecho marcado da daily e move pro destino certo. Mas é overkill pro MVP — manualmente já funciona (copiar/colar + criar arquivo no destino).

### Integração com Codex (público)

A daily note pode citar wikilinks de notas públicas: `[[Senda IA]]`, `[[03-Dominios/React/MUI]]`, `[[02-Glosas/2026-design-md-spec-coding-agents]]`. Backlinks dessas notas mostrariam **quando** elas foram tocadas no journal. Útil pra "que dia trabalhei em X?".

Pra isso, o apocrypha precisa ter acesso de leitura ao público (resolvido pela cross-vault awareness, vide topo deste arquivo).

### Privacidade dentro do apocrypha

Mesmo no apocrypha, pode haver gradação futura:
- Worklog técnico/aprendizado pode eventualmente virar post de blog (`publish: true` numa nota promovida).
- Reflexões pessoais ficam mesmo.

Pro MVP, todas as daily notes têm `publish: false`. Refinar se aparecer caso real.

### Disciplina

Daily note só funciona com hábito. Sugestão: configurar atalho rápido (Ctrl+Alt+D ou similar) e abrir como primeira coisa ao começar a trabalhar. Sem hábito, vira papel de parede.

## Outras pendências

(adicionar aqui conforme forem aparecendo nas sessões do público)

