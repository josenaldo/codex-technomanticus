---
title: "Dicionário de Controle de Versão"
created: 2026-07-31
updated: 2026-07-31
type: glossary
status: growing
publish: true
tags:
  - controle-de-versao
  - git
  - github
  - glossary
  - moc
aliases:
  - Glossário de Git
  - Dicionário de Git
---

# Dicionário de Controle de Versão

> Glossário do domínio: os termos que aparecem nos 7 níveis, do vocabulário de sobrevivência ao de forense. Cada verbete diz **o que é** e, quando ajuda, **onde isso morde** — e aponta a nota que trata do assunto a fundo.
>
> Para recursos externos e simuladores, ver a [[03-Dominios/Tecnologia/Controle de Versão/Biblioteca de Controle de Versão|Biblioteca]].

---

## Fundamentos

- **Controle de versão (VCS):** software que mantém a linha do tempo de um projeto, respondendo quatro perguntas sobre cada mudança — *o quê, quem, quando e por quê*. Ver [[03-Dominios/Tecnologia/Controle de Versão/N0 - Sobrevivência/01 - O problema que o Git resolve|01]].
- **Centralizado × distribuído:** no centralizado (CVS, Subversion) o histórico mora num servidor; no distribuído (Git, Mercurial) **cada cópia carrega o histórico completo** — daí funcionar offline e cada clone ser um backup íntegro.
- **Repositório:** uma pasta comum com uma subpasta `.git` dentro, onde vive todo o histórico. Apagar a `.git` descarta o passado e mantém só o presente.
- **Commit:** um registro na linha do tempo — um estado completo do projeto, com autor, data, mensagem e ligação aos pais. Como substantivo é o objeto; como verbo, o ato de criá-lo.
- **Git × GitHub:** Git é o programa que roda na sua máquina; GitHub é um site que hospeda repositórios Git. A relação é a de um arquivo `.docx` com o Google Drive.
- **Clone × download do ZIP:** o ZIP traz o presente; o clone traz **a memória**.

## Os três lugares

- **Diretório de trabalho (*working directory*):** os arquivos que você vê e edita.
- **Área de preparação (*staging area*, *index*, *cache*):** o rascunho do próximo commit. Os três nomes são o mesmo arquivo em papéis diferentes — daí as flags oscilarem entre `--staged` e `--cached`. Ver [[03-Dominios/Tecnologia/Controle de Versão/N3 - O modelo por baixo/20 - O index por dentro|20]].
- **Repositório (banco de objetos):** o histórico permanente, dentro de `.git/objects`.
- **`git add`:** **escreve o blob no banco de objetos** e atualiza a entrada no index. Não é só "marcar" — o conteúdo já entra no repositório aí.
- **Untracked / modified / staged / committed:** os estados do ciclo de vida de um arquivo.

## O modelo interno

- **Objeto:** unidade de armazenamento do Git, imutável e identificada pelo **hash do próprio conteúdo**. Quatro tipos: blob, tree, commit e tag anotada. Ver [[03-Dominios/Tecnologia/Controle de Versão/N3 - O modelo por baixo/17 - Tudo tem hash - o modelo de objetos|17]].
- **Blob:** o conteúdo de um arquivo. Não guarda nome nem permissão — por isso conteúdo idêntico em dois arquivos vira **um só** blob.
- **Tree:** uma pasta — lista de entradas com nome, modo e o hash do blob ou tree correspondente. **É o tree que conhece os nomes.**
- **Endereçamento por conteúdo:** o identificador de um objeto é derivado do que ele contém, com um cabeçalho `<tipo> <tamanho>\0`. Consequência: mudar qualquer coisa produz um objeto novo, e nada é editado no lugar.
- **SHA-1 / SHA-256:** as funções de hash usadas. O Git nasceu em SHA-1 e incorporou **detecção de colisão** desde a versão 2.13; repositórios em SHA-256 existem desde a 2.29, com adoção baixa por interoperabilidade incompleta.
- **DAG (grafo dirigido acíclico):** a forma do histórico. **Dirigido** porque cada commit aponta para seus pais (nunca para os filhos); **acíclico** porque um hash não pode conter a si mesmo. Ver [[03-Dominios/Tecnologia/Controle de Versão/N3 - O modelo por baixo/18 - Commit é snapshot não diff - o DAG|18]].
- **Snapshot × diff:** o Git guarda o estado inteiro a cada commit e **calcula** a diferença quando você pede. Fisicamente, o empacotamento aplica compressão por delta — otimização de armazenamento, não a estrutura da história.
- **Alcançabilidade:** um commit está alcançável se existe um caminho de setas até ele. Para o Git, **existir é ser alcançável a partir de alguma referência** — é a base de `log`, `merge-base`, coleta de lixo e do conceito de órfão.
- **Órfão (*dangling*):** objeto que nenhuma ref alcança mais. Continua no banco; some do `git log`; recuperável pelo [[03-Dominios/Tecnologia/Controle de Versão/N4 - Quando dá errado/23 - reflog - nada se perde de fato|reflog]] até a coleta de lixo.
- **Packfile / `git gc`:** empacotamento periódico de objetos soltos, com compressão entre objetos parecidos.

