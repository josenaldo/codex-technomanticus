---
name: process-roadmap
description: Use quando o usuário quiser extrair o PDF do Cronograma da mentoria GCA (Global Career Architecture, com Thaís Vieira) para o MOC mestre `03-Domínios/Inglês/GCA/Roadmap.md`. Aciona com "/process-roadmap", "processa o cronograma", "extrai o roadmap", "gera o MOC do GCA". O PDF do Cronograma vive em `03-Domínios/Inglês/GCA/` (raiz, não dentro de subpasta) e tem nome contendo "Cronograma" ou "Roadmap" (case-insensitive). Esta skill roda raramente — só uma vez no início, ou quando a Thaís refinar o cronograma. Outras skills do GCA (`process-session`, `process-mock-interview`) consultam o `Roadmap.md` gerado para inferir tema/persona/fase do funil de cada semana.
---

# process-roadmap

## O que faz

Lê o PDF do Cronograma da mentoria GCA e gera **um único arquivo** `03-Domínios/Inglês/GCA/Roadmap.md` (MOC mestre do programa). O arquivo gerado:

- Lista o **dossiê do aluno** (perfil, cenário, gargalo atual, estratégia).
- Estrutura as **12 semanas em 3 ciclos**, com tema da Session, descrição do Mock (persona + tipo + duração), checkboxes de status e wikilinks pra cada Session/Mock.
- Serve como **MOC navegacional** do vault GCA.
- Serve como **fonte de inferência** para as outras skills (`process-session`, `process-mock-interview`).

Não há Workbook associado — Roadmap é índice, não exercício.

## Quando usar

- Slash command: `/process-roadmap`
- Linguagem natural: "processa o cronograma", "extrai o roadmap", "gera o MOC do GCA", "cria o Roadmap"

## Inputs esperados

- **PDF do Cronograma** em `03-Domínios/Inglês/GCA/` (raiz, não dentro de subpasta).
- Nome do PDF deve conter "Cronograma" ou "Roadmap" (case-insensitive). Exemplo típico: `GCA — Cronograma Josenaldo (Interativo).pdf`.

## Steps

1. **Localizar o PDF do Cronograma:**
   - Procurar PDFs em `03-Domínios/Inglês/GCA/` (raiz) cujo nome contenha "Cronograma" ou "Roadmap" (case-insensitive).
   - Se exatamente 1 candidato → usar direto.
   - Se múltiplos → listar e perguntar ao usuário qual.
   - Se zero → erro: "Nenhum PDF de Cronograma encontrado em 03-Domínios/Inglês/GCA/. Coloque o PDF na raiz da pasta GCA antes de rodar."

2. **Verificar conflito com `03-Domínios/Inglês/GCA/Roadmap.md`:**
   - Se já existe → confirmação reforçada: "⚠️ Roadmap.md é o índice mestre do vault e tem N wikilinks pra Sessions/Mocks. Sobrescrever pode quebrar referências. Continuar? (sim/não)"
   - Se usuário disser não → abortar.

3. **Ler o PDF completo** (texto extraído).

4. **Carregar o template** `00-Meta/templates/GCA/Roadmap.md`:
   - Se não existir → erro: "Template não encontrado em `00-Meta/templates/GCA/Roadmap.md`. Crie o template antes de rodar a skill."

5. **Extrair do PDF:**
   - **Dossiê do aluno** — perfil, cenário, gargalo atual, estratégia. Geralmente aparece no topo do Cronograma sob título "Dossiê do Aluno" ou similar.
   - **Estrutura de ciclos e semanas** — para cada uma das 12 semanas:
     - Tema da Strategic Session (ex: "Método STAR — A Fundação").
     - Fase do funil de contratação (ex: "Initial Screening / Triagem Comportamental").
     - Descrição da Session: o que será treinado, qual o homework esperado.
     - Tipo do Mock: `drill` (30-40min, foco específico) ou `full-loop` (60min, integrador). Semanas 4, 8 e 12 costumam ser full-loops.
     - Persona do Mock (ex: "Recrutador Pragmático", "Headhunter Global de Startups").
     - Duração do Mock (`30-40 min` ou `60 min`).
     - Foco do Mock.

