#!/usr/bin/env python3
"""
TEST COMPLETE SCRIPTUREMON ULTIMATE SYSTEM
Teste completo do sistema sequencial com arquivo único
"""

import json
import logging
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Script de teste - Marcus's revenge story
TEST_SCRIPT = """INT. ABANDONED CHURCH - NIGHT

Rain pounds the broken windows. MARCUS CHEN (40s), haunted eyes,
enters the decrepit sanctuary. His footsteps echo.

FATHER MARTINEZ (60s) kneels at the altar, praying.

                    FATHER MARTINEZ
          I've been expecting you, Marcus.

Marcus pulls out a SYRINGE filled with black liquid.

                    MARCUS
          Forty years ago, you and the others
          destroyed three boys at St. Mary's.
          Tommy. Michael. James.

                    FATHER MARTINEZ
          That was... a different time. I've
          changed. I've repented.

                    MARCUS
          They killed themselves. One by one.
          Fourteen. Fifteen. Sixteen years old.

Marcus steps closer. Thunder EXPLODES outside.

                    MARCUS (CONT'D)
          I promised them justice. The kind
          that doesn't wait forty years.

                    FATHER MARTINEZ
          You're not a killer, Marcus. You're
          a good man. Your mother raised you—

                    MARCUS
          My mother signed the papers. She
          sent me to that place. To you.

He raises the syringe.

                    MARCUS (CONT'D)
          This is the same drug you used on us.
          To make us "compliant." Remember?

Martinez's eyes widen in recognition and terror.

                    FATHER MARTINEZ
          Please... I have a family now...

                    MARCUS
          So did they.

FADE TO BLACK."""

def check_models():
    """Verifica modelos disponíveis"""
    logger.info("Checking available models...")
    
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True
        )
        
        models = result.stdout
        logger.info("Available models:")
        for line in models.split('\n')[1:]:  # Skip header
            if line.strip():
                logger.info(f"  {line.split()[0]}")
        
        # Verificar modelos essenciais
        has_mixtral = 'mixtral' in models.lower()
        has_70b = '70b' in models.lower()
        
        if has_mixtral:
            logger.info("✅ Mixtral model found (for specialists)")
        else:
            logger.warning("⚠️ Mixtral not found - specialists may run slower")
        
        if has_70b:
            logger.info("✅ 70B model found (for final synthesis)")
        else:
            logger.warning("⚠️ 70B model not found - synthesis may be less accurate")
        
        return has_mixtral, has_70b
        
    except Exception as e:
        logger.error(f"Error checking models: {e}")
        return False, False

def verify_specialists():
    """Verifica que todos os 23 especialistas existem"""
    logger.info("\nVerifying specialist files...")
    
    specialists_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/super_specialists")
    
    expected_specialists = [
        "01_DIALOGUE", "02_CHARACTER", "03_PACING", "04_THEME", "05_ACTION",
        "06_STRUCTURE", "07_CONFLICT", "08_TENSION", "09_SUBTEXT", "10_EXPOSITION",
        "11_TRANSITIONS", "12_OPENING", "13_CLIMAX", "14_RESOLUTION", "15_WORLD-BUILDING",
        "16_STAKES", "17_MOTIVATION", "18_BACKSTORY", "19_FORESHADOWING", "20_TWIST",
        "21_SYMBOLISM", "22_TONE", "23_GENRE"
    ]
    
    found_count = 0
    missing = []
    
    for specialist in expected_specialists:
        num, name = specialist.split('_', 1)
        pattern = f"{num}_{name}_*.md"
        files = list(specialists_dir.glob(pattern))
        
        if files:
            found_count += 1
            logger.info(f"  ✅ {specialist}: {files[0].name}")
        else:
            missing.append(specialist)
            logger.warning(f"  ❌ {specialist}: NOT FOUND")
    
    logger.info(f"\nSpecialists found: {found_count}/23")
    
    if missing:
        logger.warning(f"Missing specialists: {', '.join(missing)}")
    
    return found_count == 23

def test_single_specialist():
    """Testa um único especialista para verificar funcionamento"""
    logger.info("\n" + "="*60)
    logger.info("TESTING SINGLE SPECIALIST (DIALOGUE)")
    logger.info("="*60)
    
    from scripturemon_ultimate_system import ScripturemonUltimateSystem
    
    system = ScripturemonUltimateSystem()
    
    # Testar apenas DIALOGUE
    specialist = "01_DIALOGUE"
    
    logger.info(f"Running {specialist} analysis...")
    start = time.time()
    
    try:
        # Simular análise de um especialista
        analysis = system._run_specialist(
            specialist,
            TEST_SCRIPT,
            ""  # Sem contexto anterior
        )
        
        elapsed = time.time() - start
        
        if analysis and len(analysis) > 100:
            logger.info(f"✅ Analysis complete in {elapsed:.1f}s")
            logger.info(f"   Word count: {len(analysis.split())}")
            logger.info(f"   Preview: {analysis[:200]}...")
            return True
        else:
            logger.error(f"❌ Analysis failed or too short")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

