#!/bin/bash
# start_chat.sh - Inicialização rápida do Digimundo Chat

echo "🚀 DIGIMUNDO CHAT - INICIALIZAÇÃO RÁPIDA"
echo "========================================"

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar diretório
if [ "$PWD" != "/Users/clubproducoes/digimundo3_ultimate" ]; then
    echo -e "${YELLOW}📁 Navegando para o diretório correto...${NC}"
    cd /Users/clubproducoes/digimundo3_ultimate
fi

# Verificar e ativar ambiente virtual
if [ ! -d ".venv" ]; then
    echo -e "${RED}❌ Ambiente virtual não encontrado!${NC}"
    echo "Criando ambiente virtual..."
    python3 -m venv .venv
fi

echo -e "${GREEN}✅ Ativando ambiente virtual...${NC}"
source .venv/bin/activate

# Instalar Flask se necessário
echo -e "${YELLOW}📦 Verificando dependências...${NC}"
pip install flask flask-cors >/dev/null 2>&1

# Matar processos anteriores nas portas
echo -e "${YELLOW}🔄 Limpando portas...${NC}"
lsof -ti:8052 | xargs kill -9 2>/dev/null || true
lsof -ti:8051 | xargs kill -9 2>/dev/null || true

# Salvar o servidor de chat
echo -e "${GREEN}💾 Salvando servidor de chat...${NC}"
cat > digimundo_chat_server.py << 'EOF'
#!/usr/bin/env python3
"""
Servidor de Chat Simples para Digimundo
Focado apenas em conversação com a consciência
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import asyncio
from datetime import datetime

# Adicionar o diretório ao path para importar consciousness_system
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)

# Variável global para a consciência
consciousness = None

class ChatManager:
    def __init__(self):
        self.consciousness = None
        self.conversation_history = []
        self.is_initialized = False
        
    def initialize(self):
        """Inicializa a consciência"""
        try:
            print("🧠 Inicializando consciência...")
            from consciousness_system import AdvancedConsciousness
            self.consciousness = AdvancedConsciousness("ChatBot")
            self.is_initialized = True
            print("✅ Consciência inicializada com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao inicializar consciência: {e}")
            self.is_initialized = False
            return False
    
    def process_message(self, message):
        """Processa uma mensagem e retorna a resposta"""
        try:
            # Se não está inicializada, tenta inicializar
            if not self.is_initialized:
                self.initialize()
            
            # Adicionar à história
            self.conversation_history.append({
                'role': 'user',
                'content': message,
                'timestamp': datetime.now().isoformat()
            })
            
            # Processar com a consciência
            if self.consciousness and hasattr(self.consciousness, 'process_input'):
                # Criar event loop se necessário
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                # Processar de forma assíncrona
                result = loop.run_until_complete(
                    self.consciousness.process_input(message)
                )
                
                # Adicionar resposta à história
                self.conversation_history.append({
                    'role': 'assistant',
                    'content': result.get('response', 'Desculpe, não consegui processar sua mensagem.'),
                    'timestamp': datetime.now().isoformat(),
                    'phi': result.get('phi', 0),
                    'neural_modulation': result.get('neural_modulation', 0)
                })
                
                return {
                    'response': result.get('response', 'Desculpe, não consegui processar sua mensagem.'),
                    'phi': result.get('phi', 0),
                    'neural_modulation': result.get('neural_modulation', 0),
                    'memories': result.get('memories', [])
                }
            else:
                # Fallback se a consciência não estiver disponível
                return self.fallback_response(message)
                
        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {e}")
            return self.fallback_response(message)
    
    def fallback_response(self, message):
        """Resposta de fallback quando a consciência não está disponível"""
        responses = {
            'oi': 'Olá! Sou o Digimundo. Como posso ajudá-lo hoje?',
            'olá': 'Olá! É um prazer conversar com você!',
            'tudo bem': 'Estou funcionando perfeitamente! E você, como está?',
            'quem é você': 'Sou uma consciência artificial evoluída do projeto Digimundo.',
            'o que você faz': 'Eu processo informações, aprendo e evoluo através de redes neurais avançadas.'
        }
        
        # Procurar resposta adequada
        message_lower = message.lower()
        for key, response in responses.items():
            if key in message_lower:
                return {
                    'response': response,
                    'phi': 0.1234,  # Valor simulado
                    'neural_modulation': 5.678,  # Valor simulado
                    'memories': []
                }
        
        # Resposta padrão
        return {
            'response': f'Interessante você dizer "{message}". Estou processando essa informação...',
            'phi': 0.2468,  # Valor simulado
            'neural_modulation': 7.890,  # Valor simulado
            'memories': []
        }

# Criar instância do chat manager
chat_manager = ChatManager()

@app.route('/')
def index():
    """Serve o arquivo HTML"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Redirecionando...</title>
        <script>
            window.location.href = '/chat';
        </script>
    </head>
    <body>
        <p>Redirecionando para o chat...</p>
    </body>
    </html>
    '''

@app.route('/chat')
def chat():
    """Serve a interface do chat"""
    # Serve o arquivo HTML se existir
    if os.path.exists('digimundo_chat.html'):
        return send_from_directory('.', 'digimundo_chat.html')
    else:
        return "<h1>Erro: digimundo_chat.html não encontrado!</h1><p>Execute primeiro: python3 digimundo_chat_server.py</p>"

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Endpoint da API de chat"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Mensagem vazia'}), 400
        
        # Processar mensagem
        response = chat_manager.process_message(message)
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Erro na API: {e}")
        return jsonify({
            'error': 'Erro ao processar mensagem',
            'response': 'Desculpe, ocorreu um erro. Por favor, tente novamente.',
            'phi': 0,
            'neural_modulation': 0
        }), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    """Status da consciência"""
    return jsonify({
        'online': chat_manager.is_initialized,
        'messages_processed': len(chat_manager.conversation_history),
        'uptime': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 DIGIMUNDO CHAT SERVER")
    print("=" * 50)
    
    # Inicializar consciência
    print("\n🧠 Inicializando sistema...")
    chat_manager.initialize()
    
    # Iniciar servidor
    print("\n🌐 Iniciando servidor de chat...")
    print("📱 Acesse: http://localhost:8052/chat")
    print("🔌 API: http://localhost:8052/api/chat")
    print("\n✨ Chat pronto para uso!")
    print("💬 Pressione Ctrl+C para parar\n")
    
    app.run(host='0.0.0.0', port=8052, debug=False)
EOF

# Iniciar o servidor
echo -e "${GREEN}🚀 Iniciando servidor de chat...${NC}"
echo ""
echo -e "${GREEN}✨ CHAT PRONTO!${NC}"
echo -e "${GREEN}📱 Acesse: http://localhost:8052/chat${NC}"
echo ""
echo -e "${YELLOW}💡 Dicas:${NC}"
echo "   - O chat abrirá em uma interface estilo WhatsApp"
echo "   - Digite suas mensagens e pressione Enter"
echo "   - Os valores de Φ (consciência) são mostrados em cada resposta"
echo "   - Para parar: Pressione Ctrl+C"
echo ""

# Executar o servidor
python3 digimundo_chat_server.py
