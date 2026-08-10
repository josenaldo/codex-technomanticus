---
title: "Roadmap — Kubernetes"
created: 2026-08-03
updated: 2026-08-09
type: meta
publish: false
tags:
  - meta
  - roadmap
  - infraestrutura
  - kubernetes
---

# Roadmap — Kubernetes (galho 2 de Infraestrutura)

Roadmap-folha do galho `Tecnologia/Infraestrutura/Kubernetes`. Segundo galho do domínio, aberto em 2026-08-03. Design: [[00-Meta/specs/2026-08-02-dominio-infraestrutura-design|design do domínio]] · Plano: [[00-Meta/specs/2026-08-03-galho-kubernetes-plano|plano de execução]].

**Lente:** o loop de reconciliação — Kubernetes não executa comandos, converge estado.

**Legenda:** ✅ escrita + M1 · 🔶 escrita, falta M1 · 📋 desenhada, não escrita.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 22 |
| 📋 desenhadas | 0 |
| 🔶 escritas (falta M1) | 18 |
| ✅ completas | 4 |
| % escrito | 100% |
| M1 (mídia) | 4/22 — em andamento |

## Notas

| # | Nota | Fase | Estado | Bloco |
|---|------|------|--------|-------|
| 01 | O problema que orquestração resolve | Iniciado | 🔶 | 1 |
| 02 | O loop de reconciliação | Iniciado | ✅ | 1 |
| 03 | O Pod, a unidade que não é o container | Iniciado | 🔶 | 1 |
| 04 | Deployment e ReplicaSet | Iniciado | 🔶 | 1 |
| 05 | Service | Iniciado | 🔶 | 2 |
| 06 | Namespaces, labels e selectors | Iniciado | 🔶 | 2 |
| 07 | kubectl é um cliente de API | Iniciado | 🔶 | 2 |
| 08 | ConfigMap e Secret | Adepto | 🔶 | 3 |
| 09 | Armazenamento — PV, PVC e StorageClass | Adepto | 🔶 | 3 |
| 10 | StatefulSet | Adepto | 🔶 | 3 |
| 11 | Job, CronJob e DaemonSet | Adepto | 🔶 | 3 |
| 12 | Scheduling | Adepto | 🔶 | 4 |
| 13 | RBAC e ServiceAccount | Adepto | 🔶 | 4 |
| 14 | Helm e Kustomize | Adepto | 🔶 | 4 |
| 15 | Ingress e a borda do cluster | Adepto | 🔶 | 4 |
| 16 | O control plane por dentro | Magus | ✅ | 5 |
| 17 | O kubelet e o nó | Magus | ✅ | 5 |
| 18 | A API como sistema extensível — CRDs | Magus | 🔶 | 5 |
| 19 | Operators | Magus | 🔶 | 6 |
| 20 | Rede do cluster por dentro | Magus | ✅ | 6 |
| 21 | Depurar um cluster | Magus | 🔶 | 6 |
| 22 | Capstone — do zero ao cluster | Magus | 🔶 | 7 |

## Corte deliberado

> [!warning] Autoscaling NÃO entra neste galho
> HPA, VPA, KEDA e Cluster Autoscaler estão cobertos com profundidade em [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/04 - Escala e capacidade|Operação 3-04]] — as três camadas, capacity planning, reactive × predictive, thundering herd. Escrever aqui produziria versão pior. O `index.md` do galho declara o corte com ponteiro, para que quem procure encontre o caminho e não o silêncio. **Isto é decisão registrada, não esquecimento.**

> [!warning] O broto `19a` (escrever um operator na prática) NÃO será escrito
> O plano previa um broto opcional com o passo a passo de construir um operator (`kubebuilder init`, layout de projeto, geração de CRD a partir de struct tags, `envtest`). Decidido em 2026-08-04 que ele **não entra**: a lente deste galho é *a ferramenta por dentro, para quem vai operá-la*, e um tutorial de autoria de controller em Go é outro ofício — duplicaria o livro oficial do Kubebuilder sem acrescentar leitura própria, e caberia melhor na trilha de Go. A nota 19 entrega o que este galho precisa: a forma do laço, a função de cada peça (finalizers, ownerReferences, status.conditions, requeue) com esboço comentado de `Reconcile`, o modelo de maturidade, e a seção honesta de quando escrever um operator é exagero. **Isto é decisão registrada, não esquecimento.**

## Fronteiras a respeitar

| Vizinho | Fica lá | Fica aqui |
|---|---|---|
| `Operação 3-02` | contrato de runtime (probes, requests/limits, shutdown) | os objetos e o loop que os reconcilia |
| `Operação 3-03` | zero-downtime, readiness gating, connection draining | Deployment/ReplicaSet como mecanismo de atualização |
| `Operação 3-04` | **autoscaling inteiro** | — (nada) |
| `Operação 3-05` | Gateway API, mesh, NetworkPolicy, operar a borda | Ingress como objeto + controlador; CNI/kube-proxy/DNS |
| `Operação 2-05` | GitOps e IaC | Helm e Kustomize como empacotamento |
| `Cloud 12-05` | o que o provedor gerencia do control plane | o control plane por dentro |
| `Ciência/SO 13` | namespaces e cgroups no kernel | kubelet → CRI → runtime |
| `Auth e Identidade` | RBAC/ABAC/ReBAC conceitual | RBAC do Kubernetes como objeto |

