---
title: Abrindo e mantendo o CNPJ certo
created: 2026-07-08
updated: 2026-07-08
type: concept
status: seedling
publish: true
tags:
  - fractional
  - empreendedorismo
  - carreira
  - tributacao
aliases:
  - CNPJ para fractional
  - MEI ou ME para dev
progress: done
---

> [!abstract] TL;DR
> Desenvolvimento de software sob encomenda (CNAE 6201-5/01) não está na lista de atividades permitidas para MEI — na prática, quase todo fractional engineer brasileiro precisa abrir uma Microempresa (ME) ou Sociedade Limitada Unipessoal (SLU) tributada pelo Simples Nacional desde o início, não MEI. O teto do MEI (R$ 81.000/ano) também seria baixo demais pra quem fatura em dólar como fractional. A ME/SLU no Simples Nacional permite faturar até R$ 4,8 milhões/ano e, com o CNAE certo, se qualifica pro Fator R (Anexo III) — o mecanismo que reduz a alíquota efetiva de forma significativa. Abrir a empresa certa desde o início evita duas dores: regularização retroativa cara e perda de tempo reabrindo CNPJ depois.

## O problema de começar pelo caminho errado

Um desenvolvedor decide virar fractional e, seguindo o conselho mais comum que circula ("comece pelo MEI, é mais simples"), abre um MEI para prestar serviço de desenvolvimento de software. Meses depois, ao tentar emitir nota fiscal de exportação de serviço pra um cliente americano, descobre que o CNAE de desenvolvimento sob encomenda não está entre as atividades permitidas pro MEI — a nota simplesmente não pode ser emitida daquela forma, ou foi emitida de forma irregular. Regularizar isso depois do fato — trocar de regime, ajustar CNAE, lidar com possíveis notas já emitidas incorretamente — custa mais tempo e dinheiro do que teria custado abrir certo desde o início.

## Como funciona o mecanismo da escolha de regime

> [!question]- Por que o MEI, que parece a opção mais simples, não serve pra a maioria dos devs?
> Duas razões independentes eliminam o MEI pra quem presta serviço de desenvolvimento de software sob encomenda ou customização: **(1) o CNAE não está na lista de atividades permitidas** para MEI — a atividade de programação sob encomenda não se enquadra; **(2) mesmo se coubesse, o teto de faturamento é baixo demais** — R$ 81.000/ano (R$ 6.750/mês) é um valor que um único cliente fractional pagando retainer em dólar frequentemente ultrapassa sozinho. Ambas as razões, juntas, tornam o MEI inviável estruturalmente pra esse tipo de atuação — não é questão de preferência, é questão de enquadramento legal.

### As opções reais: ME/SLU no Simples Nacional

Pra desenvolvimento de software, os CNAEs relevantes são:

- **6201-5/01** — Desenvolvimento de programas de computador sob encomenda
- **6202-3/00** — Desenvolvimento e licenciamento de programas de computador customizáveis

O tipo societário mais comum pra quem atua sozinho é a **Sociedade Limitada Unipessoal (SLU)** — permite um único sócio, sem precisar de um segundo nome só pra existir no papel (como a antiga EIRELI exigia). A empresa se enquadra como **Microempresa (ME)** enquanto o faturamento anual ficar até R$ 360.000 (podendo crescer até R$ 4,8 milhões permanecendo no Simples Nacional, mudando de faixa).

| Regime | Faturamento máximo/ano | CNAE de dev permitido? | Adequado pra fractional? |
|--------|---------------------------|---------------------------|-----------------------------|
| **MEI** | R$ 81.000 | Não (via de regra) | Não — CNAE não permitido e teto baixo |
| **ME/SLU — Simples Nacional** | Até R$ 4,8 milhões | Sim | Sim — regime padrão pra devs PJ |
| **Lucro Presumido** | Acima de R$ 4,8 milhões (ou por escolha estratégica) | Sim | Raro nessa fase — só relevante em faturamento muito alto |

### O Fator R entra na conta desde a abertura

> [!question]- Por que isso importa já no momento de abrir a empresa, não só depois?
> Porque o CNAE escolhido determina se a empresa cai automaticamente no Anexo V (mais caro) do Simples Nacional ou se qualifica pra buscar o Anexo III via Fator R (mais barato) — e o Fator R depende de uma janela móvel de 12 meses de pró-labore acumulado. Quem já abre a empresa planejando o pró-labore certo desde o primeiro mês chega ao Anexo III mais rápido do que quem só percebe essa alavanca depois de já estar operando há um tempo. O mecanismo completo do Fator R — a fórmula, as faixas, e como dimensionar o pró-labore — está em [[Fator R — tributação para devs PJ]]; esta nota não repete esse cálculo, só situa onde ele entra na decisão de abertura.

### O processo de abertura, em linhas gerais

1. **Escolher o tipo societário** (SLU é o padrão pra sócio único) e o CNAE correto de desenvolvimento de software.
2. **Registro na Junta Comercial** do estado, gerando o CNPJ.
3. **Inscrição municipal** (necessária pra emitir nota fiscal de serviço — NFS-e).
4. **Opção pelo Simples Nacional**, feita junto à Receita Federal, geralmente no mesmo processo de abertura ou logo em seguida.
5. **Abertura de conta PJ** em banco ou fintech que aceite recebimento internacional (ver [[12 - Organização financeira e câmbio]]).

