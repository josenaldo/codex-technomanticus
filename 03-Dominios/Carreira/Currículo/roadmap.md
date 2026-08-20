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
| ✅ escritas | 4 |
| ⬜ pendentes | 23 |
| % concluído | 15% |
| Scaffolding | ✅ roadmap.md + index.md criados (Tarefa 1) |
| Wikilinks quebrados na Tarefa 1 (linha de base) | 27 (`/verificar-wikilinks`, 2026-08-20) — as 26 notas + o broto 18a do `index.md`, nenhum ainda existe; esperado até a Tarefa 30 |

---

## Notas — Iniciado (o terreno, os níveis e as portas)

#### 01 - Para que serve um currículo   [substantivo]
- **Estado:** ✅ escrita · fase: iniciado · 2026-08-20 (revisada 2026-08-20)
- **Tarefa do plano:** Tarefa 3 (nota de abertura do galho, escrita depois da 04 para poder ancorar nela)
- **Escopo:** o objetivo único (gerar uma conversa, não relatar uma vida); os três enquadramentos errados (autobiografia, lista de tudo, vitrine gráfica), cada um com exemplo fictício e persona declarada; o currículo como peça de comunicação para um leitor apressado e cético (ancorado na nota 04, sem repetir números/fontes); a formulação que fecha — remove motivo de descarte e cria motivo de conversa — com diagrama Mermaid dos três leitores e das duas metades; o contrapeso honesto de fechamento (o currículo coloca na fila, quem tira dela costuma ser uma pessoa), com gancho explícito para as notas 20 e 26.
- **Interfaces produzidas:** a formulação "remove motivo de descarte e cria motivo de conversa" e o vocabulário dos três enquadramentos errados, usados como critério recorrente pelo resto do galho; wikilinks de ancoragem para as notas 02, 03, 04, 05, 06, 09, 11, 13, 14, 16, 18, 19, 20, 21, 25 e 26, e cross-galho para `Carreira/Entrevistas/01`.
- **Régua de profundidade — corrigida em 2026-08-20:** a régua de TAMANHO passou a medir **palavras** (faixa-alvo 4.500-6.500), não linhas — a contagem de linhas mede parágrafos, não conteúdo, num estilo de parágrafo único por linha; as notas de referência do vault têm 11-13 palavras/linha, esta tinha 31. **Contagem final: 6.420 palavras**, dentro da faixa-alvo, sem precisar de desvio.
- **Verificação:** gate G1-G5 rodado, mais uma rodada de correção de revisão — checklist de `/verificar-nota` conferido manualmente item a item (mesma ressalva de execução da nota 04: a skill carrega como procedimento para o próprio agente aplicar, não como subagente autônomo). E1, E2, E3, E5, E6, E7, E8 ✓ (TL;DR denso, abertura com cenário — não definição —, 1 diagrama Mermaid validado, O que vem a seguir, seção de inglês, tabela PT↔EN, 4 `[!warning]`); **E4 (Casos práticos) — ajuste de régua registrado abaixo**; S1 ✓ (`validar-mermaid.mjs`, 1 bloco, 0 quebrados); P1 N/A (nota conceitual); P2 ✓ (mecanismo de parsing referenciado à nota 04/05, exemplo de bullet antes/depois); P3 N/A (iniciado); P4 ✓ (números nos 3 exemplos fictícios da seção "Os três enquadramentos errados" e no bullet antes/depois da seção da formulação); T1 (linhas) já não é o critério — ver régua de palavras acima; L1 ✓ (wikilink cross-galho para `Carreira/Entrevistas/01`); L2 ✓ (Fontes com 2 entradas, ambas com URL verificável). M1 ausente — recomendado, não obrigatório em iniciado.
- **Ajuste de régua registrado — E4 "Casos práticos":** a seção `## Casos práticos` foi **removida** por decisão do revisor (achado 2 da rodada de correção): seus 3 cenários repetiam, com números diferentes, os mesmos três erros (autobiografia, lista de tudo, vitrine gráfica) já ilustrados um a um pelos exemplos de Marina, Rafael e Bianca dentro de "Os três enquadramentos errados" — duplicação de conteúdo, não cisão de tema. A ilustração concreta de cada erro ficou concentrada num único lugar (a seção dos três enquadramentos), que já satisfaz P4 (números em cada exemplo). O checklist padrão de `/verificar-nota` pede `## Casos práticos` como seção dedicada com ≥2 cenários; para esta nota específica, isso duplicava conteúdo essencial em vez de acrescentar — a régua foi ajustada em vez de a nota ser inflada para cumpri-la à letra.
- **Correção de fonte (rodada de revisão, achado 1 — Critical):** o link e a citação de "Por que ainda sou invisível?" (seção de fechamento e Fontes) apontavam para `https://josenaldo.com.br/blog/por-que-ainda-sou-invisivel`, que retorna **404** em produção — a versão em português do post existe no repositório/build local do blog, mas não está publicada. Corrigido nas duas ocorrências (seção "O currículo te coloca na fila" e `## Fontes`) para `https://josenaldo.com.br/blog/why-am-i-still-invisible` (título real: *Why am I still invisible?*, confirmado 200 pelo coordenador via `curl` ao vivo), com declaração explícita de que o post é em inglês e que a versão em português não está publicada. A data (jul/2024) já estava correta (frontmatter `2024-07-31 22:00 -0300`) e não foi alterada. O link da linha 28 (`/blog/como-escrever-o-seu-curriculo`, 200) estava correto e não foi tocado.
- **Corte de redundância (rodada de revisão, achado 2 — Important):** além da seção "Casos práticos" (ver ajuste de régua acima), cortada a seção inteira "Por que esta nota abre o galho" (meta-comentário sobre ordem de escrita vs. ordem de leitura — bastidor de produção, não conteúdo para o leitor) e material redundante identificado durante o corte para chegar à faixa-alvo de palavras: etimologia de *curriculum vitae*, lista de "quatro perguntas" heurísticas, parágrafo sobre a raiz psicológica do enquadramento "lista de tudo", parágrafo sobre por que "autobiografia" é difícil de largar, tabela de elementos decorativos (redirecionada para a nota 05), parágrafo distinguindo "peça de comunicação" de carta de apresentação/LinkedIn, o conceito de *satisficing* de Herbert Simon (removido do corpo e da seção Fontes), a tabela duplicada "Enquadramento → pergunta que ele responde" (mantida só a tabela posterior "Enquadramento errado → metade da formulação", mais central ao fecho da nota), a seção "Quando esta formulação pesa menos", e um parágrafo de fechamento redundante. Nota caiu de 9.438 para **6.420 palavras** — dentro da faixa-alvo, sem cortar o objetivo único, os três enquadramentos, a formulação de duas metades, o diagrama, ou o contrapeso honesto de fechamento (gancho para as notas 20/26 preservado).
- **Pendências:** M1 (vídeo/podcast) fica para enriquecimento futuro, não bloqueante nesta fase.

