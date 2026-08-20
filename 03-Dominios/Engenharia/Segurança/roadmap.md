---
title: "Roadmap — Segurança Conceitual"
created: 2026-08-20
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Segurança Conceitual

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`.

**Galho:** `03-Dominios/Engenharia/Segurança`
**Diagnóstico:** 2026-08-20
**Última execução:** —

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado 01-06 · Adepto 07-13 · Magus 14-22)
**Piso de linhas:** aplicável nominalmente (Iniciado ≥300 / Adepto ≥400 / Magus ≥500), **mas** vigora o padrão capítulo de livro, que o substitui — as 22 notas estão entre 450 e 496 linhas, dentro da faixa de nota profunda. Piso só é gap real se a nota for rasa de conteúdo, não por contagem.

> [!warning] Achado de inventário — `fase:` em minúscula é problema **do vault**, não deste galho
> As 22 notas usam `fase: iniciado|adepto|magus` em minúscula, contra a convenção (`Iniciado|Adepto|Magus`). A conferência vault-wide mostrou que **não é defeito local**: são **864 notas em minúscula contra 1.237 em maiúscula** (~41%), espalhadas por dezenas de galhos — inclusive alguns já declarados 100% completos, como Complexidade de Software (17) e Padrões de Projeto/GoF (23). Também aparecem 12 notas com `fase: Adepto→Magus`.
> Consequência: qualquer `GROUP BY fase` do Dataview parte cada fase em duas fatias, e MOCs que filtram por fase perdem metade das notas.
> **Fora do escopo deste passe** — é normalização mecânica de vault inteiro (`sed`), com decisão do usuário sobre quando rodar e como isolar do trabalho paralelo na working tree.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 22 |
| ⬜ pendente | 22 |
| ➖ não precisa | 0 |
| ✅ feita | 0 |
| % concluído | 0% |

> Tabela preenchida ao final do diagnóstico (Fase 3).


> [!info] Como este diagnóstico foi feito — e por que não foram 22 subagentes
> As notas **01, 02 e 03** foram auditadas por subagente, uma por uma. As três voltaram com **score idêntico e os mesmos seis gaps**, o que indicou galho gerado de um molde único. A hipótese foi então testada por varredura estrutural das 22 notas (presença de seção, contagem de `[!warning]`, de Mermaid, de wikilink cross-galho, abertura de cada nota) — e confirmada. As 19 entradas restantes derivam dessa **medição**, não de leitura integral. O que isso não cobre: julgamento fino de P2 (mecanismo) nota a nota. As três lidas passaram em P2 com folga; se alguma das 19 falhar, aparece no momento da execução.

> [!warning] Dois erros do meu diagnóstico inicial, corrigidos aqui
> Eu havia reportado **"zero diagramas Mermaid nas 22 notas"** e **"seção de inglês 0/22"**. Ambos falsos.
> - **Mermaid:** o galho tem **5 a 8 diagramas por nota** (~130 no total). A contagem inicial saiu zerada por interferência do proxy RTK no `grep`. **E3 passa nas 22.**
> - **Inglês:** existe em 22/22, sob o nome `## Em entrevista` — com frases prontas em inglês e vocabulário PT↔EN. **E6 e E7 passam nas 22.**
> A lição é a mesma do resto do galho: o que parecia ausência era **nome diferente** (ou ferramenta mentindo).

> [!tip] O padrão que barateia o passe inteiro
> O galho não carece de conteúdo — carece de **nomes canônicos**. Três seções existem com outro rótulo:
> - `## Conexões` faz o papel de `## O que vem a seguir`, mas como lista de links, sem ponte narrativa → E5.
> - O callout `[!info] Lastro` guarda as fontes que deveriam estar em `## Fontes` → L2 (mesma assinatura já encontrada no galho de Testes).
> - Casos reais existem (Equifax, Logjam, Mirai, Target) espalhados em `[!example]` e seções `## Caso histórico:` → E4 é promoção, não redação.
> Sobram como trabalho de fato novo: **M1 (mídia, 22/22)** e **L1** nas 14 notas sem wikilink cross-galho.

> [!warning] Quebra manual de linha — não corrigir em massa
> As 22 notas têm quebra manual em ~110 colunas, contra a regra do vault. **O usuário corrige manualmente à medida em que lê.** O passe de enriquecimento não deve reformatar o texto existente; apenas **o texto novo** que ele escrever precisa sair em linha única por parágrafo.

---

## Notas

