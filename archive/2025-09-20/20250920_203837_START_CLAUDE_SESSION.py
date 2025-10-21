#!/usr/bin/env python3
"""
🚀 START CLAUDE SESSION - SEMPRE EXECUTE ESTE ARQUIVO PRIMEIRO!
==============================================================
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from src.core.unified_memory_system import get_unified_memory, MemoryType
# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado


# Cores para terminal
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header():
    """Imprime cabeçalho de inicialização"""
    print("\n" + "="*80)
    print(f"{BOLD}{BLUE}🧠 CLAUDE CODE - SISTEMA DE MEMÓRIA PERSISTENTE{RESET}")
    print("="*80)

# UNUSED - Candidate for removal
# def check_memory_files():
    """Verifica se arquivos de memória existem"""
    root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")

    files_to_check = {
        'CLAUDE.md': 'Memória principal com contexto e regras',
        'COMPLETE_SYSTEM_MAP.json': 'Mapa detalhado de todos os 428 arquivos',
        '../REDUNDANCY_ROOT_CAUSE_ANALYSIS.md': 'Análise de por que há redundância',
        '../DEPLOYMENT_SYSTEM_ANALYSIS.md': 'Problema do deployment divergente'
    }

    print(f"\n{BOLD}📂 VERIFICANDO ARQUIVOS DE MEMÓRIA:{RESET}\n")

    all_exist = True
    for file, description in files_to_check.items():
        file_path = root / file
        if file_path.exists():
            size = file_path.stat().st_size / 1024  # KB
            print(f"  {GREEN}✅ {file}{RESET} ({size:.1f} KB)")
            print(f"     {description}")
        else:
            print(f"  {RED}❌ {file} - NÃO ENCONTRADO!{RESET}")
            all_exist = False

    return all_exist
# UNUSED - Candidate for removal
# 
def show_critical_info():
    """Mostra informações críticas do sistema"""
    print(f"\n{BOLD}{YELLOW}⚠️ INFORMAÇÕES CRÍTICAS QUE VOCÊ SEMPRE ESQUECE:{RESET}\n")

    critical = [
        ("CÓDIGO REAL ESTÁ EM", "deployments/green_v2.0.0/code/apps/scripturemon/"),
        ("apps/scripturemon/ ESTÁ", "VAZIO! Não crie nada lá!"),
        ("Total de geradores", "323 arquivos criam outros arquivos"),
        ("Sistemas de memória", "24 diferentes (não criar mais!)"),
        ("DigiLang ativo", "digilang_v26_mega_multilayer.py"),
        ("Crystal Memory", "Foi removido mas era útil")
    ]

    for label, value in critical:
        # UNUSED - Candidate for removal
        pass  # print(f"  {label}: {BOLD}{value}{RESET}")

def show_common_mistakes():
    """Lista erros comuns para evitar"""
    print(f"\n{BOLD}{RED}🚫 ERROS QUE VOCÊ SEMPRE COMETE:{RESET}\n")

    mistakes = [
        "Criar novo arquivo sem verificar se já existe",
        "Usar sufixos de versão (_v1, _v2, _improved)",
        "Criar código em apps/scripturemon/ (está vazio!)",
        "Sugerir deletar Crystal Memory",
        "Criar mais um sistema de memória",
        "Esquecer que 323 arquivos geram outros arquivos"
    ]

# UNUSED - Candidate for removal
#     for i, mistake in enumerate(mistakes, 1):
#         print(f"  {i}. {mistake}")

def show_correct_practices():
    """Mostra práticas corretas"""
    print(f"\n{BOLD}{GREEN}✅ O QUE FAZER SEMPRE:{RESET}\n")

    practices = [
        "Ler CLAUDE.md completo no início",
        "Verificar COMPLETE_SYSTEM_MAP.json para navegação",
        "Usar grep antes de criar qualquer arquivo",
        "Modificar existente ao invés de criar novo",
        "Usar Git para versionamento (não sufixos)",
        "Atualizar CLAUDE.md com decisões importantes"
    ]
# UNUSED - Candidate for removal
# 
    for i, practice in enumerate(practices, 1):
        print(f"  {i}. {practice}")

def create_session_marker():
    """Cria marcador de sessão iniciada"""
    session_file = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/.claude_session")

    session_data = {
        'started_at': datetime.now().isoformat(),
        'memory_loaded': False,
        'instructions_shown': True
    }

    with open(session_file, 'w') as f:
        json.dump(session_data, f)

    return session_data

def main():
    """Função principal de inicialização"""
    print_header()

    # Verificar arquivos
    if not check_memory_files():
        print(f"\n{RED}{BOLD}⚠️ ARQUIVOS DE MEMÓRIA FALTANDO!{RESET}")
        print("Execute o complete_system_mapper.py para recriar")
        sys.exit(1)

    # Mostrar informações críticas
    show_critical_info()
    show_common_mistakes()
    show_correct_practices()

    # Criar marcador de sessão
    session = create_session_marker()

    # Instruções finais
    print(f"\n{BOLD}{BLUE}📋 PRÓXIMOS PASSOS OBRIGATÓRIOS:{RESET}\n")
    print(f"1. {YELLOW}LEIA A MEMÓRIA PRINCIPAL:{RESET}")
    print(f"   cat CLAUDE.md | head -100\n")

    print(f"2. {YELLOW}VERIFIQUE O MAPA DO SISTEMA:{RESET}")
    print("   python3 -c \"import json; data = json.load(open('COMPLETE_SYSTEM_MAP.json')); print('Total:', data['structure_summary']['total_files'], 'arquivos,', data['structure_summary']['generators'], 'geradores')\"\n")

    print(f"3. {YELLOW}CONFIRME QUE LEU:{RESET}")
    print(f"   python3 claude_memory_hook.py --confirm\n")

    print("="*80)
    print(f"{GREEN}{BOLD}✅ SESSÃO INICIADA - AGORA LEIA A MEMÓRIA ANTES DE AGIR!{RESET}")
    print("="*80)

if __name__ == "__main__":
    main()

# ============================================================
# AUTO-UNIFIED MEMORY HELPER
# ============================================================
def _get_memory():
    """Helper para acesso rápido à memória unificada"""
    return get_unified_memory()

# Atalhos para compatibilidade
unified_memory = _get_memory()
