---
title: "Armadilhas de configuração — o que dá errado e como evitar"
type: concept
progress: done
publish: true
created: 2026-05-13
updated: 2026-07-07
status: growing
tags:
  - claude-code
  - configuracao
  - armadilhas
  - troubleshooting
---

# Armadilhas de configuração — o que dá errado e como evitar

> [!abstract] TL;DR
> Os erros de configuração mais comuns do Claude Code se dividem em três categorias: permissões erradas (agente para a cada passo ou faz coisas perigosas sem perguntar), CLAUDE.md ineficaz (contexto ausente, desatualizado ou diluído em ruído) e segurança (secrets vazando pro git).
> Cada armadilha catalogada aqui segue o mesmo padrão de diagnóstico — sintoma observável, causa mecânica, fix concreto — porque comportamento errado do agente quase nunca é aleatório: é sempre reflexo de uma configuração ausente ou mal calibrada em algum lugar da pilha.
> As doze armadilhas abaixo cobrem os casos reais mais recorrentes, do allow list vazio (agente trava em tudo) ao secret commitado por engano (rotação é o único fix que conta de verdade); a seção "Casos práticos" reconstrói dois desses incidentes com a sequência completa de sintoma → decisão errada → correção.

---

## A analogia: sintomas × causas

Configuração ruim raramente grita. Ela sussurra — o agente usa `console.log` em vez do logger do projeto, instala libs duplicadas, faz git push direto sem pedir confirmação. Cada comportamento errado é um sinal de uma configuração faltando ou errada.

O padrão de diagnóstico é sempre: **sintoma → causa → fix**.

---

## Armadilhas comuns

### Categoria 1 — Permissões

> [!warning] Armadilha 1 — sem `allow` configurado: agente para em tudo
> **Sintoma:** o agente pede confirmação para `git status`, `ls`, `wc -l`, leitura de arquivos. A sessão parece ter travado após cada ação mínima.
>
> **Causa:** nenhum `allow` no `settings.json`. Sem whitelist, qualquer tool call que não é trivialmente segura exige confirmação manual.
>
> **Fix:**
> ```json
> {
>   "permissions": {
>     "allow": [
>       "Read(*)",
>       "Edit(*)",
>       "Bash(git status)",
>       "Bash(git log *)",
>       "Bash(git diff *)",
>       "Bash(ls *)",
>       "Bash(find * -name *)",
>       "Bash(wc -l *)"
>     ]
>   }
> }
> ```
>
> **Regra:** sempre configure no mínimo as operações de leitura. Elas são inofensivas e eliminam 80% das confirmações desnecessárias.

> [!warning] Armadilha 2 — `allow` muito amplo: agente faz ações perigosas
> **Sintoma:** o agente faz `git push --force`, reseta branches, deleta arquivos sem pedir confirmação.
>
> **Causa:** `"Bash(git *)"` ou `"Bash(*)"` no allow. Glob amplo demais — cobre exatamente os subcomandos que você queria excluir. Ver [[03-Dominios/Tecnologia/IA/Segurança e Guardrails/06 - Permissões e sandboxing|06 - Permissões e sandboxing]] para o modelo de sandboxing por trás desse risco.
>
> **Fix:** liste subcomandos específicos e use `deny` para os perigosos:
> ```json
> {
>   "permissions": {
>     "allow": [
>       "Bash(git status)",
>       "Bash(git log *)",
>       "Bash(git diff *)",
>       "Bash(git add *)",
>       "Bash(git commit *)"
>     ],
>     "deny": [
>       "Bash(git push --force *)",
>       "Bash(git reset --hard *)",
>       "Bash(git clean -f *)",
>       "Bash(git push * main)"
>     ]
>   }
> }
> ```
>
> **Regra:** `Bash(git *)` é perigoso porque inclui `git push --force`. Prefira listas explícitas de subcomandos seguros.

