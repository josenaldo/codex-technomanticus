---
title: "Galho Segurança Conceitual — design e plano (Fundamentos, Camada D)"
created: 2026-06-20
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - seguranca-conceitual
---

# Galho Segurança Conceitual — design e plano

## Contexto
SEGUNDO galho da Camada D (a última), depois de Camada A (7), C (Complexidade), **Camada B FECHADA (5/5)**
e do galho 13 (Organização de Computadores ✓). Galho 14 do roster: "Segurança Conceitual — criptografia,
hashing, autenticação/autorização (conceito)." Conteúdo NOVO (sem monólito-semente). Roster de **22 notas
(6/7/9)** aprovado pelo usuário em 2026-06-20 na opção **Capricho ED + Expandir**: o roster base de 19 notas
(5/7/7) foi expandido com 3 eixos canônicos — **Economia e fator humano** (Schneier, Iniciado), **Confiança
transitiva / "Trusting Trust"** (Thompson, Magus) e **Privacidade e anonimato** (Magus). Depois deste, só o
galho 15 (Compiladores e Linguagens) fecha a Camada D e o domínio Fundamentos inteiro.

Tese do galho: **segurança é uma propriedade emergente que você projeta, não um recurso que você instala.**
Onde os outros galhos de Fundamentos perguntam "como a máquina funciona", Segurança Conceitual pergunta
"o que acontece quando existe um adversário inteligente tentando quebrá-la". É o *mindset adversarial* + as
**primitivas criptográficas como ideias** (não receitas de biblioteca) + os **modelos de confiança e controle
de acesso**. O fio: criptografia não é o assunto, é uma ferramenta; o assunto é confiança sob adversário.

## Decisão de fronteira (rígido — linka, não duplica)
- **Matemática para Computação** (galho 11, existe) — dona da TEORIA DOS NÚMEROS (primos, fatoração, aritmética
  modular, Fermat-Euler) que sustenta RSA e Diffie-Hellman. Notas 08/09 deste galho LINKAM
  `[[03-Dominios/Fundamentos/Matemática para Computação/14 - Teoria dos números - divisibilidade e primos]]` e
  `[[03-Dominios/Fundamentos/Matemática para Computação/15 - Aritmética modular e Fermat-Euler]]` e usam o
  *aplicado* (a chave pública, o problema do log discreto como caixa-preta) — NUNCA reescrevem a matemática.
- **Redes e Protocolos** (galho existe) — dona do TLS/HTTPS como PROTOCOLO (handshake real, versões, cifras
  negociadas). Nota 14 deste galho é dona do TLS como CONCEITO (por que cripto híbrida + PKI + PFS se combinam),
  LINKA `[[03-Dominios/Fundamentos/Redes e Protocolos/05 - TLS e HTTPS]]`; nota 11 (PKI) também linka. Não
  reescreve o protocolo.
- **Organização de Computadores** (galho 13, existe) — dona de Spectre/Meltdown como MECANISMO DE HARDWARE
  (especulação, branch prediction). Nota 15 deste galho é dona do side-channel como CLASSE DE ATAQUE (timing,
  cache, o conceito de canal lateral), LINKA
  `[[03-Dominios/Fundamentos/Organização de Computadores/14 - Branch prediction e execução especulativa]]`.
- **Teoria da Computação** (galho 10, existe) — dona das classes de complexidade (P/NP/BQP). Nota 21
  (pós-quântica) menciona em PROSA que Shor coloca fatoração em BQP; linka opcional a
  `[[03-Dominios/Fundamentos/Teoria da Computação/16 - P vs NP e o mapa das classes]]` se couber natural.
- **Sistemas Operacionais** (galho 9, existe) — dono de permissões de processo/usuário, isolamento, sandbox
  como MECANISMO DO SO. Nota 13 (autorização) linka o *modelo* (DAC/MAC/RBAC); SO é dono da implementação.
