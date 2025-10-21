#!/usr/bin/env python3
"""
Teste da estratégia de múltiplos modelos Ollama
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.ollama_strategy import OllamaStrategy

def test_strategy():
    print("🎯 Testando Estratégia de Múltiplos Modelos Ollama")
    print("=" * 60)
    
    strategy = OllamaStrategy()
    
    # Verificar modelos disponíveis
    print("\n📋 Verificando modelos disponíveis:")
    status = strategy.verify_models()
    for role, available in status.items():
        icon = "✅" if available else "❌"
        model = strategy.models[role]["name"]
        print(f"  {icon} {role}: {model}")
    
    # Teste com texto sample
    sample_text = """
    INT. RICK'S CAFE - NIGHT

    The cafe is crowded. SAM plays the piano. RICK sits alone at a 
    table, drinking. ILSA enters with LASZLO. Rick sees her.

    RICK
    Of all the gin joints in all the 
    towns in all the world, she walks 
    into mine.

    Sam stops playing. The room seems to freeze.

    FLASHBACK - PARIS - DAY

    Rick and Ilsa by the Seine, happy, in love.

    ILSA (V.O.)
    We'll always have Paris.
    """
    
    print("\n🧪 Testando com amostra de Casablanca...")
    print("-" * 40)
    
    # Testar cada função
    print("\n1️⃣ Extração de estrutura (llama3.2)...")
    structure = strategy.extract_structure(sample_text)
    print(f"   Cenas detectadas: {structure.get('scenes', 0)}")
    
    print("\n2️⃣ Análise de técnicas (mistral)...")
    techniques = strategy.analyze_techniques(sample_text)
    print(f"   Técnicas: {', '.join(techniques['techniques'][:3])}")
    
    print("\n3️⃣ Avaliação brutal (scripturemon-maestro)...")
    evaluation = strategy.brutal_evaluation(sample_text, {
        "structure": structure,
        "techniques": techniques['techniques']
    })
    print(f"   Nota: {evaluation['nota_geral']}/100")
    print(f"   Feedback: {evaluation['feedback_completo'][:100]}...")
    
    print("\n" + "=" * 60)
    print("✅ Teste completo!")
    return True

if __name__ == "__main__":
    try:
        test_strategy()
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)