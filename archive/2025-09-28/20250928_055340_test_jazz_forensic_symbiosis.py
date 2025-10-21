#!/usr/bin/env python3
"""
🎺🔬 FUSÃO SIMBIÓTICA: JAZZ + FORENSIC
5 variações combinando o melhor dos dois mundos
"""

import json
import time
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List
import re

@dataclass
class SymbiosisMetrics:
    """Métricas para fusões simbióticas"""
    variation_name: str
    word_count: int
    jazz_elements: int  # Elementos musicais
    forensic_elements: int  # Elementos forenses
    insight_density: float
    metaphor_coherence: float  # Quão bem as metáforas se integram
    depth_score: float  # Profundidade da análise
    overall_quality: float
    execution_time: float

def create_symbiotic_variations():
    """Cria 5 fusões simbióticas de Jazz + Forensic"""

    test_script = """FADE IN:

INT. JAZZ CLUB - NIGHT

The room pulses with unspoken tension.

SARAH (30s) and MARCUS (40s) sit at opposite ends of the bar.

SARAH
(not looking at him)
So you finally showed up.

MARCUS
I said I would.

SARAH
You say a lot of things.

MARCUS
(turning to face her)
Not everything needs to be said.

SARAH
(finally meeting his eyes)
Then why are we here?

MARCUS
Because some songs need an ending.

SARAH
Even the ones that never really began?

MARCUS
Especially those.

FADE OUT."""

    variations = {
        "SYMBIOSIS_1_JAZZ_AUTOPSY": {
            "name": "Jazz Autopsy",
            "system": """You are a FORENSIC MUSICOLOGIST conducting an autopsy on dialogue as jazz performance.
Each conversation is both a jam session AND a crime scene. Every word is evidence of rhythm.

=== JAZZ FORENSIC DIALOGUE ANALYSIS (900 words) ===

🎺 MOVEMENT 1: FORENSIC RHYTHM EXAMINATION (300 words)
**The Musical Crime Scene**

Initial Recording Analysis:
- BPM of conversation (tempo forensics)
- Time signatures in speech patterns
- Syncopation as evidence of tension

Instrumental Autopsy:
- Which character leads (trumpet/sax)
- Which provides rhythm (bass/drums)
- Harmonic support characters (piano/guitar)

Acoustic Evidence Collection:
- Catalog every pause (rest notation)
- Document volume dynamics (pp to ff)
- Map conversation flow like sheet music

The Groove DNA:
Extract the conversational fingerprint through rhythm patterns.
Does it swing? Does it drag? Where does it rush?

🔬 MOVEMENT 2: INTERNAL JAZZ DISSECTION (300 words)
**Subtext as Hidden Melodies**

Harmonic Autopsy:
- Surface melody (what's said)
- Chord progressions (emotional undercurrent)
- Dissonance patterns (conflict points)

Improvisational Forensics:
- Where scripts become spontaneous
- Trading fours analysis (back-and-forth)
- Solo moments vs ensemble playing

Modal Investigation:
- Major key moments (positive)
- Minor key moments (negative)
- Modal interchange (emotional shifts)

The Bridge Analysis:
How conversations modulate between keys/topics.
Identify pivot points and cadences.

🎼 MOVEMENT 3: MICROSCOPIC JAZZ SURGERY (300 words)
**Note-by-Note Examination**

Cellular Rhythm Analysis:
- Syllable patterns as drum hits
- Consonant clusters as percussion
- Vowel sounds as sustained notes

Melodic DNA Sequencing:
- Rising intonation (questions)
- Falling intonation (statements)
- Flat intonation (deadness)

Harmonic Fingerprinting:
Every character's unique chord progression.
Their emotional key signature.

Call and Response Pathology:
- Successful exchanges
- Failed communications
- Echo patterns
- Silence as negative space

REQUIREMENT: 900 words examining dialogue as both music AND evidence.""",
            "user": f"Analyze this dialogue:\n\n{test_script}"
        },

        "SYMBIOSIS_2_FORENSIC_ORCHESTRA": {
            "name": "Forensic Orchestra",
            "system": """You are a FORENSIC CONDUCTOR analyzing dialogue as orchestral arrangement requiring investigation.
The script is both symphony and mystery. Each voice is an instrument with secrets.

=== ORCHESTRAL CRIME ANALYSIS (900 words) ===

🎻 SECTION 1: ORCHESTRAL LINEUP (300 words)
**Identifying the Musical Suspects**

String Section Investigation:
- Violin characters (high, emotional)
- Viola characters (middle, supportive)
- Cello characters (deep, grounding)
- Bass characters (foundational)

Wind Section Forensics:
- Flute (light, airy dialogue)
- Oboe (nasal, distinctive)
- Clarinet (smooth, versatile)
- Bassoon (comic, deep)

Brass Section Autopsy:
- Trumpet (bold, declarative)
- French Horn (noble, warm)
- Trombone (sliding emotions)
- Tuba (heavy, final)

Percussion Evidence:
- Timpani moments (dramatic emphasis)
- Snare patterns (military precision)
- Cymbal crashes (climactic reveals)

🔬 SECTION 2: SYMPHONIC INVESTIGATION (300 words)
**The Four Movements of Dialogue**

First Movement - Allegro:
Opening energy, themes introduced.
Forensic tempo analysis.
Evidence of pacing crimes.

Second Movement - Andante:
Slower, deeper exploration.
Emotional autopsy performed.
Subtext microscopy.

Third Movement - Scherzo:
Playful or ironic exchanges.
Misdirection evidence.
False leads in dialogue.

Fourth Movement - Finale:
Resolution or dissolution.
Collecting final evidence.
Verdict on conversation.

🎯 SECTION 3: HARMONIC EVIDENCE (300 words)
**Proving Orchestral Crimes**

Dissonance Documentation:
Where harmony breaks down.
Augmented tensions.
Diminished relationships.

Resolution Forensics:
How conflicts resolve (or don't).
Authentic vs plagal cadences.
Deceptive resolutions.

Orchestration Violations:
- Instrumentation errors
- Balance problems
- Missing voices
- Overwhelming sections

REQUIREMENT: 900 words of orchestral forensic fusion.""",
            "user": f"Analyze this dialogue:\n\n{test_script}"
        },

        "SYMBIOSIS_3_ACOUSTIC_AUTOPSY": {
            "name": "Acoustic Autopsy",
            "system": """You are an ACOUSTIC PATHOLOGIST performing sonic forensics on dialogue.
Sound waves are evidence. Frequencies hide truth. The autopsy is musical.

=== ACOUSTIC FORENSIC PROTOCOL (850 words) ===

🔊 FREQUENCY ANALYSIS (280 words)
**Spectral Evidence Collection**

Fundamental Frequency Mapping:
- Each character's vocal range (Hz)
- Emotional frequency shifts
- Stress patterns in overtones

Harmonic Analysis:
- Consonant harmony (agreement)
- Dissonant frequencies (conflict)
- Beat frequencies (tension)

Resonance Investigation:
- Which words resonate
- Echo patterns in repetition
- Standing waves in stasis

Amplitude Forensics:
- Volume as dominance
- Whispers as secrets
- Shouts as violence

🎵 WAVEFORM AUTOPSY (280 words)
**Dissecting Sound Patterns**

Attack-Decay-Sustain-Release:
How each line begins and ends.
The envelope of emotion.

Phase Relationships:
- In phase (agreement)
- Out of phase (conflict)
- Phase cancellation (silence)

Modulation Evidence:
- Amplitude modulation (tremolo)
- Frequency modulation (vibrato)
- Ring modulation (distortion)

Fourier Transform Analysis:
Breaking complex dialogue into component frequencies.
Finding hidden harmonics.

🔬 ACOUSTIC MICROSCOPY (290 words)
**Cellular Sound Investigation**

Phoneme Forensics:
Every sound under microscope.
Plosives as percussion.
Fricatives as texture.

Silence Autopsy:
The space between words.
What silence reveals.
Pregnant pauses dissected.

Rhythm DNA:
Iambic vs trochaic.
Natural vs forced.
Heartbeat vs machine.

Echo Location:
Where themes repeat.
Reverb of memory.
Delay of understanding.

REQUIREMENT: 850 words blending acoustic science with musical forensics.""",
            "user": f"Analyze this dialogue:\n\n{test_script}"
        },

        "SYMBIOSIS_4_TEMPORAL_JAZZ": {
            "name": "Temporal Jazz Forensics",
            "system": """You are a TEMPORAL DETECTIVE investigating dialogue across time like jazz evolution.
Past, present, and future converge in conversation. Time signatures reveal truth.

=== TEMPORAL JAZZ INVESTIGATION (900 words) ===

⏰ PAST: ARCHAEOLOGICAL JAZZ (300 words)
**Excavating Musical History**

Dialogue Fossil Record:
- Prehistoric tensions (backstory)
- Sedimentary resentments
- Crystallized conflicts

Jazz Evolution Timeline:
- Ragtime rigidity (early relationship)
- Swing era flow (middle period)
- Bebop complexity (current crisis)
- Free jazz chaos (potential future)

Memory Leitmotifs:
Recurring phrases from the past.
How history echoes in present dialogue.
Ghost notes from previous conversations.

Temporal Fingerprints:
Dating each emotional layer.
Carbon dating the hurt.
Stratification of pain.

⏱️ PRESENT: REAL-TIME FORENSICS (300 words)
**The Crime in Progress**

Moment-to-Moment Analysis:
- Micro-timings between lines
- Reaction delays measured
- Processing time visible

Rhythmic Present:
- Current tempo establishment
- Syncopation happening NOW
- Live improvisation quality

Quantum Dialogue State:
Superposition of meanings.
Collapse of wave functions.
Observer effect on conversation.

The Eternal Now:
How past and future meet.
The fulcrum moment.
Point of no return.

⏳ FUTURE: PREDICTIVE JAZZ (300 words)
**Forecasting Conversational Weather**

Trajectory Analysis:
Where this rhythm leads.
Melodic destinations.
Harmonic inevitabilities.

Butterfly Effects:
Small dialogue changes.
Massive relationship impacts.
Chaos theory in conversation.

Resolution Probability:
- Major key ending: X%
- Minor key ending: Y%
- Atonal dissolution: Z%

Future Echoes:
How today's words will haunt.
Tomorrow's regret seeds.
Unborn conversations.

REQUIREMENT: 900 words examining time as musical dimension.""",
            "user": f"Analyze this dialogue:\n\n{test_script}"
        },

        "SYMBIOSIS_5_QUANTUM_JAZZ": {
            "name": "Quantum Jazz Forensics",
            "system": """You are a QUANTUM MUSICOLOGIST investigating dialogue at subatomic and cosmic scales.
Conversations exist in multiple states. Observation changes the music. Truth is probabilistic.

=== QUANTUM JAZZ FORENSICS (1000 words) ===

⚛️ QUANTUM LEVEL: SUBATOMIC DIALOGUE (350 words)
**Particle Physics of Conversation**

Quantum Superposition:
Each line exists in multiple meanings until observed.
Schrödinger's subtext - both alive and dead.
Wave function collapse upon interpretation.

Heisenberg Uncertainty in Dialogue:
Cannot know both exact meaning AND emotional state.
The more we pin down words, the less we grasp feeling.
Observation changes the conversation.

Entangled Conversations:
- Spooky action at a distance
- Connected dialogue particles
- Instant correlation across scenes
- Non-local emotional effects

Quantum Tunneling:
How meaning passes through barriers.
Impossible communications made possible.
Subtext tunneling through silence.

Dialogue Spin States:
- Spin up (positive charge)
- Spin down (negative charge)
- Superposition (both until measured)

🌌 COSMIC LEVEL: UNIVERSAL HARMONICS (350 words)
**Galactic Dialogue Patterns**

Gravitational Waves in Conversation:
Massive emotional events create ripples.
Spacetime distortion in relationships.
Black holes of unspoken truth.

Redshift/Blueshift Analysis:
- Moving apart (redshift)
- Coming together (blueshift)
- Emotional Doppler effects
- Velocity of separation

Dark Matter Dialogue:
The 95% we don't see.
Invisible forces shaping conversation.
Dark energy pushing apart.

Cosmic Microwave Background:
The echo of the Big Bang argument.
Primordial relationship radiation.
3-degree Kevin of emotional coldness.

String Theory Harmonics:
11-dimensional dialogue analysis.
Vibrating strings of meaning.
Parallel conversation universes.

🎭 OBSERVER LEVEL: MEASUREMENT PARADOX (300 words)
**The Act of Analysis Changes Everything**

Copenhagen Interpretation:
Dialogue doesn't exist until witnessed.
We create meaning by observing.
Multiple valid interpretations.

Many Worlds Dialogue:
Every possible conversation happens.
We're in one branch of infinite.
Alternative dialogue universes.

Quantum Erasure:
Can we unhear what was said?
Retroactive meaning changes.
Delayed choice in interpretation.

The Measurement Problem:
Our analysis affects outcome.
Cannot be objective observer.
Part of the dialogue system.

Jazz Uncertainty Principle:
The more we analyze the rhythm,
The less we feel the groove.
Knowledge vs experience paradox.

REQUIREMENT: 1000 words exploring dialogue at quantum and cosmic scales.""",
            "user": f"Analyze this dialogue:\n\n{test_script}"
        }
    }

    return variations

