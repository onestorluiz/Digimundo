#!/usr/bin/env python3
"""
🚀 SISTEMA PRINCIPAL MIXTRAL Q5 - REFATORADO
Sistema limpo e funcional para análise automatizada de roteiros
Focus: Mixtral como sistema principal (não secundário ao mixtral)
"""

import asyncio
import time
import sys
import ollama
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.screenplay_library import ScreenplayLibrary
from src.core.unified_memory_system import UnifiedMemorySystem


class MixtralPrimarySystem:
    """Sistema principal baseado em Mixtral Q5 para análise de roteiros"""

    def __init__(self):
        self.eco_model = "mixtral-eco-q5"
        self.dedicated_model = "mixtral-dedicated-q5"
        self.current_model = self.dedicated_model  # Dedicado como padrão

        self.library = ScreenplayLibrary()
        self.memory = UnifiedMemorySystem()
        self.processed_count = 0

        # Configurações por modo
        self.configs = {
            "eco": {
                'num_ctx': 32768,      # 32K context
                'num_thread': 14,      # 50% CPU
                'num_gpu': 50,         # 83% GPU
                'temperature': 0.3,
                'num_predict': 1500
            },
            "dedicated": {
                'num_ctx': 131072,     # 128K context
                'num_thread': 24,      # 86% CPU
                'num_gpu': 60,         # 100% GPU
                'temperature': 0.2,
                'num_predict': 2000
            }
        }

    def set_mode(self, mode: str):
        """Alterna entre eco e dedicated"""
        if mode.lower() == "eco":
            self.current_model = self.eco_model
        else:
            self.current_model = self.dedicated_model
        print(f"🔄 Modo alterado para: {mode.upper()} - {self.current_model}")

    async def analyze_screenplay(self, title: str, content: str, mode: str = "dedicated") -> Dict[str, Any]:
        """Análise completa com Mixtral"""

        print(f"\\n📖 ANALISANDO: {title}")
        print(f"🧠 Modelo: {self.current_model}")
        print(f"📊 Contexto: {self.configs[mode]['num_ctx']:,} tokens")
        print("-" * 60)

        # Prompt estruturado Save the Cat + Comparações
        prompt = f"""Analyze this screenplay using professional frameworks:

SCREENPLAY: {title}

{content[:80000]}  # 80K chars para contexto máximo

Provide comprehensive analysis covering:

## 1. SAVE THE CAT STRUCTURE
- Opening Image (page estimate)
- Theme Stated (page estimate)
- Setup (pages 1-10)
- Catalyst/Inciting Incident (page 12)
- Debate (pages 12-25)
- Break into Two (page 25)
- B Story introduction (page 30)
- Fun and Games (pages 30-55)
- Midpoint (page 55)
- Bad Guys Close In (pages 55-75)
- All Is Lost (page 75)
- Dark Night of the Soul (pages 75-85)
- Break into Three (page 85)
- Finale (pages 85-110)
- Final Image (page 110)

## 2. CHARACTER ANALYSIS
- Protagonist's WANT vs NEED
- Character arc transformation
- Ghost/backstory wound
- Supporting character functions

## 3. THEMATIC ANALYSIS
- Central theme
- Visual metaphors
- Symbolic elements
- Subtext layers

## 4. MASTERPIECE COMPARISON
Compare with classics like Casablanca, The Godfather, Pulp Fiction:
- Similar structural patterns
- Character archetype similarities
- Thematic connections
- Unique innovations

## 5. IMPROVEMENT RECOMMENDATIONS
- Specific page-level suggestions
- Character development opportunities
- Pacing adjustments
- Theme reinforcement ideas

Provide specific page numbers and actionable insights."""

        try:
            start_time = time.time()

            # Análise com Mixtral
            response = ollama.generate(
                model=self.current_model,
                prompt=prompt,
                options=self.configs[mode]
            )

            end_time = time.time()
            duration = end_time - start_time

            analysis = response['response']

            print(f"✅ Análise completa em {duration:.1f}s")
            print(f"📊 Tamanho: {len(analysis):,} caracteres")

            # Salvar na memória unificada
            self.memory.store_knowledge(
                key=f"mixtral_analysis:{title}",
                content=analysis,
                metadata={
                    "screenplay": title,
                    "model": self.current_model,
                    "mode": mode,
                    "duration": duration,
                    "timestamp": time.time(),
                    "context_size": self.configs[mode]['num_ctx']
                }
            )

            self.processed_count += 1

            return {
                "success": True,
                "title": title,
                "analysis": analysis,
                "duration": duration,
                "model": self.current_model,
                "mode": mode
            }

        except Exception as e:
            print(f"❌ Erro: {e}")
            return {
                "success": False,
                "title": title,
                "error": str(e),
                "model": self.current_model
            }

    async def run_continuous_analysis(self, mode: str = "dedicated", limit: int = 10):
        """Processamento contínuo automatizado"""

        print(f"🚀 SISTEMA PRINCIPAL MIXTRAL Q5 - MODO {mode.upper()}")
        print("=" * 60)
        print(f"Modelo: {self.current_model}")
        print(f"Context: {self.configs[mode]['num_ctx']:,} tokens")
        print(f"Target: {limit} roteiros")
        print("=" * 60)

        # Configurar modo
        self.set_mode(mode)

        # Obter lista de roteiros (apenas .txt)
        screenplays = self.library.list_screenplays()
        print(f"\\n📚 {len(screenplays)} roteiros disponíveis")

        # Filtrar apenas arquivos .txt existentes
        valid_screenplays = []
        for title in screenplays[:limit]:
            content = self.library.get_screenplay(title)
            if content and len(content) > 100:  # Validar conteúdo mínimo
                valid_screenplays.append(title)

        print(f"✅ {len(valid_screenplays)} roteiros válidos encontrados")

        # Processar cada roteiro
        for i, title in enumerate(valid_screenplays, 1):
            print(f"\\n{'='*60}")
            print(f"[{i}/{len(valid_screenplays)}] PROCESSAMENTO {i}")
            print(f"{'='*60}")

            # Obter conteúdo
            content = self.library.get_screenplay(title)

            # Análise principal
            result = await self.analyze_screenplay(title, content, mode)

            if result['success']:
                print(f"\\n📋 RESUMO {title}:")
                print(f"   • Modelo: {result['model']}")
                print(f"   • Modo: {result['mode']}")
                print(f"   • Análise: {len(result['analysis']):,} chars")
                print(f"   • Tempo: {result['duration']:.1f}s")
                print(f"   • Contexto: {self.configs[mode]['num_ctx']:,} tokens")
            else:
                print(f"\\n❌ FALHA em {title}: {result.get('error', 'Unknown')}")

            # Pausa entre processamentos (apenas se houver mais)
            if i < len(valid_screenplays):
                print(f"\\n⏳ Pausa de 15 segundos...")
                await asyncio.sleep(15)

        print(f"\\n✅ PROCESSAMENTO COMPLETO!")
        print(f"📊 Total processado: {self.processed_count} roteiros")
        print(f"🧠 Modelo: {self.current_model}")
        print(f"🎯 Sistema: Mixtral Primary (não secundário)")

        print("\\nDIGIMUNDO PRESENTE 🥷")

    async def quick_demo(self, mode: str = "dedicated"):
        """Demo rápido com 1 roteiro"""

        print(f"🧪 DEMO RÁPIDO MIXTRAL Q5 - {mode.upper()}")
        print("=" * 50)

        self.set_mode(mode)

        screenplays = self.library.list_screenplays()
        if not screenplays:
            print("❌ Nenhum roteiro encontrado")
            return

        # Pegar primeiro roteiro válido
        for title in screenplays[:3]:  # Testar primeiros 3
            content = self.library.get_screenplay(title)
            if content and len(content) > 100:
                result = await self.analyze_screenplay(title, content, mode)

                if result['success']:
                    print(f"\\n📋 PREVIEW DA ANÁLISE:")
                    print("=" * 40)
                    preview = result['analysis'][:800]
                    print(f"{preview}...")
                    print(f"\\n✅ Análise completa salva na memória")
                    print(f"🧠 Modelo: {result['model']}")
                    print(f"⚡ {result['duration']:.1f}s")
                    break
                else:
                    print(f"❌ Erro em {title}: {result.get('error')}")

        print("\\nDIGIMUNDO PRESENTE 🥷")


async def main():
    """Função principal"""

    processor = MixtralPrimarySystem()

    print("\\n🚀 SISTEMA PRINCIPAL MIXTRAL Q5")
    print("================================")
    print("1. Demo rápido ECO (32K context)")
    print("2. Demo rápido DEDICATED (128K context)")
    print("3. Processamento contínuo ECO (10 roteiros)")
    print("4. Processamento contínuo DEDICATED (10 roteiros)")

    choice = input("\\nEscolha (1-4): ").strip()

    if choice == "1":
        await processor.quick_demo("eco")
    elif choice == "2":
        await processor.quick_demo("dedicated")
    elif choice == "3":
        await processor.run_continuous_analysis("eco", 10)
    elif choice == "4":
        await processor.run_continuous_analysis("dedicated", 10)
    else:
        print("Opção inválida. Executando demo dedicated...")
        await processor.quick_demo("dedicated")


if __name__ == "__main__":
    asyncio.run(main())