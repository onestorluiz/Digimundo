#!/usr/bin/env python3
"""
TESTE COMPLETO DO PARSER - CASOS REAIS
Mostra exatamente o que funciona e o que falha
"""

from improved_json_parser import robust_json_parse

def test_all_cases():
    """Testa todos os 6 casos com detalhes"""

    test_cases = [
        ('{"name": "test", "value": 123}', "JSON válido"),
        ("{'name': 'test', 'value': 456}", "JSON com aspas simples"),
        ('```json\n{"result": true, "data": "test"}\n```', "JSON em Markdown"),
        ("The score is 85 and the insight shows improvement", "Texto com dados"),
        ('{invalid,,, json: broken}', "JSON muito quebrado"),
        ("This is just plain text without structure", "Texto puro sem estrutura")
    ]

    print("📊 TESTE COMPLETO DO PARSER - 6 CASOS\n")
    print("="*60)

    success_count = 0

    for i, (test_input, description) in enumerate(test_cases, 1):
        print(f"\n📝 CASO {i}: {description}")
        print(f"   Input: {test_input[:50]}...")

        parsed, confidence = robust_json_parse(test_input)

        # Critério de sucesso: confiança > 0.3
        success = confidence > 0.3 and parsed is not None

        if success:
            success_count += 1
            print(f"   ✅ SUCESSO (confiança: {confidence:.2f})")
        else:
            print(f"   ❌ FALHA (confiança: {confidence:.2f})")

        if parsed:
            print(f"   Resultado: {str(parsed)[:100]}...")
        else:
            print(f"   Resultado: None")

        print(f"   Detalhes: ", end="")
        if confidence >= 0.9:
            print("JSON extraído sem correções")
        elif confidence >= 0.7:
            print("JSON corrigido com sucesso")
        elif confidence >= 0.3:
            print("Estrutura mínima criada")
        else:
            print("Falha total no parse")

    print("\n" + "="*60)
    print(f"\n📈 RESULTADO FINAL: {success_count}/6 ({success_count/6*100:.1f}%)")

    print("\n🔍 ANÁLISE:")
    if success_count == 6:
        print("   100% - Todos os casos passaram!")
    elif success_count == 5:
        print("   83.3% - Excelente! Apenas 1 caso falhou")
    elif success_count == 4:
        print("   66.7% - Bom, mas 2 casos falharam")
    else:
        print(f"   {success_count/6*100:.1f}% - Precisa melhorar")

if __name__ == "__main__":
    test_all_cases()
    print("\n🥷 DIGIMUNDO PRESENTE")