#### 01 - O que é segurança conceitual   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 480 linhas reais · fase: iniciado · status: evergreen
- **Núcleo/gaps:** E4 (sem seção `## Casos práticos` dedicada, apenas exemplos espalhados) · E5 (seção `## Conexões` existe, mas não é a ponte narrativa `## O que vem a seguir`) · E8 (só 2 `[!warning]` soltos, sem seção `## Armadilhas comuns` com ≥3) · L1 (os 3 wikilinks em Conexões apontam para notas da própria pasta Segurança, nenhum cross-galho) · L2 (fontes existem, mas sob `> [!info] Lastro`, não `## Fontes`) · M1 (nenhum vídeo/podcast embutido)
- **Score:** 6/11 (P1 N/A — nota conceitual sem exemplo de código)
- **Plano de execução:**
  - Adicionar seção `## Casos práticos` com ≥2 cenários de produção, reaproveitando/expandindo Equifax, Mirai/Dyn, RSA/Target/Twitter ou SolarWinds já citados no corpo → ativa E4
  - Adicionar seção `## O que vem a seguir` com ponte narrativa para [[02 - Pensar como adversário]], complementando (não substituindo) `## Conexões` → ativa E5
  - Criar seção `## Armadilhas comuns` com ≥3 callouts `[!warning]` individuais, migrando os 2 já existentes (confidencialidade≠privacidade; fator humano) e somando um terceiro (ex.: confundir safety com security) → ativa E8
  - Adicionar ≥1 wikilink para nota fora da pasta Segurança (ex.: nota de segurança conceitual em Fundamentos ou trilha Auth e Identidade) → ativa L1
  - Renomear/reestruturar `> [!info] Lastro` como seção `## Fontes`, mantendo os mesmos links já verificados → ativa L2
  - Pesquisar e embutir ≥1 vídeo/podcast relevante sobre tríade CIA/segurança conceitual como callout `[!tip]` → ativa M1
- **Resultado:** —



#### 02 - Pensar como adversário   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 451 linhas reais · fase: iniciado · status: evergreen
- **Núcleo/gaps:** E4 (sem seção `## Casos práticos`), E5 (seção `## Conexões` é lista de links, não ponte narrativa `## O que vem a seguir`), E8 (sem seção `## Armadilhas comuns` com ≥3 `[!warning]`), L1 (todos os wikilinks apontam para notas dentro da própria pasta Segurança), L2 (fontes estão em callout `[!info] Lastro`, não em seção `## Fontes`), M1 (nenhum callout `[!tip]` com vídeo/podcast)
- **Score:** 6/12
- **Plano de execução:**
  - Criar seção `## Casos práticos` com ≥2 cenários de produção concretos, reaproveitando o caso Target 2013 e o worked example do login, mais um cenário adicional (resolve E4)
  - Transformar a seção `## Conexões` em `## O que vem a seguir` com ponte narrativa explicando por que as próximas notas interessam, mantendo os wikilinks (resolve E5)
  - Criar seção `## Armadilhas comuns` reaproveitando os `[!warning]` já existentes (regra das trust boundaries, erro comum sobre perfil de adversário) e somando ao menos um novo, até ≥3 callouts individuais (resolve E8)
  - Adicionar ao menos um `[[wikilink]]` para nota fora da pasta Segurança, ligando a um conceito correlato em outro domínio de Engenharia (resolve L1)
  - Converter o callout `[!info] Lastro` em seção `## Fontes` com os links externos já existentes, mantendo-os clicáveis (resolve L2)
  - Pesquisar e embutir um callout `[!tip]` com vídeo ou podcast relevante sobre threat modeling/STRIDE (resolve M1)
- **Resultado:** —

