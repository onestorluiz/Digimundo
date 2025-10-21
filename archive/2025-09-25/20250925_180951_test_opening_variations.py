#!/usr/bin/env python3
"""
TESTE DE 5 VARIAÇÕES PARA OPENING
Objetivo: Encontrar a melhor abordagem para análise de aberturas
"""

import json
import requests
import time
import re
from datetime import datetime
from typing import Dict, List, Tuple

# Script de exemplo para testar
EXAMPLE_SCRIPT = """FADE IN:

EXT. CHICAGO SKYLINE - DAWN

The city sleeps. Snow falls silently on empty streets.

                    SUPER: "DECEMBER 24, 1987"

A lone JOGGER (30s) runs along Lake Michigan. His breath forms clouds in the freezing air.

Suddenly, he stops. Stares at something in the water.

A BODY floats face-down among the ice chunks.

The jogger fumbles for his phone—

JOGGER
(into phone, panicked)
911? There's a body in the lake. 
Montrose Harbor. Jesus Christ, 
it's a kid...

As sirens approach in the distance, we—

                                                    CUT TO:

TITLE CARD: "CHRISTMAS EVE"

INT. DINER - SAME MORNING

DETECTIVE SARAH COLE (40s) sits alone at the counter. Coffee. No food. She stares at a PHOTOGRAPH: a smiling BOY (8) in a baseball uniform.

NEWS ANCHOR (ON TV)
...body of a young boy found in 
Lake Michigan this morning. Police 
suspect foul play...

Sarah's phone BUZZES. She sees the caller ID: "CAPTAIN". 

She doesn't answer.

The WAITRESS (60s, kind eyes) refills her coffee.

WAITRESS
Merry Christmas, hon.

Sarah forces a smile. Leaves a twenty. Walks out into the snow.

                                                    FADE OUT."""

