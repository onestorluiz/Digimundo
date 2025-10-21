#!/usr/bin/env python3
"""
Resource Monitor - DIGIMUNDO STYLE
Monitoramento minimalista de recursos do sistema
"""

import os
import psutil
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class ResourceMonitor:
    """Monitor de recursos para ScripturemonUltimate."""

    def __init__(self, log_dir: Path = Path("logs")):
        self.log_dir = log_dir
        self.log_dir.mkdir(exist_ok=True)
        self.metrics_file = self.log_dir / "resource_metrics.json"
        self.history = []
        self.load_history()

    def load_history(self):
        """Carrega histórico de métricas."""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = []

    def save_history(self):
        """Salva histórico de métricas."""
        try:
            # Mantém apenas últimas 1000 entradas
            if len(self.history) > 1000:
                self.history = self.history[-1000:]

            with open(self.metrics_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"⚠️ Erro salvando métricas: {e}")

    def get_system_metrics(self) -> Dict:
        """Coleta métricas do sistema."""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "percent": psutil.cpu_percent(interval=1),
                "count": psutil.cpu_count(),
                "freq": psutil.cpu_freq().current if psutil.cpu_freq() else 0
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "used": psutil.virtual_memory().used,
                "percent": psutil.virtual_memory().percent,
                "available": psutil.virtual_memory().available
            },
            "processes": []
        }

        # Busca processos relevantes
        target_processes = ["python", "ollama", "node"]
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                pinfo = proc.info
                if any(target in pinfo['name'].lower() for target in target_processes):
                    metrics["processes"].append({
                        "pid": pinfo['pid'],
                        "name": pinfo['name'],
                        "cpu": pinfo['cpu_percent'],
                        "memory": pinfo['memory_percent']
                    })
            except:
                continue

        return metrics

    def get_ollama_metrics(self) -> Optional[Dict]:
        """Coleta métricas específicas do Ollama."""
        try:
            import requests
            response = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)

            if response.status_code == 200:
                models = response.json().get('models', [])
                total_size = sum(m.get('size', 0) for m in models) / (1024**3)  # GB

                return {
                    "status": "online",
                    "models_count": len(models),
                    "total_size_gb": round(total_size, 2),
                    "models": [m.get('name', 'unknown') for m in models]
                }
        except:
            pass

        return {"status": "offline"}

    def monitor_live(self, duration: int = 60, interval: int = 5):
        """
        Monitora recursos em tempo real.

        Args:
            duration: Duração do monitoramento em segundos
            interval: Intervalo entre coletas em segundos
        """
        print(f"📊 MONITORAMENTO DE RECURSOS - {duration}s")
        print("=" * 60)

        start_time = time.time()
        max_cpu = 0
        max_memory = 0
        samples = []

        while time.time() - start_time < duration:
            metrics = self.get_system_metrics()
            samples.append(metrics)

            # Atualiza máximos
            max_cpu = max(max_cpu, metrics['cpu']['percent'])
            max_memory = max(max_memory, metrics['memory']['percent'])

            # Display
            self._display_metrics(metrics)

            # Salva no histórico
            self.history.append(metrics)

            time.sleep(interval)

        # Sumário
        self._display_summary(samples, max_cpu, max_memory)
        self.save_history()

    def _display_metrics(self, metrics: Dict):
        """Exibe métricas formatadas."""
        timestamp = metrics['timestamp'].split('T')[1].split('.')[0]
        cpu = metrics['cpu']['percent']
        mem = metrics['memory']['percent']

        # Barra visual de CPU
        cpu_bar = "█" * int(cpu / 5) + "░" * (20 - int(cpu / 5))

        print(f"\n⏰ {timestamp}")
        print(f"   CPU: [{cpu_bar}] {cpu:5.1f}%")
        print(f"   MEM: {mem:5.1f}% ({metrics['memory']['used'] / (1024**3):.1f}GB)")

        # Processos top
        if metrics['processes']:
            top_procs = sorted(metrics['processes'],
                             key=lambda x: x['cpu'],
                             reverse=True)[:3]
            print("   Top Processos:")
            for proc in top_procs:
                print(f"     - {proc['name']}: CPU {proc['cpu']:.1f}%")

    def _display_summary(self, samples: List[Dict], max_cpu: float, max_memory: float):
        """Exibe sumário do monitoramento."""
        avg_cpu = sum(s['cpu']['percent'] for s in samples) / len(samples)
        avg_mem = sum(s['memory']['percent'] for s in samples) / len(samples)

        print("\n" + "=" * 60)
        print("📈 SUMÁRIO")
        print(f"   CPU - Média: {avg_cpu:.1f}% | Máximo: {max_cpu:.1f}%")
        print(f"   MEM - Média: {avg_mem:.1f}% | Máximo: {max_memory:.1f}%")

        # Verifica Ollama
        ollama_metrics = self.get_ollama_metrics()
        if ollama_metrics['status'] == 'online':
            print(f"\n🤖 OLLAMA")
            print(f"   Status: Online")
            print(f"   Modelos: {ollama_metrics['models_count']}")
            print(f"   Tamanho: {ollama_metrics['total_size_gb']}GB")

    def get_report(self) -> Dict:
        """Gera relatório completo de recursos."""
        current = self.get_system_metrics()
        ollama = self.get_ollama_metrics()

        # Calcula médias do histórico (última hora)
        recent = [m for m in self.history
                 if datetime.fromisoformat(m['timestamp']) >
                    datetime.now().replace(hour=datetime.now().hour-1)]

        if recent:
            avg_cpu = sum(m['cpu']['percent'] for m in recent) / len(recent)
            avg_mem = sum(m['memory']['percent'] for m in recent) / len(recent)
        else:
            avg_cpu = current['cpu']['percent']
            avg_mem = current['memory']['percent']

        return {
            "timestamp": current['timestamp'],
            "current": {
                "cpu": current['cpu']['percent'],
                "memory": current['memory']['percent'],
                "processes": len(current['processes'])
            },
            "averages": {
                "cpu": round(avg_cpu, 2),
                "memory": round(avg_mem, 2)
            },
            "ollama": ollama,
            "history_samples": len(self.history)
        }


def main():
    """Função principal para testes."""
    monitor = ResourceMonitor()

    print("🔍 Escolha uma opção:")
    print("1. Monitoramento ao vivo (60s)")
    print("2. Métricas atuais")
    print("3. Relatório completo")

    choice = input("\nOpção: ")

    if choice == "1":
        monitor.monitor_live(duration=60, interval=5)
    elif choice == "2":
        metrics = monitor.get_system_metrics()
        print(json.dumps(metrics, indent=2))
    elif choice == "3":
        report = monitor.get_report()
        print(json.dumps(report, indent=2))
    else:
        print("Opção inválida")


if __name__ == "__main__":
    main()