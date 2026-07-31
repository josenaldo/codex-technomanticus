---
name: process-community
description: >
  Use quando o usuário quiser extrair um PDF de Community Session da mentoria GCA (Global Career Architecture, com Thaís Vieira) para o formato canônico do vault. Aciona com "/process-community", "processa o pdf da community", "extrai a community NN", "processa a sessão em grupo". Contexto típico: arquivos em `03-Domínios/Inglês/GCA/Community/`. Community sessions são em grupo (quinta à noite) com role-plays em pares (Breakout Rooms) — formato bem diferente de Sessions/Mocks. Esta skill NÃO consulta o Roadmap (Community é stream paralelo, não segue grid de 12 semanas).
---

# process-community

## O que faz

Lê um PDF de Community Session na pasta `03-Domínios/Inglês/GCA/Community/` e gera **dois arquivos** markdown no mesmo diretório:

1. **`Community NN - <Nome>.md`** (Processed) — knowledge estruturado: tema central, N rounds (cada um com conceito + culture clash + room assignments), mentor notes globais, seções extras se aplicável (ex: voting/schedule).
2. **`Community NN - <Nome> - Workbook.md`** (Workbook) — scaffold reflexivo: regras de boa reflexão no topo, e por round em que o usuário participou: slots para frases usadas + o que funcionou + o que travou + vocab novo + ajustes. Reflexão geral ao final com vocabulário consolidado e próximas práticas.

## Quando usar

- Slash command: `/process-community`
- Linguagem natural: "processa o pdf da community", "extrai a community NN", "processa a sessão em grupo", "gera a community 02"

## Inputs esperados

- **PDF da Community Session** em `03-Domínios/Inglês/GCA/Community/`. Nomes típicos: `GCA Extreme Ownership Sparring Protocol.pdf`, `GSCommunity Selling Seniority Globally.pdf`.

## Steps

1. **Localizar o PDF:**
   - Procurar PDFs em `03-Domínios/Inglês/GCA/Community/` que ainda não tenham `.md` correspondente (PDF "novo").
   - Se exatamente 1 candidato → usar direto.
   - Se múltiplos → listar e perguntar.
   - Se zero → erro: "Nenhum PDF novo encontrado em 03-Domínios/Inglês/GCA/Community/."

2. **Inferir o número da Community Session:**
   - Tentar extrair do nome do PDF se houver numeração (ex: "Community 03"). Senão, perguntar ao usuário ("Qual o número desta Community Session?").
   - Validar contra histórico: listar arquivos `Community NN - *.md` existentes pra evitar duplicar número.

3. **Inferir/perguntar:**
   - **Tema central** — extrair do título do PDF (ex: "Extreme Ownership Framework", "Selling Seniority Globally"). Confirmar com usuário.
   - **Nome curto** — propor baseado no tema (ex: "Extreme Ownership", "Selling Seniority"). Confirmar.
   - **Data da sessão** — procurar no PDF (ex: "Date: 04/23/2026"). Se não encontrar → perguntar.

4. **Verificar conflitos de arquivo:**
   - Processed existe → confirmação simples.
   - Workbook existe E tem conteúdo manual → confirmação reforçada.

5. **Ler PDF completo** (texto + imagens, via Read tool).

6. **Carregar templates:**
   - `00-Meta/templates/GCA/Community - Processed.md`
   - `00-Meta/templates/GCA/Community - Workbook.md`
   - Se algum não existir → abortar.

