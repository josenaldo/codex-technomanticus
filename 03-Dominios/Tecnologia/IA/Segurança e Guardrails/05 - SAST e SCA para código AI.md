---
title: "SAST e SCA para código AI"
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
  - guardrails
  - sast
  - sca
aliases:
  - SAST AI code
  - SCA AI code
  - Snyk Semgrep CodeQL
  - Static analysis AI
---

# SAST e SCA para código AI

> [!abstract] TL;DR
> Static Application Security Testing (SAST) analisa código em busca de vulnerabilidades; Software Composition Analysis (SCA) analisa dependências em busca de vulns conhecidas e pacotes maliciosos. Para código IA, **rode os dois, em CI, em todo commit**. Semgrep + Snyk Code (ou CodeQL) é a combinação dominante em 2026. **Use 2+ ferramentas SAST simultaneamente** — pesquisa mostra que 78% dos issues confirmados são pegos por **só uma ferramenta**. Foque rules em CWE-918 (SSRF), CWE-78 (command injection), CWE-89 (SQLi), CWE-798 (hardcoded creds) — os mais comuns em código LLM.

> [!question]- Por que SAST e SCA precisam de ajuste para código gerado por IA?
> Ferramentas SAST e SCA clássicas foram calibradas para encontrar bugs que humanos cometem com certa frequência. Código AI tem um perfil diferente: algumas classes de vulnerabilidade aparecem com frequência muito maior (CWE-80 XSS em 86% dos samples, hardcoded credentials crônicos), e os padrões específicos são reprodutíveis e previsíveis — não são desvios raros. Isso significa que as regras padrão podem ter sensibilidade insuficiente para os CWEs mais comuns em código LLM, e que rodar apenas uma ferramenta perde até 78% dos issues que outra ferramenta capturaria. O ajuste não é "ativar mais regras" — é entender quais classes de erro o modelo comete sistematicamente e garantir que a cobertura é adequada especificamente para elas.

## SAST vs SCA — quem pega o quê

| | SAST | SCA |
|---|---|---|
| **O que analisa** | Seu código | Dependências |
| **Pega** | XSS, SQLi, command injection, race conditions | CVEs em libs, slopsquat, licenças |
| **Quando** | Cada commit | Cada commit + alerta contínuo |
| **Falsos positivos** | Médio | Baixo |
| **Custo** | Tempo de scan | Tempo de scan + manutenção de allowlist |

Os dois são **complementares**. Times pulam SCA pensando "uso só libs famosas" — exatamente onde slopsquat e CVEs aparecem.

## Top SAST tools 2026

| Tool | Forte em | Modelo |
|---|---|---|
| **Semgrep** | Rules customizáveis, rapidíssimo (~10s scan), zero FP em OWASP benchmark | Open source + cloud |
| **Snyk Code** | DeepCode AI, IDE integration real-time, fix suggestions | SaaS |
| **CodeQL (GitHub)** | Semantic analysis, queries declarativas, indirect data flow | Free para repos públicos |
| **SonarQube/Cloud** | Quality + security, dashboards corporativos | Self-hosted ou SaaS |
| **Checkmarx** | Enterprise SAST, compliance focus | SaaS |
| **Veracode** | Compliance + binary analysis | SaaS |
| **DryRun Security** | PR-native scanning | SaaS |

## Rule prioritization para AI code

