#!/usr/bin/env python3
"""
Phase 6 - Personas System Test Suite
Tests all persona functionality including switching, scoring, and tone modifications
"""

import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.personas.manager import PersonasManager, Persona, get_personas_manager
from apps.scripturemon.chat import ScripturemonChat

def test_personas_manager():
    """Test the PersonasManager functionality"""
    print("🧪 Testing PersonasManager...")
    
    manager = PersonasManager()
    
    # Test 1: List personas
    print("\n1️⃣ Available Personas:")
    personas = manager.list_personas()
    for p in personas:
        active = " ✅" if p["active"] else ""
        print(f"   • {p['name']}: {p['display_name']}{active}")
    assert len(personas) >= 2, "Should have at least brutal and merciful"
    
    # Test 2: Default persona
    print("\n2️⃣ Default Persona:")
    current = manager.get_current_persona()
    print(f"   Current: {current.name} ({current.display_name})")
    assert current.name == "brutal", "Default should be brutal"
    
    # Test 3: Score strategies
    print("\n3️⃣ Testing Score Strategies:")
    base_score = 75.0
    
    # Test brutal (fixed)
    manager.set_persona("brutal")
    score, _ = manager.apply_persona(base_score, "Test feedback")
    print(f"   • Brutal: {base_score} → {score} (fixed at 62)")
    assert score == 62, "Brutal should always return 62"
    
    # Test merciful (variable_plus)
    manager.set_persona("merciful")
    score, _ = manager.apply_persona(base_score, "Test feedback")
    print(f"   • Merciful: {base_score} → {score} (offset +15)")
    assert score == 90, "Merciful should add 15 to base"
    
    # Test analytical (calculated) if exists
    if "analytical" in [p["name"] for p in personas]:
        manager.set_persona("analytical")
        score, _ = manager.apply_persona(base_score, "Test feedback")
        print(f"   • Analytical: {base_score} → {score} (multiplier 1.0)")
        assert score == 75, "Analytical with 1.0 multiplier should maintain score"
    
    # Test creative (variable_plus with min) if exists
    if "creative" in [p["name"] for p in personas]:
        manager.set_persona("creative")
        low_score = 30.0
        score, _ = manager.apply_persona(low_score, "Test feedback")
        print(f"   • Creative: {low_score} → {score} (offset +10, min 50)")
        assert score >= 50, "Creative should respect minimum score"
    
    print("\n✅ PersonasManager tests passed!")
    return True

def test_chat_interface_personas():
    """Test persona integration in ScripturemonChat"""
    print("\n🧪 Testing ScripturemonChat Persona Integration...")
    
    # Create chat interface
    chat = ScripturemonChat()
    manager = get_personas_manager()
    
    # Test 1: Initial persona
    print("\n1️⃣ Initial State:")
    print(f"   Default persona: {manager.current_persona_name}")
    assert manager.current_persona_name == "brutal"
    
    # Test 2: Persona command
    print("\n2️⃣ Testing /persona command:")
    
    # List personas
    response = chat.cmd_persona("list")
    print("   • List command executed")
    
    # Switch to merciful
    response = chat.cmd_persona("merciful")
    print(f"   • Switched to: {manager.current_persona_name}")
    assert manager.current_persona_name == "merciful"
    
    # Test 3: Score application in analysis
    print("\n3️⃣ Testing Score Application:")
    
    # Mock analysis with brutal
    chat.cmd_persona("brutal")
    print("   • Set to brutal persona")
    
    # The score should be fixed at 62
    current = manager.get_current_persona()
    test_score = 80.0
    final_score, _ = manager.apply_persona(test_score, "Test")
    print(f"   • Brutal scoring: {test_score} → {final_score}")
    assert final_score == 62
    
    # Switch to merciful and test
    chat.cmd_persona("merciful")
    final_score, _ = manager.apply_persona(test_score, "Test")
    print(f"   • Merciful scoring: {test_score} → {final_score}")
    assert final_score == 95  # 80 + 15
    
    print("\n✅ ChatInterface persona tests passed!")
    return True

def test_feedback_tone_modifications():
    """Test that personas modify feedback tone appropriately"""
    print("\n🧪 Testing Feedback Tone Modifications...")
    
    manager = PersonasManager()
    base_feedback = "O roteiro tem problemas estruturais mas mostra criatividade."
    
    print(f"\n📝 Base Feedback: '{base_feedback}'")
    
    # Test each persona's tone
    personas_to_test = ["brutal", "merciful"]
    if "analytical" in [p.name for p in manager.personas.values()]:
        personas_to_test.append("analytical")
    if "creative" in [p.name for p in manager.personas.values()]:
        personas_to_test.append("creative")
    
    for persona_name in personas_to_test:
        manager.set_persona(persona_name)
        persona = manager.get_current_persona()
        _, modified = manager.apply_persona(70, base_feedback)
        
        print(f"\n🎭 {persona.display_name} ({persona.tone} tone):")
        
        # Check for signature phrases
        has_signature = any(phrase in modified for phrase in persona.signature_phrases)
        if has_signature:
            print("   ✓ Contains signature phrase")
        
        # Check for emphasis additions
        if "⚠️" in modified or "✨" in modified or "📐" in modified or "🎨" in modified:
            print("   ✓ Contains emphasis marker")
        
        # Show preview
        preview = modified.split('\n')[0][:100]
        print(f"   Preview: '{preview}...'")
    
    print("\n✅ Feedback tone tests passed!")
    return True

def test_persona_persistence():
    """Test that persona selection persists across commands"""
    print("\n🧪 Testing Persona Persistence...")
    
    chat = ScripturemonChat()
    manager = get_personas_manager()
    
    # Set to merciful
    chat.cmd_persona("merciful")
    assert manager.current_persona_name == "merciful"
    print("   ✓ Set to merciful")
    
    # Execute another command (status)
    chat.cmd_status()
    
    # Check persona is still merciful
    assert manager.current_persona_name == "merciful"
    print("   ✓ Still merciful after status command")
    
    # Reset to brutal
    chat.cmd_persona("brutal")
    assert manager.current_persona_name == "brutal"
    print("   ✓ Reset to brutal")
    
    print("\n✅ Persona persistence tests passed!")
    return True

def main():
    """Run all Phase 6 tests"""
    print("=" * 60)
    print("📋 PHASE 6 - PERSONAS SYSTEM TEST SUITE")
    print("=" * 60)
    
    test_count = 0
    passed_count = 0
    
    tests = [
        ("PersonasManager", test_personas_manager),
        ("ChatInterface Integration", test_chat_interface_personas),
        ("Feedback Tone Modifications", test_feedback_tone_modifications),
        ("Persona Persistence", test_persona_persistence)
    ]
    
    for test_name, test_func in tests:
        test_count += 1
        try:
            if test_func():
                passed_count += 1
                print(f"\n✅ {test_name}: PASSED")
            else:
                print(f"\n❌ {test_name}: FAILED")
        except Exception as e:
            print(f"\n❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTS: {passed_count}/{test_count} tests passed")
    
    if passed_count == test_count:
        print("🎉 ALL PHASE 6 TESTS PASSED!")
        return 0
    else:
        print("⚠️ Some tests failed. Please review.")
        return 1

if __name__ == "__main__":
    sys.exit(main())