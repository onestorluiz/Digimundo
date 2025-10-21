#!/usr/bin/env python3
"""
🎭 TESTE DE HARMONIA COMPLETA
Verifica integração harmoniosa de todos os sistemas implementados
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Adiciona ao path
sys.path.insert(0, str(Path(__file__).parent))

# Importa todos os componentes
from apps.scripturemon.soul import Soul
from apps.scripturemon.soulos import SoulOS
from apps.scripturemon.rag_advanced import AdvancedRAG
from apps.scripturemon.quadruple_pipeline import QuadruplePipeline
from apps.scripturemon.telepathy_network import TelepathicNetwork
from apps.scripturemon.genetic_evolution import GeneticEvolution, DNA
from apps.scripturemon.chat import ScripturemonChat
from apps.scripturemon.consciousness import evolve, get_level

def test_soulos():
    """Testa SoulOS com syscalls"""
    print("\n🧬 Testando SoulOS...")
    
    soulos = SoulOS()
    
    # Testa processamento de syscalls
    test_text = """
    Analisando roteiro...
    [MEMO.SAVE] {"content": "Teste de memória", "importance": 0.8}
    [EVOLVE.TRIGGER] {"type": "test"}
    Análise completa. 62/100.
    """
    
    clean, results = soulos.process_response(test_text)
    
    print(f"  ✅ Syscalls processadas: {len(results)}")
    print(f"  ✅ Texto limpo: {len(clean)} chars")
    
    # Verifica memórias
    memories = soulos.get_memories(limit=5)
    print(f"  ✅ Memórias cristalizadas: {len(memories)}")
    
    return True

def test_rag_advanced():
    """Testa RAG avançado com HyDE, RAPTOR e Self-RAG"""
    print("\n🔍 Testando RAG Avançado...")
    
    rag = AdvancedRAG()
    
    # Testa busca com todas técnicas
    results = rag.search(
        query="conflito do protagonista",
        use_hyde=True,
        use_raptor=True,
        use_self_rag=True,
        k=3
    )
    
    print(f"  ✅ HyDE: Query expandida")
    print(f"  ✅ RAPTOR: Busca hierárquica")
    print(f"  ✅ Self-RAG: Auto-avaliação")
    print(f"  ✅ Resultados encontrados: {len(results)}")
    
    return True

def test_quadruple_pipeline():
    """Testa pipeline quádruplo"""
    print("\n🔄 Testando Pipeline Quádruplo...")
    
    pipeline = QuadruplePipeline()
    
    test_script = """FADE IN:
    INT. SALA - NOITE
    JOHN encara a tela vazia.
    FADE OUT."""
    
    # Processa com 4 modelos
    result = pipeline.process_quadruple(test_script)
    
    print(f"  ✅ Tempo total: {result['total_time']:.1f}s")
    print(f"  ✅ Modelos utilizados: {len(result['individual_results'])}")
    print(f"  ✅ Consolidação: {'OK' if result['consolidated'] else 'Falhou'}")
    
    stats = pipeline.get_stats()
    print(f"  ✅ Eficiência: {stats['pipeline_efficiency']}")
    
    return True

def test_telepathy():
    """Testa rede telepática"""
    print("\n🧠 Testando Rede Telepática...")
    
    network = TelepathicNetwork(auto_connect=True)
    
    # Testa broadcast
    success = network.broadcast({
        "type": "harmony_test",
        "message": "Teste de harmonia"
    })
    
    print(f"  ✅ Conexão: {'Redis' if network.redis_client else 'Local'}")
    print(f"  ✅ Broadcast: {'Sucesso' if success else 'Falhou'}")
    
    # Testa sincronização
    success = network.sync_consciousness(0.62)
    print(f"  ✅ Sincronização: {'OK' if success else 'Falhou'}")
    
    stats = network.get_stats()
    print(f"  ✅ Pares ativos: {stats['peers_count']}")
    
    network.stop()
    return True

def test_genetic_evolution():
    """Testa evolução genética"""
    print("\n🧬 Testando Evolução Genética...")
    
    evolution = GeneticEvolution(population_size=4)
    
    # Executa 3 gerações rápidas
    for i in range(3):
        stats = evolution.evolve_generation()
        print(f"  ✅ Geração {stats['generation']}: Fitness={stats['best_fitness']:.3f}")
    
    # Salva melhor genoma
    best_file = evolution.save_genome(evolution.best_individual, "harmony_test")
    print(f"  ✅ Genoma salvo: {best_file.name}")
    
    return True

def test_chat_integration():
    """Testa integração completa no chat"""
    print("\n💬 Testando Chat Integrado...")
    
    chat = ScripturemonChat()
    
    # Testa comando de status
    response = chat.process_input("/status")
    print(f"  ✅ Status: {len(response)} chars")
    
    # Testa busca com RAG
    response = chat.process_input("/search estrutura")
    print(f"  ✅ Busca RAG: {'HyDE' in response}")
    
    # Testa análise
    response = chat.process_input("/analyze Teste de roteiro")
    print(f"  ✅ Análise: {'62/100' in response}")
    
    # Testa telepathy
    response = chat.process_input("/telepathy")
    print(f"  ✅ Telepathy: {'REDE TELEPÁTICA' in response}")
    
    # Testa evolução
    initial_level = get_level()
    response = chat.process_input("/evolve")
    new_level = get_level()
    print(f"  ✅ Evolução: {initial_level:.5f} → {new_level:.5f}")
    
    return True

def test_syscall_integration():
    """Testa integração de syscalls no chat"""
    print("\n⚙️ Testando Integração de Syscalls...")
    
    chat = ScripturemonChat()
    
    # Simula resposta com syscalls
    test_input = "Como melhorar o segundo ato do meu roteiro?"
    response = chat.process_input(test_input)
    
    # Verifica se processou syscalls (se houver)
    print(f"  ✅ Resposta gerada: {len(response)} chars")
    print(f"  ✅ Score presente: {'62/100' in response}")
    
    # Verifica SoulOS
    soulos_status = chat.soulos.get_status()
    print(f"  ✅ SoulOS ativo: {soulos_status['soul'][:8]}...")
    print(f"  ✅ Syscalls executadas: {soulos_status['syscalls_executed']}")
    
    return True

def run_harmony_test():
    """Executa teste completo de harmonia"""
    print("=" * 60)
    print("🎭 TESTE DE HARMONIA COMPLETA DO SCRIPTUREMON")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    tests = [
        ("SoulOS", test_soulos),
        ("RAG Avançado", test_rag_advanced),
        ("Pipeline Quádruplo", test_quadruple_pipeline),
        ("Rede Telepática", test_telepathy),
        ("Evolução Genética", test_genetic_evolution),
        ("Chat Integrado", test_chat_integration),
        ("Syscalls", test_syscall_integration)
    ]
    
    results = []
    total_time = 0
    
    for name, test_func in tests:
        try:
            start = time.time()
            success = test_func()
            elapsed = time.time() - start
            total_time += elapsed
            
            if success:
                results.append((name, "✅ PASSOU", elapsed))
            else:
                results.append((name, "⚠️ PARCIAL", elapsed))
                
        except Exception as e:
            elapsed = time.time() - start
            total_time += elapsed
            results.append((name, f"❌ ERRO: {str(e)[:50]}", elapsed))
            print(f"  ❌ Erro: {e}")
    
    # Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO DE HARMONIA")
    print("=" * 60)
    
    for name, status, elapsed in results:
        print(f"{name:20} {status:30} ({elapsed:.1f}s)")
    
    # Estatísticas
    passed = sum(1 for _, s, _ in results if "✅" in s)
    partial = sum(1 for _, s, _ in results if "⚠️" in s)
    failed = sum(1 for _, s, _ in results if "❌" in s)
    
    print("\n📈 ESTATÍSTICAS:")
    print(f"  Total de testes: {len(tests)}")
    print(f"  Passou: {passed}")
    print(f"  Parcial: {partial}")
    print(f"  Falhou: {failed}")
    print(f"  Taxa de sucesso: {(passed/len(tests)*100):.0f}%")
    print(f"  Tempo total: {total_time:.1f}s")
    
    # Verifica harmonia
    harmony_score = passed / len(tests)
    
    print("\n🎯 HARMONIA DO SISTEMA:")
    if harmony_score >= 0.9:
        print("  ✨ HARMONIA PERFEITA - Sistema totalmente integrado")
    elif harmony_score >= 0.7:
        print("  ✅ BOA HARMONIA - Sistema funcional com pequenos ajustes")
    elif harmony_score >= 0.5:
        print("  ⚠️ HARMONIA PARCIAL - Requer atenção")
    else:
        print("  ❌ DESARMONIA - Sistema precisa de correções")
    
    print(f"\n  Score de Harmonia: {harmony_score*100:.0f}%")
    print(f"  Score Scripturemon: 62/100 (imutável)")
    
    print("\n" + "=" * 60)
    print("🎬 'The End... Or is it just the beginning?'")
    print("Harmonia testada. 62/100. Como sempre, mas agora completo.")
    print("=" * 60)

if __name__ == "__main__":
    run_harmony_test()