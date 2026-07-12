---
title: "Poetry — a alternativa madura"
created: 2026-07-12
type: concept
fase: Adepto
status: seedling
publish: true
tags:
  - python
  - packaging
  - poetry
  - build
aliases:
  - "Poetry"
  - "poetry.lock"
  - "poetry publish"
  - "tool.poetry"
---

# Poetry — a alternativa madura

> [!abstract] TL;DR
> Poetry existe desde 2018 — seis anos antes do `uv` sequer ser anunciado — e resolveu, na época, exatamente o mesmo problema que motiva a adoção de gerenciadores de projeto hoje: um comando único (`poetry`) que cobre dependência, ambiente virtual, lockfile e publicação, em vez de `pip` + `venv` + `twine` como ferramentas separadas que não se falam. A seção `[tool.poetry]` do `pyproject.toml` guarda a configuração; `poetry.lock` trava versões exatas com hash; `poetry build`/`poetry publish` levam um pacote da sua máquina até o PyPI em dois comandos. Esta nota cobre Poetry isoladamente — a comparação direta com `uv` fica para a [[06 - uv vs Poetry — trade-offs honestos|nota 06]].

## Um time que adotou Poetry em 2019 e nunca teve motivo forte pra sair

O time de Plataforma de uma fintech de médio porte migrou seu serviço de cobrança para Poetry em 2019. Na época, a escolha não foi óbvia por acaso — era, literalmente, a alternativa mais madura disponível: `pipenv` estava perdendo tração por lentidão de resolução de dependências, `setup.py` ainda era o jeito "oficial" de empacotar, e a PEP 621 (que padronizaria `[project]` no `pyproject.toml`) nem tinha sido escrita ainda. Poetry já entregava, em 2018, o que a maioria dos times só teria de novo com `uv` seis anos depois: lockfile determinístico, resolução de dependências consistente, um comando pra cada etapa do ciclo de vida do pacote.

Sete anos depois, o serviço de cobrança ainda roda Poetry. Ninguém no time considera isso um problema a resolver. O onboarding de gente nova leva vinte minutos (`poetry install` e pronto), o CI é estável, o lockfile nunca causou uma build não-reprodutível, e a última vez que alguém propôs migrar para `uv` — atraído pela velocidade — a resposta do tech lead foi direta: "quanto tempo o `poetry install` leva hoje?" Quinze segundos, com cache quente. "E quanto isso está custando pra gente, em minutos de CI por semana?" Praticamente nada, porque o CI já cacheia o `.venv` entre runs. A migração teria custo real (reescrever scripts de CI, revalidar o lockfile, treinar o time num fluxo novo) para um ganho que, nesse projeto específico, não movia nenhum indicador que importasse.

> [!tip] "Mais rápido" não é sinônimo de "vale migrar"
> Este é o ponto central desta nota, e vale antecipá-lo: Poetry continua sendo uma escolha legítima em 2026 não porque seja tecnicamente superior a `uv` em algum eixo — na maioria dos benchmarks, não é — mas porque a decisão de trocar ferramenta de build num projeto maduro em produção precisa justificar o custo da migração, não só apontar um número menor num benchmark. A [[06 - uv vs Poetry — trade-offs honestos|nota 06]] desenvolve esse raciocínio a fundo; aqui, o ponto é só reconhecer que a pergunta "por que esse time ainda usa Poetry?" quase sempre tem uma resposta racional, não uma de inércia.

Esta nota cobre Poetry como ferramenta — os comandos, o fluxo, o que ele resolve — sem comparar linha a linha com `uv` (isso é assunto da nota seguinte). A [[03 - pyproject.toml — o padrão unificado|nota 03]] já cobriu a estrutura geral do `pyproject.toml` (`[build-system]`, `[project]`, `[tool.*]`); aqui o foco é só na seção que Poetry usa e nos comandos que ele expõe.

## `[tool.poetry]`: a seção que Poetry lê

