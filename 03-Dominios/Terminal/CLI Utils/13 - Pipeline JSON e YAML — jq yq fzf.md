---
title: "Pipeline JSON e YAML — jq yq fzf"
created: 2026-05-22
updated: 2026-05-22
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - cli-utils
  - magus
  - jq
  - yq
  - fzf
  - pipeline
aliases:
  - Pipeline JSON YAML
  - jq yq fzf
---

> [!abstract] TL;DR
> Capstone — receitas reais de pipeline composto pra processar dados estruturados no fluxo cotidiano. `curl | jq | fzf` pra explorar API; `kubectl get -o json | jq` pra filtrar k8s; `yq -o json | jq` pra usar yq Go com sintaxe jq downstream; error handling com `set -o pipefail` + `jq -e`. Assume leitura das notas [[07 - jq — processor JSON com DSL]] e [[08 - yq — processor YAML e as duas implementações]].

## O que é / Como funciona

### Por que composição

- **jq sozinho**: transformações JSON elegantes
- **yq sozinho**: transformações YAML
- **fzf sozinho**: seleção interativa
- **Juntos**: pipeline reativo que filtra → escolhe → age

### Os três padrões

1. **Explorar** — `<fonte JSON/YAML> | jq <filtro> | fzf` — selecionar item de output estruturado
2. **Modificar** — `<fonte> | yq -o json | jq <transform> | <consumer>` — pipeline de transformação
3. **Acionar** — `<seleção> | xargs <comando>` — agir sobre seleção

### Error handling em pipes

```bash
set -euo pipefail              # standard prelude

# -e: exit em erro
# -u: erro em variável não-definida
# -o pipefail: pipe falha se QUALQUER comando do pipe falhar

# Sem pipefail: curl_falha | jq retorna sucesso (jq nem viu o erro)
# Com pipefail: pipeline detecta falha do curl
```

### `jq -e` em scripts

```bash
# -e: exit 1 se output é null/false/vazio
if curl -sf https://api/health | jq -e '.ok == true' >/dev/null; then
    echo "healthy"
fi
```

### `xargs -r` (GNU) ou `xargs --no-run-if-empty`

- Default xargs: lista vazia → executa comando sem args (comportamento indefinido)
- `-r`: lista vazia → não roda nada (mais seguro)

## Na prática

### Explorar API REST

```bash
# GitHub: listar issues open do repo, escolher uma
curl -s https://api.github.com/repos/cli/cli/issues | \
  jq -r '.[] | "\(.number)\t\(.title)"' | \
  fzf --delimiter='\t' --with-nth=2 --preview 'echo {1}'

# Selecionar e ver detalhes do escolhido
issue_number=$(curl -s https://api.github.com/repos/cli/cli/issues | \
  jq -r '.[] | "\(.number)\t\(.title)"' | \
  fzf | awk -F'\t' '{print $1}')

curl -s "https://api.github.com/repos/cli/cli/issues/${issue_number}" | jq .
```

### Filtrar k8s resources (assume kubectl configurado)

```bash
# Pods com status NotReady em todos os namespaces
kubectl get pods --all-namespaces -o json | \
  jq -r '.items[] | select(.status.containerStatuses[]?.ready == false) |
         "\(.metadata.namespace)\t\(.metadata.name)"'

# Imagens únicas usadas em deployments
kubectl get deploy -A -o json | \
  jq -r '.items[].spec.template.spec.containers[].image' | \
  sort -u

# Selecionar pod interativamente pra exec
pod=$(kubectl get pods -o json | \
  jq -r '.items[].metadata.name' | \
  fzf --preview "kubectl describe pod {}")
kubectl exec -it "$pod" -- bash
```

### YAML → JSON pra pipeline com jq

```bash
# values.yaml (Helm) → extrair imagem com jq
yq -o json values.yaml | jq '.global.image'

# Diff semântico de dois YAMLs (normalizado via JSON ordenado)
diff <(yq -o json --indent=2 a.yaml | jq -S .) \
     <(yq -o json --indent=2 b.yaml | jq -S .)

# Multi-doc YAML → array JSON
yq -o json eval-all '. as $i ireduce ([]; . + [$i])' multidoc.yaml | jq '.[0]'
```

### Script robusto com error handling

```bash
#!/usr/bin/env bash
set -euo pipefail

API="https://api.example.com/v1"

# curl falha → pipeline falha (pipefail captura)
users=$(curl -sf "$API/users")

# jq -re: -r raw + -e exit-on-empty; falha se filtro vazio
admin_id=$(echo "$users" | jq -re '.users[] | select(.role == "admin") | .id' | head -1) || {
    echo "ERR: no admin found" >&2
    exit 1
}

# xargs -r evita executar com input vazio
echo "$users" | jq -r '.users[].email' | xargs -r -n1 echo "Notifying:"
```

### Receitas avançadas

```bash
# jq + parallel pra processamento concorrente
cat large.json | jq -c '.items[]' | parallel -j 4 'echo {} | jq -r .id | xargs process-item'

# yq pra atualizar versão em vários files (encontra com fd, modifica com yq Go)
fd -t f -e yaml -x yq -i '.image = "myapp:v2.3.0"' {}

# Comparar k8s manifests antes/depois de deploy (com delta pro diff)
kubectl get deployment myapp -o json > before.json
kubectl apply -f new-deploy.yaml
kubectl get deployment myapp -o json > after.json
diff <(jq -S '.spec' before.json) <(jq -S '.spec' after.json) | delta
```

