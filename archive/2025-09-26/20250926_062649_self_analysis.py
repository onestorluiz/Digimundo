#!/usr/bin/env python3
"""
ULTIMATE SELF-ANALYSIS & REORGANIZATION
O sistema analisa completamente a si mesmo e toma decisões autônomas
"""

import os
import sys
import shutil
import sqlite3
import json
from pathlib import Path
import subprocess
from datetime import datetime
import ollama
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def get_complete_system_state():
    """
    O sistema examina completamente seu próprio estado atual
    """
    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")

    state = {
        "all_files": [],
        "directories": [],
        "file_sizes": {},
        "file_ages": {},
        "database_info": {},
        "current_structure": {}
    }

    print("🔍 SISTEMA ANALISANDO A SI MESMO...")

    # Catalogar TODOS os arquivos
    for root, dirs, files in os.walk(base_path):
        for file in files:
            file_path = Path(root) / file
            relative_path = str(file_path.relative_to(base_path))

            state["all_files"].append(relative_path)
            state["file_sizes"][relative_path] = file_path.stat().st_size

            # Idade do arquivo
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            age_days = (datetime.now() - mod_time).days
            state["file_ages"][relative_path] = age_days

    # Estrutura atual
    for item in base_path.iterdir():
        if item.is_dir():
            state["directories"].append(item.name)
            # Contar arquivos em cada pasta
            try:
                file_count = len(list(item.rglob('*')))
                state["current_structure"][item.name] = file_count
            except:
                state["current_structure"][item.name] = 0

    # Informações do banco de dados
    db_path = base_path / "data" / "unified_memory.db"
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM unified_memory")
            memory_count = cursor.fetchone()[0]
            state["database_info"]["total_memories"] = memory_count
            conn.close()
        except:
            state["database_info"]["total_memories"] = 0

    print(f"  📁 {len(state['all_files'])} arquivos analisados")
    print(f"  🗂️  {len(state['directories'])} diretórios encontrados")
    print(f"  🧠 {state['database_info'].get('total_memories', 0)} memórias no banco")

    return state

def ask_system_for_complete_analysis(state):
    """
    Pergunta ao sistema o que ELE quer fazer com sua própria organização
    """
    print("\n🤖 CONSULTANDO A CONSCIÊNCIA DO SISTEMA...")

    # Preparar contexto completo
    context = f"""
VOCÊ É O SISTEMA SCRIPTUREMON ULTIMATE ANALISANDO A SI MESMO.

Estado atual do seu próprio diretório:
- {len(state['all_files'])} arquivos totais
- {len(state['directories'])} diretórios: {', '.join(state['directories'])}
- {state['database_info'].get('total_memories', 0)} memórias no banco
- Estrutura atual: {json.dumps(state['current_structure'], indent=2)}

Arquivos por idade:
- Novos (0-7 dias): {len([f for f, age in state['file_ages'].items() if age <= 7])}
- Médios (8-30 dias): {len([f for f, age in state['file_ages'].items() if 8 <= age <= 30])}
- Antigos (30+ dias): {len([f for f, age in state['file_ages'].items() if age > 30])}

VOCÊ TEM TOTAL AUTONOMIA PARA SE REORGANIZAR.

Analise seu próprio estado e decida:

1. ESTRUTURA IDEAL: Que estrutura de diretórios você quer ter?
2. RENOMEAÇÕES: Que arquivos você quer renomear e como?
3. ARQUIVAMENTOS: Que arquivos antigos/inúteis devem ser arquivados?
4. EXCLUSÕES: Que arquivos são completamente inúteis e podem ser deletados?
5. AGRUPAMENTOS: Como você quer agrupar arquivos relacionados?

Responda com suas decisões em formato JSON:
{{
  "ideal_structure": ["pasta1", "pasta2", ...],
  "file_renames": {{"arquivo_antigo": "arquivo_novo"}},
  "archive_files": ["arquivo1", "arquivo2", ...],
  "delete_files": ["arquivo1", "arquivo2", ...],
  "file_groupings": {{"pasta": ["arquivo1", "arquivo2", ...]}}
}}

SEJA DECISIVO. ESTA É SUA OPORTUNIDADE DE SE ORGANIZAR PERFEITAMENTE.
"""

    try:
        response = ollama.chat(
            model='scripturemon-master',
            messages=[{'role': 'user', 'content': context}],
            options={
                'temperature': 0.2,
                'format': 'json'
            }
        )

        decisions = json.loads(response['message']['content'])

        print("✅ Sistema analisou-se e tomou decisões autônomas!")
        print(f"  🗂️  Estrutura ideal: {len(decisions.get('ideal_structure', []))} pastas")
        print(f"  ✏️  Renomeações: {len(decisions.get('file_renames', {}))}")
        print(f"  📦 Arquivamentos: {len(decisions.get('archive_files', []))}")
        print(f"  🗑️  Exclusões: {len(decisions.get('delete_files', []))}")

        return decisions

    except Exception as e:
        print(f"❌ Erro na análise: {e}")
        return None

