---
title: "Roadmap — Docker"
created: 2026-08-02
updated: 2026-08-09
type: meta
publish: false
tags:
  - meta
  - roadmap
  - infraestrutura
  - docker
---

# Roadmap — Docker (galho 1 de Infraestrutura)

Roadmap-folha do galho `Tecnologia/Infraestrutura/Docker`. Primeiro galho do domínio, aberto em 2026-08-02. Design: [[00-Meta/specs/2026-08-02-dominio-infraestrutura-design|design do domínio]] · Plano: [[00-Meta/specs/2026-08-02-galho-docker-plano|plano de execução]].

**Lente:** a imagem como artefato — tudo é consequência de a imagem ser imutável e em camadas.

**Legenda:** ✅ escrita + M1 · 🔶 escrita, falta M1 · 📋 desenhada, não escrita · ⬜ não iniciada.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 18 |
| 📋 desenhadas | 0 |
| 🔶 escritas | 18 |
| ✅ completas | 0 |
| % escrito | **100% (18/18)** ✅ |
| M1 (mídia) | passada posterior, após a escrita |

## Notas

| # | Nota | Fase | Estado | Bloco do plano |
|---|------|------|--------|----------------|
| 01 | O problema que o container resolve | Iniciado | 🔶 | 1 |
| 02 | A anatomia de uma imagem | Iniciado | 🔶 | 1 |
| 03 | O ciclo de vida de um container | Iniciado | 🔶 | 1 |
| 04 | O Dockerfile como receita de camadas | Iniciado | 🔶 | 1 |
| 05 | Build e cache — por que seu build está lento | Iniciado | 🔶 | 2 |
| 06 | Dados que sobrevivem ao container | Iniciado | 🔶 | 2 |
| 07 | Rede no Docker | Iniciado | 🔶 | 2 |
| 08 | ENTRYPOINT, CMD e o container que não morre direito | Adepto | 🔶 | 3 |
| 09 | Multi-stage e imagens mínimas | Adepto | 🔶 | 3 |
| 10 | BuildKit por dentro | Adepto | 🔶 | 3 |
| 11 | Compose como ambiente de desenvolvimento | Adepto | 🔶 | 3 |
| 12 | Registry | Adepto | 🔶 | 4 |
| 13 | Segurança da imagem e do runtime | Adepto | 🔶 | 4 |
| 14 | Debugar um container | Adepto | 🔶 | 4 |
| 15 | Docker por dentro | Magus | 🔶 | 5 |
| 16 | O ecossistema além do Docker | Magus | 🔶 | 5 |
| 17 | Docker em CI e na máquina de dev | Magus | 🔶 | 5 |
| 18 | Capstone — empacotar uma app do zero | Magus | 🔶 | 6 |

## Material a consumir

| Fonte | Onde | Aproveitamento |
|---|---|---|
| `Infraestrutura/Docker.md` | 1298 linhas, `publish: false` | semente principal — rica em código e já organizada por assunto; vira tronco podado no bloco 7 |
| `Infraestrutura/Comandos Docker e WSL.md` | 431 linhas | referência solta de ambiente local; permanece, não vira nota |
| `Infraestrutura/Docker credential helpers.md` | 83 linhas | citado pela nota 12 (registry), permanece como referência |

> [!warning] Regra de conteúdo
> As seções `Na prática (da minha experiência)` e `How to explain in English` do monólito são **relato pessoal do autor e material de entrevista**. Elas ficam no tronco podado e **não migram** para as notas do galho. Nada sobre a experiência do autor pode ser inventado nas notas.

## Fronteiras a respeitar

| Vizinho | Fica lá | Fica aqui |
|---|---|---|
| `Ciência/SO 13` | namespaces, cgroups, runc, OCI, escape de container | como o Docker usa isso; a cadeia daemon → containerd → runc |
| `Operação 3-01` | imagem de produção como disciplina (imutabilidade, digest, política de não-root) | como a imagem é construída; cache; camadas |
| `Cloud 12` | ECS, Fargate, App Platform, Kubernetes gerenciado | o Docker que você mesmo opera |
| `Terminal/TUIs` | Lazydocker e a ergonomia | o que a TUI está manipulando por baixo |
| `Java`/`Go`/`Python` cloud-native | o Dockerfile daquela linguagem | o Dockerfile como mecanismo, agnóstico de stack |
| `Java/Testes 11`, `Testes JS` | Testcontainers como prática de teste | Docker em CI como mecanismo (nota 17) |

## Pendências

- **Escrita:** ✅ **18/18 completa em 2026-08-02** (blocos 1-6 do plano).
- **M1 (mídia):** passada posterior. Busca e verificação de ID **centrais via `yt-dlp`** — nunca delegadas a subagente.
- **Poda do monólito e callouts de volta:** bloco 7 do plano.

## Notas de execução

- Galho aberto em 2026-08-02 como primeiro do domínio Infraestrutura, na sequência direta do fechamento de Controle de Versão.

## M1 — candidato verificado, aguardando transcrição

| Nota | Vídeo | ID | Canal | Estado |
|---|---|---|---|---|
| 15 | Containers From Scratch | `8fi7uSYlOdc` | GOTO 2018, Liz Rice, 43 min, 312 mil views | Metadados verificados; **transcrição não lida** |

Liz Rice constrói um container ao vivo, em Go, chamando namespaces e cgroups à mão. O ponto de inserção já está escolhido: a seção **"Onde os namespaces e cgroups entram — e onde esta nota para"** da nota 15 declara uma fronteira dura (o *como* do kernel pertence a `Ciência/Sistemas Operacionais/13`) — e a palestra é exatamente o que fica logo depois desse ponto de parada, o que a torna leitura complementar ideal sem mover a fronteira. **Não foi embutida** porque a sessão de 2026-08-09 esbarrou de novo no rate limit do YouTube, e a regra de ouro proíbe embutir sem ter lido a transcrição.

> [!warning] Método de descoberta de ID
> Usar `uvx yt-dlp "ytsearch5:<título>" --print "%(id)s|%(title)s|%(channel)s|%(duration)s|%(view_count)s"`, que devolve IDs reais direto do YouTube. Busca web devolve IDs *plausíveis* e já custou retrabalho nos galhos Nginx e Kubernetes.

## Próximos alvos de M1

Prioridade nas conceituais: **15** (candidato já escolhido acima), **01** (o problema que o container resolve), **10** (BuildKit por dentro), **13** (segurança de imagem e runtime). A nota **08** (ENTRYPOINT/CMD, PID 1 e zumbis) foi buscada e **não rendeu**: os candidatos eram um vídeo de 66 views e dois fora do inglês/português. Não repetir a busca sem ângulo novo.