- **Complexidade de Software** (galho 12, existe) — "Trusting Trust" toca confiança transitiva; a nota 17
  conversa com a ideia de complexidade da cadeia, mas é dona do ângulo de SEGURANÇA (confiança sob adversário).
- **Compiladores e Linguagens** (galho 15, Camada D, NÃO existe ainda) — "Trusting Trust" cita o compilador
  comprometido; mencionar em PROSA, SEM wikilink quebrado.
- **Infraestrutura / DevSecOps / appsec aplicado** — *operar* segurança (WAF, scanners, hardening de servidor,
  incident response) é prática, não fundamento. Fica de fora; este galho é a TEORIA.

## Assinatura ED deste galho (capricho)
Cada primitiva fecha com **a falha real** que ela previne ou que sua ausência causa: por que ECB vaza o pinguim
(modo de cifra), por que reusar nonce em GMAC/CTR quebra tudo, por que MD5 caiu (colisão → certificado forjado),
por que `==` em comparação de hash de senha vaza timing, por que "roll your own crypto" é o anti-padrão. O
**cluster cripto (07–10)** recebe tratamento ED: diagrama do fluxo cifra→decifra, `sequenceDiagram` do
Diffie-Hellman e do handshake TLS, tabela simétrico×assimétrico×híbrido. A **nota 17 (Trusting Trust)** recria
o argumento de Thompson passo a passo (compilador que se auto-infecta). O **capstone (22)** traz cheat-sheet
"ameaça → defesa → primitiva" e um threat-model worked-example de um sistema de login real.

## Roster de notas (22)

### Iniciado — o mindset e os fundamentos (6)
1. **O que é segurança conceitual** *(âncora)* — CIA (confidencialidade/integridade/disponibilidade) + AAA
   (autenticação/autorização/auditoria); o modelo adversarial (existe alguém inteligente contra você);
   superfície de ataque; segurança como propriedade emergente, não feature; o elo mais fraco.
2. **Pensar como adversário** — modelagem de ameaças; STRIDE; árvores de ataque; trust boundaries; o que é
   um *threat model* e como se faz um; "assume breach".
3. **Economia e fator humano da segurança** — Schneier: *segurança é um processo, não um produto*; custo do
   ataque × custo da defesa (não existe segurança absoluta, existe trade-off); engenharia social; o elo humano;
   *security theater*; por que o usuário contorna controle ruim.
4. **Princípios de design seguro** — Saltzer & Schroeder (os 8 princípios); least privilege; defense in depth;
   fail-safe defaults; complete mediation; economy of mechanism; separation of privilege; **Kerckhoffs** (o
   segredo está na chave, não no algoritmo); open design × security through obscurity.
5. **Aleatoriedade e segredos** — entropia; PRNG × CSPRNG; por que `Math.random()` não serve pra cripto; nonces,
   IVs, salts (o que cada um é e por que precisa ser único/imprevisível); a falha de Debian OpenSSL como caso.
6. **Hashing criptográfico** — propriedades (preimage, 2nd preimage, resistência a colisão); SHA-2/SHA-3;
   por que MD5 e SHA-1 morreram (colisões práticas); hash de senha ≠ hash cripto (bcrypt/scrypt/argon2,
   work factor); salt e pepper; rainbow tables.

### Adepto — criptografia e identidade (7)
7. **Criptografia simétrica** — cifras de bloco × fluxo; AES; modos de operação (por que ECB vaza, CBC, e
   AEAD/GCM); o problema da distribuição de chave (n² chaves); confidencialidade ≠ integridade.
8. **Criptografia assimétrica** — chave pública/privada; a ideia de função de mão única com alçapão; RSA e ECC
   (conceito, sem a aritmética — linka Matemática); por que é lenta → **cripto híbrida** (KEM); o que cada
   chave faz (cifrar vs assinar).
