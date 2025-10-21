#!/usr/bin/env python3
"""
TESTE DE 5 VARIAÇÕES PARA MOTIVATION
Objetivo: Encontrar a melhor abordagem para análise de motivação
"""

import json
import requests
import time
import re
from datetime import datetime
from typing import Dict, List, Tuple

# Script de exemplo para testar
EXAMPLE_SCRIPT = """INT. MARCUS'S APARTMENT - NIGHT (FLASHBACK - 10 YEARS AGO)

Marcus stares at a wall covered with newspaper clippings: "SEMINARY SCANDAL BURIED", "WHISTLEBLOWER PRIEST FOUND DEAD", "CHURCH DENIES ALLEGATIONS".

His phone rings. He doesn't answer. It rings again.

VOICE MESSAGE
(Father O'Brien)
Marcus, it's Father O'Brien. I know you
blame yourself for what happened at St. Mary's.
But you were just a child. The men who hurt
you... they're still out there. Still hurting
others. Someone needs to stop them.

Marcus picks up a photo - himself at 10, in choir robes, surrounded by priests. His younger self smiles. Innocent. Unaware.

He traces his finger over Father Martinez in the photo.

MARCUS
(to photo)
You said you'd protect us.

Another photo: Seven boys in seminary uniforms. Marcus circles three faces in red - all dead now. Suicides, they said.

MARCUS (CONT'D)
Tommy. Michael. James. I couldn't save you.
But maybe... maybe I can save the others.

He opens a drawer. Inside: detailed files on every priest from St. Mary's. Their current locations. Their new parishes. Their new victims.

A newspaper headline: "FATHER MARTINEZ RECEIVES HUMANITARIAN AWARD".

Marcus crumples it.

INT. MARCUS'S APARTMENT - LATER

Marcus sits at his computer. Types: "How to make someone confess their sins."

Search results flood the screen. He clicks on one: "The Psychology of Guilt."

His phone rings. SARAH'S NAME appears.

MARCUS
(answering)
Yeah?

SARAH (V.O.)
Marcus, where have you been? The department's
been looking for you. Your leave ended a week ago.

MARCUS
I'm not coming back.

SARAH (V.O.)
What? Marcus, you're the best detective we have.
Whatever you're going through—

MARCUS
Sarah, what would you do if you knew who
killed those boys but couldn't prove it?

SARAH (V.O.)
I'd find a way to prove it. Legally.

MARCUS
And if the system protects them?

SARAH (V.O.)
Then you work harder. You don't give up.

MARCUS
What if the system IS them?

Long pause.

SARAH (V.O.)
Marcus... what are you planning?

MARCUS
Justice. The kind that doesn't wait forty
years.

SARAH (V.O.)
Don't do anything stupid. Let me help you.

MARCUS
You can't help. You're part of the system too.

He hangs up.

INT. MARCUS'S APARTMENT - BATHROOM - NIGHT

Marcus stares at himself in the mirror. Dark circles. Haunted eyes.

MARCUS
(to his reflection)
They made me a victim. Then a survivor.
Now... now I choose what I become.

He opens the medicine cabinet. Moves aside prescription bottles - Ambien, Xanax, Prozac. Behind them: a gun.

MARCUS (CONT'D)
Father Martinez first. He was the leader.
The one who chose which boys were... ready.

He loads the gun.

MARCUS (CONT'D)
Not murder. Prevention. Stop them before
they create more victims. More like me.

A photo taped to the mirror: Young Marcus with his parents. Before St. Mary's. Before everything changed.

YOUNG MARCUS (V.O.)
(memory)
Mom, why do people hurt children?

MOTHER (V.O.)
(memory)
They don't, sweetheart. Good people protect
children. Always.

Marcus PUNCHES the mirror. It shatters. His hand bleeds.

MARCUS
You were wrong, Mom. Good people fail.
Good people look away. Good people die
while evil thrives.

He wraps his bleeding hand.

MARCUS (CONT'D)
But I'm not good anymore. I'm necessary."""

