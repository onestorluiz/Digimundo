#!/usr/bin/env python3
"""
🔍 ANÁLISE PROFUNDA E REORGANIZAÇÃO DA ESTRUTURA DO PROJETO
===========================================================
Analisa cada arquivo pelo conteúdo e data, não apenas nome
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json
import hashlib
from typing import Dict, List, Tuple

class DeepStructureAnalyzer:
    def __init__(self):
        self.root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        self.analysis = {
            'active_files': [],      # Arquivos recentemente modificados e usados
            'stale_files': [],       # Arquivos não modificados há muito tempo
            'duplicate_content': [], # Arquivos com conteúdo duplicado
            'empty_files': [],       # Arquivos vazios ou quase vazios
            'misplaced_files': [],   # Arquivos no lugar errado
            'structure_issues': [],  # Problemas de organização
        }
        self.file_hashes = {}  # Para detectar duplicatas

    def analyze_file_age(self, file_path: Path) -> Dict:
        """Analisa idade e atividade de um arquivo"""
        try:
            stat = file_path.stat()
            modified = datetime.fromtimestamp(stat.st_mtime)
            created = datetime.fromtimestamp(stat.st_ctime)
            size = stat.st_size

            days_since_modified = (datetime.now() - modified).days

            return {
                'path': str(file_path.relative_to(self.root)),
                'size': size,
                'modified': modified.isoformat(),
                'created': created.isoformat(),
                'days_old': days_since_modified,
                'is_stale': days_since_modified > 30,  # Não modificado há mais de 30 dias
                'is_empty': size < 10,  # Arquivo praticamente vazio
            }
        except:
            return None

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calcula hash do conteúdo para detectar duplicatas"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except:
            return None

    def analyze_imports(self, file_path: Path) -> List[str]:
        """Analisa imports de um arquivo Python"""
        imports = []
        try:
            if file_path.suffix == '.py':
                content = file_path.read_text(encoding='utf-8')
                for line in content.split('\n'):
                    if line.startswith('import ') or line.startswith('from '):
                        imports.append(line.strip())
        except:
            pass
        return imports

    def check_file_location(self, file_path: Path) -> str:
        """Verifica se arquivo está no lugar correto"""
        name = file_path.name
        parent = file_path.parent.name

        # Regras de localização
        if name.startswith('test_') and parent != 'tests':
            return 'test_file_not_in_tests'
        elif name.endswith('_test.py') and parent != 'tests':
            return 'test_file_not_in_tests'
        elif 'config' in name.lower() and parent not in ['config', 'core']:
            return 'config_file_misplaced'
        elif name.endswith('.md') and parent not in ['docs', 'scripturemon-champion']:
            return 'documentation_misplaced'
        elif 'script' in name and parent not in ['scripts', 'core']:
            return 'script_misplaced'

        return 'correct'

    def analyze_src_structure(self):
        """Analisa estrutura de src/ em detalhe"""
        print("\n📂 ANALISANDO ESTRUTURA DE SRC/")
        print("=" * 60)

        src_path = self.root / 'src'

        # Analisar cada subpasta
        for subdir in ['core', 'advanced', 'learning']:
            subdir_path = src_path / subdir
            if subdir_path.exists():
                py_files = list(subdir_path.glob('*.py'))
                print(f"\n📁 src/{subdir}/: {len(py_files)} arquivos")

                # Analisar cada arquivo
                for file_path in py_files[:5]:  # Primeiros 5 como amostra
                    info = self.analyze_file_age(file_path)
                    if info:
                        status = "✅" if not info['is_stale'] else "⚠️"
                        print(f"  {status} {file_path.name:30} {info['days_old']} dias")

                        # Verificar se tem imports corretos
                        imports = self.analyze_imports(file_path)
                        broken_imports = [i for i in imports if 'apps.scripturemon' in i]
                        if broken_imports:
                            print(f"     ❌ Import quebrado: {broken_imports[0]}")

    def analyze_scripts_folder(self):
        """Analisa pasta scripts/ em detalhe"""
        print("\n📂 ANALISANDO PASTA SCRIPTS/")
        print("=" * 60)

        scripts_path = self.root / 'scripts'
        py_files = list(scripts_path.glob('*.py'))

        # Categorizar scripts
        categories = {
            'migration': [],
            'test': [],
            'analysis': [],
            'cleanup': [],
            'build': [],
            'other': []
        }

        for file_path in py_files:
            name = file_path.name.lower()
            info = self.analyze_file_age(file_path)

            if 'migrate' in name or 'migration' in name or 'unify' in name:
                categories['migration'].append(info)
            elif 'test' in name:
                categories['test'].append(info)
            elif 'analyze' in name or 'analysis' in name:
                categories['analysis'].append(info)
            elif 'clean' in name or 'remove' in name:
                categories['cleanup'].append(info)
            elif 'build' in name or 'create' in name:
                categories['build'].append(info)
            else:
                categories['other'].append(info)

        # Mostrar resultados
        for category, files in categories.items():
            if files:
                recent = [f for f in files if f and not f['is_stale']]
                stale = [f for f in files if f and f['is_stale']]
                print(f"\n{category.upper()}: {len(files)} arquivos")
                print(f"  ✅ Recentes: {len(recent)}")
                if stale:
                    print(f"  ⚠️ Antigos: {len(stale)}")
                    for f in stale[:3]:
                        print(f"     - {Path(f['path']).name} ({f['days_old']} dias)")

    def check_duplicate_functionality(self):
        """Detecta arquivos com funcionalidade duplicada"""
        print("\n🔍 DETECTANDO DUPLICAÇÕES")
        print("=" * 60)

        # Padrões de duplicação comuns
        patterns = {
            'memory': [],
            'unified': [],
            'test': [],
            'analyze': [],
            'cleanup': [],
            'import': []
        }

        for py_file in self.root.rglob('*.py'):
            if 'Pre_Limpeza' in str(py_file):
                continue

            name = py_file.name.lower()

            for pattern in patterns:
                if pattern in name:
                    patterns[pattern].append(py_file)

        # Mostrar duplicações
        for pattern, files in patterns.items():
            if len(files) > 2:
                print(f"\n'{pattern}' aparece em {len(files)} arquivos:")
                for f in files[:5]:
                    info = self.analyze_file_age(f)
                    if info:
                        age_info = f"({info['days_old']}d)"
                        print(f"  - {f.parent.name}/{f.name} {age_info}")

    def analyze_data_folder(self):
        """Analisa pasta data/ em detalhe"""
        print("\n📂 ANALISANDO PASTA DATA/")
        print("=" * 60)

        data_path = self.root / 'data'

        # Verificar subpastas
        subdirs = [d for d in data_path.iterdir() if d.is_dir()]

        print(f"Subpastas: {len(subdirs)}")
        for subdir in subdirs:
            files = list(subdir.iterdir())
            total_size = sum(f.stat().st_size for f in files if f.is_file()) / 1024 / 1024

            # Verificar idade
            if files:
                latest = max(f.stat().st_mtime for f in files if f.is_file())
                days_old = (datetime.now() - datetime.fromtimestamp(latest)).days

                status = "✅" if days_old < 7 else "⚠️" if days_old < 30 else "❌"
                print(f"  {status} {subdir.name:20} {len(files)} arquivos, {total_size:.1f}MB, {days_old}d")

                if days_old > 30:
                    self.analysis['stale_files'].append({
                        'path': str(subdir.relative_to(self.root)),
                        'days_old': days_old,
                        'size_mb': total_size
                    })

    def analyze_docs_folder(self):
        """Analisa documentação"""
        print("\n📂 ANALISANDO DOCUMENTAÇÃO")
        print("=" * 60)

        docs_path = self.root / 'docs'
        md_files = list(docs_path.glob('*.md'))

        # Categorizar docs
        categories = {
            'system': [],
            'phase': [],
            'report': [],
            'analysis': [],
            'config': [],
            'other': []
        }

        for doc in md_files:
            name = doc.name.upper()
            info = self.analyze_file_age(doc)

            if 'SYSTEM' in name or 'UNIFIED' in name:
                categories['system'].append(info)
            elif 'PHASE' in name or 'FASE' in name:
                categories['phase'].append(info)
            elif 'REPORT' in name or 'RESULTADO' in name:
                categories['report'].append(info)
            elif 'ANALYSIS' in name or 'ANALISE' in name:
                categories['analysis'].append(info)
            else:
                categories['other'].append(info)

        # Mostrar categorias
        for cat, docs in categories.items():
            if docs:
                print(f"\n{cat.upper()}: {len(docs)} documentos")
                recent = [d for d in docs if d and d['days_old'] < 7]
                if recent:
                    print(f"  📝 Recentes ({len(recent)}):")
                    for d in recent[:3]:
                        print(f"     - {Path(d['path']).name}")

    def suggest_new_structure(self):
        """Sugere nova estrutura otimizada"""
        print("\n" + "=" * 60)
        print("🏗️ ESTRUTURA OTIMIZADA SUGERIDA")
        print("=" * 60)

        suggestion = """
