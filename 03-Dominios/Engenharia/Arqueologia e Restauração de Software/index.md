---
title: "Arqueologia e Restauração de Software"
created: 2026-07-02
updated: 2026-07-02
type: moc
status: seedling
publish: true
tags:
  - engenharia
  - arqueologia-e-restauracao-de-software
  - moc
aliases:
  - Arqueologia e Restauração de Software
  - Trabalhando com Sistemas Legados
  - Legado
---

# Arqueologia e Restauração de Software

> [!abstract] TL;DR
> Galho de Engenharia. O ofício de **assumir e trabalhar com sistemas que você não
> escreveu** — do primeiro contato até ser o dono confiante. Escavar (arqueologia: entender
> o código, o histórico e a organização) e intervir sem destruir o sítio (restauração:
> trocar o que apodreceu por partes funcionais, sem perder o que tem valor). A espinha:
> *como um consultor sênior assume um sistema legado, o compreende, decide seu destino e o
> restaura com segurança?*

## A tese

O que se restaura nunca foi o código — foi a **teoria do sistema**. Seguindo Naur
([[03-Dominios/Engenharia/Complexidade de Software/04 - O programa como teoria|O programa como teoria]]),
o valor real de um software é a teoria viva na cabeça de quem o construiu: o *porquê* de
cada decisão. Legado é o que sobra quando essa teoria se perde. Restaurar é **recuperar a
teoria** e reencarná-la — às vezes remendando uma viga podre, às vezes trocando um módulo
inteiro, e no limite reescrevendo o corpo do zero para que o conceito reviva num corpo novo.
Até o rewrite total é restauração: o código muda, a ideia continua.

Por isso o galho recusa o reflexo do *"kill it with fire"* (Bellotti): destruir é fácil e
quase sempre erra. O default é **restaurar por incrementos seguros**; aposentar ou reescrever
é uma decisão deliberada, nunca um impulso.

## Sobre este galho

Escrito da cadeira do **consultor** — alguém paraquedado *de fora* em codebases que ninguém
explica (due diligence de aquisição, herança de cliente, resgate de emergência), não do
onboarding interno tranquilo. Vai do primeiro contato (não se afogar, construir o mapa
mental) à escavação técnica (engenharia reversa, forense de `git`, rede de testes, seams),
à restauração estratégica (Strangler Fig, migração de dados, deploy seguro) e à camada
humana e política que decide se o trabalho vive ou morre (os R's da modernização, vender a
mudança, conhecimento tribal, compliance).

**Não cobre (linka):**
- *Por que* o software apodrece — entropia, dívida técnica, Naur, Conway: é pré-requisito em
  [[03-Dominios/Engenharia/Complexidade de Software/index|Complexidade de Software]]. Aqui a gente
  **assume o diagnóstico e age** sobre ele.
- As técnicas de teste em geral (pirâmide, TDD, mocking): base em
  [[03-Dominios/Engenharia/Testes/index|Testes]]. Aqui usamos o subconjunto que serve de rede de
  segurança para código sem testes (characterization, approval).
- SRE, SLO/SLI, observabilidade e resposta a incidentes como disciplina: moram em
  [[03-Dominios/Engenharia/Operação/index|Operação]]. Aqui os pegamos emprestados **sob a lente do
  legado** — instrumentar e apagar incêndio num sistema que você ainda não entende.
- O **instrumental de `git`** — as flags de `blame` que sobrevivem a refatoração, pickaxe (`log -S`/`-G`),
  `bisect` automatizado, os comandos que produzem hotspots e acoplamento temporal, e o que esses dados
  *não* dizem: mora em [[03-Dominios/Tecnologia/Controle de Versão/N6 - O repositório como testemunha/index|Controle de Versão — N6, O repositório como testemunha]].
  Aqui está o **método** (que perguntas fazer, como priorizar, como conversar com o cliente); lá está o
  **instrumento**. As notas 07, 09 e 28 deste galho linkam as contrapartes diretas.

## Iniciado — o primeiro contato: entender antes de tocar

