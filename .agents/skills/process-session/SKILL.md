---
name: process-session
description: >
  Use quando o usuário quiser extrair um PDF de Strategic Session da mentoria GCA (Global Career Architecture, com Thaís Vieira) para o formato canônico do vault. Aciona com "/process-session", "processa o pdf da session", "extrai a session NN", "processa a sessão". Contexto típico: arquivos em `03-Domínios/Inglês/GCA/Sessions/`. Consulta `03-Domínios/Inglês/GCA/Roadmap.md` (se existir) para inferir tema, fase do funil, ciclo e gerar cross-links automáticos pra Mock Interview da mesma semana e pro Roadmap.
---

# process-session

## O que faz

Lê um PDF de Strategic Session na pasta `03-Domínios/Inglês/GCA/Sessions/` e gera **dois arquivos** markdown no mesmo diretório:

1. **`Session NN - <Nome>.md`** (Processed) — knowledge estruturado: partes (I, II, III...) com glossários, frameworks (PPF, STAR, BLUF, etc.), exercícios, callouts Obsidian, War Room (próximos exercícios + banco de histórias).
2. **`Session NN - <Nome> - Workbook.md`** (Workbook) — scaffold de exercícios: regras invioláveis no topo, e por exercício/checklist/STAR slot: regra GSC associada + armadilhas (se houver feedback prévio) + slot Draft vazio.

## Quando usar

- Slash command: `/process-session`
- Linguagem natural: "processa o pdf da session", "extrai a session NN", "processa a sessão", "gera a session 03"

## Inputs esperados

- **PDF da Session** em `03-Domínios/Inglês/GCA/Sessions/`. Nome típico vindo da Thaís: `GCA — <Strategic ou Session> NN <Tema> Josenaldo.pdf` (formato varia).

## Steps

1. **Localizar o PDF:**
   - Procurar PDFs em `03-Domínios/Inglês/GCA/Sessions/` que ainda não tenham `.md` correspondente (PDF "novo").
   - **Importante:** ignorar o PDF do Cronograma (ele NÃO é uma Session — pertence à raiz `03-Domínios/Inglês/GCA/`). Se aparecer aqui, alertar o usuário e sugerir movê-lo de volta pra raiz.
   - Se exatamente 1 candidato → usar direto.
   - Se múltiplos → listar e perguntar.
   - Se zero → erro: "Nenhum PDF novo encontrado em 03-Domínios/Inglês/GCA/Sessions/. Coloque o PDF na pasta antes de rodar."

2. **Inferir o número da Session:**
   - Tentar extrair do nome do PDF (ex: "Session 02" → 02).
   - Se ambíguo → perguntar ao usuário.
   - Validar contra range 1-12 (são 12 sessions no programa).

3. **Consultar `03-Domínios/Inglês/GCA/Roadmap.md`** (se existir):
   - Localizar a `### Semana NN` correspondente.
   - Extrair: tema, fase do funil, cycle, objetivo macro (vindo do "Tema:" do callout Strategic Session no Roadmap).
   - **Se Roadmap não existe** → degradar graciosamente: avisar usuário ("⚠️ Roadmap.md não encontrado — rode `/process-roadmap` primeiro pra habilitar inferência de tema e cross-links."), seguir perguntando esses valores.

4. **Sugerir/perguntar nome curto:**
   - Se Roadmap disponível e tema identificado → propor: "Sugestão: 'Session NN - <Nome inferido>'. Ex: 'Foundation', 'Pitch Manager of One', 'BLUFF Framework'. Confirmar ou alterar?"
   - Se sem Roadmap → perguntar: "Qual o nome curto pra essa Session?"

5. **Verificar conflitos de arquivo:**
   - Processed existe → confirmação simples.
   - Workbook existe E tem conteúdo manual (mais linhas que template puro) → confirmação reforçada.
   - Se usuário disser não → abortar.

