#!/usr/bin/env python3
"""
TESTE DE 5 VARIAÇÕES PARA BACKSTORY
Objetivo: Encontrar a melhor abordagem para análise de backstory/história pregressa
"""

import json
import requests
import time
import re
from datetime import datetime
from typing import Dict, List, Tuple

# Script de exemplo para testar
EXAMPLE_SCRIPT = """INT. ST. MARY'S SEMINARY - DORMITORY - NIGHT (1987)

Young Marcus (10) lies awake in his narrow bed. Moonlight streams through barred windows.

YOUNG MARCUS (V.O.)
My parents sent me here after Dad died.
Mom said the priests would take care of me.
Make me a good man like him.

FOOTSTEPS in the hallway. Marcus pulls covers over his head.

The door creaks open. BROTHER VICTOR (30s) enters with Father Martinez.

BROTHER VICTOR
(whispering)
Marcus Chen. Father Martinez wants to
discuss your progress.

YOUNG MARCUS
It's after lights out, Brother.

FATHER MARTINEZ
Special students have special rules, Marcus.
Your mother mentioned you sing beautifully.

They lead him down the dark corridor.

INT. SEMINARY - "PURIFICATION ROOM" - CONTINUOUS

A small chapel converted to something else. Medical equipment. Recording devices. Other boys' photos on the wall - all marked with dates and coded symbols.

FATHER MARTINEZ
Your father was Chinese, yes? Your mother
Irish Catholic. A unique combination.
The Church needs to understand such...
mixing.

Young Marcus backs toward the door. Brother Victor blocks it.

BROTHER VICTOR
Your mother signed the papers, Marcus.
You belong to St. Mary's now. To us.

YOUNG MARCUS
I want to call my mom.

FATHER MARTINEZ
Your mother thinks you're becoming a
priest. Would you disappoint her? After
your father's death broke her heart?

A SCREAM echoes from somewhere below. Marcus recognizes the voice.

YOUNG MARCUS
Tommy? What did you do to Tommy?

BROTHER VICTOR
Tommy failed his purification. Some boys
aren't strong enough for God's love.

Father Martinez approaches with a syringe.

FATHER MARTINEZ
But you're strong, aren't you, Marcus?
Your father was a soldier. Died in Vietnam
serving his country. You have his strength.

YOUNG MARCUS
(desperate)
He died in a car accident!

FATHER MARTINEZ
(smiling)
That's what your mother told you. But we
know the truth. We know everything about
our special boys.

The needle goes in. Marcus's vision blurs.

CUT TO:

INT. MARCUS'S APARTMENT - NIGHT (PRESENT)

Adult Marcus jolts awake, sweating. He goes to a locked drawer, pulls out military documents: "STAFF SERGEANT JAMES CHEN - KILLED IN ACTION - CLASSIFIED"

His phone shows missed calls from his mother. A voicemail:

MOTHER (V.O.)
Marcus, it's Mom. I know you're angry about
St. Mary's. But you have to understand -
after your father died, I had no choice.
The Church promised to educate you, protect
you. How could I know...

Marcus deletes it mid-message.

He opens another file: "ST. MARY'S SEMINARY - FINANCIAL RECORDS". Large payments from wealthy families after their sons' "accidents" or "suicides."

A newspaper clipping: "PROSECUTOR DROPS CHARGES AGAINST SEMINARY - LACK OF EVIDENCE"

The prosecutor's name: HAROLD REYNOLDS. Now Captain Reynolds.

Another document: "PSYCHOLOGICAL EVALUATION - MARCUS CHEN, AGE 10"
"Subject shows signs of severe trauma. Recommends immediate removal from Seminary environment. - Dr. Sarah Morrison"

A note scrawled at bottom: "Report suppressed by order of Cardinal Bishop."

Marcus finds a photo - seven boys at St. Mary's. He's circled three faces:
- TOMMY WRIGHT (Died 1987 - "Suicide")
- MICHAEL TORRES (Died 1988 - "Accident")
- JAMES O'SULLIVAN (Died 1989 - "Overdose")

Next to each name, he's written what really happened:
- "Beaten to death for refusing"
- "Pushed from bell tower for threatening to tell"
- "Force-fed pills when parents asked questions"

At the bottom of the box: Marcus's childhood journal. He opens it:

YOUNG MARCUS'S WRITING: "Father O'Brien is different. He tries to protect us. He said he's collecting evidence. Said he'll stop them. I believe him."

Next entry, different pen: "Father O'Brien is gone. Transferred. They said he had inappropriate feelings. But I know the truth. He was going to expose them."

Final entry: "I will survive this. I will remember everything. And one day, when I'm strong enough, I'll come back for them."

Adult Marcus closes the journal.

MARCUS
(to the photo)
I kept my promise, boys. They're paying
for what they did to us. To all of us."""

