#!/usr/bin/env python3
"""
TESTE DE 5 VARIAÇÕES PARA EXPOSITION
Objetivo: Encontrar a melhor abordagem para análise de exposição
"""

import json
import requests
import time
import re
from datetime import datetime
from typing import Dict, List, Tuple

# Script de exemplo para testar
EXAMPLE_SCRIPT = """INT. POLICE STATION - DAY

DETECTIVE SARAH COLE (40s, sharp eyes, worn badge) studies a wall of photos - three victims, all priests.

CAPTAIN REYNOLDS (50s) enters.

REYNOLDS
Cole, you've been on this for six months.
The press is calling him the Confessor.

SARAH
Three dead priests. All heard confessions
the night they died. All stabbed through
the heart with a crucifix.

REYNOLDS
The Cardinal's breathing down my neck.
Says it's making the Church look bad.

SARAH
(studying photos)
First victim - Father Martinez, 72. Twenty
years at St. Augustine's. Found in his
confessional booth.

REYNOLDS
I remember. No witnesses, no forensics.

SARAH
Second victim - Father O'Brien, 58.
Soup kitchen volunteer. Found at the altar.
Same MO. Same message carved in Latin:
"Peccata patris" - sins of the father.

REYNOLDS
And now Father Thompson makes three.
What's the connection?

SARAH
All three served at St. Mary's Seminary
in the 80s. All three transferred out
suddenly in 1987.

REYNOLDS
You think this is about something that
happened forty years ago?

SARAH
(turns to him)
I think someone's been waiting forty years
for justice."""