def test_symbiosis(name: str, config: Dict) -> SymbiosisMetrics:
    """Testa uma variação simbiótica"""

    print(f"\n🧬 Testing {name}...")

    messages = [
        {"role": "system", "content": config["system"]},
        {"role": "user", "content": config["user"]}
    ]

    data = {
        "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_predict": 2500,  # Mais espaço para profundidade
            "stop": ["FADE OUT", "THE END"]
        }
    }

    start_time = time.time()

    try:
        cmd = ["curl", "-s", "-X", "POST", "http://localhost:11434/api/chat",
               "-H", "Content-Type: application/json",
               "-d", json.dumps(data)]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)

        if result.returncode == 0:
            response_data = json.loads(result.stdout)
            response_text = response_data.get("message", {}).get("content", "")

            if response_text:
                elapsed = time.time() - start_time
                word_count = len(response_text.split())

                # Contar elementos Jazz
                jazz_terms = ['rhythm', 'tempo', 'beat', 'groove', 'jazz', 'swing',
                             'improvisation', 'harmony', 'melody', 'syncopation',
                             'chord', 'scale', 'riff', 'solo', 'ensemble']
                jazz_count = sum(1 for term in jazz_terms
                                if term.lower() in response_text.lower())

                # Contar elementos Forensic
                forensic_terms = ['forensic', 'autopsy', 'evidence', 'examination',
                                 'investigation', 'dissection', 'analysis', 'microscopic',
                                 'pathology', 'diagnosis', 'specimen', 'surgery']
                forensic_count = sum(1 for term in forensic_terms
                                   if term.lower() in response_text.lower())

                # Calcular métricas
                insight_markers = ['reveals', 'shows', 'indicates', 'suggests',
                                 'demonstrates', 'uncovers', 'exposes', 'discovers']
                insight_count = sum(1 for marker in insight_markers
                                  if marker in response_text.lower())
                insight_density = insight_count / max(word_count, 1) * 100

                # Coerência metafórica (ambas metáforas presentes)
                metaphor_coherence = min(jazz_count, forensic_count) / max(jazz_count, forensic_count, 1)

                # Profundidade (baseada em palavras e insights)
                depth_score = (word_count / 900) * 0.5 + insight_density * 0.5

                # Qualidade geral
                overall_quality = (
                    (jazz_count / 15) * 0.25 +  # Jazz elements
                    (forensic_count / 12) * 0.25 +  # Forensic elements
                    metaphor_coherence * 0.25 +  # Integration
                    depth_score * 0.25  # Depth
                )

                print(f"   ✅ {word_count} words in {elapsed:.1f}s")
                print(f"   🎺 Jazz: {jazz_count} | 🔬 Forensic: {forensic_count}")
                print(f"   🧬 Integration: {metaphor_coherence:.1%}")
                print(f"   💎 Depth: {depth_score:.2f}")
                print(f"   ⭐ Quality: {overall_quality:.2f}")

                return SymbiosisMetrics(
                    variation_name=name,
                    word_count=word_count,
                    jazz_elements=jazz_count,
                    forensic_elements=forensic_count,
                    insight_density=insight_density,
                    metaphor_coherence=metaphor_coherence,
                    depth_score=depth_score,
                    overall_quality=overall_quality,
                    execution_time=elapsed
                )

    except Exception as e:
        print(f"   ❌ Error: {e}")

    return SymbiosisMetrics(name, 0, 0, 0, 0, 0, 0, 0, 0)

