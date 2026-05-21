---
title: "Spec — Skill /glosa + reestruturação do vault em 5 zonas"
date: 2026-04-27
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Skill `/glosa` + reestruturação do vault em 5 zonas

## 1. Contexto e motivação

O Codex Technomanticus cresce como commonplace book pessoal — cada vez mais notas em [[IA]], [[Arquitetura]], [[03-Dominios/JavaScript/index]], etc. Mas há uma lacuna: **artigos lidos não viram nada**. Hoje o fluxo é:

1. Achar um link interessante → cola em `00 - Inbox/Entradas.md`
2. Ler o artigo no navegador
3. Esquecer

Resultado: muitas vezes o autor procura artigos que sabe ter lido, não acha, sente que perdeu o conhecimento. Não há banco de dados pesquisável do que foi lido.

A intenção é montar esse banco com **baixo custo por entrada e alto retorno em pesquisa**: ficha leve por artigo, metadados ricos pra busca, comentário pessoal pra "voz própria" no banco. Não é Zettelkasten profundo — é **diário de leitura curado**.

A solução tem duas partes:

- **Reestruturação do vault em 5 zonas** que tornam o pipeline "captura → destilação → integração" explícito na hierarquia de pastas
- **Skill `/glosa`** que automatiza a criação da ficha a partir de uma URL

A skill é a peça que fecha o loop: tira o atrito de "fichar" e torna o gesto natural enquanto o artigo ainda está fresco.

## 2. Objetivo

Entregar:

1. Um vault reorganizado em 5 zonas numeradas (`00-Meta`, `01-Pergaminhos`, `02-Glosas`, `03-Domínios`, `04-Sendas`) que reflete o pipeline cognitivo do commonplace book
2. Uma skill `/glosa <url>` que, dado um link, gera um fichamento estruturado em `02-Glosas/<ano>-<slug>.md` e remove o link de `01-Pergaminhos/entradas.md` se ele estava lá

Tudo entregue em duas fases independentes:

- **Fase A** (reestrutura): migração de pastas + auditoria de configs (Quartz, Obsidian, deploy)
- **Fase B** (skill): criação da skill e do template

## 3. Escopo

### Em escopo

- Renomear/mover 14 pastas existentes pra estrutura de 5 zonas
- Criar zona `02-Glosas/` (vazia inicialmente) e `04-Sendas/senda-frontend/` (placeholder)
- Criar `00-Meta/workflow.md` documentando as 5 zonas e o fluxo `/glosa`
- Criar `00-Meta/templates/template-glosa.md` (template Templater pro Obsidian)
- Auditar e atualizar configs do Quartz, `.obsidian/`, scripts de deploy cross-repo
- Criar a skill `.claude/skills/glosa/SKILL.md` com comportamento descrito na seção 7
- Suporte a artigos web (HTML via WebFetch)
- Idiomas suportados: PT-BR e EN (detecção automática)

### Fora de escopo (trabalho futuro)

- **Outros tipos de fonte** — PDF, YouTube, podcasts, tweets, papers acadêmicos. Quando vier um link de tipo não-suportado, a skill avisa e não escreve arquivo.
- **Sugestão automática de wikilinks** no campo "Ver também" — exigiria indexar tags/títulos do vault inteiro a cada chamada. Adiado pra v2.
- **Geração automática de "Meu comentário"** — deliberadamente deixado vazio. Esse campo é onde a ficha vira do autor e não da IA.
- **Conteúdo da Senda Frontend** — só o placeholder vazio é criado. O conteúdo (JS/TS/HTML/CSS/React/React+TS) é trabalho de spec separado.
- **Detecção de duplicatas semânticas** — a skill só checa colisão de slug.
- **Migração de arquivos do apocrypha** — o repo apocrypha (privado) não é tocado por esta spec.
- **Refactor das notas existentes em Domínios** — só o path muda; conteúdo e wikilinks internos ficam intactos.

## 4. Decisões e justificativas

### 4.1 Por que 5 zonas e não 3 ou 4?

