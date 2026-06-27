---
name: process-mock-interview
description: >
 Use quando o usuário quiser extrair um PDF de Mock Interview da mentoria GCA (Global Career Architecture, com Thaís Vieira) para o formato canônico do vault. Aciona com "/process-mock-interview", "processa o pdf da mock", "extrai a mock NN", "processa a mock interview". Contexto típico: arquivos em `03-Domínios/Inglês/GCA/Mock Interview/`. Consulta `03-Domínios/Inglês/GCA/Roadmap.md` (se existir) para inferir tema, persona, tipo (drill/full-loop), duração e fase do funil — além de gerar cross-links automáticos pra Session da mesma semana e pro Roadmap.
---

# process-mock-interview

## O que faz

Lê um PDF de Mock Interview na pasta `03-Domínios/Inglês/GCA/Mock Interview/` e gera **dois arquivos** markdown no mesmo diretório:

1. **`Mock Interview NN - <Nome>.md`** (Processed) — knowledge estruturado: perguntas Q1-Qn com regra GSC + mentor notes + audit checklist; diagnóstico transversal; plano de ação.
2. **`Mock Interview NN - <Nome> - Workbook.md`** (Workbook) — scaffold de respostas: regras invioláveis no topo, persona em destaque, e por Q: pergunta + framework + armadilhas (do feedback) + slots Draft vazios + slot Versão final consolidada.

## Quando usar

- Slash command: `/process-mock-interview`
- Linguagem natural: "processa o pdf da mock", "extrai a mock NN", "processa a mock interview", "gera a mock 04"

## Inputs esperados

- **PDF da Mock Interview** em `03-Domínios/Inglês/GCA/Mock Interview/`. Nome típico vindo da Thaís: `GCA — Mock Interview NN Josenaldo.pdf`.

## Steps

1. **Localizar o PDF:**
   - Procurar PDFs em `03-Domínios/Inglês/GCA/Mock Interview/` que ainda não tenham `.md` correspondente (PDF "novo").
   - Se exatamente 1 → usar direto.
   - Se múltiplos → listar e perguntar qual.
   - Se zero → erro: "Nenhum PDF novo encontrado em 03-Domínios/Inglês/GCA/Mock Interview/. Coloque o PDF na pasta antes de rodar."

2. **Inferir o número da Mock:**
   - Tentar extrair do nome do PDF (ex: "Mock Interview 01" → 01).
   - Se ambíguo → perguntar ao usuário.
   - Validar contra range 1-12 (são 12 mocks no programa).

3. **Consultar `03-Domínios/Inglês/GCA/Roadmap.md`** (se existir):
   - Localizar a `### Semana NN` correspondente.
   - Extrair: tema, fase do funil, persona, tipo (`drill` ou `full-loop`), duração, foco/regra de estresse, cycle.
   - **Se Roadmap não existe** → degradar graciosamente: avisar usuário ("⚠️ Roadmap.md não encontrado — rode `/process-roadmap` primeiro pra habilitar inferência de tema, persona e cross-links."), seguir perguntando esses valores explicitamente.

4. **Sugerir/perguntar nome curto:**
   - Se Roadmap disponível e tema identificado → propor: "Sugestão: 'Mock Interview NN - <Nome inferido do tema>'. Confirmar ou alterar?"
   - Se sem Roadmap → perguntar diretamente: "Qual o nome curto pra essa Mock?"

5. **Verificar conflitos de arquivo:**
   - **Processed existe** → confirmação simples ("⚠️ Mock Interview NN - X.md já existe. Sobrescrever? (sim/não)").
   - **Workbook existe E tem conteúdo manual** (mais linhas que template puro) → confirmação reforçada ("⚠️ esse Workbook tem N linhas suas, sobrescrever?").
   - Se usuário disser não em qualquer prompt → abortar.

6. **Ler PDF completo** (texto extraído).

7. **Carregar templates:**
   - `00-Meta/templates/GCA/Mock Interview - Processed.md`
   - `00-Meta/templates/GCA/Mock Interview - Workbook.md`
   - Se algum não existir → abortar com erro apontando o path.

8. **Extrair conteúdo do PDF:**
   - Lista de perguntas Q1-Qn (texto exato da pergunta).
   - Por Q: GSC rule (regra/framework aplicado), Mentor notes/Feedback (comentários da Thaís), Audit checklist (já marcado ou vazio).
   - Padrões recorrentes do diagnóstico (latência vocal, fillers, code-switching, over-explaining, persona de guerreiro, etc.).
   - Plano de ação / próximos passos.

9. **Resolver placeholders Templater do template Processed (16 cursors):**
   - **Frontmatter (1-7):** sessao number, week, cycle, interview_phase, mock_type, duration_min, persona — todos vindos do Roadmap.
   - **Callout Persona (8-11):** persona, tipo, duração, foco/regra de estresse — vindos do Roadmap.
   - **Sumário (12):** lista de Q1-Qn com wikilinks `[[#QN — <Title>|QN — <Title>]]`.
   - **Corpo principal (13):** todas as Qs estruturadas como em `Mock Interview/Mock Interview 01.md`:

     ```
     ## QN — <Title>

     > [!quote] Pergunta
     > "<texto exato da pergunta>"

     > [!tip] GSC Rule — <nome da regra>
     > <descrição da regra/framework>

     > [!warning] Mentor Notes / Feedback
     > <comentários da Thaís, bullets>

     ### Audit Checklist
     - [ ] / [x] <itens>

     ---
     ```

   - **Diagnóstico (14):** padrões recorrentes em seções numeradas (latência vocal, leitura de notas, code-switching, over-explaining, persona de guerreiro, princípio central) seguindo padrão de `Mock Interview 01.md`.
   - **Plano de Ação (15):** checklist de próximos passos extraídos do PDF.
   - **Veja também (16):** wikilink `[[Session NN]]` (Session da mesma semana).

