#!/usr/bin/env python3
"""
TESTE DE 5 VARIAÇÕES PARA TRANSITIONS
Objetivo: Encontrar a melhor abordagem para análise de transições
"""

import json
import requests
import time
import re
from datetime import datetime
from typing import Dict, List, Tuple

# Script de exemplo para testar
EXAMPLE_SCRIPT = """FADE IN:

EXT. CEMETERY - DAWN

Marcus stands before a fresh grave. Rain begins to fall.

MARCUS
(to gravestone)
Forgive me, Father Martinez.

                                                    CUT TO:

INT. CHURCH - CONFESSIONAL - NIGHT (FLASHBACK - 3 DAYS AGO)

Father Martinez sits in darkness. A shadow enters the other booth.

FATHER MARTINEZ
How may I help you, my child?

MARCUS (O.S.)
I've come to confess... your sins.

                                                    MATCH CUT:

INT. POLICE STATION - INTERROGATION ROOM - DAY (PRESENT)

Sarah slams a photo on the table - Father Martinez, dead.

SARAH
Three priests. Same message. Why?

Marcus doesn't flinch.

MARCUS
Perhaps they needed forgiveness.

                                                    DISSOLVE TO:

EXT. ST. MARY'S SEMINARY - NIGHT (1987)

Young Marcus (20s) runs through the rain, blood on his hands.

                                                    SMASH CUT TO:

INT. MARCUS'S APARTMENT - NIGHT (PRESENT)

Marcus jolts awake. Sweating. The phone RINGS.

SARAH (V.O.)
(filtered)
We found another body.

                                                    FADE OUT."""

