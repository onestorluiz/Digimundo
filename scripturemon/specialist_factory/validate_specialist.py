#!/usr/bin/env python3
"""
Specialist Validator

Validates that a specialist was created correctly following the template.
This script compensates for AI limitations by catching common errors.

Usage:
    python3 validate_specialist.py <specialist_name>

Example:
    python3 validate_specialist.py dialogue
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple


class SpecialistValidator:
    """Validates specialist creation against checklist."""

    def __init__(self, specialist_name: str):
        self.specialist_name = specialist_name
        self.base_dir = Path(__file__).parent.parent
        self.specialist_dir = self.base_dir / "engine" / "specialists" / specialist_name

        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passed_checks: List[str] = []

    def validate(self) -> Tuple[bool, Dict]:
        """Run all validation checks."""
        print(f"\n🔍 Validating Specialist: {self.specialist_name}")
        print("=" * 80)

        # 1. Check files exist
        self._check_files_exist()

        # 2. Check no placeholders left
        self._check_no_placeholders()

        # 3. Check imports work
        self._check_imports()

        # 4. Check paths are relative
        self._check_relative_paths()

        # 5. Check deep context queries
        self._check_deep_context_queries()

        # 6. Check validation criteria
        self._check_validation_criteria()

        # 7. Check class structure
        self._check_class_structure()

        # Print results
        self._print_results()

        # Return summary
        is_valid = len(self.errors) == 0
        return is_valid, {
            "valid": is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "passed": self.passed_checks
        }

    def _check_files_exist(self):
        """Check all required files exist."""
        print("\n📁 Checking files exist...")

        required_files = [
            self.specialist_dir / "specialist.py",
            self.specialist_dir / "prompts.py",
            self.specialist_dir / "README.md",
            self.base_dir / "tests" / f"test_{self.specialist_name}.py",
        ]

        for file_path in required_files:
            if file_path.exists():
                self.passed_checks.append(f"✓ File exists: {file_path.name}")
            else:
                self.errors.append(f"✗ Missing file: {file_path}")

    def _check_no_placeholders(self):
        """Check no template placeholders remain."""
        print("\n🔎 Checking for placeholders...")

        files_to_check = [
            self.specialist_dir / "specialist.py",
            self.specialist_dir / "prompts.py",
            self.specialist_dir / "README.md",
        ]

        placeholder_pattern = re.compile(r'\{\{.*?\}\}')

        for file_path in files_to_check:
            if not file_path.exists():
                continue

            content = file_path.read_text()
            placeholders = placeholder_pattern.findall(content)

            if placeholders:
                self.errors.append(
                    f"✗ Placeholders found in {file_path.name}: {placeholders}"
                )
            else:
                self.passed_checks.append(f"✓ No placeholders in {file_path.name}")

    def _check_imports(self):
        """Check that imports work."""
        print("\n📦 Checking imports...")

        try:
            # Try importing the specialist
            sys.path.insert(0, str(self.base_dir))

            specialist_module = f"engine.specialists.{self.specialist_name}.specialist"
            prompts_module = f"engine.specialists.{self.specialist_name}.prompts"

            try:
                __import__(specialist_module)
                self.passed_checks.append(f"✓ Import works: {specialist_module}")
            except ImportError as e:
                self.errors.append(f"✗ Import failed: {specialist_module} - {e}")

            try:
                __import__(prompts_module)
                self.passed_checks.append(f"✓ Import works: {prompts_module}")
            except ImportError as e:
                self.errors.append(f"✗ Import failed: {prompts_module} - {e}")

        except Exception as e:
            self.errors.append(f"✗ Import test failed: {e}")

    def _check_relative_paths(self):
        """Check no absolute paths hardcoded."""
        print("\n🗂️  Checking for hardcoded paths...")

        specialist_file = self.specialist_dir / "specialist.py"
        if not specialist_file.exists():
            return

        content = specialist_file.read_text()

        # Look for absolute paths (starting with /)
        absolute_path_pattern = re.compile(r'["\'](/Users/|/home/|C:\\)')
        matches = absolute_path_pattern.findall(content)

        if matches:
            self.errors.append(
                f"✗ Absolute paths found in specialist.py: {matches}"
            )
        else:
            self.passed_checks.append("✓ No absolute paths hardcoded")

        # Check for Path(__file__) usage (correct pattern)
        if "Path(__file__)" in content:
            self.passed_checks.append("✓ Uses relative paths (Path(__file__))")
        else:
            self.warnings.append("⚠ Should use Path(__file__) for relative paths")

    def _check_deep_context_queries(self):
        """Check deep context queries are defined."""
        print("\n🔍 Checking deep context queries...")

        prompts_file = self.specialist_dir / "prompts.py"
        if not prompts_file.exists():
            return

        content = prompts_file.read_text()

        if "DEEP_CONTEXT_QUERIES" in content:
            self.passed_checks.append("✓ DEEP_CONTEXT_QUERIES defined")

            # Check it's a list with items
            if "DEEP_CONTEXT_QUERIES = [" in content:
                # Count queries (rough estimate)
                query_count = content.count('",') + content.count('"]')
                if query_count >= 5:
                    self.passed_checks.append(f"✓ Has {query_count} deep context queries")
                else:
                    self.warnings.append(
                        f"⚠ Only {query_count} queries (recommend 5-7)"
                    )
        else:
            self.errors.append("✗ DEEP_CONTEXT_QUERIES not defined in prompts.py")

    def _check_validation_criteria(self):
        """Check validation criteria are defined."""
        print("\n✅ Checking validation criteria...")

        prompts_file = self.specialist_dir / "prompts.py"
        if not prompts_file.exists():
            return

        content = prompts_file.read_text()

        if "VALIDATION_CRITERIA" in content:
            self.passed_checks.append("✓ VALIDATION_CRITERIA defined")

            # Check for key criteria
            expected_criteria = [
                "minimum_length",
                "scenes_analyzed",
                "quotes_included",
                "rewrites_proposed"
            ]

            for criterion in expected_criteria:
                if criterion in content:
                    self.passed_checks.append(f"✓ Has criterion: {criterion}")
                else:
                    self.warnings.append(f"⚠ Missing criterion: {criterion}")
        else:
            self.errors.append("✗ VALIDATION_CRITERIA not defined in prompts.py")

    def _check_class_structure(self):
        """Check specialist class has required methods."""
        print("\n🏗️  Checking class structure...")

        specialist_file = self.specialist_dir / "specialist.py"
        if not specialist_file.exists():
            return

        content = specialist_file.read_text()

        # Required methods
        required_methods = [
            "__init__",
            "analyze_screenplay",
            "_validate_analysis",
        ]

        for method in required_methods:
            if f"def {method}" in content:
                self.passed_checks.append(f"✓ Has method: {method}")
            else:
                self.errors.append(f"✗ Missing method: {method}")

    def _print_results(self):
        """Print validation results."""
        print("\n" + "=" * 80)
        print("📊 VALIDATION RESULTS")
        print("=" * 80)

        if self.passed_checks:
            print(f"\n✅ PASSED ({len(self.passed_checks)} checks):")
            for check in self.passed_checks:
                print(f"   {check}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"   {error}")

        print("\n" + "=" * 80)

        if len(self.errors) == 0:
            print("✅ ✅ ✅  VALIDATION PASSED  ✅ ✅ ✅")
            print("\nSpecialist is ready for testing!")
        else:
            print("❌ ❌ ❌  VALIDATION FAILED  ❌ ❌ ❌")
            print("\nPlease fix all errors before proceeding.")

        print("=" * 80 + "\n")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 validate_specialist.py <specialist_name>")
        print("Example: python3 validate_specialist.py dialogue")
        sys.exit(1)

    specialist_name = sys.argv[1]

    validator = SpecialistValidator(specialist_name)
    is_valid, results = validator.validate()

    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
