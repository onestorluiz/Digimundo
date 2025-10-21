#!/usr/bin/env python3
"""
🎯 TESTE COMPARATIVO: 5 Métodos para CHARACTER
Foco em aplicação real de teoria dos livros de roteiro
"""

import json
import subprocess
import time
from pathlib import Path
import re

def analyze_theory_application(response: str) -> dict:
    """Analisa aplicação de teorias de roteiro"""

    response_lower = response.lower()

    # Teorias específicas mencionadas
    theories = {
        "mckee": response_lower.count("mckee"),
        "truby": response_lower.count("truby"),
        "vogler": response_lower.count("vogler"),
        "field": response_lower.count("field"),
        "campbell": response_lower.count("campbell"),
        "snyder": response_lower.count("snyder"),
        "aristotle": response_lower.count("aristotle")
    }

    # Conceitos técnicos aplicados
    concepts = {
        "character_arc": "character arc" in response_lower or "arc" in response_lower,
        "want_vs_need": "want" in response_lower and "need" in response_lower,
        "internal_external": "internal" in response_lower and "external" in response_lower,
        "backstory": "backstory" in response_lower or "background" in response_lower,
        "motivation": "motivation" in response_lower or "motive" in response_lower,
        "conflict": "conflict" in response_lower,
        "transformation": "transformation" in response_lower or "change" in response_lower,
        "flaw": "flaw" in response_lower or "weakness" in response_lower,
        "ghost": "ghost" in response_lower or "wound" in response_lower,
        "stakes": "stakes" in response_lower
    }

    # Aplicação prática
    practical = {
        "specific_examples": len(re.findall(r'"[^"]{10,}"', response)),
        "page_references": len(re.findall(r'page \d+', response_lower)),
        "scene_analysis": "scene" in response_lower,
        "dialogue_quotes": response.count('"'),
        "character_names": len(re.findall(r'\b[A-Z][a-z]+\b', response))
    }

    words = len(response.split())

    return {
        "words": words,
        "theories": theories,
        "total_theories": sum(theories.values()),
        "concepts": concepts,
        "concepts_used": sum(concepts.values()),
        "practical": practical,
        "practical_score": sum(practical.values())
    }

def test_character_method(prompt_dict: dict, test_script: str) -> dict:
    """Testa um método específico"""

    method_name = prompt_dict["name"]
    system_prompt = prompt_dict["system"]

    print(f"\n🔬 Testing {method_name}...")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze these characters:\n\n{test_script}"}
    ]

    data = {
        "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.75,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            "num_predict": 2000
        }
    }

    start = time.time()

    try:
        cmd = ["curl", "-s", "-X", "POST", "http://localhost:11434/api/chat",
               "-H", "Content-Type: application/json",
               "-d", json.dumps(data)]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)

        if result.returncode == 0:
            response_data = json.loads(result.stdout)
            response_text = response_data.get("message", {}).get("content", "")

            if response_text:
                elapsed = time.time() - start
                analysis = analyze_theory_application(response_text)

                print(f"   ✅ {analysis['words']} words in {elapsed:.1f}s")
                print(f"   📚 Theories: {analysis['total_theories']}")
                print(f"   💡 Concepts: {analysis['concepts_used']}/10")
                print(f"   🎯 Practical: {analysis['practical_score']}")

                # Salvar resposta
                filename = f"character_{method_name.replace(' ', '_')}_{int(time.time())}.txt"
                with open(filename, 'w') as f:
                    f.write(response_text)

                return {
                    "method": method_name,
                    "words": analysis['words'],
                    "time": elapsed,
                    "theories": analysis['total_theories'],
                    "concepts": analysis['concepts_used'],
                    "practical": analysis['practical_score'],
                    "analysis": analysis,
                    "response_file": filename
                }

    except Exception as e:
        print(f"   ❌ Error: {e}")

    return None