# 5 Variações diferentes
VARIATIONS = {
    "V1_Field_Classical": {
        "name": "TRANSITIONS FIELD CLASSICAL",
        "system_prompt": """You are an expert in Syd Field's classical transition techniques from 'Screenplay' (2005).

FIELD'S TRANSITION ARCHITECTURE - CITE TECHNIQUES:

**CLASSICAL TRANSITIONS (Screenplay, Chapter 12, p.200-210):**

Field teaches: "Transitions move story forward" (p.200). Apply:

- **CUT TO**: Direct scene change (p.201)
- **DISSOLVE**: Time passage/emotional shift (p.202)
- **FADE IN/OUT**: Beginning/ending beats (p.203)
- **MATCH CUT**: Visual continuity (p.204)
- **WIPE**: Old-fashioned transition (p.205)
- **IRIS IN/OUT**: Focus technique (p.206)
- **MONTAGE**: Compressed time (p.207)

Quote Field: "Every transition has dramatic purpose" (p.200)

ANALYZE TRANSITION FUNCTIONS!""",
        "technique_keywords": {
            'cut to': 3,
            'dissolve': 3,
            'fade': 3,
            'match cut': 3,
            'wipe': 2,
            'iris': 2,
            'montage': 3,
            'dramatic purpose': 2,
            'story forward': 2
        }
    },

    "V2_McKee_Seamless": {
        "name": "TRANSITIONS McKEE SEAMLESS",
        "system_prompt": """You are an expert in Robert McKee's seamless transitions from 'Story' (2010).

MCKEE'S SEAMLESS TRANSITIONS - INVISIBLE FLOW:

**TRANSITION AS STORY (Story, Chapter 14, p.298-310):**

McKee states: "The best transition is invisible" (p.298). Apply:

- **CAUSALITY BRIDGES**: Effect becomes cause (p.299)
- **EMOTIONAL TRANSITIONS**: Feeling carries over (p.300)
- **THEMATIC LINKS**: Ideas connect scenes (p.301)
- **IRONIC TRANSITIONS**: Contrast for effect (p.302)
- **MOMENTUM TRANSITIONS**: Energy propels (p.303)
- **QUESTION TRANSITIONS**: Curiosity drives (p.304)

Quote McKee: "Transitions are story telling" (p.298)

NAME EVERY SEAMLESS TECHNIQUE!""",
        "technique_keywords": {
            'causality bridge': 3,
            'emotional transition': 3,
            'thematic link': 3,
            'ironic transition': 3,
            'momentum transition': 3,
            'question transition': 3,
            'invisible': 2,
            'seamless': 2,
            'story telling': 2
        }
    },

    "V3_Eisenstein_Montage": {
        "name": "TRANSITIONS EISENSTEIN MONTAGE",
        "system_prompt": """You are an expert in Sergei Eisenstein's montage theory applied to screenplay transitions.

EISENSTEIN'S MONTAGE THEORY - COLLISION CREATES MEANING:

**MONTAGE TYPES (Film Form/Film Sense):**

Eisenstein: "Montage is collision" - two shots create third meaning. Apply:

- **METRIC MONTAGE**: Mathematical rhythm
- **RHYTHMIC MONTAGE**: Visual tempo
- **TONAL MONTAGE**: Emotional resonance
- **OVERTONAL MONTAGE**: Multiple stimuli
- **INTELLECTUAL MONTAGE**: Conceptual juxtaposition
- **DIALECTICAL MONTAGE**: Thesis + antithesis = synthesis

Quote: "From collision of shots, concepts are born"

ANALYZE COLLISION TRANSITIONS!""",
        "technique_keywords": {
            'metric montage': 3,
            'rhythmic montage': 3,
            'tonal montage': 3,
            'overtonal': 3,
            'intellectual montage': 3,
            'dialectical': 3,
            'collision': 2,
            'juxtaposition': 2,
            'synthesis': 2
        }
    },

    "V4_Snyder_Beat": {
        "name": "TRANSITIONS SNYDER BEAT",
        "system_prompt": """You are an expert in Blake Snyder's beat transitions from 'Save the Cat' (2005).

SNYDER'S BEAT TRANSITIONS - STRUCTURAL BRIDGES:

**BEAT SHEET TRANSITIONS (Save the Cat, p.70-90):**

Snyder emphasizes: "Each beat must flow to the next" (p.70). Apply:

- **CATALYST TO DEBATE**: Question posed (p.76)
- **BREAK INTO TWO**: World shift (p.78)
- **B STORY INTRODUCTION**: New element (p.79)
- **MIDPOINT SHIFT**: False victory/defeat (p.80)
- **ALL IS LOST TO DARK NIGHT**: Emotional bottom (p.86)
- **BREAK INTO THREE**: Solution found (p.88)

Quote Snyder: "Transitions are promises kept" (p.70)

MAP BEAT TRANSITIONS!""",
        "technique_keywords": {
            'catalyst': 3,
            'debate': 3,
            'break into': 3,
            'b story': 3,
            'midpoint shift': 3,
            'all is lost': 3,
            'dark night': 3,
            'promises kept': 2,
            'beat flow': 2
        }
    },

    "V5_Integrated_Master": {
        "name": "TRANSITIONS INTEGRATED MASTER",
        "system_prompt": """You are a master of ALL transition techniques from every major theorist.

INTEGRATED TRANSITIONS MASTERY - ALL TECHNIQUES:

**FIELD'S CLASSICAL (Screenplay p.200-210):**
- **CUT TO**: Direct change (p.201)
- **DISSOLVE**: Time/emotion shift (p.202)
- **MATCH CUT**: Visual bridge (p.204)
Quote: "Every transition has purpose" (p.200)

**MCKEE'S SEAMLESS (Story p.298-310):**
- **CAUSALITY BRIDGES**: Effect→cause (p.299)
- **THEMATIC LINKS**: Ideas connect (p.301)
- **IRONIC TRANSITIONS**: Contrast (p.302)
Quote: "Best transition is invisible" (p.298)

**EISENSTEIN'S MONTAGE (Film Form):**
- **INTELLECTUAL MONTAGE**: Concepts collide
- **DIALECTICAL**: Thesis+antithesis=synthesis
Quote: "Montage is collision"

**SNYDER'S BEATS (Cat p.70-90):**
- **CATALYST→DEBATE**: Question flow (p.76)
- **MIDPOINT SHIFT**: Story turns (p.80)
Quote: "Transitions are promises" (p.70)

**TRUBY'S REVEALS (Anatomy p.298-305):**
- **REVELATION TRANSITIONS**: Discovery drives (p.299)
- **SCENE WEAVE**: Multiple storylines (p.300)
Quote: "Transitions reveal character" (p.298)

**VOGLER'S THRESHOLDS (Journey p.127-134):**
- **THRESHOLD CROSSINGS**: World changes (p.127)
- **SYMBOLIC TRANSITIONS**: Meaning shifts (p.130)
Quote: "Every transition is a threshold" (p.127)

**ARISTOTLE'S UNITIES (Poetics 1450b):**
- **UNITY OF ACTION**: Causal necessity (1450b)
- **EPISODIC AVOIDANCE**: Logical flow (1451a)

MAXIMUM TOKENS! CITE ALL TECHNIQUES!
ANALYZE EVERY TRANSITION TYPE!""",
        "technique_keywords": {
            'cut to': 3,
            'dissolve': 3,
            'match cut': 3,
            'fade': 3,
            'causality bridge': 3,
            'thematic link': 3,
            'ironic transition': 3,
            'intellectual montage': 3,
            'dialectical': 3,
            'catalyst': 3,
            'midpoint shift': 3,
            'revelation transition': 3,
            'scene weave': 3,
            'threshold crossing': 3,
            'symbolic transition': 3,
            'unity of action': 3,
            'invisible': 2,
            'collision': 2,
            'promises': 2
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
        'aristotle': len(re.findall(r'(?i)(aristotle|poetics)', text)),
        'eisenstein': len(re.findall(r'(?i)(eisenstein|montage|film form)', text))
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
            "content": f"Analyze the TRANSITIONS in this screenplay excerpt:\n\n{EXAMPLE_SCRIPT}"
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
    print("⚡ TESTE DE 5 VARIAÇÕES PARA TRANSITIONS")
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
    print("📊 RANKING DAS VARIAÇÕES DE TRANSITIONS")
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
    print(f"TRANSITIONS ainda não tem versão original")
    if results and results[0]['total_score'] >= 25:
        print(f"Melhor variação: {results[0]['name']} com {results[0]['total_score']} pontos")
        print(f"🏆 EXCELENTE! Superou 25 pontos!")

    # Salvar resultados
    if results:
        winner = results[0]
        print(f"\n💡 VENCEDOR: {winner['name']} com {winner['total_score']} pontos!")

        # Salvar resumo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = f"transitions_variations_summary_{timestamp}.json"

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