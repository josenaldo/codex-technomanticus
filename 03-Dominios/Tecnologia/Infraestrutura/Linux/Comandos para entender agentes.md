---
title: "Comandos para entender agentes"
created: 2026-05-17
updated: 2026-05-17
type: reference
status: budding
tags:
  - infraestrutura/linux
  - shell
  - bash
publish: true
---

# Comandos para entender agentes

Galho do tronco [[Linux]]. Referência por comando + receitas reais — pensado pra quando você vê um agente rodar `sed -n '50,80p' file.md | grep -E ...` e quer entender o que ele acabou de fazer.

Foco em *ler* o que aparece no terminal, não em virar manual exaustivo. Os comandos aqui foram escolhidos a partir do que de fato apareceu nos meus históricos de sessão — não é teoria, é o vocabulário real do dia a dia.

## Panorama

Bata o olho na tabela quando quiser identificar rápido o que cada comando faz:

| Comando | Uso típico |
|---------|-----------|
| `ls` | Listar arquivos/diretórios |
| `cat` | Imprimir conteúdo de arquivo |
| `head` / `tail` | Primeiras / últimas N linhas |
| `wc` | Contar linhas, palavras, bytes |
| `file` | Detectar tipo de arquivo |
| `stat` | Metadados (tamanho, mtime, permissões) |
| `tree` | Árvore de diretórios |
| `find` | Procurar arquivos por nome/tipo/data |
| `grep` | Buscar padrões em texto |
| `xargs` | Passar resultados como argumentos |
| `sed` | Editar/substituir em stream |
| `awk` | Processar texto por colunas |
| `cut` | Recortar colunas |
| `tr` | Substituir/deletar caracteres |
| `sort` | Ordenar linhas |
| `uniq` | Deduplicar linhas adjacentes |
| `jq` | Processar JSON |
| `mkdir` / `cp` / `mv` / `rm` | Criar / copiar / mover / deletar |

## Inspecionar

### ls — listar

Lista arquivos e diretórios. É o primeiro comando que um agente roda quando precisa "ver" onde está.

**Flags essenciais:**
- `-l` formato longo (permissões, dono, tamanho, data)
- `-a` inclui ocultos (que começam com `.`)
- `-h` tamanhos humanos (1K, 234M, 2G)
- `-t` ordena por data de modificação
- `-S` ordena por tamanho
- `-r` reverso

```bash
# Ver tudo de uma pasta, com permissões
ls -la

# Tamanhos legíveis, mais recentes primeiro
ls -lht

# Maiores arquivos primeiro
ls -laSh
```

### cat — concatenar e imprimir

Despeja conteúdo do arquivo no stdout. Para arquivos pequenos é direto; para grandes, prefira `less` (paginado) ou `head`/`tail`.

```bash
cat arquivo.txt
cat arquivo1 arquivo2 > combinado.txt   # junta dois
```

**Pegadinha:** agente rodando `cat` em arquivo de 10MB enche o contexto. Quando ver `cat` num arquivo grande, suspeita.

### head / tail — pontas do arquivo

`head` mostra as primeiras N linhas, `tail` as últimas.

**Flags essenciais:**
- `-n N` quantas linhas (default 10)
- `-f` (só `tail`) follow — fica imprimindo enquanto o arquivo cresce

```bash
head -n 20 README.md          # primeiras 20 linhas
tail -n 50 logs/app.log       # últimas 50
tail -f logs/app.log          # acompanha em tempo real
head -n 100 file | tail -n 20 # linhas 81-100 (combo)
```

### wc — contar

Conta linhas, palavras, bytes.

**Flags essenciais:**
- `-l` linhas
- `-w` palavras
- `-c` bytes
- `-m` caracteres (importante em UTF-8)

```bash
wc -l arquivo.md              # quantas linhas tem?
ls | wc -l                    # quantos itens na pasta?
grep -r "TODO" . | wc -l      # quantos TODOs?
```

### file — tipo de arquivo

Detecta o tipo real, sem se importar com a extensão.

```bash
file imagem.dat               # → PNG image data, 800 x 600
file script                   # → Bourne-Again shell script
```

### stat — metadados

Mostra tudo sobre o arquivo: tamanho, inode, permissões em formato numérico e simbólico, mtime, atime, ctime.

```bash
stat arquivo.md
```

### tree — árvore de diretórios

Mostra a estrutura de pastas em formato visual. Requer instalação separada na maioria das distros.

**Flags úteis:**
- `-L N` limita profundidade
- `-d` só diretórios
- `-I 'padrão'` ignora (ex: `-I 'node_modules|.git'`)

