---
title: "Usuários, grupos e o problema da credencial de longa duração"
type: concept
fase: Iniciado
created: 2026-07-20
updated: 2026-07-25
status: seedling
publish: true
tags:
  - cloud
  - aws
  - digitalocean
  - iam
  - identidade
  - credenciais
---
# Usuários, grupos e o problema da credencial de longa duração

> [!abstract] TL;DR
> Um usuário de nuvem — IAM user na AWS, membro de um Team na DigitalOcean — existe para representar uma pessoa ou uma aplicação e carregar credenciais que provam quem ela é. O problema não é o usuário: é o tipo de credencial mais comum que se anexa a ele, a **chave de acesso estática** (access key). Ela não expira sozinha, é fácil de colar num lugar errado (repositório, variável de ambiente, script), continua válida depois que quem a criou sai da empresa, e não deixa rastro óbvio de quem a está usando de fato. MFA reduz o risco de uma senha vazada, mas não resolve o problema da chave — são mecanismos diferentes protegendo pontos diferentes. E o usuário raiz, a identidade mais poderosa que existe numa conta, fica trancado por um motivo direto: qualquer credencial associada a ele, se vazar, dá controle total e irrestrito sobre a conta inteira, sem um teto de permissão para conter o estrago.

## O commit que ninguém queria ter feito

Um desenvolvedor está testando um script local que sobe arquivos para um bucket de armazenamento. Para não perder tempo configurando um perfil de credenciais no computador, ele cola a chave de acesso direto no topo do arquivo — `access_key = "AKIA..."`, `secret_key = "wJal..."` — só para essa sessão de teste, com a intenção de tirar depois. O script funciona, o teste passa, e ele segue para a próxima tarefa. Duas semanas depois, faz um commit rápido no fim do dia, sem revisar o diff com cuidado, e sobe o arquivo — chave incluída — para um repositório que, sem que ele lembrasse, é público.

Não é um cenário hipotético raro: é comum o suficiente para que o próprio GitHub mantenha um **programa de parceria de secret scanning**, que varre commits públicos em busca de formatos de credencial conhecidos — inclusive os de provedores de nuvem — e, ao encontrar uma correspondência de um provedor parceiro, notifica automaticamente esse provedor para que ele revogue a credencial antes que alguém mal-intencionado a use. A AWS é um desses parceiros. O fato de essa infraestrutura de detecção automática existir e operar em produção diz algo importante: o vazamento de chave estática em repositório não é um acidente raro de um desenvolvedor descuidado — é comum o bastante para justificar um sistema de vigilância permanente rodando sobre todo commit público da plataforma.

Só que o commit é só uma das portas de saída. A mesma chave podia ter vazado de outro jeito, igualmente banal: uma variável de ambiente ecoada sem querer num log de aplicação, um `.env` sincronizado num backup que também sincroniza para um serviço de nuvem pessoal, um print de terminal colado num canal de chat da empresa "só para debug", um script de CI que imprime todas as variáveis de ambiente ao falhar. Nenhum desses caminhos exige um atacante sofisticado. Todos exigem só uma coisa: que a chave exista, esteja copiável, e não tenha prazo de validade embutido.

É essa combinação — copiável e sem prazo — que faz da chave de acesso estática a pior credencial que existe na nuvem. Esta nota constrói esse argumento peça por peça: o que é um usuário e um grupo, por que a chave estática concentra tanto risco, o papel do MFA, e por que a identidade mais poderosa da conta fica deliberadamente fora de uso no dia a dia.

```mermaid
flowchart TD
    A["Chave de acesso criada<br/>para um teste rápido"] --> B{"Onde ela pode vazar?"}
    B --> C["Commit em repositório<br/>(até público, por engano)"]
    B --> D["Variável de ambiente<br/>ecoada em log"]
    B --> E["Script de CI que<br/>imprime env em falha"]
    B --> F["Backup ou print<br/>compartilhado 'só para debug'"]
    C --> G["Credencial válida,<br/>sem prazo, fora do controle<br/>de quem a criou"]
    D --> G
    E --> G
    F --> G
```

## Usuário e grupo: a unidade básica de identidade

Um **usuário** (IAM user, na AWS) é uma entidade nomeada dentro de uma conta de nuvem, que representa uma pessoa ou uma carga de trabalho e carrega credenciais próprias. Por padrão, um usuário recém-criado não tem permissão nenhuma — nem para listar os próprios recursos da conta. Permissão é algo que se concede depois, explicitamente, seja diretamente ao usuário, seja através de um **grupo**.

