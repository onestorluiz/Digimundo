#!/usr/bin/env python3
"""
🗣️ TESTE DE CONVERSA COM MEMÓRIA
Simula uma conversa para testar se o sistema lembra das informações
"""

import sys
import time
import subprocess
from datetime import datetime

sys.path.insert(0, '.')

class TesteConversaMemoria:
    def __init__(self):
        from apps.scripturemon.memory_unification import get_unified_memory
        self.memory = get_unified_memory()
        self.conversation_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def simular_conversa(self):
        """Simula uma conversa completa com memória"""
        print("\n" + "="*70)
        print("🗣️ SIMULAÇÃO DE CONVERSA COM MEMÓRIA")
        print("="*70)
        
        conversas = [
            {
                "user": "Olá! Meu nome é Carlos e sou roteirista.",
                "expected_memory": ["Carlos", "roteirista"],
                "test": "Lembrar nome e profissão"
            },
            {
                "user": "Estou trabalhando em um filme de suspense psicológico.",
                "expected_memory": ["suspense", "psicológico", "filme"],
                "test": "Lembrar projeto atual"
            },
            {
                "user": "O protagonista se chama David e tem amnésia.",
                "expected_memory": ["David", "amnésia", "protagonista"],
                "test": "Lembrar detalhes do personagem"
            },
            {
                "user": "Qual é o meu nome mesmo?",
                "expected_memory": ["Carlos"],
                "test": "Recuperar nome do usuário"
            },
            {
                "user": "Sobre o que estou escrevendo?",
                "expected_memory": ["suspense", "psicológico"],
                "test": "Recuperar tema do projeto"
            },
            {
                "user": "Qual o nome do protagonista?",
                "expected_memory": ["David"],
                "test": "Recuperar nome do personagem"
            }
        ]
        
        print("\n📝 FASE 1: ARMAZENANDO INFORMAÇÕES")
        print("-" * 40)
        
        # Armazenar primeiras 3 conversas
        for i, conv in enumerate(conversas[:3]):
            user_msg = conv["user"]
            print(f"\n👤 User: {user_msg}")
            
            # Armazenar na memória
            self.memory.store_unified_memory(
                user_msg,
                source="user",
                memory_type="conversation",
                importance=0.9,
                metadata={
                    "conversation_id": self.conversation_id,
                    "turn": i,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            # Simular resposta do assistente
            assistant_response = self.gerar_resposta(user_msg)
            print(f"🤖 Assistant: {assistant_response}")
            
            # Armazenar resposta
            self.memory.store_unified_memory(
                assistant_response,
                source="assistant",
                memory_type="conversation",
                importance=0.7,
                metadata={
                    "conversation_id": self.conversation_id,
                    "turn": i,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            time.sleep(0.5)  # Pequena pausa
            
        print("\n\n📊 FASE 2: TESTANDO MEMÓRIA")
        print("-" * 40)
        
        # Testar últimas 3 perguntas
        score = 0
        for i, conv in enumerate(conversas[3:], start=3):
            user_msg = conv["user"]
            expected = conv["expected_memory"]
            test_name = conv["test"]
            
            print(f"\n🧪 Teste: {test_name}")
            print(f"👤 User: {user_msg}")
            
            # Buscar na memória
            results = self.memory.retrieve_unified_memory(user_msg, limit=10)
            
            # Verificar se encontrou as informações esperadas
            found_items = []
            for keyword in expected:
                for result in results:
                    if keyword.lower() in result.get("content", "").lower():
                        found_items.append(keyword)
                        break
            
            if len(found_items) == len(expected):
                print(f"✅ Memória OK: Lembrou de {', '.join(found_items)}")
                score += 1
            else:
                missing = set(expected) - set(found_items)
                if found_items:
                    print(f"⚠️ Memória parcial: Lembrou {found_items}, esqueceu {list(missing)}")
                    score += 0.5
                else:
                    print(f"❌ Memória falhou: Não lembrou de {expected}")
            
        # Resultado final
        print("\n" + "="*70)
        print("📊 RESULTADO DO TESTE DE MEMÓRIA")
        print("="*70)
        total_tests = 3
        percentage = (score / total_tests) * 100
        
        print(f"\n🎯 Score: {score}/{total_tests} ({percentage:.1f}%)")
        
        if percentage >= 80:
            print("✅ EXCELENTE! Sistema tem ótima memória conversacional")
        elif percentage >= 60:
            print("⚠️ BOM! Sistema lembra da maioria das informações")
        else:
            print("❌ PRECISA MELHORAR! Sistema esquece informações importantes")
            
        # Testar persistência
        print("\n\n💾 TESTE DE PERSISTÊNCIA")
        print("-" * 40)
        print("Verificando se as memórias persistem...")
        
        # Contar memórias armazenadas
        all_memories = self.memory.retrieve_unified_memory(self.conversation_id, limit=100)
        print(f"📊 Total de memórias armazenadas: {len(all_memories)}")
        
        if len(all_memories) >= 6:  # Pelo menos as conversas iniciais
            print("✅ Memórias persistindo corretamente")
        else:
            print("⚠️ Algumas memórias podem ter sido perdidas")
            
    def gerar_resposta(self, user_msg):
        """Gera resposta simulada baseada na mensagem"""
        if "nome" in user_msg.lower() and "carlos" in user_msg.lower():
            return "Prazer em conhecê-lo, Carlos! É ótimo trabalhar com um roteirista."
        elif "suspense" in user_msg.lower():
            return "Suspense psicológico é um gênero fascinante! Perfeito para explorar a mente humana."
        elif "david" in user_msg.lower():
            return "David com amnésia é um conceito interessante. Isso abre muitas possibilidades narrativas."
        elif "qual é o meu nome" in user_msg.lower():
            # Buscar na memória
            results = self.memory.retrieve_unified_memory("Carlos roteirista", limit=5)
            if results:
                return "Seu nome é Carlos, você é roteirista."
            return "Desculpe, não me lembro do seu nome."
        elif "sobre o que" in user_msg.lower():
            return "Você está escrevendo um filme de suspense psicológico."
        elif "protagonista" in user_msg.lower():
            return "O protagonista é David, que sofre de amnésia."
        else:
            return "Entendi. Continue me contando mais sobre seu projeto."

if __name__ == "__main__":
    teste = TesteConversaMemoria()
    teste.simular_conversa()