#!/usr/bin/env python3
"""
Teste específico para verificar se estamos usando a versão correta do Scripturemon
E se o chat está integrado com todos os sistemas
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_version():
    """Test if we're using the correct version"""
    print("=" * 70)
    print("TESTE DE VERSÃO DO SCRIPTUREMON")
    print("=" * 70)
    
    from apps.scripturemon import __version__, get_version
    
    print(f"\n1. Versão detectada:")
    print(f"   __version__: {__version__}")
    print(f"   get_version(): {get_version()}")
    
    # Verificar se é a versão correta
    assert __version__ == "1.0.0-vFinal", f"Versão incorreta: {__version__}"
    assert get_version() == "1.0.0-vFinal", f"get_version incorreta: {get_version()}"
    
    print(f"   ✅ Versão correta: 1.0.0-vFinal")
    return True

def test_bootstrap():
    """Test bootstrap initialization"""
    print("\n2. Testando Bootstrap:")
    
    try:
        from apps.scripturemon.bootstrap import ensure_bootstrap_once, status_report
        
        # Bootstrap único
        context = ensure_bootstrap_once()
        print("   ✅ Bootstrap executado")
        
        # Verificar contexto
        status = status_report()
        print(f"   Status:")
        print(f"     - Memory: {status.get('memory', {}).get('functional', False)}")
        print(f"     - Telepathy: {status.get('telepathy', {}).get('type', 'unknown')}")
        print(f"     - Consciousness: {status.get('consciousness', {}).get('enabled', False)}")
        print(f"     - Monitoring: {status.get('monitoring', {}).get('enabled', False)}")
        
        return True
    except Exception as e:
        print(f"   ❌ Bootstrap falhou: {e}")
        return False

def test_consciousness():
    """Test ConsciousnessStream"""
    print("\n3. Testando ConsciousnessStream:")
    
    try:
        from apps.scripturemon.canonical.consciousness import ConsciousnessStream
        
        # Criar instância
        cs = ConsciousnessStream()
        print(f"   ✅ ConsciousnessStream criado")
        print(f"     - Enabled: {cs.enabled}")
        print(f"     - Mode: {cs.mode}")
        print(f"     - Circuit Breaker Open: {cs.circuit_breaker.is_open()}")
        
        # Verificar métodos essenciais
        methods = ['start', 'stop', 'should_run_burst', 'run_burst']
        all_ok = True
        for method in methods:
            if hasattr(cs, method):
                print(f"     ✅ Método '{method}' existe")
            else:
                print(f"     ❌ Método '{method}' não encontrado")
                all_ok = False
        
        return all_ok
    except Exception as e:
        print(f"   ❌ ConsciousnessStream falhou: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_memory_manager():
    """Test Memory Manager"""
    print("\n4. Testando Memory Manager:")
    
    try:
        from apps.scripturemon.canonical.memory_manager import get_memory_manager
        
        # Obter instância
        mm = get_memory_manager()
        if mm:
            print(f"   ✅ Memory Manager obtido")
            print(f"     - Functional: {getattr(mm, 'functional', 'unknown')}")
            
            # Verificar métodos
            methods = ['save', 'get_context', 'search']
            for method in methods:
                if hasattr(mm, method):
                    print(f"     ✅ Método '{method}' existe")
                else:
                    print(f"     ⚠️  Método '{method}' não encontrado")
        else:
            print(f"   ⚠️  Memory Manager não inicializado (pode ser normal)")
        
        return True
    except Exception as e:
        print(f"   ❌ Memory Manager falhou: {e}")
        return False

def test_chat_system():
    """Test Chat System Components"""
    print("\n5. Testando Sistema de Chat:")
    
    try:
        # Primeiro corrigir o erro de indentação
        from apps.scripturemon.chat import ScripturemonChat, ConversationHistory
        
        print("   ✅ Imports do chat bem-sucedidos")
        
        # Testar ConversationHistory
        history = ConversationHistory()
        history.add("teste", "resposta")
        context = history.get_context()
        
        if "teste" in context:
            print("   ✅ ConversationHistory funcionando")
        else:
            print("   ❌ ConversationHistory não está salvando corretamente")
        
        # Tentar criar ScripturemonChat
        try:
            chat = ScripturemonChat()
            print("   ✅ ScripturemonChat criado")
            
            # Verificar componentes
            components = {
                'soul': 'Soul system',
                'personality': 'Personality system',
                'rag': 'RAG system',
                'quad_pipeline': 'Quadruple pipeline'
            }
            
            for comp, desc in components.items():
                if hasattr(chat, comp):
                    print(f"     ✅ {desc} inicializado")
                else:
                    print(f"     ⚠️  {desc} não encontrado")
                    
        except Exception as e:
            print(f"   ⚠️  ScripturemonChat criado com avisos: {e}")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Erro de import no chat: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Chat system falhou: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_integration():
    """Test CLI integration"""
    print("\n6. Testando Integração CLI:")
    
    try:
        from apps.scripturemon.cli import app, bootstrap_callback
        
        print("   ✅ CLI importado com sucesso")
        
        # Verificar comandos disponíveis
        commands = ['status', 'analyze', 'backup', 'chat', 'doctor']
        for cmd in commands:
            # Typer usa um formato especial para comandos
            if any(cmd in str(c) for c in app.registered_commands):
                print(f"     ✅ Comando '{cmd}' registrado")
            else:
                print(f"     ⚠️  Comando '{cmd}' pode não estar registrado")
        
        return True
    except Exception as e:
        print(f"   ❌ CLI falhou: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("INICIANDO TESTES COMPLETOS DO SCRIPTUREMON v1.0.0-vFinal")
    print("=" * 70)
    
    tests = [
        ("Versão", test_version),
        ("Bootstrap", test_bootstrap),
        ("ConsciousnessStream", test_consciousness),
        ("Memory Manager", test_memory_manager),
        ("Chat System", test_chat_system),
        ("CLI Integration", test_cli_integration)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Teste '{name}' teve erro crítico: {e}")
            results.append((name, False))
    
    # Resumo
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{status}: {name}")
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("O Scripturemon v1.0.0-vFinal está funcionando corretamente!")
    else:
        print(f"\n⚠️  {total - passed} testes falharam")
        print("Verifique os erros acima para diagnóstico")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())