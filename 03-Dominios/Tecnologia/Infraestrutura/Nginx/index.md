---
title: "Nginx"
created: 2026-08-06
updated: 2026-08-06
type: moc
status: growing
publish: true
tags:
  - moc
  - infraestrutura
  - nginx
  - proxy-reverso
aliases:
  - "Nginx (galho)"
  - "Galho Nginx"
---

# Nginx

> [!abstract] TL;DR
> Terceiro galho do domínio [[03-Dominios/Tecnologia/Infraestrutura/index|Infraestrutura]], sob a lente **o ciclo de vida de uma request**: a ordem em que o Nginx avalia a configuração **não é a ordem em que ela está escrita no arquivo**. Um `location` não é escolhido de cima para baixo, uma diretiva de `rewrite` não roda no mesmo momento que uma de `access`, e uma configuração que "não faz efeito" quase sempre está na fase errada — não errada em si. Quem segue a request pelas fases prevê o comportamento; quem lê o arquivo de cima para baixo tenta e erra. O galho sobe do modelo de processos e da estrutura da configuração até o proxy, a borda e o diagnóstico. 16 notas, 3 fases.

## Sobre este galho

Os dois galhos anteriores fecharam empurrando o assunto para cá. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/15 - Ingress e a borda do cluster|Ingress e a borda do cluster]] explica que o objeto Ingress não faz nada sozinho — quem faz é um **controlador**, e o controlador mais comum do mundo é um Nginx com um processo ao lado reescrevendo `nginx.conf`. O que aquele Nginx faz por dentro nunca foi explicado, ali nem em lugar nenhum do vault. Este galho é essa lacuna preenchida.

O recorte não é receita de configuração. Existe documentação oficial excelente para isso, e ela envelhece melhor do que qualquer nota. O recorte é o **modelo de avaliação** — o que permite ler uma configuração alheia e prever o que ela faz, que é o que separa quem copia bloco do Stack Overflow de quem debuga um 502 às três da manhã.

**Audiência primária:** quem já tem um Nginx na frente de alguma coisa e o trata como caixa-preta configurada por herança cultural. **Audiência secundária:** quem vai precisar explicar, num loop sênior, por onde passa uma request entre o cliente e a aplicação.

> [!info] Fronteira — o sanduíche de quatro camadas
> | Camada | Casa | Pergunta que responde |
> |---|---|---|
> | Mecanismo | [[03-Dominios/Ciência/Redes e Protocolos/index\|Ciência/Redes e Protocolos]] | como TLS, cache HTTP e balanceamento funcionam |
> | **A ferramenta** | **este galho** | **como o Nginx avalia e serve uma request** |
> | O ofício | [[03-Dominios/Engenharia/Operação/index\|Engenharia/Operação]] | o que muda quando a borda é produção |
> | A plataforma | [[03-Dominios/Tecnologia/Cloud/14 - API Gateway e edge de aplicação/01 - Por que um API Gateway\|Cloud, galho 14]] | quando o provedor opera a borda por você |

> [!warning] A teoria não está neste galho — e isso é deliberado
> **TLS** (handshake, cadeia de confiança, SNI, mTLS) está em [[03-Dominios/Ciência/Redes e Protocolos/05 - TLS e HTTPS|TLS e HTTPS]]. **A semântica de cache HTTP** (`Cache-Control`, `ETag`, `Vary`, revalidação) está em [[03-Dominios/Ciência/Redes e Protocolos/08 - Caching HTTP|Caching HTTP]]. **Os algoritmos de balanceamento e a camada L4 × L7** estão em [[03-Dominios/Ciência/Redes e Protocolos/13 - Load balancing e CDN|Load balancing e CDN]]. Aqui ficam só as diretivas — o arquivo, não o protocolo. E na outra direção: **o objeto Ingress e a Gateway API** ficam em [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/15 - Ingress e a borda do cluster|Kubernetes 15]], e **operar a borda em produção** fica em [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/05 - Rede e borda em produção|Rede e borda em produção]].

