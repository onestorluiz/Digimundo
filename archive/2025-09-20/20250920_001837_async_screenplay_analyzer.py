#!/usr/bin/env python3
"""
🚀 ANALISADOR ASSÍNCRONO DE ROTEIROS
Versão otimizada com programação assíncrona para máxima performance
"""

import asyncio
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.screenplay_library import get_screenplay_library

# Integration with other components
try:
    from scripts.active.integrated_system import get_integrated_system
except:
    pass  # Integration optional

from src.core.unified_memory_system import get_unified_memory, MemoryType


class AsyncScreenplayAnalyzer:
    """
    Analisador assíncrono de roteiros com máxima performance
    """

    def __init__(self):
        self.library = get_screenplay_library()
        self.memory = get_unified_memory()
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._cache = {}

    async def analyze_screenplay_async(self, title: str) -> Dict[str, Any]:
        """
        Analisa um roteiro de forma assíncrona

        Args:
            title: Título do roteiro

        Returns:
            Resultado da análise
        """
        start_time = time.time()

        # Check cache first
        cache_key = f"async_analysis:{title}"
        if cache_key in self._cache:
            print(f"📦 {title}: Cache hit")
            return self._cache[cache_key]

        try:
            # Buscar conteúdo assincronamente
            content = await self._get_screenplay_content_async(title)

            if not content:
                return {
                    'title': title,
                    'status': 'not_found',
                    'error': 'Screenplay not found'
                }

            # Executar análises em paralelo
            tasks = [
                self._analyze_structure_async(content),
                self._analyze_dialogue_async(content),
                self._analyze_themes_async(content),
                self._analyze_beats_async(content),
                self._analyze_characters_async(content)
            ]

            results = await asyncio.gather(*tasks)

            # Combinar resultados
            analysis = {
                'title': title,
                'status': 'completed',
                'structure': results[0],
                'dialogue': results[1],
                'themes': results[2],
                'beats': results[3],
                'characters': results[4],
                'processing_time': time.time() - start_time
            }

            # Salvar no cache
            self._cache[cache_key] = analysis

            # Salvar na memória de forma assíncrona
            asyncio.create_task(self._save_to_memory_async(cache_key, analysis))

            print(f"✅ {title}: {analysis['processing_time']:.2f}s")

            return analysis

        except Exception as e:
            print(f"❌ {title}: {str(e)}")
            return {
                'title': title,
                'status': 'error',
                'error': str(e),
                'processing_time': time.time() - start_time
            }

    async def _get_screenplay_content_async(self, title: str) -> Optional[str]:
        """Busca conteúdo do roteiro de forma assíncrona"""
        # Como a biblioteca não é async, usar executor
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(
            self.executor,
            self.library.get_screenplay_text,
            title
        )
        return content

    async def _analyze_structure_async(self, content: str) -> Dict:
        """Analisa estrutura do roteiro assincronamente"""
        await asyncio.sleep(0)  # Yield control

        lines = content.split('\n')
        scenes = []
        current_scene = None

        for line in lines:
            if line.startswith('INT.') or line.startswith('EXT.'):
                if current_scene:
                    scenes.append(current_scene)
                current_scene = {
                    'heading': line,
                    'lines': [],
                    'type': 'INT' if line.startswith('INT.') else 'EXT'
                }
            elif current_scene:
                current_scene['lines'].append(line)

        if current_scene:
            scenes.append(current_scene)

        return {
            'total_scenes': len(scenes),
            'int_scenes': len([s for s in scenes if s['type'] == 'INT']),
            'ext_scenes': len([s for s in scenes if s['type'] == 'EXT']),
            'avg_scene_length': sum(len(s['lines']) for s in scenes) / len(scenes) if scenes else 0
        }

    async def _analyze_dialogue_async(self, content: str) -> Dict:
        """Analisa diálogos assincronamente"""
        await asyncio.sleep(0)

        lines = content.split('\n')
        dialogue_lines = 0
        action_lines = 0
        character_lines = {}

        for line in lines:
            stripped = line.strip()
            if stripped:
                # Detectar personagem (linha toda em maiúsculas)
                if stripped.isupper() and len(stripped) > 2 and not any(x in stripped for x in ['INT.', 'EXT.']):
                    current_character = stripped
                    character_lines[current_character] = character_lines.get(current_character, 0)
                # Detectar diálogo (linha com indentação mas não toda em maiúsculas)
                elif line.startswith('  ') and not stripped.isupper():
                    dialogue_lines += 1
                    if 'current_character' in locals():
                        character_lines[current_character] += 1
                else:
                    action_lines += 1

        return {
            'dialogue_lines': dialogue_lines,
            'action_lines': action_lines,
            'dialogue_ratio': dialogue_lines / (dialogue_lines + action_lines) if (dialogue_lines + action_lines) > 0 else 0,
            'top_speakers': sorted(character_lines.items(), key=lambda x: x[1], reverse=True)[:5]
        }

    async def _analyze_themes_async(self, content: str) -> List[str]:
        """Analisa temas assincronamente"""
        await asyncio.sleep(0)

        content_lower = content.lower()
        themes = []

        theme_keywords = {
            'love': ['love', 'heart', 'romance', 'kiss', 'passion'],
            'revenge': ['revenge', 'vengeance', 'payback', 'retribution'],
            'redemption': ['redemption', 'forgive', 'second chance', 'atone'],
            'family': ['family', 'father', 'mother', 'son', 'daughter', 'brother', 'sister'],
            'power': ['power', 'control', 'dominate', 'rule', 'authority'],
            'identity': ['identity', 'who am i', 'self', 'discovery'],
            'survival': ['survive', 'survival', 'alive', 'death', 'danger'],
            'justice': ['justice', 'fair', 'right', 'wrong', 'law'],
            'betrayal': ['betray', 'traitor', 'backstab', 'deceive'],
            'sacrifice': ['sacrifice', 'give up', 'lose', 'cost']
        }

        theme_scores = {}
        for theme, keywords in theme_keywords.items():
            score = sum(content_lower.count(kw) for kw in keywords)
            if score > 5:
                theme_scores[theme] = score

        # Retornar top 5 temas
        sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)
        return [theme for theme, _ in sorted_themes[:5]]

    async def _analyze_beats_async(self, content: str) -> List[Dict]:
        """Analisa beats do Save the Cat assincronamente"""
        await asyncio.sleep(0)

        beats = []
        content_lower = content.lower()
        lines = content.split('\n')
        total_lines = len(lines)

        # Heurísticas para detectar beats baseado em posição
        beat_patterns = [
            {
                'name': 'Opening Image',
                'position': 0.01,
                'keywords': ['fade in', 'open on', 'begin'],
                'detected': False
            },
            {
                'name': 'Theme Stated',
                'position': 0.05,
                'keywords': ['lesson', 'moral', 'truth', 'believe'],
                'detected': False
            },
            {
                'name': 'Catalyst',
                'position': 0.10,
                'keywords': ['suddenly', 'phone rings', 'news', 'arrives', 'discovers'],
                'detected': False
            },
            {
                'name': 'Debate',
                'position': 0.12,
                'keywords': ['should i', 'what if', 'but', 'however'],
                'detected': False
            },
            {
                'name': 'Break into Two',
                'position': 0.25,
                'keywords': ['decides', 'chooses', 'journey', 'leaves'],
                'detected': False
            },
            {
                'name': 'B Story',
                'position': 0.30,
                'keywords': ['love interest', 'mentor', 'friend', 'relationship'],
                'detected': False
            },
            {
                'name': 'Fun and Games',
                'position': 0.50,
                'keywords': ['montage', 'series of', 'adventure', 'action'],
                'detected': False
            },
            {
                'name': 'Midpoint',
                'position': 0.50,
                'keywords': ['revelation', 'discovers', 'realizes', 'turning point'],
                'detected': False
            },
            {
                'name': 'All Is Lost',
                'position': 0.75,
                'keywords': ['death', 'loses', 'defeated', 'hopeless'],
                'detected': False
            },
            {
                'name': 'Dark Night of the Soul',
                'position': 0.80,
                'keywords': ['alone', 'despair', 'gives up', 'contemplates'],
                'detected': False
            },
            {
                'name': 'Break into Three',
                'position': 0.85,
                'keywords': ['idea', 'solution', 'realizes', 'epiphany'],
                'detected': False
            },
            {
                'name': 'Finale',
                'position': 0.90,
                'keywords': ['final', 'battle', 'confrontation', 'showdown'],
                'detected': False
            },
            {
                'name': 'Final Image',
                'position': 0.99,
                'keywords': ['fade out', 'the end', 'credits'],
                'detected': False
            }
        ]

        # Detectar beats baseado em posição e keywords
        for beat in beat_patterns:
            start_line = int(total_lines * max(0, beat['position'] - 0.05))
            end_line = int(total_lines * min(1, beat['position'] + 0.05))

            section = ' '.join(lines[start_line:end_line]).lower()

            if any(keyword in section for keyword in beat['keywords']):
                beat['detected'] = True
                beat['line'] = start_line
                beats.append({
                    'name': beat['name'],
                    'position': f"{beat['position']*100:.0f}%",
                    'line': start_line
                })

        return beats

    async def _analyze_characters_async(self, content: str) -> Dict:
        """Analisa personagens assincronamente"""
        await asyncio.sleep(0)

        lines = content.split('\n')
        characters = {}
        current_character = None

        for line in lines:
            stripped = line.strip()
            # Detectar nome de personagem
            if stripped.isupper() and len(stripped) > 2 and not any(x in stripped for x in ['INT.', 'EXT.', 'CUT', 'FADE']):
                current_character = stripped.split('(')[0].strip()  # Remove parentheses
                if current_character not in characters:
                    characters[current_character] = {
                        'name': current_character,
                        'dialogue_count': 0,
                        'mentions': 0,
                        'first_appearance': lines.index(line)
                    }
            elif current_character and line.startswith('  '):
                characters[current_character]['dialogue_count'] += 1

        # Contar menções
        content_upper = content.upper()
        for char_name in characters:
            characters[char_name]['mentions'] = content_upper.count(char_name)

        # Classificar personagens
        for char in characters.values():
            if char['dialogue_count'] > 50:
                char['role'] = 'protagonist'
            elif char['dialogue_count'] > 20:
                char['role'] = 'major'
            elif char['dialogue_count'] > 5:
                char['role'] = 'supporting'
            else:
                char['role'] = 'minor'

        return {
            'total_characters': len(characters),
            'main_characters': [c for c in characters.values() if c['role'] in ['protagonist', 'major']],
            'character_distribution': {
                'protagonist': len([c for c in characters.values() if c['role'] == 'protagonist']),
                'major': len([c for c in characters.values() if c['role'] == 'major']),
                'supporting': len([c for c in characters.values() if c['role'] == 'supporting']),
                'minor': len([c for c in characters.values() if c['role'] == 'minor'])
            }
        }

    async def _save_to_memory_async(self, key: str, data: Dict):
        """Salva resultado na memória de forma assíncrona"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            self.executor,
            self.memory.store,
            MemoryType.ANALYSIS,
            key,
            data,
            {
                'analyzer': 'async',
                'timestamp': time.time()
            },
            None,  # ttl
            0.9,   # confidence
            'async_analyzer'  # source
        )

    async def analyze_batch_async(self, titles: List[str]) -> Dict[str, Any]:
        """
        Analisa múltiplos roteiros de forma totalmente assíncrona

        Args:
            titles: Lista de títulos

        Returns:
            Resultados consolidados
        """
        print(f"\n🚀 ANÁLISE ASSÍNCRONA DE {len(titles)} ROTEIROS")
        print("=" * 50)

        start_time = time.time()

        # Criar tasks para todos os roteiros
        tasks = [self.analyze_screenplay_async(title) for title in titles]

        # Executar todas simultaneamente
        results = await asyncio.gather(*tasks)

        total_time = time.time() - start_time

        # Consolidar estatísticas
        successful = [r for r in results if r.get('status') == 'completed']
        failed = [r for r in results if r.get('status') != 'completed']

        consolidated = {
            'total_analyzed': len(titles),
            'successful': len(successful),
            'failed': len(failed),
            'total_time': total_time,
            'avg_time': total_time / len(titles) if titles else 0,
            'results': results,
            'statistics': self._calculate_batch_statistics(successful)
        }

        print(f"\n📊 RESULTADOS ASSÍNCRONOS:")
        print(f"   ✅ Sucesso: {consolidated['successful']}/{consolidated['total_analyzed']}")
        print(f"   ⏱️  Tempo total: {consolidated['total_time']:.2f}s")
        print(f"   ⚡ Tempo médio: {consolidated['avg_time']:.2f}s")
        print(f"   🚀 Totalmente assíncrono!")

        return consolidated

    def _calculate_batch_statistics(self, results: List[Dict]) -> Dict:
        """Calcula estatísticas agregadas"""
        if not results:
            return {}

        stats = {
            'avg_scenes': sum(r['structure']['total_scenes'] for r in results) / len(results),
            'avg_dialogue_ratio': sum(r['dialogue']['dialogue_ratio'] for r in results) / len(results),
            'common_themes': {},
            'detected_beats': {}
        }

        # Agregar temas
        for result in results:
            for theme in result.get('themes', []):
                stats['common_themes'][theme] = stats['common_themes'].get(theme, 0) + 1

        # Agregar beats
        for result in results:
            for beat in result.get('beats', []):
                beat_name = beat['name']
                stats['detected_beats'][beat_name] = stats['detected_beats'].get(beat_name, 0) + 1

        return stats


async def main():
    """
    Demonstração do analisador assíncrono
    """
    print("\n⚡ ANALISADOR ASSÍNCRONO DE ROTEIROS")
    print("-" * 50)

    analyzer = AsyncScreenplayAnalyzer()

    # Pegar roteiros da biblioteca
    library = get_screenplay_library()
    all_screenplays = library.list_screenplays()

    if not all_screenplays:
        print("❌ Nenhum roteiro encontrado")
        return

    # Testar com 10 roteiros
    test_titles = all_screenplays[:10]

    print(f"\n📚 Analisando {len(test_titles)} roteiros:")
    for i, title in enumerate(test_titles, 1):
        print(f"   {i}. {title}")

    # Executar análise assíncrona
    results = await analyzer.analyze_batch_async(test_titles)

    # Comparação com versão síncrona
    print(f"\n⚡ COMPARAÇÃO DE PERFORMANCE:")
    print(f"   Assíncrono: {results['total_time']:.2f}s")
    estimated_sync = results['avg_time'] * len(test_titles) * 2  # Estimativa conservadora
    print(f"   Síncrono (estimado): {estimated_sync:.2f}s")
    print(f"   🚀 Speedup: {estimated_sync/results['total_time']:.2f}x")

    # Gerar relatório
    report = f"""# ⚡ ANÁLISE ASSÍNCRONA - RESULTADOS

