#!/usr/bin/env python3
"""
Teste único V10 para debug
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from apps.scripturemon.digilang_v10_supreme import DigiLangV10Supreme

# Testar com Dark Knight que sabemos funcionar
pdf_path = "./digilibrary/The Dark Knight - Release.pdf"

v10 = DigiLangV10Supreme()
result = v10.process_pdf(pdf_path)

if result:
    print(f"✅ Sucesso! Compressão: {result['stats']['token_compression']:.2f}%")
else:
    print("❌ Falhou")