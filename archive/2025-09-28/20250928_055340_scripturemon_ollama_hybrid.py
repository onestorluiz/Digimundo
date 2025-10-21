#!/usr/bin/env python3
"""
SCRIPTUREMON ULTIMATE - OLLAMA HYBRID INTEGRATION
Combines Ollama modelfiles with Python orchestration for best of both worlds
"""

import json
import logging
import time
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ScripturemonOllamaHybrid:
    """
    Hybrid system that uses Ollama registered models with Python orchestration
    """

    def __init__(self, use_modelfiles: bool = False):
        """
        Initialize the hybrid system

        Args:
            use_modelfiles: If True, use registered Ollama models. If False, use API directly
        """
        self.use_modelfiles = use_modelfiles

        # Specialist order
        self.specialists = [
            "dialogue", "character", "pacing", "theme", "action",
            "structure", "conflict", "tension", "subtext", "exposition",
            "transitions", "opening", "climax", "resolution", "worldbuilding",
            "stakes", "motivation", "backstory", "foreshadowing", "twist",
            "symbolism", "tone", "genre"
        ]

        if use_modelfiles:
            self._check_models()

    def _check_models(self):
        """Check if Ollama models are registered"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True
            )

            available = result.stdout
            missing = []

            for specialist in self.specialists:
                model_name = f"scripturemon-{specialist}"
                if model_name not in available:
                    missing.append(model_name)

            if missing:
                logger.warning(f"Missing models: {missing[:3]}... ({len(missing)} total)")
                logger.info("Run: cd modelfiles && ./register_models.sh")
                logger.info("Falling back to API mode")
                self.use_modelfiles = False
            else:
                logger.info(f"✅ All {len(self.specialists)} specialist models registered")

        except Exception as e:
            logger.error(f"Error checking models: {e}")
            self.use_modelfiles = False

    def analyze_with_modelfile(self, specialist: str, screenplay: str, context: str = "") -> str:
        """Run analysis using registered Ollama model"""

        model_name = f"scripturemon-{specialist}"

        # Prepare input with context
        if context:
            full_input = f"{context}\n\n--- SCREENPLAY TO ANALYZE ---\n\n{screenplay}"
        else:
            full_input = screenplay

        try:
            # Run ollama with the model
            result = subprocess.run(
                ['ollama', 'run', model_name],
                input=full_input,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                return result.stdout
            else:
                logger.error(f"Model {model_name} failed: {result.stderr}")
                return f"Analysis failed for {specialist}"

        except subprocess.TimeoutExpired:
            logger.error(f"Timeout for {model_name}")
            return f"Timeout for {specialist}"
        except Exception as e:
            logger.error(f"Error running {model_name}: {e}")
            return f"Error for {specialist}"

    def analyze_with_api(self, specialist: str, screenplay: str, context: str = "") -> str:
        """Run analysis using Ollama API (fallback)"""

        # This would use the existing scripturemon_ultimate_system.py logic
        # Import and use the existing system
        try:
            from scripturemon_ultimate_system import ScripturemonUltimateSystem
            system = ScripturemonUltimateSystem()

            # Use the specialist prompts from the system
            specialist_key = f"{self.specialists.index(specialist)+1:02d}_{specialist.upper()}"
            prompt = system.specialist_prompts.get(specialist_key, "")

            if context:
                prompt += f"\n\n{context}"

            # Run the specialist
            return system._run_specialist(specialist_key, screenplay, context)

        except Exception as e:
            logger.error(f"API fallback failed: {e}")
            return f"Analysis failed for {specialist}"

    def run_sequential_analysis(self, screenplay_file: str, output_dir: str = "hybrid_reports"):
        """
        Run complete sequential analysis

        Args:
            screenplay_file: Path to screenplay file
            output_dir: Directory for output reports
        """

        # Read screenplay
        with open(screenplay_file, 'r', encoding='utf-8') as f:
            screenplay = f.read()

        # Setup output
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = output_path / f"hybrid_analysis_{timestamp}.md"

        # Initialize report
        with open(report_file, 'w') as f:
            f.write(f"# SCRIPTUREMON ULTIMATE HYBRID ANALYSIS\n\n")
            f.write(f"**Generated**: {timestamp}\n")
            f.write(f"**Mode**: {'Modelfiles' if self.use_modelfiles else 'API'}\n\n")
            f.write("---\n\n")

        logger.info("=" * 60)
        logger.info("STARTING HYBRID ANALYSIS")
        logger.info(f"Mode: {'Modelfiles' if self.use_modelfiles else 'API'}")
        logger.info("=" * 60)

        # Run specialists sequentially with context passing
        previous_analyses = ""

        for i, specialist in enumerate(self.specialists, 1):
            logger.info(f"\n[{i}/{len(self.specialists)}] Running {specialist}...")

            # Prepare context from previous analyses
            if i > 1:
                context = f"CONTEXT: Previous specialists have analyzed this screenplay:\n{previous_analyses[:2000]}"
            else:
                context = ""

            # Run analysis
            if self.use_modelfiles:
                analysis = self.analyze_with_modelfile(specialist, screenplay, context)
            else:
                analysis = self.analyze_with_api(specialist, screenplay, context)

            # Append to report
            with open(report_file, 'a') as f:
                f.write(f"## {i:02d}. {specialist.upper()}\n\n")
                f.write(analysis)
                f.write("\n\n---\n\n")

            # Accumulate for context
            previous_analyses += f"\n{specialist.upper()}: {analysis[:500]}..."

            logger.info(f"   ✓ Complete ({len(analysis.split())} words)")

            # Small delay
            time.sleep(0.5)

        # Run final 70B synthesis
        logger.info("\n" + "=" * 40)
        logger.info("RUNNING FINAL 70B SYNTHESIS")
        logger.info("=" * 40)

        if self.use_modelfiles:
            # Use evaluator modelfile
            with open(report_file, 'r') as f:
                full_report = f.read()

            synthesis = self.analyze_with_modelfile("evaluator", full_report)
        else:
            # Use API for 70B
            synthesis = self._run_70b_synthesis(report_file)

        # Append synthesis
        with open(report_file, 'a') as f:
            f.write("\n## FINAL SYNTHESIS (70B)\n\n")
            f.write(synthesis)
            f.write("\n\n---\n\n*Generated by Scripturemon Ultimate Hybrid System*")

        logger.info(f"\n✅ Analysis complete! Report: {report_file}")
        return str(report_file)

    def _run_70b_synthesis(self, report_file: Path) -> str:
        """Run 70B synthesis using API"""
        try:
            from scripturemon_ultimate_system import ScripturemonUltimateSystem
            system = ScripturemonUltimateSystem()

            with open(report_file, 'r') as f:
                screenplay = f.read()

            return system._run_final_evaluation(report_file, screenplay)
        except Exception as e:
            logger.error(f"70B synthesis failed: {e}")
            return "Synthesis failed"

    def test_single_specialist(self, specialist: str, test_text: str = None):
        """Test a single specialist model"""

        if test_text is None:
            test_text = """
