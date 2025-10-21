#!/usr/bin/env python3
"""
🏗️ REORGANIZAÇÃO FINAL E COMPLETA DO PROJETO
============================================
Organiza toda estrutura de forma profissional e minimalista
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class FinalReorganization:
    def __init__(self):
        self.root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        # REGRA #40: TODO LIXO VAI PARA PASTA EXTERNA
        self.backup_dir = Path("/Users/clubproducoes/Digimundo/Pre_Limpeza_Minimalista_Lixo/claude_code_lixo/final_reorganization_backup")
        self.moves = []
        self.keeps = []

    def analyze_and_plan(self):
        """Analisa e cria plano de reorganização"""
        print("🏗️ PLANO DE REORGANIZAÇÃO FINAL")
        print("=" * 60)

        # 1. LIMPAR DATA/
        self.cleanup_data_folder()

        # 2. ORGANIZAR SCRIPTS/
        self.organize_scripts()

        # 3. ORGANIZAR DOCS/
        self.organize_docs()

        # 4. LIMPAR SRC/
        self.cleanup_src()

        # 5. VERIFICAR RAIZ
        self.check_root_files()

    def cleanup_data_folder(self):
        """Limpa pasta data/"""
        print("\n📂 LIMPEZA DE DATA/")
        print("-" * 40)

        # Pastas essenciais para manter
        essential = {
            'pdfs',           # PDFs originais
            'screenplays',    # TXTs convertidos
            'models',         # Modelfiles
            'legacy_backup'   # Backup de consolidação
        }

        # Pastas suspeitas para mover
        to_check = []
        data_path = self.root / 'data'

        for item in data_path.iterdir():
            if item.is_dir() and item.name not in essential:
                to_check.append(item)

        print(f"✅ Manter: {', '.join(essential)}")
        print(f"❌ Mover {len(to_check)} subpastas antigas:")

        for folder in to_check[:10]:
            print(f"   - {folder.name}")
            self.moves.append(('data_cleanup', folder))

        if len(to_check) > 10:
            print(f"   ... e mais {len(to_check) - 10} pastas")

    def organize_scripts(self):
        """Organiza pasta scripts/"""
        print("\n📂 ORGANIZAÇÃO DE SCRIPTS/")
        print("-" * 40)

        scripts_path = self.root / 'scripts'

        # Scripts essenciais (modificados esta semana)
        essential_scripts = [
            'test_unified_memory.py',
            'quick_deep_learning.py',
            'deep_screenplay_learning.py',
            'integrate_screenplay_library.py',
            'analyze_real_unification.py'
        ]

        # Scripts de migração/setup (podem ser arquivados após uso)
        migration_scripts = [
            'complete_unification_plan.py',
            'consolidate_remaining_databases.py',
            'execute_complete_migration.py',
            'update_main_system.py',
            'execute_root_cleanup.py',
            'analyze_and_cleanup_root.py',
            'cleanup_legacy_memory.py',
            'unify_all_memory_systems.py',
            'force_total_unification.py',
            'final_unification_push.py',
            'add_unified_imports.py'
        ]

        print(f"✅ Scripts essenciais: {len(essential_scripts)}")
        print(f"📦 Scripts de migração (arquivar): {len(migration_scripts)}")

        # Marcar para movimento
        for script in migration_scripts:
            script_path = scripts_path / script
            if script_path.exists():
                self.moves.append(('scripts_migration', script_path))

    def organize_docs(self):
        """Organiza documentação"""
        print("\n📂 ORGANIZAÇÃO DE DOCS/")
        print("-" * 40)

        docs_path = self.root / 'docs'
        docs = list(docs_path.glob('*.md'))

        # Categorias de documentação
        categories = {
            'current': [],    # Documentação ativa
            'reports': [],    # Relatórios de análise
            'phases': [],     # Documentação de fases
            'archive': []     # Para arquivar
        }

        for doc in docs:
            name = doc.name.upper()

            # Documentos principais (sempre manter)
            if name in ['README.MD', 'CLAUDE.MD', 'SYSTEM_ARCHITECTURE.MD']:
                categories['current'].append(doc)

            # Relatórios e análises (arquivar)
            elif 'ANALISE' in name or 'ANALYSIS' in name or 'REPORT' in name or 'RESULTADO' in name:
                categories['reports'].append(doc)

            # Fases antigas (arquivar)
            elif 'PHASE' in name or 'FASE' in name:
                categories['phases'].append(doc)

            # Documentação de sistema (manter)
            elif 'SYSTEM' in name or 'UNIFIED' in name or 'LEARNING' in name:
                categories['current'].append(doc)

            else:
                categories['archive'].append(doc)

        print(f"✅ Documentação ativa: {len(categories['current'])}")
        print(f"📊 Relatórios (arquivar): {len(categories['reports'])}")
        print(f"📋 Fases antigas (arquivar): {len(categories['phases'])}")
        print(f"📦 Outros (arquivar): {len(categories['archive'])}")

        # Marcar para movimento
        for doc in categories['reports'] + categories['phases'] + categories['archive']:
            self.moves.append(('docs_archive', doc))

    def cleanup_src(self):
        """Limpa pasta src/"""
        print("\n📂 VERIFICAÇÃO DE SRC/")
        print("-" * 40)

        # Verificar se existe pasta possiveis_complementos
        possiveis = self.root / 'src' / 'possiveis_complementos'
        if possiveis.exists():
            files = list(possiveis.glob('*'))
            print(f"❌ Pasta 'possiveis_complementos' com {len(files)} arquivos")
            self.moves.append(('src_unused', possiveis))

        # Renomeações sugeridas
        print("\n💡 SUGESTÕES DE RENOMEAÇÃO:")
        print("  src/advanced/ → src/features/")
        print("  src/learning/ → src/ml/")

    def check_root_files(self):
        """Verifica arquivos na raiz"""
        print("\n📂 VERIFICAÇÃO DA RAIZ")
        print("-" * 40)

        # Arquivos essenciais na raiz
        essential_root = {
            'README.md',
            'CLAUDE.md',
            'requirements.txt',
            'script_doctor.py',
            '.gitignore'
        }

        root_files = [f for f in self.root.iterdir() if f.is_file()]

        for file in root_files:
            if file.name not in essential_root and not file.name.startswith('.'):
                if file.suffix in ['.bak', '.backup', '.old']:
                    self.moves.append(('root_backup', file))
                    print(f"❌ Backup na raiz: {file.name}")

    def create_new_structure(self):
        """Cria nova estrutura organizada"""
        print("\n🏗️ NOVA ESTRUTURA PROPOSTA")
        print("=" * 60)

        structure = """