6. **Ler PDF completo** (texto extraído).

7. **Carregar templates:**
   - `00-Meta/templates/GCA/Session - Processed.md`
   - `00-Meta/templates/GCA/Session - Workbook.md`
   - Se algum não existir → abortar com erro.

8. **Extrair conteúdo do PDF:**
   - Estrutura em "Parts" (I, II, III...) ou "Sections" — cada uma com seu título e conteúdo conceitual.
   - Identificar **frameworks** (PPF, STAR, BLUF, etc.), **glossários** (ex: Power Verbs), **exercícios práticos**, **modelos de exemplo** (ex: pitch da Thaís).
   - Identificar **regras GSC** ditas explicitamente no PDF (regra de ouro, time-box, "evite", "faça").
   - Extrair War Room: próximos exercícios / homework declarado pelo PDF.
   - Extrair (se houver) banco de histórias / exemplos canônicos.

9. **Resolver placeholders Templater do template Processed (15 cursors):**
   - **Frontmatter (1-5):** sessao number, week, cycle, interview_phase, tag específica do tema (ex: `star`, `pitch`, `bluf`, `system-design`).
   - **Info callout (6-9):** tema, fase do funil, ciclo, objetivo macro — vindos do Roadmap.
   - **Sumário (10):** lista de Parts com wikilinks `[[#Part N — <Title>|Part N — <Title>]]`.
   - **Corpo principal (11):** todas as Parts estruturadas como em `Sessions/Session 01 - Foundation.md`:
     - `## Part N — <Title>`
     - Callouts Obsidian apropriados ao conteúdo:
       - `> [!abstract]` para propósito/contexto da parte
       - `> [!warning]` para regras de ouro / cuidados
       - `> [!tip]` para dicas/truques
       - `> [!example]` para modelos da Thaís
       - `> [!quote]` para frases-chave / citações
       - `> [!todo]` para ações que o usuário deve tomar
       - `> [!important]` para princípios centrais
       - `> [!danger]` para anti-patterns severos
     - Tabelas para glossários (ex: Power Verbs com Categoria/Significado/Tradução/Exemplo).
   - **War Room — Próximos Exercícios (12-13):** descrição da tarefa principal + checklist detalhado de subtarefas.
   - **War Room — Histórias (14):** banco de histórias STAR ou exemplos canônicos. Pode começar vazio se a Session não trouxer; o usuário acumula ao longo do tempo.
   - **Veja também (15):** wikilinks adicionais (ex: notas conceituais relacionadas).

10. **Resolver placeholders Templater do template Workbook (6 cursors):**
    - **Frontmatter (1-3):** sessao, week, cycle.
    - **Cross-link (4):** título do Processed correspondente (aparece em 2 lugares).
    - **Sumário (5):** lista de exercícios/seções com wikilinks.
    - **Corpo principal (6):** todos os exercícios estruturados seguindo **padrão B uniforme**:
      ```
      ## <Nome do Exercício>

      > [!tip] Regra GSC associada
      > <regra extraída da Part correspondente do Processed>

      > [!failure] Armadilhas (se aplicável)
      > - ❌ <armadilha 1, se houver feedback prévio>
      > ...

      ### <Subseção do exercício, se aplicável>
      > [!quote]-

      ---
      ```
      Os slots `> [!quote]-` ficam **vazios** — usuário preenche.
      Para checklists de positioning (ex: "Marcar atributos que ressoam"), usar `- [ ]` por item.
      Para histórias STAR draftadas, usar slots `> [!quote]- Situation`, `> [!quote]- Task`, etc.

      **Adições permitidas (calibrações que NÃO violam "não inventar"):**
      - **Tabelas de tracking** quando o tema da semana exige medição (ex: WPM Log para Session 02 sobre "calibração de cadência"; Time-box log para sessões com time-box rígido). Linhas iniciam vazias — usuário preenche. Decisão: se o PDF menciona métrica que precisa ser auditada ao longo da semana → adicionar tabela.
      - **Exercício de refactor de anti-pattern**: se o Processed contém um exemplo concreto de "resposta ruim" (ex: trecho do Mock anterior que demonstra over-explaining, ingredient list, narrativa de guerreiro), **copiar** esse trecho pro Workbook como exercício "Refactor — <descrição>": apresentar o anti-padrão original num callout `> [!example]-` e abaixo um slot `> [!quote]-` vazio pra versão refatorada. Justificativa pedagógica: anti-pattern só vira aprendizado quando o aluno re-escreve com as próprias mãos.

