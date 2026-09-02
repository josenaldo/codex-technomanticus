---
title: "Secrets e configuração em produção"
created: 2026-07-08
updated: 2026-07-08
type: concept
status: seedling
fase: adepto
tags:
  - operacao
  - devops
  - secrets
  - seguranca
  - configuracao
publish: true
---

# Secrets e configuração em produção

> [!abstract] TL;DR
> **Config não é secret.** Uma URL de banco, um feature flag, o timeout de um cliente HTTP — tudo isso é config: varia por ambiente, mas pode aparecer num log ou numa tela de debug sem incendiar nada (12-Factor, fator III — ver [[02 - O contrato de uma app operável (12-Factor)]]). Um **secret** — senha, chave de API, certificado privado, token de acesso — é um subconjunto de config com uma propriedade extra: **se vazar, alguém pode se passar pelo seu sistema**. Essa diferença muda tudo: onde guardar (secret manager centralizado, não `.env` solto), como entregar (**injetado em runtime**, nunca embutido na imagem ou no git), e o que fazer quando falha (**rotacionar**, não só remover). O histórico do git é permanente — um commit revertido ainda existe em `git log`, e bots varrem repositórios públicos em minutos à procura exatamente disso. Esta nota cobre o ciclo de vida completo de um secret em produção: por que ele nunca deveria tocar o controle de versão em claro, onde ele vive (env vars vs. secret managers vs. K8s Secrets), como entra no processo em runtime, por que rotação é a rede de segurança que limita o dano de um vazamento, e como o dilema do GitOps — "o git é a fonte da verdade, mas não pode ter segredo em claro" — se resolve na prática.

São 2h14 da manhã de uma terça-feira quando um scanner automatizado, rodando em algum lugar do mundo, encontra um commit novo num repositório público no GitHub. O commit tem duas semanas — um desenvolvedor júnior, testando uma integração local, colou uma access key da AWS direto no código, `git add .`, `git commit`, `git push`, e só depois percebeu o erro. Ele reverteu o commit na hora, dez minutos depois. Achou que resolveu.

Não resolveu. O commit com a chave ainda existe — não no branch principal, mas no histórico do git, acessível por qualquer pessoa que rode `git log --all` ou simplesmente clone o repositório e olhe os commits antigos. Reverter tira o arquivo da versão atual; **não apaga o passado**. E o passado, num repositório git, é público para sempre a menos que alguém reescreva o histórico inteiro e force-push — algo que a maioria dos times nunca faz, porque é destrutivo e quebra clones de outras pessoas.

O scanner que encontrou a chave não é sofisticado. É um bot que monitora o feed de eventos públicos do GitHub — todo push para todo repositório público gera um evento — e passa cada diff por uma lista de expressões regulares que reconhecem o formato de chaves da AWS, tokens do Stripe, credenciais do Twilio, chaves privadas SSH, e centenas de outros padrões. O relatório *State of Secrets Sprawl 2026* da GitGuardian mediu **29 milhões de novos segredos hardcoded** adicionados a repositórios públicos do GitHub só em 2025 — um salto de 34% sobre o ano anterior, o maior já registrado, com vazamento de credenciais de serviços de IA subindo 81%. Esses bots não são hipotéticos: em maio de 2026, uma única campanha automatizada empurrou 5.718 commits maliciosos para 5.561 repositórios numa janela de seis horas, cada um injetando um workflow do GitHub Actions desenhado para exfiltrar segredos de CI, credenciais de nuvem e chaves SSH para um servidor de comando e controle.

Às 2h20, seis minutos depois do push, a chave já está em uso — não pelo desenvolvedor, por alguém do outro lado do mundo, provisionando instâncias EC2 de mineração de criptomoeda na conta da empresa. Pela manhã, a fatura da AWS mostra um crescimento de milhares de dólares em seis horas.

Esse cenário não é um exagero didático. É o padrão documentado, repetido, do que acontece quando um segredo entra no controle de versão. E é exatamente por isso que esta nota separa, desde a primeira linha, duas categorias que o vocabulário do dia a dia mistura: **config** e **secret**.

## Config e secret não são a mesma coisa

O [[02 - O contrato de uma app operável (12-Factor)|fator III do 12-Factor]] já estabeleceu o princípio geral: configuração fica fora do código, injetada pelo ambiente, variando por deploy (dev, staging, produção) sem exigir uma nova build. Essa nota trata do subconjunto de configuração que precisa de um tratamento categoricamente diferente.

| Propriedade | Config comum | Secret |
|---|---|---|
| Exemplo | URL do banco, timeout de HTTP, feature flag, nível de log | Senha do banco, chave de API, certificado TLS privado, token OAuth |
| Pode aparecer num log de debug? | Geralmente sim (ou é aceitável o risco) | **Nunca** — cada aparição é um vazamento |
| Pode ir pro histórico do git em claro? | Discutível, mas tolerável em muitos casos | **Nunca**, sob nenhuma circunstância |
| Consequência de exposição | Confusão, no pior caso um bug | Alguém se autentica como você — dados roubados, custo financeiro, movimento lateral |
| Quem pode ver | Times de dev, ops, geralmente amplo | Least privilege — só quem/o que precisa, auditado |
| O que fazer se vazar | Corrigir e seguir | **Rotacionar imediatamente** — a credencial antiga está morta a partir de agora |

