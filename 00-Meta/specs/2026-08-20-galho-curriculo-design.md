---
title: "Design — Galho: Currículo"
created: 2026-08-20
type: meta
publish: false
tags:
  - meta
  - spec
  - design
  - curriculo
  - carreira
---

# Design — Galho: Currículo

> [!abstract] TL;DR
> Galho novo em `03-Dominios/Carreira/Currículo/`, par de Entrevistas. **26 notas + 1 broto**, três fases, duas lentes cruzadas — **peça do documento** (eixo principal) × **caminho de entrada no mercado** (eixo transversal, concentrado no início da carreira). Seis níveis: estagiário, trainee, júnior, pleno, sênior, staff. A tese que diferencia o galho de qualquer guia do mercado: **o currículo é a saída de um sistema de evidência, não um documento**. Todo dado é etiquetado como real ou fictício. O capstone tem seis peças: quatro de pessoas reais, uma persona fictícia (estagiário) e uma projeção (staff), cada uma declarada.

## 1. Problema

Perguntas sobre "como fazer currículo" chegam ao usuário com frequência, vindas de todos os níveis — do estagiário ao sênior. As respostas disponíveis publicamente são ruins por três razões distintas, e cada uma exige um remédio diferente.

**Primeira: o mercado de conteúdo sobre currículo é comercialmente contaminado.** A esmagadora maioria das fontes que aparecem em busca é de empresas que vendem "ATS checker" e "resume optimizer" — Jobscan, Enhancv, Teal, ResumeGeni, entre outras. Elas têm incentivo direto para inflar a importância do ATS e vender a cura. O resultado é um corpo de folclore repetido por anos sem verificação: o "ATS score" que reprova, o PDF que quebra o parser, os seis segundos de leitura. A pesquisa conduzida em 2026-08-20 encontrou evidência sólida contra as três formulações (ver seção 8).

**Segunda: o material existente cobre um nível só.** O post do blog do próprio usuário, `como-escrever-o-seu-curriculo.md` (fev/2026), é um guia completo e bem escrito, mas declara no subtítulo que mira "estagiários, juniores e plenos com pouca experiência". Sênior e staff não têm material equivalente em português, e o que muda entre os níveis quase nunca é explicado — assume-se que o leitor descobrirá sozinho.

**Terceira, e a mais grave: ninguém escreve sobre o caminho de entrada.** Um autodidata e um recém-formado não têm o mesmo material para colocar num currículo, não enfrentam a mesma dúvida do leitor, e sequer têm acesso às mesmas portas de entrada. Todo guia trata "júnior" como categoria única, quando na prática o que a pessoa tem para mostrar é determinado por como ela chegou ali.

Há ainda um problema de fundo que este galho resolve por acidente: o usuário construiu ao longo de 2025-2026 um sistema completo de evidência de carreira — brag documents, métricas canônicas com níveis de confiança, pipeline de geração de currículo com guardas automatizadas — e esse conhecimento não existe escrito em lugar nenhum, nem público nem privado, exceto disperso em specs de implementação e mensagens de commit.

## 2. Objetivo

Produzir um galho público que sirva **do estagiário ao staff**, organizado pela peça do documento, com a senioridade e o caminho de entrada aparecendo como variação dentro de cada nota. O galho deve ser honesto sobre a qualidade da evidência disponível, distinguindo o que é medido do que é folclore, e deve ensinar o sistema por trás do documento — não apenas o documento.

Objetivo secundário, declarado: o galho é também **peça de vitrine**. Ao usar a trajetória real do autor como exemplo trabalhado, ele apresenta o autor a quem chegou procurando ajuda com currículo. Isso é deliberado e não conflita com o rigor — ao contrário, a política de etiquetagem da seção 6 torna a vitrine auditável, o que a fortalece.

## 3. Decisões

### 3.1 Galho próprio sob Carreira, não sub-galho de Entrevistas

O galho mora em `03-Dominios/Carreira/Currículo/`, par de `Carreira/Entrevistas/` e `Carreira/Empreendedorismo/`.

**Por quê:** o assunto extrapola o funil seletivo. Brag document, LinkedIn e portfólio são atividade **contínua**, exercida quando a pessoa não está se candidatando a nada. Colocar isso dentro de Entrevistas subordinaria o hábito ao evento — que é precisamente o erro que o galho existe para combater. Entrevistas declara no próprio índice ser "catálogo de teoria geral do processo de entrevista técnica sênior"; currículo não cabe nessa fronteira sem distorcê-la.

**Rejeitado — sub-galho de Entrevistas:** mais barato e preservaria a numeração existente, mas herda a fronteira errada.

**Rejeitado por ora — domínio novo "Marca Profissional"** englobando currículo, LinkedIn, portfólio, blog e presença pública. É para onde o assunto tende a crescer, e o post *Por que ainda sou invisível no mercado de trabalho?* já é matéria-prima disso. Grande demais para abrir agora; o galho pode graduar a domínio depois, pela convenção broto → galho que o vault já usa.

