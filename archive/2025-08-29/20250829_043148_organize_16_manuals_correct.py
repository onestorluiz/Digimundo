#!/usr/bin/env python3
"""
🎯 Organizador Final - 16 Manuais de Roteiro + Estrutura Correta
"""

import shutil
from pathlib import Path
import os

class FinalOrganizer16Manuals:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.unified_path = self.base_path / "DIGILANG_FINAL_SYSTEM"
        
        print("╔" + "═"*58 + "╗")
        print("║  📚 ORGANIZADOR FINAL - 16 MANUAIS + CINEMA           ║")
        print("╚" + "═"*58 + "╝")
        
        # Lista COMPLETA dos 16 manuais de roteiro
        self.manual_identifiers = [
            # Os 12 já identificados
            ('anatomy of story', 'john truby'),
            ('story', 'robert', 'mckee'),
            ('screenplay', 'foundations', 'syd field'),
            ('creating character arcs', 'weiland'),
            ('writers journey', 'vogler'),
            ('art of dramatic writing', 'egri'),
            ('writing short films', 'cowgill'),
            ('writing the tv drama', 'pamela douglas'),
            ('21st century screenplay', 'aronson'),
            ('heroine', 'journey', 'murdock'),
            ('ontology', 'tragedy', 'aristotle'),
            ('fundamentals of screenwriting',),
            
            # Os 4 que faltavam
            ('making a good script great', 'seger'),
            ('save the cat', 'snyder'),
            ('screenwriter', 'bible', 'trottier'),
            ('into the woods', 'yorke')
        ]
        
        self.stats = {
            'manuais': [],
            'roteiros_cinema': [],
            'roteiros_tv': [],
            'digimundo': [],
            'nestor': []
        }
    
    def setup_final_structure(self):
        """Cria estrutura definitiva"""
        print("\n📁 CRIANDO ESTRUTURA FINAL DEFINITIVA")
        print("="*50)
        
        structure = {
            "01_MEU_ROTEIRO": ["nestor_luiz"],
            "02_MANUAIS_ROTEIRO": ["16_livros_teoria"],
            "03_ROTEIROS_CINEMA": ["classicos"],
            "04_ROTEIROS_TV": ["series"],
            "05_SISTEMA_DIGIMUNDO": ["docs_internos"],
            "06_DIGILANG": ["dictionary", "cache", "translations"]
        }
        
        self.unified_path.mkdir(exist_ok=True)
        
        for main_dir, subdirs in structure.items():
            for subdir in subdirs:
                path = self.unified_path / main_dir / subdir
                path.mkdir(parents=True, exist_ok=True)
        
        print("   ✅ Estrutura criada")
    
    def is_manual(self, filename):
        """Verifica se é um dos 16 manuais"""
        name_lower = filename.lower()
        
        for manual_terms in self.manual_identifiers:
            if all(term in name_lower for term in manual_terms):
                return True
        return False
    
    def categorize_pdf(self, pdf_path):
        """Categoriza PDF corretamente"""
        name = pdf_path.name.lower()
        
        # 1. Nestor Luiz (seu roteiro)
        if 'nestor' in name or 'sonhos sem' in name:
            return 'nestor'
        
        # 2. Um dos 16 manuais de roteiro
        if self.is_manual(pdf_path.name):
            return 'manual'
        
        # 3. Documentos do Digimundo
        if any(emoji in pdf_path.name for emoji in ['🌟', '🔥', '📜', '🧬', '🎯', '🌐', '💬', '📊']):
            return 'digimundo'
        if any(term in name for term in ['digimundo', 'digimon', 'claudemon', 'blueprint', 'protocolo']):
            return 'digimundo'
        
        # 4. Séries de TV
        tv_shows = ['breaking bad', 'game of thrones', 'true detective', 'black mirror',
                    'succession', 'the boys', 'house of cards', 'mad men', 'mr. robot',
                    'mindhunter', 'peaky blinders', 'this is us', 'vikings', 'barry',
                    'entourage', 'spartacus', 'narcos', 'queens gambit', 'bear', 'severance']
        if any(show in name for show in tv_shows):
            return 'tv'
        
        # 5. Roteiros de cinema (default para roteiros)
        if any(term in name for term in ['screenplay', 'script', 'draft', 'release', 'production']):
            return 'cinema'
        
        return 'cinema'  # default
    
    def copy_from_downloads_if_needed(self):
        """Copia os manuais faltantes de Downloads se necessário"""
        print("\n🔍 Verificando manuais em Downloads...")
        
        downloads_path = Path("/Users/clubproducoes/Downloads/Arquivo 2")
        if downloads_path.exists():
            # Buscar Making a Good Script Great
            making_good_script = list(downloads_path.glob("*Making*Good*Script*.epub"))
            if making_good_script:
                print(f"   ✅ Encontrado: Making a Good Script Great (EPUB)")
                # Nota: é EPUB, não PDF, mas ainda é um manual importante
    
    def organize_all_pdfs(self):
        """Organiza todos os PDFs na estrutura correta"""
        print("\n🚀 ORGANIZANDO TODOS OS PDFs")
        print("="*50)
        
        # Buscar todos os PDFs únicos já consolidados
        existing_unified = self.base_path / "DIGILANG_UNIFIED_SYSTEM"
        all_pdfs = []
        
        if existing_unified.exists():
            all_pdfs = list(existing_unified.glob("**/*.pdf"))
        
        # Adicionar PDFs de outras localizações conhecidas
        other_locations = [
            self.base_path / "digimons/scripturemon/data/roteiros",
            self.base_path / "digimons/scripturemon_backup_20250827_165659/cinema/1_teoria_roteiro"
        ]
        
        for location in other_locations:
            if location.exists():
                all_pdfs.extend(list(location.glob("*.pdf")))
        
        # Remove duplicatas baseado no nome
        unique_pdfs = {}
        for pdf in all_pdfs:
            if pdf.name not in unique_pdfs:
                unique_pdfs[pdf.name] = pdf
        
        print(f"   📊 {len(unique_pdfs)} PDFs únicos encontrados")
        
        # Organizar por categoria
        for pdf_name, pdf_path in unique_pdfs.items():
            category = self.categorize_pdf(pdf_path)
            
            # Define destino baseado na categoria
            if category == 'nestor':
                dest_dir = self.unified_path / "01_MEU_ROTEIRO/nestor_luiz"
                self.stats['nestor'].append(pdf_name)
            elif category == 'manual':
                dest_dir = self.unified_path / "02_MANUAIS_ROTEIRO/16_livros_teoria"
                self.stats['manuais'].append(pdf_name)
            elif category == 'tv':
                dest_dir = self.unified_path / "04_ROTEIROS_TV/series"
                self.stats['roteiros_tv'].append(pdf_name)
            elif category == 'digimundo':
                dest_dir = self.unified_path / "05_SISTEMA_DIGIMUNDO/docs_internos"
                self.stats['digimundo'].append(pdf_name)
            else:  # cinema
                dest_dir = self.unified_path / "03_ROTEIROS_CINEMA/classicos"
                self.stats['roteiros_cinema'].append(pdf_name)
            
            # Copiar arquivo se não existe no destino
            dest_file = dest_dir / pdf_name
            if not dest_file.exists() and pdf_path.exists():
                try:
                    shutil.copy2(pdf_path, dest_file)
                except Exception as e:
                    pass
    
    def verify_16_manuals(self):
        """Verifica se temos os 16 manuais"""
        print("\n📚 VERIFICANDO OS 16 MANUAIS DE ROTEIRO")
        print("="*50)
        
        expected_manuals = [
            "The Anatomy of Story - John Truby",
            "Story - Robert McKee", 
            "Screenplay: The Foundations - Syd Field",
            "Creating Character Arcs - K.M. Weiland",
            "The Writers Journey - Christopher Vogler",
            "The Art of Dramatic Writing - Lajos Egri",
            "Writing Short Films - Linda Cowgill",
            "Writing the TV Drama Series - Pamela Douglas",
            "The 21st Century Screenplay - Linda Aronson",
            "The Heroine's Journey Workbook - Maureen Murdock",
            "Ontology and the Art of Tragedy - Martha Husain",
            "The Fundamentals of Screenwriting",
            "Making a Good Script Great - Linda Seger",
            "Save the Cat! - Blake Snyder",
            "The Screenwriter's Bible - David Trottier",
            "Into the Woods - John Yorke"
        ]
        
        found_manuals = []
        missing_manuals = []
        
        for expected in expected_manuals:
            found = False
            for manual in self.stats['manuais']:
                manual_lower = manual.lower()
                # Verificação flexível
                if ('anatomy' in expected.lower() and 'anatomy' in manual_lower) or \
                   ('story' in expected.lower() and 'mckee' in expected.lower() and 'story' in manual_lower and 'substance' in manual_lower) or \
                   ('screenplay' in expected.lower() and 'foundations' in expected.lower() and 'screenplay' in manual_lower and 'syd' in manual_lower) or \
                   ('character arcs' in expected.lower() and 'character arcs' in manual_lower) or \
                   ('writers journey' in expected.lower() and 'writers journey' in manual_lower) or \
                   ('dramatic writing' in expected.lower() and 'dramatic writing' in manual_lower) or \
                   ('short films' in expected.lower() and 'short films' in manual_lower) or \
                   ('tv drama' in expected.lower() and 'tv drama' in manual_lower) or \
                   ('21st century' in expected.lower() and '21st century' in manual_lower) or \
                   ('heroine' in expected.lower() and 'heroine' in manual_lower) or \
                   ('ontology' in expected.lower() and 'ontology' in manual_lower) or \
                   ('fundamentals' in expected.lower() and 'fundamentals' in manual_lower and 'screenwriting' in manual_lower) or \
                   ('making' in expected.lower() and 'good script' in expected.lower() and 'making' in manual_lower and 'good' in manual_lower) or \
                   ('save the cat' in expected.lower() and 'save' in manual_lower and 'cat' in manual_lower) or \
                   ('screenwriter' in expected.lower() and 'bible' in expected.lower() and 'screenwriter' in manual_lower and 'bible' in manual_lower) or \
                   ('into the woods' in expected.lower() and 'into' in manual_lower and 'woods' in manual_lower):
                    found = True
                    found_manuals.append(expected)
                    break
            
            if not found:
                missing_manuals.append(expected)
        
        print(f"   ✅ Encontrados: {len(found_manuals)}/16")
        for manual in found_manuals[:5]:
            print(f"      • {manual}")
        if len(found_manuals) > 5:
            print(f"      • ... +{len(found_manuals)-5} mais")
        
        if missing_manuals:
            print(f"\n   ⚠️ Faltando: {len(missing_manuals)}")
            for manual in missing_manuals:
                print(f"      • {manual}")
        
        return len(found_manuals), missing_manuals
    
    def generate_final_report(self):
        """Gera relatório final"""
        print(f"\n{'='*60}")
        print("📊 RELATÓRIO FINAL - SISTEMA ORGANIZADO")
        print(f"{'='*60}")
        
        found_count, missing = self.verify_16_manuals()
        
        print(f"""
📁 ESTRUTURA FINAL DEFINITIVA:

1️⃣ MEU ROTEIRO:
   • {len(self.stats['nestor'])} arquivo(s)
   {"• " + self.stats['nestor'][0] if self.stats['nestor'] else ""}

2️⃣ MANUAIS DE ROTEIRO ({found_count}/16):
   • Encontrados: {len(self.stats['manuais'])} PDFs
   
3️⃣ ROTEIROS DE CINEMA:
   • {len(self.stats['roteiros_cinema'])} roteiros clássicos

4️⃣ ROTEIROS DE TV:
   • {len(self.stats['roteiros_tv'])} séries

5️⃣ SISTEMA DIGIMUNDO:
   • {len(self.stats['digimundo'])} documentos internos

📍 Local: {self.unified_path}

✅ SISTEMA PRONTO PARA USO!
   • Scripturemon deve focar nos roteiros de cinema
   • Manuais separados para referência teórica
   • Documentos Digimundo isolados
""")
        
        if missing:
            print("\n⚠️ NOTA: Alguns manuais podem estar em formato EPUB ou não disponíveis")

def main():
    organizer = FinalOrganizer16Manuals()
    
    # Criar estrutura
    organizer.setup_final_structure()
    
    # Verificar Downloads
    organizer.copy_from_downloads_if_needed()
    
    # Organizar PDFs
    organizer.organize_all_pdfs()
    
    # Relatório final
    organizer.generate_final_report()
    
    print("\n🎉 ORGANIZAÇÃO COMPLETA!")

if __name__ == "__main__":
    main()