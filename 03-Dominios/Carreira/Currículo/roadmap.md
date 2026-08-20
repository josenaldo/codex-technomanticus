---
title: "Roadmap — Currículo"
created: 2026-08-20
type: meta
publish: false
tags:
  - meta
  - roadmap
  - carreira
  - curriculo
---

# Roadmap — Currículo (galho-folha, construção)

Roadmap do galho `03-Dominios/Carreira/Currículo`. Construção nova (2026-08-20), a partir do plano em `00-Meta/specs/2026-08-20-galho-curriculo-plano.md` (30 tarefas) e da spec de design em `00-Meta/specs/2026-08-20-galho-curriculo-design.md`. Esta é a memória de retomada: cada linha aponta a tarefa do plano que a escreve, para que o galho possa ser continuado em outra sessão sem reler o plano inteiro.

> [!warning] Diagnóstico de 2026-08-20 — Tarefa 1 (andaime)
> Só a Tarefa 1 (pasta, MOC, roadmap) está feita. As outras 29 tarefas do plano ainda não rodaram. Todos os 26 alvos de nota abaixo são `pendente`.

## A tese e as duas lentes

**Tese (TL;DR do galho):** o currículo é a saída de um sistema de evidência, não um documento.

**Lente principal (eixo das notas):** a peça do documento — cabeçalho, sumário, experiência, habilidades — com a variação de senioridade mostrada lado a lado dentro de cada nota, não segregada numa trilha separada.

**Lente transversal:** o caminho de entrada no mercado — dez portas (ensino superior + estágio, trainee, iniciação científica, curso técnico, bootcamp, autodidata puro, transição de carreira, virada interna, projeto próprio, comunidade/open source), cada uma produzindo um inventário de evidência diferente. Concentra-se nas notas 02 e 10, e pesa nas notas de Iniciado; praticamente desaparece em Magus.

**Seis níveis:** estagiário · trainee · júnior · pleno · sênior · staff.

## Fronteiras (herdadas da spec, seção 5)

| O leitor quer | Vá para |
| --- | --- |
| o que a etapa de entrevista está avaliando | `Carreira/Entrevistas/` |
| inglês para contexto internacional | `Carreira/Inglês/` |
| posicionamento como negócio próprio, precificação, prospecção | `Carreira/Empreendedorismo/Fractional Engineer Brasil/` |
| o conteúdo técnico que a vaga cobra | as notas *"X em entrevista"* de cada galho técnico |

Sobreposição com Entrevistas é esperada e não deve ser policiada — a fronteira é de lente (o que esta etapa avalia × o que este documento precisa provar), não de assunto.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Notas de conteúdo (26 + broto) | 27 |
| Iniciado (01-09) | 9 |
| Adepto (10-19 + 18a) | 11 |
| Magus (20-26) | 7 |
| ✅ escritas | 1 |
| ⬜ pendentes | 26 |
| % concluído | 4% |
| Scaffolding | ✅ roadmap.md + index.md criados (Tarefa 1) |
| Wikilinks quebrados na Tarefa 1 (linha de base) | 27 (`/verificar-wikilinks`, 2026-08-20) — as 26 notas + o broto 18a do `index.md`, nenhum ainda existe; esperado até a Tarefa 30 |

---

## Notas — Iniciado (o terreno, os níveis e as portas)

#### 01 - Para que serve um currículo   [substantivo]
- **Estado:** ⬜ pendente · fase: iniciado
- **Tarefa do plano:** Bloco B
- **Escopo:** um objetivo único — gerar uma conversa; os três filtros em sequência; o erro de enquadramento (autobiografia, histórico de vida, vitrine de ferramenta gráfica).
- **Pendências:** —

#### 02 - As portas de entrada no mercado   [substantivo]
- **Estado:** ⬜ pendente · fase: iniciado
- **Tarefa do plano:** Bloco B
- **Escopo:** as dez portas, o requisito formal de cada uma, e a assimetria que isso cria; estágio e trainee são portas, não níveis (Lei 11.788/2008 verificada na fonte primária pela spec).
- **Pendências:** —

#### 03 - Os seis níveis e o que muda entre eles   [substantivo]
- **Estado:** ⬜ pendente · fase: iniciado
- **Tarefa do plano:** Bloco B
- **Escopo:** nota-mapa — ensina a ler o galho, estabelece o vocabulário de nível usado em todas as demais, e dá a regra de páginas por nível com a ressalva de que é consenso de mercado, não estudo.
- **Pendências:** —

