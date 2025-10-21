#!/usr/bin/env python3
"""
Dashboard de Progresso em Tempo Real

Monitora todas as análises em execução e exibe:
- Progresso visual com barras
- Specialist/Author atual
- ETA (tempo estimado)
- Custo acumulado
- Qualidade média
- Taxa de sucesso

Uso:
    python dashboard.py                    # Atualiza a cada 5s
    python dashboard.py --interval 10      # Atualiza a cada 10s
    python dashboard.py --simple           # Modo simples (sem rich)
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import argparse

# Try importing rich for beautiful terminal UI
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
    from rich.live import Live
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class AnalysisDashboard:
    """Dashboard de monitoramento em tempo real"""

    def __init__(self, workspace_dir: Path = None, use_rich: bool = True):
        self.workspace_dir = workspace_dir or Path('workspace/outputs')
        self.use_rich = use_rich and RICH_AVAILABLE

        if self.use_rich:
            self.console = Console()

    def find_all_analyses(self) -> List[Dict]:
        """Encontra todas as análises em execução ou recentes"""
        analyses = []

        for checkpoint_path in self.workspace_dir.glob('*/2_logs/checkpoint.json'):
            try:
                with open(checkpoint_path, 'r') as f:
                    data = json.load(f)

                folder = checkpoint_path.parent.parent
                completed = len(data.get('completed', []))
                total = data.get('total_analyses', 312)
                percentage = (completed / total * 100) if total > 0 else 0

                started_at = datetime.fromisoformat(data['started_at'])
                last_update_str = data.get('last_update')
                last_update = datetime.fromisoformat(last_update_str) if last_update_str else started_at

                # Calcular ETA
                elapsed = (last_update - started_at).total_seconds()
                remaining = total - completed

                if completed > 0 and remaining > 0:
                    avg_per_analysis = elapsed / completed
                    eta_seconds = avg_per_analysis * remaining
                    eta = last_update + timedelta(seconds=eta_seconds)
                else:
                    eta = None

                # Status: running, paused, completed
                age_seconds = (datetime.now() - last_update).total_seconds()
                if percentage >= 100:
                    status = 'completed'
                elif age_seconds > 300:  # 5 minutos sem atualização
                    status = 'paused'
                else:
                    status = 'running'

                # Informações atuais
                current_specialist = data.get('current_specialist', '?')
                current_author = data.get('current_author', '?')

                analyses.append({
                    'path': folder,
                    'name': folder.name,
                    'data': data,
                    'started_at': started_at,
                    'last_update': last_update,
                    'completed': completed,
                    'total': total,
                    'percentage': percentage,
                    'failed': len(data.get('failed', [])),
                    'status': status,
                    'eta': eta,
                    'elapsed_seconds': elapsed,
                    'current_specialist': current_specialist,
                    'current_author': current_author,
                    'age_seconds': age_seconds
                })

            except Exception as e:
                continue

        # Ordenar: running primeiro, depois por last_update
        analyses.sort(key=lambda x: (
            0 if x['status'] == 'running' else 1 if x['status'] == 'paused' else 2,
            -x['last_update'].timestamp()
        ))

        return analyses

    def format_duration(self, seconds: float) -> str:
        """Formata duração em formato legível"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            return f"{seconds/60:.0f}m"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h{minutes:02d}m"

    def format_eta(self, eta: datetime) -> str:
        """Formata ETA"""
        if not eta:
            return "N/A"

        now = datetime.now()
        if eta < now:
            return "now"

        delta = (eta - now).total_seconds()
        return self.format_duration(delta)

    def calculate_cost(self, analysis: Dict) -> float:
        """Calcula custo estimado baseado no modelo"""
        # Por enquanto, assume $0.11 por análise para GPT
        # e $0.00 para Ollama
        model_info_path = analysis['path'] / '2_logs' / 'model_info.json'

        cost_per_analysis = 0.0

        if model_info_path.exists():
            try:
                with open(model_info_path, 'r') as f:
                    model_data = json.load(f)
                    model = model_data.get('model', '')
                    if model.startswith('gpt-'):
                        cost_per_analysis = 0.11
            except:
                pass

        return analysis['completed'] * cost_per_analysis

    def render_rich_dashboard(self, analyses: List[Dict]) -> Layout:
        """Renderiza dashboard usando Rich"""
        layout = Layout()

        # Header
        header_text = Text()
        header_text.append("🚀 SCRIPTUREMON - DASHBOARD DE PROGRESSO\n", style="bold cyan")
        header_text.append(f"Atualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="dim")

        # Tabela de análises
        table = Table(show_header=True, header_style="bold magenta", expand=True)
        table.add_column("Análise", style="cyan", width=35)
        table.add_column("Progresso", justify="center", width=20)
        table.add_column("Status", justify="center", width=10)
        table.add_column("Atual", width=25)
        table.add_column("ETA", justify="right", width=10)
        table.add_column("Tempo", justify="right", width=10)
        table.add_column("Custo", justify="right", width=10)

        if not analyses:
            table.add_row("Nenhuma análise encontrada", "", "", "", "", "", "")

        for analysis in analyses[:10]:  # Mostrar no máximo 10
            # Nome
            name = analysis['name'][:35]

            # Progresso
            completed = analysis['completed']
            total = analysis['total']
            percentage = analysis['percentage']
            progress_text = f"{completed}/{total} ({percentage:.0f}%)"

            # Status
            if analysis['status'] == 'running':
                status_icon = "🟢"
                status_style = "green"
            elif analysis['status'] == 'paused':
                status_icon = "🟡"
                status_style = "yellow"
            else:
                status_icon = "✅"
                status_style = "blue"

            # Atual
            current = f"Dr{analysis['current_specialist'][:10]}/{analysis['current_author'][:8]}"

            # ETA
            eta_str = self.format_eta(analysis['eta'])

            # Tempo decorrido
            elapsed_str = self.format_duration(analysis['elapsed_seconds'])

            # Custo
            cost = self.calculate_cost(analysis)
            cost_str = f"${cost:.2f}" if cost > 0 else "$0.00"

            table.add_row(
                name,
                progress_text,
                f"{status_icon}",
                current,
                eta_str,
                elapsed_str,
                cost_str
            )

        # Resumo
        total_running = sum(1 for a in analyses if a['status'] == 'running')
        total_paused = sum(1 for a in analyses if a['status'] == 'paused')
        total_completed = sum(1 for a in analyses if a['status'] == 'completed')
        total_analyses = sum(a['completed'] for a in analyses)
        total_cost = sum(self.calculate_cost(a) for a in analyses)

        summary_text = Text()
        summary_text.append(f"\n📊 Resumo: ", style="bold")
        summary_text.append(f"{total_running} em execução | ", style="green")
        summary_text.append(f"{total_paused} pausadas | ", style="yellow")
        summary_text.append(f"{total_completed} completas\n", style="blue")
        summary_text.append(f"🎯 Total de análises: {total_analyses} | ", style="")
        summary_text.append(f"💰 Custo total: ${total_cost:.2f}", style="cyan")

        # Montar layout
        layout.split_column(
            Layout(Panel(header_text, border_style="cyan"), size=3),
            Layout(table),
            Layout(Panel(summary_text, border_style="cyan"), size=4)
        )

        return layout

    def render_simple_dashboard(self, analyses: List[Dict]):
        """Renderiza dashboard em modo simples (sem rich)"""
        # Limpar terminal
        print("\033[2J\033[H")  # Clear screen and move to top

        print("=" * 100)
        print("🚀 SCRIPTUREMON - DASHBOARD DE PROGRESSO")
        print(f"Atualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 100)
        print()

        if not analyses:
            print("⚠️  Nenhuma análise encontrada.")
            print()
            return

        # Cabeçalho
        print(f"{'Análise':<35} {'Progresso':<20} {'St':<4} {'Atual':<25} {'ETA':<10} {'Tempo':<10} {'Custo':<10}")
        print("-" * 100)

        for analysis in analyses[:10]:
            # Nome
            name = analysis['name'][:35]

            # Progresso
            completed = analysis['completed']
            total = analysis['total']
            percentage = analysis['percentage']

            # Barra de progresso simples
            bar_width = 15
            filled = int(bar_width * percentage / 100)
            bar = "█" * filled + "░" * (bar_width - filled)
            progress_text = f"{bar} {percentage:>3.0f}%"

            # Status
            if analysis['status'] == 'running':
                status_icon = "🟢"
            elif analysis['status'] == 'paused':
                status_icon = "🟡"
            else:
                status_icon = "✅"

            # Atual
            current = f"Dr{analysis['current_specialist'][:10]}/{analysis['current_author'][:8]}"

            # ETA
            eta_str = self.format_eta(analysis['eta'])

            # Tempo
            elapsed_str = self.format_duration(analysis['elapsed_seconds'])

            # Custo
            cost = self.calculate_cost(analysis)
            cost_str = f"${cost:.2f}" if cost > 0 else "$0.00"

            print(f"{name:<35} {progress_text:<20} {status_icon:<4} {current:<25} {eta_str:<10} {elapsed_str:<10} {cost_str:<10}")

        print("-" * 100)

        # Resumo
        total_running = sum(1 for a in analyses if a['status'] == 'running')
        total_paused = sum(1 for a in analyses if a['status'] == 'paused')
        total_completed = sum(1 for a in analyses if a['status'] == 'completed')
        total_analyses = sum(a['completed'] for a in analyses)
        total_cost = sum(self.calculate_cost(a) for a in analyses)

        print()
        print(f"📊 Resumo: {total_running} em execução | {total_paused} pausadas | {total_completed} completas")
        print(f"🎯 Total de análises: {total_analyses} | 💰 Custo total: ${total_cost:.2f}")
        print()
        print("=" * 100)
        print("Pressione Ctrl+C para sair")
        print()

    def run(self, interval: int = 5):
        """Executa dashboard com atualização automática"""
        if self.use_rich:
            self._run_rich(interval)
        else:
            self._run_simple(interval)

    def _run_rich(self, interval: int):
        """Executa dashboard com Rich"""
        try:
            with Live(console=self.console, refresh_per_second=1) as live:
                while True:
                    analyses = self.find_all_analyses()
                    layout = self.render_rich_dashboard(analyses)
                    live.update(layout)
                    time.sleep(interval)
        except KeyboardInterrupt:
            self.console.print("\n\n👋 Dashboard encerrado.", style="bold yellow")

    def _run_simple(self, interval: int):
        """Executa dashboard em modo simples"""
        try:
            while True:
                analyses = self.find_all_analyses()
                self.render_simple_dashboard(analyses)
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n👋 Dashboard encerrado.")

    def snapshot(self):
        """Exibe snapshot único (não atualiza)"""
        analyses = self.find_all_analyses()

        if self.use_rich:
            layout = self.render_rich_dashboard(analyses)
            self.console.print(layout)
        else:
            self.render_simple_dashboard(analyses)


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description='Dashboard de progresso em tempo real')
    parser.add_argument('--interval', type=int, default=5, help='Intervalo de atualização em segundos')
    parser.add_argument('--simple', action='store_true', help='Modo simples sem Rich')
    parser.add_argument('--snapshot', action='store_true', help='Exibir apenas uma vez (sem loop)')
    parser.add_argument('--workspace', type=Path, default=Path('workspace/outputs'), help='Diretório de workspace')

    args = parser.parse_args()

    use_rich = not args.simple

    if use_rich and not RICH_AVAILABLE:
        print("⚠️  Biblioteca 'rich' não encontrada. Usando modo simples.")
        print("💡 Instale com: pip install rich")
        print()
        use_rich = False

    dashboard = AnalysisDashboard(workspace_dir=args.workspace, use_rich=use_rich)

    if args.snapshot:
        dashboard.snapshot()
    else:
        print(f"🚀 Iniciando dashboard (atualização a cada {args.interval}s)...")
        print("   Pressione Ctrl+C para sair\n")
        time.sleep(1)
        dashboard.run(interval=args.interval)


if __name__ == '__main__':
    main()
