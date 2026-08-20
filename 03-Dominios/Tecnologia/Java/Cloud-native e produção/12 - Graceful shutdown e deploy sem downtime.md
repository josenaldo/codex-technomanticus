---
title: "Graceful shutdown e deploy sem downtime"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - cloud-native
  - adepto
  - kubernetes
  - deploy
aliases:
  - "Graceful shutdown"
  - "Deploy sem downtime"
---

# Graceful shutdown e deploy sem downtime

> [!abstract] TL;DR
> Quando o orquestrador manda uma instância morrer, ela recebe um `SIGTERM`. Se a aplicação cair na hora, toda requisição em andamento vira erro 500 para o usuário. O **graceful shutdown** resolve isso: a aplicação para de aceitar conexões novas, **deixa as requisições em voo terminarem** dentro de um prazo (o *grace period*), e só então desliga. No Spring Boot, `server.shutdown=graceful` é o **default** e o prazo é `spring.lifecycle.timeout-per-shutdown-phase` (**30s** por padrão). Mas o desligamento limpo da aplicação **não basta**: existe uma *race condition* entre o desligamento e o load balancer ainda mandando tráfego. A coordenação correta envolve **`preStop` hook**, **`terminationGracePeriodSeconds` maior que o timeout** e a readiness virando `REFUSING_TRAFFIC` para o k8s parar de rotear. Por cima disso, **rolling / blue-green / canary** garantem que sempre haja instâncias saudáveis recebendo tráfego — é assim que se faz deploy sem downtime.

## O que é

**Graceful shutdown** (desligamento gracioso) é o processo de encerrar uma aplicação de forma ordenada: em vez de morrer no meio de uma requisição, ela termina o que está fazendo antes de desligar.

Pense num restaurante que vai fechar. O jeito brutal seria apagar as luzes e empurrar todo mundo para fora — inclusive quem está no meio do prato. O jeito gracioso é **trancar a porta da entrada** (ninguém novo entra), **deixar quem já está dentro terminar de comer**, e só então fechar. O prazo que você dá para isso é o *grace period*: depois de X minutos, mesmo quem não terminou tem que sair.

Em termos técnicos, quando o orquestrador (Kubernetes, por exemplo) decide remover uma instância, ele envia o sinal **`SIGTERM`** ao processo. A aplicação pode:

- **Ignorar e morrer na hora** (ou ser morta por `SIGKILL`) → requisições em voo viram erro.
- **Tratar o sinal graciosamente** → para de aceitar conexões novas, deixa as ativas terminarem, libera recursos (`@PreDestroy`) e sai com código zero.

**Deploy sem downtime** é o problema maior do qual o graceful shutdown é uma peça: como substituir a versão antiga da aplicação pela nova **sem que nenhum usuário veja um erro** durante a troca.

## Por que importa

Em produção, instâncias são gado, não bicho de estimação: elas sobem, descem, são substituídas e movidas o tempo todo. Todo deploy, todo *autoscaling* para baixo, toda realocação de pod **mata instâncias**. Se cada morte de instância derruba requisições, sua taxa de erro fica refém da frequência de deploys.

O custo de não fazer isso direito:

- **Erros visíveis ao usuário** a cada deploy (500s, conexões cortadas).
- **Transações corrompidas** — uma operação interrompida na metade pode deixar dado inconsistente.
- **Mensagens perdidas** — um consumidor de fila morto no meio do processamento pode perder ou reprocessar mensagens.
- **SLA furado** — se você promete 99,9% de disponibilidade, não pode se dar ao luxo de gerar erros toda vez que faz deploy (e times maduros fazem deploy várias vezes ao dia).

O graceful shutdown é o que torna deploys **invisíveis**. É a diferença entre "fizemos deploy às 14h" e "alguns usuários receberam erro às 14h".

## Como funciona

### Graceful shutdown no Spring Boot e o timeout

No Spring Boot, graceful shutdown é o **comportamento padrão** desde a versão 2.3, para os três servidores embarcados (Tomcat, Jetty, Reactor Netty), tanto em aplicações servlet quanto reativas. A propriedade equivalente é:

```properties
server.shutdown=graceful
```

O desligamento ocorre como parte do fechamento do `ApplicationContext`, na fase mais cedo de parada dos beans `SmartLifecycle`. Durante o *grace period*:

- **Requisições em andamento** podem completar normalmente.
- **Requisições novas** são rejeitadas na camada de rede (o servidor para de aceitar conexões).

O prazo é controlado por:

```properties
spring.lifecycle.timeout-per-shutdown-phase=30s
```

O **default é 30 segundos**. Se as requisições em voo não terminarem dentro desse prazo, elas são cortadas e o desligamento prossegue. Para desabilitar o comportamento gracioso, usa-se `server.shutdown=immediate`.

