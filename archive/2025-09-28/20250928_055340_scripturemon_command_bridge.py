#!/usr/bin/env python3
"""
SCRIPTUREMON COMMAND BRIDGE - ULTIMATE EDITION
Permite ao Scripturemon executar comandos como Claude
"""

import os
import sys
import json
import shutil
import subprocess
import sqlite3
from pathlib import Path
from datetime import datetime
import ollama

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class ScripturemonCommandBridge:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")
        self.safe_commands = {
            'mkdir': self.safe_mkdir,
            'move': self.safe_move,
            'copy': self.safe_copy,
            'rename': self.safe_rename,
            'delete': self.safe_delete,
            'restore': self.restore_from_trash,
            'organize': self.organize_files,
            'create_structure': self.create_knowledge_structure,
            'list': self.list_directory,
            'search': self.search_files,
            'backup': self.backup_files,
        }

    def safe_mkdir(self, directory_name, parent=""):
        """Cria diretórios de forma segura"""
        # Validação adicional de caracteres perigosos
        dangerous_chars = ['..', ';', '&', '|', '`', '$', '>', '<', '*', '?']
        if any(char in directory_name for char in dangerous_chars):
            return {"error": "Caracteres perigosos detectados"}

        if parent:
            full_path = self.base_path / parent / directory_name
        else:
            full_path = self.base_path / directory_name

        if not str(full_path).startswith(str(self.base_path)):
            return {"error": "Caminho inseguro"}

        try:
            full_path.mkdir(parents=True, exist_ok=True)
            return {"success": f"Diretório criado: {full_path.name}", "path": str(full_path)}
        except Exception as e:
            return {"error": str(e)}

    def safe_move(self, source, destination):
        """Move arquivos de forma segura"""
        src_path = self.base_path / source
        dst_path = self.base_path / destination

        if not (str(src_path).startswith(str(self.base_path)) and
                str(dst_path).startswith(str(self.base_path))):
            return {"error": "Caminhos inseguros"}

        try:
            if src_path.exists():
                # Cria diretório destino se não existe
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src_path), str(dst_path))
                return {"success": f"Movido: {source} → {destination}"}
            else:
                return {"error": f"Arquivo não encontrado: {source}"}
        except Exception as e:
            return {"error": str(e)}

    def safe_copy(self, source, destination):
        """Copia arquivos de forma segura"""
        src_path = self.base_path / source
        dst_path = self.base_path / destination

        if not (str(src_path).startswith(str(self.base_path)) and
                str(dst_path).startswith(str(self.base_path))):
            return {"error": "Caminhos inseguros"}

        try:
            if src_path.exists():
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                if src_path.is_dir():
                    shutil.copytree(str(src_path), str(dst_path), dirs_exist_ok=True)
                else:
                    shutil.copy2(str(src_path), str(dst_path))
                return {"success": f"Copiado: {source} → {destination}"}
            else:
                return {"error": f"Arquivo não encontrado: {source}"}
        except Exception as e:
            return {"error": str(e)}

    def safe_rename(self, old_name, new_name):
        """Renomeia arquivos de forma segura"""
        old_path = self.base_path / old_name
        new_path = self.base_path / new_name

        if not (str(old_path).startswith(str(self.base_path)) and
                str(new_path).startswith(str(self.base_path))):
            return {"error": "Caminhos inseguros"}

        try:
            if old_path.exists():
                old_path.rename(new_path)
                return {"success": f"Renomeado: {old_name} → {new_name}"}
            else:
                return {"error": f"Arquivo não encontrado: {old_name}"}
        except Exception as e:
            return {"error": str(e)}

    def organize_files(self, pattern="", target_dir=""):
        """Organiza arquivos baseado em padrões"""
        try:
            results = []
            for file_path in self.base_path.glob(pattern or "*"):
                if file_path.is_file():
                    if target_dir:
                        target = self.base_path / target_dir
                        target.mkdir(exist_ok=True)
                        new_path = target / file_path.name
                        file_path.rename(new_path)
                        results.append(f"Organizado: {file_path.name} → {target_dir}/")
            return {"success": f"Organizados {len(results)} arquivos", "details": results}
        except Exception as e:
            return {"error": str(e)}

    def create_knowledge_structure(self):
        """Cria estrutura de conhecimento completa"""
        structure = {
            'knowledge': {
                'roteiro': ['estrutura', 'personagens', 'dialogo', 'conflito'],
                'teoria_roteiro': ['mckee', 'truby', 'snyder', 'field'],
                'estudos_de_caso': ['classicos', 'modernos', 'generos'],
                'referencias': ['livros', 'artigos', 'videos'],
                'projetos': ['em_andamento', 'completos', 'ideias']
            },
            'workspace': {
                'drafts': [],
                'reviews': [],
                'final': []
            }
        }

        try:
            results = []
            for main_dir, subdirs in structure.items():
                main_path = self.base_path / main_dir
                main_path.mkdir(exist_ok=True)
                results.append(f"Criado: {main_dir}/")

                if isinstance(subdirs, dict):
                    for sub_dir, sub_subdirs in subdirs.items():
                        sub_path = main_path / sub_dir
                        sub_path.mkdir(exist_ok=True)
                        results.append(f"Criado: {main_dir}/{sub_dir}/")

                        for sub_sub_dir in sub_subdirs:
                            sub_sub_path = sub_path / sub_sub_dir
                            sub_sub_path.mkdir(exist_ok=True)
                            results.append(f"Criado: {main_dir}/{sub_dir}/{sub_sub_dir}/")
                else:
                    for sub_dir in subdirs:
                        sub_path = main_path / sub_dir
                        sub_path.mkdir(exist_ok=True)
                        results.append(f"Criado: {main_dir}/{sub_dir}/")

            return {"success": f"Estrutura completa criada", "details": results}
        except Exception as e:
            return {"error": str(e)}

    def list_directory(self, directory=""):
        """Lista conteúdo de diretório"""
        target = self.base_path / directory if directory else self.base_path

        if not str(target).startswith(str(self.base_path)):
            return {"error": "Caminho inseguro"}

        try:
            items = []
            for item in target.iterdir():
                item_info = {
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None,
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                }
                items.append(item_info)

            return {"success": f"Listado {len(items)} itens", "items": items}
        except Exception as e:
            return {"error": str(e)}

    def search_files(self, pattern, directory=""):
        """Busca arquivos por padrão"""
        search_path = self.base_path / directory if directory else self.base_path

        try:
            matches = []
            for match in search_path.rglob(pattern):
                if search_path != self.base_path:
                    rel_path = match.relative_to(search_path)
                else:
                    rel_path = match.relative_to(self.base_path)
                matches.append(str(rel_path))

            return {"success": f"Encontrados {len(matches)} arquivos", "matches": matches}
        except Exception as e:
            return {"error": str(e)}

    def safe_delete(self, file_pattern, permanent=False):
        """Move arquivos para lixeira (padrão) ou delete permanente se especificado"""
        # Verificar se pode deletar permanentemente
        if permanent:
            found_files = list(self.base_path.glob(file_pattern))
            for file_path in found_files:
                if not (file_path.name.startswith("temp_") or file_path.name.startswith("test_")):
                    return {"error": f"Deleção permanente só permitida para arquivos temp_* ou test_*. Arquivo '{file_path.name}' não permitido."}

        # Validação de caracteres perigosos (* e ? são permitidos para wildcards)
        dangerous_chars = ['..', ';', '&', '|', '`', '$', '>', '<']
        if any(char in file_pattern for char in dangerous_chars):
            return {"error": "Caracteres perigosos detectados"}

        try:
            deleted = []
            files_to_process = list(self.base_path.glob(file_pattern))
            files_to_process = [f for f in files_to_process if f.is_file()]

            if permanent:
                # Deleção permanente apenas para arquivos temp/test
                for file_path in files_to_process:
                    file_path.unlink()
                    deleted.append(f"{file_path.name} (PERMANENTE)")
            else:
                # Move para lixeira (padrão seguro)
                trash_dir = self.base_path / "trash" / datetime.now().strftime("%Y%m%d_%H%M%S")
                trash_dir.mkdir(parents=True, exist_ok=True)

                for file_path in files_to_process:
                    trash_path = trash_dir / file_path.name
                    shutil.move(str(file_path), str(trash_path))
                    deleted.append(f"{file_path.name} → lixeira")

            return {"success": f"Deletados {len(deleted)} arquivos", "details": deleted}
        except Exception as e:
            return {"error": str(e)}

    def restore_from_trash(self, file_name=""):
        """Restaura arquivos da lixeira"""
        trash_base = self.base_path / "trash"
        if not trash_base.exists():
            return {"error": "Lixeira não encontrada"}

        try:
            restored = []
            if file_name:
                # Restaura arquivo específico
                for trash_dir in trash_base.iterdir():
                    if trash_dir.is_dir():
                        trash_file = trash_dir / file_name
                        if trash_file.exists():
                            restore_path = self.base_path / file_name
                            shutil.move(str(trash_file), str(restore_path))
                            restored.append(file_name)
                            break
            else:
                # Lista arquivos na lixeira
                items = []
                for trash_dir in trash_base.iterdir():
                    if trash_dir.is_dir():
                        for item in trash_dir.iterdir():
                            items.append({
                                "name": item.name,
                                "deleted_date": trash_dir.name,
                                "size": item.stat().st_size if item.is_file() else None
                            })
                return {"success": f"Lixeira contém {len(items)} itens", "items": items}

            if restored:
                return {"success": f"Restaurados {len(restored)} arquivos", "details": restored}
            else:
                return {"error": f"Arquivo '{file_name}' não encontrado na lixeira"}
        except Exception as e:
            return {"error": str(e)}

    def backup_files(self, source_pattern="*"):
        """Faz backup de arquivos"""
        backup_dir = self.base_path / "backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir.mkdir(parents=True, exist_ok=True)

        try:
            backed_up = []
            for file_path in self.base_path.glob(source_pattern):
                if file_path.is_file() and "backup" not in str(file_path):
                    backup_path = backup_dir / file_path.name
                    shutil.copy2(file_path, backup_path)
                    backed_up.append(file_path.name)

            return {"success": f"Backup de {len(backed_up)} arquivos", "location": str(backup_dir)}
        except Exception as e:
            return {"error": str(e)}

    def execute_command(self, command, **kwargs):
        """Executa comando solicitado pelo Scripturemon"""
        if command not in self.safe_commands:
            return {"error": f"Comando não permitido: {command}"}

        return self.safe_commands[command](**kwargs)

    def process_ollama_request(self, request_text):
        """Processa solicitação em linguagem natural do Ollama"""
        # Parse simples de comandos em linguagem natural
        request_lower = request_text.lower()

        if "criar pasta" in request_lower or "mkdir" in request_lower:
            # Extrair nome da pasta
            import re
            match = re.search(r'(?:criar pasta|mkdir)\s+(.+)', request_lower)
            if match:
                folder_name = match.group(1).strip().replace('"', '').replace("'", "")
                return self.execute_command('mkdir', directory_name=folder_name)

        elif "mover" in request_lower:
            # Extrair origem e destino
            import re
            match = re.search(r'mover\s+(.+?)\s+(?:para|→)\s+(.+)', request_lower)
            if match:
                source = match.group(1).strip()
                dest = match.group(2).strip()
                return self.execute_command('move', source=source, destination=dest)

        elif "organizar" in request_lower:
            return self.execute_command('organize')

        elif "estrutura" in request_lower and "conhecimento" in request_lower:
            return self.execute_command('create_structure')

        elif "listar" in request_lower:
            return self.execute_command('list')

        elif "deletar" in request_lower or "apagar" in request_lower or "remover" in request_lower:
            # Extrair nome do arquivo
            import re
            match = re.search(r'(?:deletar|apagar|remover)\s+(.+)', request_lower)
            if match:
                file_pattern = match.group(1).strip().replace('"', '').replace("'", "")
                permanent = "permanente" in request_lower
                return self.execute_command('delete', file_pattern=file_pattern, permanent=permanent)

        elif "restaurar" in request_lower:
            # Extrair nome do arquivo (opcional)
            import re
            match = re.search(r'restaurar(?:\s+(.+))?', request_lower)
            file_name = match.group(1).strip().replace('"', '').replace("'", "") if match and match.group(1) else ""
            return self.execute_command('restore', file_name=file_name)

        elif "lixeira" in request_lower:
            return self.execute_command('restore')  # Lista lixeira

        elif "backup" in request_lower:
            return self.execute_command('backup')

        return {"error": "Comando não reconhecido", "help": "Comandos disponíveis: criar pasta, mover, deletar, restaurar, organizar, estrutura conhecimento, listar, lixeira, backup"}

