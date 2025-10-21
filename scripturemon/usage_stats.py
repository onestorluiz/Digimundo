#!/usr/bin/env python3
"""
Sistema de Estatísticas de Uso do Scripturemon

Rastreia e exibe estatísticas de uso:
- Total de análises realizadas
- Tempo médio por specialist/author
- Specialists e autores mais usados
- Modelos LLM mais usados
- Taxa de sucesso/falha
- Custos estimados

Uso:
    python usage_stats.py              # Exibe estatísticas
    python usage_stats.py --reset      # Reset estatísticas
    python usage_stats.py --export     # Exporta para CSV
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import Counter, defaultdict


class UsageStats:
    """Gerencia estatísticas de uso do sistema"""

    def __init__(self, stats_file: Path = None):
        self.stats_file = stats_file or Path('workspace/stats/usage.json')
        self.stats_file.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self) -> Dict:
        """Carrega estatísticas existentes"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                return self._new_stats()
        return self._new_stats()

    def _new_stats(self) -> Dict:
        """Cria estrutura de estatísticas vazia"""
        return {
            'version': '1.0',
            'created_at': datetime.now().isoformat(),
            'last_update': None,
            'total_analyses': 0,
            'total_time_seconds': 0.0,
            'total_successes': 0,
            'total_failures': 0,
            'by_specialist': {},  # {specialist_name: {count, total_time, successes, failures}}
            'by_author': {},      # {author_name: {count, total_time, successes, failures}}
            'by_model': {},       # {model_name: {count, total_time, cost}}
            'screenplays_analyzed': [],  # Lista de roteiros analisados
            'analysis_history': []  # Histórico completo (últimas 1000 análises)
        }

    def save(self):
        """Salva estatísticas no disco"""
        self.data['last_update'] = datetime.now().isoformat()
        with open(self.stats_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def record_analysis(
        self,
        specialist: str,
        author: str,
        model: str,
        time_seconds: float,
        success: bool,
        quality_score: float = 0.0,
        screenplay_name: str = "",
        estimated_cost: float = 0.0
    ):
        """
        Registra uma análise completa.

        Args:
            specialist: Nome do specialist
            author: Nome do autor teórico
            model: Modelo LLM usado
            time_seconds: Tempo de execução
            success: Se foi bem-sucedida
            quality_score: Score de qualidade (0-10)
            screenplay_name: Nome do roteiro
            estimated_cost: Custo estimado em USD
        """

        # Atualizar totais
        self.data['total_analyses'] += 1
        self.data['total_time_seconds'] += time_seconds

        if success:
            self.data['total_successes'] += 1
        else:
            self.data['total_failures'] += 1

        # Atualizar por specialist
        if specialist not in self.data['by_specialist']:
            self.data['by_specialist'][specialist] = {
                'count': 0,
                'total_time': 0.0,
                'successes': 0,
                'failures': 0,
                'avg_quality': 0.0,
                'quality_scores': []
            }

        spec_stats = self.data['by_specialist'][specialist]
        spec_stats['count'] += 1
        spec_stats['total_time'] += time_seconds
        spec_stats['successes' if success else 'failures'] += 1
        if success:
            spec_stats['quality_scores'].append(quality_score)
            spec_stats['avg_quality'] = sum(spec_stats['quality_scores']) / len(spec_stats['quality_scores'])

        # Atualizar por author
        if author not in self.data['by_author']:
            self.data['by_author'][author] = {
                'count': 0,
                'total_time': 0.0,
                'successes': 0,
                'failures': 0
            }

        auth_stats = self.data['by_author'][author]
        auth_stats['count'] += 1
        auth_stats['total_time'] += time_seconds
        auth_stats['successes' if success else 'failures'] += 1

        # Atualizar por modelo
        if model not in self.data['by_model']:
            self.data['by_model'][model] = {
                'count': 0,
                'total_time': 0.0,
                'total_cost': 0.0
            }

        model_stats = self.data['by_model'][model]
        model_stats['count'] += 1
        model_stats['total_time'] += time_seconds
        model_stats['total_cost'] += estimated_cost

        # Adicionar roteiro à lista (se não existir)
        if screenplay_name and screenplay_name not in self.data['screenplays_analyzed']:
            self.data['screenplays_analyzed'].append(screenplay_name)

        # Adicionar ao histórico (manter últimas 1000)
        self.data['analysis_history'].append({
            'timestamp': datetime.now().isoformat(),
            'specialist': specialist,
            'author': author,
            'model': model,
            'time_seconds': time_seconds,
            'success': success,
            'quality_score': quality_score,
            'screenplay': screenplay_name
        })

        # Limitar histórico a 1000 entradas
        if len(self.data['analysis_history']) > 1000:
            self.data['analysis_history'] = self.data['analysis_history'][-1000:]

        self.save()

    def get_summary(self) -> Dict:
        """Retorna resumo formatado das estatísticas"""
        total = self.data['total_analyses']
        if total == 0:
            return {'message': 'Nenhuma análise registrada ainda.'}

        success_rate = (self.data['total_successes'] / total * 100) if total > 0 else 0
        avg_time = self.data['total_time_seconds'] / total if total > 0 else 0

        # Top 5 specialists
        top_specialists = sorted(
            self.data['by_specialist'].items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:5]

        # Top 5 authors
        top_authors = sorted(
            self.data['by_author'].items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:5]

        # Custos por modelo
        model_costs = {
            model: stats['total_cost']
            for model, stats in self.data['by_model'].items()
        }

        return {
            'total_analyses': total,
            'total_successes': self.data['total_successes'],
            'total_failures': self.data['total_failures'],
            'success_rate': success_rate,
            'total_time_hours': self.data['total_time_seconds'] / 3600,
            'avg_time_minutes': avg_time / 60,
            'total_screenplays': len(self.data['screenplays_analyzed']),
            'top_specialists': top_specialists,
            'top_authors': top_authors,
            'models': self.data['by_model'],
            'model_costs': model_costs,
            'created_at': self.data['created_at'],
            'last_update': self.data['last_update']
        }

    def print_stats(self):
        """Exibe estatísticas formatadas no console"""
        summary = self.get_summary()

        if 'message' in summary:
            print(f"\n{summary['message']}\n")
            return

        print("\n" + "=" * 80)
        print("📊 SCRIPTUREMON - ESTATÍSTICAS DE USO")
        print("=" * 80)
        print()

        print(f"📅 Período: {datetime.fromisoformat(summary['created_at']).strftime('%Y-%m-%d')} → ", end="")
        if summary['last_update']:
            print(f"{datetime.fromisoformat(summary['last_update']).strftime('%Y-%m-%d')}")
        else:
            print("Hoje")
        print()

        # Totais
        print("📈 TOTAIS GERAIS")
        print("-" * 80)
        print(f"   Total de análises: {summary['total_analyses']:,}")
        print(f"   ✅ Sucessos: {summary['total_successes']:,} ({summary['success_rate']:.1f}%)")
        print(f"   ❌ Falhas: {summary['total_failures']:,} ({100 - summary['success_rate']:.1f}%)")
        print(f"   🎬 Roteiros analisados: {summary['total_screenplays']}")
        print(f"   ⏱️  Tempo total: {summary['total_time_hours']:.1f}h")
        print(f"   ⏱️  Tempo médio por análise: {summary['avg_time_minutes']:.1f} min")
        print()

        # Top Specialists
        print("🔬 TOP 5 SPECIALISTS MAIS USADOS")
        print("-" * 80)
        for i, (name, stats) in enumerate(summary['top_specialists'], 1):
            avg_time = stats['total_time'] / stats['count'] if stats['count'] > 0 else 0
            success_rate = stats['successes'] / stats['count'] * 100 if stats['count'] > 0 else 0
            avg_quality = stats.get('avg_quality', 0)

            print(f"   {i}. Dr{name.title()}")
            print(f"      ├─ Análises: {stats['count']:,}")
            print(f"      ├─ Taxa de sucesso: {success_rate:.0f}%")
            print(f"      ├─ Qualidade média: {avg_quality:.1f}/10")
            print(f"      └─ Tempo médio: {avg_time/60:.1f} min")
        print()

        # Top Authors
        print("📚 TOP 5 AUTORES TEÓRICOS MAIS USADOS")
        print("-" * 80)
        for i, (name, stats) in enumerate(summary['top_authors'], 1):
            avg_time = stats['total_time'] / stats['count'] if stats['count'] > 0 else 0
            success_rate = stats['successes'] / stats['count'] * 100 if stats['count'] > 0 else 0

            print(f"   {i}. {name.upper()}")
            print(f"      ├─ Análises: {stats['count']:,}")
            print(f"      ├─ Taxa de sucesso: {success_rate:.0f}%")
            print(f"      └─ Tempo médio: {avg_time/60:.1f} min")
        print()

        # Modelos LLM
        print("🤖 MODELOS LLM")
        print("-" * 80)
        for model, stats in summary['models'].items():
            cost = summary['model_costs'].get(model, 0)
            avg_time = stats['total_time'] / stats['count'] if stats['count'] > 0 else 0

            print(f"   • {model}")
            print(f"      ├─ Análises: {stats['count']:,}")
            print(f"      ├─ Tempo total: {stats['total_time']/3600:.1f}h")
            print(f"      ├─ Tempo médio: {avg_time/60:.1f} min")
            print(f"      └─ Custo total: ${cost:.2f}")
        print()

        print("=" * 80)
        print()

    def reset(self):
        """Reset todas as estatísticas"""
        self.data = self._new_stats()
        self.save()
        print("\n✅ Estatísticas resetadas com sucesso!\n")

    def export_csv(self, output_file: Path = None):
        """Exporta histórico para CSV"""
        output_file = output_file or Path('workspace/stats/history.csv')
        output_file.parent.mkdir(parents=True, exist_ok=True)

        import csv

        if not self.data['analysis_history']:
            print("\n⚠️  Nenhum histórico para exportar.\n")
            return

        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['timestamp', 'specialist', 'author', 'model', 'time_seconds', 'success', 'quality_score', 'screenplay']
            )
            writer.writeheader()
            writer.writerows(self.data['analysis_history'])

        print(f"\n✅ Histórico exportado para: {output_file}\n")


def main():
    """Main execution"""
    stats = UsageStats()

    if '--reset' in sys.argv:
        stats.reset()
    elif '--export' in sys.argv:
        stats.export_csv()
    else:
        stats.print_stats()


if __name__ == '__main__':
    main()