### Versão hedged

Verifique localmente: jq 1.7+, yq Go 4.x+ ou yq Python 3.x+, fzf 0.4x+. kubectl varia por cluster.

## Armadilhas

### (1) Pipe sem `set -o pipefail` mascara falhas

**Causa:** default shell — exit code do pipeline é do ÚLTIMO comando; `cmd_falha | jq` retorna sucesso (jq não falhou).

**Sintoma:** script "termina OK" mas resultado está errado.

**Como detectar:** rodar com pipefail desligado e ver script "ter sucesso" mesmo com curl 404.

**Solução:** SEMPRE `set -o pipefail` em scripts. Idealmente `set -euo pipefail` (errexit + nounset + pipefail) no topo.

### (2) `jq -e` surpreendendo com null/false

**Causa:** `-e` retorna exit ≠ 0 quando output é null/false/vazio. Útil mas vira armadilha se você esperava só "vazio".

**Sintoma:** script falha pq jq filter retornou `false` (não null).

**Como detectar:** `echo '{"x":false}' | jq -e '.x'; echo $?` mostra 1.

**Solução:** entender: `-e` é "output é truthy?". Se quer só "tem output?", usar `jq` sem `-e` + `grep -q .` ou check `[[ -n "$result" ]]`.

### (3) `kubectl -o json` vs `-o yaml` mudam parser downstream

**Causa:** copiar receita "kubectl ... | jq" mas usar `-o yaml` por engano — jq não parse YAML.

**Sintoma:** `parse error: Invalid numeric literal`.

**Como detectar:** primeira linha do output não é JSON válido (não começa com `{` ou `[`).

**Solução:** combinar coerentemente — `-o json | jq` ou `-o yaml | yq` (Go) ou `-o yaml | yq | jq` (Python wrappa jq).

### (4) `xargs` sem `-r` em lista vazia executa comando vazio

**Causa:** lista vazia → xargs executa `cmd` sem args, com semantics indefinida (alguns rodam vazio; outros falham; alguns surpreendem).

**Sintoma:** comportamento estranho em pipeline com filtro que pode resultar vazio.

**Como detectar:** `echo '' | xargs ls` lista diretório atual (surpresa).

**Solução:** SEMPRE `xargs -r` em scripts (GNU extension; macOS pode precisar `--no-run-if-empty` se for BSD xargs).

### (5) Binary safety no preview fzf com jq output

**Causa:** jq emite JSON binary-safe, mas piping pra cat/preview sem cuidado pode quebrar terminal se valor contém chars de controle (escape sequences).

**Sintoma:** terminal corrompido após fzf preview de JSON com chars exóticos; precisa `reset`.

**Como detectar:** ver `\x1b` ou `\x07` no output do jq.

**Solução:** usar `bat --color=always` no preview (lida com binary detection); ou sanitizar com `jq -c | tr -cd '\n[:print:]'`.

### (6) jq float64 perde precisão em IDs grandes

**Causa:** mesma armadilha de [[07 - jq — processor JSON com DSL]] (#4) — IDs `int64` (Twitter, Snowflake) viram float64; perde dígitos.

**Sintoma:** ID `1234567890123456789` vira `1234567890123456800`.

**Como detectar:** comparar input vs output em IDs grandes.

**Solução:** preservar como string no JSON original; ou usar `--raw-input --raw-output -R` pra IDs como strings. Em pipelines com Twitter/Snowflake IDs, manter `id` como string sempre.

## Em inglês

- **Pipeline** — *pipeline*. "Pipelines compõem ferramentas pequenas em fluxos maiores."
- **Tratamento de erros** — *error handling*. "`set -o pipefail` é parte essencial do error handling em scripts shell."
- **Exit code** — *exit code*. "O exit code do pipeline reflete o último comando — sem pipefail."
- **Pipefail** — *pipefail*. "Pipefail propaga falhas em qualquer estágio do pipe."
- **Dados estruturados** — *structured data*. "JSON e YAML são os formatos mais comuns de structured data em APIs."
- **JSON** — *JSON*. "jq é o filtro canônico pra JSON em pipelines shell."
- **YAML** — *YAML*. "yq processa YAML mantendo a estrutura."
- **Conversão** — *conversion*. "`yq -o json` faz a conversion YAML → JSON downstream."
- **Seleção interativa** — *interactive selection*. "fzf adiciona interactive selection em qualquer pipeline."
- **Processamento em lote** — *batch processing*. "`xargs -X` ou `parallel` permitem batch processing concorrente."

## Veja também

- [[07 - jq — processor JSON com DSL]] — base
- [[08 - yq — processor YAML e as duas implementações]] — base
- [[01 - fzf — fuzzy finder universal]] — motor de seleção
- [[12 - Stack interativo — fzf zoxide atuin]] — outro capstone (composição interativa)
- [[10 - delta — pager moderno pra git diff]] — útil pra diff de manifests
- [[03-Dominios/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#pipefail|pipefail]]
- [[Dicionário do Terminal#xargs -r|xargs -r]]
- [[Dicionário do Terminal#jq|jq]]
- [[Dicionário do Terminal#yq (Go)|yq (Go)]]
- [[Dicionário do Terminal#raw output (jq -r)|raw output (jq -r)]]

## Referências

- jq manual: https://jqlang.github.io/jq/manual/
- yq Go: https://mikefarah.gitbook.io/yq/
- kubectl JSONPath (referência cruzada): https://kubernetes.io/docs/reference/kubectl/jsonpath/