Veracode e DryRun mostram que [[Dicionário de IA#LLM (Large Language Model)|LLMs]] **falham consistentemente** em algumas classes:

| CWE | Vulnerabilidade | Por que LLMs falham |
|---|---|---|
| **CWE-80** | XSS | Templates sem auto-escape; modelo não detecta context |
| **CWE-89** | SQL Injection | String concat em queries; modelo "esquece" parametrização |
| **CWE-918** | SSRF | URLs construídas com input; modelo não valida hosts |
| **CWE-78** | Command Injection | `subprocess.run(f"cmd {user_input}")` |
| **CWE-22** | Path Traversal | `open(f"./{user_input}")` |
| **CWE-502** | Insecure Deserialization | `pickle.loads(network_data)` |
| **CWE-798** | Hardcoded Credentials | API keys em código |
| **CWE-117** | Log Injection | `log.info(f"User: {user}")` sem sanitização |
| **CWE-943** | NoSQL Injection | MongoDB com `$where` sem validação |

Configure suas SAST rules para **alta sensibilidade** nestes. Aceite alguns false positives — eles são de longe menos custosos que false negatives.

## Configuração mínima — Semgrep

```yaml
# .semgrepignore — coisas a pular
node_modules/
build/
*.test.ts

# .github/workflows/semgrep.yml
on: [pull_request]
jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          docker run --rm -v $(pwd):/src \
            returntocorp/semgrep \
            --config=auto \
            --error \
            --severity=ERROR \
            --severity=WARNING
```

`--config=auto` carrega Semgrep Registry com regras para a stack detectada. `--error` faz CI falhar se vulnerabilidade for achada.

Para código IA, considere também:

```yaml
- run: semgrep --config=p/owasp-top-ten --config=p/secrets --config=p/python-correctness
```

## Configuração mínima — Snyk Code

```bash
# CLI
snyk auth
snyk code test

# Em CI (GitHub Actions):
- uses: snyk/actions/setup@master
- run: snyk code test --severity-threshold=medium
```

Snyk Code adiciona **fix suggestions** automatizadas. Útil em PR comments — dev vê o problema E a correção.

## Configuração mínima — CodeQL

```yaml
# .github/workflows/codeql.yml
on:
  pull_request:
  schedule:
    - cron: '0 0 * * 1'  # weekly

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: javascript,python
          queries: security-extended
      - uses: github/codeql-action/analyze@v3
```

`security-extended` query suite cobre os CWEs principais com semantic analysis (segue data flow através de chamadas).

## A regra dos 78%

> [!warning] Pesquisa essencial
> *"In testing, 78% of confirmed vulnerabilities were caught by only a single tool."* — DryRun Security, 2026
>
> Significa: rodar **só** uma ferramenta deixa passar **78%** dos issues que outra ferramenta acharia. Combine: Semgrep + Snyk, ou CodeQL + Snyk, ou Semgrep + CodeQL.

Combo recomendado para 2026:
- **Semgrep** (velocidade, customização, OSS)
- **+ Snyk Code** OU **CodeQL** (semantic analysis, dataflow)
- **+ Snyk Open Source** ou **Socket.dev** (SCA)

## SCA — focando em slopsquat

Para [[02 - Slopsquatting — o ataque via alucinação|slopsquat]] e supply chain:

| Tool | Forte em |
|---|---|
| **Snyk Open Source** | CVE database grande, fix suggestions |
| **Socket.dev** | Detecção de pacote malicioso (não só CVE) |
| **Endor Labs** | Reachability analysis (vuln só conta se chega em runtime) |
| **Aikido Security** | Slopsquat detection nativo |
| **GitHub Dependabot** | Free, integrado |

> [!tip] Socket.dev — destaque
> Socket detecta **comportamento suspeito** em pacotes (post-install scripts, network exfil, obfuscation) — não depende de CVE estar publicada. Crítica em 2026 para detectar slopsquat *antes* da CVE ser conhecida.

## Pipeline integrado — exemplo completo

```yaml
name: Security Pipeline

on: [push, pull_request]

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # SAST tool 1
      - name: Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >
            p/owasp-top-ten
            p/secrets
            p/python-correctness

      # SAST tool 2 (different engine)
      - name: CodeQL
        uses: github/codeql-action/analyze@v3

      # SCA — code dependencies
      - name: Snyk Open Source
        uses: snyk/actions/python@master
        with:
          args: --severity-threshold=high

      # SCA — slopsquat / behavioral
      - name: Socket Security
        uses: socketsecurity/action@v1
```

Tempo total target: <8min. Custo de NÃO ter: incidente em prod.

## AI-assisted remediation

> [!info] Padrão emergente em 2026
> Ferramentas começam a oferecer **auto-fix por LLM** para findings. Snyk Code, Semgrep Assistant, GitHub Copilot autofix.
>
> **Cuidado:** AI-fix carrega mesmo risco de [[01 - Código gerado por IA é untrusted|45% inseguro]]. Trate fix gerado como código novo: passa pelo mesmo SAST de novo.

## Métricas que importam

| Métrica | Alvo |
|---|---|
| **% PRs com finding crítico bloqueado** | Variável, mas existir |
| **Mean time to remediate (MTTR)** | <1 dia para críticos, <1 semana para médios |
| **% findings com false positive** | <15% (acima → calibre rules) |
| **Cobertura de SAST** (% LOC scaneadas) | >90% |
| **Tempo CI total para SAST + SCA** | <10 min |

## Anti-patterns

- **Rodar SAST como warning, não erro** — todo mundo ignora warnings
- **Single-vendor SAST** — perde 78% (regra de DryRun)
- **SCA só em PRs grandes** — slopsquat entra via PR pequeno
- **Sem allowlist de licenças** — copyleft em proprietário causa pesadelo legal
- **Ignorar SCA "porque uso só libs famosas"** — slopsquat ataca exatamente assim
- **AI auto-fix sem re-scan** — fix pode introduzir issue diferente

## Armadilhas comuns

> [!warning] SAST como warning não para nada
> A configuração mais perigosa é ter Semgrep ou CodeQL rodando em CI mas sem flag `--error` — os findings aparecem nos logs, o CI passa, e ninguém olha. A diferença entre SAST como gate e SAST como decoração é uma flag de configuração. Times que "têm SAST configurado" mas não bloqueiam PR em findings críticos têm o custo sem o benefício.

> [!warning] Aceitar "AI auto-fix" sem re-scan cria loop de vulnerabilidades
> Ferramentas como Snyk Code e Semgrep Assistant oferecem correções automáticas geradas por LLM para os findings. O problema é que a correção AI carrega exatamente o mesmo risco que o código original: pode conter vulnerabilidade diferente, pode reintroduzir a mesma vuln com outra forma, pode quebrar a correção semanticamente. AI-fix deve passar pelo mesmo pipeline SAST que qualquer outro código gerado.

> [!warning] Não fazer SCA "porque uso só libs famosas"
> Slopsquatting não atinge só libs obscuras — atinge exatamente o espaço adjacente às libs mais comuns, onde o modelo confla nomes (`axios-fetch`, `react-codeshift`). E CVEs em libs famosas existem — o npm advisory database tem entradas em Express, lodash, moment. SCA não é opcional para times que usam geração por IA.

## Como explicar em inglês

SAST and SCA are complementary tools that address different layers of security risk in AI-generated code. SAST analyzes the code itself — finding SQL injection patterns, hardcoded credentials, XSS vulnerabilities, and command injection. SCA analyzes the dependency graph — catching known CVEs in libraries and detecting behavioral signals of malicious packages like slopsquat targets.

For AI-generated code specifically, both need calibration. LLMs fail consistently on a predictable set of CWEs: XSS in 86% of samples, SQL injection in ~50%, SSRF increasingly common. Tuning SAST rules to high sensitivity on those specific classes, and accepting some false positives in exchange for lower false negative rate, is the right trade-off when the alternative is a vulnerability in production.

The most important finding from DryRun Security research is the 78% single-tool rule: 78% of confirmed vulnerabilities were found by only one of the tools tested. This means running a single SAST tool gives a false sense of coverage. The minimum viable configuration is two complementary scanners — Semgrep for speed and customizability, CodeQL or Snyk Code for semantic data flow analysis.

**In a technical interview**, you might say:

> "We run two SAST tools in combination — Semgrep with OWASP and secrets rulesets, plus CodeQL for semantic data flow analysis — because research shows 78% of confirmed vulnerabilities are caught by only a single tool. For SCA we use both Snyk Open Source for CVE detection and Socket.dev for behavioral analysis of packages, which is critical for catching slopsquat targets before a CVE is even published. All of these are hard blocks in CI, not warnings. The LLM-specific tuning is high sensitivity on CWE-80, 89, 918, and 798 — the classes where LLMs fail most consistently."

| PT | EN |
|----|-----|
| análise estática de segurança | static application security testing (SAST) |
| análise de composição de software | software composition analysis (SCA) |
| vulnerabilidade confirmada | confirmed vulnerability |
| falso positivo | false positive |
| falso negativo | false negative |
| injeção SQL | SQL injection |
| requisição forjada do lado do servidor | server-side request forgery (SSRF) |
| injeção de comando | command injection |
| credenciais fixas no código | hardcoded credentials |
| análise de fluxo de dados | data flow analysis |

## O que vem a seguir

Com SAST e SCA cobrindo análise estática e dependências, a próxima camada de defesa é o ambiente de execução. Mas sandboxing vai além de "rodar em container" — é sobre definir o que o agente pode e não pode fazer: quais sistemas de arquivo pode tocar, quais chamadas de rede pode fazer, quais operações privilegiadas estão fora do alcance. A próxima nota explora permissões e sandboxing como fronteira de contenção para workflows agênticos.

- [[06 - Permissões e sandboxing]] — como configurar o ambiente de execução para que código AI não possa causar dano além do escopo permitido

## Veja também

- [[01 - Código gerado por IA é untrusted]]
- [[02 - Slopsquatting — o ataque via alucinação]]
- [[04 - A pirâmide de validação AI]]
- [[09 - Testes imutáveis — a barreira que o agente não pode reescrever]]
- [[Spec-Driven Development|07 - Fase Validate — spec como contrato executável]]

## Referências

- **DryRun Security** — *Top 10 AI SAST Tools for 2026 and How to Enforce Code Policy* (2026).
- **Veracode** — *2025 GenAI Code Security Report* (2025).
- **Vibe-eval** — *Best SAST Tools for AI-Generated Code: Snyk vs Semgrep vs Checkmarx* (2026).
- **Rafter** — *Static Code Analysis Tools Comparison 2026* (2026).
- **Konvu** — *SCA vs SAST 2026: What Each Tool Finds, Misses, and Costs* (2026).
- **Doyensec** — *Independent SAST testing on OWASP benchmarks* (2025).














