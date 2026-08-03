---
title: "Plano de execução — Galho 2: Kubernetes"
created: 2026-08-03
updated: 2026-08-03
type: spec
publish: false
tags:
  - meta
  - spec
  - plano
  - infraestrutura
  - kubernetes
---

# Plano de execução — Galho 2: Kubernetes

> **Para quem executa:** cada bloco é uma unidade fechada com gate próprio. Escrita via subagente Sonnet (teto de 3 por bloco); gate estrutural por script. Fonte do desenho: [[00-Meta/specs/2026-08-02-dominio-infraestrutura-design|design do domínio]]. Precedente de execução: [[00-Meta/specs/2026-08-02-galho-docker-plano|plano do galho Docker]].

**Objetivo:** escrever as 22 notas do galho `Tecnologia/Infraestrutura/Kubernetes`, em 3 fases, sob a lente *o loop de reconciliação*, e podar o monólito `Kubernetes.md` ao final.

**Arquitetura:** galho-folha com `index.md` (MOC por fase) + `roadmap.md` + 22 notas `01..22`. Semente: `Kubernetes.md` (1612 linhas, o maior monólito da estante).

## O que o levantamento de fronteira mudou (2026-08-03)

O roster esboçado na spec de design previa autoscaling e rede do cluster. O levantamento mostrou que **ambos já estão cobertos em Operação, com profundidade**:

- `Operação 3-04 (Escala e capacidade)` cobre HPA, KEDA com escala a zero, VPA, Cluster Autoscaler, as três camadas juntas, capacity planning, reactive × predictive e thundering herd. **Autoscaling foi CORTADO deste galho** — vira callout apontando para lá. Decisão consciente e registrada: quem procurar autoscaling no galho de Kubernetes encontra o ponteiro, não o silêncio.
- `Operação 3-05 (Rede e borda em produção)` cobre Ingress, Gateway API, service mesh, NetworkPolicy, CoreDNS e mTLS. Aqui sobra o **mecanismo**: Ingress como objeto e o controlador que o implementa (nota 15), e o que roda por baixo — CNI, kube-proxy, DNS do cluster (nota 20).
- `Operação 3-02` cobre o **contrato de runtime** (probes, requests/limits, graceful shutdown) e `3-03` cobre zero-downtime, readiness gating e connection draining. Este galho ensina os **objetos**; a política de produção fica lá.
- `Cloud 12-05` cobre Kubernetes gerenciado — onde termina o control plane do provedor. Este galho é o Kubernetes que você mesmo opera.

**Buraco real encontrado:** `CRD` e `CustomResource` não aparecem em nenhuma nota do vault, e "operator" só é citado de passagem. É a parte que transforma o cluster em plataforma extensível, é assunto de entrevista sênior, e está inteiramente descoberta. Ganha duas notas (18 e 19).

## Restrições globais

- **Lente:** *o loop de reconciliação*. Kubernetes não executa comandos, converge estado — `kubectl apply` escreve um objeto no etcd e vai embora; controllers fazem o resto. Toda nota deve poder ser lida como corolário disso, do mesmo jeito que no galho Docker tudo caía de "a imagem é imutável e em camadas".
- **Escala:** padrão capítulo de livro, 440-540 linhas.
- **Fase:** `Iniciado` (01-07), `Adepto` (08-15), `Magus` (16-22).
- **Núcleo por nota:** TL;DR `[!abstract]` · abertura por problema (nunca "X é...") · corpo-mecanismo · `## Armadilhas comuns` com ≥3 `[!warning]` · `## Como explicar em inglês` com tabela PT↔EN ≥5 linhas · `## O que vem a seguir` (ponte para a próxima nota) · `## Fontes` com URLs clicáveis.
- **Diagramas:** Mermaid onde estrutural. `quadrantChart` proibido.
- **Caducidade:** Kubernetes envelhece rápido. Toda nota que crava comportamento de versão leva `[!info]` com a baseline declarada.
- **Nada inventado:** proibido fabricar experiência do autor. As seções `Na prática (da minha experiência)` e `How to explain in English` do monólito ficam no tronco podado.
- **Sem quebra manual de linha.**
- **Manifestos YAML** completos e comentados onde o assunto pede — é o material que o leitor vai copiar e adaptar.

---

## Bloco 0 — Esqueleto

