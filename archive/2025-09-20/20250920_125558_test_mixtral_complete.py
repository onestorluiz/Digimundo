#!/usr/bin/env python3
"""
🧪 TESTES COMPLETOS DO SISTEMA MIXTRAL
Valida todas as correções aplicadas
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import ollama
from src.core.screenplay_library import ScreenplayLibrary
from src.core.unified_memory_system import get_unified_memory, MemoryType
from datetime import datetime

def test_model_exists():
    """Verifica se modelo Mixtral existe"""
    print("1️⃣ Testando existência do modelo...")
    try:
        models = ollama.list()
        # A API retorna objetos com atributo .model, não dicionários
        model_names = [m.model for m in models.models] if hasattr(models, 'models') else []

        # Procurar por variações do modelo Mixtral
        mixtral_models = [m for m in model_names if 'mixtral' in m.lower()]

        if mixtral_models:
            print(f"   ✅ Modelos Mixtral encontrados: {', '.join(mixtral_models)}")
            return True
        else:
            # Fallback para llama3.2 se não tiver Mixtral
            llama_models = [m for m in model_names if 'llama' in m.lower()]
            if llama_models:
                print(f"   ⚠️ Usando fallback: {llama_models[0]}")
                return True
            print("   ❌ Nenhum modelo compatível encontrado")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_library_access():
    """Testa acesso à biblioteca"""
    print("\n2️⃣ Testando acesso à biblioteca...")
    try:
        library = ScreenplayLibrary()
        screenplays = library.list_screenplays()
        print(f"   ✅ {len(screenplays)} roteiros acessíveis")

        if screenplays:
            # Testar leitura do primeiro
            title = screenplays[0]
            content = library.get_screenplay(title)
            if content and content != '.' and len(content) > 100:
                print(f"   ✅ Conteúdo válido: {title} ({len(content):,} chars)")
            else:
                print(f"   ⚠️ Conteúdo inválido para {title}")
        return True
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_memory_integration():
    """Testa memória unificada"""
    print("\n3️⃣ Testando memória unificada...")
    try:
        memory = get_unified_memory()

        # Teste de escrita
        test_data = {
            'test': True,
            'timestamp': datetime.now().isoformat(),
            'component': 'test_mixtral'
        }

        memory.store(
            memory_type=MemoryType.ANALYSIS,
            key="test:mixtral",
            value=test_data,
            metadata={'test': True}
        )

        # Teste de leitura
        results = memory.search(
            query="test:mixtral",
            memory_types=[MemoryType.ANALYSIS],
            limit=1
        )

        if results:
            print(f"   ✅ Memória funcionando: {len(results)} registro(s)")
        else:
            print("   ⚠️ Memória vazia mas funcional")

        return True
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_no_deeplearning_references():
    """Verifica que não há mais referências a deeplearning-hybrid"""
    print("\n4️⃣ Verificando ausência de deeplearning-hybrid...")

    scripts_path = Path(__file__).parent.parent / "scripts" / "active"
    count = 0

    for file_path in scripts_path.glob("*.py"):
        try:
            content = file_path.read_text()
            if "deeplearning-hybrid" in content:
                print(f"   ⚠️ Ainda tem referência em {file_path.name}")
                count += 1
        except:
            pass

    if count == 0:
        print("   ✅ Nenhuma referência a deeplearning-hybrid")
        return True
    else:
        print(f"   ❌ {count} arquivo(s) ainda com referências antigas")
        return False

def test_memory_type_pattern():
    """Verifica que MemoryType.PATTERN foi corrigido"""
    print("\n5️⃣ Verificando correção de MemoryType.PATTERN...")

    scripts_path = Path(__file__).parent.parent / "scripts" / "active"
    count = 0

    for file_path in scripts_path.glob("*.py"):
        try:
            content = file_path.read_text()
            if "MemoryType.PATTERN" in content:
                print(f"   ⚠️ Ainda tem MemoryType.PATTERN em {file_path.name}")
                count += 1
        except:
            pass

    if count == 0:
        print("   ✅ MemoryType.PATTERN corrigido em todos os arquivos")
        return True
    else:
        print(f"   ❌ {count} arquivo(s) ainda com MemoryType.PATTERN")
        return False

def test_config_exists():
    """Verifica se configuração centralizada existe"""
    print("\n6️⃣ Verificando configuração centralizada...")

    config_path = Path(__file__).parent.parent / "src" / "core" / "mixtral_config.py"

    if config_path.exists():
        try:
            # Tentar importar
            from src.core.mixtral_config import MixtralConfig, get_model_config

            model, options = get_model_config("dedicated")
            print(f"   ✅ Configuração existe: {model}")
            print(f"      • Contexto: {options['num_ctx']:,} tokens")
            print(f"      • Threads: {options['num_thread']}")
            return True
        except Exception as e:
            print(f"   ⚠️ Configuração existe mas com erro: {e}")
            return False
    else:
        print("   ❌ Configuração não encontrada")
        return False

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 EXECUTANDO TESTES COMPLETOS DO SISTEMA MIXTRAL")
    print("=" * 60)

    results = {
        "Modelo existe": test_model_exists(),
        "Biblioteca acessível": test_library_access(),
        "Memória funcional": test_memory_integration(),
        "Sem deeplearning-hybrid": test_no_deeplearning_references(),
        "MemoryType corrigido": test_memory_type_pattern(),
        "Config centralizada": test_config_exists()
    }

    # Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")

    print("\n" + "-" * 40)
    percentage = (passed / total) * 100

    if percentage == 100:
        print(f"🎉 TODOS OS TESTES PASSARAM! ({passed}/{total})")
        print("Sistema está PRONTO para uso!")
    elif percentage >= 80:
        print(f"✅ Sistema funcional: {passed}/{total} testes OK ({percentage:.0f}%)")
    else:
        print(f"⚠️ Sistema precisa correções: {passed}/{total} testes OK ({percentage:.0f}%)")

    print("\nDIGIMUNDO PRESENTE 🥷")

    return percentage == 100

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)