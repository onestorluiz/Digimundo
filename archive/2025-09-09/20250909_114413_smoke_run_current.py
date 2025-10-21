#!/usr/bin/env python3
"""
Current smoke tests for Scripturemon CLI
Tests basic functionality with current interfaces
"""

import subprocess
import sys
import tempfile
from pathlib import Path


def run_command(cmd):
    """Run a command and return result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def test_help():
    """Test help command"""
    print("Testing: scripturemon --help")
    success, stdout, stderr = run_command("./bin/scripturemon --help")
    if success and "Scripturemon" in stdout:
        print("✅ Help command works")
        return True
    else:
        print(f"❌ Help command failed: {stderr}")
        return False


def test_status():
    """Test status command"""
    print("\nTesting: scripturemon status")
    success, stdout, stderr = run_command("./bin/scripturemon status")
    if success and "SCRIPTUREMON STATUS" in stdout:
        print("✅ Status command works")
        return True
    else:
        print(f"❌ Status command failed: {stderr}")
        return False


def test_analyze():
    """Test analyze command with a sample file"""
    print("\nTesting: scripturemon analyze")
    
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("INT. QUARTO - NOITE\n\nUm personagem escreve código.\n\nPERSONAGEM\nMais uma noite...\n\nFADE OUT.")
        temp_file = f.name
    
    try:
        success, stdout, stderr = run_command(f"./bin/scripturemon analyze {temp_file}")
        if success and ("Analyzing" in stdout or "Score" in stdout):
            print("✅ Analyze command works")
            return True
        else:
            print(f"❌ Analyze command failed: {stderr}")
            return False
    finally:
        Path(temp_file).unlink(missing_ok=True)


def test_backup():
    """Test backup command"""
    print("\nTesting: scripturemon backup")
    success, stdout, stderr = run_command("./bin/scripturemon backup")
    if success and ("Backup created" in stdout or "backup" in stdout.lower()):
        print("✅ Backup command works")
        return True
    else:
        print(f"❌ Backup command failed: {stderr}")
        return False


def main():
    """Run all smoke tests"""
    print("=" * 60)
    print("SCRIPTUREMON SMOKE TESTS (CURRENT)")
    print("=" * 60)
    
    tests = [
        ("Help", test_help),
        ("Status", test_status),
        ("Analyze", test_analyze),
        ("Backup", test_backup)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {name} test error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())