## Referências e ponteiros

- **Ref:** um nome legível apontando para um hash. Vivem em `.git/refs/` (ou compactadas em `.git/packed-refs`). Ver [[03-Dominios/Tecnologia/Controle de Versão/N3 - O modelo por baixo/19 - Refs HEAD e branch como ponteiro|19]].
- **Branch (ramo):** **um arquivo de texto com 41 bytes** contendo o hash de um commit. Criar é escrever esse arquivo; apagar é removê-lo — e não apaga commit nenhum.
- **`HEAD`:** o arquivo que diz onde você está. Normalmente contém o **nome de uma ref** (`ref: refs/heads/main`) — é essa indireção que faz o commit "empurrar o ramo para frente".
- **`detached HEAD`:** estado em que o `HEAD` contém um hash direto em vez de um nome de ramo. Não é erro; o único risco é que commits feitos ali não pertencem a ramo nenhum.
- **Ramo de rastreamento remoto (`origin/main`):** a **fotografia** do servidor na última sincronização. Só muda com `fetch` ou `pull` — nunca sozinho.
- **`origin`:** convenção de nome para "o servidor principal deste projeto". Não tem nada de especial; um repositório aceita quantos remotos você quiser, inclusive uma pasta num pendrive.
- **Tag leve × anotada:** a leve é só uma ref apontando para o commit; a anotada é um **objeto** com autor, data e mensagem próprios. Para versão publicada, use anotada.
- **`ORIG_HEAD`:** onde o `HEAD` estava antes da última operação grande (merge, rebase, reset). `git reset --hard ORIG_HEAD` desfaz de primeira.
- **`~` × `^`:** `~` anda gerações seguindo sempre o primeiro pai (`HEAD~2`); `^` escolhe **qual** pai num merge (`HEAD^2`).

## Integrar e reescrever

- **Merge:** combina duas linhas criando um commit com **dois pais**, preservando o registro de que houve paralelismo.
- **Three-way merge:** a comparação de **três** pontos — o ancestral comum (base), o seu lado (*ours*) e o outro (*theirs*). Só há conflito quando os dois lados mudaram o mesmo trecho **em relação à base**. Ver [[03-Dominios/Tecnologia/Controle de Versão/N3 - O modelo por baixo/21 - Merge e rebase por dentro|21]].
- **Ancestral comum / *merge base*:** o ponto onde as duas histórias se separaram (`git merge-base`).
- **Fast-forward:** quando a base é o seu próprio commit, não há o que combinar — o Git só **move a ref** para frente. Nenhum objeto novo é criado.
- **Conflito:** o Git recusando-se a escolher entre dois trabalhos legítimos. Não é erro. Ver [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/09 - Conflito - por que acontece e como resolver|09]].
- **`ours` / `theirs`:** os dois lados de um conflito. **Atenção: durante um rebase eles se invertem** — *ours* passa a ser a base sobre a qual você reaplica, e *theirs* são os seus próprios commits.
- **`zdiff3`:** estilo de conflito que mostra também **o que a base dizia**, entre `|||||||`. A configuração mais subestimada do Git.
- **Rebase:** **reconstrói** seus commits sobre outra base, criando objetos novos com hashes novos e deixando os antigos órfãos. Daí a regra de ouro.
- **Regra de ouro:** *antes de publicar, a história é sua e pode ser reescrita; depois de publicar, ela é de todos* — e a correção passa a ser um commit novo (`revert`), não uma alteração do passado.
- **Cherry-pick:** copia a mudança de um commit para outro lugar, criando um commit novo. `-x` anota a origem na mensagem.
- **Estratégia de merge (`ort`):** o algoritmo padrão desde a versão 2.34 (substituiu `recursive`); lida com renomeações, múltiplas bases e conflitos entre arquivo e diretório.
- **`rerere`:** *reuse recorded resolution* — grava como você resolveu um conflito e o reaplica sozinho quando ele reaparecer.