A linha divisória não é sempre óbvia — uma URL de banco *parece* inofensiva até você notar que ela costuma incluir usuário e senha embutidos (`postgres://user:senha@host/db`), e nesse momento vira secret. A regra prática que a maioria dos times sênior usa: **se um valor, sozinho, permite autenticação ou personificação em algum sistema, ele é secret — trate-o como tal mesmo que "pareça" só uma configuração**.

> [!question]- Toda credencial é secret, mas todo secret é credencial?
> Não exatamente. Credenciais (senhas, tokens, chaves de API) são o caso mais comum de secret, mas a categoria é mais ampla: um certificado TLS privado não "autentica" no sentido de login, mas se vazar permite que um atacante se passe pelo seu servidor numa conexão TLS (man-in-the-middle). Uma chave de assinatura de JWT não é uma "senha" tradicional, mas quem a possui pode forjar tokens de autenticação válidos para qualquer usuário do sistema. O teste unificador é: **o valor, por si só, concede alguma forma de confiança ou identidade que um atacante pode explorar?** Se sim, é secret, independente do formato.

## O princípio central: nunca commitar segredo

Tudo que segue nesta nota é uma elaboração de uma regra única: **um segredo nunca deve existir em claro dentro de um repositório git**, nem no arquivo atual, nem em nenhum commit do histórico. A razão técnica é simples e já foi ilustrada na abertura: git é um sistema de controle de versão **aditivo por design** — cada commit é imutável e permanece acessível por hash mesmo depois de "removido" de um branch. Reverter, deletar o arquivo, ou até fazer squash de commits recentes não elimina cópias já clonadas, forks, ou o próprio objeto no repositório remoto até uma reescrita agressiva de histórico (`git filter-repo` ou similar, seguida de força bruta em todos os clones).

O **OWASP Secrets Management Cheat Sheet** organiza essa disciplina como o primeiro dos princípios gerais de gestão de segredos: segredos precisam ser gerados de forma segura, ter o mínimo de privilégio necessário para seu papel, e nunca devem ser armazenados sem criptografia em nenhum meio persistente que não seja um cofre desenhado para isso — o que exclui explicitamente arquivos de configuração versionados.

Na prática, a indústria constrói três camadas de defesa contra esse erro:

**1. Prevenção — nunca deixar o commit acontecer.** O GitHub oferece **push protection**: antes de um push completar, o servidor escaneia o diff contra mais de 200 padrões conhecidos de secret (chaves AWS, tokens Stripe, certificados privados, e dezenas de outros formatos reconhecíveis) e **bloqueia o push** se encontrar uma correspondência. Ferramentas como **GitGuardian** (via `ggshield`, rodando como pre-commit hook local) fazem o mesmo antes mesmo de o código sair da máquina do desenvolvedor. Essa é a defesa mais barata: pegar o erro antes que ele saia do laptop.

**2. Detecção — assumir que algo vai passar.** Mesmo com push protection, secrets escapam — em repositórios privados sem a proteção habilitada, em formatos de credencial não reconhecidos pelos padrões, ou simplesmente porque alguém desabilitou o scanner "temporariamente" e esqueceu de reativar. Ferramentas de secret scanning contínuo (GitHub Advanced Security, GitGuardian, TruffleHog) vasculham o histórico completo do repositório, não só o commit mais recente, procurando o que já entrou.

**3. Resposta — rotacionar, não só remover.** Este é o ponto que mais gente erra na prática, e vale grifar: **remover o segredo do código não neutraliza o vazamento**. A credencial continua válida até que alguém a invalide ativamente no sistema que a emitiu — trocar a senha, revogar a chave de API, reemitir o certificado. A documentação de remediação do GitHub é explícita sobre isso: qualquer segredo vazado deve ser considerado **imediatamente comprometido**, e o passo essencial é revogá-lo/rotacioná-lo no provedor de origem — remover do git é limpeza, não remediação.

```mermaid
sequenceDiagram
    participant Dev as Desenvolvedor
    participant Git as Push protection
    participant Repo as Repositório
    participant Scan as Scanner contínuo
    participant Vault as Secret manager

    Dev->>Git: git push (contém API key)
    alt Push protection ativa
        Git-->>Dev: ❌ bloqueado — secret detectado
        Dev->>Dev: remove do commit, usa secret manager
    else Push protection ausente/burlada
        Git->>Repo: push aceito
        Repo->>Scan: varredura contínua do histórico
        Scan-->>Dev: 🚨 alerta — secret no histórico
        Dev->>Vault: revoga/rotaciona a credencial AGORA
        Note over Dev,Vault: remover do git não é suficiente —<br/>o histórico antigo continua exposto
    end
```

