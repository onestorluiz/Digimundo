#!/usr/bin/env python3
"""
Teste simplificado de análise de roteiro
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Testa o brain diretamente
from apps.scripturemon.scripturemon_brain import ScripturemonBrain

def main():
    print("\n🧠 TESTE DIRETO DO SCRIPTUREMON BRAIN")
    print("="*60)
    
    screenplay = """INT. COFFEE SHOP - DAY

JOHN enters. Looks tired.

JOHN
I need coffee. Black.

BARISTA
Coming right up.

John sits. Waits.

FADE OUT."""
    
    print("📝 Analisando roteiro simples...")
    
    try:
        brain = ScripturemonBrain()
        result = brain.analyze_screenplay(screenplay, "Teste Café")
        
        print("\n✅ Análise completa!")
        print(f"Score: {result['score']}/100")
        print(f"Cenas: {len(result['structure']['scenes'])}")
        print(f"Personagens: {result['structure']['characters']}")
        print(f"Diálogo: {result['structure']['dialogue_ratio']*100:.0f}%")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()