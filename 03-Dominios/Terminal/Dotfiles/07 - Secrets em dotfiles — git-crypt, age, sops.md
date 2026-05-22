---
title: "Secrets em dotfiles — git-crypt, age, sops"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - dotfiles
  - magus
  - secrets
  - encryption
aliases:
  - Secrets dotfiles
  - git-crypt
  - age
  - sops
---

# Secrets em dotfiles — git-crypt, age, sops

> [!abstract] TL;DR
> 3 abordagens canônicas pra secrets em dotfiles: **git-crypt** (encryption transparente em git, GPG-based, marca files em `.gitattributes`), **age** (encryption moderna ssh-key based, simples), **sops** (Mozilla/CNCF, YAML/JSON aware com partial encryption, suporta age/GPG/KMS). Cada um vence em contexto diferente. **Regra crítica:** commitar plaintext UMA vez = vazou pro history; tem que rotacionar o secret imediatamente.

## O que é / Como funciona

### O problema

Dotfiles tipicamente contêm secrets — e a maioria dos desenvolvedores aprende isso da pior forma:

- `~/.aws/credentials` — access key + secret AWS
- `~/.gnupg/` — GPG private keys
- `~/.ssh/id_ed25519` — SSH private keys
- `~/.netrc` — credenciais FTP/HTTP básicas
- `~/.config/<app>/config.toml` — API tokens de apps custom

Versionar dotfiles resolve portabilidade e histórico de config, mas commitar esses arquivos sem criptografia expõe todas as credenciais publicamente. O problema não é só "evitar commitar acidentalmente" — é garantir que, mesmo quando commitar é intencional (sync entre máquinas), o que vai pro repo já está cifrado.

> [!warning] Aviso crítico
> Commitar um secret em plaintext UMA única vez = o secret está comprometido, mesmo que você faça `git rm` imediatamente. O conteúdo fica preservado no histórico do git. Qualquer pessoa com acesso ao repo pode recuperá-lo via `git log -p`. A única resposta correta é **rotacionar o secret** (revogar e gerar novo) e limpar o histórico com `git filter-repo` ou BFG.

### Opção 1: git-crypt

git-crypt adiciona um **filtro de clean/smudge** ao git: no commit (clean), encripta os files marcados; no checkout (smudge), decripta. O resultado é que os arquivos ficam em plaintext na máquina local, mas cifrados no objeto git (e portanto no remote).

A marcação é feita em `.gitattributes`:

```gitattributes
secrets/* filter=git-crypt diff=git-crypt
*.key filter=git-crypt diff=git-crypt
.env filter=git-crypt diff=git-crypt
```

**Backend:** GPG (assimétrico). Cada colaborador é adicionado via sua GPG public key. git-crypt também suporta **symmetric key export** (`git-crypt export-key`) para distribuição via canal seguro (ex: gerenciador de senhas).

**Algoritmo:** AES-256 em modo CTR com IV sintético derivado de SHA-1 HMAC do arquivo — semanticamente seguro contra chosen-plaintext attack determinístico.

Setup inicial:

```bash
cd ~/dotfiles
git-crypt init
git-crypt add-gpg-user alice@example.com
```

Marcar arquivos em `.gitattributes` e commitar normalmente:

```bash
cat >> .gitattributes <<'EOF'
secrets/* filter=git-crypt diff=git-crypt
*.key filter=git-crypt diff=git-crypt
EOF

echo "API_KEY=xyz" > secrets/api.env
git add .gitattributes secrets/api.env
git commit -m "chore: add secret (encrypted)"
```

Em nova máquina:

```bash
git clone git@github.com:alice/dotfiles.git
git-crypt unlock   # usa GPG key local automaticamente
```

**Prós:** workflow git normal após unlock; transparente; integra com CI via symmetric key; AES-256.
**Contras:** GPG é complicado (geração de key, keyring, web of trust); não revoga acesso após grant; não encripta nomes de arquivo nem mensagens de commit.

Repositório: https://github.com/AGWA/git-crypt

### Opção 2: age

age (pronuncia "ahj", do grego para "burn") é uma ferramenta de encryption de arquivo moderna (2019+) criada por Filippo Valsorda. Foco em simplicidade: chaves explícitas pequenas, sem configuração, composável com pipes Unix.

**Backends:** X25519 (chaves nativas `age1...`) ou SSH keys (`ssh-ed25519`, `ssh-rsa`).

Gerar key pair:

```bash
mkdir -p ~/.age
age-keygen -o ~/.age/key.txt
# Saída:
# Public key: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
# Chave privada salva em ~/.age/key.txt
```

Encriptar:

```bash
# Com chave nativa age
age -r age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p \
    -o secret.age secret.txt

# Com SSH public key (conveniente se você já tem ~/.ssh/id_ed25519.pub)
age -R ~/.ssh/id_ed25519.pub -o secret.age secret.txt

# Múltiplos recipients (qualquer um pode decriptar)
age -r age1abc... -r age1xyz... -o secret.age secret.txt
```

Decriptar:

```bash
age --decrypt -i ~/.age/key.txt secret.age > secret.txt
# Ou com SSH private key
age --decrypt -i ~/.ssh/id_ed25519 secret.age > secret.txt
```

**Prós:** API simples; ssh-key based (zero nova infra); rápido; sem state externo.
**Contras:** não integra automaticamente com git (você encripta manualmente antes de commitar); não há partial encryption de YAML/JSON.

> [!tip] Privacidade com ssh keys
> Usar SSH public keys como recipient embute um identificador no ciphertext (permite rastrear pra qual key foi cifrado). Para máxima privacidade, use chaves nativas `age1...`.

Repositório: https://github.com/FiloSottile/age

### Opção 3: sops

sops (Secrets OPerationS), originalmente Mozilla, hoje projeto CNCF sandbox, é uma ferramenta de encryption **structure-aware**: em arquivos YAML e JSON, encripta os **valores** mas preserva as **chaves**. O resultado é um arquivo que pode ser commitado, permanece legível na sua estrutura, e só os valores sensíveis estão cifrados.

**Backends:** age, GPG, AWS KMS, GCP KMS, Azure Key Vault, HuaweiCloud KMS, HashiCorp Vault.

Exemplo de arquivo após encryption com sops:

```yaml
# Antes (plaintext)
database:
  password: "s3cr3t"
api_key: "ghp_abc123"

# Depois (sops encrypted)
database:
    password: ENC[AES256_GCM,data:8vABcD==,iv:xyz...,tag:abc...,type:str]
api_key: ENC[AES256_GCM,data:QrStUv==,iv:def...,tag:ghi...,type:str]
sops:
    age:
        - recipient: age1ql3z7...
          enc: |
              -----BEGIN AGE ENCRYPTED FILE-----
              ...
    lastmodified: "2026-05-22T00:00:00Z"
    version: 3.8.1
```

Configurar `.sops.yaml` no repo (define rules por path):

```yaml
creation_rules:
  - path_regex: '^secrets/.*\.yaml$'
    age: 'age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p'
  - path_regex: '\.env$'
    age: 'age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p'
```

Encriptar in-place:

```bash
# Definir onde está a age key
export SOPS_AGE_KEY_FILE=~/.config/sops/age/keys.txt

sops -e -i secrets/config.yaml    # encripta in-place
sops -d secrets/config.yaml       # decripta pra stdout
sops secrets/config.yaml          # abre no $EDITOR (decripta, edita, reencripta ao salvar)
```

Extrair valor individual sem decriptar o arquivo inteiro:

```bash
sops -d secrets/config.yaml | yq '.database.password'
```

**Prós:** estrutura YAML/JSON preservada (diff legível); partial encryption; multi-backend (KMS pra equipes); CNCF-backed.
**Contras:** setup mais complexo; requer `SOPS_AGE_KEY_FILE` no ambiente; metadados sops visíveis no arquivo.

Repositório: https://github.com/getsops/sops

### Comparativo

| Critério | git-crypt | age | sops |
|---|---|---|---|
| Setup | médio (GPG obrigatório) | simples | médio |
| Granularidade | file completo | file completo | partial (yaml/json) |
| Integração git | nativa (filtro transparente) | manual | manual (ou hook) |
| Backend | GPG | ssh/X25519 | age/GPG/KMS/Vault |
| Cloud KMS | não | não | sim |
| Curva de aprendizado | alta (GPG) | baixa | média |
| Diff legível no repo | não | não | sim (estrutura preservada) |
| Quando vence | time já usa GPG; quer transparência total | dev solo; quer simplicidade; já tem ssh key | secrets estruturados; equipes DevOps; multi-cloud |

### Integração com chezmoi

chezmoi tem suporte de encryption **nativo** — o melhor dos mundos: você declara o arquivo como encrypted no source tree e o chezmoi gerencia a criptografia automaticamente.

Configurar em `~/.config/chezmoi/chezmoi.toml`:

```toml
encryption = "age"

[age]
  identity = "~/.age/key.txt"
  recipient = "age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p"
```

Adicionar arquivo como encrypted:

```bash
chezmoi add --encrypt ~/.ssh/secret_token
# Source fica em: ~/.local/share/chezmoi/encrypted_dot_ssh/secret_token.age
```