# 5 Variações diferentes
VARIATIONS = {
    "V1_McKee_Invisible": {
        "name": "EXPOSITION McKEE INVISIBLE",
        "system_prompt": """You are an expert in Robert McKee's exposition techniques from 'Story' (2010 edition).

MCKEE'S INVISIBLE EXPOSITION - CITE SPECIFIC TECHNIQUES:

**EXPOSITION AS AMMUNITION (Story, Chapter 15, p.334-344):**

McKee states: "Exposition is ammunition that must be fired at the right moment" (p.334). Apply:

- **SHOW DON'T TELL**: Dramatize information (p.335)
- **PROGRESSIVE REVELATION**: Layer information strategically (p.336)
- **CONFLICT-DRIVEN EXPOSITION**: Info through confrontation (p.337)
- **INVISIBLE EXPOSITION**: Hide in conflict/humor (p.338)
- **DELAY AND DENY**: Withhold then reveal (p.339)
- **FALSE EXPOSITION**: Mislead then correct (p.340)
- **EMOTIONAL EXPOSITION**: Info charged with feeling (p.341)

Quote McKee: "Never include anything the audience can reasonably assume" (p.335)
"Convert exposition to ammunition" (p.334)

CITE EVERY TECHNIQUE! MAXIMUM DEPTH!""",
        "technique_keywords": {
            'show don\'t tell': 3,
            'progressive revelation': 3,
            'conflict-driven': 3,
            'invisible exposition': 3,
            'delay deny': 3,
            'false exposition': 3,
            'emotional exposition': 3,
            'ammunition': 2,
            'reasonably assume': 2
        }
    },

    "V2_Truby_Reveal": {
        "name": "EXPOSITION TRUBY REVEAL",
        "system_prompt": """You are an expert in John Truby's revelation sequence from 'Anatomy of Story' (2007).

TRUBY'S REVELATION SEQUENCE - STRATEGIC REVEALS:

**EXPOSITION THROUGH REVEALS (Anatomy, p.330-340):**

Truby teaches: "Information is power - control its release" (p.330). Apply:

- **REVELATION SEQUENCE**: Strategic information timing (p.331)
- **ICEBERG TECHNIQUE**: Show 10%, suggest 90% (p.332)
- **BACKSTORY WEAVE**: Past woven into present (p.333)
- **GHOST REVELATION**: Past event driving present (p.334)
- **NEED EXPOSITION**: Character's flaw revealed (p.335)
- **OPPONENT REVEALS**: Info through antagonist (p.336)

Quote Truby: "Great exposition feels like discovery" (p.331)

NAME EVERY REVEAL TECHNIQUE!""",
        "technique_keywords": {
            'revelation sequence': 3,
            'iceberg technique': 3,
            'backstory weave': 3,
            'ghost revelation': 3,
            'need exposition': 3,
            'opponent reveals': 3,
            'feels like discovery': 2,
            'information power': 2
        }
    },

    "V3_Field_Context": {
        "name": "EXPOSITION FIELD CONTEXT",
        "system_prompt": """You are an expert in Syd Field's contextual exposition from 'Screenplay' (2005).

FIELD'S CONTEXTUAL EXPOSITION - ORGANIC INFORMATION:

**SETUP AND CONTEXT (Screenplay, p.88-95):**

Field emphasizes: "Context creates natural exposition" (p.88). Apply:

- **SETUP PAYOFF**: Plant information early (p.89)
- **VISUAL EXPOSITION**: Show through images (p.90)
- **CONTEXTUAL REVEAL**: Situation reveals info (p.91)
- **ACTION EXPOSITION**: Info through doing (p.92)
- **INCITING INCIDENT INFO**: Exposition in catalyst (p.93)

Quote Field: "The first ten pages tell us everything" (p.88)

ANALYZE CONTEXTUAL REVEALS!""",
        "technique_keywords": {
            'setup payoff': 3,
            'visual exposition': 3,
            'contextual reveal': 3,
            'action exposition': 3,
            'inciting incident': 3,
            'first ten pages': 2,
            'context creates': 2
        }
    },

    "V4_Snyder_Pope": {
        "name": "EXPOSITION SNYDER POPE",
        "system_prompt": """You are an expert in Blake Snyder's 'Pope in the Pool' from 'Save the Cat' (2005).

SNYDER'S POPE IN THE POOL - FUN & GAMES EXPOSITION:

**ENTERTAINING EXPOSITION (Save the Cat, p.123-125):**

Snyder's rule: "Give exposition while something interesting happens" (p.123). Apply:

- **POPE IN THE POOL**: Boring info + interesting visual (p.123)
- **DOUBLE MUMBO JUMBO**: Avoid tech overload (p.124)
- **FUN AND GAMES**: Entertain while informing (p.125)
- **LAYING PIPE**: Essential setup work (p.70)
- **SAVE THE CAT INFO**: Character revealed in action (p.xv)

Quote Snyder: "Audience will forgive exposition if entertained" (p.123)

FIND THE POPE IN EVERY POOL!""",
        "technique_keywords": {
            'pope in pool': 3,
            'double mumbo jumbo': 3,
            'fun and games': 3,
            'laying pipe': 3,
            'save the cat': 3,
            'forgive exposition': 2,
            'something interesting': 2
        }
    },

    "V5_Integrated_Ultra": {
        "name": "EXPOSITION INTEGRATED ULTRA",
        "system_prompt": """You are a master of ALL exposition techniques from every major theorist.

INTEGRATED EXPOSITION MASTERY - ALL TECHNIQUES:

**MCKEE'S AMMUNITION (Story p.334-344):**
- **SHOW DON'T TELL**: Dramatize information (p.335)
- **INVISIBLE EXPOSITION**: Hide in conflict (p.338)
- **PROGRESSIVE REVELATION**: Strategic layers (p.336)
Quote: "Convert exposition to ammunition" (p.334)

**TRUBY'S REVEALS (Anatomy p.330-340):**
- **REVELATION SEQUENCE**: Timed releases (p.331)
- **ICEBERG TECHNIQUE**: Show 10% suggest 90% (p.332)
- **GHOST REVELATION**: Past driving present (p.334)
Quote: "Great exposition feels like discovery" (p.331)

**FIELD'S CONTEXT (Screenplay p.88-95):**
- **VISUAL EXPOSITION**: Show through images (p.90)
- **SETUP PAYOFF**: Plant early harvest late (p.89)
Quote: "The first ten pages tell everything" (p.88)

**SNYDER'S ENTERTAINMENT (Cat p.123-125):**
- **POPE IN THE POOL**: Info + interest (p.123)
- **DOUBLE MUMBO JUMBO**: Avoid overload (p.124)
Quote: "Audience forgives if entertained" (p.123)

**VOGLER'S ORDINARY WORLD (Journey p.81-89):**
- **ORDINARY WORLD**: Establish normal (p.81)
- **SPECIAL WORLD CONTRAST**: Show change (p.85)
Quote: "Context is everything" (p.82)

**CAMPBELL'S THRESHOLD (Hero p.77-89):**
- **THRESHOLD INFORMATION**: Portal moment (p.77)
- **KNOWN TO UNKNOWN**: Info at border (p.80)

**ARISTOTLE'S RECOGNITION (Poetics 1452a):**
- **ANAGNORISIS**: Discovery of information (1452a29)
- **FROM IGNORANCE**: Knowledge revealed (1452a30)

MAXIMUM TOKENS! EVERY TECHNIQUE! CITE ALL!
SPEND TOKENS ON QUALITY EXPOSITION ANALYSIS!""",
        "technique_keywords": {
            'show don\'t tell': 3,
            'invisible exposition': 3,
            'progressive revelation': 3,
            'ammunition': 3,
            'revelation sequence': 3,
            'iceberg technique': 3,
            'ghost revelation': 3,
            'visual exposition': 3,
            'setup payoff': 3,
            'pope in pool': 3,
            'double mumbo jumbo': 3,
            'ordinary world': 3,
            'special world': 3,
            'threshold information': 3,
            'anagnorisis': 3,
            'feels discovery': 2,
            'first ten pages': 2,
            'forgive entertained': 2,
            'context everything': 2
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
            "content": f"Analyze the EXPOSITION techniques in this scene:\n\n{EXAMPLE_SCRIPT}"
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
    print("⚡ TESTE DE 5 VARIAÇÕES PARA EXPOSITION")
    print("=" * 60)

    results = []

    for key, config in VARIATIONS.items():
        print(f"\n📝 {key}: {config['name']}")

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
    print("📊 RANKING DAS VARIAÇÕES DE EXPOSITION")
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
    print(f"EXPOSITION ainda não tem versão original")
    if results and results[0]['total_score'] >= 25:
        print(f"Melhor variação: {results[0]['name']} com {results[0]['total_score']} pontos")
        print(f"🏆 EXCELENTE! Superou 25 pontos!")

    # Salvar resultados
    if results:
        winner = results[0]
        print(f"\n💡 VENCEDOR: {winner['name']} com {winner['total_score']} pontos!")

        # Salvar resumo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = f"exposition_variations_summary_{timestamp}.json"

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