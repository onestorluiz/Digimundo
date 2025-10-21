#!/usr/bin/env python3
"""
Quick Start - Análise rápida de roteiro
Use: python3 quick_start.py <arquivo.txt>
"""

import sys
from pathlib import Path

# Setup path
sys.path.insert(0, 'src')

from scripturemon_champion.script_doctor import ScriptDoctorEnhanced
from scripturemon_champion.rag import search_documents
from scripturemon_champion.ollama import OllamaReal

def analyze_screenplay(file_path: str):
    """Análise completa de roteiro"""

    print("="*60)
    print(f"🎬 ANÁLISE DE ROTEIRO: {Path(file_path).name}")
    print("="*60)

    # Ler arquivo
    try:
        text = Path(file_path).read_text(encoding='utf-8')
        print(f"✅ Arquivo lido: {len(text):,} caracteres\n")
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return

    # Criar doctor
    doctor = ScriptDoctorEnhanced(use_ollama=True)

    # 1. Análise básica
    print("📊 ANÁLISE BÁSICA:")
    print("-"*40)
    analysis = doctor.analyze_script(text)

    print(f"Cenas: {analysis.scenes}")
    print(f"Personagens principais: {analysis.characters}")
    print(f"Palavras: {analysis.words:,}")
    print(f"Média palavras/cena: {analysis.avg_scene_len:.0f}")
    print(f"Ratio diálogo: {analysis.dialogue_ratio:.1%}")
    print(f"Score de ritmo: {analysis.pacing_score:.2f}")

    if analysis.top_characters:
        print(f"\nTop personagens:")
        for i, char in enumerate(analysis.top_characters[:5], 1):
            print(f"  {i}. {char}")

    if analysis.notes:
        print(f"\n⚠️  Notas:")
        for note in analysis.notes:
            print(f"  - {note}")

    # 2. Save the Cat
    print("\n🎬 SAVE THE CAT:")
    print("-"*40)
    stc = doctor.analyze_save_the_cat(text)

    print(f"Score estrutural: {stc.structure_score:.1%}")
    print(f"Beats encontrados: {len(stc.beats)}/{len(stc.beats) + len(stc.missing_beats)}")

    if stc.beats:
        print(f"\n✅ Beats identificados:")
        for beat in stc.beats[:5]:
            print(f"  - {beat.name.replace('_', ' ').title()} ({beat.position_pct:.0f}%): {beat.confidence:.1f}")

    if stc.missing_beats:
        print(f"\n❌ Beats faltando:")
        for beat_name in stc.missing_beats[:5]:
            print(f"  - {beat_name.replace('_', ' ').title()}")

    # 3. Buscar referências similares
    print("\n🔍 REFERÊNCIAS SIMILARES:")
    print("-"*40)

    # Extrair palavras-chave
    keywords = " ".join(analysis.top_characters[:2])
    if len(text) > 1000:
        keywords += " " + " ".join(text[:1000].split()[:10])

    results = search_documents(keywords, top_k=3)

    if results:
        print(f"Roteiros relacionados na biblioteca:")
        for i, r in enumerate(results, 1):
            category = r['doc_id'].split('/')[0]
            name = r['doc_id'].split('/')[1] if '/' in r['doc_id'] else r['doc_id']
            print(f"  {i}. [{category}] {name[:40]}... (score: {r['score']:.1f})")
    else:
        print("  Nenhuma referência similar encontrada")

    # 4. Análise com Ollama/Mixtral (se disponível)
    ollama = OllamaReal()
    if ollama.default_model and False:  # Desabilitado por padrão (demora)
        print("\n🤖 ANÁLISE PROFUNDA (Mixtral):")
        print("-"*40)

        prompt = f"""Analyze this screenplay excerpt and provide insights:

        Characters: {', '.join(analysis.top_characters[:3])}
        Scenes: {analysis.scenes}
        First 500 chars: {text[:500]}

        Provide: theme, tone, and one unique insight."""

        response = ollama.generate(prompt, temperature=0.7, max_tokens=150, timeout=10)

        if response.success:
            print(response.completion)
        else:
            print("  (Mixtral não disponível no momento)")

    print("\n" + "="*60)
    print("✅ ANÁLISE COMPLETA!")
    print("="*60)

def main():
    if len(sys.argv) < 2:
        # Modo interativo
        print("🎬 ScriptureMonChampion - Quick Start")
        print("-"*40)
        print("\nEscolha uma opção:")
        print("1. Analisar um dos roteiros da biblioteca")
        print("2. Analisar arquivo próprio")
        print("3. Buscar na biblioteca")
        print("4. Sair")

        choice = input("\nOpção: ").strip()

        if choice == "1":
            # Listar alguns roteiros
            from pathlib import Path
            screenplays = list(Path("data/screenplays").glob("*.txt"))[:10]

            print("\nRoteiros disponíveis:")
            for i, sp in enumerate(screenplays, 1):
                print(f"  {i}. {sp.stem[:50]}")

            idx = input("\nNúmero do roteiro: ").strip()
            try:
                file_path = screenplays[int(idx)-1]
                analyze_screenplay(str(file_path))
            except:
                print("❌ Seleção inválida")

        elif choice == "2":
            file_path = input("Caminho do arquivo: ").strip()
            analyze_screenplay(file_path)

        elif choice == "3":
            query = input("Buscar por: ").strip()
            results = search_documents(query, top_k=5)

            print(f"\n🔍 Resultados para '{query}':")
            for i, r in enumerate(results, 1):
                print(f"  {i}. {r['doc_id']}: {r['score']:.2f}")
                print(f"     {r['excerpt'][:100]}...")

        else:
            print("👋 Até logo!")

    else:
        # Modo arquivo
        analyze_screenplay(sys.argv[1])

if __name__ == "__main__":
    main()