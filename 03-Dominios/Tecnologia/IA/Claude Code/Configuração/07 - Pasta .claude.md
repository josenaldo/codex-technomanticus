---
title: "A pasta .claude — estrutura e propósito de cada arquivo"
type: concept
progress: done
publish: true
created: 2026-05-13
updated: 2026-07-07
status: growing
tags:
  - claude-code
  - configuracao
  - dotclaude
  - estrutura
---

# A pasta .claude — estrutura e propósito de cada arquivo

> [!abstract] TL;DR
> `.claude/` é o diretório de configuração do projeto para o Claude Code. Contém CLAUDE.md (contexto), settings.json (permissões, versionado), settings.local.json (sobrescritas pessoais, no .gitignore) e commands/ (slash commands). Cada arquivo tem um papel distinto — entender isso evita configurar no lugar errado.

---

## A analogia: a pasta `.github/`

Você já conhece a `.github/` — onde ficam os workflows de CI/CD, os templates de PR e issue, as regras de CODEOWNERS. Ela configura o comportamento do GitHub para o repositório sem ser código de produto.

A `.claude/` tem o mesmo papel, mas para o Claude Code. Ela configura o comportamento do agente para o projeto — o que ele sabe, o que ele pode fazer, quais atalhos ele oferece. Também fica no repositório, também é versionada, também é compartilhada com o time.

---

## Estrutura completa

```
.claude/
├── CLAUDE.md              ← contexto do projeto (vai pro git)
├── settings.json          ← permissões e comportamentos (vai pro git)
├── settings.local.json    ← sobrescritas pessoais (NÃO vai pro git)
└── commands/              ← slash commands do projeto (vai pro git)
    ├── review.md          → /review
    ├── pr-check.md        → /pr-check
    ├── debug.md           → /debug
    └── changelog.md       → /changelog
```

---

## Diagrama de responsabilidades

```mermaid
flowchart TD
    subgraph Git["Versionado no repositório"]
        CM["CLAUDE.md\nContexto do projeto\n(lido pelo modelo)"]
        SJ["settings.json\nPermissões e comportamentos\n(interpretado pelo runtime)"]
        CMD["commands/\nSlash commands\n(prompts encapsulados)"]
    end

    subgraph Local["Apenas na sua máquina"]
        SL["settings.local.json\nSobrescritas pessoais\n(secrets, paths locais)"]
    end

    subgraph Agent["Sessão do agente"]
        CTX["Contexto da sessão"]
    end

    CM --> CTX
    SJ --> CTX
    CMD --> CTX
    SL --> CTX

    style Git fill:#e8f4e8
    style Local fill:#f4e8e8
    style Agent fill:#e8e8f4
```

---

## Cada arquivo e seu propósito

### `CLAUDE.md` — o onboarding doc do agente

**O que é:** Contexto do projeto em linguagem natural. Lido pelo modelo no início de cada sessão. Concatenado com `~/.claude/CLAUDE.md` (global) — ambos chegam ao agente.

**Contém:** Stack e versões, arquitetura (onde as coisas ficam), convenções de código, comandos de desenvolvimento, restrições e o que nunca fazer.

**Vai pro git?** Sim. Todo dev que usar Claude Code no projeto recebe o mesmo contexto, tornando o comportamento do agente consistente entre membros do time.

**Quando atualizar:** quando a stack muda, quando uma nova convenção é adotada, quando o agente toma uma decisão errada por falta de contexto — esse é o sinal mais claro.

Ver [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|02 - CLAUDE.md anatomia]] para estrutura detalhada.

---

### `settings.json` — regras do projeto para o runtime

**O que é:** Configuração estruturada JSON, interpretada pelo runtime do Claude Code (não pelo modelo). Define o que o agente pode e não pode fazer mecanicamente.

**Contém:**
```json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm test -- *)",
      "Bash(npm run lint)",
      "Edit(*)",
      "Read(*)"
    ],
    "deny": [
      "Bash(git push --force*)",
      "Bash(rm -rf *)"
    ]
  },
  "env": {
    "NODE_ENV": "development"
  },
  "includeCoAuthoredBy": false
}
```

**Vai pro git?** Sim. Define o contrato de segurança do projeto — quais comandos o agente pode executar sem pedir confirmação, e quais são bloqueados independente do que o modelo queira fazer.

Ver [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json]] para todos os campos.

---

### `settings.local.json` — suas sobrescritas pessoais