## Material a consumir

| Fonte | Onde | Aproveitamento |
|---|---|---|
| `Infraestrutura/Kubernetes.md` | 1612 linhas | semente principal, o maior monólito da estante; vira tronco podado no bloco 8 |
| `Infraestrutura/WSL, Docker e Kubernetes.md` | 144 linhas | referência de ambiente local, permanece |

> [!warning] Regra de conteúdo
> `Na prática (da minha experiência)` e `How to explain in English` do monólito são relato pessoal do autor e material de entrevista. Ficam no tronco podado e **não migram** para as notas.

## Pendências

- **Escrita:** ✅ **22/22 COMPLETA** (2026-08-04). Blocos 1-7 do plano executados.
- **M1 (mídia):** passada posterior, verificação central via `yt-dlp`.
- **Poda e callouts de volta:** bloco 8 do plano.
- **Referências textuais:** ✅ resolvidas em 2026-08-04 — as 19 citações em texto puro à fase Magus viraram wikilink.
- **Broto `19a` — DESCARTADO (decisão de 2026-08-04).** Ver "Corte deliberado" abaixo.

## Notas de execução

- Galho aberto em 2026-08-03, na sequência direta do fechamento do galho Docker. A ponte narrativa já existia: a nota 11 do Docker desenvolve, no corpo, por que Compose não reconcilia estado — e é daí que a nota 01 deste galho parte.

## M1 — mídia embutida e descartes

| Nota | Vídeo | ID | Canal | Âncora |
|---|---|---|---|---|
| 02 | Level Triggering and Reconciliation in Kubernetes | `tCht7FvIDdY` | James Bowes, 25 min | 12:59 |
| 16 | Protecting Your Control Plane: kube-apiserver Memory Exhaustion | `1Jno9-3DdA4` | Cloud Native Days Austria, 32 min | 20:28 |
| 20 | Liberating Kubernetes From Kube-proxy and Iptables | `bIRwSIwNHC0` | CNCF / KubeCon, 35 min | 28:54 |
| 17 | Everything You Ever Wanted to Know About Resource Scheduling | `nWGkvrIPqJ4` | CNCF / KubeCon, Tim Hockin, 43 min | 18:49 |

> [!warning] Critério aplicado neste galho
> **Views baixas não reprovam sozinhas.** Palestra técnica de nicho legitimamente tem pouca audiência — `tCht7FvIDdY` tem 555 views e é uma palestra real e substancial. O que reprova é fazenda de conteúdo: vídeo curto, sem autoria identificável, com alinhamento raso. Reprovados aqui por esse critério: `ARH6jjMQNeM` (41 views) · `JNe1gzVCMIo` (205 views, 5,6 min).
>
> **Legenda automática degradada** nos embutidos (garbla `kubectl` como "cube control", `pods` como "ports", `1.33` como "133"). A citação de destaque foi escolhida entre os trechos limpos, e as notas 02 e 20 trazem aviso explícito ao leitor.
>
> **Fato duro verificado na fonte antes de escrever** (lição do galho Nginx): a correção citada na nota 16 é o KEP-5116 da SIG API Machinery — codificação em streaming de respostas `LIST`, beta habilitado por padrão na 1.33, estável previsto para 1.34, pico de memória de ~70 GB para ~3 GB. Confirmado no blog oficial do projeto, não só na palestra. Mesmo procedimento na nota 17: os valores de `oom_score_adj` por classe de QoS (`Guaranteed` -997, `BestEffort` 1000, `Burstable` por fórmula) foram confirmados fora da palestra antes de entrar na nota, junto com a ressalva de que o *OOM killer* do kernel ignora `PriorityClass`.
>
> **Ressalva de idade registrada dentro do callout** quando o vídeo é anterior à baseline da nota: `bIRwSIwNHC0` é de 2019 e não conhece o modo `nftables` (GA na 1.33); `nWGkvrIPqJ4` é de 2016, e embora o modelo de `requests`/`limits` siga inalterado, números e flags citados de passagem envelheceram.
>
> **Rate limit do YouTube** (`Sign in to confirm you're not a bot`) interrompeu a passada de 2026-08-09 por um intervalo. Não é link morto e não descarta candidato — é motivo para pausar e retomar. Foi o que aconteceu com a palestra do Hockin, rejeitada por engano antes de ser revalidada e, depois, embutida.

## Próximos alvos de M1

Prioridade nas conceituais profundas, onde o rendimento se concentra: **03** (o Pod e o container `pause`), **18** (API extensível, CRD e admission), **19** (Operators), **12** (scheduling). As notas de uso cotidiano (**05**-**11**, **14**) tendem a só ter tutorial genérico — esperar rendimento baixo e não forçar.
