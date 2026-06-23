---
title: "Redesign enriquecer-nota — Skill Graph (Estágio 3)"
created: 2026-06-14
type: spec
status: draft
publish: false
tags:
  - meta
  - skills
  - spec
---

# Redesign `enriquecer-nota` — Skill Graph (Estágio 3)

## Contexto e problema

A skill `enriquecer-nota` hoje é monolítica: uma skill com 4 lentes (profundidade,
lacunas, novidade, conexões) + higiene + um subagente crítico. Ela **fecha lacunas factuais
com fonte**, mas não **ensina**.

Diagnóstico a partir do diff de `03-Dominios/Tecnologia/IA/Anatomia dos LLMs/03 - A janela de contexto.md`
(versão original 128 linhas → versão enriquecida à mão 382 linhas):

1. **A skill produz esqueleto; o usuário produz carne.** A versão original era bullets +
   tabelas + descrições de uma linha. O valor que o usuário adicionou à mão é a **prosa
   didática**: analogias (chef/despensa pra banda de memória, holofote pra atenção diluída),
   perguntas retóricas ("Por que é o gargalo?"), camadas sintoma/causa, callouts aninhados,
   resumo de uma linha. A skill atual **não tem lente que gere isso**.
2. **O começo das notas continua seco.** Mesmo na versão final, a seção "O que é" permaneceu
   a bullet-list original. Toda a riqueza didática ficou no miolo/fundo. A skill nunca atacou
   a introdução.
3. **Causa raiz suspeita confirmada:** o limite de linhas inicial empurrou o agente a resumir.
   O registro Feynman já está documentado em `references/lentes.md`, mas como *higiene de
   redação*, não como uma lente que **gera** explicação didática proativamente.

### O que o usuário quer adicionar

- **Meta-skill + micro-skills** de enriquecimento (vocabulário do próprio artigo do usuário,
  `context-engineering-guia-completo.md`, seções 6 e 9 — o Skill Graph do Estágio 3).
- Um **conselho de personas** (estilo LLM council do Karpathy) lendo a nota e extraindo
  **dúvidas comuns**; das dúvidas → responder na própria nota, linkar pra nota que já responde,
  ou adicionar diagramas.
- **Diagramas/infográficos** que expliquem melhor os conceitos.
- Texto **mais didático e explicativo no começo** das notas.
- Manter o que já existe: atualizar info, cobrir lacunas, expandir sem sair do assunto.

## Decisões (confirmadas com o usuário)

| Decisão | Escolha |
| ------- | ------- |
| Arquitetura | **Skill graph completo (Estágio 3)** — meta + micro-skills instaláveis + constraint |
| Conselho — personas | **8 personas**: 3 leitores por nível (Iniciado/Adepto/Magus) + 5 advisors adaptados (Recém-chegado, Fundamentalista, Cético, Conector, Praticante) |
| Conselho — papel | **Só gera dúvidas**; o crítico continua sendo o gate de qualidade |
| Diagramas | **Mermaid + ASCII nativos** apenas (sem imagens binárias / pipeline novo) |
| Limite de tamanho | **Cresce, mas marca candidatos a galho** no relatório final |
| Lente didática | **Pode reescrever** trechos secos via diff antes→depois aprovado item a item |
| Dúvidas no plano | Entram no **plano único** como proveniência ("por que" de cada candidato); triagem crua opcional via flag `--triagem` |
| Local do spec | `00-Meta/specs/` com `publish: false` |

## Goals / Non-goals

**Goals**
- Transformar `enriquecer-nota` em meta-skill que orquestra micro-skills + uma constraint-skill.
- Introduzir geração de prosa didática como lente de primeira classe, atacando o começo seco.
- Introduzir o conselho de 8 personas como motor de dúvidas que alimenta as lentes.
- Introduzir geração de diagramas/ASCII como lente.
- Preservar: plano único antes de executar, calibração por fase, proveniência obrigatória,
  ordem determinística de execução, higiene baseline, "nunca remove em silêncio".

