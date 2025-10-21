#!/usr/bin/env python3
"""
Executa análise completa do roteiro com SCRIPTUREMON ULTIMATE
Sistema com 24 especialistas + Ollama
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Adicionar paths necessários
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-ultimate')
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-ultimate/src')

from src.core.scripturemon_ultimate_system import ScripturemonUltimateSystem

def main():
    print("🎬 SCRIPTUREMON ULTIMATE - ANÁLISE COMPLETA")
    print("=" * 60)
    print("Sistema: 24 Especialistas Sequenciais")
    print("Roteiro: Sonhos Sem Lembranças")
    print("=" * 60)

    # Configurar sistema com timeout maior
    system = ScripturemonUltimateSystem(
        orchestrator_model="mixtral:8x7b-instruct-v0.1-q5_K_M",
        evaluator_model="llama3.1:70b-instruct-q4_K_M",
        output_dir="analysis_reports"
    )

    # Ajustar timeout
    system.timeout = 120  # 2 minutos por especialista

    # Carregar roteiro
    screenplay_path = '/Users/clubproducoes/Digimundo/scripturemon-Omega/content/screenplays/personal/sonhos_sem_lembrancas_t3.txt'

    with open(screenplay_path, 'r', encoding='utf-8') as f:
        screenplay = f.read()

    print(f"📄 Roteiro carregado: {len(screenplay):,} caracteres")
    print(f"📊 Aproximadamente {len(screenplay.splitlines())} linhas")
    print("")
    print("⏳ Iniciando análise com 24 especialistas...")
    print("   Tempo estimado: 15-30 minutos")
    print("")

    # Usar apenas as primeiras páginas para análise mais rápida
    # (roteiro completo demora muito)
    screenplay_sample = screenplay[:20000]  # ~10 páginas

    try:
        # Executar análise
        result = system.analyze_screenplay(
            screenplay_sample,
            title="Sonhos Sem Lembranças"
        )

        # Salvar resultado
        output_file = Path(f"analysis_reports/sonhos_sem_lembrancas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print("")
        print("=" * 60)
        print("✅ ANÁLISE COMPLETA!")
        print(f"📁 Resultado salvo em: {output_file}")
        print("=" * 60)

        # Exibir resumo
        if result and 'analysis' in result:
            print("\n📊 RESUMO DA ANÁLISE:")
            print("-" * 40)

            analysis = result['analysis']

            # Contar especialistas que completaram
            completed = len([s for s in analysis if s.get('content', '').strip()])
            print(f"✅ Especialistas completos: {completed}/24")

            # Mostrar primeiros 3 especialistas
            for i, specialist in enumerate(analysis[:3]):
                if specialist.get('content'):
                    print(f"\n{specialist['name']}:")
                    print(f"  {specialist['content'][:200]}...")

            print("\n[...mais 21 especialistas...]")

    except Exception as e:
        print(f"❌ Erro durante análise: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()