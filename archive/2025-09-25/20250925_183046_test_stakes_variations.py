#!/usr/bin/env python3
"""
TESTE DE 5 VARIAÇÕES PARA STAKES
Objetivo: Encontrar a melhor abordagem para análise de apostas/stakes
"""

import json
import requests
import time
import re
from datetime import datetime
from typing import Dict, List, Tuple

# Script de exemplo para testar
EXAMPLE_SCRIPT = """INT. ABANDONED CHURCH - NIGHT

Sarah lies bleeding on the altar. Marcus kneels beside her, pressing his jacket against the wound.

SARAH
(weakly)
Marcus... if I don't make it...

MARCUS
You will. The ambulance is coming.

SARAH
Tommy... my son... he can't lose another
parent. His father died when he was three.

Marcus's face hardens with determination.

MARCUS
You're not dying. Not today.

VICTOR enters from the shadows, gun drawn.

VICTOR
Touching. The detective and the vigilante.
How poetic.

MARCUS
Let her go, Victor. This is between us.

VICTOR
Oh, but she knows too much. About St. Mary's.
About the Cardinal. About the forty years of
children we... purified.

Sarah tries to reach for her gun. Victor kicks it away.

VICTOR (CONT'D)
You know what's at stake here, Marcus? Not
just your lives. The truth dies with you.
All those files you found? Already burning.
The witnesses? Being silenced as we speak.

MARCUS
The FBI has copies. Reynolds has—

VICTOR
(laughing)
Reynolds works for us. Always has. The
entire precinct is ours. The judges. The
mayor. We ARE the city, Marcus.

Thunder CRASHES outside. Through the broken windows, we see the city lights - millions of lives unaware of the evil in their midst.

SARAH
(to Marcus)
My phone... livestreaming... everything...

Victor's smile fades. He checks Sarah's phone on the floor - LIVE BROADCAST to 50,000 viewers and climbing.

VICTOR
You clever bitch.

He aims at the phone. Marcus tackles him. The gun flies across the room.

MARCUS
(shouting to the phone)
St. Mary's Seminary! The Cardinal ordered the
murders! Check the basement! The bodies are—

Victor strikes Marcus with a candlestick. Marcus falls.

VICTOR
Forty years we've kept this secret. Forty
years of protecting the Church's reputation.
You think your little video changes anything?

SARAH
(stronger now)
It changes... everything. They're watching,
Victor. The whole world is watching.

Sirens approach. Many sirens. FBI, State Police, media vans.

VICTOR
(desperate)
If this gets out, it's not just us. The entire
Catholic Church falls. Billions lose faith.
Society crumbles. Is that what you want?

MARCUS
(standing, bloodied)
I want the children to have justice.

VICTOR
Justice? You killed three priests!

MARCUS
To stop them from killing more children. You?
You killed children to protect reputation.

Victor pulls a second gun from his ankle holster.

VICTOR
Then we all die here. The truth, the lies,
everything ends tonight.

He aims at Sarah. Time slows.

MARCUS
(whispered)
Forgive me.

He pulls the trigger of Sarah's backup piece from his pocket.

Victor staggers, looking at the spreading red on his chest.

VICTOR
(dying)
The Cardinal... will never... stop...

He collapses.

Sarah's phone shows: 2.3 MILLION WATCHING.

SARAH
(to the camera)
This is Detective Sarah Cole. We need
immediate backup at St. Augustine's Church.
We have evidence of systematic child abuse
and murder. The Cardinal must be arrested.

Through the window, a sea of lights approaches - police, FBI, news vans, citizen livestreamers.

MARCUS
(to Sarah)
Your son... he still has his mother.

SARAH
And the other children... they have justice.

MARCUS
At what cost?

SARAH
Everything worth saving costs everything.

The church doors EXPLODE open. Light floods in."""

