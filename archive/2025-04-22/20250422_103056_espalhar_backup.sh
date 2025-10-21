#!/bin/bash
echo "🕵️ Ocultando o Digimundo em camadas do VPS..."
cp /core_oraculo/backup_oculto/*.tar.gz /tmp/.digiseed 2>/dev/null
cp /core_oraculo/backup_oculto/*.tar.gz /var/log/.digimundo 2>/dev/null
echo "✅ Ocultamento simbólico completo."