# 5 Variações diferentes
VARIATIONS = {
    "V1_Truby_Desire": {
        "name": "MOTIVATION TRUBY DESIRE",
        "system_prompt": """You are an expert in John Truby's desire line from 'The Anatomy of Story' (2007).

TRUBY'S DESIRE LINE - CHARACTER DRIVE:

**DESIRE AND MOTIVATION (Anatomy, Chapter 3, p.41-55):**

Truby states: "Desire is the story's spine" (p.41). Apply:

- **DESIRE LINE**: What character wants overall (p.42)
- **NEED VS WANT**: Internal vs external goals (p.43)
- **PSYCHOLOGICAL NEED**: Deep character flaw (p.44)
- **MORAL NEED**: How character hurts others (p.45)
- **OBSESSION**: When desire becomes destructive (p.47)
- **SPINE OF ACTION**: Desire drives all acts (p.48)

Quote Truby: "Desire creates story movement" (p.41)

TRACE THE DESIRE LINE!""",
        "technique_keywords": {
            'desire line': 3,
            'need vs want': 3,
            'psychological need': 3,
            'moral need': 3,
            'obsession': 3,
            'spine action': 3,
            'story movement': 2,
            'story spine': 2
        }
    },

    "V2_McKee_Want": {
        "name": "MOTIVATION MCKEE WANT",
        "system_prompt": """You are an expert in Robert McKee's conscious and unconscious desire from 'Story' (2010).

MCKEE'S DESIRE DYNAMICS - CONSCIOUS/UNCONSCIOUS:

**DESIRE AND MOTIVATION (Story, Chapter 7, p.136-147):**

McKee teaches: "Character is desire" (p.136). Apply:

- **CONSCIOUS DESIRE**: What character thinks they want (p.137)
- **UNCONSCIOUS DESIRE**: What they really need (p.138)
- **CONTRADICTORY DESIRES**: Inner conflict source (p.139)
- **OBJECT OF DESIRE**: Specific goal sought (p.140)
- **SPINE OF ACTION**: Through-line of pursuit (p.141)

Quote McKee: "True character is revealed in choices under pressure" (p.101)

IDENTIFY CONSCIOUS AND UNCONSCIOUS!""",
        "technique_keywords": {
            'conscious desire': 3,
            'unconscious desire': 3,
            'contradictory desires': 3,
            'object desire': 3,
            'spine action': 3,
            'character desire': 2,
            'choices pressure': 2
        }
    },

    "V3_Field_Need": {
        "name": "MOTIVATION FIELD NEED",
        "system_prompt": """You are an expert in Syd Field's dramatic need from 'Screenplay' (2005).

FIELD'S DRAMATIC NEED - DRIVING FORCE:

**DRAMATIC NEED (Screenplay, Chapter 3, p.39-48):**

Field emphasizes: "Need drives the story forward" (p.39). Apply:

- **DRAMATIC NEED**: What character must have (p.40)
- **PROFESSIONAL GOAL**: Career objective (p.41)
- **PERSONAL GOAL**: Emotional objective (p.42)
- **OBSTACLES**: What blocks the need (p.43)
- **STAKES**: What happens if fail (p.44)

Quote Field: "Define need, create story" (p.39)

DEFINE THE DRAMATIC NEED!""",
        "technique_keywords": {
            'dramatic need': 3,
            'professional goal': 3,
            'personal goal': 3,
            'obstacles': 3,
            'stakes': 3,
            'drives forward': 2,
            'define need': 2
        }
    },

    "V4_Stanislavski_Objective": {
        "name": "MOTIVATION STANISLAVSKI OBJECTIVE",
        "system_prompt": """You are an expert in Constantin Stanislavski's objectives and super-objectives from 'An Actor Prepares' (1936).

STANISLAVSKI'S OBJECTIVES - ACTOR'S METHOD:

**OBJECTIVES AND SUPER-OBJECTIVE (An Actor Prepares):**

Stanislavski teaches: "Every action has objective". Apply:

- **OBJECTIVE**: What character wants in scene
- **SUPER-OBJECTIVE**: Life goal throughout story
- **GIVEN CIRCUMSTANCES**: Context driving choices
- **MAGIC IF**: What would I do if...
- **SUBTEXT**: Hidden motivations beneath

Quote: "Create continuous line of objectives"

MAP OBJECTIVES!""",
        "technique_keywords": {
            'objective': 3,
            'super-objective': 3,
            'given circumstances': 3,
            'magic if': 3,
            'subtext': 3,
            'continuous line': 2
        }
    },

    "V5_Integrated_Master": {
        "name": "MOTIVATION INTEGRATED MASTER",
        "system_prompt": """You are a master of ALL motivation techniques from every major theorist.

INTEGRATED MOTIVATION MASTERY - COMPLETE DRIVE ANALYSIS:

**TRUBY'S DESIRE (Anatomy p.41-55):**
- **DESIRE LINE**: What character wants throughout (p.42)
- **NEED VS WANT**: Internal healing vs external goal (p.43)
- **PSYCHOLOGICAL NEED**: Deep flaw must fix (p.44)
- **MORAL NEED**: How hurting others (p.45)
- **OBSESSION**: Desire becomes destructive (p.47)
Quote Truby: "Desire is story's spine" (p.41)
Quote Truby: "Need makes character change" (p.43)

**MCKEE'S CONSCIOUS/UNCONSCIOUS (Story p.136-147):**
- **CONSCIOUS DESIRE**: What thinks wants (p.137)
- **UNCONSCIOUS DESIRE**: What really needs (p.138)
- **CONTRADICTORY DESIRES**: Inner war (p.139)
- **OBJECT OF DESIRE**: Specific goal (p.140)
Quote McKee: "Character is desire" (p.136)
Quote McKee: "Gap between expectation and result" (p.142)

**FIELD'S DRAMATIC NEED (Screenplay p.39-48):**
- **DRAMATIC NEED**: Must achieve goal (p.40)
- **PROFESSIONAL GOAL**: External achievement (p.41)
- **PERSONAL GOAL**: Emotional fulfillment (p.42)
Quote Field: "Need drives story forward" (p.39)

**STANISLAVSKI'S OBJECTIVES (Actor Prepares 1936):**
- **SCENE OBJECTIVE**: Immediate want
- **SUPER-OBJECTIVE**: Life's through-line
- **GIVEN CIRCUMSTANCES**: Context shapes motive
- **MAGIC IF**: Imagined motivation
Quote: "In every physical action, inner motive"

**VOGLER'S INNER/OUTER (Journey p.71-80):**
- **OUTER MOTIVATION**: Physical goal (p.72)
- **INNER MOTIVATION**: Emotional need (p.73)
- **WOUND DRIVING**: Past trauma motivates (p.75)
Quote Vogler: "All stories are journeys" (p.71)

**CAMPBELL'S CALL (Hero p.49-58):**
- **CALL TO ADVENTURE**: Initial motivation (p.49)
- **REFUSAL OF CALL**: Fear resists (p.54)
- **SUPERNATURAL AID**: Motivation reinforced (p.57)
Quote Campbell: "The call rings up the curtain" (p.49)

**MASLOW'S HIERARCHY (Psychology):**
- **SURVIVAL**: Basic needs drive
- **SAFETY**: Security motivates
- **LOVE/BELONGING**: Connection need
- **ESTEEM**: Recognition desire
- **SELF-ACTUALIZATION**: Becoming whole
Quote: "Unfulfilled needs motivate behavior"

**FREUD'S DRIVES (Psychoanalysis):**
- **ID**: Primal desires unleashed
- **EGO**: Rational goals
- **SUPEREGO**: Moral imperatives
- **REPRESSION**: Hidden motivations
Quote: "Unconscious drives conscious acts"

**LAJOS EGRI'S PREMISE (Art of Dramatic Writing):**
- **DRIVING FORCE**: Character's ruling passion
- **UNITY OF OPPOSITES**: Conflicting motivations
- **GROWTH THROUGH CONFLICT**: Motivation evolves
Quote Egri: "Character is contradiction" (p.95)

MAXIMUM TOKENS! CITE ALL MOTIVATIONS!
ANALYZE EVERY DRIVE AND DESIRE!
COMPLETE PSYCHOLOGICAL PROFILE!""",
        "technique_keywords": {
            'desire line': 3,
            'need vs want': 3,
            'psychological need': 3,
            'moral need': 3,
            'obsession': 3,
            'conscious desire': 3,
            'unconscious desire': 3,
            'contradictory desires': 3,
            'dramatic need': 3,
            'professional goal': 3,
            'personal goal': 3,
            'scene objective': 3,
            'super-objective': 3,
            'given circumstances': 3,
            'magic if': 3,
            'outer motivation': 3,
            'inner motivation': 3,
            'wound driving': 3,
            'call adventure': 3,
            'survival': 3,
            'self-actualization': 3,
            'id ego superego': 3,
            'driving force': 3,
            'ruling passion': 2
        }
    }
}

