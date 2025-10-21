#!/usr/bin/env python3
"""
TESTE DE CORREÇÃO DE ASPAS MISTAS
Verifica se o parser corrige JSONs com aspas incorretas
"""

from improved_json_parser import robust_json_parse, fix_malformed_json
import json

def test_aspas_mistas():
    """Testa diferentes casos de aspas mistas"""

    print("🧪 TESTE: Correção de Aspas Mistas")
    print("="*50)

    test_cases = [
        # Caso 1: Valor com aspas simples
        ('{"key": \'value\'}', "Valor com aspas simples"),

        # Caso 2: Múltiplos valores com aspas mistas
        ('{"name": "John", "city": \'Paris\', "age": 25}', "Múltiplos valores mistos"),

        # Caso 3: Nested com aspas mistas (como o Ollama retorna)
        ('{"evidence_log": [{"page": 1, "evidence": \'INT. LABORATÓRIO\'}]}', "Nested com aspas mistas"),

        # Caso 4: String com aspas internas
        ('{"dialog": "She said \'hello\'"}', "Aspas internas"),

        # Caso 5: JSON real do Ollama (truncado)
        ('''{"metadata": {"genre": "Sci-Fi"}, "evidence_log": [{"evidence": 'INT. LAB', "page": 1}]}''', "JSON estilo Ollama"),
    ]

    passed = 0
    failed = 0

    for i, (test_json, description) in enumerate(test_cases, 1):
        print(f"\n📝 Caso {i}: {description}")
        print(f"   Input: {test_json[:60]}...")

        # Teste 1: Parser robusto
        result, confidence = robust_json_parse(test_json)

        if result and confidence >= 0.7:
            print(f"   ✅ PASSOU (confiança: {confidence:.2f})")

            # Verificar se tem os campos esperados
            if 'evidence_log' in test_json:
                if 'evidence_log' in result:
                    print(f"      Campos preservados: {list(result.keys())}")
                else:
                    print(f"      ⚠️ Campo evidence_log perdido!")

            passed += 1
        else:
            print(f"   ❌ FALHOU (confiança: {confidence:.2f})")

            # Tentar com fix_malformed_json diretamente
            fixed = fix_malformed_json(test_json)
            if fixed:
                print(f"      Fix direto funcionou: {list(fixed.keys())}")
            else:
                print(f"      Fix direto também falhou")

            failed += 1

    # Resultado final
    print("\n" + "="*50)
    print(f"📊 RESULTADO: {passed}/{len(test_cases)} passaram")

    taxa_sucesso = (passed / len(test_cases)) * 100
    print(f"Taxa de sucesso: {taxa_sucesso:.0f}%")

    if taxa_sucesso >= 80:
        print("✅ CORREÇÃO DE ASPAS APROVADA!")
        return True
    else:
        print("❌ CORREÇÃO PRECISA MELHORIAS")
        return False

if __name__ == "__main__":
    success = test_aspas_mistas()
    print("\n🥷 DIGIMUNDO PRESENTE")
    exit(0 if success else 1)