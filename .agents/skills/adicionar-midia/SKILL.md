---
name: adicionar-midia
description: Micro-skill: pesquisa vídeos (YouTube) e podcasts (com transcrição disponível) relevantes para uma nota, baixa as legendas via uvx yt-dlp, analisa relevância e embute os melhores como callouts [!tip] na nota. Use quando o usuário pedir "adicionar vídeo", "adicionar mídia", "embutir vídeo", "buscar vídeo sobre X", "enriquecer com mídia", "podcast sobre X". Também invocada pela lente Mídia do /enriquecer-nota.
---

# Skill: adicionar-midia

Pesquisa, analisa e embute vídeos do YouTube e podcasts (com transcrição) em notas do vault.
Cada mídia aprovada vira um callout `> [!tip]` com link + contexto de relevância.

**Regra de ouro:** nunca embutir sem ter lido a transcrição. Sem legenda = descarta.

## Invocação

```
/adicionar-midia [path] [instrução]
```

- **Sem `path`:** pergunta qual nota enriquecer.
- **Com `path`:** usa o arquivo indicado (relativo à raiz do vault).
- **Instrução complementar:** tema específico, canais preferidos, idioma, tipo (vídeo|podcast).

## Dependência: yt-dlp via uvx

Todos os downloads usam `uvx yt-dlp` (sem instalação global). Se `uvx` falhar, reporta o comando
exato e aborta sem editar a nota. Avisos de "No supported JavaScript runtime" e "impersonation"
são não-fatais — o download das legendas funciona mesmo assim.

---

## Fase 1 — Perfil da nota

1. Lê a nota-alvo (frontmatter + corpo).
2. Extrai: tema principal, conceitos-chave, `fase:`, domínio.
3. Lista as mídias já embutidas na nota (callouts `[!tip]` com links de vídeo/podcast) para evitar duplicar.

---

## Fase 2 — Pesquisa de candidatos

### Vídeos (YouTube)

Critérios de seleção (aplicar todos):

- **Idioma:** PT-BR prioritário; EN se referência canônica no domínio.
- **Tipo:** tutorial técnico, talk de conferência, explicação conceitual. **Nunca:** vlogs, anúncios, "top N coisas sem profundidade".
- **Autores prioritários por domínio:**
  - IA/LLMs → Andrej Karpathy, François Chollet, DeepMind, Anthropic, OpenAI
  - Web/Frontend → Fireship, Theo, Matt Pocock (TypeScript), Kent C. Dodds
  - Java/Backend → Venkat Subramaniam, Josh Long, InfoQ, GOTO conferences
  - Arquitetura → Martin Fowler, Sam Newman, Software Engineering Radio
  - Sistemas → Brandon Gregg, Brendan Burns
- **Duração:** 5-60 min (curto demais = superficial; longo demais = difícil de ancorar).

Buscas WebSearch (2-3 queries dirigidas):

```
site:youtube.com "<tema principal>" <autor-prioritário>
"<conceito-chave>" tutorial conference talk youtube <ano>
"<conceito-chave>" explained youtube
```

Seleciona 3-5 candidatos com URL, título, canal e duração estimada.

### Podcasts (EN com transcrição)

Critérios adicionais:

- **Obrigatório:** transcrição disponível no site do podcast ou no YouTube.
- **Idioma:** EN apenas (padrão de mercado para podcasts técnicos com transcrição).
- **Fontes preferenciais:** Lex Fridman Podcast, Practical AI, Software Engineering Daily, The TWIML AI Podcast, Acquired, CoRecursive.
- **Como verificar transcrição:** buscar `site:<podcast-url> transcript` ou verificar se há vídeo no YouTube com legendas.

Apresenta lista de candidatos com tipo (vídeo/podcast) e fonte de transcrição antes de prosseguir.

---

## Fase 3 — Download de legendas

Para cada candidato aprovado pelo usuário:

```bash
# 1. Listar legendas disponíveis:
uvx yt-dlp --list-subs --skip-download "https://youtube.com/watch?v=<id>"

# 2a. Legenda manual PT-BR (preferido):
uvx yt-dlp --write-sub --sub-lang pt-BR --sub-format vtt \
  --skip-download -o "/tmp/addmidia-%(id)s.%(ext)s" "<url>"

# 2b. Fallback — legenda automática PT-BR:
uvx yt-dlp --write-auto-sub --sub-lang pt-BR --sub-format vtt \
  --skip-download -o "/tmp/addmidia-%(id)s.%(ext)s" "<url>"

# 2c. Fallback final — EN (manual > automática):
uvx yt-dlp --write-sub --sub-lang en --sub-format vtt \
  --skip-download -o "/tmp/addmidia-%(id)s.%(ext)s" "<url>"
```

Limpar VTT para leitura (remove marcações de tempo e tags):