scripturemon-champion/
│
├── src/                      # Código fonte principal
│   ├── core/                 # Sistema principal (manter)
│   │   ├── __init__.py
│   │   ├── script_doctor_system.py
│   │   ├── unified_memory_system.py
│   │   └── screenplay_library.py
│   │
│   ├── features/             # Renomear 'advanced' → 'features'
│   │   ├── rag_system.py
│   │   ├── chat_assistant.py
│   │   └── deep_reflection.py
│   │
│   └── ml/                   # Renomear 'learning' → 'ml'
│       ├── trainer.py
│       ├── consciousness.py
│       └── evolution.py
│
├── scripts/
│   ├── active/               # Scripts em uso ativo
│   │   ├── test_unified_memory.py
│   │   ├── quick_deep_learning.py
│   │   └── analyze_system.py
│   │
│   └── archive/              # Scripts antigos/migração
│       └── [scripts com >30 dias]
│
├── data/
│   ├── unified_memory.db    # Banco único
│   ├── pdfs/                # PDFs originais
│   ├── screenplays/         # TXTs convertidos
│   └── models/              # Modelfiles
│
├── docs/
│   ├── current/             # Documentação ativa
│   │   ├── README.md
│   │   ├── CLAUDE.md
│   │   └── SYSTEM_ARCHITECTURE.md
│   │
│   └── archive/             # Docs antigas/relatórios
│       └── [docs com >30 dias]
│
├── tests/                    # Testes ativos
│   ├── test_system_minimal.py
│   └── test_integration.py
│
├── config/                   # Configurações
│   └── settings.yaml
│
└── digilibrary/             # Biblioteca de roteiros (manter)
        """

        print(suggestion)

        return suggestion

    def create_reorganization_script(self):
        """Cria script para reorganizar projeto"""
        script = '''#!/usr/bin/env python3
"""
🏗️ REORGANIZAÇÃO ESTRUTURAL DO PROJETO
"""

import shutil
from pathlib import Path

def reorganize_project():
    root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")

    # Criar novas estruturas
    (root / "src" / "features").mkdir(exist_ok=True)
    (root / "src" / "ml").mkdir(exist_ok=True)
    (root / "scripts" / "active").mkdir(exist_ok=True)
    (root / "scripts" / "archive").mkdir(exist_ok=True)
    (root / "docs" / "current").mkdir(exist_ok=True)
    (root / "docs" / "archive").mkdir(exist_ok=True)

    print("✅ Estrutura criada")

    # TODO: Implementar movimentações específicas baseadas na análise

if __name__ == "__main__":
    reorganize_project()
'''

        script_path = self.root / "scripts" / "reorganize_structure.py"
        script_path.write_text(script)
        script_path.chmod(0o755)

        return script_path

    def run_complete_analysis(self):
        """Executa análise completa"""
        print("🔍 ANÁLISE PROFUNDA DA ESTRUTURA DO PROJETO")
        print("=" * 60)

        # Análises específicas
        self.analyze_src_structure()
        self.analyze_scripts_folder()
        self.analyze_data_folder()
        self.analyze_docs_folder()
        self.check_duplicate_functionality()

        # Sugestão de nova estrutura
        self.suggest_new_structure()

        # Criar script de reorganização
        script_path = self.create_reorganization_script()

        print("\n" + "=" * 60)
        print("📊 RESUMO DA ANÁLISE")
        print("=" * 60)

        # Estatísticas
        all_py_files = list(self.root.rglob('*.py'))
        all_py_files = [f for f in all_py_files if 'Pre_Limpeza' not in str(f)]

        recent = []
        stale = []

        for f in all_py_files:
            info = self.analyze_file_age(f)
            if info:
                if info['days_old'] < 7:
                    recent.append(info)
                elif info['days_old'] > 30:
                    stale.append(info)

        print(f"\n📈 ESTATÍSTICAS:")
        print(f"  Total arquivos Python: {len(all_py_files)}")
        print(f"  Modificados esta semana: {len(recent)}")
        print(f"  Não modificados há 30+ dias: {len(stale)}")

        if stale:
            print(f"\n⚠️ ARQUIVOS MUITO ANTIGOS (candidatos a archive):")
            for s in sorted(stale, key=lambda x: x['days_old'], reverse=True)[:10]:
                print(f"  - {s['path']} ({s['days_old']} dias)")

        print(f"\n✅ Script de reorganização criado: {script_path}")

        # Salvar análise
        analysis_file = self.root / "docs" / "STRUCTURE_ANALYSIS.json"
        with open(analysis_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_files': len(all_py_files),
                'recent_files': len(recent),
                'stale_files': len(stale),
                'stale_list': stale[:20] if stale else []
            }, f, indent=2)

        print(f"\n📄 Análise salva em: {analysis_file}")

def main():
    analyzer = DeepStructureAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()