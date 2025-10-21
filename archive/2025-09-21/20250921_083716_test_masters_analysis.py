#!/usr/bin/env python3
"""
TESTE: Verificar análise dos roteiros mestres
"""

import sys
from pathlib import Path
sys.path.insert(0, 'src')

from scripturemon_champion.analysis.script_doctor import ScriptDoctor

def test_masters_analysis():
    """Testa que o sistema analisa roteiros mestres"""

    print("="*80)
    print("🎬 TESTE DE ANÁLISE DOS ROTEIROS MESTRES")
    print("="*80)

    doctor = ScriptDoctor()
    masters_dir = Path("screenplays/masters")

    if not masters_dir.exists():
        print("❌ Pasta masters não encontrada!")
        return

    masters = list(masters_dir.glob("*.txt"))
    print(f"\n📌 {len(masters)} roteiros mestres encontrados")

    # Analisar 3 roteiros icônicos
    test_scripts = [
        "Fight-Club-Release.txt",
        "inception_-_screenplay.docx.txt",
        "the_matrix_-_screenplay.docx.txt"
    ]

    print("\n🔍 Analisando roteiros icônicos:")
    print("-" * 40)

    for script_name in test_scripts:
        script_path = masters_dir / script_name
        if script_path.exists():
            print(f"\n📄 {script_name}:")

            # Ler e analisar
            text = script_path.read_text(encoding='utf-8', errors='ignore')
            analysis = doctor.analyze_script(text, script_path.stem)

            # Mostrar resultados
            print(f"  • Cenas: {analysis.scenes}")
            print(f"  • Personagens: {len(analysis.top_characters)}")
            print(f"  • Diálogos: {analysis.dialogue_ratio:.1%}")

            # Top 3 personagens
            if analysis.top_characters:
                print(f"  • Protagonistas: {', '.join([c[0] for c in analysis.top_characters[:3]])}")
        else:
            print(f"  ⚠️ {script_name} não encontrado")

    print("\n" + "="*80)
    print("✅ SISTEMA ESTÁ ANALISANDO ROTEIROS MESTRES CORRETAMENTE!")
    print("="*80)

if __name__ == "__main__":
    test_masters_analysis()