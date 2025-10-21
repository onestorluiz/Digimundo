#!/usr/bin/env python3
"""
DEDUPLICAÇÃO INTELIGENTE USANDO DOCUMENTAÇÃO PRESERVADA
Usa nossa própria documentação como referência para identificar arquivos legítimos
"""

import os
import re
from pathlib import Path
from datetime import datetime
import hashlib

class IntelligentDeduplicator:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.documented_files = set()
        self.evolution_timeline = {}
        self.legitimate_patterns = set()

    def load_documentation_knowledge(self):
        """Extrai conhecimento dos arquivos de documentação que criamos"""
        print("📚 Carregando conhecimento da documentação...")

        # Procurar arquivos de documentação
        doc_files = []
        preservation_path = self.base_path / "SURGICAL_PRESERVATION"

        for doc_type in ["EVOLUTION_LOG*.md", "TECHNICAL_CHANGES*.md", "LESSONS_LEARNED*.md"]:
            doc_files.extend(preservation_path.rglob(doc_type))

        # Extrair nomes de arquivos mencionados na documentação
        for doc_file in doc_files:
            self.extract_file_references(doc_file)

        print(f"✅ Encontrados {len(self.documented_files)} arquivos documentados")

    def extract_file_references(self, doc_file):
        """Extrai referências a arquivos da documentação"""
        try:
            content = doc_file.read_text(encoding='utf-8')

            # Patterns para encontrar nomes de arquivos na documentação
            file_patterns = [
                r'`([^`]+\.(py|js|json|md|sh|txt))`',  # Arquivos em backticks
                r'"([^"]+\.(py|js|json|md|sh|txt))"',  # Arquivos em aspas
                r'- ([^\s]+\.(py|js|json|md|sh|txt))',  # Arquivos em listas
                r'/([^/\s]+\.(py|js|json|md|sh|txt))',  # Arquivos com path
            ]

            for pattern in file_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    filename = match[0] if isinstance(match, tuple) else match
                    self.documented_files.add(filename)

        except Exception as e:
            print(f"⚠️ Erro lendo {doc_file}: {e}")

    def find_duplicates_intelligently(self, scan_path):
        """Encontra duplicados usando conhecimento da documentação"""
        print(f"🔍 Analisando duplicados em {scan_path}...")

        # Padrões comum de arquivos duplicados pelo Drive
        duplicate_patterns = [
            r'^(.+) \(\d+\)(\.[^.]+)$',        # arquivo (1).ext
            r'^(.+) - Copy(\.[^.]+)$',         # arquivo - Copy.ext
            r'^Copy of (.+)(\.[^.]+)$',        # Copy of arquivo.ext
            r'^(.+) \d{4}-\d{2}-\d{2}(\.[^.]+)$',  # arquivo 2024-01-01.ext
        ]

        files_by_base = {}

        # Agrupar arquivos por nome base
        for file_path in Path(scan_path).rglob("*"):
            if file_path.is_file():
                filename = file_path.name

                # Verificar se é duplicado
                base_name = filename
                is_duplicate = False

                for pattern in duplicate_patterns:
                    match = re.match(pattern, filename)
                    if match:
                        base_name = match.group(1) + (match.group(2) if match.lastindex >= 2 else "")
                        is_duplicate = True
                        break

                if base_name not in files_by_base:
                    files_by_base[base_name] = []

                files_by_base[base_name].append({
                    'path': file_path,
                    'filename': filename,
                    'is_duplicate_pattern': is_duplicate,
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
                    'documented': filename in self.documented_files,
                    'hash': self.quick_hash(file_path) if file_path.stat().st_size < 10*1024*1024 else None
                })

        # Analisar grupos com múltiplos arquivos
        duplicates_analysis = {}
        for base_name, files in files_by_base.items():
            if len(files) > 1:
                duplicates_analysis[base_name] = self.analyze_duplicate_group(files)

        return duplicates_analysis

    def analyze_duplicate_group(self, files):
        """Analisa um grupo de possíveis duplicados"""
        analysis = {
            'files': files,
            'recommendation': None,
            'keep': [],
            'safe_to_delete': [],
            'manual_review': []
        }

        # Separar por documentados vs não documentados
        documented = [f for f in files if f['documented']]
        not_documented = [f for f in files if not f['documented']]

        # Separar por padrões de duplicação
        originals = [f for f in files if not f['is_duplicate_pattern']]
        duplicates = [f for f in files if f['is_duplicate_pattern']]

        # Lógica de decisão
        if documented:
            # Se há arquivos documentados, mantê-los
            analysis['keep'] = documented
            analysis['recommendation'] = "Manter arquivos documentados"

            # Duplicados não documentados podem ser deletados SE tiverem mesmo hash
            for dup in duplicates:
                if not dup['documented']:
                    # Verificar se é idêntico a algum documentado
                    is_identical = False
                    for doc in documented:
                        if (dup['size'] == doc['size'] and
                            dup['hash'] and doc['hash'] and
                            dup['hash'] == doc['hash']):
                            is_identical = True
                            break

                    if is_identical:
                        analysis['safe_to_delete'].append(dup)
                    else:
                        analysis['manual_review'].append(dup)

        elif originals and duplicates:
            # Sem documentação, manter original mais recente
            latest_original = max(originals, key=lambda x: x['modified'])
            analysis['keep'] = [latest_original]
            analysis['recommendation'] = "Manter original mais recente"

            # Duplicados idênticos podem ser deletados
            for dup in duplicates:
                if (dup['size'] == latest_original['size'] and
                    dup['hash'] and latest_original['hash'] and
                    dup['hash'] == latest_original['hash']):
                    analysis['safe_to_delete'].append(dup)
                else:
                    analysis['manual_review'].append(dup)
        else:
            # Caso complexo - revisão manual
            analysis['manual_review'] = files
            analysis['recommendation'] = "Revisão manual necessária"

        return analysis

    def quick_hash(self, file_path):
        """Hash rápido para comparação"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                # Ler apenas primeiros 64KB para performance
                chunk = f.read(65536)
                hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None

    def generate_safe_deletion_script(self, analysis):
        """Gera script seguro para deletar duplicados"""
        script_lines = [
            "#!/bin/bash",
            "# SCRIPT DE DELEÇÃO SEGURA DE DUPLICADOS",
            "# Gerado automaticamente usando documentação como referência",
            "# IMPORTANTE: Move para lixeira, não deleta permanentemente",
            "",
            "echo '🗑️ Movendo duplicados seguros para lixeira...'",
            ""
        ]

        total_safe_deletes = 0

        for base_name, group_analysis in analysis.items():
            if group_analysis['safe_to_delete']:
                script_lines.append(f"# Grupo: {base_name}")
                script_lines.append(f"# Recomendação: {group_analysis['recommendation']}")

                for file_info in group_analysis['safe_to_delete']:
                    script_lines.append(f'echo "Movendo: {file_info["filename"]}"')
                    script_lines.append(f'mv "{file_info["path"]}" ~/.Trash/')
                    total_safe_deletes += 1

                script_lines.append("")

        script_lines.append(f"echo '✅ {total_safe_deletes} duplicados movidos para lixeira'")
        script_lines.append("echo '♻️ Verifique ~/.Trash antes de esvaziar'")

        return "\n".join(script_lines), total_safe_deletes

def main():
    base_path = "/Users/clubproducoes/Digimundo"

    dedup = IntelligentDeduplicator(base_path)

    # Carregar conhecimento da documentação
    dedup.load_documentation_knowledge()

    # Analisar duplicados (você pode especificar pasta específica)
    print("\n📂 Onde quer analisar duplicados?")
    print("1. Todo o Digimundo")
    print("2. Apenas RECOVERED_CODE")
    print("3. Caminho específico")

    # Por enquanto, vamos analisar RECOVERED_CODE
    scan_path = f"{base_path}/RECOVERED_CODE"

    if os.path.exists(scan_path):
        analysis = dedup.find_duplicates_intelligently(scan_path)

        if analysis:
            print(f"\n📊 ANÁLISE DE DUPLICADOS:")
            print(f"Encontrados {len(analysis)} grupos com possíveis duplicados")

            # Gerar script de deleção segura
            script, count = dedup.generate_safe_deletion_script(analysis)

            script_path = f"{base_path}/SAFE_DEDUP_SCRIPT.sh"
            with open(script_path, 'w') as f:
                f.write(script)

            os.chmod(script_path, 0o755)

            print(f"\n✅ Script gerado: {script_path}")
            print(f"📊 {count} arquivos seguros para deleção identificados")
            print("\n🔍 Para revisar antes de executar:")
            print(f"cat {script_path}")
            print("\n▶️ Para executar:")
            print(f"{script_path}")

        else:
            print("✅ Nenhum duplicado encontrado!")
    else:
        print(f"❌ Pasta não encontrada: {scan_path}")

if __name__ == "__main__":
    main()