#!/usr/bin/env python3
"""
Preview de Análise

Gera preview rápido de uma análise completa:
- Sumário executivo
- Scores gerais
- Top insights de cada specialist
- Forças e fraquezas identificadas
- Recomendações principais

Uso:
    python analysis_preview.py <analysis_dir>
    python analysis_preview.py workspace/outputs/TE_ENCONTRO_EM_MIM__all_specialists_0004
    python analysis_preview.py --latest                                    # Preview da análise mais recente
    python analysis_preview.py <analysis_dir> --export preview.md          # Exportar para Markdown
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse


class AnalysisPreview:
    """Gera preview de análises completas"""

    def __init__(self, analysis_dir: Path):
        self.analysis_dir = Path(analysis_dir)
        self.checkpoint_file = self.analysis_dir / '2_logs' / 'checkpoint.json'
        self.results_dir = self.analysis_dir / '1_results'

        if not self.checkpoint_file.exists():
            raise FileNotFoundError(f"Checkpoint não encontrado: {self.checkpoint_file}")

        self.checkpoint = self._load_checkpoint()
        self.results = self._load_results()

    def _load_checkpoint(self) -> Dict:
        """Carrega checkpoint"""
        with open(self.checkpoint_file, 'r') as f:
            return json.load(f)

    def _load_results(self) -> Dict[str, Dict]:
        """Carrega todos os resultados disponíveis"""
        results = {}

        if not self.results_dir.exists():
            return results

        for result_file in self.results_dir.glob('*.json'):
            try:
                with open(result_file, 'r') as f:
                    data = json.load(f)
                    # Nome do arquivo sem extensão é a chave
                    key = result_file.stem
                    results[key] = data
            except Exception as e:
                continue

        return results

    def get_summary_stats(self) -> Dict:
        """Calcula estatísticas gerais"""
        completed = len(self.checkpoint.get('completed', []))
        total = self.checkpoint.get('total_analyses', 312)
        failed = len(self.checkpoint.get('failed', []))

        started = datetime.fromisoformat(self.checkpoint['started_at'])
        last_update_str = self.checkpoint.get('last_update', self.checkpoint['started_at'])
        last_update = datetime.fromisoformat(last_update_str)

        duration = (last_update - started).total_seconds()

        # Agrupar por specialist
        specialists = {}
        for spec, author in self.checkpoint.get('completed', []):
            if spec not in specialists:
                specialists[spec] = []
            specialists[spec].append(author)

        return {
            'completed': completed,
            'total': total,
            'failed': failed,
            'percentage': (completed / total * 100) if total > 0 else 0,
            'duration_hours': duration / 3600,
            'avg_minutes_per_analysis': (duration / completed / 60) if completed > 0 else 0,
            'specialists_used': list(specialists.keys()),
            'specialists_count': len(specialists),
            'authors_per_specialist': specialists,
            'started_at': started,
            'last_update': last_update
        }

    def extract_top_insights(self, limit: int = 3) -> Dict[str, List[str]]:
        """Extrai top insights de cada specialist"""
        insights = {}

        for key, data in self.results.items():
            # Tentar extrair insights
            # (Assumindo formato padrão dos resultados)
            if 'insights' in data:
                specialist = data.get('specialist', 'unknown')
                if specialist not in insights:
                    insights[specialist] = []

                # Pegar top insights
                for insight in data['insights'][:limit]:
                    insights[specialist].append(insight)

            elif 'recommendations' in data:
                specialist = data.get('specialist', 'unknown')
                if specialist not in insights:
                    insights[specialist] = []

                for rec in data['recommendations'][:limit]:
                    insights[specialist].append(rec)

        return insights

    def extract_quality_scores(self) -> Dict[str, float]:
        """Extrai scores de qualidade"""
        scores = {}

        for key, data in self.results.items():
            if 'quality_score' in data:
                specialist = data.get('specialist', key)
                scores[specialist] = data['quality_score']

            elif 'score' in data:
                specialist = data.get('specialist', key)
                scores[specialist] = data['score']

        return scores

    def generate_preview(self) -> str:
        """Gera preview formatado"""
        stats = self.get_summary_stats()

        preview = []

        # Cabeçalho
        preview.append("=" * 80)
        preview.append("🎬 SCRIPTUREMON - PREVIEW DE ANÁLISE")
        preview.append("=" * 80)
        preview.append("")

        # Informações básicas
        preview.append(f"📁 Análise: {self.analysis_dir.name}")
        preview.append(f"📅 Iniciada: {stats['started_at'].strftime('%Y-%m-%d %H:%M')}")
        preview.append(f"📅 Última atualização: {stats['last_update'].strftime('%Y-%m-%d %H:%M')}")
        preview.append("")

        # Progresso
        preview.append("📊 PROGRESSO")
        preview.append("-" * 80)
        preview.append(f"   Análises completadas: {stats['completed']}/{stats['total']} ({stats['percentage']:.1f}%)")

        if stats['failed'] > 0:
            preview.append(f"   ❌ Falhas: {stats['failed']}")

        preview.append(f"   ⏱️  Tempo total: {stats['duration_hours']:.1f}h")
        preview.append(f"   ⚡ Média por análise: {stats['avg_minutes_per_analysis']:.1f} min")
        preview.append("")

        # Specialists
        preview.append("🔬 SPECIALISTS UTILIZADOS")
        preview.append("-" * 80)

        for spec in stats['specialists_used']:
            authors = stats['authors_per_specialist'].get(spec, [])
            preview.append(f"   • Dr{spec.title()}: {len(authors)} authors ({', '.join(authors[:3])}{'...' if len(authors) > 3 else ''})")

        preview.append("")

        # Quality Scores
        scores = self.extract_quality_scores()

        if scores:
            preview.append("🎯 SCORES DE QUALIDADE")
            preview.append("-" * 80)

            # Ordenar por score
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

            for specialist, score in sorted_scores[:10]:
                stars = "⭐" * int(score / 2)
                preview.append(f"   {specialist:<20} {score:.1f}/10 {stars}")

            avg_score = sum(scores.values()) / len(scores)
            preview.append("")
            preview.append(f"   📊 Qualidade Média: {avg_score:.1f}/10")
            preview.append("")

        # Top Insights
        insights = self.extract_top_insights(limit=3)

        if insights:
            preview.append("💡 TOP INSIGHTS")
            preview.append("-" * 80)

            for specialist, specialist_insights in list(insights.items())[:5]:
                preview.append(f"\n   🔬 Dr{specialist.title()}:")

                for i, insight in enumerate(specialist_insights[:3], 1):
                    # Truncar se muito longo
                    insight_text = insight if isinstance(insight, str) else str(insight)
                    if len(insight_text) > 100:
                        insight_text = insight_text[:97] + "..."

                    preview.append(f"      {i}. {insight_text}")

            preview.append("")

        # Status
        preview.append("📋 STATUS")
        preview.append("-" * 80)

        if stats['percentage'] >= 100:
            preview.append("   ✅ ANÁLISE COMPLETA")
        elif stats['percentage'] >= 75:
            preview.append("   🟢 ANÁLISE QUASE COMPLETA")
        elif stats['percentage'] >= 50:
            preview.append("   🟡 ANÁLISE EM PROGRESSO")
        elif stats['percentage'] >= 25:
            preview.append("   🟠 ANÁLISE INICIADA")
        else:
            preview.append("   🔴 ANÁLISE NO INÍCIO")

        preview.append("")

        # Recomendações
        preview.append("💡 PRÓXIMOS PASSOS")
        preview.append("-" * 80)

        if stats['percentage'] < 100:
            remaining = stats['total'] - stats['completed']
            eta_hours = remaining * stats['avg_minutes_per_analysis'] / 60

            preview.append(f"   • Faltam {remaining} análises ({eta_hours:.1f}h estimadas)")
            preview.append("   • Continue a análise ou monitore o progresso com dashboard.py")
        else:
            preview.append("   • Análise completa! Revise os reports HTML/Markdown")
            preview.append("   • Execute benchmark_performance.py para análise de performance")
            preview.append("   • Use compare_analyses.py para comparar com outras análises")

        preview.append("")
        preview.append("=" * 80)
        preview.append("")

        return "\n".join(preview)

    def export_markdown(self, output_file: Path):
        """Exporta preview para Markdown"""
        content = self.generate_preview()

        # Converter para Markdown apropriado
        md_content = content.replace("=" * 80, "---")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"✅ Preview exportado para: {output_file}")


def find_latest_analysis(workspace_dir: Path = Path('workspace/outputs')) -> Optional[Path]:
    """Encontra análise mais recente"""
    analyses = []

    for checkpoint_path in workspace_dir.glob('*/2_logs/checkpoint.json'):
        try:
            with open(checkpoint_path, 'r') as f:
                data = json.load(f)

            last_update_str = data.get('last_update', data.get('started_at'))
            if last_update_str:
                last_update = datetime.fromisoformat(last_update_str)
                analyses.append({
                    'path': checkpoint_path.parent.parent,
                    'last_update': last_update
                })

        except:
            continue

    if not analyses:
        return None

    # Retornar mais recente
    latest = max(analyses, key=lambda x: x['last_update'])
    return latest['path']


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(
        description='Preview de análise do Scripturemon',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python analysis_preview.py workspace/outputs/TE_ENCONTRO_EM_MIM__all_specialists_0004
  python analysis_preview.py --latest
  python analysis_preview.py workspace/outputs/analysis_0001 --export preview.md
        """
    )

    parser.add_argument('analysis_dir', nargs='?', help='Diretório da análise')
    parser.add_argument('--latest', action='store_true', help='Preview da análise mais recente')
    parser.add_argument('--export', type=Path, help='Exportar para arquivo Markdown')

    args = parser.parse_args()

    # Determinar análise
    if args.latest:
        analysis_dir = find_latest_analysis()
        if not analysis_dir:
            print("\n❌ Nenhuma análise encontrada.\n")
            sys.exit(1)

        print(f"📊 Análise mais recente: {analysis_dir.name}\n")

    elif args.analysis_dir:
        analysis_dir = Path(args.analysis_dir)

        if not analysis_dir.exists():
            print(f"\n❌ Diretório não encontrado: {analysis_dir}\n")
            sys.exit(1)

    else:
        parser.print_help()
        print()
        print("💡 Use --latest para preview da análise mais recente")
        print()
        sys.exit(1)

    # Gerar preview
    try:
        preview = AnalysisPreview(analysis_dir)

        if args.export:
            preview.export_markdown(args.export)
        else:
            print(preview.generate_preview())

    except FileNotFoundError as e:
        print(f"\n❌ Erro: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro ao gerar preview: {e}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
