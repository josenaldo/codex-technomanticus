---
title: "Lazydocker — config, customização e workflow"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - tuis
  - lazydocker
  - adepto
  - config
  - docker
aliases:
  - Lazydocker config
---

# Lazydocker — config, customização e workflow

> [!abstract] TL;DR
> Lazydocker lê `~/.config/lazydocker/config.yml`. Seções: `gui` (theme, showAllContainers), `commandTemplates` (rebind `dockerCompose` pra podman ou `docker compose` v2), `customCommands` (atalhos shell com placeholders `{{ .Container.ID }}`), `logs` (timestamps, since, tail). Workflow recomendado: Lazydocker rodando num pane Zellij ao lado do dev server; restart on demand. Auto-detecta `docker-compose.yml` no cwd e agrupa containers como services.

## O que é / Como funciona

### Local e formato

- **Path:** `~/.config/lazydocker/config.yml` — respeita `$XDG_CONFIG_HOME` se definido
- **Formato:** YAML; comentários com `#`; indentação 2 espaços (tabs causam parse error)
- **Sem arquivo:** Lazydocker aplica defaults internos — nenhuma config é obrigatória
- **Reload:** Lazydocker lê config somente na startup; alterações requerem restart (`q` + `lazydocker`)

### Seções principais

#### `gui:`

Controla aparência e comportamento da interface.

Propriedades mais usadas:

- `theme:` — mapa de cores dos elementos visuais
- `showAllContainers: true|false` *(default: false)* — exibir containers parados além dos ativos
- `language: "en"` *(default: auto)* — `"auto"`, `"en"`, `"pl"`, `"nl"`, `"de"`, `"tr"`
- `border: "rounded"` *(default: rounded)* — estilo de borda: `"rounded"`, `"single"`, `"double"`, `"hidden"`
- `sidePanelWidth: 0.333` *(default: 0.333)* — largura do painel lateral como fração da tela
- `expandFocusedSidePanel: false` *(default: false)* — expandir painel lateral com foco

Exemplo com tema Catppuccin-ish:

```yaml
gui:
  theme:
    activeBorderColor:
      - "#a6e3a1"
      - bold
    inactiveBorderColor:
      - "#585b70"
    selectedLineBgColor:
      - "#313244"
  showAllContainers: true
  language: "en"
  border: "rounded"
```

#### `commandTemplates:`

Rebind dos comandos Docker internos. Útil para:

- Substituir `docker compose` v2 por `docker-compose` v1 (ou vice-versa)
- Substituir `docker` por `podman` em ambientes sem Docker daemon
- Adicionar flags default a operações recorrentes

Variáveis de template disponíveis nas strings de `commandTemplates`: `{{ .DockerCompose }}`, `{{ .Service.Name }}`, `{{ .Container.Name }}`.

Valores default relevantes (verificados no código-fonte):

```yaml
commandTemplates:
  dockerCompose: "docker compose"            # v2 (espaço); v1 seria "docker-compose"
  restartService: "{{ .DockerCompose }} restart {{ .Service.Name }}"
  startService: "{{ .DockerCompose }} start {{ .Service.Name }}"
  stopService: "{{ .DockerCompose }} stop {{ .Service.Name }}"
  upService: "{{ .DockerCompose }} up -d {{ .Service.Name }}"
  rebuildService: "{{ .DockerCompose }} up -d --build {{ .Service.Name }}"
  recreateService: "{{ .DockerCompose }} up -d --force-recreate {{ .Service.Name }}"
  serviceLogs: "{{ .DockerCompose }} logs --since=60m --follow {{ .Service.Name }}"
  up: "{{ .DockerCompose }} up -d"
```

Pra usuário podman:

```yaml
commandTemplates:
  dockerCompose: "podman-compose"
```

#### `customCommands:`

Atalhos shell definidos pelo usuário com placeholders Go template. Estrutura organizada por tipo de recurso: `containers`, `services`, `images`, `volumes`, `networks`.

Campos de cada item:

| Campo | Tipo | Descrição |
|---|---|---|
| `name` | string | Label exibido no menu de comandos |
| `command` | string | Comando shell; aceita placeholders Go template |
| `serviceNames` | lista | Restringe o comando a serviços específicos (vazio = todos) |
| `attach` | bool | `true` — Lazydocker suspende e cede terminal (shell/REPL); `false` — output capturado sem interação |

Placeholders disponíveis por contexto (verificados no código-fonte):

- **containers:** `{{ .Container.ID }}`, `{{ .Container.Name }}`, `{{ .Container.ServiceName }}`, `{{ .Container.ProjectName }}`
- **services:** `{{ .Service.Name }}`, `{{ .Service.ProjectName }}`, `{{ .DockerCompose }}`
- **images:** `{{ .Image.ID }}`, `{{ .Image.Name }}`
- **volumes:** `{{ .Volume.Name }}`

Exemplo — abrir bash em container:

```yaml
customCommands:
  containers:
    - name: "bash"
      command: "docker exec -it {{ .Container.ID }} bash"
      serviceNames: []
      attach: true
```

Exemplo — backup de volume:

```yaml
customCommands:
  volumes:
    - name: "backup"
      command: "docker run --rm -v {{ .Volume.Name }}:/v -v $(pwd):/b alpine tar czf /b/{{ .Volume.Name }}.tar.gz /v"
      attach: false
```

Exemplo — rebuild de serviço específico:

```yaml
customCommands:
  services:
    - name: "rebuild"
      command: "{{ .DockerCompose }} up -d --build {{ .Service.Name }}"
      serviceNames: []
      attach: false
```

#### `logs:`

Controla o comportamento do painel de logs.

- `timestamps: true|false` *(default: false)* — exibir timestamps nas linhas de log
- `since: "60m"` *(default: "60m")* — janela de tempo; `""` pra histórico completo
- `tail: "200"` *(default: "")* — limitar às últimas N linhas; `""` pra sem limite

```yaml
logs:
  timestamps: true
  since: "10m"
  tail: "500"
```

---

## Na prática

### Setup mínimo (podman-compose user)

Config funcional pra ambiente com podman no lugar de Docker:

```yaml
# ~/.config/lazydocker/config.yml
gui:
  showAllContainers: true
commandTemplates:
  dockerCompose: "podman-compose"
logs:
  timestamps: true
  since: "30m"
```

Justificativas:

- `showAllContainers: true` — exibe containers parados, útil pra diagnosticar crashes
- `dockerCompose: "podman-compose"` — substitui o binário interno; sem isso, `r` (restart service) falha com "docker compose: command not found"
- `timestamps: true` — correlacionar eventos de log com ações no painel

### Custom command: bash em vez de sh

O `E` (exec) padrão do Lazydocker abre `/bin/sh`. Para abrir `bash` com fallback pra `sh` (cobre Alpine sem bash):

```yaml
customCommands:
  containers:
    - name: "bash"
      command: "docker exec -it {{ .Container.ID }} bash || docker exec -it {{ .Container.ID }} sh"
      serviceNames: []
      attach: true
```

O `|| sh` garante que o comando não falhe em imagens minimalistas (Alpine, distroless slim).

> [!note]
> `attach: true` é obrigatório para shell interativo. Sem ele, Lazydocker executa o comando e retorna imediatamente, sem mostrar o terminal.

### Workflow recomendado

Configuração de ambiente de desenvolvimento com Zellij:

1. **Layout Zellij com dois panes:** Lazydocker à esquerda, dev server (ex: `npm run dev`) à direita
2. **Lazydocker sempre visível:** `Enter` em container → Tab `Logs` → auto-tail ativo
3. **Restart on demand:** foco no pane Lazydocker, selecionar serviço, `r` (restart) ou `R` (rebuild)
4. **Monitorar CPU/mem:** Tab `Stats` no container de interesse pra detectar memory leaks

Esse padrão elimina alternar entre terminais pra `docker logs -f` e `docker restart`.

### Auto-detect docker-compose

Ao iniciar Lazydocker no mesmo diretório que contém `docker-compose.yml` (ou `compose.yml`):

- Containers são agrupados como **services** no painel Project
- Dependências (`depends_on`) ficam visíveis no status agregado
- Operações de serviço (restart, rebuild, stop) usam o compose configurado em `commandTemplates.dockerCompose`

Se Lazydocker não detectar o compose, verificar: arquivo nomeado `docker-compose.yml` ou `docker-compose.yaml` (não `compose.yml` sozinho em versões mais antigas do Lazydocker).

---

## Armadilhas

**1. `commandTemplates.dockerCompose` com binário errado**

- **Causa:** Docker Compose mudou de `docker-compose` (v1, binário separado) para `docker compose` (v2, plugin). O default atual do Lazydocker é `"docker compose"` (espaço). Em sistemas com apenas v1 instalado, o comando falha.
- **Sintoma:** `docker-compose: command not found` ou `docker: 'compose' is not a docker command` ao tentar restart/rebuild de serviço.
- **Como detectar:** `docker compose version` (v2, espaço) vs `docker-compose --version` (v1, hífen) — ver qual responde sem erro.
- **Solução:** ajustar `commandTemplates.dockerCompose: "docker-compose"` pra v1 ou `"docker compose"` pra v2; pra podman, usar `"podman-compose"`.

**2. Placeholder inválido em `customCommands`**

- **Causa:** typo no placeholder Go template (ex: `{{ .Container.Id }}` em vez de `{{ .Container.ID }}`). Go templates são case-sensitive.
- **Sintoma:** o comando executa com o valor `<no value>` literal ou string vazia no lugar do ID/nome esperado.
- **Como detectar:** executar o comando manualmente no terminal substituindo o placeholder pelo valor real; comparar com a struct verificada no código-fonte.
- **Solução:** usar exatamente os campos definidos na struct: `{{ .Container.ID }}`, `{{ .Container.Name }}`, `{{ .Service.Name }}`, `{{ .Volume.Name }}`, `{{ .Image.ID }}`.

