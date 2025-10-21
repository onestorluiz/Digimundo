#!/usr/bin/env python3
"""
🎬 FEED FULL SCREENPLAY - Sistema para alimentar roteiro completo ao Scripturemon
Resolve o problema de leitura parcial do Ollama
"""

import subprocess
import json
from pathlib import Path
import sys

class ScreenplayFeeder:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.screenplay_path = self.base_path / "roteiros" / "sonhos_sem_lembrancas.txt"
        self.model_name = "scripturemon-sdl"
        
    def load_screenplay(self) -> str:
        """Carrega o roteiro completo"""
        with open(self.screenplay_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def chunk_screenplay(self, text: str, chunk_size: int = 2000) -> list:
        """Divide o roteiro em chunks menores para processar"""
        lines = text.split('\n')
        chunks = []
        current_chunk = []
        current_size = 0
        
        for line in lines:
            current_chunk.append(line)
            current_size += len(line)
            
            if current_size >= chunk_size:
                chunks.append('\n'.join(current_chunk))
                current_chunk = []
                current_size = 0
        
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks
    
    def feed_to_ollama(self, text: str, context: str = "") -> str:
        """Alimenta texto ao Ollama com contexto"""
        prompt = f"""
CONTEXTO DO ROTEIRO COMPLETO:
{context}

ANÁLISE ESPECÍFICA:
{text}
"""
        
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Erro: {e}"
    
    def analyze_complete_screenplay(self, question: str):
        """Analisa o roteiro completo para responder uma pergunta"""
        print("📖 Carregando roteiro completo...")
        screenplay = self.load_screenplay()
        lines = screenplay.split('\n')
        
        print(f"✅ Roteiro carregado: {len(lines)} linhas")
        
        # Criar contexto resumido
        context = f"""
ROTEIRO: Sonhos Sem Lembranças
PROTAGONISTA: Samantha Turner / Elizabeth Chen
GÊNERO: Thriller Psicológico
TOTAL DE LINHAS: {len(lines)}

INÍCIO (linhas 1-50):
{chr(10).join(lines[:50])}

MEIO (linhas 250-300):
{chr(10).join(lines[250:300])}

FINAL (linhas 550-573):
{chr(10).join(lines[550:])}

LINHA 560 ESPECÍFICA: "{lines[559] if len(lines) > 559 else 'N/A'}"
"""
        
        # Criar prompt com a pergunta
        full_prompt = f"""
Como Scripturemon, analise profundamente o roteiro COMPLETO de Nestor:

{context}

PERGUNTA DO NESTOR: {question}

Responda com análise profunda e comparações com roteiros mestres.
Cite páginas e linhas ESPECÍFICAS do roteiro.
"""
        
        print("🤔 Processando com Scripturemon...")
        response = self.feed_to_ollama(full_prompt)
        
        return response
    
    def interactive_mode(self):
        """Modo interativo para perguntas sobre o roteiro"""
        print("="*60)
        print("🎬 SCRIPTUREMON - ANÁLISE COMPLETA DE ROTEIRO")
        print("="*60)
        print("Digite suas perguntas sobre 'Sonhos Sem Lembranças'")
        print("Digite 'sair' para terminar")
        print("="*60)
        
        while True:
            question = input("\n❓ Sua pergunta: ")
            
            if question.lower() == 'sair':
                break
            
            print("\n" + "="*60)
            response = self.analyze_complete_screenplay(question)
            print("\n💬 SCRIPTUREMON RESPONDE:")
            print(response)
            print("="*60)

def main():
    feeder = ScreenplayFeeder()
    
    if len(sys.argv) > 1:
        # Modo direto com pergunta
        question = " ".join(sys.argv[1:])
        response = feeder.analyze_complete_screenplay(question)
        print(response)
    else:
        # Modo interativo
        feeder.interactive_mode()

if __name__ == "__main__":
    main()