#### 03 - Economia e fator humano da segurança   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 451 linhas reais · fase: iniciado · status: evergreen
- **Núcleo/gaps:** E4 (sem seção `## Casos práticos`; os exemplos Equifax e Google BeyondCorp estão soltos em callouts `[!example]`, não numa seção dedicada), E5 (seção `## Conexões` é lista de links, não ponte narrativa `## O que vem a seguir`), E8 (só 1 `[!warning]` isolado — "Teatro no contexto corporativo" —, sem seção `## Armadilhas comuns` com ≥3), L1 (todos os wikilinks — 01, 02, 04, 12 — apontam para notas dentro da própria pasta Segurança), L2 (fontes estão em callout `[!info] Lastro`, não em seção `## Fontes`), M1 (nenhum callout `[!tip]` com vídeo/podcast)
- **Score:** 6/12
- **Plano de execução:**
  - Criar seção `## Casos práticos` com ≥2 cenários de produção concretos, reaproveitando Equifax (2017) e Google BeyondCorp já presentes no texto, mais um cenário adicional se necessário (resolve E4)
  - Transformar a seção `## Conexões` em `## O que vem a seguir` com ponte narrativa explicando por que design seguro (nota 04) e autenticação (nota 12) interessam depois deste tema, mantendo os wikilinks (resolve E5)
  - Criar seção `## Armadilhas comuns` reaproveitando o `[!warning]` existente (teatro corporativo) e somando ao menos dois novos (ex.: confundir compliance com segurança real, treinar sem redesenhar o controle), até ≥3 callouts individuais (resolve E8)
  - Adicionar ao menos um `[[wikilink]]` para nota fora da pasta Segurança, ligando a conceito correlato (ex.: incentivos/teoria de jogos em Complexidade de Software ou vieses cognitivos em outro domínio) (resolve L1)
  - Converter o callout `[!info] Lastro` em seção `## Fontes` com os links externos já existentes, mantendo-os clicáveis (resolve L2)
  - Pesquisar e embutir um callout `[!tip]` com vídeo ou podcast relevante sobre economia de segurança, engenharia social ou usable security (resolve M1)
- **Resultado:** —

