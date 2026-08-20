---
title: "Lazydocker — debugging avançado e docker-compose"
created: 2026-05-21
updated: 2026-05-21
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - terminal
  - tuis
  - lazydocker
  - magus
  - debugging
  - docker-compose
aliases:
  - Lazydocker debugging
---

# Lazydocker — debugging avançado e docker-compose

> [!abstract] TL;DR
> Magus em Lazydocker: stack docker-compose mostrado como grupo com dependências; `enter` em container abre Config (env vars, ports, mounts), Top (processes), Stats (CPU/mem live). Logs: tail automático, `m` para fullscreen, `logs.since`/`logs.tail` controlam buffer. Exec custom via `customCommands` para shell preferido com fallback. Debug crash loop: olhar restart count + tail logs + Config. Health checks visíveis (`(healthy)`, `(unhealthy)`, `(starting)`). Compose overrides (`docker-compose.override.yml`) auto-carregados pelo daemon — Lazydocker reflete o estado resultante.

## O que é / Como funciona

### Stack docker-compose no Lazydocker

Quando Lazydocker é iniciado no mesmo diretório que contém um `docker-compose.yml` ou `compose.yaml`, o daemon Docker Compose é detectado automaticamente e o painel Project exibe `compose detected`.

Comportamento com compose ativo:

- **Painel Project** (tecla `1`) mostra o nome do projeto e estado geral
- **Painel Services** (tecla `2`) agrupa containers por service name (`api`, `db`, `cache`, ...)
- Cada service exibe status agregado: `running`, `exited`, ou `restarting` com contador de containers
- Navegar com `j`/`k` entre services; `enter` expande o service e foca no painel de conteúdo
- Operações de service usam `docker compose` por trás (configurável via `commandTemplates.dockerCompose`)

Teclas de operação no painel Services:

| Tecla | Ação |
|---|---|
| `u` | Up service (`docker compose up -d <service>`) |
| `S` | Start service |
| `s` | Stop service |
| `r` | Restart service |
| `d` | Remove containers do service |
| `U` | Up project inteiro |
| `D` | Down project inteiro |
| `E` | Exec shell no container do service |
| `m` | View logs do service |

> [!note]
> Sem `docker-compose.yml` no cwd, o painel Services fica vazio e os containers aparecem soltos no painel Containers (tecla `3`). Se isso acontecer inesperadamente, verificar o diretório de trabalho.

### Inspect verboso

Selecionar um container individual (painel Containers, tecla `3`) e pressionar `enter` foca o painel direito. As abas são trocadas com `]` (próxima) e `[` (anterior):

| Aba | Conteúdo |
|---|---|
| **Logs** | Tail ao vivo da stdout/stderr do container |
| **Config** | JSON do `docker inspect`: env vars, ports, mounts, networks |
| **Top** | Processos rodando dentro do container (`docker top`) |
| **Stats** | CPU%, memória, network I/O — refresh ~1s |

A aba **Config** é o equivalente visual de `docker inspect <container>` e mostra:

- `Env` — variáveis de ambiente com seus valores (inclui segredos se não houver segredo manager)
- `ExposedPorts` e `HostConfig.PortBindings` — mapeamento host:container
- `HostConfig.Binds` e `Mounts` — volumes montados
- `Networks` — redes conectadas e IPs
- `Config.Cmd` / `Config.Entrypoint` — comando de inicialização

### Logs filter e tail

O painel Logs exibe a saída do container com tail automático (auto-scroll para o final):

- **Aba Logs padrão:** tail ao vivo com as configurações de `logs.since` e `logs.tail` do `config.yml`
- **`m` no container/service:** abre logs em fullscreen no painel principal
- **Navegação no fullscreen:** `j`/`k` para scrollar linha a linha; `G` para ir ao final; `g` para o início
- **`/`** filtra a lista de containers/services no painel esquerdo (não é filtro inline de logs)

Configuração global que controla o buffer de logs:

```yaml
logs:
  timestamps: true      # exibir timestamp em cada linha
  since: "60m"          # janela de tempo (default: 60m); "" = histórico completo
  tail: "200"           # últimas N linhas; "" = sem limite
```

Para debug de boot (erros ocorridos no startup de horas atrás), ajustar temporariamente:

```yaml
logs:
  since: ""
  tail: "500"
```

### Exec custom — shell preferido

O `E` (uppercase) padrão usa `/bin/sh`. Em imagens baseadas em Debian/Ubuntu, `bash` está disponível. Em Alpine e imagens distroless slim, apenas `sh`. Para configurar um shell preferido com fallback automático:

