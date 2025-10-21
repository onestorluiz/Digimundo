#!/usr/bin/env python3
"""
Teste dos componentes da API sem Flask
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from apps.scripturemon.ocr_pipeline import OCRPipeline
from apps.scripturemon.pdf_detector import PDFDetector
from apps.scripturemon.screenplay_normalizer import ScreenplayNormalizer
from apps.scripturemon.digilang_v7_ultimate import DigiLangV7Ultimate
from apps.scripturemon.ollama_prospero import OllamaPróspero, ModeloPróspero
from apps.scripturemon.unified_manager import UnifiedMemoryManager
from apps.scripturemon.ai_sentiment import analyze_text_sentiment

print("=" * 60)
print("TESTE DE COMPONENTES DA API")
print("=" * 60)

# Teste de inicialização
components = {}

try:
    print("\n1. Inicializando OCR Pipeline...")
    components['ocr'] = OCRPipeline()
    print("   ✅ OCR Pipeline inicializado")
except Exception as e:
    print(f"   ❌ Erro: {e}")

try:
    print("\n2. Inicializando PDF Detector...")
    components['pdf'] = PDFDetector()
    print("   ✅ PDF Detector inicializado")
except Exception as e:
    print(f"   ❌ Erro: {e}")

try:
    print("\n3. Inicializando Normalizer...")
    components['normalizer'] = ScreenplayNormalizer()
    print("   ✅ Normalizer inicializado")
except Exception as e:
    print(f"   ❌ Erro: {e}")

try:
    print("\n4. Inicializando DigiLang V7...")
    components['digilang'] = DigiLangV7Ultimate()
    print("   ✅ DigiLang V7 inicializado")
except Exception as e:
    print(f"   ❌ Erro: {e}")

try:
    print("\n5. Inicializando Ollama Próspero...")
    components['ollama'] = OllamaPróspero()
    print("   ✅ Ollama Próspero inicializado")
except Exception as e:
    print(f"   ❌ Erro: {e}")

try:
    print("\n6. Inicializando Memory Manager...")
    components['memory'] = UnifiedMemoryManager()
    print("   ✅ Memory Manager inicializado")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# Teste funcional básico
print("\n" + "=" * 60)
print("TESTES FUNCIONAIS")
print("=" * 60)

# Teste de sentimento
try:
    print("\n7. Testando análise de sentimento...")
    result = analyze_text_sentiment("I love this amazing screenplay!")
    print(f"   ✅ Sentimento: {result.compound:.2f} (Positivo)")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# Teste de compressão
if 'digilang' in components:
    try:
        print("\n8. Testando compressão DigiLang V7...")
        text = "FADE IN:\n\nINT. OFFICE - DAY\n\nJohn enters."
        encoded, stats = components['digilang'].encode(text)
        print(f"   ✅ Compressão: {stats.compression_ratio:.2f}%")
        print(f"   Original: {stats.original_tokens} tokens")
        print(f"   Comprimido: {stats.compressed_tokens} tokens")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

# Teste de normalização
if 'normalizer' in components:
    try:
        print("\n9. Testando normalização...")
        text_pt = "João entra na sala rapidamente."
        normalized = components['normalizer'].normalize(text_pt, source_lang='pt')
        print(f"   ✅ Texto normalizado: {normalized[:50]}...")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

# Resumo
print("\n" + "=" * 60)
print("RESUMO")
print("=" * 60)
print(f"Componentes inicializados: {len(components)}/6")
print(f"Status: {'✅ PRONTO PARA API' if len(components) == 6 else '⚠️ PARCIALMENTE PRONTO'}")