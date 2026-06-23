---
title: "06 - Como dizer ao modelo o tipo de leitura"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - multimodal
  - prompt-engineering
  - ia
  - reading-instruction
publish: true
aliases:
  - Reading instruction
  - Tipo de leitura
  - Dirigir a leitura do modelo
---

# 06 - Como dizer ao modelo o tipo de leitura

> [!abstract] TL;DR
> A mesma imagem rende outputs radicalmente diferentes dependendo do **tipo de leitura** que você pede. "Descreva esta tela" vs "Analise esta tela quanto a problemas de acessibilidade" vs "Extraia os campos de formulário desta tela" entregam respostas que mal se reconhecem como vindas do mesmo input. Esta nota cobre seis tipos de leitura — descritiva, analítica, extrativa, comparativa, diagnóstica, avaliativa — e um template prático com quatro slots: **Reading instruction**, **Focus**, **Ignore**, **Output**. É a técnica que mais melhora qualidade sem trocar de modelo, sem subir resolução, sem mais tokens de input.

## Por que dizer o tipo de leitura importa

Um modelo multimodal recebe a imagem e tem que decidir o quê "ver". Sem instrução explícita, ele cai no comportamento default — geralmente descrição genérica do que está visualmente saliente, contaminada pelos exemplos do treino ("foi treinado pra fazer caption ⇒ entrega caption"). Resultado: você queria diagnóstico, recebeu descrição. Queria extração, recebeu narração.

A solução não é melhor modelo nem mais resolução. É declarar, no prompt, **qual processo cognitivo o modelo deveria seguir**. Mudança barata, ganho grande.

Caso concreto. Mesma imagem (screenshot de tela de login com problemas de UX), três prompts:

> **Prompt 1**: "Descreva esta imagem."
> Output: "A imagem mostra uma tela de login com um campo de email, um campo de senha, um botão azul escrito 'Entrar', e um link 'Esqueci minha senha'."

> **Prompt 2**: "Analise esta tela quanto a problemas de UX."
> Output: "Problemas visíveis: (1) o campo de senha não tem toggle de visibilidade; (2) o label 'Email' não está associado ao input via for/id, prejudicando acessibilidade; (3) não há indicador visual do estado de erro ou validação..."

> **Prompt 3**: "Extraia o estado atual do formulário e retorne em JSON."
> Output: `{"campos": [{"label": "Email", "preenchido": false, "tipo": "email"}, ...]}`

Três outputs úteis — três outputs diferentes — três tarefas diferentes. O modelo não adivinha; você manda.

## Os seis tipos de leitura

Útil pensar em **seis modos de leitura** que cobrem 95% dos casos:

### 1. Descritiva

"O que está na imagem?" — Caption, alt text, indexação. Modelo descreve o que vê, sem julgar nem extrair.

**Quando:** alt text, indexação semântica, descrição pra acessibilidade.

```
Descreva esta imagem em uma frase curta, otimizada para alt text.
Foque no conteúdo principal e na função visual. Não invente detalhes
que não consegue ver claramente.
```

### 2. Analítica

"O que essa imagem significa? O que ela demonstra?" — Interpretação de gráfico, conclusão a partir de evidência visual.

**Quando:** análise de dashboard, leitura de gráfico, interpretação de mockup.

```
Analise este gráfico de receita trimestral. Identifique:
- A tendência geral (alta, baixa, estável)
- Pontos de inflexão e possíveis causas observáveis
- Quaisquer anomalias visuais (escalas distorcidas, eixo Y não começando em zero)
```

### 3. Extrativa

"Liste os fatos contidos na imagem." — OCR + estruturação.

**Quando:** captura de formulário, extração de tabela, transcrição.

```
Extraia desta imagem em JSON:
- nome do produto
- preço (apenas o número)
- moeda
- avaliação em estrelas (1-5, decimal)
Se algum campo não for visível ou for ilegível, marque null. Não invente.
```

### 4. Comparativa

"Compare A com B e diga o que difere." — Before/after, A/B test, design review.

**Quando:** revisão de mudança, comparação de duas versões, contraste de opções.

```
Compare as duas telas (A = primeira, B = segunda).
Liste apenas diferenças visíveis e relevantes para UX:
- Estrutura de layout
- Hierarquia visual (tamanho, contraste, peso tipográfico)
- Estados de interação (foco, hover, disabled)
Ignore: diferenças de pixel resultantes de compressão ou anti-aliasing.
```

### 5. Diagnóstica

"O que está errado aqui? Por quê?" — Debug, troubleshoot, RCA visual.

**Quando:** bug em UI, falha em layout, erro em screenshot de monitoramento.

```
Esta é uma captura de tela de bug em produção.
Comportamento esperado: <descreva>
Comportamento observado: o dropdown aparece atrás do modal.

Analise a imagem e proponha hipóteses ordenadas pela evidência visual,
da mais provável pra menos provável. Pra cada hipótese, indique:
- O que da imagem sustenta a hipótese
- Que evidência adicional seria necessária pra confirmar
```

### 6. Avaliativa

"Isso atende a este critério?" — Compliance, conformidade, auditoria.

**Quando:** checagem de acessibilidade, conformidade com brand guidelines, auditoria de heurística.

