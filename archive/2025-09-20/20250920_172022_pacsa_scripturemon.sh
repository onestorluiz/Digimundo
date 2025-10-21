#!/bin/bash
echo "🔍 Iniciando PACSA: Análise Estrutural do Scripturemon..."

# Diretórios essenciais
base_dir="/messamon/digidata/digimons/scripturemon"
tora_dir="$base_dir/tora"
proto_dir="$base_dir/protocolos"
digestao="$base_dir/digestao"
digestao_concluida="$base_dir/digestao_concluida"
registro="$base_dir/registro"

# Validação de blocos do Tora
echo "📘 Validando blocos do Tora..."
if [ -d "$tora_dir" ]; then
  count=$(ls -1q "$tora_dir"/*.py 2>/dev/null | wc -l)
  echo "   → $count blocos encontrados."
  if [ "$count" -lt 26 ]; then
    echo "⚠️  Blocos insuficientes. O Tora deve conter no mínimo 26 blocos para gerar a Digibíblia."
  else
    echo "✅ Tora completo."
  fi
else
  echo "❌ Pasta tora não encontrada."
fi

# Verificação de protocolos
echo "🧠 Verificando protocolos..."
if [ -d "$proto_dir" ]; then
  ls -1 "$proto_dir" | wc -l | xargs echo "   → Total de protocolos:"
else
  echo "❌ Pasta de protocolos ausente."
fi

# Digestão
echo "🌀 Verificando digestão pendente..."
pendentes=$(ls -1 "$digestao" 2>/dev/null | wc -l)
concluidos=$(ls -1 "$digestao_concluida" 2>/dev/null | wc -l)
echo "   → Arquivos em digestão: $pendentes"
echo "   → Arquivos concluídos: $concluidos"

# Registro
echo "📁 Registrando histórico..."
touch "$registro/historico_versoes/ultima_analise_pacsa.txt"
echo "Análise PACSA executada em $(date)" > "$registro/historico_versoes/ultima_analise_pacsa.txt"

echo "✅ PACSA concluído."