**O que é:** Sobrescritas pessoais do `settings.json` do projeto. Mesma estrutura JSON, mas aplicadas apenas para você na sua máquina. Nunca sai do seu ambiente.

**Contém:** Variáveis de ambiente locais (DATABASE_URL apontando para seu banco local), paths pessoais, permissões temporárias para debugging, secrets de desenvolvimento.

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run dev:local)",
      "Bash(docker-compose up*)"
    ]
  },
  "env": {
    "DATABASE_URL": "postgresql://localhost:5432/myapp_dev",
    "REDIS_URL": "redis://localhost:6379",
    "JWT_SECRET": "dev-only-never-prod"
  }
}
```

**Vai pro git?** NUNCA. Adicione ao `.gitignore` imediatamente ao criar o arquivo.

**Por que existe separado?** Para não forçar você a escolher entre "compartilho tudo no settings.json (inclusive coisas sensíveis)" e "não compartilho nada (perco o valor para o time)". O par settings.json + settings.local.json resolve essa tensão.

---

### `commands/` — slash commands do projeto

**O que é:** Pasta com arquivos Markdown. Cada arquivo vira um slash command disponível no Claude Code.

**Contém:** Um arquivo `.md` por comando. O nome do arquivo (sem `.md`) vira o `/comando`. O conteúdo do arquivo é o prompt executado.

```
commands/
├── pr-check.md    → /pr-check    (checklist antes de PR)
├── explain.md     → /explain     (explicar código)
├── debug.md       → /debug       (sessão de debugging)
└── changelog.md   → /changelog   (gerar changelog)
```

**Vai pro git?** Sim. Commands compartilhados são padrões de qualidade do time — quando `/pr-check` é atualizado para incluir uma nova verificação, todos herdam imediatamente.

Ver [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/06 - Slash commands customizados|06 - Slash commands customizados]] para como criar e usar.

---

## O que vai pro git e o que não vai

```mermaid
flowchart LR
    subgraph Versioned["Versionar no git"]
        direction TB
        A["CLAUDE.md"]
        B["settings.json"]
        C["commands/"]
    end

    subgraph NotVersioned["Adicionar ao .gitignore"]
        D["settings.local.json\n(secrets, paths pessoais)"]
    end
```

**.gitignore recomendado:**
```gitignore
# Claude Code — sobrescritas pessoais (contém secrets de dev)
.claude/settings.local.json
```

Somente `settings.local.json` fica fora. O resto faz parte do harness do projeto e deve ser versionado.

---

## Relação com a estrutura global

A `.claude/` do projeto é uma das camadas. A estrutura completa:

```
~/.claude/              ← camada global (suas preferências pessoais)
├── CLAUDE.md
├── settings.json
└── commands/

[projeto]/.claude/      ← camada de projeto (este repositório)
├── CLAUDE.md
├── settings.json
├── settings.local.json
└── commands/
```

- **CLAUDE.md** — ambas as camadas são lidas e concatenadas
- **settings.json** — a camada mais específica sobrescreve a mais geral
- **commands/** — commands de ambas as camadas ficam disponíveis

---

## Montando do zero em um novo projeto

```bash
# 1. Criar estrutura
mkdir -p .claude/commands

# 2. Criar os arquivos base
touch .claude/CLAUDE.md
touch .claude/settings.json

# 3. Proteger settings.local.json antes de criá-lo
echo ".claude/settings.local.json" >> .gitignore

# 4. Configuração mínima do settings.json
cat > .claude/settings.json << 'EOF'
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Edit(*)",
      "Bash(git status)",
      "Bash(git log *)",
      "Bash(git diff *)",
      "Bash(git add *)",
      "Bash(git commit *)"
    ],
    "deny": [
      "Bash(git push --force *)",
      "Bash(git reset --hard *)",
      "Bash(rm -rf *)"
    ]
  },
  "includeCoAuthoredBy": false
}
EOF

# 5. Preencher CLAUDE.md com contexto do projeto
# (ver nota 02 — CLAUDE.md anatomia para estrutura)
```

---

## Evolução natural da pasta .claude

A `.claude/` não nasce completa — ela cresce junto com o uso do Claude Code no projeto. Uma evolução típica:

```
Semana 1 — Mínimo viável
.claude/
└── settings.json   (só allow/deny básico)

Semana 2 — Agente contextualizado
.claude/
├── CLAUDE.md       (visão geral, stack, convenções)
└── settings.json

