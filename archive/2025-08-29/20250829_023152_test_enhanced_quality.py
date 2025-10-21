#!/usr/bin/env python3
"""
🧪 Teste de Qualidade do DigiLang Aprimorado
"""

import json
from pathlib import Path

def test_enhanced_digilang():
    print("╔" + "═"*58 + "╗")
    print("║     🧪 TESTE DE QUALIDADE DIGILANG v10.0              ║")
    print("╚" + "═"*58 + "╝")
    
    base_path = Path("/Users/clubproducoes/Digimundo")
    dict_path = base_path / "digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json"
    
    # Carregar dicionário
    print("\n📚 Carregando dicionário aprimorado...")
    with open(dict_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        dictionary = data.get('symbols', {})
        metadata = data.get('metadata', {})
    
    print(f"   ✅ {len(dictionary):,} palavras")
    print(f"   📊 Versão: {data.get('version', 'unknown')}")
    
    # Teste 1: Agrupamento Semântico
    print("\n🧠 TESTE 1: AGRUPAMENTO SEMÂNTICO")
    print("="*60)
    
    family_words = ['father', 'mother', 'son', 'daughter', 'pai', 'mae', 'filho', 'filha']
    family_symbols = [dictionary.get(w, '?') for w in family_words]
    
    print("   Família:")
    for word, symbol in zip(family_words, family_symbols):
        if word in dictionary:
            print(f"      {word}: {symbol}")
    
    # Verificar se são emoji relacionados
    emoji_count = sum(1 for s in family_symbols if len(s) == 1 and 0x1F300 <= ord(s) <= 0x1F9FF)
    print(f"   ✅ {emoji_count}/{len(family_words)} usando emoji relacionados")
    
    # Teste 2: Mnemônicos Visuais
    print("\n🎨 TESTE 2: MNEMÔNICOS VISUAIS")
    print("="*60)
    
    mnemonic_tests = {
        'sun': '☀️', 'moon': '🌙', 'star': '⭐',
        'water': '💧', 'fire': '🔥', 'tree': '🌳',
        'heart': '❤️', 'house': '🏠', 'car': '🚗'
    }
    
    correct = 0
    for word, expected in mnemonic_tests.items():
        actual = dictionary.get(word, '?')
        if actual == expected or (len(actual) == 1 and 0x1F300 <= ord(actual) <= 0x1F9FF):
            correct += 1
            print(f"   ✅ {word}: {actual}")
        else:
            print(f"   ❌ {word}: {actual} (esperado emoji)")
    
    print(f"   Score: {correct}/{len(mnemonic_tests)} ({correct/len(mnemonic_tests)*100:.0f}%)")
    
    # Teste 3: Frequência
    print("\n⚡ TESTE 3: OTIMIZAÇÃO POR FREQUÊNCIA")
    print("="*60)
    
    high_freq = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'o', 'de', 'que']
    simple_count = 0
    
    for word in high_freq:
        if word in dictionary:
            symbol = dictionary[word]
            if len(symbol) == 1:
                code = ord(symbol)
                # Símbolos simples: < U+1000
                if code < 0x1000:
                    simple_count += 1
                    print(f"   ✅ '{word}': {symbol} (simples)")
                else:
                    print(f"   ❌ '{word}': {symbol} (complexo)")
    
    print(f"   Score: {simple_count}/{len(high_freq)} palavras frequentes otimizadas")
    
    # Teste 4: Morfologia
    print("\n📐 TESTE 4: PADRÕES MORFOLÓGICOS")
    print("="*60)
    
    morphology_tests = [
        ('book', 'books'),
        ('walk', 'walked'),
        ('livro', 'livros')
    ]
    
    patterns_found = 0
    for base, derived in morphology_tests:
        if base in dictionary and derived in dictionary:
            base_sym = dictionary[base]
            derived_sym = dictionary[derived]
            
            # Verificar se há modificador
            if '⁺' in derived_sym or '⁻' in derived_sym or len(derived_sym) > len(base_sym):
                patterns_found += 1
                print(f"   ✅ {base}/{derived}: {base_sym} → {derived_sym}")
            else:
                print(f"   ❌ {base}/{derived}: {base_sym} → {derived_sym} (sem padrão)")
    
    print(f"   Score: {patterns_found}/{len(morphology_tests)} padrões preservados")
    
    # Teste 5: Coerência PT/EN
    print("\n🌐 TESTE 5: COERÊNCIA BILÍNGUE")
    print("="*60)
    
    coherence_tests = [
        ('love', 'amor'), ('water', 'agua'), ('sun', 'sol'),
        ('moon', 'lua'), ('fire', 'fogo'), ('tree', 'arvore'),
        ('house', 'casa'), ('car', 'carro'), ('book', 'livro')
    ]
    
    coherent = 0
    for en, pt in coherence_tests:
        if en in dictionary and pt in dictionary:
            if dictionary[en] == dictionary[pt]:
                coherent += 1
                print(f"   ✅ {en}/{pt}: {dictionary[en]}")
            else:
                print(f"   ❌ {en}/{pt}: {dictionary[en]} ≠ {dictionary[pt]}")
    
    print(f"   Score: {coherent}/{len(coherence_tests)} ({coherent/len(coherence_tests)*100:.0f}%)")
    
    # Estatísticas Finais
    print("\n" + "="*60)
    print("📊 RESUMO DA QUALIDADE")
    print("="*60)
    
    # Calcular score geral
    scores = {
        'Agrupamento Semântico': emoji_count/len(family_words) * 100,
        'Mnemônicos Visuais': correct/len(mnemonic_tests) * 100,
        'Otimização Frequência': simple_count/len(high_freq) * 100,
        'Padrões Morfológicos': patterns_found/len(morphology_tests) * 100,
        'Coerência Bilíngue': coherent/len(coherence_tests) * 100
    }
    
    for category, score in scores.items():
        status = "✅" if score >= 70 else "⚠️" if score >= 40 else "❌"
        print(f"   {status} {category}: {score:.0f}%")
    
    overall_quality = sum(scores.values()) / len(scores)
    
    print(f"\n   🎯 QUALIDADE GERAL: {overall_quality:.0f}%")
    
    if overall_quality >= 80:
        print("   ✨ EXCELENTE! DigiLang está altamente otimizada!")
    elif overall_quality >= 60:
        print("   ✅ BOM! DigiLang tem boa qualidade geral.")
    else:
        print("   ⚠️ DigiLang precisa de mais ajustes.")
    
    return scores, overall_quality

if __name__ == "__main__":
    test_enhanced_digilang()