O grupo existe para resolver um problema de escala organizacional simples: se dez pessoas do time de dados precisam da mesma permissão de leitura num data warehouse, conceder essa permissão dez vezes, individualmente, é trabalho redundante e uma fonte garantida de inconsistência — alguém vai esquecer de atualizar uma das dez quando a política mudar. Um grupo agrupa usuários e recebe permissões uma única vez; todo usuário membro do grupo herda essas permissões automaticamente. Adicionar a décima primeira pessoa ao time de dados vira uma operação de "colocar no grupo certo", não de "recriar a mesma configuração de permissão do zero".

Isso já é, em miniatura, o problema que a **nota seguinte desta trilha** vai tratar a fundo — como uma permissão é de fato avaliada. Por ora, o que importa é a peça anterior: quem é o usuário, e com que credencial ele prova que é quem diz ser.

```mermaid
flowchart LR
    subgraph SemGrupo["Sem grupo — 10 concessões separadas"]
        P1["Política de leitura<br/>no data warehouse"] --> U1["Usuário 1"]
        P1 --> U2["Usuário 2"]
        P1 --> U3["... Usuário 10"]
    end
    subgraph ComGrupo["Com grupo — 1 concessão, 10 heranças"]
        G["Grupo: time-de-dados<br/>(política anexada uma vez)"] --> M1["Usuário 1"]
        G --> M2["Usuário 2"]
        G --> M3["... Usuário 10"]
    end
```

Na prática, criar o usuário, criar o grupo e conceder a permissão uma única vez, no grupo, é uma sequência curta de chamadas de API. Todo comando abaixo segue a sintaxe documentada no AWS CLI Command Reference:

```bash
# Criar o usuário — nasce sem nenhuma permissão
aws iam create-user --user-name maria.dados
```

```bash
# Criar o grupo — uma vez só, não por pessoa
aws iam create-group --group-name time-de-dados
```

```bash
# Anexar a política ao grupo, não a cada usuário individualmente
aws iam attach-group-policy \
    --group-name time-de-dados \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

```bash
# Colocar o usuário no grupo — ele herda a política imediatamente
aws iam add-user-to-group \
    --user-name maria.dados \
    --group-name time-de-dados
