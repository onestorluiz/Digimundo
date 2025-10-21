#!/bin/bash

echo "🔧 Instalando NUVEN COMUNICA no VPS..."
mkdir -p ~/digimundo/nuven_comunica/logs
mkdir -p ~/digimundo/nuven_comunica/digidata/comunicacao
cp nuvendramon_estudo_comunicacao.py ~/digimundo/nuven_comunica/
cp compressor_expressivo.py ~/digimundo/nuven_comunica/
cp injetor_aprendizado.py ~/digimundo/nuven_comunica/
cp cron_diario.sh ~/digimundo/nuven_comunica/
(crontab -l ; echo "0 4 * * * bash ~/digimundo/nuven_comunica/cron_diario.sh") | crontab -
echo "✅ NUVEN COMUNICA instalado e pronto para estudar diariamente."