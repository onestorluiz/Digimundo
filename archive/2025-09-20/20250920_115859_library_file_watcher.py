#!/usr/bin/env python3
"""
📚 BIBLIOTECA FILE WATCHER
Monitora automaticamente a pasta BIBLIOTECA_ROTEIROS por novos arquivos
e os adiciona à biblioteca automaticamente!
"""

import asyncio
import time
from pathlib import Path
from typing import Set, Dict
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.screenplay_library import ScreenplayLibrary
from src.core.unified_memory_system import get_unified_memory, MemoryType


class LibraryFileWatcher:
    """Monitora mudanças na biblioteca de roteiros"""

    def __init__(self, check_interval: int = 10):
        """
        Args:
            check_interval: Segundos entre verificações (padrão: 10)
        """
        self.library_path = Path("digilibrary/BIBLIOTECA_ROTEIROS")
        self.check_interval = check_interval
        self.library = ScreenplayLibrary()
        self.memory = get_unified_memory()
        self._known_files: Set[Path] = set()
        self._file_hashes: Dict[Path, str] = {}

    def scan_files(self) -> Set[Path]:
        """Escaneia todos os arquivos na biblioteca"""
        files = set()

        if self.library_path.exists():
            # Buscar todos os .txt e .pdf recursivamente
            for pattern in ["*.txt", "*.pdf"]:
                for file_path in self.library_path.rglob(pattern):
                    files.add(file_path)

        return files

    def get_file_info(self, file_path: Path) -> Dict:
        """Obtém informações sobre um arquivo"""
        stats = file_path.stat()
        relative_path = file_path.relative_to(self.library_path)

        # Determinar categoria baseada no caminho
        parts = relative_path.parts
        category = parts[0] if len(parts) > 1 else "root"

        return {
            'path': str(file_path),
            'relative_path': str(relative_path),
            'category': category,
            'name': file_path.stem,
            'extension': file_path.suffix,
            'size': stats.st_size,
            'modified': datetime.fromtimestamp(stats.st_mtime).isoformat(),
            'created': datetime.fromtimestamp(stats.st_ctime).isoformat()
        }

    async def process_new_file(self, file_path: Path):
        """Processa um novo arquivo detectado"""
        print(f"\n🆕 NOVO ARQUIVO DETECTADO: {file_path.name}")
        print(f"   Caminho: {file_path.relative_to(self.library_path)}")

        # Obter informações do arquivo
        file_info = self.get_file_info(file_path)

        # Salvar na memória unificada
        self.memory.store(
            memory_type=MemoryType.SCREENPLAY,
            key=f"file:{file_path.stem}",
            value=file_info,
            metadata={
                'filename': file_path.name,
                'category': file_info['category'],
                'detected_at': datetime.now().isoformat()
            }
        )

        # Forçar atualização da lista na biblioteca
        self.library.list_screenplays(force_refresh=True)

        # Log de estatísticas
        total_files = len(self.library.list_screenplays())
        print(f"   ✅ Adicionado à biblioteca!")
        print(f"   📊 Total de arquivos na biblioteca: {total_files}")

        # Se for um arquivo de texto, fazer uma análise rápida
        if file_path.suffix == '.txt':
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.count('\n')
                words = len(content.split())
                print(f"   📝 Estatísticas: {lines:,} linhas, {words:,} palavras")
            except Exception as e:
                print(f"   ⚠️ Erro ao ler arquivo: {e}")

    async def process_removed_file(self, file_path: Path):
        """Processa um arquivo removido"""
        print(f"\n❌ ARQUIVO REMOVIDO: {file_path.name}")
        print(f"   Caminho: {file_path.relative_to(self.library_path)}")

        # Forçar atualização da lista
        self.library.list_screenplays(force_refresh=True)

        # Log de estatísticas
        total_files = len(self.library.list_screenplays())
        print(f"   📊 Total de arquivos na biblioteca: {total_files}")

    async def watch(self):
        """Loop principal de monitoramento"""
        print("🔍 BIBLIOTECA FILE WATCHER INICIADO")
        print(f"📁 Monitorando: {self.library_path.absolute()}")
        print(f"⏱️ Intervalo de verificação: {self.check_interval}s")
        print("-" * 60)

        # Scan inicial
        self._known_files = self.scan_files()
        print(f"📊 Arquivos encontrados inicialmente: {len(self._known_files)}")

        # Mostrar categorias
        categories = {}
        for file_path in self._known_files:
            info = self.get_file_info(file_path)
            cat = info['category']
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1

        print("\n📚 Categorias:")
        for cat, count in sorted(categories.items()):
            print(f"   • {cat}: {count} arquivos")

        print("\n" + "=" * 60)
        print("👀 Monitorando mudanças...")
        print("   (Pressione Ctrl+C para parar)")
        print("=" * 60)

        # Loop de monitoramento
        try:
            while True:
                await asyncio.sleep(self.check_interval)

                # Escanear novamente
                current_files = self.scan_files()

                # Detectar novos arquivos
                new_files = current_files - self._known_files
                for file_path in new_files:
                    await self.process_new_file(file_path)

                # Detectar arquivos removidos
                removed_files = self._known_files - current_files
                for file_path in removed_files:
                    await self.process_removed_file(file_path)

                # Atualizar lista conhecida
                if new_files or removed_files:
                    self._known_files = current_files

        except KeyboardInterrupt:
            print("\n\n⏹️ File watcher parado pelo usuário")
            print(f"📊 Total de arquivos monitorados: {len(self._known_files)}")


async def main():
    """Função principal"""
    import argparse

    parser = argparse.ArgumentParser(description='Monitor BIBLIOTECA_ROTEIROS for changes')
    parser.add_argument(
        '--interval',
        type=int,
        default=10,
        help='Check interval in seconds (default: 10)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode: create a test file to see detection'
    )

    args = parser.parse_args()

    if args.test:
        # Modo teste: criar um arquivo de teste
        print("🧪 MODO TESTE")
        test_path = Path("digilibrary/BIBLIOTECA_ROTEIROS/teste_automatico.txt")

        print(f"📝 Criando arquivo de teste: {test_path.name}")
        test_path.write_text("Este é um arquivo de teste criado automaticamente!")

        print("⏳ Aguarde 15 segundos para ver a detecção...")
        print("   (O watcher deve detectar o novo arquivo)")

        # Iniciar watcher
        watcher = LibraryFileWatcher(check_interval=5)
        try:
            await asyncio.wait_for(watcher.watch(), timeout=15)
        except asyncio.TimeoutError:
            pass

        # Limpar arquivo de teste
        print(f"\n🧹 Removendo arquivo de teste...")
        test_path.unlink()
        print("✅ Teste concluído!")

    else:
        # Modo normal
        watcher = LibraryFileWatcher(check_interval=args.interval)
        await watcher.watch()


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║   📚 BIBLIOTECA ROTEIROS FILE WATCHER 📚     ║
║                                              ║
║   Monitora automaticamente novos arquivos   ║
║   na pasta BIBLIOTECA_ROTEIROS              ║
╚══════════════════════════════════════════════╝
    """)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Até logo!")