> [!warning] "Já removi do commit, tá resolvido"
> **O que acontece:** um secret vaza, alguém percebe rápido, faz um `git revert` ou até reescreve o histórico com `filter-repo`, e o time considera o incidente encerrado. **Por quê:** a credencial em si não mudou. Se o commit ficou público por qualquer janela de tempo — mesmo minutos — bots já podem tê-lo indexado, e reescrever o histórico não afeta forks, clones locais ou cópias em cache de serviços de terceiros que já leram o conteúdo. **Como evitar:** trate remoção do git e rotação da credencial como **dois passos obrigatórios e independentes**. A ordem correta é: rotacionar primeiro (mata o vazamento na origem), limpar o git depois (higiene, não segurança).

## Onde secrets vivem: do mais simples ao mais seguro

Depois de aceitar que secret não pode estar em claro em lugar nenhum versionado, a pergunta seguinte é onde ele deve viver de fato. Existem três camadas, com trade-offs bem diferentes.

### Variáveis de ambiente: simples, mas vazam mais do que parece

A prática mais comum — e o próprio texto original do 12-Factor recomendava — é passar secrets como variáveis de ambiente para o processo. É simples, funciona em qualquer runtime, e não exige infraestrutura adicional. Mas variáveis de ambiente têm um problema estrutural que ficou mais claro à medida que a observabilidade amadureceu: **elas são um namespace global e plano dentro do processo**. Qualquer código rodando no mesmo processo — sua lógica de negócio, mas também qualquer dependência de terceiros, SDK de telemetria, ou biblioteca de logging — tem acesso de leitura irrestrito a todas as variáveis de ambiente, não só às que ele precisa.

Na prática, isso gera vazamentos silenciosos e recorrentes:

- **Crash dumps e SDKs de observabilidade.** Muitas ferramentas de monitoramento de erro (Sentry, Datadog e similares) capturam o estado do processo — incluindo variáveis de ambiente — no momento de uma exceção não tratada, para ajudar no diagnóstico. Isso significa que uma credencial de banco pode acabar indexada em texto plano dentro do seu próprio sistema de observabilidade.
- **Introspecção do processo.** Em Linux, o conteúdo de `/proc/<pid>/environ` é legível por qualquer processo com permissão suficiente na mesma máquina — incluindo, em ambientes multi-tenant mal isolados, processos de outros times ou até um container vizinho comprometido.
- **Herança por processos filhos.** Variáveis de ambiente são herdadas automaticamente por qualquer subprocesso que a aplicação disparar (um script auxiliar, uma chamada de shell), ampliando a superfície de quem tem acesso sem que ninguém tenha decidido isso explicitamente.
- **Logging acidental.** É comum alguém adicionar um `console.log(process.env)` para debugar um problema de configuração em produção — e esquecer de remover, ou o log ficar retido por semanas num agregador central.

Isso não significa "nunca use variáveis de ambiente" — é o mecanismo de *entrega* mais universal que existe, e a maioria dos secret managers entrega o valor final justamente como variável de ambiente no momento em que o processo sobe. O ponto é: **variáveis de ambiente não são um sistema de gestão de segredo, são só o canal de transporte final**. A fonte da verdade — onde o valor é gerado, versionado, auditado e revogado — precisa ser outra coisa.

### Secret managers: centralizados, auditáveis, com controle de acesso

Um **secret manager** — HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault — resolve o problema de origem: em vez de o segredo existir espalhado em `.env` files, pipelines de CI e manifests, ele existe **em um único lugar**, com controle de acesso granular (quem/o que pode ler qual segredo), trilha de auditoria (quem leu o quê e quando), e — no caso do Vault — a capacidade de gerar **secrets dinâmicos**: credenciais criadas sob demanda, com TTL embutido, que expiram e são revogadas automaticamente sem intervenção manual.

A documentação do Vault descreve a diferença entre secret estático e dinâmico como uma escolha estrutural: um secret estático (uma senha fixa configurada uma vez) exige rotação manual ou agendada — por padrão o Vault pode rotacionar credenciais de banco a cada 24 horas, com granularidade mínima de 5 segundos, ou seguir um cron custom. Um secret dinâmico é gerado *no momento em que a aplicação pede*, com TTL curto, e simplesmente deixa de existir quando expira — não há "rotação" no sentido de trocar um valor por outro, porque o valor nunca teve vida longa o suficiente para precisar disso.

```mermaid
graph LR
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    classDef falha fill:#FF6B6B24,stroke:#FF6B6B,color:#E9ECF2
    A["Secret manager<br/>(Vault / AWS Secrets Manager)"] -->|"1. autentica<br/>(IAM role / K8s SA)"| B["Container sobe"]
    B -->|"2. pede o secret<br/>em runtime"| A
    A -->|"3. injeta como<br/>env var ou arquivo montado"| C["Processo da aplicação<br/>já rodando"]
    D["Imagem de container"] -.->|"❌ NUNCA contém<br/>o secret"| C
    E["Repositório git"] -.->|"❌ NUNCA contém<br/>o secret em claro"| A
    class D destaque
    class E falha
```

