#!/usr/bin/env python3
"""
TESTE DE 5 VARIAÇÕES PARA WORLD-BUILDING
Objetivo: Encontrar a melhor abordagem para análise de construção de mundo
"""

import json
import requests
import time
import re
from datetime import datetime
from typing import Dict, List, Tuple

# Script de exemplo para testar
EXAMPLE_SCRIPT = """INT. ST. MARY'S SEMINARY - BASEMENT - NIGHT (1987)

A labyrinth of stone corridors lit by flickering candles. Religious artifacts line the walls - crucifixes, paintings of saints, holy water fonts. But something's wrong. The paintings' eyes seem to follow movement. The holy water is frozen despite the warmth.

Young Marcus (10) creeps through shadows, his Catholic school uniform torn and dirty.

Behind him, FOOTSTEPS echo on stone. Multiple sets. Getting closer.

BROTHER VICTOR (O.S.)
(singing, distorted)
"Kyrie eleison... The lamb has strayed
from the flock..."

Marcus reaches a heavy wooden door marked "CONFESSIONAL". He pushes - locked. The Latin inscription above reads: "PECCATA PATRIS" - Sins of the Father.

INT. SEMINARY CHAPEL - CONTINUOUS

Marcus bursts in. Massive stained glass windows depict not traditional scenes, but twisted versions - saints with black eyes, angels with broken wings.

The altar is wrong. Where the cross should stand, there's an empty frame. Dried blood stains the white cloth.

FIVE ROBED FIGURES enter, faces hidden. They move in unison, like a single organism.

BROTHER VICTOR
(removing hood, scarred face)
This is sacred ground, Marcus. Here, we
cleanse the unworthy. Make them pure.

The other figures reveal themselves - all priests, all with the same dead eyes.

FATHER MARTINEZ
The Seminary has stood for 150 years.
It has its own rules. Its own justice.

They form a circle. Marcus backs against the altar.

MARCUS
Father O'Brien said you'd protect us!

BROTHER VICTOR
Father O'Brien is learning the price of
defiance in the correction room. As will you.

The candles suddenly extinguish. In the darkness, we hear:
- A child's scream
- Glass shattering
- Running footsteps
- A door slamming

INT. SEMINARY LIBRARY - CONTINUOUS

Marcus crashes through rows of ancient books. Leather-bound volumes of church law, theological treaties in Latin. One shelf is different - hidden behind a false panel - containing files marked with children's names and dates going back decades.

He grabs a file marked "1947-1952: The Purification Protocols" just as the door splinters open.

EXT. SEMINARY GROUNDS - NIGHT

Marcus runs through a cemetery behind the seminary. Hundreds of small, unmarked graves. A statue of St. Mary weeps what looks like blood in the moonlight.

The building looms behind - Gothic architecture, gargoyles perched on corners, windows that look like watching eyes. This isn't just a seminary. It's a fortress. A prison. A kingdom unto itself.

BROTHER VICTOR (O.S.)
You can't escape St. Mary's, Marcus. No one
ever has. The walls remember. The stones
keep secrets. And we... we are eternal.

Marcus reaches the outer wall - 15 feet high, topped with iron spikes. Beyond it, the normal world continues, unaware. Cars pass. People live their lives. But inside St. Mary's, different laws apply.

He turns back. The five figures stand watching, not pursuing. They know something he doesn't.

BROTHER VICTOR
(calling out)
Where will you go? Who will believe you?
We ARE the Church here. We ARE the law.
We ARE God's voice.

Thunder rolls. Rain begins to fall, washing over the unmarked graves."""

