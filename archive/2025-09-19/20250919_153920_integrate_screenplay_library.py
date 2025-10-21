#!/usr/bin/env python3
"""
🎬 INTEGRAÇÃO DA BIBLIOTECA DE ROTEIROS
Integra 48 roteiros ao sistema unificado de memória e learning
"""

import sys
import json
import hashlib
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unified_memory_system import get_unified_memory, MemoryType
from src.learning.ollama_cinema_trainer import OllamaCinemaTrainer

class ScreenplayLibraryIntegrator:
    """Integra biblioteca de roteiros ao sistema"""

    def __init__(self):
        self.library_path = Path("digilibrary/BIBLIOTECA_ROTEIROS")
        self.memory = get_unified_memory()
        self.trainer = OllamaCinemaTrainer()

        # Categorias de roteiros
        self.categories = {
            'meus_filmes': 'personal_screenplays',
            'roteiros_mestres': 'masterpiece_screenplays',
            'teoria': 'screenplay_theory'
        }

        self.stats = {
            'total_files': 0,
            'processed': 0,
            'knowledge_extracted': 0,
            'errors': 0
        }

    def discover_screenplays(self) -> Dict[str, List[Path]]:
        """Descobre e categoriza todos os roteiros"""
        screenplays = {}

        for category_dir in self.library_path.iterdir():
            if category_dir.is_dir():
                category = category_dir.name
                txt_files = list(category_dir.glob("*.txt"))
                if txt_files:
                    screenplays[category] = txt_files
                    self.stats['total_files'] += len(txt_files)

        return screenplays

    def index_screenplay(self, file_path: Path, category: str) -> str:
        """Indexa roteiro no sistema de memória unificado"""
        try:
            # Ler conteúdo
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            # Criar ID único
            file_id = hashlib.md5(f"{file_path.name}{category}".encode()).hexdigest()[:16]

            # Metadados do arquivo
            metadata = {
                'filename': file_path.name,
                'category': category,
                'category_type': self.categories.get(category, 'unknown'),
                'path': str(file_path),
                'size_kb': len(content) / 1024,
                'indexed_at': datetime.now().isoformat()
            }

            # Extrair informações básicas
            lines = content.split('\n')

            # Tentar identificar título e autor
            title = file_path.stem.replace('_', ' ').replace('-', ' ').title()

            # Primeiras 500 linhas para análise rápida
            preview = '\n'.join(lines[:500])

            # Armazenar no sistema unificado
            entry_id = self.memory.store(
                memory_type=MemoryType.SCREENPLAY,
                key=f"screenplay:{file_id}",
                value={
                    'title': title,
                    'content_preview': preview[:5000],  # Primeiros 5K chars
                    'total_lines': len(lines),
                    'total_chars': len(content)
                },
                metadata=metadata,
                confidence=1.0,
                source='screenplay_library'
            )

            # Armazenar caminho completo para acesso rápido
            self.memory.store(
                memory_type=MemoryType.SCREENPLAY,
                key=f"screenplay_path:{title.lower().replace(' ', '_')}",
                value=str(file_path),
                metadata={'category': category},
                confidence=1.0,
                source='screenplay_library'
            )

            print(f"  ✅ Indexado: {file_path.name}")
            return entry_id

        except Exception as e:
            print(f"  ❌ Erro ao indexar {file_path.name}: {e}")
            self.stats['errors'] += 1
            return None

    async def extract_knowledge(self, file_path: Path, category: str):
        """Extrai conhecimento cinematográfico usando OllamaCinemaTrainer"""
        try:
            print(f"  🧠 Extraindo conhecimento de: {file_path.name}")

            # Usar o trainer para extrair conhecimento
            knowledge = await self.trainer.train_on_document(file_path)

            if knowledge:
                self.stats['knowledge_extracted'] += len(knowledge)
                print(f"    → {len(knowledge)} conceitos extraídos")

                # Armazenar relação entre arquivo e conhecimento
                for k in knowledge:
                    self.memory.store(
                        memory_type=MemoryType.KNOWLEDGE,
                        key=f"knowledge:{file_path.stem}:{k.concept[:50]}",
                        value={
                            'concept': k.concept,
                            'source_file': file_path.name,
                            'category': category,
                            'examples': k.examples
                        },
                        confidence=k.confidence,
                        source=f"ml_extraction:{category}"
                    )

        except Exception as e:
            print(f"  ⚠️ Erro no ML: {e}")

    def create_search_index(self):
        """Cria índice de busca para acesso rápido pelos Ollamas"""
        print("\n📑 Criando índice de busca...")

        # Criar índice por categoria
        for category in self.categories.keys():
            entries = self.memory.retrieve(
                memory_type=MemoryType.SCREENPLAY,
                min_confidence=0.5
            )

            category_entries = [
                e for e in entries
                if e.metadata.get('category') == category
            ]

            if category_entries:
                # Criar índice consolidado
                index = {
                    'category': category,
                    'count': len(category_entries),
                    'files': [e.metadata.get('filename') for e in category_entries],
                    'created_at': datetime.now().isoformat()
                }

                self.memory.store(
                    memory_type=MemoryType.SCREENPLAY,
                    key=f"index:{category}",
                    value=index,
                    confidence=1.0,
                    source='screenplay_indexer'
                )

                print(f"  ✅ Índice '{category}': {len(category_entries)} arquivos")

    async def process_all(self, enable_ml: bool = True):
        """Processa toda a biblioteca"""
        print("🎬 INICIANDO INTEGRAÇÃO DA BIBLIOTECA")
        print("=" * 60)

        # Descobrir arquivos
        screenplays = self.discover_screenplays()
        print(f"\n📚 Encontrados {self.stats['total_files']} roteiros em {len(screenplays)} categorias")

        for category, files in screenplays.items():
            print(f"\n📂 {category} ({len(files)} arquivos):")

            for file_path in files:
                # 1. Indexar arquivo
                entry_id = self.index_screenplay(file_path, category)
                if entry_id:
                    self.stats['processed'] += 1

                    # 2. Extrair conhecimento (se ML habilitado)
                    if enable_ml and category != 'meus_filmes':  # Não processar pessoais por privacidade
                        await self.extract_knowledge(file_path, category)

        # 3. Criar índices de busca
        self.create_search_index()

        # 4. Evoluir modelos se tiver conhecimento suficiente
        if self.stats['knowledge_extracted'] > 50:
            print("\n🧬 Evoluindo modelos com conhecimento acumulado...")
            await self.trainer.evolve_model("scripturemon-cpu-themes")

        print("\n" + "=" * 60)
        print("📊 RESUMO DA INTEGRAÇÃO:")
        print(f"  Total de arquivos: {self.stats['total_files']}")
        print(f"  Processados: {self.stats['processed']}")
        print(f"  Conhecimento extraído: {self.stats['knowledge_extracted']} conceitos")
        print(f"  Erros: {self.stats['errors']}")

        # Estatísticas da memória
        mem_stats = self.memory.get_stats()
        print(f"\n💾 MEMÓRIA UNIFICADA:")
        print(f"  Total entradas: {mem_stats['total_entries']}")
        print(f"  Tamanho DB: {mem_stats['db_size_kb']:.1f} KB")

        return self.stats

