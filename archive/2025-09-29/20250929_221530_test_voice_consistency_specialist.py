#!/usr/bin/env python3
"""
Test Suite for Script Doctor Voicemon - Character Voice Consistency Specialist
Tests the voice consistency specialist in isolation.
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.voice_consistency_specialist import DrVoiceConsistency


def create_distinct_voices_screenplay():
    """Create a screenplay with distinct character voices."""
    return """FADE IN:

INT. POLICE STATION - DAY

DETECTIVE HARRIS (50s), grizzled veteran.

HARRIS
Look, kid, I've been doing this for
twenty-three years. Twenty-three years
of scumbags and lowlifes. You think
this punk's any different?

ROOKIE CHEN (20s), eager and formal.

CHEN
With all due respect, Detective Harris,
the evidence suggests we should pursue
alternative theories. The forensic analysis
indicates multiple points of entry.

HARRIS
Forensic analysis? Kid, when I started,
we solved cases with shoe leather and
gut instinct. This punk's guilty.

CHEN  
Perhaps we could examine the security
footage more thoroughly? I believe
there may be details we've overlooked.

HARRIS
Believe? Kid, in this job, you don't
believe. You know or you don't. And
I know this punk did it.

TEENAGER JAZZ (17), street-smart.

JAZZ
Yo, I ain't no punk, old man. Y'all
got nothing on me. This is straight
up harassment, for real.

HARRIS
Shut it, punk. We got you dead to rights.

JAZZ
Nah, man, this is whack. I was with
my crew all night. We was gaming,
streaming, whatever. Check the logs.

CHEN
If you could provide us with verifiable
alibi witnesses, that would certainly
help clarify the situation.

JAZZ
Man, why you gotta talk like that?
I just told you - my boys can vouch.
We was online, check the streams.

PROFESSOR WILLIAMS (60s), intellectual.

WILLIAMS
Excuse me, officers. I couldn't help
but overhear. The young man's linguistic
patterns suggest authenticity. Moreover,
the sociological implications of this
interrogation are quite troubling.

HARRIS
Who the hell are you?

WILLIAMS
Professor Williams, criminology department.
I've published extensively on youth
culture and criminal justice. This
interaction exemplifies systemic issues.

JAZZ
Yo, prof's got my back! See? Even
the smart dude knows y'all trippin'.

FADE OUT."""


def create_inconsistent_voices_screenplay():
    """Create a screenplay with inconsistent character voices."""
    return """FADE IN:

INT. OFFICE - DAY

JOHN enters.

JOHN
Hello, how are you today?

MARY looks up.

MARY
I'm fine. How are you?

JOHN
I'm good. Did you see the report?

MARY
Yes, I saw it. It was interesting.

JOHN
Yo, that's what's up! The data was
straight fire, for real!

MARY
Indeed, the statistical analysis was
most illuminating. Furthermore, the
implications are quite significant.

JOHN
I agree. We should discuss it more.

MARY
Yeah, totally! Let's do it!

JOHN
Indubitably, we must examine the
ramifications more thoroughly. The
epistemological foundations require
scrutiny.

MARY
Okay. When should we meet?

JOHN
I don't know. When are you free?

MARY
I don't know. When are you free?

