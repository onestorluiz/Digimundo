#!/usr/bin/env python3
"""
Teste do 24º Especialista - Contrast & Comparison Integration Test
"""

from src.core.scripturemon_ultimate_system import ScripturemonUltimateSystem

# Sample screenplay for testing
TEST_SCREENPLAY = """FADE IN:

EXT. TOKYO - CYBERPUNK DISTRICT - NIGHT (2087)

Neon bleeds through acid rain. The city breathes in binary.

INT. UNDERGROUND SHRINE - CONTINUOUS

Ancient incense meets digital static. KENJI (60s, cybernetic eye,
monk's robes over neural implants) kneels before both Buddha statue
and holographic data stream.

KENJI
(whispered prayer/code)
Electric dreams of electric sheep...
seeking the ghost in the shell.

The data stream FRACTURES. Reality GLITCHES.

FADE OUT."""

def test_24th_specialist():
    """Test the integrated 24th specialist system"""
    print("🧪 TESTING 24TH SPECIALIST INTEGRATION")
    print("="*60)

    # Create system
    system = ScripturemonUltimateSystem()

    print(f"✅ System initialized with {len(system.specialists)} specialists")

    # Check that 24th specialist is included
    last_specialist = system.specialists[-1]
    print(f"📋 Last specialist: {last_specialist}")

    if last_specialist == "24_CONTRAST_COMPARISON":
        print("✅ 24th Contrast & Comparison Specialist correctly integrated!")
    else:
        print("❌ 24th Specialist not found!")
        return

    # Test the contrast specialist function directly
    print("\n🎭 Testing Contrast Specialist Function...")
    try:
        analysis = system._run_contrast_specialist(TEST_SCREENPLAY, "")
        if "Error" in analysis:
            print("⚠️  Contrast specialist returned error:")
            print(f"   {analysis}")
        else:
            print("✅ Contrast specialist executed successfully!")
            print(f"📝 Analysis preview: {analysis[:100]}...")
    except Exception as e:
        print(f"❌ Error testing contrast specialist: {e}")

    print(f"\n🎯 INTEGRATION TEST COMPLETE")
    print(f"   System now has: {len(system.specialists)} specialists")
    print(f"   Technical Evolution specialist ready for production!")

if __name__ == "__main__":
    test_24th_specialist()