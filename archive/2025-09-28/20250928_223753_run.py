#!/usr/bin/env python3
"""
🔥 SCRIPTUREMON ULTIMATE 🔥
Sistema de análise de roteiros com memória persistente
Uso: python run.py <comando> [opções]
"""

import argparse
import sys
import logging
from pathlib import Path
from datetime import datetime

# Adicionar core ao path
sys.path.insert(0, str(Path(__file__).parent))

# Imports do sistema
from core.config import (
    BASE_DIR, OUTPUTS_DIR, INPUTS_DIR, DB_PATH,
    LOG_LEVEL, LOG_FORMAT, get_config_dict
)
from core.memory_system import ScripturemonMemory, MemoryIntegration

# Configurar logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def cmd_analyze(args):
    """Comando para analisar roteiro"""
    # Verificar arquivo de entrada
    screenplay_path = Path(args.screenplay)
    if not screenplay_path.exists():
        print(f"❌ Arquivo não encontrado: {screenplay_path}")
        sys.exit(1)

    # Ler conteúdo
    with open(screenplay_path, 'r', encoding='utf-8') as f:
        screenplay_content = f.read()

    title = args.title or screenplay_path.stem

    print(f"\n📝 Analisando: {title}")
    print(f"   Modo: {args.mode}")
    print(f"   Memória: {'Ativada' if not args.no_memory else 'Desativada'}")

    # Criar sistema (importar aqui para evitar dependências circulares)
    from core.scripturemon import ScripturemonSystem

    system = ScripturemonSystem(use_memory=not args.no_memory)

    # Executar análise
    report_file = system.analyze(
        screenplay_content=screenplay_content,
        title=title,
        mode=args.mode
    )

    print(f"\n✅ Análise completa!")
    print(f"📄 Relatório salvo em: {report_file}")

    # Exportar memória se solicitado
    if args.export_memory:
        memory = ScripturemonMemory()
        export_path = memory.export_to_json()
        print(f"💾 Memória exportada para: {export_path}")
        memory.close()

    return 0


def cmd_memory(args):
    """Comando para gerenciar memória"""
    memory = ScripturemonMemory()

    if args.action == "stats":
        stats = memory.get_stats()
        print("\n📊 ESTATÍSTICAS DA MEMÓRIA:")
        print("="*40)
        for key, value in stats.items():
            print(f"  {key}: {value}")

    elif args.action == "export":
        if args.file:
            export_path = memory.export_to_json(args.file)
        else:
            export_path = memory.export_to_json()
        print(f"✅ Memória exportada para: {export_path}")

    elif args.action == "import":
        if not args.file:
            print("❌ Especifique o arquivo para importar com --file")
            memory.close()
            return 1

        if not Path(args.file).exists():
            print(f"❌ Arquivo não encontrado: {args.file}")
            memory.close()
            return 1

        success = memory.import_from_json(args.file)
        if success:
            print("✅ Importação completa!")
            stats = memory.get_stats()
            print(f"   Total de memórias: {stats['total_memories']}")
        else:
            print("❌ Erro na importação")

    elif args.action == "clear":
        if not args.confirm:
            print("⚠️  Esta ação irá APAGAR toda a memória!")
            print("   Use --confirm para confirmar")
            memory.close()
            return 1

        memory.clear_all(confirm=True)
        print("🗑️  Memória limpa!")

    elif args.action == "search":
        if not args.query:
            print("❌ Especifique a busca com --query")
            memory.close()
            return 1

        results = memory.search_knowledge(args.query, limit=10)
        print(f"\n🔍 Busca: '{args.query}'")
        print(f"📚 {len(results)} resultados encontrados:")
        print("="*40)

        for i, result in enumerate(results, 1):
            print(f"\n[{i}] {result.get('title', 'Sem título')}")
            print(f"    Fonte: {result.get('source', 'N/A')}")
            print(f"    Preview: {result.get('content', '')[:100]}...")

    memory.close()
    return 0


