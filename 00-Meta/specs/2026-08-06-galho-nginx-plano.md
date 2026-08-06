---
title: "Plano de execução — Galho 3: Nginx"
created: 2026-08-06
updated: 2026-08-06
type: spec
publish: false
tags:
  - meta
  - spec
  - plano
  - infraestrutura
  - nginx
---

# Plano de execução — Galho 3: Nginx

> **Para quem executa:** cada bloco é uma unidade fechada com gate próprio. Escrita via subagente Sonnet (teto de 3 por bloco); gate estrutural por script. Fonte do desenho: [[00-Meta/specs/2026-08-02-dominio-infraestrutura-design|design do domínio]]. Precedentes de execução: [[00-Meta/specs/2026-08-02-galho-docker-plano|plano do galho Docker]] e [[00-Meta/specs/2026-08-03-galho-kubernetes-plano|plano do galho Kubernetes]].

**Objetivo:** escrever as 16 notas do galho `Tecnologia/Infraestrutura/Nginx`, em 3 fases, sob a lente *o ciclo de vida de uma request*, e podar o monólito `Nginx.md` ao final.

**Arquitetura:** galho-folha com `index.md` (MOC por fase) + `roadmap.md` + 16 notas `01..16`. Semente: `Nginx.md` (1285 linhas, denso em configuração real).

## O que o levantamento de fronteira mudou (2026-08-06)

O esboço da spec de design previa ~10-12 notas. O levantamento confirmou o achado central e ajustou o dimensionamento em duas direções opostas.

**A teoria toda já existe, em `Ciência/Redes e Protocolos` — e isso *encolhe* várias notas:**

- `Redes 05 (TLS e HTTPS)` cobre handshake 1.3, cadeia de confiança, revogação, cipher suites, forward secrecy, mTLS, SNI e onde o TLS termina. A nota 09 daqui é **só a configuração no Nginx**, não a criptografia.
- `Redes 08 (Caching HTTP)` cobre `Cache-Control`, `max-age` × `s-maxage`, revalidação condicional, `ETag`, `Vary`, `stale-while-revalidate` e invalidação. A nota 10 daqui é **só o cache de proxy do Nginx** — zonas, chave, e quando o Nginx desobedece o backend.
- `Redes 13 (Load balancing e CDN)` cobre L4 × L7, algoritmos de distribuição, health checks, sticky sessions e CDN. A nota 08 daqui é **só o bloco `upstream`** e o que o Nginx OSS implementa de fato.

**O ofício e o objeto Kubernetes já existem — e isso crava duas fronteiras duras:**

- `Operação 3-05 (Rede e borda em produção)` cobre Ingress, Gateway API, TLS termination na borda, rate limiting na borda, service mesh, NetworkPolicy e egress. É *a borda em produção*; aqui é *o arquivo de configuração*.
- `Kubernetes/15 (Ingress e a borda do cluster)` tem 447 linhas sobre o objeto Ingress, `IngressClass`, `pathType`, annotations e Gateway API. A nota 14 daqui aborda o **Nginx como processo dentro do controlador** e a tradução Ingress → `nginx.conf`, e **não** reexplica o objeto.
- `Cloud 14-01 (Por que um API Gateway)` cobre o gateway gerenciado e a comparação com LB e CDN. Fora de escopo aqui.

**Buraco real encontrado — e é o galho inteiro.** Nenhuma nota do vault explica o modelo master/worker, contextos e herança de diretivas, a tabela de precedência do `location`, o que a barra final do `proxy_pass` faz, as fases de processamento de uma request, ou `root` × `alias`. `Operação 3-05` usa Nginx como Ingress sem ensinar uma linha de configuração — exatamente o pressuposto que a spec de design mandou preencher.

**Ajuste de escala:** 16 notas em vez de 10-12. As notas de TLS/cache/balanceamento ficam mais finas (a teoria mora em Redes), mas o núcleo de configuração — que não existe em lugar nenhum — pede mais espaço do que o esboço previa, e o ecossistema de alternativas ganha nota própria, no mesmo movimento de `Docker/16`.

