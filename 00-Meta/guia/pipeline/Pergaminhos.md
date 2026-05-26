---
title: "Pergaminhos — captura inicial"
type: moc
publish: true
created: 2026-05-04
updated: 2026-05-04
tags:
  - guia
  - pipeline
  - pergaminhos
---

# Pergaminhos — captura inicial

A zona `01-Pergaminhos/` é a **inbox** do vault: tudo que ainda não foi processado. Links interessantes, ideias soltas, capturas de chat com LLMs, anotações de reunião, fragmentos.

## O que vai aqui

- URLs encontradas em redes/feeds que merecem leitura.
- Ideias cruas que não cabem ainda em domínio nenhum.
- Notas tomadas em contexto de captura rápida (mobile, durante leitura, em conversa).
- Fragmentos de chat com LLMs que valem revisitar.

## Convenções

### `entradas.md`

Arquivo principal da zona. É a inbox de URLs. Funciona como TODO list de leituras pendentes.

Formato (não rígido):

```markdown
- https://exemplo.com/artigo-interessante
- [Título legível](https://exemplo.com/outro)
- https://blog.tecnomante.dev/topic — comentário curto
```

A skill `/glosa <url>` lê uma URL daqui (ou recebida diretamente) e produz uma glosa. Se o link estava em `entradas.md`, a skill remove a linha automaticamente.

### Outros pergaminhos

Arquivos `.md` soltos em `01-Pergaminhos/` são notas não-estruturadas. Sem template fixo. Podem virar glosas ou notas de domínio quando o tema amadurecer (manual ou via skill futura).

## Como passa pra próxima etapa

| Origem | Caminho | Skill |
|---|---|---|
| URL em `entradas.md` ou compartilhada | URL → Glosa em `02-Glosas/` | `/glosa <url>` |
| Pergaminho de texto livre | Manual: ler, decidir destino | (sem skill atual; futuro) |

A skill `/glosa` cobre apenas artigos web (HTML). PDF, vídeo, podcast, tweets ficam pendentes — vide [[Glosas]].

## Ver também

- [[Codex/00-Meta/guia/pipeline/index|Pipeline do Codex]]
- [[Glosas]]
