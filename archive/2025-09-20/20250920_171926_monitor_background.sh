#!/bin/bash

# Script para rodar em background
cd /Users/clubproducoes/Digimundo/digimons/scripturemon

# Log file
LOG="conhecimento/evolution.log"

echo "🚀 Evolução automática iniciada: $(date)" >> "$LOG"

# Executar Python script
python3 SCRIPTUREMON_RAG_EVOLUTION.py << INPUT
1
INPUT