```yaml
customCommands:
  containers:
    - name: "bash-or-sh"
      command: "docker exec -it {{ .Container.ID }} bash 2>/dev/null || docker exec -it {{ .Container.ID }} sh"
      serviceNames: []
      attach: true
```

O `2>/dev/null` suprime o erro quando `bash` não existe e o `||` faz fallback para `sh`. O campo `attach: true` é obrigatório para qualquer shell interativo — sem ele, Lazydocker executa e retorna imediatamente sem ceder o terminal.

Para acessar via custom command: `c` no container abre o menu de custom commands; selecionar o item pelo nome.

### Debug crash loop

Um container em crash loop reinicia repetidamente e exibe restart count crescente na coluna do painel Containers. Sequência de investigação:

1. **Identificar:** painel Containers mostra `Restarting` no status e restart count no painel direito (aba Config → campo `RestartCount`)
2. **Logs:** `enter` → aba Logs → o tail exibe a última execução antes do crash — procurar a última linha antes do container morrer
3. **Config:** aba Config → campo `Env` — verificar variáveis de ambiente obrigatórias (connection strings, API keys, paths)
4. **Comando:** aba Config → `Config.Cmd` / `Config.Entrypoint` — confirmar que o comando de startup está correto
5. **Top:** aba Top — se o processo aparece como zumbi (`Z` na coluna status), o processo pai morreu e o container está preso
6. **Ação:** `s` (stop) → `r` (restart) após corrigir a causa; ou `d` (remove) + `u` (up) para recriar o container com estado limpo

> [!tip]
> O restart count exibido pelo Lazydocker vem do daemon Docker e reseta se o container for removido e recriado (`docker compose up -d --force-recreate`). Para histórico persistente, usar `docker inspect <c> | grep RestartCount`.

### Health checks

O `HEALTHCHECK` no Dockerfile instrui o Docker a executar um comando periodicamente para avaliar a saúde do container:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=15s \
  CMD curl -f http://localhost:8080/health || exit 1
```

Opções do `HEALTHCHECK`:

| Opção | Default | Descrição |
|---|---|---|
| `--interval` | 30s | Intervalo entre checks |
| `--timeout` | 30s | Timeout de cada check |
| `--retries` | 3 | Falhas consecutivas até `unhealthy` |
| `--start-period` | 0s | Grace period inicial antes de começar a contar falhas |

No docker-compose, o health check pode ser declarado no serviço:

```yaml
services:
  api:
    image: myapp:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s
```

Lazydocker exibe o status de saúde na coluna do container no painel Containers:

- `(healthy)` — último check passou
- `(unhealthy)` — check falhou N vezes consecutivas (N = retries)
- `(starting)` — dentro do `start-period`; falhas não contam ainda

Para inspecionar detalhes do health check: aba Config → campo `State.Health` — mostra o último output do check, timestamp e contagem de falhas.

### Compose overrides

O Docker Compose auto-carrega `docker-compose.override.yml` ao lado do `docker-compose.yml` — sem flags adicionais. O arquivo override usa a mesma sintaxe e faz merge com o principal: campos definidos no override sobrescrevem ou estendem os do principal.

Caso de uso típico: adicionar env vars de debug, mapear porta extra, montar o código-fonte local:

```yaml
# docker-compose.override.yml
services:
  api:
    environment:
      DEBUG: "true"
      LOG_LEVEL: debug
    ports:
      - "3001:3000"
    volumes:
      - ./src:/app/src
```

Lazydocker reflete o estado resultante do merge — o container exibido na aba Config já mostra os valores merged. Para visualizar o compose resultante antes de subir:

```bash
docker compose config
```

O Lazydocker não tem atalho nativo para `docker compose config`, mas um custom command resolve:

```yaml
customCommands:
  services:
    - name: "show merged config"
      command: "docker compose config"
      serviceNames: []
      attach: false
