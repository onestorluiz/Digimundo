#!/usr/bin/env python3
"""
🚀 LAUNCHER AUTOMÁTICO PARA MIXTRAL ENHANCED MASTER
Inicia processamento completo sem interação
Inclui teoria, meus_filmes e comparações com obras-primas
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.active.mixtral_enhanced_master import MixtralEnhancedMaster


async def main():
    """Lança diretamente o processamento completo"""

    print("🚀 INICIANDO MIXTRAL ENHANCED MASTER AUTOMATICAMENTE")
    print("=" * 60)
    print("Incluindo:")
    print("  • Teoria (13 livros)")
    print("  • Meus Filmes (seu roteiro)")
    print("  • Roteiros Mestres (34 obras)")
    print("  • Comparações com obras-primas")
    print("=" * 60)

    system = MixtralEnhancedMaster()

    # Processar tudo automaticamente
    await system.run_complete_analysis(limit=15)  # 15 análises completas

    print("\n✅ PROCESSAMENTO COMPLETO FINALIZADO!")
    print("DIGIMUNDO PRESENTE 🥷")


if __name__ == "__main__":
    print("🥷 LAUNCHER MIXTRAL ENHANCED MASTER")
    print("Iniciando processamento completo automatizado...")
    asyncio.run(main())