**Non-goals**
- Não gerar imagens binárias.
- Não criar notas novas (só edita a nota-alvo + dicionário). Split tronco/galho continua manual
  (a skill só *marca* candidatos).
- Não substituir o crítico pelo conselho.
- Não publicar nada novo no Quartz por efeito colateral.

## Arquitetura — o grafo de skills

```
enriquecer-nota  (META-SKILL — orquestra, não detalha)
├── enriquecer-duvidas       (CONSELHO — 8 personas → dúvidas roteadas)   [novo]
├── enriquecer-didatica      (prosa explicativa; ataca o começo seco)     [novo]
├── enriquecer-diagramas     (mermaid + ASCII)                            [novo]
├── enriquecer-profundidade  (trade-offs, edge cases)                     [extrai da atual]
├── enriquecer-lacunas       (sub-tópicos faltantes)                      [extrai]
├── enriquecer-novidade      (fatos novos com fonte)                      [extrai]
├── enriquecer-conexoes      (wikilinks + Veja também; delega /verbete)   [extrai]
└── validar-enriquecimento   (CONSTRAINT — gate final, com scripts/)      [vira o crítico]
```

Total: 8 diretórios novos em `.agents/skills/` (a meta já existe). 7 lentes (micro-skills) +
1 constraint-skill + a meta.

### Regras do grafo (do artigo, seção 6 e 9)

- **Profundidade máxima 1 nível.** A meta chama todas as micro-skills e a constraint. As
  micro-skills **nunca** chamam umas às outras (evita cadeias A→B→C e ciclos). O conselho
  *roteia* dúvidas, mas quem **dispara** cada lente é sempre a meta.
- **Anti-duplicação.** `enriquecer-conexoes` delega à lógica do `/verbete` (não reimplementa).
  `validar-enriquecimento` reusa `verificar-wikilinks/scripts/check_wikilinks.py`.
- **Nomenclatura** = convenção do vault (português, verbo-substantivo), não o inglês do artigo
  — coerente com `enriquecer-nota`, `promover-glosa`, `sintetizar-glosas`.
- **`description`** < 1024 chars, sem tags XML, "empurrativa" (frases que o usuário diria).
- SKILL.md de cada micro-skill enxuto (<~120 linhas); motores longos vão em `references/`.

## Componente: meta-skill `enriquecer-nota`

Orquestração pura. Pipeline:

```
1. Identificar alvo      path → domínio (03-Dominios/<X>) → fase → dicionário do domínio
2. Escolher lentes       menu multi-select; o conselho é uma das lentes
3. Conselho (se ligado)  → enriquecer-duvidas → lista de dúvidas roteadas
4. Lentes selecionadas   → cada micro-skill roda seu motor, consumindo as dúvidas roteadas
                           pra ela → pool de candidatos (schema único)
5. Crítica semântica     → validar-enriquecimento (modo crítico) poda o pool por fase + fonte
6. PLANO ÚNICO           agrupado por lente; reescritas como diff antes→depois;
                           cada item mostra a dúvida de origem como proveniência   [CONFIRMAÇÃO]
7. Execução              ordem determinística; relê o arquivo antes de cada edição
8. Validação programática validar-enriquecimento (modo script): wikilinks + frontmatter +
                           ## Referências presente quando houve fonte
9. Relatório             + seção CANDIDATOS A GALHO (notas que cresceram além de ~600 linhas)
```

Mantém o menu da Fase 2 atual, acrescido das lentes novas:

```
Quais lentes rodar? (a higiene baseline sempre roda)
[ ] Conselho de dúvidas — 8 leitores extraem dúvidas e roteiam pras lentes
[ ] Didática — prosa explicativa; reescreve trechos secos (esp. TL;DR / "O que é" / intro)
[ ] Diagramas — mermaid + ASCII pra mecanismos e argumentos
[ ] Profundidade — trade-offs, edge cases, o que separa júnior de sênior
[ ] Lacunas — sub-tópicos que faltam
[ ] Novidade c/ fonte — fatos novos com fonte verificável
[ ] Conexões — wikilinks pro dicionário + notas relacionadas
```

