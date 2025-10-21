#!/usr/bin/env python3
"""
Benchmark de Performance do Scripturemon

Analisa performance do sistema:
- Tempo médio por specialist
- Tempo médio por author
- Gargalos identificados
- Comparação de modelos LLM
- Recomendações de otimização

Uso:
    python benchmark_performance.py            # Análise completa
    python benchmark_performance.py --quick    # Análise rápida (últimas 100)
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from collections import defaultdict

# Import usage stats para ler dados históricos
from usage_stats import UsageStats


class PerformanceBenchmark:
    """Analisa performance do sistema"""

    def __init__(self):
        self.stats = UsageStats()

    def analyze_specialist_performance(self) -> Dict:
        """Analisa performance por specialist"""
        by_specialist = self.stats.data.get('by_specialist', {})

        results = []
        for name, data in by_specialist.items():
            if data['count'] == 0:
                continue

            avg_time = data['total_time'] / data['count']
            success_rate = (data['successes'] / data['count'] * 100) if data['count'] > 0 else 0
            avg_quality = data.get('avg_quality', 0)

            results.append({
                'specialist': name,
                'count': data['count'],
                'avg_time_minutes': avg_time / 60,
                'total_time_hours': data['total_time'] / 3600,
                'success_rate': success_rate,
                'avg_quality': avg_quality,
                'failures': data['failures']
            })

        # Ordenar por tempo médio (mais lentos primeiro)
        results.sort(key=lambda x: x['avg_time_minutes'], reverse=True)

        return results

    def analyze_author_performance(self) -> Dict:
        """Analisa performance por autor"""
        by_author = self.stats.data.get('by_author', {})

        results = []
        for name, data in by_author.items():
            if data['count'] == 0:
                continue

            avg_time = data['total_time'] / data['count']
            success_rate = (data['successes'] / data['count'] * 100) if data['count'] > 0 else 0

            results.append({
                'author': name,
                'count': data['count'],
                'avg_time_minutes': avg_time / 60,
                'total_time_hours': data['total_time'] / 3600,
                'success_rate': success_rate,
                'failures': data['failures']
            })

        # Ordenar por tempo médio
        results.sort(key=lambda x: x['avg_time_minutes'], reverse=True)

        return results

    def analyze_model_performance(self) -> Dict:
        """Analisa performance por modelo LLM"""
        by_model = self.stats.data.get('by_model', {})

        results = []
        for name, data in by_model.items():
            if data['count'] == 0:
                continue

            avg_time = data['total_time'] / data['count']
            cost_per_analysis = data['total_cost'] / data['count'] if data['count'] > 0 else 0

            results.append({
                'model': name,
                'count': data['count'],
                'avg_time_minutes': avg_time / 60,
                'total_time_hours': data['total_time'] / 3600,
                'total_cost': data['total_cost'],
                'cost_per_analysis': cost_per_analysis
            })

        return results

    def identify_bottlenecks(self, specialist_perf: List, threshold_minutes: float = 3.0) -> List:
        """Identifica gargalos (specialists muito lentos)"""
        bottlenecks = []

        for spec in specialist_perf:
            if spec['avg_time_minutes'] > threshold_minutes:
                bottlenecks.append({
                    'specialist': spec['specialist'],
                    'avg_time_minutes': spec['avg_time_minutes'],
                    'slowdown_factor': spec['avg_time_minutes'] / threshold_minutes,
                    'total_analyses': spec['count']
                })

        return bottlenecks

    def generate_recommendations(self, specialist_perf: List, author_perf: List) -> List:
        """Gera recomendações de otimização"""
        recommendations = []

        # Verificar specialists lentos
        slow_specialists = [s for s in specialist_perf if s['avg_time_minutes'] > 3.0]
        if slow_specialists:
            recommendations.append({
                'type': 'performance',
                'priority': 'high',
                'title': f"{len(slow_specialists)} Specialists Lentos Detectados",
                'description': f"Os specialists {', '.join([s['specialist'] for s in slow_specialists[:3]])} estão com tempo médio > 3 min.",
                'suggestion': "Considere otimizar as queries desses specialists ou revisar a lógica de análise."
            })

        # Verificar falhas
        failed_specialists = [s for s in specialist_perf if s['failures'] > 0]
        if failed_specialists:
            total_failures = sum(s['failures'] for s in failed_specialists)
            recommendations.append({
                'type': 'reliability',
                'priority': 'medium',
                'title': f"{total_failures} Falhas Registradas",
                'description': f"Falhas detectadas em {len(failed_specialists)} specialists.",
                'suggestion': "Revisar logs de erro e adicionar tratamento de exceções."
            })

        # Verificar qualidade baixa
        low_quality = [s for s in specialist_perf if s['avg_quality'] > 0 and s['avg_quality'] < 6.0]
        if low_quality:
            recommendations.append({
                'type': 'quality',
                'priority': 'medium',
                'title': f"{len(low_quality)} Specialists com Qualidade Baixa",
                'description': f"Qualidade média < 6.0 para {', '.join([s['specialist'] for s in low_quality[:3]])}.",
                'suggestion': "Revisar prompts e queries para melhorar qualidade das análises."
            })

        # Verificar se há dados suficientes
        total_analyses = self.stats.data.get('total_analyses', 0)
        if total_analyses < 50:
            recommendations.append({
                'type': 'data',
                'priority': 'low',
                'title': "Poucos Dados para Benchmark Preciso",
                'description': f"Apenas {total_analyses} análises registradas até agora.",
                'suggestion': "Execute mais análises para obter benchmark mais preciso (recomendado: > 100)."
            })

        return recommendations

    def print_benchmark(self, quick: bool = False):
        """Exibe benchmark completo"""
        print("\n" + "=" * 80)
        print("⚡ SCRIPTUREMON - BENCHMARK DE PERFORMANCE")
        print("=" * 80)
        print()

        total = self.stats.data.get('total_analyses', 0)
        if total == 0:
            print("⚠️  Nenhuma análise registrada. Execute análises primeiro.")
            print()
            return

        print(f"📊 Total de análises: {total}")
        print(f"⏱️  Tempo total: {self.stats.data.get('total_time_seconds', 0)/3600:.1f}h")
        print()

        # Performance por Specialist
        specialist_perf = self.analyze_specialist_performance()

        if specialist_perf:
            print("🔬 PERFORMANCE POR SPECIALIST (top 10 mais lentos)")
            print("-" * 80)

            limit = 10 if not quick else 5
            for i, spec in enumerate(specialist_perf[:limit], 1):
                print(f"   {i:2}. Dr{spec['specialist'].title()}")
                print(f"       ├─ Tempo médio: {spec['avg_time_minutes']:.1f} min")
                print(f"       ├─ Análises: {spec['count']}")
                print(f"       ├─ Sucesso: {spec['success_rate']:.0f}%")
                print(f"       ├─ Qualidade: {spec['avg_quality']:.1f}/10")
                print(f"       └─ Tempo total: {spec['total_time_hours']:.1f}h")
            print()

        # Performance por Author
        author_perf = self.analyze_author_performance()

        if author_perf and not quick:
            print("📚 PERFORMANCE POR AUTOR (top 5 mais lentos)")
            print("-" * 80)

            for i, author in enumerate(author_perf[:5], 1):
                print(f"   {i}. {author['author'].upper()}")
                print(f"      ├─ Tempo médio: {author['avg_time_minutes']:.1f} min")
                print(f"      ├─ Análises: {author['count']}")
                print(f"      └─ Sucesso: {author['success_rate']:.0f}%")
            print()

        # Performance por Modelo
        model_perf = self.analyze_model_performance()

        if model_perf:
            print("🤖 PERFORMANCE POR MODELO")
            print("-" * 80)

            for model in model_perf:
                print(f"   • {model['model']}")
                print(f"      ├─ Tempo médio: {model['avg_time_minutes']:.1f} min")
                print(f"      ├─ Análises: {model['count']}")
                print(f"      ├─ Custo médio: ${model['cost_per_analysis']:.3f}")
                print(f"      └─ Custo total: ${model['total_cost']:.2f}")
            print()

        # Gargalos
        bottlenecks = self.identify_bottlenecks(specialist_perf)

        if bottlenecks and not quick:
            print("⚠️  GARGALOS IDENTIFICADOS")
            print("-" * 80)

            for bn in bottlenecks[:5]:
                print(f"   • Dr{bn['specialist'].title()}")
                print(f"      ├─ Tempo: {bn['avg_time_minutes']:.1f} min ({bn['slowdown_factor']:.1f}x mais lento que threshold)")
                print(f"      └─ Impacto: {bn['total_analyses']} análises")
            print()

        # Recomendações
        recommendations = self.generate_recommendations(specialist_perf, author_perf)

        if recommendations:
            print("💡 RECOMENDAÇÕES DE OTIMIZAÇÃO")
            print("-" * 80)

            for rec in recommendations:
                priority_icon = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                print(f"   {priority_icon} {rec['title']}")
                print(f"      {rec['description']}")
                print(f"      → {rec['suggestion']}")
                print()

        print("=" * 80)
        print()


def main():
    """Main execution"""
    quick = '--quick' in sys.argv

    benchmark = PerformanceBenchmark()
    benchmark.print_benchmark(quick=quick)


if __name__ == '__main__':
    main()
