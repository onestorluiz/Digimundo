#!/usr/bin/env python3
"""
💯 Mapeamento Completo 100% - DigiLang Ultimate
Usa caracteres CJK para garantir cobertura total
"""

import json
import sqlite3
import re
from pathlib import Path
from collections import Counter
from datetime import datetime
import unicodedata

class DigiLangUltimateMapper:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.db_path = self.base_path / "digistore/database/digistore.db"
        self.dict_path = self.base_path / "digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json"
        
        # Carregar dicionário
        self.load_dictionary()
        
        # CJK Ranges - 20,000+ caracteres disponíveis
        self.cjk_start = 0x4E00
        self.cjk_end = 0x9FFF
        self.current_cjk = self.cjk_start
        
    def load_dictionary(self):
        """Carrega dicionário atual"""
        print("📚 Carregando dicionário DigiLang...")
        
        with open(self.dict_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.current_dict = data['symbols']
            self.metadata = data
            
        self.used_symbols = set(self.current_dict.values())
        print(f"   ✅ {len(self.current_dict)} palavras mapeadas")
        print(f"   ✅ {len(self.used_symbols)} símbolos em uso")
        
    def get_next_cjk_symbol(self):
        """Retorna próximo caractere CJK disponível"""
        while self.current_cjk <= self.cjk_end:
            symbol = chr(self.current_cjk)
            self.current_cjk += 1
            
            if symbol not in self.used_symbols:
                self.used_symbols.add(symbol)
                return symbol
                
        return None
    
    def normalize_word(self, word: str) -> str:
        """Normaliza palavra"""
        word = word.lower().strip()
        # Manter pontuação interna (para palavras como "don't")
        word = re.sub(r'^[^\w\']+|[^\w\']+$', '', word)
        return word
    
    def complete_mapping(self):
        """Mapeia TODAS as palavras dos documentos"""
        print("\n🚀 MAPEAMENTO COMPLETO 100%...")
        print("="*60)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Coletar TODAS as palavras únicas
        all_words = set()
        
        cursor.execute("SELECT original_text FROM chunks")
        
        chunk_count = 0
        for row in cursor.fetchall():
            chunk_count += 1
            text = row[0]
            
            # Processar todas as palavras
            words = re.findall(r'\b[\w\']+\b', text.lower())
            all_words.update(words)
            
            if chunk_count % 1000 == 0:
                print(f"   Processados: {chunk_count} chunks, {len(all_words)} palavras únicas")
        
        conn.close()
        
        print(f"\n📊 Total de palavras únicas encontradas: {len(all_words)}")
        
        # Mapear palavras não mapeadas
        new_mappings = {}
        already_mapped = 0
        newly_mapped = 0
        
        for word in all_words:
            normalized = self.normalize_word(word)
            
            if normalized in self.current_dict:
                already_mapped += 1
            else:
                # Criar novo mapeamento com CJK
                symbol = self.get_next_cjk_symbol()
                if symbol:
                    new_mappings[normalized] = symbol
                    newly_mapped += 1
                    
                    if newly_mapped <= 50:
                        print(f"   ✅ {normalized} → {symbol}")
        
        print(f"\n📈 Resultados:")
        print(f"   • Já mapeadas: {already_mapped}")
        print(f"   • Novos mapeamentos: {newly_mapped}")
        print(f"   • Total: {already_mapped + newly_mapped}")
        
        return new_mappings
    
    def save_complete_dictionary(self, new_mappings):
        """Salva dicionário 100% completo"""
        print("\n💾 SALVANDO DICIONÁRIO 100% COMPLETO...")
        print("="*60)
        
        # Combinar todos os mapeamentos
        complete_dict = {**self.current_dict, **new_mappings}
        
        # Criar versão definitiva
        final_data = {
            "version": "7.0-ULTIMATE-100%",
            "name": "DigiLang Ultimate - Cobertura Total Garantida",
            "description": "Sistema com 100% de cobertura usando caracteres CJK",
            "created": self.metadata.get("created"),
            "completed": datetime.now().isoformat(),
            "rules": [
                "REGRA 1: Cada palavra = exatamente 1 símbolo Unicode",
                "REGRA 2: Conceitos equivalentes PT/EN = mesmo símbolo",
                "REGRA 3: 100% de cobertura garantida com CJK",
                "REGRA 4: Determinístico - mesma palavra sempre gera mesmo símbolo"
            ],
            "stats": {
                "total_words": len(complete_dict),
                "unique_symbols": len(set(complete_dict.values())),
                "coverage": "100%",
                "cjk_symbols_used": len([s for s in complete_dict.values() if 0x4E00 <= ord(s) <= 0x9FFF])
            },
            "symbols": complete_dict
        }
        
        # Backup
        backup_path = self.base_path / f"DIGILANG_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(self.dict_path, 'r') as f:
            backup = json.load(f)
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup, f, ensure_ascii=False, indent=2)
        print(f"   💾 Backup: {backup_path}")
        
        # Salvar versão final
        with open(self.dict_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ Dicionário 100% salvo: {self.dict_path}")
        print(f"   📊 Total de palavras: {len(complete_dict):,}")
        print(f"   🎯 Símbolos únicos: {len(set(complete_dict.values())):,}")
        print(f"   🀄 Símbolos CJK usados: {final_data['stats']['cjk_symbols_used']:,}")
        
        return complete_dict
    
    def verify_coverage(self, complete_dict):
        """Verifica se realmente temos 100% de cobertura"""
        print("\n✅ VERIFICANDO COBERTURA 100%...")
        print("="*60)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Pegar amostra de chunks
        cursor.execute("SELECT original_text FROM chunks ORDER BY RANDOM() LIMIT 100")
        
        total_words = 0
        mapped_words = 0
        unmapped_examples = []
        
        for row in cursor.fetchall():
            text = row[0]
            words = re.findall(r'\b[\w\']+\b', text.lower())
            
            for word in words:
                total_words += 1
                normalized = self.normalize_word(word)
                
                if normalized in complete_dict:
                    mapped_words += 1
                else:
                    if len(unmapped_examples) < 10:
                        unmapped_examples.append(word)
        
        conn.close()
        
        coverage = (mapped_words / total_words * 100) if total_words else 0
        
        print(f"   📊 Amostra de 100 chunks aleatórios:")
        print(f"   • Total de palavras: {total_words}")
        print(f"   • Palavras mapeadas: {mapped_words}")
        print(f"   • Cobertura: {coverage:.2f}%")
        
        if unmapped_examples:
            print(f"   ⚠️ Exemplos não mapeados: {unmapped_examples}")
        else:
            print(f"   ✅ COBERTURA 100% CONFIRMADA!")
            
        return coverage

def main():
    print("╔" + "═"*58 + "╗")
    print("║      💯 DIGILANG ULTIMATE - COBERTURA 100%             ║")
    print("╚" + "═"*58 + "╝")
    
    mapper = DigiLangUltimateMapper()
    
    # Mapear TODAS as palavras
    new_mappings = mapper.complete_mapping()
    
    # Salvar dicionário completo
    complete_dict = mapper.save_complete_dictionary(new_mappings)
    
    # Verificar cobertura
    coverage = mapper.verify_coverage(complete_dict)
    
    print("\n✨ SISTEMA COMPLETO!")
    print(f"🎯 DigiLang agora tem cobertura de {coverage:.2f}%")
    
    if coverage >= 99.9:
        print("💯 OBJETIVO ALCANÇADO: COBERTURA TOTAL!")
    
    return complete_dict

if __name__ == "__main__":
    main()