```

A décima primeira pessoa do time repete só o último comando — `add-user-to-group`. Nenhuma política nova, nenhuma configuração duplicada.

## As credenciais de um usuário

Um usuário de nuvem pode ter mais de um tipo de credencial ao mesmo tempo, cada uma para um canal de acesso diferente:

- **Senha de console** — usada para login interativo na interface web do provedor. Existe só para humanos que operam pelo navegador.
- **Chave de acesso** (*access key*, na AWS) — um par de valores, um **ID da chave de acesso** e uma **chave de acesso secreta**, usado para autenticar chamadas programáticas: linha de comando, SDK, scripts, integrações de CI/CD. É o par que qualquer chamada de API precisa apresentar quando não há uma sessão de navegador por trás.
- Outras formas mais específicas — chave SSH para um serviço de versionamento de código gerenciado, certificado de servidor para TLS em cenários legados — que não fazem parte do escopo desta nota.

A senha de console e a chave de acesso protegem canais diferentes, mas compartilham a mesma propriedade estrutural que interessa aqui: são **credenciais de longa duração**. Uma vez criadas, continuam válidas indefinidamente até que alguém, manualmente, decida desativá-las ou apagá-las. Não existe um relógio embutido que as invalide sozinho depois de um dia, uma hora, ou uma sessão.

> [!tip] Assista: AWS IAM Users and Groups | Part 1 | AWS IAM Tutorials
> **Canal:** BeSA Cloud Academy | **Duração:** ~17min | **Idioma:** EN
>
> O mesmo vídeo mostra, na prática, a troca de canal de autenticação que esta seção descreve: login por senha no console versus a chave de acesso alfanumérica exigida quando a mesma identidade precisa autenticar chamadas programáticas (CLI, SDK) em vez de uma sessão de navegador.
> Trecho de destaque [02:48]: *"time I have to provide something else which is called access key and secret access key it's like alpha numeric"*
>
> 🎬 [Assistir no YouTube](https://www.youtube.com/watch?v=1leLe7qlkqA)

Criar uma chave é uma única chamada — e é aí que o problema começa: nada na resposta da API avisa que aquele par de valores vai sobreviver para sempre.

```bash
# Cria a chave — o segredo só aparece nesta resposta, uma vez
aws iam create-access-key --user-name maria.dados
```

```json
{
    "AccessKey": {
        "UserName": "maria.dados",
        "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
        "Status": "Active",
        "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY",
        "CreateDate": "2026-07-20T18:39:23Z"
    }
}
```

Note o que **não** aparece nesse JSON: nenhum campo de expiração. `CreateDate` registra quando a chave nasceu, não quando ela morre — porque ela não morre sozinha. Para saber há quanto tempo uma chave existente está ativa e quando foi usada pela última vez:

```bash
# Lista as chaves do usuário e quando cada uma foi usada por último
aws iam list-access-keys --user-name maria.dados
```

> [!info] Fronteira
> Autenticação (provar quem você é) e autorização (o que você pode fazer depois de provar) já foram distinguidas na **nota 01** deste galho. Aqui, o assunto é só o primeiro lado — a credencial que carrega a prova de identidade. O que essa identidade pode fazer, uma vez autenticada, é o assunto da política — nota seguinte desta trilha.

## Por que a chave estática é a pior credencial que existe

A documentação da própria AWS é direta sobre isso, num tom que raramente aparece em documentação técnica: "IAM users with access keys are an account security risk" — usuários IAM com chaves de acesso são um risco de segurança da conta. Não é um aviso genérico de boa prática — é um alerta específico sobre esse tipo particular de credencial. Vale desmontar por que, ponto a ponto.

| Propriedade | Chave de acesso estática | Credencial temporária (nota 04) |
|---|---|---|
| Expiração | Nenhuma — vale até ser revogada à mão | Embutida na criação, minutos a horas |
| Rastreabilidade | Uma string, copiável para qualquer lugar sem registro central | Emitida por sessão, atrelada ao papel assumido |
| Raio de vazamento | Tudo que a política do usuário permitir, pelo tempo que ninguém perceber | Limitado à janela de validade da sessão |
| Dono sai da empresa | Chave continua ativa até alguém procurar e revogar manualmente | Sessão expira sozinha; nada para esquecer |

**Ela não expira sozinha.** Uma chave de acesso criada hoje continua funcionando daqui a um ano, cinco anos, dez anos — a menos que alguém, ativamente, entre no painel e a revogue. Comparado com uma credencial temporária (o assunto da nota 04 desta trilha), que carrega um prazo de validade embutido e simplesmente para de funcionar quando esse prazo acaba, a chave estática exige vigilância humana contínua para não virar um risco permanente. E vigilância humana contínua é exatamente o tipo de tarefa que, na prática, as organizações fazem mal — não por incompetência, mas porque "revisar chaves antigas" nunca compete de igual para igual, na fila de prioridades de um time, com uma entrega de produto com prazo.

**Ela vaza em lugares banais.** A cena do começo desta nota — chave colada num script "só para teste", esquecida, commitada — não é folclore de segurança. É comportamento humano previsível sob pressão de prazo: copiar-colar é mais rápido que configurar um mecanismo de credencial adequado, e "eu tiro isso depois" é uma promessa que compete com todas as outras tarefas do dia. A própria AWS lista, em letras maiúsculas na documentação oficial, o que **não** fazer: não embutir chaves de acesso em código de aplicação, não incluir arquivos com chaves na área do projeto, não usar as credenciais da conta raiz para criar chaves. O fato de a documentação precisar dizer isso tão explicitamente é, por si, evidência de que a prática errada é comum o suficiente para merecer o aviso.

**Ela sobrevive ao desligamento de quem a criou.** Uma chave de acesso não está amarrada ao emprego de ninguém — está amarrada ao usuário IAM ao qual foi anexada. Se um funcionário sai da empresa e o processo de desligamento cuida de desativar o login dele no provedor de identidade corporativo, mas esquece de revogar uma chave de acesso que ele havia criado meses antes para um script pessoal de automação, essa chave continua válida, silenciosamente, até que alguém a encontre numa auditoria — se é que alguém a encontra. Isso não é um cenário exótico: é exatamente o motivo pelo qual a AWS oferece uma ferramenta dedicada, o **relatório de credenciais** (*credential report*), que lista todo usuário IAM da conta e o status de cada senha e chave de acesso associada — incluindo há quanto tempo cada uma foi usada pela última vez. A existência dessa ferramenta é reconhecimento institucional de que "encontrar credenciais órfãs" é problema comum demais para depender de alguém lembrar manualmente.

Uma varredura rápida em duas chamadas — a AWS armazena um único relatório por conta e o reaproveita se tiver menos de quatro horas:

```bash
# Pede a geração do relatório mais recente (CSV, um usuário por linha)
aws iam generate-credential-report
```

```bash
# Baixa o relatório — o conteúdo vem em base64, precisa decodificar
aws iam get-credential-report --query 'Content' --output text | base64 -d > credential-report.csv
```

O CSV resultante tem colunas como `access_key_1_active`, `access_key_1_last_rotated` e `access_key_1_last_used_date` — exatamente o que uma auditoria de chaves esquecidas precisa cruzar. Para uma visão mais rápida e agregada, sem baixar o CSV inteiro:

```bash
# Retrato agregado da conta: quantos usuários, quantas chaves ativas, MFA habilitado
aws iam get-account-summary
```

Quando o relatório aponta uma chave suspeita, o passo seguinte não é apagar direto — é desativar primeiro, confirmar que nada quebrou, e só então apagar:

```bash
# Desativa sem apagar — reversível se algo depender dela
aws iam update-access-key \
    --user-name maria.dados \
    --access-key-id AKIAIOSFODNN7EXAMPLE \
    --status Inactive