Poetry adota o `pyproject.toml` como manifesto único, igual qualquer ferramenta moderna do ecossistema — mas, por ter nascido antes da PEP 621 (2020), historicamente usava sua própria seção `[tool.poetry]` para metadados, em vez do `[project]` padronizado depois pela PEP. Isso mudou nas versões recentes: desde a série 2.0 (lançada no fim de 2024), Poetry suporta nativamente a seção `[project]` padrão da PEP 621 como fonte de metadados, com `[tool.poetry]` reservado só para configuração específica de Poetry (fontes de pacote alternativas, grupos de dependência, scripts). Um projeto criado hoje com `poetry init` já gera `[project]` por padrão; projetos legados de antes de 2025 ainda concentram tudo em `[tool.poetry]`.

```toml
# pyproject.toml — projeto Poetry moderno (2.0+), estilo PEP 621
[project]
name = "servico-cobranca"
version = "3.4.0"
description = "Serviço de cobrança recorrente — API REST"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115,<1.0",
    "sqlalchemy>=2.0",
    "httpx>=0.27",
]

[tool.poetry]
packages = [{ include = "servico_cobranca" }]

[tool.poetry.group.dev.dependencies]
pytest = "^8.3"
ruff = "^0.7"

[build-system]
requires = ["poetry-core>=2.0"]
build-backend = "poetry.core.masonry.api"
```

Repare no `build-backend`: `poetry.core.masonry.api` é o backend de build próprio do Poetry — a peça que a [[03 - pyproject.toml — o padrão unificado|nota 03]] descreveu, na tabela de backends comuns, como uma das opções junto de `setuptools.build_meta` e `hatchling`. É esse backend que sabe transformar o código-fonte em wheel/sdist quando você roda `poetry build`.

> [!question]- E projetos legados que ainda usam só `[tool.poetry]` para tudo (nome, versão, dependências)?
> Continuam funcionando — Poetry 2.x mantém retrocompatibilidade total com o formato antigo, onde `[tool.poetry]` concentra `name`, `version`, `description`, `authors` e `dependencies` (esta última numa sintaxe própria, `[tool.poetry.dependencies]`, diferente da lista `dependencies = [...]` da PEP 621). Migrar um projeto legado para `[project]` é opcional, não obrigatório — a diferença prática é cosmética na maioria dos casos, mas projetos novos devem preferir `[project]` porque é o formato que qualquer outra ferramenta do ecossistema (não só Poetry) sabe ler sem tradução.

## `poetry init`: criando o projeto

Um projeto novo começa com `poetry init`, que faz uma série de perguntas interativas (nome, versão, descrição, autor, licença, dependências) e gera o `pyproject.toml` a partir das respostas:

```bash
$ poetry init

This command will guide you through creating your pyproject.toml config.

Package name [servico-notificacoes]:
Version [0.1.0]:
Description []:  Serviço de notificações — consumidor de fila
Author [Time de Plataforma <plataforma@empresa.dev>, n to skip]:
License []:  MIT
Compatible Python versions [>=3.12]:

Would you like to define your main dependencies interactively? (yes/no) [yes]
...
```

Para automação (CI, scripts, geração de projeto a partir de template), o modo interativo pode ser pulado com `--no-interaction`, aceitando os valores padrão ou passados via flag:

```bash
poetry init --no-interaction --name servico-notificacoes --python ">=3.12"
```

Diferente de `uv init` (que a [[04 - uv — o gerenciador moderno|nota 04]] cobre), `poetry init` não cria a estrutura de diretórios do projeto sozinho por padrão — ele assume que você já está numa pasta com código, e só gera o manifesto. Para começar um projeto do zero com estrutura de pastas incluída, o comando é `poetry new nome-do-projeto`, que cria `src/`, `tests/` e o `pyproject.toml` de uma vez.

## Gerenciando dependências: `add`, `remove` e groups

