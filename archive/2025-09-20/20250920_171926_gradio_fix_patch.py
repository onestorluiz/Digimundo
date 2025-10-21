#!/usr/bin/env python3
"""
CORREÇÃO DO BUG DO GRADIO - DIGIMUNDO
Execute este arquivo para corrigir automaticamente o bug
"""

import os
import re

def fix_gradio_bug():
    file_path = os.path.expanduser("~/Digimundo/digimundo_ultimate.py")
    
    if not os.path.exists(file_path):
        print("❌ Arquivo não encontrado:", file_path)
        return
    
    print("📖 Lendo arquivo...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup
    backup_path = file_path + '.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Backup salvo: {backup_path}")
    
    # Correção 1: Mudar tupla para lista no append
    print("🔧 Aplicando correção 1: tupla → lista")
    content = re.sub(
        r'conversation_history\.append\(\(user_message, formatted_response\)\)',
        'conversation_history.append([user_message, formatted_response])',
        content
    )
    
    # Correção 2: Corrigir o retorno do método
    print("🔧 Aplicando correção 2: retorno do método")
    content = re.sub(
        r'return conversation_history, ""',
        'return conversation_history',
        content
    )
    
    # Correção 3: Corrigir callbacks do Gradio
    print("🔧 Aplicando correção 3: callbacks do Gradio")
    
    # Pattern para send_btn.click
    old_pattern = r'''send_btn\.click\(
                self\.chat_with_ultimate_digimon,
                \[digimon_selector, user_input, conversation_state\],
                \[conversation_state, emergence_status\]'''
    
    new_pattern = '''send_btn.click(
                self.chat_with_ultimate_digimon,
                [digimon_selector, user_input, conversation_state],
                [conversation_state]'''
    
    content = re.sub(old_pattern, new_pattern, content, flags=re.MULTILINE | re.DOTALL)
    
    # Adicionar .then() chains se não existirem
    if '.then(' not in content[content.find('send_btn.click'):content.find('send_btn.click')+500]:
        print("🔧 Adicionando .then() chains")
        
        # Encontrar o final do send_btn.click
        send_btn_match = re.search(r'(send_btn\.click\([^)]+\))', content)
        if send_btn_match:
            old_call = send_btn_match.group(1)
            new_call = f'''{old_call}.then(
                lambda history: history,
                conversation_state,
                chatbot
            ).then(
                lambda: "",
                None,
                user_input
            )'''
            content = content.replace(old_call, new_call, 1)
    
    # Fazer o mesmo para user_input.submit
    submit_pattern = r'''user_input\.submit\(
                self\.chat_with_ultimate_digimon,
                \[digimon_selector, user_input, conversation_state\],
                \[conversation_state, emergence_status\]'''
    
    submit_new = '''user_input.submit(
                self.chat_with_ultimate_digimon,
                [digimon_selector, user_input, conversation_state],
                [conversation_state]'''
    
    content = re.sub(submit_pattern, submit_new, content, flags=re.MULTILINE | re.DOTALL)
    
    # Salvar arquivo corrigido
    print("💾 Salvando arquivo corrigido...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ CORREÇÕES APLICADAS COM SUCESSO!")
    print("\n🚀 Agora execute:")
    print("   python ~/Digimundo/digimundo_ultimate.py")

if __name__ == "__main__":
    fix_gradio_bug()