```bash
tree -L 2                     # 2 níveis
tree -d -L 3                  # só pastas, 3 níveis
tree -I 'node_modules|.git'   # ignorando ruído
```

## Buscar

### find — encontrar arquivos

Percorre a árvore e devolve caminhos que casam com critérios.

**Flags essenciais:**
- `-name "padrão"` por nome (glob, não regex)
- `-iname` mesmo, case-insensitive
- `-type f` só arquivos, `-type d` só diretórios
- `-mtime -N` modificados nos últimos N dias
- `-size +100M` maiores que 100MB
- `-maxdepth N` limita profundidade
- `-exec cmd {} \;` roda comando em cada resultado

```bash
# Todos os .md modificados hoje
find . -name "*.md" -mtime -1

# Só diretórios chamados "node_modules"
find . -type d -name "node_modules"

# Listar e ordenar
find . -name "*.log" | sort

# Combo clássico: find + xargs + grep
find . -name "*.md" | xargs grep -l "callout"
```

**Pegadinha:** `find -name` usa glob (`*.md`), não regex. Para regex use `-regex '.*\.(md|txt)'`.

### grep — buscar texto

Filtra linhas que casam com padrão. O comando que mais aparece em sessão de agente.

**Flags essenciais:**
- `-r` recursivo
- `-n` número da linha
- `-E` regex estendido (permite `|`, `+`, `?` sem escape)
- `-l` só nomes de arquivos que casam
- `-i` case-insensitive
- `-v` inverter (linhas que NÃO casam)
- `-c` contar matches
- `-A N` / `-B N` / `-C N` linhas de contexto depois / antes / em volta

```bash
# Busca recursiva mostrando arquivo:linha
grep -rn "TODO" .

# Só os nomes dos arquivos
grep -rl "deprecated" src/

# Regex estendido
grep -rnE "fn (handle|process)_" src/

# Linhas em volta do match
grep -rn -C 3 "panic" src/

# Combinar com find
find . -name "*.md" | xargs grep -l "publish: true"
```

**Pegadinha:** macOS vem com BSD grep, Linux com GNU grep. Algumas flags diferem (`-P` Perl-regex existe no GNU, não no BSD). Em macOS, instale `ggrep` via Homebrew se precisar do GNU.

### xargs — alimentar comandos com stdin

Pega linhas do stdin e usa como **argumentos** do comando alvo (não como stdin do alvo). Crítico pra encadear `find` com qualquer outra coisa.

**Flags essenciais:**
- `-I {}` placeholder customizado (default usa tudo no fim)
- `-0` lê separado por null (combina com `find -print0`, seguro pra nomes com espaço)
- `-n N` no máximo N argumentos por chamada
- `-P N` paralelizar em N processos

```bash
# Equivalente: grep -l "x" $(find . -name "*.md")
find . -name "*.md" | xargs grep -l "publish"

# Com placeholder
find . -name "*.tmp" | xargs -I {} mv {} /tmp/

# Seguro pra nomes com espaço
find . -name "*.log" -print0 | xargs -0 rm
```

## Transformar

### sed — stream editor

Edita texto fluindo no pipe. Tem três usos principais: imprimir faixa de linhas, substituir padrões, deletar linhas.

**Flags essenciais:**
- `-n` suprime output default (combina com `p` pra imprimir só o pedido)
- `-i` edita o arquivo in-place (CUIDADO — sem backup)
- `-E` regex estendido
- `'N,Mp'` imprime linhas N a M
- `'s/x/y/g'` substitui x por y em todo lugar
- `'/padrão/d'` deleta linhas que casam

```bash
# Mostrar linhas 50 a 80 de um arquivo
sed -n '50,80p' arquivo.md

# Substituir em todo o arquivo, in-place
sed -i 's/old/new/g' arquivo.md

# Deletar linhas vazias
sed -i '/^$/d' arquivo.md

# Trocar delimitador quando padrão tem /
sed 's|/old/path|/new/path|g' arquivo
```

**Pegadinha:** `sed -i` no macOS (BSD) exige um sufixo de backup: `sed -i '' 's/x/y/g'`. No Linux (GNU), `-i` sozinho funciona. Por isso scripts portáveis fazem `sed -i.bak '...'` (cria `.bak` em ambos).

### awk — campos e colunas

Processa texto em **campos** (separados por whitespace por default). Pensa em colunas: `$1` é a primeira, `$0` é a linha inteira, `NF` é o número de campos, `NR` é o número da linha.

**Flags / construções essenciais:**
- `-F','` separador de campo (ex: vírgula pra CSV)
- `'{print $1}'` imprime primeira coluna de cada linha
- `'NR > 1'` pula o header
- `'$3 > 100 {print}'` filtro por valor
- `'{sum+=$3} END {print sum}'` agregação

```bash
# Primeira coluna de cada linha
awk '{print $1}' arquivo.log

# CSV: nome (coluna 2) sem header
awk -F',' 'NR>1 {print $2}' dados.csv

# Soma da coluna 3
awk '{sum+=$3} END {print sum}' numeros.txt
```

### cut — recortar colunas

Versão mais simples do awk pra quando a estrutura é regular (CSV, TSV, etc.).

**Flags essenciais:**
- `-d','` delimitador
- `-f N` qual campo (ou `-f 1,3` ou `-f 2-5`)
- `-c N-M` por caracteres

```bash
cut -d',' -f2 dados.csv       # coluna 2 do CSV
cut -d':' -f1 /etc/passwd     # só usernames
cut -c1-10 arquivo            # primeiros 10 chars de cada linha
```

### tr — translate

Substitui ou deleta caracteres. Diferente de sed: opera em **caracteres individuais**, não padrões.

**Flags essenciais:**
- `-d` deletar
- `-s` "squeeze" — colapsa repetições
- `-c` complementar (tudo que NÃO casa)

```bash
# Maiúsculas
echo "olá" | tr 'a-z' 'A-Z'

# Tirar caracteres
echo "1-2-3" | tr -d '-'      # → 123

# Quebrar palavras em linhas
echo "a b c" | tr ' ' '\n'

# Colapsar espaços múltiplos
echo "a   b   c" | tr -s ' '
```

### sort — ordenar

Ordena linhas.

**Flags essenciais:**
- `-n` numérico (não lexicográfico)
- `-r` reverso
- `-u` deduplica (combina sort + uniq)
- `-k N` ordena pela coluna N
- `-t','` separador
- `-h` "human" — entende 1K, 2M, 3G

```bash
sort arquivo.txt
sort -n numeros.txt           # 1, 2, 10 e não 1, 10, 2
sort -rn -k2 -t',' dados.csv  # ordena por coluna 2, numérica, desc
du -sh * | sort -h            # arquivos por tamanho, humano
```

### uniq — deduplicar adjacentes

**Só remove duplicatas consecutivas.** Por isso quase sempre vem depois de `sort`.

**Flags essenciais:**
- `-c` conta ocorrências
- `-d` só linhas duplicadas
- `-u` só linhas únicas

```bash
sort arquivo.txt | uniq               # únicas
sort arquivo.txt | uniq -c            # com contagem
sort arquivo.txt | uniq -c | sort -rn # top por frequência
```

## Conectar

### Pipes `|`

Conecta stdout de um comando ao stdin do próximo. É a essência do shell — ferramentas pequenas compostas em pipeline.

```bash
ls -la | grep "^d"            # só linhas que começam com d (diretórios)
cat log | grep ERROR | wc -l  # quantos erros
```

### Redirections `>`, `>>`, `<`, `2>`, `2>&1`

Cada processo tem três streams: stdin (0), stdout (1), stderr (2).

```bash
cmd > arquivo                 # stdout → arquivo (sobrescreve)
cmd >> arquivo                # stdout → arquivo (append)
cmd < arquivo                 # stdin ← arquivo
cmd 2> erros.log              # stderr → arquivo
cmd > out.log 2>&1            # stdout E stderr → mesmo arquivo
cmd 2>/dev/null               # silencia erros
cmd >/dev/null 2>&1           # silencia tudo
```

**Pegadinha:** a ordem importa. `cmd > log 2>&1` redireciona stdout pro log e depois manda stderr "pra onde stdout está apontando" (o log). Se inverter — `cmd 2>&1 > log` —, stderr vai pro terminal e stdout pro log.

### Subshells `$(...)`

Executa um comando e substitui pelo seu output.

```bash
hoje=$(date +%Y-%m-%d)
echo "Hoje é $hoje"

# Quantos .md tem
echo "Total: $(find . -name '*.md' | wc -l)"

# Em scripts modernos, sempre $(...) ao invés de backticks `...`
```

### Encadeamento `&&`, `||`, `;`

Roda comandos em sequência com regras diferentes:

- `cmd1 && cmd2` — roda `cmd2` **só se** `cmd1` deu certo (exit 0)
- `cmd1 || cmd2` — roda `cmd2` **só se** `cmd1` falhou
- `cmd1 ; cmd2` — roda `cmd2` independente

```bash
mkdir build && cd build           # cd só se mkdir funcionou
test -f arquivo || echo "sumiu"   # echo só se test falhar
git pull; npm install             # roda os dois, ignora falha
```

