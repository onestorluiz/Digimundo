#!/usr/bin/env python3
"""
Teste de integração DigiLibrary + DigiLang
"""

import sys
sys.path.insert(0, '.')

from apps.scripturemon.digilibrary_integration import get_digilibrary_manager, get_digilang_integration

def test_digilibrary():
    """Testa integração da biblioteca."""
    print("=" * 50)
    print("TESTE DIGILIBRARY + DIGILANG")
    print("=" * 50)

    # Inicializa gerenciador
    print("\n1. Inicializando DigiLibrary...")
    library = get_digilibrary_manager()

    # Estatísticas
    stats = library.get_statistics()
    print(f"\n📚 Biblioteca carregada:")
    print(f"   - Total de documentos: {stats['total_documents']}")
    print(f"   - Roteiros mestres: {stats['categories']['master_scripts']}")
    print(f"   - Teoria: {stats['categories']['theory']}")
    print(f"   - Meus filmes: {stats['categories']['my_films']}")

    # Busca
    print("\n2. Testando busca...")
    results = library.search("cinema")
    print(f"   - Resultados para 'cinema': {len(results)} documentos")

    # DigiLang integration
    print("\n3. Testando DigiLang...")
    digilang = get_digilang_integration()

    test_text = """
    FADE IN:

    INT. CAFÉ - DAY

    JOHN, 30s, nervously sips his coffee while reading a screenplay.
    His eyes widen as he reaches the climax.

    JOHN
    (whispering to himself)
    This is it... this is the one.

    He closes the script, determination in his eyes.
    """

    compressed, ratio = digilang.compress_text(test_text)
    print(f"   - Texto original: {len(test_text)} bytes")
    print(f"   - Texto comprimido: {len(str(compressed))} bytes")
    print(f"   - Taxa de compressão: {ratio:.2%}")

    # Otimização para Ollama
    print("\n4. Testando otimização para Ollama...")
    long_prompt = test_text * 100  # Simula prompt longo
    optimized = digilang.optimize_for_ollama(long_prompt)
    print(f"   - Prompt original: {len(long_prompt)} caracteres")
    print(f"   - Prompt otimizado: {len(optimized)} caracteres")

    print("\n✅ Todos os testes passaram!")
    print("=" * 50)

if __name__ == "__main__":
    test_digilibrary()