Mês 1 — Time usando junto
.claude/
├── CLAUDE.md
├── settings.json
├── settings.local.json  (em .gitignore, cada dev tem o seu)
└── commands/
    └── pr-check.md     (primeiro command do time)

Mês 3 — Harness maduro
.claude/
├── CLAUDE.md
├── settings.json
└── commands/
    ├── pr-check.md
    ├── review.md
    ├── debug.md
    ├── changelog.md
    └── security-check.md
```

O sinal de que a `.claude/` está evoluindo bem: o agente toma menos decisões erradas ao longo do tempo, não mais. Cada decisão errada é uma oportunidade de adicionar contexto.

---

## Skills vs. commands — a distinção

Commands em `commands/` são prompts Markdown simples. Skills (em `.claude/skills/` ou como plugins externos via MCP) são integrações mais poderosas que podem usar ferramentas externas, contexto persistente, e fluxos multi-step.

| Característica | commands/ | skills (MCP) |
|---------------|-----------|-------------|
| Implementação | Arquivo .md | Plugin externo |
| Execução | Prompt simples | Multi-step com tools |
| Contexto externo | Não | Sim |
| Complexidade | Baixa | Alta |
| Setup | Nenhum | Requer MCP server |

Para a maioria dos casos de uso, `commands/` é suficiente e infinitamente mais simples. Skills fazem sentido quando você precisa integrar com sistemas externos (banco de dados externo, APIs, ferramentas CI/CD) dentro do fluxo do agente.

> [!tip] Assista: Anatomy of the .claude/ Folder — The Secret to 10x Claude Code
> **Canal:** Daniel Novoreta | **Duração:** ~18min | **Idioma:** EN
>
> Percorre a mesma anatomia desta nota (CLAUDE.md, settings.json, settings.local.json, commands/) e acrescenta dois ângulos que vale complementar aqui: a distinção entre a `.claude/` do projeto e a `.claude/` global no `$HOME` lado a lado, e a hierarquia de precedência de permissões — políticas de organização vencem o `settings.json` do projeto, que vence o `settings.local.json` pessoal. Trecho de destaque [15:19]: *"The allow list — those are commands that run without Claude asking for confirmation [...] the deny list, that's the hard block for Claude [...] anything that's not in either list, Claude will ask you before proceeding."*
>
> 🎬 [Assistir no YouTube](https://www.youtube.com/watch?v=rX6DLHlaOhU)

---

## Armadilhas comuns

> [!warning] Secrets em `settings.json`
> Vai pro git, fica no histórico para sempre. Coloque em `settings.local.json`.

> [!warning] Esquecer o `.gitignore` antes de criar `settings.local.json`
> Se você cria o arquivo e só então adiciona ao `.gitignore`, o arquivo já pode ter sido staged. Use `git rm --cached .claude/settings.local.json` se isso acontecer.

> [!warning] `CLAUDE.md` na raiz do projeto em vez de `.claude/CLAUDE.md`
> Funciona — Claude Code lê ambos. Mas ter os dois cria redundância. Padronize em `.claude/CLAUDE.md` para manter tudo junto.

> [!warning] Commands com espaços no nome
> `deploy check.md` não funciona como `/deploy-check`. Use kebab-case: `deploy-check.md`.

---

## Casos práticos

Três cenários reais de como essas armadilhas se manifestam em produção — não como regra abstrata, mas como incidente que já aconteceu em algum time.

### Caso 1 — o secret que vazou por estar no lugar errado

Um dev precisava que o agente rodasse contra uma API interna de staging durante uma sessão de debugging. Em vez de usar `settings.local.json`, ele colocou a chave direto em `env` no `settings.json` do projeto — "é só pra essa sessão, tiro depois". Esqueceu. O commit foi feito, revisado (ninguém reparou num JSON de config) e mergeado.

A chave ficou no histórico do git a partir daquele commit. Mesmo revertida em um commit seguinte, ela continua recuperável por qualquer pessoa com acesso ao repositório — `git log -p` ou um clone antigo bastam. O fix real não foi reverter a linha: foi rotacionar a credencial na origem e, só depois, reescrever o histórico (`git filter-repo` ou equivalente) para remover o segredo de fato.

Uma camada extra de defesa contra esse tipo de vazamento é combinar essa disciplina de "secrets nunca em `settings.json`" com [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/07 - Segurança com hooks|hooks de segurança]] que interceptam o commit antes dele sair da máquina do dev, em vez de depender só da revisão humana.

### Caso 2 — o time que divergiu por falta de `commands/` compartilhado

Um time de 5 devs usava Claude Code havia meses, mas nunca formalizou um `commands/`. Cada um tinha seu próprio jeito de pedir revisão de PR — um prompt salvo nas notas pessoais, outro copiava e colava de uma conversa antiga, um terceiro simplesmente descrevia o checklist de memória toda vez. O resultado: três padrões diferentes de "o que checar antes de abrir um PR", nenhum deles completo, e revisões inconsistentes dependendo de quem preparou o PR.

Quando finalmente criaram `commands/pr-check.md` versionado, a inconsistência não desapareceu da noite pro dia — mas a partir daquele ponto havia uma única fonte de verdade. Atualizar o command uma vez (por exemplo, adicionar verificação de migração de banco) propagou a mudança pra todo mundo no próximo `/pr-check`, em vez de exigir aviso manual em cinco lugares.

### Caso 3 — `settings.local.json` staged antes do `.gitignore` existir

Um dev novo no projeto criou `settings.local.json` pra apontar o `DATABASE_URL` pro Postgres local e colou um token de API de um serviço de terceiros pra testar uma integração. Rodou `git add .` por hábito antes de configurar o `.gitignore` — o arquivo entrou no stage junto com o resto. O commit foi abortado a tempo porque o hook de pre-commit do time bloqueou (por sorte, não por processo), mas o cenário inverso — sem esse hook — teria vazado o token do mesmo jeito que no Caso 1.

Do lado oposto, times que reagem a esse tipo de incidente endurecendo demais o `settings.json` caem noutra armadilha: um `deny` amplo demais (`"Bash(git *)"`, por exemplo, tentando bloquear `push --force`) acaba bloqueando `git status` e `git diff` também, e o agente passa a pedir confirmação manual para comandos totalmente inofensivos. A resposta certa pros dois problemas é a mesma: regras de `allow`/`deny` específicas (comando + argumento, não o binário inteiro) e `settings.local.json` protegido no `.gitignore` desde o primeiro commit do arquivo, não depois.

---

## Checklist — pasta .claude

- [ ] `.claude/CLAUDE.md` existe e tem contexto real do projeto
- [ ] `.claude/settings.json` existe com allow list do projeto
- [ ] `.claude/settings.local.json` está no `.gitignore`
- [ ] `commands/` tem ao menos `/pr-check` para o ciclo de review
- [ ] Nenhum secret está em `settings.json`

---

## Como explicar em inglês

| Português | Inglês |
|-----------|--------|
| Pasta de configuração | Configuration directory |
| Sobrescrita pessoal | Personal override / local override |
| Versionado no git | Version-controlled / committed to git |
| Contrato de segurança | Security contract |

**Frases úteis:**
- ".claude/ is to Claude Code what .github/ is to GitHub — it configures the tool's behavior for the project."
- "settings.local.json is like a .env.local file — it stays on your machine, never gets committed, and can hold dev credentials safely."
- "Commands in commands/ are shared team quality standards: when you update pr-check.md and push, everyone gets the new check next time they run /pr-check."

---

## O que vem a seguir

Conhecer a estrutura da `.claude/` resolve a pergunta "onde configuro isso". A próxima pergunta é "o que dá errado quando eu configuro errado" — e é exatamente aí que os Casos práticos acima só arranham a superfície. [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/08 - Armadilhas de configuração|08 - Armadilhas de configuração]] cataloga o padrão sintoma → causa → fix em três categorias (permissão, CLAUDE.md ineficaz, segurança) — o mapa completo de troubleshooting que esta nota só introduziu pelos exemplos.

Outras notas relacionadas:

- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/01 - Hierarquia de configuração|01 - Hierarquia de configuração]] — contexto das camadas global + projeto
- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|02 - CLAUDE.md anatomia]] — o que colocar no CLAUDE.md
- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json]] — campos do settings.json
- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/06 - Slash commands customizados|06 - Slash commands customizados]] — como criar commands
- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/index|Configuração]] — índice do galho

---

## Fontes

- **Anthropic** — *Claude Code configuration* (2026). Estrutura da pasta .claude e papel de cada arquivo — https://docs.anthropic.com/pt/docs/claude-code/settings
- **Anthropic** — *Claude Code memory* (2026). CLAUDE.md no contexto de configuração hierárquica — https://docs.anthropic.com/pt/docs/claude-code/memory






























