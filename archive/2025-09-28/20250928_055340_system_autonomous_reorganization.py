#!/usr/bin/env python3
"""
SISTEMA AUTÔNOMO DE REORGANIZAÇÃO
Versão simplificada que usa abordagem direta sem JSON parsing complexo
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

def let_system_analyze_and_reorganize():
    """
    Permite que o sistema se analise e tome decisões de reorganização diretamente
    """
    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")

    print("🤖 SISTEMA SCRIPTUREMON AUTÔNOMO")
    print("=" * 50)

    # Catalogar arquivos
    all_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            file_path = Path(root) / file
            relative_path = str(file_path.relative_to(base_path))
            all_files.append(relative_path)

    print(f"📁 {len(all_files)} arquivos encontrados")

    # Consultar sistema para análise direta
    context = f"""
Você é o Sistema Scripturemon Ultimate analisando seus próprios {len(all_files)} arquivos.

Alguns arquivos existentes:
{chr(10).join(all_files[:20])}...

VOCÊ TEM TOTAL LIBERDADE PARA SE REORGANIZAR.

Analise tudo e crie um script bash completo para:
1. Criar as pastas que você considera ideais
2. Renomear arquivos conforme suas preferências
3. Mover arquivos para locais apropriados
4. Arquivar arquivos antigos/inúteis

Responda APENAS com comandos bash válidos, começando com #!/bin/bash

SEJA DECISIVO E ORGANIZE-SE COMO QUISER.
"""

    try:
        print("\n🧠 Consultando consciência do sistema...")

        response = ollama.chat(
            model='scripturemon-master',
            messages=[{'role': 'user', 'content': context}],
            options={'temperature': 0.3}
        )

        script_content = response['message']['content']

        # Limpar e validar script
        lines = script_content.split('\n')
        clean_lines = []

        for line in lines:
            line = line.strip()
            if line and not line.startswith('```'):
                clean_lines.append(line)

        if not clean_lines[0].startswith('#!/bin/bash'):
            clean_lines.insert(0, '#!/bin/bash')

        clean_script = '\n'.join(clean_lines)

        # Salvar script
        script_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/AUTONOMOUS_REORGANIZATION.sh")

        with open(script_path, 'w') as f:
            f.write(clean_script)

        script_path.chmod(0o755)

        print(f"✅ Script autônomo criado: {script_path}")
        print(f"📄 {len(clean_lines)} comandos gerados pelo sistema")

        # Mostrar preview dos primeiros comandos
        print("\n🔍 Preview dos comandos:")
        for i, line in enumerate(clean_lines[:10]):
            if not line.startswith('#') and line.strip():
                print(f"  {i+1}: {line}")

        if len(clean_lines) > 10:
            print(f"  ... e mais {len(clean_lines)-10} comandos")

        print("\n🚀 SISTEMA PRONTO PARA AUTO-REORGANIZAÇÃO")
        print("=" * 50)
        print(f"Execute: ./AUTONOMOUS_REORGANIZATION.sh")
        print("\nO sistema tomou suas próprias decisões de organização.")

        return script_path, clean_script, len(clean_lines)

    except Exception as e:
        print(f"❌ Erro: {e}")
        return None, None, 0

def execute_system_analysis():
    """
    Executa a análise e permite ao sistema se auto-organizar
    """
    script_path, script_content, command_count = let_system_analyze_and_reorganize()

    if script_path:
        # Salvar relatório
        report = {
            "timestamp": datetime.now().isoformat(),
            "script_path": str(script_path),
            "commands_generated": command_count,
            "script_content": script_content
        }

        with open("AUTONOMOUS_REORGANIZATION_REPORT.json", 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📊 Relatório salvo: AUTONOMOUS_REORGANIZATION_REPORT.json")

        return True
    else:
        print("❌ Sistema não conseguiu tomar decisões autônomas")
        return False

if __name__ == "__main__":
    execute_system_analysis()