---
title: "Infraestrutura"
type: moc
publish: true
---

# Infraestrutura

Docker, Kubernetes, WSL, cloud e configuração de ambientes.

## Containers e Orquestração

- [[Docker]] — containers, Dockerfile, Compose, multi-stage, security
- [[Kubernetes]] — orquestração, objetos core, GitOps, production patterns
- [[WSL, Docker e Kubernetes]]
- [[Comandos Docker e WSL]]
- [[Docker credential helpers]]

## Web Servers

- [[Nginx]] — reverse proxy, load balancing, TLS, caching, rate limiting

## DevOps

- [[CI-CD]] — pipelines, GitHub Actions, GitOps, security, deployment strategies
- [[Observabilidade]] — logs, metrics, traces, SLOs, OpenTelemetry, Prometheus, Grafana

## Ambiente de Desenvolvimento

- [[Linux]] — shell, permissions, systemd, networking, debugging
- [[Terminal]]
- [[GitHub CLI]] — gh, automação GitHub, repos, PRs, Actions, secrets, API
- [[Configurando Ambiente Linux no WSL]]

## Cloud

- [[Digital Ocean]]

---

```dataview
LIST
FROM "Infraestrutura"
WHERE type != "moc"
SORT file.name ASC
```
