#!/usr/bin/env bash
set -euo pipefail
echo "[bootstrap] Criando pastas de dados…"
BASE="$HOME/Library/Application Support/Digimundo"
mkdir -p "$BASE/models" "$BASE/workspace" "$BASE/memory" "$BASE/indices" "$BASE/logs"
echo "[bootstrap] OK: $BASE"
echo "[bootstrap] Dica: coloque um .gguf em '$BASE/models' e configure na UI ou via: node app/server/tools/config-set-model.js PATH_DO_GGUF"