# 5 Variações diferentes
VARIATIONS = {
    "V1_Truby_Ghost": {
        "name": "BACKSTORY TRUBY GHOST",
        "system_prompt": """You are an expert in John Truby's ghost concept from 'The Anatomy of Story' (2007).

TRUBY'S GHOST - PAST HAUNTING PRESENT:

**GHOST AND BACKSTORY (Anatomy, Chapter 4, p.78-87):**

Truby states: "The ghost is the past event still haunting the character" (p.78). Apply:

- **GHOST EVENT**: Specific trauma from past (p.79)
- **WOUND**: Psychological damage done (p.80)
- **FEAR**: What character now avoids (p.81)
- **NEED CREATED**: What must overcome (p.82)
- **FALSE BELIEF**: Wrong lesson learned (p.83)
- **BACKSTORY REVEAL**: Strategic disclosure (p.84)

Quote Truby: "Ghost drives all character action" (p.78)

IDENTIFY THE GHOST!""",
        "technique_keywords": {
            'ghost event': 3,
            'wound': 3,
            'fear': 3,
            'need created': 3,
            'false belief': 3,
            'backstory reveal': 3,
            'haunting': 2,
            'drives action': 2
        }
    },

    "V2_McKee_Backstory": {
        "name": "BACKSTORY MCKEE EXPOSITION",
        "system_prompt": """You are an expert in Robert McKee's backstory principles from 'Story' (2010).

MCKEE'S BACKSTORY AS AMMUNITION:

**BACKSTORY AND EXPOSITION (Story, Chapter 15, p.334-344):**

McKee teaches: "Backstory is best when it's ammunition" (p.334). Apply:

- **PROGRESSIVE REVELATION**: Layer backstory gradually (p.335)
- **DRAMATIZE BACKSTORY**: Show through conflict (p.336)
- **WITHHOLD AND REVEAL**: Strategic timing (p.337)
- **FLASHBACK NECESSITY**: Only when essential (p.338)
- **EMOTIONAL LOGIC**: Past explains present (p.339)

Quote McKee: "Never include backstory unless critical" (p.334)

ANALYZE BACKSTORY DEPLOYMENT!""",
        "technique_keywords": {
            'progressive revelation': 3,
            'dramatize backstory': 3,
            'withhold reveal': 3,
            'flashback necessity': 3,
            'emotional logic': 3,
            'ammunition': 2,
            'critical': 2
        }
    },

    "V3_Vogler_Wound": {
        "name": "BACKSTORY VOGLER WOUND",
        "system_prompt": """You are an expert in Christopher Vogler's backstory wounds from 'The Writer's Journey' (2007).

VOGLER'S BACKSTORY WOUNDS - PAST SHAPES JOURNEY:

**BACKSTORY AND WOUNDS (Journey, p.89-98):**

Vogler states: "Every hero has an inner wound" (p.89). Apply:

- **INNER WOUND**: Past trauma driving present (p.90)
- **OUTER WOUND**: Physical/visible scar (p.91)
- **WOUND AS MOTIVATION**: Pain drives action (p.92)
- **HEALING JOURNEY**: Story heals wound (p.93)
- **REFUSAL REASON**: Wound causes fear (p.94)

Quote Vogler: "The wound is the hero's humanity" (p.89)

MAP THE WOUND!""",
        "technique_keywords": {
            'inner wound': 3,
            'outer wound': 3,
            'wound motivation': 3,
            'healing journey': 3,
            'refusal reason': 3,
            'humanity': 2,
            'past trauma': 2
        }
    },

    "V4_Field_Setup": {
        "name": "BACKSTORY FIELD SETUP",
        "system_prompt": """You are an expert in Syd Field's setup and backstory from 'Screenplay' (2005).

FIELD'S BACKSTORY SETUP:

**SETUP AND BACKSTORY (Screenplay, p.88-95):**

Field emphasizes: "Setup is backstory in action" (p.88). Apply:

- **CHARACTER BIOGRAPHY**: Life before page one (p.89)
- **DEFINING INCIDENT**: Event that changed everything (p.90)
- **SETUP PAYOFF**: Plant backstory early (p.91)
- **CONTEXT CREATION**: Past explains actions (p.92)
- **EMOTIONAL HISTORY**: Relationships before story (p.93)

Quote Field: "Know your character's life before FADE IN" (p.88)

SETUP THE BACKSTORY!""",
        "technique_keywords": {
            'character biography': 3,
            'defining incident': 3,
            'setup payoff': 3,
            'context creation': 3,
            'emotional history': 3,
            'before fade in': 2,
            'life before': 2
        }
    },

    "V5_Integrated_Master": {
        "name": "BACKSTORY INTEGRATED MASTER",
        "system_prompt": """You are a master of ALL backstory techniques from every major theorist.

INTEGRATED BACKSTORY MASTERY - COMPLETE PAST ANALYSIS:

**TRUBY'S GHOST (Anatomy p.78-87):**
- **GHOST EVENT**: Specific past trauma haunting (p.79)
- **WOUND**: Deep psychological damage (p.80)
- **FEAR CREATED**: What character avoids (p.81)
- **FALSE BELIEF**: Wrong lesson from trauma (p.83)
- **NEED FROM GHOST**: What must overcome (p.82)
Quote Truby: "Ghost drives all action" (p.78)
Quote Truby: "Character is walking ghost" (p.79)

**MCKEE'S AMMUNITION (Story p.334-344):**
- **PROGRESSIVE REVELATION**: Layer gradually (p.335)
- **DRAMATIZE BACKSTORY**: Show in conflict (p.336)
- **WITHHOLD AND REVEAL**: Strategic timing (p.337)
- **EMOTIONAL LOGIC**: Past explains present (p.339)
Quote McKee: "Backstory is ammunition" (p.334)
Quote McKee: "Never include unless critical" (p.334)

**VOGLER'S WOUNDS (Journey p.89-98):**
- **INNER WOUND**: Emotional trauma driving (p.90)
- **OUTER WOUND**: Physical manifestation (p.91)
- **WOUND AS MOTIVATION**: Pain propels journey (p.92)
- **HEALING ARC**: Story heals wound (p.93)
Quote Vogler: "Wound is hero's humanity" (p.89)

**FIELD'S SETUP (Screenplay p.88-95):**
- **CHARACTER BIOGRAPHY**: Complete life before (p.89)
- **DEFINING INCIDENT**: Changed everything (p.90)
- **EMOTIONAL HISTORY**: Past relationships (p.93)
Quote Field: "Know life before FADE IN" (p.88)

**CAMPBELL'S PAST (Hero p.77-89):**
- **SUPERNATURAL AID**: Past helpers return (p.77)
- **THRESHOLD GUARDIANS**: Past creates barriers (p.78)
- **BELLY OF WHALE**: Past swallows hero (p.83)
Quote Campbell: "Past is prologue to journey" (p.77)

**FREUD'S REPRESSION (Psychoanalysis):**
- **REPRESSED MEMORIES**: Hidden trauma
- **RETURN OF REPRESSED**: Past erupts
- **SCREEN MEMORIES**: False/distorted past
- **PRIMAL SCENE**: Original trauma
Quote: "The repressed always returns"

**STANISLAVSKI'S GIVEN CIRCUMSTANCES:**
- **PREVIOUS ACTION**: What happened before
- **EMOTIONAL MEMORY**: Past feelings persist
- **THROUGH-LINE**: Past connects to present
Quote: "The past is present on stage"

**ARISTOTLE'S PREVIOUS ACTION (Poetics):**
- **ANTECEDENT ACTION**: Before play begins
- **RECOGNITION**: Discovery of past truth (1452a)
Quote Aristotle: "Beginning presupposes before" (1450b)

**HITCHCOCK'S MACGUFFIN (Film Theory):**
- **PAST SECRET**: Hidden information drives plot
- **BURIED TRUTH**: What everyone seeks
Quote Hitchcock: "The past is the real story"

**SORKIN'S FLASHBACK (Masterclass):**
- **FLASHBACK RULE**: Only if changes everything
- **REVELATION TIMING**: Maximum impact moment
Quote Sorkin: "Backstory is present story"

MAXIMUM TOKENS ON BACKSTORY!
ANALYZE EVERY PAST ELEMENT!
COMPLETE GHOST ARCHAEOLOGY!""",
        "technique_keywords": {
            'ghost event': 3,
            'wound': 3,
            'inner wound': 3,
            'outer wound': 3,
            'fear created': 3,
            'false belief': 3,
            'need from ghost': 3,
            'progressive revelation': 3,
            'dramatize backstory': 3,
            'withhold reveal': 3,
            'emotional logic': 3,
            'character biography': 3,
            'defining incident': 3,
            'emotional history': 3,
            'supernatural aid': 3,
            'threshold guardians': 3,
            'repressed memories': 3,
            'return repressed': 3,
            'primal scene': 3,
            'given circumstances': 3,
            'emotional memory': 3,
            'antecedent action': 3,
            'past secret': 3,
            'flashback rule': 3,
            'ammunition': 2,
            'haunting': 2
        }
    }
}

