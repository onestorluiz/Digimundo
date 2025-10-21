#!/usr/bin/env python3
"""
Screenplay Analyzer - Triple-Core Main Orchestrator

Orquestra todos os 22 especialistas Triple-Core para análise completa de screenplay.
"""

import time
from pathlib import Path
from typing import Dict, Any, Optional
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

# Import orchestrator components
from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper
from triple_core.aggregators import OverallQualityAggregator, ExecutiveSummaryGenerator


class ScreenplayAnalyzer:
    """
    Orquestrador principal que executa todos os 22 especialistas Triple-Core.
    """

    def __init__(self, llm_model: str = "scripturemon-optimized", deep_context: bool = True):
        """
        Initialize the screenplay analyzer.

        Args:
            llm_model: Ollama model to use for Core 3
            deep_context: Whether to use deep context (True = better quality, False = faster)
        """
        self.llm_model = llm_model
        self.deep_context = deep_context

        # Initialize all 22 specialists
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

        print(f"✅ Initialized {len(self.specialists)} Triple-Core specialists")
        print(f"🤖 LLM Model: {llm_model}")
        print(f"📚 Deep Context: {deep_context}")

    def analyze_screenplay(
        self,
        screenplay_path: str,
        output_dir: str = "workspace/outputs/analysis"
    ) -> Dict[str, Any]:
        """
        Analisa screenplay completo com todos os 22 especialistas.

        Args:
            screenplay_path: Path to screenplay file
            output_dir: Directory to save reports

        Returns:
            Complete analysis results
        """
        print("\n" + "="*80)
        print("🎬 SCREENPLAY ANALYZER - Triple-Core Complete Analysis")
        print("="*80)
        print()

        # Load screenplay
        print(f"📄 Loading screenplay: {screenplay_path}")
        screenplay_text = self._load_screenplay(screenplay_path)
        screenplay_stats = self._get_screenplay_stats(screenplay_text)

        print(f"   ✅ Loaded: {screenplay_stats['pages']} pages, "
              f"{screenplay_stats['scenes']} scenes, "
              f"{screenplay_stats['words']:,} words")
        print()

        # Run all 22 specialists
        print(f"⚡ Running {len(self.specialists)} Triple-Core specialists...")
        print()

        start_time = time.time()
        specialist_results = {}

        for i, (name, specialist) in enumerate(self.specialists.items(), 1):
            print(f"[{i:2d}/22] Running {name}...", end=" ", flush=True)

            spec_start = time.time()

            # Wrap with Triple-Core
            wrapper = TripleCoreWrapper(
                python_specialist=specialist,
                llm_model=self.llm_model,
                deep_context=self.deep_context
            )

            # Analyze
            result = wrapper.analyze(screenplay_text)

            spec_time = time.time() - spec_start

            # Extract score safely (handle both "score" and 'score')
            score = result.get('score') or result.get('python_core1', {}).get('score', 0)

            print(f"✅ Score: {score}/100 ({spec_time:.1f}s)")

            specialist_results[name] = result

        total_time = time.time() - start_time

        print()
        print(f"✅ All {len(self.specialists)} specialists completed in {total_time:.1f}s")
        print()

        # Aggregate results
        print("📊 Aggregating results...")
        aggregator = OverallQualityAggregator()

        # Prepare results for aggregator (extract python_core1 scores)
        aggregator_input = {}
        for name, result in specialist_results.items():
            # Get Core 1 results
            core1 = result.get('python_core1', {})
            if core1:
                aggregator_input[name] = core1
            else:
                # Fallback: use result directly if no python_core1
                aggregator_input[name] = result

        overall_quality = aggregator.aggregate(aggregator_input)

        print(f"   ✅ Overall Score: {overall_quality.overall_score:.1f}/100 "
              f"({overall_quality.quality_level.upper()})")
        print()

        # Generate executive summary
        print("📝 Generating executive summary...")
        generator = ExecutiveSummaryGenerator()

        screenplay_title = Path(screenplay_path).stem.replace('_', ' ').title()

        summary = generator.generate(
            screenplay_title=screenplay_title,
            screenplay_stats=screenplay_stats,
            overall_quality_result=overall_quality,
            specialist_results=aggregator_input
        )

        print(f"   ✅ Summary generated")
        print()

        # Save reports
        print("💾 Saving reports...")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{screenplay_title.replace(' ', '_')}_{timestamp}"

        html_path = output_path / f"{base_name}.html"
        md_path = output_path / f"{base_name}.md"

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(summary.html_report)
        print(f"   ✅ HTML: {html_path}")

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(summary.markdown_report)
        print(f"   ✅ Markdown: {md_path}")

        print()
        print("="*80)
        print("✅ ANALYSIS COMPLETE!")
        print("="*80)
        print()
        print(f"📊 Overall Score: {overall_quality.overall_score:.1f}/100 ({overall_quality.quality_level.upper()})")
        print(f"⏱️  Total Time: {total_time:.1f}s")
        print(f"📄 Reports saved to: {output_dir}")
        print()

        return {
            'screenplay_path': screenplay_path,
            'screenplay_stats': screenplay_stats,
            'specialist_results': specialist_results,
            'overall_quality': overall_quality,
            'executive_summary': summary,
            'total_time': total_time,
            'html_report_path': str(html_path),
            'markdown_report_path': str(md_path)
        }

    def _load_screenplay(self, path: str) -> str:
        """Load screenplay from file (supports PDF, TXT, Fountain, MD)."""
        if path.endswith('.pdf'):
            # PDF is supported natively by Read tool
            # For Python processing, we extract text
            try:
                import PyPDF2
                with open(path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            except ImportError:
                # Fallback: use pdfplumber if available
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
            # TXT, Fountain, MD, etc.
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()

    def _get_screenplay_stats(self, text: str) -> Dict[str, Any]:
        """Get basic screenplay statistics."""
        lines = text.split('\n')
        words = text.split()

        # Estimate pages (roughly 55 lines per page)
        pages = max(1, len(lines) // 55)

        # Count scenes (INT. or EXT. at start of line)
        scenes = sum(1 for line in lines if line.strip().upper().startswith(('INT.', 'EXT.')))

        # Estimate characters (unique character names in dialogue)
        # Very rough estimation
        characters = len(set(
            line.strip().rstrip(':').strip()
            for line in lines
            if line.strip() and line.strip()[0].isupper() and ':' not in line[-10:]
        ))

        return {
            'pages': pages,
            'scenes': max(1, scenes),
            'words': len(words),
            'lines': len(lines),
            'characters': min(characters, 50)  # Cap at reasonable number
        }


if __name__ == "__main__":
    # Example usage
    analyzer = ScreenplayAnalyzer(
        llm_model="scripturemon-optimized",
        deep_context=True  # True = better quality (Deep Dive), False = faster (Shallow)
    )

    # Analyze a screenplay
    result = analyzer.analyze_screenplay(
        screenplay_path="content/screenplays/personal/sonhos_sem_lembrancas_t3.txt",
        output_dir="workspace/outputs/analysis"
    )

    print(f"Analysis saved to: {result['html_report_path']}")
