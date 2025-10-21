#!/usr/bin/env python3
"""
Teste NER Validation - Valida implementação da validação anti-alucinação

Testa:
1. Lazy loading do spaCy funciona
2. Extração de entidades do roteiro
3. Validação detecta personagens legítimos
4. Validação detecta personagens inventados
5. Graceful degradation em caso de erro
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

def test_basic_ner_extraction():
    """Teste básico: extração NER funciona"""
    print("\n" + "="*80)
    print("TESTE 1: Extração básica de entidades")
    print("="*80)

    from engine.analyzers.dr_character import DrCharacter
    from engine.orchestration.dual_core_wrapper import DualCoreWrapper

    specialist = DrCharacter()
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        specialist_type='mckee',
        llm_model='scripturemon-optimized',
        deep_context=False,
        use_personalized_prompts=False
    )

    # Texto de teste
    screenplay_text = """
    INT. APARTAMENTO - DIA

    JOÃO entra pela porta. Ele olha ao redor.

    JOÃO
    Onde está a MARIA?

    PEDRO aparece da cozinha.

    PEDRO
    Ela saiu com a ANA.
    """

    print("📄 Texto do roteiro:")
    print(screenplay_text)

    # Extrai entidades
    print("\n🔍 Extraindo entidades...")
    entities = wrapper._extract_entities_safe(screenplay_text)

    print(f"✅ Entidades encontradas: {entities}")

    # Validação
    expected = {'JOÃO', 'MARIA', 'PEDRO', 'ANA'}
    found = entities.intersection(expected)

    if len(found) >= 3:  # Pelo menos 3 dos 4
        print(f"✅ TESTE PASSOU: Encontrou {len(found)}/4 personagens esperados")
        return True
    else:
        print(f"❌ TESTE FALHOU: Encontrou apenas {len(found)}/4 personagens")
        return False


def test_validation_legitimate_characters():
    """Teste: validação aceita personagens legítimos"""
    print("\n" + "="*80)
    print("TESTE 2: Validação com personagens legítimos")
    print("="*80)

    from engine.analyzers.dr_character import DrCharacter
    from engine.orchestration.dual_core_wrapper import DualCoreWrapper

    specialist = DrCharacter()
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        specialist_type='mckee',
        llm_model='scripturemon-optimized',
        deep_context=False
    )

    screenplay_text = "JOÃO conversa com MARIA. PEDRO observa."
    llm_insights = "A análise mostra que JOÃO é o protagonista e MARIA é a deuteragonista. PEDRO tem papel secundário."

    print(f"📄 Roteiro: {screenplay_text}")
    print(f"🤖 LLM: {llm_insights}")

    validation = wrapper._validate_character_names(llm_insights, screenplay_text)

    print(f"\n📊 Resultado validação:")
    print(f"   Valid: {validation['valid']}")
    print(f"   Overlap: {validation.get('overlap_ratio', 0):.1%}")
    print(f"   Matched: {validation.get('matched', [])}")
    print(f"   Hallucinated: {validation.get('hallucinated', [])}")

    if validation['valid'] and validation.get('overlap_ratio', 0) >= 0.8:
        print("✅ TESTE PASSOU: Validação aceitou personagens legítimos")
        return True
    else:
        print("❌ TESTE FALHOU: Validação rejeitou personagens legítimos")
        return False


def test_validation_hallucinated_characters():
    """Teste: validação detecta personagens inventados"""
    print("\n" + "="*80)
    print("TESTE 3: Validação detecta alucinações")
    print("="*80)

    from engine.analyzers.dr_character import DrCharacter
    from engine.orchestration.dual_core_wrapper import DualCoreWrapper

    specialist = DrCharacter()
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        specialist_type='mckee',
        llm_model='scripturemon-optimized',
        deep_context=False
    )

    screenplay_text = "JOÃO conversa com MARIA."
    llm_insights = "JOÃO, CARLOS e FERNANDA formam um triângulo amoroso. LUCAS observa tudo."

    print(f"📄 Roteiro: {screenplay_text}")
    print(f"🤖 LLM (com alucinações): {llm_insights}")

    validation = wrapper._validate_character_names(llm_insights, screenplay_text)

    print(f"\n📊 Resultado validação:")
    print(f"   Valid: {validation['valid']}")
    print(f"   Overlap: {validation.get('overlap_ratio', 0):.1%}")
    print(f"   Matched: {validation.get('matched', [])}")
    print(f"   Hallucinated: {validation.get('hallucinated', [])}")

    # Espera-se que detecte CARLOS, FERNANDA e LUCAS como inventados
    hallucinated = set(validation.get('hallucinated', []))
    expected_hallucinations = {'CARLOS', 'FERNANDA', 'LUCAS'}

    detected = hallucinated.intersection(expected_hallucinations)

    if not validation['valid'] and len(detected) >= 2:
        print(f"✅ TESTE PASSOU: Detectou {len(detected)}/3 alucinações")
        return True
    else:
        print(f"❌ TESTE FALHOU: Não detectou alucinações adequadamente")
        return False


def test_graceful_degradation():
    """Teste: sistema não quebra se validação falhar"""
    print("\n" + "="*80)
    print("TESTE 4: Graceful degradation")
    print("="*80)

    from engine.analyzers.dr_character import DrCharacter
    from engine.orchestration.dual_core_wrapper import DualCoreWrapper

    specialist = DrCharacter()

    # Teste com validação DESABILITADA
    import os
    os.environ['ENABLE_NER_VALIDATION'] = 'false'

    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        specialist_type='mckee',
        llm_model='scripturemon-optimized',
        deep_context=False
    )

    print("🔧 Validação desabilitada via env var")

    screenplay_text = "JOÃO conversa."
    llm_insights = "Análise de JOÃO."

    validation = wrapper._validate_character_names(llm_insights, screenplay_text)

    print(f"📊 Resultado: {validation}")

    # Restaurar env var
    os.environ['ENABLE_NER_VALIDATION'] = 'true'

    if validation['valid'] and 'warning' in validation:
        print("✅ TESTE PASSOU: Sistema continua funcionando com validação desabilitada")
        return True
    else:
        print("❌ TESTE FALHOU: Sistema não lidou gracefully com validação desabilitada")
        return False


def main():
    """Executa todos os testes"""
    print("\n🎬 SUITE DE TESTES: NER VALIDATION")
    print("="*80)

    import os
    os.environ['ENABLE_NER_VALIDATION'] = 'true'

    results = []

    try:
        results.append(("Extração básica", test_basic_ner_extraction()))
    except Exception as e:
        print(f"❌ ERRO no teste 1: {e}")
        results.append(("Extração básica", False))

    try:
        results.append(("Personagens legítimos", test_validation_legitimate_characters()))
    except Exception as e:
        print(f"❌ ERRO no teste 2: {e}")
        results.append(("Personagens legítimos", False))

    try:
        results.append(("Detecção alucinações", test_validation_hallucinated_characters()))
    except Exception as e:
        print(f"❌ ERRO no teste 3: {e}")
        results.append(("Detecção alucinações", False))

    try:
        results.append(("Graceful degradation", test_graceful_degradation()))
    except Exception as e:
        print(f"❌ ERRO no teste 4: {e}")
        results.append(("Graceful degradation", False))

    # Resumo
    print("\n" + "="*80)
    print("📊 RESUMO DOS TESTES")
    print("="*80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {name}")

    print(f"\n🎯 Taxa de sucesso: {passed}/{total} ({passed/total*100:.0f}%)")

    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam")
        return 1


if __name__ == '__main__':
    exit(main())