scripturemon-champion/
│
├── src/                        # Código fonte
│   ├── core/                   # Sistema principal ✅
│   ├── features/               # Features avançadas (renomear de advanced)
│   └── ml/                     # Machine Learning (renomear de learning)
│
├── scripts/
│   ├── active/                 # Scripts em uso ativo
│   │   ├── test_unified_memory.py
│   │   ├── quick_deep_learning.py
│   │   └── analyze_system.py
│   │
│   └── archive/                # Scripts de migração/setup
│       └── [11+ scripts de migração]
│
├── data/
│   ├── unified_memory.db      # Banco único ✅
│   ├── pdfs/                   # PDFs originais ✅
│   ├── screenplays/           # TXTs convertidos ✅
│   ├── models/                # Modelfiles ✅
│   └── legacy_backup/         # Backup consolidação ✅
│
├── docs/
│   ├── README.md              # Principal ✅
│   ├── CLAUDE.md              # Memória ✅
│   ├── system/                # Docs do sistema
│   └── archive/               # Relatórios e análises antigas
│
├── tests/                     # Testes ✅
├── config/                    # Configurações ✅
└── digilibrary/              # Biblioteca roteiros ✅
"""
        print(structure)

    def generate_execution_script(self):
        """Gera script de execução"""

        # Criar diretórios de backup
        dirs_to_create = [
            self.backup_dir / "data_old",
            self.backup_dir / "scripts_migration",
            self.backup_dir / "docs_archive",
            self.backup_dir / "src_unused"
        ]

        print("\n📝 SCRIPT DE EXECUÇÃO")
        print("=" * 60)
        print(f"\n# Criar estrutura de backup")
        for d in dirs_to_create:
            print(f"mkdir -p '{d}'")

        print(f"\n# Mover {len(self.moves)} items")

        # Agrupar por categoria
        by_category = {}
        for category, path in self.moves:
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(path)

        for category, paths in by_category.items():
            print(f"\n# {category} ({len(paths)} items)")
            for path in paths[:3]:
                dest = self.backup_dir / category
                print(f"mv '{path}' '{dest}/'")
            if len(paths) > 3:
                print(f"# ... e mais {len(paths) - 3} items")

        print("\n# Renomear pastas")
        print("mv src/advanced src/features")
        print("mv src/learning src/ml")

        print("\n# Criar estrutura de scripts")
        print("mkdir -p scripts/active scripts/archive")
        print("mv scripts/*migration*.py scripts/archive/")
        print("mv scripts/*unif*.py scripts/archive/")
        print("mv scripts/*cleanup*.py scripts/archive/")

        # Salvar como script executável
        script_path = self.root / "scripts" / "execute_final_reorganization.sh"
        with open(script_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Script de reorganização final\n\n")

            # Criar diretórios
            for d in dirs_to_create:
                f.write(f"mkdir -p '{d}'\n")

            f.write("\n# Mover arquivos\n")
            for category, path in self.moves[:20]:  # Primeiros 20 como exemplo
                dest = self.backup_dir / category
                f.write(f"mv '{path}' '{dest}/' 2>/dev/null\n")

            f.write("\n# Reorganizar estrutura\n")
            f.write("mv src/advanced src/features 2>/dev/null\n")
            f.write("mv src/learning src/ml 2>/dev/null\n")
            f.write("mkdir -p scripts/active scripts/archive\n")
            f.write("mv scripts/*migration*.py scripts/archive/ 2>/dev/null\n")
            f.write("mv scripts/*unif*.py scripts/archive/ 2>/dev/null\n")
            f.write("mv scripts/*cleanup*.py scripts/archive/ 2>/dev/null\n")
            f.write("\necho '✅ Reorganização completa!'\n")

        script_path.chmod(0o755)
        print(f"\n✅ Script salvo em: {script_path}")

    def summarize(self):
        """Resume plano"""
        print("\n" + "=" * 60)
        print("📊 RESUMO DO PLANO")
        print("=" * 60)

        # Contar por categoria
        by_category = {}
        for category, _ in self.moves:
            by_category[category] = by_category.get(category, 0) + 1

        print(f"\nTotal para mover: {len(self.moves)} items")
        for category, count in by_category.items():
            print(f"  - {category}: {count} items")

        print("\nRenomeações:")
        print("  - src/advanced → src/features")
        print("  - src/learning → src/ml")

        print("\nReorganizações:")
        print("  - scripts/ → active/ e archive/")
        print("  - docs/ → system/ e archive/")

        print("\nEstrutura final:")
        print("  - Mais organizada e profissional")
        print("  - Separação clara entre ativo e arquivo")
        print("  - Nomes mais intuitivos")

    def run(self):
        """Executa análise e geração do plano"""
        self.analyze_and_plan()
        self.create_new_structure()
        self.generate_execution_script()
        self.summarize()

def main():
    print("🏗️ ANÁLISE E REORGANIZAÇÃO FINAL DO PROJETO")
    print("=" * 60)

    reorganizer = FinalReorganization()
    reorganizer.run()

    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. Revisar o plano acima")
    print("2. Executar: bash scripts/execute_final_reorganization.sh")
    print("3. Verificar que tudo funciona")
    print("4. Atualizar documentação")

if __name__ == "__main__":
    main()