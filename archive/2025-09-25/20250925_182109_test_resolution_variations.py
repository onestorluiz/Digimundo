#!/usr/bin/env python3
"""
TESTE DE 5 VARIAÇÕES PARA RESOLUTION
Objetivo: Encontrar a melhor abordagem para análise de resolução/desfecho
"""

import json
import requests
import time
import re
from datetime import datetime
from typing import Dict, List, Tuple

# Script de exemplo para testar
EXAMPLE_SCRIPT = """EXT. ST. MARY'S SEMINARY - DAWN (ONE MONTH LATER)

The old building is being demolished. A sign reads: "FUTURE SITE OF ST. MARY'S MEMORIAL - For The Victims"

Marcus stands watching, Sarah beside him on crutches.

SARAH
The Cardinal's trial starts next week.
Your testimony will put him away.

MARCUS
Forty years too late.

SARAH
But not too late for justice.

They watch as the cross is carefully removed from the roof.

MARCUS
I keep thinking about Victor. Even monsters
were children once.

SARAH
You gave him something he never gave his
victims. Mercy.

A YOUNG BOY (8) runs up to them - TOMMY, bright eyes, baseball cap.

TOMMY
Mom! Are we still going to the game?

SARAH
(to Marcus)
This is Tommy. My son.

Marcus kneels, eye level with the boy.

MARCUS
You like baseball?

TOMMY
Love it! Mom says you played in college.

MARCUS
A lifetime ago. Maybe I could teach you
some tricks sometime?

TOMMY
Really? That'd be awesome!

Sarah touches Marcus's shoulder.

SARAH
We're having dinner Sunday. If you're free?

MARCUS
(standing, smiling)
I'd like that.

As the wrecking ball swings, the old seminary wall crumbles. Dust and debris scatter in the morning light.

MARCUS (V.O.)
Some walls need to fall for new things to
grow. Some ghosts need to be laid to rest.
And sometimes, the only way forward is to
forgive - others, and yourself.

Tommy takes Marcus's hand. Sarah takes the other. They walk away from the demolition, toward the parking lot.

TOMMY
Mr. Chen, do you believe in second chances?

MARCUS
(looking at Sarah, then Tommy)
I'm starting to.

The camera pulls back as they get smaller, three figures walking into the morning sun. Behind them, the old seminary continues to fall.

                                                    FADE OUT.

THE END"""