## Restrições globais

- **Lente:** *o ciclo de vida de uma request*. A ordem de avaliação não é a ordem do arquivo — seguir a request pelas fases explica 90% dos bugs de Nginx. Toda nota deve poder ser lida como corolário disso, do mesmo jeito que no galho Docker tudo caía de "a imagem é imutável e em camadas" e no Kubernetes de "o controller converge estado".
- **Escala:** padrão capítulo de livro, 440-540 linhas.
- **Fase:** `Iniciado` (01-05), `Adepto` (06-11), `Magus` (12-16).
- **Núcleo por nota:** TL;DR `[!abstract]` · abertura por problema (nunca "X é...") · corpo-mecanismo · `## Armadilhas comuns` com ≥3 `[!warning]` · `## Como explicar em inglês` com tabela PT↔EN ≥5 linhas · `## O que vem a seguir` (ponte para a próxima nota) · `## Fontes` com URLs clicáveis.
- **Diagramas:** Mermaid onde estrutural, `<br/>` para quebra de linha — **nunca** `\n`. `quadrantChart` proibido.
- **Blocos de configuração completos e comentados** onde o assunto pede — é o material que o leitor vai copiar e adaptar. Equivalente ao YAML no galho Kubernetes.
- **Baseline de versão:** **mainline 1.31.3 (15 jul 2026) · stable 1.30.4** — confirmado em `nginx.org` em 2026-08-06. Toda nota que crava comportamento de versão leva `[!info]` com a baseline declarada.
- **Nada inventado:** proibido fabricar experiência do autor. As seções `Na prática (da minha experiência)` e `How to explain in English` do monólito ficam no tronco podado.
- **Sem quebra manual de linha.**

## Regras de prompt de subagente (herdadas do galho 2, aplicadas desde o bloco 1)

Estas cinco existem porque cada uma custou uma passada de correção no galho anterior. Entram em **todo** prompt, desde o primeiro bloco.

1. **`<br/>` em Mermaid, nunca `\n`.**
2. **Verificar cada URL de `## Fontes`** com WebFetch/curl antes de escrever — o bloco sem essa regra produziu dois 404.
3. **Proibido narrar o próprio processo** de escrita ou verificação dentro da nota.
4. **Confirme na fonte ou omita — nunca escreva "não consegui confirmar".**
5. **Lista branca de wikilinks no prompt**, e validação por script depois, mesmo assim.

> [!warning] A lição mais cara do galho 2
> **O hedge cauteloso do subagente vira afirmação FALSA.** Duas vezes o agente não confirmou um fato e escreveu a negativa em vez de omitir — e numa delas a nota chegou a recomendar migrar para um modo que estava sendo depreciado. **Toda dúvida que o agente declarar no relatório final tem de ser conferida na fonte antes do commit.**

---

## Bloco 0 — Esqueleto

- [ ] Criar `Nginx/index.md` (MOC por fase, TL;DR com a lente, callout do sanduíche de quatro camadas, tabela de fronteira).
- [ ] Criar `Nginx/roadmap.md` (16 linhas, todas `📋`).
- [ ] Commit: `feat(infra): abre galho Nginx — index e roadmap`.

## Bloco 1 — Iniciado, o modelo e a configuração (01-03) · parada de revisão ao fim

