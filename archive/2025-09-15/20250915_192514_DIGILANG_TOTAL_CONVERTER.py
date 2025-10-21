#!/usr/bin/env python3
"""
🔄 DIGILANG TOTAL CONVERTER
Converte TODO o ecossistema Digimundo para DigiLang
Nível: Revolucionário | Vale do Silício
"""

import os
import json
import shutil
import hashlib
import re
import ast
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class DigiLangTotalConverter:
    """Conversor total do Digimundo para DigiLang"""
    
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.backup_path = self.base_path / f"BACKUP_PRE_DIGILANG_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.digilang_path = self.base_path / "𝕯𝖎𝖌𝖎𝖒𝖚𝖓𝖉𝖔"  # Nome em símbolos especiais
        
        # Carrega vocabulário
        self.load_vocabulary()
        
        # Estatísticas
        self.stats = {
            "files_converted": 0,
            "functions_renamed": 0,
            "variables_renamed": 0,
            "logs_converted": 0,
            "total_compression": 0
        }
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║         🔄 DIGILANG TOTAL CONVERTER - REVOLUÇÃO             ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        
    def load_vocabulary(self):
        """Carrega vocabulário completo DigiLang"""
        vocab_path = self.base_path / "core/digilang/DIGILANG_DIGIMUNDO_COMPLETE.json"
        
        if vocab_path.exists():
            with open(vocab_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.symbols = data.get('symbols', {})
                self.reverse = data.get('reverse', {})
                print(f"✅ Vocabulário carregado: {len(self.symbols)} palavras")
        else:
            raise FileNotFoundError("DigiLang vocabulary not found!")
            
    def create_backup(self):
        """Cria backup completo antes da conversão"""
        print(f"\n📦 Criando backup em {self.backup_path}...")
        
        # Copia toda a estrutura
        shutil.copytree(
            self.base_path,
            self.backup_path,
            ignore=shutil.ignore_patterns('BACKUP_*', '*.pyc', '__pycache__')
        )
        
        print(f"✅ Backup criado com sucesso!")
        
    def convert_filename(self, filename: str) -> str:
        """Converte nome de arquivo para símbolos"""
        # Remove extensão
        name_parts = filename.rsplit('.', 1)
        base_name = name_parts[0]
        extension = name_parts[1] if len(name_parts) > 1 else ''
        
        # Converte cada palavra do nome
        words = re.findall(r'[A-Z][a-z]+|[a-z]+|[A-Z]+|\d+', base_name)
        
        symbols = []
        for word in words:
            word_lower = word.lower()
            if word_lower in self.symbols:
                symbols.append(self.symbols[word_lower])
            else:
                # Hash para palavras desconhecidas
                hash_val = hashlib.md5(word_lower.encode()).hexdigest()[:3]
                symbol = chr(0x2600 + int(hash_val, 16) % 500)
                symbols.append(symbol)
                
        # Monta novo nome
        new_name = ''.join(symbols)
        
        # Adiciona extensão convertida
        ext_map = {
            'py': '🐍',
            'js': '☕',
            'sh': '🐚',
            'json': '📊',
            'txt': '📝',
            'md': '📚',
            'log': '📜',
            'db': '💾',
            'env': '⚙️'
        }
        
        new_ext = ext_map.get(extension, f'.{extension}')
        
        return new_name + new_ext
        
    def convert_python_code(self, code: str) -> Tuple[str, Dict]:
        """Converte código Python para usar DigiLang"""
        changes = {
            "functions": {},
            "variables": {},
            "strings": {}
        }
        
        try:
            tree = ast.parse(code)
            
            class DigiLangTransformer(ast.NodeTransformer):
                def visit_FunctionDef(self, node):
                    # Converte nomes de funções
                    old_name = node.name
                    if not old_name.startswith('__'):  # Não muda métodos especiais
                        words = re.findall(r'[A-Z][a-z]+|[a-z]+|[A-Z]+', old_name)
                        new_name = ''.join(
                            self.parent.symbols.get(w.lower(), w[0]) 
                            for w in words
                        )
                        changes["functions"][old_name] = new_name
                        node.name = new_name
                    
                    self.generic_visit(node)
                    return node
                    
                def visit_Name(self, node):
                    # Converte nomes de variáveis
                    old_name = node.id
                    if not old_name.startswith('_') and old_name.lower() in self.parent.symbols:
                        new_name = self.parent.symbols[old_name.lower()]
                        changes["variables"][old_name] = new_name
                        node.id = new_name
                    
                    return node
                    
                def visit_Str(self, node):
                    # Converte strings literais (mensagens)
                    if isinstance(node.s, str) and len(node.s) > 10:
                        compressed = self.parent.compress_text(node.s)
                        if len(compressed) < len(node.s) * 0.8:  # Só se comprimir 20%+
                            changes["strings"][node.s[:30]] = compressed[:30]
                            node.s = f"📝{compressed}📝"  # Marca strings comprimidas
                    
                    return node
                    
            transformer = DigiLangTransformer()
            transformer.parent = self
            
            # Transforma a AST
            transformed = transformer.visit(tree)
            
            # Converte de volta para código
            try:
                import astor
                new_code = astor.to_source(transformed)
            except:
                # Fallback: conversão simples por substituição
                new_code = code
                for old, new in changes["functions"].items():
                    new_code = re.sub(rf'\b{old}\b', new, new_code)
                for old, new in changes["variables"].items():
                    new_code = re.sub(rf'\b{old}\b', new, new_code)
                    
        except SyntaxError:
            # Se não conseguir parsear, faz conversão básica
            new_code = self.basic_code_conversion(code)
            
        return new_code, changes
        
    def basic_code_conversion(self, code: str) -> str:
        """Conversão básica de código quando AST falha"""
        # Palavras-chave comuns para converter
        replacements = {
            'data': self.symbols.get('data', '📊'),
            'process': self.symbols.get('process', '🔄'),
            'system': self.symbols.get('system', '🌐'),
            'energy': self.symbols.get('energy', '⚡'),
            'memory': self.symbols.get('memory', '💾'),
            'network': self.symbols.get('network', '🌍'),
            'file': self.symbols.get('file', '📁'),
            'save': self.symbols.get('save', '💾'),
            'load': self.symbols.get('load', '📥'),
            'error': self.symbols.get('error', '❌'),
            'warning': self.symbols.get('warning', '⚠️'),
            'success': self.symbols.get('success', '✅'),
        }
        
        new_code = code
        for word, symbol in replacements.items():
            # Substitui palavras completas
            new_code = re.sub(rf'\b{word}\b', symbol, new_code, flags=re.IGNORECASE)
            
        return new_code
        
    def compress_text(self, text: str) -> str:
        """Comprime texto para DigiLang"""
        words = text.lower().split()
        compressed = []
        
        for word in words:
            if word in self.symbols:
                compressed.append(self.symbols[word])
            elif len(word) > 3:  # Só comprime palavras maiores
                hash_val = hashlib.md5(word.encode()).hexdigest()[:3]
                compressed.append(chr(0x4E00 + int(hash_val, 16) % 1000))
            else:
                compressed.append(word)
                
        return ' '.join(compressed)
        
    def convert_shell_script(self, script: str) -> str:
        """Converte shell script para DigiLang"""
        lines = script.split('\n')
        new_lines = []
        
        for line in lines:
            # Pula comentários de cabeçalho
            if line.startswith('#!'):
                new_lines.append(line)
                continue
                
            # Converte echo/print statements
            if 'echo' in line or 'printf' in line:
                # Extrai mensagem
                match = re.search(r'echo\s+["\'](.+?)["\']', line)
                if match:
                    msg = match.group(1)
                    compressed = self.compress_text(msg)
                    line = line.replace(msg, compressed)
                    
            # Converte nomes de variáveis
            for word in ['SYSTEM', 'PROCESS', 'DATA', 'MEMORY', 'NETWORK']:
                if word in line:
                    symbol = self.symbols.get(word.lower(), word[0])
                    line = line.replace(word, symbol)
                    
            new_lines.append(line)
            
        return '\n'.join(new_lines)
        
    def convert_directory(self, dir_path: Path, level: int = 0):
        """Converte recursivamente um diretório"""
        indent = "  " * level
        
        # Lista arquivos e pastas
        items = sorted(dir_path.iterdir())
        
        for item in items:
            # Pula backups e caches
            if any(skip in str(item) for skip in ['BACKUP_', '__pycache__', '.git']):
                continue
                
            if item.is_file():
                # Converte arquivo
                print(f"{indent}📄 {item.name}", end=" ")
                
                try:
                    # Determina tipo e converte
                    if item.suffix == '.py':
                        with open(item, 'r', encoding='utf-8') as f:
                            original = f.read()
                        
                        converted, changes = self.convert_python_code(original)
                        
                        # Salva com novo nome
                        new_name = self.convert_filename(item.name)
                        new_path = item.parent / new_name
                        
                        with open(new_path, 'w', encoding='utf-8') as f:
                            f.write(converted)
                            
                        # Remove original se diferente
                        if new_path != item:
                            item.unlink()
                            
                        self.stats["files_converted"] += 1
                        self.stats["functions_renamed"] += len(changes.get("functions", {}))
                        self.stats["variables_renamed"] += len(changes.get("variables", {}))
                        
                        print(f"→ {new_name} ✅")
                        
                    elif item.suffix == '.sh':
                        with open(item, 'r', encoding='utf-8') as f:
                            original = f.read()
                        
                        converted = self.convert_shell_script(original)
                        
                        new_name = self.convert_filename(item.name)
                        new_path = item.parent / new_name
                        
                        with open(new_path, 'w', encoding='utf-8') as f:
                            f.write(converted)
                            
                        if new_path != item:
                            item.unlink()
                            
                        self.stats["files_converted"] += 1
                        print(f"→ {new_name} ✅")
                        
                    elif item.suffix in ['.txt', '.log', '.md']:
                        # Comprime conteúdo de texto
                        with open(item, 'r', encoding='utf-8') as f:
                            original = f.read()
                        
                        compressed = self.compress_text(original)
                        
                        new_name = self.convert_filename(item.name)
                        new_path = item.parent / new_name
                        
                        with open(new_path, 'w', encoding='utf-8') as f:
                            f.write(compressed)
                            
                        if new_path != item:
                            item.unlink()
                            
                        self.stats["logs_converted"] += 1
                        compression = (1 - len(compressed) / len(original)) * 100
                        self.stats["total_compression"] += compression
                        
                        print(f"→ {new_name} ✅ ({compression:.0f}% compressão)")
                        
                    else:
                        # Apenas renomeia outros arquivos
                        new_name = self.convert_filename(item.name)
                        new_path = item.parent / new_name
                        
                        if new_path != item:
                            item.rename(new_path)
                            
                        print(f"→ {new_name} ✅")
                        
                except Exception as e:
                    print(f"❌ Erro: {e}")
                    
            elif item.is_dir():
                # Converte nome da pasta
                print(f"{indent}📁 {item.name}/")
                
                new_name = self.convert_filename(item.name)
                new_path = item.parent / new_name
                
                if new_path != item:
                    item.rename(new_path)
                    item = new_path
                    
                print(f"{indent}   → {new_name}/ ✅")
                
                # Recursão
                self.convert_directory(item, level + 1)
                
    def create_translation_map(self):
        """Cria mapa de tradução para referência"""
        map_path = self.base_path / "DIGILANG_TRANSLATION_MAP.json"
        
        translation_map = {
            "timestamp": datetime.now().isoformat(),
            "stats": self.stats,
            "file_mappings": {},
            "function_mappings": {},
            "variable_mappings": {},
            "common_translations": {
                "system": self.symbols.get("system", "🌐"),
                "process": self.symbols.get("process", "🔄"),
                "data": self.symbols.get("data", "📊"),
                "energy": self.symbols.get("energy", "⚡"),
                "memory": self.symbols.get("memory", "💾"),
                "network": self.symbols.get("network", "🌍"),
                "file": self.symbols.get("file", "📁"),
                "digimundo": "𝕯𝖎𝖌𝖎𝖒𝖚𝖓𝖉𝖔"
            }
        }
        
        with open(map_path, 'w', encoding='utf-8') as f:
            json.dump(translation_map, f, indent=2, ensure_ascii=False)
            
        print(f"\n📍 Mapa de tradução salvo em: {map_path}")
        
    def create_launcher_in_digilang(self):
        """Cria launcher completamente em DigiLang"""
        launcher_content = f"""#!/bin/bash
# {'🚀 𝕯𝖎𝖌𝖎𝖒𝖚𝖓𝖉𝖔 🌐'}

{self.symbols.get('system', '🌐')}="{self.base_path}"
{self.symbols.get('memory', '💾')}="${{self.symbols.get('system', '🌐')}}}/memory"
{self.symbols.get('data', '📊')}="${{self.symbols.get('system', '🌐')}}}/data"

echo "{'⚡ 🔄 🌐 💾'}"

# {self.compress_text('Initialize system')}
{self.symbols.get('process', '🔄')}() {{
    echo "{'⚡'}: $(pmset -g batt)"
    echo "{'📊'}: $(df -h)"
    echo "{'🌐'}: $(ifconfig | grep inet)"
}}

# {self.compress_text('Main execution')}
{self.symbols.get('process', '🔄')}

echo "{'✅ 𝕯𝖎𝖌𝖎𝖒𝖚𝖓𝖉𝖔 🚀'}"
"""
        
        launcher_path = self.base_path / "🚀🌐🐚"  # Launch system shell
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
            
        os.chmod(launcher_path, 0o755)
        print(f"✅ Launcher DigiLang criado: {launcher_path}")
        
    def generate_report(self):
        """Gera relatório da conversão"""
        print("\n" + "="*60)
        print("           📊 RELATÓRIO DE CONVERSÃO DIGILANG")
        print("="*60)
        
        print(f"\n📈 ESTATÍSTICAS:")
        print(f"   Arquivos convertidos: {self.stats['files_converted']}")
        print(f"   Funções renomeadas: {self.stats['functions_renamed']}")
        print(f"   Variáveis renomeadas: {self.stats['variables_renamed']}")
        print(f"   Logs comprimidos: {self.stats['logs_converted']}")
        
        if self.stats['logs_converted'] > 0:
            avg_compression = self.stats['total_compression'] / self.stats['logs_converted']
            print(f"   Compressão média: {avg_compression:.1f}%")
            
        print(f"\n🏗️ NOVA ESTRUTURA:")
        print(f"   Diretório principal: 𝕯𝖎𝖌𝖎𝖒𝖚𝖓𝖉𝖔")
        print(f"   Launcher: 🚀🌐🐚")
        print(f"   Arquivos: Convertidos para símbolos")
        print(f"   Código: Variáveis e funções em DigiLang")
        
        print(f"\n✨ TRANSFORMAÇÃO COMPLETA!")
        print(f"   O Digimundo agora fala nativamente DigiLang!")
        
    def run_complete_conversion(self):
        """Executa conversão completa do Digimundo"""
        print("\n⚠️ ATENÇÃO: Esta operação converterá TODO o Digimundo para DigiLang!")
        print("Isso inclui:")
        print("  • Renomear TODOS os arquivos para símbolos")
        print("  • Converter variáveis e funções no código")
        print("  • Comprimir logs e mensagens")
        print("  • Criar nova estrutura em DigiLang")
        
        response = input("\n❓ Deseja continuar? (sim/não): ")
        
        if response.lower() != 'sim':
            print("❌ Conversão cancelada")
            return
            
        # Executa conversão
        print("\n🚀 INICIANDO CONVERSÃO TOTAL...")
        
        # 1. Backup
        self.create_backup()
        
        # 2. Converte recursivamente
        print("\n📂 CONVERTENDO ARQUIVOS...")
        self.convert_directory(self.base_path)
        
        # 3. Cria launcher DigiLang
        self.create_launcher_in_digilang()
        
        # 4. Cria mapa de tradução
        self.create_translation_map()
        
        # 5. Relatório final
        self.generate_report()
        
        print("\n🎯 CONVERSÃO COMPLETA!")
        print("   Backup salvo em:", self.backup_path)
        print("   Para reverter: mv", self.backup_path, self.base_path)


if __name__ == "__main__":
    converter = DigiLangTotalConverter()
    converter.run_complete_conversion()