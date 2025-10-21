#!/usr/bin/env python3
"""
🎬 INTELLIGENT CHAT ORCHESTRATOR
Sistema conversacional inteligente que ativa análise profunda sob demanda
Mac Studio M3 Ultra - 96GB RAM - 28 cores
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
import logging
from dataclasses import dataclass
import threading
from concurrent.futures import ThreadPoolExecutor

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ChatContext:
    """Contexto da conversa para decisões inteligentes"""
    is_screenplay_related: bool = False
    needs_deep_analysis: bool = False
    pdf_mentioned: Optional[str] = None
    analysis_requested: bool = False
    conversation_mode: str = "casual"  # casual, analysis, deep

class IntelligentChatOrchestrator:
    """
    Orquestrador inteligente de conversa
    Conversa naturalmente até detectar necessidade de análise profunda
    """

    def __init__(self):
        """Inicializa o sistema de chat inteligente"""

        # Caminhos importantes
        self.biblioteca_path = Path('/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS')
        self.teoria_path = Path('/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/TEORIA_CINEMA')

        # Configurações de cores (14 cores para CPU, deixa 14 para sistema)
        self.cpu_cores = 14  # Aumentado de 8 para 14 como solicitado
        self.gpu_cores = 4   # Para modelos leves

        # Modelos disponíveis
        self.models = {
            # Modelos conversacionais (rápidos)
            'casual': 'llama3.2:3b',       # Conversa casual
            'assistant': 'gemma2:2b',      # Assistente rápido
            'quick': 'mistral:7b',         # Respostas rápidas

            # Modelos de análise (médios)
            'analyzer': 'llama3.1:8b',     # Análise básica
            'reviewer': 'qwen2.5:14b',     # Review detalhado

            # Modelos profundos (CPU otimizado)
            'deep': 'scripturemon-cpu-optimized',  # Análise profunda
            'themes': 'scripturemon-cpu-themes',   # Temas
            'structure': 'scripturemon-cpu-structure',  # Estrutura
            'dialogue': 'scripturemon-cpu-dialogue',    # Diálogos

            # Orquestrador
            'orchestrator': 'producermon'  # Decide qual usar
        }

        # Estado da conversa
        self.conversation_history = []
        self.current_context = ChatContext()
        self.pdf_cache = {}
        self.active_analyses = {}

        # Executor para tarefas em background
        self.executor = ThreadPoolExecutor(max_workers=4)

        # Palavras-chave para detectar contexto
        self.screenplay_keywords = [
            'roteiro', 'script', 'screenplay', 'filme', 'movie',
            'cena', 'scene', 'personagem', 'character', 'diálogo',
            'dialogue', 'ato', 'act', 'fade', 'int.', 'ext.',
            'análise', 'analyze', 'review', 'feedback', 'opinião'
        ]

        self.deep_analysis_triggers = [
            'análise profunda', 'deep analysis', 'analise completa',
            'feedback detalhado', 'detailed feedback', 'review completo',
            'o que você acha', 'sua opinião sobre', 'avalie meu',
            'critique', 'avaliar', 'melhorar', 'sugestões'
        ]

        logger.info(f"✅ Chat Orchestrator iniciado com {self.cpu_cores} cores para CPU")

    def detect_context(self, user_input: str) -> ChatContext:
        """Detecta o contexto da conversa para decidir como responder"""

        input_lower = user_input.lower()
        context = ChatContext()

        # Verifica se menciona roteiros/cinema
        if any(keyword in input_lower for keyword in self.screenplay_keywords):
            context.is_screenplay_related = True
            context.conversation_mode = "analysis"

        # Verifica se pede análise profunda
        if any(trigger in input_lower for trigger in self.deep_analysis_triggers):
            context.needs_deep_analysis = True
            context.analysis_requested = True
            context.conversation_mode = "deep"

        # Detecta menção a PDFs específicos
        pdf_pattern = r'(\w+\.pdf)'
        pdf_match = re.search(pdf_pattern, input_lower)
        if pdf_match:
            context.pdf_mentioned = pdf_match.group(1)
            context.is_screenplay_related = True

        # Verifica PDFs na biblioteca
        if context.is_screenplay_related:
            pdfs = list(self.biblioteca_path.glob('*.pdf'))
            for pdf in pdfs:
                if pdf.stem.lower() in input_lower:
                    context.pdf_mentioned = pdf.name
                    break

        return context

    async def respond(self, user_input: str) -> str:
        """
        Responde ao usuário de forma inteligente
        Usa modelos simples para conversa, ativa profundos quando necessário
        """

        # Detecta contexto
        self.current_context = self.detect_context(user_input)

        # Adiciona ao histórico
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user': user_input,
            'context': self.current_context
        })

        # Decide estratégia de resposta
        if self.current_context.conversation_mode == "casual":
            # Conversa casual - modelo rápido
            return await self._casual_response(user_input)

        elif self.current_context.conversation_mode == "analysis":
            # Análise básica - modelo médio
            return await self._analysis_response(user_input)

        elif self.current_context.conversation_mode == "deep":
            # Análise profunda - ativa sistema completo
            return await self._deep_analysis_response(user_input)

        # Fallback
        return await self._casual_response(user_input)

    async def _casual_response(self, user_input: str) -> str:
        """Resposta casual usando modelo leve"""

        try:
            # Usa modelo leve para conversa
            response = ollama.generate(
                model=self.models['casual'],
                prompt=user_input,
                system="Você é um assistente amigável e prestativo. Responda de forma natural e concisa.",
                options={
                    'num_thread': self.gpu_cores,
                    'temperature': 0.7,
                    'num_ctx': 4096
                }
            )

            return response['response']

        except Exception as e:
            logger.error(f"Erro em resposta casual: {e}")
            return "Desculpe, tive um problema ao processar sua mensagem. Pode tentar novamente?"

    async def _analysis_response(self, user_input: str) -> str:
        """Resposta com análise básica de roteiro"""

        try:
            # Se mencionou PDF específico, carrega contexto
            context = ""
            if self.current_context.pdf_mentioned:
                pdf_path = self.biblioteca_path / self.current_context.pdf_mentioned
                if pdf_path.exists():
                    context = await self._load_pdf_context(pdf_path)
                    context = f"Contexto do roteiro {self.current_context.pdf_mentioned}:\n{context[:2000]}\n\n"

            # Usa modelo de análise
            prompt = f"{context}Pergunta: {user_input}"

            response = ollama.generate(
                model=self.models['analyzer'],
                prompt=prompt,
                system="Você é um analista de roteiros experiente. Forneça insights úteis sobre estrutura, personagens e narrativa.",
                options={
                    'num_thread': 6,
                    'temperature': 0.6,
                    'num_ctx': 8192
                }
            )

            return response['response']

        except Exception as e:
            logger.error(f"Erro em análise: {e}")
            return "Não consegui analisar o roteiro no momento. Posso ajudar de outra forma?"

    async def _deep_analysis_response(self, user_input: str) -> str:
        """
        Resposta com análise profunda usando CPU model otimizado
        Fornece feedback imediato e análise profunda em background
        """

        print("\n🎭 Ativando análise profunda...")
        print(f"📊 Usando {self.cpu_cores} cores para processamento")

        # Resposta imediata
        immediate_response = await self._get_quick_preview(user_input)

        # Inicia análise profunda em background
        deep_task = asyncio.create_task(
            self._run_deep_analysis(user_input)
        )

        # Retorna preview imediato
        response = f"{immediate_response}\n\n"
        response += "⏳ **Análise profunda em andamento** (2-5 minutos)...\n"
        response += "Você receberá insights detalhados quando estiver pronto."

        # Salva task para consulta posterior
        analysis_id = datetime.now().isoformat()
        self.active_analyses[analysis_id] = deep_task

        return response

    async def _get_quick_preview(self, user_input: str) -> str:
        """Gera preview rápido enquanto análise profunda roda"""

        try:
            # Usa ProducerMon para preview
            response = ollama.generate(
                model=self.models['orchestrator'],
                prompt=f"Provide a quick preview analysis for: {user_input}",
                system="You are ProducerMon. Give a quick 2-3 sentence preview of what you'll analyze.",
                options={
                    'num_thread': 4,
                    'temperature': 0.7,
                    'num_ctx': 4096
                }
            )

            return "📋 **Preview Rápido:**\n" + response['response']

        except:
            return "📋 Preparando análise detalhada do seu roteiro..."

    async def _run_deep_analysis(self, user_input: str) -> Dict:
        """
        Executa análise profunda com CPU model
        Usa 14 cores como solicitado
        """

        start_time = time.time()
        results = {}

        try:
            # Carrega contexto do PDF se mencionado
            full_context = user_input
            if self.current_context.pdf_mentioned:
                pdf_path = self.biblioteca_path / self.current_context.pdf_mentioned
                if pdf_path.exists():
                    pdf_content = await self._load_pdf_context(pdf_path, full=True)
                    full_context = f"Script: {pdf_content}\n\nQuestion: {user_input}"

            # Análise profunda com CPU model otimizado
            print(f"🧠 Iniciando análise profunda com {self.cpu_cores} cores...")

            deep_response = ollama.generate(
                model=self.models['deep'],
                prompt=full_context,
                system="""You are Scripturemon-CPU, the Deep Thinker.
                Provide comprehensive analysis covering:
                1. Three-act structure and pacing
                2. Character development and arcs
                3. Dialogue quality and subtext
                4. Themes and symbolism
                5. Market potential and audience
                6. Specific recommendations for improvement

                Be thorough but organized. Use your full capacity.""",
                options={
                    'num_thread': self.cpu_cores,  # 14 cores
                    'temperature': 0.6,
                    'num_ctx': 16384,
                    'num_batch': 512
                }
            )

            results['deep_analysis'] = deep_response['response']

            # Se houver tempo, adiciona perspectivas especializadas
            if time.time() - start_time < 180:  # Se ainda tem tempo (< 3 min)

                # Análise de temas
                theme_response = ollama.generate(
                    model=self.models['themes'],
                    prompt=full_context[:5000],  # Versão resumida
                    options={'num_thread': 6, 'temperature': 0.65}
                )
                results['themes'] = theme_response['response']

                # Análise de diálogos
                dialogue_response = ollama.generate(
                    model=self.models['dialogue'],
                    prompt=full_context[:5000],
                    options={'num_thread': 6, 'temperature': 0.7}
                )
                results['dialogue'] = dialogue_response['response']

            elapsed = time.time() - start_time
            print(f"✅ Análise profunda concluída em {elapsed:.1f}s")

            # Notifica usuário
            await self._notify_analysis_complete(results, elapsed)

        except Exception as e:
            logger.error(f"Erro em análise profunda: {e}")
            results['error'] = str(e)

        return results

    async def _load_pdf_context(self, pdf_path: Path, full: bool = False) -> str:
        """Carrega conteúdo do PDF (cached)"""

        if str(pdf_path) in self.pdf_cache:
            content = self.pdf_cache[str(pdf_path)]
        else:
            # Aqui você integraria com o sistema de leitura de PDFs
            # Por enquanto, retorna placeholder
            content = f"[Conteúdo do roteiro {pdf_path.name}]"
            self.pdf_cache[str(pdf_path)] = content

        if full:
            return content
        else:
            return content[:2000]  # Preview

    async def _notify_analysis_complete(self, results: Dict, elapsed_time: float):
        """Notifica quando análise profunda está pronta"""

        print("\n" + "="*60)
        print("🎉 ANÁLISE PROFUNDA CONCLUÍDA!")
        print(f"⏱️  Tempo total: {elapsed_time:.1f} segundos")
        print("="*60)

        if 'deep_analysis' in results:
            print("\n📊 ANÁLISE PRINCIPAL:")
            print("-" * 40)
            print(results['deep_analysis'][:500] + "...")

        if 'themes' in results:
            print("\n🎭 ANÁLISE TEMÁTICA:")
            print("-" * 40)
            print(results['themes'][:300] + "...")

        if 'dialogue' in results:
            print("\n💬 ANÁLISE DE DIÁLOGOS:")
            print("-" * 40)
            print(results['dialogue'][:300] + "...")

    def get_analysis_status(self, analysis_id: str) -> Dict:
        """Verifica status de análise em andamento"""

        if analysis_id in self.active_analyses:
            task = self.active_analyses[analysis_id]
            if task.done():
                return {
                    'status': 'complete',
                    'result': task.result()
                }
            else:
                return {'status': 'processing'}

        return {'status': 'not_found'}

    async def chat_loop(self):
        """Loop principal de conversa interativa"""

        print("\n" + "="*60)
        print("🎬 SCRIPTUREMON INTELLIGENT CHAT")
        print("Mac Studio M3 Ultra - 96GB RAM - 28 cores")
        print("="*60)
        print("\n💡 Dicas:")
        print("  • Converse normalmente - uso modelos leves")
        print("  • Peça 'análise profunda' - ativo CPU com 14 cores")
        print("  • Mencione PDFs da biblioteca para contexto")
        print("\nDigite 'sair' para encerrar\n")

        while True:
            try:
                # Input do usuário
                user_input = input("🎭 Você: ").strip()

                if user_input.lower() in ['sair', 'exit', 'quit']:
                    print("👋 Até logo! Foi ótimo conversar com você.")
                    break

                if not user_input:
                    continue

                # Processa resposta
                response = await self.respond(user_input)

                # Mostra resposta
                print(f"\n🤖 ScriptureMon: {response}\n")

                # Adiciona resposta ao histórico
                if self.conversation_history:
                    self.conversation_history[-1]['response'] = response

            except KeyboardInterrupt:
                print("\n\n⚠️  Interrompido. Digite 'sair' para encerrar.")
            except Exception as e:
                logger.error(f"Erro no chat: {e}")
                print(f"❌ Erro: {e}")

class SmartChatCLI:
    """Interface CLI para o chat inteligente"""

    def __init__(self):
        self.orchestrator = IntelligentChatOrchestrator()

    async def run(self):
        """Executa o chat"""
        await self.orchestrator.chat_loop()

async def main():
    """Função principal"""
    cli = SmartChatCLI()
    await cli.run()

if __name__ == "__main__":
    # Executa o chat
    asyncio.run(main())
    print("\nDIGIMUNDO PRESENTE")