- [ ] **01 — O problema que o Nginx resolve e o modelo de processos.** O C10K e por que thread-por-conexão não escala; master e workers; o worker como laço de eventos não-bloqueante; o que o master faz que o worker não faz (ler config, abrir socket, `root`). Pontes: `Ciência/Concorrência 14` (loop de eventos) e `Ciência/SO 10` (I/O). Abre com o problema, não com "Nginx é um servidor web".
- [ ] **02 — A estrutura da configuração: contextos e herança.** `main`, `events`, `http`, `server`, `location`, `upstream`; herança de diretiva **por substituição, não por merge** — a raiz de metade da confusão; `include` e organização em múltiplos arquivos; o que só pode aparecer em cada contexto.
- [ ] **03 — Como o Nginx escolhe o `server` block.** `listen` e a especificidade do endereço; `server_name` e a ordem de precedência (exato, curinga à esquerda, curinga à direita, regex); `default_server` e o que acontece com um `Host` que não casa; o papel do SNI quando é HTTPS.
- [ ] Gate + rastreio + commit + **parada de revisão**.

## Bloco 2 — Iniciado, o coração da lente (04-05)

- [ ] **04 — `location` e a tabela de precedência.** Os modificadores (`=`, `^~`, `~`, `~*`, prefixo puro) e a ordem real de avaliação, que **não** é a ordem do arquivo; `location` aninhado; a diferença entre o mais longo prefixo e o primeiro regex que casa. Tabela de precedência e diagrama de decisão.
- [ ] **05 — O ciclo de vida de uma request.** **A nota que carrega a lente do galho.** As fases de processamento e o que roda em cada uma; onde `rewrite`, `access`, `try_files` e o handler de conteúdo atuam; por que uma diretiva "não faz efeito" quando está na fase errada. Diagrama do fluxo completo, da aceitação do socket ao log.
- [ ] Gate + rastreio + commit.

## Bloco 3 — Adepto, servir e fazer proxy (06-08)

- [ ] **06 — Servir arquivos estáticos.** `root` × `alias` e a armadilha da barra final; `try_files` e o fallback de SPA; `index`; `sendfile`, `tcp_nopush` e o caminho zero-copy. Amarra com `Ciência/SO 10`.
- [ ] **07 — Proxy reverso.** `proxy_pass` **com e sem URI — a barra final que reescreve o path**; `Host` e os `X-Forwarded-*`; `proxy_set_header` e a herança que zera os headers do contexto de cima; buffers e o disco que enche; timeouts; upgrade de WebSocket e o caso gRPC.
- [ ] **08 — `upstream` e balanceamento.** O bloco `upstream`; o que o Nginx OSS implementa de fato; `keepalive` para o upstream e por que ele exige `proxy_http_version 1.1`; health check **passivo** no OSS × ativo no Plus; `zone` e estado compartilhado entre workers. Teoria de algoritmos fica em `Redes 13`.
- [ ] Gate + rastreio + commit.

## Bloco 4 — Adepto, a borda (09-11) · parada de revisão ao fim

- [ ] **09 — TLS no Nginx.** A cadeia no arquivo e a ordem que importa; `ssl_protocols` e `ssl_ciphers`; sessão e tickets; OCSP stapling; HTTP/2 e o estado do HTTP/3; o redirect de HTTP para HTTPS feito certo. **Teoria fica em `Redes 05`** — aqui é o arquivo.
- [ ] **10 — Cache no Nginx.** `proxy_cache_path` e as zonas; a chave de cache e por que a default causa vazamento entre usuários; `proxy_cache_use_stale`; o que o Nginx faz quando o backend manda `Cache-Control` — e como ele desobedece. **Semântica HTTP fica em `Redes 08`.**
- [ ] **11 — Limitar e comprimir.** `limit_req` e o algoritmo de balde furado (`burst` e `nodelay` explicados de verdade); `limit_conn`; `gzip` e o custo de CPU, e onde entra Brotli; `client_max_body_size` e o 413 que ninguém entende.
- [ ] Gate + rastreio + commit + **parada de revisão**.

## Bloco 5 — Magus, o que sustenta (12-14)

