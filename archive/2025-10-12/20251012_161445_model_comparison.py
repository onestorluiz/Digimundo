#!/usr/bin/env python3
"""
Comparação de Modelos LLM

Compara performance de diferentes modelos LLM:
- Executa mesma análise com diferentes modelos
- Compara qualidade, tempo, custo
- Gera relatório de comparação
- Recomenda melhor modelo por caso de uso

Uso:
    python model_comparison.py <screenplay.pdf> --models llama3.1:70b,qwen2.5:72b
    python model_comparison.py <screenplay.pdf> --models gpt-4,claude-3-opus
    python model_comparison.py --compare <analysis1_dir> <analysis2_dir>  # Compara análises existentes
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import argparse


class ModelComparison:
    """Gerencia comparação entre modelos LLM"""

    # Modelos conhecidos com suas características
    KNOWN_MODELS = {
        'llama3.1:70b': {
            'provider': 'ollama',
            'cost_per_analysis': 0.0,
            'expected_speed': 'fast',
            'strengths': 'Gratuito, boa qualidade geral, rápido'
        },
        'qwen2.5:72b': {
            'provider': 'ollama',
            'cost_per_analysis': 0.0,
            'expected_speed': 'fast',
            'strengths': 'Gratuito, excelente reasoning, multi-idioma'
        },
        'scripturemon-optimized': {
            'provider': 'ollama',
            'cost_per_analysis': 0.0,
            'expected_speed': 'fast',
            'strengths': 'Gratuito, otimizado para análise de roteiros'
        },
        'gpt-4-turbo': {
            'provider': 'openai',
            'cost_per_analysis': 0.11,
            'expected_speed': 'medium',
            'strengths': 'Alta qualidade, bom reasoning, API estável'
        },
        'gpt-4': {
            'provider': 'openai',
            'cost_per_analysis': 0.15,
            'expected_speed': 'slow',
            'strengths': 'Máxima qualidade, detalhado'
        },
        'claude-3-opus': {
            'provider': 'anthropic',
            'cost_per_analysis': 0.12,
            'expected_speed': 'medium',
            'strengths': 'Excelente análise criativa, nuances'
        },
        'claude-3-sonnet': {
            'provider': 'anthropic',
            'cost_per_analysis': 0.08,
            'expected_speed': 'fast',
            'strengths': 'Bom custo-benefício, rápido'
        }
    }

    def __init__(self):
        pass

    def get_model_info(self, model_name: str) -> Dict:
        """Retorna informações sobre um modelo"""
        return self.KNOWN_MODELS.get(model_name, {
            'provider': 'unknown',
            'cost_per_analysis': 0.0,
            'expected_speed': 'unknown',
            'strengths': 'Desconhecido'
        })

    def run_analysis_with_model(
        self,
        screenplay_path: str,
        model: str,
        specialists: List[str],
        authors: List[str],
        output_suffix: str = None
    ) -> Optional[Path]:
        """
        Executa análise com um modelo específico

        Returns:
            Path para o diretório de output da análise
        """
        print(f"\n🔬 Executando análise com modelo: {model}")
        print("=" * 80)

        # Construir comando
        cmd = [
            'python3',
            'analyze_all_specialists.py',
            screenplay_path,
            '--model', model,
            '--yes'
        ]

        if specialists:
            cmd.extend(['--specialists', ','.join(specialists)])

        if authors:
            cmd.extend(['--authors', ','.join(authors)])

        # Output customizado
        if output_suffix:
            output_name = f"COMPARISON_{output_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            cmd.extend(['--output-name', output_name])

        try:
            # Executar
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Parse output para encontrar diretório
            # (Assumindo que analyze_all_specialists.py retorna o path)
            # Por ora, vamos buscar no workspace/outputs

            # Encontrar o output mais recente
            workspace = Path('workspace/outputs')
            analyses = sorted(
                [d for d in workspace.glob('*') if d.is_dir()],
                key=lambda d: d.stat().st_mtime,
                reverse=True
            )

            if analyses:
                return analyses[0]
            else:
                print(f"⚠️  Não foi possível localizar output da análise")
                return None

        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao executar análise: {e}")
            return None

    def load_analysis_results(self, analysis_dir: Path) -> Dict:
        """Carrega resultados de uma análise"""
        checkpoint_file = analysis_dir / '2_logs' / 'checkpoint.json'

        if not checkpoint_file.exists():
            return None

        try:
            with open(checkpoint_file, 'r') as f:
                checkpoint = json.load(f)

            # Calcular métricas
            completed = len(checkpoint.get('completed', []))
            total = checkpoint.get('total_analyses', 312)
            failed = len(checkpoint.get('failed', []))

            started = datetime.fromisoformat(checkpoint['started_at'])
            ended_str = checkpoint.get('last_update', checkpoint['started_at'])
            ended = datetime.fromisoformat(ended_str)

            duration = (ended - started).total_seconds()

            # Tentar carregar qualidade média
            # (Assumindo que existe um summary.json ou similar)
            avg_quality = 0.0
            summary_file = analysis_dir / '2_logs' / 'summary.json'
            if summary_file.exists():
                with open(summary_file, 'r') as f:
                    summary = json.load(f)
                    avg_quality = summary.get('average_quality', 0.0)

            return {
                'directory': analysis_dir,
                'checkpoint': checkpoint,
                'completed': completed,
                'total': total,
                'failed': failed,
                'started_at': started,
                'ended_at': ended,
                'duration_seconds': duration,
                'duration_hours': duration / 3600,
                'avg_quality': avg_quality,
                'analyses_per_hour': (completed / (duration / 3600)) if duration > 0 else 0
            }

        except Exception as e:
            print(f"⚠️  Erro ao carregar análise de {analysis_dir}: {e}")
            return None

    def compare_analyses(self, analysis1: Dict, analysis2: Dict, model1: str, model2: str):
        """Compara duas análises lado a lado"""
        print("\n" + "=" * 80)
        print("🔬 COMPARAÇÃO DE MODELOS LLM")
        print("=" * 80)
        print()

        # Informações dos modelos
        info1 = self.get_model_info(model1)
        info2 = self.get_model_info(model2)

        print(f"🤖 Modelo 1: {model1}")
        print(f"   Provider: {info1['provider']}")
        print(f"   Pontos fortes: {info1['strengths']}")
        print()

        print(f"🤖 Modelo 2: {model2}")
        print(f"   Provider: {info2['provider']}")
        print(f"   Pontos fortes: {info2['strengths']}")
        print()

        # Tabela de comparação
        print("=" * 80)
        print("📊 RESULTADOS")
        print("=" * 80)
        print()

        # Progresso
        print(f"{'Métrica':<30} {'Modelo 1':<25} {'Modelo 2':<25}")
        print("-" * 80)

        print(f"{'Análises completadas':<30} {analysis1['completed']:<25} {analysis2['completed']:<25}")
        print(f"{'Análises falhadas':<30} {analysis1['failed']:<25} {analysis2['failed']:<25}")

        rate1 = f"{(analysis1['completed'] / analysis1['total'] * 100):.1f}%"
        rate2 = f"{(analysis2['completed'] / analysis2['total'] * 100):.1f}%"
        print(f"{'Taxa de sucesso':<30} {rate1:<25} {rate2:<25}")
        print()

        # Tempo
        print(f"{'Tempo total (h)':<30} {analysis1['duration_hours']:<25.2f} {analysis2['duration_hours']:<25.2f}")
        print(f"{'Análises por hora':<30} {analysis1['analyses_per_hour']:<25.1f} {analysis2['analyses_per_hour']:<25.1f}")

        # Velocidade relativa
        if analysis1['analyses_per_hour'] > 0 and analysis2['analyses_per_hour'] > 0:
            speedup = analysis2['analyses_per_hour'] / analysis1['analyses_per_hour']
            if speedup > 1.1:
                print(f"\n   ⚡ Modelo 2 é {speedup:.1f}x MAIS RÁPIDO")
            elif speedup < 0.9:
                print(f"\n   🐌 Modelo 2 é {1/speedup:.1f}x MAIS LENTO")
            else:
                print(f"\n   ⚖️  Velocidade similar entre modelos")

        print()

        # Qualidade
        if analysis1['avg_quality'] > 0 or analysis2['avg_quality'] > 0:
            print(f"{'Qualidade média':<30} {analysis1['avg_quality']:<25.1f} {analysis2['avg_quality']:<25.1f}")

            if analysis1['avg_quality'] > 0 and analysis2['avg_quality'] > 0:
                quality_diff = analysis2['avg_quality'] - analysis1['avg_quality']
                if abs(quality_diff) > 0.5:
                    better = "Modelo 2" if quality_diff > 0 else "Modelo 1"
                    print(f"\n   🎯 {better} tem qualidade superior ({abs(quality_diff):.1f} pontos)")
                else:
                    print(f"\n   ⚖️  Qualidade similar entre modelos")

            print()

        # Custo
        cost1 = info1['cost_per_analysis'] * analysis1['completed']
        cost2 = info2['cost_per_analysis'] * analysis2['completed']

        print(f"{'Custo total':<30} ${cost1:<24.2f} ${cost2:<24.2f}")

        if cost1 > 0 or cost2 > 0:
            cost_diff = cost2 - cost1
            if cost_diff != 0:
                cheaper = "Modelo 2" if cost_diff < 0 else "Modelo 1"
                print(f"\n   💰 {cheaper} é ${abs(cost_diff):.2f} mais barato")

        print()
        print("=" * 80)

        # Recomendações
        self.generate_recommendations(analysis1, analysis2, info1, info2, model1, model2)

    def generate_recommendations(
        self,
        analysis1: Dict,
        analysis2: Dict,
        info1: Dict,
        info2: Dict,
        model1: str,
        model2: str
    ):
        """Gera recomendações baseadas na comparação"""
        print()
        print("💡 RECOMENDAÇÕES")
        print("=" * 80)

        recommendations = []

        # Performance
        speed_ratio = analysis2['analyses_per_hour'] / analysis1['analyses_per_hour'] if analysis1['analyses_per_hour'] > 0 else 0

        if speed_ratio > 1.3:
            recommendations.append({
                'title': f'Use {model2} para análises rápidas',
                'reason': f'É significativamente mais rápido ({speed_ratio:.1f}x)'
            })
        elif speed_ratio < 0.7:
            recommendations.append({
                'title': f'Use {model1} para análises rápidas',
                'reason': f'É significativamente mais rápido ({1/speed_ratio:.1f}x)'
            })

        # Qualidade
        if analysis1['avg_quality'] > 0 and analysis2['avg_quality'] > 0:
            quality_diff = analysis2['avg_quality'] - analysis1['avg_quality']

            if quality_diff > 0.5:
                recommendations.append({
                    'title': f'Use {model2} quando qualidade é prioridade',
                    'reason': f'Qualidade média {quality_diff:.1f} pontos superior'
                })
            elif quality_diff < -0.5:
                recommendations.append({
                    'title': f'Use {model1} quando qualidade é prioridade',
                    'reason': f'Qualidade média {abs(quality_diff):.1f} pontos superior'
                })

        # Custo
        cost1 = info1['cost_per_analysis']
        cost2 = info2['cost_per_analysis']

        if cost1 == 0 and cost2 > 0:
            recommendations.append({
                'title': f'Use {model1} para análises em volume',
                'reason': 'É gratuito (Ollama local)'
            })
        elif cost2 == 0 and cost1 > 0:
            recommendations.append({
                'title': f'Use {model2} para análises em volume',
                'reason': 'É gratuito (Ollama local)'
            })

        # Exibir recomendações
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['title']}")
            print(f"   → {rec['reason']}")
            print()

        if not recommendations:
            print("Ambos modelos têm performance similar. Escolha baseado em:")
            print("  • Disponibilidade (Ollama local vs API)")
            print("  • Orçamento (gratuito vs pago)")
            print("  • Preferência pessoal de estilo de análise")
            print()

        print("=" * 80)
        print()


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(
        description='Comparação de modelos LLM do Scripturemon',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Executar análise com 2 modelos e comparar
  python model_comparison.py screenplay.pdf --models llama3.1:70b,qwen2.5:72b

  # Comparar análises já existentes
  python model_comparison.py --compare analysis1/ analysis2/ --model-names llama3.1,qwen2.5
        """
    )

    parser.add_argument('screenplay', nargs='?', help='Caminho do roteiro PDF')
    parser.add_argument('--models', help='Modelos a comparar (separados por vírgula)')
    parser.add_argument('--compare', nargs=2, metavar=('ANALYSIS1', 'ANALYSIS2'),
                        help='Comparar duas análises existentes')
    parser.add_argument('--model-names', help='Nomes dos modelos para comparação (separados por vírgula)')
    parser.add_argument('--specialists', help='Specialists para análise (padrão: character,structure)')
    parser.add_argument('--authors', help='Authors para análise (padrão: mckee,field)')

    args = parser.parse_args()

    comparer = ModelComparison()

    # Modo 1: Comparar análises existentes
    if args.compare:
        analysis1_dir = Path(args.compare[0])
        analysis2_dir = Path(args.compare[1])

        if not analysis1_dir.exists() or not analysis2_dir.exists():
            print("\n❌ Erro: Um ou ambos diretórios de análise não existem\n")
            sys.exit(1)

        print("📊 Carregando análises...")
        analysis1 = comparer.load_analysis_results(analysis1_dir)
        analysis2 = comparer.load_analysis_results(analysis2_dir)

        if not analysis1 or not analysis2:
            print("\n❌ Erro ao carregar análises\n")
            sys.exit(1)

        # Nomes dos modelos
        if args.model_names:
            models = args.model_names.split(',')
            model1, model2 = models[0].strip(), models[1].strip()
        else:
            model1, model2 = "Model 1", "Model 2"

        comparer.compare_analyses(analysis1, analysis2, model1, model2)

    # Modo 2: Executar análises e comparar
    elif args.screenplay and args.models:
        models = [m.strip() for m in args.models.split(',')]

        if len(models) != 2:
            print("\n❌ Erro: Forneça exatamente 2 modelos para comparar\n")
            sys.exit(1)

        specialists = ['character', 'structure']
        if args.specialists:
            specialists = [s.strip() for s in args.specialists.split(',')]

        authors = ['mckee', 'field']
        if args.authors:
            authors = [a.strip() for a in args.authors.split(',')]

        print("\n" + "=" * 80)
        print("🔬 COMPARAÇÃO DE MODELOS - EXECUTANDO ANÁLISES")
        print("=" * 80)
        print()
        print(f"📄 Screenplay: {args.screenplay}")
        print(f"🤖 Modelos: {', '.join(models)}")
        print(f"🔬 Specialists: {', '.join(specialists)}")
        print(f"📚 Authors: {', '.join(authors)}")
        print()

        # Executar análise 1
        print("▶️  Executando análise com modelo 1...")
        result1_dir = comparer.run_analysis_with_model(
            args.screenplay,
            models[0],
            specialists,
            authors,
            output_suffix=models[0].replace(':', '_')
        )

        if not result1_dir:
            print("\n❌ Falha na análise 1\n")
            sys.exit(1)

        # Executar análise 2
        print("\n▶️  Executando análise com modelo 2...")
        result2_dir = comparer.run_analysis_with_model(
            args.screenplay,
            models[1],
            specialists,
            authors,
            output_suffix=models[1].replace(':', '_')
        )

        if not result2_dir:
            print("\n❌ Falha na análise 2\n")
            sys.exit(1)

        # Carregar resultados
        print("\n📊 Carregando resultados...")
        analysis1 = comparer.load_analysis_results(result1_dir)
        analysis2 = comparer.load_analysis_results(result2_dir)

        if not analysis1 or not analysis2:
            print("\n❌ Erro ao carregar resultados\n")
            sys.exit(1)

        # Comparar
        comparer.compare_analyses(analysis1, analysis2, models[0], models[1])

    else:
        parser.print_help()
        print()
        print("💡 Use --compare para comparar análises existentes")
        print("💡 Ou forneça screenplay e --models para executar novas análises")
        print()
        sys.exit(1)


if __name__ == '__main__':
    main()
