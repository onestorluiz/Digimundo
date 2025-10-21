#!/usr/bin/env python3
"""
🧪 Teste da Expansão Universal DigiLang
"""

import json
from pathlib import Path

def test_expansion():
    print("╔" + "═"*58 + "╗")
    print("║   🧪 TESTE DA EXPANSÃO UNIVERSAL DIGILANG            ║")
    print("╚" + "═"*58 + "╝")
    
    base_path = Path("/Users/clubproducoes/Digimundo")
    dict_path = base_path / "digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json"
    expansion_path = base_path / "digilang_expansion"
    
    # Carregar dicionário atualizado
    print("\n📚 Analisando dicionário expandido...")
    with open(dict_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        dictionary = data.get('symbols', {})
        metadata = data.get('metadata', {})
    
    print(f"   📊 Versão: {data.get('version', 'unknown')}")
    print(f"   📊 Total de palavras: {len(dictionary):,}")
    
    # Estatísticas do metadata
    if 'statistics' in metadata:
        stats = metadata['statistics']
        print("\n📈 Estatísticas da expansão:")
        for key, value in stats.items():
            print(f"   • {key}: {value:,}")
    
    # Testar features implementadas
    print("\n🔬 TESTE DE FEATURES:")
    print("="*60)
    
    # 1. Teste de modificadores morfológicos
    print("\n1️⃣ MODIFICADORES MORFOLÓGICOS:")
    morpho_tests = [
        ('book', 'books', '⁺'),
        ('walk', 'walked', '⁻'),
        ('run', 'running', '~'),
        ('livro', 'livros', '⁺')
    ]
    
    morpho_success = 0
    for base, derived, modifier in morpho_tests:
        if base in dictionary and derived in dictionary:
            base_sym = dictionary[base]
            derived_sym = dictionary[derived]
            if modifier in derived_sym:
                print(f"   ✅ {base}/{derived}: {base_sym} → {derived_sym}")
                morpho_success += 1
            else:
                print(f"   ❌ {base}/{derived}: {base_sym} → {derived_sym} (sem modificador)")
        else:
            print(f"   ⚠️ {base} ou {derived} não encontrado")
    
    print(f"   Score: {morpho_success}/{len(morpho_tests)}")
    
    # 2. Teste de cognatos
    print("\n2️⃣ COGNATOS UNIFICADOS:")
    cognate_tests = [
        ('nation', 'nação'),
        ('information', 'informação'),
        ('hospital', 'hospital'),
        ('hotel', 'hotel'),
        ('total', 'total')
    ]
    
    cognate_success = 0
    for en, pt in cognate_tests:
        if en in dictionary and pt in dictionary:
            if dictionary[en] == dictionary[pt]:
                print(f"   ✅ {en}/{pt}: {dictionary[en]}")
                cognate_success += 1
            else:
                print(f"   ❌ {en}/{pt}: {dictionary[en]} ≠ {dictionary[pt]}")
    
    print(f"   Score: {cognate_success}/{len(cognate_tests)}")
    
    # 3. Teste de frequência
    print("\n3️⃣ OTIMIZAÇÃO POR FREQUÊNCIA:")
    high_freq = ['the', 'be', 'to', 'of', 'and', 'o', 'de', 'que', 'e', 'do']
    
    simple_count = 0
    for word in high_freq:
        if word in dictionary:
            symbol = dictionary[word]
            # Verificar se é símbolo simples (ASCII ou símbolo matemático básico)
            if len(symbol) == 1:
                code = ord(symbol)
                if code < 0x1000 or (0x2190 <= code <= 0x2300):
                    simple_count += 1
                    print(f"   ✅ '{word}': {symbol} (simples)")
                else:
                    print(f"   ❌ '{word}': {symbol} (complexo)")
    
    print(f"   Score: {simple_count}/{len(high_freq)}")
    
    # 4. Teste de cobertura expandida
    print("\n4️⃣ COBERTURA EXPANDIDA:")
    
    # Palavras que deveriam estar no dicionário expandido
    test_words = [
        # Inglês comum
        'ability', 'accept', 'account', 'achieve', 'action',
        'activity', 'actually', 'address', 'admit', 'affect',
        
        # Português comum
        'abanar', 'abater', 'abelha', 'aberto', 'abraçar',
        'abraço', 'abrir', 'absoluto', 'absurdo', 'abundância'
    ]
    
    covered = sum(1 for w in test_words if w in dictionary)
    print(f"   Cobertura de teste: {covered}/{len(test_words)} ({covered/len(test_words)*100:.0f}%)")
    
    # Análise de símbolos
    print("\n📊 ANÁLISE DE SÍMBOLOS:")
    print("="*60)
    
    unique_symbols = len(set(dictionary.values()))
    print(f"   • Símbolos únicos: {unique_symbols:,}")
    print(f"   • Taxa de reutilização: {(1 - unique_symbols/len(dictionary))*100:.1f}%")
    
    # Distribuição de tipos de símbolos
    symbol_types = {
        'ASCII': 0,
        'Matemático': 0,
        'Emoji': 0,
        'CJK': 0,
        'Hangul': 0,
        'Outros': 0
    }
    
    for symbol in set(dictionary.values()):
        if len(symbol) == 1:
            code = ord(symbol)
            if code < 128:
                symbol_types['ASCII'] += 1
            elif 0x2190 <= code <= 0x2300:
                symbol_types['Matemático'] += 1
            elif 0x1F300 <= code <= 0x1F9FF:
                symbol_types['Emoji'] += 1
            elif 0x4E00 <= code <= 0x9FFF:
                symbol_types['CJK'] += 1
            elif 0xAC00 <= code <= 0xD7AF:
                symbol_types['Hangul'] += 1
            else:
                symbol_types['Outros'] += 1
    
    print("\n   Distribuição de símbolos:")
    for tipo, count in sorted(symbol_types.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"      • {tipo}: {count:,} ({count/unique_symbols*100:.1f}%)")
    
    # Conclusão
    print("\n" + "="*60)
    print("📋 RESUMO DA VALIDAÇÃO")
    print("="*60)
    
    total_score = (morpho_success + cognate_success + simple_count + covered) 
    total_tests = len(morpho_tests) + len(cognate_tests) + len(high_freq) + len(test_words)
    overall_score = total_score / total_tests * 100
    
    print(f"\n   🎯 Score Geral: {overall_score:.1f}%")
    
    if overall_score >= 80:
        print("   ✅ Expansão bem-sucedida!")
    elif overall_score >= 60:
        print("   ⚠️ Expansão parcial - precisa melhorias")
    else:
        print("   ❌ Expansão insuficiente - revisar implementação")
    
    # Recomendações
    print("\n💡 RECOMENDAÇÕES:")
    if morpho_success < len(morpho_tests):
        print("   • Melhorar sistema morfológico")
    if cognate_success < len(cognate_tests):
        print("   • Expandir detecção de cognatos")
    if simple_count < len(high_freq):
        print("   • Realocar símbolos por frequência")
    if covered < len(test_words):
        print("   • Adicionar mais palavras do corpus")

if __name__ == "__main__":
    test_expansion()