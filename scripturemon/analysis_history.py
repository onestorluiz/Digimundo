#!/usr/bin/env python3
"""
Histórico de Análises

Mantém registro histórico de todas as análises realizadas:
- Screenplay analisado
- Data/hora de início e fim
- Specialists utilizados
- Qualidade média obtida
- Tempo total de execução
- Modelo LLM usado
- Custo estimado
- Status final

Uso:
    python analysis_history.py                        # Lista histórico completo
    python analysis_history.py --recent 10            # Últimas 10 análises
    python analysis_history.py --screenplay "Nome"    # Busca por screenplay
    python analysis_history.py --export history.csv   # Exporta para CSV
    python analysis_history.py --stats                # Estatísticas gerais
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse


class AnalysisHistory:
    """Gerenciador de histórico de análises"""

    def __init__(self, history_file: Path = None):
        self.history_file = history_file or Path('workspace/history/analyses.json')
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load_history()

    def _load_history(self) -> Dict:
        """Carrega histórico do arquivo"""
        if not self.history_file.exists():
            return {
                'version': '1.0',
                'created_at': datetime.now().isoformat(),
                'analyses': []
            }

        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Erro ao carregar histórico: {e}")
            return {
                'version': '1.0',
                'created_at': datetime.now().isoformat(),
                'analyses': []
            }

    def _save_history(self):
        """Salva histórico no arquivo"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Erro ao salvar histórico: {e}")

    def add_analysis(
        self,
        screenplay_path: str,
        screenplay_name: str,
        started_at: str,
        completed_at: str,
        total_analyses: int,
        completed_analyses: int,
        failed_analyses: int,
        specialists_used: List[str],
        authors_used: List[str],
        avg_quality: float,
        total_time_seconds: float,
        llm_model: str,
        estimated_cost: float,
        output_dir: str,
        status: str = "completed"
    ):
        """
        Adiciona uma análise ao histórico

        Args:
            screenplay_path: Caminho do roteiro
            screenplay_name: Nome do roteiro
            started_at: ISO timestamp de início
            completed_at: ISO timestamp de conclusão
            total_analyses: Total de análises planejadas
            completed_analyses: Análises completadas
            failed_analyses: Análises falhadas
            specialists_used: Lista de specialists usados
            authors_used: Lista de authors usados
            avg_quality: Qualidade média (0-10)
            total_time_seconds: Tempo total em segundos
            llm_model: Modelo LLM usado
            estimated_cost: Custo estimado total
            output_dir: Diretório de saída
            status: Status final (completed, partial, failed)
        """
        analysis_entry = {
            'id': len(self.data['analyses']) + 1,
            'screenplay': {
                'path': screenplay_path,
                'name': screenplay_name
            },
            'timestamps': {
                'started_at': started_at,
                'completed_at': completed_at
            },
            'results': {
                'total_analyses': total_analyses,
                'completed': completed_analyses,
                'failed': failed_analyses,
                'completion_percentage': (completed_analyses / total_analyses * 100) if total_analyses > 0 else 0
            },
            'specialists': {
                'count': len(specialists_used),
                'list': specialists_used
            },
            'authors': {
                'count': len(authors_used),
                'list': authors_used
            },
            'quality': {
                'average': avg_quality,
                'rating': self._quality_rating(avg_quality)
            },
            'performance': {
                'total_time_seconds': total_time_seconds,
                'total_time_hours': total_time_seconds / 3600,
                'avg_per_analysis_minutes': (total_time_seconds / completed_analyses / 60) if completed_analyses > 0 else 0
            },
            'llm': {
                'model': llm_model,
                'estimated_cost': estimated_cost
            },
            'output': {
                'directory': output_dir
            },
            'status': status
        }

        self.data['analyses'].append(analysis_entry)
        self._save_history()

        return analysis_entry['id']

    def _quality_rating(self, score: float) -> str:
        """Converte score em rating"""
        if score >= 9.0:
            return "Excepcional"
        elif score >= 8.0:
            return "Excelente"
        elif score >= 7.0:
            return "Muito Bom"
        elif score >= 6.0:
            return "Bom"
        elif score >= 5.0:
            return "Regular"
        else:
            return "Precisa Melhorar"

    def get_all(self) -> List[Dict]:
        """Retorna todas as análises"""
        return self.data.get('analyses', [])

    def get_recent(self, count: int = 10) -> List[Dict]:
        """Retorna as N análises mais recentes"""
        analyses = self.get_all()
        # Ordenar por completed_at (mais recente primeiro)
        analyses.sort(key=lambda x: x['timestamps']['completed_at'], reverse=True)
        return analyses[:count]

    def search_by_screenplay(self, screenplay_name: str) -> List[Dict]:
        """Busca análises por nome do screenplay"""
        analyses = self.get_all()
        search_lower = screenplay_name.lower()

        return [
            a for a in analyses
            if search_lower in a['screenplay']['name'].lower()
        ]

    def get_by_status(self, status: str) -> List[Dict]:
        """Retorna análises por status"""
        return [a for a in self.get_all() if a['status'] == status]

    def get_stats(self) -> Dict:
        """Calcula estatísticas gerais do histórico"""
        analyses = self.get_all()

        if not analyses:
            return {
                'total_analyses': 0,
                'total_screenplays': 0,
                'total_individual_analyses': 0,
                'total_time_hours': 0,
                'total_cost': 0,
                'avg_quality': 0,
                'status_breakdown': {},
                'most_used_specialist': None,
                'most_used_model': None,
                'specialist_usage': {},
                'model_usage': {}
            }

        # Contadores
        total_time = sum(a['performance']['total_time_seconds'] for a in analyses)
        total_cost = sum(a['llm']['estimated_cost'] for a in analyses)
        total_completed = sum(a['results']['completed'] for a in analyses)

        # Qualidade média
        quality_scores = [a['quality']['average'] for a in analyses if a['quality']['average'] > 0]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0

        # Breakdown por status
        status_breakdown = {}
        for analysis in analyses:
            status = analysis['status']
            status_breakdown[status] = status_breakdown.get(status, 0) + 1

        # Specialist mais usado
        specialist_counts = {}
        for analysis in analyses:
            for specialist in analysis['specialists']['list']:
                specialist_counts[specialist] = specialist_counts.get(specialist, 0) + 1

        most_used_specialist = max(specialist_counts.items(), key=lambda x: x[1])[0] if specialist_counts else None

        # Modelo mais usado
        model_counts = {}
        for analysis in analyses:
            model = analysis['llm']['model']
            model_counts[model] = model_counts.get(model, 0) + 1

        most_used_model = max(model_counts.items(), key=lambda x: x[1])[0] if model_counts else None

        # Screenplays únicos
        unique_screenplays = len(set(a['screenplay']['name'] for a in analyses))

        return {
            'total_analyses': len(analyses),
            'total_screenplays': unique_screenplays,
            'total_individual_analyses': total_completed,
            'total_time_hours': total_time / 3600,
            'total_cost': total_cost,
            'avg_quality': avg_quality,
            'status_breakdown': status_breakdown,
            'most_used_specialist': most_used_specialist,
            'most_used_model': most_used_model,
            'specialist_usage': specialist_counts,
            'model_usage': model_counts
        }

    def export_csv(self, output_file: Path):
        """Exporta histórico para CSV"""
        import csv

        analyses = self.get_all()

        if not analyses:
            print("⚠️  Nenhuma análise para exportar.")
            return

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'ID', 'Screenplay', 'Started', 'Completed', 'Duration (h)',
                'Status', 'Completed Analyses', 'Failed Analyses', 'Completion %',
                'Avg Quality', 'Quality Rating', 'Specialists Count', 'Specialists',
                'Model', 'Cost', 'Output Dir'
            ]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for analysis in analyses:
                writer.writerow({
                    'ID': analysis['id'],
                    'Screenplay': analysis['screenplay']['name'],
                    'Started': analysis['timestamps']['started_at'],
                    'Completed': analysis['timestamps']['completed_at'],
                    'Duration (h)': f"{analysis['performance']['total_time_hours']:.2f}",
                    'Status': analysis['status'],
                    'Completed Analyses': analysis['results']['completed'],
                    'Failed Analyses': analysis['results']['failed'],
                    'Completion %': f"{analysis['results']['completion_percentage']:.1f}",
                    'Avg Quality': f"{analysis['quality']['average']:.1f}",
                    'Quality Rating': analysis['quality']['rating'],
                    'Specialists Count': analysis['specialists']['count'],
                    'Specialists': ', '.join(analysis['specialists']['list']),
                    'Model': analysis['llm']['model'],
                    'Cost': f"${analysis['llm']['estimated_cost']:.2f}",
                    'Output Dir': analysis['output']['directory']
                })

        print(f"✅ Histórico exportado para: {output_file}")
        print(f"   Total: {len(analyses)} análises")

    def print_history(self, analyses: List[Dict], detailed: bool = False):
        """Exibe histórico formatado"""
        if not analyses:
            print("\n⚠️  Nenhuma análise encontrada.\n")
            return

        print("\n" + "=" * 100)
        print("📚 HISTÓRICO DE ANÁLISES")
        print("=" * 100)
        print()

        for analysis in analyses:
            # Cabeçalho
            print(f"#{analysis['id']:03d} - {analysis['screenplay']['name']}")
            print("-" * 100)

            # Timestamps
            started = datetime.fromisoformat(analysis['timestamps']['started_at'])
            completed = datetime.fromisoformat(analysis['timestamps']['completed_at'])
            print(f"   📅 Início: {started.strftime('%Y-%m-%d %H:%M')}")
            print(f"   ✅ Término: {completed.strftime('%Y-%m-%d %H:%M')}")
            print(f"   ⏱️  Duração: {analysis['performance']['total_time_hours']:.1f}h")

            # Resultados
            print(f"   📊 Progresso: {analysis['results']['completed']}/{analysis['results']['total_analyses']} ({analysis['results']['completion_percentage']:.0f}%)")

            if analysis['results']['failed'] > 0:
                print(f"   ❌ Falhas: {analysis['results']['failed']}")

            # Qualidade
            print(f"   🎯 Qualidade: {analysis['quality']['average']:.1f}/10 ({analysis['quality']['rating']})")

            # Specialists
            if detailed:
                print(f"   🔬 Specialists ({analysis['specialists']['count']}): {', '.join(analysis['specialists']['list'][:5])}")
                if len(analysis['specialists']['list']) > 5:
                    print(f"       ... e mais {len(analysis['specialists']['list']) - 5}")

            # Modelo e custo
            cost_str = f"${analysis['llm']['estimated_cost']:.2f}" if analysis['llm']['estimated_cost'] > 0 else "$0.00 (gratuito)"
            print(f"   🤖 Modelo: {analysis['llm']['model']}")
            print(f"   💰 Custo: {cost_str}")

            # Status
            status_icons = {
                'completed': '✅',
                'partial': '⚠️',
                'failed': '❌'
            }
            status_icon = status_icons.get(analysis['status'], '❓')
            print(f"   {status_icon} Status: {analysis['status']}")

            # Output
            if detailed:
                print(f"   📁 Output: {analysis['output']['directory']}")

            print()

        print("=" * 100)
        print(f"Total: {len(analyses)} análise(s)")
        print()

    def print_stats(self):
        """Exibe estatísticas gerais"""
        stats = self.get_stats()

        print("\n" + "=" * 100)
        print("📊 ESTATÍSTICAS GERAIS DO HISTÓRICO")
        print("=" * 100)
        print()

        print(f"🎬 Total de análises completas: {stats['total_analyses']}")
        print(f"📚 Roteiros únicos analisados: {stats['total_screenplays']}")
        print(f"🔬 Análises individuais realizadas: {stats['total_individual_analyses']}")
        print(f"⏱️  Tempo total de análise: {stats['total_time_hours']:.1f}h")
        print(f"💰 Custo total acumulado: ${stats['total_cost']:.2f}")
        print(f"🎯 Qualidade média: {stats['avg_quality']:.1f}/10")
        print()

        # Breakdown por status
        if stats['status_breakdown']:
            print("📈 Breakdown por Status:")
            for status, count in stats['status_breakdown'].items():
                print(f"   • {status}: {count}")
            print()

        # Specialists mais usados
        if stats['specialist_usage']:
            print("🔬 Top 5 Specialists Mais Usados:")
            sorted_specialists = sorted(stats['specialist_usage'].items(), key=lambda x: x[1], reverse=True)[:5]
            for i, (specialist, count) in enumerate(sorted_specialists, 1):
                print(f"   {i}. Dr{specialist.title()}: {count} análises")
            print()

        # Modelos mais usados
        if stats['model_usage']:
            print("🤖 Modelos LLM Utilizados:")
            for model, count in stats['model_usage'].items():
                print(f"   • {model}: {count} análises")
            print()

        print("=" * 100)
        print()


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description='Histórico de análises do Scripturemon')
    parser.add_argument('--recent', type=int, metavar='N', help='Mostrar últimas N análises')
    parser.add_argument('--screenplay', type=str, help='Buscar por nome do screenplay')
    parser.add_argument('--status', type=str, choices=['completed', 'partial', 'failed'], help='Filtrar por status')
    parser.add_argument('--export', type=Path, help='Exportar para CSV')
    parser.add_argument('--stats', action='store_true', help='Exibir estatísticas gerais')
    parser.add_argument('--detailed', action='store_true', help='Exibir detalhes completos')
    parser.add_argument('--history-file', type=Path, help='Arquivo de histórico customizado')

    args = parser.parse_args()

    history = AnalysisHistory(history_file=args.history_file)

    # Export
    if args.export:
        history.export_csv(args.export)
        return

    # Stats
    if args.stats:
        history.print_stats()
        return

    # Lista conforme filtros
    if args.screenplay:
        analyses = history.search_by_screenplay(args.screenplay)
    elif args.status:
        analyses = history.get_by_status(args.status)
    elif args.recent:
        analyses = history.get_recent(args.recent)
    else:
        analyses = history.get_all()

    history.print_history(analyses, detailed=args.detailed)


if __name__ == '__main__':
    main()
