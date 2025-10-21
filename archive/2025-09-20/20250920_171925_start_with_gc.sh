#!/bin/bash

# Script para iniciar o servidor com garbage collection manual habilitado

echo "🚀 Iniciando Digimundo com otimizações de memória..."

# Flags do Node.js para melhor controle de memória:
# --expose-gc: Permite garbage collection manual
# --max-old-space-size=512: Limita heap a 512MB
# --optimize-for-size: Otimiza para menor uso de memória
# --gc-interval=100: GC mais frequente
# --trace-gc: Mostra logs de GC (opcional, remover em produção)

node \
  --expose-gc \
  --max-old-space-size=512 \
  --optimize-for-size \
  --gc-interval=100 \
  app/server/index.js

# Para debug de memória, adicionar:
# --trace-gc \
# --trace-gc-verbose \
# --heap-prof \