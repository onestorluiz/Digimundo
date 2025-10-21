#!/usr/bin/env python3
"""
Comparação completa entre v32 e harmony_v100
"""
import json
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple

sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-validation')

class VersionComparator:
    def __init__(self):
        self.root = Path('/Users/clubproducoes/Digimundo/scripturemon-validation')
        self.results = {
            'v32': {},
            'harmony_v100': {},
            'comparison': {}
        }
        
    def test_cli_commands(self) -> Dict[str, Any]:
        """Testa comandos CLI básicos"""
        results = {}
        
        commands = [
            ('help', ['./bin/scripturemon', '--help']),
            ('status', ['./bin/scripturemon', 'status']),
            ('backup_status', ['./bin/scripturemon', 'backup', 'status']),
        ]
        
        for cmd_name, cmd in commands:
            try:
                start = time.time()
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                elapsed = time.time() - start
                
                results[cmd_name] = {
                    'success': result.returncode == 0,
                    'time': elapsed,
                    'output_size': len(result.stdout),
                    'has_output': bool(result.stdout.strip())
                }
            except subprocess.TimeoutExpired:
                results[cmd_name] = {
                    'success': False,
                    'error': 'timeout'
                }
            except Exception as e:
                results[cmd_name] = {
                    'success': False,
                    'error': str(e)
                }
                
        return results
        
    def analyze_v32_features(self) -> Dict[str, Any]:
        """Analisa características da v32"""
        features = {
            'files': 0,
            'tests': 0,
            'components': [],
            'focus': []
        }
        
        # Contar arquivos v32
        v32_files = list(self.root.glob('**/*v32*.py'))
        features['files'] = len(v32_files)
        
        # Analisar componentes
        for f in v32_files:
            if 'rag' in f.name.lower():
                if 'RAG/Chroma' not in features['components']:
                    features['components'].append('RAG/Chroma')
            if 'perf' in f.name.lower():
                if 'Performance' not in features['components']:
                    features['components'].append('Performance')
            if 'smoke' in f.name.lower():
                features['tests'] += 1
                
        # Identificar foco
        if features['tests'] > 5:
            features['focus'].append('Testing')
        if 'RAG/Chroma' in features['components']:
            features['focus'].append('Knowledge Management')
            
        return features
        
    def analyze_harmony_features(self) -> Dict[str, Any]:
        """Analisa características da harmony_v100"""
        features = {
            'files': 0,
            'reports': 0,
            'components': [],
            'focus': [],
            'config': {}
        }
        
        # Contar relatórios harmony
        harmony_reports = list(self.root.glob('reports/harmony_*/**/*.json'))
        features['reports'] = len(harmony_reports)
        
        # Verificar componentes
        components_to_check = [
            ('monitoring_system.py', 'Monitoring'),
            ('memory_harmony.py', 'Memory Harmony'),
            ('telepathy_network.py', 'Telepathy'),
            ('soulos.py', 'SoulOS'),
            ('backup_enhanced.py', 'Enhanced Backup')
        ]
        
        for filename, component in components_to_check:
            if (self.root / 'apps' / 'scripturemon' / filename).exists():
                features['components'].append(component)
                
        # Ler configuração se existir
        settings_file = self.root / 'config' / 'settings.yaml'
        if settings_file.exists():
            try:
                import yaml
                with open(settings_file) as f:
                    settings = yaml.safe_load(f)
                    features['config'] = {
                        'memory': settings.get('memory', {}).get('enabled', False),
                        'rag': settings.get('rag', {}).get('enabled', False),
                        'redis': settings.get('redis', {}).get('enabled', False),
                        'soulos': settings.get('soulos', {}).get('enabled', False),
                        'monitoring': settings.get('monitoring', {}).get('enabled', False)
                    }
            except:
                pass
                
        # Identificar foco
        if features['reports'] > 10:
            features['focus'].append('Reporting/Analytics')
        if 'Memory Harmony' in features['components']:
            features['focus'].append('Memory Unification')
        if 'Telepathy' in features['components']:
            features['focus'].append('Distributed Intelligence')
            
        return features
        
    def test_memory_systems(self) -> Dict[str, Any]:
        """Testa sistemas de memória"""
        results = {}
        
        try:
            # Testar Memory Bridge
            from apps.scripturemon.membridge_restored import MemoryBridge
            bridge = MemoryBridge()
            
            # Salvar memória teste
            save_result = bridge.save("Test memory", importance=0.5)
            results['membridge_save'] = bool(save_result)
            
            # Buscar memória
            search_result = bridge.search("test", limit=1)
            results['membridge_search'] = len(search_result) > 0
            
        except Exception as e:
            results['membridge_error'] = str(e)
            
        try:
            # Testar Memory Harmony se existir
            from apps.scripturemon.memory_harmony import MemoryHarmony
            harmony = MemoryHarmony()
            
            save_result = harmony.save("Harmony test", importance=0.7)
            results['harmony_save'] = bool(save_result)
            
        except ImportError:
            results['harmony_available'] = False
        except Exception as e:
            results['harmony_error'] = str(e)
            
        return results
        
    def calculate_harmony_percentage(self) -> float:
        """Calcula percentual de funcionalidade harmônica"""
        scores = {
            'components': 0,
            'integration': 0,
            'stability': 0,
            'features': 0
        }
        
        # Componentes harmônicos
        harmony_components = ['Memory Harmony', 'Telepathy', 'Monitoring', 'Enhanced Backup']
        for comp in harmony_components:
            if comp in self.results['harmony_v100'].get('features', {}).get('components', []):
                scores['components'] += 25
                
        # Integração
        cli_results = self.results['harmony_v100'].get('cli', {})
        working_commands = sum(1 for r in cli_results.values() if r.get('success'))
        scores['integration'] = (working_commands / max(len(cli_results), 1)) * 100
        
        # Estabilidade (baseado em erros)
        errors = 0
        for test_name, test_result in self.results['harmony_v100'].items():
            if isinstance(test_result, dict) and 'error' in test_result:
                errors += 1
        scores['stability'] = max(0, 100 - (errors * 20))
        
        # Features avançadas
        config = self.results['harmony_v100'].get('features', {}).get('config', {})
        enabled_features = sum(1 for v in config.values() if v)
        scores['features'] = (enabled_features / max(len(config), 1)) * 100
        
        # Média ponderada
        weights = {
            'components': 0.3,
            'integration': 0.3,
            'stability': 0.2,
            'features': 0.2
        }
        
        total = sum(scores[k] * weights[k] for k in scores)
        return round(total, 2)
        
    def generate_comparison_report(self) -> Dict[str, Any]:
        """Gera relatório comparativo final"""
        comparison = {
            'timestamp': datetime.now().isoformat(),
            'versions': {
                'v32': {
                    'period': 'August 2024',
                    'focus': 'Performance, Testing, RAG',
                    'strengths': [],
                    'weaknesses': []
                },
                'harmony_v100': {
                    'period': 'September 2024',
                    'focus': 'Harmony, Integration, Monitoring',
                    'strengths': [],
                    'weaknesses': []
                }
            },
            'evolution': [],
            'harmony_score': 0,
            'recommendation': ''
        }
        
        # Análise v32
        v32_features = self.results['v32'].get('features', {})
        if v32_features.get('tests', 0) > 5:
            comparison['versions']['v32']['strengths'].append('Comprehensive testing')
        if 'RAG/Chroma' in v32_features.get('components', []):
            comparison['versions']['v32']['strengths'].append('Knowledge management')
        comparison['versions']['v32']['weaknesses'].append('Limited monitoring')
        comparison['versions']['v32']['weaknesses'].append('No harmony features')
        
        # Análise harmony_v100
        harmony_features = self.results['harmony_v100'].get('features', {})
        if 'Memory Harmony' in harmony_features.get('components', []):
            comparison['versions']['harmony_v100']['strengths'].append('Unified memory')
        if 'Monitoring' in harmony_features.get('components', []):
            comparison['versions']['harmony_v100']['strengths'].append('System monitoring')
        if harmony_features.get('reports', 0) > 10:
            comparison['versions']['harmony_v100']['strengths'].append('Rich reporting')
            
        # Evolução
        comparison['evolution'] = [
            'Added memory harmony layer',
            'Introduced monitoring system',
            'Enhanced backup with deduplication',
            'Improved CLI integration',
            'Added telepathy network'
        ]
        
        # Score harmônico
        comparison['harmony_score'] = self.calculate_harmony_percentage()
        
        # Recomendação
        if comparison['harmony_score'] > 70:
            comparison['recommendation'] = 'harmony_v100 is production-ready with good integration'
        elif comparison['harmony_score'] > 50:
            comparison['recommendation'] = 'harmony_v100 shows promise but needs stabilization'
        else:
            comparison['recommendation'] = 'Consider using v32 for stability, harmony_v100 for features'
            
        return comparison
        
    def run_full_comparison(self):
        """Executa comparação completa"""
        print("🔍 Iniciando comparação v32 vs harmony_v100...")
        
        # Testes CLI
        print("📋 Testando comandos CLI...")
        self.results['harmony_v100']['cli'] = self.test_cli_commands()
        
        # Análise de features
        print("🔬 Analisando features v32...")
        self.results['v32']['features'] = self.analyze_v32_features()
        
        print("🔬 Analisando features harmony_v100...")
        self.results['harmony_v100']['features'] = self.analyze_harmony_features()
        
        # Testes de memória
        print("🧠 Testando sistemas de memória...")
        self.results['harmony_v100']['memory'] = self.test_memory_systems()
        
        # Gerar comparação
        print("📊 Gerando relatório comparativo...")
        self.results['comparison'] = self.generate_comparison_report()
        
        # Salvar resultados
        output_dir = self.root / 'reports' / 'harmony_vFinal' / 'test_audit'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / 'version_comparison.json'
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
            
        print(f"✅ Relatório salvo em: {output_file}")
        
        # Imprimir resumo
        self.print_summary()
        
    def print_summary(self):
        """Imprime resumo da comparação"""
        comp = self.results['comparison']
        
        print("\n" + "="*60)
        print("📊 RESUMO DA COMPARAÇÃO: v32 vs harmony_v100")
        print("="*60)
        
        print("\n🔹 V32 (Agosto 2024)")
        print(f"  Foco: {comp['versions']['v32']['focus']}")
        print(f"  Pontos fortes: {', '.join(comp['versions']['v32']['strengths'])}")
        print(f"  Pontos fracos: {', '.join(comp['versions']['v32']['weaknesses'])}")
        
        print("\n🔹 HARMONY_V100 (Setembro 2024)")
        print(f"  Foco: {comp['versions']['harmony_v100']['focus']}")
        print(f"  Pontos fortes: {', '.join(comp['versions']['harmony_v100']['strengths'])}")
        
        print("\n📈 EVOLUÇÃO:")
        for evo in comp['evolution']:
            print(f"  • {evo}")
            
        print(f"\n🎯 HARMONIA FUNCIONAL: {comp['harmony_score']}%")
        print(f"\n💡 RECOMENDAÇÃO: {comp['recommendation']}")
        print("="*60)

if __name__ == "__main__":
    comparator = VersionComparator()
    comparator.run_full_comparison()