FADE IN:
INT. COFFEE SHOP - DAY
SARAH (30s, tired) sits across from JOHN (40s, nervous).

SARAH
We need to talk about what happened.

JOHN
(avoiding eye contact)
There's nothing to talk about.

SARAH
You can't keep running from this, John.
"""

        logger.info(f"Testing {specialist} specialist...")

        if self.use_modelfiles:
            result = self.analyze_with_modelfile(specialist, test_text)
        else:
            result = self.analyze_with_api(specialist, test_text)

        print(f"\n{specialist.upper()} Analysis:")
        print("=" * 40)
        print(result[:500])
        print("..." if len(result) > 500 else "")
        print("=" * 40)

def main():
    """Main function for testing"""
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Test single: python scripturemon_ollama_hybrid.py test [specialist]")
        print("  Full analysis: python scripturemon_ollama_hybrid.py analyze <screenplay_file>")
        print("  Register models: python scripturemon_ollama_hybrid.py register")
        sys.exit(1)

    command = sys.argv[1]

    if command == "test":
        # Test mode
        hybrid = ScripturemonOllamaHybrid(use_modelfiles=True)
        specialist = sys.argv[2] if len(sys.argv) > 2 else "dialogue"
        hybrid.test_single_specialist(specialist)

    elif command == "analyze":
        # Full analysis
        if len(sys.argv) < 3:
            print("Please provide screenplay file")
            sys.exit(1)

        screenplay_file = sys.argv[2]
        hybrid = ScripturemonOllamaHybrid(use_modelfiles=True)
        report = hybrid.run_sequential_analysis(screenplay_file)
        print(f"✅ Report saved: {report}")

    elif command == "register":
        # Register all models
        import os
        os.chdir("modelfiles")
        os.system("./register_models.sh")

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()