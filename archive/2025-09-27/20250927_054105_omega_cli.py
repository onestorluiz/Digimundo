#!/usr/bin/env python3
"""
OMEGA-ASCENT CLI Interface v4.0.0
"""

import argparse
import sys
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Scripturemon OMEGA-ASCENT v4.0.0 - Advanced Screenplay Analysis"
    )

    parser.add_argument(
        "script",
        help="Path to screenplay file"
    )

    parser.add_argument(
        "--mode",
        choices=["full", "fast", "debug"],
        default="full",
        help="Processing mode"
    )

    parser.add_argument(
        "--output",
        default="output",
        help="Output directory"
    )

    parser.add_argument(
        "--features",
        nargs="+",
        default=["all"],
        help="Features to enable"
    )

    parser.add_argument(
        "--config",
        help="Custom configuration file"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )

    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run benchmarks"
    )

    args = parser.parse_args()

    # Import system components
    try:
        from core.engine import OmegaEngine
        from config.loader import ConfigLoader

        # Load configuration
        config = ConfigLoader.load(args.config) if args.config else ConfigLoader.default()

        # Initialize engine
        engine = OmegaEngine(config, verbose=args.verbose)

        # Process screenplay
        result = engine.process(
            script_path=args.script,
            mode=args.mode,
            features=args.features,
            output_dir=args.output
        )

        # Save results
        output_path = Path(args.output) / "omega_results.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2))

        print(f"✅ Analysis complete! Results saved to {output_path}")

        if args.benchmark:
            print("\n📊 Benchmarks:")
            for metric, value in result.get("metrics", {}).items():
                print(f"  {metric}: {value}")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