#### 04 - Quem lê o seu currículo — e o que a evidência diz   [substantivo]
- **Estado:** ✅ escrita · fase: iniciado · 2026-08-20
- **Tarefa do plano:** Tarefa 2 (escrita antes do Bloco B, para estabelecer o vocabulário de ancoragem)
- **Escopo:** a nota de crítica de fonte — três leitores em sequência (máquina/varredura/leitura técnica), de onde vem a contaminação comercial (Jobscan/Enhancv/Teal/ResumeGeni/Greenhouse, nomeadas), três mitos derrubados (score automático, PDF quebra ATS, 6 segundos), texto branco/prompt injection como ponte para a nota 25, o que sobrevive, e caixa-preta declarada (LinkedIn Recruiter Search, market share de ATS).
- **Interfaces produzidas:** vocabulário de três categorias (evidência sólida / plausível mas não medido / caixa-preta declarada), usado pelo galho inteiro; wikilinks de ancoragem para as notas 05, 09, 17, 23 e 25.
- **Verificação:** gate G1-G5 rodado manualmente (checklist de `/verificar-nota` conferido item a item, sem invocar a skill via runtime) — 300 linhas (piso T1 ≥300 cumprido no limite), 1 diagrama Mermaid validado sem erro de sintaxe (`validar-mermaid.mjs`, 1 bloco, 0 quebrados), E1-E8 presentes, P2/P4 presentes, P1/P3 N/A, L1/L2 presentes, M1 ausente (recomendado, não obrigatório em iniciado).
- **Ajuste de régua registrado:** nenhum — a nota coube nas seções padrão do checklist (Casos práticos e Armadilhas comuns foram adaptados ao gênero de crítica de fonte, mas encaixaram sem forçar conteúdo).
- **Pendências:** M1 (vídeo/podcast) fica para enriquecimento futuro, não bloqueante nesta fase.

#### 05 - Formato e legibilidade de máquina   [substantivo]
- **Estado:** ⬜ pendente · fase: iniciado
- **Tarefa do plano:** Bloco B
- **Escopo:** coluna única, texto selecionável, cabeçalho e rodapé, tabelas, nome do arquivo, o teste de copiar e colar; por que "não use Canva" está certo pelo motivo errado — o problema é o layout, não a ferramenta.
- **Pendências:** —

#### 06 - Cabeçalho e identidade   [substantivo]
- **Estado:** ⬜ pendente · fase: iniciado
- **Tarefa do plano:** Bloco B
- **Escopo:** contato, links, localização e fuso, e o que nunca entra — com a ressalva de que isso varia por país.
- **Pendências:** —

#### 07 - O sumário profissional   [substantivo]
- **Estado:** ⬜ pendente · fase: iniciado
- **Tarefa do plano:** Bloco B
- **Escopo:** o trailer do documento; BLUF entra aqui; variação nos seis níveis.
- **Pendências:** —

#### 08 - Formação, cursos e certificações   [substantivo]
- **Estado:** ⬜ pendente · fase: iniciado
- **Tarefa do plano:** Bloco B
- **Escopo:** curadoria, posição no documento por nível, e onde o caminho de entrada pesa mais.
- **Pendências:** —

#### 09 - Habilidades técnicas   [substantivo]
- **Estado:** ⬜ pendente · fase: iniciado
- **Tarefa do plano:** Bloco B
- **Escopo:** a "Lista de Ingredientes" e a "Alphabet Soup", categorias, barras de proficiência, os termos da vaga, e a regra de lastro — não liste o que você não sustenta numa pergunta. Fecha o bloco Iniciado.
- **Pendências:** —

## Notas — Adepto (a matéria-prima)

#### 10 - Inventário de evidência   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Tarefa do plano:** Bloco C
- **Escopo:** a ponte entre as duas lentes — converte cada porta de entrada em material aproveitável, e nomeia a dúvida que cada porta desperta no leitor.
- **Pendências:** —

#### 11 - A linha de bullet   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Tarefa do plano:** Bloco C
- **Escopo:** a unidade de projeto — verbo de ação + o que foi feito + resultado; "responsável por" como a construção mais fraca do gênero; a matriz de power verbs.
- **Pendências:** —

#### 12 - XYZ, CAR e PAR — e as críticas   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Tarefa do plano:** Bloco C
- **Escopo:** origem da fórmula XYZ em Laszlo Bock, *Work Rules!* (2015); quando engessa, quando força métrica inexistente, quando a repetição mecânica denuncia.
- **Pendências:** —

#### 13 - Responsabilidade, realização e alavancagem   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Tarefa do plano:** Bloco C
- **Escopo:** a escada onde a senioridade fica mais nítida — task-taker, owner, force multiplier.
- **Pendências:** —

#### 14 - Números que você pode defender   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Tarefa do plano:** Bloco C
- **Escopo:** os três níveis de confiança — medido, contado, lembrado; par de números vale mais que percentual; falsa precisão do percentual derivado de baseline lembrada; números aposentados.
- **Pendências:** —

#### 15 - Quando não há número   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Tarefa do plano:** Bloco C
- **Escopo:** proxies de segunda ordem, consequência, escopo, frequência; honestidade como estratégia, não como limitação.
- **Pendências:** —