No `chezmoi apply`, ele decripta automaticamente antes de aplicar ao destino. Não requer steps manuais pós-clone.

### Integração com stow

Stow não tem mecanismo de encryption nativo — ele gerencia symlinks, não conteúdo. Opções:

- **git-crypt sobre o repo do stow:** adicione `.gitattributes` com os filtros no repo; o stow não interfere com os filtros do git.
- **Pasta `secrets/` separada com age:** encriptar manualmente com age e commitar `.age` files; script de setup decripta na máquina nova.
- **Não versionar secrets com stow:** excluir do repo via `.gitignore` e restaurar manualmente ou via gerenciador de senhas (1Password, Bitwarden CLI).

### Integração com bare repo

git-crypt funciona identicamente em bare repos — o filtro clean/smudge é transparente ao tipo de repo. Configuração idêntica:

```bash
# No bare repo
dotfiles config filter.git-crypt.smudge "git-crypt smudge"
dotfiles config filter.git-crypt.clean "git-crypt clean"
# Ou simplesmente: git-crypt init (com o alias dotfiles configurado)
```

age e sops funcionam de forma manual: encripta o arquivo antes de `dotfiles add`, commita o `.age` ou o YAML cifrado.

### Pre-commit hook anti-secret

Camada de defesa extra: um hook que barra commits com padrões suspeitos de secrets em plaintext:

```bash
#!/usr/bin/env bash
# .git/hooks/pre-commit  (chmod +x)

if git diff --cached | grep -iE "(api[_-]?key|password|token|secret|private[_-]?key)\s*[=:]\s*['\"]?[a-zA-Z0-9+/]{16,}"; then
  echo "ERRO: possível secret em plaintext no staged diff."
  echo "Verifique com: git diff --cached"
  echo "Use git-crypt, age ou sops antes de commitar."
  exit 1
fi
```

Alternativas mais robustas: ferramentas dedicadas como `gitleaks` e `trufflehog` que usam padrões regex curados para dezenas de provedores (AWS, GitHub, Stripe, etc.).

## Na prática

### Setup git-crypt do zero

```bash
# Instalar
brew install git-crypt          # macOS
sudo apt install git-crypt      # Ubuntu/Debian

# Gerar GPG key (se não tiver)
gpg --full-generate-key         # tipo RSA, 4096 bits, inserir email

# Verificar key ID longa
gpg --list-keys --keyid-format LONG

# Inicializar git-crypt no repo de dotfiles
cd ~/dotfiles
git-crypt init

# Adicionar usuário (usa email ou key ID longa)
git-crypt add-gpg-user alice@example.com

# Marcar arquivos pra encriptar em .gitattributes
cat >> .gitattributes <<'EOF'
.env filter=git-crypt diff=git-crypt
secrets/** filter=git-crypt diff=git-crypt
EOF

git add .gitattributes
git commit -m "chore: setup git-crypt"

# Adicionar secret (será encriptado automaticamente no commit)
echo "GITHUB_TOKEN=ghp_abc123" > secrets/tokens.env
git add secrets/tokens.env
git commit -m "feat: add github token (encrypted)"

# Verificar que o objeto git está encriptado
git show HEAD:secrets/tokens.env | file -   # deve mostrar "data", não texto
```

Em nova máquina após clone:

```bash
git clone git@github.com:alice/dotfiles.git ~/dotfiles
cd ~/dotfiles
git-crypt unlock    # usa GPG key local (precisa ter a private key importada)
cat secrets/tokens.env   # plaintext local
```

Para distribuir acesso sem GPG (ex: CI/CD):

```bash
git-crypt export-key /tmp/dotfiles.key
# Distribuir dotfiles.key via canal seguro (1Password, vault, etc.)
# Na máquina receptora:
git-crypt unlock /path/to/dotfiles.key
```

### Workflow age standalone

```bash
# Instalar
brew install age       # macOS
sudo apt install age   # Ubuntu 22.04+

# Gerar key pair
mkdir -p ~/.age
age-keygen -o ~/.age/key.txt
# Anotar o public key impresso (age1...)
chmod 600 ~/.age/key.txt

# Capturar recipient pra uso em scripts
RECIPIENT=$(grep "^# public key:" ~/.age/key.txt | awk '{print $4}')

# Encriptar secret
age -e -r "$RECIPIENT" -o ~/dotfiles/secrets/api.env.age ~/secrets/api.env

# Commitar o arquivo .age (não o original)
cd ~/dotfiles
git add secrets/api.env.age
git commit -m "feat: add api.env (age encrypted)"

# Em nova máquina: decriptar pra uso
age -d -i ~/.age/key.txt ~/dotfiles/secrets/api.env.age > /tmp/api.env
source /tmp/api.env
rm /tmp/api.env    # nunca deixar plaintext em disco desnecessariamente
```

