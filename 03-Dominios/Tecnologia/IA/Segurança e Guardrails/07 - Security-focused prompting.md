---
title: "Security-focused prompting"
created: 2026-05-02
updated: 2026-07-06
type: concept
fase: iniciado
progress: backlog
status: seedling
publish: true
tags:
  - seguranca-ia
  - ia
  - guardrails
  - prompting
aliases:
  - Security prompting
  - Constraining output
  - Pre-LLM guardrails
---

# Security-focused prompting

> [!abstract] TL;DR
> A primeira linha de defesa **antes** do código existir é o prompt. Não basta dizer "gere código seguro" — modelo concorda e gera inseguro do mesmo jeito ([[01 - Código gerado por IA é untrusted|Veracode 45%]]). Funciona: **constraining explícito** com policies, threat models, exemplos negativos, e schema enforcement. Esta nota dá os patterns que funcionam — e os que parecem funcionar mas não funcionam. Importante: security-focused prompting **não substitui** [[05 - SAST e SCA para código AI|SAST]] e [[06 - Permissões e sandboxing|sandbox]] — é a camada **anterior** delas, não substituta.

> [!question]- Por que security prompting não substitui guardrails de código?
> Prompting influencia probabilidades — aumenta a chance de o modelo gerar código com certas características, mas não garante. O modelo pode "concordar" com a instrução de segurança e ainda gerar código vulnerável porque seus pesos foram treinados em dados que contêm padrões inseguros. Guardrails de código (SAST, schema validation, sandboxing) são determinísticos — eles verificam o resultado independentemente da intenção declarada do modelo. A analogia: avisar um funcionário novo sobre as regras (prompting) não substitui os controles de acesso no sistema (guardrails). Os dois existem porque o primeiro falha com frequência mensurável.

Imagine o prompt: "Implemente o endpoint de transferência entre contas, com validações de segurança apropriadas." É razoável, é o que a maioria dos devs escreveria no dia a dia — e é exatamente o tipo de instrução que não funciona. O modelo concorda educadamente ("vou garantir validação de segurança...") e entrega uma função que checa se `amount` é positivo, nada além disso. Nenhuma checagem de ownership da conta, nenhuma proteção contra double-spend, nenhum tratamento de overflow decimal. O dev revisa, vê "tem validação", aprova o PR. Semanas depois, um pentest encontra exatamente a classe de vulnerabilidade que o prompt genérico devia ter evitado. Essa é a lacuna que os patterns desta nota fecham: o modelo não "recusou" ser seguro — "seguro" sem especificação concreta é um alvo que não aponta pra lugar nenhum.

## O que NÃO funciona