O pipeline mental real tem 3 estados (bruto → destilado → integrado), mas o vault precisa de 2 zonas auxiliares pra funcionar: **Meta** (templates, guia, recursos meta-carreira — coisas sobre o codex em si) e **Sendas** (caminhos curatoriais que sequenciam Domínios pra estudo, ex: Trilha Entrevistas).

Sem Meta, materiais "sobre o sistema" se misturam com conhecimento técnico e poluem a navegação. Sem Sendas, trilhas viram "domínios disfarçados" e quebram a regra de "Domínio = conhecimento atômico evergreen".

### 4.2 Por que o nome "Glosas"?

*Glosa* é um termo técnico-histórico: anotação que estudantes medievais faziam nas margens de textos canônicos. Descreve precisamente o que um fichamento de artigo é (uma anotação sobre um texto alheio) e mantém coerência com o tema arcano do *Codex* Technomanticus. Pergaminhos (rolos soltos) → Glosas (anotações) → Domínios (maestria) → Sendas (caminhos iniciáticos): pipeline coerente.

### 4.3 Por que template "B (Padrão)" e não A (minimalista) ou C (completo)?

A pura (TL;DR + bullets) sacrifica a "âncora textual" — sem citações verbatim, daqui a 1 ano o autor pode não ser transportado de volta ao artigo. C (completo, com aplicação prática + contra-argumentos) é overkill pra "diário de leitura"; aprofundamento real acontece quando o material é puxado pra Domínio.

B captura: metadados ricos (busca), TL;DR (recall rápido), pontos-chave (mapa do argumento), citações (âncora textual), comentário pessoal (voz própria, recuperação por sentimento), ver também (conexões). Custo: ~7 min/ficha. Retorno: alto.

### 4.4 Por que o filename usa só ano + slug?

Original: `<data-completa>-<slug>.md`. Decisão: simplificar para `<ano>-<slug>.md`. Razão: o autor não pesquisa fichas por data exata; o ano dá contexto temporal suficiente, e o frontmatter `read:` preserva a data precisa pra quem precisa. Em colisão de slug no mesmo ano, sufixar `-2`, `-3`, etc.

### 4.5 Por que Pergaminhos é um arquivo único e os links são removidos quando processados?

Um arquivo (`entradas.md`) com seções por tema (`# Notion + Obsidian`, `# Claude Code`, etc) é mais simples de buscar e revisar. **Links são removidos quando viram Glosa** — se o arquivo cresce demais, é sinal de que o autor parou de processar e precisa fichar. O tamanho do arquivo é, ele mesmo, um indicador de saúde do hábito.

### 4.6 Por que não gerar "Meu comentário" automaticamente?

Se a IA preencher, vira tentação de aceitar o que ela escreveu. Daí o banco perde personalidade e a recuperação por sentimento ("aquele artigo que me irritou") deixa de funcionar. O placeholder `*Escreva aqui sua reação, surpresas, discordâncias.*` é convite, não obrigação — pode ficar vazio, mas se for preenchido, é genuíno.

## 5. Estrutura final do vault

```text
codex-technomanticus/
├── README.md
├── index.md                           # mantém — Quartz quebra sem
├── LICENSE                            # opcional, criar se desejar (decisão durante Fase A)
├── docs/                              # specs do superpowers — mantém
├── .obsidian/  .claude/  .vscode/     # configs — mantém
├── 00-Meta/
│   ├── guia/                          # ex _guia/
│   │   └── Como usar este vault.md
│   ├── templates/                     # ex _templates/
│   │   ├── Template - Nota.md
│   │   ├── Template - Glosa.md        # NOVO
│   │   └── ... (demais templates atuais)
│   ├── recursos/                      # ex Recursos/
│   │   ├── Brag Document.md
│   │   ├── Courses.md
│   │   └── Cursos completos.md
│   ├── mestres/                       # ex Aprendizado/Mestres/
│   └── workflow.md                    # NOVO — documenta as 5 zonas e o fluxo /glosa
├── 01-Pergaminhos/
│   ├── entradas.md                    # ex "00 - Inbox/Entradas.md"
│   └── avaliar.md                     # ex "00 - Inbox/Avaliar.md"
├── 02-Glosas/                         # NOVO, vazio (populado por /glosa)
│   └── .gitkeep
├── 03-Domínios/
│   ├── Arquitetura/
│   ├── Ferramentas/
│   ├── Fundamentos/
│   ├── Go/
│   ├── IA/
│   ├── Infraestrutura/
│   ├── Inglês/                        # absorve 00 - Inbox/entradas/inglês.md
│   ├── Java/
│   ├── JavaScript/
│   └── Python/
└── 04-Sendas/
    ├── trilha-entrevistas/            # ex Aprendizado/ (nota Trilha Entrevistas.md)
    ├── rpa/                           # ex Aprendizado/RPA/
    └── senda-frontend/                # NOVO placeholder
        └── .gitkeep
```

