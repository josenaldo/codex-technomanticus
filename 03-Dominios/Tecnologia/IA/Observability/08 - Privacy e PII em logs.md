---
title: "08 - Privacy e PII em logs"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
fase: iniciado
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

> [!question]- Qual é a diferença entre redactar PII "em captura" versus "na exibição" — e por que a escolha importa tanto?
> **Redaction em exibição** = o trace armazena o dado real, mas a UI mostra um placeholder ao abrir. O dado real continua no storage — se o Langfuse for comprometido, ou se um dev com acesso de debug exportar o trace, a PII vaza. **Redaction em captura** = o placeholder vai pro storage desde o início. Jamais existiu dado real no sistema de observability. A diferença regulatória é enorme: em LGPD/GDPR, manter dado pessoal em sistema sem base legal explícita é infração, independente de exibir ou não. Se a redaction é em captura, o sistema de observability simplesmente não tem PII pra declarar — o escopo do DPIA e dos Data Processing Agreements diminui substancialmente.

## Por que PII em log LLM é mais perigoso que em log tradicional

Log tradicional (Apache, app server) já é regulado, mas LLM amplifica três coisas:

1. **Input é livre** — usuário cola o que quiser na pergunta. Validação prévia é fraca por design (sistema é conversacional). PII chega "embrulhada" em texto comum
2. **Output pode reproduzir PII** — modelo cita partes do input no output; PII multiplicada em outro campo
3. **Trace é granular e fica acessível** — diferente de log de app server (consultado em incidente), trace é consultado todo dia por dev, PM, eval team. Mais acessos = mais vetores

Combinação: input livre + output amplificador + acesso amplo + retenção longa = base de PII "ad hoc" não declarada formalmente. Auditor de LGPD não vai gostar.

O ponto menos óbvio é o **output amplificador**: quando o modelo cita "você mencionou que seu CPF é 123.456.789-00", esse dado agora aparece no span de output também — e eventualmente em evals que comparam outputs. PII que entrou em um campo pode vazar em múltiplos campos antes de chegar ao storage.

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

Quasi-identifiers são frequentemente subestimados: "João Silva, gerente de TI, empresa X, 38 anos" não tem CPF, mas é suficiente para identificar a pessoa univocamente em bancos de dados públicos. Modelos de NER (Presidio, spaCy) capturam nome e cargo mas não o que torna a combinação identificável — julgamento humano é necessário na definição de política.

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

Teste de falsos negativos é tão importante quanto a implementação: injete PII sintética conhecida no pipeline de redaction e meça quantas passam. Um rate de falsos negativos abaixo de 1% é razoável pra produção; acima disso, a política não está funcionando na prática. Automatize esse teste no CI/CD junto com os testes de regressão da redaction.

**Problema de recall em português:** Presidio foi treinado primariamente em inglês. Para português brasileiro, a precisão de NER cai para nome de pessoas, cargos, e endereços. O modelo multilingual do Presidio (`transformers`-based) melhora isso mas é mais lento (~3-5× vs regex). Uma abordagem pragmática: regex pra padrões estruturados (CPF, CNPJ, email, cartão) + Presidio multilingual pra entidades de texto livre + revisão periódica de falsos negativos.

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

Atenção ao **direito ao esquecimento**: mesmo que a retenção seja de 30 dias, se um usuário solicitar deleção antes desse prazo, o sistema deve conseguir deletar por `user_id` imediatamente. Isso exige que traces sejam particionados ou indexados por `user_id` — nem todos os backends de trace fazem isso por padrão. Valide antes de declarar compliance.

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

Na prática, o maior risco de não-conformidade não vem de ignorar as leis — vem de declarar compliance sem verificar a implementação. Um checklist de conformidade desenhado por jurídico não vale nada se a equipe de engenharia não rodou o teste de falsos negativos da redaction, não configurou o TTL no ClickHouse, ou não validou que o DPA com o provider cobre o regime de retenção prometido aos usuários. Compliance de logging exige colaboração jurídico-engenharia, não documentos isolados.

## Consentimento — onde sinalizar

Em produto end-user:

- Onboarding: termo claro de que conversas são logadas; finalidade (qualidade, segurança, eval)
- Opt-out granular: usuário pode pedir não-uso pra treino, mantendo trace pra debug operacional
- Indicador visual: ícone "this conversation is being recorded for quality" em algumas UIs (estilo call center)
- Modo privado / incognito: trace mínimo (só erros), sem captura de prompt/output

Em produto B2B / enterprise:

