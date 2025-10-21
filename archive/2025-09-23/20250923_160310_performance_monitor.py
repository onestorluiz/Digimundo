#!/usr/bin/env python3
"""
Performance Monitor para SCRIPTUREMON v9
Monitora e ajusta performance em tempo real
"""

import psutil
import time
import threading
import subprocess
import json
from typing import Dict, Any, Optional
from datetime import datetime

class PerformanceMonitor:
    """
    Sistema de monitoramento e auto-ajuste de performance
    """

    def __init__(self, model_name: str = "scripturemon-v9-final"):
        self.model_name = model_name
        self.start_time = None
        self.initial_metrics = None
        self.current_metrics = {}
        self.monitoring = False
        self.monitor_thread = None
        self.adjustments_made = []
        self.alerts = []

        # Thresholds
        self.thresholds = {
            "ram_critical": 85,      # % RAM usage
            "ram_warning": 75,
            "cpu_critical": 90,       # % CPU usage
            "cpu_warning": 80,
            "time_slow_short": 120,   # 2min for short
            "time_slow_medium": 180,  # 3min for medium
            "time_slow_long": 300,    # 5min for long
            "swap_warning": 1024      # MB swap usage
        }

        # Performance history
        self.performance_history = []

    def start_monitoring(self, script_size_category: str = "medium"):
        """
        Inicia monitoramento em thread separada
        """
        self.start_time = time.time()
        self.script_category = script_size_category
        self.monitoring = True

        # Capturar métricas iniciais
        self.initial_metrics = self.get_current_metrics()

        # Iniciar thread de monitoramento
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )
        self.monitor_thread.start()

        print(f"🔍 Performance Monitor iniciado")
        print(f"   RAM inicial: {self.initial_metrics['ram_percent']:.1f}%")
        print(f"   CPU inicial: {self.initial_metrics['cpu_percent']:.1f}%")

    def stop_monitoring(self):
        """
        Para o monitoramento
        """
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)

        # Relatório final
        self.generate_report()

    def get_current_metrics(self) -> Dict[str, Any]:
        """
        Captura métricas atuais do sistema
        """
        # Memória
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_per_core = psutil.cpu_percent(percpu=True, interval=1)

        # Processos Ollama
        ollama_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
            if 'ollama' in proc.info['name'].lower():
                ollama_processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'memory': proc.info['memory_percent'],
                    'cpu': proc.info['cpu_percent']
                })

        return {
            'timestamp': datetime.now().isoformat(),
            'ram_percent': mem.percent,
            'ram_used_gb': mem.used / (1024**3),
            'ram_available_gb': mem.available / (1024**3),
            'swap_used_mb': swap.used / (1024**2),
            'cpu_percent': cpu_percent,
            'cpu_per_core': cpu_per_core,
            'ollama_processes': ollama_processes,
            'elapsed_time': time.time() - self.start_time if self.start_time else 0
        }

    def _monitor_loop(self):
        """
        Loop principal de monitoramento
        """
        check_interval = 10  # Verificar a cada 10 segundos

        while self.monitoring:
            time.sleep(check_interval)

            # Capturar métricas
            metrics = self.get_current_metrics()
            self.current_metrics = metrics
            self.performance_history.append(metrics)

            # Verificar problemas
            issues = self.check_for_issues(metrics)

            # Auto-ajuste se necessário
            if issues:
                self.handle_issues(issues)

    def check_for_issues(self, metrics: Dict[str, Any]) -> list:
        """
        Verifica se há problemas de performance
        """
        issues = []

        # RAM crítica
        if metrics['ram_percent'] > self.thresholds['ram_critical']:
            issues.append({
                'type': 'ram_critical',
                'value': metrics['ram_percent'],
                'severity': 'critical'
            })
        elif metrics['ram_percent'] > self.thresholds['ram_warning']:
            issues.append({
                'type': 'ram_warning',
                'value': metrics['ram_percent'],
                'severity': 'warning'
            })

        # CPU crítico
        if metrics['cpu_percent'] > self.thresholds['cpu_critical']:
            issues.append({
                'type': 'cpu_critical',
                'value': metrics['cpu_percent'],
                'severity': 'critical'
            })

        # Swap usage
        if metrics['swap_used_mb'] > self.thresholds['swap_warning']:
            issues.append({
                'type': 'swap_warning',
                'value': metrics['swap_used_mb'],
                'severity': 'warning'
            })

        # Tempo excessivo
        elapsed = metrics['elapsed_time']
        if self.script_category == 'curta' and elapsed > self.thresholds['time_slow_short']:
            issues.append({
                'type': 'slow_analysis',
                'value': elapsed,
                'severity': 'warning'
            })
        elif self.script_category == 'média' and elapsed > self.thresholds['time_slow_medium']:
            issues.append({
                'type': 'slow_analysis',
                'value': elapsed,
                'severity': 'warning'
            })

        return issues

    def handle_issues(self, issues: list):
        """
        Tenta resolver problemas detectados
        """
        for issue in issues:
            alert = f"⚠️ {issue['type']}: {issue['value']:.1f}"
            self.alerts.append(alert)
            print(f"\n{alert}")

            # Aplicar ajuste apropriado
            adjustment = self.get_adjustment_for_issue(issue)
            if adjustment and adjustment not in self.adjustments_made:
                self.apply_adjustment(adjustment)
                self.adjustments_made.append(adjustment)

    def get_adjustment_for_issue(self, issue: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Determina ajuste apropriado para o problema
        """
        issue_type = issue['type']
        severity = issue['severity']

        if issue_type == 'ram_critical':
            return {
                'action': 'reduce_memory',
                'params': {
                    'num_ctx': 32768,      # Reduzir contexto pela metade
                    'num_batch': 512,      # Reduzir batch
                    'num_keep': 256        # Reduzir keep
                },
                'reason': 'RAM crítica > 85%'
            }

        elif issue_type == 'cpu_critical':
            return {
                'action': 'reduce_threads',
                'params': {
                    'num_thread': 4        # Reduzir threads drasticamente
                },
                'reason': 'CPU crítico > 90%'
            }

        elif issue_type == 'swap_warning':
            return {
                'action': 'emergency_reduction',
                'params': {
                    'num_ctx': 16384,      # Contexto mínimo
                    'num_batch': 256,
                    'num_predict': 2048    # Output mínimo
                },
                'reason': 'Swap excessivo'
            }

        elif issue_type == 'slow_analysis' and severity == 'warning':
            return {
                'action': 'speed_boost',
                'params': {
                    'temperature': 0.3,    # Menos exploração
                    'top_p': 0.8          # Mais focado
                },
                'reason': 'Análise muito lenta'
            }

        return None

    def apply_adjustment(self, adjustment: Dict[str, Any]):
        """
        Aplica ajuste dinâmico
        """
        print(f"\n🔧 Aplicando ajuste: {adjustment['action']}")
        print(f"   Razão: {adjustment['reason']}")

        # Em produção, isso comunicaria com o modelo em execução
        # Por ora, apenas registra a intenção
        for param, value in adjustment['params'].items():
            print(f"   {param}: {value}")

        # Registrar ajuste
        adjustment['timestamp'] = datetime.now().isoformat()

    def get_performance_score(self) -> float:
        """
        Calcula score de performance (0-100)
        """
        if not self.current_metrics:
            return 0

        score = 100

        # Penalizar por RAM alta
        ram_penalty = max(0, self.current_metrics['ram_percent'] - 60) * 0.5
        score -= ram_penalty

        # Penalizar por CPU alto
        cpu_penalty = max(0, self.current_metrics['cpu_percent'] - 70) * 0.3
        score -= cpu_penalty

        # Penalizar por swap
        if self.current_metrics['swap_used_mb'] > 100:
            score -= 10

        # Penalizar por tempo excessivo
        expected_time = {
            'curta': 60,
            'média': 120,
            'longa': 180
        }.get(self.script_category, 120)

        if self.current_metrics['elapsed_time'] > expected_time * 1.5:
            score -= 15

        # Bônus se nenhum ajuste foi necessário
        if not self.adjustments_made:
            score += 10

        return max(0, min(100, score))

    def generate_report(self) -> Dict[str, Any]:
        """
        Gera relatório de performance
        """
        if not self.start_time:
            return {"error": "Monitoring not started"}

        total_time = time.time() - self.start_time
        final_metrics = self.get_current_metrics()

        # Calcular médias
        if self.performance_history:
            avg_ram = sum(m['ram_percent'] for m in self.performance_history) / len(self.performance_history)
            avg_cpu = sum(m['cpu_percent'] for m in self.performance_history) / len(self.performance_history)
            max_ram = max(m['ram_percent'] for m in self.performance_history)
            max_cpu = max(m['cpu_percent'] for m in self.performance_history)
        else:
            avg_ram = avg_cpu = max_ram = max_cpu = 0

        report = {
            'summary': {
                'total_time': f"{total_time:.1f}s",
                'performance_score': self.get_performance_score(),
                'adjustments_count': len(self.adjustments_made),
                'alerts_count': len(self.alerts)
            },
            'metrics': {
                'ram': {
                    'initial': f"{self.initial_metrics['ram_percent']:.1f}%",
                    'final': f"{final_metrics['ram_percent']:.1f}%",
                    'average': f"{avg_ram:.1f}%",
                    'maximum': f"{max_ram:.1f}%"
                },
                'cpu': {
                    'initial': f"{self.initial_metrics['cpu_percent']:.1f}%",
                    'final': f"{final_metrics['cpu_percent']:.1f}%",
                    'average': f"{avg_cpu:.1f}%",
                    'maximum': f"{max_cpu:.1f}%"
                }
            },
            'adjustments': self.adjustments_made,
            'alerts': self.alerts,
            'grade': self.get_performance_grade()
        }

        # Imprimir relatório
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO DE PERFORMANCE")
        print("=" * 60)
        print(f"\n⏱️ Tempo total: {report['summary']['total_time']}")
        print(f"🎯 Score: {report['summary']['performance_score']:.1f}/100")
        print(f"📈 Grade: {report['grade']}")

        print(f"\n💾 RAM:")
        print(f"   Média: {report['metrics']['ram']['average']}")
        print(f"   Máxima: {report['metrics']['ram']['maximum']}")

        print(f"\n⚡ CPU:")
        print(f"   Média: {report['metrics']['cpu']['average']}")
        print(f"   Máxima: {report['metrics']['cpu']['maximum']}")

        if self.adjustments_made:
            print(f"\n🔧 Ajustes realizados: {len(self.adjustments_made)}")
            for adj in self.adjustments_made:
                print(f"   - {adj['action']}: {adj['reason']}")

        if self.alerts:
            print(f"\n⚠️ Alertas: {len(self.alerts)}")
            for alert in self.alerts[:5]:  # Mostrar apenas primeiros 5
                print(f"   {alert}")

        return report

    def get_performance_grade(self) -> str:
        """
        Retorna grade de performance (A-F)
        """
        score = self.get_performance_score()

        if score >= 90:
            return "A - Excelente"
        elif score >= 80:
            return "B - Bom"
        elif score >= 70:
            return "C - Satisfatório"
        elif score >= 60:
            return "D - Precisa melhorias"
        else:
            return "F - Crítico"


def demo():
    """
    Demonstração do Performance Monitor
    """
    print("🎬 DEMO: Performance Monitor")
    print("=" * 60)

    monitor = PerformanceMonitor()

    # Simular análise
    monitor.start_monitoring(script_size_category="curta")

    print("\n⏳ Simulando análise por 30 segundos...")
    print("   (Monitor rodando em background)")

    # Simular trabalho
    for i in range(30):
        time.sleep(1)
        if i % 10 == 0:
            metrics = monitor.get_current_metrics()
            print(f"\n[{i}s] RAM: {metrics['ram_percent']:.1f}% | CPU: {metrics['cpu_percent']:.1f}%")

    # Parar e gerar relatório
    monitor.stop_monitoring()


if __name__ == "__main__":
    demo()