Flag opcional `--triagem`: insere um gate extra após o passo 3, mostrando as dúvidas cruas
roteadas pro usuário aprovar/descartar **antes** de gerar candidatos (economiza trabalho quando
o conselho dispara muitas dúvidas). Default: sem triagem (dúvidas entram direto no plano único).

## Componente: `enriquecer-duvidas` (o conselho)

Motor de dúvidas. **Não** edita a nota — produz uma lista de dúvidas roteadas que a meta consome.

### Fan-out — 8 personas em paralelo (Agent tool, `general-purpose`)

Cada persona recebe: título + corpo integral da nota + a `fase` da nota. Pergunta-guia comum:
*"Lendo isto como [persona], o que me confundiria, o que eu não entenderia, e o que eu quereria
entender melhor?"* Cada uma devolve uma lista de dúvidas (schema abaixo).

**3 leitores por nível** (calibram pela fase do vault):

| Persona | Pergunta característica |
| ------- | ----------------------- |
| Iniciado (júnior) | "o que é esse termo? por que isso importa? não entendi o salto" |
| Adepto (pleno) | "como se compara com Y? quando eu usaria? qual o trade-off?" |
| Magus (sênior) | "e o edge case em produção? qual a pegadinha? isso ainda vale na versão nova?" |

**5 advisors adaptados** (Karpathy → leitor/professor):

| Persona | Origem | Lente que alimenta |
| ------- | ------ | ------------------ |
| O Recém-chegado | Outsider | pergunta ingênua que expõe pressuposto não-dito → **didática** |
| O Fundamentalista | First Principles | "de onde vem? qual o mecanismo por baixo?" → **didática/profundidade** |
| O Cético | Contrarian | caça impreciso/desatualizado/sem-fonte/oversimplificação → **novidade/lacunas** |
| O Conector | Expansionist | "isso liga a quê? que panorama eu perco?" → **conexões/lacunas** |
| O Praticante | Executor | "como aplico segunda de manhã? exemplo? gotcha?" → **profundidade** |

### Síntese (passo após o fan-out)

1. **Dedup** de dúvidas sobrepostas entre personas.
2. **Roteamento** de cada dúvida pra uma lente-alvo (tabela de roteamento abaixo) + prioridade.
3. **Busca no vault** (`grep` por termos/títulos relacionados): se outra nota **já responde** a
   dúvida → marca como candidato de **conexão** (linka, não duplica). Regra do vault:
   "redundância entre notas é reforço, mas linkar > repetir".

### Tabela de roteamento dúvida → lente

| Tipo de dúvida | Lente-alvo |
| -------------- | ---------- |
| compreensão / "o que é" / salto não explicado / pergunta ingênua | `enriquecer-didatica` |
| "isso se liga a / existe nota sobre" | `enriquecer-conexoes` |
| "falta cobrir o sub-tópico X" | `enriquecer-lacunas` |
| "tá desatualizado / sem fonte / fato novo" | `enriquecer-novidade` |
| "trade-off / edge case / gotcha de produção / exemplo prático" | `enriquecer-profundidade` |
| "isso pede um diagrama pra entender" | `enriquecer-diagramas` |

### Schema da dúvida

```yaml
- id: D1
  persona: iniciado          # iniciado|adepto|magus|recem-chegado|fundamentalista|cetico|conector|praticante
  duvida: "<a pergunta do leitor, na voz dele>"
  local: "§Seção onde a dúvida surge"   # ou "geral"
  lente_alvo: didatica       # destino do roteamento
  prioridade: alta           # alta|media|baixa
  ja_respondida_em: null     # path/wikilink se uma nota existente já responde
```

### Custo

8 subagentes por execução (o usuário aceitou o custo explicitamente — o objetivo é material de
estudo que leve de adepto a magus). Conselho é **uma lente selecionável**, não obrigatória.

## Componente: `enriquecer-didatica` (a peça que resolve a queixa central)

