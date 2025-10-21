#!/usr/bin/env python3
"""
DIGIMUNDO SIMPLE - VERSÃO QUE FUNCIONA GARANTIDAMENTE
"""

import gradio as gr
import ollama
import json
from datetime import datetime

# Lista de Digimons
DIGIMONS = {
    "Nexusmon": {"emoji": "🌐", "role": "Coordenador Supremo"},
    "Psychemon": {"emoji": "🧠", "role": "Analista Mental"},
    "Quantomon": {"emoji": "🔬", "role": "Processador Quântico"},
    "Creativemon": {"emoji": "🎨", "role": "Gerador de Ideias"},
    "Wisemon": {"emoji": "📚", "role": "Sábio Conhecedor"},
    "Terminamon": {"emoji": "💻", "role": "Controlador de Terminal"},
    "Scripturemon": {"emoji": "📝", "role": "Editor de Código"},
    "Filemon": {"emoji": "📁", "role": "Gerenciador de Arquivos"}
}

def chat_with_digimon(message, history, digimon_name):
    """Chat simples mas funcional"""
    if not message.strip():
        return history
    
    try:
        # Verificar Ollama
        ollama.list()
        
        # Criar prompt
        digimon = DIGIMONS.get(digimon_name, {"emoji": "🤖", "role": "Digimon"})
        
        prompt = f"""Você é {digimon_name} {digimon['emoji']}, {digimon['role']} do Digimundo.
        
Responda à mensagem do usuário de forma única e característica.

Usuário: {message}
{digimon_name}:"""
        
        # Gerar resposta
        response = ollama.generate(
            model='llama3.2:latest',
            prompt=prompt,
            options={'temperature': 0.8}
        )
        
        bot_response = f"{digimon['emoji']} **{digimon_name}:** {response['response']}"
        
        # IMPORTANTE: Adicionar como LISTA, não tupla!
        history.append([message, bot_response])
        
        # Salvar checkpoint
        save_checkpoint(history, digimon_name)
        
        return history
        
    except Exception as e:
        error_msg = f"❌ Erro: {str(e)}"
        history.append([message, error_msg])
        return history

def save_checkpoint(history, digimon):
    """Salvar conversa"""
    try:
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'digimon': digimon,
            'messages': len(history),
            'last_5': history[-5:] if len(history) > 5 else history
        }
        
        filename = f"checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2, ensure_ascii=False)
    except:
        pass

def count_tokens(text):
    """Contador de tokens simples"""
    tokens = len(text) // 4  # Aproximação
    color = "green" if tokens < 3000 else "orange" if tokens < 3500 else "red"
    return f"📊 Tokens: <span style='color:{color}'>{tokens}</span> / ~4000"

# Interface Gradio
with gr.Blocks(title="🌟 Digimundo Simple", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌟 DIGIMUNDO SIMPLE - VERSÃO FUNCIONAL")
    gr.Markdown("Sistema simplificado mas 100% funcional com 8 Digimons")
    
    with gr.Row():
        with gr.Column(scale=1):
            digimon_selector = gr.Dropdown(
                choices=list(DIGIMONS.keys()),
                value="Nexusmon",
                label="🤖 Escolha seu Digimon"
            )
            
            digimon_info = gr.Markdown("")
            
            def update_info(digimon):
                d = DIGIMONS.get(digimon, {})
                return f"## {d.get('emoji', '🤖')} {digimon}\n**Função:** {d.get('role', 'Digimon')}"
            
            digimon_selector.change(update_info, digimon_selector, digimon_info)
            
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                label="💬 Chat",
                height=400
            )
            
            msg = gr.Textbox(
                label="Digite sua mensagem",
                placeholder="Olá! Como você está?",
                lines=2
            )
            
            token_counter = gr.Markdown("📊 Tokens: 0 / ~4000")
            
            with gr.Row():
                send = gr.Button("🚀 Enviar", variant="primary")
                clear = gr.Button("🔄 Limpar")
    
    # Eventos
    msg.change(count_tokens, msg, token_counter)
    
    send.click(
        chat_with_digimon,
        [msg, chatbot, digimon_selector],
        chatbot
    ).then(
        lambda: "",
        None,
        msg
    )
    
    msg.submit(
        chat_with_digimon,
        [msg, chatbot, digimon_selector],
        chatbot
    ).then(
        lambda: "",
        None,
        msg
    )
    
    clear.click(lambda: [], None, chatbot)
    
    # Carregar info inicial
    demo.load(update_info, digimon_selector, digimon_info)

if __name__ == "__main__":
    print("🌟 Iniciando Digimundo Simple...")
    
    # Verificar Ollama
    try:
        ollama.list()
        print("✅ Ollama conectado!")
    except:
        print("❌ ERRO: Ollama não está rodando!")
        print("   Execute 'ollama serve' em outro terminal")
        exit(1)
    
    print("🚀 Abrindo interface...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )
