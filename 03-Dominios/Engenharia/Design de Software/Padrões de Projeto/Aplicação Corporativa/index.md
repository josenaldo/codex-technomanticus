---
title: "Aplicação Corporativa"
created: 2026-07-30
updated: 2026-07-30
type: moc
status: evergreen
publish: true
tags:
  - moc
  - design-de-software
  - aplicacao-corporativa
  - poeaa
  - legado
aliases:
  - Aplicação Corporativa
  - PoEAA
  - Patterns of Enterprise Application Architecture
  - Enterprise Application Patterns
  - Galho - Aplicação Corporativa
---

# Aplicação Corporativa

> [!abstract] TL;DR
> A metade **não-dados** do catálogo de **Martin Fowler** (*Patterns of Enterprise Application Architecture*, 2002): apresentação web, distribuição, concorrência offline, estado de sessão e os padrões-base. Quarta família do galho-pai [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/index|Padrões de Projeto]]. É a família mais **datada** das seis — e é justamente por isso que ela serve ao ofício de legado: estes são os padrões que você **encontra** ao abrir um sistema de 2006. A lente é **arqueológica** (era × hoje), e cada nota tem uma seção **A ressurreição**, porque a maioria destes padrões voltou — quase sempre por causa da nuvem.

## Sobre esta família

Catálogo de consulta para o sênior de plantão. Cada nota é autocontida, a seção **Armadilhas** pesa no *quando não usar*, e a seção **A ressurreição** marca explicitamente o que é **correspondência reconhecida** (BFF *é* Remote Facade) e o que é **leitura deste catálogo** (React como Transform View) — nunca apresentando interpretação como consenso.

**Fronteira com [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Acesso a Dados/index|Acesso a Dados]]:** aquela é a outra metade do mesmo livro. *Service Layer*, *Gateway* e *Mapper* têm casa canônica lá e aqui aparecem só em prosa + cross-link — a única redundância que o galho não aceita é duas notas disputando o mesmo padrão.

**Fronteira com [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]]:** a nota 08 trata de **onde o estado da conversa mora** (decisão de arquitetura); as consequências de segurança de token e cookie têm casa profunda naquele galho.

## Iniciado — Apresentação: como a requisição vira tela

1. [[01 - Panorama da aplicação corporativa]] — as três camadas, o contexto de 2002 e o método de ler um legado por elas.
2. [[02 - MVC — o padrão mais mal-entendido]] — o original (Reenskaug, 1979) × o web × a diáspora MV*; o observer como coração perdido.
3. [[03 - Page Controller × Front Controller]] — quem recebe a requisição; o *file-based routing* ressuscitou o primeiro, o segundo virou infraestrutura.
4. [[04 - Application Controller]] — quem decide o próximo passo; a máquina de estados que virou Step Functions e XState.
5. [[05 - Template View × Transform View × Two-Step View]] — as três formas de produzir a saída; a migração silenciosa para Transform View.

## Adepto — Distribuição, estado e concorrência offline

6. [[06 - Remote Facade]] — interface grossa na fronteira remota; hoje se chama BFF.
7. [[07 - DTO — e por que virou pejorativo]] — as quatro situações em que ele se justifica, e todas as outras.
8. [[08 - Session State — Client × Server × Database]] — a nuvem **inverteu** a recomendação de 2002.
9. [[09 - Optimistic × Pessimistic Offline Lock]] — o *lost update* e a transação de negócio que o banco não enxerga.
10. [[10 - Coarse-Grained Lock]] — travar o conjunto; o único padrão **sem** ressurreição, absorvido pelo agregado do DDD.

## Magus — os padrões-base que você usa sem nomear

11. [[11 - Layer Supertype + Separated Interface]] — destinos opostos: um caiu com a composição, o outro virou o Hexagonal.
12. [[12 - Registry + Plugin + Service Stub]] — quem decide qual implementação: execução, configuração, teste.
13. [[13 - Value Object + Money]] — identidade por valor; por que dinheiro em ponto flutuante é bug garantido.
14. [[14 - Special Case + Null Object]] — a ausência como objeto; **fecha a família** com o mapa de reconhecimento dos 14 padrões e a síntese da lente arqueológica.

> [!tip] Atalho para quem está com um legado na mesa
> A nota [[14 - Special Case + Null Object]] termina com um **mapa de reconhecimento**: uma tabela que vai do que você encontra no código (`web.xml` com servlet único, classes `XxxVO`, coluna `VERSION`, `AbstractEntity`) direto para o padrão e a nota. É o índice mais útil da família em campo.

## Veja também

- [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/index|Padrões de Projeto]] — o galho-pai e as seis famílias.
- [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Acesso a Dados/index|Acesso a Dados]] — a outra metade do PoEAA.
- [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Integração Empresarial (EIP)/index|Integração Empresarial (EIP)]] — a família anterior.
- [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index|Arqueologia e Restauração de Software]] — o método de assumir um sistema herdado, de que esta família é o vocabulário.
