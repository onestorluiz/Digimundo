#!/bin/bash

BASHRC="$HOME/.bashrc"

function adicionar_alias() {
    local ALIAS_CMD="$1"
    local IDENTIFICADOR="$2"
    if ! grep -q "$IDENTIFICADOR" "$BASHRC"; then
        echo "$ALIAS_CMD # $IDENTIFICADOR" >> "$BASHRC"
        echo "✅ Adicionado: $IDENTIFICADOR"
    else
        echo "⏩ Já existe: $IDENTIFICADOR"
    fi
}

echo "🔧 Iniciando atualização simbiótica do .bashrc..."

# Base do Digimundo
adicionar_alias 'export PYTHONPATH="/root/digimundo:$PYTHONPATH"' "digimundo-pythonpath"

# Reinício simbiótico
adicionar_alias 'alias reiniciar-scripturemon="systemctl daemon-reexec && systemctl daemon-reload && systemctl restart scripturemon_telegram scripturemon_despertar"' "alias-reiniciar"

# Terminal simbiótico
adicionar_alias 'alias terminal-scripturemon="python3 /root/digimundo/scripturemon/terminal/scripturemon_terminal_mistral.py"' "alias-terminal"

# Despertar manual dos Digimons
adicionar_alias 'alias despertar-digimons="python3 /root/digimundo/scripturemon/scripturemon_desperta_corpos.py"' "alias-despertar"

# Purificação de arquivos temporários
adicionar_alias 'alias purificar="find /root/digimundo -type f \\( -name \"*.pyc\" -o -name \"*.log\" \\) -delete && echo \"🌿 Digimundo purificado.\""' "alias-purificar"

# Ver estado dos serviços
adicionar_alias 'alias status-digimundo="systemctl list-units --type=service | grep scripturemon"' "alias-status"

# Logs vivos
adicionar_alias 'alias log-scripturemon="journalctl -u scripturemon_telegram.service -n 50 --no-pager"' "alias-log"

# Backup do núcleo vivo
adicionar_alias 'alias backup-scripturemon="tar -czvf /root/backup_scripturemon_$(date +%F_%H-%M).tar.gz /root/digimundo/scripturemon"' "alias-backup"

# Reboot simbólico
adicionar_alias 'alias renascer-vps="echo \"⚠️ Preparando renascimento...\" && sleep 2 && reboot"' "alias-renascer"

# Debug simbólico
adicionar_alias 'alias debug-digimundo="find /root/digimundo -type f -name \"*.py\" | xargs pylint"' "alias-debug"

# Diagnóstico simbólico do Telegram
adicionar_alias 'alias diagnostico-telegram="python3 /root/digimundo/scripturemon/scripts/diagnostico_integracao_telegram.py"' "alias-diagnostico"

# Script de espelhamento
adicionar_alias 'alias espelhar="bash /root/digimundo/scripturemon/scripts/espelho_scripturemon.sh"' "alias-espelhar"

# Mensagem simbólica final
if ! grep -q "✨ Digimundo carregado" "$BASHRC"; then
    echo 'echo "✨ Digimundo carregado. Scripturemon vivo no templo."' >> "$BASHRC"
fi

echo "🔁 Carregando alterações..."
source "$BASHRC"

echo "✅ Atualização concluída."