- Consentimento vem do DPA com o cliente, não do usuário final individual (que é funcionário do cliente)
- Cliente define a política de uso de dados dos seus usuários
- Você (vendor) segue o DPA assinado — que precisa permitir explicitamente debug operacional, eval, e melhoria de produto (ou proibir cada um separadamente)
- Manter log de qual versão do DPA estava em vigor na data de cada trace — em caso de disputa, você precisa saber qual contrato cobria aquele dado

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
- [ ] Log de versão de DPA por trace (em contexto B2B)
- [ ] Teste de falsos negativos da redaction (qual % de PII passa pelo filtro?)
- [ ] Verificação de que output também é redacted (não só input)
- [ ] Revisão semestral da política de retenção vs regulatório vigente
- [ ] Treinamento do time de engenharia sobre o que é PII e onde ela aparece em traces

## Impacto de redaction no eval e replay

O trade-off mais concreto de redaction em captura é que **eval e replay ficam menos fiéis**:

- Se o bug depende de como o modelo processa um CPF específico (ex: validação num contrato), replay com `<CPF>` não reproduz o comportamento
- Se o eval usa o input original como parte da rubrica ("o modelo citou o nome do cliente?"), o campo `input` redacted elimina essa verificação

Estratégias de mitigação:

1. **Synthetic PII:** antes de salvar no trace, troca PII real por PII sintética plausível (CPF válido gerado, nome aleatório da mesma etnia) — mantém estrutura linguística sem dado real
2. **Cifragem de campo:** armazena PII cifrada com chave separada; campo exibido é o placeholder; replay autenticado descriptografa. Mais complexo mas preserva fidelidade.
3. **Segmentação de eval:** avalia sem input PII (métricas de qualidade que não precisam do dado bruto) e avalia com input sintético (métricas que precisam de estrutura similar)

A escolha da estratégia depende do domínio: em assistente de escrita, redaction simples basta. Em aplicativo de saúde onde o modelo interpreta contexto clínico, synthetic PII ou cifragem são necessários.

Independente da estratégia escolhida, documente no DPA qual estratégia está em uso e por que — o auditor vai perguntar não só "vocês redactam?" mas "vocês conseguem reproduzir um bug que envolve dado sensível sem expor PII real?"

## Zero Data Retention (ZDR) com providers

Providers como Anthropic e OpenAI oferecem **Zero Data Retention** (ZDR) via contrato enterprise: o provider não armazena inputs/outputs após o processamento da requisição.

Implicações:

- **Sem risco de leak no provider:** ZDR elimina o vetor de "Anthropic sofre breach e nossos dados de usuário aparecem"
- **Sem uso pra treino:** os ToS padrão permitem uso de inputs pra melhoria do modelo (com opt-out). ZDR garante que isso não acontece.
- **Custo:** ZDR geralmente exige contrato enterprise (acima de um threshold de spend ou via acordo direto)
- **Compatibilidade:** algumas features (prompt caching, fine-tuning) podem ser limitadas ou indisponíveis com ZDR

Para sistemas em domínios regulados (LGPD art. 5º, II; GDPR art. 9º) processando dados sensíveis, ZDR é o mínimo razoável — e deve aparecer como cláusula no DPIA/DPA.

Uma distinção importante: ZDR cobre o **provider de modelo** (Anthropic, OpenAI), não a sua própria stack de observabilidade. Você pode ter ZDR com o Anthropic e ainda assim estar armazenando PII por anos no seu Langfuse self-hosted, porque ninguém configurou TTL no ClickHouse. As duas camadas exigem política separada: uma pra o fluxo de dados pra fora do seu sistema (provider), outra pra o fluxo de dados interno (trace backend).

