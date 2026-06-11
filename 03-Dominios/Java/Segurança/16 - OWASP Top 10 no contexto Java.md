---
title: "OWASP Top 10 no contexto Java"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - seguranca
  - magus
  - owasp
aliases:
  - "OWASP Top 10"
  - "OWASP em Java"
---

# OWASP Top 10 no contexto Java

> [!abstract] TL;DR
> O **OWASP Top 10** é a lista de referência das categorias de risco em aplicações web — um documento de *conscientização*, não um checklist exaustivo. A boa notícia: este galho já cobriu as defesas concretas para a maioria das categorias. Esta nota é a **síntese**: ela mapeia, categoria por categoria, a defesa que o Spring Security oferece e aponta para a nota do galho que aprofunda cada uma. Pense nela como o índice reverso da trilha — você sai do *risco* e chega na *defesa*. A ideia central a carregar é **defense-in-depth**: nenhuma categoria do Top 10 é vencida por uma única camada; é a combinação de password encoding, autorização, headers, CSRF, validação e logging que sustenta a postura de segurança.

## O que é

O OWASP Top 10 é um documento mantido pela **Open Worldwide Application Security Project (OWASP)** que consolida as dez categorias de risco mais críticas para aplicações web. Cada edição agrupa famílias de vulnerabilidades sob um código (`A01`, `A02`, …) e um nome de categoria — por exemplo, *Broken Access Control* ou *Injection*.

O ponto que mais se entende errado: o Top 10 **não é um checklist exaustivo**. É um instrumento de *conscientização* — um ponto de partida para conversas, treinamento e priorização. Cumprir os dez itens não significa que a aplicação está segura; significa que os riscos mais comuns foram considerados. As edições mudam ao longo do tempo (categorias entram, saem, são renomeadas ou fundidas), justamente porque o cenário de ameaças muda. A edição mais recente é a **2025**, e é a numeração dela que esta nota adota.

Uma distinção que ajuda a usar o documento com maturidade: o Top 10 lista *categorias de risco*, não *vulnerabilidades específicas*. "Injection" não é um bug; é uma família que inclui SQL injection, command injection e correlatos. Essa granularidade de categoria é intencional — ela sobrevive à evolução das tecnologias. Um bug concreto de SQL injection num driver específico envelhece; a categoria "Injection" como classe de risco continua válida década após década. Por isso o mapeamento desta nota é por *defesa de categoria*: você aprende o padrão de proteção, não um patch pontual.

As categorias da edição 2025, na ordem oficial, são:

- A01 — Broken Access Control
- A02 — Security Misconfiguration
- A03 — Software Supply Chain Failures
- A04 — Cryptographic Failures
- A05 — Injection
- A06 — Insecure Design
- A07 — Authentication Failures
- A08 — Software or Data Integrity Failures
- A09 — Security Logging and Alerting Failures
- A10 — Mishandling of Exceptional Conditions

Vale notar duas mudanças de vocabulário em relação a edições anteriores, porque elas aparecem em material mais antigo e podem confundir. *Identification and Authentication Failures* aparece agora como **Authentication Failures** (A07). E o que antes vivia espalhado como "componentes vulneráveis e desatualizados" foi reenquadrado e ampliado como **Software Supply Chain Failures** (A03), refletindo que o risco não é só usar uma biblioteca vulnerável, mas toda a cadeia de build, dependências transitivas e artefatos. Se você decorou uma edição antiga, vale recalibrar pelos nomes e códigos da fonte oficial — categorias migram entre edições, e citar o código errado em entrevista entrega que o conhecimento é de segunda mão.

O caráter de *lista viva* é parte do design. O OWASP revisa o Top 10 periodicamente justamente para que ele continue refletindo o que realmente machuca aplicações em produção, e não um retrato congelado. Por isso a postura correta diante dele não é "memorizar os dez", e sim **entender a família de risco que cada categoria nomeia** — assim, quando a numeração mudar, você continua sabendo do que se trata.

## Por que importa

