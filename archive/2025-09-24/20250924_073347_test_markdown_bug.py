#!/usr/bin/env python3
"""
TESTE DO BUG DE MARKDOWN NO PARSER
Mostra exatamente onde está o erro
"""

import re
import json
from improved_json_parser import robust_json_parse, extract_json_from_text

def test_markdown_extraction():
    """Testa extração de JSON em markdown"""

    print("🔍 TESTANDO BUG DO MARKDOWN\n")
    print("="*60)

    # Caso de teste: JSON em markdown
    markdown_text = """```json
{
  "score": 85,
  "insight": "Great screenplay"
}
```"""

    print("ENTRADA (JSON em Markdown):")
    print(markdown_text)
    print("\n" + "-"*40 + "\n")

    # Teste 1: Função extract_json_from_text
    print("1. Testando extract_json_from_text():")
    result = extract_json_from_text(markdown_text)
    print(f"   Resultado: {result}")

    # Teste 2: Regex manual para entender o problema
    print("\n2. Testando regex patterns:")

    # Pattern atual no código
    patterns = [
        (r'```json\s*(.*?)\s*```', "Pattern 1: ```json...```"),
        (r'```\s*(.*?)\s*```', "Pattern 2: ```...```"),
        (r'\{[^{}]*\}', "Pattern 3: {...}"),
        (r'\{.*?\}', "Pattern 4: {.*?}"),
        (r'\{[\s\S]*?\}', "Pattern 5: {[\\s\\S]*?}")
    ]

    for pattern, name in patterns:
        try:
            match = re.search(pattern, markdown_text, re.DOTALL)
            if match:
                print(f"   ✅ {name}: ENCONTROU")
                print(f"      Match: {match.group(0)[:50]}...")
                # Tentar extrair só o JSON
                if match.group(1) if len(match.groups()) > 0 else None:
                    json_part = match.group(1)
                else:
                    json_part = match.group(0)
                print(f"      JSON extraído: {json_part[:50]}...")
            else:
                print(f"   ❌ {name}: NÃO encontrou")
        except Exception as e:
            print(f"   ❌ {name}: ERRO - {e}")

    # Teste 3: Parser completo
    print("\n3. Testando robust_json_parse():")
    parsed, confidence = robust_json_parse(markdown_text)
    print(f"   Resultado: {parsed}")
    print(f"   Confiança: {confidence}")

    # Teste 4: Solução correta
    print("\n4. SOLUÇÃO PROPOSTA:")
    print("   Pattern correto: r'```(?:json)?\\s*({.*?})\\s*```'")

    # Testar solução
    correct_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    match = re.search(correct_pattern, markdown_text, re.DOTALL)
    if match:
        json_str = match.group(1)
        print(f"   ✅ JSON extraído: {json_str}")
        try:
            parsed = json.loads(json_str)
            print(f"   ✅ Parse OK: {parsed}")
        except:
            print(f"   ❌ Parse falhou")
    else:
        print("   ❌ Pattern não encontrou")

    print("\n" + "="*60)
    print("\n📊 DIAGNÓSTICO DO BUG:")
    print("""
O problema está em extract_json_from_text():
1. Os patterns atuais NÃO capturam o grupo correto
2. O código procura por patterns mas não extrai o JSON interno
3. Quando encontra markdown, retorna None ao invés do JSON

LINHA DO BUG: improved_json_parser.py, linhas 20-45
Pattern problemático: Não captura o grupo (1) corretamente
""")

if __name__ == "__main__":
    test_markdown_extraction()

    print("\n🥷 DIGIMUNDO PRESENTE")