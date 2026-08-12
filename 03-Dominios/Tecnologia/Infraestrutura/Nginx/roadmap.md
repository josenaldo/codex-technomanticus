---
title: "Roadmap — Nginx"
created: 2026-08-06
updated: 2026-08-09
type: meta
publish: false
tags:
  - meta
  - roadmap
  - infraestrutura
  - nginx
---

# Roadmap — Nginx (galho 3 de Infraestrutura)

Roadmap-folha do galho `Tecnologia/Infraestrutura/Nginx`. Terceiro galho do domínio, aberto em 2026-08-06. Design: [[00-Meta/specs/2026-08-02-dominio-infraestrutura-design|design do domínio]] · Plano: [[00-Meta/specs/2026-08-06-galho-nginx-plano|plano de execução]].

**Lente:** o ciclo de vida de uma request — a ordem de avaliação não é a ordem do arquivo.

**Baseline de versão:** mainline **1.31.3** (15 jul 2026) · stable **1.30.4**. Confirmado em `nginx.org` em 2026-08-06.

**Legenda:** ✅ escrita + M1 · 🔶 escrita, falta M1 · 📋 desenhada, não escrita.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 16 |
| 📋 desenhadas | 0 |
| 🔶 escritas (falta M1) | 12 |
| ✅ completas | 4 |
| % escrito | 100% |
| M1 (mídia) | 4/16 — em andamento |

## Notas

| # | Nota | Fase | Estado | Bloco |
|---|------|------|--------|-------|
| 01 | O problema que o Nginx resolve e o modelo de processos | Iniciado | ✅ | 1 |
| 02 | A estrutura da configuração — contextos e herança | Iniciado | 🔶 | 1 |
| 03 | Como o Nginx escolhe o server block | Iniciado | 🔶 | 1 |
| 04 | `location` e a tabela de precedência | Iniciado | 🔶 | 2 |
| 05 | O ciclo de vida de uma request | Iniciado | 🔶 | 2 |
| 06 | Servir arquivos estáticos | Adepto | ✅ | 3 |
| 07 | Proxy reverso | Adepto | ✅ | 3 |
| 08 | `upstream` e balanceamento | Adepto | 🔶 | 3 |
| 09 | TLS no Nginx | Adepto | 🔶 | 4 |
| 10 | Cache no Nginx | Adepto | 🔶 | 4 |
| 11 | Limitar e comprimir | Adepto | 🔶 | 4 |
| 12 | Variáveis, `map`, rewrite e logging | Magus | 🔶 | 5 |
| 13 | Tuning e diagnóstico | Magus | 🔶 | 5 |
| 14 | Nginx em container e como Ingress Controller | Magus | 🔶 | 5 |
| 15 | O ecossistema além do Nginx | Magus | ✅ | 6 |
| 16 | Capstone — a borda de uma aplicação | Magus | 🔶 | 6 |

## Fronteiras a respeitar

O levantamento de fronteira de 2026-08-06 encontrou a teoria inteira já escrita em `Ciência/Redes e Protocolos`. Isso **encolhe** as notas 08, 09 e 10 de propósito: elas são configuração, não protocolo.

| Vizinho | Fica lá | Fica aqui |
|---|---|---|
| `Redes 05` | handshake TLS, cadeia de confiança, SNI, mTLS, cipher suites | as diretivas `ssl_*` e a ordem do arquivo |
| `Redes 08` | `Cache-Control`, `ETag`, `Vary`, revalidação condicional | `proxy_cache_*`, zonas, chave, e quando o Nginx desobedece |
| `Redes 13` | L4 × L7, algoritmos de distribuição, sticky sessions, CDN | o bloco `upstream` e o que o OSS implementa de fato |
| `Operação 3-05` | Ingress, Gateway API, mesh, NetworkPolicy, a borda em produção | o arquivo de configuração do Nginx em si |
| `Kubernetes 15` | o objeto Ingress, `IngressClass`, `pathType`, annotations | o Nginx **dentro** do controlador e a tradução para `nginx.conf` |
| `Cloud 14` | API Gateway gerenciado, throttling e quotas na nuvem | — (nada aqui) |
| `Ciência/Concorrência 14` | loop de eventos como modelo de concorrência | o worker do Nginx como implementação disso |
| `Ciência/SO 10` | I/O, `epoll`, zero-copy no kernel | `sendfile` e `tcp_nopush` como diretiva |

## Material a consumir

| Fonte | Onde | Aproveitamento |
|---|---|---|
| `Infraestrutura/Nginx.md` | 1285 linhas | semente principal, densa em configuração real; vira tronco podado no bloco 7 |

> [!warning] Regra de conteúdo
> `Na prática (da minha experiência)` (linha 1129) e `How to explain in English` (linha 1197) do monólito são relato pessoal do autor e material de entrevista. Ficam no tronco podado e **não migram** para as notas.

## O que fica fora

