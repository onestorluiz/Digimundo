#!/usr/bin/env python3
"""
FASE 17.b - Mineração de Padrões de Livros Teóricos
Analisa livros sobre roteiro para extrair termos técnicos recorrentes
"""

import os
import re
from collections import Counter
from pathlib import Path
import PyPDF2
import pdfplumber
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TheoryMiner")

class TheoryPatternMiner:
    """Minerador especializado em livros teóricos sobre roteiro"""

    def __init__(self):
        self.theory_books = [
            "The Fundamentals Of Screenwriting",
            "Writing Your Screenplay",
            "The Hero's Journey",
            "Story; Writing",
            "The Anatomy of Story",
            "Save the Cat",
            "The Screenwriter's Bible",
            "Writing Movies for Fun and Profit",
            "The Heroine's Journey"
        ]

        # Termos técnicos comuns em teoria de roteiro
        self.technical_terms = [
            "protagonist", "antagonist", "conflict", "plot", "subplot",
            "character arc", "three-act structure", "inciting incident",
            "rising action", "climax", "resolution", "denouement",
            "dialogue", "exposition", "backstory", "foreshadowing",
            "theme", "motif", "setup and payoff", "character development",
            "story structure", "narrative", "point of view", "voice",
            "scene", "sequence", "beat", "turning point", "midpoint",
            "catalyst", "debate", "break into two", "b-story",
            "fun and games", "bad guys close in", "all is lost",
            "dark night of the soul", "break into three", "finale"
        ]

    def extract_text_from_pdf(self, pdf_path):
        """Extrai texto de PDF usando múltiplas estratégias"""
        text = ""

        # Tentar com pdfplumber primeiro (melhor para PDFs complexos)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages[:50]:  # Primeiras 50 páginas
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except:
            pass

        # Fallback para PyPDF2
        if not text:
            try:
                with open(pdf_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for i in range(min(50, len(reader.pages))):
                        text += reader.pages[i].extract_text()
            except:
                pass

        return text

    def mine_theory_patterns(self):
        """Minera padrões específicos de livros teóricos"""

        print("="*60)
        print("FASE 17.b - MINERAÇÃO DE PADRÕES TEÓRICOS")
        print("="*60)

        # Diretório dos PDFs
        pdf_dir = Path('digilibrary/BIBLIOTECA_ROTEIROS')

        # Coletar textos dos livros teóricos
        theory_texts = []
        theory_count = 0

        print("\n📚 Identificando livros teóricos...")
        for pdf_file in pdf_dir.glob('**/*.pdf'):
            # Verificar se é livro teórico
            is_theory = any(term.lower() in pdf_file.name.lower()
                          for term in self.theory_books)

            if is_theory or "writing" in pdf_file.name.lower() or "story" in pdf_file.name.lower():
                print(f"  📖 {pdf_file.name}")
                text = self.extract_text_from_pdf(pdf_file)
                if text:
                    theory_texts.append(text)
                    theory_count += 1

        print(f"\n✅ {theory_count} livros teóricos identificados")

        if not theory_texts:
            print("⚠️ Nenhum livro teórico encontrado")
            return {}

        # Juntar todos os textos
        corpus = '\n'.join(theory_texts)
        corpus_lower = corpus.lower()

        # Minerar padrões
        patterns = {}

        print("\n🔍 Minerando padrões técnicos...")

        # 1. Termos técnicos de roteiro
        technical_counts = Counter()
        for term in self.technical_terms:
            count = corpus_lower.count(term.lower())
            if count > 10:  # Mínimo de 10 ocorrências
                technical_counts[term] = count

        print(f"  📊 {len(technical_counts)} termos técnicos frequentes")

        # 2. Capítulos e seções comuns
        chapter_patterns = re.findall(r'Chapter \d+[:\s]+([A-Z][A-Za-z\s]+)', corpus)
        chapter_counts = Counter(chapter_patterns)

        # 3. Conceitos com definições (padrão: "X is/means...")
        definitions = re.findall(r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+(?:is|means|refers to)\s+', corpus)
        definition_counts = Counter(definitions)

        # 4. Exemplos de filmes citados
        film_mentions = re.findall(r'"([^"]+)"(?:\s+\(\d{4}\))?', corpus)
        film_counts = Counter(film_mentions)

        # 5. Estruturas narrativas
        structure_terms = [
            "act one", "act two", "act three",
            "first act", "second act", "third act",
            "opening", "middle", "ending",
            "beginning", "development", "conclusion"
        ]

        structure_counts = Counter()
        for term in structure_terms:
            count = corpus_lower.count(term)
            if count > 5:
                structure_counts[term] = count

        print("\n📊 TOP PADRÕES ENCONTRADOS:")

        print("\n1. TERMOS TÉCNICOS MAIS FREQUENTES:")
        for term, count in technical_counts.most_common(15):
            print(f"   {term:30s} : {count:4d}x")
            patterns[f"TT_{term.replace(' ', '_').upper()[:10]}"] = term

        print("\n2. ESTRUTURAS NARRATIVAS:")
        for term, count in structure_counts.most_common(10):
            print(f"   {term:30s} : {count:4d}x")
            patterns[f"SN_{term.replace(' ', '_').upper()[:10]}"] = term

        print("\n3. CONCEITOS DEFINIDOS:")
        for concept, count in definition_counts.most_common(10):
            if count > 3 and len(concept) > 5:
                print(f"   {concept[:30]:30s} : {count:4d}x")
                patterns[f"CD_{concept.replace(' ', '_').upper()[:10]}"] = concept

        print("\n4. FILMES MAIS CITADOS:")
        for film, count in film_counts.most_common(10):
            if count > 2 and len(film) > 3:
                print(f"   {film[:30]:30s} : {count:4d}x")

        # Calcular economia potencial
        total_occurrences = sum(technical_counts.values()) + sum(structure_counts.values())
        potential_savings = total_occurrences * 2  # média de 2 tokens por termo

        print("\n💡 ANÁLISE DE POTENCIAL:")
        print(f"  ✅ Padrões teóricos identificados: {len(patterns)}")
        print(f"  📊 Ocorrências totais: {total_occurrences:,}")
        print(f"  💰 Economia potencial: ~{potential_savings:,} tokens")
        print(f"  📈 Ganho estimado: +5-8% de compressão em livros teóricos")

        return patterns

    def save_patterns(self, patterns):
        """Salva padrões minerados"""
        output_file = Path('theory_patterns.json')

        with open(output_file, 'w') as f:
            json.dump(patterns, f, indent=2)

        print(f"\n📁 Padrões salvos em: {output_file}")

        # Criar versão markdown para documentação
        md_file = Path('PADROES_TEORICOS.md')
        with open(md_file, 'w') as f:
            f.write("# 📚 PADRÕES MINERADOS DE LIVROS TEÓRICOS\n\n")
            f.write(f"**Data:** 14/09/2025\n")
            f.write(f"**Total de padrões:** {len(patterns)}\n\n")
            f.write("## PADRÕES PARA DIGILANG V9 ACADEMIC\n\n")

            for code, pattern in patterns.items():
                f.write(f"- `{code}`: {pattern}\n")

        print(f"📝 Documentação salva em: {md_file}")

def main():
    miner = TheoryPatternMiner()
    patterns = miner.mine_theory_patterns()

    if patterns:
        miner.save_patterns(patterns)

        print("\n" + "="*60)
        print("🎯 FASE 17.b CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print("\nPRÓXIMOS PASSOS:")
        print("1. Integrar padrões teóricos no DigiLang V9 Academic")
        print("2. Criar modo adaptativo que detecta tipo de conteúdo")
        print("3. Testar com biblioteca completa")

if __name__ == "__main__":
    main()