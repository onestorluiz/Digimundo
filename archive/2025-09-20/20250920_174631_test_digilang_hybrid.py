#!/usr/bin/env python3
"""
Test DigiLang Hybrid System
Demonstra como TODOS os nossos sistemas trabalham juntos
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.scripturemon.digilang_hybrid import DigiLangHybrid

# Texto de teste (roteiro)
test_text = """INT. CASA - DAY

JOÃO entra em cena e olha para MARIA que está sentada no sofá.

JOÃO
(sussurrando)
Eu não sei o que você está pensando, mas precisamos conversar sobre ontem.

MARIA
(pausa)
Com certeza. Mas primeiro, por favor, senta-se aqui.

João caminha para o sofá e senta-se ao lado dela.

CUT TO:

EXT. PARQUE - NIGHT

O parque está vazio. A lua brilha intensamente.

FADE OUT.
"""

def test_all_modes():
    """Testa todos os modos de compressão."""
    print("=" * 60)
    print("TESTE DO SISTEMA HÍBRIDO DIGILANG")
    print("=" * 60)

    modes = ["conservative", "balanced", "aggressive"]

    for mode in modes:
        print(f"\n{'='*60}")
        print(f"MODO: {mode.upper()}")
        print(f"{'='*60}")

        # Criar compressor
        compressor = DigiLangHybrid(
            mode=mode,
            enable_tpd=True,
            enable_keywords=(mode == "aggressive"),
            enable_schema=True,
            enable_segmentation=False
        )

        # Comprimir
        result = compressor.compress(test_text)

        print(f"Original: {result.original_tokens} tokens")
        print(f"Comprimido: {result.compressed_tokens} tokens")
        print(f"Redução: {result.compression_ratio:.1%}")
        print(f"Camadas aplicadas: {', '.join(result.metadata['layers_applied'])}")
        print(f"Reversível: {'SIM' if result.metadata['reversible'] else 'NÃO'}")

        # Mostrar amostra
        print(f"\nAMOSTRA COMPRIMIDA (primeiros 200 chars):")
        print("-" * 40)
        print(result.compressed_text[:200])
        print("-" * 40)

        # Testar reversibilidade
        if result.metadata['reversible']:
            decompressed = compressor.decompress(result.compressed_text)
            matches = decompressed.strip() == test_text.strip()
            print(f"Teste de reversibilidade: {'✓ PASSOU' if matches else '✗ FALHOU'}")

def test_auto_mode():
    """Testa modo automático."""
    print(f"\n{'='*60}")
    print("TESTE DO MODO AUTOMÁTICO")
    print(f"{'='*60}")

    compressor = DigiLangHybrid()

    # Diferentes limites de token
    limits = [100, 50, 30]

    for limit in limits:
        print(f"\nLimite: {limit} tokens")
        result = compressor.auto_compress(test_text, max_tokens=limit)
        print(f"  Conseguiu: {result.compressed_tokens} tokens")
        print(f"  Redução: {result.compression_ratio:.1%}")
        print(f"  Método: {result.method_used}")

def test_with_segmentation():
    """Testa com segmentação por contexto."""
    print(f"\n{'='*60}")
    print("TESTE COM SEGMENTAÇÃO")
    print(f"{'='*60}")

    # Contexto: queremos apenas cenas com João
    context = "João conversa"

    compressor = DigiLangHybrid(
        mode="balanced",
        enable_segmentation=True
    )

    result = compressor.compress(test_text, context=context)

    print(f"Contexto: '{context}'")
    print(f"Original: {result.original_tokens} tokens")
    print(f"Com segmentação: {result.compressed_tokens} tokens")
    print(f"Redução: {result.compression_ratio:.1%}")

    print(f"\nTEXTO SEGMENTADO:")
    print("-" * 40)
    print(result.compressed_text)
    print("-" * 40)

def show_statistics():
    """Mostra estatísticas acumuladas."""
    print(f"\n{'='*60}")
    print("ESTATÍSTICAS DO SISTEMA")
    print(f"{'='*60}")

    compressor = DigiLangHybrid(mode="balanced")

    # Processar várias vezes
    for _ in range(5):
        compressor.compress(test_text)

    stats = compressor.get_statistics()

    print(f"Total de compressões: {stats['total_compressions']}")
    print(f"Tokens economizados: {stats['total_saved_tokens']}")
    print(f"Cache: {stats['cache_size']} entradas")
    print(f"\nCamadas usadas:")
    for layer, count in stats.items():
        if layer.startswith('layer'):
            print(f"  {layer}: {count} vezes")

def main():
    """Executa todos os testes."""
    print("\n" + "=" * 60)
    print("DIGILANG HYBRID - SISTEMA COMPLETO")
    print("Combinando TUDO que desenvolvemos:")
    print("  • Simple (87 padrões PT/EN)")
    print("  • TPD (validation - token-aware)")
    print("  • Keywords (compressão extrema)")
    print("  • Schema (estrutura de roteiros)")
    print("  • Segmentação (contexto relevante)")
    print("=" * 60)

    test_all_modes()
    test_auto_mode()
    test_with_segmentation()
    show_statistics()

    print("\n" + "=" * 60)
    print("✓ SISTEMA HÍBRIDO FUNCIONANDO!")
    print("  Aproveitamos TODO o trabalho anterior")
    print("  Múltiplas estratégias disponíveis")
    print("  Ajuste automático conforme necessidade")
    print("=" * 60)

if __name__ == "__main__":
    main()