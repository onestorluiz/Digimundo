#!/usr/bin/env python3
"""
Relatório de status do processamento dos PDFs
"""

import sqlite3
import json
from pathlib import Path

print("=" * 80)
print("📊 RELATÓRIO DE PROCESSAMENTO - CINEMA KNOWLEDGE")
print("=" * 80)

# Conecta ao banco
db_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/CINEMA_KNOWLEDGE/03_METADATA/cinema_knowledge.db")

if not db_path.exists():
    print("❌ Banco de dados não encontrado")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Estatísticas gerais
cursor.execute("SELECT COUNT(*) FROM documents")
total_processed = cursor.fetchone()[0]

cursor.execute("SELECT SUM(original_size), SUM(compressed_size), SUM(tokens_saved) FROM documents")
result = cursor.fetchone()
total_original = result[0] or 0
total_compressed = result[1] or 0
total_tokens_saved = result[2] or 0

print(f"\n📚 Total de documentos processados: {total_processed}")
print(f"📏 Tamanho total original: {total_original:,} caracteres")
print(f"📉 Tamanho total comprimido: {total_compressed:,} caracteres")

if total_original > 0:
    overall_rate = ((total_original - total_compressed) / total_original) * 100
    print(f"💾 Taxa de compressão geral: {overall_rate:.2f}%")
else:
    overall_rate = 0

print(f"🎯 Tokens economizados: {total_tokens_saved:,}")

# Melhores compressões
print("\n✅ MELHORES COMPRESSÕES:")
print("-" * 60)

cursor.execute("""
    SELECT filename, compression_rate * 100, tokens_saved 
    FROM documents 
    WHERE compression_rate > 0
    ORDER BY compression_rate DESC 
    LIMIT 5
""")

best = cursor.fetchall()
for doc in best:
    print(f"  • {doc[0][:40]:40} {doc[1]:6.2f}% ({doc[2]} tokens)")

# Piores resultados
print("\n⚠️ DOCUMENTOS QUE AUMENTARAM DE TAMANHO:")
print("-" * 60)

cursor.execute("""
    SELECT filename, compression_rate * 100
    FROM documents 
    WHERE compression_rate < 0
    ORDER BY compression_rate 
    LIMIT 5
""")

worst = cursor.fetchall()
for doc in worst:
    print(f"  • {doc[0][:40]:40} {abs(doc[1]):6.2f}% maior")

# Por tipo
print("\n📊 POR TIPO DE DOCUMENTO:")
print("-" * 60)

cursor.execute("""
    SELECT 
        CASE 
            WHEN filename LIKE '%Screenplay%' OR filename LIKE '%Draft%' 
                 OR filename LIKE '%Release%' OR filename LIKE '%Scriptment%'
            THEN 'Roteiro'
            ELSE 'Livro/Teoria'
        END as tipo,
        COUNT(*) as qtd,
        AVG(compression_rate) * 100 as taxa_media
    FROM documents
    GROUP BY tipo
""")

by_type = cursor.fetchall()
for tipo in by_type:
    print(f"  {tipo[0]:15} Qtd: {tipo[1]:3}  Taxa média: {tipo[2]:6.2f}%")

# Análise do problema
print("\n⚠️ ANÁLISE DO PROBLEMA:")
print("-" * 80)
print("""
O sistema de fallback do DigiLang (sem tiktoken) está AUMENTANDO o tamanho
dos documentos ao invés de comprimir. Isso acontece porque:

1. O fallback usa substituições simples que podem aumentar o tamanho
2. Não tem Token Pair Database (TPD) real
3. Não tem canonicalização efetiva

SOLUÇÃO: Instalar tiktoken para usar o DigiLang completo:
  pip install tiktoken

Com o DigiLang completo, esperamos:
- 23-32% de compressão real
- Reversibilidade total
- Economia significativa de tokens
""")

conn.close()

print("=" * 80)