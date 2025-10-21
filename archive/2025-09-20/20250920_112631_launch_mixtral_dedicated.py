#!/usr/bin/env python3
"""
🚀 LAUNCHER DIRETO PARA MIXTRAL DEDICATED MODE
Inicia processamento contínuo sem interação
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.active.mixtral_primary_system import MixtralPrimarySystem


async def main():
    """Lança diretamente o modo Dedicado"""

    print("🚀 INICIANDO MIXTRAL DEDICATED MODE AUTOMATICAMENTE")
    print("=" * 60)

    processor = MixtralPrimarySystem()

    # Inicia diretamente processamento dedicado com 10 roteiros
    await processor.run_continuous_analysis(mode="dedicated", limit=10)


if __name__ == "__main__":
    print("🥷 LAUNCHER MIXTRAL DEDICATED")
    print("Iniciando processamento automatizado...")
    asyncio.run(main())