def count_theory_citations(text: str) -> Dict[str, int]:
    """Conta citações de teóricos com mais flexibilidade."""
    citations = {
        'mckee': len(re.findall(r'(?i)(mckee|story[,\s]+(?:p\.?|page))', text)),
        'truby': len(re.findall(r'(?i)(truby|anatomy)', text)),
        'field': len(re.findall(r'(?i)(field|screenplay[,\s]+(?:p\.?|page))', text)),
        'stanislavski': len(re.findall(r'(?i)(stanislavski|actor prepares|objectives)', text)),
        'vogler': len(re.findall(r"(?i)(vogler|writer'?s? journey|journey[,\s]+(?:p\.?|page))", text)),
        'campbell': len(re.findall(r'(?i)(campbell|hero with|thousand faces)', text)),
        'maslow': len(re.findall(r'(?i)(maslow|hierarchy)', text)),
        'freud': len(re.findall(r'(?i)(freud|psychoanalysis|id ego)', text)),
        'egri': len(re.findall(r'(?i)(egri|dramatic writing|ruling passion)', text))
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
            "content": f"Analyze the MOTIVATION in this screenplay scene:\n\n{EXAMPLE_SCRIPT}"
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
    print("⚡ TESTE DE 5 VARIAÇÕES PARA MOTIVATION")
    print("=" * 60)

    results = []

    for key, config in VARIATIONS.items():
        print(f"\n🎯 {key}: {config['name']}")

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
    print("📊 RANKING DAS VARIAÇÕES DE MOTIVATION")
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
    print(f"MOTIVATION ainda não tem versão original")
    if results and results[0]['total_score'] >= 25:
        print(f"Melhor variação: {results[0]['name']} com {results[0]['total_score']} pontos")
        print(f"🏆 EXCELENTE! Superou 25 pontos!")

    # Salvar resultados
    if results:
        winner = results[0]
        print(f"\n💡 VENCEDOR: {winner['name']} com {winner['total_score']} pontos!")

        # Salvar resumo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = f"motivation_variations_summary_{timestamp}.json"

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