- [ ] **12 — Variáveis, `map`, rewrite e logging.** Variáveis built-in e o que elas custam; `map` como tabela de decisão; `rewrite` × `return` e o loop de rewrite; `log_format` em JSON; `request_id` propagado até o backend. Fronteira: observabilidade como ofício fica em `Operação`.
- [ ] **13 — Tuning e diagnóstico.** `nginx -t` antes de todo reload; a **mecânica do reload gracioso** — como o master troca workers sem derrubar conexão; níveis de `error_log` e o que cada um revela; `stub_status`; `worker_connections` e o teto de descritores; o catálogo de erros (502 × 504 × 413 × 499) e o que cada um diz sobre onde o problema está.
- [ ] **14 — Nginx em container e como Ingress Controller.** A imagem oficial e o que ela faz no `entrypoint`; config por bind mount × imagem própria; multi-stage servindo SPA; e o Nginx **dentro** do ingress-nginx — como o controlador traduz objeto Ingress em `nginx.conf` e recarrega. **Fronteira dura:** o objeto Ingress fica em `Kubernetes/15`, a borda em produção fica em `Operação 3-05`.
- [ ] Gate + rastreio + commit.

## Bloco 6 — Magus, o ecossistema e o capstone (15-16)

- [ ] **15 — O ecossistema além do Nginx.** Onde Nginx deixou de ser a única resposta: Caddy (TLS automático), Traefik (descoberta dinâmica), HAProxy (L4/L7 de alto desempenho), Envoy (a base do mesh e da Gateway API). O que mudou depois da aquisição pela F5 e o que existe de fork/derivado — **cada afirmação verificada na fonte ou omitida**. Espelha `Docker/16`.
- [ ] **16 — Capstone.** Caso trabalhado, não resumo. Pega a app empacotada nos capstones anteriores e põe uma borda na frente dela, decidindo em voz alta: como o `server` é escolhido, onde cada `location` cai, o que é estático e o que é proxy, onde o TLS termina, o que se cacheia, o que se limita, como se diagnostica quando dá 502. Cada decisão cita a nota que a fundamenta. Fecha nomeando o que fica em `Operação` e em `Kubernetes`.
- [ ] Gate + commit.

## Bloco 7 — Fechamento

- [ ] Podar `Nginx.md` (1285 linhas) para tronco com tabela de redirecionamento, preservando **literalmente** `Na prática (da minha experiência)` (linha 1129) e `How to explain in English` (linha 1197).
- [ ] Callouts de volta em `Operação 3-05` e `Kubernetes/15`.
- [ ] Atualizar `Infraestrutura/index.md`, `Infraestrutura/roadmap.md` e o Roadmap central.
- [ ] Gate de wikilinks em toda a pasta.
- [ ] Commit e pergunta ao usuário sobre o galho 4 (Linux) × a passada de M1.

## O que fica fora

- **M1 (mídia):** passada posterior, busca e verificação de ID **centrais via `yt-dlp`**, nunca delegadas a subagente.
- **Teoria de TLS, cache HTTP e algoritmos de balanceamento:** ficam em `Ciência/Redes e Protocolos` 05, 08 e 13. Aqui só a configuração.
- **O objeto Ingress e a Gateway API:** ficam em `Kubernetes/15` e `Operação 3-05`.
- **`njs` e módulos Lua/OpenResty:** fora do escopo — é autoria de extensão, outro ofício, como o broto de operator foi no galho 2. Se pedir, vira broto depois.

## Gate estrutural

O script do galho 2 vivia no scratchpad da sessão e se perdeu. **Reescrever no bloco 0.** Checa: contagem de linhas · seções obrigatórias · ≥3 `[!warning]` · tabela EN · ausência de `quadrantChart` · `\n` dentro de Mermaid · quebra manual de linha (dá falso positivo no frontmatter — ignorar) · wikilinks resolvidos. **Não rodar em `index.md`/`roadmap.md`** — são MOC/meta e reprovam por não terem estrutura de nota.

## Governança de custo

Sonnet para escrita, teto de 3 subagentes por bloco, gate por script antes de cada commit. O galho Docker custou ~1,2M tokens de subagente para 18 notas; o Kubernetes, 22 notas na mesma ordem de grandeza. Este tem 16 e deve custar menos.
