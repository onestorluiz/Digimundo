#!/usr/bin/env python3
"""
REORGANIZAÇÃO INTELIGENTE DO SCRIPTUREMON
Consolida redundâncias e cria estrutura limpa e lógica
"""

import os
import shutil
from pathlib import Path
import json
from datetime import datetime

class IntelligentReorganizer:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")
        self.backup_path = self.base_path / "archive" / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.changes_log = []

    def analyze_current_structure(self):
        """Analisa a estrutura atual e identifica problemas"""
        print("🔍 ANALISANDO ESTRUTURA ATUAL...")

        problems = {
            "test_folders": [],
            "script_folders": [],
            "output_folders": [],
            "config_folders": [],
            "strange_folders": []
        }

        # Identificar pastas de teste
        for folder in self.base_path.iterdir():
            if folder.is_dir():
                folder_name = folder.name

                # Pastas de teste
                if 'test' in folder_name.lower():
                    problems['test_folders'].append(folder_name)

                # Pastas de scripts
                elif folder_name in ['scripts', 'reference_scripts', 'bin']:
                    problems['script_folders'].append(folder_name)

                # Pastas de output
                elif 'output' in folder_name or 'report' in folder_name:
                    problems['output_folders'].append(folder_name)

                # Pastas de config
                elif folder_name in ['config', 'modelfiles']:
                    problems['config_folders'].append(folder_name)

                # Pastas estranhas
                elif any(char in folder_name for char in ['📁', 'emoji', '-']):
                    problems['strange_folders'].append(folder_name)

        # Relatório
        print("\n📊 PROBLEMAS IDENTIFICADOS:")
        print(f"  • {len(problems['test_folders'])} pastas de teste: {problems['test_folders']}")
        print(f"  • {len(problems['script_folders'])} pastas de scripts: {problems['script_folders']}")
        print(f"  • {len(problems['output_folders'])} pastas de output: {problems['output_folders']}")
        print(f"  • {len(problems['config_folders'])} pastas de config: {problems['config_folders']}")
        print(f"  • {len(problems['strange_folders'])} pastas estranhas: {problems['strange_folders']}")

        return problems

    def create_intelligent_structure(self):
        """Cria a nova estrutura inteligente"""
        print("\n🏗️ CRIANDO NOVA ESTRUTURA INTELIGENTE...")

        new_structure = {
            # Código fonte principal
            "src": ["core", "models", "memory", "integration"],

            # Configuração unificada
            "config": ["modelfiles", "settings"],

            # Testes unificados
            "tests": ["unit", "integration", "fixtures"],

            # Scripts organizados
            "scripts": ["analysis", "maintenance", "tools"],

            # Dados e conhecimento
            "data": ["knowledge", "learning", "cache"],

            # Outputs unificados
            "outputs": ["reports", "logs", "exports"],

            # Workspace para projetos
            "workspace": [],

            # Arquivo histórico
            "archive": ["old_code", "backups", "legacy"],

            # Documentação
            "docs": []
        }

        # Criar estrutura
        for parent, subdirs in new_structure.items():
            parent_path = self.base_path / parent
            parent_path.mkdir(exist_ok=True)

            for subdir in subdirs:
                (parent_path / subdir).mkdir(exist_ok=True)

        print("✅ Nova estrutura criada!")
        return new_structure

    def consolidate_tests(self):
        """Consolida todas as pastas de teste em uma única"""
        print("\n🧪 CONSOLIDANDO TESTES...")

        test_folders = ['tests', 'test_data', 'test_scripturemon', 'test_scripts']
        target_dir = self.base_path / 'tests'

        for folder_name in test_folders:
            source = self.base_path / folder_name
            if source.exists() and source != target_dir:
                print(f"  • Movendo {folder_name} → tests/")

                # Determinar subdiretório apropriado
                if 'data' in folder_name:
                    dest = target_dir / 'fixtures'
                elif 'script' in folder_name:
                    dest = target_dir / 'integration'
                else:
                    dest = target_dir / 'unit'

                # Mover conteúdo
                if source.is_dir():
                    for item in source.iterdir():
                        try:
                            if item.is_file():
                                shutil.move(str(item), str(dest / item.name))
                            elif item.is_dir():
                                shutil.move(str(item), str(dest / item.name))
                            self.changes_log.append(f"Movido: {item.name} → {dest.name}/")
                        except Exception as e:
                            print(f"    ⚠️ Erro ao mover {item.name}: {e}")

                    # Remover pasta vazia
                    if not any(source.iterdir()):
                        source.rmdir()
                        print(f"    ✓ Removido diretório vazio: {folder_name}")

    def consolidate_scripts(self):
        """Consolida todas as pastas de scripts"""
        print("\n🛠️ CONSOLIDANDO SCRIPTS...")

        script_folders = ['scripts', 'reference_scripts', 'bin']
        target_dir = self.base_path / 'scripts'

        for folder_name in script_folders:
            if folder_name == 'scripts':
                continue

            source = self.base_path / folder_name
            if source.exists():
                print(f"  • Movendo {folder_name} → scripts/")

                # Determinar subdiretório
                if folder_name == 'bin':
                    dest = target_dir / 'tools'
                elif 'reference' in folder_name:
                    dest = target_dir / 'analysis'
                else:
                    dest = target_dir / 'maintenance'

                # Mover conteúdo
                if source.is_dir():
                    for item in source.iterdir():
                        try:
                            target_path = dest / item.name
                            if not target_path.exists():
                                shutil.move(str(item), str(target_path))
                                self.changes_log.append(f"Movido: {item.name} → scripts/{dest.name}/")
                        except Exception as e:
                            print(f"    ⚠️ Erro: {e}")

                    # Remover se vazio
                    if not any(source.iterdir()):
                        source.rmdir()

    def consolidate_outputs(self):
        """Consolida pastas de output"""
        print("\n📤 CONSOLIDANDO OUTPUTS...")

        output_folders = ['outputs', 'analysis_reports']
        target_dir = self.base_path / 'outputs'

        for folder_name in output_folders:
            if folder_name == 'outputs':
                continue

            source = self.base_path / folder_name
            if source.exists():
                print(f"  • Movendo {folder_name} → outputs/reports/")
                dest = target_dir / 'reports'

                if source.is_dir():
                    for item in source.iterdir():
                        try:
                            shutil.move(str(item), str(dest / item.name))
                            self.changes_log.append(f"Movido: {item.name} → outputs/reports/")
                        except Exception as e:
                            print(f"    ⚠️ Erro: {e}")

                    if not any(source.iterdir()):
                        source.rmdir()

    def clean_strange_folders(self):
        """Remove ou renomeia pastas com nomes problemáticos"""
        print("\n🧹 LIMPANDO PASTAS ESTRANHAS...")

        strange_patterns = ['📁', 'emoji', '- ']

        for folder in self.base_path.iterdir():
            if folder.is_dir():
                folder_name = folder.name

                # Detectar pasta estranha
                if any(pattern in folder_name for pattern in strange_patterns):
                    print(f"  • Pasta problemática encontrada: {folder_name}")

                    # Renomear removendo caracteres problemáticos
                    clean_name = folder_name.replace('📁', '').replace('- ', '').strip()
                    clean_name = clean_name.replace(' ', '_').lower()

                    if clean_name:
                        new_path = self.base_path / 'archive' / clean_name
                        print(f"    → Movendo para archive/{clean_name}")
                        try:
                            shutil.move(str(folder), str(new_path))
                            self.changes_log.append(f"Arquivado: {folder_name} → archive/{clean_name}")
                        except Exception as e:
                            print(f"    ⚠️ Erro: {e}")

    def organize_modelfiles(self):
        """Move modelfiles para config/modelfiles"""
        print("\n⚙️ ORGANIZANDO CONFIGURAÇÕES...")

        source = self.base_path / 'modelfiles'
        dest = self.base_path / 'config' / 'modelfiles'

        if source.exists() and source.is_dir():
            print(f"  • Movendo modelfiles → config/modelfiles/")

            for item in source.iterdir():
                try:
                    shutil.move(str(item), str(dest / item.name))
                    self.changes_log.append(f"Movido: {item.name} → config/modelfiles/")
                except Exception as e:
                    print(f"    ⚠️ Erro: {e}")

            if not any(source.iterdir()):
                source.rmdir()

    def generate_report(self):
        """Gera relatório da reorganização"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "changes": self.changes_log,
            "total_changes": len(self.changes_log)
        }

        report_path = self.base_path / 'outputs' / 'reports' / f'reorganization_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📊 Relatório salvo em: {report_path}")
        return report

    def execute_reorganization(self):
        """Executa a reorganização completa"""
        print("=" * 60)
        print("🚀 INICIANDO REORGANIZAÇÃO INTELIGENTE")
        print("=" * 60)

        # 1. Analisar estrutura atual
        problems = self.analyze_current_structure()

        # 2. Criar nova estrutura
        self.create_intelligent_structure()

        # 3. Consolidar pastas
        self.consolidate_tests()
        self.consolidate_scripts()
        self.consolidate_outputs()

        # 4. Organizar configs
        self.organize_modelfiles()

        # 5. Limpar pastas estranhas
        self.clean_strange_folders()

        # 6. Gerar relatório
        report = self.generate_report()

        print("\n" + "=" * 60)
        print("✅ REORGANIZAÇÃO COMPLETA!")
        print("=" * 60)
        print(f"  • Total de mudanças: {report['total_changes']}")
        print(f"  • Estrutura otimizada e limpa")
        print(f"  • Redundâncias eliminadas")
        print("\n💡 Próximos passos:")
        print("  1. Verificar se tudo está funcionando")
        print("  2. Atualizar imports nos scripts Python")
        print("  3. Commitar as mudanças no Git")

def main():
    reorganizer = IntelligentReorganizer()

    # Confirmar antes de executar
    print("⚠️ ATENÇÃO: Esta operação vai reorganizar completamente o diretório!")
    print("Recomenda-se fazer backup antes de continuar.")

    response = input("\nDeseja continuar? (s/n): ")

    if response.lower() == 's':
        reorganizer.execute_reorganization()
    else:
        print("Operação cancelada.")

if __name__ == "__main__":
    main()