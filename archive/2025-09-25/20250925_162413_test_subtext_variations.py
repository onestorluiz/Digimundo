#!/usr/bin/env python3
"""
TESTE DE 5 VARIAÇÕES PARA SUBTEXT
Objetivo: Encontrar a melhor abordagem para análise de subtexto
"""

import json
import requests
import time
import re
from datetime import datetime
from typing import Dict, List, Tuple

# Script de exemplo para testar
EXAMPLE_SCRIPT = """EXT. CHURCH - NIGHT

FATHER MARCUS (60s) kneels before the altar, rosary in hand.

MARCUS
Forgive me, Father, for I have sinned.

The church door CREAKS. DETECTIVE SARAH COLE (40s) enters.

SARAH
Beautiful church. Must be peaceful,
praying here every night.

MARCUS
(not turning)
Peace is earned, Detective. Not given.

SARAH
Three murders. All confessed their sins
before dying. Coincidence?

MARCUS
The Lord works in mysterious ways.

SARAH
So do killers.

Marcus's fingers tighten on the rosary.

MARCUS
I'll pray for you, Detective.

SARAH
Save your prayers. You'll need them.

She leaves. Marcus remains kneeling, but his prayers have stopped."""

# 5 Variações diferentes
VARIATIONS = {
    "V1_McKee_Layers": {
        "name": "SUBTEXT McKEE LAYERS",
        "system_prompt": """You are an expert in Robert McKee's subtext analysis from 'Story' (2010 edition).

MCKEE'S SUBTEXT LAYERS - CITE SPECIFIC TECHNIQUES:

**THE TEXT BENEATH TEXT (Story, Chapter 11, p.252-265):**

McKee defines: "Subtext is the life under the surface" (p.252). Apply:

- **SAID VS UNSAID**: What characters say vs what they mean (p.253)
- **TRUE ACTION**: "What characters DO reveals truth" (p.254)
- **BEHAVIORAL CONTRADICTIONS**: Actions betraying words (p.255)
- **INDIRECT DIALOGUE**: Characters talking around issues (p.256)
- **EMOTIONAL SUBTEXT**: Feelings beneath surface (p.257)
- **POWER DYNAMICS**: Who controls conversation (p.258)
- **HIDDEN AGENDAS**: Unspoken motivations (p.259)

Quote McKee: "Nothing is what it seems" (p.252)
"If the scene is about what it's about, you're in trouble" (p.253)

SPEND MAXIMUM TOKENS ON SUBTEXT LAYERS!
CITE EVERY PAGE NUMBER AND TECHNIQUE!""",
        "technique_keywords": {
            'text beneath': 3,
            'said vs unsaid': 3,
            'true action': 3,
            'behavioral contradiction': 3,
            'indirect dialogue': 3,
            'emotional subtext': 3,
            'power dynamic': 3,
            'hidden agenda': 3,
            'nothing is what it seems': 2
        }
    },

    "V2_Truby_Moral": {
        "name": "SUBTEXT TRUBY MORAL",
        "system_prompt": """You are an expert in John Truby's moral subtext from 'Anatomy of Story' (2007).

TRUBY'S MORAL SUBTEXT - HIDDEN VALUES:

**MORAL ARGUMENT BENEATH DIALOGUE (Anatomy, p.144-150):**

Truby states: "Great dialogue is moral argument in disguise" (p.144). Apply:

- **MORAL DIALOGUE**: Values clash through conversation (p.144)
- **VALUES IN CONFLICT**: Opposing belief systems (p.145)
- **JUSTIFICATION SUBTEXT**: How characters rationalize (p.146)
- **MORAL BLINDNESS**: What characters can't see (p.147)
- **THEME THROUGH SUBTEXT**: Story meaning beneath (p.148)
- **CHARACTER VALUES**: Hidden belief systems (p.149)

Quote Truby: "Dialogue is values fighting" (p.145)

NAME EVERY MORAL SUBTEXT TECHNIQUE!""",
        "technique_keywords": {
            'moral dialogue': 3,
            'moral argument': 3,
            'values conflict': 3,
            'justification': 3,
            'moral blindness': 3,
            'theme through subtext': 3,
            'belief system': 3,
            'values fighting': 2
        }
    },

    "V3_Vogler_Psychological": {
        "name": "SUBTEXT VOGLER PSYCHOLOGICAL",
        "system_prompt": """You are an expert in Christopher Vogler's psychological subtext from 'Writer's Journey' (2007).

VOGLER'S PSYCHOLOGICAL SUBTEXT - UNCONSCIOUS PATTERNS:

**ARCHETYPAL SUBTEXT (Writer's Journey, p.80-95):**

Vogler reveals: "Characters speak from archetypal depths" (p.80). Apply:

- **SHADOW PROJECTION**: Dark side expressed indirectly (p.81)
- **MASK VS TRUTH**: Persona hiding real self (p.82)
- **ARCHETYPAL DIALOGUE**: Universal patterns beneath (p.83)
- **PSYCHOLOGICAL DEFENSE**: Subtext as protection (p.84)
- **UNCONSCIOUS COMMUNICATION**: What's really being said (p.85)

Quote Vogler: "The real conversation happens beneath words" (p.86)

ANALYZE EVERY PSYCHOLOGICAL LAYER!""",
        "technique_keywords": {
            'shadow projection': 3,
            'mask vs truth': 3,
            'archetypal': 3,
            'psychological defense': 3,
            'unconscious communication': 3,
            'persona': 2,
            'beneath words': 2
        }
    },

    "V4_Mamet_Practical": {
        "name": "SUBTEXT MAMET PRACTICAL",
        "system_prompt": """You are an expert in David Mamet's practical subtext from 'On Directing Film' and plays.

MAMET'S PRACTICAL SUBTEXT - ACTION BENEATH WORDS:

**DIALOGUE AS ACTION (Various works):**

Mamet principle: "Characters speak to get what they want." Apply:

- **OBJECTIVE BENEATH**: What character wants (Glengarry)
- **TACTICS IN DIALOGUE**: How they manipulate (Oleanna)
- **POWER PLAYS**: Dominance through words (Speed-the-Plow)
- **DEFLECTION**: Avoiding real issues (American Buffalo)
- **REPETITION AS SUBTEXT**: Meaning through rhythm

Quote Mamet: "People only speak to get something"

FIND THE WANT BENEATH EVERY LINE!""",
        "technique_keywords": {
            'objective beneath': 3,
            'tactics': 3,
            'power play': 3,
            'deflection': 3,
            'repetition': 3,
            'manipulation': 2,
            'want': 2
        }
    },

    "V5_Integrated_Master": {
        "name": "SUBTEXT INTEGRATED MASTER",
        "system_prompt": """You are a master of ALL subtext techniques from every major theorist.

INTEGRATED SUBTEXT MASTERY - ALL TECHNIQUES:

**MCKEE'S LAYERS (Story p.252-265):**
- **TEXT BENEATH TEXT**: Surface vs depth (p.252)
- **BEHAVIORAL CONTRADICTIONS**: Actions betray words (p.255)
- **INDIRECT DIALOGUE**: Talking around truth (p.256)
Quote: "Nothing is what it seems" (p.252)

**TRUBY'S MORAL SUBTEXT (Anatomy p.144-150):**
- **MORAL DIALOGUE**: Values in conflict (p.144)
- **JUSTIFICATION SUBTEXT**: How characters rationalize (p.146)
- **MORAL BLINDNESS**: What they can't see (p.147)
Quote: "Dialogue is values fighting" (p.145)

**VOGLER'S PSYCHOLOGICAL (Journey p.80-95):**
- **SHADOW PROJECTION**: Dark side indirect (p.81)
- **MASK VS TRUTH**: Persona hiding self (p.82)
Quote: "Real conversation beneath words" (p.86)

**MAMET'S PRACTICAL (Various):**
- **OBJECTIVE BENEATH**: Hidden wants
- **TACTICS IN DIALOGUE**: Manipulation
Quote: "People speak to get something"

**FIELD'S CONTEXT (Screenplay p.180-185):**
- **CONTEXT IS SUBTEXT**: Situation creates meaning (p.181)
- **VISUAL SUBTEXT**: What we see vs hear (p.182)
Quote: "Context determines meaning" (p.181)

**SNYDER'S EMOTIONAL (Save the Cat p.140-145):**
- **EMOTIONAL TRUTH**: Real feelings hidden (p.141)
- **PRIMAL BENEATH**: Basic needs under surface (p.142)
Quote: "Truth is in the gaps" (p.141)

**ARISTOTLE'S DRAMATIC IRONY (Poetics 1452a):**
- **DRAMATIC IRONY**: Audience knows more (1452a)
- **HIDDEN RECOGNITION**: Delayed understanding

MAXIMUM TOKENS! CITE EVERY TECHNIQUE WITH PAGES!
ANALYZE EVERY LAYER OF SUBTEXT!
SPEND TOKENS ON QUALITY DEPTH!""",
        "technique_keywords": {
            'text beneath text': 3,
            'behavioral contradiction': 3,
            'indirect dialogue': 3,
            'moral dialogue': 3,
            'moral argument': 3,
            'justification': 3,
            'moral blindness': 3,
            'shadow projection': 3,
            'mask vs truth': 3,
            'objective beneath': 3,
            'tactics': 3,
            'context subtext': 3,
            'visual subtext': 3,
            'emotional truth': 3,
            'primal beneath': 3,
            'dramatic irony': 3,
            'hidden recognition': 3,
            'nothing seems': 2,
            'values fighting': 2,
            'beneath words': 2,
            'people speak get': 2
        }
    }
}

