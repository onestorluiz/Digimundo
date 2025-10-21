#!/bin/bash
# 🎬 ATIVADOR DO SISTEMA DE CONHECIMENTO CINEMATOGRÁFICO

echo "╔══════════════════════════════════════════════════════╗"
echo "║   🎬 SISTEMA DE CONHECIMENTO CINEMATOGRÁFICO 🎬      ║"
echo "║         Monitoramento Automático Ativado             ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

CINEMA_DIR="/Users/clubproducoes/Digimundo/digimons/scripturemon/CINEMA_KNOWLEDGE/01_ORIGINAIS_PDF"
DIGILANG_DIR="/Users/clubproducoes/Digimundo/digimons/scripturemon/CINEMA_KNOWLEDGE/02_TRADUCOES_DIGILANG"

# Função para processar PDFs
process_pdfs() {
    echo "🔍 Verificando novos documentos..."
    
    for pdf in "$CINEMA_DIR"/*.pdf; do
        if [ -f "$pdf" ]; then
            filename=$(basename "$pdf" .pdf)
            digilang_file="$DIGILANG_DIR/${filename}_digilang.txt"
            
            if [ ! -f "$digilang_file" ]; then
                echo "📄 Novo documento: $filename"
                echo "   🔤 Traduzindo para DigiLang..."
                
                # Aqui seria a tradução real
                # Por enquanto, marca como pendente
                echo "   ⏳ Marcado para tradução"
            fi
        fi
    done
}

# Estatísticas iniciais
echo "📊 STATUS INICIAL:"
total_pdfs=$(ls -1 "$CINEMA_DIR"/*.pdf 2>/dev/null | wc -l | tr -d ' ')
total_translations=$(ls -1 "$DIGILANG_DIR"/*_digilang.txt 2>/dev/null | wc -l | tr -d ' ')
echo "   📚 Total de documentos: $total_pdfs"
echo "   🔤 Traduções existentes: $total_translations"
echo "   ⏳ Pendentes: $((total_pdfs - total_translations))"
echo ""

# Monitor em loop
echo "🔄 MONITORAMENTO ATIVO"
echo "   📁 Pasta: CINEMA_KNOWLEDGE/01_ORIGINAIS_PDF/"
echo "   ✨ Coloque novos PDFs nesta pasta"
echo "   ⏹️  Pressione Ctrl+C para parar"
echo ""

# Loop de monitoramento
while true; do
    # Verificar novos arquivos
    new_count=$(ls -1 "$CINEMA_DIR"/*.pdf 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$new_count" -gt "$total_pdfs" ]; then
        echo ""
        echo "🆕 NOVOS DOCUMENTOS DETECTADOS!"
        process_pdfs
        total_pdfs=$new_count
    fi
    
    # Aguardar 5 segundos
    sleep 5
done