def test_context_passing():
    """Testa passagem de contexto entre especialistas"""
    logger.info("\n" + "="*60)
    logger.info("TESTING CONTEXT PASSING")
    logger.info("="*60)
    
    from scripturemon_ultimate_system import ScripturemonUltimateSystem
    
    system = ScripturemonUltimateSystem()
    
    # Simular análise de DIALOGUE
    dialogue_analysis = """The dialogue reveals deep trauma through subtext.
Marcus's lines are sparse but loaded with meaning.
The confrontation builds through verbal sparring."""
    
    # Preparar contexto para CHARACTER
    context = system._prepare_context(f"\n\n## 01_DIALOGUE\n{dialogue_analysis}", True)
    
    logger.info("Testing CHARACTER with DIALOGUE context...")
    
    try:
        analysis = system._run_specialist(
            "02_CHARACTER",
            TEST_SCRIPT,
            context
        )
        
        # Verificar se CHARACTER menciona DIALOGUE
        if "dialogue" in analysis.lower() or "verbal" in analysis.lower():
            logger.info("✅ Context passing works - CHARACTER referenced DIALOGUE")
            return True
        else:
            logger.warning("⚠️ Context may not be working - no reference found")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

def test_report_generation():
    """Testa geração de relatório"""
    logger.info("\n" + "="*60)
    logger.info("TESTING REPORT GENERATION")
    logger.info("="*60)
    
    from scripturemon_ultimate_system import ScripturemonUltimateSystem
    
    system = ScripturemonUltimateSystem()
    
    # Criar arquivo de teste
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = Path(f"test_report_{timestamp}.md")
    
    # Inicializar relatório
    system._initialize_report(report_file, "TEST_SCRIPT", timestamp)
    
    # Adicionar análise de teste
    system._append_to_report(
        report_file,
        "01_DIALOGUE",
        "Test dialogue analysis content."
    )
    
    # Verificar se arquivo foi criado
    if report_file.exists():
        content = report_file.read_text()
        if "SCRIPTUREMON ULTIMATE" in content and "01 DIALOGUE" in content:
            logger.info(f"✅ Report file created successfully: {report_file}")
            # Limpar arquivo de teste
            report_file.unlink()
            return True
        else:
            logger.error("❌ Report file missing expected content")
            return False
    else:
        logger.error("❌ Report file not created")
        return False

def test_mini_run():
    """Executa mini análise com 3 especialistas"""
    logger.info("\n" + "="*60)
    logger.info("MINI RUN TEST (3 SPECIALISTS)")
    logger.info("="*60)
    
    from scripturemon_ultimate_system import ScripturemonUltimateSystem
    
    # Modificar temporariamente para usar apenas 3 especialistas
    system = ScripturemonUltimateSystem()
    system.specialists = system.specialists[:3]  # Apenas DIALOGUE, CHARACTER, PACING
    
    logger.info("Running mini analysis with 3 specialists...")
    start = time.time()
    
    try:
        report_file = system.analyze_screenplay(TEST_SCRIPT, "MINI_TEST")
        elapsed = time.time() - start
        
        logger.info(f"✅ Mini run complete in {elapsed:.1f}s")
        logger.info(f"   Report: {report_file}")
        
        # Verificar conteúdo
        content = Path(report_file).read_text()
        has_dialogue = "01 DIALOGUE" in content or "DIALOGUE" in content
        has_character = "02 CHARACTER" in content or "CHARACTER" in content
        has_pacing = "03 PACING" in content or "PACING" in content
        
        if has_dialogue and has_character and has_pacing:
            logger.info("✅ All 3 specialists present in report")
            return True
        else:
            logger.warning("⚠️ Some specialists missing from report")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

def main():
    """Executa suite completa de testes"""
    print("\n" + "#"*60)
    print("# SCRIPTUREMON ULTIMATE - COMPLETE SYSTEM TEST")
    print("#"*60)
    
    results = {}
    
    # 1. Verificar modelos
    logger.info("\n[TEST 1/6] Model Availability")
    has_mixtral, has_70b = check_models()
    results['models'] = has_mixtral or has_70b
    
    # 2. Verificar especialistas
    logger.info("\n[TEST 2/6] Specialist Files")
    results['specialists'] = verify_specialists()
    
    # 3. Testar um especialista
    logger.info("\n[TEST 3/6] Single Specialist")
    results['single'] = test_single_specialist()
    
    # 4. Testar contexto
    logger.info("\n[TEST 4/6] Context Passing")
    results['context'] = test_context_passing()
    
    # 5. Testar relatório
    logger.info("\n[TEST 5/6] Report Generation")
    results['report'] = test_report_generation()
    
    # 6. Mini run
    logger.info("\n[TEST 6/6] Mini Run (3 Specialists)")
    results['mini_run'] = test_mini_run()
    
    # Resumo final
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = 0
    for test, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test.upper():15} {status}")
        if result:
            passed += 1
    
    print("\n" + "-"*40)
    print(f"TOTAL: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED! System is ready for full analysis.")
        print("\nTo run full analysis:")
        print("python scripturemon_ultimate_system.py <screenplay_file>")
    elif passed >= 4:
        print("\n⚠️ MOSTLY WORKING - Some features may have issues.")
    else:
        print("\n❌ CRITICAL ISSUES - System needs fixes before use.")
    
    print("="*60)

if __name__ == "__main__":
    main()