```bash
grep -vE '^WEBVTT|^Kind:|^Language:|-->|^[[:space:]]*$|align:|position:' \
  "/tmp/addmidia-<id>.<lang>.vtt" | sed -E 's/<[^>]*>//g' | awk '!seen[$0]++'
```

Para encontrar timestamps de trechos relevantes, consultar as linhas `HH:MM:SS.mmm -->` do `.vtt`
original. Formatar como `[mm:ss]` ou `[h:mm:ss]` se ≥1h.

Se nenhuma legenda disponível para o candidato → descarta e avisa o usuário.

---

## Fase 4 — Análise de relevância

Para cada transcrição lida, avalia em 3 dimensões (0-10 cada):

| Dimensão | Critério |
|----------|----------|
| **Alinhamento** | A transcrição trata do conceito central da nota (não só tangencial)? |
| **Profundidade** | Acrescenta ângulo, exemplo ou mecanismo que a nota ainda não cobre? |
| **Qualidade pedagógica** | Clareza de explicação, exemplos concretos, sem jargão vazio? |

**Trecho âncora:** identifica o trecho mais relevante (timestamp + citação de 1-2 frases).

**Filtro:** descarta candidatos com Alinhamento <7. Apresenta shortlist com pontuação e justificativa:

```
CANDIDATOS APROVADOS:
📹 [Título do Vídeo] — Canal (~Xmin) — EN
   Alinhamento: 9 | Profundidade: 8 | Pedagógico: 8
   Trecho âncora [X:XX]: "<citação>"
   → Relevância: <por que acrescenta à nota em 1 linha>

🎙️ [Título do Episódio] — Podcast (~Xmin) — EN (transcrição no site)
   Alinhamento: 8 | Profundidade: 7 | Pedagógico: 9
   → Relevância: <por que acrescenta em 1 linha>

DESCARTADOS:
✗ [Título] — Alinhamento: 5 — superficial demais para o tema
```

---

## Fase 5 — Plano de inserção

Sugere onde inserir cada mídia na nota (seção de maior encaixe semântico):

```
PLANO — <título da nota>

📹 [<Título do Vídeo>](<url>) — <Canal> (~Xmin) — <idioma>
   Inserir após §<Nome da Seção>
   Relevância: <1 linha>
   Trecho âncora [X:XX]: "<citação>"

🎙️ [<Título do Episódio>](<url>) — <Podcast> (~Xmin) — EN
   Inserir após §<Nome da Seção>
   Relevância: <1 linha>

[c] confirmar tudo   [N] descartar item N   [x] cancelar
```

---

## Fase 6 — Inserção

Para cada mídia aprovada, insere o callout no local indicado:

### Vídeo

```markdown
> [!tip] Assista: <Título do Vídeo>
> **Canal:** <Nome> | **Duração:** ~Xmin | **Idioma:** PT-BR / EN
>
> <1-2 frases sobre o que o vídeo acrescenta que a nota não cobre — no registro Feynman.>
> Trecho de destaque [X:XX]: *"<citação do trecho âncora>"*
>
> 🎬 [Assistir no YouTube](<url>)
```

### Podcast

```markdown
> [!tip] Ouça: <Título do Episódio>
> **Podcast:** <Nome> | **Duração:** ~Xmin | **Idioma:** EN (transcrição disponível)
>
> <1-2 frases sobre o que o episódio acrescenta que a nota não cobre.>
>
> 🎙️ [Ouvir](<url>)
```

Após inserção: atualiza `updated:` no frontmatter. Descarta os `.vtt` de `/tmp`:

```bash
rm -f /tmp/addmidia-*.vtt
```

---

## Convenções rígidas

- **Legendas obrigatórias** — nunca embutir vídeo sem ter lido a transcrição. Sem legenda = descarta.
- **Podcast só com transcrição** — verificar antes do download; sem transcrição = descarta.
- **Máximo 2 mídias por nota** — mais do que isso fragmenta o foco. Exceção: notas capstone (>600 linhas) podem ter até 3.
- **Callout `[!tip]`** — padrão canônico para mídia. Nunca embutir só o link cru.
- **Não duplicar** — checar mídias já presentes antes de qualquer inserção.
- **Fontes autoritativas prioritárias** — Karpathy/3Blue1Brown/InfoQ/GOTO valem mais que tutoriais genéricos.
- **Confirmar antes de editar** — mostra plano; não grava sem aprovação.

## Edge cases

| Caso | Comportamento |
|------|---------------|
| Nenhuma legenda disponível | Descarta candidato; avisa |
| Todos os candidatos com Alinhamento <7 | "Nenhum vídeo passou o critério de relevância"; encerra sem editar |
| Nota já tem ≥2 mídias | Avisa; pergunta se quer substituir ou adicionar mesmo assim |
| `uvx`/`yt-dlp` falha | Reporta o comando exato; não escreve; aborta |
| Podcast sem transcrição disponível | Descarta; nunca embutir sem transcrição |
| URL inválida ou não-YouTube | Avisa; pede nova URL ou aborta |
