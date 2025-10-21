#!/usr/bin/env python3
"""
🔍 ANÁLISE COMPLETA: ONDE CADA SISTEMA ESTÁ CRIANDO ARQUIVOS
Objetivo: Descobrir todos os locais onde arquivos estão sendo criados
"""

import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Tuple
import json

class FileLocationAnalyzer:
    def __init__(self):
        self.base_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        self.apps_dir = self.base_dir / "apps" / "scripturemon"
        self.problematic_patterns = {
            '/tmp': [],
            '/private/tmp': [],
            'tempfile': [],
            'mmap': [],
            'sqlite': [],
            'json_files': [],
            'csv_files': [],
            'pickle_files': [],
            'numpy_files': [],
            'torch_files': []
        }

    def analyze_file(self, filepath: Path) -> Dict:
        """Analisa um arquivo Python em busca de criação de arquivos"""
        results = {
            'file': str(filepath),
            'locations': [],
            'problems': []
        }

        try:
            with open(filepath, 'r') as f:
                content = f.read()

            # Buscar padrões problemáticos
            patterns = [
                (r'/tmp/[\w_]+', 'hardcoded_tmp'),
                (r'/private/tmp/[\w_]+', 'hardcoded_private_tmp'),
                (r'tempfile\.\w+', 'tempfile_usage'),
                (r'mmap\.mmap', 'mmap_usage'),
                (r'open\([^,]+,\s*[\'"]w', 'file_write'),
                (r'sqlite3\.connect', 'sqlite_connection'),
                (r'\.to_csv\(', 'csv_write'),
                (r'\.to_json\(', 'json_write'),
                (r'pickle\.dump', 'pickle_write'),
                (r'np\.save', 'numpy_save'),
                (r'torch\.save', 'torch_save'),
                (r'Path\([\'"][^\'"]*/tmp', 'path_tmp'),
                (r'os\.makedirs', 'creating_dirs'),
                (r'os\.mkdir', 'creating_dir'),
            ]

            for pattern, problem_type in patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    # Encontrar número da linha
                    line_num = content[:match.start()].count('\n') + 1
                    results['locations'].append({
                        'type': problem_type,
                        'line': line_num,
                        'text': match.group(0),
                        'context': content[max(0, match.start()-50):min(len(content), match.end()+50)]
                    })

            # Busca específica por storage_path em __init__
            init_pattern = r'def __init__.*storage_path[^)]+\):'
            init_matches = re.finditer(init_pattern, content, re.MULTILINE | re.DOTALL)
            for match in init_matches:
                # Extrair valor padrão
                storage_match = re.search(r'storage_path:\s*str\s*=\s*[\'"]([^\'\"]+)[\'"]', match.group(0))
                if storage_match:
                    path = storage_match.group(1)
                    if '/tmp' in path or '/private/tmp' in path:
                        line_num = content[:match.start()].count('\n') + 1
                        results['problems'].append({
                            'severity': 'CRITICAL',
                            'issue': f'Hardcoded /tmp path in __init__',
                            'path': path,
                            'line': line_num
                        })

            # Busca por criação de arquivos gigantes
            mmap_size_pattern = r'(\d+)\s*\*\s*1024\s*\*\s*1024\s*\*\s*1024'  # GB
            size_matches = re.finditer(mmap_size_pattern, content)
            for match in size_matches:
                size_gb = int(match.group(1))
                if size_gb >= 1:
                    line_num = content[:match.start()].count('\n') + 1
                    results['problems'].append({
                        'severity': 'HIGH',
                        'issue': f'Creating {size_gb}GB file',
                        'line': line_num
                    })

        except Exception as e:
            results['error'] = str(e)

        return results

    def scan_all_systems(self) -> Dict:
        """Varre todos os sistemas Python"""
        all_results = {
            'memory_systems': {},
            'ollama_systems': {},
            'other_systems': {},
            'summary': {
                'total_files': 0,
                'problematic_files': 0,
                'tmp_users': [],
                'mmap_users': [],
                'large_file_creators': []
            }
        }

        # Listar todos os arquivos Python
        python_files = list(self.apps_dir.glob("*.py"))

        for py_file in python_files:
            if py_file.name.startswith('__'):
                continue

            results = self.analyze_file(py_file)

            # Categorizar
            if 'memory' in py_file.name.lower():
                all_results['memory_systems'][py_file.name] = results
            elif 'ollama' in py_file.name.lower():
                all_results['ollama_systems'][py_file.name] = results
            else:
                all_results['other_systems'][py_file.name] = results

            # Atualizar sumário
            all_results['summary']['total_files'] += 1

            if results['problems']:
                all_results['summary']['problematic_files'] += 1

            for problem in results.get('problems', []):
                if '/tmp' in str(problem.get('path', '')):
                    all_results['summary']['tmp_users'].append(py_file.name)
                if problem.get('issue', '').startswith('Creating'):
                    all_results['summary']['large_file_creators'].append({
                        'file': py_file.name,
                        'size': problem['issue']
                    })

        return all_results

    def check_actual_files(self) -> Dict:
        """Verifica arquivos realmente criados no sistema"""
        locations = {
            '/tmp': [],
            '/private/tmp': [],
            str(self.base_dir / 'data'): [],
            str(self.base_dir / 'cache'): [],
            str(self.base_dir / 'memory'): [],
            str(self.base_dir / 'temp'): []
        }

        for location in locations:
            if os.path.exists(location):
                try:
                    # Listar arquivos suspeitos
                    path = Path(location)
                    patterns = ['*.mmap', '*.db', '*.sqlite', '*.pkl', '*.npy', '*.pt']
                    for pattern in patterns:
                        files = list(path.glob(pattern))
                        for f in files:
                            if f.stat().st_size > 1024*1024:  # Maior que 1MB
                                locations[location].append({
                                    'file': f.name,
                                    'size_mb': f.stat().st_size / (1024*1024),
                                    'modified': f.stat().st_mtime
                                })
                except PermissionError:
                    locations[location].append({'error': 'Permission denied'})

        return locations

    def generate_report(self) -> str:
        """Gera relatório completo"""
        print("🔍 Iniciando análise de localização de arquivos...")

        # Análise de código
        code_analysis = self.scan_all_systems()

        # Verificação de arquivos reais
        actual_files = self.check_actual_files()

        report = []
        report.append("# 🔍 ANÁLISE COMPLETA: ONDE OS SISTEMAS ESTÃO CRIANDO ARQUIVOS\n")
        from datetime import datetime
        report.append(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        report.append(f"**Sistemas analisados:** {code_analysis['summary']['total_files']}\n")
        report.append(f"**Sistemas problemáticos:** {code_analysis['summary']['problematic_files']}\n\n")

        # Problemas críticos
        report.append("## 🚨 PROBLEMAS CRÍTICOS ENCONTRADOS\n\n")

        # Sistemas de memória com problemas
        report.append("### SISTEMAS DE MEMÓRIA QUE USAM /tmp:\n")
        for name, data in code_analysis['memory_systems'].items():
            if data.get('problems'):
                report.append(f"\n**{name}:**\n")
                for problem in data['problems']:
                    report.append(f"- Linha {problem['line']}: {problem['issue']}\n")
                    if 'path' in problem:
                        report.append(f"  Path: `{problem['path']}`\n")

        # Criadores de arquivos grandes
        if code_analysis['summary']['large_file_creators']:
            report.append("\n### SISTEMAS CRIANDO ARQUIVOS GIGANTES:\n")
            for creator in code_analysis['summary']['large_file_creators']:
                report.append(f"- {creator['file']}: {creator['size']}\n")

        # Arquivos reais encontrados
        report.append("\n## 📁 ARQUIVOS ENCONTRADOS NO SISTEMA:\n")
        for location, files in actual_files.items():
            if files:
                report.append(f"\n### {location}:\n")
                total_size = sum(f.get('size_mb', 0) for f in files if 'size_mb' in f)
                report.append(f"Total: {total_size:.1f}MB em {len(files)} arquivos\n")
                for f in sorted(files, key=lambda x: x.get('size_mb', 0), reverse=True)[:10]:
                    if 'size_mb' in f:
                        report.append(f"- {f['file']}: {f['size_mb']:.1f}MB\n")

        # Recomendações
        report.append("\n## 💡 CORREÇÕES NECESSÁRIAS:\n\n")
        report.append("### 1. MUDAR TODOS OS PATHS DE /tmp PARA:\n")
        report.append("```python\n")
        report.append("from pathlib import Path\n")
        report.append("BASE_DIR = Path(__file__).parent.parent.parent\n")
        report.append("DATA_DIR = BASE_DIR / 'data'\n")
        report.append("MEMORY_DIR = DATA_DIR / 'memory'\n")
        report.append("CACHE_DIR = DATA_DIR / 'cache'\n")
        report.append("\n# Em vez de:\n")
        report.append("storage_path = '/tmp/algo'\n")
        report.append("\n# Usar:\n")
        report.append("storage_path = str(MEMORY_DIR / 'algo')\n")
        report.append("```\n\n")

        report.append("### 2. ADICIONAR LIMPEZA AUTOMÁTICA:\n")
        report.append("```python\n")
        report.append("import atexit\n")
        report.append("import shutil\n\n")
        report.append("def cleanup():\n")
        report.append("    if self.temp_dir.exists():\n")
        report.append("        shutil.rmtree(self.temp_dir)\n\n")
        report.append("atexit.register(cleanup)\n")
        report.append("```\n\n")

        report.append("### 3. LIMITAR TAMANHO DE MMAP:\n")
        report.append("```python\n")
        report.append("# Em vez de 3GB:\n")
        report.append("MAX_MMAP_SIZE = 100 * 1024 * 1024  # 100MB máximo\n")
        report.append("```\n")

        return '\n'.join(report)


def main():
    analyzer = FileLocationAnalyzer()
    report = analyzer.generate_report()

    # Salvar relatório
    report_path = Path("/Users/clubproducoes/Digimundo/claude_code/memory/FILE_LOCATION_ANALYSIS.md")
    report_path.write_text(report)

    print(f"\n✅ Relatório salvo em: {report_path}")
    print("\n" + "="*60)
    print(report[:2000])  # Primeiras 2000 chars
    print("...\n[Relatório completo salvo no arquivo]")

    return report_path


if __name__ == "__main__":
    main()