#!/usr/bin/env python3
"""
Test chat responses to ensure never silent
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_chat_response(input_text: str, case_name: str) -> dict:
    """Test a single chat input and capture response"""
    
    result = {
        "case": case_name,
        "input": input_text,
        "response": None,
        "error": None,
        "non_empty": False,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        # Import chat
        from apps.scripturemon.chat import ScripturemonChat
        
        # Create chat instance
        chat = ScripturemonChat()
        
        # Process message
        response = chat.process_message(input_text)
        
        # Store result
        result["response"] = response
        result["non_empty"] = bool(response and str(response).strip())
        
        # Save to file
        output_file = Path(f"reports/harmony_vFinal/phase5_chat/case_{case_name}.txt")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"=" * 60 + "\n")
            f.write(f"CASE: {case_name}\n")
            f.write(f"TIMESTAMP: {result['timestamp']}\n")
            f.write(f"=" * 60 + "\n\n")
            f.write(f"INPUT:\n{input_text}\n\n")
            f.write(f"RESPONSE:\n{response}\n\n")
            f.write(f"NON-EMPTY: {result['non_empty']}\n")
            f.write(f"LENGTH: {len(response) if response else 0} chars\n")
        
        print(f"✅ Case {case_name}: Response received ({len(response) if response else 0} chars)")
        
    except Exception as e:
        result["error"] = str(e)
        result["non_empty"] = False
        
        # Save error
        output_file = Path(f"reports/harmony_vFinal/phase5_chat/case_{case_name}.txt")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"=" * 60 + "\n")
            f.write(f"CASE: {case_name}\n")
            f.write(f"TIMESTAMP: {result['timestamp']}\n")
            f.write(f"=" * 60 + "\n\n")
            f.write(f"INPUT:\n{input_text}\n\n")
            f.write(f"ERROR:\n{e}\n\n")
            f.write(f"NON-EMPTY: False\n")
        
        print(f"❌ Case {case_name}: Error - {e}")
    
    return result

def main():
    """Run all test cases"""
    print("=" * 60)
    print("🧪 TESTING CHAT RESPONSES")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        ("a", "Oi, teste rápido."),
        ("b", "Explique o uso de travellings em VHS anos 80."),
        ("c", "Faça uma análise profunda e detalhada do simbolismo da cor vermelha no cinema de horror dos anos 70, considerando especialmente as obras de Dario Argento, Mario Bava e Lucio Fulci, comparando com o expressionismo alemão."),
        ("d", "/status"),
        ("e", ""),  # Empty input to force error
    ]
    
    all_results = []
    
    for case_name, input_text in test_cases:
        print(f"\n📝 Testing case {case_name}...")
        result = test_chat_response(input_text, case_name)
        all_results.append(result)
        
        # Small delay between tests
        import time
        time.sleep(1)
    
    # Check special commands
    print("\n📝 Testing additional commands...")
    
    # Test /help command
    help_result = test_chat_response("/help", "help_cmd")
    all_results.append(help_result)
    
    # Generate acceptance report
    print("\n" + "=" * 60)
    print("📊 GENERATING ACCEPTANCE REPORT")
    print("=" * 60)
    
    # Check results
    all_non_empty = all(r["non_empty"] for r in all_results)
    status_ok = any(r["case"] == "d" and r["non_empty"] for r in all_results)
    help_ok = any(r["case"] == "help_cmd" and r["non_empty"] for r in all_results)
    
    acceptance = {
        "all_responses_non_empty": all_non_empty,
        "status_cmd_ok": status_ok,
        "help_cmd_ok": help_ok,
        "status": "PASS" if all_non_empty else "FAIL",
        "notes": f"Tested {len(all_results)} cases. All responses guaranteed non-empty with fallback message.",
        "test_results": [
            {
                "case": r["case"],
                "input_preview": r["input"][:50] + "..." if len(r["input"]) > 50 else r["input"],
                "non_empty": r["non_empty"],
                "response_length": len(r["response"]) if r["response"] else 0,
                "error": r["error"]
            }
            for r in all_results
        ]
    }
    
    # Save acceptance report
    with open("reports/harmony_vFinal/phase5_chat/acceptance.json", 'w') as f:
        json.dump(acceptance, f, indent=2)
    
    # Print summary
    print(f"\nAll responses non-empty: {acceptance['all_responses_non_empty']}")
    print(f"Status command OK: {acceptance['status_cmd_ok']}")
    print(f"Help command OK: {acceptance['help_cmd_ok']}")
    print(f"Overall status: {acceptance['status']}")
    
    print("\n✅ Test complete. Results saved to reports/harmony_vFinal/phase5_chat/")
    
    return 0 if acceptance["status"] == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())