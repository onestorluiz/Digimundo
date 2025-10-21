#!/usr/bin/env python3
"""
🔍 BENCHMARK PATTERN MINER
Extrai padrões quantitativos e qualitativos das análises de sucesso.

Fase 1 do plano de melhoria baseada em benchmarks.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any
from bs4 import BeautifulSoup


class BenchmarkPatternMiner:
    """
    Minera padrões de análises de alta qualidade (benchmarks).

    Extrai:
    - Métricas quantitativas (chars, palavras, parágrafos, citações)
    - Padrões estruturais (seções, formato, organização)
    - Padrões de conteúdo (tipos de exemplos, citações, recomendações)
    """

    def __init__(self, benchmark_html_paths: List[Path]):
        self.benchmark_paths = benchmark_html_paths
        self.patterns = {}

    def extract_llm_insights_text(self, html_path: Path) -> str:
        """Extrai o texto dos LLM insights do HTML."""
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find PARTE 2 section
        part2 = soup.find('div', class_='part-2')
        if not part2:
            return ""

        # Extract all insight paragraphs
        insights = part2.find_all('div', class_='insight-paragraph')

        # Join all text
        text = '\n\n'.join(p.get_text(strip=True) for p in insights)
        return text

    def analyze_single_benchmark(self, html_path: Path) -> Dict[str, Any]:
        """Analisa um único arquivo de benchmark."""

        llm_text = self.extract_llm_insights_text(html_path)

        # 1. MÉTRICAS QUANTITATIVAS
        char_count = len(llm_text)
        word_count = len(llm_text.split())

        # Contar parágrafos (separados por \n\n ou por marcadores como **Problemas:**)
        paragraphs = [p.strip() for p in llm_text.split('\n\n') if p.strip()]
        paragraph_count = len(paragraphs)

        # 2. CITAÇÕES E EXEMPLOS
        # Citações diretas entre aspas
        quote_pattern = r'"([^"]+)"'
        quotes = re.findall(quote_pattern, llm_text)
        quote_count = len(quotes)

        # Citações de cena/página
        scene_citations = len(re.findall(r'\bcena\s+\d+\b', llm_text.lower()))
        page_citations = len(re.findall(r'\bpágina\s+\d+\b', llm_text.lower()))

        # Menções de personagens (nomes próprios em maiúscula)
        character_pattern = r'\b[A-Z][a-záàâãéêíóôõúç]+\b'
        characters = set(re.findall(character_pattern, llm_text))
        character_count = len(characters)

        # 3. ESTRUTURA E SEÇÕES
        # Identificar seções principais (marcadas com **)
        section_pattern = r'\*\*([^*]+):\*\*'
        sections = re.findall(section_pattern, llm_text)
        section_count = len(sections)

        # 4. INDICADORES DE PROFUNDIDADE
        depth_indicators = [
            'porque', 'portanto', 'exemplo', 'especificamente',
            'notamos que', 'sugere que', 'pode ser', 'recomend',
            'em vez de', 'isto', 'adicional'
        ]
        depth_count = sum(
            llm_text.lower().count(indicator)
            for indicator in depth_indicators
        )

        # 5. EXEMPLOS BEFORE/AFTER
        before_after_pattern = r'(em vez de|invés de|ao invés de|substituir|trocar)'
        before_after_count = len(re.findall(before_after_pattern, llm_text.lower()))

        # 6. ANÁLISE DE SEÇÕES
        has_interpretation = 'interpretação' in llm_text.lower()
        has_patterns = 'padrões' in llm_text.lower() or 'padrão' in llm_text.lower()
        has_problems = 'problemas' in llm_text.lower() or 'problema' in llm_text.lower()
        has_solutions = 'soluções' in llm_text.lower() or 'solução' in llm_text.lower()
        has_context = 'contexto' in llm_text.lower()

        return {
            'file_name': html_path.name,
            'author_type': self._extract_author_from_filename(html_path.name),

            # Quantitative metrics
            'char_count': char_count,
            'word_count': word_count,
            'paragraph_count': paragraph_count,
            'avg_paragraph_length': char_count / paragraph_count if paragraph_count > 0 else 0,

            # Citations & Examples
            'quote_count': quote_count,
            'scene_citations': scene_citations,
            'page_citations': page_citations,
            'character_mentions': character_count,
            'before_after_examples': before_after_count,

            # Structure
            'section_count': section_count,
            'sections': sections,
            'has_interpretation': has_interpretation,
            'has_patterns': has_patterns,
            'has_problems': has_problems,
            'has_solutions': has_solutions,
            'has_context': has_context,

            # Depth
            'depth_indicators': depth_count,
            'depth_density': depth_count / word_count if word_count > 0 else 0,

            # Sample quotes
            'sample_quotes': quotes[:3] if quotes else [],
            'sample_characters': list(characters)[:5] if characters else []
        }

    def _extract_author_from_filename(self, filename: str) -> str:
        """Extrai o tipo de autor do nome do arquivo."""
        match = re.search(r'ANALISE_([A-Z_]+)_', filename)
        return match.group(1) if match else 'UNKNOWN'

    def mine_patterns(self) -> Dict[str, Any]:
        """
        Minera padrões de todos os benchmarks.

        Returns:
            Dict com padrões agregados e individuais
        """
        individual_analyses = []

        print('🔍 MINERANDO PADRÕES DOS BENCHMARKS')
        print('='*80)
        print()

        for html_path in self.benchmark_paths:
            print(f'📖 Analisando: {html_path.name}')
            analysis = self.analyze_single_benchmark(html_path)
            individual_analyses.append(analysis)

            # Print summary
            print(f'   ✅ {analysis["char_count"]:,} chars, {analysis["word_count"]:,} palavras')
            print(f'   📝 {analysis["paragraph_count"]} parágrafos')
            print(f'   📊 {analysis["quote_count"]} citações diretas')
            print(f'   🎬 {analysis["scene_citations"]} cenas, {analysis["page_citations"]} páginas')
            print(f'   👥 {analysis["character_mentions"]} personagens mencionados')
            print()

        # AGGREGATE PATTERNS
        print('📊 CALCULANDO PADRÕES AGREGADOS...')
        print()

        n = len(individual_analyses)

        aggregated = {
            # Averages
            'avg_char_count': sum(a['char_count'] for a in individual_analyses) / n,
            'avg_word_count': sum(a['word_count'] for a in individual_analyses) / n,
            'avg_paragraph_count': sum(a['paragraph_count'] for a in individual_analyses) / n,
            'avg_paragraph_length': sum(a['avg_paragraph_length'] for a in individual_analyses) / n,

            'avg_quote_count': sum(a['quote_count'] for a in individual_analyses) / n,
            'avg_scene_citations': sum(a['scene_citations'] for a in individual_analyses) / n,
            'avg_page_citations': sum(a['page_citations'] for a in individual_analyses) / n,
            'avg_character_mentions': sum(a['character_mentions'] for a in individual_analyses) / n,
            'avg_before_after_examples': sum(a['before_after_examples'] for a in individual_analyses) / n,

            'avg_section_count': sum(a['section_count'] for a in individual_analyses) / n,
            'avg_depth_indicators': sum(a['depth_indicators'] for a in individual_analyses) / n,
            'avg_depth_density': sum(a['depth_density'] for a in individual_analyses) / n,

            # Minimums (thresholds)
            'min_char_count': min(a['char_count'] for a in individual_analyses),
            'min_word_count': min(a['word_count'] for a in individual_analyses),
            'min_paragraph_count': min(a['paragraph_count'] for a in individual_analyses),
            'min_quote_count': min(a['quote_count'] for a in individual_analyses),

            # Structure patterns
            'required_sections': {
                'interpretation': all(a['has_interpretation'] for a in individual_analyses),
                'patterns': all(a['has_patterns'] for a in individual_analyses),
                'problems': all(a['has_problems'] for a in individual_analyses),
                'solutions': all(a['has_solutions'] for a in individual_analyses),
                'context': all(a['has_context'] for a in individual_analyses),
            },

            # All sections found
            'all_sections': list(set(
                section
                for a in individual_analyses
                for section in a['sections']
            )),
        }

        # Print aggregated patterns
        print('📈 PADRÕES AGREGADOS:')
        print()
        print(f'   Média de caracteres: {aggregated["avg_char_count"]:,.0f}')
        print(f'   Média de palavras: {aggregated["avg_word_count"]:,.0f}')
        print(f'   Média de parágrafos: {aggregated["avg_paragraph_count"]:.1f}')
        print()
        print(f'   Média de citações diretas: {aggregated["avg_quote_count"]:.1f}')
        print(f'   Média de cenas citadas: {aggregated["avg_scene_citations"]:.1f}')
        print(f'   Média de páginas citadas: {aggregated["avg_page_citations"]:.1f}')
        print(f'   Média de personagens: {aggregated["avg_character_mentions"]:.1f}')
        print(f'   Média de exemplos before/after: {aggregated["avg_before_after_examples"]:.1f}')
        print()
        print(f'   Seções obrigatórias:')
        for section, required in aggregated['required_sections'].items():
            status = '✅' if required else '⚠️ '
            print(f'      {status} {section}')
        print()

        self.patterns = {
            'individual_analyses': individual_analyses,
            'aggregated_patterns': aggregated,
            'benchmark_count': n,
            'mined_at': str(Path.cwd())
        }

        return self.patterns

    def save_patterns(self, output_path: Path):
        """Salva padrões em JSON."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.patterns, f, indent=2, ensure_ascii=False)

        print(f'💾 Padrões salvos em: {output_path}')
        print()