### 3.2 A nota 05 de Entrevistas vira ponte, não é apagada

`Carreira/Entrevistas/05 - Currículo e LinkedIn como artefatos de triagem.md` (126 linhas, fase Iniciado) é podada e reescrita como **nota-ponte**, mantendo apenas o enquadramento de triagem que serve ao funil e remetendo ao galho novo para tudo o mais.

**Por quê:** é exatamente o padrão que `09 - System design em entrevista — a ponte` (89 linhas) já executa para a trilha de System Design. Precedente do próprio vault, sem invenção de convenção nova. A numeração de Entrevistas permanece intacta, e os inbound links continuam resolvendo.

O conteúdo absorvido pelo galho novo inclui: a fórmula verbo + o que foi feito + resultado, a crítica ao "responsável por", os três avisos de armadilha, o bloco "Como soa em inglês" e a tabela PT/EN. O diagrama Mermaid da linha de bullet migra para a nota da linha de bullet.

### 3.3 Lente principal: a peça do documento, com senioridade variando dentro

Cada nota trata de uma peça ou de um conceito, e mostra a variação por nível **lado a lado dentro da nota** — o sumário do estagiário, o do pleno e o do staff na mesma página.

**Por quê:** o leitor lê o galho uma vez e ele continua servindo quando for promovido; o currículo dele evolui junto com a carreira. Casa com o padrão de fases do vault (Iniciado/Adepto/Magus). E resolve um problema real da alternativa: conceitos como âncora, BLUF e níveis de confiança não são "assunto de sênior" — são o mesmo assunto explicado com exemplos de tamanhos diferentes, e plantar o hábito do brag document em quem está começando é provavelmente o conselho mais valioso do galho inteiro.

**Rejeitado — trilhas paralelas por nível:** o iniciante lê só a parte dele e vai embora, mas o material de sênior fica ilhado numa ponta que ele nunca alcança, e a repetição entre trilhas seria grande.

### 3.4 Lente transversal: o caminho de entrada no mercado

Dez portas de entrada, mapeadas explicitamente. Cada uma produz um **inventário de evidência** diferente e uma **dúvida do leitor** diferente.

1. Ensino superior → estágio → efetivação
2. Ensino superior → programa de trainee
3. Iniciação científica / laboratório de pesquisa
4. Curso técnico / Instituto Federal → jovem aprendiz ou estágio técnico
5. Bootcamp / curso livre
6. Autodidata puro
7. Transição de carreira (traz experiência profissional real de outra área)
8. Virou dev por dentro da empresa (suporte, QA, analista de negócio — ou o caso de quem entra sem saber nada e vira a pessoa do software)
9. Projeto próprio, freelance, indie
10. Comunidade e open source

**A observação que sustenta a nota 02:** estágio e trainee **não são níveis de senioridade — são portas com requisito formal**. Estágio exige matrícula em curso; programa de trainee tipicamente exige formação recente. O autodidata não tem acesso a nenhuma das duas, e por isso entra direto como júnior, competindo com quem já acumulou dois anos de estágio. Isso explica frustração que muita gente vive sem entender a causa.

> [!success] Verificado na fonte primária em 2026-08-20
> **Lei 11.788/2008**, texto consolidado no Planalto. Estágio é ato educativo escolar supervisionado e exige **matrícula e frequência regular atestadas pela instituição de ensino** (Art. 1º e Art. 3º, I); **não cria vínculo empregatício** (Art. 3º); jornada máxima de **6h diárias e 30h semanais** para ensino superior (Art. 10, II); duração máxima de **2 anos na mesma parte concedente**, exceto estagiário com deficiência (Art. 11); **bolsa e auxílio-transporte são compulsórios** no estágio não obrigatório (Art. 12); recesso de 30 dias quando o estágio dura 1 ano ou mais (Art. 13).
>
> **Achado que sustenta a porta 3.** O **Art. 2º, § 3º** — na redação dada pela **Lei nº 14.913, de 2024** — estabelece que atividades de extensão, monitoria, **iniciação científica** e intercâmbio no exterior *poderão ser equiparadas ao estágio em caso de previsão no projeto pedagógico do curso*. A porta da IC não é analogia: tem status legal explícito e recente.
>
> **Trainee** não tem lei própria: é contratação **CLT com todos os direitos trabalhistas**, programas tipicamente de 12 a 24 meses, dirigidos a recém-formados ou com até ~2 anos de formação, com rodízio por áreas e mira em posição de liderança. Fontes secundárias (Exame, Serasa Experian, UBES) — declarar como prática de mercado, não como norma.

O eixo é **transversal, não estrutural**: ele não gera um bloco de notas próprio. Concentra-se na nota 02 (o mapa das portas), na nota 10 (o inventário de evidência que cada porta produz) e nas notas de Iniciado em que pesa mais — formação e certificações, projetos, seção de experiência. Nas notas de Magus praticamente desaparece, porque a essa altura o caminho de entrada deixou de determinar o material.

