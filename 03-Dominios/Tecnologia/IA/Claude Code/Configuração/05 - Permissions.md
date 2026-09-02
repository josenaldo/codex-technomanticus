---
title: "Permissions — allow/deny, glob patterns, tool rules"
type: concept
progress: done
publish: true
created: 2026-05-13
updated: 2026-07-07
status: growing
tags:
  - claude-code
  - configuracao
  - permissions
  - settings
---

# Permissions — allow/deny, glob patterns, tool rules

> [!abstract] TL;DR
> Permissions controlam quais tool calls o Claude Code executa automaticamente versus quais precisam de confirmação humana. A sintaxe é `"NomeTool(padrão)"` nos arrays `allow` e `deny` de `settings.json`. Glob patterns com `*` funcionam para caminhos e argumentos de Bash. `deny` sempre prevalece sobre `allow`.

---

## A analogia: porteiro com lista VIP e lista negra

Imagine um porteiro de clube. Cada vez que um agente quer executar uma ação (rodar um teste, editar um arquivo, fazer git add), o porteiro verifica dois critérios:

1. **Lista negra (deny):** "Isso está proibido?" → se sim, bloqueio imediato. Sem exceções.
2. **Lista VIP (allow):** "Isso está autorizado?" → se sim, passa sem parar ninguém.
3. **Nenhuma das duas:** "Não sei." → pergunta para o dono (usuário) antes de deixar entrar.

O ponto crucial é que o porteiro não convence ninguém. Não há argumentação. A lista é a lei — diferente do CLAUDE.md, que o modelo pode interpretar com flexibilidade.

---

## Sintaxe geral

```
"NomeTool(padrão)"
```

- **NomeTool** — nome exato da tool: `Bash`, `Edit`, `Read`, `Write`, `WebFetch`, `WebSearch`
- **padrão** — string comparada com o argumento da tool call; suporta glob com `*`

Para liberar uma tool inteira sem restrição de argumento:
```json
"Read(*)"    // Qualquer leitura de arquivo
"Edit(*)"    // Qualquer edição de arquivo
```

---

## Bash — a tool mais crítica

Bash engloba todos os comandos shell — é onde a maioria dos riscos está e onde permissões bem calibradas fazem mais diferença.

### Comandos exatos

```json
"Bash(npm test)"      // Apenas 'npm test', exato
"Bash(git status)"    // Apenas 'git status'
"Bash(ls -la)"        // Apenas 'ls -la' (inclui a flag)
```

### Glob com `*`

```json
"Bash(npm test *)"    // npm test + qualquer argumento
"Bash(npm run *)"     // qualquer npm run <script>
"Bash(git log *)"     // git log com qualquer flag/argumento
"Bash(find * -name *)"
```

> [!warning] Atenção com globs amplos
> `"Bash(git *)"` permite `git push --force`. Prefira listar subcomandos específicos: `"Bash(git status)"`, `"Bash(git log *)"`, `"Bash(git diff *)"`.

### Prefixo de matching

O padrão é verificado como **prefixo** do comando completo. `"Bash(npm run)"` cobre `npm run lint`, `npm run build`, `npm run test:watch` — qualquer comando que começa com `npm run`.

---

## Ferramentas de arquivo — Read, Edit, Write

Para tools de arquivo, o padrão é comparado com o caminho.

```json
"Read(*)"                  // Qualquer arquivo em qualquer caminho
"Edit(*)"                  // Editar qualquer arquivo
"Edit(src/*)"              // Apenas arquivos diretamente em src/
"Edit(src/**/*.ts)"        // TypeScript em qualquer subpasta de src/
"Write(tests/*)"           // Escrever apenas dentro de tests/
"Write(src/generated/*)"   // Apenas código gerado (não handcrafted)
```

**Padrão recomendado:** liberar `Read(*)` e `Edit(*)` quase sempre. Leitura é inofensiva; edição é reversível via git. Restringir `Write(*)` apenas para projetos com arquivos protegidos específicos.

---

## WebFetch e WebSearch

```json
"WebFetch(*)"                                       // Qualquer URL
"WebFetch(https://docs.anthropic.com/*)"            // Apenas docs Anthropic
"WebFetch(https://docs.python.org/*)"               // Apenas docs Python
"WebSearch(*)"                                      // Qualquer pesquisa web
```