Proteger a private key com passphrase opcional:

```bash
# age-keygen não suporta passphrase diretamente;
# proteger a key com age sobre si mesma:
age -p -o ~/.age/key.txt.enc ~/.age/key.txt
# Ou usar ssh-keygen -p na ssh key usada como identity
```

### Setup sops com age

```bash
# Instalar sops
brew install sops      # macOS
# Linux: baixar binário de https://github.com/getsops/sops/releases

# Instalar age (se não tiver)
brew install age

# Gerar age key pra sops
mkdir -p ~/.config/sops/age
age-keygen -o ~/.config/sops/age/keys.txt

# Configurar env (adicionar ao .zshrc)
export SOPS_AGE_KEY_FILE="$HOME/.config/sops/age/keys.txt"

# Criar .sops.yaml no repo (define quais arquivos usar qual backend)
RECIPIENT=$(grep "^# public key:" ~/.config/sops/age/keys.txt | awk '{print $4}')

cat > ~/dotfiles/.sops.yaml <<EOF
creation_rules:
  - path_regex: '^secrets/.*\.yaml$'
    age: '${RECIPIENT}'
  - path_regex: '^secrets/.*\.env$'
    age: '${RECIPIENT}'
EOF

git -C ~/dotfiles add .sops.yaml
git -C ~/dotfiles commit -m "chore: setup sops config"

# Criar e encriptar arquivo de secrets
mkdir -p ~/dotfiles/secrets
cat > ~/dotfiles/secrets/config.yaml <<'EOF'
database:
  host: localhost
  password: s3cr3t
api_key: ghp_abc123
EOF

sops -e -i ~/dotfiles/secrets/config.yaml

# Verificar estrutura preservada
cat ~/dotfiles/secrets/config.yaml  # chaves visíveis, valores ENC[...]

git -C ~/dotfiles add secrets/config.yaml
git -C ~/dotfiles commit -m "feat: add config secrets (sops encrypted)"

# Editar secrets interativamente (decripta, abre $EDITOR, reencripta ao salvar)
sops ~/dotfiles/secrets/config.yaml

# Ler valor específico em script
sops -d ~/dotfiles/secrets/config.yaml | yq '.api_key'
```

## Armadilhas

**Commitar plaintext UMA vez = history comprometido para sempre**
**Causa:** setup de git-crypt não foi feito antes de adicionar o arquivo, ou o arquivo ficou fora do padrão de `.gitattributes`.
**Sintoma:** `git log -p -- secrets/api.env` mostra o valor em plaintext em algum commit anterior.
**Como detectar:** `git log --all -p -- <arquivo>` mostra o histórico completo. Ferramentas como `gitleaks` e `trufflehog` auditam todo o histórico automaticamente.
**Solução:** **rotacionar o secret imediatamente** (assumir que está vazado independentemente de o repo ser público ou privado). Depois: `git filter-repo --invert-paths --path secrets/api.env` (ou BFG Repo Cleaner) + force-push + notificar colaboradores pra reclonarem.

---

**git-crypt GPG key perdida = repo permanentemente bloqueado**
**Causa:** a GPG private key foi perdida (disco formatado, key expirada sem backup) e não há outro GPG user adicionado ao repo.
**Sintoma:** `git-crypt unlock` falha em qualquer máquina: "no secret key available".
**Como detectar:** ao tentar unlock em máquina nova.
**Solução preventiva:** (1) adicionar múltiplos GPG users (`git-crypt add-gpg-user` com keys de backup); (2) fazer backup da GPG key via `gpg --export-secret-keys` pra mídia offline ou YubiKey; (3) usar `git-crypt export-key` pra gerar symmetric key e armazenar em gerenciador de senhas.

---

**age `key.txt` commitado por engano no repo**
**Causa:** `age-keygen -o ~/.age/key.txt` foi rodado dentro de uma pasta que é working tree de um repo, seguido de `git add .` inadvertente.
**Sintoma:** `git log --all -- '**/*.txt'` mostra a private key no histórico.
**Como detectar:** `git log --all -p -- ~/.age/key.txt` ou auditar com gitleaks.
**Solução:** revogar/regenerar o key pair; todos os arquivos encriptados com a key comprometida precisam ser reencriptados com a nova key. Limpar histórico com `git filter-repo`.

---

