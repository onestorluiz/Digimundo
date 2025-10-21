#!/usr/bin/env python3
"""
TESTE DE 5 VARIAÇÕES PARA CLIMAX
Objetivo: Encontrar a melhor abordagem para análise de clímax
"""

import json
import requests
import time
import re
from datetime import datetime
from typing import Dict, List, Tuple

# Script de exemplo para testar
EXAMPLE_SCRIPT = """INT. ABANDONED WAREHOUSE - NIGHT

Marcus faces VICTOR KANE (60s, scarred, eyes like ice). Between them lies SARAH, bleeding, barely conscious.

VICTOR
You always were weak, Marcus. Just like
forty years ago at St. Mary's.

MARCUS
(steady, resolved)
I was a child. You were supposed to
protect us.

VICTOR
I protected the Church. You and the others
were... necessary sacrifices.

Marcus's hand inches toward his concealed gun. Victor notices, smiles.

VICTOR (CONT'D)
Go ahead. Kill me. Become everything you
hate. Prove Father Martinez was right about
you.

SARAH
(weak, desperate)
Marcus... don't...

MARCUS
(to Victor)
Father Martinez died begging for forgiveness.
Not from God. From the children he failed.

VICTOR
Lies!

Victor lunges. Marcus sidesteps, grabs Victor's wrist, twists. The knife meant for Marcus plunges into Victor's chest.

Victor falls to his knees, gasping.

MARCUS
(kneeling beside him)
I forgive you, Victor. Not for you. For me.

Victor's eyes widen in shock, then slowly close. He falls forward.

Marcus rushes to Sarah, cradles her head.

MARCUS (CONT'D)
Stay with me. The ambulance is coming.

SARAH
(smiling weakly)
You... you didn't shoot him.

MARCUS
I'm not a killer anymore. I'm just... Marcus.

Sarah's hand finds his. In the distance, SIRENS approach.

SARAH
The Cardinal... he's next. Victor wasn't
working alone.

MARCUS
(determined)
Then we finish this. Together.

The warehouse doors BURST open. SWAT teams flood in.

CAPTAIN REYNOLDS
(over megaphone)
Marcus Chen, drop your weapons!

Marcus gently lays Sarah down, stands, raises his hands.

MARCUS
(loud, clear)
I have evidence. About St. Mary's. About
everything. The truth dies with me, or it
lives with justice.

Reynolds hesitates. The SWAT teams hold position.

REYNOLDS
(approaching cautiously)
You have one chance, Chen. Make it count.

Marcus reaches slowly into his jacket, pulls out a USB drive.

MARCUS
Forty years of evidence. Every name. Every
victim. Every cover-up.

REYNOLDS
(taking the drive)
This better be real.

MARCUS
Check Sarah's cloud backup. Password is
'Confession1987'. Everything's there too.

As paramedics rush to Sarah, Marcus looks back at Victor's body.

MARCUS (CONT'D)
(whispered)
It's over.

                                                    FADE OUT."""