```

---

## Na prática

### Workflow: stack dev local não sobe

Cenário: `lazydocker` iniciado, vários services em crash loop ou parados.

```text
1. Abrir lazydocker no diretório com docker-compose.yml
2. Painel Project (1) confirma "compose detected"
3. Painel Services (2): service "db" mostra status "Restarting", count 5+
4. Selecionar container "db" no painel Containers (3)
5. Enter → aba Logs → última linha: "FATAL: database 'app' does not exist"
6. Aba Config → campo Env → confirmar POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
7. Identificar: variável POSTGRES_DB ausente ou errada no .env
8. Corrigir .env → painel Services → "D" (down project) → "U" (up project)
9. Services sobem em sequência; "db" healthy → "api" e "cache" iniciam
```

### Workflow: debug HTTP no container API

Cenário: container `api` está `running` mas requisições retornam 500.

```text
1. Painel Containers → selecionar "api"
2. Enter → aba Logs → scroll para ver stack trace recente
3. Aba Config → campo Env → confirmar DATABASE_URL aponta para o host correto
   (containers Docker usam nome do service como hostname, não "localhost")
4. "E" (exec) → bash aberto dentro do container
5. Testar conectividade: curl http://db:5432 (TCP) ou psql $DATABASE_URL
6. Identificar: DATABASE_URL usa "localhost" em vez do service name "db"
7. Corrigir variável → sair do shell → "r" para restart
```

### Workflow: limpar imagens órfãs após ciclo de dev

Cenário: muito `docker compose up -d --build`, disco em 90%.

```text
1. Painel Images (4) → ver lista de imagens "<none>" (dangling)
2. Custom command para prune:
   customCommands:
     images:
       - name: "prune dangling"
         command: "docker image prune -f"
         attach: false
3. "c" no painel Images → selecionar "prune dangling" → confirma
4. Lazydocker atualiza a lista; imagens dangling removidas
5. Para prune mais agressivo (incluindo imagens não usadas):
   command: "docker image prune -a -f"
   (atenção: remove todas as imagens sem container ativo)
```

### Workflow: subir override para teste local

Cenário: testar feature com variáveis de debug sem alterar o compose principal.

```text
1. Criar docker-compose.override.yml no mesmo diretório:
   services:
     api:
       environment:
         DEBUG: "true"
         FEATURE_FLAG_X: "enabled"
       ports:
         - "3001:3000"

2. Painel Services → "D" para down → "U" para up
   (Lazydocker usa "docker compose up -d" que auto-carrega o override)

3. Aba Config do container "api" → campo Env → confirmar DEBUG e FEATURE_FLAG_X presentes

4. Testar feature na porta 3001 (mapeada pelo override)

5. Ao terminar: remover docker-compose.override.yml → "D" → "U"
```

---

## Armadilhas

**1. Lazydocker iniciado fora do diretório de compose**

- **Causa:** auto-detect lê o cwd no momento da inicialização; sem `docker-compose.yml` ou `compose.yaml` ali, o Lazydocker não detecta o projeto.
- **Sintoma:** containers aparecem soltos no painel Containers, sem agrupamento por service; painel Services vazio; painel Project não mostra nome do projeto.
- **Detecção:** `ls docker-compose.yml compose.yaml 2>/dev/null` — se não listar nenhum, o cwd está errado.
- **Solução:** encerrar (`q`), `cd` para o diretório correto e reiniciar; ou verificar se há flag `--compose-file` na versão instalada (`lazydocker --help`).

**2. Container unhealthy sem `HEALTHCHECK` definido aparece como "running"**

- **Causa:** sem `HEALTHCHECK` no Dockerfile ou `healthcheck:` no compose, o Docker não monitora a saúde — apenas sabe se o processo principal está rodando.
- **Sintoma:** container responde com 5xx ou não aceita conexões, mas Lazydocker exibe status `running` sem sinal de alerta.
- **Detecção:** `docker inspect <container> | grep -A5 '"Health"'` — se retornar `null` ou campo ausente, não há health check.
- **Solução:** adicionar `HEALTHCHECK CMD ...` no Dockerfile ou `healthcheck:` no serviço do compose; depende_on de outro serviço deve usar `condition: service_healthy` para aguardar o check passar.

**3. `depends_on` sem `condition: service_healthy` causa crash silencioso**

- **Causa:** `depends_on: [db]` (forma simplificada) espera apenas que o container `db` tenha *iniciado*, não que esteja *pronto* para aceitar conexões.
- **Sintoma:** service `api` sobe antes do `db` estar pronto; logs da `api` mostram "connection refused" ou "ECONNREFUSED"; crash loop. Lazydocker exibe restart count crescendo.
- **Detecção:** comparar timestamps dos logs — `api` tenta conectar antes do `db` exibir "ready to accept connections".
- **Solução:** usar a forma longa no compose com `condition: service_healthy`; o serviço dependência deve ter `HEALTHCHECK` definido:

```yaml
services:
  api:
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      retries: 5
      start_period: 10s
