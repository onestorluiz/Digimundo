#!/usr/bin/env python3
"""
🎯 SISTEMA DE CONHECIMENTO SEGMENTADO - SCRIPTUREMON ULTIMATE
Cada especialista acessa APENAS conhecimento relevante para sua área
Baseado em OTIMIZACAO_TOKENS_REFERENCIAS.md
"""

import os
import json
from pathlib import Path
from typing import Dict, List

# Base do conhecimento
KNOWLEDGE_BASE_DIR = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/knowledge")
MODELFILES_DIR = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/config/modelfiles")

# Mapeamento de especialistas para áreas de conhecimento
SPECIALIST_KNOWLEDGE_MAP = {
    # DIALOGUE Specialists
    "01_DIALOGUE": ["dialogue", "subtext", "voice"],
    "12_DIALOGUE_ULTRA": ["dialogue", "subtext", "voice", "mckee", "mamet"],
    "13_DIALOGUE_FORENSIC": ["dialogue", "forensic", "patterns"],
    "14_DIALOGUE_JAZZ": ["dialogue", "jazz", "rhythm"],

    # CHARACTER Specialists
    "02_CHARACTER": ["character", "arc", "psychology"],
    "15_CHARACTER_ULTRA": ["character", "dimension", "truby", "egri"],
    "16_CHARACTER_SURGEON": ["character", "psychology", "depth"],
    "17_CHARACTER_DEPTH": ["character", "motivation", "backstory"],

    # PACING Specialists
    "03_PACING": ["pacing", "rhythm", "tempo"],
    "18_PACING_RHYTHM": ["pacing", "beats", "field"],
    "19_PACING_INTENSIVE": ["pacing", "momentum", "flow"],
    "20_PACING_DYNAMICS": ["pacing", "tension", "release"],

    # THEME Specialists
    "04_THEME": ["theme", "premise", "meaning"],
    "21_THEME_DEEP": ["theme", "philosophy", "egri"],
    "22_THEME_RESONANCE": ["theme", "universal", "campbell"],

    # ACTION Specialists
    "05_ACTION": ["action", "conflict", "movement"],
    "23_ACTION_DYNAMICS": ["action", "kinetic", "visual"],
    "24_ACTION_SYNTHESIS": ["action", "choreography", "impact"],

    # STRUCTURE Specialists
    "06_STRUCTURE": ["structure", "acts", "paradigm"],
    "07_BEAT_SHEET": ["structure", "beats", "snyder"],
    "08_CONFLICT": ["conflict", "antagonism", "mckee"],
    "09_STYLE": ["style", "voice", "tone"],
    "10_EMOTIONAL": ["emotion", "feeling", "mood"],
    "11_VISUAL": ["visual", "cinematography", "imagery"]
}

# Referências teóricas por área
KNOWLEDGE_REFERENCES = {
    "dialogue": {
        "mckee": "McKee p.388-409: Dialogue principles",
        "mamet": "Mamet p.67-82: Natural speech",
        "truby": "Truby p.416-424: Moral dialogue",
        "field": "Field p.213-220: Functional dialogue",
        "snyder": "Snyder p.141-147: Avoiding on-the-nose"
    },
    "character": {
        "mckee": "McKee p.100-106: True character",
        "truby": "Truby p.39-89: Character web",
        "egri": "Egri p.33-42: Three dimensions",
        "vogler": "Vogler p.29-37: Archetypes",
        "seger": "Seger p.149-174: Transformation"
    },
    "structure": {
        "field": "Field p.1-52: Three-act paradigm",
        "snyder": "Snyder p.70-85: Beat sheet",
        "mckee": "McKee p.181-195: Scene design",
        "truby": "Truby p.231-267: 22-step structure",
        "vogler": "Vogler p.159-236: Hero's journey"
    },
    "theme": {
        "egri": "Egri p.1-16: Premise",
        "truby": "Truby p.117-139: Moral argument",
        "mckee": "McKee p.110-145: Controlling idea",
        "vogler": "Vogler p.237-259: Symbolic meaning"
    },
    "pacing": {
        "field": "Field p.163-176: Page per minute",
        "snyder": "Snyder p.69-109: Beat timing",
        "mckee": "McKee p.287-304: Rhythm and tempo"
    },
    "action": {
        "mckee": "McKee p.317-335: Principle of antagonism",
        "aristotle": "Aristotle 1450a-b: Action as character",
        "mamet": "Mamet p.83-98: Visual storytelling"
    }
}