O ponto central desse diagrama — e o requisito explícito desta nota — é que **o segredo entra no processo em runtime, nunca antes**. A imagem de container é um artefato imutável que pode circular por registries, ser copiada, arquivada, inspecionada por qualquer pessoa com acesso ao registry; se um secret estivesse embutido nela via `ARG`/`ENV` no build, ele estaria permanentemente gravado nas layers da imagem — visível até com um simples `docker history` ou extraindo o filesystem da layer. A injeção em runtime — via variável de ambiente populada pelo orquestrador, um arquivo montado por um sidecar/CSI driver, ou uma chamada direta da aplicação ao secret manager na inicialização — garante que o segredo só existe na memória do processo em execução, nunca em um artefato persistido.

> [!warning] Secret embutido em ARG/ENV do Dockerfile
> **O que acontece:** um time passa uma credencial de build (token de um registry privado, chave de API de terceiro) via `ARG` ou `ENV` no Dockerfile, para o processo de build conseguir baixar uma dependência. **Por quê:** mesmo que o `ARG` não apareça na imagem final "visualmente", ele fica gravado permanentemente numa layer intermediária do build, recuperável por qualquer pessoa com acesso à imagem (`docker history --no-trunc` ou extraindo as layers). `ENV` é ainda pior — persiste explicitamente até no `docker inspect` da imagem final. **Como evitar:** para credenciais de build, use **BuildKit secrets** (`--secret` do Docker BuildKit, montado só durante o `RUN` específico e nunca persistido em layer) ou builds multi-stage onde o estágio final não herda a credencial. Para credenciais de runtime, a regra desta nota vale sem exceção: injeção via orquestrador, nunca via imagem.

### Kubernetes Secrets: melhor que ConfigMap, mas não é criptografia por si só

Dentro de um cluster Kubernetes, o objeto nativo `Secret` existe justamente para separar dados sensíveis de `ConfigMap` (que guarda config comum). A documentação oficial do Kubernetes é direta sobre uma confusão frequente: **os valores de um Secret são armazenados como base64, e base64 não é criptografia** — é apenas uma codificação reversível, sem chave, sem segredo nenhum envolvido. Qualquer pessoa com o valor em mãos faz `base64 -d` e lê o conteúdo original instantaneamente.

Por padrão, sem configuração adicional, um Kubernetes Secret é guardado **sem criptografia** dentro do etcd (o banco de dados que armazena todo o estado do cluster) — só codificado em base64. Isso significa que qualquer pessoa com acesso de leitura ao etcd, ou um snapshot de backup do etcd, tem acesso trivial a todos os secrets do cluster. A própria documentação do Kubernetes, no guia de boas práticas, recomenda três camadas para fechar esse gap:

1. **Encryption at rest** — habilitar uma `EncryptionConfiguration` no `kube-apiserver` para que os Secrets sejam criptografados antes de ir para o etcd, tipicamente usando um provider KMS que delega a chave de criptografia a um serviço externo (AWS KMS, GCP KMS, Vault) via envelope encryption — o mesmo padrão de duas camadas (chave mestra + chave de dados) usado pelos secret managers de nuvem.
2. **RBAC restritivo** — Secrets do Kubernetes são objetos da API como qualquer outro; sem RBAC bem configurado, qualquer ServiceAccount ou usuário com permissão de `get`/`list` em Secrets no namespace enxerga tudo, não só o que o Pod específico precisa.
3. **Least privilege por Pod** — montar só o Secret que aquele Pod específico precisa, nunca dar acesso amplo a todos os Secrets do namespace.

> [!question]- Então K8s Secrets nativos são inseguros e eu deveria evitar?
> Não é bem "inseguro", é "insuficiente sozinho". K8s Secrets resolvem um problema real — não deixar credencial solta num ConfigMap em texto claro, e oferecem uma abstração nativa que RBAC, montagem em volume e integração com service accounts já entendem. O problema é confiar que a existência do objeto `Secret` já é suficiente proteção. Times maduros usam K8s Secrets como a **interface final** (é isso que o Pod monta), mas preenchem esse objeto a partir de uma fonte externa e mais forte — é exatamente o papel do **External Secrets Operator**, discutido na seção de GitOps abaixo — e habilitam encryption at rest por cima. Pense em K8s Secret nativo como "melhor que ConfigMap, ainda não é cofre".

## Injeção em runtime: o padrão que atravessa todas as opções

Independente de a fonte ser Vault, AWS Secrets Manager, ou um K8s Secret nativo, o princípio operacional é sempre o mesmo, e vale repetir porque é o requisito de segurança mais frequentemente ignorado por pressa: **o container sobe sem o segredo, se autentica no secret manager usando uma identidade que ele já tem (IAM role, Kubernetes ServiceAccount com federação OIDC), pede o segredo, e só então o recebe** — como variável de ambiente populada pelo orquestrador, arquivo montado num volume `tmpfs` (que nunca toca disco persistente), ou via chamada direta de uma biblioteca cliente do secret manager na inicialização da aplicação.

