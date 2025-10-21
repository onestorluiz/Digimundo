#!/usr/bin/env python3
"""
Test script for new export functions:
- DrDialogue.export_dialogue_features()
- TheoryIndexer.export_text_chunks()
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from specialists.implementations.character_dialogue_specialist import DrDialogue
from core.theory_indexer import get_theory_indexer


def test_dialogue_export():
    """Test DrDialogue.export_dialogue_features()"""
    print("="*70)
    print("🔬 TESTE 1: DrDialogue.export_dialogue_features()")
    print("="*70)

    # Load test screenplay
    screenplay_path = Path(__file__).parent / "content" / "screenplays" / "personal" / "sonhos_sem_lembrancas_t3.txt"

    if not screenplay_path.exists():
        print(f"❌ Roteiro não encontrado: {screenplay_path}")
        return False

    screenplay_text = screenplay_path.read_text(errors='ignore')[:5000]  # First 5000 chars
    print(f"📖 Roteiro: {screenplay_path.name} ({len(screenplay_text)} chars)")

    # Create specialist
    dr_dialogue = DrDialogue()

    # Export dialogue features
    print("\n⏳ Exportando features de diálogo...")
    windows = dr_dialogue.export_dialogue_features(screenplay_text, window_size=5)

    if not windows:
        print("⚠️ Nenhuma janela de diálogo encontrada")
        return False

    print(f"\n✅ {len(windows)} janelas exportadas\n")

    # Show first window
    print("📊 Primeira janela:")
    print(json.dumps(windows[0], indent=2, ensure_ascii=False))

    # Validate structure
    required_keys = ["text", "window_id", "character_count", "characters", "style", "meta"]
    for key in required_keys:
        if key not in windows[0]:
            print(f"❌ Falta chave obrigatória: {key}")
            return False

    print("\n✅ Estrutura validada!")
    return True


def test_theory_export():
    """Test TheoryIndexer.export_text_chunks()"""
    print("\n" + "="*70)
    print("🔬 TESTE 2: TheoryIndexer.export_text_chunks()")
    print("="*70)

    # Get indexer
    print("\n⏳ Carregando indexador...")
    indexer = get_theory_indexer()

    stats = indexer.get_stats()
    print(f"📚 Indexador: {stats['books_indexed']} livros, {stats['total_chunks']} chunks")

    # Export first 5 chunks
    print("\n⏳ Exportando primeiros 5 chunks...")
    chunks = indexer.export_text_chunks(limit=5)

    if not chunks:
        print("❌ Nenhum chunk exportado")
        return False

    print(f"\n✅ {len(chunks)} chunks exportados\n")

    # Show first chunk (truncated)
    print("📚 Primeiro chunk:")
    first_chunk = chunks[0].copy()
    first_chunk['text'] = first_chunk['text'][:200] + "..."  # Truncate for display
    print(json.dumps(first_chunk, indent=2, ensure_ascii=False))

    # Validate structure
    required_keys = ["text", "book", "chunk_id", "word_count", "meta"]
    for key in required_keys:
        if key not in chunks[0]:
            print(f"❌ Falta chave obrigatória: {key}")
            return False

    print("\n✅ Estrutura validada!")

    # Test with book filter
    print("\n⏳ Testando filtro por livro (Dialogue)...")
    dialogue_chunks = indexer.export_text_chunks(book_filter="Dialogue", limit=3)
    print(f"✅ {len(dialogue_chunks)} chunks do livro 'Dialogue'")

    return True


def test_combined_usage():
    """Example of using both exports together"""
    print("\n" + "="*70)
    print("🔥 TESTE 3: Uso Combinado (Roteiro + Teoria)")
    print("="*70)

    # Get both data sources
    dr_dialogue = DrDialogue()
    indexer = get_theory_indexer()

    screenplay_path = Path(__file__).parent / "content" / "screenplays" / "personal" / "sonhos_sem_lembrancas_t3.txt"
    screenplay_text = screenplay_path.read_text(errors='ignore')[:5000]

    # Export both
    dialogue_windows = dr_dialogue.export_dialogue_features(screenplay_text, window_size=10)
    theory_chunks = indexer.export_text_chunks(book_filter="Dialogue", limit=10)

    print(f"\n📊 Dados disponíveis para correlação:")
    print(f"   Janelas de diálogo: {len(dialogue_windows)}")
    print(f"   Chunks de teoria:   {len(theory_chunks)}")

    # Calculate total text
    dialogue_text_size = sum(len(w['text']) for w in dialogue_windows)
    theory_text_size = sum(len(c['text']) for c in theory_chunks)

    print(f"\n📏 Tamanho de texto:")
    print(f"   Diálogo: {dialogue_text_size:,} chars")
    print(f"   Teoria:  {theory_text_size:,} chars")
    print(f"   Total:   {dialogue_text_size + theory_text_size:,} chars")

    print("\n✅ Dados prontos para indexação/correlação externa!")
    return True


if __name__ == "__main__":
    print("🔥🔥🔥 VALIDAÇÃO DE EXPORTS 🔥🔥🔥\n")

    results = []

    # Run tests
    results.append(("DrDialogue Export", test_dialogue_export()))
    results.append(("TheoryIndexer Export", test_theory_export()))
    results.append(("Combined Usage", test_combined_usage()))

    # Summary
    print("\n" + "="*70)
    print("📊 RESUMO DOS TESTES")
    print("="*70)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")

    all_passed = all(r[1] for r in results)
    print("\n" + ("🎉 TODOS OS TESTES PASSARAM!" if all_passed else "❌ ALGUNS TESTES FALHARAM"))

    sys.exit(0 if all_passed else 1)