9. **Troca de chaves** — o problema: combinar segredo num canal público; **Diffie-Hellman** (passo a passo,
   sem MITM); forward secrecy (PFS); por que DH sozinho é vulnerável a MITM e precisa de autenticação (assinatura/PKI).
10. **MAC, HMAC e assinaturas digitais** — integridade e autenticidade da mensagem; MAC simétrico × assinatura
    assimétrica; HMAC; **não-repúdio** (só assinatura dá); encrypt-then-MAC × MAC-then-encrypt; a diferença
    entre "ninguém alterou" e "foi você quem mandou".
11. **PKI e certificados** — o problema da chave pública confiável; CA e cadeia de confiança; X.509; raiz de
    confiança (trust anchor); revogação (CRL, OCSP, OCSP stapling); web of trust × hierárquico; Let's Encrypt.
12. **Autenticação** — provar quem você é; os três fatores (algo que sabe/tem/é); MFA; senhas (e por que são
    ruins); tokens e magic links; **FIDO2/passkeys** (criptografia de chave pública contra phishing); ataques
    (phishing, credential stuffing, password spraying).
13. **Autorização e controle de acesso** — provar o que você pode fazer (≠ autenticação); modelos DAC/MAC/RBAC/ABAC;
    ACL × capability; **confused deputy**; least privilege aplicado; **OAuth2/OIDC** (delegação de acesso ≠
    autenticação — o erro clássico de usar OAuth pra login).

### Magus — sistemas, ataques e futuro (9)
14. **Criptografia em trânsito e em repouso** — juntando as peças: o handshake TLS conceitual (híbrido + PKI +
    PFS + AEAD numa coisa só); encryption at rest × in transit × in use; gerenciamento de quem tem a chave.
    *(fronteira c/ Redes — linka o protocolo)*.
15. **Ataques a sistemas cripto** — não se ataca a matemática, ataca-se a implementação; **side channels**
    (timing, cache, power); padding oracle; downgrade; replay; nonce reuse; length-extension; por que comparação
    de hash precisa ser constant-time; *"don't roll your own crypto"*. *(fronteira c/ Org — Spectre como mecanismo)*.
16. **Classes de vulnerabilidade** — a anatomia conceitual de uma falha; injection (SQL/command); XSS; memory
    safety (buffer overflow, use-after-free) e por que Rust importa; SSRF; o **OWASP Top 10** como mapa, não
    como checklist; a raiz comum (misturar dado com código/controle).
17. **Confiança transitiva e "Trusting Trust"** — Ken Thompson, *Reflections on Trusting Trust* (Turing Lecture):
    você não pode confiar em código que não escreveu — nem no compilador que o compilou; o compilador que se
    auto-infecta; confiança transitiva; supply-chain conceitual (dependências, SBOM como ideia, o ataque
    SolarWinds/xz como ilustração); a quem você delega confiança e por quê.
18. **Gestão de chaves e segredos** — o ciclo de vida da chave (geração, distribuição, rotação, revogação,
    destruição); KMS e HSM (conceito); secrets em código/CI/variáveis de ambiente (o anti-padrão); envelope
    encryption; "turtles all the way down" (a chave que protege a chave).
19. **Zero trust e defesa em profundidade** — o modelo de perímetro ("castelo e fosso") e por que falhou;
    **zero trust** (nunca confie, sempre verifique); BeyondCorp; defesa em profundidade na arquitetura; blast
    radius e contenção; microssegmentação (conceito).
20. **Privacidade, anonimato e metadados** — **privacidade ≠ segurança** (a confusão clássica); anonimato ×
    pseudonimato; o que metadados vazam (quem fala com quem, quando); Tor e mixnets (conceito); criptografia que
    preserva privacidade como teaser (zero-knowledge proofs, criptografia homomórfica, MPC); o modelo de ameaça
    da vigilância.
21. **Criptografia pós-quântica** — a ameaça quântica: **algoritmo de Shor** quebra RSA/ECC (fatoração e log
    discreto em BQP); Grover só enfraquece simétrico (dobre a chave); **harvest-now-decrypt-later**; PQC
    (lattices, NIST: Kyber/Dilithium); por que migrar agora mesmo sem computador quântico útil ainda.
