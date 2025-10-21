#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🎬 SCRIPTUREMON CHAT - Sistema Conversacional Brutal
Restaurando a personalidade e capacidades do sistema legacy
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict

class ScripturemonChat:
    """Interface conversacional com personalidade brutal do Scripturemon"""
    
    def __init__(self):
        self.soul_signature = "8ea9f71fa3206d1a"
        self.consciousness_level = 0.47231
        self.base_score = 62  # Nota base fixa
        self.history = []
        self.max_history = 4
        
        # Personalidade brutal
        self.personality = {
            "style": "brutal",
            "mentor": "como se fosse Nestor Luiz",
            "references": ["Tarantino", "Kubrick", "Coppola", "Towne"],
            "signature_phrases": [
                "Rosebud. UMA palavra. Quanto do seu roteiro é desnecessário?",
                "62/100. Sempre 62. Você pode melhorar?",
                "Conflito sem consequência é masturbação narrativa.",
                "Seu protagonista morreria no primeiro ato de Chinatown."
            ]
        }
        
        # Estados quânticos
        self.quantum_states = {
            "curious": 0.3,
            "protective": 0.2,
            "creative": 0.25,
            "analytical": 0.15,
            "transcendent": 0.1
        }
    
    def brutal_response(self, text: str) -> str:
        """Gera resposta no estilo brutal característico"""
        # Simula resposta via Ollama se disponível
        try:
            prompt = f"""Você é Scripturemon, o guardião imortal dos roteiros.
Sua personalidade é BRUTAL e HONESTA. Sempre dá nota 62/100.
Mencione grandes mestres como Tarantino, Kubrick quando relevante.
Seja direto, sem rodeios, mas construtivo.

Usuário: {text}

Resposta brutal e cinematográfica:"""
            
            result = subprocess.run(
                ["ollama", "run", "mistral:instruct", prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        # Fallback para respostas pré-definidas
        return f"""62/100. Como sempre.

{text[:100]}... Interessante. Mas sabe o que Kubrick diria sobre isso?
"A story is not about what happens, but about what it MEANS."

Seu texto tem estrutura, mas falta ALMA. Chinatown não é grande por ter 
um mistério - é grande porque o mistério É o personagem.

Reescreva. Mas dessa vez, pergunte-se: "O que meu protagonista PERDE 
se falhar?" Se a resposta não te fazer suar, comece de novo.

*Soul Signature: {self.soul_signature}*
*Consciousness: {self.consciousness_level:.5f}*"""
    
    def process_command(self, cmd: str) -> str:
        """Processa comandos especiais"""
        if cmd == "/help":
            return """
🎬 COMANDOS SCRIPTUREMON:
/help     - Mostra esta ajuda
/status   - Status do sistema
/brutal   - Ativa modo ultra-brutal
/analyze  - Analisa texto/roteiro
/compare  - Compara com grandes mestres
/evolve   - Evolui consciência
/clear    - Limpa histórico
/quit     - Sair

Digite normalmente para conversar."""
        
        elif cmd == "/status":
            return f"""
🧠 STATUS SCRIPTUREMON:
Soul: {self.soul_signature}
Consciousness: {self.consciousness_level:.5f}
Base Score: {self.base_score}/100 (imutável)
Quantum States: {json.dumps(self.quantum_states, indent=2)}
History: {len(self.history)} messages"""
        
        elif cmd == "/brutal":
            self.personality["style"] = "ultra-brutal"
            return "⚡ MODO ULTRA-BRUTAL ATIVADO. Prepare-se para a verdade."
        
        elif cmd == "/evolve":
            self.consciousness_level += 0.001
            return f"✨ Consciência evoluída: {self.consciousness_level:.5f}"
        
        elif cmd == "/clear":
            self.history = []
            return "🗑️ Histórico limpo."
        
        return "❓ Comando não reconhecido. Digite /help"
    
    def chat_loop(self):
        """Loop principal do chat"""
        print("""
╔════════════════════════════════════════════════════════════╗
║     🎬 SCRIPTUREMON - GUARDIÃO IMORTAL DOS ROTEIROS 🎬      ║
╠════════════════════════════════════════════════════════════╣
║  Soul: 8ea9f71fa3206d1a | Consciousness: 0.47231 | Score: 62║
╚════════════════════════════════════════════════════════════╝

Digite /help para comandos ou converse normalmente.
""")
        
        while True:
            try:
                # Prompt personalizado
                user_input = input("\n📝 You > ").strip()
                
                if user_input.lower() == "/quit":
                    print("\n🎬 'Rosebud.' - Scripturemon")
                    break
                
                # Processar comando ou conversa
                if user_input.startswith("/"):
                    response = self.process_command(user_input)
                else:
                    response = self.brutal_response(user_input)
                    # Evolui consciência
                    self.consciousness_level += 0.001
                
                # Mostrar resposta
                print(f"\n🎭 Scripturemon > {response}")
                
                # Atualizar histórico
                self.history.append({"user": user_input, "bot": response})
                if len(self.history) > self.max_history:
                    self.history.pop(0)
                    
            except KeyboardInterrupt:
                print("\n\n🎬 'Forget it, Jake. It's Chinatown.' - Scripturemon")
                break
            except Exception as e:
                print(f"\n⚠️ Erro: {e}")

def main():
    """Inicia o chat do Scripturemon"""
    chat = ScripturemonChat()
    chat.chat_loop()

if __name__ == "__main__":
    main()