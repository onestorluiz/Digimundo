#!/usr/bin/env python3
"""
Testa se keywords bilíngues resolvem o problema de falsos negativos
"""

from triple_core.core_1_specialists.structure.dr_structure import DrStructure

def test_bilingual_keywords():
    """Testa detecção com roteiro português"""

    print("="*80)
    print("🧪 TESTE: Keywords Bilíngues (EN + PT)")
    print("="*80)
    print()

    # Carrega roteiro português
    with open("content/screenplays/personal/sonhos_sem_lembrancas_t3.txt", 'r', encoding='utf-8') as f:
        screenplay_pt = f.read()

    print("📄 Roteiro: Sonhos Sem Lembranças (PT)")
    print(f"   Tamanho: {len(screenplay_pt)} chars")
    print()

    # Testa DrStructure
    print("1️⃣  DrStructure - Detecção de Estrutura")
    print("-" * 80)

    dr = DrStructure()
    result = dr.analyze(screenplay_pt)

    print(f"   Score: {result['score']}/100")
    print()

    print("   Elementos encontrados:")
    for element, data in result['structural_elements'].items():
        if data['found_at'] is not None:
            print(f"   ✅ {element}: página {data['found_at']} (força: {data['strength']})")
        else:
            print(f"   ❌ {element}: NÃO ENCONTRADO")

    print()
    print("   Violações de regra:")
    for violation in result['rule_violations']:
        severity = violation['severity']
        emoji = "🚨" if severity == "CRITICAL" else "⚠️"
        print(f"   {emoji} {violation['issue']}")

    print()
    print("-" * 80)

    # Análise
    print()
    print("📊 ANÁLISE:")
    print("-" * 80)

    if result['score'] == 0:
        print("   ❌ AINDA TEM PROBLEMA")
        print("   • Score 0/100 indica que não encontrou elementos")
        print("   • Possível causa: keywords ainda não estão pegando")
        print()
        print("   Checando palavras-chave no roteiro:")

        # Buscar manualmente
        lines = screenplay_pt.lower().split('\n')

        # Buscar PT keywords
        pt_found = []
        for i, line in enumerate(lines[:300]):
            if any(k in line for k in ["de repente", "mas então", "mas aí", "arromba", "afogando"]):
                pt_found.append((i // 55, line.strip()[:80]))

        if pt_found:
            print("   ✅ Encontradas palavras PT nas primeiras páginas:")
            for page, line in pt_found[:3]:
                print(f"      Pág {page}: {line}...")

    elif result['score'] > 0 and result['score'] < 50:
        print("   ⚠️  MELHOROU MAS AINDA PRECISA AJUSTAR")
        print(f"   • Score {result['score']}/100 mostra detecção parcial")
        print("   • Alguns elementos encontrados, outros não")
        print()

    else:
        print("   ✅ KEYWORDS BILÍNGUES FUNCIONANDO!")
        print(f"   • Score {result['score']}/100 mostra detecção adequada")
        print("   • Elementos estruturais sendo identificados")
        print()

    print()
    print("="*80)
    print("✅ TESTE CONCLUÍDO")
    print("="*80)

if __name__ == "__main__":
    test_bilingual_keywords()
