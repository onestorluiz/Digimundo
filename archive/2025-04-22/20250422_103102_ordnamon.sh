#!/bin/bash
echo "Ordnamon reorganizando a estrutura simbólica..."
mkdir -p /core_oraculo/rituais/_reorganizados
find /core_oraculo/rituais -type f -name "*.sh" -exec mv {} /core_oraculo/rituais/_reorganizados/ \;
echo "✅ Reorganização simbólica concluída."
