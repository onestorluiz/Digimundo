#!/usr/bin/env python3
"""
📊 MONITOR EM TEMPO REAL DA ANÁLISE FORENSE
Dashboard visual com progresso, ETA e estatísticas
"""

import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import threading
import subprocess

class ForensicMonitor:
    """Monitor em tempo real da análise forense"""

    def __init__(self):
        self.base_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        self.results_dir = self.base_dir / "forensic_results"
        self.checkpoint_file = self.results_dir / "checkpoint.json"
        self.log_file = self.results_dir / "forensic_analysis.log"

        self.is_running = False
        self.last_update = None

    def clear_screen(self):
        """Limpa a tela"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def get_progress_data(self) -> Dict[str, Any]:
        """Obtém dados de progresso do checkpoint"""
        default_data = {
            'timestamp': datetime.now().isoformat(),
            'total_files': 0,
            'completed_files': 0,
            'results': {}
        }

        if not self.checkpoint_file.exists():
            return default_data

        try:
            with open(self.checkpoint_file, 'r') as f:
                data = json.load(f)
            return data
        except Exception:
            return default_data

    def get_analysis_stats(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula estatísticas da análise"""
        if not results:
            return {
                'broken': 0, 'problematic': 0, 'warning': 0, 'ok': 0,
                'critical_issues': 0, 'high_issues': 0, 'medium_issues': 0, 'low_issues': 0,
                'avg_claude_vice': 0.0, 'total_fix_time': 0.0
            }

        health_counts = {'BROKEN': 0, 'PROBLEMATIC': 0, 'WARNING': 0, 'OK': 0, 'ERROR': 0}
        total_critical = total_high = total_medium = total_low = 0
        total_claude_vice = total_fix_time = 0.0

        for result in results.values():
            health = result.get('overall_health', 'ERROR')
            health_counts[health] = health_counts.get(health, 0) + 1

            total_critical += len(result.get('critical_issues', []))
            total_high += len(result.get('high_issues', []))
            total_medium += len(result.get('medium_issues', []))
            total_low += len(result.get('low_issues', []))

            total_claude_vice += result.get('claude_vice_score', 0)
            total_fix_time += result.get('fix_time_estimate_hours', 0)

        completed = len(results)
        avg_claude_vice = total_claude_vice / completed if completed > 0 else 0

        return {
            'broken': health_counts.get('BROKEN', 0),
            'problematic': health_counts.get('PROBLEMATIC', 0),
            'warning': health_counts.get('WARNING', 0),
            'ok': health_counts.get('OK', 0),
            'error': health_counts.get('ERROR', 0),
            'critical_issues': total_critical,
            'high_issues': total_high,
            'medium_issues': total_medium,
            'low_issues': total_low,
            'avg_claude_vice': avg_claude_vice,
            'total_fix_time': total_fix_time
        }

    def format_time(self, seconds: float) -> str:
        """Formata tempo em formato legível"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}min"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"

    def get_eta(self, completed: int, total: int, elapsed_seconds: float) -> Optional[str]:
        """Calcula ETA (Estimated Time of Arrival)"""
        if completed == 0:
            return None

        avg_time_per_file = elapsed_seconds / completed
        remaining_files = total - completed
        remaining_seconds = avg_time_per_file * remaining_files

        eta_time = datetime.now() + timedelta(seconds=remaining_seconds)
        return eta_time.strftime("%H:%M:%S")

    def create_progress_bar(self, current: int, total: int, width: int = 50) -> str:
        """Cria barra de progresso visual"""
        if total == 0:
            return "█" * width

        progress = current / total
        filled = int(width * progress)
        bar = "█" * filled + "░" * (width - filled)
        percentage = progress * 100

        return f"[{bar}] {percentage:5.1f}% ({current}/{total})"

    def get_recent_activity(self) -> str:
        """Obtém atividade recente do log"""
        if not self.log_file.exists():
            return "Nenhuma atividade ainda..."

        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()

            # Últimas 5 linhas
            recent_lines = lines[-5:] if len(lines) >= 5 else lines

            activity = []
            for line in recent_lines:
                if "Analisando:" in line or "✅" in line or "❌" in line:
                    # Extrair timestamp e mensagem
                    if " - " in line:
                        parts = line.split(" - ", 2)
                        if len(parts) >= 3:
                            timestamp = parts[0]
                            message = parts[2].strip()
                            # Formatear timestamp
                            try:
                                dt = datetime.fromisoformat(timestamp)
                                time_str = dt.strftime("%H:%M:%S")
                                activity.append(f"{time_str} {message}")
                            except:
                                activity.append(message)

            return "\n".join(activity[-3:]) if activity else "Aguardando atividade..."

        except Exception as e:
            return f"Erro ao ler log: {e}"

    def check_if_analysis_running(self) -> bool:
        """Verifica se análise está rodando"""
        try:
            # Verificar se processo Python com forensic_orchestrator está rodando
            result = subprocess.run(
                ["pgrep", "-f", "forensic_orchestrator.py"],
                capture_output=True, text=True
            )
            return result.returncode == 0
        except:
            return False

    def display_dashboard(self):
        """Exibe dashboard principal"""
        # Obter dados
        progress_data = self.get_progress_data()
        stats = self.get_analysis_stats(progress_data.get('results', {}))

        total_files = progress_data.get('total_files', 0)
        completed_files = progress_data.get('completed_files', 0)

        # Calcular tempos
        if progress_data.get('timestamp'):
            try:
                start_time = datetime.fromisoformat(progress_data['timestamp'])
                elapsed = (datetime.now() - start_time).total_seconds()
            except:
                elapsed = 0
        else:
            elapsed = 0

        eta = self.get_eta(completed_files, total_files, elapsed) if elapsed > 0 else None

        # Verificar se está rodando
        is_running = self.check_if_analysis_running()

        # Limpar tela e exibir
        self.clear_screen()

        print("🔬 " + "="*70)
        print("    MONITOR FORENSE EM TEMPO REAL - SCRIPTUREMON CHAMPION")
        print("="*74)
        print()

        # Status principal
        status_icon = "🟢" if is_running else "🔴"
        status_text = "EXECUTANDO" if is_running else "PARADO"
        print(f"📊 STATUS: {status_icon} {status_text}")
        print(f"🕐 INÍCIO: {datetime.now().strftime('%H:%M:%S')}")
        print(f"⏱️ ELAPSED: {self.format_time(elapsed)}")
        if eta:
            print(f"🎯 ETA: {eta}")
        print()

        # Barra de progresso principal
        progress_bar = self.create_progress_bar(completed_files, total_files, 60)
        print("📈 PROGRESSO GERAL:")
        print(f"   {progress_bar}")
        print()

        # Estatísticas de saúde dos arquivos
        if completed_files > 0:
            print("🏥 SAÚDE DOS ARQUIVOS:")
            print(f"   🔴 Quebrados:     {stats['broken']:3d}")
            print(f"   ⚠️ Problemáticos: {stats['problematic']:3d}")
            print(f"   🟡 Com Avisos:    {stats['warning']:3d}")
            print(f"   ✅ OK:           {stats['ok']:3d}")
            if stats['error'] > 0:
                print(f"   💥 Erros:        {stats['error']:3d}")
            print()

            # Problemas encontrados
            total_problems = stats['critical_issues'] + stats['high_issues'] + stats['medium_issues'] + stats['low_issues']
            print("🐛 PROBLEMAS IDENTIFICADOS:")
            print(f"   🚨 Críticos:  {stats['critical_issues']:4d}")
            print(f"   🔺 Altos:     {stats['high_issues']:4d}")
            print(f"   🔸 Médios:    {stats['medium_issues']:4d}")
            print(f"   🔹 Baixos:    {stats['low_issues']:4d}")
            print(f"   📊 TOTAL:     {total_problems:4d}")
            print()

            # Métricas Claude
            print("🤖 ÍNDICES CLAUDE AI:")
            print(f"   🎯 Vícios Médios: {stats['avg_claude_vice']:5.1f}%")
            print(f"   ⏱️ Tempo Correção: {stats['total_fix_time']:5.1f}h")
            print()

        # Velocidade de processamento
        if elapsed > 0 and completed_files > 0:
            files_per_minute = (completed_files / elapsed) * 60
            print("⚡ PERFORMANCE:")
            print(f"   📂 Velocidade: {files_per_minute:.1f} arquivos/min")
            if total_files > completed_files:
                remaining = total_files - completed_files
                remaining_time = remaining / files_per_minute if files_per_minute > 0 else 0
                print(f"   ⏰ Tempo Restante: {self.format_time(remaining_time * 60)}")
            print()

        # Atividade recente
        print("📝 ATIVIDADE RECENTE:")
        activity = self.get_recent_activity()
        for line in activity.split('\n'):
            if line.strip():
                print(f"   {line}")
        print()

        # Instruções
        print("🎮 CONTROLES:")
        print("   Ctrl+C - Parar monitor")
        if not is_running:
            print("   Para iniciar análise: python3 apps/scripturemon/forensic_orchestrator.py")
        else:
            print("   Análise rodando em background...")

        print("="*74)

        # Atualizar timestamp
        self.last_update = datetime.now()

    def run_monitor(self, refresh_interval: int = 5):
        """Executa monitor em loop"""
        print("🚀 Iniciando monitor forense...")
        print("   Atualizando a cada 5 segundos...")
        print("   Pressione Ctrl+C para sair")
        time.sleep(2)

        try:
            while True:
                self.display_dashboard()
                time.sleep(refresh_interval)

        except KeyboardInterrupt:
            self.clear_screen()
            print("\n👋 Monitor forense finalizado.")
            print("📊 Dashboard disponível a qualquer momento executando:")
            print("   python3 apps/scripturemon/forensic_monitor.py")

def main():
    """Função principal"""
    monitor = ForensicMonitor()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--once":
            # Exibir uma vez apenas
            monitor.display_dashboard()
            return
        elif sys.argv[1] == "--help":
            print("📊 Monitor Forense - Scripturemon Champion")
            print()
            print("Uso:")
            print("  python3 forensic_monitor.py          # Monitor contínuo")
            print("  python3 forensic_monitor.py --once   # Exibir uma vez")
            print("  python3 forensic_monitor.py --help   # Esta ajuda")
            return

    # Monitor contínuo
    monitor.run_monitor()

if __name__ == "__main__":
    main()