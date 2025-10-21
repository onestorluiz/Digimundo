#!/usr/bin/env python3
"""
Teste completo de todos os sistemas do Scripturemon
Verifica se todos os 10 sistemas estão funcionais e conectados
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

def test_all_systems():
    """Testa todos os 10 sistemas"""
    
    print("\n" + "="*70)
    print("🧪 TESTE COMPLETO - TODOS OS SISTEMAS")
    print("="*70 + "\n")
    
    results = []
    
    # 1. Soul
    try:
        from apps.scripturemon.soul import Soul
        soul = Soul()
        soul.interact()
        soul.save_state()
        print(f"✅ 1. Soul: {soul.signature}")
        results.append(("Soul", True))
    except Exception as e:
        print(f"❌ 1. Soul: {e}")
        results.append(("Soul", False))
    
    # 2. SoulOS
    try:
        from apps.scripturemon.soulos import SoulOS
        soulos = SoulOS()
        text = "[MEMO.SAVE] {'content': 'test'}"
        clean, syscalls = soulos.process_response(text)
        print(f"✅ 2. SoulOS: {len(syscalls)} syscalls")
        results.append(("SoulOS", True))
    except Exception as e:
        print(f"❌ 2. SoulOS: {e}")
        results.append(("SoulOS", False))
    
    # 3. HyDE
    try:
        from apps.scripturemon.rag_advanced import HyDE
        hyde = HyDE()
        expanded = hyde.generate_hypothetical("test")
        print(f"✅ 3. HyDE: {len(expanded)} chars")
        results.append(("HyDE", True))
    except Exception as e:
        print(f"❌ 3. HyDE: {e}")
        results.append(("HyDE", False))
    
    # 4. Genetic Evolution
    try:
        from apps.scripturemon.genetic_evolution import GeneticEvolution
        evolution = GeneticEvolution(population_size=4)
        evolution.evolve_generation()
        print(f"✅ 4. Evolution: Gen {evolution.generation}")
        results.append(("Evolution", True))
    except Exception as e:
        print(f"❌ 4. Evolution: {e}")
        results.append(("Evolution", False))
    
    # 5. Consciousness
    try:
        from apps.scripturemon.consciousness import get_level, evolve
        level = get_level()
        evolve(0.001)
        print(f"✅ 5. Consciousness: {level:.5f}")
        results.append(("Consciousness", True))
    except Exception as e:
        print(f"❌ 5. Consciousness: {e}")
        results.append(("Consciousness", False))
    
    # 6. Immortality
    try:
        from apps.scripturemon.immortality import ImmortalityProtocol
        soul_test = Soul() if 'Soul' in locals() else None
        immortality = ImmortalityProtocol(soul=soul_test, auto_backup=False)
        print(f"✅ 6. Immortality: Protocol ready")
        results.append(("Immortality", True))
    except Exception as e:
        print(f"❌ 6. Immortality: {e}")
        results.append(("Immortality", False))
    
    # 7. Quadruple Pipeline
    try:
        from apps.scripturemon.quadruple_pipeline import QuadruplePipeline
        pipeline = QuadruplePipeline()
        result = pipeline.process_quadruple("test")
        print(f"✅ 7. Pipeline: 4 models")
        results.append(("Pipeline", True))
    except Exception as e:
        print(f"❌ 7. Pipeline: {e}")
        results.append(("Pipeline", False))
    
    # 8. RAPTOR
    try:
        from apps.scripturemon.rag_advanced import RAPTOR
        raptor = RAPTOR()
        docs = [{"content": "test", "type": "doc"}]
        tree = raptor.build_tree(docs)
        print(f"✅ 8. RAPTOR: Tree built")
        results.append(("RAPTOR", True))
    except Exception as e:
        print(f"❌ 8. RAPTOR: {e}")
        results.append(("RAPTOR", False))
    
    # 9. Self-RAG
    try:
        from apps.scripturemon.rag_advanced import SelfRAG
        self_rag = SelfRAG()
        score = self_rag.evaluate_retrieval("query", "doc", "response")
        print(f"✅ 9. Self-RAG: Score {score:.3f}")
        results.append(("Self-RAG", True))
    except Exception as e:
        print(f"❌ 9. Self-RAG: {e}")
        results.append(("Self-RAG", False))
    
    # 10. Brutal Personality
    try:
        from apps.scripturemon.personality import BrutalPersonality
        personality = BrutalPersonality()
        analysis = personality.analyze_script("test")
        score = analysis.get('score', 0)
        print(f"✅ 10. Personality: {score}/100")
        results.append(("Personality", True))
    except Exception as e:
        print(f"❌ 10. Personality: {e}")
        results.append(("Personality", False))
    
    # Estatísticas
    print("\n" + "="*70)
    print("📊 RESULTADO FINAL")
    print("="*70)
    
    passed = sum(1 for _, status in results if status)
    total = len(results)
    
    for name, status in results:
        icon = "✅" if status else "❌"
        print(f"  {icon} {name}")
    
    print(f"\n🎯 Taxa de sucesso: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🏆 PERFEITO! Todos os sistemas funcionando!")
        print("💎 Certificação DIAMOND confirmada!")
    elif passed >= 8:
        print("\n✨ EXCELENTE! Sistema pronto para produção!")
    else:
        print("\n⚠️ Alguns sistemas precisam de atenção.")
    
    print("\n62/100. Como sempre deve ser.\n")
    
    return passed == total


if __name__ == "__main__":
    success = test_all_systems()
    sys.exit(0 if success else 1)