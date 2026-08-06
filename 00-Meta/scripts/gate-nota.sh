#!/usr/bin/env bash
# gate-nota.sh — gate estrutural das notas de trilha do vault.
#
# Uso:  00-Meta/scripts/gate-nota.sh <arquivo.md> [arquivo.md ...]
#       00-Meta/scripts/gate-nota.sh "03-Dominios/Tecnologia/Infraestrutura/Nginx/"*.md
#
# Checa, por nota:  tamanho · seções obrigatórias · >=3 [!warning] · tabela PT<->EN
#                   · quadrantChart proibido · "\n" dentro de Mermaid
#                   · quebra manual de linha (advisory) · wikilinks resolvidos
#
# NÃO rodar em index.md / roadmap.md — são MOC/meta e reprovam por não terem
# estrutura de nota. O script os pula sozinho, com aviso.
#
# Saída: relatório por arquivo. Código 1 se houver ERRO (avisos não reprovam).
# Histórico: reescrito em 2026-08-06 e trazido para cá — as versões anteriores
# viviam no scratchpad da sessão e se perdiam a cada /clear.

set -uo pipefail

VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MIN_LINHAS=440
MAX_LINHAS=540
FALHOU=0

if [ $# -eq 0 ]; then
  echo "uso: $0 <arquivo.md> [...]" >&2
  exit 2
fi

erro() { printf '  \033[31m✗ ERRO\033[0m   %s\n' "$1"; FALHOU=1; }
aviso() { printf '  \033[33m! aviso\033[0m  %s\n' "$1"; }
ok()   { printf '  \033[32m✓\033[0m       %s\n' "$1"; }

for f in "$@"; do
  base="$(basename "$f")"

  if [ ! -f "$f" ]; then
    printf '\n\033[1m%s\033[0m\n' "$f"; erro "arquivo não existe"; continue
  fi

  case "$base" in
    index.md|roadmap.md)
      printf '\n\033[1m%s\033[0m — pulado (MOC/meta, não é nota)\n' "$f"; continue ;;
  esac

  printf '\n\033[1m%s\033[0m\n' "$f"

  linhas=$(wc -l < "$f")

  # ---------- tamanho ----------
  if [ "$linhas" -lt "$MIN_LINHAS" ]; then
    erro "tamanho: $linhas linhas (piso $MIN_LINHAS)"
  elif [ "$linhas" -gt "$MAX_LINHAS" ]; then
    aviso "tamanho: $linhas linhas (teto sugerido $MAX_LINHAS)"
  else
    ok "tamanho: $linhas linhas"
  fi

  # ---------- frontmatter ----------
  for campo in title created updated type fase publish tags; do
    grep -qE "^${campo}:" "$f" || erro "frontmatter: falta '${campo}:'"
  done
  head -1 "$f" | grep -qx -- "---" || erro "frontmatter: não começa com ---"

  # ---------- seções obrigatórias ----------
  grep -qF '[!abstract]' "$f"                || erro "falta TL;DR em callout [!abstract]"
  grep -qE '^## Armadilhas comuns'           "$f" || erro "falta '## Armadilhas comuns'"
  grep -qE '^## Como explicar em inglês'     "$f" || erro "falta '## Como explicar em inglês'"
  grep -qE '^## O que vem a seguir'          "$f" || erro "falta '## O que vem a seguir'"
  grep -qE '^## Fontes'                      "$f" || erro "falta '## Fontes'"

  # ---------- abertura por problema ----------
  # heurística: o primeiro parágrafo após o H1 não deve começar definindo o termo
  if grep -qE '^(O |A )?[A-Z][A-Za-z_-]+ (é|são) (um|uma|o|a) ' "$f"; then
    aviso "possível abertura por definição ('X é um...') — conferir se abre por problema"
  fi

  # ---------- >=3 [!warning] ----------
  n_warn=$(grep -cF '[!warning]' "$f")
  if [ "$n_warn" -lt 3 ]; then
    erro "só $n_warn [!warning] (mínimo 3)"
  else
    ok "$n_warn [!warning]"
  fi

  # ---------- tabela PT<->EN com >=5 linhas ----------
  n_en=$(awk '
    /^## Como explicar em inglês/ {dentro=1; next}
    dentro && /^## / {dentro=0}
    dentro && /^\|/ && !/^\|[ :|-]*\|[ :|-]*\|?[ :|-]*$/ {n++}
    END {print n+0}
  ' "$f")
  # desconta a linha de cabeçalho da tabela
  n_en=$((n_en > 0 ? n_en - 1 : 0))
  if [ "$n_en" -lt 5 ]; then
    erro "tabela PT<->EN com $n_en linhas de conteúdo (mínimo 5)"
  else
    ok "tabela PT<->EN: $n_en linhas"
  fi

  # ---------- proibições ----------
  grep -qF 'quadrantChart' "$f" && erro "usa quadrantChart (proibido)"

  # "\n" literal dentro de bloco Mermaid
  mermaid_n=$(awk '
    /^```mermaid/ {dentro=1; next}
    dentro && /^```/ {dentro=0; next}
    dentro && /\\n/ {print NR}
  ' "$f")
  if [ -n "$mermaid_n" ]; then
    erro "\\n literal dentro de Mermaid (usar <br/>) nas linhas: $(echo "$mermaid_n" | tr '\n' ' ')"
  fi

  n_mermaid=$(grep -cE '^```mermaid' "$f")
  [ "$n_mermaid" -eq 0 ] && aviso "nenhum diagrama Mermaid"

  # narrar o próprio processo de escrita
  if grep -qiE 'nesta nota (eu|nós) (vou|vamos) (escrever|verificar)|não consegui confirmar|conforme verificado (na|em) ' "$f"; then
    erro "narra o próprio processo de escrita/verificação, ou hedge de verificação"
  fi

  # ---------- quebra manual de linha (advisory) ----------
  # Duas linhas de prosa consecutivas em que a primeira não termina em
  # pontuação: sintoma clássico de wrap manual. Ignora frontmatter, código,
  # tabelas, listas, callouts e cabeçalhos.
  quebras=$(awk '
    NR==1 && /^---$/ {fm=1; next}
    fm && /^---$/ {fm=0; next}
    fm {next}
    /^```/ {cod = !cod; next}
    cod {next}
    {
      linha[NR]=$0
    }
    END {
      for (i in linha) {
        a=linha[i]; b=linha[i+1]
        if (a=="" || b=="") continue
        if (a ~ /^[#>|\-*0-9]/ || b ~ /^[#>|\-*0-9]/) continue
        if (a ~ /[.:;!?)"]$/) continue
        if (length(a) < 40 || length(a) > 110) continue
        n++
      }
      print n+0
    }
  ' "$f")
  if [ "${quebras:-0}" -gt 0 ]; then
    aviso "$quebras possível(is) quebra(s) manual de linha — conferir (dá falso positivo)"
  fi

  # ---------- wikilinks resolvidos ----------
  quebrados=""
  # extrai alvos: [[alvo]] ou [[alvo|alias]], tolerando o escape \| dentro de callout
  while IFS= read -r alvo; do
    [ -z "$alvo" ] && continue
    case "$alvo" in \#*) continue ;; esac   # link só de âncora
    alvo="${alvo%%#*}"                       # descarta âncora
    alvo="${alvo%"${alvo##*[![:space:]]}"}"  # trim à direita
    [ -z "$alvo" ] && continue
    if [ -f "$VAULT_ROOT/$alvo.md" ] || [ -f "$VAULT_ROOT/$alvo" ]; then
      continue
    fi
    # fallback: resolução por basename, como o Obsidian faz
    if find "$VAULT_ROOT" -name "$(basename "$alvo").md" -not -path "*/node_modules/*" \
         -print -quit 2>/dev/null | grep -q .; then
      continue
    fi
    quebrados="$quebrados $alvo"
  done < <(grep -oE '\[\[[^]]+\]\]' "$f" \
             | sed -E 's/^\[\[//; s/\]\]$//; s/\\\|/|/g; s/\|.*$//')

  if [ -n "$quebrados" ]; then
    erro "wikilink(s) não resolvido(s):$(echo "$quebrados" | tr ' ' '\n' | sort -u | tr '\n' ' ')"
  else
    ok "wikilinks resolvidos"
  fi
done

printf '\n'
if [ "$FALHOU" -eq 1 ]; then
  printf '\033[31mGATE REPROVOU\033[0m — corrigir os ERRO antes do commit.\n'
else
  printf '\033[32mGATE APROVOU\033[0m (avisos não reprovam, mas confira).\n'
fi
exit "$FALHOU"
