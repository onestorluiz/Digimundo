#!/usr/bin/env python3
"""
📊 MONITOR DO SISTEMA mixtral
Visualiza status, métricas e resultados
"""

import json
import time
from pathlib import Path
from datetime import datetime


def monitor():
    """Monitor principal"""

    log_dir = Path(__file__).parent.parent.parent / "data" / "logs" / "deep_learning_mixtral"

    print("📊 MONITOR mixtral mixtral")
    print("=" * 60)

    # 1. STATUS ATUAL
    status_file = log_dir / "current_status.json"
    if status_file.exists():
        with open(status_file) as f:
            status = json.load(f)

        print("\n📍 STATUS ATUAL:")
        print(f"  • Estado: {status.get('status', 'idle')}")

        if status.get('status') == 'processing':
            print(f"  • Processando: {status.get('current', 'N/A')}")
            print(f"  • Modo: {status.get('mode', 'N/A')}")
            if status.get('started'):
                elapsed = time.time() - status['started']
                print(f"  • Tempo decorrido: {elapsed:.1f}s")
            if status.get('pid'):
                print(f"  • PID: {status['pid']}")
        elif status.get('last_completed'):
            print(f"  • Último: {status['last_completed']}")
            print(f"  • Duração: {status.get('last_duration', 0):.1f}s")
            print(f"  • Sucesso: {status.get('last_success', False)}")

        print(f"  • Total processados: {status.get('total_processed', 0)}")
    else:
        print("\n⚠️ Nenhum status encontrado. Sistema não iniciado.")

    # 2. MÉTRICAS DE PERFORMANCE
    metrics_file = log_dir / "performance_metrics.json"
    if metrics_file.exists():
        with open(metrics_file) as f:
            metrics = json.load(f)

        print("\n📈 MÉTRICAS DE PERFORMANCE:")

        for mode in ["ECO", "DEDICATED"]:
            if mode in metrics and metrics[mode]['total_processed'] > 0:
                m = metrics[mode]
                print(f"\n  {mode}:")
                print(f"    • Processados: {m['total_processed']}")
                print(f"    • Taxa sucesso: {m['successes']}/{m['total_processed']} ({m['successes']/m['total_processed']*100:.0f}%)")
                print(f"    • Tempo médio: {m['avg_time']:.1f}s")
                print(f"    • Tempo min/max: {m['min_time']:.1f}s / {m['max_time']:.1f}s")

                if m['total_tokens'] > 0:
                    print(f"    • Tokens totais: {m['total_tokens']:,}")
                    avg_tokens = m['total_tokens'] / m['successes'] if m['successes'] > 0 else 0
                    print(f"    • Média tokens/análise: {avg_tokens:.0f}")

                if m['avg_time'] > 0:
                    scripts_per_hour = 3600 / m['avg_time']
                    print(f"    • Taxa: {scripts_per_hour:.1f} roteiros/hora")

    # 3. ÚLTIMOS RESULTADOS
    result_files = sorted(log_dir.glob("results_*.jsonl"))
    if result_files:
        latest_file = result_files[-1]

        print(f"\n📄 ÚLTIMOS RESULTADOS ({latest_file.name}):")

        with open(latest_file) as f:
            lines = f.readlines()

        # Mostrar últimos 5 resultados
        for line in lines[-5:]:
            result = json.loads(line)
            status_icon = "✅" if result['success'] else "❌"
            print(f"  {status_icon} {result['screenplay'][:20]}: {result['duration']:.1f}s ({result['mode']})")

            if result.get('model_info'):
                tokens = result['model_info'].get('eval_count', 0)
                tps = result['model_info'].get('tokens_per_second', 0)
                if tokens > 0:
                    print(f"      {tokens:,} tokens @ {tps:.1f} t/s")

    # 4. RECURSOS DO SISTEMA (estimativa)
    print("\n💻 RECURSOS ESTIMADOS:")
    if status.get('status') == 'processing':
        mode = status.get('mode', 'ECO')
        if mode == 'ECO':
            print("  • RAM: ~45 GB (47% de 96GB)")
            print("  • CPU: ~12 threads (43% de 28)")
            print("  • GPU: ~40% utilização")
        else:  # DEDICATED
            print("  • RAM: ~65 GB (68% de 96GB)")
            print("  • CPU: ~24 threads (86% de 28)")
            print("  • GPU: ~95% utilização")
    else:
        print("  • Sistema idle")

    # 5. ESPAÇO EM DISCO
    total_size = sum(f.stat().st_size for f in log_dir.rglob('*') if f.is_file())
    print(f"\n💾 ESPAÇO USADO:")
    print(f"  • Logs: {total_size / 1024 / 1024:.1f} MB")
    print(f"  • Arquivos: {len(list(log_dir.rglob('*')))} total")

    print("\n" + "=" * 60)
    print("💡 COMANDOS ÚTEIS:")
    print("  • Testar: python3 scripts/active/test_mixtral_modes.py")
    print("  • Status: tail -f data/logs/deep_learning_mixtral/current_status.json")
    print("  • Processar: python3 scripts/active/async_mixtral_processor.py")

    print("\nDIGIMUNDO PRESENTE 🥷")


def watch():
    """Modo watch - atualiza a cada 5 segundos"""
    import os

    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        monitor()
        print("\n🔄 Atualizando em 5s... (Ctrl+C para sair)")
        time.sleep(5)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "watch":
        try:
            watch()
        except KeyboardInterrupt:
            print("\n\n✋ Monitor parado")
    else:
        monitor()
        print("\n💡 Use 'python3 monitor_mixtral.py watch' para monitoramento contínuo")