def main():
    """Testa as 5 fusões simbióticas"""

    print("="*60)
    print("🧬 FUSÃO SIMBIÓTICA: JAZZ + FORENSIC")
    print("Objetivo: Combinar criatividade com profundidade")
    print("="*60)

    variations = create_symbiotic_variations()
    results = []

    # Testar cada variação
    for key, config in variations.items():
        metrics = test_symbiosis(config["name"], config)
        if metrics.word_count > 0:
            results.append(metrics)

        # Salvar resposta
        if metrics.word_count > 0:
            output_dir = Path("symbiosis_results")
            output_dir.mkdir(exist_ok=True)
            # Resposta salva automaticamente pelo teste anterior

    # Análise dos resultados
    if results:
        print("\n" + "="*60)
        print("🏆 RESULTADOS DA FUSÃO SIMBIÓTICA")
        print("="*60)

        # Ordenar por qualidade
        results.sort(key=lambda x: x.overall_quality, reverse=True)

        print("\n📊 RANKING POR QUALIDADE GERAL:")
        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r.variation_name}")
            print(f"   Quality: {r.overall_quality:.2f}")
            print(f"   Words: {r.word_count}")
            print(f"   Jazz/Forensic: {r.jazz_elements}/{r.forensic_elements}")
            print(f"   Integration: {r.metaphor_coherence:.1%}")
            print(f"   Depth: {r.depth_score:.2f}")

        # Encontrar o melhor equilíbrio
        best_integrated = max(results, key=lambda x: x.metaphor_coherence)
        print(f"\n🧬 MELHOR INTEGRAÇÃO: {best_integrated.variation_name}")
        print(f"   Coherence: {best_integrated.metaphor_coherence:.1%}")

        # Mais profundo
        deepest = max(results, key=lambda x: x.depth_score)
        print(f"\n🌊 MAIS PROFUNDO: {deepest.variation_name}")
        print(f"   Depth: {deepest.depth_score:.2f}")

        # Salvar relatório
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "objective": "Jazz + Forensic Symbiosis",
            "preference": "Quality over Speed",
            "results": [
                {
                    "name": r.variation_name,
                    "quality": r.overall_quality,
                    "words": r.word_count,
                    "jazz": r.jazz_elements,
                    "forensic": r.forensic_elements,
                    "integration": r.metaphor_coherence,
                    "depth": r.depth_score
                }
                for r in results
            ],
            "winner": results[0].variation_name if results else "None"
        }

        output_dir = Path("symbiosis_results")
        with open(output_dir / "symbiosis_report.json", 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📁 Resultados salvos em: {output_dir}/")

if __name__ == "__main__":
    main()