```

```bash
# Confirmado que nada quebrou, agora sim revoga de vez
aws iam delete-access-key \
    --user-name maria.dados \
    --access-key-id AKIAIOSFODNN7EXAMPLE
```

```mermaid
flowchart TD
    A["Chave criada<br/>(Active)"] --> B["Em uso normal"]
    B --> C{"Relatório de credenciais<br/>aponta uso antigo?"}
    C -->|Não| B
    C -->|Sim| D["update-access-key<br/>--status Inactive"]
    D --> E{"Algo quebrou<br/>em produção?"}
    E -->|Sim| F["Reativa: --status Active<br/>investiga o dono real"]
    E -->|Não, período seguro passou| G["delete-access-key<br/>— revogação definitiva"]
    F --> C
```

**Ela é difícil de rastrear.** Uma chave de acesso é só duas strings. Ela não sabe, por si mesma, em qual laptop está salva, em quantos scripts foi copiada, ou se foi compartilhada num canal de chat "só dessa vez". Diferente de uma sessão de navegador, que tem um único ponto de uso ativo por vez, uma chave pode estar simultaneamente num arquivo de configuração local, num pipeline de CI, num script de automação esquecido num servidor antigo — e cada um desses lugares é uma superfície de vazamento independente, sem que exista, por padrão, um único lugar central onde alguém possa ver "todos os lugares onde essa chave está em uso agora".

A soma dessas quatro propriedades — sem prazo, fácil de vazar, sobrevive ao dono, difícil de rastrear — é o motivo pelo qual a orientação mais recente da própria AWS parou de tratar chave de acesso como o caminho padrão de acesso programático e passou a recomendar, explicitamente, que se prefiram **credenciais temporárias** sempre que possível — o mecanismo que a nota 04 desta trilha vai desenrolar em detalhe. Esta nota planta o problema; a solução fica para lá, de propósito.

> [!info] Fronteira
> Esta nota não resolve o problema que acabou de descrever — só o expõe com clareza. O mecanismo que a nuvem oferece para eliminar a necessidade de credencial de longa duração (assumir um papel, receber uma credencial temporária que expira sozinha em minutos ou horas) é o assunto da **nota 04** desta trilha.

## MFA: reforça o login, não resolve a chave

Autenticação multifator (MFA) exige uma segunda prova de identidade além da senha — um código gerado por um aplicativo autenticador, uma chave de segurança física baseada em FIDO, ou um token de hardware que gera um código numérico temporário. A AWS recomenda MFA para todo usuário IAM, e o torna obrigatório para o usuário raiz — mas vale entender exatamente o que o MFA protege e o que ele deixa de fora.

MFA protege o **login interativo**: alguém tentando entrar no console pela senha precisa, além da senha, de um segundo fator que só o dono legítimo da conta deveria conseguir apresentar. Isso é uma defesa real contra senha vazada ou adivinhada.

MFA **não** protege uma chave de acesso comprometida. Quando alguém usa uma chave de acesso para autenticar uma chamada de API, a chamada não passa por tela de login nenhuma — não há segundo fator para apresentar, porque o fluxo inteiro é programático, sem interação humana no momento da chamada. Uma chave de acesso vazada continua plenamente funcional mesmo numa conta com MFA habilitado e bem configurado para login de console. São dois mecanismos de defesa cobrindo dois canais diferentes de acesso — e um deles, MFA, simplesmente não tem jurisdição sobre o canal onde a chave estática opera.

Vale notar, também, que a AWS foi ampliando o tipo de fator recomendado ao longo do tempo: hoje a orientação prioriza mecanismos resistentes a phishing — passkeys e chaves de segurança físicas baseadas em FIDO — sobre aplicativos autenticadores baseados em código numérico (TOTP), que continuam suportados mas são tratados como alternativa intermediária ("enquanto o hardware não chega"). A AWS encerrou o suporte à habilitação de MFA por SMS — o motivo não é detalhado na documentação oficial, mas se alinha à razão conhecida do setor: mensagens de texto são vulneráveis a ataques de troca de SIM, o que faz do SMS o elo mais fraco entre os fatores disponíveis.

Registrar um dispositivo MFA virtual e anexá-lo a um usuário são duas chamadas separadas — a primeira gera o QR code, a segunda exige dois códigos consecutivos do app autenticador, prova de que o dispositivo está de fato sincronizado:

```bash
# Gera o dispositivo virtual e salva o QR code para escanear no app
aws iam create-virtual-mfa-device \
    --virtual-mfa-device-name maria.dados-mfa \
    --outfile QRCode.png \
    --bootstrap-method QRCodePNG