O dia a dia de um projeto Poetry gira em torno de `poetry add` e `poetry remove` — cada um atualiza o `pyproject.toml` **e** o `poetry.lock` na mesma operação, sem exigir um passo manual de sincronização.

```bash
# adiciona uma dependência de produção
poetry add fastapi

# adiciona com faixa de versão específica
poetry add "sqlalchemy>=2.0,<3.0"

# adiciona uma dependência de desenvolvimento a um grupo nomeado
poetry add --group dev pytest ruff

# remove uma dependência (some do pyproject.toml e do lockfile)
poetry remove httpx
```

O que `poetry add fastapi` faz, por trás do comando único: resolve a versão mais recente compatível com as restrições já declaradas no projeto, escreve a entrada em `[project.dependencies]` (ou `[tool.poetry.dependencies]`, no formato legado), atualiza o `poetry.lock` com a resolução completa do grafo de dependências (incluindo transitivas, com hash), e — se houver um `.venv` ativo gerenciado pelo Poetry — instala o pacote nesse ambiente. Um comando, quatro efeitos coordenados.

### Groups: separando dependências por propósito

A seção `[tool.poetry.group.<nome>.dependencies]` organiza dependências por contexto de uso, sem misturar tudo numa lista só nem exigir um `requirements-dev.txt` separado (o problema que a [[01 - Panorama — por que packaging Python era confuso|nota 01]] descreveu como sintoma da fragmentação pré-`pyproject.toml`):

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^8.3"
pytest-cov = "^6.0"
ruff = "^0.7"
mypy = "^1.13"

[tool.poetry.group.docs.dependencies]
mkdocs = "^1.6"
mkdocs-material = "^9.5"
```

Cada grupo é opcional na instalação — `poetry install` instala todos os grupos por padrão, mas `poetry install --only main` instala só as dependências de produção (sem `dev`, sem `docs`), útil para uma imagem Docker de produção que não precisa de `pytest` nem `mkdocs`:

```bash
# instala tudo, incluindo todos os grupos
poetry install

# instala só dependências de produção — típico de Dockerfile
poetry install --only main

# instala produção + um grupo específico
poetry install --with docs
```

> [!tip] Groups existem desde a versão 1.2 (2022)
> Antes disso, Poetry só tinha a distinção binária `dependencies`/`dev-dependencies`, sem grupos nomeados arbitrários. Um projeto legado que você encontrar com `[tool.poetry.dev-dependencies]` (sem `.group.`) está usando a sintaxe pré-1.2 — ainda funciona, mas é considerada obsoleta; a migração para `[tool.poetry.group.dev.dependencies]` é mecânica.

## `poetry install` e `poetry lock`: o lockfile em ação

`poetry install` é o comando que um dev novo roda no primeiro dia, ou que o CI roda em cada pipeline: lê o `poetry.lock` (não o `pyproject.toml` diretamente) e instala exatamente as versões ali travadas, com hash de integridade verificado por artefato.

```bash
$ poetry install
Installing dependencies from lock file

Package operations: 24 installs, 0 updates, 0 removals

  • Installing certifi (2024.2.2)
  • Installing charset-normalizer (3.3.2)
  • Installing idna (3.6)
  ...
  • Installing fastapi (0.115.6)
  • Installing sqlalchemy (2.0.36)

Installing the current project: servico-cobranca (3.4.0)
```

Se o `poetry.lock` não existir ainda (primeiro `poetry install` de um projeto novo, ou depois de editar `pyproject.toml` manualmente), Poetry primeiro resolve o grafo de dependências e gera o lockfile, depois instala a partir dele. O comando explícito para só regenerar o lockfile, sem instalar nada, é `poetry lock`:

```bash
# regenera o lockfile a partir do pyproject.toml, sem instalar
poetry lock