> [!warning] Mitos
>
> ❌ *"Gere código seguro"* — modelo concorda mas continua reproduzindo padrões inseguros do treino
>
> ❌ *"Use as melhores práticas de segurança"* — vago demais para acionar comportamento específico
>
> ❌ *"Não use SQL concatenation"* — pode evitar SQL e ainda criar XSS, SSRF, command injection
>
> ❌ *Listar 50 regras no [[Dicionário de IA#system prompt|system prompt]]* — atenção dilui ([[Context Engineering|03 - Context rot e atenção diluída]])
>
> ❌ *"Pense em segurança antes de escrever"* — não muda significantemente a saída

Veracode testou: prompt explícito sobre segurança **não moveu o ponteiro** dos 45%. Wishful thinking.

## O que funciona

### Pattern 1 — Threat model explícito

Em vez de "gere seguro", **declare o invasor**:

```
Você está implementando endpoint POST /transfer.

THREAT MODEL:
- Atacante autenticado tenta transferir do account de outro usuário
- Atacante envia amount negativo, decimal estranho, ou overflow
- Atacante envia destination conta inexistente, fechada, ou em outra moeda
- Atacante repete request para causar double-spend
- Atacante manipula header de currency

Para CADA classe de ataque acima, sua implementação DEVE ter validação que retorna 400 com mensagem clara.
```

Modelo agora tem **alvo concreto**. Resultado: validações específicas em vez de genéricas.

### Pattern 2 — Lista negativa explícita

```
PROIBIDO neste código:
- string concatenation em queries SQL (use parameterized)
- f-strings/template literals em comandos shell (use subprocess args)
- json.dumps sem validar schema
- pickle.loads em qualquer dado externo
- input() ou stdin direto em path/file ops (use os.path.normpath + check)
- eval() ou exec() sob nenhuma circunstância
- secrets em código (use env vars + secret manager)
```

Lista **acionável**, não filosofia. Modelo evita exatamente esses patterns.

### Pattern 3 — Schema enforcement

Em vez de pedir "valide input", **exija schema** e modelo gera com schema:

```
INPUT validation usando Pydantic com config:
- model_config = ConfigDict(extra="forbid")  # rejeita campos não declarados
- Todos os fields têm Field(..., validators)
- IDs externos são UUID4 ou int positivo (não string livre)
- Strings têm min_length e max_length explícitos
- Numbers têm ge/le explícitos
```

Por construção, output respeita schema rigoroso.

### Pattern 4 — Constraining via output format

Forçar formato estruturado limita superfície de ataque:

```
Output OBRIGATÓRIO em formato:

```python
# Section 1: Type definitions (Pydantic models)
class TransferRequest(BaseModel): model_config = ConfigDict(extra="forbid")
    # ...

# Section 2: Validation logic (pure functions)

# Section 3: Database operations (parameterized only)

# Section 4: Endpoint handler (FastAPI)
```
```

Modelo é guiado a separar concerns, em vez de gerar amalgama imprudente.

### Pattern 5 — Exemplos positivos

Em vez de só listar proibido, **mostre o certo**:

```
EXEMPLO de query segura neste projeto:

async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)  # SQLAlchemy parameterized
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

Não use string concat ou f-string em queries.
```

Modelo replica o pattern explícito > inferir o que é seguro.

### Pattern 6 — Context isolation (sub-agents)

Para tarefas sensíveis, use [[Economia de Tokens|10 - Sub-agentes especializados|sub-agente especializado]] com prompt focado:

```
Sub-agent: security-reviewer
Role: Revisar PR para vulnerabilidades específicas
Tools: read_file, grep
Cannot: write files

Foco em CWE-78, CWE-89, CWE-918, CWE-22 listados.
Para cada finding, output: file:line + tipo + sugestão de fix.
```

Sub-agente sem contexto poluído + foco estreito → melhor detecção.

## A diferença pré-LLM vs pós-LLM

| Pré-LLM (este nota) | Pós-LLM ([[Context Engineering\|12 - Guardrails determinísticos]]) |
|---|---|
| Constranger geração | Validar saída |
| Soft (probabilístico) | Hard (determinístico) |
| Pegada média | Pegada alta de classes específicas |
| Latência: zero | Latência: ms a segundos |
| **Não substitui** validação posterior | **Não substitui** prompting prévio |

Os dois juntos são defesa em profundidade.

## Templates reusáveis

### Template para feature de auth

```markdown
## Security policy para esta feature

THREAT ACTORS:
- Usuário malicioso tentando elevation of privilege
- Atacante tentando enumerar users (timing attacks, response differences)
- Atacante tentando session hijacking
- Insider threat com acesso parcial

CONSTRAINTS:
- Senhas: bcrypt com cost ≥12 (NUNCA hash simples)
- Tokens: random_urandom(32) + signing (HS256/RS256)
- Sessions: cookies com Secure, HttpOnly, SameSite=Strict
- Rate limit: max 5 tentativas/IP/min em login
- Logs: NUNCA log de senha, token, ou PII

OUTPUT requerido:
- Pydantic schemas com extra=forbid
- Funções de auth puras (testáveis)
- Endpoints FastAPI com Depends() para auth
- Testes unit cobrindo casos de falha
```

### Template para API pública

```markdown
## Security policy para API pública

THREAT MODEL:
- DOS via payload grande
- Injection (SQL, NoSQL, command, log)
- SSRF via URLs em parâmetros
- Path traversal em uploads
- Credential stuffing

CONSTRAINTS:
- max_body_size: 10MB
- rate_limit: 100/min/IP
- Input validation: Pydantic extra=forbid em tudo
- URLs externas: validate_host_in_allowlist()
- Files: pathlib.Path normalize + verify dentro de allowed_dir
- Logs: redact_pii() antes de log
```

## Embeber security em AGENTS.md

Em vez de repetir em cada prompt, registre no [[Context Engineering|11 - Skills e instructions como contexto|AGENTS.md]] do projeto:

```markdown
## Security policies (sempre aplicar)

- Pydantic com extra="forbid" em TODOS os boundaries
- Senhas: bcrypt cost ≥12
- Secrets: SEMPRE de env, nunca em código
- Queries SQL: parameterized only (nunca f-string, nunca concat)
- Comandos shell: subprocess.run com args list (nunca shell=True com input)
- Logs: redact_pii() antes de log de qualquer dado externo
- Imports: usar dependências do `requirements.txt` apenas; não inventar pacotes
```

Agente carrega isso como contexto permanente. Aplica sem precisar repetir.

## Métricas

| Métrica | Alvo |
|---|---|
| **% PRs com Pydantic extra=forbid em boundaries** | >90% |
| **% PRs com hardcoded secret detectado** | <2% |
| **% PRs com string-concat em queries SQL** | <1% |
| **Defect rate de vulns categorizadas** | Decrescente trimestre-a-trimestre |
| **Mean time entre prompt + scan** | <5 min |

## Anti-patterns

- **"Gere código seguro" sem mais detalhes** — placebo
- **System prompt com 200 linhas de "regras"** — atenção dilui, modelo ignora
- **Prompts diferentes por dev** — inconsistência massiva; centralize via AGENTS.md
- **Prompting como única camada** — não substitui SAST e sandbox
- **Sem exemplos positivos** — modelo precisa de ground truth, não só proibições
- **Generalismo** — "use HTTPS, sanitize input, hash senhas" sem especificar como

## Armadilhas comuns

> [!warning] "Gere código seguro" é placebo, não instrução
> Veracode testou: prompts explícitos de segurança genérica não movem o ponteiro dos 45% de código vulnerável. O modelo concorda com a instrução e reproduz os mesmos padrões inseguros que aprendeu nos dados de treino. O que funciona é instrução acionável e específica: listar quais CWEs são proibidos, dar exemplos negativos concretos, declarar o threat model com atacantes nomeados.

> [!warning] System prompt com 200 linhas de regras de segurança é contraproducente
> Atenção de LLMs dilui com o tamanho do contexto — regras no final de um prompt extenso têm peso muito menor que regras no início, ou que regras repetidas próximas ao pedido. Um AGENTS.md com 200 regras de segurança dá falsa sensação de cobertura: o modelo tecnicamente "tem" as regras mas não as aplica com consistência. Concentre em 5-10 regras críticas, acionáveis, com exemplos.

> [!warning] Prompting inconsistente entre desenvolvedores anula os benefícios
> Se cada dev usa seu próprio estilo de prompt de segurança, o time não tem um padrão. Um dev usa threat model explícito, outro usa "escreva código seguro", outro não menciona segurança. O resultado é qualidade de segurança variável dependendo de quem fez o prompt — exatamente o que um processo de segurança deveria eliminar. Centralizar via AGENTS.md resolve isso.

## Como explicar em inglês

Security-focused prompting is the practice of structuring your prompts to shift the probability distribution of LLM output toward more secure patterns — before any of the validation tooling runs. The key word is "shift": prompting doesn't guarantee security, it increases the likelihood of security-conscious patterns in the output.

What doesn't work is vague instruction. Saying "write secure code" or "follow security best practices" has been tested empirically by Veracode and shown not to move the needle on the 45% vulnerability rate. The model agrees with the instruction and still generates the same patterns it learned from training data.

What does work is explicit constraint: declare the threat model with named attackers and specific attack vectors. List what is forbidden with concrete technical specifics — not "validate input" but "use Pydantic with `extra='forbid'` and explicit field validators." Provide positive examples from the codebase so the model has ground truth to replicate rather than patterns to infer. Embed these policies in AGENTS.md so they apply consistently across every session without relying on individual developers to remember.

**In a technical interview**, you might say:

> "We treat security prompting as a probabilistic control, not a deterministic one. We structure it around explicit threat models — naming the attacker and the specific attack vectors for each endpoint — and explicit negative constraints with technical specifics, not philosophy. These live in AGENTS.md so every session starts with the same baseline. But we never rely on prompting alone: SAST with Semgrep and CodeQL catches what the model generates despite the instructions, and sandbox enforcement limits the blast radius if something slips through."

| PT | EN |
|----|-----|
| prompt de segurança | security prompt |
| modelo de ameaça | threat model |
| ator de ameaça | threat actor |
| restrição explícita | explicit constraint |
| lista negativa | negative list / deny list |
| exemplo positivo | positive example |
| controle probabilístico | probabilistic control |
| guardrail determinístico | deterministic guardrail |
| atenção diluída | diluted attention / context dilution |
| política de segurança | security policy |

## O que vem a seguir

Prompting tenta constranger a geração antes do código existir. Depois que o código existe, o próximo controle humano é o code review — mas code review de código AI não é igual a code review de código humano. O volume é diferente, os padrões de erro são diferentes, e o que o revisor precisa verificar muda substancialmente. A próxima nota explora como adaptar o processo de revisão para esse contexto.

- [[08 - Code review de código AI — o que muda]] — como o processo de revisão humana precisa ser adaptado quando o autor é um LLM

## Veja também

- [[01 - Código gerado por IA é untrusted]]
- [[03 - Alucinações em código — APIs fantasma e parâmetros inexistentes]]
- [[04 - A pirâmide de validação AI]]
- [[Context Engineering|11 - Skills e instructions como contexto]]
- [[Spec-Driven Development|04 - Fase Specify — definindo outcomes e constraints]]

## Referências

- **Veracode** — [*2025 GenAI Code Security Report*](https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/) (2025) — os 45% de falha em segurança que prompting genérico não move.
- **Anthropic** — [*Security — Claude Code Docs*](https://code.claude.com/docs/en/security) (2026) — modelo de permissões e controles de execução como guardrail complementar ao prompting.
- **OWASP Gen AI Security Project** — [*OWASP Top 10 for LLM Applications 2025*](https://genai.owasp.org/llm-top-10/) (2025) — taxonomia de risco (prompt injection, excessive agency) que o threat model do Pattern 1 precisa cobrir.
- **Augment Code** — [*What Is Spec-Driven Development?*](https://www.augmentcode.com/guides/what-is-spec-driven-development) (2026) — AGENTS.md e specs como contrato executável, base do padrão "Embeber security em AGENTS.md".
- **Microsoft Security Response Center** — [*How Microsoft defends against indirect prompt injection attacks*](https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks) (2025) — defesa em profundidade contra prompt injection, paralelo ao argumento "os dois juntos" desta nota.