#### 16 - A seção de experiência profissional   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Tarefa do plano:** Bloco C
- **Escopo:** ordem, densidade decrescente com a idade da experiência, lacunas, passagens curtas, PJ e freelance.
- **Pendências:** —

#### 17 - Projetos, portfólio e GitHub depois da IA   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Tarefa do plano:** Bloco C
- **Escopo:** o que conta, a regra do README, e a desvalorização do projeto genérico como sinal.
- **Pendências:** —

#### 18 - Adaptar por vaga sem reescrever   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Tarefa do plano:** Bloco C
- **Escopo:** a adaptação cirúrgica — sumário, ordem e ênfase dos bullets, os termos da descrição; reescrever o documento inteiro é desperdício.
- **Pendências:** —

#### 18a - A carta de apresentação   [substantivo, broto]
- **Estado:** ⬜ pendente · fase: magus (broto, isento do piso de linhas)
- **Tarefa do plano:** Bloco C
- **Escopo:** a evidência sobre ela é genuinamente contraditória; a nota existe para dizer isso com as fontes na mão em vez de escolher um lado.
- **Pendências:** —

#### 19 - Declarar lacuna   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Tarefa do plano:** Bloco C
- **Escopo:** como e onde — na conversa, não no documento; por que inflar competência custa a vaga depois de conquistada. Fecha o bloco Adepto.
- **Pendências:** —

## Notas — Magus (o sistema por trás do documento)

#### 20 - A âncora   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Tarefa do plano:** Bloco D
- **Escopo:** o drill-down de quatro camadas; currículo como uma das quatro saídas da âncora.
- **Pendências:** —

#### 21 - O brag document   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Tarefa do plano:** Bloco D
- **Escopo:** Cheguei / Construí / Resultado; a métrica derivada, não autorada; evidência e reprodutibilidade; o hábito que quem está começando deveria adotar hoje.
- **Pendências:** —

#### 22 - O currículo como pipeline   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Tarefa do plano:** Bloco D
- **Escopo:** fonte única, base e variante, imutabilidade do que foi enviado, guardas automatizadas, versionamento.
- **Pendências:** —

#### 23 - LinkedIn — o par que responde a busca   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Tarefa do plano:** Bloco D
- **Escopo:** o que nele é caixa-preta declarada.
- **Pendências:** —

#### 24 - Mercados, e o Brazilian Cultural Bug   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Tarefa do plano:** Bloco D
- **Escopo:** Brasil × EUA × Europa; foto, dados pessoais, GDPR, Europass; alto contexto vs. BLUF, "we" vs. "I", vender esforço vs. vender alavancagem, ancorar em custo de vida vs. ancorar em valor.
- **Pendências:** —

#### 25 - IA nos dois lados   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Tarefa do plano:** Bloco D
- **Escopo:** LLM triando (viés medido em estudo peer-reviewed), candidato gerando (saturação e AI slop), prompt injection (o dado de 41% de autorrelato contra 1% de incidência real, e a saturação que anula a tática).
- **Pendências:** —

#### 26 - Seis currículos, uma carreira   [substantivo, capstone]
- **Estado:** ⬜ pendente · fase: magus
- **Tarefa do plano:** Bloco E
- **Escopo:** capstone — seis currículos, quatro ancorados em pessoas reais, uma persona fictícia declarada (estagiário) e uma projeção declarada (staff); fecha o galho com o mapa das 26 notas + broto.
- **Pendências:** —

---

## Próximos passos

1. ✅ Tarefa 1 — pasta, `index.md`, `roadmap.md` criados; `03-Dominios/Carreira/index.md` atualizado com a linha do galho — 2026-08-20.
2. ⬜ Tarefas 2-29 — Blocos A (gate factual), B (Iniciado), C (Adepto), D (Magus), E (capstone e fechamento), conforme `00-Meta/specs/2026-08-20-galho-curriculo-plano.md`.
3. ⬜ Tarefa 30 — fechamento: `/verificar-wikilinks 03-Dominios/Carreira/Currículo` precisa chegar a **zero** quebrados (linha de base desta tarefa: 27); poda da nota 05 de `Entrevistas` para virar ponte; atualização de `00-Meta/Roadmap.md` (Tier 3).

## Disciplina

- Escrita sequencial, bloco por bloco, conforme o plano de 30 tarefas.
- Todo exemplo etiquetado — `[!example] Caso real` (com link verificável) ou `[!example] Caso fictício` (persona declarada) — sem exceção.
- Nada do vault privado (`codex-technomanticus-apocrypha`) é referenciado.
- Frontmatter: `fase:` minúsculo (iniciado · adepto · magus), `type: concept`, `publish: true`.
- **Git:** stage de paths explícitos e estreitos. Sem `Co-Authored-By`.