# regenera e sobrescreve versões já travadas, buscando as mais recentes compatíveis
poetry lock --regenerate
```

> [!warning] `poetry.lock` precisa estar versionado no Git
> Assim como `uv.lock`, o `poetry.lock` só cumpre seu papel de reprodutibilidade se for commitado junto do código — é ele, não o `pyproject.toml`, que garante que a mesma árvore exata de dependências (incluindo transitivas) seja instalada em qualquer máquina, em qualquer momento. Um erro comum, especialmente vindo de quem tratava `.lock` como "arquivo gerado, não precisa versionar" (um hábito de outras stacks onde lockfiles são artefato de build): sem o `poetry.lock` no repositório, cada `poetry install` re-resolve o grafo do zero, e duas máquinas podem legitimamente chegar a resoluções diferentes se uma dependência publicou uma versão nova entre as duas instalações.

O comando `poetry check` audita se o `pyproject.toml` e o `poetry.lock` estão consistentes entre si — útil como gate de CI, pra pegar o caso em que alguém editou dependências manualmente no `pyproject.toml` e esqueceu de rodar `poetry lock` depois:

```bash
poetry check --lock
# Error: pyproject.toml changed significantly since poetry.lock was last generated.
# Run `poetry lock` to fix the lock file.
```

## Ambiente virtual: `poetry shell` e `poetry run`

Poetry gerencia um virtual environment por projeto automaticamente — por padrão, cria um `.venv` fora do diretório do projeto (num diretório de cache central), embora a configuração `virtualenvs.in-project = true` (comum em times que querem o `.venv` visível na raiz do repositório, para o editor detectar sem configuração extra) mude esse comportamento:

```bash
# configura o Poetry pra criar o .venv dentro do projeto (recomendado por muitos times)
poetry config virtualenvs.in-project true
```

Dois jeitos de rodar comandos dentro desse ambiente, sem ativar manualmente com `source .venv/bin/activate`:

```bash
# executa um comando único dentro do venv gerenciado
poetry run pytest
poetry run python script.py
poetry run uvicorn app.main:app --reload

# abre um shell interativo já com o venv ativo (histórico: comando nativo até a 1.x)
poetry shell
```

> [!question]- `poetry shell` ainda existe em 2026?
> Depende da versão. A partir do Poetry 2.0 (dezembro de 2024), `poetry shell` deixou de ser um comando nativo e virou um plugin opcional (`poetry-plugin-shell`), instalável com `poetry self add poetry-plugin-shell`. A motivação foi reduzir a superfície do core do Poetry — `poetry shell` dependia de spawnar um subshell, o que causava comportamento inconsistente entre sistemas operacionais e terminais. `poetry run <comando>` continua nativo e é o caminho recomendado para a maioria dos casos (rodar um comando pontual); só quem realmente precisa de um shell persistente dentro do venv instala o plugin.

Isso é conceitualmente o mesmo padrão de gerenciamento automático de venv que `uv venv`/`uv run` oferece (coberto na [[04 - uv — o gerenciador moderno|nota 04]]) — a diferença não é o modelo, é o tempo de maturidade: Poetry vem gerenciando venv por projeto dessa forma desde 2018, com anos a mais de casos de borda resolvidos (comportamento em Windows, interação com `pyenv`, múltiplas versões de Python instaladas na mesma máquina).

## `poetry build` e `poetry publish`: do código ao PyPI

Aqui está o fluxo que muitos tutoriais recentes de `uv` ainda cobrem de forma incompleta, simplesmente porque o suporte a publicação no `uv` é mais novo — Poetry tem esse par de comandos maduro e estável desde as primeiras versões públicas.

`poetry build` gera os dois artefatos de distribuição padrão do ecossistema Python — o wheel (`.whl`, formato binário pré-construído, mais rápido de instalar) e a sdist (`.tar.gz`, distribuição de código-fonte, usada quando não existe wheel compatível com a plataforma de quem instala):

```bash
$ poetry build

