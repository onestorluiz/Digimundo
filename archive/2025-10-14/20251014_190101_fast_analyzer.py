#!/usr/bin/env python3
"""
Fast Analyzer - Core 1 Only (sem LLM)

Orquestrador rápido que executa apenas Core 1 (análise Python)
dos 22 especialistas, sem Core 2 (examples) e Core 3 (LLM).

Útil para:
- Testes rápidos
- Desenvolvimento
- Validação de implementação
"""

import time
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Import all 22 specialists
from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.core_1_specialists.structure.dr_structure import DrStructure
from triple_core.core_1_specialists.pacing.dr_pacing import DrPacing
from triple_core.core_1_specialists.opening.dr_opening import DrOpening
from triple_core.core_1_specialists.climax.dr_climax import DrClimax
from triple_core.core_1_specialists.resolution.dr_resolution import DrResolution
from triple_core.core_1_specialists.transitions.dr_transitions import DrTransitions
from triple_core.core_1_specialists.action.dr_action import DrAction
from triple_core.core_1_specialists.formatting.dr_formatting import DrFormatting
from triple_core.core_1_specialists.subtext.dr_subtext import DrSubtext
from triple_core.core_1_specialists.theme.dr_theme import DrTheme
from triple_core.core_1_specialists.tone.dr_tone import DrTone
from triple_core.core_1_specialists.voice.dr_voice import DrVoice
from triple_core.core_1_specialists.symbolism.dr_symbolism import DrSymbolism
from triple_core.core_1_specialists.visual.dr_visual_motifs import DrVisualMotifs
from triple_core.core_1_specialists.genre.dr_genre import DrGenreConventions
from triple_core.core_1_specialists.worldbuilding.dr_worldbuilding import DrWorldBuilding
from triple_core.core_1_specialists.character.psychology.dr_psychology import DrCharacterPsychology
from triple_core.core_1_specialists.character.arcs.dr_arcs import DrCharacterArcs
from triple_core.core_1_specialists.character.relationships.dr_relationships import DrRelationships
from triple_core.core_1_specialists.originality.dr_originality import DrOriginalityAssessment
from triple_core.core_1_specialists.market.dr_market_potential import DrMarketPotential

from triple_core.aggregators import OverallQualityAggregator, ExecutiveSummaryGenerator


