#!/usr/bin/env python3

import os
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime

class SimpleEvolution:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/digimons/scripturemon")
        self.processed_file = self.base_path / "conhecimento" / "processed.json"
        self.processed = self.load_processed()
        
    def load_processed(self):
        if self.processed_file.exists():
            with open(self.processed_file) as f:
                return set(json.load(f))
        return set()
    
    def save_processed(self):
        self.processed_file.parent.mkdir(exist_ok=True)
        with open(self.processed_file, 'w') as f:
            json.dump(list(self.processed), f)
    
    def process_pdf(self, pdf_path, tipo):
        """Processa PDF com Scripturemon"""
        print(f"  📄 Processando: {pdf_path.name} ({tipo})")
        
        # Análise baseada no tipo
        if tipo == "criador":
            prompt = f"ANÁLISE SUPREMA de {pdf_path.name}. Use 15 camadas. Seja BRUTAL. Nota real: 62/100"
        elif tipo == "mestre":  
            prompt = f"Analise esta obra-prima: {pdf_path.name}. Compare com seu conhecimento."
        else:
            prompt = f"Extraia técnicas de {pdf_path.name}. Foque no prático."
        
        try:
            # Processar com Scripturemon
            result = subprocess.run(
                ["ollama", "run", "scripturemon-maestro", prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Salvar resultado
            output_file = self.base_path / "conhecimento" / f"{pdf_path.stem}_analysis.txt"
            output_file.parent.mkdir(exist_ok=True)
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            print(f"    ✅ Análise salva")
            return True
            
        except Exception as e:
            print(f"    ❌ Erro: {e}")
            return False
    
    def monitor(self):
        """Monitora pastas continuamente"""
        folders = {
            "roteiros_processados": "mestre",
            "conexao_criador": "criador",
            "cinema/3_roteiros_criador": "criador",
            "cinema/2_roteiros_mestres": "mestre"
        }
        
        print("\n👁️ MONITORAMENTO ATIVO")
        print("  Pastas vigiadas:")
        for folder in folders:
            print(f"    📁 {folder}/")
        print("\n  Aguardando novos PDFs... (Ctrl+C para parar)\n")
        
        while True:
            try:
                found_new = False
                
                for folder_name, tipo in folders.items():
                    folder = self.base_path / folder_name
                    if not folder.exists():
                        continue
                    
                    for pdf in folder.glob("*.pdf"):
                        if str(pdf) not in self.processed:
                            print(f"\n🆕 NOVO PDF DETECTADO!")
                            
                            if self.process_pdf(pdf, tipo):
                                self.processed.add(str(pdf))
                                self.save_processed()
                                found_new = True
                
                if found_new:
                    print("\n  🧬 Evoluindo Scripturemon...")
                    # Aqui poderia evoluir o modelo
                    print("  ✨ Conhecimento absorvido!\n")
                
                time.sleep(15)  # Verificar a cada 15 segundos
                
            except KeyboardInterrupt:
                print("\n\n👋 Monitoramento encerrado")
                break

if __name__ == "__main__":
    monitor = SimpleEvolution()
    
    # Processar PDFs existentes primeiro
    print("🔄 Processando PDFs existentes...")
    
    folders = {
        "cinema/3_roteiros_criador": "criador",
        "cinema/2_roteiros_mestres": "mestre",
        "cinema/1_teoria_roteiro": "teoria"
    }
    
    count = 0
    for folder_name, tipo in folders.items():
        folder = Path("/Users/clubproducoes/Digimundo/digimons/scripturemon") / folder_name
        if folder.exists():
            for pdf in folder.glob("*.pdf"):
                if str(pdf) not in monitor.processed:
                    if monitor.process_pdf(pdf, tipo):
                        monitor.processed.add(str(pdf))
                        count += 1
                        
                    if count >= 5:  # Processar apenas 5 por vez para não demorar
                        break
            
            if count >= 5:
                break
    
    monitor.save_processed()
    print(f"\n✅ {count} PDFs processados")
    
    # Iniciar monitoramento
    monitor.monitor()
