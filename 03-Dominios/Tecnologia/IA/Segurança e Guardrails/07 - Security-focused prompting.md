---
title: "Security-focused prompting"
created: 2026-05-02
updated: 2026-05-02
type: concept
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
class TransferRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
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

## Veja também

- [[01 - Código gerado por IA é untrusted]]
- [[03 - Alucinações em código — APIs fantasma e parâmetros inexistentes]]
- [[04 - A pirâmide de validação AI]]
- [[Context Engineering|11 - Skills e instructions como contexto]]
- [[Spec-Driven Development|04 - Fase Specify — definindo outcomes e constraints]]

## Referências

- **Veracode** — *2025 GenAI Code Security Report* (2025) — limites do "prompting seguro genérico".
- **Anthropic** — *Best practices for Claude Code: Security* (2026).
- **OWASP Top 10 for LLM Applications* (2026).
- **Augment Code** — *AI Spec-Driven Development Workflows* (2026, security policies as context).
- **Microsoft Security** — *Prompt Injection Defense Patterns* (2026).