**sops falha "no age recipients" sem `SOPS_AGE_KEY_FILE`**
**Causa:** a variável de ambiente `SOPS_AGE_KEY_FILE` não está setada na sessão atual — sops não encontra a identity pra decriptar.
**Sintoma:** `sops -d secrets/config.yaml` falha com "Failed to get the data key required to decrypt the SOPS file" ou "no age recipients available".
**Como detectar:** `echo $SOPS_AGE_KEY_FILE` retorna vazio.
**Solução:** adicionar `export SOPS_AGE_KEY_FILE="$HOME/.config/sops/age/keys.txt"` ao `~/.zshrc` (ou `~/.zprofile` pra garantir em sessões non-interactive). Verificar com `sops --version` e `age --version` que ambos estão instalados.

---

**chezmoi `--encrypt` falha sem `encryption =` no `chezmoi.toml`**
**Causa:** `chezmoi add --encrypt ~/.ssh/secret` sem ter configurado o método de encryption em `~/.config/chezmoi/chezmoi.toml`.
**Sintoma:** erro "no encryption method configured" ao rodar `chezmoi add --encrypt`.
**Como detectar:** `chezmoi cat-config` — o bloco `[age]` ou `[gpg]` estará ausente.
**Solução:** configurar antes:
```toml
# ~/.config/chezmoi/chezmoi.toml
encryption = "age"
[age]
  identity = "~/.age/key.txt"
  recipient = "age1..."
```

---

**git-crypt não encripta nomes de arquivo nem metadata**
**Causa:** git-crypt só cifra conteúdo de files — os paths, nomes, commit messages e timestamps permanecem plaintext no repo.
**Sintoma:** `git log --name-only` revela que existe um arquivo chamado `secrets/stripe_prod_key.env` mesmo sem poder ler seu conteúdo.
**Como detectar:** navegar o histórico sem fazer unlock.
**Solução:** usar nomes de arquivo opacos (ex: `secrets/payments.env` em vez de `secrets/stripe_prod_key.env`) e commit messages sem mencionar valores ou providers específicos.

## Em inglês

- **encryption** — *criptografia / encriptação*. "Processo de transformar dados legíveis (plaintext) em formato ilegível (ciphertext) usando uma chave."
- **decrypt** — *decriptar / descriptografar*. "Reverter ciphertext para plaintext usando a chave correta — o que git-crypt faz no checkout e sops no `sops -d`."
- **key** — *chave*. "Segredo matemático usado para encriptar e decriptar — pode ser simétrica (mesma key pra ambos) ou assimétrica (public key encripta, private key decripta)."
- **public key** — *chave pública*. "Metade do par assimétrico que pode ser compartilhada livremente; usada para encriptar (`age -r age1...`) ou verificar assinaturas."
- **private key** — *chave privada*. "Metade do par assimétrico que deve ser mantida secreta; usada para decriptar (`age -i ~/.age/key.txt`) — se comprometida, todos os dados cifrados com a public key correspondente estão expostos."
- **ciphertext** — *texto cifrado*. "Resultado da encryption — dados ilegíveis sem a chave correta; o que fica armazenado no git repo quando git-crypt ou sops estão ativos."
- **plaintext** — *texto simples / texto claro*. "Dados legíveis antes da encryption ou após decriptar — NUNCA deve ser commitado em repos que podem ser expostos."
- **transparent** — *transparente*. "Encryption que acontece automaticamente sem mudança no workflow — git-crypt é 'transparente' porque o git cifra/decifra nos filtros clean/smudge sem intervenção manual."
- **backend** — *backend de chaves*. "Sistema responsável por armazenar e gerenciar as chaves de encryption — GPG (local), AWS KMS (cloud), age (arquivo local), HashiCorp Vault (servidor)."
- **rotate** — *rotacionar*. "Substituir um secret comprometido ou expirado por um novo e revogar o anterior — ação obrigatória quando plaintext é exposto, mesmo que brevemente."

## Veja também

- [[05 - chezmoi — manager completo com templates]] — encryption nativa com age integrada ao workflow
- [[06 - Bare git repo — abordagem minimalista]] — git-crypt funciona identicamente em bare repos
- [[08 - Bootstrap — máquina nova zero-to-ready]] — bootstrap precisa provisionar keys antes de restaurar secrets
- [[03-Dominios/Terminal/Dotfiles/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#git-crypt|git-crypt]], [[Dicionário do Terminal#age|age]], [[Dicionário do Terminal#sops|sops]], [[Dicionário do Terminal#Secret (dotfiles)|secret]]

## Referências

- git-crypt: https://github.com/AGWA/git-crypt
- age: https://github.com/FiloSottile/age
- sops: https://github.com/getsops/sops
