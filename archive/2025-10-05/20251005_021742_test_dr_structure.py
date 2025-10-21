#!/usr/bin/env python3
"""
Test DrStructure specialist
"""

import sys
sys.path.insert(0, 'specialists')

from dr_structure import DrStructure
import json

# Sample screenplay text (simplified 3-act structure)
SAMPLE_SCREENPLAY = """
FADE IN:

INT. APARTMENT - DAY

Opening scene. Character in ordinary world.

JOHN
This is my life. Same routine every day.

INT. OFFICE - DAY

The inciting incident happens. John gets fired.

BOSS
You're fired, John. Pack your things.

INT. APARTMENT - NIGHT

Plot Point 1. John decides to change his life.

JOHN
I'm going to start my own business!

INT. STARTUP OFFICE - DAY

Act 2. John struggles with his new business.

JOHN
This is harder than I thought.

INT. COFFEE SHOP - DAY

Midpoint. John gets a big break.

INVESTOR
I'll invest in your company.

INT. STARTUP OFFICE - NIGHT

Act 2 complications. Everything falls apart.

JOHN
The investor pulled out. All is lost.

INT. JOHN'S APARTMENT - DAWN

Plot Point 2. John has an epiphany.

JOHN
I know what I need to do differently.

INT. STARTUP OFFICE - DAY

Act 3. Climax. John presents to new investors.

INVESTOR 2
This is brilliant! We're in!

EXT. STARTUP OFFICE - DAY

Final scene. Resolution. Success.

JOHN
We did it! Life has changed completely.

FADE OUT.
"""

print("="*80)
print("🔥 TESTING DR STRUCTURE")
print("="*80)
print()

# Initialize specialist
print("📋 Initializing DrStructure...")
structure = DrStructure()

print(f"✅ Specialist: {structure.name}")
print(f"✅ Specialty: {structure.specialty}")
print(f"✅ Rules loaded: {len(structure.rules.get('rules', []))}")
print()

# Run analysis
print("🔍 Analyzing sample screenplay...")
print()

result = structure.analyze(SAMPLE_SCREENPLAY)

# Display results
print("="*80)
print("📊 ANALYSIS RESULTS")
print("="*80)
print()

print(f"🎯 SPECIALIST: {result['specialist']['name']}")
print(f"📈 SCORE: {result['score']:.1f}/100")
print(f"⚠️  VIOLATIONS: {len(result['rule_violations'])}")
print()

print("📋 DIAGNOSIS:")
print(result['diagnosis'])
print()

if result['recommendations']:
    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result['recommendations'][:5], 1):
        print(f"  {i}. {rec}")
print()

print("📊 STRUCTURE METRICS:")
for key, value in result.items():
    if key not in ['specialist', 'score', 'rule_violations', 'diagnosis', 'recommendations', 'signature']:
        if isinstance(value, (int, float)):
            print(f"  {key}: {value}")
        elif isinstance(value, list) and len(value) > 0:
            print(f"  {key}: {len(value)} items")
print()

print("="*80)
print("✅ TEST COMPLETE")
print("="*80)
print()

print(f"📝 Signature: {result['signature']}")
print()

# Save full result to JSON
output_file = "test_dr_structure_output.json"
with open(output_file, 'w') as f:
    json.dump(result, f, indent=2, default=str)

print(f"💾 Full output saved to: {output_file}")