Building servico-cobranca (3.4.0)
  - Building sdist
  - Built servico_cobranca-3.4.0.tar.gz
  - Building wheel
  - Built servico_cobranca-3.4.0-py3-none-any.whl
```

Os artefatos vão para `dist/` na raiz do projeto. `poetry publish` os envia para um índice de pacotes — por padrão, o PyPI:

```bash
# publica no PyPI (pede confirmação de credenciais se não configuradas)
poetry publish

# build + publish num comando só
poetry publish --build
```

Autenticação usa um token de API do PyPI, configurado uma vez por máquina (não versionado, não commitado):

```bash
poetry config pypi-token.pypi "pypi-AgEIcHlwaS5vcmc..."
```

Para publicar num índice privado (um registry interno da empresa, por exemplo Artifactory ou um PyPI self-hosted), Poetry suporta declarar repositórios nomeados no `pyproject.toml` e publicar explicitamente nesse alvo:

```toml
[[tool.poetry.source]]
name = "empresa-privado"
url = "https://pypi.empresa.dev/simple/"
priority = "explicit"
```

```bash
poetry config repositories.empresa-privado https://pypi.empresa.dev/legacy/
poetry config http-basic.empresa-privado usuario senha
poetry publish --repository empresa-privado
```

> [!warning] `poetry publish` sem `--dry-run` é irreversível
> O PyPI não permite reupload de uma versão já publicada — nem para corrigir um typo na descrição. Uma vez que `servico-cobranca==3.4.0` foi publicado, esse número de versão está queimado para sempre; a correção é publicar `3.4.1`. O comando aceita `--dry-run` para validar o pacote (metadados, se o build está correto) sem de fato enviar nada — vale rodar isso no CI antes do `publish` de verdade, especialmente na primeira vez que alguém configura o pipeline de release de um pacote novo.

## O fluxo completo, em um diagrama

```mermaid
flowchart LR
    A["poetry add fastapi"] --> B["pyproject.toml atualizado<br/>+ poetry.lock atualizado"]
    B --> C["poetry install<br/>(lê poetry.lock)"]
    C --> D[".venv populado<br/>com versões travadas"]
    D --> E["poetry run pytest<br/>(dev/CI)"]
    E --> F["poetry build<br/>gera .whl + .tar.gz"]
    F --> G["poetry publish<br/>envia ao PyPI"]

    style A fill:#4A90D9,color:#fff
    style G fill:#2E7D32,color:#fff
