#!/usr/bin/env python3
"""
HARMONY V100 - Performance & Optimization Report Generator
Analyzes validation results and generates comprehensive performance report
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import statistics

class PerformanceReporter:
    """Generate detailed performance and optimization reports"""
    
    def __init__(self):
        self.reports_dir = Path("reports/harmony_v100")
        self.validation_file = self.reports_dir / "validation/validation_results.json"
        self.performance_dir = self.reports_dir / "performance"
        self.performance_dir.mkdir(parents=True, exist_ok=True)
        
    def load_validation_results(self) -> Dict:
        """Load validation results"""
        if self.validation_file.exists():
            with open(self.validation_file, 'r') as f:
                return json.load(f)
        return {}
    
    def analyze_performance(self, results: Dict) -> Dict:
        """Analyze performance metrics"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'summary': {},
            'bottlenecks': [],
            'optimizations': [],
            'detailed_metrics': {}
        }
        
        # Extract response times
        response_times = []
        slow_operations = []
        
        for system, system_result in results.get('tests', {}).items():
            system_times = []
            for test_name, test_data in system_result.get('tests', {}).items():
                if 'time_ms' in test_data:
                    time_ms = test_data['time_ms']
                    response_times.append(time_ms)
                    system_times.append(time_ms)
                    
                    # Identify slow operations (>1000ms)
                    if time_ms > 1000:
                        slow_operations.append({
                            'system': system,
                            'test': test_name,
                            'time_ms': time_ms
                        })
            
            if system_times:
                analysis['detailed_metrics'][system] = {
                    'avg_ms': statistics.mean(system_times),
                    'median_ms': statistics.median(system_times),
                    'max_ms': max(system_times),
                    'min_ms': min(system_times),
                    'total_ms': sum(system_times)
                }
        
        # Calculate overall statistics
        if response_times:
            analysis['summary'] = {
                'total_operations': len(response_times),
                'avg_response_ms': statistics.mean(response_times),
                'median_response_ms': statistics.median(response_times),
                'p95_response_ms': self._percentile(response_times, 95),
                'p99_response_ms': self._percentile(response_times, 99),
                'std_dev_ms': statistics.stdev(response_times) if len(response_times) > 1 else 0,
                'total_time_ms': sum(response_times)
            }
        
        # Identify bottlenecks
        analysis['bottlenecks'] = sorted(slow_operations, key=lambda x: x['time_ms'], reverse=True)[:5]
        
        # Generate optimization recommendations
        analysis['optimizations'] = self._generate_optimizations(results, analysis)
        
        return analysis
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile"""
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        if index >= len(sorted_data):
            index = len(sorted_data) - 1
        return sorted_data[index]
    
    def _generate_optimizations(self, results: Dict, analysis: Dict) -> List[Dict]:
        """Generate optimization recommendations"""
        optimizations = []
        
        # Check for slow context retrieval
        if 'memory_brain' in results.get('tests', {}):
            brain_tests = results['tests']['memory_brain'].get('tests', {})
            if 'context_retrieval' in brain_tests:
                time_ms = brain_tests['context_retrieval'].get('time_ms', 0)
                if time_ms > 10000:  # >10 seconds
                    optimizations.append({
                        'priority': 'HIGH',
                        'component': 'Memory Brain',
                        'issue': f'Context retrieval taking {time_ms:.0f}ms',
                        'recommendation': 'Implement caching layer for frequent queries',
                        'expected_improvement': '50-70% reduction in response time'
                    })
        
        # Check for failed integrations
        failed_systems = [
            name for name, result in results.get('tests', {}).items()
            if result.get('status') == 'failed'
        ]
        
        if failed_systems:
            optimizations.append({
                'priority': 'CRITICAL',
                'component': 'System Integration',
                'issue': f'{len(failed_systems)} systems failed validation',
                'recommendation': 'Fix integration issues before deployment',
                'expected_improvement': 'System stability and reliability'
            })
        
        # Check for missing graph optimization
        if 'graph_memory' in analysis.get('detailed_metrics', {}):
            graph_metrics = analysis['detailed_metrics']['graph_memory']
            if graph_metrics.get('avg_ms', 0) > 100:
                optimizations.append({
                    'priority': 'MEDIUM',
                    'component': 'Graph Memory',
                    'issue': 'Graph queries slower than expected',
                    'recommendation': 'Add graph indexing and query optimization',
                    'expected_improvement': '30-40% faster graph traversal'
                })
        
        # Memory consolidation optimization
        if 'consolidation_system' in results.get('tests', {}):
            consolidation = results['tests']['consolidation_system']
            if consolidation.get('status') == 'passed':
                optimizations.append({
                    'priority': 'LOW',
                    'component': 'Consolidation System',
                    'issue': 'Consolidation running synchronously',
                    'recommendation': 'Move to background thread with adaptive scheduling',
                    'expected_improvement': 'Non-blocking memory operations'
                })
        
        # Check pass rate
        metrics = results.get('metrics', {})
        pass_rate = metrics.get('pass_rate', 0)
        if pass_rate < 80:
            optimizations.append({
                'priority': 'HIGH',
                'component': 'Overall System',
                'issue': f'Pass rate only {pass_rate:.1f}%',
                'recommendation': 'Focus on fixing failing tests before optimization',
                'expected_improvement': 'System reliability and correctness'
            })
        
        return optimizations
    
    def generate_report(self):
        """Generate comprehensive performance report"""
        print("\n" + "=" * 80)
        print("HARMONY V100 - PERFORMANCE & OPTIMIZATION REPORT")
        print("=" * 80)
        
        # Load validation results
        results = self.load_validation_results()
        if not results:
            print("❌ No validation results found")
            return
        
        # Analyze performance
        analysis = self.analyze_performance(results)
        
        # Create report
        report_lines = [
            "=" * 80,
            "HARMONY V100 - PERFORMANCE & OPTIMIZATION REPORT",
            "=" * 80,
            f"Generated: {analysis['timestamp']}",
            f"Based on: {results.get('timestamp', 'Unknown')}",
            "",
            "EXECUTIVE SUMMARY",
            "-" * 40
        ]
        
        # Add summary metrics
        summary = analysis['summary']
        if summary:
            report_lines.extend([
                f"Total Operations: {summary['total_operations']}",
                f"Average Response: {summary['avg_response_ms']:.2f}ms",
                f"Median Response: {summary['median_response_ms']:.2f}ms",
                f"95th Percentile: {summary['p95_response_ms']:.2f}ms",
                f"99th Percentile: {summary['p99_response_ms']:.2f}ms",
                f"Standard Deviation: {summary['std_dev_ms']:.2f}ms",
                f"Total Time: {summary['total_time_ms']:.2f}ms ({summary['total_time_ms']/1000:.2f}s)",
                ""
            ])
        
        # Add system breakdown
        report_lines.extend([
            "SYSTEM PERFORMANCE BREAKDOWN",
            "-" * 40
        ])
        
        for system, metrics in analysis['detailed_metrics'].items():
            report_lines.extend([
                f"\n{system.upper().replace('_', ' ')}:",
                f"  Average: {metrics['avg_ms']:.2f}ms",
                f"  Median: {metrics['median_ms']:.2f}ms",
                f"  Max: {metrics['max_ms']:.2f}ms",
                f"  Min: {metrics['min_ms']:.2f}ms",
                f"  Total: {metrics['total_ms']:.2f}ms"
            ])
        
        # Add bottlenecks
        if analysis['bottlenecks']:
            report_lines.extend([
                "",
                "PERFORMANCE BOTTLENECKS",
                "-" * 40
            ])
            
            for i, bottleneck in enumerate(analysis['bottlenecks'], 1):
                report_lines.append(
                    f"{i}. {bottleneck['system']}.{bottleneck['test']}: {bottleneck['time_ms']:.0f}ms"
                )
        
        # Add optimization recommendations
        if analysis['optimizations']:
            report_lines.extend([
                "",
                "OPTIMIZATION RECOMMENDATIONS",
                "-" * 40
            ])
            
            # Sort by priority
            priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
            sorted_opts = sorted(
                analysis['optimizations'],
                key=lambda x: priority_order.get(x['priority'], 999)
            )
            
            for opt in sorted_opts:
                report_lines.extend([
                    f"\n[{opt['priority']}] {opt['component']}",
                    f"  Issue: {opt['issue']}",
                    f"  Recommendation: {opt['recommendation']}",
                    f"  Expected Improvement: {opt['expected_improvement']}"
                ])
        
        # Add test results summary
        test_results = results.get('metrics', {})
        report_lines.extend([
            "",
            "VALIDATION SUMMARY",
            "-" * 40,
            f"Systems Tested: {test_results.get('total_systems', 0)}",
            f"Systems Passed: {test_results.get('systems_passed', 0)}",
            f"Systems Failed: {test_results.get('systems_failed', 0)}",
            f"Pass Rate: {test_results.get('pass_rate', 0):.1f}%",
            ""
        ])
        
        # Add performance grade
        grade = self._calculate_grade(analysis, results)
        report_lines.extend([
            "PERFORMANCE GRADE",
            "-" * 40,
            f"Overall Grade: {grade['letter']} ({grade['score']}/100)",
            f"",
            "Breakdown:",
            f"  Response Time: {grade['response_score']}/30",
            f"  Reliability: {grade['reliability_score']}/30",
            f"  Integration: {grade['integration_score']}/20",
            f"  Optimization: {grade['optimization_score']}/20",
            ""
        ])
        
        # Add next steps
        report_lines.extend([
            "RECOMMENDED NEXT STEPS",
            "-" * 40,
            "1. Address CRITICAL optimization recommendations",
            "2. Fix failing system integrations",
            "3. Implement caching for slow operations",
            "4. Add performance monitoring for production",
            "5. Set up automated performance regression tests",
            ""
        ])
        
        # Footer
        report_lines.extend([
            "=" * 80,
            f"STATUS: {'✅ READY FOR OPTIMIZATION' if grade['score'] >= 70 else '⚠️ FIXES REQUIRED'}",
            "=" * 80
        ])
        
        # Save report
        report_text = "\n".join(report_lines)
        
        # Save text report
        text_file = self.performance_dir / "performance_report.txt"
        with open(text_file, 'w') as f:
            f.write(report_text)
        
        # Save JSON analysis
        json_file = self.performance_dir / "performance_analysis.json"
        with open(json_file, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
        
        # Print report
        print(report_text)
        
        print(f"\n📁 Reports saved:")
        print(f"  - {text_file}")
        print(f"  - {json_file}")
        
        return grade['score'] >= 70
    
    def _calculate_grade(self, analysis: Dict, results: Dict) -> Dict:
        """Calculate performance grade"""
        grade = {
            'response_score': 0,
            'reliability_score': 0,
            'integration_score': 0,
            'optimization_score': 0
        }
        
        # Response time scoring (30 points)
        avg_response = analysis['summary'].get('avg_response_ms', float('inf'))
        if avg_response < 100:
            grade['response_score'] = 30
        elif avg_response < 500:
            grade['response_score'] = 25
        elif avg_response < 1000:
            grade['response_score'] = 20
        elif avg_response < 5000:
            grade['response_score'] = 15
        else:
            grade['response_score'] = 10
        
        # Reliability scoring (30 points)
        pass_rate = results.get('metrics', {}).get('pass_rate', 0)
        grade['reliability_score'] = int(pass_rate * 0.3)
        
        # Integration scoring (20 points)
        failed_systems = sum(1 for r in results.get('tests', {}).values() if r.get('status') == 'failed')
        total_systems = len(results.get('tests', {}))
        if total_systems > 0:
            success_ratio = (total_systems - failed_systems) / total_systems
            grade['integration_score'] = int(success_ratio * 20)
        
        # Optimization scoring (20 points)
        critical_issues = sum(1 for opt in analysis['optimizations'] if opt['priority'] == 'CRITICAL')
        high_issues = sum(1 for opt in analysis['optimizations'] if opt['priority'] == 'HIGH')
        
        if critical_issues == 0 and high_issues == 0:
            grade['optimization_score'] = 20
        elif critical_issues == 0:
            grade['optimization_score'] = 15 - (high_issues * 2)
        else:
            grade['optimization_score'] = 10 - (critical_issues * 5)
        
        grade['optimization_score'] = max(0, grade['optimization_score'])
        
        # Calculate total
        grade['score'] = sum([
            grade['response_score'],
            grade['reliability_score'],
            grade['integration_score'],
            grade['optimization_score']
        ])
        
        # Determine letter grade
        if grade['score'] >= 90:
            grade['letter'] = 'A'
        elif grade['score'] >= 80:
            grade['letter'] = 'B'
        elif grade['score'] >= 70:
            grade['letter'] = 'C'
        elif grade['score'] >= 60:
            grade['letter'] = 'D'
        else:
            grade['letter'] = 'F'
        
        return grade

def main():
    """Main entry point"""
    reporter = PerformanceReporter()
    
    try:
        success = reporter.generate_report()
        
        if success:
            print("\n✅ Performance analysis complete - Ready for optimization")
            sys.exit(0)
        else:
            print("\n⚠️ Performance issues detected - Fixes required")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Report generation interrupted")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Report generation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()