# Funções de acesso para os Ollamas
def search_screenplays(query: str, category: str = None) -> List[Dict]:
    """Busca roteiros na biblioteca"""
    memory = get_unified_memory()

    # Buscar por query
    results = memory.search(
        query=query,
        memory_types=[MemoryType.SCREENPLAY],
        limit=10
    )

    # Filtrar por categoria se especificada
    if category:
        results = [
            r for r in results
            if r.metadata.get('category') == category
        ]

    return [
        {
            'title': r.value.get('title', 'Unknown'),
            'category': r.metadata.get('category'),
            'path': r.metadata.get('path'),
            'preview': r.value.get('content_preview', '')[:500]
        }
        for r in results
    ]

def get_screenplay_content(title_or_path: str) -> str:
    """Obtém conteúdo completo de um roteiro"""
    memory = get_unified_memory()

    # Buscar por título
    key = f"screenplay_path:{title_or_path.lower().replace(' ', '_')}"
    entries = memory.retrieve(memory_type=MemoryType.SCREENPLAY, key=key)

    if entries:
        path = entries[0].value
        return Path(path).read_text(encoding='utf-8', errors='ignore')

    # Tentar como path direto
    if Path(title_or_path).exists():
        return Path(title_or_path).read_text(encoding='utf-8', errors='ignore')

    return None

def list_categories() -> Dict[str, int]:
    """Lista categorias disponíveis"""
    memory = get_unified_memory()

    categories = {}
    for cat in ['meus_filmes', 'roteiros_mestres', 'teoria']:
        entries = memory.retrieve(
            memory_type=MemoryType.SCREENPLAY,
            key=f"index:{cat}"
        )
        if entries:
            categories[cat] = entries[0].value.get('count', 0)

    return categories

async def main():
    """Executa integração completa"""
    integrator = ScreenplayLibraryIntegrator()

    print("🎯 OPÇÕES DE INTEGRAÇÃO:")
    print("1. Indexação rápida (sem ML)")
    print("2. Indexação + Machine Learning")
    print("3. Apenas atualizar índices")

    choice = input("\nEscolha (1-3): ").strip()

    if choice == '1':
        await integrator.process_all(enable_ml=False)
    elif choice == '2':
        await integrator.process_all(enable_ml=True)
    elif choice == '3':
        integrator.create_search_index()
    else:
        print("Opção inválida")

    print("\n✅ Biblioteca integrada e acessível aos Ollamas!")
    print("\n📚 FUNÇÕES DISPONÍVEIS PARA OS OLLAMAS:")
    print("  - search_screenplays(query, category)")
    print("  - get_screenplay_content(title)")
    print("  - list_categories()")

if __name__ == "__main__":
    asyncio.run(main())