---
title: "Segredos no histórico"
created: 2026-07-31
updated: 2026-07-31
type: concept
status: seedling
fase: Magus
tags:
  - controle-de-versao
  - git
  - seguranca
  - tecnologia
publish: true
---

# Segredos no histórico

> [!abstract] TL;DR
> Se uma credencial entrou no repositório, a primeira ação **não** é limpar o histórico: é **rotacionar a credencial**. Enquanto ela for válida, o estrago é possível; depois de trocada, o que sobrou no histórico é lixo inofensivo. Só então vem a limpeza, com `git filter-repo` (o `filter-branch` está oficialmente desaconselhado) — uma operação que reescreve todos os commits, muda todos os hashes e obriga todo mundo a reclonar. E há um detalhe que quase ninguém sabe: em repositório hospedado, apagar localmente **não basta** — a plataforma mantém os objetos acessíveis até que você peça a remoção.

---

## A ordem certa das ações

O instinto é errado. Quando alguém percebe que commitou o `.env`, a reação típica é entrar em pânico com o histórico — e gastar duas horas nisso enquanto a chave continua ativa.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
graph TB
    A["Descobri o vazamento"] --> B["<b>1. ROTACIONAR</b><br/>invalidar a credencial<br/>e emitir outra"]
    B --> C["<b>2. Avaliar exposição</b><br/>era público? por quanto tempo?<br/>há log de uso indevido?"]
    C --> D["<b>3. Prevenir</b><br/>.gitignore, secret scanning,<br/>gerenciador de segredos"]
    D --> E["<b>4. Limpar o histórico</b><br/>filter-repo + suporte da plataforma"]
```

**A ordem importa mais que a técnica.** Rotacionar é rápido, resolve o risco real, e não depende de coordenar ninguém. Limpar histórico é demorado, disruptivo e não desfaz nada que já foi copiado.

> [!warning] Assuma que já foi lido
> **O que acontece:** "ficou público por dez minutos, tudo bem".
> **Por quê:** existem robôs que monitoram o fluxo público de commits em tempo real, exatamente procurando por padrões de chave. Dez minutos é tempo de sobra; há relatos de exploração em menos de um minuto.
> **Como agir:** em repositório público, trate como comprometida **sempre**, sem exceção. Em repositório privado, avalie quem tinha acesso — mas o custo de rotacionar costuma ser menor que o de investigar.

---

## Por que apagar num commit novo não resolve

Pelo nível 3: os objetos são imutáveis e continuam alcançáveis pelos commits antigos (nota 17). Remover o arquivo cria um commit novo onde ele não está — e todos os commits anteriores continuam contendo o blob com a chave.

```bash
git log --all --full-history -- .env      # todos os commits que tocaram o arquivo
git show <commit>:.env                    # e o conteúdo continua ali
```

Qualquer pessoa com o repositório tem a chave, mesmo que o `git status` de hoje não mostre nada.

---

## A limpeza: `git filter-repo`

A ferramenta recomendada é o **`git-filter-repo`**, um projeto externo que a própria documentação do Git aponta como substituto do `filter-branch` (que está desaconselhado por ser lento, cheio de armadilhas e propenso a corromper).

```bash
# instalar (Python)
pip install git-filter-repo

# remover um arquivo de todo o histórico
git filter-repo --invert-paths --path .env

# remover uma pasta inteira
git filter-repo --invert-paths --path dados/brutos/