- [ ] Criar `Kubernetes/index.md` (MOC por fase, TL;DR com a lente, callout do sanduíche de quatro camadas, callout declarando o corte de autoscaling).
- [ ] Criar `Kubernetes/roadmap.md` (22 linhas, todas `📋`).
- [ ] Commit: `feat(infra): abre galho Kubernetes — index e roadmap`.

## Bloco 1 — Iniciado, o modelo (01-04) · parada de revisão ao fim

- [ ] **01 — O problema que orquestração resolve.** Parte da ponte já construída na nota 11 do galho Docker (Compose não reconcilia, roda num host só). O que muda quando são muitas máquinas e muitas réplicas. O que Kubernetes **não** é: não é PaaS, não é substituto de arquitetura, não é obrigatório.
- [ ] **02 — O loop de reconciliação.** A nota que carrega a lente, equivalente à 02 do Docker. Estado desejado × estado observado; o controller como laço infinito; `kubectl apply` não cria nada, escreve um objeto; nível-gatilho contra borda-gatilho. Diagrama do laço.
- [ ] **03 — O Pod, a unidade que não é o container.** Por que a unidade é o Pod e não o container; namespaces compartilhados dentro do Pod; sidecar e init container; por que Pod é descartável e quase nunca se cria um à mão.
- [ ] **04 — Deployment e ReplicaSet.** A cadeia de controllers: Deployment gerencia ReplicaSet, que gerencia Pods. Atualização como criação de ReplicaSet novo; histórico e rollback. Fronteira: a *estratégia* de deploy e o zero-downtime ficam em `Operação 3-03`.
- [ ] Gate + rastreio + commit + **parada de revisão**.

## Bloco 2 — Iniciado, organizar e falar com o cluster (05-07)

- [ ] **05 — Service.** Endereço estável para alvo instável; como o selector liga Service a Pods; os tipos (ClusterIP, NodePort, LoadBalancer) e o que cada um significa de verdade; Endpoints/EndpointSlice como o objeto que o kube-proxy consome.
- [ ] **06 — Namespaces, labels e selectors.** A organização do cluster; labels como o mecanismo que faz o modelo inteiro funcionar (é assim que controller acha Pod); annotations × labels; quotas e limites por namespace.
- [ ] **07 — `kubectl` é um cliente de API.** Tudo é HTTP contra o api-server; `apply` × `create` × `patch`; server-side apply e o campo de gerenciamento; `get -o yaml` para ver o objeto real com os defaults preenchidos; `explain` e `dry-run`.
- [ ] Gate + rastreio + commit.

## Bloco 3 — Adepto, configuração e cargas (08-11)

- [ ] **08 — ConfigMap e Secret.** Configuração fora da imagem (amarra com o galho Docker); as duas formas de consumir (variável e volume) e por que a segunda recarrega e a primeira não; Secret é base64, não criptografia — e o que resolve isso de verdade. Fronteira com `Operação 2-06`.
- [ ] **09 — Armazenamento.** PersistentVolume, PersistentVolumeClaim, StorageClass e provisionamento dinâmico; modos de acesso; o que acontece com o dado quando o Pod morre. Amarra com a nota 06 do Docker.
- [ ] **10 — StatefulSet.** Quando identidade importa: nome estável, disco próprio por réplica, ordem de criação e de término. Por que banco em Kubernetes é decisão, não default.
- [ ] **11 — Job, CronJob e DaemonSet.** As cargas que não são "servidor web": trabalho que termina, trabalho agendado, e um Pod por nó. Paralelismo e política de repetição em Job.
- [ ] Gate + rastreio + commit.

## Bloco 4 — Adepto, operar objetos (12-15) · parada de revisão ao fim

- [ ] **12 — Scheduling.** Como o scheduler escolhe o nó: filtragem e pontuação; nodeSelector, afinidade e antiafinidade; taints e tolerations; topology spread. Por que o Pod fica `Pending`.
- [ ] **13 — RBAC e ServiceAccount.** Identidade dentro do cluster; Role × ClusterRole e os bindings; a ServiceAccount que todo Pod recebe; princípio do menor privilégio aplicado ao cluster. Fronteira com `Engenharia/Auth e Identidade` (RBAC conceitual) e `Engenharia/Segurança`.
- [ ] **14 — Helm e Kustomize.** O problema de manter manifesto para N ambientes; template contra sobreposição; release e histórico no Helm; quando cada um serve. Fronteira: GitOps fica em `Operação 2-05`.
- [ ] **15 — Ingress e a borda do cluster.** O objeto Ingress e o controlador que o implementa — a separação que confunde todo mundo; regras por host e path; por que o objeto sozinho não faz nada. **Fronteira dura declarada:** Gateway API, mesh, NetworkPolicy e a operação da borda ficam em `Operação 3-05`.
- [ ] Gate + rastreio + commit + **parada de revisão**.

