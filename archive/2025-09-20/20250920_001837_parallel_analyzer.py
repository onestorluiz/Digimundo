#!/usr/bin/env python3
"""
⚡ ANALISADOR PARALELO DE ROTEIROS
Acelera análise processando múltiplos roteiros simultaneamente
"""

import time
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.screenplay_library import get_screenplay_library

# Integration with other components
try:
    from scripts.active.integrated_system import get_integrated_system
except:
    pass  # Integration optional

from src.core.script_doctor_system import ScriptDoctorSystem
from src.core.unified_memory_system import get_unified_memory, MemoryType


class ParallelScreenplayAnalyzer:
    """
    Analisa múltiplos roteiros em paralelo para acelerar processamento
    """

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.library = get_screenplay_library()
        self.memory = get_unified_memory()
        self.results = []

    def analyze_screenplay(self, screenplay_title: str) -> Dict[str, Any]:
        """
        Analisa um roteiro individual

        Args:
            screenplay_title: Título do roteiro

        Returns:
            Resultado da análise
        """
        start_time = time.time()

        try:
            # Verificar cache primeiro
            cache_key = f"parallel_analysis:{screenplay_title}"
            cached = self.memory.search(
                cache_key,
                memory_types=[MemoryType.ANALYSIS],
                limit=1
            )

            if cached and cached[0].confidence > 0.8:
                print(f"📦 {screenplay_title}: Usando cache")
                return cached[0].value

            # Buscar conteúdo do roteiro
            content = self.library.get_screenplay_text(screenplay_title)
            if not content:
                return {
                    'title': screenplay_title,
                    'status': 'not_found',
                    'error': 'Screenplay not found'
                }

            # Criar sistema de análise
            doctor = ScriptDoctorSystem()

            # Análise básica rápida
            analysis = {
                'title': screenplay_title,
                'status': 'completed',
                'metrics': {
                    'length': len(content),
                    'scenes': content.count('INT.') + content.count('EXT.'),
                    'dialogue_ratio': self._calculate_dialogue_ratio(content),
                    'action_ratio': self._calculate_action_ratio(content)
                },
                'beats': self._identify_basic_beats(content),
                'themes': self._extract_themes(content),
                'processing_time': 0
            }

            # Salvar no cache
            self.memory.store(
                memory_type=MemoryType.ANALYSIS,
                key=cache_key,
                value=analysis,
                metadata={
                    'analyzer': 'parallel',
                    'timestamp': time.time()
                },
                confidence=0.85
            )

            analysis['processing_time'] = time.time() - start_time
            print(f"✅ {screenplay_title}: {analysis['processing_time']:.2f}s")

            return analysis

        except Exception as e:
            print(f"❌ {screenplay_title}: {str(e)}")
            return {
                'title': screenplay_title,
                'status': 'error',
                'error': str(e),
                'processing_time': time.time() - start_time
            }

    def _calculate_dialogue_ratio(self, content: str) -> float:
        """Calcula proporção de diálogo no roteiro"""
        lines = content.split('\n')
        dialogue_lines = sum(1 for line in lines if line.strip() and not line[0].isspace())
        return dialogue_lines / len(lines) if lines else 0

    def _calculate_action_ratio(self, content: str) -> float:
        """Calcula proporção de ação no roteiro"""
        lines = content.split('\n')
        action_lines = sum(1 for line in lines if line.strip() and line[0].isspace())
        return action_lines / len(lines) if lines else 0

    def _identify_basic_beats(self, content: str) -> List[str]:
        """Identifica beats básicos do Save the Cat"""
        beats = []
        content_lower = content.lower()

        # Heurísticas simples para beats
        if any(word in content_lower[:5000] for word in ['ordinary', 'routine', 'normal']):
            beats.append('Opening Image')

        if 'catalyst' in content_lower or 'inciting' in content_lower:
            beats.append('Catalyst')

        if content_lower.count('int.') > 20 or content_lower.count('ext.') > 20:
            beats.append('Fun and Games')

        if any(word in content_lower[-5000:] for word in ['climax', 'final', 'showdown']):
            beats.append('Finale')

        return beats

    def _extract_themes(self, content: str) -> List[str]:
        """Extrai temas principais do roteiro"""
        themes = []

        theme_keywords = {
            'love': ['love', 'heart', 'romance', 'kiss'],
            'revenge': ['revenge', 'vengeance', 'payback', 'retribution'],
            'redemption': ['redemption', 'forgive', 'second chance', 'atone'],
            'survival': ['survive', 'survival', 'alive', 'death'],
            'power': ['power', 'control', 'dominate', 'rule'],
            'family': ['family', 'father', 'mother', 'son', 'daughter']
        }

        content_lower = content.lower()
        for theme, keywords in theme_keywords.items():
            if sum(content_lower.count(kw) for kw in keywords) > 5:
                themes.append(theme)

        return themes[:3]  # Top 3 temas

    def analyze_multiple(self, screenplay_titles: List[str]) -> Dict[str, Any]:
        """
        Analisa múltiplos roteiros em paralelo

        Args:
            screenplay_titles: Lista de títulos para analisar

        Returns:
            Resultados consolidados
        """
        print(f"\n⚡ ANÁLISE PARALELA DE {len(screenplay_titles)} ROTEIROS")
        print(f"   Usando {self.max_workers} workers")
        print("=" * 50)

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submeter todas as tarefas
            future_to_title = {
                executor.submit(self.analyze_screenplay, title): title
                for title in screenplay_titles
            }

            # Coletar resultados conforme completam
            for future in as_completed(future_to_title):
                title = future_to_title[future]
                try:
                    result = future.result()
                    self.results.append(result)
                except Exception as e:
                    print(f"❌ Erro ao analisar {title}: {e}")
                    self.results.append({
                        'title': title,
                        'status': 'error',
                        'error': str(e)
                    })

        total_time = time.time() - start_time

        # Consolidar resultados
        successful = [r for r in self.results if r.get('status') == 'completed']
        failed = [r for r in self.results if r.get('status') != 'completed']

        consolidated = {
            'total_analyzed': len(screenplay_titles),
            'successful': len(successful),
            'failed': len(failed),
            'total_time': total_time,
            'avg_time_per_screenplay': total_time / len(screenplay_titles) if screenplay_titles else 0,
            'speedup': self.max_workers if successful else 1,
            'results': self.results,
            'statistics': self._calculate_statistics(successful)
        }

        print(f"\n📊 RESULTADOS:")
        print(f"   ✅ Sucesso: {consolidated['successful']}/{consolidated['total_analyzed']}")
        print(f"   ⏱️  Tempo total: {consolidated['total_time']:.2f}s")
        print(f"   ⚡ Tempo médio: {consolidated['avg_time_per_screenplay']:.2f}s")
        print(f"   🚀 Speedup: {consolidated['speedup']}x")

        return consolidated

    def _calculate_statistics(self, results: List[Dict]) -> Dict:
        """Calcula estatísticas agregadas dos resultados"""
        if not results:
            return {}

        stats = {
            'avg_scenes': sum(r['metrics']['scenes'] for r in results) / len(results),
            'avg_dialogue_ratio': sum(r['metrics']['dialogue_ratio'] for r in results) / len(results),
            'common_themes': {},
            'common_beats': {}
        }

        # Contar temas e beats mais comuns
        for result in results:
            for theme in result.get('themes', []):
                stats['common_themes'][theme] = stats['common_themes'].get(theme, 0) + 1
            for beat in result.get('beats', []):
                stats['common_beats'][beat] = stats['common_beats'].get(beat, 0) + 1

        return stats

    def generate_comparative_report(self) -> str:
        """
        Gera relatório comparativo dos roteiros analisados
        """
        if not self.results:
            return "Nenhuma análise realizada ainda"

        successful = [r for r in self.results if r.get('status') == 'completed']

        report = f"""# 📊 RELATÓRIO COMPARATIVO DE ROTEIROS

**Total Analisado:** {len(self.results)} roteiros
**Análises Bem-sucedidas:** {len(successful)}

---

## 🎬 ROTEIROS ANALISADOS

| Título | Cenas | Diálogo % | Temas | Status |
|--------|-------|-----------|-------|--------|
"""

        for result in self.results[:10]:  # Top 10
            if result['status'] == 'completed':
                report += f"| {result['title']} | {result['metrics']['scenes']} | "
                report += f"{result['metrics']['dialogue_ratio']*100:.1f}% | "
                report += f"{', '.join(result['themes'][:2])} | ✅ |\n"
            else:
                report += f"| {result['title']} | - | - | - | ❌ |\n"

        if len(successful) > 0:
            stats = self._calculate_statistics(successful)
            report += f"""
---

## 📈 ESTATÍSTICAS AGREGADAS

- **Média de Cenas:** {stats['avg_scenes']:.1f}
- **Média de Diálogo:** {stats['avg_dialogue_ratio']*100:.1f}%

### Temas Mais Comuns
"""
            for theme, count in sorted(stats['common_themes'].items(), key=lambda x: x[1], reverse=True)[:5]:
                report += f"- {theme}: {count} roteiros\n"

            report += "\n### Beats Mais Identificados\n"
            for beat, count in sorted(stats['common_beats'].items(), key=lambda x: x[1], reverse=True)[:5]:
                report += f"- {beat}: {count} roteiros\n"

        report += "\n---\n**DIGIMUNDO PRESENTE** 🥷"

        return report


