#!/bin/bash

# 🚀 Script para baixar recursos linguísticos para DigiLang Universal

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   📥 BAIXANDO RECURSOS LINGUÍSTICOS PARA DIGILANG      ║"
echo "╚══════════════════════════════════════════════════════════╝"

# Criar diretório para recursos
RESOURCES_DIR="/Users/clubproducoes/Digimundo/language_resources"
mkdir -p "$RESOURCES_DIR"
cd "$RESOURCES_DIR"

echo ""
echo "📁 Diretório de recursos: $RESOURCES_DIR"
echo ""

# ==================== INGLÊS ====================
echo "🇬🇧 BAIXANDO RECURSOS DE INGLÊS..."
echo "================================================"

# 1. Google 10000 English
echo "📥 Baixando Google 10000 palavras mais comuns..."
curl -s -o google-10000-english.txt https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt
echo "   ✅ google-10000-english.txt"

# 2. Google 20k (com frequências)
echo "📥 Baixando Google 20k com frequências..."
curl -s -o 20k-english.txt https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt
echo "   ✅ 20k-english.txt"

# 3. English word list (maior)
echo "📥 Baixando lista completa de palavras inglesas..."
curl -s -o english-words.txt https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
echo "   ✅ english-words.txt (370k+ palavras)"

# 4. Common English words with frequency
echo "📥 Baixando palavras inglesas com frequência..."
curl -s -o en_50k.txt https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/en/en_50k.txt
echo "   ✅ en_50k.txt (top 50k com frequência)"

echo ""

# ==================== PORTUGUÊS ====================
echo "🇧🇷 BAIXANDO RECURSOS DE PORTUGUÊS..."
echo "================================================"

# 1. Lista de palavras PT-BR
echo "📥 Baixando dicionário português brasileiro..."
curl -s -o palavras-ptbr.txt https://raw.githubusercontent.com/pythonprobr/palavras/master/palavras.txt
echo "   ✅ palavras-ptbr.txt (290k+ palavras)"

# 2. Frequência português
echo "📥 Baixando palavras portuguesas com frequência..."
curl -s -o pt_50k.txt https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/pt/pt_50k.txt
echo "   ✅ pt_50k.txt (top 50k com frequência)"

# 3. Dicionário PT com definições (menor mas útil)
echo "📥 Baixando dicionário com acentuação..."
curl -s -o brazilian-portuguese.txt https://raw.githubusercontent.com/fserb/pt-br/master/dicio
if [ ! -f "brazilian-portuguese.txt" ] || [ ! -s "brazilian-portuguese.txt" ]; then
    # Alternativa se o primeiro falhar
    curl -s -o brazilian-portuguese.txt https://raw.githubusercontent.com/wooorm/dictionaries/main/dictionaries/pt-BR/index.dic
fi
echo "   ✅ brazilian-portuguese.txt"

echo ""

# ==================== COGNATOS ====================
echo "🔗 BAIXANDO LISTAS DE COGNATOS..."
echo "================================================"

# Lista de cognatos e falsos cognatos
echo "📥 Criando lista de cognatos comuns..."
cat > cognates.txt << 'EOF'
# Cognatos verdadeiros PT-EN (mesma origem, significado similar)
hospital,hospital
hotel,hotel
animal,animal
natural,natural
social,social
total,total
digital,digital
federal,federal
final,final
global,global
ideal,ideal
legal,legal
local,local
mental,mental
normal,normal
oral,oral
real,real
rural,rural
universal,universal
vital,vital
visual,visual
cinema,cinema
drama,drama
programa,program
sistema,system
problema,problem
música,music
físico,physical
químico,chemical
biológico,biological
psicológico,psychological
tecnológico,technological
matemático,mathematical
político,political
econômico,economic
histórico,historical
geográfico,geographical
EOF
echo "   ✅ cognates.txt"

echo ""

# ==================== ESTATÍSTICAS ====================
echo "📊 ESTATÍSTICAS DOS RECURSOS BAIXADOS:"
echo "================================================"

echo "   Arquivos baixados:"
ls -lh *.txt | awk '{print "   • "$9": "$5}'

echo ""
echo "   Total de palavras por arquivo:"
for file in *.txt; do
    if [ -f "$file" ]; then
        count=$(wc -l < "$file")
        echo "   • $file: $(printf "%'d" $count) linhas"
    fi
done

echo ""
echo "✅ DOWNLOAD COMPLETO!"
echo ""
echo "📁 Recursos salvos em: $RESOURCES_DIR"
echo ""
echo "🚀 Próximo passo: Executar o processamento com:"
echo "   python3 /Users/clubproducoes/Digimundo/process_language_resources.py"
echo ""