class FastAnalyzer:
    """Análise rápida - Core 1 apenas (Python, sem LLM)."""

    def __init__(self):
        """Initialize fast analyzer."""
        self.specialists = {
            # NARRATIVE (6)
            'Structure': DrStructure(),
            'Pacing': DrPacing(),
            'Opening': DrOpening(),
            'Climax': DrClimax(),
            'Resolution': DrResolution(),
            'Transitions': DrTransitions(),

            # CHARACTER (3)
            'Character Psychology': DrCharacterPsychology(),
            'Character Arcs': DrCharacterArcs(),
            'Character Relationships': DrRelationships(),

            # DIALOGUE (3)
            'Dialogue': DrDialogue(),
            'Voice Consistency': DrVoice(),
            'Subtext': DrSubtext(),

            # TECHNICAL (2)
            'Formatting': DrFormatting(),
            'Action Description': DrAction(),

            # DEPTH (5)
            'Symbolism': DrSymbolism(),
            'Theme Consistency': DrTheme(),
            'Tone Consistency': DrTone(),
            'Visual Motifs': DrVisualMotifs(),
            'Genre Conventions': DrGenreConventions(),

            # CRAFT (1)
            'World Building': DrWorldBuilding(),

            # MARKET (2)
            'Originality': DrOriginalityAssessment(),
            'Market Potential': DrMarketPotential(),
        }

        print(f"✅ Fast Analyzer initialized ({len(self.specialists)} specialists)")
        print(f"⚡ Mode: Core 1 only (Python analysis, no LLM)")

    def analyze_screenplay(
        self,
        screenplay_path: str,
        output_dir: str = "workspace/outputs/fast_analysis"
    ) -> Dict[str, Any]:
        """
        Análise rápida com Core 1 apenas.

        Args:
            screenplay_path: Path to screenplay
            output_dir: Output directory

        Returns:
            Analysis results
        """
        print("\n" + "="*80)
        print("⚡ FAST ANALYZER - Core 1 Only (Python Analysis)")
        print("="*80)
        print()

        # Load screenplay
        print(f"📄 Loading: {screenplay_path}")
        screenplay_text = self._load_screenplay(screenplay_path)
        stats = self._get_screenplay_stats(screenplay_text)
        print(f"   ✅ {stats['pages']} pages, {stats['scenes']} scenes, {stats['words']:,} words")
        print()

        # Run all specialists (Core 1 only)
        print(f"⚡ Running {len(self.specialists)} specialists (Core 1 only)...")
        print()

        start_time = time.time()
        results = {}

        for i, (name, specialist) in enumerate(self.specialists.items(), 1):
            print(f"[{i:2d}/22] {name:25s}...", end=" ", flush=True)

            try:
                spec_start = time.time()

                # Call analyze() directly (Core 1 only)
                result = specialist.analyze(screenplay_text)

                spec_time = time.time() - spec_start

                # Extract score (handle both "score" and 'score')
                score = result.get('score') or result.get('score', 0)

                print(f"✅ {score:3d}/100 ({spec_time:.2f}s)")

                results[name] = result

            except Exception as e:
                print(f"❌ ERROR: {e}")
                results[name] = {'score': 0, 'error': str(e)}

        total_time = time.time() - start_time

        print()
        print(f"✅ All specialists completed in {total_time:.1f}s")
        print(f"   Average: {total_time/len(self.specialists):.2f}s per specialist")
        print()

        # Aggregate
        print("📊 Aggregating results...")
        aggregator = OverallQualityAggregator()
        overall = aggregator.aggregate(results)
        print(f"   ✅ Overall: {overall.overall_score:.1f}/100 ({overall.quality_level.upper()})")
        print()

        # Generate summary
        print("📝 Generating summary...")
        generator = ExecutiveSummaryGenerator()
        title = Path(screenplay_path).stem.replace('_', ' ').title()

        summary = generator.generate(
            screenplay_title=title,
            screenplay_stats=stats,
            overall_quality_result=overall,
            specialist_results=results
        )
        print(f"   ✅ Summary generated")
        print()

        # Save reports
        print("💾 Saving reports...")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{title.replace(' ', '_')}_FAST_{timestamp}"

        html_path = output_path / f"{base_name}.html"
        md_path = output_path / f"{base_name}.md"

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(summary.html_report)
        print(f"   ✅ HTML: {html_path}")

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(summary.markdown_report)
        print(f"   ✅ MD:   {md_path}")

        print()
        print("="*80)
        print("✅ FAST ANALYSIS COMPLETE!")
        print("="*80)
        print()
        print(f"📊 Overall: {overall.overall_score:.1f}/100 ({overall.quality_level.upper()})")
        print(f"⏱️  Time:    {total_time:.1f}s")
        print()

        return {
            'screenplay_path': screenplay_path,
            'stats': stats,
            'results': results,
            'overall': overall,
            'summary': summary,
            'time': total_time,
            'html_path': str(html_path),
            'md_path': str(md_path)
        }

    def _load_screenplay(self, path: str) -> str:
        """Load screenplay from file (supports PDF, TXT, Fountain, MD)."""
        if path.endswith('.pdf'):
            try:
                import PyPDF2
                with open(path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            except ImportError:
                try:
                    import pdfplumber
                    with pdfplumber.open(path) as pdf:
                        text = ""
                        for page in pdf.pages:
                            text += page.extract_text() + "\n"
                        return text
                except ImportError:
                    raise ImportError(
                        "PDF support requires PyPDF2 or pdfplumber. "
                        "Install with: pip install PyPDF2 or pip install pdfplumber"
                    )
        else:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()

    def _get_screenplay_stats(self, text: str) -> Dict[str, Any]:
        """Get stats."""
        lines = text.split('\n')
        words = text.split()
        pages = max(1, len(lines) // 55)
        scenes = sum(1 for line in lines if line.strip().upper().startswith(('INT.', 'EXT.')))

        return {
            'pages': pages,
            'scenes': max(1, scenes),
            'words': len(words),
            'lines': len(lines),
            'characters': 12  # Estimate
        }


if __name__ == "__main__":
    analyzer = FastAnalyzer()
    result = analyzer.analyze_screenplay(
        "content/screenplays/personal/sonhos_sem_lembrancas_t3.txt"
    )
    print(f"Reports: {result['html_path']}")