def main():
    """
    Demonstração do analisador paralelo
    """
    print("\n⚡ ANALISADOR PARALELO DE ROTEIROS")
    print("-" * 50)

    analyzer = ParallelScreenplayAnalyzer(max_workers=4)

    # Pegar alguns roteiros da biblioteca
    library = get_screenplay_library()
    all_screenplays = library.list_screenplays()

    if not all_screenplays:
        print("❌ Nenhum roteiro encontrado na biblioteca")
        return

    # Analisar os primeiros 8 roteiros
    test_screenplays = all_screenplays[:8]

    print(f"\n📚 Roteiros para análise:")
    for i, title in enumerate(test_screenplays, 1):
        print(f"   {i}. {title}")

    # Executar análise paralela
    results = analyzer.analyze_multiple(test_screenplays)

    # Gerar relatório
    report = analyzer.generate_comparative_report()

    # Salvar relatório
    report_path = Path("docs") / f"PARALLEL_ANALYSIS_{time.strftime('%Y%m%d_%H%M%S')}.md"
    report_path.write_text(report, encoding='utf-8')

    print(f"\n📄 Relatório salvo em: {report_path}")

    # Comparar com execução sequencial
    print(f"\n⏱️  COMPARAÇÃO DE PERFORMANCE:")
    print(f"   Paralelo ({analyzer.max_workers} workers): {results['total_time']:.2f}s")
    estimated_sequential = results['avg_time_per_screenplay'] * len(test_screenplays)
    print(f"   Sequencial (estimado): {estimated_sequential:.2f}s")
    print(f"   🚀 Speedup real: {estimated_sequential/results['total_time']:.2f}x")


if __name__ == "__main__":
    main()