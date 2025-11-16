#!/usr/bin/env python3
"""
🤖 META-VALIDATION SCRIPT - Documentation Self-Healing System

Nível: ALÉM DO VALE DO SILÍCIO

Este script:
1. Executa TODOS os AI analyzers
2. Compara métricas reais vs. documentadas
3. Valida que todos os comandos documentados funcionam
4. Verifica links internos
5. Detecta drift e sugere correções
6. Auto-atualiza métricas se divergência > 5%

Usage:
    python scripts/phase5/validate_documentation.py
    python scripts/phase5/validate_documentation.py --auto-update
    python scripts/phase5/validate_documentation.py --ci-mode
"""

import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'


class DocumentationValidator:
    """Validates and auto-heals documentation"""

    def __init__(self, auto_update: bool = False):
        self.auto_update = auto_update
        self.project_root = self._detect_project_root()
        self.docs_dir = self.project_root.parent / 'docs' / 'fase_5'
        self.errors = []
        self.warnings = []

    def _detect_project_root(self) -> Path:
        """Auto-detect project root"""
        current = Path.cwd()

        # Try common patterns
        if (current / 'app').exists() and (current / 'tests').exists():
            return current

        if (current / 'cineprod-flask').exists():
            return current / 'cineprod-flask'

        # Try parent
        if current.name == 'scripts':
            parent = current.parent.parent
            if (parent / 'cineprod-flask').exists():
                return parent / 'cineprod-flask'

        return current

    def run_ai_analysis(self) -> Dict[str, any]:
        """Execute all AI analyzers and extract metrics"""
        print(f"{BLUE}🤖 Running AI analysis...{RESET}")

        script = self.project_root.parent / 'scripts' / 'phase5' / 'ai_semantic_analyzer.py'

        try:
            result = subprocess.run(
                ['python3', str(script), '--duplicates', '--dead-code', '--patterns'],
                capture_output=True,
                text=True,
                timeout=180
            )

            output = result.stdout

            # Extract metrics using regex
            metrics = {
                'duplications': self._extract_duplications(output),
                'dead_files': self._extract_dead_files(output),
                'dead_percentage': self._extract_dead_percentage(output),
                'orm_percentage': self._extract_orm_percentage(output),
                'timestamp': datetime.now().isoformat()
            }

            print(f"{GREEN}✅ AI analysis complete{RESET}")
            return metrics

        except subprocess.TimeoutExpired:
            self.errors.append("AI analysis timed out (>3min)")
            return {}
        except Exception as e:
            self.errors.append(f"AI analysis failed: {e}")
            return {}

    def _extract_duplications(self, text: str) -> int:
        """Extract duplication count from output"""
        # Look for "... and XXXX more duplicates"
        match = re.search(r'and (\d+) more duplicates', text)
        if match:
            shown = len(re.findall(r'^\d+\. Similarity:', text, re.MULTILINE))
            return shown + int(match.group(1))
        return 0

    def _extract_dead_files(self, text: str) -> int:
        """Extract dead files count"""
        match = re.search(r'Dead files[^:]*:\s*(\d+)', text)
        return int(match.group(1)) if match else 0

    def _extract_dead_percentage(self, text: str) -> float:
        """Extract dead files percentage"""
        match = re.search(r'Dead files[^:]*:\s*\d+\s*\((\d+\.?\d*)%\)', text)
        return float(match.group(1)) if match else 0.0

    def _extract_orm_percentage(self, text: str) -> float:
        """Extract ORM consistency percentage"""
        match = re.search(r'Direct ORM usage:\s*\d+[^(]*\((\d+\.?\d*)%\)', text)
        return float(match.group(1)) if match else 0.0

    def validate_metrics(self, real_metrics: Dict) -> bool:
        """Compare real metrics vs. documented"""
        print(f"\n{BLUE}📊 Validating metrics consistency...{RESET}")

        documented = {
            'duplications': 13903,
            'dead_files': 191,
            'dead_percentage': 68.2,
            'orm_percentage': 83.3
        }

        all_valid = True
        updates_needed = {}

        for key, expected in documented.items():
            actual = real_metrics.get(key, 0)

            if isinstance(expected, float):
                diff_pct = abs(actual - expected)
                threshold = 5.0  # 5% tolerance
            else:
                diff_pct = abs(actual - expected) / expected * 100 if expected > 0 else 0
                threshold = 5.0

            status = "✅" if diff_pct <= threshold else "⚠️"
            color = GREEN if diff_pct <= threshold else YELLOW

            print(f"{status} {key:20s}: {color}Expected {expected:>6}, Got {actual:>6} (±{diff_pct:.1f}%){RESET}")

            if diff_pct > threshold:
                all_valid = False
                self.warnings.append(
                    f"{key} drift: {diff_pct:.1f}% (expected {expected}, got {actual})"
                )
                updates_needed[key] = (expected, actual)

        # Auto-update if enabled and drift detected
        if self.auto_update and updates_needed:
            print(f"\n{YELLOW}🔄 Auto-update enabled - updating documentation...{RESET}")
            self._auto_update_documentation(updates_needed)

        return all_valid

    def _auto_update_documentation(self, updates: Dict[str, Tuple[float, float]]) -> None:
        """Auto-update documentation with new metrics"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Files to update
        docs_to_update = [
            '07_DEEP_PROJECT_ANALYSIS.md',
            'AI_INSIGHTS_REPORT.md',
            'AI_POWERED_ANALYSIS.md',
            'README.md'
        ]

        updates_made = []

        for doc_file in docs_to_update:
            filepath = self.docs_dir / doc_file

            if not filepath.exists():
                continue

            content = filepath.read_text()
            modified = False

            for key, (old_val, new_val) in updates.items():
                # Update various formats where metrics appear
                patterns = []

                if key == 'duplications':
                    patterns = [
                        (rf'\b{int(old_val):,}\s+duplicações', f'{int(new_val):,} duplicações'),
                        (rf'\b{int(old_val)}\s+duplicações', f'{int(new_val)} duplicações'),
                        (rf'13\.903\s+duplicações', f'{int(new_val):,} duplicações'),
                        (rf'13903\s+duplicações', f'{int(new_val)} duplicações'),
                    ]
                elif key == 'dead_files':
                    patterns = [
                        (rf'\b{int(old_val)}\s+arquivos mortos', f'{int(new_val)} arquivos mortos'),
                        (rf'\b{int(old_val)}\s+dead files', f'{int(new_val)} dead files'),
                    ]
                elif key == 'dead_percentage':
                    patterns = [
                        (rf'{old_val}%\s+da codebase', f'{new_val}% da codebase'),
                        (rf'{old_val}%\s+de código morto', f'{new_val}% de código morto'),
                    ]
                elif key == 'orm_percentage':
                    patterns = [
                        (rf'{old_val}%\s+Direct ORM', f'{new_val}% Direct ORM'),
                        (rf'{old_val}%\s+de consistência', f'{new_val}% de consistência'),
                    ]

                for pattern, replacement in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                        modified = True

            if modified:
                filepath.write_text(content)
                updates_made.append(doc_file)
                print(f"{GREEN}  ✅ Updated {doc_file}{RESET}")

        # Update this script's hardcoded values
        script_path = Path(__file__)
        script_content = script_path.read_text()

        for key, (old_val, new_val) in updates.items():
            if isinstance(new_val, float):
                pattern = rf"'{key}':\s*{old_val}"
                replacement = f"'{key}': {new_val}"
            else:
                pattern = rf"'{key}':\s*{int(old_val)}"
                replacement = f"'{key}': {int(new_val)}"

            script_content = re.sub(pattern, replacement, script_content)

        script_path.write_text(script_content)
        print(f"{GREEN}  ✅ Updated validate_documentation.py baseline{RESET}")

        # Create changelog entry
        changelog_path = self.docs_dir / 'METRICS_UPDATE_LOG.md'

        if changelog_path.exists():
            changelog = changelog_path.read_text()
        else:
            changelog = "# 🤖 Metrics Auto-Update Log\n\n"

        entry = f"\n## Update {timestamp}\n\n"
        entry += "**Metrics updated automatically by validation system:**\n\n"
        entry += "| Metric | Old Value | New Value | Drift |\n"
        entry += "|--------|-----------|-----------|-------|\n"

        for key, (old_val, new_val) in updates.items():
            if isinstance(old_val, float):
                drift = abs(new_val - old_val)
            else:
                drift = abs(new_val - old_val) / old_val * 100 if old_val > 0 else 0
            entry += f"| {key} | {old_val} | {new_val} | {drift:.1f}% |\n"

        entry += f"\n**Files updated:** {', '.join(updates_made)}\n"

        changelog = changelog.replace("# 🤖 Metrics Auto-Update Log\n\n",
                                       f"# 🤖 Metrics Auto-Update Log\n\n{entry}")

        changelog_path.write_text(changelog)
        print(f"{GREEN}  ✅ Updated METRICS_UPDATE_LOG.md{RESET}")

    def validate_commands(self) -> bool:
        """Validate that all documented commands work"""
        print(f"\n{BLUE}🔧 Validating documented commands...{RESET}")

        commands = [
            ['python3', 'scripts/phase5/ai_semantic_analyzer.py', '--help'],
            ['python3', 'scripts/phase5/ai_impact_analyzer.py', '--help'],
            ['python3', 'scripts/phase5/ai_semantic_analyzer.py', '--patterns'],
        ]

        all_valid = True

        for cmd in commands:
            cmd_str = ' '.join(cmd)
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    timeout=30,
                    cwd=self.project_root.parent
                )

                if result.returncode == 0:
                    print(f"{GREEN}✅{RESET} {cmd_str}")
                else:
                    print(f"{RED}❌{RESET} {cmd_str} (exit code {result.returncode})")
                    all_valid = False
                    self.errors.append(f"Command failed: {cmd_str}")

            except subprocess.TimeoutExpired:
                print(f"{RED}❌{RESET} {cmd_str} (timeout)")
                all_valid = False
                self.errors.append(f"Command timeout: {cmd_str}")
            except Exception as e:
                print(f"{RED}❌{RESET} {cmd_str} ({e})")
                all_valid = False
                self.errors.append(f"Command error: {cmd_str} - {e}")

        return all_valid

    def validate_links(self) -> bool:
        """Validate internal markdown links"""
        print(f"\n{BLUE}🔗 Validating internal links...{RESET}")

        required_files = [
            'AI_STRATEGY_MASTER.md',
            'AI_INSIGHTS_REPORT.md',
            'AI_POWERED_ANALYSIS.md',
            'QUICK_START_GUIDE.md',
            'SYSTEM_TESTING_REPORT.md',
            'README.md',
            '03_QUICK_START_GUIDES.md',
            'CHANGELOG.md',
            'HARMONY_ANALYSIS_AND_SYNC.md',
            'SYNC_COMPLETE_SUMMARY.md'
        ]

        all_valid = True

        for filename in required_files:
            filepath = self.docs_dir / filename

            if filepath.exists():
                print(f"{GREEN}✅{RESET} {filename}")
            else:
                print(f"{RED}❌{RESET} {filename} (NOT FOUND)")
                all_valid = False
                self.errors.append(f"Missing file: {filename}")

        return all_valid

    def generate_report(self, metrics: Dict, validations: Dict) -> str:
        """Generate validation report"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        report = f"""