1. [[01 - O que é código legado]] — as duas definições (Feathers: código sem testes / Bellotti: código cujo dono foi embora).
2. [[02 - A mentalidade do restaurador]] — Chesterton's Fence, respeito arqueológico, legado como ativo.
3. [[03 - A lente do consultor]] — assumir *de fora* vs. onboarding interno; due diligence, herança, resgate. **(espinha)**
4. [[04 - Os primeiros 30-60-90 dias]] — o protocolo de aterrissagem: orientação → contribuição → independência.
5. [[05 - First Contact]] — por onde entrar sem se afogar (OORP); o inventário técnico (conseguir buildar e rodar).
6. [[06 - Lendo código que você não escreveu]] — técnicas de leitura; construir o modelo mental.
7. [[07 - Arqueologia do histórico]] — `git log`/`git blame` como sítio de escavação; hotspots (introdução).

## Adepto — a escavação e a rede de segurança: mudar com segurança

8. [[08 - Engenharia reversa e recuperação de arquitetura]] — reconstruir o mapa; dependency graphs, static analysis.
9. [[09 - Forense de software]] — Tornhill: hotspots (complexidade × mudança), acoplamento temporal, bus factor.
10. [[10 - A rede de segurança primeiro]] — characterization tests: testes que *revelam* o comportamento atual.
11. [[11 - Approval e Golden Master testing]] — pôr código intocável sob teste rápido (Bache & Falco).
12. [[12 - Seams e quebra de dependência]] — os pontos de intervenção; o legacy change algorithm (Feathers).
13. [[13 - Técnicas cirúrgicas]] — Sprout/Wrap method & class, micro-committing, exploratory refactoring.
14. [[14 - Refactoring em terreno hostil]] — o catálogo de Fowler aplicado a código que resiste.
15. [[15 - O Método Mikado]] — grafo de pré-requisitos e revert agressivo para mudanças grandes.
16. [[16 - IA como acelerador e seus riscos]] — LLM para engenharia reversa e docs; a regra: characterization ANTES de deixar a IA mudar.

## Magus — restaurar, decidir e ser dono: a maestria estratégica

17. [[17 - Frameworks de decisão]] — manter/restaurar/substituir/aposentar; os 6-7 R's, TIME (Gartner); rewrite vs. incremento.
18. [[18 - Strangler Fig]] — fazer o novo crescer em volta do velho, sempre entregável.
19. [[19 - Branch by Abstraction e Anti-Corruption Layer]] — coexistência segura; proteger o novo do velho (DDD).
20. [[20 - Migração de dados e schema]] — expand-contract, dual writes, shadow tables, zero-downtime; data archaeology.
21. [[21 - Validação em produção]] — feature flags, dark launch, parallel run; instrumentar o legado com observabilidade.
22. [[22 - Dependências, upgrades e segurança]] — EOL/CVE, migração de versão de framework/runtime, due diligence de vulnerabilidades.
23. [[23 - A dimensão política]] — Bellotti: "o sistema em volta do sistema"; vender modernização, stakeholders, o business case.
24. [[24 - Conhecimento e documentação]] — ADRs (o *porquê*), living docs/C4, offboarding = onboarding, matar o bus factor.
25. [[25 - Sustentabilidade humana]] — burnout em legado, estimativa sob incerteza (spikes, time-boxing).
26. [[26 - Firefighting em produção]] — investigar e mitigar incidente num sistema que você não entende; e como evitar chegar lá.
27. [[27 - Compliance e arqueologia legal]] — por que certo código *não pode* ser deletado; desenterrar restrições antes de mexer.
28. [[28 - Capstone - Assumindo um sistema legado do zero]] — o playbook do consultor de ponta a ponta, num estudo de caso.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Engenharia/Arqueologia e Restauração de Software"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Engenharia/index|Engenharia (MOC da camada)]]
- [[03-Dominios/Engenharia/Complexidade de Software/index|Complexidade de Software]] — *por que* o software apodrece (o diagnóstico)
- [[03-Dominios/Engenharia/Testes/index|Testes]] — a base da rede de segurança
- [[03-Dominios/Engenharia/Operação/index|Operação]] — SRE, observabilidade e incidentes como disciplina
- [[03-Dominios/Tecnologia/IA/Agentes de Codificação/index|Agentes de Codificação]] — IA aplicada a codebases
