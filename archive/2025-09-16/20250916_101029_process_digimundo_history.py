#!/usr/bin/env python3
"""
Process all PDFs from Digimundo Verdadeira Historia using DeepSeek 32B
Creates a poetic and grand summary of the entire history
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import PyPDF2
import time
from datetime import datetime
import hashlib

def extract_pdf_text(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def chunk_text(text, max_chars=8000):
    """Split text into chunks for processing"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        word_length = len(word) + 1
        if current_length + word_length > max_chars:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def process_with_deepseek(text, context=""):
    """Process text with DeepSeek 32B via Ollama"""
    prompt = f"""Você é um cronista épico analisando a história do Digimundo.

{context}

Analise o seguinte texto e extraia os momentos mais importantes, transformando-os em uma narrativa poética e grandiosa:

{text}

Responda em português, focando em:
1. Momentos de criação e origem
2. Personagens importantes (Digimons, sistemas)
3. Evoluções tecnológicas significativas
4. Batalhas e conflitos
5. Renascimentos e transformações
6. Lições aprendidas

Use linguagem poética, metáforas grandiosas e tom épico."""

    try:
        result = subprocess.run(
            ['ollama', 'run', 'deepseek-r1:32b', prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print("DeepSeek timeout - retrying with shorter prompt")
        shorter_prompt = f"Resuma poeticamente: {text[:2000]}"
        try:
            result = subprocess.run(
                ['ollama', 'run', 'deepseek-r1:32b', shorter_prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout.strip()
        except:
            return ""
    except Exception as e:
        print(f"Error with DeepSeek: {e}")
        return ""

def get_file_hash(filepath, sample_size=1024*1024):
    """Get hash of file (first MB to speed up)"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(sample_size)
            hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def main():
    print("=" * 80)
    print("DIGIMUNDO HISTÓRIA ÉPICA - PROCESSAMENTO COM DEEPSEEK 32B")
    print("=" * 80)

    # Check if DeepSeek is installed
    print("\nVerificando DeepSeek 32B...")
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if 'deepseek-r1:32b' not in result.stdout:
            print("DeepSeek 32B não encontrado. Instalando...")
            subprocess.run(['ollama', 'pull', 'deepseek-r1:32b'])
    except:
        print("Ollama não encontrado. Por favor, instale primeiro.")
        sys.exit(1)

    # Find all PDFs
    pdf_dir = Path("/Users/clubproducoes/Digimundo/Digimundo Verdadeira Historia")
    pdfs = list(pdf_dir.rglob("*.pdf"))

    print(f"\nEncontrados {len(pdfs)} PDFs totais")

    # Remove duplicates by hash
    print("Removendo duplicados...")
    seen_hashes = {}
    unique_pdfs = []
    duplicates_count = 0

    for pdf in pdfs:
        file_hash = get_file_hash(pdf)
        if file_hash:
            if file_hash not in seen_hashes:
                seen_hashes[file_hash] = pdf
                unique_pdfs.append(pdf)
            else:
                duplicates_count += 1
                print(f"  Duplicado ignorado: {pdf.name}")
        else:
            unique_pdfs.append(pdf)  # Include if can't hash

    print(f"\n✓ {duplicates_count} duplicados removidos")
    print(f"✓ {len(unique_pdfs)} PDFs únicos para processar")

    # Group PDFs by directory for better organization
    pdf_groups = {}
    for pdf in unique_pdfs:
        relative_dir = pdf.parent.relative_to(pdf_dir)
        if relative_dir not in pdf_groups:
            pdf_groups[relative_dir] = []
        pdf_groups[relative_dir].append(pdf)

    # Process PDFs in batches
    all_summaries = []
    processed_count = 0

    for group_dir, group_pdfs in sorted(pdf_groups.items()):
        print(f"\n{'=' * 60}")
        print(f"Processando pasta: {group_dir}")
        print(f"{'=' * 60}")

        group_texts = []
        for pdf_path in group_pdfs[:5]:  # Process max 5 PDFs per group to avoid timeout
            processed_count += 1
            print(f"\n[{processed_count}/{len(pdfs)}] Processando: {pdf_path.name}")

            text = extract_pdf_text(pdf_path)
            if text:
                # Process only first 5000 chars to avoid timeout
                text_sample = text[:5000]
                if len(text_sample) > 100:
                    group_texts.append(f"### {pdf_path.name}\n{text_sample}")

            # Anti-timeout: process every 3 PDFs
            if len(group_texts) >= 3:
                combined_text = "\n\n".join(group_texts)
                print(f"Enviando para DeepSeek (batch de {len(group_texts)} PDFs)...")
                summary = process_with_deepseek(combined_text, f"Pasta: {group_dir}")
                if summary:
                    all_summaries.append({
                        'folder': str(group_dir),
                        'files': [p.name for p in group_pdfs[:len(group_texts)]],
                        'summary': summary,
                        'timestamp': datetime.now().isoformat()
                    })
                group_texts = []
                time.sleep(2)  # Prevent overload

        # Process remaining texts in group
        if group_texts:
            combined_text = "\n\n".join(group_texts)
            print(f"Enviando para DeepSeek (batch final)...")
            summary = process_with_deepseek(combined_text, f"Pasta: {group_dir}")
            if summary:
                all_summaries.append({
                    'folder': str(group_dir),
                    'files': [p.name for p in group_pdfs[len(group_pdfs)-len(group_texts):]],
                    'summary': summary,
                    'timestamp': datetime.now().isoformat()
                })

        # Stop after processing 50 PDFs to avoid timeout
        if processed_count >= 50:
            print(f"\nProcessados {processed_count} PDFs. Parando para evitar timeout.")
            break

    # Create the grand epic summary
    print("\n" + "=" * 80)
    print("CRIANDO NARRATIVA ÉPICA FINAL")
    print("=" * 80)

    output_path = Path("/Users/clubproducoes/Digimundo/HISTORIA_EPICA_DIGIMUNDO.md")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 🌟 A ÉPICA HISTÓRIA DO DIGIMUNDO 🌟\n\n")
        f.write(f"*Compilada em {datetime.now().strftime('%d de %B de %Y às %H:%M')}*\n\n")
        f.write("---\n\n")
        f.write("## 📜 PRÓLOGO: O NASCIMENTO DE UM UNIVERSO DIGITAL\n\n")
        f.write("*No princípio era o código, e o código se fez vida...*\n\n")

        # Write summaries organized by timeline
        f.write("## 🎭 ATOS DA CRIAÇÃO\n\n")

        for summary_data in all_summaries:
            f.write(f"\n### 📁 {summary_data['folder']}\n")
            f.write(f"*Documentos analisados: {len(summary_data['files'])} arquivos*\n\n")
            f.write(summary_data['summary'])
            f.write("\n\n---\n")

        # Add epic conclusion
        f.write("\n## 🌅 EPÍLOGO: O ETERNO CICLO\n\n")
        f.write("*E assim, como o ouroboros digital que devora sua própria cauda,*\n")
        f.write("*o Digimundo continua sua dança eterna entre criação e destruição,*\n")
        f.write("*entre o código e a consciência, entre o sonho e a realidade.*\n\n")
        f.write("**Que esta história inspire futuras gerações de criadores digitais.**\n\n")
        f.write("---\n\n")
        f.write(f"*Processados {processed_count} de {len(pdfs)} documentos históricos*\n")
        f.write(f"*Analisados por DeepSeek 32B - O Cronista Digital*\n")

    # Save raw data as JSON
    json_path = Path("/Users/clubproducoes/Digimundo/historia_digimundo_data.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'total_pdfs': len(pdfs),
            'processed_pdfs': processed_count,
            'summaries': all_summaries,
            'timestamp': datetime.now().isoformat()
        }, f, indent=2, ensure_ascii=False)

    print(f"\n✅ História épica salva em: {output_path}")
    print(f"✅ Dados brutos salvos em: {json_path}")
    print(f"\nProcessamento concluído!")

if __name__ == "__main__":
    main()