### Mapeamento explícito

| Origem                              | Destino                                       |
| ----------------------------------- | --------------------------------------------- |
| `_guia/`                            | `00-Meta/guia/`                               |
| `_templates/`                       | `00-Meta/templates/`                          |
| `Recursos/`                         | `00-Meta/recursos/`                           |
| `Aprendizado/Mestres/`              | `00-Meta/mestres/`                            |
| `Aprendizado/Trilha Entrevistas.md` | `04-Sendas/trilha-entrevistas/`               |
| `Aprendizado/RPA/`                  | `04-Sendas/rpa/`                              |
| `00 - Inbox/Entradas.md`            | `01-Pergaminhos/entradas.md`                  |
| `00 - Inbox/Avaliar.md`             | `01-Pergaminhos/avaliar.md`                   |
| `00 - Inbox/entradas/inglês.md`     | `03-Domínios/Inglês/Inglês — entradas.md`    |
| `Arquitetura/` … `Python/`          | `03-Domínios/Arquitetura/` … `03-Domínios/Python/` |

## 6. Template da Glosa

Filename: `02-Glosas/<ano>-<slug>.md` — slug é o título normalizado pra ASCII kebab-case, max ~60 chars. Em colisão no mesmo ano: sufixo `-2`, `-3`, etc.

> Nota: no template abaixo, o título do arquivo aparece como `## Título:` por restrição de single-H1 desta spec; **no arquivo real da Glosa, é `#` (H1)**.

```markdown
---
title: "AI now writes 97% of my code"
aliases: ["AI now writes 97% of my code"]
source: https://swizec.com/blog/ai-now-writes-97-of-my-code-heres-what-i-learned/
author: Swizec Teller
site: swizec.com
published: 2026-03-15
read: 2026-04-27
type: glosa
status: lido
tags: [ia, agentic-coding, produtividade]
lang: en
publish: false
---

## Título: AI now writes 97% of my code — Swizec Teller

## TL;DR

<1 a 3 frases em PT-BR sintetizando o argumento principal do artigo>

## Pontos-chave

- bullet 1
- bullet 2
- bullet 3
- (5 a 7 bullets total, em PT-BR, fiéis ao texto)

## Citações

> "trecho verbatim 1 na língua original"

> "trecho verbatim 2"

> (3 a 5 citações marcantes)

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

-
```

### Convenções

- **Idioma das seções autorais (TL;DR, Pontos-chave, Meu comentário, Ver também):** sempre PT-BR
- **Idioma das citações:** língua original do artigo (preserva o "som" do autor)
- **Tags:** sem acento, kebab-case, 3-5 tags por ficha
- **`status`**: `lido` (default ao criar). Outros valores possíveis: `relido`, `puxado-pra-dominio`
- **`publish: false`**: Glosas não são publicadas pelo Quartz. São banco pessoal.

## 7. Skill `/glosa` — contrato

### 7.1 Invocação

- **Slash command**: `/glosa <url>` — forma canônica
- **Linguagem natural**: "Claude, fiche esse link: \<url>" — também ativa pelo trigger no description da skill

### 7.2 Fluxo principal

