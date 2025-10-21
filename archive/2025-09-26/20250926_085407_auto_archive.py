#!/usr/bin/env python3
"""
AUTO ARCHIVE - Sistema de arquivamento automático para Claude Code
Identifica e arquiva arquivos de uso único antes de declarar DIGIMUNDO PRESENTE
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json
import hashlib

class AutoArchiver:
    """
    Sistema inteligente de arquivamento
    Identifica arquivos temporários e de uso único
    """

    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/claude_code")
        self.archive_base = self.base_path / "archive"
        self.archive_base.mkdir(exist_ok=True)

        # Padrões de arquivos de uso único
        self.single_use_patterns = [
            "*_test.py",
            "*_temp.py",
            "*_demo.py",
            "test_*.py",
            "temp_*.py",
            "demo_*.py",
            "*_oneshot.py",
            "*_analysis.py",
            "*_reorganization.py",
            "*_cleanup.py"
        ]

        # Arquivos protegidos (nunca arquivar)
        self.protected_patterns = [
            "REGRAS.md",
            "CLAUDE_MEMORY.md",
            "DIGIMUNDO_PRESENTE.md",
            "claude_rag.py",
            "auto_archive.py",
            "__init__.py",
            "*.db"
        ]

    def is_single_use(self, filepath: Path) -> bool:
        """Determina se arquivo é de uso único"""

        # Verifica proteção
        for pattern in self.protected_patterns:
            if filepath.match(pattern):
                return False

        # Verifica padrões de uso único
        for pattern in self.single_use_patterns:
            if filepath.match(pattern):
                return True

        # Verifica por comentários específicos
        if filepath.suffix == '.py':
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read(500)  # Primeiros 500 chars
                    if any(marker in content.lower() for marker in [
                        'uso único',
                        'single use',
                        'temporary',
                        'one-time',
                        'delete after'
                    ]):
                        return True
            except:
                pass

        return False

    def create_session_archive(self) -> Path:
        """Cria pasta de arquivo para sessão atual"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_path = self.archive_base / f"session_{timestamp}"
        session_path.mkdir(exist_ok=True)
        return session_path

    def archive_file(self, filepath: Path, session_path: Path) -> dict:
        """Arquiva um arquivo e retorna metadados"""

        # Calcula hash para verificação
        with open(filepath, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        # Destino no arquivo
        relative_path = filepath.relative_to(self.base_path)
        dest_path = session_path / relative_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Move arquivo
        shutil.move(str(filepath), str(dest_path))

        return {
            'original_path': str(filepath),
            'archive_path': str(dest_path),
            'relative_path': str(relative_path),
            'hash': file_hash,
            'size': dest_path.stat().st_size,
            'timestamp': datetime.now().isoformat()
        }

    def scan_and_archive(self) -> tuple[list, Path]:
        """
        Escaneia e arquiva arquivos de uso único
        Retorna lista de arquivos arquivados e caminho da sessão
        """

        archived_files = []
        session_path = None

        # Busca arquivos candidatos
        for pattern in self.single_use_patterns:
            for filepath in self.base_path.rglob(pattern):
                # Pula se já está no archive
                if 'archive' in filepath.parts:
                    continue

                if self.is_single_use(filepath):
                    # Cria sessão se necessário
                    if session_path is None:
                        session_path = self.create_session_archive()

                    # Arquiva
                    metadata = self.archive_file(filepath, session_path)
                    archived_files.append(metadata)

        return archived_files, session_path

    def create_session_log(self, archived_files: list, session_path: Path):
        """Cria log da sessão com arquivos arquivados"""

        if not archived_files:
            return

        log_path = session_path / "SESSION_LOG.md"

        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"# Sessão {session_path.name}\n\n")
            f.write(f"## Arquivos Arquivados: {len(archived_files)}\n\n")

            for file_info in archived_files:
                f.write(f"### {file_info['relative_path']}\n")
                f.write(f"- Hash: {file_info['hash']}\n")
                f.write(f"- Tamanho: {file_info['size']} bytes\n")
                f.write(f"- Timestamp: {file_info['timestamp']}\n\n")

        # Também salva JSON para processamento
        json_path = session_path / "archived_files.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(archived_files, f, indent=2)

    def execute_archiving(self) -> str:
        """
        Executa arquivamento completo e retorna resumo
        """

        print("🗂️ Iniciando arquivamento automático...")

        archived_files, session_path = self.scan_and_archive()

        if archived_files:
            self.create_session_log(archived_files, session_path)

            summary = f"""
📦 Arquivamento Completo:
- Sessão: {session_path.name}
- Arquivos arquivados: {len(archived_files)}
- Espaço liberado: {sum(f['size'] for f in archived_files):,} bytes

Arquivos movidos:
"""
            for f in archived_files[:5]:  # Mostra primeiros 5
                summary += f"  • {f['relative_path']}\n"

            if len(archived_files) > 5:
                summary += f"  ... e mais {len(archived_files)-5} arquivos\n"

        else:
            summary = "✅ Nenhum arquivo de uso único encontrado para arquivar"

        return summary

# Interface global
def auto_archive_before_digimundo():
    """
    Função para chamar antes de declarar DIGIMUNDO PRESENTE
    Arquiva automaticamente arquivos de uso único
    """
    archiver = AutoArchiver()
    summary = archiver.execute_archiving()
    print(summary)
    return summary

if __name__ == "__main__":
    # Teste do sistema
    result = auto_archive_before_digimundo()
    print("\nDIGIMUNDO PRESENTE 🔥")