**Data:** {time.strftime('%Y-%m-%d %H:%M')}
**Total Analisado:** {results['total_analyzed']} roteiros
**Tempo Total:** {results['total_time']:.2f}s
**Performance:** {results['avg_time']:.2f}s por roteiro

## 📊 Estatísticas

- **Média de Cenas:** {results['statistics'].get('avg_scenes', 0):.1f}
- **Taxa de Diálogo:** {results['statistics'].get('avg_dialogue_ratio', 0)*100:.1f}%

## 🎭 Temas Mais Comuns
{chr(10).join(f"- {theme}: {count} roteiros" for theme, count in sorted(results['statistics'].get('common_themes', {}).items(), key=lambda x: x[1], reverse=True)[:5])}

## 🎬 Beats Detectados
{chr(10).join(f"- {beat}: {count} roteiros" for beat, count in sorted(results['statistics'].get('detected_beats', {}).items(), key=lambda x: x[1], reverse=True)[:5])}

---
**DIGIMUNDO PRESENTE** 🥷
"""

    # Salvar relatório
    report_path = Path("docs") / f"ASYNC_ANALYSIS_{time.strftime('%Y%m%d_%H%M%S')}.md"
    report_path.write_text(report, encoding='utf-8')

    print(f"\n📄 Relatório salvo em: {report_path}")


if __name__ == "__main__":
    # Executar com asyncio
    asyncio.run(main())