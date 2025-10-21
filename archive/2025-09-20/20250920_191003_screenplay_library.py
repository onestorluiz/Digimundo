#!/usr/bin/env python3
"""
📚 SCREENPLAY LIBRARY - Interface de acesso aos roteiros para Ollamas
Permite que todos os modelos acessem a biblioteca de roteiros
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib

from .unified_memory_system import get_unified_memory, MemoryType

class ScreenplayLibrary:
    """Biblioteca de roteiros acessível aos Ollamas"""

    def __init__(self):
        # Caminho absoluto para evitar problemas
        self.library_path = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS")
        self.memory = get_unified_memory()
        self._cache = {}
        self._screenplays_list = None  # Cache da lista de roteiros
        self._file_paths = {}  # Mapear título -> caminho completo

    def get_screenplay_text(self, title: str) -> Optional[str]:
        """
        Retorna o texto completo de um roteiro (retrocompatibilidade)

        Args:
            title: Título do roteiro

        Returns:
            Texto do roteiro ou None se não encontrado
        """
        return self.get_screenplay(title)

    def get_screenplay(self, title: str) -> Optional[str]:
        """
        Retorna o texto completo de um roteiro
        BUSCA AUTOMATICAMENTE EM TODAS AS SUBPASTAS!

        Args:
            title: Título do roteiro (pode ser o título exato da lista)

        Returns:
            Texto do roteiro ou None se não encontrado
        """
        # Garantir que a lista está atualizada
        if self._screenplays_list is None:
            self.list_screenplays()

        # Primeiro, tentar buscar pelo título exato no mapeamento
        if title in self._file_paths:
            file_path = self._file_paths[title]
            if file_path.exists():
                if file_path.suffix == '.txt':
                    return file_path.read_text(encoding='utf-8', errors='ignore')
                elif file_path.suffix == '.pdf':
                    # Por enquanto, retornar mensagem para PDFs
                    return f"[PDF file: {file_path.name}] - PDF reading not yet implemented"

        # Se não encontrou, buscar por similaridade (retrocompatibilidade)
        title_lower = title.lower()

        # Buscar recursivamente em toda a biblioteca usando o nome exato com espaços
        for file_path in self.library_path.rglob("*.txt"):
            # Comparar com o nome do arquivo sem extensão
            if file_path.stem == title or file_path.stem.lower() == title_lower:
                return file_path.read_text(encoding='utf-8', errors='ignore')
            # Também tentar match parcial
            if title_lower in file_path.stem.lower():
                return file_path.read_text(encoding='utf-8', errors='ignore')

        # Buscar no mapeamento por título parcial
        for mapped_title, file_path in self._file_paths.items():
            if title_lower in mapped_title.lower():
                if file_path.suffix == '.txt':
                    return file_path.read_text(encoding='utf-8', errors='ignore')

        # Por fim, tentar como path direto
        if '/' in title or title.endswith('.txt'):
            path = Path(title) if title.startswith('/') else self.library_path / title
            if path.exists() and path.is_file():
                return path.read_text(encoding='utf-8', errors='ignore')

        return None

    def search(self, query: str, category: Optional[str] = None, limit: int = 5) -> List[Dict]:
        """
        Busca roteiros por query

        Args:
            query: Texto de busca
            category: 'meus_filmes', 'roteiros_mestres', ou 'teoria'
            limit: Número máximo de resultados

        Returns:
            Lista de roteiros encontrados
        """
        # Cache key
        cache_key = f"{query}:{category}:{limit}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Buscar na memória unificada
        results = self.memory.search(
            query=query,
            memory_types=[MemoryType.SCREENPLAY],
            limit=limit * 2  # Pegar mais para filtrar
        )

        # Filtrar por categoria
        if category:
            results = [
                r for r in results
                if r.metadata.get('category') == category
            ]

        # Formatar resultados
        formatted = []
        for r in results[:limit]:
            # Verificar tipo do value
            if isinstance(r.value, dict):
                title = r.value.get('title', 'Unknown')
                preview = r.value.get('content_preview', '')[:500]
            elif isinstance(r.value, str):
                title = r.metadata.get('filename', 'Unknown')
                preview = r.value[:500] if r.value else ''
            else:
                title = 'Unknown'
                preview = ''

            formatted.append({
                'title': title,
                'category': r.metadata.get('category', 'unknown'),
                'path': r.metadata.get('path', ''),
                'size_kb': r.metadata.get('size_kb', 0),
                'preview': preview
            })

        # Cache
        self._cache[cache_key] = formatted
        return formatted

    def get_screenplay(self, identifier: str) -> Optional[str]:
        """
        Obtém conteúdo completo de um roteiro

        Args:
            identifier: Título ou caminho do roteiro

        Returns:
            Conteúdo completo do roteiro ou None
        """
        # Validar entrada
        if not identifier or identifier in ['.', '..', ''] or identifier.startswith('.'):
            return None
        # Tentar por título primeiro
        title_key = f"screenplay_path:{identifier.lower().replace(' ', '_')}"
        entries = self.memory.retrieve(
            memory_type=MemoryType.SCREENPLAY,
            key=title_key
        )

        if entries:
            path = Path(entries[0].value)
            if path.exists() and path.is_file():
                return path.read_text(encoding='utf-8', errors='ignore')

        # Tentar como path direto
        if '/' in identifier:
            path = Path(identifier)
            if path.exists() and path.is_file() and str(self.library_path) in str(path):
                return path.read_text(encoding='utf-8', errors='ignore')

        # Buscar por nome parcial
        results = self.search(identifier, limit=1)
        if results:
            path = Path(results[0]['path'])
            if path.exists() and path.is_file():
                return path.read_text(encoding='utf-8', errors='ignore')

        return None

    def list_all(self) -> Dict[str, List[str]]:
        """
        Lista todos os roteiros por categoria

        Returns:
            Dicionário com categorias e seus roteiros
        """
        categories = {}

        for category_dir in self.library_path.iterdir():
            if category_dir.is_dir():
                txt_files = list(category_dir.glob("*.txt"))
                if txt_files:
                    categories[category_dir.name] = [
                        f.stem.replace('_', ' ').replace('-', ' ').title()
                        for f in txt_files
                    ]

        return categories

    def get_category_stats(self) -> Dict[str, Dict]:
        """
        Estatísticas por categoria

        Returns:
            Estatísticas detalhadas de cada categoria
        """
        stats = {}

        for category in ['meus_filmes', 'roteiros_mestres', 'teoria']:
            entries = self.memory.retrieve(
                memory_type=MemoryType.SCREENPLAY,
                key=f"index:{category}"
            )

            if entries:
                index_data = entries[0].value
                stats[category] = {
                    'count': index_data.get('count', 0),
                    'files': index_data.get('files', []),
                    'indexed_at': index_data.get('created_at', 'unknown')
                }
            else:
                # Contar diretamente
                category_path = self.library_path / category
                if category_path.exists():
                    count = len(list(category_path.glob("*.txt")))
                    stats[category] = {
                        'count': count,
                        'files': [],
                        'indexed_at': 'not indexed'
                    }

        return stats

    def get_knowledge_for_screenplay(self, title: str) -> List[Dict]:
        """
        Obtém conhecimento extraído de um roteiro específico

        Args:
            title: Título do roteiro

        Returns:
            Lista de conceitos aprendidos
        """
        # Buscar conhecimento relacionado
        entries = self.memory.retrieve(
            memory_type=MemoryType.KNOWLEDGE,
            min_confidence=0.5
        )

        # Filtrar por título
        knowledge = []
        for entry in entries:
            if isinstance(entry.value, dict):
                if entry.value.get('source_file', '').lower() in title.lower():
                    knowledge.append({
                        'concept': entry.value.get('concept', ''),
                        'examples': entry.value.get('examples', []),
                        'confidence': entry.confidence
                    })

        return knowledge

    def list_screenplays(self, category: Optional[str] = None, force_refresh: bool = False) -> List[str]:
        """
        Lista todos os roteiros disponíveis
        AGORA DETECTA AUTOMATICAMENTE TODOS OS ARQUIVOS EM BIBLIOTECA_ROTEIROS!

        Args:
            category: Filtrar por categoria (opcional)
            force_refresh: Forçar atualização da lista (detecta novos arquivos)

        Returns:
            Lista de títulos de roteiros
        """
        if self._screenplays_list is None or force_refresh:
            # Buscar TODOS os arquivos .txt e .pdf recursivamente
            self._screenplays_list = []
            self._file_paths = {}  # Mapear título -> caminho completo

            if self.library_path.exists():
                # Buscar recursivamente em TODAS as subpastas
                for file_path in self.library_path.rglob("*.txt"):
                    # Adicionar com caminho relativo para identificar categoria
                    relative_path = file_path.relative_to(self.library_path)
                    category_name = relative_path.parts[0] if len(relative_path.parts) > 1 else "root"

                    # Adicionar título único
                    title = file_path.stem
                    # Se já existe, adicionar categoria para diferenciar
                    if title in self._screenplays_list:
                        title = f"{title} ({category_name})"

                    self._screenplays_list.append(title)
                    self._file_paths[title] = file_path

                # Também buscar PDFs se existirem
                for file_path in self.library_path.rglob("*.pdf"):
                    relative_path = file_path.relative_to(self.library_path)
                    category_name = relative_path.parts[0] if len(relative_path.parts) > 1 else "root"

                    title = f"{file_path.stem} (PDF)"
                    if title in self._screenplays_list:
                        title = f"{file_path.stem} ({category_name}, PDF)"

                    self._screenplays_list.append(title)
                    self._file_paths[title] = file_path

        if category:
            # Filtrar por categoria no caminho
            filtered = []
            for title in self._screenplays_list:
                if title in self._file_paths:
                    path = self._file_paths[title]
                    if category.lower() in str(path).lower():
                        filtered.append(title)
            return filtered

        return self._screenplays_list

    def analyze_with_context(self, screenplay_title: str, analysis_type: str = 'structure') -> str:
        """
        Analisa roteiro com contexto de outros roteiros similares

        Args:
            screenplay_title: Título do roteiro a analisar
            analysis_type: 'structure', 'character', 'theme', 'dialogue'

        Returns:
            Prompt enriquecido com contexto
        """
        # Obter roteiro
        content = self.get_screenplay(screenplay_title)
        if not content:
            return f"Screenplay '{screenplay_title}' not found"

        # Buscar roteiros similares
        similar = self.search(screenplay_title, limit=3)

        # Criar contexto
        context = f"""
