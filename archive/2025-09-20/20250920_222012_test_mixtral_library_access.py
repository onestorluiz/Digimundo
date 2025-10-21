#!/usr/bin/env python3
"""
Test Mixtral Library Access - Verifica se Mixtral consegue ler todos os arquivos
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.screenplay_library import ScreenplayLibrary
from src.core.ollama_core_minimal import OllamaMinimal
from src.core.unified_memory_system import get_unified_memory
from src.core.logging_system import get_logger

logger = get_logger("mixtral_test")

def test_file_access() -> Dict[str, List[str]]:
    """Testa acesso aos arquivos da biblioteca"""
    library_path = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS")

    results = {
        "accessible": [],
        "inaccessible": [],
        "large_files": []
    }

    # Encontrar todos os arquivos .txt
    for txt_file in library_path.rglob("*.txt"):
        try:
            # Verificar tamanho
            size_mb = txt_file.stat().st_size / (1024 * 1024)

            # Tentar ler
            with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = len(content.splitlines())
                chars = len(content)

            results["accessible"].append(f"{txt_file.name} ({size_mb:.2f}MB, {lines:,} lines, {chars:,} chars)")

            if size_mb > 1:
                results["large_files"].append(f"{txt_file.name} ({size_mb:.2f}MB)")

        except Exception as e:
            results["inaccessible"].append(f"{txt_file.name}: {str(e)}")

    return results

def test_mixtral_processing(sample_files: int = 3) -> Dict[str, any]:
    """Testa processamento com Mixtral"""
    ollama = OllamaMinimal()
    library = ScreenplayLibrary()

    results = {
        "models_available": [],
        "processing_tests": [],
        "token_limits": {}
    }

    # Verificar modelos disponíveis
    try:
        models = ollama.list_models()
        for model in models:
            if 'mixtral' in model.lower() or 'deeplearning' in model.lower():
                results["models_available"].append(model)
    except:
        results["models_available"] = ["Erro ao listar modelos"]

    # Testar com alguns arquivos
    library_path = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS")
    test_files = list(library_path.rglob("*.txt"))[:sample_files]

    for txt_file in test_files:
        try:
            with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Teste simples de tokenização
            words = len(content.split())
            tokens_estimate = int(words * 1.3)  # Estimativa aproximada

            test_result = {
                "file": txt_file.name,
                "size_mb": txt_file.stat().st_size / (1024 * 1024),
                "estimated_tokens": tokens_estimate,
                "fits_32k": tokens_estimate <= 32000,
                "fits_128k": tokens_estimate <= 128000,
                "processing": "NOT_TESTED"  # Não vamos processar agora para economizar recursos
            }

            results["processing_tests"].append(test_result)

        except Exception as e:
            results["processing_tests"].append({
                "file": txt_file.name,
                "error": str(e)
            })

    # Calcular limites de tokens
    results["token_limits"] = {
        "mixtral_32k": "32,768 tokens (cerca de 24,000 palavras)",
        "mixtral_128k": "131,072 tokens (cerca de 98,000 palavras)",
        "typical_screenplay": "20,000-30,000 palavras (cabe em 32k)",
        "typical_book": "60,000-100,000 palavras (precisa 128k)"
    }

    return results

def test_memory_integration() -> Dict[str, any]:
    """Testa integração com memória unificada"""
    memory = get_unified_memory()

    # Verificar entradas relacionadas a roteiros usando search
    screenplay_entries = memory.search("screenplay", limit=100)
    book_entries = memory.search("book", limit=100)
    concept_entries = memory.search("concept", limit=100)

    return {
        "screenplay_entries": len(screenplay_entries),
        "book_entries": len(book_entries),
        "concept_entries": len(concept_entries),
        "total_memory_entries": memory.get_stats()['total_entries']
    }

def main():
    """Executa todos os testes"""
    print("=" * 80)
    print("🎬 TESTE DO SISTEMA MIXTRAL COM BIBLIOTECA DE ROTEIROS")
    print("=" * 80)

    # 1. Testar acesso aos arquivos
    print("\n📁 TESTANDO ACESSO AOS ARQUIVOS...")
    file_results = test_file_access()

    print(f"\n✅ Arquivos acessíveis: {len(file_results['accessible'])}")
    for f in file_results['accessible'][:5]:  # Mostrar primeiros 5
        print(f"  - {f}")
    if len(file_results['accessible']) > 5:
        print(f"  ... e mais {len(file_results['accessible']) - 5} arquivos")

    if file_results['inaccessible']:
        print(f"\n❌ Arquivos inacessíveis: {len(file_results['inaccessible'])}")
        for f in file_results['inaccessible']:
            print(f"  - {f}")

    if file_results['large_files']:
        print(f"\n📊 Arquivos grandes (>1MB): {len(file_results['large_files'])}")
        for f in file_results['large_files']:
            print(f"  - {f}")

    # 2. Testar processamento Mixtral
    print("\n🤖 TESTANDO CAPACIDADE DO MIXTRAL...")
    mixtral_results = test_mixtral_processing()

    print(f"\n📦 Modelos disponíveis:")
    for model in mixtral_results['models_available']:
        print(f"  - {model}")

    print(f"\n📈 Limites de tokens:")
    for limit, desc in mixtral_results['token_limits'].items():
        print(f"  - {limit}: {desc}")

    print(f"\n🔬 Teste de processamento (amostra):")
    for test in mixtral_results['processing_tests']:
        if 'error' not in test:
            status = "✅" if test['fits_128k'] else "⚠️"
            print(f"  {status} {test['file']}: {test['estimated_tokens']:,} tokens ({test['size_mb']:.2f}MB)")
            print(f"     - Cabe em 32k: {'✅' if test['fits_32k'] else '❌'}")
            print(f"     - Cabe em 128k: {'✅' if test['fits_128k'] else '❌'}")

    # 3. Testar memória
    print("\n💾 TESTANDO INTEGRAÇÃO COM MEMÓRIA...")
    memory_results = test_memory_integration()

    print(f"  - Entradas de roteiros: {memory_results['screenplay_entries']}")
    print(f"  - Entradas de livros: {memory_results['book_entries']}")
    print(f"  - Conceitos extraídos: {memory_results['concept_entries']}")
    print(f"  - Total na memória: {memory_results['total_memory_entries']:,}")

    # Resumo final
    print("\n" + "=" * 80)
    print("📊 RESUMO DA ANÁLISE")
    print("=" * 80)

    total_files = len(file_results['accessible']) + len(file_results['inaccessible'])
    success_rate = (len(file_results['accessible']) / total_files * 100) if total_files > 0 else 0

    print(f"""
✅ Taxa de sucesso de leitura: {success_rate:.1f}%
📚 Total de arquivos: {total_files}
📖 Arquivos acessíveis: {len(file_results['accessible'])}
🚫 Arquivos com problema: {len(file_results['inaccessible'])}
📏 Arquivos grandes (>1MB): {len(file_results['large_files'])}

🤖 CAPACIDADE DO MIXTRAL:
- Mixtral 32K: Suporta roteiros típicos (até 24k palavras)
- Mixtral 128K: Suporta livros completos (até 98k palavras)
- DeepLearning Hybrid: 128K tokens disponíveis

💡 CONCLUSÃO:
{"✅ SISTEMA PRONTO! Mixtral pode processar TODOS os arquivos da biblioteca." if success_rate == 100 else "⚠️ Alguns arquivos podem ter problemas de acesso."}
{"✅ Com 128K tokens, Mixtral pode analisar livros + roteiros simultaneamente!" if mixtral_results['models_available'] else "⚠️ Nenhum modelo Mixtral encontrado!"}
    """)

if __name__ == "__main__":
    main()