Na prática quase ninguém faz esse processo sozinho — um contador especializado em PJ de tecnologia conduz a abertura e já orienta CNAE, tipo societário e enquadramento tributário desde o primeiro passo.

**Em uma frase:** para desenvolvimento de software, o caminho padrão é abrir direto como ME/SLU no Simples Nacional com o CNAE de desenvolvimento sob encomenda — o MEI, apesar de mais simples no discurso popular, geralmente não é sequer uma opção legal disponível.

## Casos práticos

### Cenário 1: abertura planejada desde o início

Um engenheiro decidido a virar fractional consulta um contador antes de fechar o primeiro cliente. O contador recomenda SLU com CNAE 6201-5/01, orienta a definir o pró-labore inicial já mirando o Fator R (Anexo III), e a empresa nasce pronta pra emitir nota fiscal de exportação assim que o primeiro contrato internacional for assinado — sem retrabalho.

### Cenário 2: correção de rumo depois do erro

Um fractional que abriu MEI por conta própria, sem orientação contábil, descobre o problema de enquadramento ao tentar emitir a primeira nota fiscal de exportação. Ele precisa desenquadrar o MEI, abrir uma nova empresa (SLU) com o CNAE correto, e perde algumas semanas nesse processo — tempo em que o primeiro cliente já esperava a nota fiscal pra liberar o pagamento. O caso ilustra por que vale consultar um contador antes de abrir, não depois de travar num contrato real.

## Armadilhas comuns

> [!warning] Confiar em "todo mundo abre MEI primeiro" sem checar o CNAE
> **O que acontece:** o profissional segue o conselho genérico mais popular (abrir MEI por ser "mais simples e barato") sem verificar se a atividade específica de desenvolvimento de software está na lista permitida. **Por quê:** o conselho de MEI é correto pra muitas atividades, mas desenvolvimento sob encomenda historicamente não está entre elas — informação que muda por atividade, não é regra geral. **Como evitar:** verificar o CNAE específico da atividade (ou consultar um contador) antes de abrir qualquer CNPJ, em vez de seguir recomendação genérica de terceiros.

> [!warning] Escolher CNAE genérico demais
> **O que acontece:** a empresa é aberta com um CNAE de "consultoria em TI" genérico, sem refletir com precisão que o serviço prestado é desenvolvimento de software. **Por quê:** CNAE incorreto pode gerar problema na emissão de nota fiscal de exportação (que exige alinhamento entre atividade declarada e serviço prestado) e complicar o enquadramento no Fator R. **Como evitar:** usar os CNAEs específicos de desenvolvimento (6201-5/01 ou 6202-3/00) em vez de CNAEs de consultoria genérica, mesmo que pareçam mais flexíveis à primeira vista.

> [!warning] Abrir empresa sem projetar o pró-labore desde o início
> **O que acontece:** a empresa é aberta sem plano de pró-labore, e só meses depois o profissional descobre o Fator R e percebe que está pagando o Anexo V mais caro. **Por quê:** o Fator R é calculado numa janela móvel de 12 meses — quanto mais cedo o pró-labore correto começa, mais rápido a empresa cruza o gatilho dos 28% e migra pro Anexo III. **Como evitar:** definir o pró-labore já no primeiro mês de operação com o cálculo do Fator R em mente, em vez de tratar isso como ajuste posterior.

## Como explicar em inglês

Custom software development typically isn't an eligible activity for Brazil's simplified MEI structure — most Brazilian fractional engineers need to incorporate as a Sociedade Limitada Unipessoal (SLU), a single-member limited company, taxed under the Simples Nacional regime, from day one.

| PT | EN |
|----|----|
| CNPJ | Company tax ID (Brazil) |
| Sociedade Limitada Unipessoal (SLU) | Single-member limited liability company |
| Simples Nacional | Simplified national tax regime |
| CNAE | Economic activity classification code |
| Pró-labore | Owner's salary / director's compensation |

## O que vem a seguir

Com a empresa aberta e o CNAE correto, o próximo passo é entender como esse CNPJ emite nota fiscal pra um cliente no exterior e quais isenções fiscais específicas de exportação de serviço se aplicam.

- [[11 - Faturando em dólar — nota fiscal e isenções]] — nota fiscal de exportação e as isenções de PIS/COFINS
- [[Fator R — tributação para devs PJ]] — o cálculo completo de Fator R e Anexo III vs V

## Fontes

- **MeuContadorOnline** — [Desenvolvedor de Software Pode Ser MEI 2026? Entenda os Riscos](https://www.meucontadoronline.com.br/blog/desenvolvedor-de-software-pode-ser-mei/) — CNAE de desenvolvimento sob encomenda fora da lista permitida para MEI
- **Contmatic Simplifique** — [PJ para Desenvolvedor: Como Abrir sua Empresa 2026](https://simplifique.contmatic.com.br/blogs/pj-para-desenvolvedor-como-abrir-gerir-empresa-2026) — processo de abertura de ME/SLU para devs
- **Contabilizei** — [Limite MEI 2026: Teto de faturamento](https://www.contabilizei.com.br/contabilidade-online/faturamento-mei-2026/) — teto de faturamento MEI (R$ 81.000/ano) e regras de desenquadramento