Esse desenho resolve dois problemas de uma vez: primeiro, a imagem de container — que pode ser escaneada, arquivada, copiada para múltiplos ambientes — nunca contém material sensível, então vazamento de imagem não é vazamento de credencial. Segundo, a autenticação no secret manager em si não depende de outro segredo estático espalhado (a "credencial para pegar a credencial") — ambientes modernos usam identidade federada: um Pod no EKS assume uma IAM role via **IRSA** (IAM Roles for Service Accounts) sem nenhuma chave de acesso armazenada em lugar nenhum; a prova de identidade vem do próprio orquestrador, via token OIDC de curta duração.

O OWASP Cheat Sheet chama esse padrão de **passwordless authentication**: em vez de o processo carregar uma senha para se autenticar no cofre, ele prova sua identidade através de um mecanismo já confiável (a plataforma de nuvem, o próprio cluster Kubernetes), e o cofre confia nessa identidade para liberar o segredo real. Isso elimina a pergunta recursiva incômoda — "e onde guardo o segredo que dá acesso ao cofre de segredos?" — porque não existe mais esse segredo intermediário.

## Rotação: o limite de dano de um vazamento que já aconteceu

Toda a disciplina de "nunca commitar" trata de prevenção. Mas segredos vazam de outras formas além do git — um funcionário sai da empresa e a credencial compartilhada não é trocada, um log de terceiro captura um header de autenticação, uma dependência com vulnerabilidade exfiltra variáveis de ambiente. **Rotação** é a resposta estrutural a "e se um vazamento que eu nem sei que aconteceu já ocorreu?"

