#!/bin/bash
echo "Reparumon ajustando permissões e corrigindo caminhos..."
chmod -R 755 /core_oraculo/rituais
find /core_oraculo/rituais -type l ! -exec test -e {} \; -delete
echo "✅ Permissões e links corrigidos."