**3. `attach: true` em comando não-interativo**

- **Causa:** `attach: true` faz Lazydocker ceder o terminal ao subprocesso e aguardar. Comandos one-shot (backup, restart, build) terminam imediatamente, mas o Lazydocker fica em estado suspenso esperando input que nunca vem.
- **Sintoma:** Lazydocker trava após executar o custom command; tecla `q` não responde normalmente.
- **Como detectar:** testar o comando com `attach: false` — se funcionar sem travar, o problema é o attach.
- **Solução:** usar `attach: true` apenas para shell interativo (bash, sh, python REPL); usar `attach: false` para qualquer comando que termine sozinho.

**4. `logs.since` muito curto em debug de boot**

- **Causa:** o `since` limita a janela de logs exibida. Com `since: "5m"`, logs de inicialização do container (que podem ter ocorrido há mais de 5 minutos) ficam invisíveis.
- **Sintoma:** painel de logs vazio ou sem os erros de startup esperados, mesmo com container reiniciado.
- **Como detectar:** mudar temporariamente pra `since: ""` (sem limite) e verificar se os logs aparecem.
- **Solução:** pra debug de boot, usar `since: ""` ou `since: "24h"`; restaurar valor curto após investigação pra manter performance.

**5. YAML com indentação inválida (tabs em vez de spaces)**

- **Causa:** YAML não aceita tabs como indentação. Copy-paste de snippets de editores configurados com tabs, ou edição em editor sem `expandtab` pra YAML, insere tabs silenciosamente.
- **Sintoma:** Lazydocker inicia com defaults (ignora config) ou exibe erro de parse na startup; sem mensagem de erro clara na TUI.
- **Como detectar:** `cat -A ~/.config/lazydocker/config.yml | grep "^\^I"` — `^I` indica tab. Alternativa: `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" ~/.config/lazydocker/config.yml`.
- **Solução:** usar sempre 2 espaços por nível; configurar o editor pra expandir tabs em YAML (`autocmd FileType yaml setlocal expandtab` no Neovim).

**6. `customCommands` sem `serviceNames: []` trava campo obrigatório**

- **Causa:** o campo `serviceNames` é obrigatório na struct YAML do Lazydocker. Omiti-lo pode causar erro de unmarshal dependendo da versão.
- **Sintoma:** custom command não aparece no menu ou Lazydocker reporta erro ao carregar config.
- **Como detectar:** comparar config com exemplos da documentação oficial; verificar se `serviceNames` está presente.
- **Solução:** incluir sempre `serviceNames: []` (lista vazia = aplica a todos) em cada item de `customCommands`.

---

## Em inglês

- **configuração** — *configuration / config file*. "arquivo YAML que persiste preferências do Lazydocker entre sessões."
- **template de comando** — *command template*. "string com placeholders Go que o Lazydocker expande antes de executar; definido em `commandTemplates`."
- **placeholder** — *placeholder*. "expressão Go template como `{{ .Container.ID }}` substituída pelo valor real do recurso selecionado."
- **container** — *container*. "instância em execução de uma imagem Docker ou Podman; unidade básica monitorada pelo Lazydocker."
- **serviço** — *service*. "abstração do docker-compose que agrupa um ou mais containers com configuração declarativa."
- **volume** — *volume*. "unidade de armazenamento persistente gerenciada pelo Docker, independente do ciclo de vida do container."
- **logs** — *logs*. "saída stdout/stderr do container; exibida no painel direito com suporte a `since`, `tail` e `timestamps`."
- **timestamp** — *timestamp*. "marca de data/hora prefixada a cada linha de log quando `logs.timestamps: true`."
- **tail** — *tail*. "limitar a exibição às últimas N linhas de log; análogo ao `tail -n N` no terminal."
- **attach** — *attach*. "ceder o terminal ao subprocesso do custom command; necessário para shells interativos, desnecessário para comandos one-shot."

---

## Veja também

- [[02 - Lazydocker — overview e operações comuns]] — pré-req: painéis, layout e operações básicas
- [[07 - Lazydocker — debugging avançado e docker-compose]] — Magus: compose avançado e troubleshooting
- [[03-Dominios/Terminal/TUIs/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Docker-compose|docker-compose]], [[Dicionário do Terminal#Exec (Lazydocker)|exec]], [[Dicionário do Terminal#Lazydocker|lazydocker]]

---

## Referências

- Lazydocker Config: https://github.com/jesseduffield/lazydocker/blob/master/docs/Config.md
- Custom Commands (código-fonte): https://github.com/jesseduffield/lazydocker/blob/master/pkg/config/app_config.go