## Iniciado — o modelo e a configuração

1. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/01 - O problema que o Nginx resolve|01 — O problema que o Nginx resolve e o modelo de processos]] — o C10K, por que thread-por-conexão bate no teto, e a divisão de trabalho entre o master e os workers.
2. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/02 - A estrutura da configuração|02 — A estrutura da configuração: contextos e herança]] — os contextos aninhados e a regra que confunde todo mundo: diretiva herdada é **substituída**, não fundida.
3. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/03 - Como o Nginx escolhe o server block|03 — Como o Nginx escolhe o `server` block]] — `listen`, `server_name` e a precedência real; o `default_server` e o que acontece com um `Host` desconhecido.
4. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/04 - location e a tabela de precedência|04 — `location` e a tabela de precedência]] — os cinco modificadores e a ordem de avaliação que não é a ordem do arquivo.
5. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/05 - O ciclo de vida de uma request|05 — O ciclo de vida de uma request]] — **a nota que carrega a lente**: as fases de processamento e por que uma diretiva na fase errada simplesmente não faz efeito.

## Adepto — servir, fazer proxy e proteger

6. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/06 - Servir arquivos estáticos|06 — Servir arquivos estáticos]] — `root` × `alias` e a armadilha da barra, `try_files` e o fallback de SPA, o caminho zero-copy do `sendfile`.
7. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/07 - Proxy reverso|07 — Proxy reverso]] — a barra final do `proxy_pass` que reescreve o path, os `X-Forwarded-*`, buffers, timeouts e o upgrade de WebSocket.
8. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/08 - upstream e balanceamento|08 — `upstream` e balanceamento]] — o pool de backends, o `keepalive` que exige HTTP/1.1, e o health check passivo que o OSS entrega de verdade.
9. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/09 - TLS no Nginx|09 — TLS no Nginx]] — a cadeia no arquivo e a ordem que importa, sessão e tickets, OCSP stapling, HTTP/2 e HTTP/3.
10. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/10 - Cache no Nginx|10 — Cache no Nginx]] — zonas e chave de cache, o vazamento entre usuários que a chave default causa, e como o Nginx desobedece o backend.
11. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/11 - Limitar e comprimir|11 — Limitar e comprimir]] — o balde furado do `limit_req` (`burst` e `nodelay` de verdade), `limit_conn`, gzip e o 413 que ninguém entende.

## Magus — o que sustenta

12. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/12 - Variáveis, map, rewrite e logging|12 — Variáveis, `map`, rewrite e logging]] — a tabela de decisão do `map`, `rewrite` × `return`, log em JSON e o `request_id` propagado.
13. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/13 - Tuning e diagnóstico|13 — Tuning e diagnóstico]] — a mecânica do reload gracioso, o teto de descritores, e o catálogo 502 × 504 × 413 × 499.
14. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/14 - Nginx em container e como Ingress Controller|14 — Nginx em container e como Ingress Controller]] — a imagem oficial, config por bind mount, e como o controlador traduz Ingress em `nginx.conf`.
15. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/15 - O ecossistema além do Nginx|15 — O ecossistema além do Nginx]] — Caddy, Traefik, HAProxy e Envoy; onde o Nginx deixou de ser a resposta automática.
16. [[03-Dominios/Tecnologia/Infraestrutura/Nginx/16 - Capstone - a borda de uma aplicação|16 — Capstone: a borda de uma aplicação]] — caso trabalhado, da app nua até uma borda defensável, cada decisão citando a nota que a fundamenta.

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Infraestrutura/Nginx" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Infraestrutura/index|Infraestrutura]] — MOC do domínio
- [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/index|Kubernetes]] — o galho anterior; o Ingress cujo controlador é um Nginx
- [[03-Dominios/Tecnologia/Infraestrutura/Docker/index|Docker]] — o primeiro galho; a imagem que este galho põe atrás de uma borda
- [[Nginx]] — o monólito de referência que originou este galho
