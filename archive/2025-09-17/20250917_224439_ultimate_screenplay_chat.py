#!/usr/bin/env python3
"""
🎬 ULTIMATE SCREENPLAY CHAT - MÁXIMO TOKENS
Chat definitivo com configuração de máximo contexto
Mac Studio M3 Ultra - 96GB RAM - Usa TODO o potencial
"""

import os
import sys
import time
import asyncio
import ollama
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import PyPDF2
import pdfplumber

# Importa configuração de máximo tokens
from ollama_max_config import OllamaMaxTokenConfig

class UltimateScreenplayChat:
    """
    Chat definitivo com máximo de tokens configurado
    Usa toda a capacidade da máquina (96GB RAM)
    """

    def __init__(self):
        """Inicializa com configurações máximas"""

        print("🚀 INICIALIZANDO ULTIMATE SCREENPLAY CHAT")
        print("="*60)

        # Configurador de tokens
        self.token_config = OllamaMaxTokenConfig()

        # Verifica RAM
        ram_info = self.token_config.check_ram_availability()
        print(f"💾 RAM: {ram_info['available_gb']:.1f}GB disponível de {ram_info['total_gb']:.1f}GB")

        # Caminhos
        self.biblioteca_path = Path('/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS')
        self.teoria_path = Path('/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/TEORIA_CINEMA')

        # Estado
        self.current_screenplay = None
        self.conversation_history = []
        self.full_context_mode = False  # Modo contexto completo

        # Modelos recomendados por tarefa
        self.models_by_task = {
            'chat': self.token_config.recommend_models('conversation'),
            'analysis': self.token_config.recommend_models('analysis'),
            'deep': self.token_config.recommend_models('deep_analysis'),
            'orchestration': self.token_config.recommend_models('orchestration')
        }

        print("\n📊 CONFIGURAÇÃO DE MODELOS:")
        for task, config in self.models_by_task.items():
            print(f"  {task}: {config['primary']} ({config['max_tokens']} tokens)")

        print("\n✅ Sistema pronto com MÁXIMO de tokens!")
        print("="*60)

    async def chat(self, user_input: str) -> str:
        """Processa entrada com máximo de contexto"""

        # Detecta tipo de requisição
        input_lower = user_input.lower()

        # Comandos especiais
        if 'contexto completo' in input_lower or 'full context' in input_lower:
            return await self._enable_full_context()

        elif 'carregar' in input_lower or 'load' in input_lower:
            return await self._load_screenplay_full(user_input)

        elif 'análise profunda' in input_lower or 'deep analysis' in input_lower:
            return await self._deep_analysis_max_tokens(user_input)

        elif 'análise' in input_lower or 'feedback' in input_lower:
            return await self._analysis_with_context(user_input)

        else:
            # Conversa normal com contexto otimizado
            return await self._chat_response(user_input)

    async def _enable_full_context(self) -> str:
        """Ativa modo de contexto completo"""

        self.full_context_mode = True

        response = "🚀 **MODO CONTEXTO COMPLETO ATIVADO**\n\n"
        response += "Configurações máximas:\n"

        for task, config in self.models_by_task.items():
            model_config = self.token_config.get_config(config['primary'])
            response += f"• {task}: {model_config.max_tokens:,} tokens\n"

        response += f"\n💾 RAM disponível: {self.token_config.check_ram_availability()['available_gb']:.1f}GB"
        response += "\n\n⚡ Posso processar roteiros completos de 120+ páginas!"

        return response

    async def _load_screenplay_full(self, user_input: str) -> str:
        """Carrega roteiro COMPLETO na memória"""

        print("📖 Carregando roteiro completo...")

        # Encontra PDF mencionado
        pdfs = list(self.biblioteca_path.glob('*.pdf'))

        for pdf in pdfs:
            if pdf.stem.lower() in user_input.lower():
                return await self._load_pdf_complete(pdf)

        # Lista disponíveis se não encontrou
        if pdfs:
            response = "📚 Roteiros disponíveis:\n"
            for i, pdf in enumerate(pdfs[:10], 1):
                response += f"{i}. {pdf.stem}\n"
            return response
        else:
            return "❌ Nenhum roteiro encontrado na biblioteca"

    async def _load_pdf_complete(self, pdf_path: Path) -> str:
        """Carrega PDF completo usando máximo de memória"""

        start_time = time.time()
        content = ""
        pages = 0

        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                print(f"📄 Processando {total_pages} páginas...")

                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        content += text + "\n"
                        pages += 1

                    # Mostra progresso
                    if pages % 10 == 0:
                        print(f"  Processadas {pages}/{total_pages} páginas...")

        except Exception as e:
            return f"❌ Erro lendo PDF: {e}"

        # Salva contexto
        self.current_screenplay = {
            'title': pdf_path.stem,
            'content': content,
            'pages': pages,
            'characters': len(content),
            'tokens_estimate': len(content.split())
        }

        elapsed = time.time() - start_time

        response = "✅ **ROTEIRO CARREGADO COMPLETAMENTE**\n\n"
        response += f"📄 **Título:** {self.current_screenplay['title']}\n"
        response += f"📑 **Páginas:** {pages}\n"
        response += f"📊 **Caracteres:** {self.current_screenplay['characters']:,}\n"
        response += f"🔤 **Tokens estimados:** {self.current_screenplay['tokens_estimate']:,}\n"
        response += f"⏱️ **Tempo de carga:** {elapsed:.1f}s\n\n"

        # Preview
        lines = content.split('\n')[:20]
        preview = '\n'.join(lines)
        response += "**Preview:**\n```\n" + preview[:500] + "...\n```\n\n"

        response += "💡 Agora posso analisar o roteiro COMPLETO com contexto total!"

        return response

    async def _chat_response(self, user_input: str) -> str:
        """Resposta de chat com contexto otimizado"""

        # Seleciona modelo e configuração
        model_rec = self.models_by_task['chat']
        model = model_rec['primary']
        options = self.token_config.get_ollama_options(model)

        # Prepara contexto
        prompt = user_input

        # Adiciona contexto do roteiro se disponível
        if self.current_screenplay and self.full_context_mode:
            # Usa contexto substancial (até metade dos tokens disponíveis)
            max_context = options['num_ctx'] // 2
            context = self.current_screenplay['content'][:max_context * 4]  # ~4 chars por token
            prompt = f"Screenplay context:\n{context}\n\nUser: {user_input}"

        try:
            print(f"💬 Gerando resposta com {model} ({options['num_ctx']} tokens)...")

            response = ollama.generate(
                model=model,
                prompt=prompt,
                system="You are an expert screenplay analyst. Be helpful and insightful.",
                options=options
            )

            return response['response']

        except Exception as e:
            return f"❌ Erro: {e}"

    async def _analysis_with_context(self, user_input: str) -> str:
        """Análise com contexto substancial"""

        if not self.current_screenplay:
            return "❌ Carregue um roteiro primeiro com 'carregar [nome]'"

        # Usa modelo de análise com máximo contexto
        model_rec = self.models_by_task['analysis']
        model = model_rec['primary']
        options = self.token_config.get_ollama_options(model)

        print(f"📊 Analisando com {model} ({options['num_ctx']} tokens)...")

        # Usa muito contexto (75% dos tokens disponíveis)
        max_context = int(options['num_ctx'] * 0.75)
        context = self.current_screenplay['content'][:max_context * 4]

        prompt = f"""Analyze this screenplay thoroughly:

Title: {self.current_screenplay['title']}
Pages: {self.current_screenplay['pages']}

Full screenplay content:
{context}

User request: {user_input}

Provide comprehensive analysis using ALL the context available."""

        try:
            response = ollama.generate(
                model=model,
                prompt=prompt,
                options=options
            )

            return "📊 **ANÁLISE COMPLETA:**\n\n" + response['response']

        except Exception as e:
            return f"❌ Erro na análise: {e}"

    async def _deep_analysis_max_tokens(self, user_input: str) -> str:
        """Análise profunda usando MÁXIMO de tokens possível"""

        if not self.current_screenplay:
            return "❌ Carregue um roteiro primeiro"

        # Usa modelo profundo com configuração máxima
        model_rec = self.models_by_task['deep']
        model = model_rec['primary']
        options = self.token_config.get_ollama_options(model)

        print(f"🧠 ANÁLISE PROFUNDA MÁXIMA com {model}")
        print(f"   Tokens: {options['num_ctx']:,}")
        print(f"   Threads: {options['num_thread']}")
        print(f"   RAM estimada: ~50GB")
        print("   ⏳ Isso pode levar 3-7 minutos...")

        # USA TODO O ROTEIRO (até o limite de tokens)
        max_chars = options['num_ctx'] * 4  # Aproximação
        full_content = self.current_screenplay['content'][:max_chars]

        prompt = f"""DEEP COMPREHENSIVE ANALYSIS REQUESTED

COMPLETE SCREENPLAY:
{full_content}

USER REQUEST: {user_input}

You have {options['num_ctx']:,} tokens available. Use ALL of them to provide:
1. Complete scene-by-scene breakdown
2. Full character arc analysis for every character
3. Detailed dialogue examination
4. Comprehensive thematic exploration
5. Market analysis and comparisons
6. Specific, actionable recommendations

BE EXHAUSTIVE. This is a deep dive using maximum computational resources."""

        try:
            start_time = time.time()

            response = ollama.generate(
                model=model,
                prompt=prompt,
                options=options
            )

            elapsed = time.time() - start_time

            result = "\n" + "="*70 + "\n"
            result += "🧠 **ANÁLISE PROFUNDA MÁXIMA COMPLETA**\n"
            result += "="*70 + "\n\n"
            result += f"📄 Roteiro: {self.current_screenplay['title']}\n"
            result += f"🔤 Tokens processados: {options['num_ctx']:,}\n"
            result += f"⏱️ Tempo: {elapsed:.1f}s\n"
            result += f"🧵 Threads utilizadas: {options['num_thread']}\n\n"
            result += "-"*70 + "\n\n"
            result += response['response']
            result += "\n\n" + "-"*70
            result += "\n✅ Análise máxima concluída!"

            return result

        except Exception as e:
            return f"❌ Erro na análise profunda: {e}"

    async def interactive_session(self):
        """Sessão interativa com máximo de recursos"""

        print("\n" + "="*70)
        print("🎬 ULTIMATE SCREENPLAY CHAT - MÁXIMO TOKENS")
        print("Mac Studio M3 Ultra - 96GB RAM")
        print("="*70)

        # Mostra configurações
        self.token_config.print_config_table()

        print("\n💡 COMANDOS ESPECIAIS:")
        print("  • 'contexto completo' - Ativa modo máximo")
        print("  • 'carregar [nome]' - Carrega roteiro completo")
        print("  • 'análise' - Análise com contexto substancial")
        print("  • 'análise profunda' - Usa TODOS os tokens disponíveis")
        print("  • 'sair' - Encerrar")
        print("\n" + "-"*70 + "\n")

        while True:
            try:
                user_input = input("🎭 Você: ").strip()

                if user_input.lower() in ['sair', 'exit', 'quit']:
                    print("\n👋 Até logo!")
                    break

                if not user_input:
                    continue

                # Processa com máximo de recursos
                response = await self.chat(user_input)

                print(f"\n🤖 Assistant:\n{response}\n")
                print("-"*70 + "\n")

            except KeyboardInterrupt:
                print("\n\nUse 'sair' para encerrar.")
            except Exception as e:
                print(f"\n❌ Erro: {e}\n")

async def main():
    """Executa chat com máximo de tokens"""
    chat = UltimateScreenplayChat()
    await chat.interactive_session()
    print("\nDIGIMUNDO PRESENTE")

if __name__ == "__main__":
    asyncio.run(main())