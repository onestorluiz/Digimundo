#!/usr/bin/env python3
"""
Redundancy Analyzer - Versão Minimalista
Identifica duplicações com precisão e simplicidade
"""

import os
from pathlib import Path
from collections import Counter

class RedundancyScanner:
    """Escaneia arquivos por padrões de redundância"""

    def scan(self, directory: Path) -> dict:
        """Escaneia diretório por redundâncias"""
        patterns = {
            'versions': [],      # _v1, _v2, _improved
            'duplicates': [],    # nomes muito similares
            'keywords': Counter()  # palavras-chave repetitivas
        }

        files = list(directory.glob('*.py'))

        # Detecta versionamento manual
        for file in files:
            name = file.stem
            if any(suffix in name for suffix in ['_v', '_improved', '_better', '_final']):
                patterns['versions'].append(name)

        # Detecta palavras-chave excessivas
        keywords = ['quantum', 'supreme', 'ultra', 'mega', 'blockchain', 'telepathic']
        for file in files:
            name = file.stem.lower()
            for keyword in keywords:
                if keyword in name:
                    patterns['keywords'][keyword] += 1

        # Detecta nomes similares
        names = [f.stem for f in files]
        for i, name1 in enumerate(names):
            for name2 in names[i+1:]:
                similarity = self._calculate_similarity(name1, name2)
                if similarity > 0.8:  # 80% similar
                    patterns['duplicates'].append((name1, name2, similarity))

        return patterns

    def _calculate_similarity(self, s1: str, s2: str) -> float:
        """Calcula similaridade entre duas strings"""
        # Remove underscores e lowercase
        s1 = s1.replace('_', '').lower()
        s2 = s2.replace('_', '').lower()

        # Similaridade simples baseada em caracteres comuns
        if not s1 or not s2:
            return 0.0

        common = sum(1 for c in s1 if c in s2)
        return common / max(len(s1), len(s2))

class RedundancyReporter:
    """Gera relatório de redundâncias"""

    def generate(self, patterns: dict) -> str:
        """Gera relatório simples e claro"""
        lines = []
        lines.append("📊 RELATÓRIO DE REDUNDÂNCIAS")
        lines.append("=" * 50)

        # Versões manuais
        if patterns['versions']:
            lines.append(f"\n❌ VERSIONAMENTO MANUAL ({len(patterns['versions'])} arquivos)")
            for file in patterns['versions'][:5]:
                lines.append(f"  • {file}")

        # Keywords excessivas
        if patterns['keywords']:
            lines.append(f"\n⚠️ PALAVRAS-CHAVE EXCESSIVAS")
            for keyword, count in patterns['keywords'].most_common(3):
                lines.append(f"  • '{keyword}': {count} arquivos")

        # Duplicatas
        if patterns['duplicates']:
            lines.append(f"\n🔄 POSSÍVEIS DUPLICATAS ({len(patterns['duplicates'])} pares)")
            for name1, name2, sim in patterns['duplicates'][:3]:
                lines.append(f"  • {name1} ↔ {name2} ({sim*100:.0f}%)")

        # Recomendações
        lines.append("\n💡 RECOMENDAÇÕES")
        total_issues = len(patterns['versions']) + len(patterns['duplicates'])
        if total_issues > 0:
            lines.append(f"  • Remover {total_issues} redundâncias")
            lines.append(f"  • Usar Git para versionamento")
            lines.append(f"  • Simplificar nomenclatura")

        return "\n".join(lines)

def main():
    """Executa análise de redundâncias"""
    print("🔍 REDUNDANCY ANALYZER MINIMALISTA")
    print("="*50)

    scanner = RedundancyScanner()
    reporter = RedundancyReporter()

    # Escaneia diretório atual
    directory = Path('.')
    print(f"📂 Escaneando: {directory.absolute()}\n")

    patterns = scanner.scan(directory)
    report = reporter.generate(patterns)

    print(report)

    # Estatísticas finais
    total_files = len(list(directory.glob('*.py')))
    redundant = len(patterns['versions']) + len(patterns['duplicates'])
    percentage = (redundant / total_files * 100) if total_files > 0 else 0

    print(f"\n📈 ESTATÍSTICAS FINAIS")
    print(f"  • Total de arquivos: {total_files}")
    print(f"  • Arquivos redundantes: {redundant}")
    print(f"  • Taxa de redundância: {percentage:.1f}%")

    print("\n✨ Sistema minimalista: ~120 linhas vs original 300+")

if __name__ == "__main__":
    main()
    print("\nDIGIMUNDO PRESENTE")