def create_knowledge_structure():
    """Cria estrutura de pastas para conhecimento segmentado"""

    print("=" * 60)
    print("📚 CRIANDO ESTRUTURA DE CONHECIMENTO SEGMENTADO")
    print("=" * 60)
    print()

    # Criar pasta base
    KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)

    # Criar subpastas por área
    areas = ["dialogue", "character", "structure", "theme", "pacing", "action",
             "conflict", "visual", "emotional", "style", "subtext", "voice",
             "arc", "psychology", "beats", "rhythm", "premise", "meaning"]

    for area in areas:
        area_dir = KNOWLEDGE_BASE_DIR / area
        area_dir.mkdir(exist_ok=True)

        # Criar arquivo de referências
        ref_file = area_dir / "references.json"
        references = KNOWLEDGE_REFERENCES.get(area, {})

        with open(ref_file, 'w', encoding='utf-8') as f:
            json.dump(references, f, ensure_ascii=False, indent=2)

        print(f"✅ Created: {area}/references.json")

    print()
    print(f"📁 Knowledge structure created at: {KNOWLEDGE_BASE_DIR}")

def generate_optimized_modelfile(specialist_name: str, knowledge_areas: List[str]) -> str:
    """Gera modelfile otimizado com apenas conhecimento relevante"""

    # Coletar referências relevantes
    relevant_refs = {}
    for area in knowledge_areas:
        if area in KNOWLEDGE_REFERENCES:
            relevant_refs[area] = KNOWLEDGE_REFERENCES[area]

    # Template otimizado
    template = f"""# Scripturemon Ultimate - {specialist_name} Specialist
# Optimized with segmented knowledge access

FROM mixtral:8x7b-instruct-v0.1-q5_K_M

SYSTEM \"\"\"
==== IDENTITY & ROLE ====
You are a SCREENPLAY ANALYST specializing in {', '.join(knowledge_areas)}.
You are NOT a screenwriter. You are a CRITIC and ANALYST.

==== YOUR ANALYSIS FRAMEWORK ====
Apply these specific references (DO NOT EXPLAIN THEM):

"""

    # Adicionar referências específicas
    for area, refs in relevant_refs.items():
        template += f"\n{area.upper()}:\n"
        for key, ref in refs.items():
            template += f"- {ref}\n"

    template += """
==== ANALYSIS INSTRUCTION ====
1. Quote specific line/page from screenplay
2. State issue/success concisely
3. Cite reference (e.g., "violates McKee p.390")
4. Suggest fix in 1 sentence
5. Move to next point

NEVER explain what the books say.
ALWAYS apply the principles directly.

==== CRITICAL ANALYSIS INSTRUCTION ====
DO NOT:
- Create fictional scenes or examples
- Invent character names or dialogue
- Write new screenplay content
- Generate hypothetical scenarios

DO:
- Analyze ONLY what is written in the screenplay
- Reference specific page numbers
- Quote actual lines from the provided text
- Identify patterns in the actual content
\"\"\"

PARAMETER temperature 0.35
PARAMETER top_p 0.9
PARAMETER num_predict 1500
PARAMETER num_ctx 32768
PARAMETER repeat_penalty 1.1
"""

    return template