#### 04 - Princípios de design seguro   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 451 linhas · fase: iniciado · status: evergreen · 7 Mermaid · 2 `[!warning]` · 0 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L1, L2, M1
- **Score:** 5/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 2 já existentes em vez de duplicar → ativa E8
  - Acrescentar ≥1 wikilink cross-galho (Auth e Identidade, Redes/TLS, Matemática ou SO, conforme o assunto da nota) → ativa L1
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 05 - Aleatoriedade e segredos   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 457 linhas · fase: iniciado · status: evergreen · 5 Mermaid · 2 `[!warning]` · 0 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L1, M1
- **Score:** 6/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 2 já existentes em vez de duplicar → ativa E8
  - Acrescentar ≥1 wikilink cross-galho (Auth e Identidade, Redes/TLS, Matemática ou SO, conforme o assunto da nota) → ativa L1
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 06 - Hashing criptográfico   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 461 linhas · fase: iniciado · status: evergreen · 6 Mermaid · 2 `[!warning]` · 0 wikilink cross-galho
- **Núcleo/gaps:** E2, E4, E5, E8, L1, L2, M1
- **Score:** 4/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Reescrever a abertura: hoje começa com definição ("Uma função de hash criptográfica é uma função matemática que…"); trocar por cenário/problema — a nota já tem o material (MD5 morto, hash de senha) → ativa E2
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 2 já existentes em vez de duplicar → ativa E8
  - Acrescentar ≥1 wikilink cross-galho (Auth e Identidade, Redes/TLS, Matemática ou SO, conforme o assunto da nota) → ativa L1
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 07 - Criptografia simétrica   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 464 linhas · fase: adepto · status: evergreen · 8 Mermaid · 2 `[!warning]` · 0 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L1, L2, M1
- **Score:** 5/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 2 já existentes em vez de duplicar → ativa E8
  - Acrescentar ≥1 wikilink cross-galho (Auth e Identidade, Redes/TLS, Matemática ou SO, conforme o assunto da nota) → ativa L1
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 08 - Criptografia assimétrica   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 460 linhas · fase: adepto · status: evergreen · 5 Mermaid · 2 `[!warning]` · 4 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L2, M1
- **Score:** 6/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 2 já existentes em vez de duplicar → ativa E8
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 09 - Troca de chaves   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 473 linhas · fase: adepto · status: evergreen · 5 Mermaid · 2 `[!warning]` · 2 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L2, M1
- **Score:** 6/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 2 já existentes em vez de duplicar → ativa E8
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 10 - MAC, HMAC e assinaturas digitais   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 454 linhas · fase: adepto · status: evergreen · 5 Mermaid · 2 `[!warning]` · 0 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L1, L2, M1
- **Score:** 5/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 2 já existentes em vez de duplicar → ativa E8
  - Acrescentar ≥1 wikilink cross-galho (Auth e Identidade, Redes/TLS, Matemática ou SO, conforme o assunto da nota) → ativa L1
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 11 - PKI e certificados   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 461 linhas · fase: adepto · status: evergreen · 6 Mermaid · 1 `[!warning]` · 1 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L2, M1
- **Score:** 6/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 1 já existentes em vez de duplicar → ativa E8
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 12 - Autenticação   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 463 linhas · fase: adepto · status: evergreen · 5 Mermaid · 2 `[!warning]` · 2 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L2, M1
- **Score:** 6/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 2 já existentes em vez de duplicar → ativa E8
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 13 - Autorização e controle de acesso   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 470 linhas · fase: adepto · status: evergreen · 6 Mermaid · 1 `[!warning]` · 2 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L2, M1
- **Score:** 6/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 1 já existentes em vez de duplicar → ativa E8
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 14 - Criptografia em trânsito e em repouso   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 461 linhas · fase: magus · status: evergreen · 6 Mermaid · 2 `[!warning]` · 2 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L2, M1
- **Score:** 6/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 2 já existentes em vez de duplicar → ativa E8
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 15 - Ataques a sistemas cripto   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 470 linhas · fase: magus · status: evergreen · 6 Mermaid · 1 `[!warning]` · 2 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L2, M1
- **Score:** 6/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 1 já existentes em vez de duplicar → ativa E8
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 16 - Classes de vulnerabilidade   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 470 linhas · fase: magus · status: evergreen · 6 Mermaid · 2 `[!warning]` · 0 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L1, L2, M1
- **Score:** 5/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 2 já existentes em vez de duplicar → ativa E8
  - Acrescentar ≥1 wikilink cross-galho (Auth e Identidade, Redes/TLS, Matemática ou SO, conforme o assunto da nota) → ativa L1
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 17 - Confiança transitiva e Trusting Trust   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 496 linhas · fase: magus · status: evergreen · 6 Mermaid · 2 `[!warning]` · 0 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L1, L2, M1
- **Score:** 5/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 2 já existentes em vez de duplicar → ativa E8
  - Acrescentar ≥1 wikilink cross-galho (Auth e Identidade, Redes/TLS, Matemática ou SO, conforme o assunto da nota) → ativa L1
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 18 - Gestão de chaves e segredos   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 465 linhas · fase: magus · status: evergreen · 6 Mermaid · 2 `[!warning]` · 0 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L1, L2, M1
- **Score:** 5/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 2 já existentes em vez de duplicar → ativa E8
  - Acrescentar ≥1 wikilink cross-galho (Auth e Identidade, Redes/TLS, Matemática ou SO, conforme o assunto da nota) → ativa L1
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 19 - Zero trust e defesa em profundidade   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 465 linhas · fase: magus · status: evergreen · 5 Mermaid · 1 `[!warning]` · 0 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L1, L2, M1
- **Score:** 5/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 1 já existentes em vez de duplicar → ativa E8
  - Acrescentar ≥1 wikilink cross-galho (Auth e Identidade, Redes/TLS, Matemática ou SO, conforme o assunto da nota) → ativa L1
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 20 - Privacidade, anonimato e metadados   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 462 linhas · fase: magus · status: evergreen · 6 Mermaid · 3 `[!warning]` · 1 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, L2, M1
- **Score:** 7/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 21 - Criptografia pós-quântica   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 450 linhas · fase: magus · status: evergreen · 5 Mermaid · 2 `[!warning]` · 0 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L1, L2, M1
- **Score:** 5/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 2 já existentes em vez de duplicar → ativa E8
  - Acrescentar ≥1 wikilink cross-galho (Auth e Identidade, Redes/TLS, Matemática ou SO, conforme o assunto da nota) → ativa L1
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

#### 22 - Capstone - segurança como engenheiro   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 491 linhas · fase: magus · status: evergreen · 5 Mermaid · 0 `[!warning]` · 0 wikilink cross-galho
- **Núcleo/gaps:** E4, E5, E8, L1, L2, M1
- **Score:** 5/11 (P1 N/A — nota conceitual)
- **Plano de execução:**
  - Criar `## Casos práticos` com ≥2 cenários, promovendo o que já está espalhado em `[!example]` e nas seções de caso histórico desta nota → ativa E4
  - Converter `## Conexões` em `## O que vem a seguir` com ponte narrativa (por que a próxima nota importa), preservando os wikilinks → ativa E5
  - Criar `## Armadilhas comuns` com ≥3 `[!warning]`, **movendo** os 0 já existentes em vez de duplicar → ativa E8
  - Acrescentar ≥1 wikilink cross-galho (Auth e Identidade, Redes/TLS, Matemática ou SO, conforme o assunto da nota) → ativa L1
  - Converter o callout `[!info] Lastro` em `## Fontes` com URLs clicáveis → ativa L2
  - Buscar e embutir vídeo/podcast verificado por transcrição → ativa M1
- **Resultado:** —