```

```bash
# Anexa o dispositivo ao usuário — exige dois códigos consecutivos do app,
# para provar que o relógio do dispositivo está sincronizado com a AWS
aws iam enable-mfa-device \
    --user-name maria.dados \
    --serial-number arn:aws:iam::210987654321:mfa/maria.dados-mfa \
    --authentication-code1 123456 \
    --authentication-code2 789012
```

Os dois códigos precisam ser enviados logo em seguida da geração — um TOTP expira em segundos, e esperar demais dessincroniza o dispositivo antes mesmo de ele entrar em uso.

## O usuário raiz: por que ele fica trancado

Toda conta de nuvem nasce com uma identidade original, criada no momento em que a conta é aberta, com controle irrestrito sobre absolutamente tudo — todos os recursos, toda a configuração de cobrança, a capacidade de fechar a conta inteira. Na AWS, essa identidade é o **usuário raiz** (*root user*).

A orientação oficial é direta: não usar o usuário raiz no dia a dia. Criar, logo na primeira configuração da conta, um usuário administrativo separado, e reservar o raiz só para um punhado de tarefas que exigem especificamente essa identidade — coisas como fechar a conta ou alterar certas configurações de faturamento no nível mais alto, que a AWS restringe deliberadamente só ao raiz. Fora dessas exceções raras, o raiz fica trancado.

A razão é a mesma lógica de risco desta nota inteira, levada ao extremo: o usuário raiz não tem — nem pode ter — um teto de permissão que limite o estrago em caso de comprometimento. Um IAM user comum, mesmo mal configurado, ainda está sujeito a qualquer restrição que uma política explicitamente negue (assunto da próxima nota). O usuário raiz não está sujeito a nenhuma política — ele **é** a permissão máxima, por definição, sem exceção possível. Se uma credencial de um IAM user vaza, o dano está limitado ao que aquele usuário específico tinha permissão de fazer. Se a credencial do usuário raiz vaza, o dano é irrestrito por construção.

É por isso que a orientação da AWS vai além de "use MFA no raiz" — ela recomenda ativamente **não criar chave de acesso alguma para o usuário raiz**. Combinar a identidade mais poderosa da conta com o tipo de credencial mais fácil de vazar é a pior combinação possível dentro do espaço de risco que esta nota mapeou. A prática recomendada, para as raras tarefas que realmente exigem o raiz, é autenticar via login no console com senha forte e MFA obrigatório — nunca via chave de acesso programática.

E se a tarefa exigir o raiz na linha de comando, não no console? A documentação oficial de boas práticas do raiz endereça exatamente essa lacuna: em vez de criar uma access key para o raiz, o comando `aws login` autentica a CLI e os SDKs com as credenciais do raiz e devolve credenciais temporárias, renovadas automaticamente — a mesma lógica de "sem chave persistente para vazar" que a nota 04 desta trilha vai generalizar para todo o resto da conta.

> [!info] Fronteira
> O funcionamento interno do `aws login` — o que ele assume por trás dos panos — é o mesmo mecanismo de credencial temporária que a nota 04 explica em detalhe. Aqui, o ponto é só que ele existe como alternativa à chave de acesso, mesmo para o raiz.

## A lente dupla: IAM users da AWS vs. Teams e tokens da DigitalOcean

A AWS constrói identidade em torno do IAM user: uma entidade nomeada, com permissões concedidas por política, credenciais próprias (senha, chave de acesso), e um raiz separado e deliberadamente trancado atrás dele.

A DigitalOcean parte de um modelo mais simples. A unidade organizacional é o **Team** — você gerencia infraestrutura e cobrança através de um time, seja sozinho, seja convidando outras pessoas. Cada membro do time recebe um **papel** (role) que determina suas permissões: a DigitalOcean oferece um conjunto de papéis predefinidos cobrindo os casos de uso mais comuns (de proprietário do time, com controle total, a papéis mais restritos voltados a operação de recursos específicos), além da opção de criar **papéis customizados** com permissões granulares escolhidas manualmente — um paralelo direto, embora mais enxuto, do que uma política da AWS faz para um IAM user.

O ponto onde a DigitalOcean não tem equivalente direto ao IAM user é sutil e vale nomear com honestidade: não existe, na DO, uma entidade separada representando "esta aplicação específica" com um nome e um ARN próprio, do jeito que um IAM user pode representar tanto uma pessoa quanto uma carga de trabalho na AWS. O acesso programático da DO passa por outro mecanismo — o **Personal Access Token**, um token que funciona como um token de acesso OAuth, incluído no cabeçalho `Authorization` de cada chamada à API.

E é exatamente aqui que a DigitalOcean, apesar do modelo mais simples, resolve uma fatia do problema que esta nota descreveu para chave de acesso estática de um jeito que a AWS, historicamente, não resolvia por padrão: **o token da DO tem expiração escolhida no momento da criação**. Você decide por quanto tempo aquele token vale, e passado esse intervalo ele simplesmente para de autenticar — sem exigir que alguém lembre de revogá-lo manualmente. Além disso, cada token pode receber escopos granulares baseados nas operações de criar, ler, atualizar e apagar (CRUD) que ele autoriza, em vez de herdar cegamente tudo que o dono do token pode fazer.

Isso não apaga o restante do argumento desta nota — um token da DO ainda é uma string copiável, ainda pode vazar num commit, ainda funciona sem segundo fator no momento da chamada de API, e a própria documentação da DigitalOcean avisa, quase nas mesmas palavras da AWS: "keep your tokens secret — they function like passwords". Mas o prazo de validade embutido, por padrão disponível na criação do token, é uma diferença estrutural real, não cosmética — é um passo a mais em direção ao que a nota 04 desta trilha vai chamar de "credencial de curta duração", ainda que a DigitalOcean chegue lá por um caminho mais simples e menos completo que o modelo de papéis assumíveis da AWS.

Há uma pegadinha que vale registrar: o token da DO **não pode ter o escopo editado depois de criado**. Se um pipeline de CI foi configurado com escopo `Full Access` e devia ter sido `Droplet: Create`, a correção não é editar — é gerar um token novo com o escopo certo e trocar em todo lugar que usava o antigo. Diferente de uma política IAM anexada a um grupo, que pode ser ajustada em produção sem tocar na credencial em si.

Usar o token, na prática, é configurar o `doctl` uma vez e deixar a CLI cuidar do cabeçalho de autenticação daí em diante:

```bash
# Cola o token quando solicitado; nomeia esse contexto de autenticação
doctl auth init --context producao
```

```bash
# Confirma que a autenticação funcionou — retorna email, UUID, status da conta
doctl account get
```

Sem `doctl`, o mesmo token vai direto no cabeçalho `Authorization` de qualquer chamada HTTP à API:

```bash
curl -X GET \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" \
    "https://api.digitalocean.com/v2/account"
