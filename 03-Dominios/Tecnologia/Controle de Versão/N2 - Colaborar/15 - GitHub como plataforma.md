---
title: "GitHub como plataforma"
created: 2026-07-31
updated: 2026-07-31
type: concept
status: seedling
fase: Adepto
tags:
  - controle-de-versao
  - git
  - github
  - tecnologia
publish: true
---

# GitHub como plataforma

> [!abstract] TL;DR
> Tudo o que o nível 2 acordou até aqui — revisar antes de integrar, CI verde, quem aprova o quê — depende de boa vontade enquanto não estiver configurado. As **regras de proteção da branch** (hoje, *rulesets*) transformam acordo em regra que o servidor aplica. Em volta disso, a plataforma oferece rastreamento de trabalho (issues, projects), automação (Actions), delegação de revisão (CODEOWNERS) e uma camada de segurança (Dependabot, secret scanning) que vale ligar no primeiro dia.

---

## O limite do Git

O Git não sabe o que é um pull request. Não sabe o que é uma issue, uma revisão aprovada ou um teste que precisa passar. Ele guarda commits e move ponteiros — e é bom nisso justamente por não opinar sobre processo.

Tudo o que este nível descreveu como prática de equipe vive **na plataforma**, não no Git. É por isso que trocar de GitHub para GitLab leva o repositório junto sem esforço, mas leva as regras de processo a serem reconfiguradas.

Vale a distinção porque ela orienta o que aprender com profundidade (o Git, que é estável há vinte anos) e o que aprender pela documentação atual (a plataforma, que muda de nome de funcionalidade todo ano).

---

## O que faz diferença de verdade: proteger a linha principal

Sem proteção, qualquer pessoa com acesso de escrita pode empurrar direto para a `main`, ignorar revisão, ou reescrever o histórico compartilhado. O processo inteiro do nível 2 depende de uma configuração.

No GitHub, a forma atual são os **rulesets** (a antiga *branch protection* continua funcionando, e muitos projetos ainda a usam). As regras que importam:

| Regra | O que impede |
|---|---|
| **Exigir PR antes do merge** | push direto na `main` |
| **Exigir N aprovações** | integrar sem ninguém ler |
| **Descartar aprovações a cada novo push** | aprovar uma versão e mergear outra |
| **Exigir checks de status** | integrar com teste vermelho |
| **Exigir branch atualizada** | integrar código que nunca foi testado junto com a `main` atual |
| **Bloquear force push** | reescrever a história compartilhada |
| **Bloquear deleção** | apagar a `main` por engano |
| **Exigir resolução de comentários** | mergear deixando conversa aberta |

> [!info] Comece por três
> Para um repositório qualquer, três regras entregam quase todo o benefício: **PR obrigatório**, **1 aprovação** e **checks obrigatórios**. As demais resolvem problemas que você ainda não tem — e regra demais no começo gera contorno, não disciplina.
> Um detalhe que morde: por padrão, administradores costumam ficar **isentos**. Isso é razoável para emergência e péssimo como rotina — se a regra não vale para quem mais empurra código, ela não vale.

---

## CODEOWNERS: quem precisa aprovar o quê

Um arquivo `.github/CODEOWNERS` mapeia caminhos a pessoas ou times:

```text
# padrão para tudo
*                     @time-plataforma

# áreas com dono específico
/infra/               @time-infra
/src/pagamentos/      @ana @bruno
*.sql                 @time-dados
```

Quem abre um PR que toca `/src/pagamentos/` recebe automaticamente Ana e Bruno como revisores. Combinado com a regra "exigir revisão de code owner", isso deixa de ser sugestão.

É a ferramenta certa para áreas onde uma mudança errada custa caro (migração de banco, infraestrutura, autenticação). Usada demais, vira gargalo — todo PR esperando a mesma pessoa.

---

## Rastrear o trabalho: issues, labels e projects

- **Issues** são unidades de trabalho ou problema. O valor real está na ligação com o código: escrever `Closes #482` na descrição de um PR fecha a issue automaticamente no merge, e cria o vínculo permanente entre "o que se pediu" e "o que se fez".
- **Labels** classificam (`bug`, `boa-primeira-tarefa`, `precisa-de-decisão`). Poucas e com significado acordado; vinte labels que ninguém filtra são ruído.
- **Milestones** agrupam por entrega.
- **Projects** são quadros e tabelas que enxergam issues e PRs de vários repositórios, com campos próprios (prioridade, estimativa, iteração).
- **Templates** de issue e de PR (em `.github/`) capturam de saída a informação que o time sempre precisa pedir depois — versão, passos para reproduzir, o que o revisor deve olhar.

Para trabalho acadêmico e projetos pequenos, issues funcionam muito bem como lista de pendências vinculada ao texto: *"revisar a seção 3.2 após retorno da banca"* vira uma issue, e o commit que resolve a fecha.

---

## Actions: o que o repositório contrata

**GitHub Actions** executa fluxos de trabalho em resposta a eventos do repositório — abriu PR, empurrou commit, criou tag. É o que faz aparecer o "verde" que a regra de proteção exige.

```yaml
name: CI
on: [push, pull_request]
jobs:
  testes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
```

O que importa **para este domínio** é o contrato entre repositório e pipeline: que eventos disparam o quê, o que o `checkout` traz (por padrão, um clone raso, e isso quebra ferramentas que precisam do histórico completo), que permissões o token do fluxo recebe, e como uma tag vira release.