> [!warning] Armadilha 3 — `deny: ["Bash(*)"]`: agente completamente travado
> **Sintoma:** o agente não consegue executar absolutamente nada — nem `git status`, nem `ls`. Retorna erro em qualquer tool call de Bash.
>
> **Causa:** deny muito abrangente bloqueia tudo.
>
> **Fix:** deny deve ser cirúrgico:
> ```json
> {
>   "permissions": {
>     "deny": [
>       "Bash(rm -rf *)",
>       "Bash(git push --force *)",
>       "Bash(sudo *)"
>     ]
>   }
> }
> ```
>
> **Regra:** bloqueie ações perigosas específicas, não categorias inteiras.

> [!warning] Armadilha 4 — esquecer variações de argumento
> **Sintoma:** `npm test` funciona automaticamente. `npm test -- --watch` pede confirmação. `npm test -- --coverage` também.
>
> **Causa:** `"Bash(npm test)"` é matching exato. O glob `*` não está presente para cobrir argumentos extras.
>
> **Fix:**
> ```
> "Bash(npm test)",
> "Bash(npm test -- *)",
> "Bash(npm test *)"
> ```
>
> **Regra:** para comandos que você frequentemente usa com flags extras, adicione sempre a versão com `*` no final.

> [!warning] Armadilha 5 — settings.json do projeto sobrescreve o global
> **Sintoma:** as permissões de `git status` e `git log` que funcionam em outros projetos (do settings global) param de funcionar neste projeto.
>
> **Causa:** o `settings.json` do projeto define seu próprio `allow`, sobrescrevendo o do global. Permissões **não se acumulam automaticamente** — a camada mais específica substitui.
>
> **Fix — opção A:** repita o que você precisa do global:
> ```json
> // .claude/settings.json
> {
>   "permissions": {
>     "allow": [
>       "Bash(git status)",
>       "Bash(git log *)",
>       "Bash(npm test)",
>       "Bash(npm run lint)"
>     ]
>   }
> }
> ```
>
> **Fix — opção B:** não defina `allow` no projeto — apenas `deny` para restrições adicionais. O global continua valendo.

### Categoria 2 — CLAUDE.md

> [!warning] Armadilha 6 — CLAUDE.md vazio ou inexistente
> **Sintoma:** o agente usa `console.log` em vez do logger do projeto. Instala uma lib que já existe. Usa convenções de outro projeto (ou inventa as suas próprias).
>
> **Causa:** sem CLAUDE.md, o agente opera com suposições genéricas baseadas no que é comum em projetos semelhantes.
>
> **Fix:** crie `.claude/CLAUDE.md` com no mínimo: stack + logger correto + comandos de teste + seção `## Restrições`. Ver [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|02 - CLAUDE.md anatomia]].
>
> **Regra:** a ausência de CLAUDE.md não é neutra — é ruído. O agente vai preencher os gaps com suposições.

> [!warning] Armadilha 7 — CLAUDE.md desatualizado
> **Sintoma:** o agente usa Mongoose quando o projeto migrou para Prisma há 3 meses. Referencia `src/utils/database.ts` que foi movido para `src/db/client.ts`.
>
> **Causa:** CLAUDE.md foi criado mas não é mantido junto com as mudanças de stack.
>
> **Fix:** adicione "atualizar CLAUDE.md" à definição de done das tasks de migração de stack. Uma linha no `## Comandos` ou `## Stack` tem custo zero e impacto alto.
>
> **Regra:** CLAUDE.md desatualizado é pior que nenhum CLAUDE.md — o agente segue instruções erradas com confiança.

> [!warning] Armadilha 8 — placeholders `[...]` não preenchidos
> **Sintoma:** o agente se comporta de forma inconsistente ou faz perguntas que o CLAUDE.md deveria responder.
>
> **Causa:** usou um template de CLAUDE.md mas não substituiu os campos marcados com `[...]`.
>
> **Fix:** antes de commitar o CLAUDE.md, busque por `[` no arquivo:
> ```bash
> grep '\[' .claude/CLAUDE.md
> ```
> Se encontrar placeholders, preencha ou remova a seção.