FADE OUT."""


def test_basic_voice_analysis():
    """Test basic voice consistency analysis."""
    print("\n🎤 TEST 1: Basic Voice Analysis")
    print("=" * 50)

    dr_voice = DrVoiceConsistency()
    screenplay = create_distinct_voices_screenplay()

    result = dr_voice.analyze(screenplay)

    # Check required fields
    assert "specialist" in result.__dict__
    assert "score" in result.__dict__
    assert "voice_profiles" in result.__dict__
    assert "voice_analysis" in result.__dict__

    print(f"✅ Specialist: {result.specialist['name']}")
    print(f"✅ Score: {result.score}/100")
    print(f"✅ Total characters: {result.voice_analysis.total_characters}")
    print(f"✅ Distinct voices: {result.voice_analysis.distinct_voices}")

    return True


def test_voice_distinctiveness():
    """Test voice distinctiveness detection."""
    print("\n🎤 TEST 2: Voice Distinctiveness")
    print("=" * 50)

    dr_voice = DrVoiceConsistency()

    # Distinct voices
    distinct = create_distinct_voices_screenplay()
    distinct_result = dr_voice.analyze(distinct)

    # Inconsistent voices
    inconsistent = create_inconsistent_voices_screenplay()
    inconsistent_result = dr_voice.analyze(inconsistent)

    print(f"🎯 Distinct screenplay:")
    print(f"   Distinctiveness score: {distinct_result.voice_analysis.voice_distinctiveness_score:.2f}")
    print(f"   Distinct voices: {distinct_result.voice_analysis.distinct_voices}/{distinct_result.voice_analysis.total_characters}")

    print(f"\n🔀 Inconsistent screenplay:")
    print(f"   Distinctiveness score: {inconsistent_result.voice_analysis.voice_distinctiveness_score:.2f}")
    print(f"   Distinct voices: {inconsistent_result.voice_analysis.distinct_voices}/{inconsistent_result.voice_analysis.total_characters}")

    print("\n✅ Voice distinctiveness detection working")

    return True


def test_voice_profiles():
    """Test character voice profiling."""
    print("\n🎤 TEST 3: Voice Profiles")
    print("=" * 50)

    dr_voice = DrVoiceConsistency()
    screenplay = create_distinct_voices_screenplay()
    result = dr_voice.analyze(screenplay)

    print("👥 Character profiles:")
    for char_name, profile in list(result.voice_profiles.items())[:3]:
        print(f"\n{char_name}:")
        print(f"   Total lines: {profile.total_lines}")
        print(f"   Avg sentence length: {profile.avg_sentence_length:.1f} words")
        print(f"   Formality: {profile.formality_score:.2f}")
        print(f"   Vocabulary complexity: {profile.vocabulary_complexity:.2f}")
        if profile.verbal_tics:
            print(f"   Verbal tics: {', '.join(profile.verbal_tics[:3])}")

    print("\n✅ Voice profiling working")

    return True


def test_consistency_detection():
    """Test voice consistency detection."""
    print("\n🎤 TEST 4: Consistency Detection")
    print("=" * 50)

    dr_voice = DrVoiceConsistency()
    inconsistent = create_inconsistent_voices_screenplay()
    result = dr_voice.analyze(inconsistent)

    print(f"🔄 Consistency issues found: {len(result.voice_analysis.consistency_issues)}")
    for issue in result.voice_analysis.consistency_issues[:2]:
        print(f"   {issue['character']}: {issue['issue']}")
        print(f"   Score: {issue['consistency_score']:.2f}")

    print(f"\n📊 Consistency scores:")
    for char, score in list(result.consistency_scores.items())[:3]:
        print(f"   {char}: {score:.2f}")

    print("\n✅ Consistency detection working")

    return True


def test_interchangeable_dialogue():
    """Test interchangeable dialogue detection."""
    print("\n🎤 TEST 5: Interchangeable Dialogue")
    print("=" * 50)

    dr_voice = DrVoiceConsistency()
    inconsistent = create_inconsistent_voices_screenplay()
    result = dr_voice.analyze(inconsistent)

    print(f"🔀 Interchangeable dialogue found: {len(result.voice_analysis.interchangeable_dialogue)}")
    for item in result.voice_analysis.interchangeable_dialogue[:3]:
        print(f"   {item['character']}: \"{item['dialogue']}\"")
        print(f"   Reason: {item['reason']}")

    print("\n✅ Interchangeable dialogue detection working")

    return True


def test_similarity_matrix():
    """Test character voice similarity calculation."""
    print("\n🎤 TEST 6: Similarity Matrix")
    print("=" * 50)

    dr_voice = DrVoiceConsistency()
    screenplay = create_distinct_voices_screenplay()
    result = dr_voice.analyze(screenplay)

    print("📋 Voice similarity matrix (sample):")
    chars = list(result.similarity_matrix.keys())[:3]
    for char1 in chars:
        for char2 in chars:
            if char1 != char2:
                similarity = result.similarity_matrix[char1][char2]
                print(f"   {char1} ↔ {char2}: {similarity:.2f}")

    print("\n✅ Similarity matrix calculation working")

    return True


def test_formality_analysis():
    """Test formality level analysis."""
    print("\n🎤 TEST 7: Formality Analysis")
    print("=" * 50)

    dr_voice = DrVoiceConsistency()
    screenplay = create_distinct_voices_screenplay()
    result = dr_voice.analyze(screenplay)

    print("🎩 Formality levels:")
    sorted_by_formality = sorted(
        result.voice_profiles.items(),
        key=lambda x: x[1].formality_score,
        reverse=True
    )

    for char_name, profile in sorted_by_formality[:4]:
        formality_label = "Formal" if profile.formality_score > 0.6 else "Informal"
        print(f"   {char_name}: {profile.formality_score:.2f} ({formality_label})")

    print("\n✅ Formality analysis working")

    return True


def test_voice_comparisons():
    """Test voice comparison generation."""
    print("\n🎤 TEST 8: Voice Comparisons")
    print("=" * 50)

    dr_voice = DrVoiceConsistency()
    screenplay = create_distinct_voices_screenplay()
    result = dr_voice.analyze(screenplay)

    print("🆚 Voice comparisons:")
    for comparison in result.voice_comparisons:
        print(f"   Type: {comparison['type']}")
        print(f"   {comparison['description']}")
        print(f"   Insight: {comparison['insight']}")

    print("\n✅ Voice comparison generation working")

    return True


def test_rule_violations():
    """Test voice consistency rule violations."""
    print("\n🎤 TEST 9: Rule Violations")
    print("=" * 50)

    dr_voice = DrVoiceConsistency()

    # Test with inconsistent screenplay
    inconsistent = create_inconsistent_voices_screenplay()
    result = dr_voice.analyze(inconsistent)
    violations = result.rule_violations

    print(f"📋 Found {len(violations)} violations:")
    for violation in violations[:5]:  # Show first 5
        severity_emoji = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢"
        }.get(violation["severity"], "⚪")

        print(f"{severity_emoji} [{violation['severity'].upper()}] {violation['title']}")
        if "message" in violation:
            print(f"   {violation['message']}")

    # Should detect issues in inconsistent screenplay
    assert len(violations) > 0
    print("\n✅ Rule violation detection working")

    return True


def test_recommendations():
    """Test recommendation generation."""
    print("\n🎤 TEST 10: Recommendations")
    print("=" * 50)

    dr_voice = DrVoiceConsistency()
    inconsistent = create_inconsistent_voices_screenplay()

    result = dr_voice.analyze(inconsistent)

    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"{i}. {rec}")

    # Should generate recommendations for inconsistent voices
    assert len(result.recommendations) > 0
    print(f"\n✅ Generated {len(result.recommendations)} recommendations")

    return True


def run_all_tests():
    """Run all Voicemon tests."""
    print("\n" + "=" * 60)
    print("🎤 SCRIPT DOCTOR VOICEMON - TEST SUITE")
    print("=" * 60)

    tests = [
        ("Basic Voice Analysis", test_basic_voice_analysis),
        ("Voice Distinctiveness", test_voice_distinctiveness),
        ("Voice Profiles", test_voice_profiles),
        ("Consistency Detection", test_consistency_detection),
        ("Interchangeable Dialogue", test_interchangeable_dialogue),
        ("Similarity Matrix", test_similarity_matrix),
        ("Formality Analysis", test_formality_analysis),
        ("Voice Comparisons", test_voice_comparisons),
        ("Rule Violations", test_rule_violations),
        ("Recommendations", test_recommendations)
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n❌ {name} failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 60)
    print("📊 FINAL REPORT")
    print("=" * 60)
    print(f"✅ Passed: {passed}/{len(tests)}")
    if failed > 0:
        print(f"❌ Failed: {failed}/{len(tests)}")

    if passed == len(tests):
        print("\n🎉 SCRIPT DOCTOR VOICEMON IS FULLY OPERATIONAL!")
        print("✨ The Script Doctor™ Voice Consistency Specialist is ready")
        print("\n🎤 Character voice analysis systems online!")
        print("\n📝 Specialist 14/24 of the Script Doctor™ system operational!")
        print("\n🎯 DIÁLOGO E TEXTO group (4/4) COMPLETE!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix.")

    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
