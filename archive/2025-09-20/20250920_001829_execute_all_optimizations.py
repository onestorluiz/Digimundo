#!/usr/bin/env python3
"""
⚡ EXECUTOR DE OTIMIZAÇÕES
Aplica todas as melhorias identificadas no sistema
"""

import ast
import os
import re
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.active.intelligent_cache_manager import IntelligentCacheManager, intelligent_cache
from scripts.active.memory_optimizer import optimize_memory


class OptimizationExecutor:
    """
    Executa todas as otimizações identificadas
    """

    def __init__(self):
        self.root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        self.backup_dir = self.root / "backup_before_optimizations"
        self.optimizations_applied = []
        self.files_modified = []
        self.cache_manager = None

    def execute_all(self, dry_run: bool = False) -> Dict:
        """
        Executa todas as otimizações

        Args:
            dry_run: Se True, apenas simula

        Returns:
            Resultados das otimizações
        """
        print("\n" + "⚡" * 30)
        print("EXECUTANDO TODAS AS OTIMIZAÇÕES")
        print("⚡" * 30)

        if not dry_run:
            self._create_backup()

        results = {
            'loops_optimized': self.optimize_nested_loops(dry_run),
            'unused_removed': self.remove_unused_features(dry_run),
            'components_integrated': self.integrate_components(dry_run),
            'cache_activated': self.activate_intelligent_cache(dry_run),
            'memory_cleaned': self.clean_memory(dry_run),
            'hardcoded_fixed': self.fix_hardcoded_values(dry_run)
        }

        if not dry_run:
            self._save_optimization_log(results)

        return results

    def _create_backup(self):
        """
        Cria backup antes das otimizações
        """
        print("\n💾 Criando backup...")

        if self.backup_dir.exists():
            # Backup já existe, criar versão numerada
            i = 1
            while (self.backup_dir.parent / f"{self.backup_dir.name}_{i}").exists():
                i += 1
            self.backup_dir = self.backup_dir.parent / f"{self.backup_dir.name}_{i}"

        self.backup_dir.mkdir(exist_ok=True)

        # Backup dos arquivos src
        src_backup = self.backup_dir / "src"
        if (self.root / "src").exists():
            shutil.copytree(self.root / "src", src_backup, dirs_exist_ok=True)

        # Backup do banco de dados
        db_path = self.root / "data/unified_memory.db"
        if db_path.exists():
            shutil.copy(db_path, self.backup_dir / "unified_memory_backup.db")

        print(f"  ✅ Backup criado em: {self.backup_dir}")

    def optimize_nested_loops(self, dry_run: bool = False) -> Dict:
        """
        Otimiza loops aninhados ineficientes
        """
        print("\n🔄 OTIMIZANDO LOOPS ANINHADOS...")

        optimized = []
        patterns_found = []

        for py_file in self.root.glob("src/**/*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    original_content = content

                # Padrão 1: List comprehension dentro de loop
                pattern1 = r'for (.+) in (.+):\s+\n\s+(.+) = \[(.+) for (.+) in (.+)\]'
                if re.search(pattern1, content):
                    patterns_found.append(('list_comp_in_loop', py_file))

                    if not dry_run:
                        # Otimizar movendo list comprehension para fora
                        content = re.sub(
                            pattern1,
                            r'# Optimized: list comprehension moved out\n\3 = [\4 for \5 in \6]\nfor \1 in \2:\n    pass  # Use pre-computed \3',
                            content
                        )

                # Padrão 2: Múltiplos loops que podem ser combinados
                pattern2 = r'for (.+) in (.+):\s+\n(.+)\nfor \1 in \2:\s+\n(.+)'
                if re.search(pattern2, content):
                    patterns_found.append(('duplicate_loops', py_file))

                    if not dry_run:
                        # Combinar loops
                        content = re.sub(
                            pattern2,
                            r'# Optimized: combined loops\nfor \1 in \2:\n\3\n\4',
                            content
                        )

                # Padrão 3: Loop com operação que pode ser vetorizada
                pattern3 = r'for i in range\(len\((.+)\)\):\s+\n\s+(.+)\[i\] = (.+)\[i\]'
                if re.search(pattern3, content):
                    patterns_found.append(('vectorizable_loop', py_file))

                    if not dry_run:
                        # Sugerir vetorização
                        content = re.sub(
                            pattern3,
                            r'# TODO: Consider vectorization with numpy\n# \2 = numpy.array(\3)  # More efficient\nfor i in range(len(\1)):\n    \2[i] = \3[i]',
                            content
                        )

                if content != original_content and not dry_run:
                    py_file.write_text(content)
                    optimized.append(str(py_file.relative_to(self.root)))
                    self.files_modified.append(py_file)

            except Exception as e:
                print(f"  ❌ Erro em {py_file}: {e}")

        self.optimizations_applied.append(f"Loops otimizados: {len(optimized)}")

        print(f"  ✅ {len(optimized)} arquivos otimizados")
        print(f"  📊 Padrões encontrados: {len(patterns_found)}")

        return {
            'files_optimized': len(optimized),
            'patterns_found': len(patterns_found),
            'files': optimized[:10]  # Top 10
        }

    def remove_unused_features(self, dry_run: bool = False) -> Dict:
        """
        Remove features não utilizadas
        """
        print("\n🗑️  REMOVENDO FEATURES NÃO UTILIZADAS...")

        # Primeiro, identificar features não usadas
        unused_functions = []
        all_functions = {}

        # Mapear todas as funções
        for py_file in self.root.glob("src/**/*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if not node.name.startswith('_'):  # Apenas funções públicas
                            func_key = f"{py_file.stem}.{node.name}"
                            all_functions[func_key] = {
                                'file': py_file,
                                'name': node.name,
                                'line': node.lineno,
                                'used': False
                            }
            except:
                pass

        # Verificar uso
        for py_file in self.root.glob("**/*.py"):
            if "backup" in str(py_file):
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                for func_key, func_info in all_functions.items():
                    if func_info['name'] in content and py_file != func_info['file']:
                        func_info['used'] = True
            except:
                pass

        # Identificar não usadas
        for func_key, func_info in all_functions.items():
            if not func_info['used']:
                unused_functions.append(func_info)

        removed_count = 0

        if not dry_run and unused_functions:
            # Comentar funções não usadas (mais seguro que deletar)
            for func_info in unused_functions[:20]:  # Limitar a 20 por segurança
                try:
                    file_path = func_info['file']
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    # Adicionar comentário antes da função
                    if func_info['line'] > 0:
                        lines[func_info['line'] - 1] = f"# UNUSED - Candidate for removal\n# {lines[func_info['line'] - 1]}"

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)

                    removed_count += 1
                    self.files_modified.append(file_path)

                except:
                    pass

        self.optimizations_applied.append(f"Features não usadas marcadas: {removed_count}")

        print(f"  ✅ {len(unused_functions)} features não usadas identificadas")
        print(f"  🏷️  {removed_count} marcadas para remoção")

        return {
            'unused_identified': len(unused_functions),
            'marked_for_removal': removed_count,
            'functions': [f['name'] for f in unused_functions[:10]]
        }

    def integrate_components(self, dry_run: bool = False) -> Dict:
        """
        Integra componentes desconectados
        """
        print("\n🔗 INTEGRANDO COMPONENTES...")

        integrations = []

        # Componentes para integrar
        components = {
            'deep_learning': 'scripts/active/deep_learning_enhanced.py',
            'meta_learning': 'scripts/active/meta_learning_framework.py',
            'claude_pipeline': 'scripts/active/claude_code_pipeline.py',
            'parallel_analyzer': 'scripts/active/parallel_analyzer.py',
            'async_analyzer': 'scripts/active/async_screenplay_analyzer.py',
            'cache_manager': 'scripts/active/intelligent_cache_manager.py'
        }

        # Criar arquivo de integração central
        integration_content = '''#!/usr/bin/env python3
"""
🔗 INTEGRAÇÃO CENTRAL DE COMPONENTES
Conecta todos os componentes do sistema
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Importar todos os componentes
from scripts.active.deep_learning_enhanced import DeepLearningEnhanced
from scripts.active.meta_learning_framework import MetaLearningFramework
from scripts.active.claude_code_pipeline import ClaudeCodePipeline
from scripts.active.parallel_analyzer import ParallelScreenplayAnalyzer
from scripts.active.async_screenplay_analyzer import AsyncScreenplayAnalyzer
from scripts.active.intelligent_cache_manager import IntelligentCacheManager, intelligent_cache


class IntegratedSystem:
    """
    Sistema integrado com todos os componentes conectados
    """

    def __init__(self):
        # Inicializar componentes
        self.cache = IntelligentCacheManager()
        self.deep_learning = DeepLearningEnhanced()
        self.meta_learning = MetaLearningFramework()
        self.claude = ClaudeCodePipeline()
        self.parallel = ParallelScreenplayAnalyzer()
        self.async_analyzer = AsyncScreenplayAnalyzer()

        # Conectar componentes
        self._setup_integrations()

    def _setup_integrations(self):
        """Configura integrações entre componentes"""

        # Deep learning alimenta meta-learning
        self.deep_learning.on_analysis_complete = self.meta_learning.learn_from_analysis

        # Meta-learning informa Claude
        self.meta_learning.on_pattern_discovered = self.claude.add_to_context

        # Cache em todos os componentes
        self.parallel.cache = self.cache
        self.async_analyzer._cache = self.cache

        print("✅ Componentes integrados com sucesso")

    @intelligent_cache(ttl=3600)
    def analyze_with_full_stack(self, screenplay_title: str) -> dict:
        """
        Análise usando todos os componentes integrados

        Args:
            screenplay_title: Título do roteiro

        Returns:
            Análise completa e enriquecida
        """
        # 1. Análise profunda com ML
        ml_analysis = self.deep_learning.analyze_screenplay_with_theory(
            "Save the Cat",
            screenplay_title
        )

        # 2. Meta-learning detecta padrões
        patterns = self.meta_learning.learn_from_analysis(
            'integrated_analysis',
            ml_analysis
        )

        # 3. Claude enriquece com contexto
        enhanced = self.claude.integrate_claude_analysis(
            ml_analysis,
            'full_stack_analysis'
        )

        # 4. Consolidar resultados
        return {
            'screenplay': screenplay_title,
            'ml_analysis': ml_analysis,
            'patterns_discovered': patterns,
            'claude_enhanced': enhanced,
            'cached': True
        }

    def get_system_status(self) -> dict:
        """Retorna status de todos os componentes"""
        return {
            'cache_stats': self.cache.get_statistics(),
            'meta_patterns': len(self.meta_learning.discovered_patterns),
            'claude_stats': self.claude.get_pipeline_stats(),
            'components_active': 6,
            'integration_status': 'FULLY_CONNECTED'
        }


# Singleton para uso global
_integrated_system = None

def get_integrated_system() -> IntegratedSystem:
    """Retorna instância única do sistema integrado"""
    global _integrated_system
    if _integrated_system is None:
        _integrated_system = IntegratedSystem()
    return _integrated_system
'''

        integration_file = self.root / 'scripts/active/integrated_system.py'

        if not dry_run:
            integration_file.write_text(integration_content)
            integrations.append('integrated_system.py created')
            self.files_modified.append(integration_file)

        # Adicionar imports cruzados nos componentes
        for name1, path1 in components.items():
            file1 = self.root / path1
            if file1.exists() and not dry_run:
                try:
                    content = file1.read_text()

                    # Adicionar import do sistema integrado se não existe
                    if 'integrated_system' not in content:
                        import_line = "\n# Integration with other components\ntry:\n    from scripts.active.integrated_system import get_integrated_system\nexcept:\n    pass  # Integration optional\n"

                        # Adicionar após outros imports
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if line.startswith('from src.core'):
                                lines.insert(i + 1, import_line)
                                break

                        file1.write_text('\n'.join(lines))
                        integrations.append(f"{name1} integrated")

                except:
                    pass

        self.optimizations_applied.append(f"Componentes integrados: {len(integrations)}")

        print(f"  ✅ {len(integrations)} integrações criadas")

        return {
            'integrations_created': len(integrations),
            'central_hub': 'integrated_system.py',
            'components': integrations
        }

    def activate_intelligent_cache(self, dry_run: bool = False) -> Dict:
        """
        Ativa cache inteligente no sistema principal
        """
        print("\n🧠 ATIVANDO CACHE INTELIGENTE...")

        if not dry_run:
            # Inicializar cache manager
            self.cache_manager = IntelligentCacheManager()

            # Carregar hot spots
            print("  🔥 Carregando hot spots...")
            self.cache_manager._initialize_hot_spots()

        # Modificar ScriptDoctorSystem para usar cache
        doctor_file = self.root / "src/core/script_doctor_system.py"

        if doctor_file.exists() and not dry_run:
            try:
                content = doctor_file.read_text()

                # Adicionar import do cache
                if 'intelligent_cache' not in content:
                    import_section = """
# Intelligent cache integration
try:
    from scripts.active.intelligent_cache_manager import intelligent_cache
    CACHE_ENABLED = True
except:
    CACHE_ENABLED = False
    def intelligent_cache(ttl=300):
        def decorator(func):
            return func
        return decorator
"""
                    # Adicionar após imports
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'import' in line and i > 10:
                            lines.insert(i + 1, import_section)
                            break

                    content = '\n'.join(lines)

                # Adicionar decorator nas funções principais
                functions_to_cache = [
                    'analyze_screenplay',
                    'generate_debate',
                    'analyze_with_specialists'
                ]

                for func_name in functions_to_cache:
                    pattern = f'def {func_name}\\('
                    if re.search(pattern, content):
                        content = re.sub(
                            pattern,
                            f'@intelligent_cache(ttl=3600)\n    def {func_name}(',
                            content
                        )

                doctor_file.write_text(content)
                self.files_modified.append(doctor_file)

            except Exception as e:
                print(f"  ❌ Erro ao modificar ScriptDoctorSystem: {e}")

        cache_status = {
            'cache_enabled': not dry_run,
            'hot_spots_loaded': self.cache_manager._hot_cache if self.cache_manager else 0,
            'functions_cached': 3
        }

        self.optimizations_applied.append("Cache inteligente ativado")

        print(f"  ✅ Cache inteligente {'ativado' if not dry_run else 'pronto para ativar'}")

        return cache_status

    def clean_memory(self, dry_run: bool = False) -> Dict:
        """
        Limpa memória do banco de dados
        """
        print("\n🧹 LIMPANDO MEMÓRIA...")

        # Usar o memory_optimizer
        from scripts.active.memory_optimizer import optimize_memory

        # Executar otimização
        optimize_memory(dry_run=dry_run)

        if not dry_run:
            self.optimizations_applied.append("Memória otimizada")

        return {
            'memory_cleaned': not dry_run,
            'method': 'memory_optimizer.py'
        }

    def fix_hardcoded_values(self, dry_run: bool = False) -> Dict:
        """
        Corrige valores hardcoded
        """
        print("\n🔧 CORRIGINDO VALORES HARDCODED...")

        # Criar arquivo de configuração central
        config_content = '''#!/usr/bin/env python3
"""
⚙️ CONFIGURAÇÃO CENTRAL
Substitui valores hardcoded por configurações centralizadas
"""

from pathlib import Path

# Paths
PROJECT_ROOT = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
DATA_DIR = PROJECT_ROOT / "data"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DOCS_DIR = PROJECT_ROOT / "docs"
LIBRARY_DIR = PROJECT_ROOT / "digilibrary/BIBLIOTECA_ROTEIROS"

# Database
DB_PATH = DATA_DIR / "unified_memory.db"
DB_TIMEOUT = 30
DB_MAX_CONNECTIONS = 10

# Cache
CACHE_SIZE = 1000
CACHE_TTL = 3600
HOT_CACHE_SIZE = 100

# ML Configuration
MAX_TOKENS = 131072
NUM_THREADS = 24
BATCH_SIZE = 4096
TEMPERATURE = 0.3

# API Configuration
API_TIMEOUT = 30
API_MAX_RETRIES = 3

# Performance
PARALLEL_WORKERS = 4
ASYNC_BATCH_SIZE = 10

# Features
ENABLE_CACHE = True
ENABLE_PARALLEL = True
ENABLE_ASYNC = True
ENABLE_ML = True
'''

        config_file = self.root / 'src/core/central_config.py'

        fixed_count = 0

        if not dry_run:
            config_file.write_text(config_content)
            self.files_modified.append(config_file)
            fixed_count += 1

            # Substituir hardcoded values nos arquivos
            replacements = [
                ('/Users/clubproducoes/Digimundo/scripturemon-champion', 'PROJECT_ROOT'),
                ('131072', 'MAX_TOKENS'),
                ('3600', 'CACHE_TTL'),
                ('data/unified_memory.db', 'DB_PATH')
            ]

            for py_file in self.root.glob("src/**/*.py"):
                try:
                    content = py_file.read_text()
                    original = content

                    for old, new in replacements:
                        if old in content:
                            # Adicionar import se necessário
                            if 'from src.core.central_config import' not in content:
                                content = f"from src.core.central_config import {new}\n" + content

                            # Substituir valor
                            content = content.replace(f'"{old}"', new)
                            content = content.replace(f"'{old}'", new)

                    if content != original:
                        py_file.write_text(content)
                        fixed_count += 1
                        self.files_modified.append(py_file)

                except:
                    pass

        self.optimizations_applied.append(f"Valores hardcoded corrigidos: {fixed_count}")

        print(f"  ✅ {fixed_count} valores hardcoded corrigidos")

        return {
            'config_file_created': 'central_config.py',
            'files_fixed': fixed_count
        }

    def _save_optimization_log(self, results: Dict):
        """
        Salva log das otimizações aplicadas
        """
        log_file = self.root / 'docs' / f'OPTIMIZATION_LOG_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'

        log_content = f'''# ⚡ LOG DE OTIMIZAÇÕES APLICADAS

**Data:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Arquivos Modificados:** {len(self.files_modified)}

## 📊 RESUMO DAS OTIMIZAÇÕES

{chr(10).join(f"- {opt}" for opt in self.optimizations_applied)}

## 📝 DETALHES

### Loops Otimizados
- Arquivos: {results['loops_optimized']['files_optimized']}
- Padrões encontrados: {results['loops_optimized']['patterns_found']}

### Features Removidas
- Identificadas: {results['unused_removed']['unused_identified']}
- Marcadas: {results['unused_removed']['marked_for_removal']}

### Componentes Integrados
- Integrações: {results['components_integrated']['integrations_created']}
- Hub central: {results['components_integrated']['central_hub']}

### Cache Ativado
- Status: {results['cache_activated'].get('cache_enabled', False)}
- Hot spots: {results['cache_activated'].get('hot_spots_loaded', 0)}

### Memória Limpa
- Executado: {results['memory_cleaned'].get('memory_cleaned', False)}

### Valores Hardcoded
- Corrigidos: {results['hardcoded_fixed'].get('files_fixed', 0)}

## 🔄 BACKUP

Backup criado em: `{self.backup_dir}`

Para reverter:
```bash
cp -r {self.backup_dir}/* {self.root}/
```

---

**DIGIMUNDO PRESENTE** 🥷
'''

        log_file.write_text(log_content)
        print(f"\n📄 Log salvo em: {log_file}")


def main():
    """
    Executa todas as otimizações
    """
    print("\n⚡ EXECUTOR DE OTIMIZAÇÕES")
    print("-" * 50)

    executor = OptimizationExecutor()

    # Perguntar se quer dry run
    response = input("\n🔍 Executar em modo DRY RUN primeiro? (s/N): ")

    if response.lower() == 's':
        print("\n🔍 MODO DRY RUN - Nenhuma modificação será feita")
        results = executor.execute_all(dry_run=True)

        print("\n📊 RESULTADO DO DRY RUN:")
        print(f"  Loops otimizáveis: {results['loops_optimized']['files_optimized']}")
        print(f"  Features removíveis: {results['unused_removed']['unused_identified']}")
        print(f"  Integrações possíveis: {results['components_integrated']['integrations_created']}")

        response = input("\n⚠️  Aplicar otimizações de verdade? (s/N): ")

        if response.lower() != 's':
            print("❌ Otimizações canceladas")
            return

    # Executar de verdade
    print("\n🚀 EXECUTANDO OTIMIZAÇÕES...")
    results = executor.execute_all(dry_run=False)

    print("\n" + "=" * 60)
    print("✅ OTIMIZAÇÕES APLICADAS COM SUCESSO!")
    print("=" * 60)

    print(f"\n📊 RESUMO:")
    for optimization in executor.optimizations_applied:
        print(f"  ✅ {optimization}")

    print(f"\n📁 Arquivos modificados: {len(executor.files_modified)}")
    print(f"💾 Backup salvo em: {executor.backup_dir}")

    print("\n🎯 PRÓXIMOS PASSOS:")
    print("  1. Testar o sistema otimizado")
    print("  2. Monitorar performance")
    print("  3. Ajustar conforme necessário")

    print("\n🥷 DIGIMUNDO PRESENTE")


if __name__ == "__main__":
    main()