#!/usr/bin/env python3
"""
Runtime Tester - Actually executes methods to find broken code
"""

import sys
import os
import traceback
import json
from typing import Dict, List

sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-validation')

def test_actual_execution():
    """Test actual method execution to find runtime issues"""
    
    results = {
        'broken_imports': [],
        'broken_initializations': [],
        'broken_methods': [],
        'missing_attributes': [],
        'actual_errors': []
    }
    
    # Test 1: Chat system methods
    try:
        from apps.scripturemon.chat import ScripturemonChat
        chat = ScripturemonChat()
        
        # Test message processing
        try:
            result = chat.process("test message")
            print("✓ chat.process works")
        except AttributeError as e:
            results['missing_attributes'].append(f"chat.process: {e}")
        except Exception as e:
            results['broken_methods'].append(f"chat.process: {e}")
            
        # Test get_response
        try:
            response = chat.get_response("test")
            print("✓ chat.get_response works")
        except AttributeError as e:
            results['missing_attributes'].append(f"chat.get_response: {e}")
        except Exception as e:
            results['broken_methods'].append(f"chat.get_response: {e}")
            
    except ImportError as e:
        results['broken_imports'].append(f"chat: {e}")
    except Exception as e:
        results['broken_initializations'].append(f"ScripturemonChat: {e}")
    
    # Test 2: Bootstrap system
    try:
        from apps.scripturemon.bootstrap import bootstrap_all
        
        # Try to bootstrap
        try:
            context = bootstrap_all()
            print("✓ bootstrap_all works")
            
            # Check context components
            if not context.get('memory_manager'):
                results['missing_attributes'].append("bootstrap: missing memory_manager")
            if not context.get('pipeline'):
                results['missing_attributes'].append("bootstrap: missing pipeline")
                
        except Exception as e:
            results['broken_methods'].append(f"bootstrap_all: {e}")
            
    except ImportError as e:
        results['broken_imports'].append(f"bootstrap: {e}")
    
    # Test 3: Memory Manager
    try:
        from apps.scripturemon.canonical.memory_manager import MemoryManager
        
        try:
            memory = MemoryManager()
            print("✓ MemoryManager initializes")
            
            # Test store/retrieve
            try:
                memory.store("test_key", "test_value")
                value = memory.retrieve("test_key")
                if value != "test_value":
                    results['broken_methods'].append("MemoryManager: store/retrieve mismatch")
                else:
                    print("✓ MemoryManager store/retrieve works")
            except Exception as e:
                results['broken_methods'].append(f"MemoryManager.store: {e}")
                
        except Exception as e:
            results['broken_initializations'].append(f"MemoryManager: {e}")
            
    except ImportError as e:
        results['broken_imports'].append(f"canonical.memory_manager: {e}")
    
    # Test 4: Consciousness system
    try:
        from apps.scripturemon.canonical.consciousness import ConsciousnessStream
        
        try:
            consciousness = ConsciousnessStream()
            print("✓ ConsciousnessStream initializes")
            
            # Test process
            try:
                consciousness.process("test")
                print("✓ ConsciousnessStream.process works")
            except AttributeError as e:
                results['missing_attributes'].append(f"ConsciousnessStream.process: {e}")
            except Exception as e:
                results['broken_methods'].append(f"ConsciousnessStream.process: {e}")
                
        except Exception as e:
            results['broken_initializations'].append(f"ConsciousnessStream: {e}")
            
    except ImportError as e:
        results['broken_imports'].append(f"canonical.consciousness: {e}")
    
    # Test 5: QuadruplePipeline
    try:
        from apps.scripturemon.quadruple_pipeline import QuadruplePipeline
        
        try:
            pipeline = QuadruplePipeline()
            print("✓ QuadruplePipeline initializes")
            
            # Test run_pipeline
            try:
                result = pipeline.run_pipeline("test input")
                print("✓ QuadruplePipeline.run_pipeline works")
            except Exception as e:
                results['broken_methods'].append(f"QuadruplePipeline.run_pipeline: {e}")
                
        except Exception as e:
            results['broken_initializations'].append(f"QuadruplePipeline: {e}")
            
    except ImportError as e:
        results['broken_imports'].append(f"quadruple_pipeline: {e}")
    
    # Test 6: CLI components
    try:
        from apps.scripturemon.cli import main as cli_main
        print("✓ CLI imports")
    except ImportError as e:
        results['broken_imports'].append(f"cli: {e}")
    
    # Test 7: Telepathy Network
    try:
        from apps.scripturemon.telepathic_network_advanced import TelepathyNetwork
        
        try:
            network = TelepathyNetwork()
            print("✓ TelepathyNetwork initializes")
            
            # Test send/receive
            try:
                network.send("test_channel", {"data": "test"})
                print("✓ TelepathyNetwork.send works")
            except Exception as e:
                results['broken_methods'].append(f"TelepathyNetwork.send: {e}")
                
        except Exception as e:
            results['broken_initializations'].append(f"TelepathyNetwork: {e}")
            
    except ImportError as e:
        results['broken_imports'].append(f"telepathic_network: {e}")
    
    # Test 8: DigiLang Integration
    try:
        from apps.scripturemon.digilang_integration import DigiLangIntegration
        
        try:
            digilang = DigiLangIntegration()
            print("✓ DigiLangIntegration initializes")
            
            # Test compress
            try:
                compressed = digilang.compress("test text")
                print("✓ DigiLangIntegration.compress works")
            except AttributeError as e:
                results['missing_attributes'].append(f"DigiLangIntegration.compress: {e}")
            except Exception as e:
                results['broken_methods'].append(f"DigiLangIntegration.compress: {e}")
                
        except Exception as e:
            results['broken_initializations'].append(f"DigiLangIntegration: {e}")
            
    except ImportError as e:
        results['broken_imports'].append(f"digilang_integration: {e}")
    
    return results