## Desfazer e recuperar

- **`restore` × `reset` × `revert`:** `restore` age em arquivo; `reset` move a ref (e opcionalmente index e disco); `revert` **acrescenta** um commit que desfaz outro. Ver [[03-Dominios/Tecnologia/Controle de Versão/N4 - Quando dá errado/22 - A árvore de decisão do desfazer|22]].
- **`--soft` / `--mixed` / `--hard`:** a mesma operação em três profundidades — ref · ref + index · ref + index + disco. Só o `--hard` perde trabalho.
- **`--amend`:** não edita o commit, **substitui** por um novo (hash diferente). Seguro só antes de publicar.
- **`reflog`:** o diário **local e privado** de todo lugar onde suas refs estiveram. Recupera commit órfão, ramo apagado e `reset --hard` arrependido. Não vai junto no clone.
- **`fsck --lost-found`:** varre o banco procurando objetos inalcançáveis. É o que salva conteúdo que passou por `git add` mas nunca foi commitado.
- **Janela de recuperação:** por padrão, 90 dias para entradas alcançáveis do reflog, **30 dias para inalcançáveis**, 2 semanas para objetos soltos.
- **`--force` × `--force-with-lease` × `--force-if-includes`:** `--force` sobrescreve a ref do servidor incondicionalmente (apaga trabalho alheio); `--force-with-lease` só publica se o servidor ainda estiver onde você o viu; `--force-if-includes` fecha o furo de um `fetch` em segundo plano ter atualizado essa referência sem você ver.
- **`filter-repo`:** ferramenta recomendada para reescrever o histórico inteiro (remover arquivo, segredo ou dividir repositório). Substitui o `filter-branch`, oficialmente desaconselhado.

## Colaboração

- **Pull request (PR) / merge request:** proposta de merge com espaço para revisão, verificação automática e registro da decisão. Ver [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/12 - Pull requests e a cultura de code review|12]].
- **Squash × merge commit × rebase (na integração):** as três formas de fechar um PR. `squash` comprime o ramo num commit; `merge` preserva tudo e cria um commit de junção; `rebase` reaplica sem junção.
- **`nit:`** prefixo convencional para comentário de revisão que é preferência pessoal e **não bloqueia** o merge.
- **GitHub Flow / Git Flow / trunk-based:** as três estratégias de ramificação. O que decide entre elas é **como o software chega ao usuário**, não preferência. Ver [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/13 - Estratégias de branching|13]].
- **Conventional Commits:** formato de mensagem legível por máquina (`feat:`, `fix:`, `feat!:`, `BREAKING CHANGE:`) que permite derivar versão e changelog automaticamente. Sem essa automação, é cerimônia vazia.
- **Semver (`MAJOR.MINOR.PATCH`):** MAJOR quebra compatibilidade, MINOR acrescenta compatível, PATCH corrige compatível.
- **Ruleset / branch protection:** regras aplicadas pelo servidor — exigir PR, aprovações, checks verdes, bloquear force push. É o que transforma acordo em regra executável.
- **`CODEOWNERS`:** arquivo que mapeia caminhos a pessoas ou times, atribuindo revisão automaticamente.
- **`gh`:** o CLI oficial do GitHub. `gh pr checkout` é o comando que transforma revisão de leitura em revisão de execução. Catálogo completo em [[03-Dominios/Tecnologia/Controle de Versão/GitHub CLI|GitHub CLI]].

## Repositórios grandes e compostos