# 5 Variações diferentes
VARIATIONS = {
    "V1_Field_Hook": {
        "name": "OPENING FIELD HOOK",
        "system_prompt": """You are an expert in Syd Field's opening techniques from 'Screenplay' (2005).

FIELD'S OPENING ARCHITECTURE - CITE TECHNIQUES:

**THE FIRST TEN PAGES (Screenplay, Chapter 1, p.3-25):**

Field states: "You have ten pages to grab your reader" (p.3). Apply:

- **INCITING INCIDENT**: The hook that starts everything (p.7)
- **DRAMATIC CONTEXT**: World and tone established (p.9)
- **MAIN CHARACTER INTRO**: Who is this story about? (p.11)
- **DRAMATIC PREMISE**: What's the story question? (p.13)
- **VISUAL STORYTELLING**: Show the world immediately (p.15)
- **ORDINARY WORLD**: Status quo before change (p.17)

Quote Field: "A screenplay is a story told with pictures" (p.7)
"The opening determines everything" (p.3)

ANALYZE OPENING HOOKS!""",
        "technique_keywords": {
            'inciting incident': 3,
            'dramatic context': 3,
            'main character': 3,
            'dramatic premise': 3,
            'visual storytelling': 3,
            'ordinary world': 3,
            'ten pages': 2,
            'grab reader': 2
        }
    },

    "V2_McKee_Image": {
        "name": "OPENING MCKEE IMAGE",
        "system_prompt": """You are an expert in Robert McKee's opening image from 'Story' (2010).

MCKEE'S OPENING IMAGE SYSTEM - POWERFUL BEGINNINGS:

**OPENING IMAGE THEORY (Story, Chapter 10, p.188-195):**

McKee teaches: "The opening image is the first impression" (p.188). Apply:

- **OPENING IMAGE**: Visual that contains whole story (p.189)
- **WORLD BUILDING**: Establish universe rules (p.190)
- **TONE AND MOOD**: Set emotional expectation (p.191)
- **CONTROLLING IDEA SEED**: Plant theme early (p.192)
- **GENRE EXPECTATIONS**: Promise what's coming (p.193)
- **CURIOSITY GAP**: Create questions immediately (p.194)

Quote McKee: "In the first minutes, an audience makes its deal with the writer" (p.188)

NAME OPENING TECHNIQUES!""",
        "technique_keywords": {
            'opening image': 3,
            'world building': 3,
            'tone mood': 3,
            'controlling idea': 3,
            'genre expectations': 3,
            'curiosity gap': 3,
            'first impression': 2,
            'audience deal': 2
        }
    },

    "V3_Snyder_Image": {
        "name": "OPENING SNYDER IMAGE",
        "system_prompt": """You are an expert in Blake Snyder's opening image from 'Save the Cat' (2005).

SNYDER'S OPENING IMAGE - BEFORE AND AFTER:

**OPENING IMAGE BEAT (Save the Cat, p.72-75):**

Snyder emphasizes: "Opening Image is your before snapshot" (p.72). Apply:

- **OPENING IMAGE**: The "before" picture (p.72)
- **SAVE THE CAT MOMENT**: Make hero likeable fast (p.xv)
- **THEME STATED**: Someone says what it's about (p.73)
- **SET-UP**: Introduce all A-story characters (p.74)
- **CATALYST**: The moment everything changes (p.75)
- **TONE PROMISE**: Genre and style clear (p.72)

Quote Snyder: "A good opening image is worth its weight in gold" (p.72)

FIND THE OPENING SNAPSHOT!""",
        "technique_keywords": {
            'opening image': 3,
            'save the cat': 3,
            'theme stated': 3,
            'set-up': 3,
            'catalyst': 3,
            'tone promise': 3,
            'before snapshot': 2,
            'weight in gold': 2
        }
    },

    "V4_Vogler_Ordinary": {
        "name": "OPENING VOGLER ORDINARY",
        "system_prompt": """You are an expert in Christopher Vogler's ordinary world from 'The Writer's Journey' (2007).

VOGLER'S ORDINARY WORLD - HERO'S STARTING POINT:

**ORDINARY WORLD OPENING (Journey, p.81-89):**

Vogler states: "Most stories take the hero out of the ordinary" (p.81). Apply:

- **ORDINARY WORLD**: Hero's normal life (p.81)
- **INNER PROBLEM**: What needs fixing inside (p.83)
- **OUTER PROBLEM**: External challenge coming (p.84)
- **WHAT'S AT STAKE**: What could be lost (p.85)
- **DRAMATIC QUESTION**: Will the hero succeed? (p.86)
- **FORESHADOWING**: Hints of what's to come (p.87)

Quote Vogler: "The ordinary world is the base camp of the adventure" (p.81)

MAP THE ORDINARY WORLD!""",
        "technique_keywords": {
            'ordinary world': 3,
            'inner problem': 3,
            'outer problem': 3,
            'at stake': 3,
            'dramatic question': 3,
            'foreshadowing': 3,
            'base camp': 2,
            'normal life': 2
        }
    },

    "V5_Integrated_Master": {
        "name": "OPENING INTEGRATED MASTER",
        "system_prompt": """You are a master of ALL opening techniques from every major theorist.

INTEGRATED OPENING MASTERY - MAXIMUM DETAIL:

**FIELD'S TEN PAGES (Screenplay p.3-25):**
- **INCITING INCIDENT**: Hook event starts everything (p.7)
- **TEN PAGE RULE**: Must grab reader immediately (p.3)
- **DRAMATIC PREMISE**: Central story question posed (p.13)
- **VISUAL STORYTELLING**: Pictures not words (p.15)
- **CHARACTER INTRODUCTION**: Who drives story (p.11)
Quote Field: "The opening determines everything" (p.3)
Quote Field: "You know within ten pages" (p.5)

**MCKEE'S OPENING IMAGE (Story p.188-195):**
- **OPENING IMAGE**: Single visual contains whole story (p.189)
- **CURIOSITY GAP**: Create questions immediately (p.194)
- **WORLD BUILDING**: Universe rules established (p.190)
- **TONE AND MOOD**: Emotional expectation set (p.191)
- **CONTROLLING IDEA**: Theme planted early (p.192)
Quote McKee: "In first minutes, audience makes its deal" (p.188)
Quote McKee: "Opening promises what's coming" (p.189)

**SNYDER'S SNAPSHOT (Save the Cat p.72-75, p.xv):**
- **OPENING IMAGE BEAT**: The "before" snapshot (p.72)
- **SAVE THE CAT MOMENT**: Make hero likeable instantly (p.xv)
- **THEME STATED**: Someone says what it's about (p.73)
- **SET-UP BEAT**: Introduce all A-story players (p.74)
- **CATALYST COMING**: Change is imminent (p.75)
Quote Snyder: "Opening image worth its weight in gold" (p.72)
Quote Snyder: "Give me the same thing... only different" (p.24)

**VOGLER'S ORDINARY WORLD (Journey p.81-89):**
- **ORDINARY WORLD ESTABLISHED**: Hero's normal life shown (p.81)
- **INNER PROBLEM REVEALED**: What needs fixing inside (p.83)
- **OUTER PROBLEM HINTED**: External challenge coming (p.84)
- **STAKES INTRODUCED**: What could be lost (p.85)
- **DRAMATIC QUESTION POSED**: Will hero succeed? (p.86)
Quote Vogler: "Ordinary world is base camp of adventure" (p.81)

**TRUBY'S WEAKNESS-NEED (Anatomy p.39-48):**
- **CHARACTER WEAKNESS**: Fatal flaw shown (p.39)
- **PSYCHOLOGICAL NEED**: Internal change required (p.40)
- **GHOST FROM PAST**: Backstory haunting present (p.41)
- **DESIRE LINE**: What character wants (p.42)
Quote Truby: "Begin with the need" (p.39)

**CAMPBELL'S DEPARTURE (Hero p.49-58):**
- **CALL TO ADVENTURE**: Story summons hero (p.49)
- **REFUSAL OF CALL**: Initial resistance shown (p.54)
- **SUPERNATURAL AID**: Help appears (p.57)
Quote Campbell: "The adventure begins" (p.49)

**ARISTOTLE'S BEGINNING (Poetics 1450b):**
- **PROPER BEGINNING**: "That which does not follow" (1450b27)
- **IN MEDIAS RES**: Start in middle of action (1450b28)
- **RECOGNITION SETUP**: Plant later discoveries (1452a)
Quote Aristotle: "Well-constructed plot" (1450b)

**HAUGE'S SETUP (Writing Screenplays p.90-95):**
- **SYMPATHY FACTORS**: Why we care (p.91)
- **IDENTIFICATION**: Connect with hero (p.92)
Quote Hauge: "First impressions last" (p.90)

SPEND MAXIMUM TOKENS! CITE EVERY THEORIST!
ANALYZE ALL OPENING ELEMENTS WITH QUOTES!
DO NOT CONSERVE TOKENS - USE THEM ALL!""",
        "technique_keywords": {
            'inciting incident': 3,
            'ten pages': 3,
            'dramatic premise': 3,
            'opening image': 3,
            'curiosity gap': 3,
            'world rules': 3,
            'before picture': 3,
            'save the cat': 3,
            'theme stated': 3,
            'ordinary world': 3,
            'inner problem': 3,
            'outer problem': 3,
            'weakness need': 3,
            'ghost': 3,
            'call adventure': 3,
            'refusal call': 3,
            'in medias res': 3,
            'grab reader': 2,
            'first minutes': 2,
            'worth gold': 2
        }
    }
}