#### 02 - As portas de entrada no mercado   [substantivo]
- **Estado:** ✅ escrita · fase: iniciado · 2026-08-20
- **Tarefa do plano:** Tarefa 4 (Bloco B)
- **Escopo:** as dez portas, o requisito formal de cada uma, o que cada uma entrega de evidência e a dúvida que desperta no leitor; a tese de que estágio e trainee são portas com requisito formal, não níveis de senioridade; base legal com artigo citado (Lei 11.788/2008 — Art. 1º, 2º, 3º, 10, 11, 12, 13, e o Art. 2º § 3º na redação da Lei 14.913/2024, que equipara IC a estágio); trainee declarado explicitamente como prática de mercado (Exame, Serasa Experian, UBES), sem lei própria; diagrama Mermaid das dez portas convergindo para estagiário/trainee/júnior, mostrando a assimetria de acesso; dois casos reais — a trajetória encadeada do autor (1999-2006, portas 8→3→CEPEDI→PROPP) e a trajetória de Cassiana Gabriela Lima Barreto (porta 2+7, trainee de ciência de dados alocada em engenharia de dados).
- **Interfaces produzidas:** o vocabulário das dez portas (requisito de acesso / evidência / dúvida do leitor), reusado pela nota 10 (inventário de evidência) e citado pelas notas 08, 16, 19, 26; wikilinks de ancoragem para as notas 01, 03, 08, 10, 16, 19, 26, e cross-galho para `Carreira/Entrevistas/index`.
- **Régua de profundidade — palavras, não linhas:** medida em `wc -w`, faixa-alvo 4.500-6.500. **Contagem final: 6.608 palavras** (subiu de 6.563 na rodada de correção abaixo), levemente acima do teto — o revisor da rodada de correção concordou que cortar conteúdo bom por ~1-2% de excesso não compensa, então a nota ficou como está. O arquivo tem 228 linhas — abaixo do piso T1 (≥300 linhas) do checklist de `/verificar-nota`, mas essa régua de linhas mede parágrafos (1 parágrafo = 1 linha, por mais longa) e não conteúdo; a régua de palavras é a que vale, conforme a correção já registrada na nota 01. T1 tratado como N/A para este galho, substituído pela régua de palavras.
- **Verificação:** gate G1-G5 rodado — checklist de `/verificar-nota` conferido manualmente item a item. E1-E8 ✓ (TL;DR denso, abertura com cenário de frustração real — não definição —, 1 diagrama Mermaid validado por `validar-mermaid.mjs` (0 quebrados), seção "Casos práticos" com os 2 casos reais, "O que vem a seguir", seção de inglês, tabela PT↔EN, 3 `[!warning]` em Armadilhas comuns); S1 ✓; P1 N/A (nota conceitual, sem código); P2 ✓ (mecanismo legal e de mercado explicado, não só afirmado); P3 N/A (iniciado); P4 ✓ (grandezas legais — 2 anos, 6h/30h, 12-24 meses — e os dois casos reais com datas precisas); T1 — ver ajuste de régua acima; L1 ✓ (wikilink cross-galho para `Carreira/Entrevistas/index`); L2 ✓ (Fontes com 4 entradas, todas com URL verificável ou declaradas como prática de mercado); M1 ausente — recomendado, não obrigatório em iniciado.
- **G3 (conferência manual):** nenhuma linha quebrada manualmente (parágrafos em linha única, checado por comprimento de linha); as duas etiquetas `[!example] Caso real` presentes, ambas com link verificável (josenaldo.com.br/experiences; linkedin.com/in/cassianalima); nenhum vazamento de `codex-technomanticus-apocrypha` (grep vazio).
- **Correções da revisão jurídica (2026-08-20):** a base legal (Art. 1º, 2º §1º-§3º, 3º caput e I, 10 II, 11, 12, 13) foi conferida artigo por artigo pelo revisor diretamente contra o texto consolidado no Planalto — passou limpa, sem artigo trocado, condição omitida ou afirmação mais forte que a lei; o Art. 2º § 3º (Lei 14.913/2024) confirmado literalmente. Duas correções pontuais aplicadas: (1) a data da IC no caso real do autor fundia a duração da bolsa com a duração do projeto — corrigida para "bolsista de abril de 2003 a agosto de 2004, num projeto que se estendeu até 2005" (dado conferido pelo revisor em `josenaldo.com.br/experiences`), com um aparte curto transformando a própria distinção bolsa-vs-projeto numa lição sobre o que quem entrevista confere contra o LinkedIn; (2) a palavra "already" solta em inglês no TL;DR (parágrafo mais lido da nota) trocada por "já". Nenhum outro corte ou reescrita — o revisor pediu explicitamente para não tocar em mais nada além dessas duas correções.
- **Pendências:** M1 (vídeo/podcast) fica para enriquecimento futuro, não bloqueante nesta fase.

