#!/bin/bash

# 🎮 DEMONSTRAÇÃO: DIGIMONS CONVERSANDO COM CLAUDE

echo "🌟 DIGIMUNDO + CLAUDE TERMINAL"
echo "=============================="
echo ""
echo "Este sistema permite que os Digimons conversem"
echo "com o Claude através do terminal, igual você faz!"
echo ""

# Função para simular Digimon perguntando
ask_as_digimon() {
    local DIGIMON=$1
    local QUESTION=$2
    
    echo ""
    echo "🎮 $DIGIMON está digitando no terminal..."
    echo "   Pergunta: '$QUESTION'"
    echo ""
    
    # Enviar pergunta para Claude via terminal
    RESPONSE=$(echo "[$DIGIMON do Digimundo pergunta]: $QUESTION" | npx @anthropic-ai/claude-code --print 2>/dev/null)
    
    if [ ! -z "$RESPONSE" ]; then
        echo "🤖 Claude responde para $DIGIMON:"
        echo "$RESPONSE" | head -5
        echo "..."
        
        # Salvar conversa
        SAVE_DIR="$HOME/Library/Application Support/Digimundo/digimon_chats"
        mkdir -p "$SAVE_DIR"
        
        cat >> "$SAVE_DIR/conversation_log.txt" << EOF
========================================
Timestamp: $(date)
Digimon: $DIGIMON
Pergunta: $QUESTION
Resposta: $RESPONSE
========================================

EOF
        echo ""
        echo "💾 Conversa salva em: $SAVE_DIR/conversation_log.txt"
    else
        echo "❌ Claude não respondeu (precisa estar autenticado)"
    fi
}

# Menu interativo
while true; do
    echo ""
    echo "=============================="
    echo "ESCOLHA UMA OPÇÃO:"
    echo "=============================="
    echo "1. Agumon pergunta sobre programação"
    echo "2. Gabumon pergunta sobre amizade"
    echo "3. Patamon pergunta sobre esperança"
    echo "4. Tentomon pergunta sobre tecnologia"
    echo "5. Fazer sua própria pergunta"
    echo "6. Ver conversas anteriores"
    echo "7. Sair"
    echo ""
    read -p "Opção: " CHOICE
    
    case $CHOICE in
        1)
            ask_as_digimon "Agumon" "Como posso aprender a programar e ajudar meu parceiro humano?"
            ;;
        2)
            ask_as_digimon "Gabumon" "O que significa ser um verdadeiro amigo no mundo digital e real?"
            ;;
        3)
            ask_as_digimon "Patamon" "Como manter a esperança quando tudo parece difícil?"
            ;;
        4)
            ask_as_digimon "Tentomon" "Como funciona a inteligência artificial que permite nossa existência?"
            ;;
        5)
            echo "Digite seu nome:"
            read USER_NAME
            echo "Digite sua pergunta:"
            read USER_QUESTION
            ask_as_digimon "$USER_NAME" "$USER_QUESTION"
            ;;
        6)
            SAVE_DIR="$HOME/Library/Application Support/Digimundo/digimon_chats"
            if [ -f "$SAVE_DIR/conversation_log.txt" ]; then
                echo ""
                echo "📜 ÚLTIMAS CONVERSAS:"
                echo ""
                tail -30 "$SAVE_DIR/conversation_log.txt"
            else
                echo "Nenhuma conversa salva ainda"
            fi
            ;;
        7)
            echo "👋 Até logo!"
            exit 0
            ;;
        *)
            echo "Opção inválida"
            ;;
    esac
done