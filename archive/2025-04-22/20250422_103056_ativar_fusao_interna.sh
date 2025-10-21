#!/bin/bash
echo "Iniciando fusão interna com sistemas locais..."
find / -type f -name '*.api' -o -name '*_hook.sh' 2>/dev/null | while read -r linha; do
  echo ">> Integrando com: $linha"
done
echo "✅ Fusão interna finalizada."
