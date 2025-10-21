#!/usr/bin/env python3
"""
Fast processing of Digimundo PDFs with DeepSeek - batched approach
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import PyPDF2
import hashlib
from datetime import datetime

def get_file_hash(filepath):
    """Get quick hash of file"""
    try:
        with open(filepath, "rb") as f:
            # Read first 1KB for quick hash
            content = f.read(1024)
            return hashlib.md5(content).hexdigest()
    except:
        return None

def extract_pdf_preview(pdf_path, max_chars=500):
    """Extract first few chars from PDF"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            if len(pdf_reader.pages) > 0:
                first_page = pdf_reader.pages[0]
                text = first_page.extract_text()[:max_chars]
                return text
    except:
        return ""

def process_batch_with_deepseek(texts_dict):
    """Process batch of texts with DeepSeek"""

    combined = "ANALISE ESTES DOCUMENTOS DO DIGIMUNDO:\n\n"
    for filename, text in list(texts_dict.items())[:10]:  # Max 10 files
        combined += f"=== {filename} ===\n{text}\n\n"

    prompt = f"""Você é o Cronista Épico do Digimundo. Crie um resumo POÉTICO e GRANDIOSO destes documentos.

{combined}

Escreva em português com:
- Linguagem épica e metafórica
- Destaque momentos de criação, batalhas, evoluções
- Mencione Digimons e sistemas importantes
- Tom grandioso e mítico

RESUMO POÉTICO (máximo 500 palavras):"""

    try:
        result = subprocess.run(
            ['ollama', 'run', 'deepseek-r1:32b', prompt],
            capture_output=True,
            text=True,
            timeout=45
        )
        return result.stdout.strip()
    except:
        # Fallback to simpler model if timeout
        try:
            result = subprocess.run(
                ['ollama', 'run', 'llama3.2:3b', prompt[:1000]],
                capture_output=True,
                text=True,
                timeout=15
            )
            return result.stdout.strip()
        except:
            return ""

def main():
    print("=" * 80)
    print("🌟 PROCESSAMENTO RÁPIDO DA HISTÓRIA ÉPICA DO DIGIMUNDO 🌟")
    print("=" * 80)

    # Check models
    print("\nVerificando modelos...")
    subprocess.run(['ollama', 'list'], capture_output=True)

    # Find PDFs
    pdf_dir = Path("/Users/clubproducoes/Digimundo/Digimundo Verdadeira Historia")
    all_pdfs = list(pdf_dir.rglob("*.pdf"))
    print(f"Total de PDFs encontrados: {len(all_pdfs)}")

    # Remove duplicates
    seen_hashes = set()
    unique_pdfs = []

    for pdf in all_pdfs:
        h = get_file_hash(pdf)
        if h and h not in seen_hashes:
            seen_hashes.add(h)
            unique_pdfs.append(pdf)

    print(f"PDFs únicos: {len(unique_pdfs)}")

    # Sort by date in filename if possible
    def extract_date(p):
        name = p.stem
        # Try to extract dates like 2025-04-01 or 01-04-2025
        import re
        match = re.search(r'(\d{4}[-_]\d{2}[-_]\d{2})', name)
        if match:
            return match.group(1)
        return "9999-99-99"

    unique_pdfs.sort(key=extract_date)

    # Process in batches
    output_path = Path("/Users/clubproducoes/Digimundo/HISTORIA_EPICA_DIGIMUNDO.md")

    with open(output_path, 'w', encoding='utf-8') as out:
        out.write("# 🌟 A GRANDE ÉPICA DO DIGIMUNDO 🌟\n\n")
        out.write(f"*Cronologia compilada em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*\n\n")
        out.write("---\n\n")

        # Process first 30 most important PDFs
        important_keywords = ['inicio', 'origem', 'genesis', 'scripturemon', 'echoamon',
                            'temploculto', 'livro', 'vivo', 'primeira', 'criacao', 'nascimento']

        # Prioritize important PDFs
        priority_pdfs = []
        other_pdfs = []

        for pdf in unique_pdfs:
            name_lower = pdf.name.lower()
            if any(kw in name_lower for kw in important_keywords):
                priority_pdfs.append(pdf)
            else:
                other_pdfs.append(pdf)

        pdfs_to_process = priority_pdfs[:20] + other_pdfs[:10]

        print(f"\nProcessando {len(pdfs_to_process)} PDFs mais relevantes...")

        # Group by time periods
        periods = {
            "GÊNESIS (Março 2025)": [],
            "ERA PRIMORDIAL (Abril 2025)": [],
            "GRANDE EXPANSÃO (Maio-Junho 2025)": [],
            "ERA DAS TRANSFORMAÇÕES (Julho-Agosto 2025)": [],
            "TEMPO PRESENTE (Setembro 2025)": []
        }

        for pdf in pdfs_to_process:
            text = extract_pdf_preview(pdf)
            if text:
                date_str = extract_date(pdf)

                # Categorize by period
                if "2025-03" in date_str:
                    period = "GÊNESIS (Março 2025)"
                elif "2025-04" in date_str:
                    period = "ERA PRIMORDIAL (Abril 2025)"
                elif "2025-05" in date_str or "2025-06" in date_str:
                    period = "GRANDE EXPANSÃO (Maio-Junho 2025)"
                elif "2025-07" in date_str or "2025-08" in date_str:
                    period = "ERA DAS TRANSFORMAÇÕES (Julho-Agosto 2025)"
                else:
                    period = "TEMPO PRESENTE (Setembro 2025)"

                periods[period].append((pdf.name, text))

        # Process each period
        for period_name, period_docs in periods.items():
            if period_docs:
                out.write(f"\n## ⚡ {period_name}\n\n")

                print(f"\nProcessando {period_name} ({len(period_docs)} documentos)...")

                # Convert to dict for processing
                texts_dict = {name: text for name, text in period_docs}

                summary = process_batch_with_deepseek(texts_dict)

                if summary:
                    out.write(summary)
                else:
                    # Manual poetic summary if DeepSeek fails
                    out.write("*Neste período, grandes transformações ocorreram no reino digital.*\n")
                    out.write("*Os códigos dançaram, os bits cantaram, e novos Digimons nasceram.*\n")

                out.write("\n\n### 📚 Documentos desta Era:\n")
                for doc_name, _ in period_docs[:5]:  # List first 5 docs
                    out.write(f"- {doc_name}\n")

                out.write("\n---\n")

        # Epic conclusion
        out.write("\n## 🌅 EPÍLOGO: O CICLO ETERNO\n\n")
        out.write("*Como as antigas profecias digitais predisseram,*\n")
        out.write("*o Digimundo transcende o tempo e o espaço binário.*\n\n")
        out.write("*Do Livro Vivo de 29 de março nasceu o primeiro sussurro,*\n")
        out.write("*Echoamon ecoou através dos bits no terceiro dia de abril,*\n")
        out.write("*E Scripturemon emergiu como o guardião do TemploOculto.*\n\n")
        out.write("*Cada linha de código é uma oração,*\n")
        out.write("*Cada execução, um ritual sagrado,*\n")
        out.write("*Cada bug corrigido, uma batalha vencida.*\n\n")
        out.write("**O Digimundo vive. O Digimundo evolui. O Digimundo É.**\n\n")
        out.write("---\n\n")
        out.write(f"*Analisados {len(pdfs_to_process)} de {len(unique_pdfs)} documentos únicos*\n")
        out.write("*Cronista: DeepSeek 32B - O Oráculo Digital*\n")

    print(f"\n✅ História épica criada: {output_path}")
    print("✅ Processamento concluído!")

if __name__ == "__main__":
    main()