Para quem desenvolve em Java/Spring, o Top 10 é a linguagem comum que conecta o framework ao mundo de *application security*. Quando um relatório de auditoria ou uma issue de segurança chega rotulada como "A05 — Injection" ou "A01 — Broken Access Control", você precisa traduzir esse rótulo para uma ação concreta no código: qual filtro, qual anotação, qual configuração resolve. Esta nota é exatamente esse dicionário tradutor.

Importa também porque mostra **cobertura e lacuna**. Ao mapear o galho contra o Top 10, fica visível o que o Spring Security cobre por padrão (autenticação, autorização, CSRF, headers) e o que depende de disciplina fora do framework — validação de entrada, gestão de dependências, logging de segurança. Saber onde o framework *para* é o que separa quem configura de quem projeta.

Há ainda um ganho de **priorização**. Diante de tempo finito, o Top 10 dá uma ordem de conversa: antes de investir em defesas exóticas, garanta que as famílias de risco mais reincidentes estão cobertas. Para um time Java, isso quase sempre significa começar por acesso (A01) e configuração (A02) — as duas categorias onde uma única rota esquecida ou um default mal entendido abre a porta inteira. O framework não fecha essas portas sozinho; ele dá as fechaduras, e cabe a você instalá-las em cada uma.

E importa em entrevista: "How do you map OWASP categories to your Spring stack?" é uma pergunta de arquitetura, não de decoreba. Responder pela *defesa concreta* — e não recitar a lista — demonstra maturidade de segurança. O entrevistador raramente quer ouvir os dez nomes; quer ver você *conectar* uma categoria a um mecanismo do framework e admitir, com honestidade, onde o framework para e a disciplina de time começa.

## Como funciona

O mapeamento abaixo é **conceitual**: cada categoria de risco aponta para a defesa que a neutraliza no stack Spring, com link para a nota do galho que aprofunda o mecanismo. Não há aqui ranking de incidência nem peso quantitativo — só a correspondência risco → defesa.

### Broken Access Control → method security e autorização

`A01 — Broken Access Control` cobre tudo o que permite a um usuário acessar recurso ou ação além do que sua permissão autoriza: endpoints sem proteção, *insecure direct object references* (acessar `/pedido/42` que pertence a outro usuário), elevação de privilégio.

A defesa em Spring Security é em duas frentes. Na borda HTTP, a autorização por URL (`authorizeHttpRequests`) trava quais papéis alcançam quais rotas — coberta na nota [[03-Dominios/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|05 — Autorização por URL]]. No nível do método, `@PreAuthorize`/`@PostAuthorize` com SpEL aplicam regra fina, inclusive sobre o objeto retornado — coberta em [[03-Dominios/Java/Segurança/07 - Method security — @PreAuthorize, @PostAuthorize e SpEL|07 — Method security]]. Quando a decisão depende do *dono do recurso* ou de *atributos* (o caso clássico de IDOR), entra o `AuthorizationManager` custom, detalhado em [[03-Dominios/Java/Segurança/14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC|14 — Autorização avançada]]. A regra de ouro: **negar por padrão** e autorizar explicitamente.

O detalhe que separa esta categoria das outras é que ela é *contextual*: não existe uma config global que a resolva de uma vez. Cada nova rota e cada novo método é uma oportunidade de deixar uma brecha. A autorização por URL protege o *caminho*; a method security protege a *operação*; o `AuthorizationManager` custom protege o *dado específico*. As três camadas existem porque o controle de acesso correto raramente cabe num só nível — uma rota pode estar protegida e ainda assim retornar um objeto que não é do usuário, se a verificação de propriedade ficar de fora.

### Cryptographic Failures → BCrypt, HTTPS e JWT assinado

`A04 — Cryptographic Failures` reúne falhas de proteção de dados em trânsito e em repouso: senhas guardadas em texto puro ou com hash fraco, ausência de TLS, segredos hardcoded, tokens não assinados.

