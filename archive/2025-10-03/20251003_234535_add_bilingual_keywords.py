#!/usr/bin/env python3
"""
Adiciona keywords bilíngues (EN + PT) em todos os especialistas
Resolve o problema de roteiros em português não detectarem keywords em inglês
"""

BILINGUAL_KEYWORDS = {
    # STRUCTURE KEYWORDS (já implementado em dr_structure.py)
    "inciting_incident": {
        "en": ["suddenly", "but then", "everything changes", "until"],
        "pt": ["de repente", "mas então", "mas aí", "tudo muda", "até que", "subitamente", "inesperadamente"]
    },
    "midpoint": {
        "en": ["revelation", "discovers", "realizes", "truth"],
        "pt": ["revelação", "descobre", "percebe", "verdade", "compreende", "entende", "descubro", "percebo"]
    },
    "all_is_lost": {
        "en": ["dead", "lost", "over", "failed", "defeated"],
        "pt": ["morto", "morreu", "perdido", "acabou", "falhou", "derrotado", "perdeu", "acabado", "fim"]
    },
    "climax": {
        "en": ["final", "confrontation", "showdown", "battle"],
        "pt": ["final", "confronto", "batalha", "luta final", "duelo", "enfrentamento", "combate"]
    },

    # DIALOGUE KEYWORDS (para dr_dialogue.py)
    "exposition": {
        "en": ["as you know", "remember when", "let me explain", "i remember when"],
        "pt": ["como você sabe", "lembra quando", "deixa eu explicar", "eu lembro quando", "como sabe"]
    },
    "on_the_nose": {
        "en": ["i feel", "i'm angry", "i'm sad", "i love you"],
        "pt": ["eu sinto", "estou bravo", "estou triste", "eu te amo", "sinto raiva", "estou com raiva"]
    },

    # PACING KEYWORDS (para dr_pacing.py)
    "action_verbs": {
        "en": ["runs", "jumps", "fights", "escapes", "chases"],
        "pt": ["corre", "pula", "luta", "escapa", "persegue", "foge", "ataca"]
    },
    "slow_pace": {
        "en": ["slowly", "carefully", "quietly", "gently", "pauses"],
        "pt": ["devagar", "lentamente", "cuidadosamente", "silenciosamente", "gentilmente", "pausa"]
    },

    # OPENING KEYWORDS (para dr_opening.py)
    "hook": {
        "en": ["grabs attention", "shocking", "mysterious", "intriguing"],
        "pt": ["chama atenção", "chocante", "misterioso", "intrigante", "surpreendente"]
    },

    # SUBTEXT KEYWORDS (para dr_subtext.py)
    "implied": {
        "en": ["implies", "suggests", "hints", "underlying"],
        "pt": ["implica", "sugere", "insinua", "subjacente", "nas entrelinhas"]
    },

    # TONE KEYWORDS (para dr_tone.py)
    "tone_shift": {
        "en": ["suddenly shifts", "changes tone", "becomes"],
        "pt": ["muda repentinamente", "muda o tom", "torna-se", "vira", "passa a ser"]
    },

    # FORMATTING KEYWORDS (para dr_formatting.py)
    "camera_direction": {
        "en": ["close up", "wide shot", "pan to", "zoom", "cut to"],
        "pt": ["close", "plano aberto", "pan para", "zoom", "corta para", "plano fechado"]
    }
}

def generate_bilingual_config():
    """Gera configuração bilíngue para documentação"""

    print("="*80)
    print("🌍 KEYWORDS BILÍNGUES (EN + PT)")
    print("="*80)
    print()

    for category, keywords in BILINGUAL_KEYWORDS.items():
        print(f"📌 {category.upper().replace('_', ' ')}:")
        print(f"   EN: {', '.join(keywords['en'])}")
        print(f"   PT: {', '.join(keywords['pt'])}")
        print()

    print("="*80)
    print("✅ IMPLEMENTAÇÃO")
    print("="*80)
    print()
    print("Para cada especialista, substitua:")
    print()
    print("ANTES (apenas inglês):")
    print('  if any(word in line for word in ["suddenly", "but then"]):\n')
    print()
    print("DEPOIS (bilíngue):")
    print('  markers = [')
    print('      # English')
    print('      "suddenly", "but then",')
    print('      # Portuguese')
    print('      "de repente", "mas então"')
    print('  ]')
    print('  if any(word in line for word in markers):\n')
    print()

    print("="*80)
    print("📊 STATUS DE IMPLEMENTAÇÃO")
    print("="*80)
    print()
    print("✅ DrStructure - IMPLEMENTADO")
    print("   • Inciting incident: EN + PT")
    print("   • Midpoint: EN + PT")
    print("   • All is lost: EN + PT")
    print("   • Climax: EN + PT")
    print()
    print("⏳ DrDialogue - PENDENTE")
    print("   • Exposition markers: precisa EN + PT")
    print("   • On-the-nose dialogue: precisa EN + PT")
    print()
    print("⏳ DrPacing - PENDENTE")
    print("   • Action verbs: precisa EN + PT")
    print("   • Slow pace markers: precisa EN + PT")
    print()
    print("⏳ DrOpening - PENDENTE")
    print("   • Hook markers: precisa EN + PT")
    print()
    print("⏳ DrSubtext - PENDENTE")
    print("   • Implied meaning markers: precisa EN + PT")
    print()
    print("⏳ DrTone - PENDENTE")
    print("   • Tone shift markers: precisa EN + PT")
    print()
    print("⏳ DrFormatting - PENDENTE")
    print("   • Camera direction markers: precisa EN + PT")
    print()

    print("="*80)
    print("💡 PRÓXIMOS PASSOS")
    print("="*80)
    print()
    print("1. Aplicar keywords bilíngues em DrDialogue")
    print("2. Aplicar keywords bilíngues em DrPacing")
    print("3. Aplicar keywords bilíngues em DrOpening")
    print("4. Aplicar keywords bilíngues em DrSubtext")
    print("5. Aplicar keywords bilíngues em DrTone")
    print("6. Aplicar keywords bilíngues em DrFormatting")
    print("7. Testar com roteiro PT (Sonhos Sem Lembranças)")
    print("8. Testar com roteiro EN (exemplo)")
    print()

    print("="*80)
    print("📈 IMPACTO ESPERADO")
    print("="*80)
    print()
    print("ANTES (keywords EN apenas):")
    print("  • Roteiro PT: Falsos negativos (não detecta)")
    print("  • Roteiro EN: Funciona normalmente")
    print()
    print("DEPOIS (keywords EN + PT):")
    print("  • Roteiro PT: ✅ Detecta corretamente")
    print("  • Roteiro EN: ✅ Continua funcionando")
    print("  • Roteiro ES: ⚠️ Adicionar espanhol futuramente")
    print()

if __name__ == "__main__":
    generate_bilingual_config()
