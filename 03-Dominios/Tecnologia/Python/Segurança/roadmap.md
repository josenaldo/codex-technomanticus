---
title: "Roadmap — Python Segurança"
created: 2026-07-11
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Segurança (galho 11)

Roadmap-folha do galho `Python/Segurança`. Fase **Adepto→Magus** — Auth (JWT/OAuth), OWASP, validação de input, secrets. Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Web e APIs REST/index.md` e `Python/Web e APIs REST/roadmap.md` (galho anterior, mesmo padrão).

Roster **não pré-cravado no spec** (só a descrição de alto nível "Auth (JWT/OAuth), OWASP, validação de input, secrets") — desenhado nesta sessão seguindo o mesmo playbook dos Galhos 5, 7, 8, 9 e 10. Terceiro galho do bloco **"Backend e arquitetura"** (9-13) — blinda a API construída no Galho 10.

**Descoberta importante desta sessão:** a trilha [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]] (Engenharia) já tem um sub-galho 4 ("Auth nos stacks") com notas dedicadas de implementação JWT/OAuth2 em Django e FastAPI (`pyjwt`, `authlib`, `pwdlib`, `OAuth2PasswordBearer`). Isso muda o roster deste galho: em vez de reensinar JWT/OAuth do zero, o roster foca em OWASP aplicado, injeção, XSS/CSRF, validação-como-segurança, secrets, supply chain e rate limiting — com UMA nota-ponte (05) que amarra a autenticação já ensinada em Auth e Identidade à API REST do Galho 10, sem repetir o mecanismo.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 9 |
| ⬜ pendente | 0 |
| ✅ feita | 9 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

---

## Notas

#### 01 - OWASP Top 10 aplicado a Python web — o mapa
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** panorama do OWASP Top 10 (2021, versão vigente) mapeado especificamente pra stacks Python web (Django/FastAPI/Flask) — para cada categoria, onde ela aparece no vault (SQL injection já em G9N01, XSS/CSRF nas notas 02-03 deste galho, secrets na nota 06, etc.) e o que é específico de Python. Funciona como mapa de navegação do galho, não desenvolve cada categoria a fundo (isso é nas notas seguintes).
- **Resultado:** 210 linhas / 3405 palavras (nota-mapa deliberadamente mais leve, sem código extenso). Abre com pentest achando 4 vulnerabilidades numa API só revisada funcionalmente; tabela das 10 categorias × significado em Python × destino no vault; diagrama mindmap; 2 exemplos curtos (ORDER BY sem allowlist, `HttpUrl` que não previne SSRF); explica honestamente por que A04/A08(parcial)/A09 ficam fora do escopo.

#### 02 - Injeção — SQL, template, comando e deserialização insegura
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** SQL injection revisitado brevemente (referencia G9N01 sem repetir), Server-Side Template Injection (SSTI) em Jinja2/Django templates (`{{ config.items() }}` como exemplo clássico de RCE), command injection via `subprocess.run(shell=True)`/`os.system`, deserialização insegura — `pickle.loads()` de dados não confiáveis como RCE trivial, contraste com `json`/formatos seguros.
- **Resultado:** 435 linhas / 5299 palavras. Abre com endpoint de "relatório personalizado" renderizando Jinja2 com input do usuário, explorado via `{{config.items()}}` vazando `SECRET_KEY`; desenvolve SSTI (cadeia `__class__`/`__mro__`/`__globals__` no nível de princípio, sequenceDiagram do ataque, comparação Django Templates), command injection (`shell=True` vs lista de args, caso ImageMagick), deserialização insegura (`pickle.loads()` via `__reduce__`, contraste com json/Pydantic/marshmallow/`yaml.safe_load()`). Warning enfático contra unpickling de fonte não confiável.

#### 03 - XSS e CSRF nos frameworks Python
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** XSS refletido/armazenado, autoescape automático em templates (Jinja2/Django Templates) e como `|safe`/`mark_safe` desliga a proteção, XSS em APIs JSON (raro mas existe — Content-Type sniffing). CSRF: proteção built-in do Django (`CsrfViewMiddleware`/token), por que APIs stateless com JWT em header (não em cookie) são naturalmente imunes a CSRF — explica o mecanismo, referenciando a autenticação JWT já coberta em Auth e Identidade sem repetir.
- **Resultado:** 467 linhas / 6990 palavras. Abre com stored XSS via `|safe` numa bio de perfil Django; cobre autoescape/`|safe`/`mark_safe`, correção via `bleach`, XSS em APIs JSON como estruturalmente raro; CSRF clássico contra cookie de sessão vs. imunidade estrutural de JWT em header (2 sequenceDiagrams comparativos); tabela de decisão CSRF necessária/redundante.

#### 04 - Validação de input como controle de segurança
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** revisita Pydantic (Galho 10 nota 03) sob a lente de segurança — o que a validação de TIPO previne (nem tudo: um `str` válido ainda pode conter payload malicioso) e o que ela NÃO previne (SSRF, path traversal, XSS armazenado). Allowlist vs denylist como princípio geral. Validação de upload de arquivo (extensão/magic bytes/tamanho) como caso prático.
- **Resultado:** 506 linhas / 6336 palavras. Abre com upload de foto de perfil validado só por extensão, explorado com script disfarçado de `.jpg`; desenvolve 3 camadas de validação (forma/conteúdo/destino, diagrama Mermaid), allowlist vs denylist, correção completa do upload (magic bytes, limite de tamanho, nome UUID gerado no servidor).

#### 05 - Autenticação e autorização na prática — a ponte com Auth e Identidade
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** nota-ponte curta que NÃO reensina JWT/OAuth2 — amarra o que já foi ensinado em [[03-Dominios/Engenharia/Auth e Identidade/4 - Auth nos stacks/03 - Python — FastAPI|Auth e Identidade SG4 nota 03]] (FastAPI) e [[03-Dominios/Engenharia/Auth e Identidade/4 - Auth nos stacks/02 - Python — Django|nota 02]] (Django) ao contexto da API REST construída no Galho 10: onde o `Depends(get_current_user)` entra no pipeline de dependências (Galho 10 nota 04), como o contrato de erro 401/403 se encaixa no tratamento de erros padronizado (Galho 10 nota 06). Menção breve a `permission_classes` do DRF (Galho 10 nota 05) agora desenvolvida.
- **Resultado:** 348 linhas / 4308 palavras (nota-ponte deliberadamente mais curta). Abre com IDOR — endpoint que checa `Depends(get_current_user)` mas nunca filtra por posse, expondo tarefa de outro usuário; desenvolve `Depends(get_current_user)` plugado no pipeline do Galho 10 (sequenceDiagram), 401/403 no contrato de erro da nota 06, correção da checagem de posse vulnerável/corrigida, paralelo com `permission_classes`/`get_queryset` do DRF.

#### 06 - Secrets e configuração segura
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto→Magus
- **Escopo:** por que secret hardcoded no código é o erro mais comum e mais caro, variáveis de ambiente (`os.environ`/`python-dotenv`), `.env` no `.gitignore` (e o que fazer quando já vazou num commit — referência a `git-filter-repo`/rotação imediata), secret scanning (`detect-secrets`/`gitleaks` em pre-commit/CI), `pydantic-settings` (`BaseSettings`) como padrão moderno de configuração tipada, menção a secret managers de produção (Vault/AWS Secrets Manager/GCP Secret Manager) sem aprofundar (fora do escopo didático, é infra).
- **Resultado:** 428 linhas / 4858 palavras. Abre com `SECRET_KEY` de scaffold do Django nunca trocado + `.env` commitado por `.gitignore` tardio; desenvolve permanência do git (warning enfático: rotacionar primeiro), env vars/`python-dotenv`, secret scanning (sequenceDiagram do fluxo de detecção), `pydantic-settings`/`BaseSettings` com fail-fast. Menção breve a Vault/AWS/GCP linkando pra Engenharia/Segurança.

#### 07 - Segurança de dependências e supply chain
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto→Magus
- **Escopo:** por que uma dependência de terceiros é superfície de ataque (o caso `event-stream`/similares como motivação), `pip-audit`/`safety` (scan de CVEs conhecidas em dependências instaladas), lockfiles (`uv.lock`/`poetry.lock`/`requirements.txt` pinado com hash) vs. ranges soltos, typosquatting (pacotes com nome parecido ao popular), menção breve a SBOM (Software Bill of Materials) como prática emergente.
- **Resultado:** 371 linhas / 5221 palavras. Abre com o incidente REAL do PyPI `ctx` (maio 2022, domínio de email de mantenedor expirado, account takeover, exfiltração de `os.environ`); desenvolve `pip-audit` (scan/CI/`--fix`), lockfiles, typosquatting + dependency confusion (pesquisa de Alex Birsan 2021), SBOM breve, Dependabot/Renovate.

#### 08 - Rate limiting e proteção contra abuso
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** por que um endpoint de login sem rate limit é convite a brute force/credential stuffing, `slowapi` no FastAPI (baseado em `limits`, algoritmo de janela), `django-ratelimit` no Django, estratégias (por IP, por usuário autenticado, por API key), o que rate limiting NÃO resolve (DDoS distribuído de verdade é problema de infra/CDN, não de aplicação — fronteira honesta).
- **Resultado:** 455 linhas / 6921 palavras. Abre com credential stuffing (50 mil tentativas/hora detectadas via CPU do banco); desenvolve `slowapi`/`django-ratelimit`, fixed vs sliding window, estratégias de chave (com warning sobre `X-Forwarded-For` spoofável), 429 no contrato de erro da nota 06 do Galho 10. Fronteira honesta sobre DDoS volumétrico.

#### 09 - Capstone — hardening da API do Galho 10
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** recapitula o galho pegando a API de Tarefas construída na capstone do Galho 10 (que tinha `usuario_id` como query param, deliberadamente sem autenticação) e blindando-a: adiciona autenticação JWT real via `Depends(get_current_user)` (referenciando Auth e Identidade SG4 nota 03 sem repetir o mecanismo — nota 05 deste galho já fez a ponte), corrige um caso de SSTI/injeção introduzido de propósito, move secrets pra `.env`/`BaseSettings`, adiciona rate limiting no endpoint de criação de conta/login. Cenário prático integrador, não introduz conceito novo raso. Aponta para o Galho 12 (Testes) como próximo passo natural (a API blindada ainda não tem suite de testes).
- **Resultado:** 726 linhas / 6612 palavras. 6 etapas incrementais: (1) `Depends(get_current_user)` real via JWT/pwdlib; (2) Broken Access Control corrigido em todos os endpoints (404 uniforme, não 403); (3) endpoint novo de busca-com-highlight introduzindo e corrigindo SSTI; (4) `DATABASE_URL`/`JWT_SECRET` via `pydantic-settings` fail-fast; (5) `slowapi` em `/usuarios`/`/token` com chave por conta contra credential stuffing distribuído; (6) campo `anexo_url` revisitando validação de forma vs destino (DNS+blocklist de IP privado). 3 diagramas Mermaid, tabela antes/depois de ataques. Fecha o galho apontando pro Galho 12 (Testes).

> [!success] Galho 11 completo — 9/9 notas (2026-07-11)
> Mapa OWASP Top 10 (01) → injeção SQL/SSTI/comando/deserialização (02) → XSS/CSRF (03) → validação como controle de segurança (04) → ponte com Auth e Identidade/Broken Access Control (05) → secrets e configuração segura (06) → supply chain (07) → rate limiting (08) → capstone de hardening da API do Galho 10 (09). Descoberta central da sessão: JWT/OAuth2 já tinham casa profunda em Auth e Identidade SG4 — o galho usou esse fato pra evitar duplicação e focar na camada de aplicação Python-específica (injeção, XSS/CSRF, validação-como-segurança, secrets, supply chain, rate limiting). Próximo da trilha: Galho 12 — Testes.

## Decisões e fronteiras registradas

- JWT/OAuth2/sessões em profundidade (mecanismo, `pyjwt`, `OAuth2PasswordBearer`, fluxos) → [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]] SG4; aqui só a nota 05 (ponte) e a capstone (09) consomem, sem reexplicar.
- Conceitos criptográficos (hashing, PKI, MAC/HMAC, criptografia simétrica/assimétrica) e classes de vulnerabilidade genéricas → [[03-Dominios/Engenharia/Segurança/index|Engenharia/Segurança]]; aqui é só a aplicação Python.
- Mecânica do Pydantic (`BaseModel`/`Field`/`response_model`) → Galho 10 nota 03; aqui a nota 04 revisita sob lente de segurança, sem repetir a API.
- SQL injection em profundidade (bind parameters, `Table`/`MetaData`) → Galho 9 nota 01; aqui a nota 02 só referencia como abertura do tema "injeção" mais amplo.
- Testes de segurança (fuzzing, testes de autorização automatizados) → Galho 12 (Testes), não desenvolvido aqui.
- Infra de secret management (Vault/cluster K8s) → fora do escopo didático deste galho, só mencionado.