Único trabalho: gerar prosa que **ensina**, no registro Feynman já cravado no vault
(analogia concreta → pergunta retórica do leitor → camadas sintoma/causa → callout pedagógico →
resumo de uma linha). Exemplo canônico: a seção prefill/decode/KV cache da nota da janela de
contexto. Anti-exemplo: prosa enciclopédica neutra.

**Mira especialmente** TL;DR, "O que é" e introdução — onde as notas ficam secas. Duas operações:

1. **Reescrita de seção seca** (autorizada): detecta bullet-list/tabela sem prosa de intuição,
   ou salto direto pro mecanismo sem grounding. Propõe **reescrita via diff antes→depois**, item
   a item, nunca removendo em silêncio. (É o que conserta a seção "O que é" da nota exemplo.)
2. **Bloco "Intuição"**: insere grounding didático antes do mecanismo quando não existe.

Consome dúvidas roteadas `lente_alvo: didatica`. Toda adição/reescrita carrega fonte
(proveniência inalterada — vai em `## Referências`, nunca no corpo).

## Componente: `enriquecer-diagramas`

Gera **mermaid** (mindmap pra mapear argumento de seção longa; graph LR/TD pra mecanismo/fluxo;
sequence quando há protocolo) e **arte ASCII** (curvas, eixos — como a curva em U da nota exemplo).
Consome dúvidas `lente_alvo: diagramas`. Sem imagens binárias. Cada diagrama é candidato
`tipo: adicao` com `local` indicado.

## Componentes: lentes extraídas (`profundidade`, `lacunas`, `novidade`, `conexoes`)

Cada uma vira micro-skill própria, movendo o motor correspondente de `references/lentes.md`
da skill atual pro SKILL.md (ou `references/`) da micro-skill. Comportamento idêntico ao atual,
acrescido de: cada lente passa a **consumir as dúvidas roteadas pra ela** como input extra de
candidatos. `enriquecer-conexoes` continua delegando à lógica do `/verbete` pra termos ausentes
no dicionário.

## Componente: `validar-enriquecimento` (constraint-skill)

Substitui o subagente crítico atual e ganha um modo programático. Roda em dois momentos:

- **Modo crítico (passo 5):** recebe o pool de candidatos `tipo: adicao|reescrita` das lentes
  profundidade/lacunas/novidade/didática; pontua novidade+profundidade por fase (rubrica atual de
  `references/critico.md`); mantém só os que passam o gate da fase; descarta o resto com motivo.
  Conexões, diagramas e higiene **não** passam pelo crítico (como hoje).