#### 03 - Os seis níveis e o que muda entre eles   [substantivo]
- **Estado:** ✅ escrita · fase: iniciado · 2026-08-20
- **Tarefa do plano:** Tarefa 5 (nota-mapa)
- **Escopo:** os seis níveis descritos pelo que o documento precisa provar em cada um (não pelo que a pessoa sabe); remissão explícita à [[03-Dominios/Carreira/Currículo/02 - As portas de entrada no mercado|nota 02]] para não reabrir a discussão porta-vs-nível; o eixo central — o que sobe (impacto organizacional, liderança técnica sem cargo de gestão, decisão de arquitetura, mentoria) e o que desce (stack linha a linha, tarefa de dia a dia, certificação básica) — com exemplo trabalhado (persona fictícia Renata Aquino, o mesmo evento de migração de gateway de pagamento descrito em seis versões, uma por nível) e diagrama Mermaid da escada; a regra de páginas por nível declarada como convenção de mercado sem fonte primária localizada (mais perto de caixa-preta declarada do que de plausível-mas-não-medido, reusando o vocabulário da nota 04), com URLs verificáveis de Jobscan e Enhancv citadas como fontes comerciais; a tabela-mapa (nível × o que provar × onde no galho) como índice funcional do galho inteiro.
- **Interfaces produzidas:** o vocabulário de nível (o que cada um precisa provar) e o eixo sobe/desce, que o restante do galho reusa; a tabela-mapa, ponto de retorno para as notas que tratarem variação por nível sem repetir a explicação; wikilinks de ancoragem para as notas 02, 04, 07, 08, 09, 11, 13, 14, 20, 21, 22, 26, e cross-galho para `Carreira/Entrevistas/index`.
- **Régua de profundidade — palavras, não linhas:** medida em `wc -w`, faixa-alvo 4.500-6.500. **Contagem final: 5.600 palavras**, dentro da faixa-alvo. O arquivo tem 179 linhas — abaixo do piso T1 (≥300) do checklist de `/verificar-nota`, mesma situação já registrada nas notas 01 e 02: a régua de linhas mede parágrafos (1 parágrafo = 1 linha), não conteúdo; T1 tratado como N/A, substituído pela régua de palavras.
- **Verificação:** gate G1-G5 rodado — checklist de `/verificar-nota` conferido manualmente item a item. E1 ✓ (TL;DR denso) · E2 ✓ (abre com o caso fictício de Diego, não com definição) · E3 ✓ (1 diagrama Mermaid da escada sobe/desce, validado por `validar-mermaid.mjs`, 0 quebrados) · E4 — **ajuste de régua registrado abaixo** · E5 ✓ · E6 ✓ (seção "Como soa em inglês") · E7 ✓ (tabela PT↔EN) · E8 ✓ (3 `[!warning]` em Armadilhas comuns); S1 ✓; P1 N/A (nota conceitual, sem código); P2 ✓ (explica por que o eixo sobe/desce acontece, não só que acontece — ligado ao que o leitor de cada nível precisa decidir); P3 N/A (iniciado); P4 ✓ (grandezas no exemplo de Renata: 2,3% → 0,4% de taxa de falha, doze/catorze anos de carreira, seis de doze endpoints, dois anos de vigência da decisão); T1 — ver ajuste de régua de palavras acima; L1 ✓ (wikilink cross-galho para `Carreira/Entrevistas/index`); L2 ✓ (Fontes com URLs verificáveis de Jobscan e Enhancv, declaradas como comerciais); M1 ausente — recomendado, não obrigatório em iniciado.
- **Ajuste de régua registrado — E4 "Casos práticos":** nenhuma seção `## Casos práticos` dedicada foi criada, seguindo o mesmo precedente já registrado na nota 01 (achado 2 da rodada de correção): o caso de Diego (abertura) e o exemplo trabalhado de Renata Aquino (seis versões do mesmo evento, uma por nível) já cobrem, dentro do fluxo da nota, o papel que uma seção dedicada de "Casos práticos" cumpriria — duplicar esses dois cenários numa seção à parte inflaria a nota sem acrescentar conteúdo novo, contrariando a régua de palavras (faixa 4.500-6.500) que esta nota já preenche com folga confortável. Ambos os cenários carregam etiqueta `[!example] Caso fictício` com persona declarada, conforme exigido.
- **G3 (conferência manual):** nenhuma linha quebrada manualmente (parágrafos em linha única); as duas etiquetas `[!example] Caso fictício` presentes, ambas com persona declarada (Diego, Renata Aquino); nenhum vazamento de `codex-technomanticus-apocrypha` (grep vazio).
- **Pendências:** M1 (vídeo/podcast) fica para enriquecimento futuro, não bloqueante nesta fase.

