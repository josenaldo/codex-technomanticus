---
title: "Kubernetes"
created: 2026-08-03
updated: 2026-08-03
type: moc
status: growing
publish: true
tags:
  - moc
  - infraestrutura
  - kubernetes
  - orquestracao
aliases:
  - "Kubernetes (galho)"
  - "Galho Kubernetes"
  - "K8s"
---

# Kubernetes

> [!abstract] TL;DR
> Segundo galho do domínio [[03-Dominios/Tecnologia/Infraestrutura/index|Infraestrutura]], sob a lente **o loop de reconciliação**: o Kubernetes não executa comandos, ele **converge estado**. `kubectl apply` não cria nada — escreve um objeto no armazenamento do cluster e vai embora; controllers observam a diferença entre o que você declarou e o que existe, e agem para fechar essa distância. Entendido isso, o modelo de objetos inteiro deixa de ser decoreba e o comportamento estranho ("por que meu Pod voltou sozinho?", "por que ele está `Pending`?") vira consequência previsível. O galho sobe do modelo declarativo aos objetos do dia a dia e fecha no mecanismo — control plane, kubelet, CRDs e operators. 22 notas, 3 fases.

## Sobre este galho

O galho anterior fechou apontando para cá. A nota [[03-Dominios/Tecnologia/Infraestrutura/Docker/11 - Compose como ambiente de desenvolvimento|Compose como ambiente de desenvolvimento]] desenvolve, no corpo, o argumento que motiva orquestração: o Compose aplica o que você mandou e vai embora, roda numa máquina só, e não tem atualização progressiva nem descoberta entre máquinas. Este galho é a resposta a essas quatro lacunas.

O recorte não é tutorial de `kubectl`. É o modelo que permite prever o comportamento — o mesmo critério do galho de Docker, aplicado a um sistema bem maior.

**Audiência primária:** quem já tem manifestos rodando e os trata como configuração mágica. **Audiência secundária:** quem vai responder, num loop sênior, o que acontece entre `kubectl apply` e o container existir.

> [!info] Fronteira — o sanduíche de quatro camadas
> | Camada | Casa | Pergunta que responde |
> |---|---|---|
> | Mecanismo | [[03-Dominios/Ciência/Sistemas Operacionais/13 - Virtualização e containers\|Ciência/Sistemas Operacionais]] | como o isolamento funciona no kernel |
> | **A ferramenta** | **este galho** | **como o Kubernetes funciona por dentro** |
> | O ofício | [[03-Dominios/Engenharia/Operação/index\|Engenharia/Operação]] | o que muda quando é produção |
> | A plataforma | [[03-Dominios/Tecnologia/Cloud/12 - Containers gerenciados/05 - Kubernetes gerenciado de raspão\|Cloud, galho 12]] | quando o provedor opera o control plane |

> [!warning] Autoscaling não está neste galho — e isso é deliberado
> HPA, VPA, KEDA e Cluster Autoscaler estão cobertos em [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/04 - Escala e capacidade|Operação — Escala e capacidade]], com as três camadas, capacity planning e os efeitos colaterais de escalar rápido. Escrever o assunto aqui produziria uma versão pior do que já existe. O mesmo vale para **Gateway API, service mesh e NetworkPolicy**, que vivem em [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/05 - Rede e borda em produção|Rede e borda em produção]]: aqui fica o Ingress como objeto e a rede como mecanismo, lá fica a operação da borda.

## Iniciado — o modelo declarativo

1. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/01 - O problema que orquestração resolve|01 — O problema que orquestração resolve]] — o que muda quando são muitas máquinas e muitas réplicas, e as três coisas que o Kubernetes não é.
2. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/02 - O loop de reconciliação|02 — O loop de reconciliação]] — **a nota que carrega a lente**: `spec` contra `status`, o controller como laço infinito, e por que nível-gatilho explica a resiliência inteira.
3. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/03 - O Pod, a unidade que não é o container|03 — O Pod, a unidade que não é o container]] — o que os containers de um Pod compartilham, sidecar e init container, e por que o Pod é descartável por design.
4. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/04 - Deployment e ReplicaSet|04 — Deployment e ReplicaSet]] — a cadeia de controllers, a atualização como criação de um ReplicaSet novo, e o que `rollout undo` de fato faz.
5. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/05 - Service|05 — Service]] — o endereço estável para alvo instável; o selector que vira EndpointSlice, os quatro tipos e o DNS do cluster.
6. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/06 - Namespaces, labels e selectors|06 — Namespaces, labels e selectors]] — labels como o mecanismo de ligação do modelo: a relação controller↔Pod é derivada por consulta, não por posse.
7. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/07 - kubectl é um cliente de API|07 — `kubectl` é um cliente de API]] — ver o HTTP com `-v=8`, os tipos de patch, server-side apply e posse de campo, `explain` e dry-run.

## Adepto — os objetos do dia a dia

8. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/08 - ConfigMap e Secret|08 — ConfigMap e Secret]] — configuração fora da imagem; por que volume recarrega e variável de ambiente não, e por que Secret é codificação, não criptografia.
9. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/09 - Armazenamento|09 — Armazenamento: PV, PVC e StorageClass]] — o pedido, o recurso e a receita; provisionamento dinâmico como mais um laço, modos de acesso e política de recuperação.
10. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/10 - StatefulSet|10 — StatefulSet]] — quando identidade importa: nome ordinal, disco próprio por réplica e ordem; por que banco em Kubernetes é decisão, não default.
11. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/11 - Job, CronJob e DaemonSet|11 — Job, CronJob e DaemonSet]] — o mesmo laço com outra definição de estado desejado: trabalho que termina, trabalho agendado e um Pod por nó.
12. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/12 - Scheduling|12 — Scheduling]] — filtragem e pontuação, afinidade, taints e espalhamento topológico; o catálogo de por que um Pod fica `Pending`.
13. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/13 - RBAC e ServiceAccount|13 — RBAC e ServiceAccount]] — quem você é contra o que você pode; a matriz Role/ClusterRole, e por que RBAC é puramente aditivo.
14. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/14 - Helm e Kustomize|14 — Helm e Kustomize]] — template contra sobreposição, as duas filosofias de manter N variantes do mesmo manifesto; nenhuma das duas reconcilia nada.
15. [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/15 - Ingress e a borda do cluster|15 — Ingress e a borda do cluster]] — o objeto que não faz nada sem controlador; annotations como válvula de escape, e a Gateway API como sucessora.

## Magus — o mecanismo

16. O control plane por dentro
17. O kubelet e o nó
18. A API como sistema extensível — CRDs
19. Operators
20. Rede do cluster por dentro
21. Depurar um cluster
22. Capstone — do zero ao cluster

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Infraestrutura/Kubernetes" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Infraestrutura/index|Infraestrutura]] — MOC do domínio
- [[03-Dominios/Tecnologia/Infraestrutura/Docker/index|Docker]] — o galho anterior; a imagem que este galho agenda
- [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/02 - O contrato de produção do Kubernetes|O contrato de produção do Kubernetes]] — a política que este galho pressupõe conhecida
- [[Kubernetes]] — o monólito de referência que originou este galho
