#!/usr/bin/env python3
"""
🧪 TESTE RÁPIDO DOS MODOS mixtral
Script simplificado para testar ECO e DEDICATED
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


async def quick_test():
    """Teste rápido do mixtral"""

    from scripts.active.async_mixtral_processor import AsyncmixtralProcessor

    print("🧪 TESTE RÁPIDO mixtral mixtral")
    print("=" * 60)

    # Menu simples
    print("\n1. ECO (rápido, ~45GB RAM)")
    print("2. DEDICATED (completo, ~65GB RAM)")
    print("3. Ambos (comparação)")

    choice = input("\nEscolha: ").strip()

    # Roteiro de teste simples
    test_content = """FADE IN:

INT. ABANDONED WAREHOUSE - NIGHT

A cavernous space filled with shadows. WATER DRIPS from broken pipes.

SARAH (30s, determined) enters cautiously, flashlight cutting through darkness.

SARAH
(whispering into radio)
I'm inside. No sign of—

A METALLIC CLANG echoes. She freezes.

From the shadows emerges MARCUS (40s, scarred, dangerous).

MARCUS
You shouldn't have come alone.

SARAH
(steady, hand on weapon)
Who says I'm alone?

RED LASER DOTS appear on Marcus's chest. He smiles.

MARCUS
Neither am I.

MORE FIGURES emerge from the darkness. Sarah is surrounded.

SARAH
(into radio)
Now would be good.

EXPLOSION. The wall behind Marcus ERUPTS. SWAT team pours in.

FADE OUT.

THE END"""

    modes = []
    if choice == "1":
        modes = ["ECO"]
    elif choice == "2":
        modes = ["DEDICATED"]
    else:
        modes = ["ECO", "DEDICATED"]

    results = {}

    for mode in modes:
        print(f"\n{'='*60}")
        print(f"🚀 Testando modo {mode}")
        print(f"{'='*60}")

        processor = AsyncmixtralProcessor(mode=mode)

        # Processar
        result = await processor.process_screenplay(
            f"Test_Scene_{mode}",
            test_content
        )

        results[mode] = result

        # Mostrar resultado
        print(f"\n📊 Resultado {mode}:")
        print(f"  • Sucesso: {result['success']}")
        print(f"  • Tempo: {result['duration']:.1f}s")

        if result['success'] and result.get('analysis'):
            print(f"  • Análise: {len(result['analysis'])} chars")
            print(f"\n  Preview:")
            print("  " + "-" * 40)
            preview = result['analysis'][:300].replace('\n', '\n  ')
            print(f"  {preview}...")

    # Comparação se testou ambos
    if len(results) == 2:
        print(f"\n{'='*60}")
        print("📊 COMPARAÇÃO ECO vs DEDICATED:")
        print(f"{'='*60}")

        eco = results.get("ECO", {})
        ded = results.get("DEDICATED", {})

        print(f"\nTEMPO:")
        print(f"  • ECO: {eco.get('duration', 0):.1f}s")
        print(f"  • DEDICATED: {ded.get('duration', 0):.1f}s")

        print(f"\nTAMANHO ANÁLISE:")
        print(f"  • ECO: {len(eco.get('analysis', ''))} chars")
        print(f"  • DEDICATED: {len(ded.get('analysis', ''))} chars")

        if eco.get('model_info') and ded.get('model_info'):
            print(f"\nTOKENS/SEGUNDO:")
            print(f"  • ECO: {eco['model_info'].get('tokens_per_second', 0):.1f}")
            print(f"  • DEDICATED: {ded['model_info'].get('tokens_per_second', 0):.1f}")

    print(f"\n✅ Teste completo!")
    print(f"📁 Logs salvos em: data/logs/deep_learning_mixtral/")
    print("\nDIGIMUNDO PRESENTE 🥷")


if __name__ == "__main__":
    asyncio.run(quick_test())