- **Modo script (passo 8):** validação determinística (artigo §6 — "validações críticas via
  script"). `scripts/` checa:
  - frontmatter: `updated` bumpado pra hoje; `status` não regrediu; `progress` presente.
  - `## Referências` existe quando houve candidato com fonte URL.
  - wikilinks não quebrados → chama `verificar-wikilinks/scripts/check_wikilinks.py`.
  - sem remoção silenciosa (diff só com adições/substituições aprovadas).
  - **check do começo seco:** alerta se a nota ainda abre com bullet-list sob "O que é" sem
    bloco de intuição (o gap diagnosticado) — alerta, não bloqueia.

## Schema único de candidato (todas as lentes)

```yaml
- id: C1
  lente: didatica            # duvidas não gera candidato; gera dúvida roteada
  tipo: adicao               # adicao | reescrita | link | verbete | diagrama
  local: "§Nome da Seção"    # ou "após §X" | "fim da nota" | "frontmatter"
  conteudo: "<texto/diagrama rascunho>"   # p/ reescrita, é o "depois"
  antes: "<trecho original>" # SÓ quando tipo: reescrita
  fonte: { tipo: url|nota|geral, ref: "..." }
  duvida_origem: D1          # id da dúvida do conselho que originou (proveniência no plano)
```

## Formato do plano (passo 6)

Igual ao atual (agrupado por lente, diffs antes→depois, descartados recolhíveis), com duas
adições: cada item mostra `(dúvida: "<voz do leitor>")` quando veio do conselho, e grupos novos
DIDÁTICA e DIAGRAMAS. Confirmação única `[c]` executa só os marcados.

## Formato do relatório (passo 9)

```
CONCLUÍDO — <título>   (fase-alvo: <Magus>)
✓ Conselho: <n> dúvidas (<k> roteadas, <j> já respondidas em outras notas → linkadas)
✓ Didática: <n> blocos + <m> reescritas de trecho seco
✓ Diagramas: <n> (mermaid/ascii)
✓ Profundidade / Lacunas / Novidade / Conexões: <…>
– Crítico cortou <n> candidatos (óbvios para a fase)

CANDIDATOS A GALHO (nota passou de ~600 linhas)
▸ §<Seção X> — já dá sub-trilha; considere podar com o padrão tronco/galhos
```

## Layout de arquivos

```
.agents/skills/
├── enriquecer-nota/
│   ├── SKILL.md                      ← meta-skill (orquestração; encolhe)
│   └── references/
│       ├── proveniencia.md           ← mantém (compartilhado conceitualmente)
│       └── plano-e-relatorio.md      ← formatos do plano/relatório
├── enriquecer-duvidas/
│   ├── SKILL.md
│   └── references/
│       ├── personas.md               ← os 8 prompts de persona
│       └── roteamento.md             ← tabela dúvida→lente + síntese
├── enriquecer-didatica/
│   ├── SKILL.md
│   └── references/registro-feynman.md
├── enriquecer-diagramas/SKILL.md
├── enriquecer-profundidade/SKILL.md
├── enriquecer-lacunas/SKILL.md
├── enriquecer-novidade/SKILL.md
├── enriquecer-conexoes/SKILL.md
└── validar-enriquecimento/
    ├── SKILL.md
    └── scripts/
        └── validar.py                ← frontmatter + Referências + chama check_wikilinks.py
```

(`.claude/skills` é symlink pra `.agents/skills` — não duplicar.)

## Sequência de build (pra writing-plans)

1. **Constraint primeiro** (`validar-enriquecimento`): extrai o crítico atual + escreve `scripts/`.
   É o gate; o resto depende dele.
2. **Lentes extraídas** (profundidade, lacunas, novidade, conexoes): mover motores 1:1 da skill
   atual. Comportamento preservado → baixo risco.
3. **Lentes novas** (didatica, diagramas): escrever do zero com registro Feynman + dúvidas.
4. **Conselho** (`enriquecer-duvidas`): personas + síntese + roteamento.
5. **Meta-skill**: reescrever `enriquecer-nota` como orquestrador puro; remover motores embutidos.
6. **AGENTS.md / índice de skills**: registrar o grafo (meta → micro → constraint).
7. **Validação em sessão limpa**: rodar em `03 - A janela de contexto.md` e conferir que a seção
   "O que é" recebe proposta de reescrita didática.

## Edge cases (herdados + novos)

| Caso | Comportamento |
| ---- | ------------- |
| Nota sem domínio | Conexões/verbetes desativados; demais lentes seguem |
| Nota sem `fase:` | Infere; default Magus (régua mais estrita) |
| Conselho devolve 0 dúvidas | Segue só com as lentes diretas selecionadas |
| Dúvida já respondida em outra nota | Vira candidato de conexão (linka), não de didática |
| Reescrita: `antes` não casa exato | Pula o item, avisa; não edita às cegas |
| Nota passa de ~600 linhas | Cresce; lista candidatos a galho no relatório |
| WebSearch falha/offline | Lentes que dependem de web reportam "sem candidatos"; segue |
| Crítico devolve 0 sobreviventes | Mostra só higiene + conexões + diagramas |

## Validação da skill (artigo §6, métricas)

- **Triggering** da meta e das micro-skills: 10-20 queries que devem acionar + 5-10 que não.
- **Conselho:** rodar em 2-3 notas de fases diferentes; conferir que as dúvidas batem com o nível.
- **Didática:** rodar na nota da janela de contexto; a seção "O que é" deve receber reescrita.
- **Constraint:** introduzir um wikilink quebrado de propósito; o script deve pegar.
</content>
</invoke>
