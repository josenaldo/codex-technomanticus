---
title: "Slopsquatting — o ataque via alucinação"
created: 2026-05-02
updated: 2026-05-02
type: concept
fase: Iniciado
progress: backlog
status: seedling
publish: true
tags:
  - seguranca-ia
  - ia
  - supply-chain
  - hallucination
aliases:
  - Slopsquatting
  - Phantom packages
  - Package hallucination
  - AI hallucination squatting
---

# Slopsquatting — o ataque via alucinação

> [!abstract] TL;DR
> Slopsquatting (termo cunhado por Seth Larson) é um ataque de supply chain que **não existia antes dos LLMs**: atacante observa que um modelo alucina certos nomes de pacote inexistentes, **registra esses nomes** em npm/PyPI/etc, e espera que devs (ou agentes) instalem. Pesquisa USENIX Security mostrou que [[Dicionário de IA#LLM (Large Language Model)|LLMs]] são **determinísticos nas [[Dicionário de IA#Hallucination|alucinações]]** — GPT-4 sugere o mesmo nome falso para >20% dos prompts similares. Em janeiro de 2026, `react-codeshift` (pacote inexistente) se espalhou por **237 repos GitHub** via skills de agentes que ninguém revisava. Mitigação: sandboxing, lockfile verification, package allowlisting.

> [!question]- Por que slopsquatting é diferente de typosquatting tradicional?
> Typosquatting depende de erro humano de digitação — alguém escreve `reqeusts` em vez de `requests`. Slopsquatting não depende de nenhum erro humano: o nome inventado é gerado com confiança pelo LLM, parece legítimo, e o desenvolvedor não tem razão óbvia para duvidar. Pior: a alucinação é **determinística** — o mesmo nome falso aparece para múltiplos desenvolvedores em situações similares, então o atacante pode registrar sistematicamente os nomes mais alucinados e esperar o tráfego chegar. Escala industrialmente de um modo que typosquatting jamais alcançou.

## A mecânica do ataque

```mermaid
graph LR
    A["LLM alucina<br/>'pacote-foo'"] --> B{"Atacante<br/>monitora?"}
    B -->|sim| C["Atacante registra<br/>'pacote-foo' em npm"]
    C --> D["Pacote contém<br/>malware"]
    D --> E["Dev/agente<br/>instala automaticamente"]
    E --> F["Sistema<br/>comprometido"]
    A --> G["Dev pergunta de novo<br/>(prompt similar)"]
    G --> A
```

O ataque explora **determinismo da alucinação**: LLMs alucinam de forma reprodutível. Se você pergunta "como faço X em Python", o modelo sugere o mesmo pacote inventado para você e para outros mil devs.

## A descoberta que mudou o jogo

> [!quote] USENIX Security Symposium (research) — 2024-2025
> *"LLMs são creatures of habit — se GPT-4 sugere um pacote falso para um dev, há alta probabilidade (frequentemente >20%) de sugerir o mesmo pacote falso para outros devs em queries similares."*

Antes: alucinações pareciam **aleatórias**. Pensava-se que cada dev veria nomes inventados diferentes. **Falso.** Os mesmos nomes aparecem repetidamente. Atacantes apenas precisam observar e registrar.

## O caso `react-codeshift` (jan 2026)

> [!example] react-codeshift — caso real
> Janeiro de 2026: pacote `react-codeshift` foi reclamado em npm. Não tinha autor real, não tinha histórico, não tinha funcionalidade. Era um nome **alucinação-por-conflação** — modelo confundiu `react` + `codeshift` (real, mas separado).
>
> Espalhou em 237 repositórios GitHub via **AI-generated agent skills** que ninguém revisou.
>
> Downloads diários de **agentes automatizados** que instalavam sem humano olhar.
>
> Source: Trend Micro, Socket.dev (2026)

## Tipos de slopsquat

| Variante | Mecânica |
|---|---|
| **Hallucination-by-creation** | Modelo inventa nome do nada |
| **Hallucination-by-conflation** | Modelo combina nomes de libs reais (`react-codeshift`, `axios-fetch`) |
| **Hallucination-by-typo** | Modelo aproxima nome real (`pyhton-requests` em vez de `requests`) |
| **Cross-language confusion** | Modelo sugere nome de pacote npm em projeto Python e vice-versa |
| **Outdated reference** | Modelo sugere nome de lib que existiu mas foi descontinuada |

## Por que LLMs alucinam tanto pacote

- **Treinamento misto**: dados de treino incluem repos que mencionam libs antigas, deprecated, ou de domínio adjacente
- **Pattern completion**: modelo prefere completar com "nome plausível" do que admitir ignorância
- **Bundling de libs**: quando pedido para "usar X + Y + Z juntos", modelo inventa nome composto
- **Benchmarks que premiam confiança**: training optimization pode reforçar "responder algo" sobre "dizer não sei"

## Por que ataque escala em 2026

| Fator | Multiplicador |
|---|---|
| **Volume de geração** | LLMs geram milhares de imports/dia |
| **Velocidade de install automático** | Agentes rodam `npm install` sem prompt humano |
| **Tail de pacotes raros** | Atacante pode ocupar 1000s de nomes baratos |
| **Cross-pollination** | AI skills reutilizam lista de deps geradas |
| **Confiança no agente** | Devs aprovam install sem checar registry |

Slopsquat **multiplica** ataques tradicionais de supply chain (typosquatting). Antes: atacante precisava errar com letrinha. Agora: atacante apenas registra alucinações conhecidas.

## Mitigação — Defense in depth

### Layer 1 — Lockfiles + verification

```bash
# Sempre commitar e validar
package-lock.json
yarn.lock
poetry.lock

# CI verifica que install só usa pacotes do lockfile
npm ci  # NÃO npm install
```

`npm ci` falha se package.json discorda do lockfile. **Não permite que agente adicione dep silenciosamente.**

### Layer 2 — Allowlisting de registry

Usar registry interno (Verdaccio, JFrog Artifactory) com política de allowlist. Pacote desconhecido → bloqueado.

```yaml
# Política de exemplo
allowlist:
  - axios
  - react
  - lodash
  # ...

policy:
  unknown_package: BLOCK
  require_human_approval: true
```

### Layer 3 — Sandboxing de install

Rodar `npm install` em sandbox (container, VM, [[06 - Permissões e sandboxing|seatbelt/bubblewrap]]) com network limitada — evita post-install scripts maliciosos atingirem host.

### Layer 4 — Validação de pacote

```bash
# Verificar se package realmente existe e é confiável
npm view <pkg>
# Checar: idade, downloads, autor, fonte
```

Ferramentas: Socket.dev, Snyk Open Source, Endor Labs — fazem essa checagem automaticamente em CI.

### Layer 5 — Extended thinking nos agentes

Agentes modernos (Claude Code, OpenAI Codex CLI, Cursor com MCP) podem **verificar online** que o pacote existe antes de sugerir:

> [!quote] Claude Code CLI documentation
> *"Dynamically interleaves internal reasoning with external tools — live web searches, documentation lookups — to verify package availability as part of its generation pipeline."*

Reduz a alucinação significantemente. **Não elimina.**

## Detecção em projeto existente

```bash
# Listar deps suspeitas
npm ls --json | jq '.dependencies | keys[]' | xargs -I {} npm view {} --json 2>/dev/null

# Para cada dep:
# - Idade < 30 dias? Suspeito
# - Downloads < 100/semana? Suspeito
# - Sem maintainers ativos? Suspeito
# - Ausente de fontes confiáveis? Bloquear
```

Tools: Snyk, Socket.dev, npq (Node), pip-audit (Python).

## Sinais de slopsquat numa codebase

> [!question] Diagnóstico
> - [ ] Pacotes com nomes "compostos" estranhos (`react-tools-extras`)
> - [ ] Deps adicionadas sem PR — direto pelo agente
> - [ ] Lockfile mudou sem mudança de package.json correspondente
> - [ ] Pacote com <100 downloads/semana sendo usado
> - [ ] Pacote sem documentação ou repo
> - [ ] Skills de agente reutilizadas com lista de deps incluída
>
> 2+ marcadas: audit imediato.

## O que fazer se cair

1. **Isolar** — sandbox onde foi instalado, não conectar à rede
2. **Auditar** — `npm audit`, scan com Snyk; checar persistência (cron, services)
3. **Reset de credenciais** — qualquer secret tocado pelo processo
4. **Reportar** — para registry (npm support@npmjs.com, PyPI security@python.org)
5. **Postmortem** — qual gate falhou; reforçar (ver [[12 - O roadmap de segurança para times]])

## Anti-patterns

- **Confiar no `npm install`** — é o vetor primário
- **Aprovar install via prompt do agente sem checar** — humano fadiga e clica yes
- **Sem CI scan de novas deps** — slopsquat passa despercebido por dias
- **Lockfiles sem CI verification** — atacante pode adicionar via PR camuflado
- **Permitir agente em rede aberta** — install + post-install scripts comprometem host

## Armadilhas comuns

> [!warning] Verificar o nome do pacote no Google "não é suficiente"
> Um pacote malicioso de slopsquatting pode ter uma página npm legítima, README copiado de outro projeto e algumas estrelas compradas. A presença no registry não prova legitimidade — o que importa é a combinação de idade, histórico de downloads, maintainers e se o pacote aparece em fontes confiáveis auditadas.

> [!warning] Agentes em modo autônomo instalam deps sem confirmação humana
> No workflow agentico padrão, o agente gera código com `import pacote-inventado` e logo após executa `npm install pacote-inventado` como ação de tool use. Se o humano só revisa o código final e não o log de ações, a instalação já aconteceu. Configurar o agente para exigir aprovação explícita em qualquer operação de install é requisito, não opcional.

> [!warning] Lockfiles sem CI enforcement são decoração
> Commitar `package-lock.json` é bom, mas se o CI usa `npm install` em vez de `npm ci`, o lockfile é ignorado na prática. Qualquer dep nova adicionada por agente ou por PR automatizado entra sem gate. A distinção `npm install` vs `npm ci` é pequena na digitação e enorme no vetor de ataque.

## Como explicar em inglês

Slopsquatting is a supply chain attack that emerged directly from the deterministic nature of LLM hallucinations. Traditional typosquatting relied on human typing errors — an attacker registers `reqeusts` hoping someone miskeys `requests`. Slopsquatting is different: the LLM confidently suggests a package name that doesn't exist, the same hallucinated name appears for many developers asking similar questions, and an attacker only needs to monitor which names are frequently hallucinated and register them in advance.

The attack surface exploded with agentic workflows. When an AI agent writes code that imports a hallucinated package and then automatically runs the install command without human review, the malicious package executes post-install scripts on the developer's machine before anyone notices. The `react-codeshift` incident in January 2026 — where a hallucinated package spread across 237 GitHub repositories — is the clearest demonstration of how agentic speed amplifies this risk.

Defense requires treating every new dependency as untrusted until verified: lockfile enforcement with `npm ci`, package allowlists via internal registries, sandboxed install environments, and automated scanning with tools like Socket.dev or Snyk.

**In a technical interview**, you might say:

> "Slopsquatting targets the determinism of LLM hallucinations — the same fake package name appears across many developers' prompts, so attackers can pre-register those names at scale. In agentic pipelines, this is critical because the agent may install without human review. Our defense is layered: `npm ci` instead of `npm install` in CI, an internal registry allowlist so unknown packages are blocked by default, and sandboxed execution of install scripts. We also use Socket.dev to flag newly registered or suspicious packages before they enter our lockfile."

| PT | EN |
|----|-----|
| ataque de cadeia de fornecimento | supply chain attack |
| alucinação determinística | deterministic hallucination |
| nome de pacote inventado | hallucinated package name |
| lista de permissões | allowlist |
| registro interno | internal registry |
| arquivo de bloqueio | lockfile |
| script pós-instalação | post-install script |
| agente autônomo | autonomous agent |
| auditoria de dependências | dependency audit |
| superfície de ataque | attack surface |

## O que vem a seguir

Slopsquatting explora um tipo específico de alucinação: o modelo inventa nomes de pacotes. Mas as alucinações vão além dos nomes de bibliotecas — LLMs também inventam APIs inteiras, parâmetros que não existem, e assinaturas de funções que nunca foram implementadas. A próxima nota explora esse fenômeno mais amplo: quando o modelo não apenas sugere um pacote errado, mas descreve como usá-lo com detalhes convincentes que são completamente fabricados.

Entender as duas formas de alucinação juntas revela o padrão: o LLM é otimizado para gerar output plausível, não output verificado.

- [[03 - Alucinações em código — APIs fantasma e parâmetros inexistentes]] — quando o modelo inventa não só pacotes, mas métodos, classes e parâmetros inteiros

## Veja também

- [[01 - Código gerado por IA é untrusted]]
- [[03 - Alucinações em código — APIs fantasma e parâmetros inexistentes]]
- [[06 - Permissões e sandboxing]]
- [[05 - SAST e SCA para código AI]]

## Referências

- **Trend Micro** — *Slopsquatting: When AI Agents Hallucinate Malicious Packages* (2026).
- **Socket.dev** — *The Rise of Slopsquatting: How AI Hallucinations Are Fueling a New Class of Supply Chain Attacks* (2026).
- **Snyk** — *Package Hallucination: Impacts and Mitigation* (2026).
- **Aikido** — *Slopsquatting: The AI Package Hallucination Attack Already Happening* (2026).
- **Mend.io** — *The Hallucinated Package Attack: Slopsquatting Explained* (2026).
- **USENIX Security Symposium** — Pesquisa sobre determinismo de alucinações em LLMs (2024-2025).
- **Cloudsmith** — *Typosquatting & Slopsquatting: Protecting Your Software Supply Chain* (2026).























