No galho, três notas cobrem o essencial. Senhas nunca são guardadas em claro: o `DelegatingPasswordEncoder` aplica hash adaptativo (BCrypt, Argon2) com salt por senha, em [[03-Dominios/Java/Segurança/04 - Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder|04 — Password encoding]]. Tokens que carregam identidade precisam de **integridade**, e isso vem da assinatura: a estrutura e validação de assinatura de JWT estão em [[03-Dominios/Java/Segurança/08 - JWT — estrutura, assinatura e validação|08 — JWT]], com a validação do lado da API em [[03-Dominios/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|09 — OAuth2 Resource Server]]. HTTPS em si é configuração de transporte (terminação TLS no proxy/servidor), mas o Spring ajuda a *forçá-lo* via header `Strict-Transport-Security` (HSTS), tratado em [[03-Dominios/Java/Segurança/15 - Session management e security headers|15 — Headers de segurança]].

Vale separar dois conceitos que esta categoria mistura: **confidencialidade** (ninguém não autorizado *lê* o dado) e **integridade** (ninguém não autorizado *altera* o dado sem ser detectado). O hash de senha protege confidencialidade — mesmo vazando o banco, a senha original não sai do hash. A assinatura do JWT protege integridade — qualquer adulteração do payload invalida a assinatura e o token é rejeitado. São defesas criptográficas distintas para problemas distintos, e confundi-las leva a erros do tipo "achei que o token estava seguro porque estava em Base64" — Base64 é codificação, não criptografia, e não protege nada.

### Injection → JPA params e Bean Validation

`A05 — Injection` cobre SQL injection, command injection e correlatos — sempre que entrada não confiável é interpretada como código ou comando. A categoria absorve também a maioria dos casos historicamente rotulados como XSS.

A defesa de SQL injection **não mora neste galho** — mora na camada de persistência. O ponto-chave: queries parametrizadas (binding de parâmetros do JPA/JPQL, `Prepared​Statement`) tratam a entrada como *dado*, nunca como SQL, e isso é assunto do **Galho 10 — Persistência**. O que o Spring Security agrega aqui é a **validação de entrada** na borda: Bean Validation (`@Valid`, `@NotNull`, `@Pattern`) rejeita payloads malformados antes que cheguem à lógica, reduzindo a superfície. A regra que vale para todo tipo de injection é a mesma — **nunca concatene entrada do usuário em uma string interpretável**; sempre use binding/escaping da camada apropriada.

Um cuidado de raciocínio: Bean Validation **não substitui** o parameter binding do JPA. Validar que um campo é um e-mail bem-formado não impede injection se, mais adiante, esse valor for concatenado numa query construída à mão. A validação reduz superfície e melhora a higiene da entrada; a defesa *definitiva* contra SQL injection é estrutural — está em como a query é montada, não em quão limpo é o input. As duas camadas se somam: a borda filtra o grosseiro, e a persistência parametrizada garante que nenhuma entrada vire código. Pela mesma lógica, dados de saída renderizados em HTML pedem *escaping* na camada de view, fechando o flanco que historicamente se chamava XSS.

### Security Misconfiguration → CSRF, CORS e headers

`A02 — Security Misconfiguration` é a categoria mais ampla e, em geral, a mais comum de errar: defaults inseguros deixados como estão, recursos expostos sem necessidade, headers de segurança ausentes, mensagens de erro vazando *stack trace*.

O Spring Security responde com **defaults seguros** que você precisa entender antes de mexer. CSRF vem **ligado por padrão** para fluxos baseados em sessão — desligar sem entender é a misconfiguration clássica, tratada em [[03-Dominios/Java/Segurança/10 - CSRF — por que ligado por default e quando desligar|10 — CSRF]]. CORS precisa de configuração explícita e restritiva (origens permitidas, não `*` cego), coberta em [[03-Dominios/Java/Segurança/11 - CORS — a borda, o preflight e a config de segurança|11 — CORS]]. E os *security headers* (HSTS, `X-Content-Type-Options`, `Content-Security-Policy`, controle de cache) endurecem o comportamento do browser — detalhados em [[03-Dominios/Java/Segurança/15 - Session management e security headers|15 — Session e headers]].

O paradoxo desta categoria é que o Spring Security tem bons defaults — e ainda assim Misconfiguration é uma das famílias mais reincidentes. A razão é que *desligar* uma proteção costuma ser uma linha curta e conveniente (`.csrf(csrf -> csrf.disable())`, `allowedOrigins("*")`), copiada de um tutorial sem o contexto. O default seguro só protege enquanto você não o sobrescreve por engano. A disciplina certa é tratar cada relaxamento de default como uma decisão consciente, justificada e — idealmente — comentada no código, para que o próximo desenvolvedor entenda *por que* a proteção foi afrouxada e em que condições ela poderia voltar.

