---
title: Faturando em dólar — nota fiscal e isenções
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
  - Nota fiscal de exportação de serviço
  - Isenção PIS COFINS exportação
progress: done
---

> [!abstract] TL;DR
> Prestar serviço fractional pra um cliente no exterior é juridicamente uma **exportação de serviço** — e isso dá direito a isenção de PIS/COFINS (normalmente ~3,65% somados) desde que dois requisitos sejam cumpridos: o cliente precisa ser residente ou domiciliado no exterior, e precisa haver **ingresso de divisas** (o pagamento precisa entrar como câmbio, mesmo que convertido pra real). O ISS também costuma não incidir quando o resultado do serviço é usufruído fora do Brasil. Mesmo com essas isenções, a nota fiscal de exportação continua obrigatória — emitir sem ela, ou emitir errado, tira o direito ao benefício e pode gerar cobrança retroativa.

## O problema de tratar a exportação como um detalhe burocrático

Um fractional fecha o primeiro contrato com um cliente nos EUA e recebe o pagamento via Wise. Sem saber que precisa emitir nota fiscal de exportação de serviço (não uma nota fiscal comum), ele simplesmente lança a receita na contabilidade como se fosse um cliente nacional qualquer. Meses depois, o contador identifica que PIS e COFINS foram recolhidos sem necessidade — cerca de 3,65% da receita que poderia ter sido isenta virou imposto pago à toa, porque a documentação de exportação nunca foi organizada corretamente desde o início.

## Como funciona o mecanismo da isenção

> [!question]- O que exatamente precisa acontecer pra a isenção valer?
> Dois requisitos, ambos precisam estar presentes: **(1)** o serviço precisa ser prestado a pessoa física ou jurídica residente ou domiciliada no exterior, e **(2)** precisa haver **ingresso de divisas** — o pagamento precisa entrar no Brasil como operação cambial (em real ou moeda estrangeira), respeitando as regras do Banco Central. Esse ingresso pode acontecer antes, durante ou depois da prestação do serviço. Se a empresa optar por manter os recursos no exterior (permitido pela Lei 11.371/2006), a isenção ainda vale, mesmo sem entrada física do dinheiro no Brasil — o que importa é a operação cambial estar documentada corretamente, não necessariamente o dinheiro estar fisicamente aqui.

### PIS/COFINS: a isenção mais relevante

PIS e COFINS somados giram em torno de 3,65% sobre o faturamento pra empresas fora do regime de Fator R favorável — na exportação de serviço, com os dois requisitos cumpridos, essa incidência simplesmente não existe. Pra um fractional faturando consistentemente em dólar, isso representa economia real e recorrente, não um benefício pontual.

### ISS: depende de onde o resultado é usufruído

> [!question]- E o ISS, o imposto municipal sobre serviço — também some?
> Depende de onde o **resultado** do serviço é verificado, não de onde o trabalho foi fisicamente executado. Se um desenvolvedor no Brasil cria um sistema pra uso de uma empresa também no Brasil, há incidência de ISS mesmo que o pagamento venha de fora. Pra não haver incidência, o contratante precisa estar estabelecido fora do país **e** o resultado do serviço precisa ser usufruído no exterior — o caso típico de um fractional prestando serviço pra uma empresa americana, cujo produto/operação também está nos EUA, se enquadra nessa isenção.

### Documentação que sustenta a isenção

A isenção não é automática só por o cliente estar no exterior — ela precisa ser **documentada**, porque a Receita Federal pode questionar depois se a empresa não guardou as evidências:

- Comprovar que o contratante é de fato residente/domiciliado no exterior (contrato, CNPJ/EIN do cliente estrangeiro, endereço).
- Guardar comprovante da operação de câmbio (o extrato da conversão via Wise, Payoneer, banco PJ ou corretora — ver [[12 - Organização financeira e câmbio]]).
- Observar as regras do Banco Central aplicáveis à operação cambial (limites, forma de conversão, prazos).

Sem essa documentação organizada, a empresa fica exposta a questionamento — e pode acabar pagando retroativamente o imposto que deveria ter sido isento desde o início.

**Em uma frase:** exportar serviço fractional pra cliente estrangeiro dá isenção real de PIS/COFINS e frequentemente de ISS, mas só se a nota fiscal de exportação for emitida corretamente e a documentação de câmbio for guardada — a isenção existe no papel, mas só vale se o papel estiver certo.

## Casos práticos

### Cenário 1: exportação bem documentada desde o início

Um fractional CTO brasileiro, orientado pelo contador desde a abertura da empresa (ver [[10 - Abrindo e mantendo o CNPJ certo]]), emite nota fiscal de exportação de serviço pra cada fatura mensal do cliente americano, guarda o contrato assinado (provando residência do cliente no exterior) e o extrato de cada conversão cambial via conta PJ. No fechamento anual, a contabilidade aplica a isenção de PIS/COFINS sem questionamento, porque toda a documentação exigida já estava organizada mês a mês.

