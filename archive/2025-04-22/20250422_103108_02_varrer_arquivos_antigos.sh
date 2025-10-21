#!/bin/bash
mkdir -p /core_oraculo/biblioteca/legado
find / -type f -name '*.log' -size +50M -exec gzip {} \; -exec mv {}.gz /core_oraculo/biblioteca/legado/ \; 2>/dev/null
echo "✅ Ritual 02 concluído: arquivos antigos comprimidos e movidos."
