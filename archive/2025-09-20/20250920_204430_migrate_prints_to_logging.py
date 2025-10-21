#!/usr/bin/env python3
"""
🔄 MIGRAÇÃO PRINTS → LOGGING
Substitui automaticamente os 2,096+ prints por logging estruturado
Baseado na análise detalhada do ChatGPT
"""

import re
import ast
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import json

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.core.logging_system import get_logger, LogCategory
except ImportError:
    # Fallback para execução direta
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from src.core.logging_system import get_logger, LogCategory

logger = get_logger("print_migrator")

class PrintMigrator:
    """Migrador automático de prints para logging estruturado"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent

        # Estatísticas da migração
        self.stats = {
            'files_processed': 0,
            'prints_found': 0,
            'prints_migrated': 0,
            'errors': 0
        }

        # Padrões de substituição inteligente
        self.patterns = [
            # Padrões de sucesso
            (r'print\s*\(\s*["\']✅([^"\']*)["\']', r'logger.success("\1", category=LogCategory.SYSTEM, component=component)'),
            (r'print\s*\(\s*["\']🎯([^"\']*)["\']', r'logger.success("\1", category=LogCategory.SYSTEM, component=component)'),
            (r'print\s*\(\s*["\']🚀([^"\']*)["\']', r'logger.success("\1", category=LogCategory.SYSTEM, component=component)'),

            # Padrões de informação
            (r'print\s*\(\s*["\']📊([^"\']*)["\']', r'logger.info("📊\1", category=LogCategory.ANALYSIS, component=component)'),
            (r'print\s*\(\s*["\']🔧([^"\']*)["\']', r'logger.info("🔧\1", category=LogCategory.SYSTEM, component=component)'),
            (r'print\s*\(\s*["\']💾([^"\']*)["\']', r'logger.info("💾\1", category=LogCategory.MEMORY, component=component)'),

            # Padrões de warning
            (r'print\s*\(\s*["\']⚠️([^"\']*)["\']', r'logger.warning("⚠️\1", category=LogCategory.SYSTEM, component=component)'),
            (r'print\s*\(\s*["\']🚫([^"\']*)["\']', r'logger.warning("🚫\1", category=LogCategory.SYSTEM, component=component)'),

            # Padrões de erro
            (r'print\s*\(\s*["\']❌([^"\']*)["\']', r'logger.error("❌\1", category=LogCategory.ERROR, component=component)'),
            (r'print\s*\(\s*["\']🔴([^"\']*)["\']', r'logger.error("🔴\1", category=LogCategory.ERROR, component=component)'),

            # Performance/timing
            (r'print\s*\(\s*["\']⚡([^"\']*)["\']', r'logger.info("⚡\1", category=LogCategory.PERFORMANCE, component=component)'),
            (r'print\s*\(\s*["\']⏱️([^"\']*)["\']', r'logger.info("⏱️\1", category=LogCategory.PERFORMANCE, component=component)'),

            # ML/Ollama específicos
            (r'print\s*\(\s*["\']🤖([^"\']*)["\']', r'logger.info("🤖\1", category=LogCategory.OLLAMA, component=component)'),
            (r'print\s*\(\s*["\']🧠([^"\']*)["\']', r'logger.info("🧠\1", category=LogCategory.ML, component=component)'),

            # Print simples para info
            (r'print\s*\(\s*f?"([^"]*)"', r'logger.info("\1", category=LogCategory.SYSTEM, component=component)'),
            (r"print\s*\(\s*f?'([^']*)'", r"logger.info('\1', category=LogCategory.SYSTEM, component=component)"),

            # Print com f-strings
            (r'print\s*\(\s*f"([^"]*)"', r'logger.info(f"\1", category=LogCategory.SYSTEM, component=component)'),
            (r"print\s*\(\s*f'([^']*)'", r"logger.info(f'\1', category=LogCategory.SYSTEM, component=component)"),
        ]

    def get_priority_files(self) -> List[Tuple[Path, int]]:
        """Retorna arquivos prioritários baseados na análise do ChatGPT"""

        # Arquivos com mais prints (top 20)
        priority_files = [
            ("src/possiveis_complementos/test_forensic_system.py", 69),
            ("scripts/archive/final_reorganization.py", 69),
            ("scripts/deep_system_analysis.py", 60),
            ("scripts/investigate_background_processes.py", 60),
            ("src/ml/mine_screenplay_with_ollama.py", 59),
            ("scripts/active/unified_power_system.py", 58),
            ("scripts/archive/70b_deprecated/prepare_70b_dedicated.py", 57),
            ("scripts/archive/test_unified_memory.py", 53),
            ("src/possiveis_complementos/test_security_breach.py", 51),
            ("src/features/cinema_deep_reflection_system.py", 50),
            ("scripts/archive/70b_deprecated/async_70b_processor.py", 49),
            ("scripts/archive/optimize_ram.py", 47),
            ("src/core/scripturemon_start.py", 45),
            ("scripts/ml_unified.py", 45),
            ("scripts/archive/70b_deprecated/monitor_70b.py", 45),
            ("scripts/archive/deep_structure_analysis.py", 42),
            ("src/possiveis_complementos/test_enhanced_system.py", 42),
            ("src/ml/ml_pipeline.py", 42),
            ("tests/test_mixtral_complete.py", 41),
            ("scripts/active/start_ml_mixtral_correct.py", 39)
        ]

        result = []
        for file_path, print_count in priority_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                result.append((full_path, print_count))
            else:
                logger.warning(f"Arquivo não encontrado: {file_path}")

        return result

    def add_logging_import(self, content: str, filename: str) -> str:
        """Adiciona import do sistema de logging"""

        # Detectar se já tem imports
        lines = content.split('\n')

        # Determinar componente baseado no nome do arquivo
        component = Path(filename).stem

        # Preparar imports necessários
        logging_imports = [
            "from src.core.logging_system import get_logger, LogCategory, timed_operation",
            f"logger = get_logger('{component}')",
            f"component = '{component}'"
        ]

        # Encontrar posição para inserir (após shebang e docstring)
        insert_position = 0
        in_docstring = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Pular shebang
            if stripped.startswith('#!'):
                insert_position = i + 1
                continue

            # Detectar início de docstring
            if stripped.startswith('"""') or stripped.startswith("'''"):
                if not in_docstring:
                    in_docstring = True
                elif stripped.endswith('"""') or stripped.endswith("'''"):
                    in_docstring = False
                    insert_position = i + 1
                continue

            # Se não estamos em docstring e linha não está vazia
            if not in_docstring and stripped and not stripped.startswith('#'):
                break

            if not in_docstring:
                insert_position = i + 1

        # Inserir imports
        for import_line in reversed(logging_imports):
            lines.insert(insert_position, import_line)

        lines.insert(insert_position + len(logging_imports), "")  # Linha em branco

        return '\n'.join(lines)

    def migrate_prints_in_content(self, content: str) -> Tuple[str, int]:
        """Migra prints em um conteúdo específico"""

        original_content = content
        prints_migrated = 0

        # Aplicar padrões de substituição
        for pattern, replacement in self.patterns:
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                prints_migrated += len(matches)

        # Contar prints restantes que não foram capturados
        remaining_prints = len(re.findall(r'\bprint\s*\(', content))

        return content, prints_migrated

    def migrate_file(self, file_path: Path, expected_prints: int) -> Dict:
        """Migra um arquivo específico"""

        logger.info(f"Migrando {file_path.name}...",
                   category=LogCategory.SYSTEM,
                   component="migrator",
                   expected_prints=expected_prints)

        try:
            # Ler arquivo
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Contar prints originais
            original_prints = len(re.findall(r'\bprint\s*\(', original_content))

            # Adicionar imports de logging
            content_with_imports = self.add_logging_import(original_content, file_path.name)

            # Migrar prints
            migrated_content, prints_migrated = self.migrate_prints_in_content(content_with_imports)

            # Contar prints restantes
            remaining_prints = len(re.findall(r'\bprint\s*\(', migrated_content))

            # Salvar arquivo migrado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(migrated_content)

            result = {
                'file': str(file_path),
                'original_prints': original_prints,
                'prints_migrated': prints_migrated,
                'remaining_prints': remaining_prints,
                'success': True,
                'migration_rate': (prints_migrated / original_prints * 100) if original_prints > 0 else 0
            }

            logger.success(f"✅ {file_path.name}: {prints_migrated}/{original_prints} prints migrados ({result['migration_rate']:.1f}%)",
                          category=LogCategory.SYSTEM,
                          component="migrator",
                          **result)

            return result

        except Exception as e:
            logger.error(f"❌ Erro migrando {file_path.name}: {e}",
                        category=LogCategory.ERROR,
                        component="migrator",
                        error=str(e))

            return {
                'file': str(file_path),
                'success': False,
                'error': str(e),
                'original_prints': 0,
                'prints_migrated': 0,
                'remaining_prints': 0
            }

    def migrate_all_priority_files(self) -> Dict:
        """Migra todos os arquivos prioritários"""

        logger.info("🚀 Iniciando migração P2 - Prints → Logging Estruturado",
                   category=LogCategory.SYSTEM,
                   component="migrator")

        priority_files = self.get_priority_files()

        logger.info(f"📁 {len(priority_files)} arquivos prioritários identificados",
                   category=LogCategory.SYSTEM,
                   component="migrator")

        results = []
        total_original = 0
        total_migrated = 0

        for file_path, expected_prints in priority_files:
            result = self.migrate_file(file_path, expected_prints)
            results.append(result)

            if result['success']:
                total_original += result['original_prints']
                total_migrated += result['prints_migrated']

        # Estatísticas finais
        summary = {
            'files_processed': len([r for r in results if r['success']]),
            'files_failed': len([r for r in results if not r['success']]),
            'total_original_prints': total_original,
            'total_migrated_prints': total_migrated,
            'remaining_prints': total_original - total_migrated,
            'migration_rate': (total_migrated / total_original * 100) if total_original > 0 else 0,
            'results': results
        }

        logger.success(f"🎯 P2 Migração concluída: {total_migrated:,}/{total_original:,} prints migrados ({summary['migration_rate']:.1f}%)",
                      category=LogCategory.SYSTEM,
                      component="migrator",
                      **{k: v for k, v in summary.items() if k != 'results'})

        return summary

def main():
    """Função principal - executa migração"""

    migrator = PrintMigrator()

    print("🔄 MIGRAÇÃO P2: PRINTS → LOGGING ESTRUTURADO")
    print("=" * 60)
    print("📋 Baseado na análise detalhada do ChatGPT")
    print("🎯 Objetivo: Substituir 2,096+ prints por logging")
    print()

    # Executar migração
    summary = migrator.migrate_all_priority_files()

    # Exportar relatório
    report_file = Path("logs") / "p2_migration_report.json"
    report_file.parent.mkdir(exist_ok=True)

    with open(report_file, 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    print()
    print("📊 RELATÓRIO FINAL:")
    print(f"   Arquivos processados: {summary['files_processed']}")
    print(f"   Prints originais: {summary['total_original_prints']:,}")
    print(f"   Prints migrados: {summary['total_migrated_prints']:,}")
    print(f"   Taxa de migração: {summary['migration_rate']:.1f}%")
    print(f"   Relatório: {report_file}")

    if summary['files_failed'] > 0:
        print(f"   ⚠️ Arquivos com erro: {summary['files_failed']}")

if __name__ == "__main__":
    main()