7. **Extrair conteúdo do PDF:**
   - **Tema central / Executive mindset** — frase ou parágrafo de abertura que dá o propósito da sessão.
   - **N rounds / protocol steps** — identificar quantos (4 no Sparring, 6 no Selling Seniority, mas pode variar).
   - **Por round:**
     - Título (ex: "Round 01 — The Lexical Anchor: BLUF & Verbs" ou "PROTOCOL STEP 01 — Disambiguation").
     - Conceito central / Core Logic / Executive Mindset.
     - Mentor's Trap Question (se houver — formato Selling Seniority).
     - **Culture clash** (formato adaptável):
       - Estilo Selling Seniority: Brazilian Bug (3 dimensões com exemplo) vs Global Executive (3 dimensões com exemplo).
       - Estilo Sparring: DO's (Leader) vs DON'Ts (Forbidden).
       - Skill detecta o formato e preserva como tabela de 2 colunas com headers apropriados.
     - **Room assignments** — listar TODOS os 4 (ou N) rooms com:
       - Participantes (Stakeholder + Diplomat ou similar).
       - Stakeholder Goal / Diplomat Goal (objetivos da role).
       - Directive (frase-modelo, se houver).
   - **Mentor notes globais** — observações coletivas (não específicas por room).
   - **Seções extras** — voting (Next Theme / Schedule) ou outras se presentes no PDF.

8. **Identificar os rounds em que o usuário participou:**
   - Procurar o nome do aluno (configurar: substituir pelo nome real do usuário do vault) nos room assignments.
   - Por round encontrado, registrar: número do round, role (Stakeholder ou Diplomat), par, e directive específica.
   - Essa informação alimenta:
     - Cursor 7 do Processed (callout "Seus rooms").
     - Cursor 6 do Workbook (slots reflexivos só pros rounds em que participou).

9. **Resolver placeholders Templater do template Processed (12 cursors):**
   - **Frontmatter (1-5):** community_session number, theme, session_date (formato YYYY-MM-DD), rounds_count, tag específica do tema (ex: `extreme-ownership`, `executive-pitch`, slug curto).
   - **Info callout — executive mindset (6):** propósito macro (1-2 frases extraídas do PDF).
   - **Callout "Seus rooms" (7):** bullet list dos rounds em que o usuário participou:
     ```
     > - **Round 01** — Você foi **Stakeholder** com Renata Persicheto. Directive: "<directive do round>"
     > - **Round 04** — Você foi **Diplomat** com Sírio Maquea. Directive: "<directive>"
     ```
     Se o usuário não participou de nenhum round → "Você não foi designado a nenhum room nesta sessão."
   - **Sumário (8):** wikilinks aos rounds.
   - **Corpo principal (9):** todos os rounds estruturados:
     ```
     ## Round NN — <Title>

     > [!abstract] Executive Mindset
     > "<frase do mindset>"

     > [!quote] Mentor's Trap Question
     > "<pergunta-armadilha>"      (omitir esse callout se PDF não traz)

     ### Culture Clash

     | <Header coluna 1: Brazilian Bug ou DON'Ts> | <Header coluna 2: Global Executive ou DO's> |
     |---|---|
     | <item 1 col 1> | <item 1 col 2> |
     | ... | ... |

     ### Breakout Rooms

     | Room | Participantes | Goal Stakeholder | Goal Diplomat | Directive |
     |---|---|---|---|---|
     | 1 | A & B | ... | ... | "..." |
     | 2 | ... | ... | ... | "..." |

     <Se usuário participou de algum room deste round → adicionar callout em destaque>
     > [!important] **Seu room**: você foi **<role>** com **<par>**. Directive: "<directive>"

     ---
     ```
   - **Mentor notes globais (10):** observações coletivas extraídas do PDF. Se PDF tiver placeholder genérico ("!/ Document specific feedback..."), reproduzir o placeholder e marcar `_(observações específicas serão capturadas durante/após a sessão pelo usuário)_`.
   - **Seção extra opcional (11):** se PDF traz Voting/Schedule (caso Selling Seniority), preencher seção completa com options e checklists. Se não traz → **deixar cursor vazio e remover a linha `---` que o cerca** (skill faz cleanup).
   - **Veja também (12):** wikilinks adicionais relevantes (ex: notas conceituais, notas do galho Entrevistas se aplicável).

