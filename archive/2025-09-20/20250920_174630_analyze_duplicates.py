#!/usr/bin/env python3
"""
🔍 Análise de Duplicatas na Biblioteca Digital
Identifica arquivos duplicados por conteúdo e tamanho
"""

import os
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import json

class DuplicateAnalyzer:
    """Analisador de duplicatas para a biblioteca digital"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.files_by_hash = defaultdict(list)
        self.files_by_size = defaultdict(list)
        self.file_info = {}

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calcula hash MD5 do conteúdo do arquivo"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"❌ Erro calculando hash de {file_path}: {e}")
            return ""

    def _load_text_safely(self, file_path: Path) -> str:
        """Carrega texto com múltiplos encodings"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    return f.read()
            except Exception:
                continue
        return ""

    def _analyze_content_similarity(self, file1: Path, file2: Path) -> float:
        """Compara similaridade de conteúdo entre dois arquivos"""
        content1 = self._load_text_safely(file1)
        content2 = self._load_text_safely(file2)

        if not content1 or not content2:
            return 0.0

        # Normalizar conteúdo para comparação
        content1_norm = ' '.join(content1.split()).lower()
        content2_norm = ' '.join(content2.split()).lower()

        # Calcular similaridade simples
        if content1_norm == content2_norm:
            return 1.0

        # Verificar se um é substring do outro (pode indicar versão truncada)
        min_len = min(len(content1_norm), len(content2_norm))
        if min_len > 0:
            shorter = content1_norm if len(content1_norm) < len(content2_norm) else content2_norm
            longer = content2_norm if len(content1_norm) < len(content2_norm) else content1_norm

            if shorter in longer:
                return len(shorter) / len(longer)

        return 0.0

    def analyze_library(self) -> Dict:
        """Analisa toda a biblioteca para encontrar duplicatas"""
        print("🔍 Analisando biblioteca digital para duplicatas...")
        print("="*60)

        # Encontrar todos os arquivos .txt
        txt_files = list(self.data_dir.rglob("*.txt"))
        print(f"📁 Encontrados {len(txt_files)} arquivos .txt")

        # Analisar cada arquivo
        for file_path in txt_files:
            try:
                size = file_path.stat().st_size
                file_hash = self._calculate_file_hash(file_path)

                if file_hash:
                    self.files_by_hash[file_hash].append(file_path)
                    self.files_by_size[size].append(file_path)

                    self.file_info[str(file_path)] = {
                        'size': size,
                        'hash': file_hash,
                        'name': file_path.name
                    }

            except Exception as e:
                print(f"❌ Erro analisando {file_path}: {e}")

        # Encontrar duplicatas exatas
        exact_duplicates = {
            hash_val: files for hash_val, files in self.files_by_hash.items()
            if len(files) > 1
        }

        # Encontrar arquivos com mesmo tamanho
        same_size_groups = {
            size: files for size, files in self.files_by_size.items()
            if len(files) > 1
        }

        # Analisar similaridade entre arquivos de mesmo tamanho
        potential_duplicates = []
        for size, files in same_size_groups.items():
            if len(files) > 1:
                for i, file1 in enumerate(files):
                    for file2 in files[i+1:]:
                        # Verificar se já são duplicatas exatas
                        hash1 = self.file_info[str(file1)]['hash']
                        hash2 = self.file_info[str(file2)]['hash']

                        if hash1 != hash2:  # Não são duplicatas exatas
                            similarity = self._analyze_content_similarity(file1, file2)
                            if similarity > 0.95:  # 95% similar
                                potential_duplicates.append({
                                    'file1': str(file1),
                                    'file2': str(file2),
                                    'similarity': similarity,
                                    'size1': file1.stat().st_size,
                                    'size2': file2.stat().st_size
                                })

        # Identificar padrões de nomes
        name_patterns = self._analyze_name_patterns(txt_files)

        return {
            'total_files': len(txt_files),
            'exact_duplicates': {
                hash_val: [str(f) for f in files]
                for hash_val, files in exact_duplicates.items()
            },
            'potential_duplicates': potential_duplicates,
            'same_size_groups': {
                str(size): [str(f) for f in files]
                for size, files in same_size_groups.items()
            },
            'name_patterns': name_patterns,
            'file_info': self.file_info
        }

    def _analyze_name_patterns(self, files: List[Path]) -> Dict:
        """Analisa padrões nos nomes dos arquivos"""
        patterns = {
            'drafts_vs_screenplays': [],
            'different_versions': [],
            'similar_names': []
        }

        file_names = [f.stem for f in files]

        for i, name1 in enumerate(file_names):
            for j, name2 in enumerate(file_names[i+1:], i+1):
                # Verificar Draft vs Screenplay
                if (('Draft' in name1 and 'Screenplay' in name2) or
                    ('Screenplay' in name1 and 'Draft' in name2)):
                    base1 = name1.replace('-_Draft', '').replace('-_Screenplay', '')
                    base2 = name2.replace('-_Draft', '').replace('-_Screenplay', '')
                    if base1.split('_')[0] == base2.split('_')[0]:  # Mesmo filme
                        patterns['drafts_vs_screenplays'].append({
                            'file1': files[i].name,
                            'file2': files[j].name,
                            'base_name': base1.split('_')[0]
                        })

                # Verificar versões diferentes do mesmo arquivo
                if abs(len(name1) - len(name2)) < 10:  # Nomes similares em tamanho
                    # Comparar primeiras palavras
                    words1 = name1.split('_')[:3]
                    words2 = name2.split('_')[:3]

                    common_words = set(words1) & set(words2)
                    if len(common_words) >= 2:
                        patterns['similar_names'].append({
                            'file1': files[i].name,
                            'file2': files[j].name,
                            'common_words': list(common_words)
                        })

        return patterns

    def generate_report(self, analysis: Dict) -> str:
        """Gera relatório detalhado da análise"""
        report = []
        report.append("🔍 RELATÓRIO DE ANÁLISE DE DUPLICATAS")
        report.append("="*60)
        report.append(f"📊 Total de arquivos analisados: {analysis['total_files']}")
        report.append("")

        # Duplicatas exatas
        if analysis['exact_duplicates']:
            report.append("🎯 DUPLICATAS EXATAS (mesmo hash):")
            for hash_val, files in analysis['exact_duplicates'].items():
                report.append(f"  Hash {hash_val[:8]}...:")
                for file in files:
                    report.append(f"    - {Path(file).name}")
                report.append("")
        else:
            report.append("✅ Nenhuma duplicata exata encontrada")
            report.append("")

        # Duplicatas potenciais
        if analysis['potential_duplicates']:
            report.append("⚠️  DUPLICATAS POTENCIAIS (>95% similaridade):")
            for dup in analysis['potential_duplicates']:
                report.append(f"  Similaridade: {dup['similarity']:.1%}")
                report.append(f"    - {Path(dup['file1']).name} ({dup['size1']:,} bytes)")
                report.append(f"    - {Path(dup['file2']).name} ({dup['size2']:,} bytes)")
                report.append("")
        else:
            report.append("✅ Nenhuma duplicata potencial encontrada")
            report.append("")

        # Padrões de nomes
        patterns = analysis['name_patterns']

        if patterns['drafts_vs_screenplays']:
            report.append("📝 DRAFTS vs SCREENPLAYS (versões diferentes):")
            for pair in patterns['drafts_vs_screenplays']:
                report.append(f"  {pair['base_name']}:")
                report.append(f"    - {pair['file1']}")
                report.append(f"    - {pair['file2']}")
            report.append("")

        if patterns['similar_names']:
            report.append("🔤 NOMES SIMILARES (possíveis versões):")
            shown = set()
            for pair in patterns['similar_names'][:10]:  # Limitar a 10
                key = tuple(sorted([pair['file1'], pair['file2']]))
                if key not in shown:
                    shown.add(key)
                    report.append(f"  Palavras comuns: {', '.join(pair['common_words'])}")
                    report.append(f"    - {pair['file1']}")
                    report.append(f"    - {pair['file2']}")
            report.append("")

        # Arquivos únicos recomendados
        report.append("📋 RESUMO PARA TRADUÇÃO:")

        unique_files = set()
        # Adicionar todos os arquivos
        for file_path, info in analysis['file_info'].items():
            unique_files.add(file_path)

        # Remover duplicatas exatas (manter apenas o primeiro)
        for hash_val, files in analysis['exact_duplicates'].items():
            if len(files) > 1:
                # Manter o menor arquivo (provavelmente mais limpo)
                files_sorted = sorted(files, key=lambda x: analysis['file_info'][x]['size'])
                for file in files_sorted[1:]:  # Remover todos exceto o menor
                    unique_files.discard(file)

        report.append(f"  📁 Arquivos únicos recomendados: {len(unique_files)}")
        report.append(f"  🗑️ Duplicatas exatas removidas: {analysis['total_files'] - len(unique_files)}")

        # Mostrar estatísticas de tamanho
        sizes = [analysis['file_info'][f]['size'] for f in unique_files]
        if sizes:
            report.append(f"  📏 Tamanho médio: {sum(sizes) // len(sizes):,} bytes")
            report.append(f"  📏 Maior arquivo: {max(sizes):,} bytes")
            report.append(f"  📏 Menor arquivo: {min(sizes):,} bytes")

        report.append("")
        report.append("✅ CONCLUSÃO:")
        if len(unique_files) == analysis['total_files']:
            report.append("  Todos os arquivos são únicos - nenhuma duplicata encontrada!")
        else:
            report.append(f"  Recomenda-se traduzir apenas {len(unique_files)} arquivos únicos")
            report.append(f"  {analysis['total_files'] - len(unique_files)} duplicatas podem ser ignoradas")

        return "\n".join(report)


def main():
    """Função principal"""
    analyzer = DuplicateAnalyzer()
    analysis = analyzer.analyze_library()

    # Gerar relatório
    report = analyzer.generate_report(analysis)
    print(report)

    # Salvar relatório
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    report_path = output_dir / "duplicate_analysis_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    # Salvar dados JSON
    json_path = output_dir / "duplicate_analysis_data.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print(f"\n📄 Relatório salvo em: {report_path}")
    print(f"📊 Dados salvos em: {json_path}")

    return analysis


if __name__ == "__main__":
    main()