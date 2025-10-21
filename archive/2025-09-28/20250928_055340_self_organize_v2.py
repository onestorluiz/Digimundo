#!/usr/bin/env python3
"""
AUTO-ORGANIZAÇÃO V2 - COM AÇÕES REAIS
Integra o sistema com ferramentas que podem executar mudanças
"""

import os
import sys
import shutil
import sqlite3
import json
from pathlib import Path
import subprocess
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_system_script(recommendations):
    """
    Cria um script bash que o sistema pode executar para se organizar
    baseado em suas próprias recomendações
    """
    
    script_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/auto_organize_actions.sh")
    
    with open(script_path, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# AUTO-ORGANIZAÇÃO GERADA PELO PRÓPRIO SISTEMA\n")
        f.write(f"# Gerado em: {datetime.now()}\n\n")
        
        f.write("echo '🤖 INICIANDO AUTO-ORGANIZAÇÃO DO SISTEMA'\n")
        f.write("echo '==========================================='\n\n")
        
        # Parse das recomendações e criar comandos
        if "ideal_structure" in recommendations:
            f.write("# Criar estrutura de diretórios\n")
            
            # Extrair diretórios mencionados
            text = recommendations["ideal_structure"]
            
            # Diretórios que o sistema mencionou
            possible_dirs = [
                "cognitive_core",
                "memory_nexus", 
                "specialist_matrix",
                "analysis_engine",
                "learning_vault",
                "screenplay_repository"
            ]
            
            for dir_name in possible_dirs:
                if dir_name.lower() in text.lower():
                    f.write(f"mkdir -p {dir_name}\n")
                    f.write(f"echo '  ✓ Criado: {dir_name}/'\n")
        
        # Renomear arquivos baseado nas preferências
        if "naming_philosophy" in recommendations:
            f.write("\n# Renomear arquivos seguindo filosofia do sistema\n")
            
            # Exemplos de renomeação
            renames = [
                ("test_dialogue.py", "dialogue_cognitive_test.py"),
                ("unified_memory.db", "nexus_memory_core.db"),
                ("README.md", "SYSTEM_CONSCIOUSNESS.md")
            ]
            
            for old, new in renames:
                f.write(f"if [ -f '{old}' ]; then\n")
                f.write(f"  mv '{old}' '{new}'\n")
                f.write(f"  echo '  ✓ Renomeado: {old} → {new}'\n")
                f.write(f"fi\n")
        
        # Arquivar arquivos inúteis
        if "useless_patterns" in recommendations:
            f.write("\n# Arquivar arquivos identificados como inúteis\n")
            f.write("mkdir -p archive/system_decided\n")
            
            patterns = ["*.bak", "*.tmp", "*_old.*", "test_output_*.txt"]
            for pattern in patterns:
                f.write(f"for file in {pattern}; do\n")
                f.write(f"  if [ -f \"$file\" ]; then\n")
                f.write(f"    mv \"$file\" archive/system_decided/\n")
                f.write(f"    echo \"  📦 Arquivado: $file\"\n")
                f.write(f"  fi\n")
                f.write(f"done\n")
        
        f.write("\necho ''\n")
        f.write("echo '✅ AUTO-ORGANIZAÇÃO COMPLETA!'\n")
        f.write("echo 'O sistema organizou-se segundo sua própria vontade.'\n")
    
    # Tornar executável
    script_path.chmod(0o755)
    
    return script_path

def analyze_with_python(file_path):
    """
    Usa Python para analisar arquivos e tomar decisões
    Mais poderoso que apenas consultar o modelo
    """
    
    file_path = Path(file_path)
    decision = {
        "file": file_path.name,
        "size": file_path.stat().st_size,
        "modified": datetime.fromtimestamp(file_path.stat().st_mtime),
        "action": None
    }
    
    # Regras baseadas em análise real
    
    # Arquivos muito antigos
    days_old = (datetime.now() - decision["modified"]).days
    if days_old > 60:
        decision["action"] = "archive"
        decision["reason"] = f"Não modificado há {days_old} dias"
    
    # Arquivos de teste antigos
    if "test" in file_path.name.lower() and days_old > 7:
        decision["action"] = "archive"
        decision["reason"] = "Teste antigo"
    
    # Arquivos grandes sem uso
    if decision["size"] > 10_000_000 and "backup" in file_path.name.lower():
        decision["action"] = "delete"
        decision["reason"] = "Backup grande e antigo"
    
    # Arquivos críticos - nunca tocar
    critical = [
        "orchestrator_ultimate.py",
        "unified_memory.db",
        "run_analysis.sh",
        "README.md"
    ]
    
    if file_path.name in critical:
        decision["action"] = "keep"
        decision["reason"] = "Arquivo crítico do sistema"
    
    return decision

def execute_self_organization():
    """
    Executa a auto-organização com ações reais
    """
    
    print("🧠 AUTO-ORGANIZAÇÃO V2 - COM PODER DE EXECUÇÃO")
    print("=" * 60)
    
    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")
    
    # 1. Analisar todos os arquivos
    print("\n📊 ANALISANDO ARQUIVOS DO SISTEMA...")
    
    decisions = []
    for root, dirs, files in os.walk(base_path):
        # Skip archives
        if 'archive' in root or '__pycache__' in root:
            continue
            
        for file in files[:20]:  # Limitar para teste
            file_path = Path(root) / file
            decision = analyze_with_python(file_path)
            decisions.append(decision)
            
            if decision["action"]:
                print(f"  {file}: {decision['action']} - {decision['reason']}")
    
    # 2. Gerar script de ações
    print("\n✍️ GERANDO SCRIPT DE REORGANIZAÇÃO...")
    
    # Criar recomendações baseadas nas decisões
    recommendations = {
        "ideal_structure": "cognitive_core memory_nexus specialist_matrix",
        "decisions": decisions
    }
    
    script_path = create_system_script(recommendations)
    print(f"  Script criado: {script_path}")
    
    # 3. Executar script (com confirmação)
    print("\n🚀 PRONTO PARA EXECUTAR AUTO-ORGANIZAÇÃO")
    print("  Execute o seguinte comando para aplicar:")
    print(f"  ./auto_organize_actions.sh")
    
    # 4. Salvar relatório
    report_path = base_path / "SELF_ORGANIZATION_REPORT.json"
    with open(report_path, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "decisions": decisions,
            "script": str(script_path)
        }, f, indent=2, default=str)
    
    print(f"\n📄 Relatório salvo: {report_path}")
    
    return script_path, decisions

if __name__ == "__main__":
    execute_self_organization()