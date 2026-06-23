---
title: "Segurança Conceitual"
created: 2026-06-20
updated: 2026-06-20
type: moc
status: growing
publish: true
tags:
  - fundamentos
  - seguranca-conceitual
  - entrevista
  - moc
aliases:
  - Segurança Conceitual
  - Segurança da Informação
  - Conceitos de Segurança
  - Criptografia (conceito)
  - Galho - Segurança Conceitual
---

# Segurança Conceitual

> [!abstract] TL;DR
> Segurança não é um recurso que você instala — é uma **propriedade emergente que você projeta** sob a hipótese
> de que existe um adversário inteligente tentando quebrar o seu sistema. Este galho é o *mindset adversarial*
> (modelar ameaças, pensar como atacante), as **primitivas criptográficas como ideias** (hash, cifra simétrica e
> assimétrica, troca de chaves, assinatura, PKI) e os **modelos de confiança e controle de acesso** (autenticação
> ≠ autorização, zero trust, "Trusting Trust"). O fio condutor: criptografia não é o assunto — é uma ferramenta;
> o assunto é **confiança sob adversário**. Por que MD5 morreu, por que reusar nonce quebra tudo, por que não se
> deve "rolar a própria cripto", e por que o elo mais fraco quase sempre é humano.

## Sobre este galho
Onde os outros galhos de Fundamentos perguntam *como a máquina funciona*, Segurança Conceitual pergunta *o que
acontece quando alguém inteligente tenta quebrá-la de propósito*. É a teoria atemporal — os conceitos que
sobrevivem à próxima biblioteca e ao próximo CVE: o triângulo CIA, os princípios de Saltzer & Schroeder, a ideia
de chave pública, a cadeia de confiança. Não é appsec aplicado (hardening, WAF, scanners) nem operação de
segurança — é o andar conceitual que torna tudo isso inteligível.

**Fronteiras (linka, não duplica):**
- **A matemática do RSA/Diffie-Hellman** (teoria dos números, aritmética modular) → [[03-Dominios/Ciência/Matemática para Computação/index|Matemática para Computação]]. Aqui é o **uso aplicado**: a chave pública como caixa-preta, o problema difícil como alicerce.
- **TLS/HTTPS como protocolo** (handshake real, versões, cifras) → [[03-Dominios/Ciência/Redes e Protocolos/05 - TLS e HTTPS|Redes e Protocolos]]. Aqui é o **conceito**: por que cripto híbrida + PKI + forward secrecy se combinam.
- **Spectre/Meltdown como mecanismo de hardware** (especulação) → [[03-Dominios/Ciência/Organização de Computadores/14 - Branch prediction e execução especulativa|Organização de Computadores]]. Aqui é o **side-channel como classe de ataque**.
- **Permissões de SO, isolamento, sandbox** → [[03-Dominios/Ciência/Sistemas Operacionais/index|Sistemas Operacionais]] (a implementação). Aqui é o **modelo** de controle de acesso (DAC/MAC/RBAC/ABAC).
- **Operar segurança** (WAF, scanners, incident response, hardening) → prática/Infraestrutura, fora deste galho. Aqui é a **teoria**.

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção "Em entrevista" com
frases prontas em inglês e vocabulário técnico PT→EN. (Autenticação × autorização, hashing de senha, simétrico ×
assimétrico e "o que é um threat model" caem com frequência real; o resto é a cultura que separa quem *usa* uma
biblioteca de quem *entende* por que ela existe.)

## Iniciado — o mindset e os fundamentos
1. [[01 - O que é segurança conceitual]] — CIA + AAA, o modelo adversarial, superfície de ataque, o elo mais fraco.
2. [[02 - Pensar como adversário]] — modelagem de ameaças, STRIDE, árvores de ataque, trust boundaries, "assume breach".
3. [[03 - Economia e fator humano da segurança]] — Schneier (processo ≠ produto), custo ataque × defesa, engenharia social, security theater.
4. [[04 - Princípios de design seguro]] — Saltzer & Schroeder, least privilege, defense in depth, fail-safe, Kerckhoffs.
5. [[05 - Aleatoriedade e segredos]] — entropia, PRNG × CSPRNG, nonces/IVs/salts, por que aleatoriedade ruim quebra cripto.
6. [[06 - Hashing criptográfico]] — preimage/colisão, SHA-2/3, MD5/SHA-1 mortos, hash de senha (bcrypt/argon2), salt.

