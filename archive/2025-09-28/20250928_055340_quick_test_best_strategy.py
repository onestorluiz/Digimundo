#!/usr/bin/env python3
"""
TESTE RÁPIDO - ESTRATÉGIA OTIMIZADA
====================================
Testa uma estratégia otimizada baseada nos aprendizados anteriores
"""

import time
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_optimized_strategy():
    """Testa estratégia otimizada com foco em volume e profundidade"""

    screenplay = """
    FADE IN:

    INT. APARTMENT - DAY (PAGE 1)

    JOHN (35), unshaven, stares at a photo of SARAH.

    JOHN
    I don't need anyone. Never did.

    He throws the photo in the trash. Immediately retrieves it.

    JOHN (CONT'D)
    (whispered)
    Liar.

    PAGE 15: John avoids colleagues at work.
    PAGE 23: John watches old videos of Sarah.
    PAGE 45: John admits to therapist: "She's dead. Three months."
    """

    # Estratégia otimizada com elementos que funcionaram
    prompt = f"""
You are conducting a MASTERCLASS ANALYSIS with forensic precision.

YOUR MISSION: Deliver 1200+ words of DEEP, SPECIFIC analysis.

MANDATORY STRUCTURE (each section MUST be 300+ words):

SECTION 1: EVIDENCE MINING (300+ words minimum)
Begin: "Let's excavate the evidence layer by layer..."

- Quote the EXACT line "I don't need anyone. Never did." from page 1
- Analyze why he immediately retrieves the photo (contradiction)
- Note the whispered "Liar" - what does this reveal?
- Track his isolation pattern across pages 1, 15, 23, 45
- Find 3 things others would miss

SECTION 2: THEORETICAL DEEP DIVE (300+ words minimum)
Continue: "Applying our theoretical frameworks..."

- McKee's gap: His statement vs his actions (throwing/retrieving photo)
- Truby's need vs desire: Wants isolation, needs connection
- Vogler's journey: Identify his refusal of the call stage
- Reference Kubler-Ross grief stages
- Connect each theory to specific page evidence

SECTION 3: PSYCHOLOGICAL ARCHITECTURE (300+ words minimum)
Continue: "The psychological landscape reveals..."

- Defense mechanism: Denial ("I don't need anyone")
- The wound: Sarah's death (page 45 revelation)
- Projection: Pushing others away before they can leave
- Track his grief progression through the pages
- Identify the lie he believes vs truth he needs

SECTION 4: COMPARATIVE MASTERY (300+ words minimum)
Continue: "When compared to cinematic masterpieces..."

- Compare to Rick in Casablanca (pushing Ilsa away)
- Contrast with Michael in Godfather (different isolation)
- Parallel with Walter White's "I did it for me" admission
- Find one unique comparison
- What does this character do differently?

REMEMBER: Each section MUST be 300+ words. Total MUST exceed 1200 words.
Use specific page references throughout.
Be detailed, specific, and insightful.

Screenplay to analyze:
{screenplay}

Begin your masterclass analysis now:
"""

    logger.info("Testing optimized strategy...")
    start_time = time.time()

    # Call Ollama API
    api_url = "http://localhost:11434/api/generate"

    payload = {
        "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 4000,
            "temperature": 0.85,
            "top_p": 0.95,
            "num_ctx": 131072,
            "repeat_penalty": 1.0,
            "top_k": 100,
            "seed": 42  # For consistency
        }
    }

    try:
        response = requests.post(api_url, json=payload, timeout=300)

        if response.status_code == 200:
            result_json = response.json()
            output = result_json.get("response", "")

            elapsed = time.time() - start_time
            word_count = len(output.split())

            logger.info(f"✅ Success!")
            logger.info(f"   Words: {word_count}")
            logger.info(f"   Time: {elapsed:.1f}s")

            # Save output
            with open("optimized_strategy_output.txt", "w") as f:
                f.write(output)

            # Print preview
            print("\n" + "="*60)
            print("PREVIEW (first 1000 chars):")
            print("="*60)
            print(output[:1000])
            print("\n[...]")

            print(f"\n📊 RESULTS:")
            print(f"   Total words: {word_count}")
            print(f"   Target: 1200+ words")
            print(f"   Success: {'✅' if word_count >= 1200 else '❌'}")

            return output, word_count

        else:
            logger.error(f"API error: {response.status_code}")
            return None, 0

    except Exception as e:
        logger.error(f"Exception: {e}")
        return None, 0

if __name__ == "__main__":
    print("\n🚀 TESTING OPTIMIZED STRATEGY")
    print("="*60)

    output, words = test_optimized_strategy()

    if words >= 1200:
        print("\n🎉 SUCCESS! Strategy produces 1200+ words!")
    elif words >= 800:
        print("\n⚠️ PARTIAL SUCCESS: 800+ words but under 1200")
    else:
        print(f"\n❌ FAILED: Only {words} words")