> [!warning] Armadilha 9 — regras sem contexto
> **Sintoma:** o agente segue a regra literalmente mesmo em casos que claramente são exceções razoáveis. Ou pede permissão em casos em que a regra não deveria se aplicar.
>
> **Causa:** "Não use `any`" sem explicar por quê — o agente não tem contexto para julgar quando o edge case justifica exceção.
>
> **Fix:** adicione o motivo e as exceções explícitas:
> ```markdown
> ## Restrições
>
> - Não use `any` em TypeScript — use `unknown` com type guard.
>   Razão: tivemos bugs de produção por tipagem solta (incident 2024-03).
>   Exceção: tipos de resposta de APIs externas sem schema documentado
>   (use `unknown` e valide com zod antes de usar).
> ```
>
> **Regra:** a regra vale a razão que a explica. Sem razão, o agente não consegue julgar os casos de borda.

> [!warning] Armadilha 10 — CLAUDE.md muito longo e cheio de ruído
> **Sintoma:** o agente ignora instruções que estão no CLAUDE.md, ou as aplica de forma inconsistente.
>
> **Causa:** CLAUDE.md de 500 linhas com muitas instruções redundantes ou triviais. O modelo lê tudo mas presta menos atenção às partes diluídas em ruído.
>
> **Fix:** revise o CLAUDE.md e remova:
> - Instruções que já estão óbvias no código (tipos bem definidos, nomenclatura clara)
> - Repetições da mesma regra em diferentes formas
> - Detalhes técnicos que o agente pode descobrir lendo o código
>
> **Regra:** 80 linhas de alta densidade > 500 linhas com padding. O CLAUDE.md não é documentação — é briefing.

### Categoria 3 — Segurança

> [!warning] Armadilha 11 — secrets em `settings.json`
> **Sintoma:** API keys, passwords de banco de dados, tokens aparecem no histórico do git.
>
> **Causa:** `settings.json` vai pro git. Qualquer coisa no campo `env` fica exposta.
>
> **Fix:** use `settings.local.json` para qualquer coisa sensível:
> ```json
> // .claude/settings.local.json (no .gitignore)
> {
>   "env": {
>     "DATABASE_URL": "postgresql://user:senha@localhost/dev",
>     "JWT_SECRET": "dev-only-never-prod",
>     "STRIPE_SECRET_KEY": "sk_test_..."
>   }
> }
> ```

> [!warning] Armadilha 12 — `settings.local.json` commitado por acidente
> **Sintoma:** `git log` mostra `settings.local.json` sendo adicionado. Secrets no histórico.
>
> **Causa:** arquivo criado antes de adicionar ao `.gitignore`. Ou `.gitignore` não incluía a entrada correta.
>
> **Fix:**
> ```bash
> # Remover do tracking sem apagar o arquivo
> git rm --cached .claude/settings.local.json
>
> # Adicionar ao .gitignore
> echo ".claude/settings.local.json" >> .gitignore
>
> # Commitar a remoção
> git add .gitignore
> git commit -m "chore: remove settings.local.json do tracking"
> ```
> Se o secret já foi commitado e publicado, rotacione-o imediatamente — considere o secret comprometido mesmo após remover do git.

---

## Diagnóstico rápido

```mermaid
flowchart TD
    Prob["Sintoma observado"] --> Q1{"Agente pede\nconfirmação em tudo?"}
    Q1 -- "sim" --> A1["settings.json tem allow?\nConfigura Read(*) + Edit(*) + git básicos"]
    Q1 -- "não" --> Q2{"Agente faz ações\nperigosas sem perguntar?"}
    Q2 -- "sim" --> A2["allow tem glob amplo?\nSubstitui Bash(git *) por subcomandos específicos + deny"]
    Q2 -- "não" --> Q3{"Agente ignora\nconvenções do projeto?"}
    Q3 -- "sim" --> A3["CLAUDE.md existe e está\natualizado? Preenche seção Restrições"]
    Q3 -- "não" --> Q4{"Permissões globais\nsomem no projeto?"}
    Q4 -- "sim" --> A4["settings.json do projeto\nrepete o que precisa do global"]
    Q4 -- "não" --> Q5{"Secrets no git?"}
    Q5 -- "sim" --> A5["Move para settings.local.json\nAdiciona ao .gitignore\nRotaciona secrets"]
```

