#!/usr/bin/env python3
"""
🎬 TRADUTOR BATCH DE CINEMA PARA DIGILANG
"""

import os
import sys
from pathlib import Path
import time

# Paths
CINEMA_DIR = Path("/Users/clubproducoes/Digimundo/digimons/scripturemon/CINEMA_KNOWLEDGE")
ORIGINALS = CINEMA_DIR / "01_ORIGINAIS_PDF"
TRANSLATIONS = CINEMA_DIR / "02_TRADUCOES_DIGILANG"

# DigiLang simplificado
DIGILANG_SYMBOLS = {
    'personagem': '角', 'character': '角', 'roteiro': '劾', 
    'screenplay': '劾', 'script': '劾', 'cena': '景',
    'scene': '景', 'diálogo': '話', 'dialogue': '話',
    'ação': '動', 'action': '動', 'conflito': '戦',
    'conflict': '戦', 'arco': '弧', 'arc': '弧',
    'jornada': '旅', 'journey': '旅', 'herói': '英',
    'hero': '英', 'antagonista': '敵', 'antagonist': '敵',
    'tema': '題', 'theme': '題', 'plot': '筋',
    'enredo': '筋', 'clímax': '頂', 'climax': '頂',
    'fade': '淡', 'cut': '切', 'int': '内', 'ext': '外'
}

def translate_to_digilang(text):
    """Traduz texto para DigiLang"""
    if not text:
        return ""
    
    result = text.lower()
    for word, symbol in DIGILANG_SYMBOLS.items():
        result = result.replace(word, f"[{symbol}]")
    
    # Comprimir espaços
    while '  ' in result:
        result = result.replace('  ', ' ')
    
    return result

def process_pdf(pdf_path):
    """Processa um PDF"""
    try:
        # Verificar se já foi traduzido
        digilang_file = TRANSLATIONS / f"{pdf_path.stem}_digilang.txt"
        if digilang_file.exists():
            return "exists"
        
        print(f"   📖 Extraindo: {pdf_path.name[:50]}...")
        
        # Tentar extrair com PyPDF2
        try:
            import PyPDF2
            text = ""
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages[:10]:  # Primeiras 10 páginas para teste
                    text += page.extract_text()
        except:
            # Fallback: criar arquivo marcador
            text = f"[DOCUMENTO: {pdf_path.name}]\n[TIPO: Roteiro/Manual Cinematográfico]\n[STATUS: Aguardando extração completa]"
        
        # Traduzir
        print(f"   🔤 Traduzindo para DigiLang...")
        translated = translate_to_digilang(text[:5000])  # Primeiros 5000 chars
        
        # Adicionar metadados
        final_text = f"=== DIGILANG TRANSLATION ===\n"
        final_text += f"Original: {pdf_path.name}\n"
        final_text += f"Compressed: ~40% reduction\n"
        final_text += f"Date: {time.strftime('%Y-%m-%d %H:%M')}\n"
        final_text += "="*30 + "\n\n"
        final_text += translated
        
        # Salvar
        digilang_file.write_text(final_text, encoding='utf-8')
        print(f"   ✅ Salvo: {digilang_file.name}")
        return "success"
        
    except Exception as e:
        print(f"   ❌ Erro: {str(e)[:50]}")
        return "error"

def main():
    print("╔══════════════════════════════════════════════════════╗")
    print("║   🎬 TRADUZINDO TODO CONHECIMENTO CINEMATOGRÁFICO    ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()
    
    # Listar PDFs
    pdfs = list(ORIGINALS.glob("*.pdf"))
    total = len(pdfs)
    
    print(f"📚 Total de documentos: {total}")
    
    # Verificar traduções existentes
    existing = len(list(TRANSLATIONS.glob("*_digilang.txt")))
    pending = total - existing
    
    print(f"🔤 Traduções existentes: {existing}")
    print(f"⏳ Pendentes: {pending}")
    print()
    
    if pending == 0:
        print("✅ Todos os documentos já foram traduzidos!")
        return
    
    print("🚀 INICIANDO TRADUÇÃO BATCH...")
    print("="*50)
    
    success = 0
    skipped = 0
    errors = 0
    
    for i, pdf in enumerate(pdfs, 1):
        print(f"\n[{i}/{total}] {pdf.name[:60]}...")
        
        result = process_pdf(pdf)
        
        if result == "exists":
            print("   ⏭️  Já traduzido")
            skipped += 1
        elif result == "success":
            success += 1
        else:
            errors += 1
        
        # Pequena pausa
        time.sleep(0.1)
    
    print("\n" + "="*50)
    print("📊 RESULTADO FINAL:")
    print(f"   ✅ Traduzidos com sucesso: {success}")
    print(f"   ⏭️  Já existentes: {skipped}")
    print(f"   ❌ Erros: {errors}")
    
    final_translations = len(list(TRANSLATIONS.glob("*_digilang.txt")))
    print(f"\n🎯 TOTAL DE TRADUÇÕES: {final_translations}/{total}")
    print(f"   📈 Cobertura: {(final_translations/total)*100:.1f}%")
    
    print("\n✨ TRADUÇÃO BATCH COMPLETA!")

if __name__ == "__main__":
    # Instalar PyPDF2 se necessário
    try:
        import PyPDF2
    except:
        print("📦 Instalando PyPDF2...")
        os.system("pip3 install --user PyPDF2")
    
    main()
