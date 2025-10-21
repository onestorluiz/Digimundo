#!/usr/bin/env python3
"""
🎯 Reorganizador Correto - Separa PDFs nas categorias certas
"""

import shutil
from pathlib import Path

class CorrectReorganizer:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.unified_path = self.base_path / "DIGILANG_UNIFIED_SYSTEM"
        
        print("╔" + "═"*58 + "╗")
        print("║  🎯 REORGANIZADOR CORRETO DE CATEGORIAS               ║")
        print("╚" + "═"*58 + "╝")
        
        # Listas precisas de categorização
        self.real_manuals = [
            'creating character arcs',
            'anatomy of story',
            'art of dramatic writing',
            'screenplay _ the foundations',
            'writing short films',
            'writing the tv drama',
            'writers journey',
            'heroine\'s journey',
            '21st century screenplay',
            'fundamentals of screenwriting',
            'ontology and the art',
            'story _ substance'
        ]
        
        self.classic_movies = [
            'chinatown', 'godfather', 'pulp fiction', 'casablanca',
            'citizen kane', 'matrix', 'alien', 'psycho', 'apocalypse',
            'inception', 'django', 'fight club', 'gladiator', 'forrest gump',
            'back to the future', 'star wars', 'raiders', 'shining',
            'whiplash', 'memento', 'joker', 'dark knight', 'shawshank',
            'interstellar', 'terminator', 'silence of the lambs',
            'saving private ryan', 'se7en', 'goodfellas', 'departed',
            'one flew over', 'spider-man', 'lord of the rings'
        ]
        
        self.tv_series = [
            'breaking bad', 'game of thrones', 'true detective',
            'black mirror', 'succession', 'the boys', 'house of cards',
            'mad men', 'mr. robot', 'mindhunter', 'peaky blinders',
            'this is us', 'vikings', 'barry', 'entourage', 'spartacus',
            'narcos', 'queens gambit', 'bear', 'severance'
        ]
        
        self.digimundo_docs = [
            '🌟', '🔥', '📜', '🧬', '🎯', '🌐', '💬', '📊',
            'digimundo', 'digimon', 'claudemon', 'scripturemon',
            'blueprint', 'protocolo', 'plano maestro', 'consciência',
            'memória viva', 'neurogenesis', 'simbiótic',
            'híbrido', 'vírus', 'agentes de ia'
        ]
    
    def categorize_correctly(self, filename):
        """Categoriza corretamente baseado no conteúdo real"""
        name_lower = filename.lower()
        
        # 1. Documentos do Digimundo (não são roteiros!)
        if any(term in name_lower for term in self.digimundo_docs):
            return 'digimundo_internal'
        
        # 2. Manuais de roteiro REAIS
        if any(term in name_lower for term in self.real_manuals):
            return 'real_manuals'
        
        # 3. Roteiros de cinema clássico
        if any(term in name_lower for term in self.classic_movies):
            return 'classic_movies'
        
        # 4. Roteiros de séries TV
        if any(term in name_lower for term in self.tv_series):
            return 'tv_series'
        
        # 5. Nestor Luiz
        if 'nestor' in name_lower or 'sonhos sem' in name_lower:
            return 'nestor_luiz'
        
        # 6. Pesquisas sobre IA
        if 'pesquisa' in name_lower and ('ia' in name_lower or 'chatgpt' in name_lower or 'claude' in name_lower):
            return 'ai_research'
        
        return 'uncategorized'
    
    def reorganize_all(self):
        """Reorganiza todos os PDFs corretamente"""
        print("\n🚀 REORGANIZANDO PDFS NAS CATEGORIAS CORRETAS")
        print("="*50)
        
        # Criar nova estrutura
        new_structure = {
            '01_ROTEIROS_CINEMA': ['nestor_luiz', 'classicos'],
            '02_ROTEIROS_TV': ['series'],
            '03_MANUAIS_ROTEIRO': ['teoria_pratica'],
            '04_SISTEMA_DIGIMUNDO': ['documentacao', 'pesquisas'],
            '05_UNCATEGORIZED': ['revisar']
        }
        
        # Criar diretórios
        for main_dir, subdirs in new_structure.items():
            for subdir in subdirs:
                path = self.unified_path / main_dir / subdir
                path.mkdir(parents=True, exist_ok=True)
        
        # Buscar todos os PDFs
        all_pdfs = list(self.unified_path.glob("**/*.pdf"))
        
        stats = {
            'nestor_luiz': [],
            'classic_movies': [],
            'tv_series': [],
            'real_manuals': [],
            'digimundo_internal': [],
            'ai_research': [],
            'uncategorized': []
        }
        
        print(f"\nAnalisando {len(all_pdfs)} PDFs...")
        
        for pdf in all_pdfs:
            category = self.categorize_correctly(pdf.name)
            stats[category].append(pdf.name)
            
            # Mover para local correto
            if category == 'nestor_luiz':
                dest = self.unified_path / '01_ROTEIROS_CINEMA/nestor_luiz'
            elif category == 'classic_movies':
                dest = self.unified_path / '01_ROTEIROS_CINEMA/classicos'
            elif category == 'tv_series':
                dest = self.unified_path / '02_ROTEIROS_TV/series'
            elif category == 'real_manuals':
                dest = self.unified_path / '03_MANUAIS_ROTEIRO/teoria_pratica'
            elif category in ['digimundo_internal', 'ai_research']:
                dest = self.unified_path / '04_SISTEMA_DIGIMUNDO/documentacao'
            else:
                dest = self.unified_path / '05_UNCATEGORIZED/revisar'
            
            # Mover apenas se não está no lugar certo
            if pdf.parent != dest:
                try:
                    new_path = dest / pdf.name
                    if not new_path.exists():
                        shutil.move(str(pdf), str(new_path))
                except:
                    pass
        
        # Relatório
        print("\n📊 CATEGORIZAÇÃO CORRETA:")
        print(f"   • Seus roteiros: {len(stats['nestor_luiz'])}")
        for name in stats['nestor_luiz']:
            print(f"      - {name}")
        
        print(f"\n   • Roteiros cinema clássico: {len(stats['classic_movies'])}")
        print(f"   • Roteiros séries TV: {len(stats['tv_series'])}")
        print(f"   • MANUAIS REAIS de roteiro: {len(stats['real_manuals'])}")
        
        if stats['real_manuals']:
            print("\n   📚 Manuais verdadeiros:")
            for name in stats['real_manuals'][:10]:
                print(f"      - {name[:60]}...")
        
        print(f"\n   • Documentos Digimundo: {len(stats['digimundo_internal'])}")
        print(f"   • Pesquisas IA: {len(stats['ai_research'])}")
        print(f"   • Não categorizados: {len(stats['uncategorized'])}")
        
        return stats

def main():
    reorganizer = CorrectReorganizer()
    stats = reorganizer.reorganize_all()
    
    print("\n✅ REORGANIZAÇÃO COMPLETA!")
    print("\nNova estrutura:")
    print("""
    DIGILANG_UNIFIED_SYSTEM/
    ├── 01_ROTEIROS_CINEMA/
    │   ├── nestor_luiz/      → Seus roteiros
    │   └── classicos/        → Cinema clássico (~30 PDFs)
    ├── 02_ROTEIROS_TV/
    │   └── series/           → Séries TV (~20 PDFs)
    ├── 03_MANUAIS_ROTEIRO/
    │   └── teoria_pratica/   → APENAS manuais reais (~12 PDFs)
    ├── 04_SISTEMA_DIGIMUNDO/
    │   └── documentacao/     → Docs internos do sistema
    └── 05_UNCATEGORIZED/
        └── revisar/          → Para revisão manual
    """)

if __name__ == "__main__":
    main()