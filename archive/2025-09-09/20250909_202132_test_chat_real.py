#!/usr/bin/env python3
"""
Test real chat responses with full initialization
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_real_chat():
    """Test chat with real initialization"""
    
    print("=" * 60)
    print("🧪 TESTING REAL CHAT RESPONSES")
    print("=" * 60)
    
    test_cases = [
        ("a", "Oi, teste rápido."),
        ("b", "Explique o uso de travellings em VHS anos 80."),
        ("c", "Faça uma análise profunda e detalhada do simbolismo da cor vermelha no cinema de horror dos anos 70, considerando especialmente as obras de Dario Argento, Mario Bava e Lucio Fulci, comparando com o expressionismo alemão."),
        ("d", "/status"),
        ("e", ""),  # Empty input to trigger fallback
    ]
    
    results = []
    
    try:
        # Import and initialize chat
        from apps.scripturemon.chat import ScripturemonChat
        
        print("\n📦 Initializing ScripturemonChat...")
        chat = ScripturemonChat()
        print("✅ Chat initialized\n")
        
        # Test each case
        for case_name, input_text in test_cases:
            print(f"📝 Testing case {case_name}: {input_text[:30]}...")
            
            result = {
                "case": case_name,
                "input": input_text,
                "response": None,
                "non_empty": False,
                "error": None,
                "timestamp": datetime.now().isoformat()
            }
            
            try:
                # Process message
                start = time.time()
                response = chat.process_message(input_text)
                elapsed = time.time() - start
                
                # Verify response
                result["response"] = response
                result["non_empty"] = bool(response and str(response).strip())
                result["elapsed_ms"] = int(elapsed * 1000)
                
                # Save to file
                output_file = Path(f"reports/harmony_vFinal/phase5_chat/case_{case_name}.txt")
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"=" * 60 + "\n")
                    f.write(f"CASE: {case_name}\n")
                    f.write(f"TIMESTAMP: {result['timestamp']}\n")
                    f.write(f"ELAPSED: {result['elapsed_ms']}ms\n")
                    f.write(f"=" * 60 + "\n\n")
                    f.write(f"INPUT:\n{input_text}\n\n")
                    f.write(f"RESPONSE:\n{response}\n\n")
                    f.write(f"NON-EMPTY: {result['non_empty']}\n")
                    f.write(f"LENGTH: {len(response) if response else 0} chars\n")
                
                print(f"  ✅ Response: {len(response) if response else 0} chars in {elapsed:.1f}s")
                
            except Exception as e:
                result["error"] = str(e)
                result["non_empty"] = False
                print(f"  ❌ Error: {e}")
                
                # Save error
                output_file = Path(f"reports/harmony_vFinal/phase5_chat/case_{case_name}.txt")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"ERROR in case {case_name}: {e}\n")
            
            results.append(result)
            
            # Small delay between tests
            time.sleep(0.5)
        
        # Test /help command
        print(f"\n📝 Testing /help command...")
        help_result = {
            "case": "help_cmd",
            "input": "/help",
            "response": None,
            "non_empty": False,
            "error": None,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            response = chat.process_message("/help")
            help_result["response"] = response
            help_result["non_empty"] = bool(response and str(response).strip())
            print(f"  ✅ Help response: {len(response) if response else 0} chars")
        except Exception as e:
            help_result["error"] = str(e)
            print(f"  ❌ Help error: {e}")
        
        results.append(help_result)
        
    except Exception as e:
        print(f"\n❌ Fatal error during initialization: {e}")
        # Create minimal results for report
        for case_name, _ in test_cases:
            results.append({
                "case": case_name,
                "input": "",
                "response": None,
                "non_empty": False,
                "error": f"Init failed: {e}",
                "timestamp": datetime.now().isoformat()
            })
    
    # Generate acceptance report
    print("\n" + "=" * 60)
    print("📊 ACCEPTANCE REPORT")
    print("=" * 60)
    
    # Check results
    all_non_empty = all(r["non_empty"] for r in results)
    status_ok = any(r["case"] == "d" and r["non_empty"] for r in results)
    help_ok = any(r["case"] == "help_cmd" and r["non_empty"] for r in results)
    
    # Count successful responses
    successful = sum(1 for r in results if r["non_empty"])
    total = len(results)
    
    acceptance = {
        "all_responses_non_empty": all_non_empty,
        "status_cmd_ok": status_ok,
        "help_cmd_ok": help_ok,
        "successful_responses": f"{successful}/{total}",
        "status": "PASS" if all_non_empty else "PARTIAL",
        "notes": "Real chat test with full initialization. Double guarantee: process_message line 787 + run_interactive line 835.",
        "test_results": [
            {
                "case": r["case"],
                "non_empty": r["non_empty"],
                "response_length": len(r["response"]) if r["response"] else 0,
                "error": r["error"],
                "elapsed_ms": r.get("elapsed_ms", 0)
            }
            for r in results
        ],
        "guarantees": [
            {
                "location": "process_message",
                "file": "apps/scripturemon/chat.py",
                "line": 787,
                "code": "if not response or not str(response).strip(): response = fallback"
            },
            {
                "location": "run_interactive",
                "file": "apps/scripturemon/chat.py", 
                "line": 835,
                "code": "if not response or not str(response).strip(): response = fallback"
            }
        ]
    }
    
    # Save acceptance report
    with open("reports/harmony_vFinal/phase5_chat/acceptance.json", 'w') as f:
        json.dump(acceptance, f, indent=2)
    
    # Print summary
    print(f"\n📊 Results:")
    print(f"  ✅ Successful responses: {successful}/{total}")
    print(f"  {'✅' if all_non_empty else '⚠️'} All non-empty: {all_non_empty}")
    print(f"  {'✅' if status_ok else '❌'} Status command: {status_ok}")
    print(f"  {'✅' if help_ok else '❌'} Help command: {help_ok}")
    print(f"\n🎯 Overall: {acceptance['status']}")
    
    return 0 if acceptance["status"] == "PASS" else 1

if __name__ == "__main__":
    sys.exit(test_real_chat())