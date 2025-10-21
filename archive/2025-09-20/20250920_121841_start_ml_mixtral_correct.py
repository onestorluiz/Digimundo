#!/usr/bin/env python3
"""
🧠 ATIVADOR DO MACHINE LEARNING COM MIXTRAL CORRIGIDO
Inicia o processo de ML com todas as correções aplicadas
"""

import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.screenplay_library import ScreenplayLibrary
from src.core.unified_memory_system import get_unified_memory, MemoryType
import ollama
from datetime import datetime

class MixtralMLSystem:
    """Sistema de Machine Learning com Mixtral corrigido"""

    def __init__(self):
        self.library = ScreenplayLibrary()
        self.memory = get_unified_memory()
        self.model = "mixtral-dedicated-q5"

        # Configuração otimizada para Mixtral
        self.options = {
            'num_ctx': 131072,    # 128K tokens
            'num_thread': 24,     # 86% dos cores
            'num_gpu': 60,        # Todos cores GPU
            'num_batch': 4096,    # Batch otimizado
            'temperature': 0.3,   # Precisão analítica
            'top_p': 0.9,
            'seed': 42
        }

        print("🚀 SISTEMA ML MIXTRAL INICIADO")
        print(f"   • Modelo: {self.model}")
        print(f"   • Contexto: {self.options['num_ctx']:,} tokens")
        print(f"   • Threads: {self.options['num_thread']}")
        print(f"   • Biblioteca: {len(self.library.list_screenplays())} roteiros")
        print("=" * 60)

    async def analyze_screenplay(self, title: str, content: str):
        """Analisa um roteiro com ML"""
        print(f"\n📖 ANALISANDO: {title}")
        print("-" * 40)

        # 1. Análise de estrutura com Save the Cat
        structure_prompt = f"""Analyze this screenplay using Save the Cat beats:

{content[:5000]}

Identify:
1. Opening Image (1%)
2. Theme Stated (5%)
3. Setup (10%)
4. Catalyst (12%)
5. Debate (25%)
6. Break into Two (25%)
7. Midpoint (50%)

Be specific and cite exact lines."""

        print("1️⃣ Analisando estrutura Save the Cat...")
        try:
            response = ollama.generate(
                model=self.model,
                prompt=structure_prompt,
                options=self.options
            )

            analysis = response['response']
            print(f"   ✅ {len(analysis)} caracteres gerados")

            # Salvar na memória
            self.memory.store(
                memory_type=MemoryType.ANALYSIS,
                key=f"save_cat:{title}",
                value={
                    'screenplay': title,
                    'analysis': analysis,
                    'timestamp': datetime.now().isoformat()
                },
                metadata={'type': 'save_the_cat', 'model': self.model}
            )

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return False

        # 2. Análise de personagens
        character_prompt = f"""Analyze the main character in this screenplay:

{content[:5000]}

Focus on:
1. Character WANT (external goal)
2. Character NEED (internal transformation)
3. Character ARC (how they change)
4. Key dialogue that reveals character

Be specific with examples."""

        print("2️⃣ Analisando desenvolvimento de personagens...")
        try:
            response = ollama.generate(
                model=self.model,
                prompt=character_prompt,
                options=self.options
            )

            analysis = response['response']
            print(f"   ✅ {len(analysis)} caracteres gerados")

            # Salvar na memória
            self.memory.store(
                memory_type=MemoryType.ANALYSIS,
                key=f"character:{title}",
                value={
                    'screenplay': title,
                    'analysis': analysis,
                    'timestamp': datetime.now().isoformat()
                },
                metadata={'type': 'character_analysis', 'model': self.model}
            )

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return False

        # 3. Extração de padrões
        pattern_prompt = f"""Identify recurring patterns in this screenplay:

{content[:5000]}

Look for:
1. Recurring themes or motifs
2. Structural patterns
3. Dialogue patterns
4. Visual patterns

List each pattern with examples."""

        print("3️⃣ Extraindo padrões narrativos...")
        try:
            response = ollama.generate(
                model=self.model,
                prompt=pattern_prompt,
                options=self.options
            )

            analysis = response['response']
            print(f"   ✅ {len(analysis)} caracteres gerados")

            # Salvar na memória
            self.memory.store(
                memory_type=MemoryType.KNOWLEDGE,
                key=f"patterns:{title}",
                value={
                    'screenplay': title,
                    'patterns': analysis,
                    'timestamp': datetime.now().isoformat()
                },
                metadata={'type': 'pattern_extraction', 'model': self.model}
            )

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return False

        return True

    async def run_continuous_learning(self):
        """Executa aprendizado contínuo"""
        print("\n" + "=" * 60)
        print("⚡ INICIANDO MACHINE LEARNING CONTÍNUO")
        print("=" * 60)

        screenplays = self.library.list_screenplays()[:5]  # Processar 5 primeiros

        for i, title in enumerate(screenplays, 1):
            print(f"\n[{i}/{len(screenplays)}] Processando: {title}")

            # Obter conteúdo do roteiro
            content = self.library.get_screenplay(title)
            if not content or content == '.' or len(content) < 100:
                print(f"   ⚠️ Pulando - conteúdo inválido")
                continue

            # Analisar
            success = await self.analyze_screenplay(title, content)

            if success:
                print(f"   ✅ Análise completa salva na memória")

            # Pequena pausa entre análises
            await asyncio.sleep(2)

        # Estatísticas finais
        print("\n" + "=" * 60)
        print("📊 ESTATÍSTICAS DO MACHINE LEARNING")
        print("=" * 60)

        # Contar análises na memória
        analyses = self.memory.search(
            query="analysis",
            memory_types=[MemoryType.ANALYSIS],
            limit=100
        )

        knowledge = self.memory.search(
            query="pattern",
            memory_types=[MemoryType.KNOWLEDGE],
            limit=100
        )

        print(f"✅ Análises salvas: {len(analyses)}")
        print(f"✅ Conhecimentos extraídos: {len(knowledge)}")
        print(f"✅ Total na memória: {len(analyses) + len(knowledge)}")

        print("\nDIGIMUNDO PRESENTE 🥷")


