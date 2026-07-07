---
title: "Roadmap — Framework de entrevista"
created: 2026-07-06
type: meta
publish: false
tags:
  - meta
  - roadmap
  - system-design
---

# Roadmap — Framework de entrevista (sub-galho 1)

Roadmap-folha do sub-galho `System Design/1 - Framework de entrevista`. Fase **Iniciado** (piso ≥300 linhas; alvo de densidade ~440-540). Spec: [[00-Meta/specs/2026-07-06-system-design-trilha-design]].

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 5 |
| ⬜ pendente | 0 |
| ✅ feita | 5 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - O que é System Design e o que a entrevista avalia   [substantivo]
- **Estado:** ✅ feita (2026-07-06) · fase: Iniciado · **EXEMPLAR do galho** (padrão a copiar)
- **Escopo:** o sinal que o entrevistador busca (estruturação, trade-offs, comunicação — não "a resposta"); rubrica de senioridade; RF vs RNF como primeira lente.
- **Fontes:** Alex Xu Vol.1 cap.1; Hello Interview "Delivery".
- **Resultado:** 290 linhas / 4097 palavras; 3 Mermaid, 5 [!warning], 4 [!question]-, tabela PT↔EN; seções extras (o que o entrevistador anota, arquétipos de pergunta, como recuperar quando trava). Verificado: URLs canônicas conferem; wikilinks-irmãos apontam pras notas 02-05 (a criar).

#### 02 - Clarificar requisitos   [substantivo]
- **Estado:** ✅ feita (2026-07-06) · fase: Iniciado
- **Escopo:** perguntas de escopo; separar requisitos funcionais de não-funcionais (latência, disponibilidade, consistência); fechar o escopo antes de desenhar.
- **Fontes:** System Design Primer; Alex Xu; Hello Interview.
- **Resultado:** 202 linhas / 3249 palavras; 1 Mermaid, 4 [!warning], 3 [!question]-. Abertura problema-first (candidato que aceita "bit.ly" e desenha sem clarificar); banco de perguntas de escopo + separação RF/RNF na prática. Verificado: links-irmãos (→03), URLs reais, fronteiras ok.

#### 03 - Estimativas de escala (back-of-envelope)   [substantivo]
- **Estado:** ✅ feita (2026-07-06) · fase: Iniciado
- **Escopo:** QPS = usuários×ações/86.400; peak factor 3-5; storage/bandwidth; latency numbers (jboner); powers of two.
- **Fontes:** jboner gist; ByteByteGo estimation; Hello Interview "Numbers to Know".
- **Resultado:** 295 linhas / 3776 palavras; 2 Mermaid, 3 [!warning], 3 [!question]-. Latency numbers confirmados na fonte (jboner) + valores de rede cruzados com Hello Interview 2026. Verificado: links-irmãos (→04), URLs reais.

#### 04 - API design e data model na entrevista   [substantivo]
- **Estado:** ✅ feita (2026-07-06) · fase: Iniciado
- **Escopo:** esboçar endpoints/contratos e o modelo de dados enxuto; quando SQL vs NoSQL entra cedo.
- **Fontes:** Alex Xu; Hello Interview; [[API Design]].
- **Resultado:** 241 linhas / 3241 palavras; 2 Mermaid, 3 [!warning], 2 [!question]-. Verificado: links-irmãos (→05) e [[API Design]], fronteiras ok. **Débito leve:** 2-3 fontes fracas (GeeksforGeeks, Prachub "R-CRUD 2026") — trocar por fonte forte num enriquecimento futuro.

#### 05 - Do diagrama macro ao deep dive e trade-offs   [substantivo]
- **Estado:** ✅ feita (2026-07-06) · fase: Iniciado · **FECHA o sub-galho**
- **Escopo:** sequência dos 45 min — desenho de alto nível, aprofundar 1-2 componentes, fechar com trade-offs e evolução.
- **Fontes:** Alex Xu Vol.1; Hello Interview "Delivery"; System Design Primer.
- **Resultado:** 191 linhas / 3382 palavras; 2 Mermaid (diagrama macro do encurtador + fluxo de escolha do deep dive), 3 [!warning], 4 [!question]-. Fecha o arco do encurtador (notas 02-05) e linka pro SG2. Verificado: fonte fraca (befreed.ai) removida do corpo e das Fontes; links-irmãos e link pro SG2 ok.
