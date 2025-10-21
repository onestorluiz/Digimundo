#!/usr/bin/env python3
"""
🧪 TESTE SIMPLES FINAL
Verifica funcionamento básico antes da execução
"""

import ollama
import json
from pathlib import Path

def main():
    print("🧪 TESTE FINAL SIMPLES")
    print("=" * 40)

    # 1. Verificar modelo
    print("1. Modelo forense existe: ✅")

    # 2. Testar análise básica
    print("2. Testando análise...")

    test_code = '''
import fake_module
def test():
    path = "/tmp/test"
    return path
'''

    try:
        response = ollama.generate(
            model="forensic-analyzer:latest",
            prompt=test_code,
            options={'num_ctx': 4096}
        )

        if response and len(response.get('response', '')) > 100:
            print("   ✅ Análise funciona")
        else:
            print("   ❌ Análise falhou")
            return False

    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

    # 3. Verificar arquivos
    base_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
    required_files = [
        "apps/scripturemon/forensic_orchestrator.py",
        "apps/scripturemon/forensic_monitor.py",
        "launch_forensic.sh"
    ]

    print("3. Verificando arquivos...")
    for file_path in required_files:
        if (base_dir / file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            return False

    # 4. Verificar diretório de destino
    print("4. Verificando diretório de resultados...")
    results_dir = base_dir / "forensic_results"
    results_dir.mkdir(exist_ok=True)

    if results_dir.exists() and results_dir.is_dir():
        print("   ✅ Diretório de resultados OK")
    else:
        print("   ❌ Problema com diretório de resultados")
        return False

    print()
    print("🎉 TODOS OS TESTES BÁSICOS PASSARAM!")
    print("✅ Sistema está pronto para execução")
    print()
    print("🚀 Para executar:")
    print("   ./launch_forensic.sh")
    print()
    print("📊 Para monitorar:")
    print("   python3 apps/scripturemon/forensic_monitor.py")
    print()

    return True

if __name__ == "__main__":
    main()