### Identification & Auth Failures → password encoding, session, refresh tokens

`A07 — Authentication Failures` cobre falhas de identificação e autenticação: senhas fracas aceitas, ausência de proteção contra força bruta, gestão frágil de sessão, tokens que não expiram nem revogam.

O galho cobre a espinha dorsal. O armazenamento seguro de senha (BCrypt/Argon2) está em [[03-Dominios/Java/Segurança/04 - Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder|04 — Password encoding]]. A gestão de sessão — fixation protection, sessão concorrente, invalidação — está em [[03-Dominios/Java/Segurança/15 - Session management e security headers|15 — Session management]]. E em arquiteturas stateless, o ciclo de vida do token (expiração curta do access token, rotação e revogação via refresh token) está em [[03-Dominios/Java/Segurança/13 - Refresh tokens e revogação de token|13 — Refresh tokens]]. O que o framework *não* faz sozinho: bloqueio por tentativas, detecção de credenciais vazadas e MFA exigem componente ou integração adicional — o framework dá o esqueleto, não a política completa.

Aqui aparece de novo o tema da nota: autenticação é um *processo*, não um único portão. Há o momento de provar identidade (login), há o de manter a identidade (sessão ou token) e há o de encerrá-la (logout, expiração, revogação). Cada um desses momentos tem sua própria falha característica — senha fraca no login, fixation na sessão, token que nunca expira no encerramento. A defesa robusta endereça os três, e é por isso que o galho dedicou notas separadas a password, session e refresh token: são fases distintas do mesmo ciclo de vida de identidade.

### Software & Data Integrity → assinatura e origem confiável

`A08 — Software or Data Integrity Failures` cobre o risco de confiar em dados ou código cuja integridade não foi verificada: um update aplicado sem checar assinatura, um objeto desserializado de fonte não confiável, um pipeline que puxa artefato adulterado.

No recorte deste galho, a face mais visível dessa categoria é a **integridade do token**. Um JWT só vale porque a assinatura prova que o payload não foi adulterado entre quem emitiu e quem recebe — e a validação dessa assinatura é exatamente o que as notas [[03-Dominios/Java/Segurança/08 - JWT — estrutura, assinatura e validação|08 — JWT]] e [[03-Dominios/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|09 — OAuth2 Resource Server]] tratam. Aceitar um token sem verificar a assinatura (ou aceitar o algoritmo `none`) é o caso de manual desta categoria. A face que escapa do framework — verificar a integridade de dependências e artefatos de build — pertence à mesma família de A03, e é disciplina de pipeline.

### Defense-in-depth: nenhuma camada é suficiente sozinha

A lição que costura o mapeamento todo é **defense-in-depth**: as camadas se sobrepõem porque cada uma falha de um jeito diferente. Autenticação forte não protege contra um endpoint sem autorização. Autorização perfeita não protege contra injection. Validação de entrada não protege contra um token sem assinatura. CSRF ligado não protege contra CORS frouxo.

O Top 10 deixa isso explícito ao tratar categorias *independentes* — vencer A01 não te dá nada em A04. Por isso a postura de segurança de uma API production-grade não é "escolher a melhor defesa", e sim **empilhar defesas** de modo que a falha de uma seja contida pela próxima. Essa visão integrada é o assunto do capstone do galho: [[03-Dominios/Java/Segurança/18 - Capstone — projetando a segurança de uma API Spring production-grade|18 — Capstone de segurança]].

Na prática, defense-in-depth muda *como você projeta*. Em vez de perguntar "esta defesa é boa o suficiente?", você pergunta "se esta defesa falhar, o que segura o ataque depois dela?". Um token vazado deveria ser contido pela expiração curta. Uma rota esquecida deveria ser contida pelo deny-by-default. Uma entrada maliciosa que passou pela validação deveria ser contida pela query parametrizada. Cada camada assume que a anterior pode falhar — e é essa premissa pessimista, não o otimismo de uma única defesa perfeita, que sustenta sistemas em produção.

