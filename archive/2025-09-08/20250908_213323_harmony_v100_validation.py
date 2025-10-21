#!/usr/bin/env python3
"""
HARMONY V100 - Comprehensive Validation Suite
Validates all harmony components and generates detailed reports
"""

import json
import time
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import importlib
import traceback

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

class HarmonyValidator:
    """Comprehensive validation for HARMONY V100 implementation"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'phase': 'validation',
            'tests': {},
            'metrics': {},
            'errors': [],
            'warnings': []
        }
        self.reports_dir = Path("reports/harmony_v100/validation")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_memory_brain(self) -> Dict:
        """Validate Memory Brain implementation"""
        print("\n🧠 Validating Memory Brain...")
        result = {'status': 'unknown', 'tests': {}}
        
        try:
            from src.memory.memory_brain import MemoryBrain
            brain = MemoryBrain()
            
            # Test 1: Context retrieval
            print("  Testing context retrieval...")
            start_time = time.time()
            context = brain.get_context("test query", k=5)
            result['tests']['context_retrieval'] = {
                'passed': isinstance(context, list),
                'time_ms': (time.time() - start_time) * 1000,
                'items_returned': len(context)
            }
            
            # Test 2: Memory storage
            print("  Testing memory storage...")
            start_time = time.time()
            mem_id = brain.save(
                kind='episodic',
                data={'content': 'Validation test memory', 'timestamp': time.time()},
                meta={'test': True}
            )
            result['tests']['memory_storage'] = {
                'passed': bool(mem_id),
                'time_ms': (time.time() - start_time) * 1000,
                'memory_id': mem_id
            }
            
            # Test 3: Memory promotion
            print("  Testing memory promotion...")
            if mem_id:
                start_time = time.time()
                promoted = brain.promote(mem_id)
                result['tests']['memory_promotion'] = {
                    'passed': isinstance(promoted, bool),
                    'time_ms': (time.time() - start_time) * 1000,
                    'promoted': promoted
                }
            
            # Test 4: Synchronization
            print("  Testing synchronization...")
            start_time = time.time()
            sync_stats = brain.sync()
            result['tests']['synchronization'] = {
                'passed': isinstance(sync_stats, dict),
                'time_ms': (time.time() - start_time) * 1000,
                'stats': sync_stats
            }
            
            # Test 5: Statistics
            print("  Testing statistics...")
            start_time = time.time()
            stats = brain.stats()
            result['tests']['statistics'] = {
                'passed': isinstance(stats, dict) and 'total_memories' in stats,
                'time_ms': (time.time() - start_time) * 1000,
                'stats': stats
            }
            
            # Calculate overall status
            passed_count = sum(1 for t in result['tests'].values() if t.get('passed'))
            total_count = len(result['tests'])
            result['status'] = 'passed' if passed_count == total_count else 'partial'
            result['summary'] = f"{passed_count}/{total_count} tests passed"
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            result['traceback'] = traceback.format_exc()
            self.results['errors'].append(f"Memory Brain: {e}")
        
        self.results['tests']['memory_brain'] = result
        return result
    
    def validate_reflection_system(self) -> Dict:
        """Validate Reflection System"""
        print("\n🔮 Validating Reflection System...")
        result = {'status': 'unknown', 'tests': {}}
        
        try:
            from src.memory.reflection_system import ReflectionSystem
            reflection = ReflectionSystem(
                importance_threshold=20.0,  # Lower for testing
                window_size=5
            )
            
            # Test 1: Event recording
            print("  Testing event recording...")
            events_created = []
            for i in range(5):
                event = reflection.record_event(
                    content=f"Test event {i} with {'high' if i % 2 == 0 else 'low'} importance",
                    event_type='user_query' if i % 2 == 0 else 'routine',
                    tags=[f'test_{i}']
                )
                events_created.append(event)
            
            result['tests']['event_recording'] = {
                'passed': len(events_created) == 5,
                'events_created': len(events_created),
                'importance_sum': reflection.importance_sum
            }
            
            # Test 2: Importance calculation
            print("  Testing importance calculation...")
            test_cases = [
                ("Critical system error!", "system_error", None, 8.0),
                ("Routine check", "routine", None, 3.0),
                ("Important breakthrough in learning", "learning", None, 9.0)
            ]
            
            importance_tests = []
            for content, event_type, metadata, expected_min in test_cases:
                score = reflection.calculate_importance(content, event_type, metadata)
                importance_tests.append({
                    'content': content[:30],
                    'type': event_type,
                    'score': score,
                    'passed': score >= expected_min
                })
            
            result['tests']['importance_calculation'] = {
                'passed': all(t['passed'] for t in importance_tests),
                'details': importance_tests
            }
            
            # Test 3: Reflection trigger
            print("  Testing reflection trigger...")
            start_time = time.time()
            triggered_reflection = reflection.trigger_reflection('test')
            result['tests']['reflection_trigger'] = {
                'passed': triggered_reflection is not None,
                'time_ms': (time.time() - start_time) * 1000,
                'reflection_id': triggered_reflection.id if triggered_reflection else None,
                'insight': triggered_reflection.insight[:100] if triggered_reflection else None
            }
            
            # Test 4: Get insights for context
            print("  Testing context insights...")
            insights = reflection.get_insights_for_context()
            result['tests']['context_insights'] = {
                'passed': isinstance(insights, str) and len(insights) > 0,
                'insights_length': len(insights)
            }
            
            # Calculate overall status
            passed_count = sum(1 for t in result['tests'].values() if t.get('passed'))
            total_count = len(result['tests'])
            result['status'] = 'passed' if passed_count == total_count else 'partial'
            result['summary'] = f"{passed_count}/{total_count} tests passed"
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            result['traceback'] = traceback.format_exc()
            self.results['errors'].append(f"Reflection System: {e}")
        
        self.results['tests']['reflection_system'] = result
        return result
    
    def validate_graph_memory(self) -> Dict:
        """Validate Graph Memory System"""
        print("\n🕸️ Validating Graph Memory...")
        result = {'status': 'unknown', 'tests': {}}
        
        try:
            from src.memory.graph_memory import GraphMemorySystem
            graph = GraphMemorySystem()
            
            # Test 1: Add memory to graph
            print("  Testing memory addition...")
            node1 = graph.add_memory_to_graph(
                content="Alice works at TechCorp",
                vector_id="vec_001",
                importance=7.5,
                tags=['person', 'company']
            )
            node2 = graph.add_memory_to_graph(
                content="Bob is Alice's colleague",
                vector_id="vec_002",
                importance=6.0,
                tags=['person', 'relationship']
            )
            
            result['tests']['memory_addition'] = {
                'passed': node1 is not None and node2 is not None,
                'nodes_created': 2 if node1 and node2 else 0
            }
            
            # Test 2: Query related memories
            print("  Testing memory query...")
            start_time = time.time()
            related = graph.query_related_memories("Alice", max_hops=2, limit=5)
            result['tests']['memory_query'] = {
                'passed': isinstance(related, list),
                'time_ms': (time.time() - start_time) * 1000,
                'memories_found': len(related)
            }
            
            # Test 3: Get subgraph
            print("  Testing subgraph extraction...")
            if node1:
                subgraph = graph.get_subgraph(node1.id, radius=1)
                result['tests']['subgraph_extraction'] = {
                    'passed': 'nodes' in subgraph and 'edges' in subgraph,
                    'nodes_count': len(subgraph.get('nodes', [])),
                    'edges_count': len(subgraph.get('edges', []))
                }
            
            # Test 4: Statistics
            print("  Testing graph statistics...")
            stats = graph.get_statistics()
            result['tests']['statistics'] = {
                'passed': isinstance(stats, dict) and 'total_nodes' in stats,
                'stats': stats
            }
            
            # Calculate overall status
            passed_count = sum(1 for t in result['tests'].values() if t.get('passed'))
            total_count = len(result['tests'])
            result['status'] = 'passed' if passed_count == total_count else 'partial'
            result['summary'] = f"{passed_count}/{total_count} tests passed"
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            result['traceback'] = traceback.format_exc()
            self.results['errors'].append(f"Graph Memory: {e}")
        
        self.results['tests']['graph_memory'] = result
        return result
    
    def validate_consolidation(self) -> Dict:
        """Validate Consolidation System"""
        print("\n♻️ Validating Consolidation System...")
        result = {'status': 'unknown', 'tests': {}}
        
        try:
            from src.memory.consolidation_system import MemoryConsolidationSystem
            consolidator = MemoryConsolidationSystem()
            
            # Test 1: Check if consolidation runs
            print("  Testing consolidation execution...")
            start_time = time.time()
            stats = consolidator.consolidate_memories()
            result['tests']['consolidation_execution'] = {
                'passed': stats is not None,
                'time_ms': (time.time() - start_time) * 1000,
                'stats': stats.to_dict() if stats else None
            }
            
            # Test 2: Get consolidation history
            print("  Testing consolidation history...")
            history = consolidator.get_consolidation_history(limit=5)
            result['tests']['consolidation_history'] = {
                'passed': isinstance(history, list),
                'history_count': len(history)
            }
            
            # Calculate overall status
            passed_count = sum(1 for t in result['tests'].values() if t.get('passed'))
            total_count = len(result['tests'])
            result['status'] = 'passed' if passed_count == total_count else 'partial'
            result['summary'] = f"{passed_count}/{total_count} tests passed"
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            result['traceback'] = traceback.format_exc()
            self.results['errors'].append(f"Consolidation System: {e}")
        
        self.results['tests']['consolidation_system'] = result
        return result
    
    def validate_integration(self) -> Dict:
        """Validate full system integration"""
        print("\n🔗 Validating System Integration...")
        result = {'status': 'unknown', 'tests': {}}
        
        try:
            from src.memory.adaptive_memory_manager import AdaptiveMemoryManager
            manager = AdaptiveMemoryManager()
            
            # Test 1: Store memory with all systems
            print("  Testing integrated memory storage...")
            start_time = time.time()
            stored = manager.store_memory(
                content="Integration test: Important discovery about quantum computing",
                memory_type='learning',
                importance=8.5,
                tags=['quantum', 'breakthrough'],
                metadata={'source': 'validation_test'}
            )
            result['tests']['integrated_storage'] = {
                'passed': 'id' in stored,
                'time_ms': (time.time() - start_time) * 1000,
                'memory_id': stored.get('id')
            }
            
            # Test 2: Recall with hybrid approach
            print("  Testing hybrid recall...")
            start_time = time.time()
            memories = manager.recall_memory(
                query="quantum computing",
                use_graph=True,
                use_vector=True,
                limit=5
            )
            result['tests']['hybrid_recall'] = {
                'passed': isinstance(memories, list),
                'time_ms': (time.time() - start_time) * 1000,
                'memories_found': len(memories)
            }
            
            # Test 3: Trigger consolidation
            print("  Testing triggered consolidation...")
            start_time = time.time()
            consolidation_result = manager.trigger_consolidation()
            result['tests']['triggered_consolidation'] = {
                'passed': consolidation_result is not None,
                'time_ms': (time.time() - start_time) * 1000
            }
            
            # Test 4: Get system status
            print("  Testing system status...")
            status = manager.get_status()
            result['tests']['system_status'] = {
                'passed': isinstance(status, dict) and all(
                    key in status for key in ['reflection', 'graph', 'consolidation']
                ),
                'status': status
            }
            
            # Calculate overall status
            passed_count = sum(1 for t in result['tests'].values() if t.get('passed'))
            total_count = len(result['tests'])
            result['status'] = 'passed' if passed_count == total_count else 'partial'
            result['summary'] = f"{passed_count}/{total_count} tests passed"
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            result['traceback'] = traceback.format_exc()
            self.results['errors'].append(f"Integration: {e}")
        
        self.results['tests']['integration'] = result
        return result
    
    def calculate_metrics(self):
        """Calculate overall metrics"""
        print("\n📊 Calculating Metrics...")
        
        # Count test results
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        partial_systems = 0
        
        for system, result in self.results['tests'].items():
            if result['status'] == 'passed':
                passed_tests += len(result.get('tests', {}))
                total_tests += len(result.get('tests', {}))
            elif result['status'] == 'partial':
                partial_systems += 1
                for test in result.get('tests', {}).values():
                    total_tests += 1
                    if test.get('passed'):
                        passed_tests += 1
                    else:
                        failed_tests += 1
            else:
                failed_tests += len(result.get('tests', {})) or 1
                total_tests += len(result.get('tests', {})) or 1
        
        # Calculate performance metrics
        response_times = []
        for system_result in self.results['tests'].values():
            for test in system_result.get('tests', {}).values():
                if 'time_ms' in test:
                    response_times.append(test['time_ms'])
        
        self.results['metrics'] = {
            'total_systems': len(self.results['tests']),
            'systems_passed': sum(1 for r in self.results['tests'].values() if r['status'] == 'passed'),
            'systems_partial': partial_systems,
            'systems_failed': sum(1 for r in self.results['tests'].values() if r['status'] == 'failed'),
            'total_tests': total_tests,
            'tests_passed': passed_tests,
            'tests_failed': failed_tests,
            'pass_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'avg_response_ms': sum(response_times) / len(response_times) if response_times else 0,
            'max_response_ms': max(response_times) if response_times else 0,
            'min_response_ms': min(response_times) if response_times else 0
        }
    
    def generate_report(self):
        """Generate comprehensive validation report"""
        print("\n📝 Generating Report...")
        
        # Calculate metrics first
        self.calculate_metrics()
        
        # Create text report
        report_lines = [
            "=" * 80,
            "HARMONY V100 - VALIDATION REPORT",
            "=" * 80,
            f"Timestamp: {self.results['timestamp']}",
            "",
            "EXECUTIVE SUMMARY",
            "-" * 40,
            f"Systems Tested: {self.results['metrics']['total_systems']}",
            f"Systems Passed: {self.results['metrics']['systems_passed']}",
            f"Systems Partial: {self.results['metrics']['systems_partial']}",
            f"Systems Failed: {self.results['metrics']['systems_failed']}",
            "",
            f"Total Tests: {self.results['metrics']['total_tests']}",
            f"Tests Passed: {self.results['metrics']['tests_passed']}",
            f"Tests Failed: {self.results['metrics']['tests_failed']}",
            f"Pass Rate: {self.results['metrics']['pass_rate']:.1f}%",
            "",
            "PERFORMANCE METRICS",
            "-" * 40,
            f"Average Response: {self.results['metrics']['avg_response_ms']:.2f}ms",
            f"Max Response: {self.results['metrics']['max_response_ms']:.2f}ms",
            f"Min Response: {self.results['metrics']['min_response_ms']:.2f}ms",
            "",
            "DETAILED RESULTS",
            "-" * 40
        ]
        
        # Add detailed results for each system
        for system_name, system_result in self.results['tests'].items():
            report_lines.append(f"\n{system_name.upper().replace('_', ' ')}")
            report_lines.append(f"Status: {system_result['status'].upper()}")
            
            if 'error' in system_result:
                report_lines.append(f"Error: {system_result['error']}")
            
            if 'tests' in system_result:
                for test_name, test_result in system_result['tests'].items():
                    status = "✅" if test_result.get('passed') else "❌"
                    report_lines.append(f"  {status} {test_name}")
                    if 'time_ms' in test_result:
                        report_lines.append(f"     Time: {test_result['time_ms']:.2f}ms")
        
        # Add errors and warnings
        if self.results['errors']:
            report_lines.extend([
                "",
                "ERRORS",
                "-" * 40
            ])
            for error in self.results['errors']:
                report_lines.append(f"  ❌ {error}")
        
        if self.results['warnings']:
            report_lines.extend([
                "",
                "WARNINGS",
                "-" * 40
            ])
            for warning in self.results['warnings']:
                report_lines.append(f"  ⚠️ {warning}")
        
        # Add acceptance criteria
        report_lines.extend([
            "",
            "ACCEPTANCE CRITERIA",
            "-" * 40
        ])
        
        acceptance = {
            "Memory Brain Functional": self.results['tests'].get('memory_brain', {}).get('status') in ['passed', 'partial'],
            "Reflection System Active": self.results['tests'].get('reflection_system', {}).get('status') in ['passed', 'partial'],
            "Graph Memory Operational": self.results['tests'].get('graph_memory', {}).get('status') in ['passed', 'partial'],
            "Consolidation Running": self.results['tests'].get('consolidation_system', {}).get('status') in ['passed', 'partial'],
            "Integration Complete": self.results['tests'].get('integration', {}).get('status') in ['passed', 'partial'],
            "Pass Rate > 80%": self.results['metrics']['pass_rate'] > 80
        }
        
        for criterion, met in acceptance.items():
            status = "✅" if met else "❌"
            report_lines.append(f"  {status} {criterion}")
        
        all_criteria_met = all(acceptance.values())
        report_lines.extend([
            "",
            "=" * 80,
            f"OVERALL STATUS: {'✅ ACCEPTED' if all_criteria_met else '⚠️ REVIEW NEEDED'}",
            "=" * 80
        ])
        
        # Save reports
        text_report = "\n".join(report_lines)
        
        # Save text report
        report_file = self.reports_dir / "validation_report.txt"
        with open(report_file, 'w') as f:
            f.write(text_report)
        
        # Save JSON report
        json_file = self.reports_dir / "validation_results.json"
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Print summary
        print("\n" + text_report)
        
        return report_file, json_file, all_criteria_met
    
    def run_full_validation(self):
        """Run complete validation suite"""
        print("\n" + "=" * 80)
        print("HARMONY V100 - COMPREHENSIVE VALIDATION")
        print("=" * 80)
        
        # Run all validations
        self.validate_memory_brain()
        self.validate_reflection_system()
        self.validate_graph_memory()
        self.validate_consolidation()
        self.validate_integration()
        
        # Generate report
        report_file, json_file, accepted = self.generate_report()
        
        print(f"\n📁 Reports saved:")
        print(f"  - {report_file}")
        print(f"  - {json_file}")
        
        return accepted

def main():
    """Main validation entry point"""
    validator = HarmonyValidator()
    
    try:
        accepted = validator.run_full_validation()
        
        # Exit with appropriate code
        if accepted:
            print("\n✅ HARMONY V100 Validation: ACCEPTED")
            sys.exit(0)
        else:
            print("\n⚠️ HARMONY V100 Validation: REVIEW NEEDED")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Validation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()