> [!tip] Por que "per-shutdown-phase"?
> O `SmartLifecycle` do Spring organiza o desligamento em **fases**. O timeout não é o tempo total de shutdown — é o tempo máximo de **cada fase**. A fase do servidor web (parar de aceitar requisições e drenar as ativas) é a primeira; depois vêm outras fases como fechamento de pools e conexões.

### SIGTERM, preStop hook e a race condition de roteamento

Aqui mora a armadilha mais sutil. Quando o Kubernetes remove um pod, **várias coisas acontecem em paralelo**, não em sequência:

- O pod recebe `SIGTERM` e começa o graceful shutdown.
- O endpoint do pod é **removido do Service/Endpoints**, e a partir daí o load balancer/kube-proxy para de mandar tráfego.

O problema: essas duas coisas são **assíncronas e concorrentes**. A propagação da remoção do endpoint pelos nós do cluster leva um tempinho. Existe uma janela em que **o pod já recebeu `SIGTERM` (e talvez já parou de aceitar conexões), mas o load balancer ainda acha que ele é um destino válido** e manda requisições para ele → o usuário recebe *connection refused*.

A mitigação é o **`preStop` hook**: um gancho que o Kubernetes executa **antes** de enviar o `SIGTERM`. Colocando um `sleep` ali (ex.: 5–10s), você dá tempo para a remoção do endpoint se propagar **antes** de a aplicação começar a desligar:

```text
preStop sleep (5s)  →  SIGTERM  →  graceful shutdown (drena requests)  →  exit
       ↑
   nessa janela, o LB para de mandar tráfego novo
```

A ordem efetiva fica:

1. Kubernetes inicia a remoção do pod → dispara `preStop` **e** começa a desregistrar o endpoint (em paralelo).
2. Durante o `sleep` do `preStop`, o desregistro do endpoint se propaga — o LB para de rotear.
3. Terminado o `preStop`, o `SIGTERM` chega à aplicação.
4. Graceful shutdown drena as últimas requisições em voo.

> [!warning] terminationGracePeriodSeconds > timeout
> O `terminationGracePeriodSeconds` (default **30s** no k8s) é o tempo **total** que o Kubernetes espera entre o início da remoção e o `SIGKILL` forçado — e esse relógio **inclui o `preStop`**. Ele precisa ser **maior** que `preStop sleep + timeout-per-shutdown-phase`. Se for menor, o `SIGKILL` chega no meio do graceful shutdown e corta tudo — anulando todo o esforço. Ex.: `preStop=5s` + `timeout=30s` → `terminationGracePeriodSeconds` deve ser ≥ 40s, com folga.

### Readiness REFUSING_TRAFFIC e as estratégias de deploy

O Spring Boot integra o graceful shutdown com o **gerenciamento de disponibilidade** (`AvailabilityState`). Quando o shutdown começa, o estado de readiness vira **`REFUSING_TRAFFIC`**, o que faz o endpoint de **readiness probe** responder **503 (OUT_OF_SERVICE)**. Isso sinaliza ativamente ao Kubernetes: *"não me mande mais tráfego"* — reforçando o desregistro e fechando a janela da race condition por outro caminho.

Mas drenar uma instância é só metade. Para **trocar** a versão sem downtime, é preciso uma **estratégia de deploy** que garanta instâncias saudáveis o tempo todo:

| Estratégia | Como funciona | Trade-off |
| --- | --- | --- |
| **Rolling update** | Substitui instâncias aos poucos: sobe N novas, drena N antigas, repete até trocar todas. | Padrão do k8s, simples; mas as duas versões **coexistem** durante a troca (precisa compatibilidade). |
| **Blue-green** | Sobe o ambiente novo (green) **inteiro** ao lado do antigo (blue); troca o tráfego de uma vez; mantém o blue de prontidão para rollback. | Rollback instantâneo; mas **dobra o custo de infra** durante a janela. |
| **Canary** | Manda uma **fração pequena** do tráfego (ex.: 5%) para a versão nova; observa métricas; aumenta gradualmente se estiver saudável. | Detecta problema com baixo *blast radius*; mas exige roteamento ponderado e boa observabilidade. |

As três **dependem** do graceful shutdown funcionar: drenar a instância antiga sem cortar requisições é o que torna a troca invisível.

## Na prática

**1. Configuração do graceful shutdown (Spring Boot):**

```yaml
server:
  shutdown: graceful   # já é o default, mas explícito documenta a intenção

spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s   # grace period (default 30s)
```

**2. Coordenação no Deployment do Kubernetes:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pedidos-service
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0      # nunca derruba mais que o necessário
      maxSurge: 1            # sobe uma instância nova antes de drenar a antiga
  template:
    spec:
      terminationGracePeriodSeconds: 45   # > preStop(5s) + timeout(30s), com folga
      containers:
        - name: pedidos
          image: registry.exemplo.com/pedidos:1.4.0
          lifecycle:
            preStop:
              exec:
                command: ["sh", "-c", "sleep 5"]   # janela p/ o LB parar de rotear
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            periodSeconds: 5
```

**3. Cleanup de recursos com `@PreDestroy`:**

```java
import jakarta.annotation.PreDestroy;
import org.springframework.stereotype.Component;