## Bloco 5 — Magus, o mecanismo (16-18)

- [ ] **16 — O control plane por dentro.** api-server como única porta para o etcd; etcd como a fonte da verdade; scheduler e controller-manager como clientes que observam e agem; o fluxo completo de um `kubectl apply` até o Pod rodando, com `sequenceDiagram`. Fronteira com `Cloud 12-05` (o que o provedor gerencia).
- [ ] **17 — O kubelet e o nó.** O agente que recebe a atribuição e conversa com o runtime via CRI; como o Pod vira container de verdade (amarra com a nota 15 do galho Docker: containerd e runc); cAdvisor e a origem das métricas; o que acontece quando o nó fica sem recurso (eviction).
- [ ] **18 — A API como sistema extensível: CRDs.** O api-server é genérico — ele não sabe o que é um Deployment, ele sabe servir recursos. CustomResourceDefinition, versionamento e conversão, validação por esquema, subrecursos. Por que quase toda ferramenta séria do ecossistema se instala como CRD.
- [ ] Gate + rastreio + commit.

## Bloco 6 — Magus, extensão e diagnóstico (19-21)

- [ ] **19 — Operators.** O padrão: CRD (o vocabulário) + controller (o loop) = conhecimento operacional codificado. O que um operator de banco faz que um Deployment não faz; níveis de maturidade; quando escrever um é exagero. Fecha o arco aberto na 18.
- [ ] **20 — Rede do cluster por dentro.** O modelo de rede plano que o Kubernetes exige; CNI como contrato de plugin; kube-proxy e como o Service vira regra de encaminhamento; DNS do cluster e o nome de serviço. **Fronteira:** operar a borda e mesh ficam em `Operação 3-05`.
- [ ] **21 — Depurar um cluster.** Método em ordem: eventos, condições do objeto, `describe` antes de `logs`. O catálogo do que dá errado — `Pending` (recurso, taint, volume), `CrashLoopBackOff`, `ImagePullBackOff`, `OOMKilled`, readiness que nunca fecha. Amarra com a nota 14 do galho Docker.
- [ ] Gate + rastreio + commit.

## Bloco 7 — Capstone (22)

- [ ] **22 — Capstone: do zero ao cluster.** Caso trabalhado, não resumo. Pega a imagem construída no capstone do galho Docker e a leva ao cluster, decidindo em voz alta: qual controller, como expor, onde a configuração mora, o que persiste, como atualizar sem derrubar, como investigar quando não sobe. Cada decisão cita a nota que a fundamenta. Fecha nomeando o que fica em Operação.
- [ ] Gate + commit.

## Bloco 8 — Fechamento

- [ ] Podar `Kubernetes.md` (1612 linhas) para tronco com tabela de redirecionamento, preservando **literalmente** `Na prática (da minha experiência)` e `How to explain in English`.
- [ ] Callouts de volta em `Operação 3-02`, `3-03`, `3-04` (o corte de autoscaling visto do outro lado), `3-05` e `Cloud 12-05`.
- [ ] Atualizar `Infraestrutura/index.md`, `Infraestrutura/roadmap.md` e o Roadmap central.
- [ ] Gate de wikilinks em toda a pasta.
- [ ] Commit e pergunta ao usuário sobre abrir o galho 3 (Nginx).

## O que fica fora

- **M1 (mídia):** passada posterior, busca e verificação centrais via `yt-dlp`.
- **Autoscaling:** cortado por redundância com `Operação 3-04` — decisão registrada, não esquecimento.
- **Escrever um operator na prática:** se o assunto pedir, entra depois como **broto** (nota `19a`, `fase: Magus`), sem renumerar o galho.

## Governança de custo

Sonnet para escrita, teto de 3 subagentes por bloco, gate por script antes de cada commit. O galho anterior custou ~1,2M tokens de subagente para 18 notas; este tem 22 e deve ficar na mesma ordem de grandeza.