10. **Resolver placeholders Templater do template Workbook (13 cursors):**
    - **Frontmatter (1-6):** sessao, week, cycle, mock_type, duration_min, persona.
    - **Cross-link (7):** título do Processed correspondente (ex: "Mock Interview 01 - Behavioral Stress Test"). Aparece em 2 lugares (info callout + Veja também).
    - **Callout Persona (8-11):** persona, tipo, duração, foco/regra de estresse.
    - **Sumário (12):** lista de Q1-Qn com wikilinks.
    - **Corpo principal (13):** todas as Qs com a estrutura de Workbook:

      ```
      ## QN — <Title> (<framework>, <time-box>)

      > [!quote] Pergunta
      > "<texto exato da pergunta>"

      > [!abstract] Framework — <PPF | STAR | livre>
      > <bullets explicando o framework adaptado a essa Q>

      > [!failure] Armadilhas (feedback Mock NN)
      > - ❌ <armadilha 1 extraída do feedback>
      > - ❌ <armadilha 2>
      > ...

      ### Draft — <Slot 1>  (ex: Anchor, Situation, etc.)
      > [!quote]-

      ### Draft — <Slot 2>
      > [!quote]-
      ...

      ### Versão final consolidada
      > [!answer]

      ---
      ```

      Os slots Draft variam pelo framework: PPF → Anchor/Proof/Pivot; STAR → Situation/Task/Action/Result; livre → 1-2 slots genéricos. Os callouts ficam vazios — você preenche.

11. **Verificar integridade antes de salvar** (Processed e Workbook):
    - **Sem Templater:** nenhuma sintaxe `<% ... %>` pode ter sobrado em nenhum dos dois arquivos. Se sobrou → abortar antes de salvar.
    - **Com frontmatter:** cada arquivo DEVE abrir com um bloco YAML (`---` na linha 1, fechado por outro `---`) contendo, no mínimo, `title`, `type` e `sessao`. Se o Workbook OU o Processed sair sem frontmatter → abortar antes de salvar. (Regressão histórica: o Workbook nasce sem frontmatter quando se parte de um template antigo — esta guarda impede que volte a acontecer.)

12. **Gerar cross-links automáticos:**
    - Processed: link pra `[[Session NN]]` (mesma semana) na seção "Veja também".
    - Workbook: link pra `[[Session NN]]` e pro Processed correspondente.
    - **Atualizar `03-Domínios/Inglês/GCA/Roadmap.md`** se existir: substituir `[[Mock Interview NN]]` por `[[Mock Interview NN - <Nome>|Mock Interview NN]]` na semana correspondente (preserva o display, atualiza o link).

13. **Salvar** ambos os arquivos em `03-Domínios/Inglês/GCA/Mock Interview/`.

14. **Reportar** ao usuário:
    - Paths dos 2 arquivos gerados.
    - Resumo: "N perguntas extraídas, persona '<X>', tipo <drill/full-loop>, duração <N>min".
    - Próximo passo sugerido: "Abra o Workbook no Obsidian. Quando começar a rascunhar uma resposta e quiser ajuda, invoque `/coaching` (modo socrático estrito — guia, nunca escreve por você)."

## Tratamento de erros

- **PDF ausente** → erro com instrução pra colocar PDF na pasta correta.
- **Templates ausentes** → erro com paths explícitos.
- **Roadmap ausente** → degradação graciosa (não aborta), avisa e segue perguntando os valores que viriam do Roadmap.
- **PDF criptografado / só-imagem** → reportar limitação, sugerir OCR manual.
- **Mock NN fora do range 1-12** → confirmar com usuário antes de seguir.
- **Sintaxe Templater remanescente** → abortar antes de gravar (bug de mapeamento).

## Não fazer

- **Não criar templates default** — se template não existir, abortar.
- **Não escrever respostas no Workbook** — todos os slots Draft e Versão final consolidada ficam vazios. Preenchimento é trabalho do usuário (com ou sem coaching).
- **Não inferir feedback que não está no PDF** — se a Thaís não comentou em alguma Q, deixar a seção `Mentor Notes` vazia ou com placeholder claro ("_Sem comentários específicos da mentora nesta pergunta._").
- **Não modificar arquivos existentes** sem confirmação (regra do conflito).
- **Não simplificar o frontmatter** — todos os campos do template são obrigatórios pra navegação Dataview/MOC futura.

## Convenções de output

- Arquivos finais: markdown puro, sem nenhuma sintaxe Templater.
- Frontmatter completo conforme template.
- Wikilinks padrão: `[[Session NN]]`, `[[Roadmap]]`, `[[Mock Interview NN - <Nome>]]`.
- Conteúdo dos rascunhos do Workbook em **EN**; instruções/contexto em **PT-BR**.
- Time-box explícito em cada Q do Workbook (ex: "(PPF, 90s)", "(STAR, 2min)").