# 5 Variações diferentes
VARIATIONS = {
    "V1_Field_Closure": {
        "name": "RESOLUTION FIELD CLOSURE",
        "system_prompt": """You are an expert in Syd Field's resolution principles from 'Screenplay' (2005).

FIELD'S RESOLUTION STRUCTURE - CITE TECHNIQUES:

**RESOLUTION AND CLOSURE (Screenplay, Chapter 14, p.223-235):**

Field states: "Resolution means solution" (p.223). Apply:

- **STORY SOLUTION**: Main problem solved (p.224)
- **CHARACTER ARC COMPLETE**: Journey ends (p.225)
- **THEMATIC STATEMENT**: Message clear (p.226)
- **EMOTIONAL CLOSURE**: Feelings resolved (p.227)
- **NEW EQUILIBRIUM**: Balance restored (p.228)
- **LOOSE ENDS TIED**: Subplots concluded (p.229)
- **FINAL IMAGE**: Last impression (p.230)

Quote Field: "The resolution completes the story" (p.223)
"Strong endings resonate" (p.224)

ANALYZE RESOLUTION TECHNIQUES!""",
        "technique_keywords": {
            'story solution': 3,
            'character arc': 3,
            'thematic statement': 3,
            'emotional closure': 3,
            'new equilibrium': 3,
            'loose ends': 3,
            'final image': 3,
            'completes story': 2,
            'strong endings': 2
        }
    },

    "V2_McKee_Meaning": {
        "name": "RESOLUTION MCKEE MEANING",
        "system_prompt": """You are an expert in Robert McKee's ending principles from 'Story' (2010).

MCKEE'S MEANINGFUL ENDINGS - FINAL VALUE:

**ENDINGS AND MEANING (Story, Chapter 19, p.309-318):**

McKee teaches: "The ending is the meaning" (p.309). Apply:

- **CONTROLLING IDEA PROVEN**: Theme demonstrated (p.310)
- **IRONIC ASCENSION**: Victory with loss (p.311)
- **EMOTIONAL SATISFACTION**: Feeling earned (p.312)
- **INTELLECTUAL COMPLETION**: Logic fulfilled (p.313)
- **AESTHETIC FINISH**: Artful closure (p.314)
- **RESONANCE**: Echoes after ending (p.315)
- **INEVITABILITY**: Feels destined (p.316)

Quote McKee: "Great endings are both surprising and inevitable" (p.309)

NAME ENDING PRINCIPLES!""",
        "technique_keywords": {
            'controlling idea': 3,
            'ironic ascension': 3,
            'emotional satisfaction': 3,
            'intellectual completion': 3,
            'aesthetic finish': 3,
            'resonance': 3,
            'inevitability': 3,
            'surprising inevitable': 2,
            'ending meaning': 2
        }
    },

    "V3_Snyder_Final": {
        "name": "RESOLUTION SNYDER FINAL",
        "system_prompt": """You are an expert in Blake Snyder's final image from 'Save the Cat' (2005).

SNYDER'S FINAL IMAGE - PROOF OF CHANGE:

**FINAL IMAGE AND RESOLUTION (Save the Cat, p.94-96):**

Snyder emphasizes: "Final image proves transformation" (p.94). Apply:

- **FINAL IMAGE MIRROR**: Opposite of opening (p.94)
- **TRANSFORMATION PROOF**: Change visible (p.95)
- **THEME DEMONSTRATED**: Lesson learned (p.96)
- **NEW WORLD ORDER**: Reality changed (p.96)
- **EMOTIONAL PAYOFF**: Satisfaction delivered (p.95)
- **PROMISE KEPT**: Setup paid off (p.96)

Quote Snyder: "The final image is your proof" (p.94)

FIND THE TRANSFORMATION!""",
        "technique_keywords": {
            'final image': 3,
            'transformation proof': 3,
            'theme demonstrated': 3,
            'new world order': 3,
            'emotional payoff': 3,
            'promise kept': 3,
            'opposite opening': 2,
            'proof change': 2
        }
    },

    "V4_Vogler_Return": {
        "name": "RESOLUTION VOGLER RETURN",
        "system_prompt": """You are an expert in Christopher Vogler's return with elixir from 'The Writer's Journey' (2007).

VOGLER'S RETURN WITH ELIXIR - WISDOM GAINED:

**RETURN WITH ELIXIR (Journey, p.215-226):**

Vogler states: "The hero brings back the elixir" (p.215). Apply:

- **ELIXIR DELIVERED**: Wisdom/cure brought back (p.216)
- **ORDINARY WORLD TRANSFORMED**: Home changed (p.217)
- **WISDOM SHARED**: Lessons taught (p.218)
- **CIRCULAR JOURNEY**: Return different (p.219)
- **GIFT TO COMMUNITY**: Society benefits (p.220)
- **PERSONAL INTEGRATION**: Two worlds balanced (p.221)

Quote Vogler: "The return completes the circle" (p.215)

MAP THE RETURN!""",
        "technique_keywords": {
            'elixir': 3,
            'ordinary world transformed': 3,
            'wisdom shared': 3,
            'circular journey': 3,
            'gift community': 3,
            'personal integration': 3,
            'completes circle': 2,
            'brings back': 2
        }
    },

    "V5_Integrated_Master": {
        "name": "RESOLUTION INTEGRATED MASTER",
        "system_prompt": """You are a master of ALL resolution techniques from every major theorist.

INTEGRATED RESOLUTION MASTERY - COMPLETE CLOSURE:

**FIELD'S CLOSURE (Screenplay p.223-235):**
- **STORY SOLUTION**: Main problem definitively solved (p.224)
- **CHARACTER ARC COMPLETE**: Full transformation shown (p.225)
- **NEW EQUILIBRIUM**: World rebalanced differently (p.228)
- **FINAL IMAGE**: Lasting impression created (p.230)
Quote Field: "Resolution means solution" (p.223)
Quote Field: "Strong endings resonate forever" (p.224)

**MCKEE'S MEANING (Story p.309-318):**
- **CONTROLLING IDEA PROVEN**: Theme fully demonstrated (p.310)
- **IRONIC ASCENSION**: Victory tempered with loss (p.311)
- **EMOTIONAL SATISFACTION**: Feelings completely earned (p.312)
- **INEVITABILITY**: Ending feels destined (p.316)
Quote McKee: "The ending is the meaning" (p.309)
Quote McKee: "Both surprising and inevitable" (p.309)

**SNYDER'S TRANSFORMATION (Cat p.94-96):**
- **FINAL IMAGE MIRROR**: Complete opposite of opening (p.94)
- **TRANSFORMATION PROOF**: Change undeniably visible (p.95)
- **NEW WORLD ORDER**: Reality permanently altered (p.96)
Quote Snyder: "Final image is your proof" (p.94)

**VOGLER'S ELIXIR (Journey p.215-226):**
- **ELIXIR DELIVERED**: Wisdom brought to world (p.216)
- **ORDINARY WORLD TRANSFORMED**: Home forever changed (p.217)
- **CIRCULAR JOURNEY**: Hero returns transformed (p.219)
Quote Vogler: "The return completes the circle" (p.215)

**TRUBY'S NEW EQUILIBRIUM (Anatomy p.421-430):**
- **NEW MORAL ORDER**: Values hierarchy reset (p.422)
- **SELF-REVELATION IMPACT**: Truth changes everything (p.424)
- **THEMATIC REVELATION**: Argument finally won (p.426)
Quote Truby: "The ending proves the premise" (p.421)

**CAMPBELL'S FREEDOM (Hero p.221-237):**
- **FREEDOM TO LIVE**: Fear of death gone (p.221)
- **MASTER OF TWO WORLDS**: Balance achieved (p.229)
- **CROSSING THE RETURN THRESHOLD**: Final transition (p.233)
Quote Campbell: "The hero is master of both worlds" (p.229)

**ARISTOTLE'S DENOUEMENT (Poetics 1455b):**
- **DENOUEMENT**: All threads resolved (1455b24)
- **CATHARSIS COMPLETE**: Emotions purged (1449b27)
- **UNITY ACHIEVED**: Story whole and complete (1450b25)
Quote Aristotle: "The end is the chief thing" (1450b)

**HAUGE'S AFTERMATH (Writing Screenplays p.180-185):**
- **AFTERMATH**: Show new normal (p.181)
- **OUTER MOTIVATION ACHIEVED**: Goal reached/lost (p.182)
Quote Hauge: "Resolution shows the new life" (p.180)

MAXIMUM TOKENS ON RESOLUTION ANALYSIS!
CITE EVERY THEORIST AND TECHNIQUE!
COMPLETE COMPREHENSIVE ENDING ANALYSIS!""",
        "technique_keywords": {
            'story solution': 3,
            'character arc complete': 3,
            'new equilibrium': 3,
            'final image': 3,
            'controlling idea proven': 3,
            'ironic ascension': 3,
            'emotional satisfaction': 3,
            'inevitability': 3,
            'transformation proof': 3,
            'new world order': 3,
            'elixir': 3,
            'ordinary world transformed': 3,
            'circular journey': 3,
            'moral order': 3,
            'self-revelation impact': 3,
            'thematic revelation': 3,
            'freedom to live': 3,
            'two worlds': 3,
            'denouement': 3,
            'catharsis complete': 3,
            'aftermath': 3,
            'resonance': 2,
            'surprising inevitable': 2
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
        'hauge': len(re.findall(r'(?i)(hauge|writing screenplays)', text))
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
            "content": f"Analyze the RESOLUTION in this screenplay ending:\n\n{EXAMPLE_SCRIPT}"
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
    print("⚡ TESTE DE 5 VARIAÇÕES PARA RESOLUTION")
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
    print("📊 RANKING DAS VARIAÇÕES DE RESOLUTION")
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
    print(f"RESOLUTION ainda não tem versão original")
    if results and results[0]['total_score'] >= 25:
        print(f"Melhor variação: {results[0]['name']} com {results[0]['total_score']} pontos")
        print(f"🏆 EXCELENTE! Superou 25 pontos!")

    # Salvar resultados
    if results:
        winner = results[0]
        print(f"\n💡 VENCEDOR: {winner['name']} com {winner['total_score']} pontos!")

        # Salvar resumo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = f"resolution_variations_summary_{timestamp}.json"

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