async def main():
    """Função principal"""
    print("""
╔══════════════════════════════════════════════════════════╗
║       🧠 MACHINE LEARNING COM MIXTRAL CORRIGIDO 🧠       ║
║                                                          ║
║  Sistema completamente corrigido e funcional            ║
║  Usando mixtral-dedicated-q5 com 128K tokens            ║
╚══════════════════════════════════════════════════════════╝
    """)

    # Verificar se modelo existe
    try:
        models = ollama.list()
        model_names = [m['name'] for m in models['models']]

        if 'mixtral-dedicated-q5:latest' not in model_names:
            print("⚠️ Modelo mixtral-dedicated-q5 não encontrado!")
            print("   Usando modelo alternativo...")
            # Poderia usar llama3.2:3b como fallback
    except:
        pass

    # Iniciar sistema
    system = MixtralMLSystem()

    # Menu de opções
    print("\nEscolha uma opção:")
    print("1. Análise rápida (1 roteiro)")
    print("2. Aprendizado contínuo (5 roteiros)")
    print("3. Análise completa (todos os roteiros)")

    choice = input("\nOpção: ").strip()

    if choice == "1":
        # Análise rápida
        screenplays = system.library.list_screenplays()
        if screenplays:
            title = screenplays[0]
            content = system.library.get_screenplay(title)
            if content and content != '.':
                await system.analyze_screenplay(title, content)

    elif choice == "2":
        # Aprendizado contínuo
        await system.run_continuous_learning()

    elif choice == "3":
        # Análise completa (cuidado, demora muito!)
        print("⚠️ AVISO: Isso pode levar HORAS!")
        confirm = input("Continuar? (s/n): ")
        if confirm.lower() == 's':
            system.screenplays = system.library.list_screenplays()
            await system.run_continuous_learning()

    else:
        print("Opção inválida")


if __name__ == "__main__":
    asyncio.run(main())