#!/usr/bin/env python3
"""
TESTE DO FALLBACK MELHORADO
Verifica se o fallback extrai dados úteis de JSONs quebrados
"""

from improved_json_parser import create_minimal_structure, robust_json_parse
import json

def test_fallback():
    """Testa o fallback melhorado"""

    print("🧪 TESTE: Fallback Melhorado")
    print("="*50)

    # Casos de teste com JSONs parciais/quebrados
    test_cases = [
        # Caso 1: JSON quebrado com dados úteis
        ('''{"metadata": {"genre": "Sci-Fi", "pages": "2"}, "evidence_log": [{"page": 1, "evidence": 'Breaking here''',
         "JSON quebrado com aspas erradas"),

        # Caso 2: JSON parcial mas com estrutura
        ('''{"metadata": {"genre": "Drama", "title": "Test Movie"},
            "analise_personagem": [{"name": "John", "arc": "Hero Journey"}],
            "validation": {"score": 85''',
         "JSON incompleto mas com dados"),

        # Caso 3: Resposta real do Ollama truncada
        ('''{"metadata": {"genre": "Ciência-Ficção", "pages": "1", "title": "Aurora"},
            "evidence_log": [{"page": 1, "evidence": 'INT. LABORATÓRIO', "type": "setting"}],
            "analise_estrutural": {"inciting_incident": {"page": "1", "description": "AI questions"''',
         "Resposta Ollama truncada"),

        # Caso 4: Texto com fragmentos JSON
        ('''The analysis shows {"genre": "Action"} with a {"score": 90} and includes
            {"name": "Hero", "arc": "Saves the world"} as main character''',
         "Texto misto com fragmentos JSON"),

        # Caso 5: JSON completamente quebrado
        ('''Just broken data with genre": "Thriller" and "pages": "120" somewhere''',
         "Dados espalhados no texto"),
    ]

    passed = 0

    for i, (test_input, description) in enumerate(test_cases, 1):
        print(f"\n📝 Caso {i}: {description}")
        print(f"   Input: {test_input[:60]}...")

        # Primeiro tentar parse normal
        result, confidence = robust_json_parse(test_input)

        print(f"   Parse normal: {'OK' if result else 'Falhou'} (conf: {confidence:.2f})")

        # Se falhou ou confidence baixa, testar fallback
        if not result or confidence < 0.7:
            fallback = create_minimal_structure(test_input)

            print(f"   Fallback confidence: {fallback['confidence']:.2f}")

            # Verificar o que foi extraído
            extracted = []
            if fallback['metadata']:
                extracted.append(f"metadata: {list(fallback['metadata'].keys())}")
            if fallback['evidence_log']:
                extracted.append(f"evidence: {len(fallback['evidence_log'])} items")
            if fallback['analise_personagem']:
                extracted.append(f"personagens: {len(fallback['analise_personagem'])}")
            if fallback['validation'].get('score', 0) > 0:
                extracted.append(f"score: {fallback['validation']['score']}")

            if extracted:
                print(f"   ✅ Extraído: {', '.join(extracted)}")
                passed += 1
            else:
                print(f"   ❌ Nada extraído")
        else:
            # Parse normal funcionou
            print(f"   ✅ Parse normal suficiente")
            passed += 1

    # Teste especial: fallback com JSON real do Ollama (do teste anterior)
    print("\n📝 Caso Especial: JSON real do Ollama com erro")
    ollama_broken = '''
    {
      "metadata": {
        "genre": "Ciência-Ficção",
        "pages": "1",
        "title": "Aurora"
      },
      "evidence_log": [
        {"page": 1, "evidence": 'INT. LABORATÓRIO DE IA - CONTÍNUO', "type": "setting"},
        {
          "page": 1,
          "evidence": '"DR. SARAH CHEN (35), cientista brilhante mas atormentada"',
          "type": "character_description"
        },
        {"page": 1, "evidence": 'AURORA - SISTEMA ATIVO', "type": "technology"}
    '''  # Cortado propositalmente

    fallback = create_minimal_structure(ollama_broken)
    print(f"   Confidence: {fallback['confidence']:.2f}")

    if fallback['metadata']:
        print(f"   ✅ Metadata extraída: {fallback['metadata']}")
    if len(fallback['evidence_log']) > 0:
        print(f"   ✅ Evidence log: {len(fallback['evidence_log'])} items")
        for ev in fallback['evidence_log'][:2]:
            print(f"      • Page {ev['page']}: {ev['evidence'][:50]}...")

    # Resultado final
    print("\n" + "="*50)
    total_tests = len(test_cases) + 1
    print(f"📊 RESULTADO: {passed}/{len(test_cases)} casos regulares passaram")

    if fallback['metadata'] and fallback['evidence_log']:
        passed += 1
        print(f"   Caso especial: ✅ PASSOU")
    else:
        print(f"   Caso especial: ❌ FALHOU")

    taxa_sucesso = (passed / total_tests) * 100
    print(f"\nTaxa de sucesso total: {taxa_sucesso:.0f}%")

    if taxa_sucesso >= 70:
        print("✅ FALLBACK MELHORADO APROVADO!")
        return True
    else:
        print("❌ FALLBACK PRECISA MAIS MELHORIAS")
        return False

if __name__ == "__main__":
    success = test_fallback()
    print("\n🥷 DIGIMUNDO PRESENTE")
    exit(0 if success else 1)