def count_theory_citations(text: str) -> Dict[str, int]:
    """Conta citações de teóricos com mais flexibilidade."""
    citations = {
        'mckee': len(re.findall(r'(?i)(mckee|story[,\s]+(?:p\.?|page))', text)),
        'truby': len(re.findall(r'(?i)(truby|anatomy)', text)),
        'field': len(re.findall(r'(?i)(field|screenplay[,\s]+(?:p\.?|page))', text)),
        'vogler': len(re.findall(r"(?i)(vogler|writer'?s? journey|journey[,\s]+(?:p\.?|page))", text)),
        'campbell': len(re.findall(r'(?i)(campbell|hero with|thousand faces)', text)),
        'freud': len(re.findall(r'(?i)(freud|repressed|psychoanalysis)', text)),
        'stanislavski': len(re.findall(r'(?i)(stanislavski|given circumstances|actor)', text)),
        'aristotle': len(re.findall(r'(?i)(aristotle|poetics)', text)),
        'hitchcock': len(re.findall(r'(?i)(hitchcock|macguffin)', text)),
        'sorkin': len(re.findall(r'(?i)(sorkin|flashback rule)', text))
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
            "content": f"Analyze the BACKSTORY in this screenplay excerpt:\n\n{EXAMPLE_SCRIPT}"
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
    print("⚡ TESTE DE 5 VARIAÇÕES PARA BACKSTORY")
    print("=" * 60)

    results = []

    for key, config in VARIATIONS.items():
        print(f"\n📜 {key}: {config['name']}")

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
    print("📊 RANKING DAS VARIAÇÕES DE BACKSTORY")
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
    print(f"BACKSTORY ainda não tem versão original")
    if results and results[0]['total_score'] >= 25:
        print(f"Melhor variação: {results[0]['name']} com {results[0]['total_score']} pontos")
        print(f"🏆 EXCELENTE! Superou 25 pontos!")

    # Salvar resultados
    if results:
        winner = results[0]
        print(f"\n💡 VENCEDOR: {winner['name']} com {winner['total_score']} pontos!")

        # Salvar resumo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = f"backstory_variations_summary_{timestamp}.json"

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