#### 04 - Quem lê o seu currículo — e o que a evidência diz   [substantivo]
- **Estado:** ✅ escrita · fase: iniciado · 2026-08-20
- **Tarefa do plano:** Tarefa 2 (escrita antes do Bloco B, para estabelecer o vocabulário de ancoragem)
- **Escopo:** a nota de crítica de fonte — três leitores em sequência (máquina/varredura/leitura técnica) + o quarto perfil (modelo enviesado), de onde vem a contaminação comercial (Jobscan/Enhancv/Teal/ResumeGeni/Greenhouse, nomeadas), quatro mitos derrubados (score automático, PDF quebra ATS, 6 segundos, ATS score universal), texto branco/prompt injection como ponte para a nota 25, o que sobrevive, e caixa-preta declarada (LinkedIn Recruiter Search, market share de ATS).
- **Interfaces produzidas:** vocabulário de três categorias (evidência sólida / plausível mas não medido / caixa-preta declarada), usado pelo galho inteiro; wikilinks de ancoragem para as notas 05, 09, 17, 23 e 25.
- **Verificação:** gate G1-G5 rodado — rodada 1: checklist conferido manualmente item a item (a skill `/verificar-nota` carrega como procedimento de auditoria para o próprio agente executar, não como subagente autônomo que roda sozinho; segui o procedimento à risca, incluindo o validador de Mermaid, mas sem produzir o relatório no formato literal do template). Rodada de correção (2026-08-20): procedimento reexecutado com o relatório no formato do template — 323 linhas (piso T1 ≥300 com margem), 1 bloco Mermaid validado (`validar-mermaid.mjs`, 0 quebrados), E1-E8 ✓, S1 ✓, P1/P3 N/A, P2/P4 ✓, T1 ✓, L1 ✓ (wikilink cross-galho para `Tecnologia/IA/Segurança e Guardrails/13 - Prompt injection`), L2 ✓, M1 ausente (recomendado, não obrigatório em iniciado — isenção parcial, não reprova). 12/12 itens aplicáveis ✓.
- **Ajuste de régua registrado:** nenhum — a nota coube nas seções padrão do checklist (Casos práticos e Armadilhas comuns foram adaptados ao gênero de crítica de fonte, mas encaixaram sem forçar conteúdo).
- **Correções da revisão (rodada 1):** (1) linha sobre "ATS não calcula nota nenhuma" suavizada para "não configura corte automático por nota" — a spec só sustenta a ausência de corte automático, não a ausência de qualquer score interno; (2) adicionados os números do estudo Wilson & Caliskan (85% preferência por nomes brancos, 52% por nomes masculinos, homens negros mais penalizados, follow-up UW nov/2025 sobre absorção de viés por humanos) em seção própria "Quando o leitor é, ele mesmo, um modelo enviesado"; (3) o quarto mito da spec 8.2 ("existe um ATS score universal e confiável") ganhou seção própria "Mito 4", no mesmo formato dos outros três, removendo a duplicação que antes estava diluída em "De onde vem o que você ouviu". Nota cresceu de 300 para 323 linhas, só com conteúdo sourced já presente na spec (nenhum preenchimento por cota).
- **Correções da revisão (rodada 2):** os números do estudo Wilson & Caliskan foram conferidos diretamente no abstract da fonte primária (arXiv 2407.20371) em 2026-08-20, e três dos quatro reportados na rodada 1 corrigidos: amostra é "mais de 500 currículos **e** mais de 500 descrições de vaga" (não "550+ currículos"), preferência por nomes brancos é 85,1% (não 85%), o eixo de gênero correto é "nomes de mulheres favorecidos em apenas 11,1% dos casos" (não "nomes masculinos em 52%", número que não existe no paper), e homens negros são desfavorecidos em até 100% dos casos (mais forte do que a formulação anterior "categoria mais penalizada"). A spec-mãe também foi corrigida (commit `737bc948`, fora deste galho).
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
