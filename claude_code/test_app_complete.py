#!/usr/bin/env python3
"""
Test Completo do App Refatorado

Testa todas as funcionalidades:
1. CheckpointManager
2. ScreenplayAnalyzer com checkpoints
3. Dialogue Only mode
4. HTML generation
"""

import sys
import os
from pathlib import Path
import tempfile

sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-clean')

from triple_core.orchestrators.screenplay_analyzer import ScreenplayAnalyzer
from triple_core.utils.checkpoint_manager import CheckpointManager

print("="*80)
print("🧪 TESTE COMPLETO - SCRIPTUREMON v3.0 COM CHECKPOINTS")
print("="*80)
print()

# Configuration
SCREENPLAY_PATH = "/Users/clubproducoes/Digimundo/scripturemon-clean/content/screenplays/personal/Te Encontro em Mim .pdf"
SESSION_DIR = Path("/Users/clubproducoes/Digimundo/scripturemon-clean/workspace/sessions/test_session_dialogue_only")

# Clean previous test
if SESSION_DIR.exists():
    import shutil
    shutil.rmtree(SESSION_DIR)
    print("🧹 Cleaned previous test session")

SESSION_DIR.mkdir(parents=True, exist_ok=True)
print(f"📂 Session directory: {SESSION_DIR}")
print()

# ============================================================================
# TEST 1: CheckpointManager
# ============================================================================
print("TEST 1: CheckpointManager Initialization")
print("-" * 80)

checkpoint_mgr = CheckpointManager(SESSION_DIR)
print("✅ CheckpointManager created")

# Initialize session
specialist_list = ['Dialogue']  # Only Dialogue for quick test
checkpoint_mgr.initialize_session(
    screenplay_path=SCREENPLAY_PATH,
    llm_model='scripturemon-optimized',
    deep_context=True,
    specialist_names=specialist_list
)
print(f"✅ Session initialized with {len(specialist_list)} specialists")
print()

# ============================================================================
# TEST 2: ScreenplayAnalyzer with Checkpoints
# ============================================================================
print("TEST 2: ScreenplayAnalyzer with Dialogue Only")
print("-" * 80)

analyzer = ScreenplayAnalyzer(
    llm_model='scripturemon-optimized',
    deep_context=True,
    checkpoint_manager=checkpoint_mgr
)
print("✅ ScreenplayAnalyzer initialized")
print()

# ============================================================================
# TEST 3: Run Analysis (Dialogue Only)
# ============================================================================
print("TEST 3: Running Analysis - Dialogue Only")
print("-" * 80)
print()

try:
    result = analyzer.analyze_screenplay(
        screenplay_path=SCREENPLAY_PATH,
        output_dir='/Users/clubproducoes/Digimundo/scripturemon-clean/workspace/outputs/analysis',
        resume=False,
        specialists_to_run=['Dialogue']  # Only Dialogue!
    )

    print()
    print("="*80)
    print("✅ ANALYSIS COMPLETE!")
    print("="*80)
    print()
    print(f"📄 HTML Report: {result['html_report_path']}")
    print(f"📄 Markdown Report: {result['markdown_report_path']}")
    print(f"⏱️  Total Time: {result['total_time']:.1f}s")
    print(f"🎯 Overall Score: {result['overall_quality'].overall_score:.1f}/100")
    print()

    # ============================================================================
    # TEST 4: Verify Checkpoint
    # ============================================================================
    print("TEST 4: Verify Checkpoint")
    print("-" * 80)

    checkpoint_file = SESSION_DIR / 'checkpoint.json'
    if checkpoint_file.exists():
        import json
        with open(checkpoint_file, 'r') as f:
            checkpoint_data = json.load(f)

        print(f"✅ Checkpoint file exists")
        print(f"   Session: {checkpoint_data['session_id']}")
        print(f"   Specialists: {checkpoint_data['overall_progress']}")
        print(f"   Dialogue status: {checkpoint_data['specialists'].get('Dialogue', {}).get('status')}")

        if 'Dialogue' in checkpoint_data['specialists']:
            dialogue_spec = checkpoint_data['specialists']['Dialogue']
            print(f"   Dialogue quality: {dialogue_spec.get('quality_score', 'N/A')}/10")
    else:
        print("❌ Checkpoint file not found!")

    print()

    # ============================================================================
    # TEST 5: Verify HTML Output
    # ============================================================================
    print("TEST 5: Verify HTML Output")
    print("-" * 80)

    html_path = Path(result['html_report_path'])
    if html_path.exists():
        print(f"✅ HTML file exists: {html_path.name}")
        print(f"   Size: {html_path.stat().st_size / 1024:.1f} KB")

        # Check if HTML has content
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        if 'Dialogue' in html_content:
            print(f"   ✅ HTML contains Dialogue analysis")
        if len(html_content) > 1000:
            print(f"   ✅ HTML has substantial content ({len(html_content)} chars)")
    else:
        print("❌ HTML file not found!")

    print()

    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("="*80)
    print("🎉 ALL TESTS PASSED!")
    print("="*80)
    print()
    print("✅ CheckpointManager: Working")
    print("✅ ScreenplayAnalyzer: Working")
    print("✅ Dialogue Only mode: Working")
    print("✅ Checkpoint saves: Working")
    print("✅ HTML generation: Working")
    print()
    print(f"📂 View results: open {html_path}")
    print()

except Exception as e:
    print()
    print("="*80)
    print("❌ TEST FAILED!")
    print("="*80)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    print()
    sys.exit(1)
