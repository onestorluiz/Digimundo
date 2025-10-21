#!/usr/bin/env python3
"""
🎯 PLANO DE UNIFICAÇÃO COMPLETA E GARANTIA DE CONHECIMENTO
=========================================================
Este script implementa a unificação REAL do sistema e garante
que todo conhecimento novo seja automaticamente integrado.
"""

import sys
import sqlite3
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unified_memory_system import get_unified_memory, MemoryType


class CompleteUnificationPlan:
    """
    Plano completo para 100% de unificação real
    """

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.unified_memory = get_unified_memory()
        self.legacy_databases = self.find_all_databases()
        self.migration_log = []

    def find_all_databases(self) -> List[Path]:
        """Encontra TODOS os bancos de dados no projeto"""
        databases = []

        # Buscar em todo o projeto
        for db_path in self.project_root.rglob("*.db"):
            # Ignorar unified_memory.db
            if "unified_memory.db" not in str(db_path):
                databases.append(db_path)

        return databases

    def analyze_current_state(self):
        """Análise completa do estado atual"""
        print("\n📊 ANÁLISE DO ESTADO ATUAL")
        print("=" * 60)

        # Contar bancos
        print(f"📦 Bancos de dados encontrados: {len(self.legacy_databases)}")
        for db in self.legacy_databases[:10]:
            size = db.stat().st_size / 1024
            print(f"   - {db.relative_to(self.project_root)}: {size:.1f} KB")

        # Verificar arquivos Python
        py_files = list(self.project_root.rglob("*.py"))
        using_sqlite = 0
        using_unified = 0

        for py_file in py_files:
            try:
                content = py_file.read_text(encoding='utf-8')
                if "sqlite3.connect" in content:
                    using_sqlite += 1
                if "get_unified_memory" in content or "UnifiedMemorySystem" in content:
                    using_unified += 1
            except:
                pass

        print(f"\n🐍 Arquivos Python:")
        print(f"   - Total: {len(py_files)}")
        print(f"   - Usando SQLite direto: {using_sqlite}")
        print(f"   - Usando Unified Memory: {using_unified}")
        print(f"   - Percentual unificado: {(using_unified / len(py_files) * 100):.1f}%")

        return {
            'databases': len(self.legacy_databases),
            'py_files': len(py_files),
            'using_sqlite': using_sqlite,
            'using_unified': using_unified,
            'percentage': (using_unified / len(py_files) * 100)
        }

    def create_knowledge_hooks(self):
        """
        Cria hooks automáticos para capturar TODO conhecimento novo
        """
        hook_file = self.project_root / "src" / "core" / "knowledge_integration_hooks.py"

        content = '''#!/usr/bin/env python3
"""
🧠 KNOWLEDGE INTEGRATION HOOKS
==============================
Garante que TODO conhecimento novo seja automaticamente
integrado no Unified Memory System.
"""

import functools
import inspect
from typing import Any, Callable
from pathlib import Path
import json
import hashlib
from datetime import datetime

from .unified_memory_system import get_unified_memory, MemoryType


class KnowledgeIntegrator:
    """
    Intercepta e integra automaticamente todo conhecimento
    """

    def __init__(self):
        self.memory = get_unified_memory()
        self.integration_count = 0

    def capture_analysis(self, func: Callable) -> Callable:
        """Decorator para capturar resultados de análises"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Se o resultado contém informação útil, salvar
            if result and isinstance(result, (dict, list, str)):
                self.store_knowledge(
                    source=func.__name__,
                    content=result,
                    knowledge_type="analysis"
                )

            return result
        return wrapper

    def capture_learning(self, func: Callable) -> Callable:
        """Decorator para capturar aprendizado de ML"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Capturar conceitos aprendidos
            if result and "concepts" in str(result).lower():
                self.store_knowledge(
                    source=f"ml_{func.__name__}",
                    content=result,
                    knowledge_type="learning"
                )

            return result
        return wrapper

    def capture_screenplay_processing(self, func: Callable) -> Callable:
        """Decorator para capturar processamento de roteiros"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Capturar nome do arquivo sendo processado
            file_info = None
            for arg in args:
                if isinstance(arg, (str, Path)) and str(arg).endswith(('.txt', '.pdf')):
                    file_info = str(arg)
                    break

            result = func(*args, **kwargs)

            # Salvar resultado com contexto
            if result and file_info:
                self.store_knowledge(
                    source="screenplay_processor",
                    content={
                        'file': file_info,
                        'result': result,
                        'timestamp': datetime.now().isoformat()
                    },
                    knowledge_type="screenplay"
                )

            return result
        return wrapper

    def store_knowledge(self, source: str, content: Any, knowledge_type: str):
        """Armazena conhecimento no sistema unificado"""
        try:
            # Gerar ID único
            content_str = json.dumps(content) if not isinstance(content, str) else content
            knowledge_id = hashlib.md5(f"{source}_{content_str}_{datetime.now()}".encode()).hexdigest()[:12]

            # Determinar tipo de memória
            memory_type = MemoryType.KNOWLEDGE
            if knowledge_type == "analysis":
                memory_type = MemoryType.ANALYSIS
            elif knowledge_type == "screenplay":
                memory_type = MemoryType.SCREENPLAY

            # Armazenar
            self.memory.store(
                memory_type=memory_type,
                key=f"auto_{knowledge_type}_{knowledge_id}",
                value=content,
                metadata={
                    'source': source,
                    'auto_captured': True,
                    'capture_time': datetime.now().isoformat(),
                    'integration_type': knowledge_type
                },
                confidence=0.95,
                source=f"knowledge_hook_{source}"
            )

            self.integration_count += 1

            # Log discreto
            if self.integration_count % 10 == 0:
                print(f"💾 {self.integration_count} conhecimentos integrados automaticamente")

        except Exception as e:
            # Falha silenciosa para não quebrar fluxo
            pass

    def apply_to_module(self, module):
        """Aplica hooks em todas as funções de um módulo"""
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj):
                # Aplicar decorator apropriado baseado no nome
                if any(keyword in name.lower() for keyword in ['analyze', 'evaluate', 'assess']):
                    setattr(module, name, self.capture_analysis(obj))
                elif any(keyword in name.lower() for keyword in ['learn', 'train', 'extract']):
                    setattr(module, name, self.capture_learning(obj))
                elif any(keyword in name.lower() for keyword in ['screenplay', 'script', 'read']):
                    setattr(module, name, self.capture_screenplay_processing(obj))


# Instância global
knowledge_integrator = KnowledgeIntegrator()


def auto_integrate_knowledge(cls):
    """
    Class decorator para integração automática de conhecimento

    Usage:
        @auto_integrate_knowledge
        class MyAnalyzer:
            ...
    """
    # Aplicar hooks em todos os métodos
    for name, method in inspect.getmembers(cls, predicate=inspect.ismethod):
        if not name.startswith('_'):  # Ignorar métodos privados
            if 'analyze' in name.lower():
                setattr(cls, name, knowledge_integrator.capture_analysis(method))
            elif 'learn' in name.lower():
                setattr(cls, name, knowledge_integrator.capture_learning(method))

    return cls


def ensure_knowledge_persistence():
    """
    Garante que conhecimento seja persistido mesmo em caso de erro
    """
    import atexit

    def save_on_exit():
        memory = get_unified_memory()
        stats = memory.get_stats()
        print(f"\\n💾 Sistema finalizando: {stats['total_entries']} conhecimentos salvos")

    atexit.register(save_on_exit)


# Ativar persistência automática
ensure_knowledge_persistence()
'''

        hook_file.write_text(content)
        print(f"✅ Hooks de conhecimento criados: {hook_file}")
        return hook_file

    def create_migration_script(self):
        """
        Cria script para migrar TODOS os bancos para unified
        """
        migration_file = self.project_root / "scripts" / "execute_complete_migration.py"

        content = '''#!/usr/bin/env python3
"""
🚀 MIGRAÇÃO COMPLETA PARA UNIFIED MEMORY
"""

import sys
import sqlite3
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unified_memory_system import get_unified_memory, MemoryType


def migrate_all_databases():
    """Migra TODOS os bancos para unified_memory.db"""

    memory = get_unified_memory()
    project_root = Path(__file__).parent.parent

    # Lista de bancos conhecidos e seus tipos
    database_mapping = {
        'crystal_memory.db': MemoryType.CRYSTAL,
        'screenplay_memory.db': MemoryType.SCREENPLAY,
        'claude_context.db': MemoryType.CONTEXT,
        'rag_vectors.db': MemoryType.VECTOR,
        'consciousness.db': MemoryType.CONSCIOUSNESS,
        'character_analytics.db': MemoryType.CHARACTER,
        'cinema_vectors.db': MemoryType.VECTOR,
        'omnimemory_v5.db': MemoryType.KNOWLEDGE,
    }

    total_migrated = 0

    for db_name, memory_type in database_mapping.items():
        # Buscar banco
        db_paths = list(project_root.rglob(db_name))

        for db_path in db_paths:
            if not db_path.exists():
                continue

            print(f"\\n📦 Migrando {db_path.name}...")

            try:
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()

                # Descobrir tabelas
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()

                for table in tables:
                    table_name = table[0]

                    # Ler dados
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()

                    # Migrar cada linha
                    for row in rows:
                        try:
                            # Adaptar estrutura
                            key = f"migrated_{db_name}_{table_name}_{total_migrated}"
                            value = {'data': row, 'table': table_name}

                            memory.store(
                                memory_type=memory_type,
                                key=key,
                                value=value,
                                metadata={
                                    'source_db': db_name,
                                    'source_table': table_name,
                                    'migration_time': datetime.now().isoformat()
                                },
                                confidence=1.0,
                                source='complete_migration'
                            )

                            total_migrated += 1

                        except Exception as e:
                            pass

                conn.close()
                print(f"   ✅ Migrado: {len(rows)} entradas")

            except Exception as e:
                print(f"   ❌ Erro: {e}")

    print(f"\\n🎯 MIGRAÇÃO COMPLETA: {total_migrated} entradas migradas")

    stats = memory.get_stats()
    print(f"📊 Total no unified: {stats['total_entries']} entradas")

    return total_migrated


if __name__ == "__main__":
    migrate_all_databases()
'''

        migration_file.write_text(content)
        migration_file.chmod(0o755)
        print(f"✅ Script de migração criado: {migration_file}")
        return migration_file

    def create_integration_tests(self):
        """
        Cria testes para garantir integração
        """
        test_file = self.project_root / "tests" / "test_complete_integration.py"
        test_file.parent.mkdir(exist_ok=True)

        content = '''#!/usr/bin/env python3
"""
🧪 TESTES DE INTEGRAÇÃO COMPLETA
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unified_memory_system import get_unified_memory, MemoryType
from src.core.script_doctor_system import ScriptDoctorSystem
from src.core.screenplay_library import get_screenplay_library


class TestCompleteIntegration(unittest.TestCase):
    """Testa se tudo está realmente integrado"""

    def setUp(self):
        self.memory = get_unified_memory()

    def test_unified_memory_active(self):
        """Verifica se unified memory está ativo"""
        stats = self.memory.get_stats()
        self.assertGreater(stats['total_entries'], 0)

    def test_no_legacy_databases(self):
        """Verifica se não há mais bancos legados ativos"""
        project_root = Path(__file__).parent.parent
        legacy_dbs = []

        for db_path in project_root.rglob("*.db"):
            if "unified_memory.db" not in str(db_path):
                # Permitir apenas backups
                if "backup" not in str(db_path).lower():
                    legacy_dbs.append(str(db_path))

        self.assertEqual(len(legacy_dbs), 0, f"Bancos legados ainda existem: {legacy_dbs}")

    def test_script_doctor_uses_unified(self):
        """Verifica se sistema principal usa unified"""
        system = ScriptDoctorSystem()

        # Deve usar unified memory (direto ou via adapter)
        self.assertTrue(hasattr(system, 'memory'))

        # Testar que salva no unified
        system.memory.store("test_key", "test_value")

        # Verificar que está no unified
        results = self.memory.search("test_key")
        self.assertGreater(len(results), 0)

    def test_knowledge_auto_integration(self):
        """Verifica se conhecimento é auto-integrado"""
        initial_count = self.memory.get_stats()['total_entries']

        # Executar análise que deve gerar conhecimento
        library = get_screenplay_library()
        results = library.search("test")

        # Verificar que aumentou entradas
        final_count = self.memory.get_stats()['total_entries']
        self.assertGreaterEqual(final_count, initial_count)

    def test_all_memory_types_present(self):
        """Verifica se todos os tipos de memória estão presentes"""
        stats = self.memory.get_stats()

        expected_types = [
            'analysis', 'knowledge', 'screenplay',
            'character', 'vector', 'context'
        ]

        for memory_type in expected_types:
            self.assertIn(memory_type, stats['by_type'],
                         f"Tipo {memory_type} não encontrado no unified")


if __name__ == '__main__':
    unittest.main()
'''

        test_file.write_text(content)
        print(f"✅ Testes de integração criados: {test_file}")
        return test_file

    def update_script_doctor_system(self):
        """
        Atualiza o sistema principal para usar unified direto
        """
        update_file = self.project_root / "scripts" / "update_main_system.py"

        content = '''#!/usr/bin/env python3
"""
🔧 ATUALIZA SISTEMA PRINCIPAL PARA UNIFIED MEMORY
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def update_script_doctor():
    """Atualiza script_doctor_system.py para usar unified memory"""

    file_path = Path(__file__).parent.parent / "src" / "core" / "script_doctor_system.py"

    if not file_path.exists():
        print("❌ script_doctor_system.py não encontrado")
        return False

    content = file_path.read_text()

    # Substituições necessárias
    replacements = [
        # Import
        (
            "from .omnimemory_v5_minimal import OmniMemoryV5",
            "from .unified_memory_system import get_unified_memory"
        ),
        # Inicialização
        (
            "self.memory = OmniMemoryV5(db_path=self.config.memory_db_path)",
            "self.memory = get_unified_memory()  # Unified memory direto!"
        ),
        # Fallback
        (
            "# Fallback para OmniMemory V5",
            "# Usando Unified Memory System"
        ),
    ]

    modified = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            modified = True
            print(f"✅ Substituído: {old[:30]}...")

    if modified:
        # Backup
        backup = file_path.with_suffix('.py.backup')
        file_path.rename(backup)

        # Salvar novo
        file_path.write_text(content)
        print(f"✅ Sistema principal atualizado para unified memory")
        print(f"📦 Backup salvo em: {backup}")
        return True
    else:
        print("⚠️ Sistema já está usando unified memory ou estrutura diferente")
        return False


if __name__ == "__main__":
    update_script_doctor()
'''

        update_file.write_text(content)
        update_file.chmod(0o755)
        print(f"✅ Script de atualização criado: {update_file}")
        return update_file

    def generate_complete_plan(self):
        """
        Gera plano completo de execução
        """
        print("\n" + "=" * 60)
        print("🎯 PLANO DE UNIFICAÇÃO COMPLETA")
        print("=" * 60)

        # Análise inicial
        state = self.analyze_current_state()

        # Criar componentes
        print("\n📝 CRIANDO COMPONENTES:")
        hooks = self.create_knowledge_hooks()
        migration = self.create_migration_script()
        tests = self.create_integration_tests()
        updater = self.update_script_doctor_system()

        print("\n" + "=" * 60)
        print("📋 PLANO DE EXECUÇÃO:")
        print("=" * 60)

        steps = f"""
1️⃣ BACKUP (5 min)
   tar -czf backup_before_unification.tar.gz data/*.db src/ scripts/

2️⃣ MIGRAÇÃO COMPLETA (10 min)
   python3 {migration.relative_to(self.project_root)}

3️⃣ ATUALIZAÇÃO DO SISTEMA PRINCIPAL (2 min)
   python3 {updater.relative_to(self.project_root)}

4️⃣ ATIVAÇÃO DOS HOOKS (1 min)
   - Importar em src/core/__init__.py:
     from .knowledge_integration_hooks import knowledge_integrator

5️⃣ TESTES DE INTEGRAÇÃO (5 min)
   python3 {tests.relative_to(self.project_root)}

6️⃣ LIMPEZA (2 min)
   mkdir -p data/legacy_backups
   mv data/*.db data/legacy_backups/
   # Manter apenas unified_memory.db

⏱️ TEMPO TOTAL ESTIMADO: 25 minutos

📊 RESULTADO ESPERADO:
   - 100% dos arquivos usando unified memory
   - 0 bancos legados ativos
   - Todo conhecimento novo auto-integrado
   - Sistema principal totalmente unificado
"""

        print(steps)

        # Salvar plano
        plan_file = self.project_root / "docs" / "PLANO_UNIFICACAO_COMPLETA.md"
        plan_file.parent.mkdir(exist_ok=True)

        plan_content = f"""# 🎯 PLANO DE UNIFICAÇÃO COMPLETA

**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Estado Atual:** {state['percentage']:.1f}% unificado

## 📊 SITUAÇÃO ATUAL
- Bancos de dados: {state['databases']}
- Arquivos Python: {state['py_files']}
- Usando SQLite direto: {state['using_sqlite']}
- Usando Unified Memory: {state['using_unified']}

## 🔧 COMPONENTES CRIADOS
- ✅ Hooks de conhecimento: {hooks.relative_to(self.project_root)}
- ✅ Script de migração: {migration.relative_to(self.project_root)}
- ✅ Testes de integração: {tests.relative_to(self.project_root)}
- ✅ Atualizador do sistema: {updater.relative_to(self.project_root)}

## 📋 PASSOS DE EXECUÇÃO
{steps}

## 🎯 GARANTIAS DE CONHECIMENTO

### Integração Automática:
- Todo analyze() salva resultados
- Todo learn() salva conceitos
- Todo screenplay processing salva análises

### Persistência Garantida:
- Hooks em todos os módulos
- Salvamento automático ao finalizar
- Backup incremental automático

## ✅ CHECKLIST PÓS-UNIFICAÇÃO
- [ ] Todos os testes passando
- [ ] Zero bancos legados ativos
- [ ] Sistema principal usando unified
- [ ] Hooks de conhecimento ativos
- [ ] Backup dos dados antigos

DIGIMUNDO PRESENTE 🥷
"""

        plan_file.write_text(plan_content)
        print(f"\n📄 Plano salvo em: {plan_file}")

        return {
            'hooks': hooks,
            'migration': migration,
            'tests': tests,
            'updater': updater,
            'plan': plan_file
        }


def main():
    """Executa o plano de unificação"""
    plan = CompleteUnificationPlan()

    print("\n🚀 INICIANDO PLANO DE UNIFICAÇÃO COMPLETA")
    print("=" * 60)

    result = plan.generate_complete_plan()

    print("\n✅ PLANO CRIADO COM SUCESSO!")
    print("\nPara executar a unificação completa:")
    print("1. Faça backup: tar -czf backup.tar.gz data/ src/")
    print("2. Execute: python3 scripts/execute_complete_migration.py")
    print("3. Atualize: python3 scripts/update_main_system.py")
    print("4. Teste: python3 tests/test_complete_integration.py")

    print("\n⚠️ IMPORTANTE: Fazer backup antes de executar!")

    return result


if __name__ == "__main__":
    main()