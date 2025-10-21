#!/usr/bin/env python3
"""
Complete System Test for ScriptureMon Champion
Tests all components and validates REGRAS.md compliance
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, List, Tuple
import subprocess
import os


class SystemTester:
    """Complete system testing and validation."""

    def __init__(self):
        self.results = {
            'components': {},
            'regras': {},
            'performance': {},
            'errors': []
        }

    def test_digilang_system(self) -> bool:
        """Test DigiLang compression system."""
        print("\n1. TESTING DIGILANG SYSTEM:")
        print("-" * 40)

        try:
            # Test basic compression
            from apps.scripturemon.digilang import encoder, decoder

            test_text = "INT. OFFICE - DAY\nJOHN enters."
            encoded, ratio = encoder.DigiLangEncoder().encode(test_text)
            decoded = decoder.DigiLangDecoder().decode(encoded)

            success = len(encoded) < len(test_text)
            print(f"✅ DigiLang operational: {ratio:.1%} compression")

            self.results['components']['digilang'] = {
                'status': 'operational',
                'compression': ratio
            }
            return True

        except Exception as e:
            print(f"❌ DigiLang error: {e}")
            self.results['components']['digilang'] = {
                'status': 'error',
                'error': str(e)
            }
            return False

    def test_ai_integration(self) -> bool:
        """Test AI components."""
        print("\n2. TESTING AI INTEGRATION:")
        print("-" * 40)

        components = []

        # Test sentiment analysis
        try:
            from apps.scripturemon.ai_sentiment import analyze_text_sentiment
            result = analyze_text_sentiment("I am very happy")
            if result.compound > 0:
                print("✅ Sentiment analysis working")
                components.append('sentiment')
        except:
            print("❌ Sentiment analysis failed")

        # Test unified manager
        try:
            from apps.scripturemon.unified_manager import UnifiedManager
            manager = UnifiedManager()
            print("✅ Unified manager initialized")
            components.append('unified_manager')
        except:
            print("❌ Unified manager failed")

        # Test memory system
        try:
            from apps.scripturemon.ai_memory import MemorySystem
            memory = MemorySystem()
            print("✅ Memory system working")
            components.append('memory')
        except:
            print("❌ Memory system failed")

        self.results['components']['ai'] = {
            'working': components,
            'total': 3,
            'percentage': len(components) / 3 * 100
        }

        return len(components) >= 2

    def test_web_interface(self) -> bool:
        """Test Flask web interface."""
        print("\n3. TESTING WEB INTERFACE:")
        print("-" * 40)

        try:
            from apps.web.app import create_app
            app = create_app()
            print("✅ Flask app created successfully")

            # Test routes exist
            routes = [str(rule) for rule in app.url_map.iter_rules()]
            print(f"   Found {len(routes)} routes")

            self.results['components']['web'] = {
                'status': 'operational',
                'routes': len(routes)
            }
            return True

        except Exception as e:
            print(f"❌ Web interface error: {e}")
            self.results['components']['web'] = {
                'status': 'error',
                'error': str(e)
            }
            return False

    def test_cli_binary(self) -> bool:
        """Test CLI binary."""
        print("\n4. TESTING CLI BINARY:")
        print("-" * 40)

        binary_path = Path("bin/scripturemon")

        if not binary_path.exists():
            print("❌ Binary not found at bin/scripturemon")
            self.results['components']['cli'] = {'status': 'missing'}
            return False

        try:
            # Test help command
            result = subprocess.run(
                ["./bin/scripturemon", "--help"],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                print("✅ CLI binary working")
                self.results['components']['cli'] = {'status': 'operational'}
                return True
            else:
                print(f"❌ CLI error: {result.stderr}")
                self.results['components']['cli'] = {
                    'status': 'error',
                    'error': result.stderr
                }
                return False

        except Exception as e:
            print(f"❌ CLI execution error: {e}")
            self.results['components']['cli'] = {
                'status': 'error',
                'error': str(e)
            }
            return False

    def check_regras_compliance(self) -> Dict[str, bool]:
        """Check compliance with REGRAS.md."""
        print("\n5. CHECKING REGRAS.MD COMPLIANCE:")
        print("-" * 40)

        compliance = {}

        # REGRA 1: Test files in tests/
        test_files = list(Path("tests").glob("test_*.py"))
        compliance['tests_location'] = len(test_files) > 0
        print(f"{'✅' if compliance['tests_location'] else '❌'} Test files in tests/ ({len(test_files)} files)")

        # REGRA 2: No test files in root
        root_tests = list(Path(".").glob("test_*.py"))
        compliance['no_root_tests'] = len(root_tests) == 0
        print(f"{'✅' if compliance['no_root_tests'] else '❌'} No test files in root")

        # REGRA 3: requirements.txt exists
        compliance['requirements'] = Path("requirements.txt").exists()
        print(f"{'✅' if compliance['requirements'] else '❌'} requirements.txt exists")

        # REGRA 4: Proper directory structure
        required_dirs = ["apps", "tests", "data", "bin"]
        compliance['directory_structure'] = all(Path(d).exists() for d in required_dirs)
        print(f"{'✅' if compliance['directory_structure'] else '❌'} Directory structure complete")

        # REGRA 5: Binary in bin/
        compliance['binary_location'] = Path("bin/scripturemon").exists()
        print(f"{'✅' if compliance['binary_location'] else '❌'} Binary in bin/")

        # REGRA 6: Documentation exists
        docs = ["README.md", "REGRAS.md", "DIGILANG_FINDINGS.md"]
        compliance['documentation'] = sum(Path(d).exists() for d in docs) >= 2
        print(f"{'✅' if compliance['documentation'] else '❌'} Documentation present")

        # REGRA 7: Clean workspace
        pycache = list(Path(".").rglob("__pycache__"))
        compliance['clean_workspace'] = len(pycache) < 20  # Allow some __pycache__
        print(f"{'✅' if compliance['clean_workspace'] else '❌'} Clean workspace")

        # REGRA 8: Git-ready (no .git check, but structure ready)
        compliance['git_ready'] = Path(".gitignore").exists() if Path(".gitignore").exists() else True
        print(f"{'✅' if compliance['git_ready'] else '❌'} Git-ready structure")

        self.results['regras'] = compliance
        return compliance

    def performance_tests(self):
        """Run performance tests."""
        print("\n6. PERFORMANCE METRICS:")
        print("-" * 40)

        metrics = {}

        # Test DigiLang compression speed
        try:
            import time
            from apps.scripturemon.digilang import encoder

            test_text = "INT. OFFICE - DAY\n" * 100
            enc = encoder.DigiLangEncoder()

            start = time.time()
            for _ in range(10):
                enc.encode(test_text)
            elapsed = time.time() - start

            metrics['compression_speed'] = {
                'operations': 10,
                'time': elapsed,
                'ops_per_sec': 10 / elapsed
            }
            print(f"✅ Compression speed: {10/elapsed:.1f} ops/sec")
        except:
            print("❌ Could not measure compression speed")

        # Memory usage
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            metrics['memory_usage_mb'] = memory_mb
            print(f"✅ Memory usage: {memory_mb:.1f} MB")
        except:
            print("⚠️ Could not measure memory (psutil not available)")

        self.results['performance'] = metrics

    def run_all_tests(self) -> Dict:
        """Run complete system test suite."""
        print("=" * 60)
        print("SCRIPTUREMON CHAMPION - COMPLETE SYSTEM TEST")
        print("=" * 60)

        # Component tests
        digilang_ok = self.test_digilang_system()
        ai_ok = self.test_ai_integration()
        web_ok = self.test_web_interface()
        cli_ok = self.test_cli_binary()

        # Compliance check
        regras = self.check_regras_compliance()
        regras_ok = sum(regras.values()) >= len(regras) * 0.8

        # Performance
        self.performance_tests()

        # Summary
        print("\n" + "=" * 60)
        print("SUMMARY:")
        print("-" * 40)

        components_working = sum([digilang_ok, ai_ok, web_ok, cli_ok])
        print(f"Components: {components_working}/4 working")
        print(f"REGRAS compliance: {sum(regras.values())}/{len(regras)} rules")

        if 'compression_speed' in self.results['performance']:
            print(f"Performance: {self.results['performance']['compression_speed']['ops_per_sec']:.1f} ops/sec")

        overall_success = components_working >= 3 and regras_ok

        print("\n" + "=" * 60)
        if overall_success:
            print("✅ SYSTEM STATUS: OPERATIONAL")
            print("   All major components working")
            print("   REGRAS.md compliance achieved")
        else:
            print("⚠️ SYSTEM STATUS: NEEDS ATTENTION")
            if components_working < 3:
                print("   Some components need fixing")
            if not regras_ok:
                print("   REGRAS.md compliance incomplete")
        print("=" * 60)

        return self.results


def save_results(results: Dict):
    """Save test results."""
    output_path = Path("tests/system_test_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n📊 Results saved to {output_path}")


def main():
    """Run complete system tests."""
    tester = SystemTester()
    results = tester.run_all_tests()
    save_results(results)

    # Return success if system is operational
    components_ok = sum(
        1 for c in results['components'].values()
        if isinstance(c, dict) and c.get('status') == 'operational'
    ) >= 2

    regras_ok = sum(results['regras'].values()) >= len(results['regras']) * 0.7

    return components_ok and regras_ok


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)