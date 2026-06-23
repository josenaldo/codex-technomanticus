---
title: "08 - Privacy e PII em logs"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - observability
  - ia
  - pii
  - privacy
  - lgpd
  - gdpr
  - compliance
publish: true
aliases:
  - PII em logs LLM
  - Redaction de logs
  - LGPD em IA
  - GDPR em IA
---

# 08 - Privacy e PII em logs

> [!abstract] TL;DR
> Prompt e output de LLM contêm PII por default — usuário cola CPF na pergunta, conta detalhes de saúde, copia trecho de contrato. Logar trace cheio = construir base de PII com retenção indefinida e múltiplos acessos, exatamente o que LGPD, GDPR e EU AI Act regulam pesado. Solução não é "não logar"; é **redaction em captura** (Presidio, Google DLP, AWS Comprehend, regex caseiro pra padrões locais como CPF/CNPJ) + **políticas explícitas de retenção** (7-90 dias dependendo do propósito) + **consentimento explícito** pra uso em eval/treino. Em 2026: EU AI Act traz obrigações específicas pra sistemas de alto risco (saúde, jurídico, decisão de crédito); GDPR já cobria; LGPD traz mesmo princípio no Brasil. Sem política de PII no design da Logging Layer, observability vira passivo legal.

## Por que PII em log LLM é mais perigoso que em log tradicional

Log tradicional (Apache, app server) já é regulado, mas LLM amplifica três coisas:

1. **Input é livre** — usuário cola o que quiser na pergunta. Validação prévia é fraca por design (sistema é conversacional). PII chega "embrulhada" em texto comum
2. **Output pode reproduzir PII** — modelo cita partes do input no output; PII multiplicada em outro campo
3. **Trace é granular e fica acessível** — diferente de log de app server (consultado em incidente), trace é consultado todo dia por dev, PM, eval team. Mais acessos = mais vetores

Combinação: input livre + output amplificador + acesso amplo + retenção longa = base de PII "ad hoc" não declarada formalmente. Auditor de LGPD não vai gostar.

## O que conta como PII em LLM (categorias práticas)

| Categoria | Exemplos | Sensibilidade |
|---|---|---|
| **Identificadores diretos** | CPF, CNPJ, RG, SSN, email, telefone, endereço completo | Alta — facilmente atribuível |
| **Quasi-identifiers** | Nome + data de nascimento + cidade; nome + cargo + empresa | Média — agregam pra identificação |
| **Dados sensíveis (LGPD art. 5º, II)** | Saúde, orientação sexual, religião, opinião política, dados genéticos | Crítica — proteção reforçada |
| **Dados financeiros** | Número de cartão, conta bancária, salário, dívidas | Alta — fraude direta |
| **Credenciais** | Senhas, tokens, chaves de API | Crítica — leak operacional |
| **Conteúdo proprietário** | Código-fonte, contrato, documento interno | Variável — IP, NDA |

Lista regula o **mínimo a redactar**. Política de produto pode ampliar (ex: remover qualquer menção a nome próprio).

## Redaction em captura — o padrão certo

A escolha **fundamental** é: redactar antes do storage ou depois?

| Estratégia | Vantagem | Desvantagem |
|---|---|---|
| Capturar tudo, redactar na exibição | Replay perfeito | PII em storage; base regulada; acesso é vetor |
| **Redactar em captura, armazenar redacted** | Storage limpo; sem passivo regulatório | Replay perde PII original; alguns bugs ficam invisíveis |
| Capturar com cifragem em campo PII | Replay autenticado funciona; PII separada | Mais complexo; gerenciamento de chave |

**Default recomendado em 2026: redactar em captura.** Replay com placeholder cobre maioria dos casos. Casos que exigem PII real (auditoria, replay forense) usam cifragem em campo PII com chave separada e acesso logado.

### Ferramentas de redaction

| Ferramenta | Tipo | Cobertura |
|---|---|---|
| **Microsoft Presidio** | OSS, Python | NER + regex; modelo multi-idioma; extensível com padrões custom |
| **Google Cloud DLP** | Cloud API | 150+ infoTypes globais; alta precisão; pago |
| **AWS Comprehend (PII detection)** | Cloud API | PII detection + redaction managed |
| **Regex caseiro** | DIY | Padrões locais (CPF, CNPJ, CEP, telefone BR) — complemento essencial |

Padrões locais (Brasil) cobertos por regex:

```python
import re

PATTERNS = {
    "CPF":      re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),
    "CNPJ":     re.compile(r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b"),
    "CEP":      re.compile(r"\b\d{5}-?\d{3}\b"),
    "tel_BR":   re.compile(r"\b(?:\+?55\s?)?\(?\d{2}\)?\s?9?\d{4}-?\d{4}\b"),
    "email":    re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "cartao":   re.compile(r"\b(?:\d{4}[\s-]?){3}\d{4}\b"),
}

def redact(text: str) -> str:
    for label, pat in PATTERNS.items():
        text = pat.sub(f"<{label}>", text)
    return text
```

Combinar regex (recall alto pra padrões estruturados) + Presidio/DLP (precision em entidades como nome, endereço) cobre o espectro.

### Integração com o pipeline de captura

Em Langfuse SDK:

```python
from langfuse.decorators import observe, langfuse_context

@observe(name="chat-turn")
def chat_turn(user_input: str) -> str:
    # Redact ANTES de salvar no observation:
    safe_input = redact(user_input)
    langfuse_context.update_current_observation(input=safe_input)

    response = client.messages.create(
        messages=[{"role": "user", "content": user_input}],  # original vai pro provider
        ...,
    )

    safe_output = redact(response.content[0].text)
    langfuse_context.update_current_observation(output=safe_output)
    return response.content[0].text
```