A lógica é simples de enunciar: se toda credencial tem uma vida útil curta e é trocada regularmente, uma credencial vazada e não detectada tem uma **janela de exploração limitada** — no pior caso, o tempo até a próxima rotação agendada, em vez de "para sempre, até alguém perceber manualmente". É o mesmo raciocínio por trás de certificados TLS de curta duração (Let's Encrypt renovando a cada 90 dias) aplicado a qualquer credencial.

Existem dois níveis de maturidade em rotação:

**Rotação agendada de secrets estáticos.** O secret manager troca a credencial periodicamente (diariamente, semanalmente) mesmo sem nenhum evento de vazamento conhecido — pura higiene preventiva. Exige que a aplicação seja capaz de buscar a versão mais recente sem reiniciar (ou tolerar um reinício coordenado), e que o sistema autenticado (o banco de dados, o serviço externo) aceite a rotação sem downtime — geralmente com uma janela de sobreposição onde a credencial antiga e a nova são válidas simultaneamente por um curto período.

**Secrets dinâmicos, já descritos acima.** Em vez de rotacionar um valor fixo, o Vault gera uma credencial nova a cada solicitação (por exemplo, um usuário de banco de dados criado e revogado automaticamente a cada lease), com TTL curto. Não existe "a credencial" no singular — existe um fluxo contínuo de credenciais de vida curta, cada uma inútil fora da sua janela.

> [!warning] Rotacionar sem plano de compatibilidade quebra produção
> **O que acontece:** um time habilita rotação automática de uma credencial de banco sem avisar a aplicação, e no momento da troca todas as conexões ativas começam a falhar simultaneamente porque a aplicação tinha a credencial antiga em cache de conexão e não sabe buscar a nova. **Por quê:** rotação tratada como "trocar um valor" sem considerar o ciclo de vida da conexão — pools de conexão de banco, tokens já emitidos, sessões ativas — vira uma auto-negação de serviço. **Como evitar:** rotação segura em produção sempre tem uma **janela de sobreposição** (credencial antiga e nova válidas ao mesmo tempo por alguns minutos/horas) e a aplicação precisa saber recarregar a credencial sem reiniciar (watch no arquivo montado, callback do SDK do secret manager) ou tolerar um restart coordenado fora de horário de pico. Testar rotação em staging antes de habilitar em produção não é opcional.

## O dilema do GitOps: fonte da verdade sem segredo em claro

O [[05 - GitOps e Infrastructure as Code|GitOps]] estabelece o git como fonte única da verdade para o estado desejado do sistema — tudo declarativo, tudo versionado, tudo auditável por `git log`. Isso cria uma tensão direta com tudo que esta nota defendeu até aqui: se manifests de Kubernetes vivem no git, e um Pod precisa de um Secret para subir, como esse Secret entra no manifest **sem** violar a regra de nunca commitar segredo em claro?

A indústria convergiu para duas famílias de solução, com filosofias opostas:

**Criptografar o segredo e commitar a versão criptografada.** Ferramentas como **Sealed Secrets** (Bitnami) e **SOPS** (originalmente da Mozilla, hoje projeto sandbox da CNCF) permitem que o valor sensível vá para o git — mas cifrado, não em claro. O Sealed Secrets roda um controller no cluster com uma chave privada gerada na instalação; você cifra um Secret comum usando a chave pública correspondente (`kubeseal`), obtém um `SealedSecret` (só decifrável por aquele cluster específico), e **esse objeto cifrado é seguro para commitar** — sem a chave privada do controller, o conteúdo é ilegível. SOPS segue uma lógica parecida mas em nível de arquivo: cifra os *valores* de um YAML/JSON mantendo as *chaves* legíveis (então o diff no git continua útil para review), usando envelope encryption com AWS KMS, GCP KMS, Azure Key Vault, PGP ou `age` como a chave mestra.

**Manter só uma referência no git; o valor real nunca sai do secret manager.** O **External Secrets Operator (ESO)** inverte a abordagem: o git guarda um objeto `ExternalSecret` que aponta para um caminho num backend externo (Vault, AWS Secrets Manager, GCP Secret Manager) — nenhum material sensível, cifrado ou não, entra no repositório. Um controller no cluster lê periodicamente esse backend e materializa o `Secret` real do Kubernetes a partir dele, mantendo o valor sincronizado se o secret manager atualizar a credencial (o que também dá suporte nativo a rotação, gratuito).

| | Sealed Secrets / SOPS | External Secrets Operator |
|---|---|---|
| O que vai pro git | O segredo, cifrado | Só uma referência (nenhum material sensível) |
| Dependência externa em runtime | Nenhuma além do controller no cluster | Sim — precisa do backend (Vault/cloud) disponível |
| Atualização dinâmica se o valor mudar na fonte | Não — precisa recifrar e commitar de novo | Sim — sincroniza automaticamente |
| Setup | Simples | Exige configurar o backend e credenciais de acesso a ele |
| Melhor encaixe | Times pequenos, secrets relativamente estáticos, querem zero dependência externa | Times que já têm um secret manager centralizado e querem uma única fonte da verdade |

> [!question]- Por que não simplesmente não usar GitOps para nada que envolva secret?
> Porque a alternativa — aplicar Secrets manualmente fora do pipeline declarativo, com `kubectl apply` avulso — reintroduz exatamente o problema que o GitOps existe para resolver: drift não rastreado, nenhum histórico de quem mudou o quê e quando, e nenhuma forma de reconstruir o cluster do zero a partir do git sozinho. A resposta da indústria não foi "excluir secrets do GitOps", foi resolver o problema de forma que o git continue sendo a fonte da verdade *do estado desejado* (que ExternalSecret existe, que SealedSecret está associado a qual chave) sem ser a fonte da verdade *do valor sensível em si* — essa responsabilidade fica isolada no secret manager, que é o sistema desenhado para isso.

## Least privilege e auditoria: quem pode ler o quê

Centralizar segredos num secret manager resolve "onde ele mora", mas não resolve sozinho "quem pode ler". A segunda metade da disciplina — igualmente importante e frequentemente negligenciada — é controle de acesso granular:

- **Least privilege por identidade.** Cada aplicação, pipeline de CI, ou pessoa deveria ter acesso só aos segredos que efetivamente precisa, não a "todos os segredos do time" por conveniência. Um serviço de billing não precisa enxergar a credencial do serviço de notificações.
- **Least privilege por operação.** Nem todo consumidor de um segredo precisa poder *lê-lo* — em alguns desenhos (Vault com *response wrapping*, ou operações assinadas via KMS), o segredo nunca é exposto em texto plano nem para quem o usa; a operação (assinar, decifrar) acontece dentro do cofre, e só o resultado sai.
- **Auditoria de acesso.** Todo acesso a um segredo — quem, quando, de onde — deveria gerar um registro imutável. Isso não é burocracia: é a diferença entre "sabemos exatamente quais sistemas tocaram essa credencial antes de decidirmos se ela foi comprometida" e "não fazemos ideia, então vamos rotacionar tudo por precaução".
- **Segregação por ambiente.** Um secret de produção nunca deveria estar acessível — nem por engano — num ambiente de desenvolvimento. Isso parece óbvio, mas é um erro recorrente: um `.env.production` copiado "só para testar uma coisa rápida" localmente, ou um pipeline de CI mal configurado que injeta credenciais de prod num job de PR de um fork externo.

> [!warning] Vazar config de produção pelo ambiente de dev
> **O que acontece:** um desenvolvedor copia o arquivo de configuração de produção para rodar localmente "só dessa vez", ou um script de seed de dados aponta acidentalmente para o secret manager de produção em vez do de staging. **Por quê:** ambientes de desenvolvimento têm padrões de segurança mais frouxos por design — laptops sem disco criptografado, terminais compartilhados, extensões de IDE de terceiros com acesso amplo ao filesystem. Uma credencial de produção que transita por esse ambiente herda esse risco menor, mesmo que o valor em si seja idêntico ao de prod. **Como evitar:** segregação física de secret managers por ambiente (instância/namespace/vault separado para dev, staging, prod), nunca reaproveitar o mesmo caminho de segredo entre ambientes, e — quando um dev genuinamente precisa depurar um problema específico de produção — usar acesso temporário e auditado (um secret dinâmico de curtíssima duração), não copiar a credencial permanente.

## Um exemplo trabalhado: da chave hardcoded ao pipeline seguro

Vale amarrar a teoria numa progressão concreta — o mesmo serviço, evoluindo de "funciona, mas é uma bomba-relógio" para "seguro por desenho".

**Estágio 0 — o jeito errado, e o mais comum em protótipos.** Um serviço de processamento de pagamentos tem, direto no código, `stripeClient = Stripe("sk_live_51H...")`. Funciona perfeitamente em dev. É commitado sem ninguém perceber — passou pelo push protection porque o repositório é privado e a organização não tinha habilitado a proteção lá. Três meses depois, um contratante externo recebe acesso de leitura ao repo para uma auditoria de código, e sem querer expõe a chave num print de código compartilhado numa ferramenta de terceiros.

**Estágio 1 — variável de ambiente.** O time corrige o óbvio: a chave sai do código, vira `os.environ["STRIPE_KEY"]`, passada via `.env` local e como variável de ambiente no deploy. Melhor — o código nunca mais expõe a chave por si. Mas a chave ainda existe em texto plano no `.env` de cada desenvolvedor (frequentemente commitado por engano em algum ponto, apesar do `.gitignore`), e em texto plano nas variáveis de ambiente do container em produção, visível para qualquer SDK de observabilidade que capture o estado do processo.

**Estágio 2 — secret manager com injeção em runtime.** O time migra para AWS Secrets Manager. A chave do Stripe vive lá, com uma política de IAM que só permite ao role específico daquele serviço lê-la. O container sobe sem nenhuma chave; na inicialização, o processo assume o IAM role (via IRSA, sem credencial estática nenhuma), pede o segredo ao Secrets Manager, e o mantém só em memória. Nenhum artefato — imagem, manifest, log — jamais contém a chave.

**Estágio 3 — rotação e GitOps.** O time habilita rotação automática a cada 30 dias no Secrets Manager (o Stripe suporta múltiplas chaves ativas simultaneamente, então a rotação tem uma janela de sobreposição sem downtime). O manifest do Kubernetes, versionado via GitOps, contém apenas um `ExternalSecret` apontando para o caminho no Secrets Manager — nenhum valor sensível, cifrado ou não, jamais toca o git. Quando a chave rotaciona automaticamente na AWS, o External Secrets Operator detecta a mudança e atualiza o `Secret` do Kubernetes sem intervenção manual, e a aplicação recarrega a credencial sem reiniciar.

O salto do Estágio 0 ao Estágio 3 não é sobre adicionar ferramentas por adicionar — é sobre eliminar, uma a uma, cada superfície onde um humano ou um processo automatizado poderia acidentalmente expor o segredo: o código-fonte, o arquivo de config local, o processo em memória sem controle de acesso, e por fim a janela de tempo em que uma credencial comprometida continua válida.

## Em entrevista

Perguntas sobre gestão de segredos aparecem com frequência em entrevistas de nível sênior — tanto em rounds de system design ("como você gerenciaria credenciais desse sistema em produção?") quanto em rounds comportamentais/operacionais ("me conte sobre um incidente de segurança que você tratou").

O que um entrevistador sênior está de fato avaliando:

- Se você distingue **config de secret** de forma automática, sem precisar que alguém aponte a diferença — sinaliza maturidade de quem já operou sistemas reais, não só desenhou diagramas.
- Se sua resposta padrão para "um secret vazou" é **rotacionar primeiro**, não "remover do código" — essa é a resposta que separa quem já viveu um incidente de quem só leu sobre.
- Se você sabe articular **por que a imagem de container nunca deve conter o segredo** — testa entendimento de superfície de ataque, não decoreba de ferramenta.
- Se você reconhece o **trade-off entre Sealed Secrets/SOPS e External Secrets Operator** quando a pergunta é sobre GitOps — mostra que você entende o dilema arquitetural (fonte da verdade declarativa vs. segredo nunca em claro), não só o nome de uma ferramenta.

A resposta fraca cita "usamos Vault" como se o nome da ferramenta fosse a resposta. A resposta forte amarra a decisão ao princípio: "separamos config de secret desde o design; secrets nunca tocam o git, nem cifrados quando dá pra evitar, e a primeira ação em qualquer vazamento suspeito é rotacionar — investigar a causa vem depois, porque cada minuto com a credencial antiga viva é risco acumulando."

## How to explain in English

Secrets management vocabulary is used almost exclusively in English form even in PT-BR technical conversations — worth locking in early.

> "Config and secrets are not the same thing. Config can be visible — a database URL, a feature flag; a secret can't leak, because whoever holds it can impersonate your system. Secrets should never be committed to version control, even encrypted when avoidable, because git history is permanent — a revert doesn't erase a past commit. The fix for a leaked secret is rotation, not just removal from the codebase; removing it from git doesn't invalidate the credential that's already out there. In production, secrets get injected into the container at runtime — pulled from a secret manager like Vault or AWS Secrets Manager using the workload's own identity — and never baked into the image or the deployment manifest. For GitOps, where git is the source of truth, we either encrypt the secret before committing it — Sealed Secrets, SOPS — or keep only a reference in git and let an External Secrets Operator sync the real value from the backend."

| PT | EN |
|----|----|
| Segredo / credencial | Secret / credential |
| Gestão de segredos | Secrets management |
| Segredo estático | Static secret |
| Segredo dinâmico | Dynamic secret |
| Injeção em runtime | Runtime injection |
| Cofre de segredos | Secret manager / vault |
| Rotação de credenciais | Credential rotation |
| Menor privilégio | Least privilege |
| Criptografia em repouso | Encryption at rest |
| Criptografia em camadas (chave mestra + chave de dados) | Envelope encryption |
| Vazamento de segredo | Secret leak / secret exposure |
| Varredura de segredos | Secret scanning |
| Proteção no push | Push protection |
| Segredo comprometido | Compromised secret |

## O que vem a seguir

Esta nota fecha o sub-galho **Entrega e release** — a cadeia completa que começou no pipeline de CI/CD (nota 01), passou por estratégias de deploy e rollback (notas 02-03), migrações de banco (nota 04) e infraestrutura declarativa (nota 05), e termina aqui na camada final de segurança que atravessa tudo isso: como o sistema recebe, sem nunca expor, o que precisa para se autenticar no mundo. Com código, infraestrutura e credenciais chegando de forma segura a produção, a próxima etapa natural é o que acontece depois que o serviço já está no ar, servindo tráfego real, sob carga real — o sub-galho seguinte.

- [[3 - Rodar em produção/index|Rodar em produção]] — containers em produção, o contrato operacional do Kubernetes, zero-downtime, escala e resiliência: o que muda quando o sistema já está vivo e precisa continuar assim

## Veja também

- [[Operação/index|Operação]] — o galho-pai e o mapa completo da trilha
- [[2 - Entrega e release/index|Entrega e release]] — este sub-galho, agora completo
- [[02 - O contrato de uma app operável (12-Factor)]] — o fator Config, que esta nota aprofunda no caso específico de secrets
- [[05 - GitOps e Infrastructure as Code]] — o problema geral de "código versionado é a fonte da verdade"; esta nota resolve o caso específico em que essa fonte da verdade não pode conter segredo em claro

## Fontes

- **OWASP** — [Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) (OWASP Cheat Sheet Series, acessado em julho de 2026) — princípios gerais de ciclo de vida de segredo, least privilege, e passwordless authentication.
- **HashiCorp** — [Understand static and dynamic secrets](https://developer.hashicorp.com/vault/tutorials/get-started/understand-static-dynamic-secrets) e [Database secrets engine](https://developer.hashicorp.com/vault/docs/secrets/databases) (Vault Docs, acessado em julho de 2026) — a distinção entre rotação de secret estático e secrets dinâmicos com TTL.
- **Kubernetes** — [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/), [Encrypting Confidential Data at Rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) e [Good practices for Kubernetes Secrets](https://kubernetes.io/docs/concepts/security/secrets-good-practices/) (Kubernetes Docs, acessado em julho de 2026) — base64 não é criptografia, encryption at rest via KMS provider, RBAC.
- **GitHub Docs** — [About secret scanning](https://docs.github.com/code-security/secret-scanning/about-secret-scanning) e [Remediating a leaked secret in your repository](https://docs.github.com/en/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/remediating-a-leaked-secret) (acessado em julho de 2026) — push protection, e a orientação de tratar todo segredo vazado como comprometido.
- **GitGuardian** — [State of Secrets Sprawl 2026](https://blog.gitguardian.com/) e [Four Credential-Harvesting Campaigns Hit Open Source Ecosystems in Two Weeks](https://blog.gitguardian.com/four-credential-harvesting-campaigns-hit-open-source-ecosystems-in-two-weeks/) (2026) — os 29 milhões de segredos novos em repositórios públicos em 2025 e a campanha de maio de 2026 com 5.718 commits maliciosos.
- **AWS** — [AWS KMS cryptography essentials](https://docs.aws.amazon.com/kms/latest/developerguide/kms-cryptography.html) (AWS Docs, acessado em julho de 2026) — envelope encryption com chave mestra e chave de dados, o padrão conceitual replicado pelos KMS providers do Kubernetes.
- **Mozilla / CNCF** — [SOPS (Secrets OPerationS)](https://github.com/getsops/sops) (repositório GitHub, projeto Sandbox da CNCF) — criptografia por valor mantendo chaves legíveis para diff, integração com AWS/GCP/Azure KMS, PGP e age.
- **External Secrets Operator / Bitnami Sealed Secrets** — comparação de arquitetura entre referenciar um backend externo vs. cifrar o valor para commit direto no git, documentada em [Argo CD Secret Management](https://argo-cd.readthedocs.io/en/stable/operator-manual/secret-management/) e na documentação de ambos os projetos.
- **CyberArk / Doppler** — [Environment Variables Don't Keep Secrets](https://developer.cyberark.com/blog/environment-variables-dont-keep-secrets-best-practices-for-plugging-application-credential-leaks/) — os riscos de variáveis de ambiente como fonte de segredo: crash dumps, `/proc/PID/environ`, herança por processos filhos.