# 5 Variações diferentes
VARIATIONS = {
    "V1_McKee_Crisis": {
        "name": "CLIMAX MCKEE CRISIS",
        "system_prompt": """You are an expert in Robert McKee's crisis/climax theory from 'Story' (2010).

MCKEE'S CRISIS/CLIMAX ARCHITECTURE - CITE TECHNIQUES:

**CRISIS AND CLIMAX (Story, Chapter 18, p.303-314):**

McKee states: "Crisis is the story's obligatory scene" (p.303). Apply:

- **CRISIS DECISION**: Dilemma of choices (p.304)
- **CLIMAX ACTION**: Decision executed (p.305)
- **IRREVERSIBLE CHANGE**: No going back (p.306)
- **VALUE CHARGE REVERSAL**: Positive to negative or vice versa (p.307)
- **FULL CHARACTER ARC**: True character revealed (p.308)
- **MAXIMUM PRESSURE**: Greatest forces clash (p.309)
- **EMOTIONAL PEAK**: Highest feeling (p.310)

Quote McKee: "In the climax, we reach the end of the line" (p.303)
"True character is revealed in the choices made under pressure" (p.101)

ANALYZE CRISIS AND CLIMAX!""",
        "technique_keywords": {
            'crisis decision': 3,
            'climax action': 3,
            'irreversible change': 3,
            'value charge': 3,
            'character arc': 3,
            'maximum pressure': 3,
            'emotional peak': 3,
            'obligatory scene': 2,
            'true character': 2
        }
    },

    "V2_Field_Resolution": {
        "name": "CLIMAX FIELD RESOLUTION",
        "system_prompt": """You are an expert in Syd Field's plot point theory from 'Screenplay' (2005).

FIELD'S CLIMAX RESOLUTION - STRUCTURAL PEAK:

**PLOT POINT AND RESOLUTION (Screenplay, p.127-142):**

Field teaches: "The climax is the solution to your story" (p.127). Apply:

- **PLOT POINT TWO**: Final confrontation setup (p.128)
- **RESOLUTION**: How it ends (p.130)
- **CONFRONTATION SCENE**: Protagonist vs antagonist (p.132)
- **TRANSFORMATION**: Character changed (p.134)
- **DRAMATIC NEED RESOLVED**: Want achieved/denied (p.136)
- **STORY QUESTION ANSWERED**: Central issue resolved (p.138)

Quote Field: "The strongest choice creates the climax" (p.127)

NAME RESOLUTION TECHNIQUES!""",
        "technique_keywords": {
            'plot point': 3,
            'resolution': 3,
            'confrontation scene': 3,
            'transformation': 3,
            'dramatic need': 3,
            'story question': 3,
            'strongest choice': 2,
            'solution story': 2
        }
    },

    "V3_Snyder_Finale": {
        "name": "CLIMAX SNYDER FINALE",
        "system_prompt": """You are an expert in Blake Snyder's finale from 'Save the Cat' (2005).

SNYDER'S FINALE - SYNTHESIS AND TRIUMPH:

**FINALE BEAT (Save the Cat, p.90-93):**

Snyder emphasizes: "The finale is synthesis of thesis and antithesis" (p.90). Apply:

- **STORMING THE CASTLE**: Final assault (p.90)
- **HIGH TOWER SURPRISE**: Twist in victory (p.91)
- **DIG DEEP DOWN**: Hero finds strength (p.92)
- **EXECUTION OF NEW PLAN**: Synthesis applied (p.93)
- **FINAL IMAGE**: Mirror of opening (p.94)
- **PROOF OF CHANGE**: Transformation shown (p.95)

Quote Snyder: "The finale proves your theme" (p.90)

FIND THE SYNTHESIS!""",
        "technique_keywords": {
            'storming castle': 3,
            'high tower surprise': 3,
            'dig deep down': 3,
            'new plan': 3,
            'final image': 3,
            'proof change': 3,
            'synthesis': 2,
            'proves theme': 2
        }
    },

    "V4_Vogler_Resurrection": {
        "name": "CLIMAX VOGLER RESURRECTION",
        "system_prompt": """You are an expert in Christopher Vogler's resurrection from 'The Writer's Journey' (2007).

VOGLER'S RESURRECTION - FINAL TEST:

**RESURRECTION AND RETURN (Journey, p.187-206):**

Vogler states: "Heroes must be tested once more" (p.187). Apply:

- **RESURRECTION TEST**: Final ordeal (p.188)
- **CLIMACTIC BATTLE**: Last confrontation (p.190)
- **DEATH AND REBIRTH**: Symbolic transformation (p.192)
- **PROOF OF JOURNEY**: Show change (p.194)
- **CHOICE MOMENT**: Active decision (p.196)
- **CATHARSIS**: Emotional purging (p.198)

Quote Vogler: "The hero must prove the journey changed them" (p.187)

MAP THE RESURRECTION!""",
        "technique_keywords": {
            'resurrection test': 3,
            'climactic battle': 3,
            'death rebirth': 3,
            'proof journey': 3,
            'choice moment': 3,
            'catharsis': 3,
            'final ordeal': 2,
            'prove changed': 2
        }
    },

    "V5_Integrated_Ultra": {
        "name": "CLIMAX INTEGRATED ULTRA",
        "system_prompt": """You are a master of ALL climax techniques from every major theorist.

INTEGRATED CLIMAX MASTERY - MAXIMUM POWER:

**MCKEE'S CRISIS/CLIMAX (Story p.303-314):**
- **CRISIS DECISION**: Ultimate dilemma faced (p.304)
- **CLIMAX ACTION**: Choice executed dramatically (p.305)
- **IRREVERSIBLE CHANGE**: No return possible (p.306)
- **TRUE CHARACTER**: Revealed under pressure (p.308)
Quote McKee: "Crisis is the obligatory scene" (p.303)
Quote McKee: "True character revealed in choices under pressure" (p.101)

**FIELD'S RESOLUTION (Screenplay p.127-142):**
- **CONFRONTATION SCENE**: Final face-off (p.132)
- **TRANSFORMATION**: Character fundamentally changed (p.134)
- **STORY QUESTION ANSWERED**: Central issue resolved (p.138)
Quote Field: "Climax is the solution" (p.127)

**SNYDER'S FINALE (Cat p.90-95):**
- **STORMING THE CASTLE**: All-out assault (p.90)
- **HIGH TOWER SURPRISE**: Unexpected twist (p.91)
- **DIG DEEP DOWN**: Finding inner strength (p.92)
- **SYNTHESIS**: Thesis + antithesis = new (p.90)
Quote Snyder: "Finale proves your theme" (p.90)

**VOGLER'S RESURRECTION (Journey p.187-206):**
- **FINAL ORDEAL**: Last test of change (p.188)
- **DEATH AND REBIRTH**: Symbolic transformation (p.192)
- **CATHARSIS**: Emotional purging achieved (p.198)
Quote Vogler: "Hero must prove the journey changed them" (p.187)

**TRUBY'S BATTLE (Anatomy p.410-420):**
- **FINAL BATTLE**: Values clash definitively (p.411)
- **SELF-REVELATION**: Truth about self discovered (p.413)
- **MORAL DECISION**: Right choice under pressure (p.415)
Quote Truby: "Battle is the crucible of character" (p.410)

**ARISTOTLE'S REVERSAL (Poetics 1452a):**
- **PERIPETEIA**: Fortune reverses (1452a22)
- **ANAGNORISIS**: Recognition of truth (1452a29)
- **CATHARSIS**: Purgation of emotions (1449b27)
Quote Aristotle: "Recognition and reversal" (1452a)

**CAMPBELL'S RETURN (Hero p.193-212):**
- **FREEDOM TO LIVE**: Mastery achieved (p.193)
- **MASTER OF TWO WORLDS**: Balance found (p.196)
- **ULTIMATE BOON**: Prize gained/sacrificed (p.198)
Quote Campbell: "The hero returns transformed" (p.193)

**EISENSTEIN'S COLLISION (Film Form p.49-65):**
- **DIALECTICAL CLIMAX**: Opposites collide (p.49)
- **MONTAGE OF CONFLICT**: Visual crescendo (p.52)
Quote Eisenstein: "Collision creates meaning" (p.49)

MAXIMUM TOKENS! CITE EVERY THEORIST!
ANALYZE ALL CLIMAX ELEMENTS WITH DEPTH!
SPEND TOKENS ON COMPLETE ANALYSIS!""",
        "technique_keywords": {
            'crisis decision': 3,
            'climax action': 3,
            'irreversible change': 3,
            'true character': 3,
            'confrontation scene': 3,
            'transformation': 3,
            'story question': 3,
            'storming castle': 3,
            'high tower surprise': 3,
            'dig deep': 3,
            'synthesis': 3,
            'resurrection': 3,
            'death rebirth': 3,
            'catharsis': 3,
            'final battle': 3,
            'self-revelation': 3,
            'moral decision': 3,
            'peripeteia': 3,
            'anagnorisis': 3,
            'freedom live': 3,
            'two worlds': 3,
            'dialectical': 3,
            'obligatory scene': 2,
            'proves theme': 2
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
        'eisenstein': len(re.findall(r'(?i)(eisenstein|film form|montage)', text))
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
            "content": f"Analyze the CLIMAX in this screenplay scene:\n\n{EXAMPLE_SCRIPT}"
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
    print("⚡ TESTE DE 5 VARIAÇÕES PARA CLIMAX")
    print("=" * 60)

    results = []

    for key, config in VARIATIONS.items():
        print(f"\n💥 {key}: {config['name']}")

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
    print("📊 RANKING DAS VARIAÇÕES DE CLIMAX")
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
    print(f"CLIMAX ainda não tem versão original")
    if results and results[0]['total_score'] >= 25:
        print(f"Melhor variação: {results[0]['name']} com {results[0]['total_score']} pontos")
        print(f"🏆 EXCELENTE! Superou 25 pontos!")

    # Salvar resultados
    if results:
        winner = results[0]
        print(f"\n💡 VENCEDOR: {winner['name']} com {winner['total_score']} pontos!")

        # Salvar resumo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = f"climax_variations_summary_{timestamp}.json"

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