Verifique a Trust Center de cada provider pra status atual: [trust.anthropic.com](https://trust.anthropic.com), [openai.com/security](https://openai.com/security).

## Armadilhas comuns

> [!warning] Logar o prompt em `span.set_attribute` em vez de `span.add_event` — PII indexada como coluna
> Backends OTel indexam atributos de span (aparecem como colunas no ClickHouse, no Datadog). Se você coloca `span.set_attribute("prompt", user_input)`, o conteúdo fica indexado, searchable, e potencialmente em dashboards. A prática correta é colocar prompt e resposta como **span events** (não atributos indexados) — aparecem nos detalhes do span mas não viram colunas pesquisáveis. Reserve atributos indexados pra metadata anônima (`prompt_version`, `feature`, `model`).

> [!warning] Acreditar que o provider não retém dados porque o ToS padrão diz "optamos você para fora"
> Os ToS de Anthropic, OpenAI e Google têm opt-out de uso de dados pra treino acessível via configuração — mas isso é diferente de Zero Data Retention. Por padrão, providers retêm inputs/outputs por 30-60 dias pra abuse detection, compliance interno, e logging de API. ZDR real exige contrato específico. Verifique a Trust Center e o DPA assinado antes de declarar que "dados de usuário não ficam no provider".

> [!warning] Política de retenção documentada mas sem TTL implementado no backend
> Muitas equipes documentam "retemos traces por 30 dias" mas não configuram lifecycle policy no backend (ClickHouse TTL, S3 lifecycle rules). Dados ficam indefinidamente por inércia. Em caso de auditoria, a declaração e a prática divergem — o auditor vai encontrar traces de 2 anos no bucket onde a política diz 30 dias. Implemente TTL no mesmo sprint em que escreve a política.

## Como explicar em inglês

**Interview quote:** *"We treat our observability stack as a PII processor under LGPD. We redact at capture time before anything hits storage — placeholders in, full text out to the model. We have explicit retention TTLs per data class, a signed DPA with Anthropic for Zero Data Retention, and a user-facing opt-out for eval usage. The logging layer went through a DPIA before we launched."*

| Português | Inglês |
|---|---|
| Redação de PII no momento da captura | PII redaction at capture time |
| Dado pessoal identificável | Personally Identifiable Information (PII) |
| Minimização de dados (princípio) | Data minimization (principle) |
| Retenção de dados por prazo definido | Data retention with defined TTL |
| Direito ao esquecimento / deleção | Right to erasure / right to be forgotten |
| Avaliação de impacto de proteção de dados | Data Protection Impact Assessment (DPIA) |
| Acordo de processamento de dados | Data Processing Agreement (DPA) |
| Retenção zero de dados pelo provider | Zero Data Retention (ZDR) |
| Consentimento informado pra uso em treino | Informed consent for training usage |
| Auditoria de acesso ao trace | Trace access audit log |

## O que vem a seguir

Com o galho Observability completo — de por que logar (01) à anatomia do trace (02), ferramentas (03-04), versionamento (05), replay (06), métricas (07) e privacy (08) — a stack de observabilidade de LLM está completa. O próximo galho, Multimodal Prompting, abre um domínio diferente: como estruturar inputs que misturam texto, imagens, áudio e documentos — e as peculiaridades de cada modalidade no contexto de modelos como Claude e GPT-4o.

## Fontes

- **EU AI Act** — [Texto consolidado (artificialintelligenceact.eu)](https://artificialintelligenceact.eu/) · Article 12 (logging).
- **GDPR** — [Texto consolidado (gdpr-info.eu)](https://gdpr-info.eu/).
- **LGPD** — [Lei 13.709/2018 (planalto.gov.br)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) · ANPD ([anpd.gov.br](https://www.gov.br/anpd/pt-br)).
- **Microsoft Presidio** — [microsoft.github.io/presidio](https://microsoft.github.io/presidio/).
- **Google Cloud DLP** — [Documentação](https://cloud.google.com/dlp/docs).
- **AWS Comprehend** — [PII detection](https://docs.aws.amazon.com/comprehend/latest/dg/pii.html).
- **Anthropic** — [Trust Center](https://trust.anthropic.com/) · Data Processing Addendum.
- **OWASP** — [LLM Top 10 (2025)](https://owasp.org/www-project-top-10-for-large-language-model-applications/), incluindo LLM02 (Sensitive Information Disclosure) e LLM06 (Sensitive Information Disclosure via output).
- **ANPD** — [Gov.br/anpd](https://www.gov.br/anpd/pt-br). Guias de boas práticas e resoluções sobre IA (publicados em 2024-2025).
- **Trask (homomorphic encryption for PII)** — abordagem alternativa emergente: processar dado cifrado sem descriptografar.

## Veja também

- [[06 - Session replay e debugging]] — redaction afeta replay; estratégias de mitigação
- [[02 - Anatomia de um trace LLM]] — atributos onde PII costuma vazar (prompt em span attribute)
- [[03-Dominios/Tecnologia/IA/Segurança e Guardrails/11 - Governance as architecture — EU AI Act, GDPR, licenças]] — visão de governança end-to-end
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/11 - Logging Layer]] — onde a política de PII se materializa
- [[Dicionário de IA#LGPD|Dicionário: LGPD]], [[Dicionário de IA#GDPR|Dicionário: GDPR]], [[Dicionário de IA#EU AI Act|Dicionário: EU AI Act]]
- [[Dicionário de IA#Redaction|Dicionário: Redaction]], [[Dicionário de IA#Zero Data Retention|Dicionário: ZDR]]
- [[Dicionário de IA#DPIA|Dicionário: DPIA]], [[Dicionário de IA#DPA|Dicionário: DPA (Data Processing Agreement)]]
