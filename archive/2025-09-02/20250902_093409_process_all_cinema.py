#!/usr/bin/env python3
"""
Script para processar todos os PDFs de cinema automaticamente
"""

from CINEMA_KNOWLEDGE_PROCESSOR import CinemaKnowledgeProcessor

print("🎬 PROCESSAMENTO AUTOMÁTICO DE TODOS OS PDFS")
print("=" * 80)

processor = CinemaKnowledgeProcessor()

# Processa todos os PDFs
results = processor.process_all_pdfs()

print("\n" + "=" * 80)
print("✅ PROCESSAMENTO COMPLETO!")
print("=" * 80)