### 3.5 Seis níveis

Estagiário · trainee · júnior · pleno · sênior · staff.

Trainee entra por pedido explícito do usuário e por existir caso real disponível (seção 6.2). Staff entra porque a regra de páginas e a hierarquia do que sobe e desce no documento mudam de verdade ali — e porque a pesquisa encontrou consenso de que comprimir um currículo de staff em uma página é lido como sinal de que o candidato não percebeu que as regras mudaram.

### 3.6 A tese: o currículo é a saída de um sistema, não um documento

O bloco Magus não é "dicas avançadas". Ele apresenta o sistema que o usuário construiu e operou entre 2025 e 2026, e que é o conteúdo genuinamente original do galho:

- **A âncora** — uma frase que define o diferencial, obtida por drill-down de quatro camadas (ferramentas → tipo de sistema → o movimento que se repete → o diferencial). Currículo, pitch, resposta comportamental e negociação salarial são quatro saídas da mesma âncora; sem ela, cada saída improvisa uma versão diferente e o leitor sente a inconsistência.
- **O brag document** — anatomia Cheguei / Construí / Resultado, com a métrica derivada da conquista em vez de autorada. A frase que justifica o sistema inteiro: *"a nota registra o número, não o trabalho"*.
- **O currículo como pipeline** — fonte única, base reutilizável, variante por vaga como cópia autônoma e imutável (currículo enviado é registro histórico), guardas automatizadas que abortam a geração quando um número aposentado aparece.

### 3.7 Rigor de fonte é conteúdo, não rodapé

A nota 04 (quem lê e o que a evidência de fato diz) é uma peça de crítica de fonte, não um resumo de melhores práticas. Ela nomeia a contaminação comercial do assunto, mostra de onde vem cada número repetido, e distingue três categorias: o que tem evidência sólida, o que é plausível mas não medido, e o que é caixa-preta.

Isso não é preciosismo. É a mesma cultura de rigor que o resto do Codex já pratica, e é o que dá ao galho uma lente que nenhum guia de currículo do mercado tem.

## 4. Estrutura

### Iniciado — o terreno, os níveis e as portas (9 notas)

1. **O que um currículo faz — e o que ele não é.** Um objetivo único: gerar uma conversa. Os três filtros em sequência. O erro de enquadramento (autobiografia, histórico de vida, vitrine de ferramenta gráfica).
2. **Os caminhos de entrada — e por que estágio e trainee são portas, não níveis.** As dez portas, o requisito formal de cada uma, e a assimetria que isso cria.
3. **Os seis níveis e o que muda entre eles.** Nota-mapa: ensina a ler o galho, estabelece o vocabulário de níveis usado em todas as demais, e dá a regra de páginas por nível com a ressalva de que ela é consenso de mercado, não estudo.
4. **Quem lê, e o que a evidência de fato diz.** A nota de crítica de fonte.
5. **Formato e legibilidade de máquina.** Coluna única, texto selecionável, cabeçalho e rodapé, tabelas, nome do arquivo, o teste de copiar e colar. Por que "não use Canva" está certo pelo motivo errado — o problema é o layout, não a ferramenta.
6. **Cabeçalho e identidade.** Contato, links, localização e fuso, e o que nunca entra — com a ressalva de que isso varia por país.
7. **O sumário.** O trailer do documento. BLUF entra aqui. Variação nos seis níveis.
8. **Formação, cursos e certificações.** Curadoria, posição no documento por nível, e onde o caminho de entrada pesa mais.
9. **Habilidades técnicas.** A "Lista de Ingredientes" e a "Alphabet Soup", categorias, barras de proficiência, os termos da vaga, e a regra de lastro: não liste o que você não sustenta numa pergunta.

### Adepto — a matéria-prima (10 notas + 1 broto)

10. **Inventário de evidência: o que o seu caminho te deu.** A ponte entre as duas lentes. Converte cada porta de entrada em material aproveitável, e nomeia a dúvida que cada porta desperta no leitor.
11. **A linha de bullet.** A unidade de projeto. Verbo de ação + o que foi feito + resultado. "Responsável por" como a construção mais fraca do gênero. A matriz de power verbs.
12. **XYZ, CAR, PAR — os frameworks e suas críticas.** Origem da fórmula XYZ em Laszlo Bock, *Work Rules!* (2015). Quando engessa, quando força métrica inexistente, quando a repetição mecânica denuncia.
13. **A escada: responsabilidade → realização → alavancagem.** Onde a senioridade fica mais nítida. Task-taker, owner, force multiplier.
14. **Números que você pode defender.** Os três níveis de confiança — medido, contado, lembrado. Par de números vale mais que percentual. Falsa precisão: percentual derivado de baseline lembrada. Números aposentados.
15. **Quando não há número.** Proxies de segunda ordem, consequência, escopo, frequência. Honestidade como estratégia, não como limitação.
16. **A seção de experiência.** Ordem, densidade decrescente com a idade da experiência, lacunas, passagens curtas, PJ e freelance.
17. **Projetos, portfólio e GitHub depois da IA.** O que conta, a regra do README, e a desvalorização do projeto genérico como sinal.
18. **Adaptar por vaga sem reescrever.** A adaptação cirúrgica: sumário, ordem e ênfase dos bullets, os termos da descrição. Reescrever o documento inteiro é desperdício.
    - **18a — A carta de apresentação** (broto, fase Magus, isento do piso de linhas). A evidência sobre ela é genuinamente contraditória, e a nota existe para dizer isso com as fontes na mão em vez de escolher um lado.