def count_theory_citations(text: str) -> Dict[str, int]:
    """Conta citações de teóricos com mais flexibilidade."""
    citations = {
        'mckee': len(re.findall(r'(?i)(mckee|story[,\s]+(?:p\.?|page))', text)),
        'truby': len(re.findall(r'(?i)(truby|anatomy)', text)),
        'field': len(re.findall(r'(?i)(field|screenplay[,\s]+(?:p\.?|page))', text)),
        'snyder': len(re.findall(r'(?i)(snyder|save the cat|cat[,\s]+(?:p\.?|page))', text)),
        'vogler': len(re.findall(r"(?i)(vogler|writer'?s? journey|journey[,\s]+(?:p\.?|page))", text)),
        'campbell': len(re.findall(r'(?i)(campbell|hero with|thousand faces)', text)),
        'aristotle': len(re.findall(r'(?i)(aristotle|poetics)', text))
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
            "content": f"Analyze the OPENING of this screenplay:\n\n{EXAMPLE_SCRIPT}"
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
    print("⚡ TESTE DE 5 VARIAÇÕES PARA OPENING")
    print("=" * 60)

    results = []

    for key, config in VARIATIONS.items():
        print(f"\n🎬 {key}: {config['name']}")

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
    print("📊 RANKING DAS VARIAÇÕES DE OPENING")
    print("=" * 60)

    results.sort(key=lambda x: x['total_score'], reverse=True)

    medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']
    for i, result in enumerate(results[:5]):
        citations_str = ' '.join([f"{k}:{v}" for k, v in result['citations'].items() if v > 0])
        print(f"{medals[i]} {result['name']}: {result['total_score']} pts "
              f"({result['total_citations']} base + {result['technique_bonus']} técnicas), "
              f"{result['word_count']} palavras")
        print(f"   Citações: {citations_str}")

    # Comparação
    print(f"\n📊 COMPARAÇÃO:")
    print(f"OPENING ainda não tem versão original")
    if results and results[0]['total_score'] >= 25:
        print(f"Melhor variação: {results[0]['name']} com {results[0]['total_score']} pontos")
        print(f"🏆 EXCELENTE! Superou 25 pontos!")

    # Salvar resultados
    if results:
        winner = results[0]
        print(f"\n💡 VENCEDOR: {winner['name']} com {winner['total_score']} pontos!")

        # Salvar resumo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = f"opening_variations_summary_{timestamp}.json"

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