O resto — desenhar pipeline, estratégias de deploy, ambientes, promoção entre estágios — é disciplina de entrega e mora em [[03-Dominios/Engenharia/Operação/index|Engenharia/Operação]]. Este domínio para na fronteira, e a nota 30 (nível 5) fecha o que sobra do lado do repositório.

> [!warning] Permissão do token do workflow
> **O que acontece:** um fluxo de trabalho com permissões amplas é explorado por uma dependência comprometida ou por um PR vindo de fork.
> **Por quê:** o token que o Actions injeta pode ter escrita no repositório, e ações de terceiros rodam com ele.
> **Como evitar:** permissão mínima explícita (`permissions:` no topo do fluxo), ações de terceiros fixadas por commit em vez de tag móvel, e cuidado redobrado com o evento `pull_request_target`, que roda com permissões elevadas em código de fora.

---

## Segurança do repositório — ligue no primeiro dia

Três recursos que custam um clique e evitam problemas caros:

- **Secret scanning** — detecta credenciais commitadas e alerta (e, para muitos provedores, notifica o emissor para revogar). Não substitui a regra de ouro: **credencial vazada é credencial rotacionada**, o que já vimos na nota 06 e volta com todo o mecanismo na nota 25.
- **Dependabot** — abre PRs de atualização de dependências vulneráveis. Ligue os alertas mesmo que não ligue as atualizações automáticas.
- **Code scanning** — análise estática em cada PR.

E o básico de governança: quem tem acesso de escrita, se a organização exige 2FA, e o que acontece quando alguém sai do time.

---

## Os arquivos que o GitHub trata de forma especial

Alguns nomes de arquivo ganham comportamento próprio na interface:

| Arquivo | Efeito |
|---|---|
| `README.md` | exibido na página inicial do repositório |
| `LICENSE` | reconhecida e exibida como licença do projeto |
| `CONTRIBUTING.md` | linkado ao abrir issue ou PR |
| `CODE_OF_CONDUCT.md` | idem |
| `SECURITY.md` | como relatar vulnerabilidade |
| `CODEOWNERS` | revisão automática por área |
| `CITATION.cff` | gera o botão **"Cite this repository"** |
| `.github/ISSUE_TEMPLATE/` | formulários de abertura de issue |

O `CITATION.cff` merece destaque para quem publica pesquisa: ele faz o GitHub exibir a forma correta de citar o repositório, em BibTeX e APA. Combinado com o DOI do Zenodo (nota 05), fecha o ciclo de material citável.

---

## Armadilhas comuns

> [!warning] Confiar que "está protegido" sem testar
> **O que acontece:** a regra foi criada com um padrão de nome que não casa com a branch real (`main` × `master`, ou um padrão com asterisco no lugar errado), e ninguém percebe até alguém empurrar direto.
> **Por quê:** regras casam por padrão de nome, e a interface não avisa que o padrão não pegou nada.
> **Como evitar:** teste. Tente empurrar direto na `main` e confirme que é recusado. Um minuto de verificação vale mais que a tela de configuração toda verde.

> [!warning] Automatizar processo antes de acordá-lo
> **O que acontece:** o time liga exigência de duas aprovações num time de três pessoas, e tudo trava.
> **Por quê:** a regra codifica um acordo que não existia; o resultado é contorno (aprovações automáticas de cortesia) em vez de qualidade.
> **Como evitar:** acorde primeiro, verifique que funciona por hábito, e só então torne obrigatório. Regra existe para impedir o esquecimento, não para criar disciplina do zero.

> [!warning] Tornar público o que não deveria
> **O que acontece:** um repositório interno vira público numa arrumação de organização, com histórico inteiro exposto.
> **Por quê:** a mudança de visibilidade é uma configuração simples, sem etapa de revisão por padrão.
> **Como evitar:** em organização, restrinja quem pode alterar visibilidade. E lembre da nota 05: tornar público é irreversível na prática, porque o que foi lido não volta.

---

## Resumo em uma frase

**O Git guarda a história; a plataforma guarda o processo — e processo que não está configurado é só uma intenção.**

> [!tip] Pratique
> Num repositório de teste seu: crie um ruleset exigindo PR e um check de status, e então **tente** empurrar direto na `main`. Ver a recusa acontecer é o que dá confiança de que a configuração está fazendo efeito.
>
> Depois adicione um `CODEOWNERS` com você mesmo como dono de uma pasta, abra um PR que a toque, e confirme que a revisão foi pedida automaticamente. O curso *Introduction to GitHub* e os de Actions no **[GitHub Skills](https://skills.github.com/)** cobrem esse terreno com correção automática.

---

## O que vem a seguir

Você configurou o processo pela interface. A última nota do nível traz tudo isso para o terminal: abrir PR, revisar, mergear, acompanhar a CI e consultar o que não tem comando pronto — sem trocar de janela.

- **16 — `gh` CLI e automação do fluxo** — o `gh`, o `gh api`, e o que dá para automatizar.
- [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/12 - Pull requests e a cultura de code review|12 — Pull requests]] — o processo que estas regras tornam obrigatório.

## Fontes

- **GitHub Docs** — [*About rulesets*](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) — o modelo atual de proteção de branch e sua relação com as regras antigas.
- **GitHub Docs** — [*About code owners*](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) — sintaxe do `CODEOWNERS` e precedência das regras.
- **GitHub Docs** — [*Security hardening for GitHub Actions*](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) — permissões do token, fixação de ações por commit e o risco do `pull_request_target`.
- **GitHub Docs** — [*About citation files*](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files) — o `CITATION.cff` e o botão de citação.
