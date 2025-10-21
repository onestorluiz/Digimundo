#!/usr/bin/env python3
"""
📚 SCREENPLAY LIBRARY SIMPLES - VERSÃO CORRIGIDA
"""

from pathlib import Path
from typing import Dict, List, Optional

class ScreenplayLibrarySimple:
    """Biblioteca simplificada que funciona 100%"""

    def __init__(self):
        # Caminho absoluto
        self.library_path = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS")
        self._cache = {}
        self._file_map = {}
        self._build_file_map()

    def _build_file_map(self):
        """Constrói mapa de todos os arquivos"""
        if not self.library_path.exists():
            print(f"⚠️ Pasta não encontrada: {self.library_path}")
            return

        # Mapear todos os arquivos .txt
        for txt_file in self.library_path.rglob("*.txt"):
            # Nome sem extensão
            name = txt_file.stem
            # Guardar caminho completo
            self._file_map[name] = txt_file

            # Também adicionar variações
            self._file_map[name.lower()] = txt_file
            self._file_map[name.replace("_", " ")] = txt_file
            self._file_map[name.replace("-", " ")] = txt_file

        print(f"📚 {len(self._file_map)} mapeamentos criados")

    def list_screenplays(self) -> List[str]:
        """Lista todos os roteiros disponíveis"""
        titles = []
        seen = set()

        for txt_file in self.library_path.rglob("*.txt"):
            title = txt_file.stem
            if title not in seen:
                titles.append(title)
                seen.add(title)

        return sorted(titles)

    def get_screenplay(self, title: str) -> Optional[str]:
        """
        Busca e retorna conteúdo de um roteiro

        Args:
            title: Título do roteiro

        Returns:
            Conteúdo do arquivo ou None
        """
        # Cache
        if title in self._cache:
            return self._cache[title]

        # Buscar no mapa
        file_path = None

        # Tentar título exato
        if title in self._file_map:
            file_path = self._file_map[title]
        # Tentar lowercase
        elif title.lower() in self._file_map:
            file_path = self._file_map[title.lower()]
        # Tentar busca parcial
        else:
            title_lower = title.lower()
            for key, path in self._file_map.items():
                if title_lower in key.lower():
                    file_path = path
                    break

        # Se encontrou, ler
        if file_path and file_path.exists():
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            self._cache[title] = content
            return content

        # Última tentativa: caminho direto
        if title.startswith('/'):
            path = Path(title)
            if path.exists() and path.is_file():
                content = path.read_text(encoding='utf-8', errors='ignore')
                self._cache[title] = content
                return content

        return None

    def get_stats(self) -> Dict:
        """Retorna estatísticas da biblioteca"""
        stats = {
            'total_files': 0,
            'by_category': {},
            'total_size_mb': 0
        }

        for category_dir in self.library_path.iterdir():
            if category_dir.is_dir():
                files = list(category_dir.glob("*.txt"))
                stats['by_category'][category_dir.name] = len(files)
                stats['total_files'] += len(files)

                for f in files:
                    stats['total_size_mb'] += f.stat().st_size / (1024*1024)

        return stats