10. **Resolver placeholders Templater do template Workbook (6 cursors):**
    - **Frontmatter (1-3):** community_session, theme, session_date.
    - **Cross-link (4):** título do Processed correspondente (aparece em 2 lugares).
    - **Sumário (5):** wikilinks aos rounds.
    - **Corpo principal (6):** todos os rounds — formato adaptado por participação:

      **Para round em que o usuário participou:**
      ```
      ## Round NN — <Title>

      > [!info] Recap
      > Conceito: <1 linha do mindset>. Sua role: **<Stakeholder/Diplomat>** com **<par>**. Directive: "<frase modelo>".

      ### Frases que você usou
      > [!quote]-

      ### O que funcionou
      > [!success]-

      ### O que travou / erros
      > [!failure]-

      ### Vocabulário novo absorvido
      > [!example]-

      ### Ajustes pra próxima
      > [!todo]-

      ---
      ```

      **Para round em que NÃO participou:**
      ```
      ## Round NN — <Title>

      > [!info] Recap (você não foi designado neste round)
      > Conceito: <1 linha do mindset>. Ver assignments completos no [[<título do Processed>]].

      ---
      ```

11. **Verificar integridade antes de gravar** (Processed e Workbook):
    - **Sem Templater:** nenhuma sintaxe `<% ... %>` pode ter sobrado em nenhum dos dois arquivos. Se sobrou → abortar antes de gravar.
    - **Com frontmatter:** cada arquivo DEVE abrir com um bloco YAML (`---` na linha 1, fechado por outro `---`) contendo, no mínimo, `title`, `type` e `community_session`. Se o Workbook OU o Processed sair sem frontmatter → abortar antes de gravar. (Regressão histórica: o Workbook nasce sem frontmatter quando se parte de um template antigo — esta guarda impede que volte a acontecer.)

12. **Cross-links automáticos:**
    - Workbook → Processed.
    - Ambos → Roadmap (link genérico, não há semana específica).
    - Não atualizar Roadmap.md (Community não tem entrada por semana no Roadmap — fica fora dessa estrutura).

13. **Salvar** ambos em `03-Domínios/Inglês/GCA/Community/`.

14. **Reportar** ao usuário:
    - Paths dos 2 arquivos gerados.
    - Resumo: "N rounds processados, você participou de M rounds (lista breve dos números + roles)".
    - Próximo passo sugerido: "Abra o Workbook **nas 2h seguintes** à sessão (memória fresca) pra preencher os slots reflexivos. Quando travar refletindo, invoque `/coaching` (modo socrático)."

## Tratamento de erros

- **PDF ausente** → erro com instrução pra colocar PDF na pasta correta.
- **Templates ausentes** → erro com paths explícitos.
- **PDF criptografado / só-imagem** → reportar limitação, sugerir OCR manual.
- **Usuário não encontrado em nenhum room** → não é erro; reportar no callout "Seus rooms" e Workbook só com recaps (sem slots reflexivos por round).
- **Formato de culture clash não detectado** (nem Bug/Executive nem Do's/Don'ts) → fallback genérico: tabela "Anti-pattern | Target".
- **Sintaxe Templater remanescente** → abortar antes de gravar.

## Não fazer

- **Não criar templates default** — se template não existir, abortar.
- **Não escrever reflexões pelo usuário** — slots reflexivos do Workbook ficam **vazios**. Reflexão é trabalho do usuário (com /coaching se quiser).
- **Não inferir performance** do usuário nos role-plays — PDF não diz como você performou; não invente avaliação.
- **Não consultar Roadmap.md** — Community é stream paralelo, não tem cycle/week.
- **Não modificar arquivos existentes** sem confirmação.
- **Não juntar rounds em que o usuário não participou** — preserve TODOS os rounds no Processed (contexto coletivo). Só o Workbook é seletivo.

## Convenções de output

- Arquivos finais: markdown puro, sem nenhuma sintaxe Templater.
- Frontmatter completo conforme template.
- Wikilinks padrão: `[[Roadmap]]`, `[[Community NN - <Nome>]]`.
- Conteúdo das frases-modelo (directives) em **EN** (vão ser falado em entrevista); contexto/instruções em **PT-BR**.
- Callouts apropriados: `> [!quote]` (frases), `> [!success]` (o que funcionou), `> [!failure]` (o que travou), `> [!example]` (vocab), `> [!todo]` (ajustes).