- **Monorepo × polyrepo:** um repositório para vários componentes × um por componente. A pergunta que decide: **quantas mudanças atravessam fronteira de componente por semana?**
- **Clone parcial (`--filter=blob:none`):** baixa a estrutura de commits sem o conteúdo dos arquivos antigos, buscando sob demanda. **Preserva `log`, `blame` e `bisect`.**
- **Clone raso (`--depth=1`):** traz só os commits recentes. Rápido e **amputa a história** — quebra `blame`, `bisect` e `describe`. Legítimo apenas em CI que só compila.
- **Sparse-checkout:** materializa no disco só as pastas que interessam; o repositório continua completo. Use sempre com `--cone`.
- **Git LFS:** guarda binários fora do repositório, deixando ponteiros no lugar. Exige servidor, instalação por todos, e migrar arquivos já commitados é reescrita de histórico.
- **Submódulo:** entrada de modo `160000` (*gitlink*) apontando para o **commit exato de outro repositório**. Preciso e pouco perdoante — o atrito recai sobre quem clona.
- **Subtree:** copia o conteúdo do outro repositório para dentro do seu. O atrito recai sobre quem mantém.
- **`--mirror`:** clone de todas as refs, não só dos ramos. É o backup que se faz **antes** de qualquer cirurgia.
- **`--allow-unrelated-histories`:** exigido para fundir dois repositórios sem ancestral comum.

## Investigação e forense

- **`blame`:** mostra quem tocou cada linha **por último**. Com `-w -C -C` atravessa reformatação e movimentação entre arquivos. Ver [[03-Dominios/Tecnologia/Controle de Versão/N6 - O repositório como testemunha/31 - Ler história de verdade|31]].
- **`.git-blame-ignore-revs`:** arquivo versionado que lista commits a ignorar no `blame` — o remédio para a reformatação em massa que apaga a autoria real.
- **Pickaxe (`log -S`):** encontra os commits onde a **quantidade de ocorrências** de um texto mudou — tipicamente onde ele nasceu e onde morreu. `-G` é a variante por regex sobre o texto do diff: mais abrangente e mais ruidosa.
- **`log -L`:** a evolução de uma função ou faixa de linhas ao longo do tempo.
- **`bisect`:** busca binária no grafo entre um commit bom e um ruim. `bisect run <script>` automatiza; o código de saída **125** significa "não dá para testar este commit, pule". Ver [[03-Dominios/Tecnologia/Controle de Versão/N6 - O repositório como testemunha/32 - bisect - achar o commit que quebrou|32]].
- **Hotspot:** cruzamento de **frequência de mudança × complexidade**. Responde "com orçamento para refatorar 5% do sistema, qual 5%?". Conceito de Adam Tornhill.
- **Acoplamento temporal:** arquivos que mudam sempre juntos, mesmo sem dependência declarada — a evidência mais honesta de acoplamento real, e o achado que detecta duplicação que a análise estática não vê.
- **Ilha de conhecimento / *bus factor*:** área do sistema com autoria concentrada em uma ou poucas pessoas. Risco organizacional, não técnico.
- **`--contains`:** `git tag --contains <hash>` responde em **quais versões publicadas** um commit está — ou seja, quem foi afetado.

## GitOps e automação

- **GitOps:** o repositório como fonte declarativa da verdade sobre o ambiente, com um agente que **puxa** e reconcilia continuamente o que está no ar com o que está commitado. Ver [[03-Dominios/Tecnologia/Controle de Versão/N5 - Repositórios reais/30 - Git no CI-CD e GitOps|30]].
- **Drift:** divergência entre o estado real do ambiente e o estado declarado no repositório. O agente detecta e corrige.
- **`git describe`:** gera um identificador legível a partir da última tag (`v1.2.0-14-ga3f1c9d`). Depende de história e tags disponíveis — e é a primeira vítima do clone raso.
- **Hook:** script executado pelo Git em eventos (`pre-commit`, `commit-msg`, `pre-push`). **Não é versionado** por padrão (decisão de segurança) e é contornável com `--no-verify`: serve para retorno rápido, não para garantia.
- **`.gitattributes`:** arquivo **versionado** que ensina o Git a tratar tipos de arquivo — normalização de fim de linha (`text=auto`), tratamento binário, e `textconv` para gerar diff legível de `.docx` e PDF.

---

## Veja também

- [[03-Dominios/Tecnologia/Controle de Versão/index|Controle de Versão]] — o domínio e os 7 níveis
- [[03-Dominios/Tecnologia/Controle de Versão/Biblioteca de Controle de Versão|Biblioteca de Controle de Versão]] — simuladores, livros e material em português