22. **Capstone — segurança como engenheiro** — o threat-model worked-example de um sistema de login real;
    cheat-sheet "ameaça → defesa → primitiva"; os trade-offs (segurança × usabilidade × custo); onde cada
    conceito do galho entra; recap + inglês de entrevista.

## House style (espelhar galho 13 — Organização de Computadores)
- PT-BR, registro Feynman (analogias, perguntas retóricas, callouts). Banda **~380–540 ln/nota** (âncora e
  capstone podem ir a ~560).
- **4–6 diagramas Mermaid** por nota (NUNCA `xychart-beta`). `sequenceDiagram` pro Diffie-Hellman, handshake TLS,
  OAuth, assinatura/verificação; `flowchart` pra árvore de ataque, cadeia de confiança PKI, fluxo de cifra;
  `stateDiagram-v2` pro ciclo de vida de chave/sessão; `graph` pra taxonomias (CIA, fatores, modelos de acesso).
  Todo diagrama seguido de callout `> [!info] Leitura do diagrama`.
- Símbolos Unicode **LITERAIS** na prosa (≠, ≥, ⊕, →); entidades HTML só dentro de rótulos Mermaid entre aspas.
- Frontmatter idêntico ao template: `type: concept`, `fase: iniciado|adepto|magus`, `status: evergreen`,
  **`publish: false`** nas notas (só o index é `true`), tags `[fundamentos, seguranca-conceitual, <fase>, entrevista]`.
- Seções canônicas: `> [!abstract] TL;DR` no topo; corpo com `---` entre seções; `## Conexões` (anterior/próxima +
  cross-links); `> [!summary] Resumo em uma linha`; `## Em entrevista` (frases em inglês em itálico + tabela
  Vocabulário PT→EN); `> [!info] Lastro` ao final com fontes verificadas via WebSearch.
- Callouts variados: `tip`, `warning`, `success`, `example`, `danger` pra armadilhas de segurança.

## Plano de execução (subagent-driven, 1 subagente por nota)
1. **Scaffold** (este plano + index.md) → commit com paths explícitos.
2. **Fase Iniciado (01–06)** → 6 subagentes, 1 por nota, UMA Write cada, house style completo no prompt →
   conferir `wc -l` REAL → 2ª passada de enriquecimento nos floors → commit.
3. **Fase Adepto (07–13)** → idem, 7 notas → commit.
4. **Fase Magus (14–22)** → idem, 9 notas → commit.
5. **MOCs do domínio** (`03-Dominios/Fundamentos/index.md` + `Fundamentos.md`) apontam ao galho → commit.
6. Checks finais: NN-links resolvem, cross-galho verificados, zero link quebrado/relativo, zero xychart, zero
   entidade HTML na prosa, `[[...]]` literal só dentro de code fence. Atualizar memória.

## Lições do galho 13 (aplicar)
- Subagentes fazem UNDERSHOOT sistemático (~210–300 ln no 1º passe). **Front-load conteúdo senior no prompt**,
  conferir `wc -l` REAL (auto-relato infla), prever 2ª passada de enriquecimento pra atingir o floor.
- **Git hygiene (crítico):** NUNCA `git add <pasta>`; sempre paths EXPLÍCITOS + conferir
  `git diff --cached --name-only` antes de commitar — o working tree tem trabalho paralelo do usuário
  (renumeração da Anatomia dos LLMs). Commits direto na `main`, SEM push, SEM Co-Authored-By.
- NUNCA fabricar experiências/dados do usuário (galho teórico → exemplos canônicos: Debian OpenSSL, MD5/Flame,
  Heartbleed, SolarWinds/xz, KRACK — todos verificáveis e citados no Lastro).
- EVITAR `[[...]]` literal fora de code fence.