6. **Resolver placeholders Templater do template:**
   - `<% tp.file.title %>` → "Roadmap" (ou nome que faça sentido — o título do arquivo final).
   - `<% tp.date.now("YYYY-MM-DD") %>` → data atual.
   - `<% await tp.system.prompt('Nome do PDF do Cronograma (com extensão)') %>` → nome do PDF detectado no Step 1.
   - `<% tp.file.cursor(1) %>` → conteúdo do **Dossiê do aluno** extraído. Estruturar em parágrafo coeso ou bullets curtos: perfil, cenário, gargalo atual, estratégia.
   - `<% tp.file.cursor(N) %>` para semanas (cursors 2-37, três por semana):
     - Cursor `tema` (no heading): texto curto do tema da semana (ex: "Método STAR (A Fundação)").
     - Cursor `Strategic Session` (callout `> [!example]`): bloco multilinha com:
       - `**Fase do funil:** <fase>`
       - `**Tema:** <tema completo>`
       - `**Homework:** <descrição do homework, se houver no PDF>`
     - Cursor `Mock Interview` (callout `> [!quote]`): bloco multilinha com:
       - `**Tipo:** Drill` ou `**Tipo:** Full Loop`
       - `**Duração:** 30-40 min` ou `**Duração:** 60 min`
       - `**Persona:** <persona>`
       - `**Foco:** <foco>`

7. **Garantir que nenhuma sintaxe Templater (`<% ... %>`) sobrou** no arquivo final. Se sobrou, é erro de mapeamento — abortar com mensagem clara.

8. **Salvar** o resultado em `03-Domínios/Inglês/GCA/Roadmap.md`.

9. **Reportar** ao usuário:
   - Path gerado: `03-Domínios/Inglês/GCA/Roadmap.md`.
   - Resumo: "12 semanas processadas (3 ciclos), persona/tipo/duração de cada Mock identificados".
   - Próximo passo sugerido: "Abra o Roadmap no Obsidian, valide visualmente. Quando quiser processar uma Session ou Mock, rode `/process-session` ou `/process-mock-interview`."

## Tratamento de erros

- **PDF do Cronograma ausente** em `03-Domínios/Inglês/GCA/` → erro com instrução clara pra colocar o PDF na raiz.
- **Template ausente** em `00-Meta/templates/GCA/Roadmap.md` → erro com path explícito.
- **PDF criptografado / só-imagem** (sem texto extraível) → reportar limitação e sugerir OCR manual.
- **Cronograma não tem 12 semanas** ou estrutura não-padrão → reportar a divergência mas seguir, preenchendo o que conseguir e marcando os faltantes com `<% tp.file.cursor(N) %>` originais (deixando claro pro usuário o que ficou pendente).
- **Sintaxe Templater remanescente** após substituição → abortar antes de gravar o arquivo (significa bug no mapeamento de cursors).

## Não fazer

- **Não criar** o template default — se o template não existir, abortar e instruir o usuário a criar.
- **Não criar Workbook** associado ao Roadmap — Roadmap é índice navegacional, não exercício.
- **Não modificar arquivos existentes** além de `03-Domínios/Inglês/GCA/Roadmap.md`.
- **Não inferir dados** que não estão no PDF — se o Cronograma não disser a persona da semana X, deixar o cursor original com placeholder claro.
- **Não tentar gerar o conteúdo das Sessions/Mocks** — esta skill só gera o MOC. Outras skills lidam com Sessions/Mocks.

## Convenções de output

- Arquivo final: markdown puro, sem nenhuma sintaxe Templater.
- Frontmatter completo conforme template.
- Wikilinks usam padrão `[[Session NN]]` e `[[Mock Interview NN]]` (sem nome curto, pois ainda não foram processadas — Obsidian resolve depois).
- Status checkboxes começam todos desmarcados.
