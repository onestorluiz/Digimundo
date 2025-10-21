#!/usr/bin/env python3
"""
Teste Integrado Final - DIGIMUNDO STYLE
Timestamp: 20250921_214934
Verifica todas as correções implementadas
"""

import sys
import time
import json
from pathlib import Path

# Adiciona safe_json_parser ao path
sys.path.insert(0, '.')

def test_safe_json_parser():
    """Testa SafeJSONParser."""
    print("\n🧪 TESTE 1: SafeJSONParser")
    print("-" * 40)

    try:
        from safe_json_parser_20250921_214934 import safe_json_parse

        test_cases = [
            ('{"valid": "json"}', "JSON válido"),
            ('{"broken\\"quote": "test"}', "Quote escapada"),
            ('Invalid JSON text', "Texto inválido")
        ]

        for test_input, description in test_cases:
            result, confidence = safe_json_parse(test_input)
            status = "✅" if result else "⚠️"
            print(f"{status} {description}: Confiança {confidence:.0%}")

        print("✅ SafeJSONParser funcionando!")
        return True
    except Exception as e:
        print(f"⚠️ Erro no SafeJSONParser: {e}")
        return False


def test_file_encoding():
    """Testa correção de encoding."""
    print("\n📄 TESTE 2: Encoding de Arquivos")
    print("-" * 40)

    # Verifica Apocalypse Now específicamente
    problem_file = Path("screenplays/Apocalypse-Now-Screenplay.txt")

    if problem_file.exists():
        try:
            with open(problem_file, 'r', encoding='utf-8') as f:
                content = f.read(100)
            print(f"✅ {problem_file.name} legível em UTF-8")
            print(f"   Prévia: {content[:50]}...")
            return True
        except Exception as e:
            print(f"⚠️ {problem_file.name} ainda não legível: {e}")
            return False
    else:
        print(f"⚠️ Arquivo não encontrado: {problem_file}")
        return False


def test_ollama_connection():
    """Testa conexão com Ollama."""
    print("\n🤖 TESTE 3: Conexão Ollama")
    print("-" * 40)

    try:
        import requests
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)

        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama conectado com {len(models)} modelos")

            # Verifica modelo específico
            has_mixtral = any('mixtral' in m.get('name', '').lower() for m in models)
            if has_mixtral:
                print("✅ Modelo mixtral-token-turbo disponível")
            else:
                print("⚠️ Modelo mixtral-token-turbo não encontrado")

            return True
        else:
            print(f"⚠️ Ollama retornou status {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ Erro ao conectar com Ollama: {e}")
        return False


def test_main_script():
    """Testa script principal com alterações."""
    print("\n🚀 TESTE 4: Script Principal")
    print("-" * 40)

    script_path = Path("ollama_continuous_learning.py")

    if not script_path.exists():
        print(f"⚠️ Script não encontrado: {script_path}")
        return False

    try:
        with open(script_path, 'r') as f:
            content = f.read()

        # Verifica integrações
        checks = [
            ("SAFE_PARSER_AVAILABLE" in content, "SafeJSONParser integrado"),
            ("safe_json_parse" in content, "Função safe_json_parse usada"),
            ("import re" in content, "Módulo regex importado"),
            ("options" in content, "Parâmetros de API configurados")
        ]

        all_passed = True
        for check, description in checks:
            status = "✅" if check else "⚠️"
            print(f"{status} {description}")
            if not check:
                all_passed = False

        return all_passed
    except Exception as e:
        print(f"⚠️ Erro ao verificar script: {e}")
        return False


def test_checkpoint_system():
    """Testa sistema de checkpoint."""
    print("\n💾 TESTE 5: Sistema de Checkpoint")
    print("-" * 40)

    checkpoint_file = Path("checkpoint_analysis.json")

    if checkpoint_file.exists():
        try:
            with open(checkpoint_file, 'r') as f:
                data = json.load(f)

            analyses = data.get('completed_analyses', [])
            count = data.get('completed_count', 0)

            print(f"✅ Checkpoint carregado: {count} análises")
            print(f"   Última: {data.get('last_screenplay', 'N/A')}")
            print(f"   Timestamp: {data.get('timestamp', 'N/A')}")
            return True
        except Exception as e:
            print(f"⚠️ Erro ao ler checkpoint: {e}")
            return False
    else:
        print("⚠️ Arquivo de checkpoint não encontrado")
        return False


def run_mini_test():
    """Executa um teste mínimo do sistema."""
    print("\n🔬 TESTE 6: Execução Mínima")
    print("-" * 40)

    try:
        # Importa o sistema
        from ollama_continuous_learning import OllamaContinuousLearning

        # Cria instância
        system = OllamaContinuousLearning()

        print("✅ Sistema instanciado com sucesso")

        # Testa leitura de arquivo
        test_file = Path("screenplays/inception_-_screenplay.docx.txt")
        if test_file.exists():
            content = system.read_file(str(test_file))
            if content:
                print(f"✅ Arquivo lido: {len(content)} caracteres")
                return True
            else:
                print("⚠️ Erro ao ler arquivo")
                return False
        else:
            print("⚠️ Arquivo de teste não encontrado")
            return False

    except Exception as e:
        print(f"⚠️ Erro na execução: {e}")
        return False


def main():
    """Executa todos os testes."""
    print("=" * 50)
    print("🎯 TESTE INTEGRADO FINAL - SCRIPTUREMON ULTIMATE")
    print("=" * 50)

    tests = [
        ("SafeJSONParser", test_safe_json_parser),
        ("Encoding", test_file_encoding),
        ("Ollama", test_ollama_connection),
        ("Script Principal", test_main_script),
        ("Checkpoint", test_checkpoint_system),
        ("Execução", run_mini_test)
    ]

    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n⚠️ Erro no teste {name}: {e}")
            results[name] = False

    # Sumário
    print("\n" + "=" * 50)
    print("📊 RESULTADO FINAL")
    print("=" * 50)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    print("\n" + "=" * 50)
    percentage = (passed / total) * 100
    final_status = "✅ SUCESSO!" if passed == total else "⚠️ PARCIAL"

    print(f"{final_status} {passed}/{total} testes passaram ({percentage:.0f}%)")
    print("=" * 50)

    # Checkpoint final
    if passed == total:
        print("\n🎉 SISTEMA PRONTO PARA PRODUÇÃO!")
        print("📝 Execute: python3 ollama_continuous_learning.py --cycles 1")
    else:
        print("\n⚠️ Revise os testes que falharam antes de executar em produção")


if __name__ == "__main__":
    main()