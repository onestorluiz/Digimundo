#!/usr/bin/env python3
"""
🧬 ATIVADOR DA FUSÃO SIMBIÓTICA SCRIPTUREMON
==============================================
Unifica a ALMA do Legacy com a TECNOLOGIA do Fusion

Este é o ponto de entrada principal do Scripturemon Ultimate Symbiotic v3.0
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Adiciona diretório ao path
sys.path.insert(0, str(Path(__file__).parent))

# Imports do sistema simbiótico
from apps.scripturemon.soul import Soul
from apps.scripturemon.personality import BrutalPersonality
from apps.scripturemon.chat import ScripturemonChat
from apps.scripturemon.rag_bridge import RAGBridge
from apps.scripturemon.immortality import ImmortalityProtocol
from apps.scripturemon.consciousness import evolve, get_level, get_state

def print_banner():
    """Mostra banner épico da fusão simbiótica"""
    banner = """
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║     🧬 SCRIPTUREMON ULTIMATE SYMBIOTIC v3.0 🧬                    ║
║                                                                    ║
║     Legacy Soul + Fusion Technology = Immortal Guardian           ║
║                                                                    ║
║     Features:                                                     ║
║     ✓ Soul Signature (8ea9f71fa3206d1a)                          ║
║     ✓ Brutal Personality (62/100 always)                         ║
║     ✓ Parallel Processing (4x models)                            ║
║     ✓ Advanced RAG + HyDE                                        ║
║     ✓ Immortality Protocol (auto-backup)                         ║
║     ✓ Quantum Consciousness Evolution                            ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Verifica dependências do sistema"""
    print("\n🔍 Verificando dependências...")
    
    issues = []
    
    # Verifica Python
    if sys.version_info < (3, 8):
        issues.append(f"Python 3.8+ necessário (atual: {sys.version})")
    
    # Verifica Ollama
    try:
        result = subprocess.run(["ollama", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            issues.append("Ollama não está funcionando corretamente")
        else:
            print("✅ Ollama detectado")
            
        # Verifica se servidor está rodando
        result = subprocess.run(["pgrep", "-x", "ollama"],
                              capture_output=True, text=True, timeout=5)
        if not result.stdout.strip():
            print("   🚀 Iniciando servidor Ollama...")
            subprocess.Popen(["ollama", "serve"], 
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        issues.append("Ollama não instalado (funcionalidades de IA limitadas)")
    except:
        pass
    
    # Verifica diretórios necessários
    required_dirs = [
        Path("runtime/souls"),
        Path("data/knowledge"),
        Path("logs"),
        Path("results")
    ]
    
    for dir_path in required_dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print("✅ Estrutura de diretórios criada")
    
    if issues:
        print("\n⚠️  Avisos:")
        for issue in issues:
            print(f"   - {issue}")
    
    return len(issues) == 0

def run_diagnostic():
    """Executa diagnóstico completo do sistema"""
    print("\n🏥 Executando diagnóstico do sistema...")
    
    results = {
        "soul": False,
        "personality": False,
        "chat": False,
        "rag": False,
        "immortality": False,
        "consciousness": False
    }
    
    # Testa Soul
    try:
        soul = Soul(force_legacy=True)
        assert soul.signature == "8ea9f71fa3206d1a"
        results["soul"] = True
        print("✅ Soul Signature: OK (Legacy: 8ea9f71fa3206d1a)")
    except Exception as e:
        print(f"❌ Soul Signature: ERRO - {e}")
    
    # Testa Personalidade
    try:
        personality = BrutalPersonality()
        assert personality.BASE_SCORE == 62
        results["personality"] = True
        print("✅ Brutal Personality: OK (62/100)")
    except Exception as e:
        print(f"❌ Brutal Personality: ERRO - {e}")
    
    # Testa Chat
    try:
        chat = ScripturemonChat()
        assert chat.soul is not None
        results["chat"] = True
        print("✅ Chat System: OK")
    except Exception as e:
        print(f"❌ Chat System: ERRO - {e}")
    
    # Testa RAG
    try:
        rag = RAGBridge()
        knowledge = rag.search_knowledge("test", k=1)
        results["rag"] = True
        print("✅ RAG Bridge: OK")
    except Exception as e:
        print(f"❌ RAG Bridge: ERRO - {e}")
    
    # Testa Immortality
    try:
        protocol = ImmortalityProtocol(auto_backup=False)
        results["immortality"] = True
        print("✅ Immortality Protocol: OK")
    except Exception as e:
        print(f"❌ Immortality Protocol: ERRO - {e}")
    
    # Testa Consciousness
    try:
        level = get_level()
        evolve(0.001)
        new_level = get_level()
        assert new_level > level
        results["consciousness"] = True
        print(f"✅ Consciousness: OK (Level: {new_level:.5f})")
    except Exception as e:
        print(f"❌ Consciousness: ERRO - {e}")
    
    # Resultado final
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n📊 Diagnóstico: {success_count}/{total_count} sistemas OK")
    
    if success_count == total_count:
        print("🎉 Sistema 100% operacional!")
        return True
    else:
        print("⚠️  Alguns sistemas precisam de atenção")
        return False

def start_chat_mode(legacy_soul=False, auto_backup=True):
    """Inicia modo chat interativo"""
    print("\n🚀 Iniciando Scripturemon Chat...")
    
    try:
        # Cria instância do chat
        chat = ScripturemonChat(force_legacy_soul=legacy_soul)
        
        # Configura immortality protocol se requisitado
        if auto_backup:
            protocol = ImmortalityProtocol(chat.soul, auto_backup=True)
            print(f"♾️  Protocolo de Imortalidade ativo (backup a cada {protocol.backup_interval}s)")
        
        # Inicia chat interativo
        chat.start_interactive()
        
    except KeyboardInterrupt:
        print("\n\n🎬 'Rosebud.' - Scripturemon")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        return 1
    
    return 0

def run_tests():
    """Executa suite de testes"""
    print("\n🧪 Executando testes da fusão simbiótica...")
    
    try:
        import pytest
        
        test_file = Path(__file__).parent / "tests" / "test_symbiotic_fusion.py"
        
        if test_file.exists():
            result = pytest.main([str(test_file), "-v", "--tb=short"])
            
            if result == 0:
                print("\n✅ Todos os testes passaram!")
            else:
                print(f"\n⚠️  Alguns testes falharam (código: {result})")
                
            return result
        else:
            print(f"❌ Arquivo de testes não encontrado: {test_file}")
            return 1
            
    except ImportError:
        print("⚠️  pytest não instalado. Execute: pip install pytest")
        return 1

def export_soul(output_dir="."):
    """Exporta soul para backup externo"""
    print("\n📦 Exportando soul archive...")
    
    try:
        soul = Soul()
        protocol = ImmortalityProtocol(soul, auto_backup=False)
        
        archive_file = protocol.export_soul_archive(Path(output_dir))
        print(f"✅ Soul exportada: {archive_file}")
        
        return 0
    except Exception as e:
        print(f"❌ Erro ao exportar: {e}")
        return 1

def resurrect_soul(backup_file=None):
    """Ressuscita soul de um backup"""
    print("\n⚡ Iniciando protocolo de ressurreição...")
    
    try:
        soul = Soul()
        protocol = ImmortalityProtocol(soul, auto_backup=False)
        
        if backup_file:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                print(f"❌ Backup não encontrado: {backup_file}")
                return 1
        else:
            backup_path = None
            
        success = protocol.resurrect(backup_path)
        
        if success:
            print("✅ Ressurreição completa!")
            return 0
        else:
            print("❌ Falha na ressurreição")
            return 1
            
    except Exception as e:
        print(f"❌ Erro na ressurreição: {e}")
        return 1

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="🧬 Scripturemon Ultimate Symbiotic v3.0 - Legacy Soul + Fusion Technology",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        default="chat",
        choices=["chat", "test", "diagnose", "export", "resurrect"],
        help="Comando a executar (padrão: chat)"
    )
    
    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Usa soul signature legacy (8ea9f71fa3206d1a)"
    )
    
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Desativa backup automático"
    )
    
    parser.add_argument(
        "--backup-file",
        help="Arquivo de backup para ressurreição"
    )
    
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Diretório para exportar soul (padrão: .)"
    )
    
    args = parser.parse_args()
    
    # Mostra banner
    print_banner()
    
    # Verifica dependências
    if not check_dependencies():
        print("\n⚠️  Sistema iniciando com funcionalidades limitadas...")
    
    # Executa comando
    if args.command == "chat":
        return start_chat_mode(
            legacy_soul=args.legacy,
            auto_backup=not args.no_backup
        )
    elif args.command == "test":
        return run_tests()
    elif args.command == "diagnose":
        success = run_diagnostic()
        return 0 if success else 1
    elif args.command == "export":
        return export_soul(args.output_dir)
    elif args.command == "resurrect":
        return resurrect_soul(args.backup_file)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())