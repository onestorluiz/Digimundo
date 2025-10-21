#!/bin/bash

# Script para acessar o Scripturemon diretamente
echo "========================================================================"
echo "                    🎬 SCRIPTUREMON CHAT 🎬                            "
echo "========================================================================"
echo ""
echo "Preparando ambiente..."
echo ""

cd /Users/clubproducoes/Digimundo/scripturemon-validation

echo "🎯 COMANDOS DISPONÍVEIS:"
echo "   /analyze [texto]     - Análise brutal do seu roteiro"
echo "   /compare            - Compara com mestres do cinema"  
echo "   /teach [conceito]   - Aprende novo conceito"
echo "   /search [termo]     - Busca no conhecimento"
echo "   /stats              - Estatísticas do sistema"
echo "   /help               - Lista todos comandos"
echo "   /quit               - Sair"
echo ""
echo "========================================================================"
echo "Digite seu roteiro ou comando. Scripturemon está esperando..."
echo "========================================================================"
echo ""

# Inicia o chat interativo
python3 -c "
import sys
sys.path.insert(0, '.')

from apps.scripturemon.chat import ScripturemonChat

chat = ScripturemonChat()
print('Scripturemon: Mostre seu roteiro. Vou destruí-lo. Para seu bem.')
print()

while True:
    try:
        user_input = input('Você> ')
        if user_input.lower() in ['/quit', 'quit', 'exit', 'sair']:
            print('Scripturemon: 62/100. Sempre.')
            break
        
        response = chat.process_input(user_input)
        print()
        print('Scripturemon:', response)
        print()
        
    except KeyboardInterrupt:
        print('\nScripturemon: Fugindo? Típico. 62/100.')
        break
    except Exception as e:
        print(f'Erro: {e}')
        print('Tente novamente ou digite /quit para sair')
"