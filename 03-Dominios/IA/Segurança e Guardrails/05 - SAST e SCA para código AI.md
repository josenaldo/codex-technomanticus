---
title: "SAST e SCA para código AI"
created: 2026-05-02
updated: 2026-05-02
type: concept
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
