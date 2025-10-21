#!/usr/bin/env python3
"""
FULL SYSTEM TEST - Token Turbo + Memórias + Qualidade
"""

import subprocess
import json
import time
import os
from datetime import datetime
import psutil

class SystemTester:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "bugs_found": [],
            "performance": {},
            "quality": {}
        }

    def test_ollama_status(self):
        """Test if Ollama is running"""
        print("🔍 Testing Ollama status...")
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.results["tests"].append({"ollama_status": "✅ Running"})
                return True
            else:
                self.results["bugs_found"].append("❌ Ollama not running properly")
                return False
        except Exception as e:
            self.results["bugs_found"].append(f"❌ Ollama error: {str(e)}")
            return False

    def test_token_turbo_exists(self):
        """Test if Token Turbo model exists"""
        print("🔍 Checking Token Turbo model...")
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if "mixtral-token-turbo:latest" in result.stdout:
                self.results["tests"].append({"token_turbo": "✅ Model exists"})
                return True
            else:
                self.results["bugs_found"].append("❌ Token Turbo model not found")
                return False
        except Exception as e:
            self.results["bugs_found"].append(f"❌ Model check error: {str(e)}")
            return False

    def test_cpu_usage(self):
        """Test CPU usage during inference"""
        print("🔍 Testing CPU usage...")
        test_prompt = "Analyze the hero's journey in 5 words"

        # Start Ollama process
        process = subprocess.Popen(
            ["ollama", "run", "mixtral-token-turbo:latest"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Monitor CPU
        cpu_samples = []
        for _ in range(5):
            cpu_samples.append(psutil.cpu_percent(interval=0.5))

        # Send prompt
        stdout, stderr = process.communicate(input=test_prompt, timeout=30)

        avg_cpu = sum(cpu_samples) / len(cpu_samples)
        self.results["performance"]["avg_cpu"] = f"{avg_cpu:.1f}%"

        if avg_cpu > 5:
            self.results["tests"].append({"cpu_usage": f"✅ CPU used: {avg_cpu:.1f}%"})
            return True
        else:
            self.results["bugs_found"].append(f"⚠️ Low CPU usage: {avg_cpu:.1f}%")
            return False

    def test_memory_system(self):
        """Test memory system integrity"""
        print("🔍 Checking memory system...")
        memory_path = "/Users/clubproducoes/Digimundo/claude_code/memory"

        required_files = [
            "CLAUDE_MEMORY.md",
            "HARMONIA_CERTIFICADO.md",
            "TOKEN_TURBO_CPU_SUCCESS.md",
            "UNIFIED_MEMORY_SYSTEM.py"
        ]

        missing = []
        for file in required_files:
            full_path = os.path.join(memory_path, file)
            if not os.path.exists(full_path):
                missing.append(file)

        if missing:
            self.results["bugs_found"].append(f"❌ Missing memory files: {missing}")
            return False
        else:
            self.results["tests"].append({"memory_system": "✅ All critical files present"})
            return True

    def test_insight_quality(self):
        """Test quality of insights generated"""
        print("🔍 Testing insight quality...")

        test_prompt = """Analyze the inciting incident in The Matrix screenplay.
        Be specific with page numbers and dialogue examples."""

        try:
            result = subprocess.run(
                ["ollama", "run", "mixtral-token-turbo:latest"],
                input=test_prompt,
                capture_output=True,
                text=True,
                timeout=300
            )

            response = result.stdout

            # Quality checks
            quality_metrics = {
                "has_page_numbers": "page" in response.lower(),
                "has_quotes": '"' in response,
                "has_character_names": any(name in response for name in ["Neo", "Morpheus", "Trinity"]),
                "length_adequate": len(response) > 500,
                "structured": any(marker in response for marker in ["1.", "2.", "-", "•"])
            }

            passed = sum(quality_metrics.values())
            total = len(quality_metrics)

            self.results["quality"] = {
                "metrics": quality_metrics,
                "score": f"{passed}/{total}",
                "percentage": f"{(passed/total)*100:.0f}%"
            }

            if passed >= 3:
                self.results["tests"].append({"insight_quality": f"✅ Quality: {passed}/{total}"})
                return True
            else:
                self.results["bugs_found"].append(f"⚠️ Low quality insights: {passed}/{total}")
                return False

        except subprocess.TimeoutExpired:
            self.results["bugs_found"].append("❌ Timeout generating insights")
            return False
        except Exception as e:
            self.results["bugs_found"].append(f"❌ Insight generation error: {str(e)}")
            return False

    def test_checkpoint_system(self):
        """Test if checkpoint system works"""
        print("🔍 Testing checkpoint system...")
        checkpoint_file = "/Users/clubproducoes/Digimundo/scripturemon-ultimate/checkpoint_analysis.json"

        if os.path.exists(checkpoint_file):
            try:
                with open(checkpoint_file, 'r') as f:
                    checkpoint = json.load(f)

                if checkpoint.get("completed_count", 0) > 0:
                    self.results["tests"].append({
                        "checkpoint": f"✅ Checkpoint working ({checkpoint['completed_count']} analyses)"
                    })
                    return True
                else:
                    self.results["bugs_found"].append("⚠️ Checkpoint exists but no analyses completed")
                    return False
            except:
                self.results["bugs_found"].append("❌ Checkpoint file corrupted")
                return False
        else:
            self.results["bugs_found"].append("⚠️ No checkpoint file found")
            return False

    def generate_report(self):
        """Generate final report"""
        print("\n" + "="*60)
        print("📊 FULL SYSTEM TEST REPORT")
        print("="*60)

        # Tests passed
        print(f"\n✅ Tests Passed: {len(self.results['tests'])}")
        for test in self.results["tests"]:
            for key, value in test.items():
                print(f"  {value}")

        # Bugs found
        if self.results["bugs_found"]:
            print(f"\n🐛 Issues Found: {len(self.results['bugs_found'])}")
            for bug in self.results["bugs_found"]:
                print(f"  {bug}")

        # Performance
        if self.results["performance"]:
            print(f"\n⚡ Performance:")
            for key, value in self.results["performance"].items():
                print(f"  {key}: {value}")

        # Quality
        if self.results["quality"]:
            print(f"\n📝 Insight Quality: {self.results['quality']['percentage']}")
            for metric, passed in self.results["quality"]["metrics"].items():
                status = "✅" if passed else "❌"
                print(f"  {status} {metric}")

        # Save to JSON
        report_file = f"system_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📄 Report saved to: {report_file}")

        # Return overall status
        total_tests = 6
        passed = len(self.results["tests"])
        return passed >= 4  # Pass if at least 4/6 tests pass

def main():
    tester = SystemTester()

    print("🚀 Starting Full System Test...")
    print("="*60)

    # Run all tests
    tester.test_ollama_status()
    tester.test_token_turbo_exists()
    tester.test_cpu_usage()
    tester.test_memory_system()
    tester.test_insight_quality()
    tester.test_checkpoint_system()

    # Generate report
    success = tester.generate_report()

    print("\n" + "="*60)
    if success:
        print("✅ SYSTEM TEST PASSED")
    else:
        print("❌ SYSTEM TEST FAILED - Issues need attention")
    print("="*60)

    return 0 if success else 1

if __name__ == "__main__":
    exit(main())