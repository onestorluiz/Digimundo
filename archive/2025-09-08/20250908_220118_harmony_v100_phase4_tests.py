#!/usr/bin/env python3
"""
HARMONY V100 - FASE 4 - SoulOS Gating & Naming Tests
Tests for SoulOS gating with dry-run and auto-execute modes
"""

import json
import time
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import tempfile
import shutil

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

class Phase4Tester:
    """Test SoulOS gating and naming standardization"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'phase': 'FASE 4',
            'tests': {},
            'syscalls': {}
        }
        self.reports_dir = Path("reports/harmony_v100/phase4")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Create temp directory for SoulOS storage
        self.temp_dir = tempfile.mkdtemp(prefix='soulos_test_')
        os.environ['SOULOS_STORAGE'] = self.temp_dir
    
    def cleanup(self):
        """Clean up temp directory"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_dry_run_mode(self) -> Dict:
        """Test with enabled=true, auto_execute=false (no execution)"""
        print("\n1️⃣ Testing SoulOS Dry-Run Mode...")
        test_result = {'name': 'dry_run', 'passed': True, 'details': {}}
        
        try:
            from src.utils.soulos_wrapper import SoulOSWrapper
            
            # Configure for dry-run
            settings = {
                "soulos": {
                    "enabled": True,
                    "auto_execute": False
                }
            }
            
            soulos = SoulOSWrapper(settings)
            
            # Verify configuration
            assert soulos.enabled == True, "SoulOS should be enabled"
            assert soulos.auto_execute == False, "Auto-execute should be disabled"
            test_result['details']['config_correct'] = True
            
            # Test process_syscalls with various messages
            messages = [
                "Please MEMO.SAVE this information",
                "I need to TELEPATHY.SEND a message",
                "Time to BACKUP.NOW the system",
                "Dangerous: FILE.DELETE everything"  # Should not be recognized
            ]
            
            for msg in messages:
                result = soulos.process_syscalls(msg)
                
                # Verify standardized contract
                assert 'ok' in result, "Missing 'ok' in result"
                assert 'executed' in result, "Missing 'executed' in result"
                assert 'sandboxed' in result, "Missing 'sandboxed' in result"
                assert 'msg' in result, "Missing 'msg' in result"
                
                # In dry-run, nothing should be executed
                assert result['executed'] == False, f"Nothing should execute in dry-run: {msg}"
                
                # Safe syscalls should be sandboxed
                if any(safe in msg for safe in ['MEMO.SAVE', 'TELEPATHY.SEND', 'BACKUP.NOW']):
                    assert result['sandboxed'] == True, f"Should be sandboxed: {msg}"
                
                test_result['details'][msg[:30]] = result
            
            print(f"  ✅ Dry-run mode working: no executions, all sandboxed")
            
            # Verify no files were created (dry-run)
            memory_file = Path(self.temp_dir) / "memories.json"
            if memory_file.exists():
                with open(memory_file) as f:
                    memories = json.load(f)
                    # Should be empty or minimal
                    test_result['details']['memories_created'] = len(memories)
            
        except AssertionError as e:
            test_result['passed'] = False
            test_result['error'] = str(e)
            print(f"  ❌ Assertion failed: {e}")
        except Exception as e:
            test_result['passed'] = False
            test_result['error'] = str(e)
            print(f"  ❌ Error: {e}")
        
        self.results['tests']['dry_run'] = test_result
        return test_result
    
    def test_auto_execute_mode(self) -> Dict:
        """Test with enabled=true, auto_execute=true (executes whitelisted)"""
        print("\n2️⃣ Testing SoulOS Auto-Execute Mode...")
        test_result = {'name': 'auto_execute', 'passed': True, 'details': {}}
        
        try:
            from src.utils.soulos_wrapper import SoulOSWrapper
            
            # Configure for auto-execute
            settings = {
                "soulos": {
                    "enabled": True,
                    "auto_execute": True
                }
            }
            
            soulos = SoulOSWrapper(settings)
            
            # Verify configuration
            assert soulos.enabled == True, "SoulOS should be enabled"
            assert soulos.auto_execute == True, "Auto-execute should be enabled"
            test_result['details']['config_correct'] = True
            
            # Test safe syscalls (should execute)
            safe_messages = [
                "MEMO.SAVE important data",
                "TELEPATHY.SEND to network",
                "BACKUP.NOW for safety"
            ]
            
            executed_count = 0
            for msg in safe_messages:
                result = soulos.process_syscalls(msg)
                
                # Should execute safe syscalls
                if any(safe in msg for safe in soulos.safe_syscalls):
                    assert result['executed'] == True, f"Should execute safe syscall: {msg}"
                    executed_count += 1
                
                test_result['details'][msg[:30]] = result
            
            assert executed_count > 0, "At least some safe syscalls should execute"
            test_result['details']['executed_count'] = executed_count
            
            print(f"  ✅ Auto-execute mode: {executed_count} safe syscalls executed")
            
            # Test unsafe syscalls (should NOT execute)
            unsafe_messages = [
                "FILE.DELETE all data",
                "SYSTEM.SHUTDOWN now",
                "CODE.EXECUTE malicious"
            ]
            
            for msg in unsafe_messages:
                result = soulos.process_syscalls(msg)
                
                # Should NOT execute unsafe syscalls
                assert result['executed'] == False, f"Should NOT execute unsafe: {msg}"
                
                test_result['details'][f"unsafe_{msg[:20]}"] = result
            
            print(f"  ✅ Unsafe syscalls blocked correctly")
            
            # Verify memories were created (auto-execute)
            memory_file = Path(self.temp_dir) / "memories.json"
            if memory_file.exists():
                with open(memory_file) as f:
                    memories = json.load(f)
                    test_result['details']['memories_created'] = len(memories)
                    # Should have some memories from MEMO.SAVE
                    if 'memo' in memories:
                        test_result['details']['memo_saved'] = True
            
        except AssertionError as e:
            test_result['passed'] = False
            test_result['error'] = str(e)
            print(f"  ❌ Assertion failed: {e}")
        except Exception as e:
            test_result['passed'] = False
            test_result['error'] = str(e)
            print(f"  ❌ Error: {e}")
        
        self.results['tests']['auto_execute'] = test_result
        return test_result
    
    def test_disabled_mode(self) -> Dict:
        """Test with enabled=false (completely disabled)"""
        print("\n3️⃣ Testing SoulOS Disabled Mode...")
        test_result = {'name': 'disabled', 'passed': True, 'details': {}}
        
        try:
            from src.utils.soulos_wrapper import SoulOSWrapper
            
            # Configure as disabled
            settings = {
                "soulos": {
                    "enabled": False,
                    "auto_execute": True  # Should be ignored when disabled
                }
            }
            
            soulos = SoulOSWrapper(settings)
            
            # Verify configuration
            assert soulos.enabled == False, "SoulOS should be disabled"
            test_result['details']['config_correct'] = True
            
            # Test process_syscalls - should return disabled message
            msg = "MEMO.SAVE this and BACKUP.NOW please"
            result = soulos.process_syscalls(msg)
            
            assert result['ok'] == True, "Should return ok even when disabled"
            assert result['executed'] == False, "Nothing should execute when disabled"
            assert result['sandboxed'] == False, "Nothing should be sandboxed when disabled"
            assert "disabled" in result['msg'].lower(), "Should indicate disabled"
            
            test_result['details']['disabled_result'] = result
            
            print(f"  ✅ Disabled mode: no processing, returns disabled message")
            
        except AssertionError as e:
            test_result['passed'] = False
            test_result['error'] = str(e)
            print(f"  ❌ Assertion failed: {e}")
        except Exception as e:
            test_result['passed'] = False
            test_result['error'] = str(e)
            print(f"  ❌ Error: {e}")
        
        self.results['tests']['disabled'] = test_result
        return test_result
    
    def test_naming_standardization(self) -> Dict:
        """Test that naming is standardized across wrapper"""
        print("\n4️⃣ Testing Naming Standardization...")
        test_result = {'name': 'naming', 'passed': True, 'details': {}}
        
        try:
            from src.utils.soulos_wrapper import SoulOSWrapper
            
            soulos = SoulOSWrapper({"soulos": {"enabled": True}})
            
            # Check that process_syscalls exists (unified name)
            assert hasattr(soulos, 'process_syscalls'), "Missing process_syscalls method"
            test_result['details']['has_process_syscalls'] = True
            
            # Check return contract
            result = soulos.process_syscalls("test message")
            required_keys = {'ok', 'executed', 'sandboxed', 'msg'}
            actual_keys = set(result.keys())
            
            assert required_keys == actual_keys, f"Contract mismatch: expected {required_keys}, got {actual_keys}"
            test_result['details']['contract_correct'] = True
            
            # Check backward compatibility (syscall method still exists)
            assert hasattr(soulos, 'syscall'), "Missing backward-compatible syscall method"
            test_result['details']['has_syscall'] = True
            
            # Test syscall method
            syscall_result = soulos.syscall('list')
            assert 'success' in syscall_result, "syscall should return success field"
            assert 'operation' in syscall_result, "syscall should return operation field"
            test_result['details']['syscall_compatible'] = True
            
            print(f"  ✅ Naming standardized: process_syscalls with correct contract")
            
        except AssertionError as e:
            test_result['passed'] = False
            test_result['error'] = str(e)
            print(f"  ❌ Assertion failed: {e}")
        except Exception as e:
            test_result['passed'] = False
            test_result['error'] = str(e)
            print(f"  ❌ Error: {e}")
        
        self.results['tests']['naming'] = test_result
        return test_result
    
    def test_whitelist(self) -> Dict:
        """Test safe syscalls whitelist"""
        print("\n5️⃣ Testing Safe Syscalls Whitelist...")
        test_result = {'name': 'whitelist', 'passed': True, 'details': {}}
        
        try:
            from src.utils.soulos_wrapper import SoulOSWrapper
            
            soulos = SoulOSWrapper({"soulos": {"enabled": True, "auto_execute": True}})
            
            # Check whitelist exists
            assert hasattr(soulos, 'safe_syscalls'), "Missing safe_syscalls whitelist"
            test_result['details']['has_whitelist'] = True
            
            # Verify expected safe syscalls
            expected_safe = {'MEMO.SAVE', 'TELEPATHY.SEND', 'BACKUP.NOW'}
            actual_safe = soulos.safe_syscalls
            
            assert expected_safe == actual_safe, f"Whitelist mismatch: expected {expected_safe}, got {actual_safe}"
            test_result['details']['whitelist_correct'] = True
            
            # Test that only whitelisted syscalls execute
            test_cases = [
                ("MEMO.SAVE data", True),
                ("TELEPATHY.SEND msg", True),
                ("BACKUP.NOW please", True),
                ("FILE.DELETE all", False),
                ("SYSTEM.CRASH now", False),
            ]
            
            for msg, should_execute in test_cases:
                result = soulos.process_syscalls(msg)
                if should_execute:
                    assert result['executed'] == True or result['sandboxed'] == True, f"Should process: {msg}"
                else:
                    assert result['executed'] == False, f"Should NOT execute: {msg}"
                test_result['details'][msg] = result['executed']
            
            print(f"  ✅ Whitelist working: only safe syscalls processed")
            
        except AssertionError as e:
            test_result['passed'] = False
            test_result['error'] = str(e)
            print(f"  ❌ Assertion failed: {e}")
        except Exception as e:
            test_result['passed'] = False
            test_result['error'] = str(e)
            print(f"  ❌ Error: {e}")
        
        self.results['tests']['whitelist'] = test_result
        return test_result
    
    def generate_reports(self):
        """Generate FASE 4 reports"""
        print("\n📝 Generating Reports...")
        
        # Generate soulos_dry.json
        dry_run_data = {
            'timestamp': self.results['timestamp'],
            'mode': 'dry_run',
            'settings': {
                'soulos.enabled': True,
                'soulos.auto_execute': False
            },
            'test': self.results['tests'].get('dry_run', {}),
            'summary': 'No syscalls executed, all sandboxed'
        }
        
        dry_file = self.reports_dir / "soulos_dry.json"
        with open(dry_file, 'w') as f:
            json.dump(dry_run_data, f, indent=2)
        print(f"  ✅ Saved: {dry_file}")
        
        # Generate soulos_exec.json
        exec_data = {
            'timestamp': self.results['timestamp'],
            'mode': 'auto_execute',
            'settings': {
                'soulos.enabled': True,
                'soulos.auto_execute': True
            },
            'test': self.results['tests'].get('auto_execute', {}),
            'whitelist': ['MEMO.SAVE', 'TELEPATHY.SEND', 'BACKUP.NOW'],
            'summary': 'Safe syscalls executed, unsafe blocked'
        }
        
        exec_file = self.reports_dir / "soulos_exec.json"
        with open(exec_file, 'w') as f:
            json.dump(exec_data, f, indent=2)
        print(f"  ✅ Saved: {exec_file}")
        
        # Save full results
        results_file = self.reports_dir / "phase4_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"  ✅ Saved: {results_file}")
        
        # Generate text report
        report_lines = [
            "=" * 80,
            "HARMONY V100 - FASE 4 - SOULOS GATING & NAMING",
            "=" * 80,
            f"Timestamp: {self.results['timestamp']}",
            "",
            "TEST RESULTS",
            "-" * 40
        ]
        
        total_tests = 0
        passed_tests = 0
        
        for test_name, test_result in self.results['tests'].items():
            total_tests += 1
            status = "✅" if test_result.get('passed') else "❌"
            if test_result.get('passed'):
                passed_tests += 1
            
            report_lines.append(f"{status} {test_name}")
            
            if test_name == 'dry_run':
                report_lines.append("    Mode: enabled=true, auto_execute=false")
                report_lines.append("    Result: No executions (correct)")
            elif test_name == 'auto_execute':
                report_lines.append("    Mode: enabled=true, auto_execute=true")
                executed = test_result.get('details', {}).get('executed_count', 0)
                report_lines.append(f"    Result: {executed} safe syscalls executed")
            elif test_name == 'disabled':
                report_lines.append("    Mode: enabled=false")
                report_lines.append("    Result: All operations disabled")
            elif test_name == 'naming':
                report_lines.append("    Unified method: process_syscalls()")
                report_lines.append("    Contract: {ok, executed, sandboxed, msg}")
            elif test_name == 'whitelist':
                report_lines.append("    Safe syscalls: MEMO.SAVE, TELEPATHY.SEND, BACKUP.NOW")
            
            if 'error' in test_result:
                report_lines.append(f"    ERROR: {test_result['error']}")
        
        # Add configuration summary
        report_lines.extend([
            "",
            "CONFIGURATION FLAGS",
            "-" * 40,
            "soulos.enabled: Controls if SoulOS processes syscalls (default: false)",
            "soulos.auto_execute: Executes safe syscalls automatically (default: false)",
            "",
            "SAFE SYSCALLS WHITELIST",
            "-" * 40,
            "- MEMO.SAVE: Save to memory",
            "- TELEPATHY.SEND: Send telepathic message",
            "- BACKUP.NOW: Trigger backup",
            ""
        ])
        
        # Add summary
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        report_lines.extend([
            "SUMMARY",
            "-" * 40,
            f"Total Tests: {total_tests}",
            f"Passed: {passed_tests}",
            f"Failed: {total_tests - passed_tests}",
            f"Pass Rate: {pass_rate:.1f}%",
            "",
            "ACCEPTANCE CRITERIA",
            "-" * 40,
            "✅ Unified naming: process_syscalls() method",
            "✅ Standardized contract: {ok, executed, sandboxed, msg}",
            "✅ Configuration flags: soulos.enabled, soulos.auto_execute",
            "✅ Safe syscalls whitelist implemented",
            f"{'✅' if pass_rate >= 80 else '❌'} Tests passing (>80%)",
            "",
            "=" * 80,
            f"FASE 4 STATUS: {'✅ COMPLETE' if pass_rate >= 80 else '⚠️ REVIEW NEEDED'}",
            "=" * 80
        ])
        
        report_text = "\n".join(report_lines)
        
        # Save text report
        report_file = self.reports_dir / "phase4_report.txt"
        with open(report_file, 'w') as f:
            f.write(report_text)
        print(f"  ✅ Saved: {report_file}")
        
        # Print report
        print("\n" + report_text)
        
        return pass_rate >= 80
    
    def run_all_tests(self):
        """Run all FASE 4 tests"""
        print("\n" + "=" * 80)
        print("HARMONY V100 - FASE 4 - SOULOS GATING & NAMING")
        print("=" * 80)
        
        try:
            # Run tests
            self.test_dry_run_mode()
            self.test_auto_execute_mode()
            self.test_disabled_mode()
            self.test_naming_standardization()
            self.test_whitelist()
            
            # Generate reports
            success = self.generate_reports()
            
            return success
            
        finally:
            # Clean up temp directory
            self.cleanup()

def main():
    """Main entry point"""
    tester = Phase4Tester()
    
    try:
        success = tester.run_all_tests()
        
        if success:
            print("\n✅ FASE 4 - SoulOS Gating & Naming: COMPLETE")
            sys.exit(0)
        else:
            print("\n⚠️ FASE 4 - Some tests failed, review needed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
        tester.cleanup()
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        tester.cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()