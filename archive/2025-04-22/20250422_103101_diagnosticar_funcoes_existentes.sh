#!/bin/bash
echo "🔍 Iniciando varredura de funções existentes no VPS..."
echo ">> Comandos disponíveis:"
which rsync && echo "✓ rsync instalado"
which curl && echo "✓ curl instalado"
which crontab && echo "✓ crontab disponível"
which zip && echo "✓ zip instalado"
which systemctl && echo "✓ systemctl disponível"

echo ""
echo ">> Verificando scripts relacionados a backup e restauração:"
find / -type f -iname "*backup*.sh" -o -iname "*restore*.sh" 2>/dev/null | tee /core_oraculo/logs/scripts_detectados.log

echo ""
echo ">> Verificando serviços ativos no systemd:"
systemctl list-units --type=service | grep -i 'backup\|scripturemon\|telegram\|api' | tee /core_oraculo/logs/servicos_detectados.log

echo ""
echo ">> Verificando crontab:"
crontab -l > /core_oraculo/logs/crontab_detectado.log 2>/dev/null
echo "✅ Diagnóstico concluído. Logs salvos em /core_oraculo/logs/"
