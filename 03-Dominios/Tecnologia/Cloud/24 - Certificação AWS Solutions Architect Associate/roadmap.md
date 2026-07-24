---
title: "Roadmap — Certificação AWS Solutions Architect Associate"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Certificação AWS Solutions Architect Associate (galho 24)

Roadmap-folha do galho `Cloud/24 - Certificação AWS Solutions Architect Associate`. Bloco 5 (Provedores e maestria) — **último galho do bloco e da trilha**. Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 6 |
| ⬜ pendente | 0 |
| ✅ feita | 6 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |
| M1 (mídia) | pendente — enriquecimento futuro |

---

## Notas

#### 01 - O exame e seu valor
- **Estado:** ✅ feita · fase: Iniciado · 171 linhas
- **Escopo:** se a certificação vale a pena (a economia da sinalização), custo-benefício em números honestos, o formato do exame (65 questões, 130 min, passing score, custo, validade de 3 anos), o equivalente nas outras nuvens (qual escolher), os quatro domínios em peso (prévia), onde o SAA se encaixa na escada de certificações AWS, quem deve fazer e quando.

#### 02 - Os quatro domínios do blueprint
- **Estado:** ✅ feita · fase: Adepto · 185 linhas
- **Escopo:** um blueprint sem rótulo nos itens, os quatro domínios oficiais do SAA-C03 (Design Secure Architectures ~30%, Design Resilient Architectures ~26%, Design High-Performing Architectures ~24%, Design Cost-Optimized Architectures ~20%), a sobreposição quase perfeita entre os quatro domínios e os seis pilares do Well-Architected, tabela de onde a trilha já cobriu cada domínio.

#### 03 - Mapa da trilha ao blueprint
- **Estado:** ✅ feita · fase: Adepto · 190 linhas
- **Escopo:** o medo do guia de exame, por que a trilha já mapeia o blueprint, tabela galho → domínio → cobertura, seguindo o dinheiro no domínio Secure (30%), o domínio Cost-Optimized (20%) e o galho que já resolve quase tudo, as lacunas em detalhe (o que cada uma realmente pede), como usar o mapa pra montar a revisão, armadilhas ao usar este mapa.

#### 04 - Serviços que o exame ama e as pegadinhas
- **Estado:** ✅ feita · fase: Adepto · 256 linhas
- **Escopo:** 65 questões/infinitos disfarces, por que esses serviços e não outros, tabela serviço → por que o exame ama → pegadinha típica, o roteiro por trás das fantasias, as quatro pegadinhas-mãe (Multi-AZ vs Read Replica; Security Group stateful vs NACL stateless; "resposta mais barata que atende o requisito" vs superdimensionar; "gerenciado" quase sempre vence "você operando"), como ler uma questão de cenário com exemplo trabalhado, mais pares confusos (ALB vs NLB vs GWLB; EBS vs EFS vs S3 — a régua de granularidade e o vocabulário de frequência de acesso), domínio por trás da pegadinha de volta à trilha, a lente DigitalOcean (desacoplamento e custo), Azure/GCP como referência não-hands-on, onde cada pegadinha pesa mais no blueprint.

#### 05 - Estratégia de prova
- **Estado:** ✅ feita · fase: Adepto · 180 linhas
- **Escopo:** você sabe a matéria e ainda assim trava, o relógio como adversário mais previsível, a técnica das duas descartáveis e as duas na dúvida, aplicando a técnica numa questão típica, onde o requisito-chave se esconde no enunciado, conte antes de marcar, simulados como termômetro (não decoreba), online-proctored vs. centro de testes, o pânico como o verdadeiro adversário, tabela de táticas por situação, honestidade sobre o que garante (e não garante) aprovação.

#### 06 - Capstone — plano de estudo para o SAA-C03
- **Estado:** ✅ feita · fase: Magus · 159 linhas · **FECHA o galho**
- **Escopo:** recapitulando o galho em quatro frases, o problema que este capstone resolve, cronograma de 4 a 6 semanas ancorado na trilha (semana 1 Well-Architected + domínio Secure 30%; semana 2 Resilient 26% + High-Performing 24%; semana 3 Cost-Optimized 20% + serverless + lacunas restantes; semana 4 simulados e revisão de erros por domínio; semanas 5-6 condicionais até 85% e agendamento), tabela-cronograma consolidada, recursos além da própria trilha, critério objetivo de "estou pronto", fechando o galho 24 e o que vem depois no domínio inteiro. Capstone.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Galho fecha o Bloco 5 (Provedores e maestria) e a trilha Cloud como um todo — última entrada da árvore de 24 galhos.
- Todas as 6 notas escritas em 2026-07-24, fase seedling no frontmatter individual das notas (não confundir com o estado ✅ feita deste roadmap, que reflete a existência e completude do texto, não o ciclo de enriquecimento).
- Fronteira dupla clara: conteúdo técnico de serviço vive nos galhos correspondentes (especialmente 21 - AWS a fundo e 03 - Well-Architected Framework, cujos pilares mapeiam quase 1:1 aos quatro domínios do exame); este galho mapeia, prioriza e ensina a fazer a prova sobre esse conteúdo, sem reexplicá-lo.
- MOC (`index.md`) e este roadmap gerados após a escrita das 6 notas, seguindo o espelho estrutural do galho 11 (Serverless e FaaS).