1. **Validar URL**: HTTP/HTTPS bem-formado. Se não, erro e abortar.
2. **Detectar tipo de fonte**: domínio youtube.com/youtu.be → "tipo não suportado em MVP"; URL terminando em `.pdf` → "PDFs não suportados em MVP — me passe a URL canônica e o conteúdo manualmente"; demais → assume HTML.
3. **WebFetch da URL** com prompt pedindo extração de: título, autor, nome do site, data de publicação, idioma, e o body do artigo em markdown.
4. **Gerar draft** do template B:
   - **TL;DR**: 1-3 frases em PT-BR sintetizando o argumento principal
   - **Pontos-chave**: 5-7 bullets em PT-BR fiéis ao texto
   - **Citações**: 3-5 trechos verbatim na língua original que parecem mais marcantes (frases de impacto, definições, dados)
   - **Tags**: 3-5 tags em kebab-case sem acento
   - **`Meu comentário`**: literalmente o placeholder `*Escreva aqui sua reação, surpresas, discordâncias.*`
   - **`Ver também`**: literal `-` (vazio)
5. **Calcular filename**: `<ano-de-leitura>-<slug-do-titulo>.md`. Slug: ASCII, kebab-case, max 60 chars, palavras vazias do português ("de", "da", "o", "a") removidas se necessário pra caber.
6. **Resolver colisão**: se `02-Glosas/<filename>` já existe, tentar `<filename>-2`, `<filename>-3`, etc.
7. **Escrever arquivo** em `02-Glosas/<filename>` com Write tool.
8. **Limpar Pergaminhos**: ler `01-Pergaminhos/entradas.md` linha por linha. Se alguma linha **contém a URL como substring** (cobrindo os três formatos usados: `<url>`, `[texto](url)`, URL crua), remover a linha inteira. Se a remoção deixar uma seção (`# Header`) sem conteúdo, manter o header — autor decide se remove na próxima revisão manual.
9. **Reportar ao autor** uma destas duas mensagens, conforme o caso:
   - `Glosa criada: 02-Glosas/2026-<slug>.md. Link removido de Pergaminhos: ✓`
   - `Glosa criada: 02-Glosas/2026-<slug>.md. Link não estava em Pergaminhos.`

### 7.3 Edge cases

| Situação                              | Comportamento                                                                 |
| ------------------------------------- | ----------------------------------------------------------------------------- |
| URL malformada                        | Erro + abortar; não escreve nada                                              |
| WebFetch falha (404, paywall, timeout)| Erro com mensagem clara; não escreve nada                                     |
| Tipo não suportado (PDF, YouTube)     | Aviso "MVP só HTML"; não escreve nada                                         |
| Título com caracteres especiais       | Slug normalizado pra ASCII (sem acento, sem pontuação, kebab-case)            |
| Idioma não detectado                  | Default `lang: en` (maioria dos artigos técnicos lidos é em inglês) |
| Data de publicação não detectada      | Frontmatter `published:` vazio; skill relata "data de publicação não detectada" |
| Autor não detectado                   | `author: "(desconhecido)"`                                                    |
| Mesma URL já fichada (mesmo slug)     | Sufixo `-2` é aplicado; skill avisa "atenção: pode ser duplicata semântica"   |
| URL em Pergaminhos com texto extra    | Match pela URL substring; remove a linha inteira                              |

### 7.4 Estrutura da skill

```text
.claude/skills/glosa/
└── SKILL.md
```

`SKILL.md` contém:

- Frontmatter com `name: glosa` e `description` cobrindo trigger ("artigo", "fichar", "ficha", "/glosa")
- Instruções pra o Claude executar o fluxo da seção 7.2
- Template inline da Glosa (seção 6)
- Edge cases (seção 7.3)
- Convenções de idioma (seção 6)

## 8. Fluxos típicos

### 8.1 Fluxo "li agora, quero fichar"

```text
Usuário: /glosa https://swizec.com/blog/ai-now-writes-97-of-my-code/

Claude: Glosa criada: 02-Glosas/2026-ai-now-writes-97-of-my-code.md
Link não estava em Pergaminhos.

Quer revisar antes de salvar como lido? (TL;DR + Pontos-chave gerados)
```

### 8.2 Fluxo "tenho um link em Pergaminhos, quero fichar"