> [!tip] Assista: Permissions, settings.json, and plan mode: making one Claude Code session safe
> **Canal:** Tyler Renelle | **Duração:** ~26min | **Idioma:** EN
>
> Complementa as Armadilhas 1-5 explicando o mecanismo por trás delas: permission rules não sobrescrevem entre camadas, elas se **fundem** (allow/deny/ask de todos os arquivos são concatenados e deduplicados), e quando um allow e um deny colidem, o deny sempre vence — mesmo que venha de uma camada "mais fraca" na hierarquia geral de settings.
> Trecho de destaque [6:05]: *"If you write a deny rule, that's a wall the program enforces no matter what the model decides."*
>
> 🎬 [Assistir no YouTube](https://www.youtube.com/watch?v=CT9xynq7WZM)

---

## Tabela de diagnóstico rápido

| Problema | Primeira coisa a checar | Fix rápido |
|----------|------------------------|-----------|
| Confirmação em tudo | `allow` configurado? | Adiciona `Read(*)`, `Edit(*)`, git básicos |
| Ações perigosas sem perguntar | Glob amplo no `allow`? | Lista subcomandos + deny perigosos |
| Agente travado em tudo | `deny` cobre `Bash(*)`? | Torna deny cirúrgico |
| Variações do comando pedem confirmação | `*` no final do padrão? | Adiciona `"Bash(cmd *)"` |
| Permissões globais ignoradas | Projeto sobrescreve sem repetir? | Inclui explicitamente no projeto |
| Usa convenções erradas | CLAUDE.md existe? | Cria `.claude/CLAUDE.md` mínimo |
| CLAUDE.md não funciona | Tem placeholders? Está desatualizado? | Remove ruído; atualiza stack |
| Secrets no git | `settings.local.json` em `.gitignore`? | `git rm --cached`; rotaciona secret |

---

## Quando a configuração parece correta mas o comportamento é inesperado

Às vezes você tem certeza que configurou, mas o agente ainda não segue. Causas comuns:

**CLAUDE.md está no lugar errado.** Claude Code lê `CLAUDE.md` na raiz do projeto E `.claude/CLAUDE.md`. Se você criou em `.claude/CLAUDE.md` mas o agente parece ignorar, verifique se não há um `CLAUDE.md` desatualizado na raiz que está sendo lido primeiro e contraditando as instruções.

**A sessão foi iniciada antes da mudança.** Se você editou `settings.json` ou `CLAUDE.md` enquanto uma sessão estava aberta, as mudanças só entram em vigor na próxima sessão. Use `/clear` ou reinicie o Claude Code.

**O padrão no allow não está matchando o comando real.** O matching é de prefixo, não substring. `"Bash(npm test)"` cobre `npm test` mas não `npm test -- --watch`. Use `"Bash(npm test *)"` para cobrir todos os argumentos.

**Conflito entre camada global e projeto.** Se o global tem `"deny": ["Bash(git push *)"]` e o projeto precisa de push para CI, verifique se a camada local está permitindo explicitamente. Deny acumula entre camadas — um deny no global bloqueia em todos os projetos.

**Comando passado com path absoluto vs relativo.** `"Bash(find . -name *)"` não cobre `"Bash(find /home/user/repo -name *)"`. Se o agente usa path absoluto, o padrão precisa cobrir isso.

---

## Checklist de saúde da configuração

- [ ] `settings.json` tem allow list com operações básicas
- [ ] `settings.json` tem deny list com ações destrutivas
- [ ] `.claude/CLAUDE.md` existe com stack, convenções, restrições
- [ ] CLAUDE.md não tem placeholders `[...]` não preenchidos
- [ ] CLAUDE.md reflete a stack atual (nenhuma lib obsoleta mencionada)
- [ ] `settings.local.json` está no `.gitignore`
- [ ] Nenhum secret em `settings.json`
- [ ] `git log --all -- .claude/settings.local.json` não retorna commits

---

## Casos práticos

**Caso 1 — o allow amplo demais que quase forçou um push destrutivo.** Um time configurou `"Bash(git *)"` no `allow` global pensando em cobrir "todo comando git básico" de uma vez, sem revisar o que o glob realmente inclui. Semanas depois, numa sessão de limpeza de branches, o agente interpretou a instrução "sincroniza minha branch com o remoto" como justificativa suficiente para rodar `git push --force` — e o allow amplo deixou passar sem pedir confirmação. O incidente não chegou a sobrescrever histórico em `main` porque a branch de trabalho não era protegida, mas o susto expôs o problema real: `Bash(git *)` cobre `git push --force` tanto quanto `git status`, e o glob não distingue leitura de destruição. O fix aplicado foi exatamente o da Armadilha 2 — trocar o glob amplo por subcomandos explícitos no `allow` e adicionar `deny` cirúrgico para `git push --force *`, `git reset --hard *` e `git push * main`.

**Caso 2 — o secret commitado que exigiu rotação, não só remoção.** Um desenvolvedor criou `.claude/settings.local.json` com uma `STRIPE_SECRET_KEY` de teste antes de lembrar de adicionar o arquivo ao `.gitignore`. O commit foi feito, o push aconteceu, e só no dia seguinte alguém notou o arquivo no `git log`. A reação instintiva foi só rodar `git rm --cached` e considerar resolvido — mas isso remove o arquivo do tracking futuro, não do histórico: qualquer clone anterior ou fork já tem o secret nos commits antigos. O procedimento correto seguiu a Armadilha 12 até o fim: `git rm --cached .claude/settings.local.json`, entrada no `.gitignore`, commit da remoção — **e rotação imediata da chave**, tratando-a como comprometida independentemente de estar "só" num repositório privado. A lição que fica: para secrets, remover do git e rotacionar não são passos alternativos, são os dois obrigatórios.

---

## Como explicar em inglês

| Português | Inglês |
|-----------|--------|
| Armadilha | Pitfall / gotcha |
| Sintoma | Symptom |
| Configuração desatualizada | Stale configuration |
| Permissão muito abrangente | Overly broad permission |
| Rotacionar secret | Rotate the secret |

**Frases úteis:**
- "Without an allow list, every Bash call prompts for confirmation — even git status. Always configure at minimum Read(*), Edit(*), and basic git read commands."
- "A stale CLAUDE.md is worse than no CLAUDE.md — the agent follows wrong instructions confidently."
- "If you accidentally committed secrets, assume they're compromised and rotate them — removing from git history doesn't make them safe."

---

## O que vem a seguir

Depois de rodar o checklist e reconhecer qual armadilha bateu com o seu sintoma, o próximo passo é ir na causa raiz em vez de só aplicar o fix pontual: se o problema foi permissão, revise a sintaxe completa de `allow`/`deny` antes de editar às cegas; se foi CLAUDE.md, entenda a anatomia esperada do arquivo; se foi camada sobrescrevendo camada, revisite como a hierarquia de configuração resolve conflitos entre global e projeto.

- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/01 - Hierarquia de configuração|01 - Hierarquia de configuração]] — como as camadas interagem (a causa por trás da Armadilha 5)
- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json]] — referência de campos
- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/05 - Permissions|05 - Permissions]] — sintaxe detalhada de allow/deny (base das Armadilhas 1-4)
- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/07 - Pasta .claude|07 - Pasta .claude]] — o que vai no git e o que não vai (base das Armadilhas 11-12)
- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/index|Configuração]] — índice do galho

---

## Fontes

- **Anthropic** — *Claude Code settings* (2026). Referência de permissões e campos — https://docs.anthropic.com/pt/docs/claude-code/settings
- **Anthropic** — *Claude Code security* (2026). Boas práticas de segurança para configuração — https://docs.anthropic.com/pt/docs/claude-code/security