19. **Declarar lacuna.** Como e onde — na conversa, não no documento. Por que inflar competência custa a vaga depois de conquistada.

### Magus — o sistema por trás do documento (7 notas)

20. **A âncora.** O drill-down de quatro camadas. Currículo como uma das quatro saídas.
21. **O brag document.** Cheguei / Construí / Resultado. A métrica derivada, não autorada. Evidência e reprodutibilidade. O hábito que quem está começando deveria adotar hoje.
22. **O currículo como pipeline.** Fonte única, base e variante, imutabilidade do que foi enviado, guardas automatizadas, versionamento.
23. **LinkedIn — o par que responde a busca, não a leitura.** E o que nele é caixa-preta declarada.
24. **Mercados, e o *Brazilian Cultural Bug*.** Brasil × EUA × Europa. Foto, dados pessoais, GDPR, Europass. Alto contexto vs. BLUF, "we" vs. "I", vender esforço vs. vender alavancagem, ancorar em custo de vida vs. ancorar em valor.
25. **IA nos dois lados.** LLM triando (viés medido em estudo peer-reviewed), candidato gerando (saturação e AI slop), prompt injection (o dado de 41% de autorrelato contra 1% de incidência real, e a saturação que anula a tática).
26. **Capstone — seis currículos, carreiras reais.** Ver seção 6.2.

Artefatos do galho: `index.md` (MOC com as três fases) e `roadmap.md` (convenção vault-wide de rastreio recursivo). Sem Dicionário próprio — é galho, não domínio.

## 5. Fronteiras

| O leitor quer | Vá para |
| --- | --- |
| o que a etapa de entrevista está avaliando | `Carreira/Entrevistas/` |
| inglês para contexto internacional | `Carreira/Inglês/` |
| posicionamento como negócio próprio, precificação, prospecção | `Carreira/Empreendedorismo/Fractional Engineer Brasil/` |
| o conteúdo técnico que a vaga cobra | as notas *"X em entrevista"* de cada galho técnico |

Sobreposição com Entrevistas é esperada e não deve ser policiada — a fronteira é de lente, não de assunto, conforme a convenção do vault. Entrevistas pergunta *o que esta etapa avalia*; Currículo pergunta *o que este documento precisa provar*.

## 6. Política de dados e exemplos

### 6.1 Etiquetagem obrigatória

Todo dado usado como exemplo carrega um de dois marcadores, sem exceção:

- `> [!example] Caso real` — com link verificável para `josenaldo.com.br/experiences`, para o repositório, para o commit ou para a fonte pública de terceiro.
- `> [!example] Caso fictício` — persona inventada, declarada na hora.

**Por quê:** o galho ensina, nas notas 14 e 15, que a procedência de um número é parte do número. Um galho que etiqueta a própria evidência **demonstra** a tese em vez de apenas afirmá-la. E como o galho é também vitrine, a auditabilidade é o que a torna crível.

Números reais do autor **entram**, por decisão explícita do usuário em 2026-08-20. A restrição de privacidade permanece para material de terceiros e para o vault privado: nada de `codex-technomanticus-apocrypha` é referenciado, e nenhum dado de cliente é nomeado além do que já é público no site.

### 6.2 Composição do capstone

Seis peças. Quatro ancoradas em pessoas reais, uma persona fictícia declarada (estagiário) e uma projeção declarada (staff).

| Nível | Origem | Base factual |
| --- | --- | --- |
| Estagiário | **Persona fictícia declarada** | o autor nunca foi estagiário (ver 6.3) |
| Trainee | Real | Cassiana Gabriela Lima Barreto — Dadosfera, 2024 |
| Júnior | Real, reconstruído | CEPEDI, a partir de nov/2003 — júnior cuja única experiência era bolsa de IC |
| Pleno | Real, reconstruído | o arco SWB → everis → TQI → Sankhya |
| Sênior | Real e atual | o documento que existe hoje, público |
| Staff | **Projeção declarada** | o degrau seguinte, não registro |