def count_theory_citations(text: str) -> Dict[str, int]:
    """Conta citações de teóricos com mais flexibilidade."""
    citations = {
        'mckee': len(re.findall(r'(?i)(mckee|story[,\s]+(?:p\.?|page))', text)),
        'truby': len(re.findall(r'(?i)(truby|anatomy)', text)),
        'field': len(re.findall(r'(?i)(field|screenplay[,\s]+(?:p\.?|page))', text)),
        'snyder': len(re.findall(r'(?i)(snyder|save the cat|cat!)', text)),
        'vogler': len(re.findall(r"(?i)(vogler|writer'?s? journey|journey[,\s]+(?:p\.?|page))", text)),
        'campbell': len(re.findall(r'(?i)(campbell|hero with|thousand faces)', text)),
        'aristotle': len(re.findall(r'(?i)(aristotle|poetics)', text)),
        'mamet': len(re.findall(r'(?i)(mamet|glengarry|oleanna|directing film)', text))
    }
    return citations

def count_technique_bonuses(text: str, keywords: Dict[str, int]) -> int:
    """Conta bônus por técnicas específicas mencionadas."""
    text_lower = text.lower()
    total_bonus = 0

    for keyword, bonus in keywords.items():
        if keyword in text_lower:
            total_bonus += bonus

    return total_bonus