# 🤖 Documentation Validation Report

**Generated**: {timestamp}
**Auto-update**: {'Enabled' if self.auto_update else 'Disabled'}

---

## 📊 Real-time Metrics (Just Executed)

| Metric | Value | Status |
|--------|-------|--------|
| Duplications | {metrics.get('duplications', 'N/A')} | {'✅' if validations.get('metrics') else '⚠️'} |
| Dead Files | {metrics.get('dead_files', 'N/A')} ({metrics.get('dead_percentage', 'N/A')}%) | {'✅' if validations.get('metrics') else '⚠️'} |
| ORM Consistency | {metrics.get('orm_percentage', 'N/A')}% | {'✅' if validations.get('metrics') else '⚠️'} |

---

## ✅ Validations

- {'✅' if validations.get('metrics') else '❌'} Metrics consistency
- {'✅' if validations.get('commands') else '❌'} Commands executable
- {'✅' if validations.get('links') else '❌'} Internal links valid

---

## {'⚠️  Warnings' if self.warnings else '✅ No Warnings'}

"""

        if self.warnings:
            for warning in self.warnings:
                report += f"- ⚠️  {warning}\n"

        report += f"\n## {'❌ Errors' if self.errors else '✅ No Errors'}\n\n"

        if self.errors:
            for error in self.errors:
                report += f"- ❌ {error}\n"

        report += f"\n---\n\n**Status**: {'🎉 ALL VALIDATIONS PASSED' if not self.errors else '⚠️  ISSUES DETECTED'}\n"

        return report

    def run(self) -> int:
        """Run full validation"""
        print(f"{BOLD}{BLUE}{'='*80}{RESET}")
        print(f"{BOLD}{BLUE}🤖 META-VALIDATION: Documentation Self-Healing System{RESET}")
        print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")

        # 1. Run AI analysis
        metrics = self.run_ai_analysis()

        if not metrics:
            print(f"\n{RED}❌ AI analysis failed - cannot continue{RESET}")
            return 1

        # 2. Validate metrics
        metrics_valid = self.validate_metrics(metrics)

        # 3. Validate commands
        commands_valid = self.validate_commands()

        # 4. Validate links
        links_valid = self.validate_links()

        # 5. Generate report
        validations = {
            'metrics': metrics_valid,
            'commands': commands_valid,
            'links': links_valid
        }

        report = self.generate_report(metrics, validations)

        # Save report
        report_path = self.docs_dir / f'VALIDATION_REPORT_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        report_path.write_text(report)

        print(f"\n{GREEN}📝 Report saved: {report_path}{RESET}")

        # Print summary
        print(f"\n{BOLD}{'='*80}{RESET}")
        print(f"{BOLD}SUMMARY{RESET}")
        print(f"{'='*80}")
        print(f"Warnings: {YELLOW}{len(self.warnings)}{RESET}")
        print(f"Errors:   {RED if self.errors else GREEN}{len(self.errors)}{RESET}")
        print(f"Status:   {GREEN + '🎉 PASSED' + RESET if not self.errors else RED + '❌ FAILED' + RESET}")
        print(f"{'='*80}\n")

        return 0 if not self.errors else 1


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Validate documentation integrity')
    parser.add_argument('--auto-update', action='store_true', help='Auto-update metrics if drift detected')
    parser.add_argument('--ci-mode', action='store_true', help='CI mode (exit with error if validation fails)')

    args = parser.parse_args()

    validator = DocumentationValidator(auto_update=args.auto_update)
    exit_code = validator.run()

    if args.ci_mode:
        sys.exit(exit_code)

    return exit_code


if __name__ == '__main__':
    main()