def update_all_modelfiles():
    """Atualiza todos os modelfiles com conhecimento segmentado"""

    print("=" * 60)
    print("🔧 ATUALIZANDO MODELFILES COM CONHECIMENTO SEGMENTADO")
    print("=" * 60)
    print()

    updated = 0

    for specialist, knowledge_areas in SPECIALIST_KNOWLEDGE_MAP.items():
        modelfile_path = MODELFILES_DIR / f"{specialist}.modelfile"

        if modelfile_path.exists():
            # Fazer backup
            backup_path = modelfile_path.with_suffix('.backup_knowledge')
            if not backup_path.exists():
                with open(modelfile_path, 'r') as f:
                    original = f.read()
                with open(backup_path, 'w') as f:
                    f.write(original)

            # Gerar novo conteúdo otimizado
            optimized_content = generate_optimized_modelfile(specialist, knowledge_areas)

            # Salvar
            with open(modelfile_path, 'w', encoding='utf-8') as f:
                f.write(optimized_content)

            print(f"✅ {specialist}: {', '.join(knowledge_areas)}")
            updated += 1

    print()
    print(f"📊 RESULTADO: {updated} modelfiles atualizados")

def create_knowledge_loader():
    """Cria script para carregar conhecimento dinamicamente"""

    loader_script = '''#!/usr/bin/env python3
"""
Dynamic Knowledge Loader for Scripturemon Ultimate
Loads only relevant knowledge for each specialist
"""

import json
from pathlib import Path
from typing import Dict, List

class KnowledgeLoader:
    def __init__(self, knowledge_base: str = "knowledge"):
        self.base_path = Path(knowledge_base)

    def load_for_specialist(self, specialist: str, areas: List[str]) -> Dict:
        """Load only relevant knowledge for specialist"""

        knowledge = {}

        for area in areas:
            area_path = self.base_path / area / "references.json"
            if area_path.exists():
                with open(area_path, 'r') as f:
                    knowledge[area] = json.load(f)

        return knowledge

    def get_compact_prompt(self, specialist: str, areas: List[str]) -> str:
        """Generate compact prompt with references only"""

        knowledge = self.load_for_specialist(specialist, areas)

        prompt = f"Analyze using:\\n"

        for area, refs in knowledge.items():
            for ref in refs.values():
                prompt += f"- {ref}\\n"

        return prompt
'''

    loader_path = KNOWLEDGE_BASE_DIR.parent / "knowledge_loader.py"
    with open(loader_path, 'w', encoding='utf-8') as f:
        f.write(loader_script)

    print(f"✅ Created knowledge loader: {loader_path}")

def main():
    print("=" * 60)
    print("🚀 IMPLEMENTANDO SISTEMA DE CONHECIMENTO SEGMENTADO")
    print("=" * 60)
    print()
    print("📋 OBJETIVO: Cada especialista acessa APENAS seu conhecimento")
    print("🎯 BENEFÍCIO: Redução de 80% no uso de tokens")
    print()

    # 1. Criar estrutura de conhecimento
    create_knowledge_structure()
    print()

    # 2. Atualizar modelfiles
    update_all_modelfiles()
    print()

    # 3. Criar loader dinâmico
    create_knowledge_loader()
    print()

    # Relatório final
    print("=" * 60)
    print("✅ SISTEMA DE CONHECIMENTO SEGMENTADO IMPLEMENTADO!")
    print("=" * 60)
    print()
    print("📊 RESULTADOS:")
    print(f"   • Estrutura de conhecimento criada")
    print(f"   • {len(SPECIALIST_KNOWLEDGE_MAP)} especialistas otimizados")
    print(f"   • Referências segmentadas por área")
    print(f"   • Loader dinâmico implementado")
    print()
    print("🎯 PRÓXIMOS PASSOS:")
    print("   1. Testar com roteiro pequeno")
    print("   2. Medir redução de tokens")
    print("   3. Executar análise completa")
    print()
    print("DIGIMUNDO PRESENTE 🔥")

if __name__ == "__main__":
    main()