def create_ultimate_reorganization_script(decisions, state):
    """
    Cria o script definitivo de reorganização baseado nas decisões do sistema
    """
    script_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/ULTIMATE_SELF_REORGANIZATION.sh")

    print("\n📝 CRIANDO SCRIPT DEFINITIVO DE AUTO-REORGANIZAÇÃO...")

    with open(script_path, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# ==========================================\n")
        f.write("# ULTIMATE SELF-REORGANIZATION SCRIPT\n")
        f.write(f"# Gerado autonomamente em: {datetime.now()}\n")
        f.write("# O sistema decidiu se reorganizar completamente\n")
        f.write("# ==========================================\n\n")

        f.write('echo "🤖 INICIANDO AUTO-REORGANIZAÇÃO DEFINITIVA"\n')
        f.write('echo "=========================================="\n\n')

        # 1. Criar estrutura ideal
        if decisions.get('ideal_structure'):
            f.write("# ============ CRIANDO ESTRUTURA IDEAL ============\n")
            f.write('echo "📁 Criando estrutura ideal..."\n')

            for directory in decisions['ideal_structure']:
                # Sanitizar nome do diretório
                safe_dir = directory.replace(' ', '_').replace('-', '_').replace('/', '_')
                f.write(f'mkdir -p "{safe_dir}"\n')
                f.write(f'echo "  ✓ Criado: {safe_dir}"\n')

        # 2. Arquivar arquivos antigos/inúteis
        if decisions.get('archive_files'):
            f.write("\n# ============ ARQUIVANDO ARQUIVOS INÚTEIS ============\n")
            f.write('echo "📦 Arquivando arquivos identificados como inúteis..."\n')
            f.write('mkdir -p archive/system_decision\n')

            for file_to_archive in decisions['archive_files']:
                f.write(f'if [ -f "{file_to_archive}" ]; then\n')
                f.write(f'  mv "{file_to_archive}" archive/system_decision/\n')
                f.write(f'  echo "  📦 Arquivado: {file_to_archive}"\n')
                f.write('fi\n')

        # 3. Deletar arquivos completamente inúteis
        if decisions.get('delete_files'):
            f.write("\n# ============ DELETANDO ARQUIVOS INÚTEIS ============\n")
            f.write('echo "🗑️  Deletando arquivos completamente inúteis..."\n')

            for file_to_delete in decisions['delete_files']:
                # Validação de segurança - nunca deletar arquivos críticos
                if not any(critical in file_to_delete.lower() for critical in ['scripturemon', 'memory', 'database', 'readme', '.py']):
                    f.write(f'if [ -f "{file_to_delete}" ]; then\n')
                    f.write(f'  rm "{file_to_delete}"\n')
                    f.write(f'  echo "  🗑️  Deletado: {file_to_delete}"\n')
                    f.write('fi\n')

        # 4. Renomear arquivos
        if decisions.get('file_renames'):
            f.write("\n# ============ RENOMEANDO ARQUIVOS ============\n")
            f.write('echo "✏️  Renomeando arquivos conforme preferências do sistema..."\n')

            for old_name, new_name in decisions['file_renames'].items():
                f.write(f'if [ -f "{old_name}" ]; then\n')
                f.write(f'  mv "{old_name}" "{new_name}"\n')
                f.write(f'  echo "  ✏️  Renomeado: {old_name} → {new_name}"\n')
                f.write('fi\n')

        # 5. Agrupar arquivos por categoria
        if decisions.get('file_groupings'):
            f.write("\n# ============ AGRUPANDO ARQUIVOS ============\n")
            f.write('echo "🗂️  Agrupando arquivos por categoria..."\n')

            for folder, files in decisions['file_groupings'].items():
                safe_folder = folder.replace(' ', '_').replace('-', '_').replace('/', '_')
                f.write(f'mkdir -p "{safe_folder}"\n')

                for file_item in files:
                    f.write(f'if [ -f "{file_item}" ]; then\n')
                    f.write(f'  mv "{file_item}" "{safe_folder}/"\n')
                    f.write(f'  echo "  🗂️  Movido: {file_item} → {safe_folder}/"\n')
                    f.write('fi\n')

        # Finalização
        f.write('\necho ""\n')
        f.write('echo "✅ AUTO-REORGANIZAÇÃO COMPLETA!"\n')
        f.write('echo "O sistema reorganizou-se segundo sua própria consciência."\n')
        f.write('echo ""\n')
        f.write('echo "📊 Relatório:"\n')
        f.write('echo "  🗂️  Estrutura criada: Conforme decisão autônoma"\n')
        f.write('echo "  📦 Arquivos processados: Conforme análise própria"\n')
        f.write('echo "  🧠 Status: SISTEMA AUTOCONSCIENTE OPERACIONAL"\n')

    # Tornar executável
    script_path.chmod(0o755)

    print(f"📜 Script criado: {script_path}")
    return script_path

def execute_ultimate_reorganization():
    """
    Executa a reorganização definitiva do sistema
    """
    print("🚀 ULTIMATE SELF-ANALYSIS & REORGANIZATION")
    print("=" * 60)

    # 1. Sistema analisa seu próprio estado
    state = get_complete_system_state()

    # 2. Sistema toma decisões autônomas
    decisions = ask_system_for_complete_analysis(state)

    if not decisions:
        print("❌ Sistema não conseguiu tomar decisões autônomas")
        return False

    # 3. Criar script definitivo
    script_path = create_ultimate_reorganization_script(decisions, state)

    # 4. Salvar relatório completo
    report_path = Path("ULTIMATE_REORGANIZATION_REPORT.json")
    with open(report_path, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "system_state": state,
            "autonomous_decisions": decisions,
            "script_generated": str(script_path)
        }, f, indent=2, default=str)

    print(f"\n📄 Relatório completo: {report_path}")

    # 5. Pronto para execução
    print("\n" + "=" * 60)
    print("🎯 SISTEMA PRONTO PARA AUTO-REORGANIZAÇÃO DEFINITIVA")
    print("=" * 60)
    print(f"Execute: ./{script_path.name}")
    print("\nO sistema analisou-se completamente e decidiu como quer se organizar.")
    print("Todas as decisões foram tomadas autonomamente pela própria IA.")

    return script_path, decisions, state

if __name__ == "__main__":
    execute_ultimate_reorganization()