```text
Usuário: Vamos fichar esse link de Pergaminhos:
https://addyosmani.com/blog/factory-model/

Claude: Glosa criada: 02-Glosas/2026-factory-model.md
Link removido de Pergaminhos: ✓ (estava na seção "# Claude Code")
```

### 8.3 Fluxo "URL é PDF/YouTube"

```text
Usuário: /glosa https://www.youtube.com/watch?v=Unzc731iCUY

Claude: Vídeo do YouTube — fichamento de vídeo não está no MVP.
Por enquanto: salve o link em 01-Pergaminhos/entradas.md e marque como
"a fichar manualmente". Suporte a YouTube/PDF é trabalho futuro.
```

## 9. Fase A — plano de migração

### 9.1 Pré-condições e auditoria

Antes de mover qualquer arquivo:

1. **Auditar `quartz.config.ts`** no repo Quartz (cross-repo): buscar refs literais a `_templates`, `_guia`, `00 - Inbox`, `Recursos`, `Aprendizado`. Reportar matches.
2. **Auditar `.obsidian/`** do codex: arquivos de config (templates folder, attachments folder, daily notes folder, etc) podem ter paths hardcoded.
3. **Auditar scripts de deploy cross-repo** (referência em memória `project_codex.md`).
4. **Auditar `.gitignore`** por refs aos paths antigos.
5. **Verificar wikilinks**: Obsidian indexa por nome do arquivo (não path), então renames de pasta não quebram wikilinks `[[Nome]]`. Mas wikilinks com path absoluto (`[[Java/Core/Streams]]`) quebrariam. Buscar `grep -rn "\[\[.*/.*\]\]"` pra detectar.

### 9.2 Movimentação

Todos os movimentos via `git mv` pra preservar histórico:

1. `git mv _guia 00-Meta/guia`
2. `git mv _templates 00-Meta/templates`
3. `git mv Recursos 00-Meta/recursos`
4. `git mv Aprendizado/Mestres 00-Meta/mestres`
5. `git mv Aprendizado/Trilha\ Entrevistas.md 04-Sendas/trilha-entrevistas/Trilha\ Entrevistas.md` (criar pasta destino antes)
6. `git mv Aprendizado/RPA 04-Sendas/rpa`
7. `rmdir Aprendizado` (vazia agora)
8. `git mv "00 - Inbox/Entradas.md" 01-Pergaminhos/entradas.md`
9. `git mv "00 - Inbox/Avaliar.md" 01-Pergaminhos/avaliar.md`
10. `git mv "00 - Inbox/entradas/inglês.md" "03-Domínios/Inglês/Inglês — entradas.md"`
11. `rmdir "00 - Inbox/entradas" "00 - Inbox"`
12. `git mv Arquitetura 03-Domínios/Arquitetura` (e idem pras outras 9 pastas de domínio: Ferramentas, Fundamentos, Go, IA, Infraestrutura, Inglês, Java, JavaScript, Python)
13. Criar `02-Glosas/.gitkeep`, `04-Sendas/senda-frontend/.gitkeep`
14. Criar `00-Meta/workflow.md` (conteúdo: explicação das 5 zonas + descrição do fluxo `/glosa`)
15. Criar `00-Meta/templates/Template - Glosa.md` (versão Templater do template seção 6)

### 9.3 Pós-migração

- Atualizar configs identificadas na auditoria
- Build local do Quartz pra confirmar publicação intacta (se aplicável a este repo) ou validar com o repo Quartz que os paths novos não quebraram a build
- Commit único: `feat(estrutura): reorganiza vault em 5 zonas (Meta/Pergaminhos/Glosas/Domínios/Sendas)`
- Atualizar `_guia/Como usar este vault.md` (agora em `00-Meta/guia/`) refletindo a nova estrutura

### 9.4 Critério de aceitação da Fase A

- [ ] Todas as 14 pastas migradas
- [ ] Quartz build passa (se for possível executar localmente) ou config atualizada e validada
- [ ] Nenhum wikilink quebrado (Obsidian "Backlinks" não mostra "missing" novos)
- [ ] `00-Meta/workflow.md` existe e descreve as 5 zonas
- [ ] `00-Meta/templates/Template - Glosa.md` existe e é usável via Templater
- [ ] Commit único e claro