Nota crítica: o **input enviado pro provider continua sendo o original** — provider precisa do dado real pra responder. O que muda é o que vai pro storage do trace. Mas o provider tem sua própria política de retenção que precisa ser auditada separadamente (Anthropic, OpenAI, Google têm DPAs com retenção típica de 30 dias, e Zero Data Retention via contrato pra clientes enterprise).

## Retention — quanto tempo guardar

Retention é **política explícita**, não default infinito.

| Propósito | Retenção típica | Justificativa |
|---|---|---|
| Debug em incidente | 7-14 dias | Cobertura de janela de SLA / detecção |
| Eval contínua / regression dataset | 30-90 dias | Suficiente pra detectar drift |
| Análise de produto / billing | 30-180 dias | Reporting trimestral |
| Compliance / auditoria | Conforme exigência legal (5 anos em alguns setores) | Apenas dados não-PII ou agregados |
| Treino de modelo | Apenas com consentimento explícito | Acima do "interesse legítimo" do GDPR |

Implementação: TTL no backend de storage (ClickHouse, S3 com lifecycle policy), separado por tabela/bucket. Traces vão pra "hot" (7d), "warm" (30d), "cold" (180d) com schemas progressivamente mais redacted.

## Marco regulatório — em uma página

### EU AI Act (em vigor desde 2024, full enforcement 2026)

- Classifica sistemas em **risco mínimo / limitado / alto / inaceitável**
- Sistemas de alto risco (recrutamento, crédito, educação, saúde, justiça): obrigações de logging, transparência, supervisão humana
- **Article 12** (logging): sistemas de alto risco devem manter logs automaticamente; logs servem rastreabilidade pós-mercado
- Tracing detalhado é exigência, não opção, em alto risco — mas com proteção de dados garantida

### GDPR (Reg UE 2016/679)

- Princípios aplicáveis a trace LLM: minimização (não logar mais do que necessário), limitação de finalidade (não usar trace de produção pra treino sem consentimento), prazo de retenção definido
- Direito ao esquecimento: usuário pode pedir deleção; trace precisa ser deletável por `user_id`
- Article 35: DPIA (Data Protection Impact Assessment) obrigatório pra processamento de alto risco

### LGPD (Lei 13.709/2018) — Brasil

- Princípios paralelos ao GDPR: necessidade, adequação, transparência, segurança, prevenção
- **Art. 5º, II**: dados sensíveis (saúde, biometria, religião, etc.) com proteção reforçada — consentimento específico
- **Art. 18**: direitos do titular (acesso, correção, anonimização, eliminação) — aplicáveis a logs
- ANPD pode multar em até 2% do faturamento, limitado a R$ 50M por infração

### Padrão comum aos três

- **Consentimento informado** pra uso de PII em treino/eval
- **Logging declarado** com finalidade explícita
- **Retenção definida** e justificável
- **Deletabilidade por usuário** (right to be forgotten)
- **Auditoria de acesso** — quem acessou que trace, quando

## Consentimento — onde sinalizar

Em produto end-user:

- Onboarding: termo claro de que conversas são logadas; finalidade (qualidade, segurança, eval)
- Opt-out granular: usuário pode pedir não-uso pra treino, mantendo trace pra debug operacional
- Indicador visual: ícone "this conversation is being recorded for quality" em algumas UIs (estilo call center)
- Modo privado / incognito: trace mínimo (só erros), sem captura de prompt/output

## Checklist mínimo pra Logging Layer compliant

- [ ] Redaction de PII no momento da captura (pipeline com Presidio + regex local)
- [ ] Política de retenção documentada por tipo de trace (hot/warm/cold)
- [ ] TTL implementado no backend de storage
- [ ] Deletabilidade por `user_id` (endpoint ou job)
- [ ] Auditoria de acesso ao backend de trace (quem viu, quando)
- [ ] Consentimento informado em onboarding do produto
- [ ] DPIA documentada se sistema é de alto risco (EU AI Act / GDPR)
- [ ] DPA assinada com providers (Anthropic, OpenAI, Google)
- [ ] Política de incident response em caso de leak

## Fontes

- **EU AI Act** — [Texto consolidado (artificialintelligenceact.eu)](https://artificialintelligenceact.eu/) · Article 12 (logging).
- **GDPR** — [Texto consolidado (gdpr-info.eu)](https://gdpr-info.eu/).
- **LGPD** — [Lei 13.709/2018 (planalto.gov.br)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) · ANPD ([anpd.gov.br](https://www.gov.br/anpd/pt-br)).
- **Microsoft Presidio** — [microsoft.github.io/presidio](https://microsoft.github.io/presidio/).
- **Google Cloud DLP** — [Documentação](https://cloud.google.com/dlp/docs).
- **AWS Comprehend** — [PII detection](https://docs.aws.amazon.com/comprehend/latest/dg/pii.html).
- **Anthropic** — [Trust Center](https://trust.anthropic.com/) · Data Processing Addendum.
- **OWASP** — [LLM Top 10 (2025)](https://owasp.org/www-project-top-10-for-large-language-model-applications/), incluindo LLM02 (Sensitive Information Disclosure).

## Veja também

- [[06 - Session replay e debugging]] — redaction afeta replay; estratégias de mitigação
- [[02 - Anatomia de um trace LLM]] — atributos onde PII costuma vazar (prompt em span attribute)
- [[03-Dominios/Tecnologia/IA/Segurança e Guardrails/11 - Governance as architecture — EU AI Act, GDPR, licenças]] — visão de governança end-to-end
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/11 - Logging Layer]] — onde a política de PII se materializa
- [[Dicionário de IA#LGPD|Dicionário: LGPD]], [[Dicionário de IA#GDPR|Dicionário: GDPR]], [[Dicionário de IA#EU AI Act|Dicionário: EU AI Act]]