O currículo de staff ser assumidamente uma projeção é o fecho do galho: escrever o currículo do nível que se quer é técnica real, e o capstone a executa em vez de descrevê-la.

**Reconstrução é declarada como tal.** Os currículos de júnior e pleno não são documentos que existiram — são reconstruções feitas hoje a partir de registro público datado. O galho diz isso na cara do leitor.

### 6.3 A trajetória do autor como exemplo trabalhado

Fatos confirmados pelo usuário em 2026-08-20, a usar como espinha da lente dos caminhos de entrada:

- **1999** — primeiro software: sistema em Access para uma empresa de Itabuna. Entrou sem saber nada, aprendeu a ferramenta ali, implementou tabelas, consultas, relatórios e menus, e deu manutenção durante todo o ano. Porta 8 (virou dev por dentro).
- **2000** — entra na graduação, motivado pela experiência anterior.
- **2003-2005** — bolsista de iniciação científica no Labbi/UESC. **O usuário considera esta a sua primeira experiência profissional.** Porta 3.
- **nov/2003** — CEPEDI, como **Java Júnior** (não estagiário — corrigido pelo usuário em 2026-08-20); chegou pelo orientador do Labbi, que era diretor. Entrada direta em júnior, aberta pela porta 3.
- **2005 ou 2006** — PROPP (pró-reitoria de pós-graduação), com o mesmo orientador, então pró-reitor.
- Retorno ao CEPEDI depois da PROPP.

**A tese que essa trajetória sustenta, e que dá honestidade ao galho inteiro:** as portas se compõem, e quem as abre costuma ser uma pessoa, não um documento. Cinco movimentos encadeados por uma relação. Isso fecha com a frase que o próprio autor já publicou — *o currículo te coloca na fila, mas é a sua reputação que te tira dela* — e é o contrapeso necessário num galho inteiramente dedicado a um documento.

> [!success] Divergência resolvida em 2026-08-20
> O site está correto: no CEPEDI o vínculo era **Java Júnior**. O relato inicial de "estagiário" foi engano do usuário. **Consequência para o capstone:** o autor nunca foi estagiário, e a peça de estagiário passa a ser persona fictícia declarada. Em contrapartida, a peça de **júnior** fica mais forte e mais rara — um júnior real cuja única experiência anterior era bolsa de iniciação científica, situação comum e sem material publicado.

### 6.4 O caso Cassiana — trainee

Verificado em fonte pública em 2026-08-20:

- Doutorado em Sistemas Computacionais e dispositivos aplicados à saúde, UFU, 2020-2025 — portanto **entrou no mercado antes de concluir o doutorado**.
- Mestrado pelo PPG em Engenharia Biomédica da UFU; trabalho de avaliação de usabilidade de monitor multiparamétrico em unidade pública de saúde, com teste de usabilidade, categorização de falhas de dispositivo médico e análise estatística.
- Publicações sobre telemedicina no contexto da COVID-19 e avaliação de tecnologia em saúde.
- Perfil público na DIO — rastro datado de estudo autodidata.
- Hoje Engenheira de Dados Júnior na Dadosfera, em Uberlândia.
- Depoimento público na página de carreiras da Dadosfera: *"Após uma trajetória voltada à academia, minha primeira experiência no ambiente profissional marcou a transição da teoria para desafios reais."*

Relatado pelo usuário, **a confirmar com ela**: aprendeu Python durante o doutorado por necessidade da pesquisa, depois banco de dados e ciência de dados; entrou na Dadosfera como **trainee** em 2024; promovida a júnior pouco mais de um ano depois.

**Divergência resolvida em 2026-08-20.** A leitura correta é **engenharia de dados**. A trajetória explica a aparente contradição, e ela própria vira conteúdo: no início ela mirava **ciência** de dados, foi **contratada como trainee de ciência de dados**, e logo foi **alocada em engenharia de dados** — onde a carreira de fato evoluiu, até a promoção a júnior. O headline do LinkedIn ("Data Scientist | Researcher | Biomedical Engineer") é resíduo da mira original, não do cargo atual.

**A lição que este caso ensina, e que nenhum guia de currículo cobre:** o título sob o qual você entra é uma aposta da empresa, não um contrato de destino. A porta de entrada abre para a organização, não para uma carreira específica — e quem trata o título de entrada como identidade fixa perde a chance de crescer onde de fato há demanda. Isso alimenta a nota 02 (portas de entrada) e a nota 23 (a inconsistência entre LinkedIn e currículo, aqui com causa legítima e explicável, não descuido).

**Currículo recebido em 2026-08-20** e arquivado em `.superpowers/sdd/2026-08-20-galho-curriculo-plano/cassiana-cv.md` (fora do vault, diretório ignorado pelo git). 1.002 palavras.

**O achado que muda o valor da peça: é o currículo PRÉ-Dadosfera.** Não há entrada da empresa nele — este é o documento que *conseguiu* a vaga de trainee, não uma versão atualizada depois. Para o capstone isso é melhor que o previsto: é o artefato real no momento real da transição, e não uma reconstrução nem um retrato posterior.