## 10. Fase B — implementação da skill

### 10.1 Arquivos a criar

```text
.claude/skills/glosa/
└── SKILL.md
```

### 10.2 Conteúdo do `SKILL.md`

Seguir formato padrão de skills do Claude Code:

```markdown
---
name: glosa
description: Cria fichamento (Glosa) de artigo web a partir de URL. Use quando o usuário pedir pra fichar/cataloguar/registrar um artigo, falar em "ficha de leitura", "fichamento", "glosa", invocar /glosa, ou compartilhar uma URL de artigo pedindo registro. Não suporta PDFs, vídeos ou podcasts (avisa e aborta).
---

# Skill: /glosa

[corpo com fluxo da seção 7.2, template da seção 6, edge cases da 7.3]
```

### 10.3 Critério de aceitação da Fase B

- [ ] Skill ativa via `/glosa <url>` e via NL (mensagem natural com URL pedindo fichamento)
- [ ] Fluxo completo executado num exemplo real (ex: o link Swizec da seção 6)
- [ ] Arquivo gerado tem todos os campos do frontmatter preenchidos (ou marcados explicitamente como ausentes)
- [ ] TL;DR é fiel ao artigo (validado por leitura humana)
- [ ] Citações são verbatim (não parafrasea)
- [ ] Link é removido de `01-Pergaminhos/entradas.md` quando presente
- [ ] Edge cases (YouTube, PDF, URL malformada, 404) tratados conforme tabela 7.3
- [ ] Commit: `feat(skill): /glosa cria fichamento de artigo a partir de URL`

## 11. Riscos e questões abertas

### 11.1 Riscos

- **Wikilinks com path absoluto** (`[[Pasta/Nome]]`): se existirem, quebram com a migração. Auditoria da Fase A mitiga.
- **Configs Quartz desconhecidas**: o repo do Quartz é separado; auditoria pode achar refs aos paths antigos. Plano: rodar build local ou pedir ao autor pra validar manualmente.
- **`.obsidian/templates folder` config**: se aponta pra `_templates`, vai quebrar. Auditável e fixável em 1 linha.
- **WebFetch e paywalls/cookies**: alguns sites (Substack, Medium pagado, NYT) podem retornar conteúdo parcial. Skill avisa quando o conteúdo extraído é muito curto (<500 chars).

### 11.2 Questões abertas

- **LICENSE**: o autor mencionou "licença" no root do repo, mas o arquivo não existe hoje. Decisão adiada pra durante a Fase A: criar (qual licença? CC-BY-SA-4.0 pra conteúdo é comum) ou deixar pra outro momento.
- **`00 - Inbox/entradas/inglês.md`**: o destino exato (arquivo solto vs merge com nota existente em `Inglês/`) decido durante a migração após inspeção do conteúdo.

## 12. Critérios de sucesso global

A spec é considerada bem-sucedida quando:

1. O autor pode ver no `tree` do repo as 5 zonas numeradas como pastas top-level
2. O autor invoca `/glosa <url>` num link real, e em < 30 segundos tem um arquivo de Glosa pronto pra revisar
3. Daqui a 1 mês, o autor consegue achar uma Glosa específica via busca por: tag, autor, trecho do TL;DR, ou trecho do "Meu comentário"
4. O fluxo "ler artigo → fichar → arquivar link de Pergaminhos" se torna automático e barato (< 10 min total por artigo, incluindo a leitura)
5. Quartz continua publicando o site sem regressões

## 13. Não-objetivos (recap)

- Suporte a PDF, YouTube, podcasts, papers (futuras extensões)
- Sugestão automática de wikilinks no "Ver também" (v2)
- Geração automática de "Meu comentário"
- Conteúdo da Senda Frontend
- Detecção de duplicatas semânticas
- Migração ou alteração de qualquer arquivo do repo apocrypha (privado)
- Refactor de notas existentes (só paths mudam)