## Na prática

A tabela abaixo é o índice reverso do galho: do risco OWASP (edição 2025) para a defesa no Spring Security e a nota que aprofunda. Categorias que dependem de disciplina fora do framework estão marcadas como tal.

| Categoria OWASP (2025)                       | Defesa no Spring Security                                          | Nota do galho                |
| -------------------------------------------- | ----------------------------------------------------------------- | ---------------------------- |
| A01 — Broken Access Control                  | `authorizeHttpRequests`, method security, `AuthorizationManager`  | 05, 07, 14                   |
| A02 — Security Misconfiguration              | CSRF on-by-default, CORS restritivo, security headers, HSTS       | 10, 11, 15                   |
| A03 — Software Supply Chain Failures         | Gestão de dependências (fora do framework) — versões pinadas, SCA | — (disciplina de build)      |
| A04 — Cryptographic Failures                 | Password encoding (BCrypt/Argon2), JWT assinado, HSTS             | 04, 08, 09, 15               |
| A05 — Injection                              | Bean Validation na borda; queries parametrizadas no JPA           | borda: galho; SQL: Galho 10  |
| A06 — Insecure Design                        | Threat modeling, deny-by-default, modelagem de autorização        | 14, 18 (design)              |
| A07 — Authentication Failures                | `UserDetailsService`, password encoding, session, refresh tokens  | 03, 04, 13, 15               |
| A08 — Software or Data Integrity Failures    | Assinatura de token, dependências de origem confiável             | 08, 09 (integridade de token)|
| A09 — Security Logging and Alerting Failures | Logging de eventos de autenticação/autorização e alertas          | — (observabilidade)          |
| A10 — Mishandling of Exceptional Conditions  | Tratamento de erro sem vazar stack trace; `AccessDeniedHandler`   | 15 (postura de erro)         |

A leitura honesta da tabela: o galho cobre com profundidade os riscos de **acesso, criptografia de senha/token, configuração e autenticação**. Já **supply chain (A03)**, **logging/alerting (A09)** e parte de **insecure design (A06)** vivem *fora* do Spring Security — são disciplina de build, observabilidade e arquitetura. O framework é uma camada, não a fortaleza inteira.

Como ler a coluna "Nota do galho": os números remetem às notas atômicas deste galho de Segurança. Onde a célula traz um travessão ou aponta para fora, é sinal de que a defesa principal não é responsabilidade do Spring Security — e isso é informação, não lacuna. Mapear honestamente o que o framework *não* faz é metade do valor desta síntese; a outra metade é saber para onde ir quando ele para.

Onde o framework não chega, vale saber o nome da defesa para não soar ingênuo numa entrevista. **A03 (Supply Chain)** se endereça com gestão de dependências: versões pinadas, *software composition analysis* (SCA) varrendo o classpath por bibliotecas com CVE conhecido, e artefatos de origem verificável. **A09 (Logging e Alerting)** se endereça com observabilidade: emitir eventos de segurança estruturados, centralizar logs e disparar alerta em padrões anômalos. **A06 (Insecure Design)** se endereça *antes* de codar, com threat modeling e a decisão de modelo de autorização — assunto que a nota [[03-Dominios/Java/Segurança/14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC|14 — Autorização avançada]] toca e que o capstone amarra. **A10 (Mishandling of Exceptional Conditions)** lembra que erro mal tratado também é vetor: stack trace vazado em resposta é informação para o atacante, então a postura de erro (incluindo `AccessDeniedHandler` e *exception handling* genérico) faz parte da segurança, não só da experiência. Nenhum desses itens é "magia do framework" — são decisões de time e de pipeline.

## Armadilhas

### (1) "Se a autenticação está perfeita, basta"

A crença de que uma camada de login impecável fecha o problema. Ela não fecha `A09 — Security Logging and Alerting Failures`: sem registrar e *alertar* sobre tentativas de login falhas, força bruta e anomalias, o ataque acontece em silêncio — você só descobre depois do vazamento. Autenticação forte impede *algumas* portas; logging é o que te avisa que alguém está testando as fechaduras.

