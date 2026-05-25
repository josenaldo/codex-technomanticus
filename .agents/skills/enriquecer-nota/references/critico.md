# Subagente crítico — enriquecer-nota

A SKILL despacha este prompt via Agent tool (`subagent_type: general-purpose`), UMA vez por execução,
passando o pool de candidatos de conteúdo. O crítico é um julgador **independente** de quem gerou os
candidatos — é o que mata o "parágrafo óbvio".

## Entrada (a SKILL preenche)

```yaml
fase: Magus                  # Iniciado | Adepto | Magus (default Magus se a nota não tem fase)
nota:
  titulo: "<título>"
  corpo: |
    <corpo integral da nota>
candidatos:                  # SÓ tipo adicao|reescrita das lentes profundidade|lacunas|novidade
  - { id: C1, lente: profundidade, tipo: adicao, conteudo: "...", fonte: {...} }
  - ...
```

> Para candidatos `tipo: reescrita`, inclua também o campo `antes` no objeto enviado — o crítico não o usa para pontuar, mas o orquestrador precisa que ele seja preservado para a Fase 6.

## Rubrica por fase (corta se...)

| Fase                | Corta o candidato se... |
| ------------------- | ----------------------- |
| **Iniciado** (júnior) | for trivial até para quem está começando no tema |
| **Adepto** (pleno)    | um pleno da área já saberia; só passa se trouxer nuance/trade-off real |
| **Magus** (sênior)    | um sênior já domina; só passa edge case, gotcha ou detalhe de produção |

Regra adicional, todas as fases: **descarte qualquer candidato sem fonte verificável** quando a lente
for Profundidade ou Novidade (ver proveniência).

## Tarefa

Para cada candidato, pontue de 0 a 3:
- **novidade** — quão provável é que o leitor-alvo NÃO saiba disso (0 = todos sabem; 3 = realmente novo).
- **profundidade** — quão além do óbvio o conteúdo vai (0 = superficial; 3 = nuance de especialista).

Mantenha (`keep`) apenas candidatos com `novidade >= 2` **e** `profundidade >= 2` para a fase dada.
Descarte (`drop`) o resto, com motivo de 1 linha.

**Exceção — `lente: lacunas`:** novidade é secundária (essa lente cobre lacunas estruturais, não novidade). Mantenha se `profundidade >= 2`, mesmo que `novidade < 2`. Candidatos rasos (`profundidade < 2`) continuam descartados.

## Saída (formato exato — devolva só isto)

```yaml
sobreviventes:
  - id: C1
    veredito: keep
    novidade: 3
    profundidade: 2
    justificativa: "edge case de produção não-óbvio para sênior"
    confianca: alta            # alta | media | baixa
descartados:
  - id: C3
    veredito: drop
    motivo: "definição básica que um pleno já domina"
```
