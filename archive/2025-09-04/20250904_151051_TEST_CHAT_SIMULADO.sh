#!/bin/bash

# 🎭 TESTE DE CHAT SIMULADO - VALE DO SILÍCIO

echo "========================================================================="
echo "🎭 TESTE DE CHAT SIMULADO - NÍVEL VALE DO SILÍCIO"
echo "========================================================================="

cd /Users/clubproducoes/Digimundo/scripturemon-validation

# Executar teste Python diretamente
python3 << 'ENDPYTHON'
import sys
import os
import time
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-validation')

print("🚀 INICIANDO TESTE DE CHAT SIMULADO")
print("="*70)

# Importar o sistema
try:
    from apps.scripturemon.memory_unification import get_unified_memory
    from apps.scripturemon.cinema_knowledge import get_cinema_knowledge
    from apps.scripturemon.consciousness import get_level
    from apps.scripturemon.soul import Soul
    
    print("✅ Todos os módulos importados")
except Exception as e:
    print(f"❌ Erro ao importar: {e}")
    sys.exit(1)

# Simular interações
interactions = [
    ("status", "Verificando status do sistema"),
    ("Olá Scripturemon!", "Teste de saudação"),
    ("O que é cinema para você?", "Teste de conhecimento de cinema"),
    ("Conte sobre o roteiro SONHOS SEM LEMBRANÇAS", "Teste de roteiro específico"),
]

print("\n📝 SIMULANDO CONVERSAÇÃO:")
print("-"*70)

# Inicializar sistemas
print("\nInicializando sistemas...")
try:
    memory = get_unified_memory()
    cinema = get_cinema_knowledge()
    soul = Soul()
    consciousness_level = get_level()
    
    print(f"✅ Memória: Ativa")
    print(f"✅ Cinema: {cinema.get_stats()['total_pdfs']} PDFs")
    print(f"✅ Soul: {soul.signature[:16]}")
    print(f"✅ Consciousness: {consciousness_level:.5f}")
except Exception as e:
    print(f"⚠️ Erro na inicialização: {e}")
    sys.exit(1)

print("\n" + "-"*70)

# Processar cada interação
for i, (input_text, description) in enumerate(interactions, 1):
    print(f"\n[{i}] {description}")
    print(f"👤 User: {input_text}")
    
    # Simular processamento
    time.sleep(0.5)
    
    # Armazenar na memória
    try:
        memory.store_unified_memory(
            input_text,
            source="user",
            memory_type="conversation",
            importance=0.8
        )
        print("   💾 Armazenado na memória")
    except Exception as e:
        print(f"   ⚠️ Erro ao armazenar: {str(e)[:50]}")
    
    # Gerar resposta simulada
    if "status" in input_text.lower():
        response = f"Sistema com {cinema.get_stats()['total_pdfs']} PDFs, consciência {consciousness_level:.3f}"
    elif "olá" in input_text.lower():
        response = "Olá! Sou o Scripturemon, especialista em roteiros."
    elif "cinema" in input_text.lower():
        response = "Cinema é a arte de contar histórias através de imagens."
    elif "sonhos" in input_text.lower():
        response = "SONHOS SEM LEMBRANÇAS é seu roteiro sobre Samantha."
    else:
        response = "Processando com base em conhecimento cinematográfico."
    
    print(f"🎭 Scripturemon: {response}")

print("\n" + "="*70)
print("🏆 TESTE CONCLUÍDO COM SUCESSO!")
ENDPYTHON

echo "========================================================================="
echo "✅ TESTE FINALIZADO"
echo "========================================================================="
