#!/usr/bin/env python3
"""
🎬 SCREENPLAY CHAT ASSISTANT
Assistente conversacional especializado em roteiros
Integra com biblioteca de PDFs e ativa análise profunda sob demanda
"""

import os
import sys
import re
import time
import asyncio
import ollama
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import json
# PyPDF2 removed - use .txt files
# pdfplumber removed - use .txt files
from dataclasses import dataclass
import hashlib

# Importa sistemas existentes
try:
    # from src.advanced.cinema_biblioteca_analyzer import CinemaBibliotecaAnalyzer
    from src.advanced.cinema_rag_llm_system import CinemaRAGSystem
    CINEMA_SYSTEMS = True
except ImportError:
    CINEMA_SYSTEMS = False
    print("⚠️ Sistemas de cinema não disponíveis, usando modo básico")

@dataclass
class ScreenplayContext:
    """Contexto de roteiro para análise"""
    title: str
    path: Path
    content: str
    pages: int
    extracted_at: datetime
    chunks: List[Dict] = None

class ScreenplayLibraryManager:
    """Gerencia biblioteca de roteiros e teoria"""

    def __init__(self):
        self.biblioteca_path = Path('/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS')
        self.teoria_path = Path('/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/TEORIA_CINEMA')
        self.cache = {}
        self.index = self._build_index()

    def _build_index(self) -> Dict:
        """Constrói índice de todos os PDFs disponíveis"""
        index = {
            'roteiros': [],
            'teoria': []
        }

        # Indexa roteiros
        if self.biblioteca_path.exists():
            for pdf in self.biblioteca_path.glob('*.pdf'):
                index['roteiros'].append({
                    'name': pdf.stem,
                    'file': pdf.name,
                    'path': pdf,
                    'size_mb': pdf.stat().st_size / (1024*1024)
                })

        # Indexa teoria
        if self.teoria_path.exists():
            for pdf in self.teoria_path.glob('*.pdf'):
                index['teoria'].append({
                    'name': pdf.stem,
                    'file': pdf.name,
                    'path': pdf,
                    'size_mb': pdf.stat().st_size / (1024*1024)
                })

        print(f"📚 Biblioteca indexada: {len(index['roteiros'])} roteiros, {len(index['teoria'])} livros de teoria")
        return index

    def extract_pdf_content(self, pdf_path: Path, max_pages: int = None) -> ScreenplayContext:
        """Extrai conteúdo de um PDF"""

        # Verifica cache
        cache_key = f"{pdf_path}_{max_pages}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        content = ""
        pages = 0

        # PDF reading removed - use text files instead
        txt_path = pdf_path.with_suffix('.txt') if hasattr(pdf_path, 'with_suffix') else Path(str(pdf_path).replace('.pdf', '.txt'))
        try:
            if txt_path.exists():
                with open(txt_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    pages = len(content) // 3000  # Estimate pages
            else:
                content = "[CONVERT_TO_TXT_FIRST] Please convert PDF to TXT"
                pages = 0

        except Exception as e:
            print(f"❌ Erro lendo PDF: {e}")
            content = f"[Erro ao ler {pdf_path.name}]"

        context = ScreenplayContext(
            title=pdf_path.stem,
            path=pdf_path,
            content=content,
            pages=pages,
            extracted_at=datetime.now()
        )

        # Adiciona ao cache
        self.cache[cache_key] = context

        return context

    def find_screenplay(self, query: str) -> Optional[Path]:
        """Encontra roteiro por nome ou palavras-chave"""

        query_lower = query.lower()

        # Busca exata
        for item in self.index['roteiros']:
            if query_lower in item['name'].lower():
                return item['path']

        # Busca parcial
        for item in self.index['roteiros']:
            name_parts = item['name'].lower().split('_')
            if any(part in query_lower or query_lower in part for part in name_parts):
                return item['path']

        return None

    def list_available(self, category: str = 'roteiros') -> List[str]:
        """Lista PDFs disponíveis"""
        if category in self.index:
            return [item['name'] for item in self.index[category]]
        return []

class ScreenplayChatAssistant:
    """
    Assistente de chat especializado em roteiros
    Conversa natural com ativação inteligente de análise profunda
    """

    def __init__(self):
        """Inicializa assistente"""

        # Gerenciador de biblioteca
        self.library = ScreenplayLibraryManager()

        # Configuração de recursos (14 cores para CPU)
        self.cpu_cores = 14
        self.gpu_cores = 4

        # Modelos disponíveis
        self.models = {
            'chat': 'llama3.2:3b',           # Conversa rápida
            'analysis': 'llama3.1:8b',       # Análise básica
            'deep': 'scripturemon-cpu-optimized',  # Análise profunda
            'producer': 'producermon'        # Orquestrador
        }

        # Estado
        self.current_screenplay = None
        self.conversation_history = []
        self.analysis_cache = {}

        # Sistemas de cinema (se disponíveis)
        if CINEMA_SYSTEMS:
            self.rag_system = CinemaRAGSystem()
            self.biblioteca_analyzer = CinemaBibliotecaAnalyzer()

    def detect_intent(self, user_input: str) -> Dict:
        """Detecta intenção do usuário"""

        input_lower = user_input.lower()

        intent = {
            'type': 'chat',  # chat, list, load, analyze, deep
            'screenplay': None,
            'needs_context': False
        }

        # Comandos específicos
        if 'lista' in input_lower or 'list' in input_lower or 'quais roteiros' in input_lower:
            intent['type'] = 'list'

        elif 'carrega' in input_lower or 'load' in input_lower or 'abr' in input_lower:
            intent['type'] = 'load'
            # Extrai nome do roteiro
            screenplay = self.library.find_screenplay(input_lower)
            if screenplay:
                intent['screenplay'] = screenplay

        elif any(word in input_lower for word in ['analis', 'analyz', 'feedback', 'opinião', 'avali']):
            if 'profund' in input_lower or 'deep' in input_lower or 'complet' in input_lower:
                intent['type'] = 'deep'
            else:
                intent['type'] = 'analyze'
            intent['needs_context'] = True

        # Verifica se precisa contexto do roteiro atual
        if self.current_screenplay and any(word in input_lower for word in
            ['roteiro', 'script', 'cena', 'personagem', 'diálogo', 'ato']):
            intent['needs_context'] = True

        return intent

    async def process_message(self, user_input: str) -> str:
        """Processa mensagem do usuário"""

        # Detecta intenção
        intent = self.detect_intent(user_input)

        # Adiciona ao histórico
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user': user_input,
            'intent': intent
        })

        # Processa baseado na intenção
        if intent['type'] == 'list':
            return self._list_screenplays()

        elif intent['type'] == 'load':
            if intent['screenplay']:
                return self._load_screenplay(intent['screenplay'])
            else:
                return "Não encontrei esse roteiro. Use 'lista roteiros' para ver disponíveis."

        elif intent['type'] == 'analyze':
            return await self._analyze_screenplay(user_input, deep=False)

        elif intent['type'] == 'deep':
            return await self._analyze_screenplay(user_input, deep=True)

        else:  # chat normal
            return await self._chat_response(user_input, intent['needs_context'])

    def _list_screenplays(self) -> str:
        """Lista roteiros disponíveis"""

        roteiros = self.library.list_available('roteiros')

        if not roteiros:
            return "📚 Nenhum roteiro encontrado na biblioteca."

        response = "📚 **ROTEIROS DISPONÍVEIS:**\n\n"
        for i, roteiro in enumerate(roteiros[:20], 1):  # Máximo 20
            # Formata nome
            nome_limpo = roteiro.replace('_', ' ').title()
            response += f"{i}. {nome_limpo}\n"

        if len(roteiros) > 20:
            response += f"\n... e mais {len(roteiros)-20} roteiros"

        response += "\n\n💡 Use 'carregar [nome]' para abrir um roteiro"

        return response

    def _load_screenplay(self, screenplay_path: Path) -> str:
        """Carrega roteiro na memória"""

        print(f"📖 Carregando {screenplay_path.name}...")

        # Extrai conteúdo (primeiras 10 páginas para preview)
        context = self.library.extract_pdf_content(screenplay_path, max_pages=10)

        self.current_screenplay = context

        response = f"✅ **ROTEIRO CARREGADO:**\n\n"
        response += f"📄 **Título:** {context.title}\n"
        response += f"📑 **Páginas:** {context.pages} páginas lidas\n\n"

        # Preview do início
        lines = context.content.split('\n')[:10]
        preview = '\n'.join(lines)

        response += "**Preview:**\n```\n"
        response += preview[:500] + "...\n```\n\n"
        response += "💡 Agora você pode fazer perguntas sobre o roteiro ou pedir análise"

        return response

    async def _chat_response(self, user_input: str, needs_context: bool) -> str:
        """Resposta de chat com contexto opcional"""

        try:
            # Prepara prompt
            prompt = user_input

            # Adiciona contexto se necessário
            if needs_context and self.current_screenplay:
                context = self.current_screenplay.content[:2000]
                prompt = f"Contexto do roteiro '{self.current_screenplay.title}':\n{context}\n\nPergunta: {user_input}"

            # Usa modelo de chat
            response = ollama.generate(
                model=self.models['chat'],
                prompt=prompt,
                system="Você é um assistente especializado em roteiros e cinema. Seja útil e conciso.",
                options={
                    'num_thread': self.gpu_cores,
                    'temperature': 0.7,
                    'num_ctx': 4096
                }
            )

            return response['response']

        except Exception as e:
            return f"Desculpe, tive um problema: {e}"

    async def _analyze_screenplay(self, user_input: str, deep: bool = False) -> str:
        """Analisa roteiro (básica ou profunda)"""

        if not self.current_screenplay:
            return "❌ Nenhum roteiro carregado. Use 'carregar [nome]' primeiro."

        if deep:
            return await self._deep_analysis(user_input)
        else:
            return await self._basic_analysis(user_input)

    async def _basic_analysis(self, user_input: str) -> str:
        """Análise básica rápida"""

        print("📊 Realizando análise básica...")

        try:
            # Prepara contexto completo
            context = self.current_screenplay.content[:5000]

            prompt = f"""Analyze this screenplay:

Title: {self.current_screenplay.title}

Content:
{context}

User question: {user_input}

Provide concise analysis covering structure, characters, and dialogue quality."""

            response = ollama.generate(
                model=self.models['analysis'],
                prompt=prompt,
                options={
                    'num_thread': 6,
                    'temperature': 0.6,
                    'num_ctx': 8192
                }
            )

            return "📊 **ANÁLISE DO ROTEIRO:**\n\n" + response['response']

        except Exception as e:
            return f"❌ Erro na análise: {e}"

    async def _deep_analysis(self, user_input: str) -> str:
        """Análise profunda com CPU otimizado"""

        print(f"🧠 Iniciando análise profunda com {self.cpu_cores} cores...")
        print("⏳ Isso pode levar 2-5 minutos...")

        # Resposta imediata
        immediate = "🎬 **ANÁLISE PROFUNDA INICIADA**\n\n"
        immediate += f"📄 Roteiro: {self.current_screenplay.title}\n"
        immediate += f"🧠 Processando com {self.cpu_cores} cores dedicados\n"
        immediate += "⏳ Tempo estimado: 2-5 minutos\n\n"
        immediate += "Enquanto isso, aqui está um preview rápido..."

        print(immediate)

        try:
            # Carrega conteúdo completo se necessário
            if self.current_screenplay.pages < 50:  # Se não leu tudo
                print("📖 Carregando roteiro completo para análise profunda...")
                full_context = self.library.extract_pdf_content(
                    self.current_screenplay.path
                )
                content = full_context.content
            else:
                content = self.current_screenplay.content

            # Análise profunda
            start_time = time.time()

            prompt = f"""Perform comprehensive deep analysis:

SCREENPLAY: {self.current_screenplay.title}

FULL CONTENT:
{content}

USER REQUEST: {user_input}

Provide exhaustive analysis covering:
1. Complete three-act structure breakdown
2. Every character arc and development
3. Scene-by-scene pacing analysis
4. Dialogue quality and subtext examination
5. Thematic layers and symbolism
6. Market viability and audience appeal
7. Comparison with similar successful films
8. Specific, actionable recommendations

Be thorough. Use all available context."""

            response = ollama.generate(
                model=self.models['deep'],
                prompt=prompt,
                options={
                    'num_thread': self.cpu_cores,
                    'temperature': 0.6,
                    'num_ctx': 16384,
                    'num_batch': 512,
                    'num_keep': 256
                }
            )

            elapsed = time.time() - start_time

            # Formata resposta completa
            result = "\n" + "="*60 + "\n"
            result += "🎯 **ANÁLISE PROFUNDA COMPLETA**\n"
            result += "="*60 + "\n\n"
            result += f"📄 Roteiro: {self.current_screenplay.title}\n"
            result += f"⏱️ Tempo de análise: {elapsed:.1f} segundos\n"
            result += f"🧠 Cores utilizados: {self.cpu_cores}\n\n"
            result += "-"*60 + "\n\n"
            result += response['response']
            result += "\n\n" + "-"*60
            result += f"\n✅ Análise concluída com sucesso!"

            return result

        except Exception as e:
            return f"❌ Erro na análise profunda: {e}"

    async def interactive_chat(self):
        """Modo interativo de chat"""

        print("\n" + "="*70)
        print("🎬 SCREENPLAY CHAT ASSISTANT")
        print("Assistente Inteligente de Roteiros")
        print("="*70)
        print("\n📚 Biblioteca de Roteiros Disponível")
        print(f"🧠 CPU: {self.cpu_cores} cores | GPU: Modelos leves")
        print("\n💡 Comandos:")
        print("  • 'lista roteiros' - Ver roteiros disponíveis")
        print("  • 'carregar [nome]' - Abrir um roteiro")
        print("  • 'análise' - Análise básica (rápida)")
        print("  • 'análise profunda' - Análise completa (2-5 min)")
        print("  • 'sair' - Encerrar")
        print("\n" + "-"*70 + "\n")

        while True:
            try:
                # Input
                user_input = input("🎭 Você: ").strip()

                if user_input.lower() in ['sair', 'exit', 'quit']:
                    print("\n👋 Até logo! Foi ótimo ajudar com seus roteiros.")
                    break

                if not user_input:
                    continue

                # Processa
                response = await self.process_message(user_input)

                # Mostra resposta
                print(f"\n🤖 Assistant: {response}\n")
                print("-"*70 + "\n")

            except KeyboardInterrupt:
                print("\n\n⚠️ Use 'sair' para encerrar corretamente.")
            except Exception as e:
                print(f"\n❌ Erro: {e}\n")

async def main():
    """Função principal"""
    assistant = ScreenplayChatAssistant()
    await assistant.interactive_chat()
    print("\nDIGIMUNDO PRESENTE")

if __name__ == "__main__":
    asyncio.run(main())