> [!warning] `njs` e módulos Lua/OpenResty NÃO entram neste galho
> Escrever extensão para o Nginx — seja em `njs`, seja em Lua sobre OpenResty — é autoria de módulo, outro ofício, do mesmo jeito que escrever um operator ficou fora do galho de Kubernetes. A lente aqui é *a ferramenta por dentro, para quem vai operá-la*, e um tutorial de autoria duplicaria a documentação oficial sem acrescentar leitura própria. **Isto é decisão registrada, não esquecimento.** Se o assunto pedir depois, entra como broto (`12a`, `fase: Magus`), sem renumerar o galho.

- **M1 (mídia):** passada posterior, busca e verificação de ID centrais via `yt-dlp`.

## Pendências

- **Escrita:** 5/16. Bloco 1 (notas 01-03) em 2026-08-06 e Bloco 2 (notas 04-05) em 2026-08-08 concluídos — **fase Iniciado completa**. Blocos 3 (06-08) e 4 (09-11) em 2026-08-08 — **fase Adepto completa**. Blocos 5 (12-14) e 6 (15-16) em 2026-08-08 — **escrita 16/16 COMPLETA**. Falta o bloco 7 (poda, callouts de volta, estante).
- **Poda e callouts de volta** (`Operação 3-05`, `Kubernetes 15`): bloco 7 do plano.
- **M1 (mídia):** 4/16. Ver a seção abaixo.

## M1 — mídia embutida e descartes

Vídeos embutidos (todos verificados via `yt-dlp`; timestamp da âncora extraído do VTT, nunca estimado):

| Nota | Vídeo | ID | Canal | Âncora |
|---|---|---|---|---|
| 01 | NGINX Internal Architecture — Workers | `vVYM2QBk-iQ` | Hussein Nasser, 15 min | 5:42 |
| 06 | Path traversal via misconfigured NGINX alias | `IULL46LILrI` | The SecOps Group, 7 min | 3:50 |
| 06 | The surprising ways Nginx try_files actually works | `VPrBA2iZe1c` | Chris Fidao, 6 min | 3:15 |
| 07 | How Nginx and PHP-FPM turn a web request into code | `lh4RnczaATI` | Chris Fidao, 7 min | 1:04 |
| 15 | Dropbox migrates to Envoy from NginX | `ckraiZ_qa2o` | Hussein Nasser, 36 min | 11:15 |
| 02 | Learn Proper NGINX Configuration Context Logic | `C5kMgshNc6g` | NGINX (Jay Desai), 13 min | 9:34 |
| 08 | Load Balancing with NGINX | `a41jxGP9Ic8` | NGINX (Jay Desai), 30 min | 7:38 |
| 13 | The Powerful & Efficient NGINX Architecture (Lightboard) | `i-8AISuZtN8` | NGINX (Kevin Jones), 7 min | 4:44 |
| 14 | Using NGINX as a Kubernetes Ingress Controller | `AXZr2OC8Unc` | NGINX, 32 min | 30:12 |
| 16 | Load Balancer, Reverse Proxy e API Gateway (**PT-BR**) | `0frGo7vJV30` | Giuliana Bezerra, 17 min | — |

