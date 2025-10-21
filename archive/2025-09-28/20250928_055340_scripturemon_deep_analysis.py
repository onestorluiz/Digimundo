#!/usr/bin/env python3
"""
SCRIPTUREMON DEEP ANALYSIS & REORGANIZATION SYSTEM
Análise profunda de CADA arquivo do sistema para reorganização densa
"""

import os
import sys
import json
import shutil
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import ollama

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class ScripturemonDeepAnalyzer:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")
        self.analysis_results = []
        self.reorganization_plan = {}
        self.categories = {
            'core_system': [],      # Arquivos centrais do sistema
            'models': [],           # Modelos e modelfiles
            'memories': [],         # Sistema de memórias
            'tests': [],            # Testes de todos os tipos
            'analysis': [],         # Análises e resultados
            'documentation': [],    # Documentação e READMEs
            'scripts': [],          # Scripts auxiliares
            'knowledge': [],        # Base de conhecimento
            'archived': [],         # Arquivos obsoletos/antigos
            'temporary': [],        # Arquivos temporários
            'duplicates': [],       # Arquivos duplicados
            'misplaced': [],        # Arquivos fora do lugar
            'unknown': []           # Arquivos de propósito desconhecido
        }

    def analyze_file_purpose(self, file_path: Path) -> Dict:
        """Analisa profundamente o propósito e integração de um arquivo"""
        analysis = {
            'path': str(file_path.relative_to(self.base_path)),
            'name': file_path.name,
            'size': file_path.stat().st_size if file_path.is_file() else 0,
            'type': self.detect_file_type(file_path),
            'integrated': False,
            'useful': False,
            'correct_location': False,
            'suggested_location': None,
            'reason': '',
            'action': 'keep',  # keep, move, archive, delete
            'dependencies': []
        }

        # Análise por tipo de arquivo
        if file_path.is_file():
            # Python files
            if file_path.suffix == '.py':
                analysis.update(self.analyze_python_file(file_path))
            # Shell scripts
            elif file_path.suffix == '.sh':
                analysis.update(self.analyze_shell_script(file_path))
            # JSON files
            elif file_path.suffix == '.json':
                analysis.update(self.analyze_json_file(file_path))
            # Database files
            elif file_path.suffix == '.db':
                analysis.update(self.analyze_database_file(file_path))
            # Documentation
            elif file_path.suffix in ['.md', '.txt', '.rst']:
                analysis.update(self.analyze_documentation(file_path))
            # Log files
            elif file_path.suffix == '.log' or 'log' in file_path.name:
                analysis.update(self.analyze_log_file(file_path))
            # Test files
            elif 'test' in file_path.name.lower():
                analysis.update(self.analyze_test_file(file_path))

        return analysis

    def detect_file_type(self, file_path: Path) -> str:
        """Detecta o tipo/categoria do arquivo"""
        name_lower = file_path.name.lower()

        # Core system files
        if any(core in name_lower for core in ['scripturemon_ultimate', 'main', 'cli', '__init__']):
            return 'core_system'

        # Models
        if 'modelfile' in name_lower or file_path.parent.name == 'modelfiles':
            return 'models'

        # Memories
        if any(mem in name_lower for mem in ['memory', 'memories', 'unified_memory']):
            return 'memories'

        # Tests
        if 'test' in name_lower or file_path.parent.name == 'tests':
            return 'tests'

        # Analysis
        if any(ana in name_lower for ana in ['analysis', 'result', 'report']):
            return 'analysis'

        # Documentation
        if file_path.suffix in ['.md', '.rst'] or name_lower in ['readme', 'license']:
            return 'documentation'

        # Scripts
        if file_path.suffix in ['.sh', '.py'] and not any(x in name_lower for x in ['test', 'main']):
            return 'scripts'

        # Knowledge
        if any(know in name_lower for know in ['knowledge', 'content', 'theory', 'screenplay']):
            return 'knowledge'

        # Archives
        if any(arch in name_lower for arch in ['old', 'backup', 'archive', 'deprecated']):
            return 'archived'

        # Temporary
        if any(temp in name_lower for temp in ['temp', 'tmp', 'cache']):
            return 'temporary'

        return 'unknown'

    def analyze_python_file(self, file_path: Path) -> Dict:
        """Analisa arquivo Python específico"""
        updates = {}
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            # Verifica imports
            imports = [line for line in content.split('\n') if line.strip().startswith(('import ', 'from '))]
            updates['dependencies'] = imports[:5]  # Primeiros 5 imports

            # Verifica se é teste
            if 'test' in file_path.name.lower():
                updates['suggested_location'] = 'tests/'
                updates['useful'] = 'assert' in content or 'unittest' in content

            # Verifica se é parte core do sistema
            elif 'class Scripturemon' in content or 'def main(' in content:
                updates['integrated'] = True
                updates['useful'] = True
                updates['correct_location'] = True

            # Verifica duplicação
            elif self.check_duplicate_functionality(file_path, content):
                updates['action'] = 'archive'
                updates['reason'] = 'Funcionalidade duplicada'

        except Exception as e:
            updates['reason'] = f'Erro ao analisar: {str(e)}'

        return updates

    def analyze_shell_script(self, file_path: Path) -> Dict:
        """Analisa scripts shell"""
        updates = {}
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            # Scripts de teste
            if 'test' in file_path.name.lower():
                updates['suggested_location'] = 'scripts/tests/'
                updates['useful'] = True

            # Scripts de organização
            elif 'organize' in file_path.name.lower() or 'clean' in file_path.name.lower():
                updates['suggested_location'] = 'scripts/maintenance/'
                updates['useful'] = True
                updates['integrated'] = 'scripturemon' in content.lower()

        except:
            pass

        return updates

    def analyze_json_file(self, file_path: Path) -> Dict:
        """Analisa arquivos JSON"""
        updates = {}
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Análises e resultados
            if 'analysis' in file_path.name.lower() or 'result' in file_path.name.lower():
                updates['suggested_location'] = 'analysis/results/'
                # Arquivos antigos (>7 dias) vão para archive
                if (datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)).days > 7:
                    updates['action'] = 'archive'
                    updates['reason'] = 'Resultado antigo de análise'

        except:
            updates['action'] = 'delete'
            updates['reason'] = 'JSON corrompido ou inválido'

        return updates

    def analyze_database_file(self, file_path: Path) -> Dict:
        """Analisa arquivos de banco de dados"""
        updates = {}

        if 'unified_memory' in file_path.name:
            updates['integrated'] = True
            updates['useful'] = True
            updates['correct_location'] = str(file_path.parent).endswith('data')
            updates['suggested_location'] = 'data/memories/' if not updates['correct_location'] else None

        return updates

    def analyze_documentation(self, file_path: Path) -> Dict:
        """Analisa documentação"""
        updates = {}

        if file_path.name.upper() == 'README.MD':
            updates['integrated'] = True
            updates['useful'] = True
            updates['correct_location'] = file_path.parent == self.base_path

        return updates

    def analyze_log_file(self, file_path: Path) -> Dict:
        """Analisa arquivos de log"""
        updates = {}

        # Logs antigos podem ser arquivados
        if (datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)).days > 3:
            updates['action'] = 'archive'
            updates['reason'] = 'Log antigo'
            updates['suggested_location'] = 'archive/logs/'

        return updates

    def analyze_test_file(self, file_path: Path) -> Dict:
        """Analisa arquivos de teste"""
        updates = {
            'suggested_location': 'tests/',
            'useful': True
        }

        # Testes com resultado podem ir para archive
        if any(result in file_path.name for result in ['result', 'output', 'log']):
            if (datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)).days > 1:
                updates['action'] = 'archive'
                updates['reason'] = 'Resultado de teste antigo'

        return updates

    def check_duplicate_functionality(self, file_path: Path, content: str) -> bool:
        """Verifica se há funcionalidade duplicada"""
        # Lista de padrões conhecidos de duplicação
        duplicate_patterns = [
            ('test_autonomy', 'test_self_organization'),
            ('clean_database', 'database_cleanup'),
            ('organize_files', 'auto_organize'),
        ]

        for pattern1, pattern2 in duplicate_patterns:
            if pattern1 in file_path.name and pattern2 in str(list(self.base_path.glob(f'**/*{pattern2}*'))):
                return True

        return False

    def scan_all_files(self):
        """Escaneia TODOS os arquivos do sistema"""
        print("🔍 Iniciando análise profunda de TODOS os arquivos...")
        print("=" * 60)

        all_files = list(self.base_path.rglob('*'))
        total = len(all_files)

        for idx, file_path in enumerate(all_files, 1):
            # Pula diretórios especiais
            if any(skip in str(file_path) for skip in ['.git', '__pycache__', '.DS_Store', 'node_modules']):
                continue

            print(f"Analisando [{idx}/{total}]: {file_path.name}")

            analysis = self.analyze_file_purpose(file_path)
            self.analysis_results.append(analysis)

            # Categoriza o arquivo
            category = analysis['type']
            if category in self.categories:
                self.categories[category].append(analysis)
            else:
                self.categories['unknown'].append(analysis)

    def generate_reorganization_plan(self):
        """Gera plano de reorganização densa"""
        print("\n" + "=" * 60)
        print("📋 PLANO DE REORGANIZAÇÃO DENSA")
        print("=" * 60)

        self.reorganization_plan = {
            'to_move': [],
            'to_archive': [],
            'to_delete': [],
            'to_consolidate': [],
            'new_structure': {}
        }

        for analysis in self.analysis_results:
            # Arquivos para mover
            if analysis['suggested_location'] and analysis['action'] == 'keep':
                self.reorganization_plan['to_move'].append({
                    'from': analysis['path'],
                    'to': analysis['suggested_location'] + analysis['name'],
                    'reason': analysis.get('reason', 'Melhor organização')
                })

            # Arquivos para arquivar
            elif analysis['action'] == 'archive':
                self.reorganization_plan['to_archive'].append({
                    'file': analysis['path'],
                    'reason': analysis['reason']
                })

            # Arquivos para deletar
            elif analysis['action'] == 'delete':
                self.reorganization_plan['to_delete'].append({
                    'file': analysis['path'],
                    'reason': analysis['reason']
                })

        # Propõe nova estrutura
        self.reorganization_plan['new_structure'] = {
            '📦 src/': 'Código fonte principal do sistema',
            '🧠 models/': 'Modelfiles e configurações Ollama',
            '💾 data/': {
                'memories/': 'Banco de dados de memórias',
                'knowledge/': 'Base de conhecimento',
                'cache/': 'Cache temporário'
            },
            '🧪 tests/': 'Todos os testes',
            '📊 analysis/': {
                'results/': 'Resultados de análises',
                'reports/': 'Relatórios gerados'
            },
            '🔧 scripts/': {
                'maintenance/': 'Scripts de manutenção',
                'automation/': 'Scripts de automação',
                'tests/': 'Scripts de teste'
            },
            '📚 docs/': 'Toda documentação',
            '🗄️ archive/': {
                'old_versions/': 'Versões antigas',
                'logs/': 'Logs antigos',
                'results/': 'Resultados antigos'
            },
            '🗑️ trash/': 'Lixeira do sistema'
        }

        return self.reorganization_plan

    def generate_report(self):
        """Gera relatório detalhado da análise"""
        timestamp = datetime.now().isoformat()

        report = {
            'timestamp': timestamp,
            'total_files_analyzed': len(self.analysis_results),
            'categories': {k: len(v) for k, v in self.categories.items()},
            'issues_found': {
                'misplaced_files': len([a for a in self.analysis_results if a['suggested_location']]),
                'obsolete_files': len([a for a in self.analysis_results if a['action'] == 'archive']),
                'useless_files': len([a for a in self.analysis_results if a['action'] == 'delete']),
                'duplicates': len(self.categories['duplicates'])
            },
            'reorganization_plan': self.reorganization_plan,
            'detailed_analysis': self.analysis_results
        }

        # Salva relatório
        report_path = self.base_path / f'deep_analysis_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n📊 Relatório salvo em: {report_path}")

        # Exibe resumo
        print("\n" + "=" * 60)
        print("📈 RESUMO DA ANÁLISE PROFUNDA")
        print("=" * 60)
        print(f"Total de arquivos analisados: {report['total_files_analyzed']}")
        print("\nCategorias identificadas:")
        for cat, count in report['categories'].items():
            if count > 0:
                print(f"  • {cat}: {count} arquivos")

        print("\nProblemas encontrados:")
        for issue, count in report['issues_found'].items():
            if count > 0:
                print(f"  ⚠️ {issue}: {count}")

        print("\nAções recomendadas:")
        print(f"  📦 Mover: {len(self.reorganization_plan['to_move'])} arquivos")
        print(f"  🗄️ Arquivar: {len(self.reorganization_plan['to_archive'])} arquivos")
        print(f"  🗑️ Deletar: {len(self.reorganization_plan['to_delete'])} arquivos")

        return report

    def ask_scripturemon_opinion(self, file_info: Dict) -> str:
        """Pergunta ao Scripturemon sua opinião sobre um arquivo"""
        try:
            prompt = f"""
            Analisando arquivo do seu próprio sistema:
            - Nome: {file_info['name']}
            - Caminho: {file_info['path']}
            - Tipo: {file_info['type']}

            Perguntas:
            1. Este arquivo está integrado ao sistema?
            2. Ele tem utilidade atual?
            3. Está no lugar correto?
            4. Deve ser mantido, movido, arquivado ou deletado?

            Responda em JSON com: integrated, useful, correct_location, action, reason
            """

            response = ollama.generate(
                model='scripturemon-ultimate',
                prompt=prompt
            )

            return response['response']
        except:
            return "{}"

def main():
    print("🤖 SCRIPTUREMON DEEP ANALYSIS SYSTEM")
    print("Análise profunda e reorganização densa")
    print("=" * 60)

    analyzer = ScripturemonDeepAnalyzer()

    # 1. Escaneia todos os arquivos
    analyzer.scan_all_files()

    # 2. Gera plano de reorganização
    plan = analyzer.generate_reorganization_plan()

    # 3. Gera relatório completo
    report = analyzer.generate_report()

    print("\n✅ Análise completa! Revise o relatório para executar a reorganização.")

    # Pergunta se deve executar
    response = input("\n🤔 Deseja que o Scripturemon execute a reorganização? (s/n): ")
    if response.lower() == 's':
        print("\n🚀 Executando reorganização densa...")
        # Aqui chamaria o scripturemon_command_bridge.py para executar
        from scripturemon_command_bridge import ScripturemonCommandBridge
        bridge = ScripturemonCommandBridge()

        # Executa movimentos
        for move in plan['to_move'][:5]:  # Limita a 5 para teste
            print(f"Movendo: {move['from']} → {move['to']}")
            bridge.execute_command('move', source=move['from'], destination=move['to'])

        print("\n✅ Reorganização inicial executada!")

if __name__ == "__main__":
    main()