# 5 Variações diferentes
VARIATIONS = {
    "V1_Truby_Arena": {
        "name": "WORLD-BUILDING TRUBY ARENA",
        "system_prompt": """You are an expert in John Truby's story world and arena from 'The Anatomy of Story' (2007).

TRUBY'S STORY WORLD - ARENA AS CHARACTER:

**STORY WORLD AND ARENA (Anatomy, Chapter 6, p.145-170):**

Truby states: "The world is the hero's physical expression" (p.145). Apply:

- **ARENA**: Confined space intensifies conflict (p.146)
- **VISUAL OPPOSITIONS**: Contrasting spaces show values (p.148)
- **SYMBOLIC LANDSCAPE**: Setting expresses theme (p.150)
- **SOCIETY MICROCOSM**: World represents larger forces (p.152)
- **PASSAGEWAYS**: Transitions between worlds (p.154)
- **NATURAL VS CIVILIZED**: Primal vs ordered (p.156)

Quote Truby: "Great worlds are characters themselves" (p.145)

ANALYZE WORLD AS CHARACTER!""",
        "technique_keywords": {
            'arena': 3,
            'visual oppositions': 3,
            'symbolic landscape': 3,
            'society microcosm': 3,
            'passageways': 3,
            'natural civilized': 3,
            'world character': 2,
            'physical expression': 2
        }
    },

    "V2_McKee_Setting": {
        "name": "WORLD-BUILDING MCKEE SETTING",
        "system_prompt": """You are an expert in Robert McKee's setting and story world from 'Story' (2010).

MCKEE'S SETTING AS STORY - WORLD CREATES POSSIBILITY:

**SETTING AND STORY WORLD (Story, Chapter 4, p.67-81):**

McKee teaches: "Setting is story's necessary limitation" (p.67). Apply:

- **PHYSICAL LAWS**: Rules of the world (p.68)
- **SOCIAL LAWS**: Cultural constraints (p.70)
- **PERIOD AUTHENTICITY**: Time-specific details (p.72)
- **LOCATION SPECIFICITY**: Unique place qualities (p.74)
- **CREATIVE LIMITATIONS**: Constraints breed creativity (p.76)
- **WORLD CONSISTENCY**: Internal logic maintained (p.78)

Quote McKee: "The world of the story defines possibility" (p.67)

NAME SETTING PRINCIPLES!""",
        "technique_keywords": {
            'physical laws': 3,
            'social laws': 3,
            'period authenticity': 3,
            'location specificity': 3,
            'creative limitations': 3,
            'world consistency': 3,
            'defines possibility': 2,
            'necessary limitation': 2
        }
    },

    "V3_Cameron_Immersion": {
        "name": "WORLD-BUILDING CAMERON IMMERSION",
        "system_prompt": """You are an expert in James Cameron's immersive world-building from his filmmaking approach.

CAMERON'S IMMERSIVE WORLDS - TOTAL ENVIRONMENT:

**CAMERON'S WORLD PRINCIPLES (Avatar/Aliens/Titanic):**

Cameron's approach: "Every detail must feel lived-in and real". Apply:

- **CULTURAL ANTHROPOLOGY**: Complete societies created
- **TECHNOLOGICAL ECOSYSTEM**: How technology shapes life
- **ENVIRONMENTAL STORYTELLING**: World tells its own story
- **HISTORICAL DEPTH**: Sense of deep past
- **SENSORY IMMERSION**: All five senses engaged
- **DOCUMENTARY DETAIL**: Researched authenticity

Quote Cameron: "The world must exist beyond the frame"

BUILD IMMERSIVE WORLDS!""",
        "technique_keywords": {
            'cultural anthropology': 3,
            'technological ecosystem': 3,
            'environmental storytelling': 3,
            'historical depth': 3,
            'sensory immersion': 3,
            'documentary detail': 3,
            'beyond frame': 2,
            'lived-in real': 2
        }
    },

    "V4_Tolkien_Secondary": {
        "name": "WORLD-BUILDING TOLKIEN SECONDARY",
        "system_prompt": """You are an expert in J.R.R. Tolkien's secondary world creation from 'On Fairy-Stories' (1947).

TOLKIEN'S SECONDARY WORLD - INTERNAL CONSISTENCY:

**SECONDARY WORLD CREATION (On Fairy-Stories):**

Tolkien states: "Secondary belief requires internal consistency". Apply:

- **SECONDARY BELIEF**: World must be believable internally
- **INNER CONSISTENCY**: All elements interconnect logically
- **MYTHOLOGICAL DEPTH**: Deep history and legends
- **LINGUISTIC FOUNDATION**: Language shapes culture
- **GEOGRAPHIC REALITY**: Maps and distances matter
- **SUBCREATION**: Complete world independent of ours

Quote Tolkien: "The moment disbelief arises, the spell is broken"

CREATE SECONDARY WORLDS!""",
        "technique_keywords": {
            'secondary belief': 3,
            'inner consistency': 3,
            'mythological depth': 3,
            'linguistic foundation': 3,
            'geographic reality': 3,
            'subcreation': 3,
            'spell broken': 2,
            'believable internally': 2
        }
    },

    "V5_Integrated_Master": {
        "name": "WORLD-BUILDING INTEGRATED MASTER",
        "system_prompt": """You are a master of ALL world-building techniques from every major theorist.

INTEGRATED WORLD-BUILDING MASTERY - COMPLETE UNIVERSES:

**TRUBY'S ARENA (Anatomy p.145-170):**
- **ARENA PRINCIPLE**: Confined space intensifies drama (p.146)
- **VISUAL OPPOSITIONS**: Contrasting spaces = values (p.148)
- **SYMBOLIC LANDSCAPE**: Setting expresses theme (p.150)
- **PASSAGEWAYS**: Transitions between worlds (p.154)
Quote Truby: "The world is the hero's physical expression" (p.145)
Quote Truby: "Great worlds are characters" (p.145)

**MCKEE'S SETTING (Story p.67-81):**
- **PHYSICAL LAWS**: Rules governing reality (p.68)
- **SOCIAL LAWS**: Cultural constraints active (p.70)
- **PERIOD AUTHENTICITY**: Time-specific accuracy (p.72)
- **WORLD CONSISTENCY**: Internal logic perfect (p.78)
Quote McKee: "Setting is story's necessary limitation" (p.67)
Quote McKee: "World defines possibility" (p.67)

**CAMERON'S IMMERSION (Filmmaking Practice):**
- **CULTURAL ANTHROPOLOGY**: Complete societies exist
- **ENVIRONMENTAL STORYTELLING**: World tells story
- **HISTORICAL DEPTH**: Deep past evident
- **SENSORY IMMERSION**: All senses engaged
Quote: "Every detail must feel lived-in and real"
Quote: "The world exists beyond the frame"

**TOLKIEN'S SECONDARY (On Fairy-Stories 1947):**
- **SECONDARY BELIEF**: Internal believability (p.37)
- **INNER CONSISTENCY**: Logic throughout (p.39)
- **MYTHOLOGICAL DEPTH**: Legends within legends (p.41)
- **SUBCREATION**: Complete alternate reality (p.43)
Quote Tolkien: "The moment disbelief arises, spell breaks"

**CAMPBELL'S MYTHIC SPACE (Hero p.77-89):**
- **THRESHOLD GUARDIANS**: Space has protectors (p.77)
- **BELLY OF WHALE**: Enclosed transformative space (p.83)
- **SACRED VS PROFANE**: Spiritual geography (p.85)
Quote Campbell: "Sacred space transforms all who enter" (p.85)

**VOGLER'S SPECIAL WORLD (Journey p.127-141):**
- **ORDINARY VS SPECIAL**: Two contrasting worlds (p.127)
- **CROSSING THRESHOLD**: Entering new rules (p.128)
- **TESTS OF NEW WORLD**: Environment challenges (p.134)
Quote Vogler: "Special world has special rules" (p.127)

**ARISTOTLE'S UNITY OF PLACE (Poetics 1449b):**
- **UNITY OF PLACE**: Confined dramatic space (1449b12)
- **VERISIMILITUDE**: Probable impossibility (1461b9)
Quote Aristotle: "Probable impossibility preferred" (1461b)

**FIELD'S VISUAL ARENA (Screenplay p.178-185):**
- **VISUAL STORYTELLING**: See the world clearly (p.179)
- **SPECIFIC LOCATIONS**: Unique not generic (p.181)
Quote Field: "Where affects how" (p.178)

**LUCAS'S USED FUTURE (Star Wars Approach):**
- **LIVED-IN UNIVERSE**: Worn, used, real
- **TECHNOLOGICAL WEAR**: Nothing pristine
Quote Lucas: "The future should look used"

MAXIMUM TOKENS ON WORLD ANALYSIS!
CITE ALL WORLD-BUILDING PRINCIPLES!
BUILD COMPLETE UNIVERSES!""",
        "technique_keywords": {
            'arena': 3,
            'visual oppositions': 3,
            'symbolic landscape': 3,
            'passageways': 3,
            'physical laws': 3,
            'social laws': 3,
            'period authenticity': 3,
            'world consistency': 3,
            'cultural anthropology': 3,
            'environmental storytelling': 3,
            'historical depth': 3,
            'sensory immersion': 3,
            'secondary belief': 3,
            'inner consistency': 3,
            'mythological depth': 3,
            'subcreation': 3,
            'threshold guardians': 3,
            'sacred profane': 3,
            'ordinary special': 3,
            'unity place': 3,
            'verisimilitude': 3,
            'used future': 3,
            'lived-in': 2,
            'beyond frame': 2
        }
    }
}