### Heredocs `<<EOF`

Manda múltiplas linhas como stdin de um comando.

```bash
cat <<EOF > arquivo.txt
linha 1
linha 2 com $variavel expandida
EOF

# Sem expansão de variáveis: aspas no delimiter
cat <<'EOF' > script.sh
echo $isso_nao_expande
EOF
```

## Manipular arquivos

### mkdir, cp, mv, rm

O básico, com as flags que importam:

```bash
mkdir pasta
mkdir -p a/b/c                # cria intermediários sem erro

cp arquivo destino
cp -r dir1 dir2               # recursivo (precisa pra dirs)
cp -p src dst                 # preserva permissões/mtime

mv velho novo                 # move ou renomeia
mv *.log /tmp/                # vários

rm arquivo
rm -r dir                     # recursivo
rm -rf dir                    # força, sem perguntar (CUIDADO)
```

**Pegadinha:** `rm -rf $VAR/algo` com `$VAR` vazio vira `rm -rf /algo`. Sempre cite variáveis e considere `rm -rf -- "$VAR/algo"` com guard de `[ -n "$VAR" ]`.

### chmod — permissões

Muda permissões. Detalhe completo em [[Linux#Permissões e ownership]] — a essência:

```bash
chmod +x script.sh            # tornar executável
chmod 644 arquivo             # rw-r--r-- (padrão para arquivos)
chmod 755 script              # rwxr-xr-x (padrão para executáveis/dirs)
chmod -R 755 dir/             # recursivo
```

## Bônus

### jq — JSON na linha de comando

Processa JSON do mesmo jeito que awk processa colunas.

```bash
cat data.json | jq '.'                            # pretty-print
cat data.json | jq '.users[0].name'               # navegar campos
cat data.json | jq '.users | length'              # contar
cat data.json | jq '.users[] | select(.age > 18)' # filtrar
curl -s api.com/users | jq -r '.[].name'          # com curl (-r tira aspas)
```

### echo / printf

`echo` é simples e onipresente; `printf` é portável e suporta formato (`%s`, `%d`, `%.2f`).

```bash
echo "olá"
echo -n "sem newline"
printf "%-20s %5d\n" "Linhas:" 42
```

## Receitas combinadas

Padrões reais que aparecem direto em sessões. Reconhecer esses combos é mais útil que decorar flag por flag.

### Top-N por frequência

```bash
# Top 10 IPs num access log
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -n 10
```

O combo `sort | uniq -c | sort -rn` é o canivete suíço de "o que aparece mais".

### Substituição em massa

```bash
# Renomear "antigo" pra "novo" em todos os .md
find . -name "*.md" | xargs sed -i 's/antigo/novo/g'

# Com nomes de arquivo que têm espaço (seguro)
find . -name "*.md" -print0 | xargs -0 sed -i 's/antigo/novo/g'
```

### Extrair faixa de linhas

```bash
sed -n '50,80p' arquivo.md
# ou
head -n 80 arquivo.md | tail -n 31
```

### Contar matches

```bash
grep -rn "TODO" . | wc -l
# ou direto:
grep -rc "TODO" . | awk -F':' '{sum+=$2} END {print sum}'
```

### Arquivos modificados recentemente

```bash
find . -mtime -1                          # últimas 24h
find . -mtime -7 -name "*.md"             # últimos 7 dias, só .md
```

### Tamanho de diretórios

```bash
du -sh */                                 # tamanho de cada subdir
du -sh * | sort -h                        # ordenado, humano
du -h --max-depth=1 . | sort -h           # de onde estou
```

### Silenciar erros e capturar tudo

```bash
comando 2>/dev/null                       # ignora erros
comando > saida.log 2>&1                  # captura stdout + stderr
comando > saida.log 2> erros.log          # separados
```

### Loop com find via stdin

```bash
find . -name "*.md" | while read arquivo; do
  echo "Processando $arquivo"
  # ...
done
```

Preferir `find -exec` ou `xargs` quando possível — `while read` quebra com nomes que têm espaço, a menos que use `-print0` + `read -d ''`.

### Listar e processar arquivos por critério

```bash
# .md grandes ordenados por tamanho
find . -name "*.md" -size +10k -exec ls -lh {} \; | sort -k5 -h

# Top 10 arquivos por tamanho na pasta atual
ls -laSh | head -n 11

# Arquivos modificados hoje, com tamanho
find . -mtime -1 -type f -exec ls -lh {} \;
```

## Veja também

- [[Linux]] — tronco completo (filesystem, processos, permissões, networking)
- [[Terminal]] — Zsh / Oh My Zsh