**Estrutura do documento:** Sumário Executivo (8 bullets) · Experiência Profissional (4 entradas: doutorado 03/2020-atual, consultora acadêmica autônoma 08/2019-12/2023, professora assistente na UNIPAC 03-07/2020, mestrado 03/2016-11/2018) · Projetos Relevantes (2) · Formação (doutorado 2020-, mestrado 2016-2018, graduação em Engenharia Biomédica 2008-2015) · Informações Adicionais (7 bullets) · Qualificações e habilidades.

**Por que este caso ensina tanto — quatro lições, todas de um documento que FUNCIONOU:**

1. **A evidência transferível estava lá, mas enterrada.** Sete anos no laboratório NIATS/UFU, integração de sensores inerciais ao Arduino, coleta com limpeza e integração de dados de várias fontes, modelos de machine learning, análise estatística de dados de hospital público, liderança de equipe interdisciplinar. Tudo isso é trabalho de dados feito antes de ela se chamar profissional de dados. É o exemplo canônico da nota 10 (inventário de evidência): a porta de entrada determina o material, e material de pesquisa conta.
2. **A seção "Informações Adicionais" é o anti-padrão puro** — sete bullets de clichê sem evidência ("Entusiasmada em aplicar...", "Excelente habilidade em analisar...", "Capacidade de assimilar rapidamente..."). É exatamente o que as notas 07 e 09 ensinam a não fazer. E o valor didático é enorme justamente porque **o currículo funcionou mesmo assim**: mostra que o anti-padrão custa espaço e credibilidade sem necessariamente custar a vaga, o que é mais honesto do que o alarmismo habitual dos guias.
3. **O stack autodidata vive no fim do documento**, na última seção: Python, POO, Pandas/Numpy, Matplotlib/Seaborn, pipeline ETL/ELT, PowerBI, scikit-learn, Git/GitHub. A competência que motivou a contratação é a última coisa que o leitor encontra. Material direto para a nota 09 (posição e peso da seção de habilidades) e para a nota 03 (o que sobe e o que desce por nível).
4. **A cronologia tem sobreposições que assustam quem escreve currículo** e que aqui são legítimas: graduação de 2008 a 2015, mestrado 2016-2018, consultoria autônoma 2019-2023 rodando em paralelo com o doutorado desde 2020, e a docência de quatro meses em 2020. Material da nota 16 (lacunas, passagens curtas, paralelismos).

> [!danger] Dados pessoais que NÃO entram no vault público
> O documento traz telefone celular e e-mail pessoal dela. **Nenhum dos dois pode aparecer em nota alguma**, nem em exemplo, nem em captura de tela, nem em transcrição parcial. Ao reproduzir o cabeçalho no capstone, substituir por marcador genérico. Os únicos canais citáveis são os perfis públicos que ela mesma publica: LinkedIn e GitHub.

> [!question] A decidir com o usuário antes de escrever a Tarefa 28
> O currículo tem um bullet truncado — um item da seção do mestrado que ficou como uma letra solta, claramente um erro de edição que foi entregue. É um ótimo exemplo real do valor de revisar antes de enviar (nota 05), mas apontar publicamente o deslize de uma pessoa real, mesmo com autorização de citação, é escolha dela e não minha. **Perguntar antes:** ela topa que o erro seja mostrado como exemplo, ou o capstone corrige silenciosamente e a lição de revisão usa um caso fictício?

> [!important] Pré-condições para publicar o caso
> 1. ~~Cassiana lê e aprova a nota antes da publicação.~~ **Aprovado por ela em 2026-08-20**, conforme relato do usuário.
> 2. **O currículo dela**, que o usuário enviará, é a fonte para a peça do capstone. Nada de reconstrução aqui.
> 3. **Nenhum data broker como fonte.** RocketReach, ZoomInfo e similares raspam e revendem contato de pessoa física e estão excluídos, inclusive como citação. Fontes admitidas: LinkedIn, Dadosfera, UFU, DIO e as publicações.

## 7. Material de origem

### 7.1 Repositórios do usuário

| Origem | O que fornece |
| --- | --- |
| `josenaldo.github.io/content/blog/pt/como-escrever-o-seu-curriculo.md` | guia completo dos níveis de baixo; base pronta para as notas 5-9 e 16-17 |
| `josenaldo.github.io/content/experiences/` | 13 experiências públicas datadas, de 2003 a hoje — matéria-prima do capstone |
| `josenaldo.github.io/.github/skills/resume-experience-xyz/` | a fórmula XYZ já operacionalizada, com regras de "não inventar número" |
| `josenaldo.github.io/scripts/` (`brag.mjs`, `gen-metrics.mjs`, `check-metrics.mjs`) | o pipeline de métricas derivadas e a guarda de números aposentados |
| `curriculo/` | base × variante, `vaga.yaml`, `bin/build.sh`, três skills, e o histórico de lições |
| `curriculo/docs/superpowers/specs/2026-08-07-...` | as decisões de desenho e o que foi rejeitado |
| `codex-technomanticus-apocrypha` (privado) | princípios do GCA e Métricas Canônicas — **as lições entram, o conteúdo não é referenciado** |