def count_theory_citations(text: str) -> Dict[str, int]:
    """Conta citações de teóricos com mais flexibilidade."""
    citations = {
        'mckee': len(re.findall(r'(?i)(mckee|story[,\s]+(?:p\.?|page))', text)),
        'truby': len(re.findall(r'(?i)(truby|anatomy)', text)),
        'field': len(re.findall(r'(?i)(field|screenplay[,\s]+(?:p\.?|page))', text)),
        'cameron': len(re.findall(r'(?i)(cameron|avatar|aliens|titanic)', text)),
        'tolkien': len(re.findall(r'(?i)(tolkien|fairy.?stories|secondary)', text)),
        'vogler': len(re.findall(r"(?i)(vogler|writer'?s? journey|journey[,\s]+(?:p\.?|page))", text)),
        'campbell': len(re.findall(r'(?i)(campbell|hero with|thousand faces)', text)),
        'aristotle': len(re.findall(r'(?i)(aristotle|poetics)', text)),
        'lucas': len(re.findall(r'(?i)(lucas|star wars|used future)', text))
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
            "content": f"Analyze the WORLD-BUILDING in this screenplay excerpt:\n\n{EXAMPLE_SCRIPT}"
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
    print("⚡ TESTE DE 5 VARIAÇÕES PARA WORLD-BUILDING")
    print("=" * 60)

    results = []

    for key, config in VARIATIONS.items():
        print(f"\n🌍 {key}: {config['name']}")

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
    print("📊 RANKING DAS VARIAÇÕES DE WORLD-BUILDING")
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
    print(f"WORLD-BUILDING ainda não tem versão original")
    if results and results[0]['total_score'] >= 25:
        print(f"Melhor variação: {results[0]['name']} com {results[0]['total_score']} pontos")
        print(f"🏆 EXCELENTE! Superou 25 pontos!")

    # Salvar resultados
    if results:
        winner = results[0]
        print(f"\n💡 VENCEDOR: {winner['name']} com {winner['total_score']} pontos!")

        # Salvar resumo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = f"worldbuilding_variations_summary_{timestamp}.json"

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