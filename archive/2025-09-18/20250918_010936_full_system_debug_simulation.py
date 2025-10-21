#!/usr/bin/env python3
"""
🔬 SIMULAÇÃO DE DEBUG COMPLETO DO ECOSSISTEMA
Testa todos os sistemas e identifica problemas
"""

import os
import sys
import json
import time
import traceback
import psutil
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class SystemDebugSimulator:
    def __init__(self):
        self.base_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        self.apps_dir = self.base_dir / "apps" / "scripturemon"
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'memory_systems': {},
            'ollama_systems': {},
            'file_systems': {},
            'resources': {},
            'critical_issues': [],
            'warnings': []
        }

    def check_memory_system(self, name: str) -> Dict:
        """Simula teste de um sistema de memória"""
        result = {
            'name': name,
            'status': 'UNKNOWN',
            'issues': [],
            'file_creation': []
        }

        file_path = self.apps_dir / f"{name}.py"

        # Verificar se arquivo existe
        if not file_path.exists():
            result['status'] = 'NOT_FOUND'
            result['issues'].append(f"Arquivo {name}.py não encontrado")
            return result

        # Simular importação
        try:
            # Ler arquivo para análise
            with open(file_path, 'r') as f:
                content = f.read()

            # Verificar problemas conhecidos
            if '/tmp/' in content or '/private/tmp' in content:
                result['issues'].append("❌ Usando /tmp ao invés de data/")
                result['status'] = 'PROBLEMATIC'

            if 'mmap.mmap' in content:
                # Verificar tamanho do mmap
                if '* 1024 * 1024 * 1024' in content:
                    gb_size = 0
                    import re
                    size_match = re.search(r'(\d+)\s*\*\s*1024\s*\*\s*1024\s*\*\s*1024', content)
                    if size_match:
                        gb_size = int(size_match.group(1))
                        result['issues'].append(f"⚠️ Criando mmap de {gb_size}GB!")
                        result['file_creation'].append({
                            'type': 'mmap',
                            'size_gb': gb_size,
                            'location': '/tmp' if '/tmp' in content else 'unknown'
                        })

            if 'sqlite3.connect' in content:
                result['file_creation'].append({
                    'type': 'sqlite',
                    'location': 'varies'
                })

            # Verificar imports problemáticos
            problematic_imports = [
                'quantum_cryptography_suite',
                'advanced_consensus_engine',
                'quantum_error_correction'
            ]

            for imp in problematic_imports:
                if imp in content:
                    result['issues'].append(f"❌ Import inexistente: {imp}")
                    result['status'] = 'BROKEN'

            # Se não tem problemas críticos
            if not result['issues']:
                result['status'] = 'OK'

        except Exception as e:
            result['status'] = 'ERROR'
            result['issues'].append(f"Erro na análise: {str(e)}")

        return result

    def check_ollama_system(self, name: str) -> Dict:
        """Simula teste de sistema Ollama"""
        result = {
            'name': name,
            'status': 'UNKNOWN',
            'has_hybrid_config': False,
            'issues': []
        }

        file_path = self.apps_dir / f"{name}.py"

        if not file_path.exists():
            result['status'] = 'NOT_FOUND'
            return result

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Verificar configuração híbrida
            if 'num_ctx' in content and '131072' in content:
                result['has_hybrid_config'] = True
            else:
                result['issues'].append("❌ Sem configuração híbrida (128K tokens)")

            if 'num_thread' in content:
                if '28' in content:
                    result['issues'].append("⚠️ Usando todos os 28 cores (ineficiente)")
                elif '14' in content:
                    result['has_hybrid_config'] = True

            if 'num_gpu' in content and '999' in content:
                result['has_hybrid_config'] = True
            elif 'num_gpu' in content and '0' in content:
                result['issues'].append("❌ GPU desabilitada!")

            result['status'] = 'OK' if result['has_hybrid_config'] else 'NEEDS_UPDATE'

        except Exception as e:
            result['status'] = 'ERROR'
            result['issues'].append(str(e))

        return result

    def check_file_creation_patterns(self) -> Dict:
        """Verifica padrões de criação de arquivos"""
        patterns = {
            'tmp_users': [],
            'data_users': [],
            'proper_cleanup': [],
            'no_cleanup': []
        }

        for py_file in self.apps_dir.glob("*.py"):
            try:
                with open(py_file, 'r') as f:
                    content = f.read()

                name = py_file.name

                if '/tmp' in content or 'tempfile' in content:
                    patterns['tmp_users'].append(name)

                if 'data/' in content or 'DATA_DIR' in content:
                    patterns['data_users'].append(name)

                if 'atexit' in content or '__del__' in content or 'cleanup' in content:
                    patterns['proper_cleanup'].append(name)
                elif 'open(' in content or 'mmap' in content:
                    patterns['no_cleanup'].append(name)

            except:
                pass

        return patterns

    def check_resource_usage(self) -> Dict:
        """Verifica uso atual de recursos"""
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return {
            'ram': {
                'total_gb': mem.total / (1024**3),
                'used_gb': (mem.total - mem.available) / (1024**3),
                'available_gb': mem.available / (1024**3),
                'percent': mem.percent
            },
            'disk': {
                'total_gb': disk.total / (1024**3),
                'used_gb': disk.used / (1024**3),
                'free_gb': disk.free / (1024**3),
                'percent': disk.percent
            },
            'tmp_usage': self.check_tmp_usage()
        }

    def check_tmp_usage(self) -> Dict:
        """Verifica uso de /tmp e /private/tmp"""
        tmp_info = {}

        for tmp_dir in ['/tmp', '/private/tmp']:
            if os.path.exists(tmp_dir):
                try:
                    total_size = 0
                    file_count = 0
                    suspicious_files = []

                    for root, dirs, files in os.walk(tmp_dir):
                        for file in files:
                            try:
                                filepath = Path(root) / file
                                size = filepath.stat().st_size
                                total_size += size
                                file_count += 1

                                # Arquivos suspeitos (do Digimundo)
                                if any(pattern in file for pattern in ['mmap', 'memory', 'quantum', 'telepathic', 'akashic']):
                                    suspicious_files.append({
                                        'name': file,
                                        'size_mb': size / (1024**2)
                                    })
                            except:
                                pass

                    tmp_info[tmp_dir] = {
                        'total_gb': total_size / (1024**3),
                        'file_count': file_count,
                        'suspicious_files': suspicious_files[:10]  # Top 10
                    }
                except:
                    tmp_info[tmp_dir] = {'error': 'Cannot access'}

        return tmp_info

    def run_full_simulation(self) -> None:
        """Executa simulação completa de debug"""
        print("🔬 INICIANDO SIMULAÇÃO DE DEBUG COMPLETO")
        print("=" * 60)

        # 1. Testar sistemas de memória
        print("\n📊 Testando sistemas de memória...")
        memory_files = [f.stem for f in self.apps_dir.glob("*memory*.py")]

        for mem_system in memory_files:
            result = self.check_memory_system(mem_system)
            self.results['memory_systems'][mem_system] = result

            if result['status'] == 'BROKEN':
                self.results['critical_issues'].append(f"{mem_system}: {result['issues']}")
            elif result['status'] == 'PROBLEMATIC':
                self.results['warnings'].append(f"{mem_system}: {result['issues']}")

        # 2. Testar sistemas Ollama
        print("\n🦙 Testando sistemas Ollama...")
        ollama_files = [f.stem for f in self.apps_dir.glob("*ollama*.py")]

        for ollama_system in ollama_files:
            result = self.check_ollama_system(ollama_system)
            self.results['ollama_systems'][ollama_system] = result

        # 3. Verificar padrões de criação de arquivos
        print("\n📁 Analisando padrões de criação de arquivos...")
        self.results['file_systems'] = self.check_file_creation_patterns()

        # 4. Verificar recursos
        print("\n💾 Verificando recursos do sistema...")
        self.results['resources'] = self.check_resource_usage()

        # 5. Análise final
        self.analyze_results()

    def analyze_results(self) -> None:
        """Analisa e sumariza resultados"""
        # Contar problemas
        memory_broken = sum(1 for r in self.results['memory_systems'].values() if r['status'] == 'BROKEN')
        memory_problematic = sum(1 for r in self.results['memory_systems'].values() if r['status'] == 'PROBLEMATIC')
        ollama_needs_update = sum(1 for r in self.results['ollama_systems'].values() if r['status'] == 'NEEDS_UPDATE')

        self.results['summary'] = {
            'total_memory_systems': len(self.results['memory_systems']),
            'broken_memory_systems': memory_broken,
            'problematic_memory_systems': memory_problematic,
            'total_ollama_systems': len(self.results['ollama_systems']),
            'ollama_needs_update': ollama_needs_update,
            'files_using_tmp': len(self.results['file_systems']['tmp_users']),
            'files_without_cleanup': len(self.results['file_systems']['no_cleanup']),
            'ram_available_gb': self.results['resources']['ram']['available_gb'],
            'tmp_usage_gb': sum(v.get('total_gb', 0) for v in self.results['resources']['tmp_usage'].values())
        }

    def generate_report(self) -> str:
        """Gera relatório final"""
        report = []
        report.append("# 🔬 RELATÓRIO DE DEBUG SIMULADO DO SISTEMA\n")
        report.append(f"**Timestamp:** {self.results['timestamp']}\n\n")

        # Sumário
        s = self.results.get('summary', {})
        report.append("## 📊 SUMÁRIO EXECUTIVO\n")
        report.append(f"- **Sistemas de memória:** {s.get('total_memory_systems', 0)} total\n")
        report.append(f"  - ❌ Quebrados: {s.get('broken_memory_systems', 0)}\n")
        report.append(f"  - ⚠️ Problemáticos: {s.get('problematic_memory_systems', 0)}\n")
        report.append(f"- **Sistemas Ollama:** {s.get('ollama_needs_update', 0)} precisam atualização\n")
        report.append(f"- **Arquivos usando /tmp:** {s.get('files_using_tmp', 0)}\n")
        report.append(f"- **Arquivos sem cleanup:** {s.get('files_without_cleanup', 0)}\n")
        report.append(f"- **RAM disponível:** {s.get('ram_available_gb', 0):.1f}GB\n")
        report.append(f"- **Uso de /tmp:** {s.get('tmp_usage_gb', 0):.1f}GB\n\n")

        # Problemas críticos
        if self.results['critical_issues']:
            report.append("## 🚨 PROBLEMAS CRÍTICOS\n")
            for issue in self.results['critical_issues']:
                report.append(f"- {issue}\n")
            report.append("\n")

        # Avisos
        if self.results['warnings']:
            report.append("## ⚠️ AVISOS\n")
            for warning in self.results['warnings'][:10]:
                report.append(f"- {warning}\n")
            report.append("\n")

        # Sistemas de memória problemáticos
        report.append("## 💾 SISTEMAS DE MEMÓRIA COM PROBLEMAS\n")
        for name, data in self.results['memory_systems'].items():
            if data['status'] in ['BROKEN', 'PROBLEMATIC']:
                report.append(f"\n### {name}\n")
                report.append(f"- Status: {data['status']}\n")
                for issue in data['issues']:
                    report.append(f"- {issue}\n")
                if data['file_creation']:
                    for fc in data['file_creation']:
                        report.append(f"- Cria: {fc['type']} ({fc.get('size_gb', '?')}GB)\n")

        # Recomendações
        report.append("\n## 💡 AÇÕES RECOMENDADAS\n")
        report.append("1. **URGENTE:** Corrigir paths /tmp em todos os sistemas de memória\n")
        report.append("2. **URGENTE:** Implementar cleanup automático de mmap files\n")
        report.append("3. **IMPORTANTE:** Atualizar configuração Ollama para híbrida\n")
        report.append("4. **IMPORTANTE:** Limitar tamanho de mmap para 100MB máximo\n")
        report.append("5. **MÉDIO:** Criar diretório data/memory/ centralizado\n")

        return '\n'.join(report)


def main():
    simulator = SystemDebugSimulator()

    print("🔬 Iniciando simulação de debug...")
    simulator.run_full_simulation()

    # Gerar relatório
    report = simulator.generate_report()

    # Salvar relatório
    report_path = Path("/Users/clubproducoes/Digimundo/claude_code/memory/DEBUG_SIMULATION_REPORT.md")
    report_path.write_text(report)

    # Salvar JSON detalhado
    json_path = Path("/Users/clubproducoes/Digimundo/claude_code/memory/debug_simulation_results.json")
    with open(json_path, 'w') as f:
        json.dump(simulator.results, f, indent=2, default=str)

    print(f"\n✅ Relatório salvo em: {report_path}")
    print(f"✅ JSON detalhado em: {json_path}")

    print("\n" + "="*60)
    print(report)

    return simulator.results


if __name__ == "__main__":
    main()