---

## Deny sempre prevalece sobre allow

Se um padrão aparece nos dois lados, `deny` vence. Sem exceção.

```json
{
  "permissions": {
    "allow": ["Bash(git *)"],
    "deny": ["Bash(git push *)"]
  }
}
```

Resultado: qualquer `git *` é permitido, **exceto** `git push *`. O agente pode `git status`, `git add`, `git commit`, mas não `git push`.

Isso é útil para liberar amplo e restringir pontualmente, sem ter que listar cada subcomando permitido:

```json
{
  "permissions": {
    "allow": ["Bash(npm *)"],
    "deny": [
      "Bash(npm publish *)",
      "Bash(npm deprecate *)"
    ]
  }
}
```

---

## Como as camadas se combinam

Permissions se acumulam entre camadas. A regra prática é:

```
Allow final = union(allow global, allow projeto, allow local)
Deny final  = union(deny global, deny projeto, deny local)
```

**Exemplo:**
```
~/.claude/settings.json:    allow: ["Bash(git status)", "Bash(git log *)"]
.claude/settings.json:      allow: ["Bash(npm test)"], deny: ["Bash(rm -rf *)"]

Sessão resultante:
  allow: git status + git log * + npm test
  deny:  rm -rf *
```

> [!info] Nota de comportamento observado
> A documentação oficial descreve settings.json com sobrescrita por camada. Na prática, permissões se acumulam entre camadas (a mais específica adiciona, não substitui). Se encontrar comportamento diferente, liste explicitamente o que precisa em cada camada — não confie no comportamento de merge.

---

## Mapa de segurança por zona

```mermaid
quadrantChart
    title Risco × Frequência de uso
    x-axis Baixo risco --> Alto risco
    y-axis Baixa frequência --> Alta frequência
    quadrant-1 Liberar com allow
    quadrant-2 Liberar com allow — monitorar
    quadrant-3 Deixar pedir confirmação
    quadrant-4 Bloquear com deny
    Read — *: [0.1, 0.9]
    git status: [0.1, 0.8]
    git log: [0.1, 0.7]
    npm test: [0.2, 0.85]
    Edit — *: [0.3, 0.9]
    git add: [0.3, 0.7]
    git commit: [0.4, 0.6]
    npm install: [0.5, 0.5]
    git push: [0.6, 0.4]
    rm -rf: [0.95, 0.1]
    git push force: [0.98, 0.05]
```

---

## Fluxo de decisão completo

```mermaid
flowchart TD
    classDef falha fill:#FF6B6B24,stroke:#FF6B6B,color:#E9ECF2
    classDef ok fill:#4ADE8021,stroke:#4ADE80,color:#E9ECF2
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    classDef marca fill:#8855DF33,stroke:#8855DF,color:#E9ECF2
    AgentWant["Agente quer executar\nTool X com argumento Y"]
    CheckDeny{"Algum padrão em deny\ncobre Tool X(Y)?"}
    DenyBlock["Bloqueado\nRuntimeError"]
    CheckAllow{"Algum padrão em allow\ncobre Tool X(Y)?"}
    AutoExec["Executa\nautomaticamente"]
    AskUser{"Usuário aprova?"}
    ExecAfterApproval["Executa"]
    Abort["Cancelado"]

    AgentWant --> CheckDeny
    CheckDeny -- "sim" --> DenyBlock
    CheckDeny -- "não" --> CheckAllow
    CheckAllow -- "sim" --> AutoExec
    CheckAllow -- "não" --> AskUser
    AskUser -- "sim" --> ExecAfterApproval
    AskUser -- "não" --> Abort

    class DenyBlock falha
    class AutoExec ok
    class ExecAfterApproval neutro
    class Abort marca
```

O fluxo tem três saídas possíveis: bloqueio (deny), execução automática (allow), execução após aprovação (nenhuma regra → pergunta ao usuário). Não existe "convencer o porteiro" — o resultado é determinístico.

---

## Diferença entre allow list vazia e ausente

Existe uma diferença sutil entre ter `"allow": []` (array vazio) e não ter o campo `allow` no arquivo:

- **Campo ausente:** herda da camada superior (global ou padrão do Claude Code)
- **Array vazio `[]`:** sobrescreve para vazio — nada é permitido automaticamente

```json
// settings.json sem allow — herda do global
{
  "permissions": {
    "deny": ["Bash(rm -rf *)"]
  }
}

// settings.json com allow vazio — NADA é automático neste projeto
{
  "permissions": {
    "allow": [],
    "deny": ["Bash(rm -rf *)"]
  }
}
```

Use `allow: []` explicitamente apenas quando quiser que o projeto force confirmação em tudo — por exemplo, em projetos de infra crítica onde qualquer execução deve ser revisada.

> [!tip] Vídeo — permissions e settings.json na prática
> [Permissions, settings.json, and plan mode: making one Claude Code session safe](https://www.youtube.com/watch?v=CT9xynq7WZM) — percorre onde as configurações vivem, qual arquivo vence quando há conflito, e como escrever regras allow/ask/deny do zero.

Permissions cirúrgicas resolvem metade do problema de segurança; a outra metade é lembrar que o próprio código gerado por um agente é `untrusted` até passar por revisão — ver [[03-Dominios/Tecnologia/IA/Segurança e Guardrails/06 - Permissões e sandboxing|Permissões e sandboxing]], que trata o mesmo tema pelo ângulo da defesa em profundidade (sandboxing além do settings.json).

---

## Configuração recomendada por tier

### Nível global — mínimo para qualquer projeto

```json
// ~/.claude/settings.json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Edit(*)",
      "Bash(git status)",
      "Bash(git log *)",
      "Bash(git diff *)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(ls *)",
      "Bash(find * -name *)",
      "Bash(wc -l *)"
    ],
    "deny": [
      "Bash(git push --force *)",
      "Bash(git reset --hard *)",
      "Bash(git clean -f *)",
      "Bash(rm -rf *)",
      "Bash(sudo *)"
    ]
  }
}
```

### Nível projeto — Node.js/TypeScript

```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm test -- *)",
      "Bash(npm run lint)",
      "Bash(npm run lint -- *)",
      "Bash(npm run type-check)",
      "Bash(npm run build)",
      "Bash(npm run dev)"
    ],
    "deny": [
      "Bash(npm publish *)"
    ]
  }
}
```

### Nível projeto — Python

```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(pytest)",
      "Bash(pytest *)",
      "Bash(ruff check *)",
      "Bash(ruff format *)",
      "Bash(python -m *)",
      "Bash(alembic upgrade *)",
      "Bash(alembic revision *)"
    ],
    "deny": [
      "Bash(alembic downgrade *)"
    ]
  }
}
```

### Nível projeto — Java/Maven

```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(./mvnw test)",
      "Bash(./mvnw test *)",
      "Bash(./mvnw compile)",
      "Bash(./mvnw clean package *)",
      "Bash(./mvnw spring-boot:run)"
    ]
  }
}
```

---

## Armadilhas comuns

> [!warning] Sem nenhum allow
> Cada tool call pede confirmação, inclusive `git status` e leitura de arquivos. Sessão fica inutilizavelmente lenta. Configure pelo menos `Read(*)`, `Edit(*)` e os comandos git de consulta.

> [!warning] `"deny": ["Bash(*)"]`
> Bloqueia absolutamente tudo. O agente fica paralisado. Deny deve ser cirúrgico — alveje o perigoso, não tudo.

> [!warning] `"Bash(*)"` no allow
> Libera todo e qualquer comando shell, incluindo `rm -rf /`, `git push --force`, `sudo`. Se você quiser liberar "quase tudo", use `deny` para as exceções, não allow amplo.

> [!warning] Esquecer variações de argumento
> `"Bash(npm test)"` não cobre `npm test -- --watch`. Adicione `"Bash(npm test *)"` para cobrir argumentos extras.

> [!warning] Não testar
> Configure, faça uma sessão de teste com comandos variados, verifique o que fica travado. Permissions mal calibradas são descobertas na hora errada.

---

## Casos práticos

**Cenário 1 — onboarding de um repo Node novo.** Um dev entra num projeto TypeScript que nunca teve `.claude/settings.json`. Na primeira sessão, cada `npm test`, cada `git status`, cada leitura de arquivo pára pra pedir confirmação — a sessão vira uma sequência de cliques em "yes". Ele copia o tier "Node.js/TypeScript" da seção anterior (`Bash(npm test)`, `Bash(npm run lint)`, `Bash(npm run build)` no allow; `Bash(npm publish *)` no deny) pro `.claude/settings.json` do projeto. Na sessão seguinte, lint/test/build rodam direto; publicar pro registry continua exigindo aprovação humana — que é exatamente o ponto de risco que merece um humano no loop.

**Cenário 2 — pipeline Python com migração de banco.** Um time usa Claude Code pra rodar `pytest` e `ruff` livremente, mas migrations (`alembic upgrade`/`alembic revision`) tocam num banco compartilhado de staging. O tier "Python" já modela essa distinção: `alembic upgrade *` e `alembic revision *` no allow (aplicar migração pra frente é rotina, revisável), `alembic downgrade *` no deny (reverter em produção é decisão que exige revisão humana, porque desfazer uma migração pode perder dados). O mesmo padrão se replica pro tier Java/Maven: `./mvnw test` e `./mvnw compile` liberados, mas nenhum comando de deploy entra no allow — fica de fora da lista inteira, forçando confirmação.

---

## Checklist — permissions

- [ ] `Read(*)` está no allow (leitura nunca é destrutiva)
- [ ] `Edit(*)` está no allow ou restrito ao subdiretório correto
- [ ] Comandos de teste e lint do projeto estão no allow
- [ ] `rm -rf *`, `git push --force *`, `git reset --hard *` estão no deny
- [ ] Globs amplos no allow têm deny complementares para os casos perigosos
- [ ] Testado com uma sessão real — nada que deveria funcionar fica travado

---

## Como explicar em inglês

| Português | Inglês |
|-----------|--------|
| Lista de permissão | Allow list / allowlist |
| Lista de bloqueio | Deny list / blocklist |
| Padrão glob | Glob pattern |
| Confirmação manual | Manual confirmation / user approval |
| Prevalece sobre | Takes precedence over |

**Frases úteis:**
- "The deny list always takes precedence over the allow list — even if a pattern appears in both, the deny wins."
- "Without any allow list configured, every single tool call — including git status and file reads — will prompt for approval."
- "Use deny to surgically block dangerous operations; don't use allow: Bash(*) and then try to list exceptions in deny — it becomes hard to reason about."

---

## O que vem a seguir

Este capítulo tratou permissions isoladamente — a sintaxe `allow`/`deny`, os globs, a precedência. Mas permissions não vivem sozinhas: elas são só um dos blocos de `settings.json`, que também define modelo, hooks e outras chaves — vale voltar pra [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json]] pra ver o arquivo inteiro, não só a fatia de permissions.

