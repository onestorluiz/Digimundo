#!/usr/bin/env python3
"""
Comparador Melhorado de Análises

Compare duas análises lado a lado:
- Progresso relativo
- Tempo de execução
- Qualidade média
- Specialists completos
- Diferenças detalhadas

Uso:
    python compare_analyses.py <checkpoint1> <checkpoint2>
    python compare_analyses.py --list                          # Lista análises disponíveis
    python compare_analyses.py --latest                        # Compara 2 mais recentes
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


class AnalysisComparator:
    """Compara duas análises"""

    def __init__(self, workspace_dir: Path = None):
        self.workspace_dir = workspace_dir or Path('workspace/outputs')

    def find_all_analyses(self) -> List[Dict]:
        """Encontra todas as análises"""
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

                analyses.append({
                    'path': folder,
                    'checkpoint_path': checkpoint_path,
                    'name': folder.name,
                    'data': data,
                    'started_at': started_at,
                    'last_update': last_update,
                    'completed': completed,
                    'total': total,
                    'percentage': percentage,
                    'failed': len(data.get('failed', []))
                })

            except Exception as e:
                continue

        # Ordenar por data de update (mais recente primeiro)
        analyses.sort(key=lambda x: x['last_update'], reverse=True)

        return analyses

    def load_analysis(self, path: str) -> Dict:
        """Carrega uma análise específica"""
        checkpoint_path = Path(path) / '2_logs' / 'checkpoint.json'

        if not checkpoint_path.exists():
            # Tentar como nome de pasta
            for analysis in self.find_all_analyses():
                if analysis['name'] == path or str(analysis['path']).endswith(path):
                    return analysis
            raise FileNotFoundError(f"Análise não encontrada: {path}")

        with open(checkpoint_path, 'r') as f:
            data = json.load(f)

        folder = checkpoint_path.parent.parent
        completed = len(data.get('completed', []))
        total = data.get('total_analyses', 312)
        percentage = (completed / total * 100) if total > 0 else 0

        started_at = datetime.fromisoformat(data['started_at'])
        last_update_str = data.get('last_update')
        last_update = datetime.fromisoformat(last_update_str) if last_update_str else started_at

        return {
            'path': folder,
            'checkpoint_path': checkpoint_path,
            'name': folder.name,
            'data': data,
            'started_at': started_at,
            'last_update': last_update,
            'completed': completed,
            'total': total,
            'percentage': percentage,
            'failed': len(data.get('failed', []))
        }

    def compare_progress(self, analysis1: Dict, analysis2: Dict) -> Dict:
        """Compara progresso entre duas análises"""
        return {
            'analysis1': {
                'completed': analysis1['completed'],
                'percentage': analysis1['percentage'],
                'failed': analysis1['failed']
            },
            'analysis2': {
                'completed': analysis2['completed'],
                'percentage': analysis2['percentage'],
                'failed': analysis2['failed']
            },
            'diff': {
                'completed': analysis2['completed'] - analysis1['completed'],
                'percentage': analysis2['percentage'] - analysis1['percentage'],
                'failed': analysis2['failed'] - analysis1['failed']
            }
        }

    def compare_timing(self, analysis1: Dict, analysis2: Dict) -> Dict:
        """Compara tempo de execução"""
        duration1 = (analysis1['last_update'] - analysis1['started_at']).total_seconds()
        duration2 = (analysis2['last_update'] - analysis2['started_at']).total_seconds()

        avg_per_analysis1 = duration1 / analysis1['completed'] if analysis1['completed'] > 0 else 0
        avg_per_analysis2 = duration2 / analysis2['completed'] if analysis2['completed'] > 0 else 0

        return {
            'analysis1': {
                'total_seconds': duration1,
                'total_hours': duration1 / 3600,
                'avg_per_analysis_minutes': avg_per_analysis1 / 60
            },
            'analysis2': {
                'total_seconds': duration2,
                'total_hours': duration2 / 3600,
                'avg_per_analysis_minutes': avg_per_analysis2 / 60
            },
            'diff': {
                'total_seconds': duration2 - duration1,
                'avg_per_analysis_seconds': avg_per_analysis2 - avg_per_analysis1,
                'speedup_factor': avg_per_analysis1 / avg_per_analysis2 if avg_per_analysis2 > 0 else 0
            }
        }

    def compare_specialists(self, analysis1: Dict, analysis2: Dict) -> Dict:
        """Compara specialists completos"""
        completed1 = set(tuple(item) for item in analysis1['data'].get('completed', []))
        completed2 = set(tuple(item) for item in analysis2['data'].get('completed', []))

        only_in_1 = completed1 - completed2
        only_in_2 = completed2 - completed1
        in_both = completed1 & completed2

        # Agrupar por specialist
        specialists1 = {}
        specialists2 = {}

        for spec, author in completed1:
            if spec not in specialists1:
                specialists1[spec] = []
            specialists1[spec].append(author)

        for spec, author in completed2:
            if spec not in specialists2:
                specialists2[spec] = []
            specialists2[spec].append(author)

        return {
            'only_in_1': list(only_in_1),
            'only_in_2': list(only_in_2),
            'in_both': len(in_both),
            'specialists_only_1': set(specialists1.keys()) - set(specialists2.keys()),
            'specialists_only_2': set(specialists2.keys()) - set(specialists1.keys()),
            'specialists_both': set(specialists1.keys()) & set(specialists2.keys())
        }

    def print_comparison(self, analysis1: Dict, analysis2: Dict):
        """Exibe comparação formatada"""
        print("\n" + "=" * 80)
        print("🔄 COMPARAÇÃO DE ANÁLISES")
        print("=" * 80)
        print()

        # Cabeçalho
        print(f"📊 Análise 1: {analysis1['name']}")
        print(f"   Iniciada: {analysis1['started_at'].strftime('%Y-%m-%d %H:%M')}")
        print(f"   Atualizada: {analysis1['last_update'].strftime('%Y-%m-%d %H:%M')}")
        print()

        print(f"📊 Análise 2: {analysis2['name']}")
        print(f"   Iniciada: {analysis2['started_at'].strftime('%Y-%m-%d %H:%M')}")
        print(f"   Atualizada: {analysis2['last_update'].strftime('%Y-%m-%d %H:%M')}")
        print()

        # Progresso
        progress = self.compare_progress(analysis1, analysis2)

        print("📈 PROGRESSO")
        print("-" * 80)
        print(f"   Análise 1: {progress['analysis1']['completed']}/{analysis1['total']} ({progress['analysis1']['percentage']:.1f}%)")
        print(f"   Análise 2: {progress['analysis2']['completed']}/{analysis2['total']} ({progress['analysis2']['percentage']:.1f}%)")

        diff = progress['diff']['completed']
        diff_str = f"+{diff}" if diff > 0 else str(diff)
        print(f"   Diferença: {diff_str} análises ({progress['diff']['percentage']:+.1f}%)")
        print()

        # Falhas
        if progress['analysis1']['failed'] > 0 or progress['analysis2']['failed'] > 0:
            print(f"   ❌ Falhas Análise 1: {progress['analysis1']['failed']}")
            print(f"   ❌ Falhas Análise 2: {progress['analysis2']['failed']}")
            print(f"   Diferença: {progress['diff']['failed']:+d}")
            print()

        # Timing
        timing = self.compare_timing(analysis1, analysis2)

        print("⏱️  TEMPO DE EXECUÇÃO")
        print("-" * 80)
        print(f"   Análise 1: {timing['analysis1']['total_hours']:.1f}h (média: {timing['analysis1']['avg_per_analysis_minutes']:.1f} min/análise)")
        print(f"   Análise 2: {timing['analysis2']['total_hours']:.1f}h (média: {timing['analysis2']['avg_per_analysis_minutes']:.1f} min/análise)")

        if timing['diff']['speedup_factor'] > 0:
            if timing['diff']['speedup_factor'] > 1:
                print(f"   ⚡ Análise 2 é {timing['diff']['speedup_factor']:.1f}x MAIS RÁPIDA")
            elif timing['diff']['speedup_factor'] < 1:
                print(f"   🐌 Análise 2 é {1/timing['diff']['speedup_factor']:.1f}x MAIS LENTA")
        print()

        # Specialists
        specialists = self.compare_specialists(analysis1, analysis2)

        print("🔬 SPECIALISTS")
        print("-" * 80)
        print(f"   Em ambas: {specialists['in_both']} análises idênticas")
        print(f"   Apenas em Análise 1: {len(specialists['only_in_1'])} análises")
        print(f"   Apenas em Análise 2: {len(specialists['only_in_2'])} análises")
        print()

        if specialists['specialists_only_1']:
            print(f"   Specialists apenas em 1: {', '.join(specialists['specialists_only_1'])}")
        if specialists['specialists_only_2']:
            print(f"   Specialists apenas em 2: {', '.join(specialists['specialists_only_2'])}")
        if specialists['specialists_only_1'] or specialists['specialists_only_2']:
            print()

        # Recomendações
        print("💡 RECOMENDAÇÕES")
        print("-" * 80)

        if progress['analysis2']['percentage'] < progress['analysis1']['percentage']:
            print("   ⚠️  Análise 2 está ATRÁS da Análise 1")
            print("   → Considere continuar Análise 2 ou remover se não for mais necessária")
        elif progress['analysis2']['percentage'] > progress['analysis1']['percentage']:
            print("   ✅ Análise 2 está AVANÇANDO")
            if progress['analysis2']['percentage'] < 100:
                print("   → Continue a análise até 100%")
        else:
            print("   ℹ️  Ambas análises no mesmo progresso")

        if timing['diff']['speedup_factor'] > 1.2:
            print("   ⚡ Análise 2 está significativamente mais rápida")
            print("   → Pode indicar melhorias no sistema ou modelo LLM diferente")
        elif timing['diff']['speedup_factor'] < 0.8:
            print("   🐌 Análise 2 está significativamente mais lenta")
            print("   → Verifique gargalos ou problemas de performance")

        print()
        print("=" * 80)
        print()

    def list_analyses(self):
        """Lista todas as análises disponíveis"""
        analyses = self.find_all_analyses()

        if not analyses:
            print("\n⚠️  Nenhuma análise encontrada.\n")
            return

        print("\n" + "=" * 80)
        print("📋 ANÁLISES DISPONÍVEIS")
        print("=" * 80)
        print()

        for i, analysis in enumerate(analyses, 1):
            age_days = (datetime.now() - analysis['last_update']).days
            age_str = f"{age_days}d atrás" if age_days > 0 else "hoje"

            print(f"{i:2}. {analysis['name']}")
            print(f"    ├─ Progresso: {analysis['completed']}/{analysis['total']} ({analysis['percentage']:.0f}%)")
            print(f"    ├─ Atualização: {age_str} ({analysis['last_update'].strftime('%Y-%m-%d %H:%M')})")
            if analysis['failed'] > 0:
                print(f"    ├─ ❌ Falhas: {analysis['failed']}")
            print(f"    └─ Pasta: {analysis['path']}")

        print()
        print("=" * 80)
        print()


def main():
    """Main execution"""
    comparator = AnalysisComparator()

    if '--list' in sys.argv:
        comparator.list_analyses()
        return

    if '--latest' in sys.argv:
        analyses = comparator.find_all_analyses()
        if len(analyses) < 2:
            print("\n⚠️  Precisa de pelo menos 2 análises para comparar.\n")
            return

        analysis1 = analyses[1]  # Segunda mais recente
        analysis2 = analyses[0]  # Mais recente

        comparator.print_comparison(analysis1, analysis2)
        return

    if len(sys.argv) < 3:
        print("Uso:")
        print("  python compare_analyses.py <análise1> <análise2>")
        print("  python compare_analyses.py --list")
        print("  python compare_analyses.py --latest")
        print()
        print("Exemplo:")
        print("  python compare_analyses.py --latest")
        print("  python compare_analyses.py TE_ENCONTRO_0003 TE_ENCONTRO_0004")
        sys.exit(1)

    try:
        analysis1 = comparator.load_analysis(sys.argv[1])
        analysis2 = comparator.load_analysis(sys.argv[2])

        comparator.print_comparison(analysis1, analysis2)

    except FileNotFoundError as e:
        print(f"\n❌ Erro: {e}\n")
        print("Use --list para ver análises disponíveis.\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