# substituir o texto de uma chave, mantendo o resto
git filter-repo --replace-text expressoes.txt
```

O arquivo de substituições tem uma regra por linha:

```text
AKIAIOSFODNN7EXAMPLE==>CHAVE_REMOVIDA
literal:senha123==>REMOVIDO
```

Uma alternativa mais simples para o caso "remover arquivos grandes ou por nome" é o **BFG Repo-Cleaner**, que é mais rápido e tem interface mais direta, embora menos flexível.

> [!info] Por que o `filter-repo` exige um clone limpo
> Ele recusa rodar num repositório com modificações pendentes ou que não seja um clone fresco, e remove o `origin` depois de operar. Isso é proposital: a reescrita é destrutiva e irreversível, e ele força você a trabalhar sobre uma cópia — para que o original continue existindo enquanto você confere o resultado.

---

## O que acontece depois — e é aqui que dói

A reescrita muda o hash de **todos** os commits a partir do primeiro afetado (nota 17: mudou o conteúdo, mudou o hash; mudou o pai, mudou o hash dos descendentes). Na prática, o repositório inteiro passa a ser outro.

Consequências que precisam ser planejadas antes, não descobertas depois:

- **Todo mundo precisa reclonar.** Um `git pull` numa cópia antiga tenta mesclar as duas histórias e produz um monstro. O procedimento correto para quem tem cópia é reclonar, ou `git fetch` + `git reset --hard origin/main` — e qualquer trabalho local não publicado precisa ser resgatado por `cherry-pick` antes.
- **Pull requests abertos quebram.** As referências apontam para commits que deixaram de existir.
- **Tags e releases** precisam ser recriadas.
- **Forks continuam com a história antiga**, inclusive com a chave. Você não controla o repositório dos outros.
- **A plataforma ainda guarda os objetos.** Este é o ponto mais ignorado: no GitHub, commits antigos continuam acessíveis por URL direta mesmo depois de removidos do histórico, porque a rede do repositório mantém os objetos em cache. **É preciso abrir um chamado no suporte** pedindo a remoção — e mesmo assim os forks são um problema à parte.

Some tudo isso e a conclusão fica óbvia: **a limpeza é cara e imperfeita; a rotação é barata e efetiva.** Faça a limpeza para higiene e conformidade, não como medida de segurança.

---

## Prevenção, que é onde vale investir

| Camada | O quê |
|---|---|
| **Não escreva o segredo em arquivo** | variáveis de ambiente, cofres (Vault, Secrets Manager), gerenciador de segredos da plataforma |
| **`.gitignore` desde o primeiro commit** | `.env`, `*.pem`, `*.key`, `credentials.json` — antes de existir arquivo |
| **Arquivo de exemplo versionado** | `.env.example` com as chaves e valores falsos: documenta sem vazar |
| **Hook local de pré-commit** | `gitleaks`, `detect-secrets` ou `talisman` barram antes do commit existir |
| **Verificação no servidor** | secret scanning da plataforma (nota 15) e *push protection*, que recusa o envio |
| **Repositório privado por padrão** | a decisão da nota 05 |

A camada mais eficaz é a primeira: **um segredo que nunca foi escrito em arquivo não pode ser commitado**. Todas as outras são redes para quando a primeira falha.

E vale conhecer o *push protection*: quando ativo, a plataforma **recusa o push** que contém um padrão de credencial conhecido. É a única defesa que age antes de a informação sair da sua máquina.

---

## Casos vizinhos, mesma técnica

O `filter-repo` serve para mais do que segredo:

- **Arquivo gigante que inchou o repositório** (nota 17) — `--strip-blobs-bigger-than 10M`.
- **Dados pessoais** commitados por engano — nome, e-mail, dados de participantes de pesquisa. Aqui há dimensão legal (LGPD), não só técnica.
- **E-mail errado na autoria** de todos os commits — `--email-callback`.
- **Separar um subdiretório em repositório próprio** — `--subdirectory-filter`, preservando o histórico daquele pedaço. Este caso é a nota 29.

---

## Armadilhas comuns

> [!warning] Limpar o histórico e não rotacionar
> **O que acontece:** duas horas de reescrita, todo mundo reclonando, e a chave continua válida — e já copiada.
> **Por quê:** inversão de prioridade por pânico estético.
> **Como evitar:** rotacione **primeiro**. Sempre. Se só der para fazer uma das duas coisas, faça essa.

> [!warning] Rodar `filter-branch` porque foi o que apareceu na busca
> **O que acontece:** a operação demora horas num repositório médio e frequentemente produz resultado incorreto (tags perdidas, refs inconsistentes).
> **Por quê:** é a ferramenta antiga, e a própria documentação do Git desaconselha o uso.
> **Como evitar:** `git filter-repo` ou BFG. A página oficial do `filter-branch` traz o aviso no topo.

> [!warning] Achar que repositório privado é cofre
> **O que acontece:** o segredo vive no repositório privado "porque só o time tem acesso". Um dia o repositório vira público, alguém sai da empresa, ou um integrador ganha acesso de leitura.
> **Por quê:** controle de acesso a repositório não é gestão de segredos — não há rotação, auditoria de uso, nem escopo por ambiente.
> **Como evitar:** segredo mora em cofre, e o repositório referencia o nome, não o valor.

---

## Resumo em uma frase

**Credencial vazada é credencial rotacionada — reescrever o histórico vem depois, é caro, e nunca alcança as cópias que já saíram.**

> [!tip] Vídeo — removendo segredo do histórico
> [**How to Remove Secrets from Git History**](https://www.youtube.com/watch?v=z8tIOYg_oho) (Claudio Bernasconi, 5 min) mostra a limpeza na prática — e vale assistir lembrando que, nesta nota, ela é o **passo 4**, não o primeiro.

> [!tip] Pratique
> Num repositório descartável: commite um arquivo `segredo.txt`, faça mais três commits por cima, e então remova-o com `git filter-repo --invert-paths --path segredo.txt`. Compare `git log --oneline` antes e depois — **todos os hashes mudaram**, e é isso que explica por que todo mundo precisa reclonar.
>
> Depois instale o `gitleaks` como hook de pré-commit e tente commitar uma chave de teste. Ver o commit ser barrado antes de existir é a demonstração de qual camada realmente resolve.

---

## O que vem a seguir

O nível fecha com a nota mais prática de todas: a configuração que faz o Git parar de te atrapalhar. Boa parte do sofrimento dos níveis anteriores — conflito repetido, `push` que precisa de argumento, tag que não vai junto, `status` lento — some com meia dúzia de linhas de configuração.

- **26 — Configurar o Git a seu favor** — aliases, `rerere`, hooks, `.gitattributes` e manutenção.
- [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/06 - Ignorar arquivos - o gitignore e suas regras|06 — Ignorar arquivos]] — onde a promessa "ignorar não é proteger" foi feita, e aqui cumprida.

## Fontes

- **Elijah Newren** — [*git-filter-repo*](https://github.com/newren/git-filter-repo) — a ferramenta recomendada, incluindo `--invert-paths`, `--replace-text` e `--strip-blobs-bigger-than`.
- **Git** — [*git-filter-branch*](https://git-scm.com/docs/git-filter-branch) — o aviso oficial desaconselhando o uso e apontando o `filter-repo`.
- **GitHub Docs** — [*Removing sensitive data from a repository*](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) — o procedimento completo, incluindo a necessidade de contatar o suporte para purgar o cache e o problema dos forks.
- **GitHub Docs** — [*About push protection*](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection) — a recusa de push com credencial detectada.
- **OWASP** — [*Secrets Management Cheat Sheet*](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) — rotação, escopo e por que repositório não é cofre.
