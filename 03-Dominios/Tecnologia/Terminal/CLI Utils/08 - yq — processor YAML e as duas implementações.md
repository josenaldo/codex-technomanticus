---
title: "yq — processor YAML e as duas implementações"
created: 2026-05-22
updated: 2026-05-22
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - terminal
  - cli-utils
  - adepto
  - yq
  - yaml
aliases:
  - yq
  - yq Go
  - yq Python
---

> [!abstract] TL;DR
> yq processa YAML/JSON/XML — mas existem **duas implementações populares com sintaxe diferente**: Mike Farah (Go, default em Homebrew) e kislyuk (Python, wrappa jq). Confundir as duas é o footgun central — exemplos da web frequentemente não rodam por serem da outra impl. Detectar versão: `yq --version`. Receita segura pra Go: usar sintaxe própria. Pra Python: sintaxe = jq mas operando em YAML.

## O que é / Como funciona

### As duas implementações

Existem duas ferramentas independentes, ambas chamadas `yq`, com histórico, mantedores e sintaxe distintos:

| Aspecto | yq (Go) — Mike Farah | yq (Python) — kislyuk |
|---|---|---|
| Linguagem | Go | Python (wrappa jq nativo) |
| Default install | Homebrew, snap | pip, apt em Debian/Ubuntu |
| Sintaxe | Própria, estilo jq mas ≠ | Idêntica a jq |
| In-place edit | `yq -i '.foo = "bar"' file.yaml` | não nativo (script) |
| Multi-doc | `yq eval-all` | menos completo |
| Preservação comments | sim (em casos) | não |
| Anchors/aliases YAML | expandidos por default | comportamento custom |

### Detectar qual está instalado

`yq --version` é o detector canônico:

- **yq Go**: imprime `yq (https://github.com/mikefarah/yq/) version v4.x.x` — note o `v` antes do número.
- **yq Python**: imprime `yq 3.x.x` — sem `v`, sem URL.

Se a versão difere entre máquinas, as receitas podem falhar silenciosamente.

### Sintaxe yq (Go) — exemplos canônicos

```bash
# Ler campo aninhado
yq '.spec.template.spec.containers[0].image' deployment.yaml

# Editar in-place (nativo)
yq -i '.image = "nginx:latest"' file.yaml

# Converter YAML → JSON
yq -o json file.yaml

# Merge multi-doc (eval-all processa todos os docs)
yq eval-all '. as $item ireduce ({}; . * $item)' *.yaml

# Append a lista
yq '.items += ["novo"]' file.yaml
```

### Sintaxe yq (Python) — exemplos canônicos

```bash
# Ler campo (output default = JSON)
yq '.spec.template.spec.containers[0].image' deployment.yaml

# Ler campo com output YAML (flag -y obrigatória)
yq -y '.spec' deployment.yaml

# Editar e salvar (não tem -i nativo; usa tmp file)
yq -y '.image = "nginx:latest"' file.yaml > tmp && mv tmp file.yaml
```

### Conversão YAML ↔ JSON para usar com jq (Go)

yq Go converte YAML para JSON e então você usa jq normalmente:

```bash
yq -o json values.yaml | jq '.global.image'
```

### Multi-doc (`---`)

YAML multi-doc separa documentos com `---`. Comportamento de cada impl:

```yaml
# file.yaml com dois documentos
---
name: alpha
---
name: beta
```

- **yq Go**: `yq '.name' file.yaml` retorna os dois valores, um por linha. Para merge: `yq eval-all`.
- **yq Python**: comportamento varia; pode precisar de `--slurp` pra agregar em array antes de filtrar.

## Na prática

### Receitas Go (Mike Farah)

```bash
# Listar todas as imagens num deploy k8s
yq '.spec.template.spec.containers[].image' k8s/deploy.yaml

# Atualizar versão da imagem in-place
yq -i '.image = "myapp:v2.3.0"' deploy.yaml

# Merge kustomize-style: overlay sobrescreve base
yq eval-all '. as $item ireduce ({}; . * $item)' base.yaml overlay.yaml

# Comparar dois YAMLs via JSON normalizado
yq -o json a.yaml > /tmp/a.json
yq -o json b.yaml > /tmp/b.json
diff <(jq -S . /tmp/a.json) <(jq -S . /tmp/b.json)
```

### Receitas Python (kislyuk)

```bash
# Filtrar usuários ativos (sintaxe jq pura, output YAML)
yq -y '.users[] | select(.active)' users.yaml

# Pipar campo YAML pro jq
yq '.metrics' app.yaml | jq '.cpu_threshold'
```

### Decidir qual usar

**yq Go (Mike Farah):**

- Padrão em Homebrew e asdf.
- Melhor pra fluxos Kubernetes, kustomize, helm values.
- Preserva comments melhor (na maioria dos casos).
- Suporte multi-doc rico via `eval-all`.
- In-place nativo com `-i`.

**yq Python (kislyuk):**

- Se já usa jq intensivamente e quer reutilizar sintaxe sem aprender nova DSL.
- Instalação leve via pip, sem binário externo (desde que jq esteja instalado).
- Comum em pipelines onde jq já é base.