```

| Propriedade | AWS access key (IAM user) | DigitalOcean Personal Access Token |
|---|---|---|
| Expiração escolhida na criação | Não — é preciso desativar manualmente | Sim, intervalo definido no momento da criação |
| Escopo editável depois de criado | Sim, via política anexada ao usuário/grupo | Não — exige gerar um token novo |
| Máximo simultâneo por identidade | 2 chaves ativas por usuário IAM | Sem teto documentado da mesma forma |

| Conceito | AWS | Azure | GCP | DigitalOcean |
|---|---|---|---|---|
| Identidade de usuário | IAM user | Microsoft Entra ID user | Cloud Identity / IAM user | Membro de Team |
| Agrupamento de permissões | Grupo IAM | Grupo do Entra ID | Grupo do Google Workspace/Cloud Identity | Papel (role) predefinido ou customizado |
| Credencial programática | Access key (ID + secret) | Client secret / certificado de app registrado | Chave de conta de serviço | Personal Access Token |
| Identidade mais privilegiada | Usuário raiz (root user) | Conta de proprietário global do tenant | Proprietário do projeto/organização | Owner do Team |

> [!info] Caducidade
> Nomes de papel, tipos de MFA suportados e comportamento de expiração de token verificados em 2026-07-23. A lista de papéis predefinidos da DigitalOcean e as opções específicas de MFA da AWS são áreas que os provedores ajustam com alguma frequência — confira a documentação oficial antes de configurar uma conta real.

## Casos práticos

**A automação que ninguém sabia quem tinha criado.** Um pipeline de deploy antigo, escrito anos atrás, referencia uma variável de ambiente com uma chave de acesso que ninguém no time atual reconhece. A pessoa que a criou já não trabalha mais na empresa. Ninguém sabe, com certeza, se essa chave ainda é necessária, o que aconteceria se fosse revogada, ou que permissões exatas ela carrega — porque não há um registro vivo ligando "esta chave" a "este propósito". A resolução exige um trabalho de arqueologia: rodar o relatório de credenciais, cruzar com a data do último uso, testar a revogação num ambiente controlado antes de fazer isso em produção. Esse tipo de situação é exatamente o sintoma que uma credencial de longa duração sem dono claro produz — e é o tipo de trabalho que simplesmente não existe quando o acesso é concedido via papel assumível com credencial temporária, porque não há chave persistente para se perder de vista.

**O token de CI com escopo maior do que precisava.** Um pipeline de integração contínua precisa só de permissão para publicar uma imagem de container num registro. Por conveniência, alguém gera um Personal Access Token com acesso total (*Full Access*) em vez de configurar os escopos granulares de create/read/update/delete que cobririam exatamente a operação necessária. Meses depois, um log de erro do próprio pipeline, por acidente, imprime o token completo numa mensagem de falha visível para todo o time. Como o escopo era total, o vazamento desse único token expõe muito mais do que a capacidade de publicar imagens — expõe qualquer operação que aquele token, com aquele escopo amplo, tivesse permissão de fazer. O princípio que evitaria esse estrago — conceder só o necessário, escopo por escopo — é o mesmo raciocínio que a próxima nota desta trilha vai formalizar como a lógica de avaliação de uma política.

**A auditoria que revelou seis chaves de acesso ativas para um usuário que só precisava de uma.** Um usuário IAM de serviço acumula, ao longo de dois anos, múltiplas chaves de acesso criadas em momentos diferentes — uma para um script de migração de dados que rodou uma vez e nunca mais, outra para um teste de integração que ficou esquecida, outra ainda ativa e de fato em uso. A AWS permite no máximo duas chaves de acesso simultâneas por usuário justamente para forçar alguma disciplina de rotação — mas nada impede que as duas permitidas fiquem, ambas, obsoletas e esquecidas ao mesmo tempo. Uma auditoria de segurança, rodando o relatório de credenciais, descobre a situação só quando já é tarde para saber com certeza se alguma das chaves antigas foi usada por alguém sem autorização no meio do caminho.

## Armadilhas comuns

> [!warning] Achar que revogar a senha do funcionário desligado é suficiente
> O processo de desligamento de RH normalmente desativa o login corporativo — mas uma chave de acesso, criada meses ou anos antes para um script ou uma integração pessoal, não está amarrada a esse login. Ela continua válida até alguém, especificamente, ir ao painel de IAM e revogá-la. Offboarding de identidade de nuvem exige uma varredura própria de credenciais, não só a desativação do SSO corporativo.

> [!warning] Tratar MFA como solução completa de segurança de credencial
> MFA protege login de console contra senha comprometida — não protege chave de acesso comprometida, porque chamadas de API autenticadas por chave não passam por segundo fator nenhum. Uma conta com MFA impecável no console pode, ainda assim, estar exposta por uma chave de acesso vazada há meses num repositório privado que alguém tornou público sem perceber.

> [!warning] Criar chave de acesso para o usuário raiz "só para automatizar uma tarefa administrativa"
> É exatamente a combinação que a orientação oficial pede para evitar: a identidade sem teto de permissão, presa à credencial mais fácil de vazar e mais difícil de conter depois do vazamento. Qualquer tarefa que pareça exigir automação via raiz quase sempre tem uma alternativa — um usuário administrativo com permissão suficiente, mas não irrestrita — que resolve o mesmo problema sem essa exposição.

## O que vem a seguir

Esta nota mapeou o problema, mas deixou uma pergunta em aberto de propósito: se um usuário tem permissão concedida por política, como exatamente a nuvem decide, no momento de cada chamada de API, se aquela ação específica é permitida ou negada? A resposta não é tão óbvia quanto parece — envolve uma lógica de avaliação com uma regra que surpreende quem vem de outros modelos de permissão, e explica por que "funciona no console mas falha na aplicação" é um dos erros mais comuns e mais confusos de depurar na nuvem. Essa é a **próxima nota** desta trilha: **Políticas — como uma permissão é avaliada**.

## Fontes

- [AWS IAM — IAM users (documentação oficial)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) — definição de IAM user, tipos de credencial associados, uso como service account; acessado em 2026-07-23.
- [AWS IAM — Manage access keys for IAM users (documentação oficial)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) — estrutura da access key, limite de duas chaves por usuário, avisos explícitos contra embutir chaves em código; acessado em 2026-07-23.
- [AWS IAM — Root user best practices (documentação oficial)](https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html) — por que não usar o usuário raiz no dia a dia, recomendação contra criar access key para o raiz, MFA obrigatório; acessado em 2026-07-23.
- [AWS IAM — Multi-factor authentication in IAM (documentação oficial)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html) — tipos de MFA suportados (passkeys/security keys, TOTP virtual, hardware TOTP), descontinuação de MFA por SMS; acessado em 2026-07-23.
- [GitHub Docs — About secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning) — programa de parceria de secret scanning, notificação automática a provedores parceiros sobre credenciais vazadas em repositórios públicos; acessado em 2026-07-23.
- [GitHub Docs — Supported secret scanning patterns](https://docs.github.com/en/code-security/secret-scanning/introduction/supported-secret-scanning-patterns) — confirma a Amazon AWS Access Key ID como padrão coberto pelo programa parceiro; acessado em 2026-07-23.
- [AWS CLI Command Reference — iam](https://docs.aws.amazon.com/cli/latest/reference/iam/) — sintaxe verificada dos comandos `create-user`, `create-group`, `add-user-to-group`, `attach-group-policy`, `create-access-key`, `list-access-keys`, `update-access-key`, `delete-access-key`, `generate-credential-report`, `get-credential-report`, `get-account-summary`, `create-virtual-mfa-device` e `enable-mfa-device`; acessado em 2026-07-23.
- [DigitalOcean — doctl install and configure](https://docs.digitalocean.com/reference/doctl/how-to/install/) — sintaxe de `doctl auth init` e `doctl account get`; acessado em 2026-07-23.
- [DigitalOcean — Teams (documentação oficial)](https://docs.digitalocean.com/platform/teams/) — modelo de Team para infraestrutura e cobrança compartilhada, papéis predefinidos e customizados; acessado em 2026-07-23.
- [DigitalOcean — Team roles (documentação oficial)](https://docs.digitalocean.com/platform/teams/roles/) — existência de seis papéis predefinidos e papéis customizados com permissões granulares; acessado em 2026-07-23.
- [DigitalOcean API — How to Create a Personal Access Token (documentação oficial)](https://docs.digitalocean.com/reference/api/create-personal-access-token/) — funcionamento do token como bearer token, escolha de expiração na criação, escopos CRUD, impossibilidade de editar escopo após criação, orientação de tratar tokens como senhas; acessado em 2026-07-23.