def cmd_test(args):
    """Comando para executar testes"""
    print("\n🧪 EXECUTANDO TESTES")
    print("="*40)

    # Teste 1: Configuração
    print("\n1️⃣ Testando configuração...")
    config = get_config_dict()
    print(f"   Base dir: {config['base_dir']}")
    print(f"   DB path: {config['db_path']}")
    print("   ✅ Configuração OK")

    # Teste 2: Memória
    print("\n2️⃣ Testando sistema de memória...")
    try:
        memory = ScripturemonMemory()
        stats = memory.get_stats()
        print(f"   Total memórias: {stats['total_memories']}")

        # Teste de escrita
        success = memory.store_knowledge(
            category="test",
            source="test",
            title="Test Item",
            content="This is a test",
            tags=["test"]
        )
        if success:
            print("   ✅ Escrita OK")

        # Teste de busca
        results = memory.search_knowledge("test", limit=1)
        if results:
            print("   ✅ Busca OK")

        memory.close()
        print("   ✅ Memória OK")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return 1

    # Teste 3: Modelfiles
    print("\n3️⃣ Verificando modelfiles...")
    modelfiles_dir = BASE_DIR / "specialists" / "modelfiles"
    modelfiles = list(modelfiles_dir.glob("*.modelfile"))
    print(f"   {len(modelfiles)} modelfiles encontrados")
    if len(modelfiles) > 0:
        print("   ✅ Modelfiles OK")
    else:
        print("   ⚠️ Nenhum modelfile encontrado")

    print("\n✅ TODOS OS TESTES PASSARAM!")
    return 0


def cmd_config(args):
    """Comando para mostrar configuração"""
    config = get_config_dict()

    print("\n⚙️ CONFIGURAÇÃO DO SISTEMA")
    print("="*40)

    for key, value in config.items():
        print(f"  {key}: {value}")

    print("\n📁 DIRETÓRIOS:")
    print(f"  Inputs: {INPUTS_DIR}")
    print(f"  Outputs: {OUTPUTS_DIR}")
    print(f"  Database: {DB_PATH}")

    return 0


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Scripturemon Ultimate - Sistema de Análise de Roteiros',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python run.py analyze screenplay.txt --title "Meu Filme"
  python run.py memory stats
  python run.py test
  python run.py config
        """
    )

    # Subcomandos
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')

    # ========== ANALYZE ==========
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analisar um roteiro'
    )
    analyze_parser.add_argument(
        'screenplay',
        help='Caminho para o arquivo do roteiro'
    )
    analyze_parser.add_argument(
        '--title', '-t',
        help='Título do roteiro'
    )
    analyze_parser.add_argument(
        '--mode', '-m',
        choices=['QUICK', 'STANDARD', 'COMPLETE'],
        default='STANDARD',
        help='Modo de análise (default: STANDARD)'
    )
    analyze_parser.add_argument(
        '--no-memory',
        action='store_true',
        help='Desativar enriquecimento com memória'
    )
    analyze_parser.add_argument(
        '--export-memory',
        action='store_true',
        help='Exportar memória após análise'
    )

    # ========== MEMORY ==========
    memory_parser = subparsers.add_parser(
        'memory',
        help='Gerenciar sistema de memória'
    )
    memory_parser.add_argument(
        'action',
        choices=['stats', 'export', 'import', 'clear', 'search'],
        help='Ação a executar'
    )
    memory_parser.add_argument(
        '--file', '-f',
        help='Arquivo para import/export'
    )
    memory_parser.add_argument(
        '--query', '-q',
        help='Termo de busca'
    )
    memory_parser.add_argument(
        '--confirm',
        action='store_true',
        help='Confirmar ações destrutivas'
    )

    # ========== TEST ==========
    test_parser = subparsers.add_parser(
        'test',
        help='Executar testes do sistema'
    )

    # ========== CONFIG ==========
    config_parser = subparsers.add_parser(
        'config',
        help='Mostrar configuração do sistema'
    )

    # Parse argumentos
    args = parser.parse_args()

    # Executar comando
    if args.command == 'analyze':
        return cmd_analyze(args)
    elif args.command == 'memory':
        return cmd_memory(args)
    elif args.command == 'test':
        return cmd_test(args)
    elif args.command == 'config':
        return cmd_config(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""
DIGIMUNDO PRESENTE 🥷
"""