```

Cada seta é reversível ou reexecutável sem efeito colateral perigoso — exceto a última. `poetry add` pode ser desfeito com `poetry remove`; `poetry lock` pode ser regenerado; `poetry install` pode ser rodado quantas vezes for preciso. `poetry publish`, como já visto, não.

## Armadilhas

### (1) Achar que `poetry install` também atualiza dependências

`poetry install` instala exatamente o que está no `poetry.lock` — não busca versões mais novas, mesmo que existam e sejam compatíveis com as faixas declaradas em `pyproject.toml`. Quem quer atualizar dependências precisa de `poetry update` (que re-resolve o grafo, respeitando as faixas declaradas, e regrava o lockfile) ou `poetry add pacote@latest` para uma dependência específica.

Exemplo: um dev roda `poetry install` esperando pegar a correção de segurança que acabou de sair para uma biblioteca — mas `poetry install` só respeita o que já está travado. A correção só entra com `poetry update nome-do-pacote`.

Fix: separar mentalmente os dois comandos — `poetry install` é "reproduzir o que já foi decidido", `poetry update` é "decidir de novo, dentro das faixas permitidas".

### (2) Misturar `pip install` e Poetry no mesmo projeto

Rodar `pip install algum-pacote` dentro de um venv gerenciado pelo Poetry instala o pacote no ambiente, mas não atualiza `pyproject.toml` nem `poetry.lock` — o pacote fica "invisível" para qualquer outra máquina que rode `poetry install`, porque o lockfile nunca soube da sua existência.

Exemplo: alguém faz `pip install ipdb` pra debugar localmente, esquece de remover, e um script no projeto passa a depender dele sem que isso apareça em nenhum manifesto — o CI, que sempre roda `poetry install` a partir de um venv limpo, falha com `ModuleNotFoundError` na primeira vez que alguém tenta rodar esse script fora da máquina de quem instalou.

Fix: tudo que precisa estar disponível de forma consistente no projeto passa por `poetry add` (mesmo que temporariamente, com `--group dev`), nunca por `pip install` direto dentro do venv do Poetry.

### (3) Publicar sem checar se o pacote já existe na versão atual

Como visto no callout de aviso acima, uma versão publicada no PyPI é permanente. É comum, em pipelines de release automatizados mal configurados, um CI tentar publicar a mesma versão duas vezes (por exemplo, um workflow que roda em cada push para `main`, sem checar se a versão em `pyproject.toml` já mudou desde o último release).

Fix: o CI de publicação deve comparar a versão declarada no `pyproject.toml` contra o que já está publicado (via `poetry publish --dry-run` como checagem, ou consultando a API do PyPI) antes de tentar o `publish` de verdade — e falhar de forma clara, não silenciosa, se a versão já existir.

## Em entrevista

### Frase pronta (inglês)

> Poetry has been a mature Python project manager since 2018 — years before `uv` existed — and it's still a legitimate choice today, not out of inertia but because migrating a stable production project to a faster tool has a real cost that needs to justify itself. It manages dependencies, a project-scoped virtualenv, and a deterministic `poetry.lock` through one CLI, and its `poetry build`/`poetry publish` workflow for shipping a package to PyPI is more battle-tested than most alternatives, simply because it's had more years in production. Dependency groups (`[tool.poetry.group.dev.dependencies]`) let a project separate production, dev, and docs dependencies cleanly, and `poetry install --only main` installs just the production set — useful for a lean Docker image.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| Gerenciador de projeto | Project manager |
| Arquivo de bloqueio | Lockfile |
| Grupo de dependências | Dependency group |
| Ambiente virtual gerenciado | Managed virtual environment |
| Construir o pacote | Build the package |
| Publicar no índice | Publish to the index |
| Token de API | API token |
| Índice privado | Private index |

## Síntese

Poetry não é "a ferramenta antiga que ainda não foi substituída" — é a ferramenta que resolveu, com anos de antecedência, o mesmo problema estrutural que motiva a adoção de `uv` hoje: um comando único cobrindo dependência, ambiente e publicação, apoiado num lockfile determinístico. O que Poetry tem, e um gerenciador mais novo não tem por definição, é tempo de produção: casos de borda resolvidos, comportamento estável em Windows/Linux/macOS, um ecossistema de plugins maduro, e times inteiros que já internalizaram o fluxo. Migrar um projeto estável dessas para outra ferramenta só porque ela é mais rápida é uma troca que precisa justificar seu próprio custo — e nem sempre justifica. A [[06 - uv vs Poetry — trade-offs honestos|nota 06]] pega esse raciocínio e coloca os dois lado a lado, com números.

## Fontes

- [Poetry — Documentation](https://python-poetry.org/docs/), consultado em 2026-07-12.
- [Poetry — Dependency specification](https://python-poetry.org/docs/dependency-specification/), consultado em 2026-07-12.
- [Poetry — Managing dependencies (groups)](https://python-poetry.org/docs/managing-dependencies/), consultado em 2026-07-12.
- [Poetry — Libraries (build/publish workflow)](https://python-poetry.org/docs/libraries/), consultado em 2026-07-12.
- [Poetry — CLI reference](https://python-poetry.org/docs/cli/), consultado em 2026-07-12.
- [Poetry 2.0 release notes — python-poetry/poetry, GitHub](https://github.com/python-poetry/poetry/releases), consultado em 2026-07-12.