### 7.2 Lições extraídas do histórico do repositório `curriculo`

Todas verificáveis em mensagem de commit, e todas viram conteúdo de nota:

- **A âncora governa o documento.** "I build delivery machines" abre o sumário e organiza tudo abaixo.
- **Negrito é recurso escasso.** De 106 para 26 trechos num único passe. Negrito demais é negrito nenhum.
- **Não inflar competência sem lastro.** Kubernetes removido da seção de skills por não haver experiência própria; o bullet que diz "partnered with DevOps to run a Kafka cluster on Kubernetes" permanece, porque descreve parceria e é factualmente correto.
- **Declarar lacuna na conversa, não no documento.** A seção que declarava lacunas de Go, GCP e Terraform foi removida: a transparência já tinha sido feita por e-mail e a recrutadora respondeu bem. Repetir no documento custava uma página.
- **Adaptação por vaga é cirúrgica.** A reescrita completa do currículo para uma vaga foi **revertida**; a variante voltou a ser idêntica à base exceto por um bullet.
- **O que se prova geral sobe para a base.** Ajustes feitos para uma vaga, quando se mostram gerais, viram padrão.
- **Verificar o dado difícil na fonte.** "Três codebases" virou "dez repositórios" depois de um levantamento — e o mesmo levantamento mostrou que contar diretórios ingenuamente inflaria o número em 90%.
- **Currículo enviado é imutável.** Corrigir um dado exige tocar N arquivos, e os já enviados permanecem com os números antigos. Isso é desenho, não descuido.
- **Guarda automatizada não pode falhar em silêncio.** A verificação de números aposentados aborta a geração; quando ela podia se desligar sozinha na falta de uma dependência, isso foi tratado como defeito.

### 7.3 Princípios do GCA aproveitáveis (genéricos, sem dado privado)

BLUF · a matriz de power verbs · "manager of one" · force multiplier · o drill-down da âncora em quatro camadas · task-taker vs. strategic asset · claim de esforço vs. claim de outcome · "Lista de Ingredientes" e "Alphabet Soup" · Extreme Ownership ("I", não "we") · a postura correta ao descrever uso de IA (arquiteto, não datilógrafo) · o pareado Brasil × padrão executivo global.

## 8. Pesquisa externa — achados e limites

Conduzida em 2026-08-20. **Ressalva metodológica que precisa aparecer no galho:** a maioria esmagadora do conteúdo público sobre currículo vem de empresas que vendem otimização de currículo e têm incentivo direto para inflar a importância do ATS.

### 8.1 Evidência sólida

- **Wilson, K. & Caliskan, A.**, "Gender, Race, and Intersectional Bias in Resume Screening via Language Model Retrieval", AAAI/ACM AIES 2024 — <https://arxiv.org/abs/2407.20371>. **Números conferidos no abstract da fonte primária em 2026-08-20**, e três deles corrigem o que a pesquisa inicial havia reportado: mais de 500 currículos públicos e mais de 500 descrições de vaga (não "550+ currículos"); nomes associados a brancos favorecidos em **85,1%** dos casos; nomes associados a **mulheres** favorecidos em apenas **11,1%** dos casos (o relatório de pesquisa dizia "nomes masculinos em 52%" — número inexistente no paper, descartado); e **homens negros desfavorecidos em até 100% dos casos**, formulação mais forte e mais precisa que "a categoria mais penalizada". A âncora acadêmica mais sólida do levantamento. Follow-up da UW em nov/2025 sugere que humanos expostos a rankings enviesados de IA absorvem o viés.
- **Duke / ASU / Berkeley / UNC / hireEZ**, "Measuring Real-World Prompt Injection Attacks in LLM-based Resume Screening", USENIX Security Symposium, ago/2026 — <https://pratt.duke.edu/news/thwarting-prompt-injection/>. 200.000 currículos reais submetidos à plataforma da parceira de pesquisa hireEZ; **pelo menos 1%** com instruções ocultas (o abstract diz "at least 1%" — é piso, não estimativa); incidência **sete vezes maior entre julho de 2024 e novembro de 2025**. Números conferidos na fonte em 2026-08-20. Os pesquisadores deliberadamente **não** testaram se as instruções influenciam decisões, por razões éticas.
- **Greenhouse**, "AI in Hiring Report" 2025: 41% dos candidatos dizem ter usado prompt injection; 1% dos currículos reais continham texto oculto. O gap entre autorrelato e comportamento é o achado.
- **Estudo ACL 2026**: prompt injection funciona **justamente enquanto poucos usam** — satura sozinho.