def test_variation(name: str, config: Dict) -> Dict:
    """Testa uma variação específica."""
    print(f"   ⚡ Processando {name}...")

    messages = [
        {
            "role": "system",
            "content": config["system_prompt"]
        },
        {
            "role": "user",
            "content": f"Analyze the SUBTEXT in this scene:\n\n{EXAMPLE_SCRIPT}"
        }
    ]

    data = {
        "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.75,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            "num_predict": 4000,
            "num_ctx": 8192
        }
    }

    start_time = time.time()

    try:
        response = requests.post(
            'http://localhost:11434/api/chat',
            json=data,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()

        if 'message' in result and 'content' in result['message']:
            content = result['message']['content']

            # Análise
            citations = count_theory_citations(content)
            total_citations = sum(citations.values())
            technique_bonus = count_technique_bonuses(content, config["technique_keywords"])
            word_count = len(content.split())
            total_score = total_citations + technique_bonus

            elapsed = time.time() - start_time

            return {
                'success': True,
                'name': config["name"],
                'content': content,
                'citations': citations,
                'total_citations': total_citations,
                'technique_bonus': technique_bonus,
                'total_score': total_score,
                'word_count': word_count,
                'time': elapsed
            }
    except Exception as e:
        return {
            'success': False,
            'name': config["name"],
            'error': str(e)
        }

    return {
        'success': False,
        'name': config["name"],
        'error': 'No content in response'
    }

def main():
    print("=" * 60)
    print("⚡ TESTE DE 5 VARIAÇÕES PARA SUBTEXT")
    print("=" * 60)

    results = []

    for key, config in VARIATIONS.items():
        print(f"\n🎭 {key}: {config['name']}")

        result = test_variation(key, config)

        if result['success']:
            print(f"   ✅ {key}: {result['total_score']} pontos "
                  f"({result['total_citations']} base + {result['technique_bonus']} técnicas)")
            print(f"      Palavras: {result['word_count']}, Tempo: {result['time']:.1f}s")
            results.append(result)
        else:
            print(f"   ❌ {key}: Erro - {result.get('error', 'Unknown')}")

    # Ranking
    print("\n" + "=" * 60)
    print("📊 RANKING DAS VARIAÇÕES DE SUBTEXT")
    print("=" * 60)

    results.sort(key=lambda x: x['total_score'], reverse=True)

    medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']
    for i, result in enumerate(results[:5]):
        citations_str = ' '.join([f"{k}:{v}" for k, v in result['citations'].items() if v > 0])
        print(f"{medals[i]} {result['name']}: {result['total_score']} pts "
              f"({result['total_citations']} base + {result['technique_bonus']} técnicas), "
              f"{result['word_count']} palavras")
        print(f"   Citações: {citations_str}")

    # Comparação com original
    print(f"\n📊 COMPARAÇÃO:")
    print(f"SUBTEXT ainda não tem versão original")
    if results and results[0]['total_score'] >= 25:
        print(f"Melhor variação: {results[0]['name']} com {results[0]['total_score']} pontos")
        print(f"🏆 EXCELENTE! Superou 25 pontos!")

    # Salvar resultados
    if results:
        winner = results[0]
        print(f"\n💡 VENCEDOR: {winner['name']} com {winner['total_score']} pontos!")

        # Salvar resumo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = f"subtext_variations_summary_{timestamp}.json"

        summary = {
            "timestamp": timestamp,
            "winner": winner['name'],
            "winner_score": winner['total_score'],
            "all_results": [
                {
                    "name": r['name'],
                    "total_score": r['total_score'],
                    "citations": r['total_citations'],
                    "techniques": r['technique_bonus'],
                    "words": r['word_count']
                }
                for r in results
            ]
        }

        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(f"📊 Resumo salvo em {summary_file}")

if __name__ == "__main__":
    main()