@Component
public class ConexaoExternaManager {

    private final ClienteRemoto cliente;

    public ConexaoExternaManager(ClienteRemoto cliente) {
        this.cliente = cliente;
    }

    /**
     * Executado durante o fechamento do ApplicationContext,
     * depois que o servidor web drenou as requisições em voo.
     * Bom lugar para fechar conexões, flush de buffers, etc.
     */
    @PreDestroy
    public void liberarRecursos() {
        cliente.flushPendentes();   // garante que nada fica pela metade
        cliente.fechar();           // libera sockets/threads
    }
}
```

> [!note] A ordem importa
> O `@PreDestroy` roda **depois** do drain do servidor web (são fases diferentes do `SmartLifecycle`). Isso é bom: você fecha conexões externas só quando tem certeza de que nenhuma requisição em voo ainda precisa delas.

## Armadilhas

### (1) SIGTERM cortando requisições sem graceful shutdown

Se o graceful shutdown estiver desabilitado (`server.shutdown=immediate`) ou se você usa um servidor/runtime que não trata `SIGTERM`, o sinal mata o processo **na hora**. Toda requisição em voo vira erro. O sintoma clássico: a taxa de 500s **sobe a cada deploy** e some logo depois. No Spring Boot moderno isso já vem resolvido por default — mas vale confirmar que ninguém colocou `immediate` "para os testes rodarem mais rápido".

### (2) terminationGracePeriodSeconds < timeout → SIGKILL corta o graceful

Esta é a armadilha mais comum e mais traiçoeira, porque a config parece certa. Você aumenta o `timeout-per-shutdown-phase` para 60s (porque tem requisições longas), mas esquece de aumentar o `terminationGracePeriodSeconds`, que continua nos 30s padrão. Resultado: aos 30s, o Kubernetes manda `SIGKILL` e **corta o graceful shutdown pela metade** — exatamente o que você tentou evitar. **Regra de ouro:** `terminationGracePeriodSeconds` ≥ `preStop sleep` + `timeout-per-shutdown-phase`, sempre com folga.

### (3) ENTRYPOINT em shell-form não propaga SIGTERM

Mesmo com tudo configurado certo, o graceful shutdown **nunca dispara** se o `SIGTERM` não chega ao processo Java. Isso acontece quando o `ENTRYPOINT` do Dockerfile está em **shell-form** (`ENTRYPOINT java -jar app.jar`): o shell vira PID 1 e recebe o sinal, mas **não o repassa** ao Java filho. A aplicação só morre quando o `SIGKILL` chega — sem chance de drenar nada. A correção é usar **exec-form** (`ENTRYPOINT ["java", "-jar", "app.jar"]`), que coloca o Java como PID 1 diretamente. Veja [[03-Dominios/Tecnologia/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar|Dockerfile na prática]] para o detalhe de propagação de sinais.

## Em entrevista

### Frase pronta (inglês)

> Graceful shutdown is non-negotiable for zero-downtime deployments. When Kubernetes terminates a pod, it sends a SIGTERM, and Spring Boot — where graceful shutdown is the default — stops accepting new connections while letting in-flight requests finish within the configured grace period, which is thirty seconds by default. The subtle part is the race condition: deregistering the pod from the load balancer is concurrent with the shutdown, so I add a preStop hook with a short sleep to let the endpoint removal propagate before SIGTERM arrives, and I make sure terminationGracePeriodSeconds is larger than the shutdown timeout, otherwise SIGKILL cuts the drain short. On top of that, the deployment strategy — rolling, blue-green, or canary — is what keeps healthy instances serving traffic throughout the rollout.

### Vocabulário

| Português | Inglês |
| --- | --- |
| desligamento gracioso | graceful shutdown |
| gancho pré-término | preStop hook |
| período de graça | grace period |
| sinal de término | SIGTERM |
| sem tempo de inatividade | zero-downtime |
| implantação canário | canary deployment |
| drenar requisições em voo | drain in-flight requests |
| condição de corrida | race condition |

## Veja também

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar|Dockerfile na prática]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/10 - Health e probes — o contrato com o orquestrador|Health e probes]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/20 - CI-CD e o caminho até produção|CI/CD e o caminho até produção]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Spring Boot Reference — Graceful Shutdown: https://docs.spring.io/spring-boot/reference/web/graceful-shutdown.html
- Spring Boot How-to — Deploying to the Cloud (Kubernetes, preStop, terminationGracePeriodSeconds): https://docs.spring.io/spring-boot/how-to/deployment/cloud.html