## Adepto — criptografia e identidade
7. [[07 - Criptografia simétrica]] — bloco × fluxo, AES, modos (ECB ruim → AEAD/GCM), o problema da chave compartilhada.
8. [[08 - Criptografia assimétrica]] — chave pública/privada, RSA/ECC (conceito), por que é lenta → cripto híbrida.
9. [[09 - Troca de chaves]] — Diffie-Hellman, forward secrecy, MITM e a necessidade de autenticar.
10. [[10 - MAC, HMAC e assinaturas digitais]] — integridade, autenticidade, não-repúdio, encrypt-then-MAC.
11. [[11 - PKI e certificados]] — CA, cadeia de confiança, X.509, raiz de confiança, revogação (CRL/OCSP).
12. [[12 - Autenticação]] — fatores, MFA, senhas, tokens, FIDO2/passkeys, phishing/credential stuffing.
13. [[13 - Autorização e controle de acesso]] — DAC/MAC/RBAC/ABAC, ACL × capability, confused deputy, OAuth2/OIDC (delegação ≠ login).

## Magus — sistemas, ataques e futuro
14. [[14 - Criptografia em trânsito e em repouso]] — handshake TLS conceitual (híbrido + PKI + PFS + AEAD), at rest × in transit.
15. [[15 - Ataques a sistemas cripto]] — side channels, padding oracle, downgrade, replay, nonce reuse; "don't roll your own crypto".
16. [[16 - Classes de vulnerabilidade]] — injection, XSS, memory safety, confused deputy; OWASP como mapa, não checklist.
17. [[17 - Confiança transitiva e Trusting Trust]] — Thompson (Turing Lecture), o compilador que se auto-infecta, supply-chain conceitual.
18. [[18 - Gestão de chaves e segredos]] — lifecycle, rotação, KMS/HSM, secrets em código/CI, "turtles all the way down".
19. [[19 - Zero trust e defesa em profundidade]] — perímetro × zero trust, BeyondCorp, camadas, blast radius.
20. [[20 - Privacidade, anonimato e metadados]] — privacidade ≠ segurança, anonimato × pseudonimato, Tor/mixnets, ZK como teaser.
21. [[21 - Criptografia pós-quântica]] — ameaça de Shor, harvest-now-decrypt-later, PQC/lattices, por que migrar já.
22. [[22 - Capstone - segurança como engenheiro]] — threat-model worked-example, cheat-sheet ameaça → defesa → primitiva; inglês; recap.

## Rotas alternativas

### O essencial (o que mais cai em entrevista)
01 → 06 → 12 → 13. CIA, hashing de senha, autenticação × autorização — o quarteto que separa quem entende de quem decora.

### A trilha da criptografia (do hash ao TLS)
06 → 07 → 08 → 09 → 10 → 11 → 14. Hash, simétrico, assimétrico, troca de chaves, assinatura, PKI e como tudo vira o handshake TLS.

### O mindset adversarial (pensar como atacante)
02 → 04 → 15 → 16 → 17. Modelar ameaças, projetar com princípios, e ver como sistemas reais quebram.

### Identidade e acesso (o cluster de produto)
12 → 13 → 19 + [[03-Dominios/Ciência/Redes e Protocolos/05 - TLS e HTTPS|TLS na prática]]. Autenticação, autorização e zero trust.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Engenharia/Segurança"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Ciência/index|Fundamentos (MOC do domínio)]]
- [[03-Dominios/Ciência/Matemática para Computação/index|Matemática para Computação]] — a teoria dos números que sustenta RSA e Diffie-Hellman
- [[03-Dominios/Ciência/Redes e Protocolos/05 - TLS e HTTPS|TLS e HTTPS]] — a criptografia conceitual virada protocolo de rede
- [[03-Dominios/Ciência/Organização de Computadores/14 - Branch prediction e execução especulativa|Branch prediction e especulação]] — Spectre como mecanismo de hardware por trás dos side channels
- [[Dicionário de Fundamentos]]
