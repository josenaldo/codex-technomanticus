---
title: "Roadmap — Nginx"
created: 2026-08-06
updated: 2026-08-06
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
| 📋 desenhadas | 13 |
| 🔶 escritas | 3 |
| ✅ completas | 0 |
| % escrito | 19% |
| M1 (mídia) | passada posterior |

## Notas

| # | Nota | Fase | Estado | Bloco |
|---|------|------|--------|-------|
| 01 | O problema que o Nginx resolve e o modelo de processos | Iniciado | 🔶 | 1 |
| 02 | A estrutura da configuração — contextos e herança | Iniciado | 🔶 | 1 |
| 03 | Como o Nginx escolhe o server block | Iniciado | 🔶 | 1 |
| 04 | `location` e a tabela de precedência | Iniciado | 📋 | 2 |
| 05 | O ciclo de vida de uma request | Iniciado | 📋 | 2 |
| 06 | Servir arquivos estáticos | Adepto | 📋 | 3 |
| 07 | Proxy reverso | Adepto | 📋 | 3 |
| 08 | `upstream` e balanceamento | Adepto | 📋 | 3 |
| 09 | TLS no Nginx | Adepto | 📋 | 4 |
| 10 | Cache no Nginx | Adepto | 📋 | 4 |
| 11 | Limitar e comprimir | Adepto | 📋 | 4 |
| 12 | Variáveis, `map`, rewrite e logging | Magus | 📋 | 5 |
| 13 | Tuning e diagnóstico | Magus | 📋 | 5 |
| 14 | Nginx em container e como Ingress Controller | Magus | 📋 | 5 |
| 15 | O ecossistema além do Nginx | Magus | 📋 | 6 |
| 16 | Capstone — a borda de uma aplicação | Magus | 📋 | 6 |

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

- **Escrita:** 3/16. Bloco 1 concluído em 2026-08-06 (notas 01-03). Blocos 2-6 pendentes.
- **Poda e callouts de volta** (`Operação 3-05`, `Kubernetes 15`): bloco 7 do plano.
- **M1 (mídia):** passada posterior.

## Notas de execução

- Galho aberto em 2026-08-06, na sequência direta do fechamento do galho Kubernetes.
- **O que o levantamento mudou:** o esboço da spec de design previa ~10-12 notas. A teoria já coberta em `Ciência/Redes` encolheu três notas, mas o núcleo de configuração — contextos, precedência de `location`, fases de processamento, `root` × `alias`, a barra do `proxy_pass` — não existe em nenhum lugar do vault e pediu mais espaço. Fechou em 16.
- A ponte narrativa já existia: `Kubernetes/15` explica que o objeto Ingress precisa de um controlador, e que o controlador mais comum é um Nginx. O que aquele Nginx faz por dentro é este galho.