def interactive_mode():
    """Modo interativo para testes"""
    bridge = ScripturemonCommandBridge()

    print("🤖 SCRIPTUREMON COMMAND BRIDGE - Modo Interativo")
    print("=" * 50)
    print("Comandos disponíveis:")
    print("- criar pasta <nome>")
    print("- mover <origem> para <destino>")
    print("- deletar <arquivo> (move para lixeira)")
    print("- deletar <arquivo> permanente (só temp_* e test_*)")
    print("- restaurar <arquivo> (da lixeira)")
    print("- lixeira (ver conteúdo)")
    print("- organizar")
    print("- estrutura conhecimento")
    print("- listar")
    print("- backup")
    print("- quit (sair)")
    print("")

    while True:
        try:
            user_input = input("scripturemon> ").strip()

            if user_input.lower() in ['quit', 'exit', 'sair']:
                print("👋 Saindo...")
                break

            if not user_input:
                continue

            result = bridge.process_ollama_request(user_input)

            if "error" in result:
                print(f"❌ Erro: {result['error']}")
                if "help" in result:
                    print(f"💡 {result['help']}")
            else:
                print(f"✅ {result['success']}")
                if "details" in result:
                    for detail in result['details'][:5]:  # Mostra apenas primeiros 5
                        print(f"   - {detail}")
                    if len(result['details']) > 5:
                        print(f"   ... e mais {len(result['details']) - 5} itens")

        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro interno: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Modo comando único
        bridge = ScripturemonCommandBridge()
        request = " ".join(sys.argv[1:])
        result = bridge.process_ollama_request(request)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Modo interativo
        interactive_mode()