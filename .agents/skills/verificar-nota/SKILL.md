---
name: verificar-nota
description: Constraint-skill: audita a qualidade estrutural de uma nota de domínio contra o padrão do vault (checklist ESTRUTURA/PROFUNDIDADE/TAMANHO/LINKS/MÍDIA). Serve de gate compartilhado entre /escrever-nota e /enriquecer-nota. Não edita — só reporta e sugere ação. Use quando o usuário pedir "verificar nota", "auditar qualidade", "checar se a nota está boa", ou após criar/enriquecer uma nota.
---

# Skill: verificar-nota

Audita uma nota de domínio contra o padrão de qualidade do vault. **Não edita** — reporta o que
está ok, o que está faltando, e sugere qual skill usar para corrigir cada item.

É o gate compartilhado entre `/escrever-nota` (roda automaticamente ao final) e `/enriquecer-nota`
(roda na Fase 0 para escolher entre Modo A e Modo B).

## Invocação

```
/verificar-nota [path]
```

- **Sem `path`:** pergunta qual nota verificar.
- **Com `path`:** usa o arquivo indicado (relativo à raiz do vault).

---

## Checklist por seção

### ESTRUTURA

| # | Item | Critério de aprovação |
|---|------|-----------------------|
| E1 | TL;DR callout | `> [!abstract] TL;DR` presente com ≥3 linhas densas (não apenas 1 frase solta) |
| E2 | Abertura com problema | Intro ou 1ª seção abre com problema/cenário real; não começa com definição ("X é um...") |
| E3 | Diagrama Mermaid | ≥1 diagrama Mermaid com semântica visual (fluxo, contraste, sequência) — não decorativo |
| E4 | Casos práticos | Seção `## Casos práticos` com ≥2 cenários de produção concretos |
| E5 | O que vem a seguir | Seção `## O que vem a seguir` presente — narrativa de ponte, não só lista de links |
| E6 | Como explicar em inglês | Seção de inglês presente (nome exato ou variação equivalente) |
| E7 | Tabela PT↔EN | Tabela de termos técnicos PT ↔ EN presente |
| E8 | Armadilhas comuns | Seção `## Armadilhas comuns` com ≥3 callouts `[!warning]` individuais |

### PROFUNDIDADE

| # | Item | Critério de aprovação |
|---|------|-----------------------|
| P1 | Código com falha | Exemplo de código mostra pelo menos 1 caso-problema, não só o caminho feliz |
| P2 | Mecanismo explicado | Nota explica *por que* funciona assim, não apenas *o quê* (anti-padrão: "X faz Y" sem explicar como) |
| P3 | Teoria subjacente | `fase: Magus` → conecta a teoria formal ou fundamento conceitual (não cobrado em Iniciado/Adepto) |

### TAMANHO

| # | Item | Critério de aprovação |
|---|------|-----------------------|
| T1 | Iniciado | `fase: Iniciado` → ≥300 linhas |
| T2 | Adepto | `fase: Adepto` → ≥400 linhas |
| T3 | Magus | `fase: Magus` → ≥500 linhas |

### LINKS

| # | Item | Critério de aprovação |
|---|------|-----------------------|
| L1 | Wikilink cross-galho | ≥1 `[[wikilink]]` apontando para nota fora da pasta atual |
| L2 | Referência externa | Seção `## Fontes` com ≥1 link externo verificável |

### MÍDIA

| # | Item | Critério de aprovação |
|---|------|-----------------------|
| M1 | Vídeo ou podcast embutido | ≥1 callout `[!tip]` com link para vídeo/podcast relevante |

---

## Como executar

1. Lê a nota (valida path; aborta com erro se não encontrar).
2. Infere `fase:` do frontmatter (Iniciado/Adepto/Magus). Se ausente: aplica critério de Adepto.
3. Conta linhas totais do arquivo.
4. Verifica cada item da checklist por busca estrutural no conteúdo.
5. Exibe relatório agrupado por seção:

```
VERIFICAÇÃO — <título>   (fase: <Adepto>)   <N> linhas

ESTRUTURA
✓ E1 TL;DR callout — 5 linhas
✓ E2 Abertura com problema
✗ E3 Diagrama Mermaid — ausente
✓ E4 Casos práticos — 3 cenários
✓ E5 O que vem a seguir
✗ E6 Como explicar em inglês — seção ausente
✗ E7 Tabela PT↔EN — ausente
⚠ E8 Armadilhas comuns — 2 [!warning] (mínimo: 3)

PROFUNDIDADE
✓ P1 Código com falha
✗ P2 Mecanismo explicado — nota descreve comportamento, não mecanismo causal

TAMANHO
✓ T2 Adepto — 427 linhas (mínimo: 400)

LINKS
✓ L1 Wikilink cross-galho
✗ L2 Referência externa — seção Fontes ausente

MÍDIA
✗ M1 Vídeo/podcast embutido — callout [!tip] com mídia ausente

RESULTADO: 6/12 itens ✓   (fase: Adepto)
Aprovado: NÃO — itens críticos faltando: E3, E6, E7, P2, L2, M1
```

6. Sugere ação para cada `✗`:

| Item | Sugestão |
|------|----------|
| E3, E4, P1, P2 | `/enriquecer-nota` com lente Profundidade |
| E6, E7 | `/enriquecer-nota` com instrução "adicionar seção de inglês e tabela PT↔EN" |
| E8 | `/enriquecer-nota` com instrução "adicionar armadilhas comuns" |
| L2 | `/enriquecer-nota` com lente Novidade c/ fonte |
| M1 | `/adicionar-midia` para pesquisar e embutir vídeo/podcast relevante |
| E5 | `/enriquecer-nota` com instrução "adicionar seção O que vem a seguir" |

---

## Regras de isenção

| Caso | Isenção aplicada |
|------|-----------------|
| Notas `type: meta` ou `type: glossary` | Isentas de E6 e E7 (sem seção de inglês) |
| Brotos (filename `Xa`, `Xb` — ex: `04a.md`) | Isentos de T1/T2/T3 (sem piso de linhas) |
| `fase: Iniciado` ou `fase: Adepto` | Isentos de P3 (teoria subjacente) |
| `fase: Iniciado` | M1 recomendado, não obrigatório (isenção parcial) |

---

## Convenções rígidas

- **Não edita** — esta skill é read-only. Reporta; não conserta.
- **Score de aprovação**: nota "aprovada" quando ≥9/12 itens ✓ (considerando isenções).
- **Score crítico**: <6/12 itens ✓ → informa que a nota precisa de Modo B (elevação estrutural) antes de enriquecimento de conteúdo.
- **⚠ (aviso)**: item presente mas abaixo do mínimo quantitativo (ex: 2 armadilhas quando precisa 3).
- **✗ (falha)**: item completamente ausente.

## Edge cases

| Caso | Comportamento |
|------|---------------|
| Arquivo não encontrado | Aborta com erro claro |
| Nota sem `fase:` | Aplica critério de Adepto; avisa |
| Nota fora de `03-Dominios/` | Isenção total de L1 (sem domínio definido) |
| Nota sem seção de código | P1 marcado como N/A (não se aplica a notas conceptuais puras) |
