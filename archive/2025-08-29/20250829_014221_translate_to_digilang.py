#!/usr/bin/env python3
"""
🌐 Sistema de Tradução em Lote para DigiLang
Traduz todos os documentos do DigiStore para a língua simbólica do Digimundo
"""

import json
import sqlite3
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import unicodedata
import re

class DigiLangBatchTranslator:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.db_path = self.base_path / "digistore/database/digistore.db"
        self.dict_path = self.base_path / "digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json"
        self.output_dir = self.base_path / "translated_documents"
        
        # Criar diretório de saída
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Carregar dicionário DigiLang
        self.load_dictionary()
        
        # Estatísticas
        self.stats = {
            'total_documents': 0,
            'total_chunks': 0,
            'total_words': 0,
            'translated_words': 0,
            'unique_symbols': set(),
            'coverage_by_doc': {}
        }
        
    def load_dictionary(self):
        """Carrega o dicionário definitivo da DigiLang"""
        print("📚 Carregando dicionário DigiLang...")
        
        with open(self.dict_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.digilang_dict = data['symbols']
            self.metadata = {
                'version': data.get('version', 'unknown'),
                'stats': data.get('stats', {})
            }
        
        # Criar dicionário reverso para decodificação
        self.reverse_dict = {v: k for k, v in self.digilang_dict.items()}
        
        print(f"   ✅ {len(self.digilang_dict)} palavras carregadas")
        print(f"   ✅ Versão: {self.metadata.get('version', 'unknown')}")
        
    def normalize_word(self, word: str) -> str:
        """Normaliza palavra para busca no dicionário"""
        # Remover acentos e converter para minúsculas
        word = word.lower().strip()
        # Remover pontuação das extremidades
        word = re.sub(r'^[^\w]+|[^\w]+$', '', word)
        return word
    
    def translate_word(self, word: str) -> str:
        """Traduz uma palavra para DigiLang"""
        normalized = self.normalize_word(word)
        
        # Buscar no dicionário
        if normalized in self.digilang_dict:
            symbol = self.digilang_dict[normalized]
            self.stats['translated_words'] += 1
            self.stats['unique_symbols'].add(symbol)
            return symbol
        
        # Se não encontrar, gerar símbolo consistente
        return self.generate_symbol(normalized)
    
    def generate_symbol(self, word: str) -> str:
        """Gera símbolo consistente para palavra não mapeada"""
        # Usar hash para gerar símbolo determinístico
        hash_val = hash(word) % 0x10000
        
        # Ranges seguros de Unicode
        ranges = [
            (0x2600, 0x26FF),  # Miscellaneous Symbols
            (0x2700, 0x27BF),  # Dingbats
            (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
        ]
        
        # Selecionar range baseado no hash
        range_idx = hash_val % len(ranges)
        start, end = ranges[range_idx]
        
        # Gerar símbolo dentro do range
        symbol_code = start + (hash_val % (end - start))
        
        try:
            return chr(symbol_code)
        except:
            # Fallback para símbolo padrão
            return '◊'
    
    def translate_text(self, text: str) -> Tuple[str, float]:
        """Traduz texto completo para DigiLang"""
        words = text.split()
        translated = []
        words_found = 0
        
        for word in words:
            # Preservar pontuação especial
            if word in ['.', ',', '!', '?', ':', ';', '-', '—']:
                translated.append(word)
                continue
            
            # Separar pontuação do final
            punct = ''
            clean_word = word
            if word and word[-1] in '.!?,;:':
                punct = word[-1]
                clean_word = word[:-1]
            
            # Traduzir palavra
            symbol = self.translate_word(clean_word)
            
            # Verificar se foi encontrada no dicionário
            if self.normalize_word(clean_word) in self.digilang_dict:
                words_found += 1
            
            translated.append(symbol + punct)
        
        # Calcular cobertura
        coverage = (words_found / len(words) * 100) if words else 0
        
        self.stats['total_words'] += len(words)
        
        return ' '.join(translated), coverage
    
    def load_documents(self) -> List[Dict]:
        """Carrega todos os documentos do banco"""
        print("\n📄 Carregando documentos do DigiStore...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Buscar todos os documentos
        cursor.execute("""
            SELECT id, source_file, title, metadata
            FROM documents
            ORDER BY source_file
        """)
        
        documents = []
        for row in cursor.fetchall():
            doc = {
                'id': row[0],
                'filename': row[1],  # source_file
                'title': row[2],
                'content': '',  # Será carregado dos chunks
                'metadata': json.loads(row[3]) if row[3] else {}
            }
            documents.append(doc)
        
        conn.close()
        
        print(f"   ✅ {len(documents)} documentos carregados")
        self.stats['total_documents'] = len(documents)
        
        return documents
    
    def translate_document(self, doc: Dict) -> Dict:
        """Traduz um documento completo"""
        filename = doc['filename']
        print(f"\n🔄 Traduzindo: {filename}")
        
        # Buscar chunks do documento para tradução
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT original_text
            FROM chunks
            WHERE doc_id = ?
            ORDER BY chunk_index
        """, (doc['id'],))
        
        chunks = cursor.fetchall()
        
        # Combinar todos os chunks para formar o documento completo
        full_text = ' '.join([chunk[0] for chunk in chunks])
        
        # Traduzir conteúdo completo
        translated_content, coverage = self.translate_text(full_text)
        
        # Traduzir chunks individuais para estatísticas
        translated_chunks = []
        for chunk in chunks[:10]:  # Primeiros 10 chunks para amostra
            chunk_translated, chunk_coverage = self.translate_text(chunk[0])
            translated_chunks.append({
                'original': chunk[0][:50] + "...",
                'translated': chunk_translated[:50] + "...",
                'coverage': chunk_coverage
            })
        
        conn.close()
        
        self.stats['total_chunks'] += len(chunks)
        self.stats['coverage_by_doc'][filename] = coverage
        
        print(f"   📊 Cobertura: {coverage:.1f}%")
        print(f"   📝 Chunks traduzidos: {len(chunks)}")
        
        return {
            'filename': filename,
            'original_size': len(full_text),
            'translated_size': len(translated_content),
            'content': translated_content,
            'chunks': translated_chunks,
            'coverage': coverage,
            'metadata': {
                **doc['metadata'],
                'translation_date': datetime.now().isoformat(),
                'digilang_version': self.metadata.get('version', 'unknown')
            }
        }
    
    def save_translation(self, translation: Dict):
        """Salva documento traduzido"""
        # Nome do arquivo de saída
        original_name = Path(translation['filename']).stem
        output_file = self.output_dir / f"{original_name}.dlg"
        
        # Salvar conteúdo traduzido
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translation['content'])
        
        # Salvar metadados
        meta_file = self.output_dir / f"{original_name}.dlg.json"
        
        metadata = {
            'original_filename': translation['filename'],
            'translation_date': translation['metadata']['translation_date'],
            'coverage': translation['coverage'],
            'original_size': translation['original_size'],
            'translated_size': translation['translated_size'],
            'chunks_count': len(translation['chunks']),
            'digilang_version': translation['metadata']['digilang_version']
        }
        
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"   💾 Salvo: {output_file}")
    
    def generate_report(self, translations: List[Dict]):
        """Gera relatório detalhado das traduções"""
        print("\n📊 GERANDO RELATÓRIO...")
        print("="*60)
        
        report_file = self.output_dir / f"translation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        # Calcular estatísticas gerais
        avg_coverage = sum(self.stats['coverage_by_doc'].values()) / len(self.stats['coverage_by_doc'])
        compression_rate = sum(t['translated_size'] for t in translations) / sum(t['original_size'] for t in translations)
        
        report = f"""# 📊 Relatório de Tradução DigiLang

## 📅 Informações Gerais
- **Data**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Versão DigiLang**: {self.metadata.get('version', 'unknown')}
- **Documentos processados**: {self.stats['total_documents']}
- **Total de chunks**: {self.stats['total_chunks']}

## 📈 Estatísticas de Tradução
- **Total de palavras**: {self.stats['total_words']:,}
- **Palavras traduzidas**: {self.stats['translated_words']:,}
- **Símbolos únicos usados**: {len(self.stats['unique_symbols']):,}
- **Cobertura média**: {avg_coverage:.2f}%
- **Taxa de compressão**: {compression_rate:.2f}x

## 📄 Documentos Traduzidos

| Documento | Tamanho Original | Tamanho Traduzido | Cobertura | Chunks |
|-----------|------------------|-------------------|-----------|---------|
"""
        
        for trans in sorted(translations, key=lambda x: x['coverage'], reverse=True):
            name = Path(trans['filename']).stem[:30]
            report += f"| {name} | {trans['original_size']:,} | {trans['translated_size']:,} | {trans['coverage']:.1f}% | {len(trans['chunks'])} |\n"
        
        report += f"""

## 🏆 Top 10 Símbolos Mais Usados
"""
        
        # Contar frequência de símbolos
        symbol_freq = {}
        for trans in translations:
            for symbol in trans['content']:
                if symbol in self.reverse_dict:
                    symbol_freq[symbol] = symbol_freq.get(symbol, 0) + 1
        
        top_symbols = sorted(symbol_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        report += "\n| Símbolo | Palavra Original | Frequência |\n"
        report += "|---------|------------------|------------|\n"
        
        for symbol, freq in top_symbols:
            word = self.reverse_dict.get(symbol, "?")
            report += f"| {symbol} | {word} | {freq:,} |\n"
        
        report += f"""

## 💾 Arquivos Gerados
- **Diretório de saída**: `{self.output_dir}`
- **Formato**: `.dlg` (DigiLang Document)
- **Metadados**: `.dlg.json`

## 🎯 Próximos Passos
1. Revisar traduções com baixa cobertura
2. Expandir dicionário DigiLang com termos técnicos
3. Implementar sistema de contexto para melhor tradução
4. Criar visualizador de documentos DigiLang

---
*Relatório gerado automaticamente pelo Sistema DigiLang v{self.metadata.get('version', '?')}*
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ Relatório salvo: {report_file}")
        
        # Imprimir resumo
        print("\n" + "="*60)
        print("📊 RESUMO DA TRADUÇÃO")
        print("="*60)
        print(f"✅ Documentos traduzidos: {self.stats['total_documents']}")
        print(f"📝 Total de palavras: {self.stats['total_words']:,}")
        print(f"🎯 Cobertura média: {avg_coverage:.2f}%")
        print(f"💾 Arquivos salvos em: {self.output_dir}")
        print(f"📊 Relatório em: {report_file.name}")
    
    def translate_all(self):
        """Executa tradução completa de todos os documentos"""
        print("╔" + "═"*58 + "╗")
        print("║      🌐 TRADUÇÃO EM LOTE PARA DIGILANG                  ║")
        print("╚" + "═"*58 + "╝")
        
        # Carregar documentos
        documents = self.load_documents()
        
        if not documents:
            print("❌ Nenhum documento encontrado para traduzir!")
            return
        
        # Traduzir cada documento
        translations = []
        
        print("\n🚀 INICIANDO TRADUÇÕES...")
        print("="*60)
        
        for i, doc in enumerate(documents, 1):
            print(f"\n[{i}/{len(documents)}]", end="")
            
            try:
                translation = self.translate_document(doc)
                self.save_translation(translation)
                translations.append(translation)
                
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                continue
        
        # Gerar relatório final
        self.generate_report(translations)
        
        print("\n✨ TRADUÇÃO CONCLUÍDA COM SUCESSO!")
        
        return translations

def main():
    translator = DigiLangBatchTranslator()
    translations = translator.translate_all()
    
    # Criar script de visualização rápida
    viewer_script = Path("/Users/clubproducoes/Digimundo/view_digilang.sh")
    
    viewer_content = """#!/bin/bash
# Visualizador rápido de documentos DigiLang

if [ -z "$1" ]; then
    echo "Uso: ./view_digilang.sh <arquivo.dlg>"
    echo ""
    echo "Documentos disponíveis:"
    ls -la /Users/clubproducoes/Digimundo/translated_documents/*.dlg
    exit 1
fi

echo "📄 Visualizando: $1"
echo "="
head -n 20 "$1"
echo ""
echo "..."
echo ""
echo "📊 Metadados:"
cat "${1}.json" 2>/dev/null | python3 -m json.tool
"""
    
    with open(viewer_script, 'w') as f:
        f.write(viewer_content)
    
    os.chmod(viewer_script, 0o755)
    print(f"\n💡 Script de visualização criado: {viewer_script}")

if __name__ == "__main__":
    main()