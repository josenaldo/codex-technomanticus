---
title: "Roadmap — Identidade e acesso (IAM)"
created: 2026-07-20
updated: 2026-07-23
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Identidade e acesso (IAM) (galho 4)

Roadmap-folha do galho `Cloud/04 - Identidade e acesso (IAM)`. Bloco 1 (Modelo mental e fundamentos). Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - Por que identidade é o primeiro serviço
- **Estado:** ✅ feita · fase: Iniciado
- **Escopo:** ausência de perímetro de rede na nuvem, autenticação + autorização como os dois portões de toda chamada de API.

#### 02 - Usuários, grupos e o problema da credencial de longa duração
- **Estado:** ✅ feita · fase: Iniciado
- **Escopo:** IAM user/Team member, chave de acesso estática, MFA, o usuário raiz trancado.

#### 03 - Políticas — como uma permissão é avaliada
- **Estado:** ✅ feita · fase: Adepto
- **Escopo:** default nega, política de identidade vs de recurso, negação explícita é definitiva.

#### 04 - Roles e credenciais temporárias
- **Estado:** ✅ feita · fase: Adepto
- **Escopo:** trust policy, AWS STS, credencial de curta duração, tokens de API da DigitalOcean.

#### 05 - Least privilege na prática
- **Estado:** ✅ feita · fase: Magus
- **Escopo:** apertar permissão com dados de uso real, permissivo-depois-observa-depois-aperta, guarda-corpos organizacionais.

#### 06 - Identidade entre contas e federação
- **Estado:** ✅ feita · fase: Magus · **FECHA o galho**
- **Escopo:** assumir papel entre contas, SSO/OIDC corporativo, identidade de carga de trabalho para CI/CD, fecha o arco aberto na nota 02.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura de enriquecimento.