### Cenário 2: correção depois do erro

Um fractional que vinha tratando a receita internacional como receita nacional comum descobre o erro num diagnóstico contábil de rotina, quase um ano depois de começar. A correção exige reprocessar as notas fiscais já emitidas, calcular a diferença de PIS/COFINS pago indevidamente, e ajustar o enquadramento pros meses seguintes. O prejuízo não é só o imposto pago à toa — é também o tempo do contador reconstruindo o histórico que deveria ter sido registrado corretamente desde o mês 1.

## Armadilhas comuns

> [!warning] Emitir nota fiscal comum em vez de nota de exportação
> **O que acontece:** o sistema de emissão de nota fiscal do município não distingue automaticamente cliente nacional de estrangeiro, e a nota sai no formato padrão, sem sinalizar exportação de serviço. **Por quê:** sem o enquadramento correto na nota, a Receita Federal e a prefeitura não têm como identificar que aquela receita deveria ser isenta — o sistema simplesmente cobra como se fosse operação nacional. **Como evitar:** confirmar com o contador, antes da primeira fatura internacional, como o sistema de nota fiscal do seu município trata exportação de serviço — alguns exigem campo específico, outros exigem CNAE e natureza de operação particulares.

> [!warning] Não guardar comprovante de câmbio
> **O que acontece:** o pagamento chega via Wise ou Payoneer e o fractional só olha o saldo — sem baixar ou arquivar o comprovante formal da operação cambial. **Por quê:** sem esse comprovante, o requisito de "ingresso de divisas" fica sem prova documental caso a Receita questione a isenção depois. **Como evitar:** arquivar sistematicamente o comprovante de cada conversão cambial (mesmo que a plataforma de pagamento gere isso automaticamente, garantir que o contador tenha acesso ou cópia).

> [!warning] Assumir que toda receita em dólar é automaticamente isenta
> **O que acontece:** o fractional assume que, por receber em dólar, está automaticamente livre de PIS/COFINS/ISS, sem verificar se o resultado do serviço realmente é usufruído no exterior. **Por quê:** um cliente pode pagar em dólar mas ter operação e usufruto do resultado no Brasil (ex: uma empresa brasileira com conta em dólar no exterior) — nesse caso a isenção de ISS pode não se aplicar, mesmo com a moeda estrangeira. **Como evitar:** confirmar com o contador, caso a caso, se o cliente específico se enquadra nos dois requisitos (residência no exterior + resultado usufruído fora), em vez de assumir isenção automática pela moeda de pagamento.

## Como explicar em inglês

Providing fractional services to a foreign client counts as a service export under Brazilian law, which grants exemption from PIS/COFINS taxes (roughly 3.65% combined) as long as two conditions are met: the client is domiciled abroad, and the payment enters as a documented foreign exchange transaction. The exemption isn't automatic — it requires a properly issued export invoice and retained proof of the currency conversion.

| PT | EN |
|----|----|
| Exportação de serviço | Service export |
| Ingresso de divisas | Foreign exchange inflow |
| Nota fiscal de exportação | Export service invoice |
| Isenção fiscal | Tax exemption |
| Resultado usufruído no exterior | Result enjoyed/consumed abroad |

## Veja também

- [[Fator R — tributação para devs PJ]] — a isenção de PIS/COFINS reduz a carga, mas o Fator R ainda define a alíquota do DAS sobre o que sobra

## O que vem a seguir

Com a nota fiscal e as isenções entendidas, falta o lado prático do dinheiro em si: como converter, organizar e reservar o que chega em dólar de forma que sustente a operação e não vire surpresa na declaração anual de imposto de renda.

- [[12 - Organização financeira e câmbio]] — plataformas de câmbio, separação PF/PJ e reserva de imposto
- [[10 - Abrindo e mantendo o CNPJ certo]] — pré-requisito estrutural pra essa nota fiscal existir

## Fontes

- **Tributo Devido** — [Requisitos para isenção de PIS/COFINS na exportação de serviços](https://tributodevido.com.br/requisitos-isencao-pis-cofins-exportacao-servicos/) — os dois requisitos centrais (cliente no exterior + ingresso de divisas)
- **FecomercioSP** — [Entenda como funcionam as isenções de PIS/Pasep e Cofins na exportação de serviços](https://www.fecomercio.com.br/noticia/entenda-como-funcionam-as-isencoes-de-pis-pasep-e-cofins-na-exportacao-de-servicos) — regras de ingresso de divisas e manutenção de recursos no exterior (Lei 11.371/2006)
- **Meu Contador Online** — [Exportação de serviços](https://www.meucontadoronline.com.br/blog/exportacao-de-servicos/) — critério de local de usufruto do resultado para incidência de ISS