**Fix:** trate logging e alerting de segurança como requisito, não como afterthought. Registre eventos de autenticação e autorização (sucesso *e* falha), correlacione tentativas e configure alerta para padrões anômalos. A camada de defesa que falta nunca é "mais auth" — é visibilidade.

### (2) "CORS protege o servidor"

A confusão mais comum sobre CORS: achar que ele é uma defesa do servidor contra requisições maliciosas. Não é. CORS é uma política aplicada **pelo browser** — ele decide se o JavaScript de uma origem pode *ler* a resposta de outra. Um cliente que não é browser (curl, um script, um atacante) ignora CORS completamente. Configurar CORS nunca substitui autenticação nem autorização.

**Fix:** trate CORS como o que ele é — controle de compartilhamento entre origens *no browser*, coberto em [[03-Dominios/Java/Segurança/11 - CORS — a borda, o preflight e a config de segurança|11 — CORS]]. A autenticação e a autorização do endpoint são **obrigatórias de qualquer forma**, com ou sem CORS. CORS frouxo é misconfiguration; CORS rígido não é segurança de backend.

### (3) "O framework cobre tudo automaticamente"

A ilusão de que adicionar Spring Security ao classpath resolve segurança por mágica. Os defaults ajudam — mas a esmagadora maioria dos bugs de segurança em apps Spring é de **configuração**, não de framework quebrado: uma rota que escapou do `authorizeHttpRequests`, um CSRF desligado por engano, um CORS com `*`, um endpoint de actuator exposto. O framework é uma ferramenta poderosa e mal configurada com a mesma facilidade.

**Fix:** não confie no default cego — **teste cada endpoint**. Escreva testes de autorização (`@WithMockUser`, MockMvc) que provam que rota protegida nega acesso anônimo e que papel errado recebe 403. A postura integrada e testada é o tema de [[03-Dominios/Java/Segurança/18 - Capstone — projetando a segurança de uma API Spring production-grade|18 — Capstone de segurança]]. Segurança é propriedade que se *verifica*, não que se *assume*.

## Em entrevista

### Frase pronta (inglês)

> "I use the OWASP Top 10 as a shared vocabulary, not as a checklist — it maps risk categories to concrete defenses in my Spring stack. Broken Access Control I handle with `authorizeHttpRequests` plus method security and custom `AuthorizationManager`s for ownership checks; Cryptographic Failures with BCrypt password hashing and signed JWTs; Injection with parameterized JPA queries and Bean Validation at the edge; and Misconfiguration with CSRF on by default, restrictive CORS, and security headers. The principle underneath all of it is defense-in-depth: no single layer is enough, so I stack them and verify each endpoint with authorization tests rather than trusting framework defaults."

### Vocabulário

| Termo (inglês)          | Significado                                                              |
| ----------------------- | ----------------------------------------------------------------------- |
| Broken Access Control   | Acesso além da permissão (IDOR, endpoint exposto, elevação de privilégio)|
| Defense-in-depth        | Empilhar camadas independentes de defesa, sem ponto único de falha       |
| Deny by default         | Negar acesso por padrão e autorizar apenas o explicitamente permitido    |
| Injection               | Entrada não confiável interpretada como código/comando (SQL, etc.)       |
| Parameterized query     | Query com binding de parâmetros — entrada tratada como dado, não SQL      |
| Security misconfiguration| Defaults inseguros, recursos expostos, headers ausentes                  |
| Awareness document      | Documento de conscientização (o que o Top 10 é), não checklist exaustivo  |

## Veja também

- [[03-Dominios/Java/Segurança/04 - Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder|Password encoding]]
- [[03-Dominios/Java/Segurança/10 - CSRF — por que ligado por default e quando desligar|CSRF]]
- [[03-Dominios/Java/Segurança/14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC|Autorização avançada]]
- [[03-Dominios/Java/Segurança/18 - Capstone — projetando a segurança de uma API Spring production-grade|Capstone de segurança]]
- [[03-Dominios/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]]

## Referências

- OWASP Top 10 (projeto oficial): https://owasp.org/www-project-top-ten/
- OWASP Top 10:2025: https://owasp.org/Top10/2025/
- OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