# DEFINIR OS 5 MÉTODOS
methods = {
    "METHOD_1_MCKEE_FOCUSED": {
        "name": "McKee Focused",
        "system": """You are Robert McKee's top student, analyzing characters through his STORY framework.

Apply McKee's principles EXPLICITLY:

1. CHARACTER vs CHARACTERIZATION (300 words)
- CHARACTERIZATION: What the character appears to be (quote evidence)
- TRUE CHARACTER: What they reveal under pressure (quote evidence)
- THE GAP: Measure the distance between mask and truth
- Quote McKee: "True character is revealed in the choices a human being makes under pressure"

2. CONSCIOUS vs UNCONSCIOUS DESIRE (300 words)
- CONSCIOUS: What they say they want (quote dialogue)
- UNCONSCIOUS: What they really need (analyze subtext)
- CONTRADICTION: How these conflict
- Apply McKee's principle: "The finest writing not only reveals true character, but arcs it"

3. DIMENSIONAL ANALYSIS (300 words)
- CONTRADICTION: Internal contradictions that make them human
- CREDIBILITY: Do their actions match their nature?
- COMPLEXITY: Analyze using McKee's dimensional scale
- Quote specific page/scene evidence for each point

4. PRESSURE COOKER MOMENTS (300 words)
- Identify 3 moments of maximum pressure
- Show choice made vs choice not made
- Reveal true character through action
- Apply McKee: "Pressure is essential. Choices made when nothing is at risk mean little"

Use McKee's exact terminology throughout. Reference his concepts explicitly."""
    },

    "METHOD_2_TRUBY_ANATOMY": {
        "name": "Truby Anatomy",
        "system": """You are applying John Truby's 22-Step Story Structure to character analysis.

TRUBY'S ANATOMY OF CHARACTER:

1. WEAKNESS AND NEED (300 words)
- PSYCHOLOGICAL WEAKNESS: Internal flaw (be specific)
- MORAL WEAKNESS: How they hurt others
- NEED: What they must learn to have better life
- Apply Truby: "Need is what's missing within the hero"

2. DESIRE LINE (300 words)
- EXTERNAL GOAL: What they're trying to accomplish
- SPINE OF ACTION: Track their pursuit scene by scene
- OBSTACLES: What blocks them (internal and external)
- Quote Truby: "Desire is what your hero wants in the story"

3. GHOST AND BACKSTORY (300 words)
- THE GHOST: Event that haunts them (stated or implied)
- HOW IT CONTROLS: Present behavior driven by past
- BACKSTORY REVEALS: When/how we learn about it
- Truby principle: "The ghost is the event from the past that still haunts the hero"

4. SELF-REVELATION (300 words)
- FALSE BELIEFS: What lies do they believe?
- BATTLE: Internal struggle to change
- REVELATION: What truth do they discover?
- NEW EQUILIBRIUM: How are they different?
- Quote Truby on character change mechanism

Reference Truby's Anatomy of Story explicitly. Use his exact framework."""
    },

    "METHOD_3_VOGLER_ARCHETYPAL": {
        "name": "Vogler Archetypal",
        "system": """You are Christopher Vogler's apprentice, applying The Writer's Journey archetypal analysis.

VOGLER'S ARCHETYPAL CHARACTER ANALYSIS:

1. PRIMARY ARCHETYPE (300 words)
- Identify: Hero/Mentor/Threshold Guardian/Herald/Shapeshifter/Shadow/Ally/Trickster
- FUNCTION: What archetypal role do they serve?
- MASK: How do they embody this archetype?
- Quote Vogler: "Archetypes are amazingly constant throughout all times and cultures"

2. HERO'S JOURNEY POSITION (300 words)
- ORDINARY WORLD: Where do they start?
- CALL TO ADVENTURE: What disrupts their world?
- REFUSAL: How do they resist change?
- CROSSING THRESHOLD: When do they commit?
- Map their position using Vogler's 12 stages

3. SHADOW WORK (300 words)
- EXTERNAL SHADOW: Who/what opposes them?
- INTERNAL SHADOW: Dark aspects of self
- PROJECTION: What do they deny in themselves?
- Apply Jung via Vogler: "The Shadow represents the energy of the dark side"

4. TRANSFORMATION THROUGH ARCHETYPES (300 words)
- SHAPESHIFTING: How do they change masks?
- MENTOR INFLUENCE: Who guides them?
- DEATH/REBIRTH: What old self must die?
- ELIXIR: What do they bring back?

Use Campbell's monomyth via Vogler's interpretation. Reference archetypes explicitly."""
    },

    "METHOD_4_FIELD_STRUCTURAL": {
        "name": "Field Structural",
        "system": """You are Syd Field's protégé, applying his Paradigm Structure to character development.

FIELD'S STRUCTURAL CHARACTER ANALYSIS:

1. SETUP - WHO IS THIS CHARACTER? (300 words)
- CONTEXT: Professional/Personal/Private life
- DRAMATIC NEED: What drives them through story?
- POINT OF VIEW: Their attitude/way of life
- CHANGE OR GROWTH: Which will it be?
- Quote Field: "Character is the essential foundation of your screenplay"

2. CONFRONTATION - CHARACTER IN CONFLICT (300 words)
- PLOT POINT I: How does it change them?
- OBSTACLES: Progressive complications faced
- MIDPOINT: How do they shift approach?
- PLOT POINT II: What forces final change?
- Track using Field's three-act structure

3. INTERIOR VS EXTERIOR (300 words)
- EXTERIOR: Physical journey/actions taken
- INTERIOR: Emotional journey within
- CONVERGENCE: Where these meet
- Apply Field: "Action is character"

4. RESOLUTION - CHARACTER TRANSFORMED (300 words)
- CLIMAX: Ultimate test of character
- RESOLUTION: New equilibrium achieved
- CHANGE MEASURED: From setup to resolution
- Field's principle: "The resolution must resolve the story"

Use Field's Paradigm structure. Reference plot points explicitly."""
    },

    "METHOD_5_SYNTHESIS_MASTER": {
        "name": "Synthesis Master",
        "system": """You are a master analyst synthesizing ALL major screenwriting theories.

THEORETICAL SYNTHESIS ANALYSIS (1200 words):

1. UNIVERSAL STORY PRINCIPLES (300 words)
Apply these foundational concepts:
- ARISTOTLE: Hamartia (tragic flaw) - identify it
- CAMPBELL: Hero's journey stage - place them
- MCKEE: True character under pressure - reveal it
- Quote from each theorist

2. CHARACTER ARCHITECTURE (300 words)
Layer these frameworks:
- TRUBY: Weakness → Need → Desire → Struggle → Revelation
- FIELD: Setup → Confrontation → Resolution arc
- VOGLER: Archetypal function in story
- Show how each lens reveals different aspects

3. PRACTICAL CRAFT ELEMENTS (300 words)
Apply working writer tools:
- SNYDER: Save the Cat moment - do they have one?
- DIALOGUE: Subtext vs text analysis
- VISUAL STORYTELLING: Show don't tell examples
- SCENE WORK: Beats and turns

4. INTEGRATED DIAGNOSIS (300 words)
Synthesize all approaches:
- Which theory best explains this character?
- Where do theories contradict?
- What's missing from standard analysis?
- Your expert recommendation using all tools

Reference multiple theorists by name. Show mastery of various approaches."""
    }
}