11. **Verificar integridade antes de gravar** (Processed e Workbook):
    - **Sem Templater:** nenhuma sintaxe `<% ... %>` pode ter sobrado em nenhum dos dois arquivos. Se sobrou → abortar antes de gravar.
    - **Com frontmatter:** cada arquivo DEVE abrir com um bloco YAML (`---` na linha 1, fechado por outro `---`) contendo, no mínimo, `title`, `type` e `sessao`. Se o Workbook OU o Processed sair sem frontmatter → abortar antes de gravar. (Regressão histórica: o Workbook nasce sem frontmatter quando se parte de um template antigo — esta guarda impede que volte a acontecer.)

12. **Gerar cross-links automáticos:**
    - Processed: link pra `[[Mock Interview NN]]` (mesma semana) e `[[Roadmap]]` em "Veja também".
    - Workbook: link pra Processed correspondente, `[[Mock Interview NN]]`, `[[Roadmap]]`.
    - **Atualizar `03-Domínios/Inglês/GCA/Roadmap.md`** se existir: substituir `[[Session NN]]` por `[[Session NN - <Nome>|Session NN]]` na semana correspondente.

13. **Salvar** ambos em `03-Domínios/Inglês/GCA/Sessions/`.

14. **Reportar** ao usuário:
    - Paths dos 2 arquivos gerados.
    - Resumo: "N partes extraídas (<lista breve dos títulos>), M exercícios mapeados pro Workbook".
    - Próximo passo sugerido: "Abra o Workbook no Obsidian. Quando começar um exercício e travar, invoque `/coaching` (modo socrático estrito — guia, nunca escreve por você)."

## Tratamento de erros

- **PDF ausente** → erro com instrução pra colocar PDF na pasta correta.
- **PDF do Cronograma na pasta Sessions/** → alerta, sugerir mover pra raiz `03-Domínios/Inglês/GCA/`.
- **Templates ausentes** → erro com paths explícitos.
- **Roadmap ausente** → degradação graciosa.
- **PDF criptografado / só-imagem** → reportar limitação, sugerir OCR manual.
- **Session NN fora do range 1-12** → confirmar com usuário antes de seguir.
- **Sintaxe Templater remanescente** → abortar antes de gravar (bug de mapeamento).

## Não fazer

- **Não criar templates default** — se template não existir, abortar.
- **Não escrever respostas no Workbook** — todos os slots Draft ficam vazios. Preenchimento é trabalho do usuário.
- **Não inventar conteúdo** — se a Session não traz uma seção, deixar fora ou marcar com placeholder claro.
- **Não modificar arquivos existentes** sem confirmação.
- **Não tratar o Cronograma como Session** — Cronograma é meta-documento, vive na raiz e é processado pelo `process-roadmap`.

## Convenções de output

- Arquivos finais: markdown puro, sem nenhuma sintaxe Templater.
- Frontmatter completo conforme template.
- Wikilinks padrão: `[[Roadmap]]`, `[[Mock Interview NN]]`, `[[Session NN - <Nome>]]`.
- Conteúdo dos exercícios em **EN** quando for material de entrevista; instruções/contexto em **PT-BR**.
- Power Verbs e regras GSC sempre destacadas em callouts apropriados (não em texto corrido).