```

**4. Restart count reseta após remoção e recriação do container**

- **Causa:** o restart count exibido vem do daemon Docker e é atributo do container específico. `docker compose up -d --force-recreate` ou `docker rm` + `docker run` cria um novo container com count zerado.
- **Sintoma:** container estava em crash loop com count 10+; após um `D` (down) + `U` (up) no Lazydocker, o count volta a 0 mesmo sem ter corrigido a causa raiz.
- **Detecção:** monitorar os logs imediatamente após o up — crash loop reaparece rapidamente mesmo com count zerado.
- **Solução:** não confiar no count absoluto como indicador de estabilidade; usar os logs para confirmar se o problema foi resolvido; `docker inspect <c> | grep RestartCount` durante a sessão atual antes de recriar.

**5. Logs com `since` curto escondem erros de inicialização**

- **Causa:** `logs.since: "60m"` (default) limita o buffer de logs exibido. Se o container iniciou há mais de 60 minutos, os logs de startup — onde geralmente estão os erros fatais — ficam fora da janela.
- **Sintoma:** aba Logs aparece vazia ou sem os erros esperados, mesmo com container em estado problemático.
- **Detecção:** `docker logs <container> --since 0` no terminal mostra logs completos que o Lazydocker não está exibindo.
- **Solução:** ajustar temporariamente `logs.since: ""` no `~/.config/lazydocker/config.yml` e reiniciar o Lazydocker para debug de boot; restaurar após a investigação.

**6. Override não detectado por nome de arquivo fora do padrão**

- **Causa:** o Docker Compose v2 auto-carrega apenas `docker-compose.override.yml` ou `compose.override.yaml` (em versões mais recentes). Arquivos com outros nomes (ex: `docker-compose.dev.yml`) precisam ser passados explicitamente com `-f`.
- **Sintoma:** override parece não ter efeito; aba Config do container não mostra as variáveis ou portas do override.
- **Detecção:** `docker compose config` no terminal mostra o compose merged; se as configurações do override não aparecerem, o arquivo não foi carregado automaticamente.
- **Solução:** renomear para `docker-compose.override.yml`; ou configurar `commandTemplates` no Lazydocker para incluir `-f docker-compose.dev.yml` explicitamente.

---

## Em inglês

- **stack** — *stack*. "conjunto de services definidos num docker-compose.yml que sobem e se comunicam como unidade."
- **serviço** — *service*. "abstração do Compose que define como um container deve ser criado, configurado e conectado a outros."
- **dependência** — *dependency*. "relação entre services declarada em `depends_on`; define ordem de inicialização."
- **health check** — *health check*. "comando periódico que o daemon Docker executa para avaliar se o container está operacional, não apenas em execução."
- **inspecionar** — *inspect*. "obter metadados detalhados de um container: env vars, ports, mounts, networks e estado de saúde."
- **override** — *override*. "arquivo complementar (`docker-compose.override.yml`) que modifica ou estende o compose principal sem alterá-lo."
- **regex** — *regex (regular expression)*. "padrão de texto usado para filtrar ou buscar linhas específicas em logs."
- **crash loop** — *restart loop / crash loop*. "ciclo de reinicializações contínuas porque o container inicia, falha e é reiniciado pelo daemon."
- **daemon** — *daemon*. "processo Docker em background que gerencia containers, imagens, volumes e networks; o Lazydocker se conecta a ele."
- **efêmero** — *ephemeral*. "de vida curta; containers são efêmeros por design — estado não persistido em volume é perdido ao remover o container."

---

## Veja também

- [[02 - Lazydocker — overview e operações comuns]] — pré-req: painéis, layout e operações básicas
- [[05 - Lazydocker — config, customização e workflow]] — customCommands, logs config e commandTemplates
- [[03-Dominios/Tecnologia/Terminal/TUIs/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Docker-compose|docker-compose]], [[Dicionário do Terminal#Exec (Lazydocker)|exec]], [[Dicionário do Terminal#Lazydocker|lazydocker]]

---

## Referências

- Lazydocker: https://github.com/jesseduffield/lazydocker
- Lazydocker Config: https://github.com/jesseduffield/lazydocker/blob/master/docs/Config.md
- Lazydocker Keybindings: https://github.com/jesseduffield/lazydocker/blob/master/docs/keybindings/Keybindings_en.md
- Docker Compose: https://docs.docker.com/compose/
- HEALTHCHECK: https://docs.docker.com/engine/reference/builder/#healthcheck