def test_dependency_chain():
    """Test dependency chains to find circular imports"""
    
    circular_imports = []
    import_errors = []
    
    modules_to_test = [
        'apps.scripturemon.chat',
        'apps.scripturemon.bootstrap',
        'apps.scripturemon.cli',
        'apps.scripturemon.quadruple_pipeline',
        'apps.scripturemon.canonical.memory_manager',
        'apps.scripturemon.canonical.consciousness',
        'apps.scripturemon.telepathic_network_advanced',
        'apps.scripturemon.digilang_integration',
        'apps.scripturemon.immortality',
        'apps.scripturemon.memory_unification',
        'apps.scripturemon.soulos_crystal'
    ]
    
    for module in modules_to_test:
        try:
            # Force reimport to catch circular dependencies
            if module in sys.modules:
                del sys.modules[module]
            __import__(module)
            print(f"✓ {module} imports successfully")
        except ImportError as e:
            if "circular" in str(e).lower() or "cannot import" in str(e).lower():
                circular_imports.append(f"{module}: {e}")
            else:
                import_errors.append(f"{module}: {e}")
        except Exception as e:
            import_errors.append(f"{module}: {e}")
    
    return circular_imports, import_errors


def main():
    print("🔬 DigiDoctor Runtime Tester")
    print("=" * 60)
    
    # Test actual execution
    print("\n📝 Testing Actual Method Execution...")
    print("-" * 40)
    execution_results = test_actual_execution()
    
    # Test dependency chains
    print("\n🔗 Testing Dependency Chains...")
    print("-" * 40)
    circular, import_errs = test_dependency_chain()
    
    # Compile report
    report = {
        'execution_tests': execution_results,
        'circular_imports': circular,
        'import_errors': import_errs,
        'summary': {
            'broken_imports': len(execution_results['broken_imports']),
            'broken_initializations': len(execution_results['broken_initializations']),
            'broken_methods': len(execution_results['broken_methods']),
            'missing_attributes': len(execution_results['missing_attributes']),
            'circular_imports': len(circular),
            'total_issues': sum([
                len(execution_results['broken_imports']),
                len(execution_results['broken_initializations']),
                len(execution_results['broken_methods']),
                len(execution_results['missing_attributes']),
                len(circular)
            ])
        }
    }
    
    # Save report
    report_path = '/Users/clubproducoes/Digimundo/scripturemon-validation/DigiDoctor/reports/runtime_test_report.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print results
    print("\n🚨 ISSUES FOUND:")
    print("-" * 40)
    
    if execution_results['broken_imports']:
        print("\n❌ Broken Imports:")
        for issue in execution_results['broken_imports']:
            print(f"  • {issue}")
    
    if execution_results['broken_initializations']:
        print("\n❌ Broken Initializations:")
        for issue in execution_results['broken_initializations']:
            print(f"  • {issue}")
    
    if execution_results['broken_methods']:
        print("\n❌ Broken Methods:")
        for issue in execution_results['broken_methods']:
            print(f"  • {issue}")
    
    if execution_results['missing_attributes']:
        print("\n❌ Missing Attributes:")
        for issue in execution_results['missing_attributes']:
            print(f"  • {issue}")
    
    if circular:
        print("\n❌ Circular Imports:")
        for issue in circular:
            print(f"  • {issue}")
    
    print(f"\n📊 Total Issues Found: {report['summary']['total_issues']}")
    print(f"✅ Report saved to: {report_path}")
    
    return report


if __name__ == "__main__":
    main()