ANALYZING: {screenplay_title}

SIMILAR SCREENPLAYS IN LIBRARY:
{chr(10).join([f"- {s['title']} ({s['category']})" for s in similar])}

ANALYSIS TYPE: {analysis_type}

SCREENPLAY EXCERPT (first 5000 chars):
{content[:5000]}

Please provide a {analysis_type} analysis considering the patterns found in similar masterpiece screenplays.
"""
        return context

# Singleton para acesso global
_screenplay_library = None

def get_screenplay_library() -> ScreenplayLibrary:
    """Retorna instância singleton da biblioteca"""
    global _screenplay_library
    if _screenplay_library is None:
        _screenplay_library = ScreenplayLibrary()
    return _screenplay_library

# Funções de conveniência para os Ollamas
def search_screenplays(query: str, **kwargs) -> List[Dict]:
    """Busca rápida de roteiros"""
    return get_screenplay_library().search(query, **kwargs)

def read_screenplay(title: str) -> Optional[str]:
    """Lê um roteiro completo"""
    return get_screenplay_library().get_screenplay(title)

def list_screenplays() -> Dict[str, List[str]]:
    """Lista todos os roteiros"""
    return get_screenplay_library().list_all()

def screenplay_stats() -> Dict[str, Dict]:
    """Estatísticas da biblioteca"""
    return get_screenplay_library().get_category_stats()