def main():
    print("="*60)
    print("🎯 TESTE COMPARATIVO: 5 MÉTODOS DE CHARACTER")
    print("Foco: Aplicação real de teoria dos livros")
    print("="*60)

    # Script de teste
    test_script = """FADE IN:

INT. ABANDONED CHURCH - NIGHT

MARCUS (42), priest's collar loose, whiskey bottle in hand,
sits in the front pew. His hands shake.

ELENA (38), leather jacket over scrubs, enters quietly.
She sits beside him, doesn't look at him.

ELENA
You called me here to watch you drink?

MARCUS
I called you here to confess.

ELENA
I'm not a priest anymore, Marcus.
Haven't been for five years.

MARCUS
Neither am I. Not after tonight.

ELENA
(finally looking at him)
What did you do?

MARCUS
What I had to. What you taught me.

ELENA
I taught you to save lives.

MARCUS
(laughing bitterly)
No. You taught me that some lives
aren't worth saving.

ELENA
That's not—

MARCUS
The Morrison boy. You remember?
You let him die.

ELENA
(standing)
He was brain dead. There was no—

MARCUS
And tonight, I let someone die too.
Someone who trusted me. Someone who
came to me for salvation.

Marcus pulls out a blood-stained confession note.

MARCUS (CONT'D)
He confessed to killing three children.
And I... I gave him communion wine.
With something extra.

FADE OUT."""

    results = []

    for method_key, method_data in methods.items():
        result = test_character_method(method_data, test_script)
        if result:
            results.append(result)
            time.sleep(2)  # Pausa entre testes

    # Análise comparativa
    if results:
        print("\n" + "="*60)
        print("📊 ANÁLISE COMPARATIVA")
        print("="*60)

        # Ordenar por aplicação de teoria
        results.sort(key=lambda x: x['theories'] + x['concepts'], reverse=True)

        print("\n🏆 RANKING POR APLICAÇÃO DE TEORIA:")
        for i, r in enumerate(results, 1):
            theory_score = r['theories'] + r['concepts']
            print(f"\n{i}. {r['method']}")
            print(f"   📚 Theory Score: {theory_score}")
            print(f"   📝 Words: {r['words']}")
            print(f"   🎓 Theories cited: {r['theories']}")
            print(f"   💡 Concepts used: {r['concepts']}/10")
            print(f"   🎯 Practical examples: {r['practical']}")

        # Análise detalhada do vencedor
        winner = results[0]
        print("\n" + "="*60)
        print("🥇 VENCEDOR POR APLICAÇÃO DE TEORIA")
        print("="*60)
        print(f"\n{winner['method']}: {winner['theories'] + winner['concepts']} pontos de teoria")

        if winner['analysis']['theories']:
            print("\nTeorias mencionadas:")
            for theory, count in winner['analysis']['theories'].items():
                if count > 0:
                    print(f"  - {theory}: {count}x")

        print("\nConceitos aplicados:")
        for concept, used in winner['analysis']['concepts'].items():
            if used:
                print(f"  ✓ {concept}")

        # Relatório final
        report = {
            "test": "Character Methods Comparison",
            "focus": "Theory Application from Screenwriting Books",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": results,
            "winner": winner['method'],
            "winner_theory_score": winner['theories'] + winner['concepts']
        }

        report_file = f"character_methods_comparison_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📁 Relatório salvo: {report_file}")

if __name__ == "__main__":
    main()