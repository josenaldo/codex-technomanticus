#!/usr/bin/env bash
# Revisão semanal do vault — disparado por cron de sábado.
# Roda /revisao-semanal headless. Veja `crontab -l`.

export HOME=/home/josenaldo
export PATH=$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin

VAULT=/home/josenaldo/repos/personal/codex-technomanticus
LOG="$VAULT/00-Meta/revisoes/.cron.log"
mkdir -p "$(dirname "$LOG")"

cd "$VAULT" || { echo "[$(date -Iseconds)] vault não encontrado" >> "$LOG"; exit 1; }
echo "[$(date -Iseconds)] iniciando revisão semanal..." >> "$LOG"
/home/josenaldo/.local/bin/claude -p "/revisao-semanal" >> "$LOG" 2>&1
echo "[$(date -Iseconds)] done (exit=$?)" >> "$LOG"
