#!/usr/bin/env python3
"""
♾️ DEEP LEARNING AUTÔNOMO CONTÍNUO
Sistema que roda indefinidamente processando roteiros
"""

import sys
import subprocess
import json
import time
import random
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Importar controle de potência
try:
    from scripts.active.power_control import PowerControl
    POWER_CONTROL_ENABLED = True
except:
    POWER_CONTROL_ENABLED = False


def run_autonomous_deep_learning():
    """Sistema autônomo que roda continuamente"""

    print("♾️ DEEP LEARNING AUTÔNOMO - RODANDO CONTINUAMENTE")
    print("=" * 60)

    # Carregar configurações de potência
    if POWER_CONTROL_ENABLED:
        power_config = PowerControl.get_current_config()
        preset = power_config.get('preset', 'ECO')
        print(f"\n⚡ POTÊNCIA: {preset}")
        print(f"  • Pausa: {power_config['sleep_between_scripts']}s")
        print(f"  • Ollama: 1/{power_config['ollama_frequency']}")
        print(f"  • Chunk: {power_config['scene_chunk_size']} chars")
    else:
        # Valores padrão se não tiver controle de potência
        power_config = {
            'sleep_between_scripts': 2.0,
            'ollama_frequency': 5,
            'ollama_timeout': 20,
            'scene_chunk_size': 500,
            'num_predict': 30
        }
        print("\n⚡ Modo ECO (padrão)")

    # Importar componentes
    from scripts.active.integrated_system import get_integrated_system
    from src.core.screenplay_library import get_screenplay_library
    from src.core.unified_memory_system import get_unified_memory, MemoryType

    system = get_integrated_system()
    library = get_screenplay_library()
    memory = get_unified_memory()

    print("\n✅ SISTEMA INICIALIZADO")
    print(f"  • Memória: {memory.get_stats()['total_entries']:,} entradas")
    print(f"  • Biblioteca: 48 roteiros disponíveis")
    print(f"  • Modelo: mixtral-dedicated-q5 (128K tokens)")
    print(f"  • Claude: 55,634+ chars de memórias")

    # Estatísticas globais
    global_stats = {
        'start_time': time.time(),
        'total_processed': 0,
        'total_patterns': 0,
        'total_ollama_calls': 0,
        'total_cache_hits': 0,
        'total_errors': 0,
        'cycles_completed': 0
    }

    # Pegar lista de roteiros
    all_scripts = library.list_all()
    screenplay_queue = []

    for category, scripts in all_scripts.items():
        for script in scripts:
            screenplay_queue.append((script, category))

    # Embaralhar para variedade
    random.shuffle(screenplay_queue)

    print(f"\n📚 {len(screenplay_queue)} roteiros na fila")
    print("\n⚡ INICIANDO PROCESSAMENTO CONTÍNUO...")
    print("   (Pressione Ctrl+C para parar)")
    print("=" * 60)

    # LOOP INFINITO
    cycle_num = 0
    while True:
        try:
            cycle_num += 1
            print(f"\n{'='*60}")
            print(f"🔄 CICLO #{cycle_num} - {datetime.now().strftime('%H:%M:%S')}")
            print(f"{'='*60}")

            # Pegar próximo roteiro (volta ao início se acabar)
            if not screenplay_queue:
                # Recarregar fila
                for category, scripts in all_scripts.items():
                    for script in scripts:
                        screenplay_queue.append((script, category))
                random.shuffle(screenplay_queue)
                global_stats['cycles_completed'] += 1
                print(f"\n♻️ Reiniciando fila - Ciclo completo #{global_stats['cycles_completed']}")

            screenplay, category = screenplay_queue.pop(0)
            print(f"\n📖 [{global_stats['total_processed']+1}] {screenplay} ({category})")
            print("-" * 40)

            # 1. WHY THIS WORKS
            try:
                print("1️⃣ Why This Works...")
                text = library.get_screenplay_text(screenplay)
                if text and len(text) > 100:
                    scene = text[:power_config['scene_chunk_size']]
                    result = system.deep_learning.why_this_works(scene, limit=2)
                    patterns = len(result.get('explanations', []))
                    global_stats['total_patterns'] += patterns
                    print(f"   ✅ {patterns} padrões encontrados")
            except Exception as e:
                print(f"   ⚠️ Erro: {str(e)[:30]}")
                global_stats['total_errors'] += 1

            # 2. META-LEARNING
            try:
                print("2️⃣ Meta-learning...")
                system.meta_learning.discovered_patterns.append({
                    'screenplay': screenplay,
                    'category': category,
                    'cycle': cycle_num,
                    'timestamp': time.time()
                })

                # Verificar evolução a cada 10 roteiros
                if global_stats['total_processed'] % 10 == 0:
                    if system.meta_learning.check_evolution_readiness().get('ready', False):
                        print("   🔄 Sistema evoluindo!")

                print(f"   ✅ Padrão #{len(system.meta_learning.discovered_patterns)} registrado")
            except:
                pass

            # 3. CACHE
            try:
                print("3️⃣ Cache inteligente...")
                cache_key = f"auto_analysis_{screenplay}"
                cached = memory.retrieve(MemoryType.CACHE, key=cache_key)

                if cached and len(cached) > 0:
                    global_stats['total_cache_hits'] += 1
                    print(f"   ✅ Cache hit! (total: {global_stats['total_cache_hits']})")
                else:
                    # Salvar no cache
                    memory.store(
                        memory_type=MemoryType.CACHE,
                        key=cache_key,
                        value={
                            'screenplay': screenplay,
                            'category': category,
                            'cycle': cycle_num,
                            'timestamp': time.time()
                        },
                        metadata={'autonomous': True}
                    )
                    print(f"   💾 Novo cache salvo")
            except:
                pass

            # 4. OLLAMA (frequência controlada por potência)
            if global_stats['total_processed'] % power_config['ollama_frequency'] == 0:
                try:
                    print("4️⃣ Deep Learning Ollama...")

                    prompt = f"Analyze {screenplay} themes in {power_config['num_predict']} words"
                    payload = {
                        'model': 'mixtral-dedicated-q5',
                        'prompt': prompt,
                        'stream': False,
                        'options': {'temperature': 0.3, 'num_predict': power_config['num_predict']}
                    }

                    result = subprocess.run(
                        ['curl', '-s', '--max-time', str(power_config['ollama_timeout']),
                         'http://localhost:11434/api/generate',
                         '-d', json.dumps(payload)],
                        capture_output=True,
                        text=True
                    )

                    if result.returncode == 0 and result.stdout:
                        response = json.loads(result.stdout)
                        analysis = response.get('response', '')[:100]
                        global_stats['total_ollama_calls'] += 1
                        print(f"   ✅ Análise: {analysis[:50]}...")

                        # Salvar conhecimento
                        memory.store(
                            memory_type=MemoryType.KNOWLEDGE,
                            key=f"ollama_{screenplay}_{cycle_num}",
                            value={'analysis': analysis},
                            metadata={'cycle': cycle_num}
                        )
                except:
                    print(f"   ⚠️ Ollama timeout")

            global_stats['total_processed'] += 1

            # ESTATÍSTICAS A CADA ROTEIRO
            elapsed = time.time() - global_stats['start_time']
            rate = global_stats['total_processed'] / (elapsed / 60) if elapsed > 0 else 0

            print(f"\n📊 STATUS:")
            print(f"  • Processados: {global_stats['total_processed']}")
            print(f"  • Padrões: {global_stats['total_patterns']}")
            print(f"  • Cache hits: {global_stats['total_cache_hits']}")
            print(f"  • Ollama: {global_stats['total_ollama_calls']}")
            print(f"  • Taxa: {rate:.1f}/min")
            print(f"  • Uptime: {elapsed/60:.1f} min")

            # Salvar progresso na memória
            if global_stats['total_processed'] % 10 == 0:
                memory.store(
                    memory_type=MemoryType.KNOWLEDGE,
                    key=f"autonomous_progress_{datetime.now().isoformat()}",
                    value=global_stats,
                    metadata={'checkpoint': True}
                )
                mem_stats = memory.get_stats()
                print(f"\n💾 Checkpoint: {mem_stats['total_entries']:,} conhecimentos")

            # Pausa controlada por potência
            time.sleep(power_config['sleep_between_scripts'])

            # Recarregar config a cada 10 roteiros (para mudanças dinâmicas)
            if POWER_CONTROL_ENABLED and global_stats['total_processed'] % 10 == 0:
                new_config = PowerControl.get_current_config()
                if new_config.get('preset') != power_config.get('preset'):
                    print(f"\n⚡ Potência alterada: {power_config.get('preset')} → {new_config.get('preset')}")
                power_config = new_config

        except KeyboardInterrupt:
            print("\n\n⏹️ INTERROMPIDO PELO USUÁRIO")
            break
        except Exception as e:
            print(f"\n⚠️ Erro no ciclo: {str(e)[:50]}")
            global_stats['total_errors'] += 1
            time.sleep(5)  # Pausa maior em caso de erro
            continue

    # RELATÓRIO FINAL
    elapsed_total = time.time() - global_stats['start_time']

    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL - PROCESSAMENTO AUTÔNOMO")
    print("=" * 60)

    print(f"\n✅ RESULTADOS:")
    print(f"  • Tempo total: {elapsed_total/60:.1f} minutos")
    print(f"  • Roteiros processados: {global_stats['total_processed']}")
    print(f"  • Ciclos completos: {global_stats['cycles_completed']}")
    print(f"  • Padrões descobertos: {global_stats['total_patterns']}")
    print(f"  • Cache hits: {global_stats['total_cache_hits']}")
    print(f"  • Ollama calls: {global_stats['total_ollama_calls']}")
    print(f"  • Erros recuperados: {global_stats['total_errors']}")
    print(f"  • Taxa média: {global_stats['total_processed']/(elapsed_total/60):.1f} roteiros/min")

    mem_final = memory.get_stats()
    print(f"\n💾 MEMÓRIA FINAL:")
    print(f"  • Total: {mem_final['total_entries']:,} entradas")
    print(f"  • Crescimento: {mem_final['total_entries'] - 9814} novos conhecimentos")

    print("\nDIGIMUNDO PRESENTE 🥷")


if __name__ == "__main__":
    print("=" * 60)
    print("♾️ INICIANDO DEEP LEARNING AUTÔNOMO CONTÍNUO")
    print("=" * 60)
    print("\nO sistema vai rodar INDEFINIDAMENTE:")
    print("  • Processando todos os 48 roteiros")
    print("  • Reiniciando quando terminar a fila")
    print("  • Salvando checkpoints a cada 10 roteiros")
    print("  • Recuperando de erros automaticamente")
    print("\nPressione Ctrl+C para parar quando quiser")
    print("=" * 60)

    try:
        run_autonomous_deep_learning()
    except KeyboardInterrupt:
        print("\n\n✅ Sistema parado com sucesso")
        print("DIGIMUNDO PRESENTE 🥷")