#!/usr/bin/env python3
"""
Teste de Integração: Importação e Instanciação de Todos os 22 Especialistas Triple-Core
"""

import sys

print("="*80)
print("🧪 TESTE DE INTEGRAÇÃO - Todos os 22 Especialistas Triple-Core")
print("="*80)
print()

# Lista de todos os especialistas migrados
specialists = [
    ("Action Description", "triple_core.core_1_specialists.action.dr_action", "DrAction"),
    ("Character Arcs", "triple_core.core_1_specialists.character.arcs.dr_arcs", "DrCharacterArcs"),
    ("Character Psychology", "triple_core.core_1_specialists.character.psychology.dr_psychology", "DrCharacterPsychology"),
    ("Character Relationships", "triple_core.core_1_specialists.character.relationships.dr_relationships", "DrRelationships"),
    ("Climax", "triple_core.core_1_specialists.climax.dr_climax", "DrClimax"),
    ("Dialogue", "triple_core.core_1_specialists.dialogue.dr_dialogue", "DrDialogue"),
    ("Formatting", "triple_core.core_1_specialists.formatting.dr_formatting", "DrFormatting"),
    ("Genre Conventions", "triple_core.core_1_specialists.genre.dr_genre", "DrGenreConventions"),
    ("Market Potential", "triple_core.core_1_specialists.market.dr_market_potential", "DrMarketPotential"),
    ("Opening", "triple_core.core_1_specialists.opening.dr_opening", "DrOpening"),
    ("Originality", "triple_core.core_1_specialists.originality.dr_originality", "DrOriginalityAssessment"),
    ("Pacing", "triple_core.core_1_specialists.pacing.dr_pacing", "DrPacing"),
    ("Resolution", "triple_core.core_1_specialists.resolution.dr_resolution", "DrResolution"),
    ("Structure", "triple_core.core_1_specialists.structure.dr_structure", "DrStructure"),
    ("Subtext", "triple_core.core_1_specialists.subtext.dr_subtext", "DrSubtext"),
    ("Symbolism", "triple_core.core_1_specialists.symbolism.dr_symbolism", "DrSymbolism"),
    ("Theme Consistency", "triple_core.core_1_specialists.theme.dr_theme", "DrTheme"),
    ("Tone Consistency", "triple_core.core_1_specialists.tone.dr_tone", "DrTone"),
    ("Transitions", "triple_core.core_1_specialists.transitions.dr_transitions", "DrTransitions"),
    ("Visual Motifs", "triple_core.core_1_specialists.visual.dr_visual_motifs", "DrVisualMotifs"),
    ("Voice Consistency", "triple_core.core_1_specialists.voice.dr_voice", "DrVoice"),
    ("World Building", "triple_core.core_1_specialists.worldbuilding.dr_worldbuilding", "DrWorldBuilding"),
]

print(f"📋 Total de especialistas a testar: {len(specialists)}")
print()

successful = []
failed = []

for i, (name, module_path, class_name) in enumerate(specialists, 1):
    try:
        print(f"[{i:2d}/22] Testando {name}...", end=" ")

        # Importar módulo
        module = __import__(module_path, fromlist=[class_name])

        # Obter classe
        specialist_class = getattr(module, class_name)

        # Instanciar
        specialist = specialist_class()

        # Verificar se tem método analyze
        if not hasattr(specialist, 'analyze'):
            raise AttributeError(f"{class_name} não tem método analyze()")

        print("✅")
        successful.append(name)

    except Exception as e:
        print(f"❌ ERRO: {e}")
        failed.append((name, str(e)))

print()
print("="*80)
print("📊 RESULTADOS")
print("="*80)
print()

print(f"✅ Sucessos: {len(successful)}/22")
print(f"❌ Falhas: {len(failed)}/22")
print()

if failed:
    print("❌ ESPECIALISTAS COM FALHA:")
    for name, error in failed:
        print(f"   • {name}: {error}")
    print()
    print("❌ TESTE FALHOU!")
    sys.exit(1)
else:
    print("="*80)
    print("✅ TESTE PASSOU! Todos os 22 especialistas foram importados e instanciados com sucesso!")
    print("="*80)
    print()
    print("Especialistas verificados:")
    for i, name in enumerate(successful, 1):
        print(f"   {i:2d}. {name}")
    print()
    print("🎉 Triple-Core Migration 100% COMPLETA!")
    sys.exit(0)