### 8.2 Mitos a derrubar nominalmente

| Mito | O que a evidência diz |
| --- | --- |
| "O ATS reprova automaticamente por score" | Só ~8% dos recrutadores configuram auto-rejeição por match score; o resto usa knockout questions e revisão humana. Fonte fraca, mas nenhuma fonte séria sustenta o contrário |
| "PDF quebra o ATS, use DOCX" | Falso como regra. O que quebra o parsing é a complexidade do documento — duas colunas (o parser lê atravessando as colunas), texto em imagem, contato em cabeçalho/rodapé, tabelas |
| "Texto branco escondido engana o ATS" | O extrator lê texto oculto normalmente; é tratado como desonestidade e, hoje, como risco de segurança (OWASP nº 1 para aplicações de IA em 2025) |
| "Existe um ATS score universal e confiável" | Scanners de terceiros usam métricas de marketing próprias, sem relação com o que o ATS real faz |
| "São 6 segundos, é regra" | Vem do estudo Ladders 2018: n=30, nunca publicado com revisão por pares, critérios de seleção não divulgados. O padrão de leitura em F sobrevive; o número exato, não |

### 8.3 Sem consenso — a declarar como tal

- **Carta de apresentação.** Uma fonte de 2025 (753 recrutadores) diz que 89% esperam e 83% leem; outra (ResumeBuilder, 2024, 948 líderes nos EUA) diz que só 26% leem regularmente e 44% pulam. Um estudo controlado com 7.287 candidaturas achou 53% mais callback com carta personalizada. Os números não batem e nenhuma fonte é claramente mais autoritativa. É o que justifica o broto 18a.
- **Regra de páginas por nível.** Consenso de mercado, sem estudo primário. Declarar como convenção, não como dado.

### 8.4 Caixa-preta declarada

**Não existe documentação oficial de engenharia do LinkedIn sobre o funcionamento do Recruiter Search.** Tudo que circula é inferência de terceiros comerciais. A nota 23 precisa dizer isso explicitamente em vez de repetir números de blog como se fossem fato. O mesmo vale para market share de ATS: nenhuma fonte com metodologia pública e neutra foi encontrada.

## 9. Convenções herdadas do vault

- **Padrão capítulo de livro** — cada nota lê como capítulo que pega o leitor pela mão, com exemplo trabalhado e divulgação progressiva; não como referência ou lista.
- **Notas profundas com diagramas** — faixa de ~440-540 linhas, com Mermaid onde o diagrama mostra mecanismo.
- **Sem quebra manual de linha** — parágrafo é uma linha só, por mais longa.
- **Três fases** no frontmatter (`fase: iniciado | adepto | magus`) e no agrupamento do MOC.
- **`roadmap.md`** por galho, pela convenção de rastreio recursivo.
- **Registro Feynman** no enriquecimento; callouts `[!question]` para tangentes e `[!warning]` para armadilhas, no formato *o que acontece / por quê / como evitar* já usado na nota 05.

## 10. Fora de escopo

- Corrigir a divergência de título do CEPEDI no site (registrada em 6.3, mas é trabalho no repositório do site).
- Revisar o post `como-escrever-o-seu-curriculo.md` do blog, que repete parte do folclore de ATS derrubado na seção 8.2. O usuário fará isso em **sessão separada, depois de o galho estar pronto**.
- Popular `cglima.github.io`, que ainda contém as 13 experiências do autor em vez das da titular. O usuário definiu em 2026-08-20 que o site dela vem **depois** de o site dele estar completo.
- Currículo acadêmico, Lattes e Europass em profundidade — mencionados na nota 24, sem trilha própria.
- Preparação para a entrevista em si — é `Carreira/Entrevistas/`.
- Negociação salarial — é o capstone de Entrevistas.

## 11. Riscos

| Risco | Mitigação |
| --- | --- |
| Vitrine degenerar em autopromoção e sufocar o ensino | Etiquetagem obrigatória; todo caso real precisa ensinar algo verificável, não só demonstrar competência |
| Citar terceiro real (Cassiana) num artefato público e permanente | **Aprovação dela obtida em 2026-08-20**; só fonte pública ou material que ela forneça; nenhum data broker |
| Reconstruir currículos antigos e a reconstrução ser lida como registro | Declaração explícita em cada peça reconstruída do capstone |
| Repetir folclore de ATS por inércia | A nota 04 é escrita primeiro e serve de gate para as demais |
| Vazar conteúdo do apocrypha para o repositório público | Só princípios genéricos entram; nenhum caminho, wikilink ou dado privado |
| 26 notas serem grandes demais para uma sessão | Execução em blocos, com `roadmap.md` como memória em disco |
| ~~Afirmar base legal de estágio/trainee sem verificar~~ | **Resolvido** — Lei 11.788/2008 verificada no Planalto em 2026-08-20 (ver 3.4) |
