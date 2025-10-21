#!/usr/bin/env python3
"""
Sistema de Arquivamento com Deduplicação usando Git
Técnica: Organização por data (YYYY-MM) sem repetições
"""

import os
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
import json
import subprocess

# Pastas para arquivar
SOURCE_DIRS = [
    '/Users/clubproducoes/Digimundo/scripturemon-champion',
    '/Users/clubproducoes/Digimundo/scripturemon-champion-refactored_chatgpt',
    '/Users/clubproducoes/Digimundo/Respostas CHAT GPT',
    '/Users/clubproducoes/Digimundo/Pre_Limpeza_Minimalista_Lixo',
    '/Users/clubproducoes/Digimundo/Respostas_testes'
]

# Arquivos soltos para arquivar
SOURCE_FILES = [
    '/Users/clubproducoes/Digimundo/ollama_multi_system.py',
    '/Users/clubproducoes/Digimundo/analyze_backups_digimunod.py'
]

# Destino do arquivo
ARCHIVE_BASE = '/Users/clubproducoes/Digimundo/Archive/scripturemon-history'

class ArchiveDeduplicator:
    def __init__(self):
        self.file_hashes = {}  # hash -> (path, size, mtime)
        self.duplicates = []   # Lista de duplicados encontrados
        self.stats = {
            'total_files': 0,
            'unique_files': 0,
            'duplicates': 0,
            'space_saved': 0
        }
        
    def get_file_hash(self, filepath):
        """Calcula SHA256 do arquivo"""
        sha256 = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except:
            return None
            
    def get_git_info(self, filepath):
        """Pega informações do git se disponível"""
        try:
            dir_path = os.path.dirname(filepath)
            # Tenta pegar a data do último commit
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%ai', '--', filepath],
                cwd=dir_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout:
                return datetime.fromisoformat(result.stdout.strip())
        except:
            pass
        # Fallback para mtime do arquivo
        return datetime.fromtimestamp(os.path.getmtime(filepath))
        
    def scan_directory(self, directory):
        """Escaneia diretório e cataloga arquivos"""
        print(f"\n🔍 Escaneando: {directory}")
        
        if not os.path.exists(directory):
            print(f"  ⚠️  Não encontrado: {directory}")
            return
            
        for root, dirs, files in os.walk(directory):
            # Ignora diretórios do git e node_modules
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.DS_Store']]
            
            for file in files:
                if file.startswith('.') or file.endswith('.pyc'):
                    continue
                    
                filepath = os.path.join(root, file)

                # Ignora symlinks
                if os.path.islink(filepath):
                    continue

                self.stats['total_files'] += 1

                # Calcula hash
                file_hash = self.get_file_hash(filepath)
                if not file_hash:
                    continue
                    
                file_size = os.path.getsize(filepath)
                file_date = self.get_git_info(filepath)
                
                if file_hash in self.file_hashes:
                    # Duplicado encontrado
                    self.duplicates.append({
                        'original': self.file_hashes[file_hash]['path'],
                        'duplicate': filepath,
                        'size': file_size,
                        'hash': file_hash
                    })
                    self.stats['duplicates'] += 1
                    self.stats['space_saved'] += file_size
                else:
                    # Arquivo único
                    self.file_hashes[file_hash] = {
                        'path': filepath,
                        'size': file_size,
                        'date': file_date,
                        'relative_path': os.path.relpath(filepath, directory)
                    }
                    self.stats['unique_files'] += 1
                    
    def organize_by_date(self):
        """Organiza arquivos por data YYYY-MM"""
        organized = {}
        
        for hash_val, info in self.file_hashes.items():
            date_key = info['date'].strftime('%Y-%m')
            if date_key not in organized:
                organized[date_key] = []
            organized[date_key].append(info)
            
        return organized
        
    def archive_files(self, dry_run=True):
        """Arquiva arquivos sem duplicação"""
        print("\n📦 Iniciando arquivamento...")
        
        # Escaneia todas as pastas
        for directory in SOURCE_DIRS:
            self.scan_directory(directory)
            
        # Escaneia arquivos soltos
        for filepath in SOURCE_FILES:
            if os.path.exists(filepath):
                print(f"\n🔍 Escaneando arquivo: {filepath}")
                self.stats['total_files'] += 1
                
                file_hash = self.get_file_hash(filepath)
                if file_hash and file_hash not in self.file_hashes:
                    file_size = os.path.getsize(filepath)
                    file_date = self.get_git_info(filepath)
                    self.file_hashes[file_hash] = {
                        'path': filepath,
                        'size': file_size,
                        'date': file_date,
                        'relative_path': os.path.basename(filepath)
                    }
                    self.stats['unique_files'] += 1
                    
        # Organiza por data
        organized = self.organize_by_date()
        
        # Cria estrutura de arquivamento
        os.makedirs(ARCHIVE_BASE, exist_ok=True)
        
        # Categorias
        categories = {
            '.py': 'code',
            '.js': 'code',
            '.ts': 'code',
            '.jsx': 'code',
            '.tsx': 'code',
            '.md': 'docs',
            '.txt': 'docs',
            '.pdf': 'docs',
            '.json': 'config',
            '.yaml': 'config',
            '.yml': 'config',
            '.toml': 'config',
        }
        
        archived = []
        
        for date_key, files in sorted(organized.items()):
            print(f"\n📅 Processando {date_key}: {len(files)} arquivos")
            
            for file_info in files:
                # Determina categoria
                ext = Path(file_info['path']).suffix.lower()
                category = categories.get(ext, 'misc')
                
                # Cria caminho de destino
                dest_dir = Path(ARCHIVE_BASE) / category / date_key
                # Limita tamanho do caminho
                relative = file_info['relative_path']
                if len(relative) > 100:
                    # Pega apenas nome do arquivo se caminho muito longo
                    relative = Path(relative).name
                dest_file = dest_dir / relative
                
                if dry_run:
                    print(f"  [DRY RUN] {file_info['path'][:50]}... -> {dest_file}")
                else:
                    # Cria diretório se necessário
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Copia arquivo se não existir
                    if not dest_file.exists():
                        shutil.copy2(file_info['path'], dest_file)
                        print(f"  ✅ Arquivado: {dest_file.name}")
                        archived.append(str(dest_file))
                    else:
                        print(f"  ⏭️ Já existe: {dest_file.name}")
                        
        # Salva relatório
        report = {
            'timestamp': datetime.now().isoformat(),
            'stats': self.stats,
            'duplicates_found': len(self.duplicates),
            'unique_files': len(self.file_hashes),
            'dates_covered': list(organized.keys()),
            'archived_files': archived if not dry_run else [],
            'duplicate_details': self.duplicates[:10]  # Primeiros 10 duplicados
        }
        
        report_path = Path(ARCHIVE_BASE) / f"archive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        print(f"\n📊 Relatório salvo: {report_path}")
        
        # Estatísticas finais
        print(f"\n📦 RESUMO DO ARQUIVAMENTO:")
        print(f"  Total de arquivos: {self.stats['total_files']}")
        print(f"  Arquivos únicos: {self.stats['unique_files']}")
        print(f"  Duplicados encontrados: {self.stats['duplicates']}")
        print(f"  Espaço economizado: {self.stats['space_saved'] / 1024 / 1024:.2f} MB")
        print(f"  Períodos cobertos: {len(organized)} meses")
        
        if dry_run:
            print("\n⚠️  DRY RUN - Nenhum arquivo foi movido")
            print("Execute com --execute para realizar o arquivamento")
        else:
            print(f"\n✅ {len(archived)} arquivos arquivados com sucesso!")
            
        return report
        
    def cleanup_sources(self, verify_first=True):
        """Remove pastas originais após verificar arquivamento"""
        if verify_first:
            print("\n🔍 Verificando integridade do arquivo...")
            
            # Verifica se todos os arquivos únicos foram arquivados
            missing = []
            for hash_val, info in self.file_hashes.items():
                # Constrói caminho esperado no arquivo
                ext = Path(info['path']).suffix.lower()
                category = 'code' if ext in ['.py', '.js', '.ts'] else 'misc'
                date_key = info['date'].strftime('%Y-%m')
                expected = Path(ARCHIVE_BASE) / category / date_key / info['relative_path']
                
                if not expected.exists():
                    missing.append(info['path'])
                    
            if missing:
                print(f"\n❌ {len(missing)} arquivos não foram arquivados!")
                print("Abortando limpeza. Arquivos faltando:")
                for m in missing[:10]:
                    print(f"  - {m}")
                return False
                
        print("\n🗑️ Removendo pastas originais...")
        
        for directory in SOURCE_DIRS:
            if os.path.exists(directory):
                print(f"  Removendo: {directory}")
                # shutil.rmtree(directory)  # COMENTADO POR SEGURANÇA
                print(f"    [SIMULADO] rm -rf {directory}")
                
        for filepath in SOURCE_FILES:
            if os.path.exists(filepath):
                print(f"  Removendo: {filepath}")
                # os.remove(filepath)  # COMENTADO POR SEGURANÇA
                print(f"    [SIMULADO] rm {filepath}")
                
        print("\n✅ Limpeza concluída!")
        return True


if __name__ == "__main__":
    import sys
    
    dedup = ArchiveDeduplicator()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--execute':
        # Execução real
        dedup.archive_files(dry_run=False)
        
        if len(sys.argv) > 2 and sys.argv[2] == '--cleanup':
            dedup.cleanup_sources()
    else:
        # Dry run
        dedup.archive_files(dry_run=True)