```
Avalie este mockup contra as 10 heurísticas de Nielsen.
Para cada heurística, indique:
- Atende (sim / parcialmente / não)
- Evidência visual da resposta
- Severidade se não atende (1-5)

Heurísticas:
1. Visibility of system status
2. Match between system and the real world
...
```

## O template — quatro slots

Pra qualquer leitura, quatro slots cobrem o essencial:

```
Reading instruction: <um dos 6 tipos — descritiva, analítica, extrativa,
                     comparativa, diagnóstica, avaliativa>
Focus:              <o que o modelo deve atender com cuidado>
Ignore:             <o que o modelo deve descartar ou tratar como ruído>
Output:             <forma final esperada — prosa, JSON, lista, tabela>
```

Exemplo aplicado a screenshot de dashboard financeiro:

```
Reading instruction: Análise.
Focus:               KPIs do topo, variação YoY, formatação condicional
                     (verde/vermelho) que indica status.
Ignore:              Header, footer, navegação lateral, ícones decorativos.
Output:              JSON com {kpi, valor, variacao_yoy, status}.
```

Os slots não precisam virar literalmente esses tokens. Podem ser parágrafo natural. A função é forçar você a tomar quatro decisões explícitas antes de enviar.

## Pares before/after

### Caso A — Mockup de homepage

**Before:**
```
O que tem nessa página?
```
Output esperado: descrição genérica ("hero com título grande, três cards com features, footer com links...").

**After:**
```
Reading instruction: Avaliativa.
Focus: Hierarquia visual (qual é o CTA principal?), contraste de texto sobre
       imagem do hero, alt-text inferível em cada imagem.
Ignore: Cores específicas de brand, escolha tipográfica.
Output: Lista numerada de problemas, cada um com (a) qual elemento, (b) qual
        princípio é violado, (c) severidade 1-5.
```
Output esperado: lista priorizada de issues, útil pra design review.

### Caso B — Print de erro do navegador

**Before:**
```
Que erro é esse?
```
Output esperado: leitura do texto do erro ("Stack overflow at line 42").

**After:**
```
Reading instruction: Diagnóstica.
Focus: Mensagem do erro, stack trace visível, estado do DevTools (Network,
       Console, Sources se aparecer).
Ignore: Layout da página subjacente, conteúdo não relacionado ao erro.
Output: (1) Hipótese mais provável de causa, com 1-2 linhas de justificativa;
        (2) Próximo passo concreto pra confirmar.
```
Output esperado: hipótese acionável.

### Caso C — Tabela de extrato bancário

**Before:**
```
Extraia os dados.
```
Output esperado: dump bagunçado, talvez perdendo coluna de saldo.

**After:**
```
Reading instruction: Extrativa.
Focus: Todas as transações listadas, com data (DD/MM/YYYY), descrição,
       valor (negativo se débito), saldo após transação.
Ignore: Cabeçalho do banco, rodapé com termos legais, marca d'água.
Output: JSON array. Schema: [{data, descricao, valor, saldo}]. Use null se
        ilegível. Não invente valores.
```
Output esperado: JSON estruturado, auditável.

## Princípios

- **Modelo default = leitura descritiva.** Tudo o que não for descrição precisa ser pedido explícito.
- **Não confunda "ignore X" com "não veja X".** Ignore desloca atenção, não cega. Pra cegar, corte a imagem.
- **Output é parte do tipo de leitura.** Pedir JSON força leitura extrativa; pedir prosa força narrativa.
- **Pra leitura comparativa, mande as duas imagens com rótulo claro.** "A é a primeira, B é a segunda" elimina ambiguidade.
- **Combine com structured output quando tipo for extrativo ou avaliativo.** Ver [[03-Dominios/Tecnologia/IA/Structured Outputs/04 - OpenAI Structured Outputs — strict mode]] ou equivalente do seu provider.

## Anti-padrões

- **"Analise" como única instrução.** "Analise esta imagem" é tão vago quanto "descreva" — o modelo precisa saber **analisar pra quê**.
- **Misturar dois tipos no mesmo prompt.** "Descreva e extraia e compare e diagnostique" gera uma sopa. Divida em duas chamadas se precisar dos dois outputs.
- **Esquecer o slot Output.** Sem indicar a forma final, o modelo improvisa — geralmente longas frases em prosa que sua aplicação não consegue parsear.
- **Focus + Ignore contraditórios.** "Foque no header. Ignore tudo no topo da imagem." O modelo escolhe um e o outro vira sorte.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #17. Tese central de "dirigir a leitura".
- **Anthropic** — *Vision* ([docs](https://docs.anthropic.com/en/docs/build-with-claude/vision)). Recomendação de instruções específicas.
- **OpenAI** — *Vision guide* ([docs](https://platform.openai.com/docs/guides/vision)). "Tell the model what to look for".

## Veja também

- [[02 - Imagens como input — screenshots, charts, mockups]] — onde aplicar isso primeiro
- [[03 - PDFs e documentos — extração e análise]] — leitura extrativa em PDF longo
- [[Prompt Engineering]] — princípios de prompt textual estendidos para multimodal
- [[03-Dominios/Tecnologia/IA/Structured Outputs/02 - JSON Schema como contrato]] — pra forçar o slot Output
- [[07 - Limites e armadilhas multimodais]] — onde até a leitura bem dirigida falha
