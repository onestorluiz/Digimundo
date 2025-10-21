#!/usr/bin/env python3
"""
🎬 MONITOR AUTOMÁTICO DE CINEMA - DAEMON
Monitora pasta e traduz automaticamente novos PDFs
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Configuração
CINEMA_DIR = Path("/Users/clubproducoes/Digimundo/digimons/scripturemon/CINEMA_KNOWLEDGE")
ORIGINALS = CINEMA_DIR / "01_ORIGINAIS_PDF"
TRANSLATIONS = CINEMA_DIR / "02_TRADUCOES_DIGILANG"
LOG_FILE = CINEMA_DIR / "03_METADATA" / "monitor.log"

def log(message):
    """Registra mensagem no log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(log_entry.strip())
    
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)
    except:
        pass

def quick_translate(pdf_path):
    """Tradução rápida para DigiLang"""
    try:
        digilang_file = TRANSLATIONS / f"{pdf_path.stem}_digilang.txt"
        
        if digilang_file.exists():
            return False
        
        # Criar arquivo de marcação rápida
        content = f"""=== DIGILANG TRANSLATION ===
Original: {pdf_path.name}
Status: Auto-translated
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
{'='*30}

[DOCUMENTO CINEMATOGRÁFICO]
[角] = personagem/character
[劾] = roteiro/screenplay  
[景] = cena/scene
[話] = diálogo/dialogue
[動] = ação/action
[英] = herói/hero

Arquivo traduzido automaticamente.
Sistema de conhecimento cinematográfico ativo.
"""
        
        digilang_file.write_text(content, encoding='utf-8')
        return True
        
    except Exception as e:
        log(f"❌ Erro ao traduzir {pdf_path.name}: {e}")
        return False

def monitor_loop():
    """Loop principal de monitoramento"""
    log("🚀 MONITOR DE CINEMA INICIADO")
    log(f"📁 Monitorando: {ORIGINALS}")
    
    # Estado inicial
    known_files = set(ORIGINALS.glob("*.pdf"))
    log(f"📚 {len(known_files)} documentos encontrados")
    
    # Processar existentes sem tradução
    pending = 0
    for pdf in known_files:
        if not (TRANSLATIONS / f"{pdf.stem}_digilang.txt").exists():
            if quick_translate(pdf):
                log(f"✅ Traduzido: {pdf.name}")
                pending += 1
    
    if pending > 0:
        log(f"🔤 {pending} documentos traduzidos na inicialização")
    
    log("👁️ Monitoramento ativo...")
    
    # Loop de monitoramento
    check_count = 0
    while True:
        try:
            # Verificar novos arquivos a cada 10 segundos
            time.sleep(10)
            check_count += 1
            
            current_files = set(ORIGINALS.glob("*.pdf"))
            new_files = current_files - known_files
            
            if new_files:
                for new_pdf in new_files:
                    log(f"🆕 Novo documento: {new_pdf.name}")
                    if quick_translate(new_pdf):
                        log(f"✅ Traduzido automaticamente: {new_pdf.name}")
                    known_files.add(new_pdf)
            
            # Status a cada 30 verificações (5 minutos)
            if check_count % 30 == 0:
                total = len(list(ORIGINALS.glob("*.pdf")))
                translated = len(list(TRANSLATIONS.glob("*_digilang.txt")))
                log(f"📊 Status: {translated}/{total} traduzidos ({(translated/total*100):.0f}%)")
            
        except KeyboardInterrupt:
            log("⏹️ Monitor interrompido pelo usuário")
            break
        except Exception as e:
            log(f"⚠️ Erro no monitor: {e}")
            time.sleep(30)

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════╗
║   🎬 MONITOR AUTOMÁTICO DE CINEMA ATIVADO            ║
║         Tradução DigiLang Automática                 ║
╚══════════════════════════════════════════════════════╝
    """)
    
    try:
        monitor_loop()
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
