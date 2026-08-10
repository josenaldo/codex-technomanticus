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
| 03 | Pods and Containers — Kubernetes Networking | `5cNrTU6o3Fw` | TechWorld with Nana, 14 min | 11:46 |
| 05 | Kubernetes — Kube Proxy — iptables mode | `6azrY0F1x3s` | JOMO Developer, 13 min | 10:53 |
| 07 | Using mitmproxy to understand what kubectl does | `30a0WrfaS2A` | Maël Valais, 11 min | — |
| 09 | Kubernetes Volumes explained (PV, PVC, StorageClass) | `0swOh5C3OVM` | TechWorld with Nana, 21 min | — |
| 10 | Kubernetes StatefulSet simply explained | `pPQKAR1pA9U` | TechWorld with Nana, 16 min | — |
| 12 | How Scheduling in Kubernetes Works | `0FvQR-0tK54` | CNCF / KubeCon, GoJek, 20 min | 18:30 |
| 13 | Understanding Kubernetes RBAC | `jvhKOAyD8S8` | That DevOps Guy, 33 min | — |
| 18 | What are Custom Resource Definitions (CRDs) | `TScDYMym7LA` | CookNCode, 9 min | — |
| 19 | Kubernetes Operator simply explained | `ha3LjlD6g7g` | TechWorld with Nana, 10 min | — |

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

**Rodada de 2026-08-09: +9 notas, galho vai de 4/22 para 13/22.** Os quatro alvos prioritários previstos aqui (**03**, **18**, **19**, **12**) foram todos fechados.

**A previsão de rendimento baixo para as notas de uso cotidiano estava errada, e vale corrigir o registro.** As notas **05**, **09** e **10** renderam material forte — três deles do canal TechWorld with Nana, com centenas de milhares de visualizações e conteúdo que não é tutorial genérico: o vídeo da 05 lista as regras de `iptables` num nó e lê as **probabilidades encadeadas** que produzem a distribuição; o da 09 traz a divisão de trabalho administrador/desenvolvedor que explica por que o modelo tem três peças; o da 10 chega às três garantias partindo do que quebraria num banco replicado sob Deployment. A lição é a mesma que o galho Nginx aprendeu por outro caminho: **o que decide não é o assunto ser "cotidiano" ou "profundo", é existir um canal com autoridade cobrindo aquele ângulo** — no Kubernetes existe, no Nginx de configuração não existia.

**Exceção declarada à régua de autoridade, na nota 07:** `30a0WrfaS2A` tem poucas centenas de visualizações. Entrou por três motivos escritos dentro do próprio callout — autor contribuidor do ecossistema (cert-manager), ângulo inédito (observar o `kubectl` de fora, como tráfego interceptado por mitmproxy), e técnica reprodutível por quem assiste, o que troca autoridade de canal por verificabilidade.

**Restam 9 notas:** 01, 04, 06, 08, 11, 14, 15, 21, 22. Candidatos já levantados e com transcrição baixada, aguardando leitura e inserção: **14** `ZMFYSm0ldQ0` (Helm vs Kustomize — templating contra patching, 34 min, 33 mil views) · **15** `xaZ87iSvMAI` (Gateway API Explained, KodeKloud, 45 min, 51 mil) · **21** `QtXHkzLtqZE` (A Basic Kubernetes Debugging Kit — curl, jq, openssl, CNCF, 33 min). As notas 01, 04, 06, 08, 11 e 22 ainda não tiveram rodada de busca.
