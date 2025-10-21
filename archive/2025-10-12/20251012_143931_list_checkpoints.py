#!/usr/bin/env python3
"""
Lista checkpoints disponíveis - Scripturemon
Uso: python3 list_checkpoints.py [--interactive]

Sem argumentos: apenas lista os checkpoints
Com --interactive: abre dialog com botões para selecionar
"""

import sys
from checkpoint_manager_improved import find_incomplete_checkpoints, prompt_user_with_buttons

def main():
    # Check if interactive mode
    interactive = "--interactive" in sys.argv or "-i" in sys.argv

    print("🔍 BUSCANDO ANÁLISES INCOMPLETAS...\n")

    checkpoints = find_incomplete_checkpoints()

    if not checkpoints:
        print("✅ Nenhuma análise incompleta encontrada")
        print("   Todas as análises foram concluídas ou não há análises em andamento.\n")
        return

    # Listar checkpoints no terminal
    print(f"📋 Encontradas {len(checkpoints)} análise(s) incompleta(s):\n")
    print("="*70)

    for i, cp in enumerate(checkpoints, 1):
        print(f"\n{i}. {cp.folder.name}")
        print(f"   📄 Roteiro: {cp.screenplay_name}")
        print(f"   🤖 Modelo: {cp.model}")
        print(f"   📊 Progresso: {cp.progress[0]}/{cp.progress[1]} ({cp.percentage:.1f}%)")
        print(f"   🔬 Último completo: {cp.current_specialist} × {cp.current_author}")

        resume = cp.get_resume_point()
        if resume:
            print(f"   ▶️  Próximo: {resume[0]} × {resume[1]}")

        if cp.last_update:
            print(f"   🕐 Atualizado: {cp.last_update}")

        print(f"   📁 Pasta: {cp.folder}")

    print("\n" + "="*70)

    # Se modo interativo, mostrar dialog
    if interactive:
        print("\n🎯 Abrindo seletor interativo...\n")
        selected = prompt_user_with_buttons()

        if selected:
            print(f"\n✅ Você selecionou: {selected.folder.name}")
            print(f"\n💡 Para continuar esta análise, use:")
            print(f"   python3 analyze_all_specialists.py \"{selected.screenplay_name}\" --resume")
        else:
            print(f"\n💡 Para começar nova análise, use:")
            print(f"   python3 analyze_all_specialists.py <roteiro.pdf>")
    else:
        print(f"\n💡 Para continuar uma análise, use:")
        print(f"   python3 analyze_all_specialists.py <roteiro.pdf> --resume")
        print(f"\n💡 Para modo interativo (com botões), use:")
        print(f"   python3 list_checkpoints.py --interactive\n")

if __name__ == "__main__":
    main()