def main():
    """Executa mineração de padrões."""

    # Paths dos benchmarks
    benchmarks = [
        Path('workspace/outputs/TE_ENCONTRO_EM_MIM__dialogue_0001/1_individuais/ANALISE_MCKEE_DIALOGUE_20251009_112138.html'),
        Path('workspace/outputs/TE_ENCONTRO_EM_MIM__dialogue_0001/1_individuais/ANALISE_CAMPBELL_20251009_111908.html')
    ]

    # Check existence
    for path in benchmarks:
        if not path.exists():
            print(f'❌ ERRO: Benchmark não encontrado: {path}')
            return

    # Mine patterns
    miner = BenchmarkPatternMiner(benchmarks)
    patterns = miner.mine_patterns()

    # Save
    output_path = Path('/Users/clubproducoes/Digimundo/claude_code/benchmark_patterns.json')
    miner.save_patterns(output_path)

    print('='*80)
    print('✅ MINERAÇÃO COMPLETA!')
    print('='*80)
    print()
    print(f'📊 {len(benchmarks)} benchmarks analisados')
    print(f'📁 Padrões salvos em: {output_path}')
    print()
    print('🎯 PRÓXIMO PASSO: Fase 2 - Prompt Engineering')
    print('   Use esses padrões para gerar prompts melhorados')
    print()


if __name__ == '__main__':
    main()