> [!warning] Descartes registrados — não repetir a busca sem ângulo novo
> **IDs inacessíveis** — a caracterização anterior ("links mortos vindos de busca alucinada") estava **errada**, e foi corrigida em 2026-08-09 depois de revalidar um a um. Os vídeos existem; o que varia é o motivo de não abrirem, e cada motivo pede uma conduta diferente:
>
> | ID | Motivo real | Conduta |
> |---|---|---|
> | `WC2-hNNBWII` · `QbmOyr0HwnM` · `BQY1l0rgDSQ` | **Exclusivo para membros** do canal (Hussein Nasser mantém parte do acervo atrás de assinatura) | Inacessível de fato — não insistir |
> | `9RAvTDTbuso` | Exige login | Inacessível sem conta |
> | `3q2xxMc7XEo` | Indisponível de verdade | Único caso de link morto |
>
> **A lição correta não é "a busca alucina IDs".** É que `yt-dlp` falha por motivos diferentes e a mensagem precisa ser lida: `Sign in to confirm you're not a bot` é **rate limit** (o vídeo existe e volta a funcionar depois), `Join this channel` é paywall, e só `This video is not available` é ausência real. Tratar rate limit como link morto descarta material bom por engano — **aconteceu**, com a palestra do Tim Hockin (`nWGkvrIPqJ4`), rejeitada por engano antes de ser revalidada.
>
> **Método melhor para achar ID:** `uvx yt-dlp "ytsearch5:<título>" --print "%(id)s|%(title)s|%(channel)s|%(duration)s|%(view_count)s"` devolve IDs reais direto do YouTube, em vez de IDs plausíveis vindos de busca web.
>
> **Reprovados por conteúdo:** `LM-3SWQiCNg` (Durgadas Kamath, 24 min) — tutorial iniciante de rewrite/`try_files`/log, e ele mesmo declara que não entra em logging avançado; a nota 12 é Magus e já cobre tudo, com mais profundidade. `siZ1t1w-iNY` (Very Academy) — é sobre master/worker e `worker_connections`, território da nota 01, e não toca nas 11 fases. `viAeG0Miwho` (Chris Fidao) — tour de `sites-available`/`sites-enabled` e `nginx -t`/`-T`, todo já coberto pela nota 02. `OM_N0jjghqI` (F5 DevCentral, 33 mil views) — autoridade alta, mas é de **2019**, anterior ao `networking.k8s.io/v1`; ensinaria API obsoleta na nota 14.
>
> **Reprovados por régua:** `0Q9I-x--np4` (285 s) · `_DdBJs6NfzI` (226 s) · `aYN9Y4_09o0` (94 s) · `LpkiX2ZJ3YI` (220 s) — todos abaixo do piso de 5 min. `psEHRwH5jYk` (440 views) · `_BCfoJoj-9g` (1.352) · `ODxw1QWpdEM` (133) · `dkElINJl_ZA` (93 s, 13 views) · `KZOaO_s5LXI` · `wYjhS42mbWM` — autoridade baixa demais.
>
> **Nota 07:** a primeira rodada de busca (proxy reverso genérico) não rendeu nada; o vídeo que entrou veio de um ângulo lateral (FastCGI como protocolo de gateway).
>
> **Notas 13 e 14: fechadas em 2026-08-09 (3ª rodada).** O que destravou foi mudar o ângulo de busca do *assunto da nota* para o *canal oficial da NGINX*, que tem material de conferência e de lightboard não indexado pelas consultas anteriores. Ambos os vídeos trazem **caducidade registrada no próprio callout**, o que aumenta o valor em vez de diminuir: o da 13 descreve `accept_mutex on` como padrão (mudou na 1.11.3), e o da 08 declara `least_time` e `sticky` como exclusivos do Plus (migraram na 1.31.0 e 1.29.6). São os mesmos achados que este galho levantou na doc oficial — o vídeo vira prova de que a literatura em circulação está atrasada.
>
> **3ª rodada — reprovados por conteúdo ou autoridade:** notas 03, 04, 05, 09, 10, 11, 12 e 16 seguem sem candidato. As consultas tentadas foram registradas para não repetir: `nginx location directive matching priority` (zero resultados), `nginx server_name virtual host matching`, `nginx request processing phases internals`, `nginx caching proxy_cache deep dive`, `nginx rate limiting limit_req leaky bucket`, `nginx rewrite map variables regex`, `nginx TLS SSL best practices`, `nginx production edge architecture`. O que aparece é (a) canal `Roel Van de Paar`, que publica leituras automatizadas de perguntas do StackOverflow — nunca usar; (b) `Dargslan`, série "Nginx Mastery", com 18-25 views por vídeo; (c) tutoriais de Let's Encrypt, que resolvem emissão de certificado e não configuração de TLS. **A hipótese do galho se confirma:** minúcia de configuração não tem vídeo bom em circulação, e o que existe é abaixo da régua.
>
> **Em aberto:** `hcw-NjOh8r0` (Hussein Nasser, crash course de 2 h) viola o teto de 60 min, mas é a fonte mais autoritativa disponível — decidir se entra com âncora muito precisa em alguma nota.

> [!question] Qual o piso aceitável de cobertura?
> O yield realista deste domínio parece ficar em torno de 50%, concentrado nas notas **conceituais** — minúcia de configuração (`location`, `proxy_pass`, `upstream`) simplesmente não tem vídeo bom em circulação.
>
> **Rodada PT-BR de 2026-08-12: +1 nota (16), galho vai a 9/16.** O ângulo em português foi finalmente testado nas 8 notas vazias e **confirmou a escassez** — as consultas para `server_name`, `location`, fases, cache, rate limit e rewrite em português devolveram zero resultado relevante ou vídeos de outro assunto. A única exceção foi o capstone, que não é sobre configuração e sim sobre **escolher o componente certo na borda** — e aí existe material bom em PT-BR. **A conclusão do galho fica mais forte, não mais fraca: a ausência é de material sobre minúcia de configuração do Nginx, em qualquer idioma.**

**Em 2026-08-09 a previsão se confirmou na mosca: o galho fechou em 8/16 = exatamente 50%.** As 8 notas cobertas são as conceituais (01, 02, 06, 07, 08, 13, 14, 15); as 8 sem vídeo são as de configuração fina e as duas de fronteira (03, 04, 05, 09, 10, 11, 12, 16). O ângulo que ainda não foi tentado é **PT-BR** e **conferências** (GOTO/InfoQ/NDC) — decisão do usuário se vale uma 4ª rodada ou se 50% encerra o M1 deste galho.

## Notas de execução

- Galho aberto em 2026-08-06, na sequência direta do fechamento do galho Kubernetes.
- **O que o levantamento mudou:** o esboço da spec de design previa ~10-12 notas. A teoria já coberta em `Ciência/Redes` encolheu três notas, mas o núcleo de configuração — contextos, precedência de `location`, fases de processamento, `root` × `alias`, a barra do `proxy_pass` — não existe em nenhum lugar do vault e pediu mais espaço. Fechou em 16.
- A ponte narrativa já existia: `Kubernetes/15` explica que o objeto Ingress precisa de um controlador, e que o controlador mais comum é um Nginx. O que aquele Nginx faz por dentro é este galho.
