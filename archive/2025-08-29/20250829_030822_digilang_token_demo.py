#!/usr/bin/env python3
"""
💰 Demonstração da Economia de Tokens com DigiLang
Mostra economia real em tokens para LLMs
"""

import json

def count_tokens(text, model="gpt-3.5-turbo"):
    """Conta tokens usando estimativa baseada em caracteres Unicode"""
    # Estimativa aproximada baseada em custo real de tokens
    tokens = 0
    for char in text:
        code = ord(char)
        if code < 128:  # ASCII
            tokens += 1
        elif code < 256:  # Latin Extended
            tokens += 1
        elif 0x4E00 <= code <= 0x9FFF:  # CJK
            tokens += 1.5
        elif 0x1F300 <= code <= 0x1F9FF:  # Emoji
            tokens += 3
        else:
            tokens += 2
    return int(tokens)

def main():
    print("╔" + "═"*58 + "╗")
    print("║  💰 ECONOMIA DE TOKENS COM DIGILANG                   ║")
    print("╚" + "═"*58 + "╝")
    
    # Carregar DigiLang
    with open('/Users/clubproducoes/Digimundo/digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json', 'r') as f:
        digilang = json.load(f)
        symbols = digilang['symbols']
    
    # Textos de teste (roteiros)
    test_scripts = [
        """FADE IN:

INT. COFFEE SHOP - DAY

The protagonist enters the crowded coffee shop. She looks around nervously, searching for someone.

PROTAGONIST
(to herself)
Where is he? He said he would be here.

She spots a man sitting alone in the corner. Their eyes meet.

CUT TO:""",
        
        """EXT. CITY STREET - NIGHT

Rain pours down on the empty street. A lone figure walks slowly through the puddles.

NARRATOR (V.O.)
Sometimes the hardest battles are the ones we fight with ourselves.

The figure stops under a streetlight, looking up at the rain.

FADE OUT."""
    ]
    
    print("\n📝 ANÁLISE DE ECONOMIA EM ROTEIROS")
    print("="*60)
    
    total_original = 0
    total_compressed = 0
    
    for i, script in enumerate(test_scripts, 1):
        print(f"\n📄 Roteiro {i}:")
        print(f"   Preview: {script[:50]}...")
        
        # Tokens originais
        original_tokens = count_tokens(script)
        
        # Comprimir com DigiLang
        compressed_parts = []
        for word in script.split():
            # Limpar palavra
            clean = ''.join(c for c in word.lower() if c.isalnum())
            
            if clean in symbols:
                compressed_parts.append(symbols[clean])
            else:
                compressed_parts.append(word)
        
        compressed = ' '.join(compressed_parts)
        compressed_tokens = count_tokens(compressed)
        
        # Economia
        saving = (1 - compressed_tokens/original_tokens) * 100
        
        print(f"   • Original: {original_tokens} tokens")
        print(f"   • Comprimido: {compressed_tokens} tokens")
        print(f"   • 💰 Economia: {saving:.1f}%")
        
        total_original += original_tokens
        total_compressed += compressed_tokens
    
    # Totais
    print("\n" + "="*60)
    print("📊 ECONOMIA TOTAL")
    print("="*60)
    print(f"   • Tokens originais: {total_original}")
    print(f"   • Tokens comprimidos: {total_compressed}")
    print(f"   • 💰 ECONOMIA TOTAL: {(1 - total_compressed/total_original) * 100:.1f}%")
    
    # Custo estimado (GPT-3.5)
    cost_per_1k = 0.0015  # $0.0015 por 1k tokens
    original_cost = (total_original / 1000) * cost_per_1k
    compressed_cost = (total_compressed / 1000) * cost_per_1k
    saved_cost = original_cost - compressed_cost
    
    print("\n💵 ECONOMIA FINANCEIRA (GPT-3.5 Turbo):")
    print(f"   • Custo original: ${original_cost:.4f}")
    print(f"   • Custo comprimido: ${compressed_cost:.4f}")
    print(f"   • 💰 Economia: ${saved_cost:.4f} ({(saved_cost/original_cost)*100:.0f}%)")
    
    print("\n✨ Com DigiLang, você economiza tokens E dinheiro!")
    
    # Mostrar palavras mais frequentes otimizadas
    print("\n🎯 TOP PALAVRAS OTIMIZADAS (1 token cada):")
    ascii_words = [(w, s) for w, s in symbols.items() if s and ord(s[0]) < 128]
    for word, symbol in sorted(ascii_words[:10], key=lambda x: x[0]):
        print(f"   • {word}: {symbol}")

if __name__ == "__main__":
    main()