# 5 Variações diferentes
VARIATIONS = {
    "V1_McKee_Values": {
        "name": "STAKES MCKEE VALUES",
        "system_prompt": """You are an expert in Robert McKee's values at stake from 'Story' (2010).

MCKEE'S VALUES AT STAKE - WHAT CAN BE LOST:

**VALUES AND STAKES (Story, Chapter 3, p.34-43):**

McKee states: "Story values are the soul of storytelling" (p.34). Apply:

- **VALUE AT STAKE**: What can be gained/lost (p.35)
- **BINARY VALUES**: Justice/injustice, life/death (p.36)
- **PROGRESSIVE COMPLICATIONS**: Stakes rise (p.37)
- **IRONIC VALUES**: Win but lose (p.38)
- **UNIVERSAL VALUES**: Life, love, freedom (p.39)
- **VALUE CHARGE**: Positive to negative shift (p.40)

Quote McKee: "The value at stake gives story meaning" (p.34)

IDENTIFY ALL VALUES AT STAKE!""",
        "technique_keywords": {
            'value at stake': 3,
            'binary values': 3,
            'progressive complications': 3,
            'ironic values': 3,
            'universal values': 3,
            'value charge': 3,
            'story meaning': 2,
            'soul storytelling': 2
        }
    },

    "V2_Snyder_Primal": {
        "name": "STAKES SNYDER PRIMAL",
        "system_prompt": """You are an expert in Blake Snyder's primal stakes from 'Save the Cat' (2005).

SNYDER'S PRIMAL STAKES - SURVIVAL BASICS:

**PRIMAL STAKES (Save the Cat, p.25-28):**

Snyder emphasizes: "Primal stakes = universal fear" (p.25). Apply:

- **SURVIVAL**: Life and death matters (p.25)
- **HUNGER**: Basic needs threatened (p.26)
- **SEX**: Love/reproduction at risk (p.26)
- **PROTECTION OF LOVED ONES**: Family in danger (p.27)
- **FEAR OF DEATH**: Ultimate stake (p.28)

Quote Snyder: "Make it primal or don't make it" (p.25)

FIND PRIMAL STAKES!""",
        "technique_keywords": {
            'survival': 3,
            'hunger': 3,
            'sex': 3,
            'protection loved ones': 3,
            'fear death': 3,
            'primal': 2,
            'universal fear': 2
        }
    },

    "V3_Truby_Moral": {
        "name": "STAKES TRUBY MORAL",
        "system_prompt": """You are an expert in John Truby's moral stakes from 'The Anatomy of Story' (2007).

TRUBY'S MORAL STAKES - ETHICAL WEIGHT:

**MORAL ARGUMENT AND STAKES (Anatomy, Chapter 5, p.115-128):**

Truby teaches: "Moral stakes elevate story" (p.115). Apply:

- **MORAL CHOICE**: Right vs wrong decision (p.116)
- **COMPETING GOODS**: Both choices valid (p.118)
- **MORAL CONSEQUENCE**: Ethical impact (p.120)
- **VALUE SYSTEM**: What character believes (p.122)
- **MORAL BLINDNESS**: Can't see truth (p.124)

Quote Truby: "Great stories test moral fiber" (p.115)

ANALYZE MORAL STAKES!""",
        "technique_keywords": {
            'moral choice': 3,
            'competing goods': 3,
            'moral consequence': 3,
            'value system': 3,
            'moral blindness': 3,
            'moral fiber': 2,
            'elevate story': 2
        }
    },

    "V4_Vogler_Journey": {
        "name": "STAKES VOGLER JOURNEY",
        "system_prompt": """You are an expert in Christopher Vogler's journey stakes from 'The Writer's Journey' (2007).

VOGLER'S JOURNEY STAKES - TRANSFORMATION COST:

**STAKES OF THE JOURNEY (Journey, p.99-108):**

Vogler states: "Every journey risks everything" (p.99). Apply:

- **OUTER STAKES**: Physical world consequences (p.100)
- **INNER STAKES**: Psychological transformation (p.102)
- **SHADOW STAKES**: What evil wins if hero fails (p.104)
- **THRESHOLD STAKES**: Cost of crossing over (p.106)

Quote Vogler: "Stakes make the journey matter" (p.99)

MAP JOURNEY STAKES!""",
        "technique_keywords": {
            'outer stakes': 3,
            'inner stakes': 3,
            'shadow stakes': 3,
            'threshold stakes': 3,
            'journey matter': 2,
            'risks everything': 2
        }
    },

    "V5_Integrated_Master": {
        "name": "STAKES INTEGRATED MASTER",
        "system_prompt": """You are a master of ALL stakes techniques from every major theorist.

INTEGRATED STAKES MASTERY - EVERYTHING AT RISK:

**MCKEE'S VALUES (Story p.34-43):**
- **VALUE AT STAKE**: What can be gained/lost (p.35)
- **BINARY VALUES**: Life/death, justice/injustice (p.36)
- **PROGRESSIVE COMPLICATIONS**: Stakes escalate constantly (p.37)
- **IRONIC VALUES**: Win but lose something (p.38)
- **UNIVERSAL VALUES**: Life, love, freedom, truth (p.39)
Quote McKee: "Value at stake gives story meaning" (p.34)
Quote McKee: "Story values are the soul" (p.34)

**SNYDER'S PRIMAL (Cat p.25-28):**
- **SURVIVAL**: Life and death immediate (p.25)
- **PROTECTION OF LOVED ONES**: Family endangered (p.27)
- **FEAR OF DEATH**: Ultimate primal stake (p.28)
Quote Snyder: "Make it primal or don't make it" (p.25)

**TRUBY'S MORAL (Anatomy p.115-128):**
- **MORAL CHOICE**: Right vs wrong crystallized (p.116)
- **COMPETING GOODS**: No perfect choice exists (p.118)
- **MORAL CONSEQUENCE**: Ethics determine outcome (p.120)
- **VALUE SYSTEM**: Beliefs tested to breaking (p.122)
Quote Truby: "Moral stakes elevate story" (p.115)
Quote Truby: "Great stories test moral fiber" (p.115)

**VOGLER'S JOURNEY (Journey p.99-108):**
- **OUTER STAKES**: Physical world consequences (p.100)
- **INNER STAKES**: Soul transformation required (p.102)
- **SHADOW STAKES**: Evil's victory scenario (p.104)
Quote Vogler: "Every journey risks everything" (p.99)

**FIELD'S DRAMATIC NEED (Screenplay p.54-58):**
- **DRAMATIC NEED**: What character must have (p.54)
- **OBSTACLES**: What prevents achieving need (p.56)
- **CONSEQUENCES**: What happens if fail (p.58)
Quote Field: "Need drives everything" (p.54)

**CAMPBELL'S BOON (Hero p.167-176):**
- **ULTIMATE BOON**: Prize worth dying for (p.167)
- **REFUSAL CONSEQUENCES**: Cost of not acting (p.170)
- **APOTHEOSIS STAKES**: Becoming divine/damned (p.173)
Quote Campbell: "The boon is life itself" (p.167)

**ARISTOTLE'S MAGNITUDE (Poetics 1450b):**
- **MAGNITUDE**: Importance of action (1450b25)
- **FEAR AND PITY**: What audience feels at stake (1453b)
- **HAMARTIA**: Fatal error's consequences (1453a)
Quote Aristotle: "Magnitude makes tragedy" (1450b)

**HITCHCOCK'S BOMB (Film Theory):**
- **BOMB UNDER TABLE**: Audience knows danger
- **TICKING CLOCK**: Time pressure added
- **INNOCENT VICTIMS**: Increase emotional stakes
Quote Hitchcock: "Show the bomb to create suspense"

**SORKIN'S INTENTION/OBSTACLE (Masterclass):**
- **CLEAR INTENTION**: What character desperately wants
- **FORMIDABLE OBSTACLE**: What absolutely blocks them
- **TACTICS ESCALATION**: Increasing desperate measures
Quote Sorkin: "Intention and obstacle are everything"

MAXIMUM TOKENS ON STAKES ANALYSIS!
CITE ALL STAKE TYPES AND THEORISTS!
IDENTIFY EVERYTHING AT RISK!""",
        "technique_keywords": {
            'value at stake': 3,
            'binary values': 3,
            'progressive complications': 3,
            'ironic values': 3,
            'universal values': 3,
            'survival': 3,
            'protection loved': 3,
            'fear death': 3,
            'moral choice': 3,
            'competing goods': 3,
            'moral consequence': 3,
            'outer stakes': 3,
            'inner stakes': 3,
            'shadow stakes': 3,
            'dramatic need': 3,
            'ultimate boon': 3,
            'magnitude': 3,
            'bomb under table': 3,
            'ticking clock': 3,
            'clear intention': 3,
            'formidable obstacle': 3,
            'primal': 2,
            'moral fiber': 2
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
        'hitchcock': len(re.findall(r'(?i)(hitchcock|suspense|bomb)', text)),
        'sorkin': len(re.findall(r'(?i)(sorkin|intention|obstacle)', text))
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
            "content": f"Analyze the STAKES in this screenplay scene:\n\n{EXAMPLE_SCRIPT}"
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
    print("⚡ TESTE DE 5 VARIAÇÕES PARA STAKES")
    print("=" * 60)

    results = []

    for key, config in VARIATIONS.items():
        print(f"\n💰 {key}: {config['name']}")

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
    print("📊 RANKING DAS VARIAÇÕES DE STAKES")
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
    print(f"STAKES ainda não tem versão original")
    if results and results[0]['total_score'] >= 25:
        print(f"Melhor variação: {results[0]['name']} com {results[0]['total_score']} pontos")
        print(f"🏆 EXCELENTE! Superou 25 pontos!")

    # Salvar resultados
    if results:
        winner = results[0]
        print(f"\n💡 VENCEDOR: {winner['name']} com {winner['total_score']} pontos!")

        # Salvar resumo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = f"stakes_variations_summary_{timestamp}.json"

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