Também vale a pena revisitar [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/01 - Hierarquia de configuração|01 - Hierarquia de configuração]]: o exemplo de "camadas se combinam" desta nota (global + projeto + local) só faz sentido plenamente depois de entender a ordem de precedência entre os quatro níveis de arquivo.

Por fim, se a dúvida for "o que mais dá errado além do que já vi aqui", a [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/08 - Armadilhas de configuração|08 - Armadilhas de configuração]] cataloga erros de configuração além de permissions — MCP mal configurado, hooks quebrados, CLAUDE.md gigante — o mesmo espírito de "isso trava a sessão na hora errada", mas para o resto do arquivo.

---

## Veja também

- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json]] — arquivo que contém permissions
- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/01 - Hierarquia de configuração|01 - Hierarquia de configuração]] — como permissões se combinam entre camadas
- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/08 - Armadilhas de configuração|08 - Armadilhas de configuração]] — erros comuns

---

## Referências

- **Anthropic** — *Claude Code settings — permissions* (2026). Sintaxe de allow/deny e precedência — https://docs.anthropic.com/pt/docs/claude-code/settings#permissions
- **Anthropic** — *Claude Code security* (2026). Práticas de segurança recomendadas para permissões — https://docs.anthropic.com/pt/docs/claude-code/security
- **YouTube** — *Permissions, settings.json, and plan mode: making one Claude Code session safe* (2026) — https://www.youtube.com/watch?v=CT9xynq7WZM



