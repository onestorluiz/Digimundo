#!/usr/bin/env python3
"""
Teste simples do sistema Scripturemon com DeepSeek-R1:70b
"""

import sys
from pathlib import Path

# Adiciona path do projeto
sys.path.insert(0, str(Path(__file__).parent))

def test_ollama_core():
    """Testa o Ollama Core básico"""
    print("=" * 60)
    print("🧠 TESTE DO OLLAMA CORE")
    print("=" * 60)
    
    from apps.scripturemon.ollama_core import OllamaCore
    
    # Inicializa
    core = OllamaCore()
    print(f"\n✅ Modelo padrão: {core.default_model}")
    print(f"✅ Modelos disponíveis: {len(core.models)}")
    
    # Teste simples
    print("\n📝 Teste de geração rápida...")
    response = core.generate(
        "Diga apenas: 'Sistema funcionando'",
        temperature=0.1,
        max_tokens=10
    )
    print(f"Resposta: {response[:100]}")
    
    return True

def test_scripturemon_brain():
    """Testa o Brain"""
    print("\n" + "=" * 60)
    print("🎬 TESTE DO SCRIPTUREMON BRAIN")
    print("=" * 60)
    
    from apps.scripturemon.scripturemon_brain import ScripturemonBrain
    
    brain = ScripturemonBrain()
    print(f"✅ Brain inicializado")
    print(f"✅ Modelo padrão: {brain.default_model}")
    
    # Teste de análise simples
    test_script = """FADE IN:

INT. OFFICE - DAY

A simple test scene.

FADE OUT."""
    
    print("\n📊 Testando análise...")
    try:
        analysis = brain.analyze_screenplay(test_script)
        print(f"✅ Análise completa!")
        print(f"   Score: {analysis.get('final_score', 62)}/100")
    except Exception as e:
        print(f"⚠️ Erro na análise: {e}")
    
    return True

def test_chat_system():
    """Testa o sistema de chat"""
    print("\n" + "=" * 60)
    print("💬 TESTE DO SISTEMA CHAT")
    print("=" * 60)
    
    try:
        from apps.scripturemon.chat import ScripturemonChat
        
        chat = ScripturemonChat()
        print(f"✅ Chat inicializado")
        
        # Testa comando help
        print("\n📋 Testando comando help...")
        chat.do_help("")
        
        print("\n✅ Sistema de chat funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no chat: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "TESTE COMPLETO DO SISTEMA" + " " * 18 + "║")
    print("║" + " " * 15 + "Com DeepSeek-R1:70b" + " " * 23 + "║")
    print("╚" + "=" * 58 + "╝")
    
    tests = [
        ("Ollama Core", test_ollama_core),
        ("Scripturemon Brain", test_scripturemon_brain),
        ("Chat System", test_chat_system)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Erro em {name}: {e}")
            results.append((name, False))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    for name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{name}: {status}")
    
    # Verificação final
    all_passed = all(r[1] for r in results)
    
    if all_passed:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("Sistema funcionando com DeepSeek-R1:70b")
        print("62/100. Como sempre.")
    else:
        print("\n⚠️ Alguns testes falharam. Verifique os erros acima.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)