Em times e projetos: **fixar uma implementação e documentar**. Misturar as duas gera confusão — receitas que funcionam pra um dev quebram no outro.

**Versão hedged:** yq Go 4.x+; yq Python 3.x+; verifique `yq --version` localmente.

## Armadilhas

### (1) Confundir as duas impls — receita não funciona

**Causa:** copiar exemplo da web sem checar qual yq está instalado.

**Sintoma:** comando dá erro de sintaxe; output inesperado.

**Como detectar:** `yq --version` — Go fala `v4.x.x` (com `v`); Python fala `3.x.x` (sem `v`).

**Solução:** sempre prefaciar receitas internas com `[yq Go]` ou `[yq Python]`. Usar a impl que o time padronizou. Em scripts CI, validar versão antes de rodar.

### (2) Preservação de comments difere entre impls

**Causa:** edição in-place pode descartar comments dependendo de impl e versão.

**Sintoma:** comments somem após `yq -i ...`.

**Como detectar:** diff antes/depois mostra perda.

**Solução:** yq Go preserva melhor; verificar versão recente. Para comments críticos, considerar ferramentas dedicadas (`ruamel.yaml` em Python).

### (3) Multi-doc (`---`) com suporte diferente entre impls

**Causa:** YAML multi-doc é comum em k8s/CI; cada impl trata de forma diferente.

**Sintoma:** comando que funciona em arquivo single-doc falha em multi-doc.

**Como detectar:** `yq '.name' multidoc.yaml` — Go retorna múltiplos valores; Python varia.

**Solução:** yq Go usa `eval-all`; yq Python usa `--slurp`. Documentar abordagem por impl no projeto.

### (4) Anchors e aliases YAML — comportamento opaco

**Causa:** `&anchor` e `*alias` permitem reuso de nós; yq tipicamente expande no parse.

**Sintoma:** output não tem mais `&`/`*` — YAML "perde" estrutura de reuso.

**Como detectar:** input tem `&base` e `*base`; output só tem valores duplicados.

**Solução:** se precisa preservar anchors, ler doc da impl (ex: flags específicas em yq Go). Aceitar expansão como comportamento default na maioria dos pipelines.

### (5) Instalar acidentalmente a impl errada

**Causa:** `apt install yq` em Debian instala Python (kislyuk); `brew install yq` instala Go; `pip install yq` instala Python.

**Sintoma:** scripts copiados pra outra máquina falham; sintaxe esperada não bate.

**Como detectar:** comparar `yq --version` entre máquinas.

**Solução:** documentar qual impl em README/dotfiles. Para Go em Debian: baixar binário direto do GitHub Releases ou usar snap (`snap install yq`).

### (6) yq Python output default = JSON, não YAML

**Causa:** kislyuk converte YAML→JSON internamente para usar jq; output default é JSON.

**Sintoma:** rodar `yq '.foo' file.yaml` retorna JSON — surpreende quem esperava YAML.

**Como detectar:** output entre `{}`/`""`/`[]` puros, sem indentação YAML.

**Solução:** usar flag `-y` (yaml output): `yq -y '.foo' file.yaml`. Em yq Go não é necessário.

## Em inglês

- **implementação** — *implementation*. "Existem duas implementations incompatíveis de yq: Mike Farah (Go) e kislyuk (Python)."
- **derivação** — *fork*. "kislyuk/yq é um projeto fork-adjacent, não um fork direto de mikefarah/yq."
- **multi-documento** — *multi-document*. "Manifestos Kubernetes frequentemente usam multi-document YAML separado por `---`."
- **âncora** — *anchor*. "YAML anchors (`&name`) definem nós reutilizáveis no documento."
- **apelido** — *alias*. "Um alias (`*name`) referencia um anchor previamente definido no documento."
- **edição in-place** — *in-place edit*. "yq Go suporta in-place editing via `-i`; yq Python não tem equivalente nativo."
- **analisador** — *parser*. "Cada implementation tem seu próprio YAML parser com comportamento diferente para anchors e multi-doc."
- **conversão** — *conversion*. "yq Go realiza YAML-to-JSON conversion nativamente com `yq -o json`."
- **preservação** — *preserve*. "yq Go preserves comments YAML melhor que yq Python na maioria dos casos."
- **expansão** — *expand*. "Ambas as implementations expandem anchors e aliases por default ao processar o YAML."

## Veja também

- [[07 - jq — processor JSON com DSL]] — base do yq Python; complementa yq Go via conversão
- [[13 - Pipeline JSON e YAML — jq yq fzf]] — composição capstone
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#yq (Go)|yq (Go)]]
- [[Dicionário do Terminal#yq (Python/kislyuk)|yq (Python/kislyuk)]]
- [[Dicionário do Terminal#YAML multi-doc|YAML multi-doc]]
- [[Dicionário do Terminal#anchors e aliases (YAML)|anchors e aliases (YAML)]]

## Referências

- yq Go (Mike Farah): https://mikefarah.gitbook.io/yq/
- yq Python (kislyuk): https://github.com/kislyuk/yq
- yq Python doc: https://kislyuk.github.io/yq/
