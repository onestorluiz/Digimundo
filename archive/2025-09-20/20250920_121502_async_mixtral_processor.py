#!/usr/bin/env python3
"""
🔥 PROCESSADOR ASSÍNCRONO mixtral mixtral
Sistema inteligente para rodar análises em background
"""

import asyncio
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class AsyncmixtralProcessor:
    """Processador assíncrono com logs e monitoramento"""

    def __init__(self, mode: str = "ECO"):
        """
        Inicializa processador

        Args:
            mode: "ECO" ou "DEDICATED"
        """
        self.mode = mode.upper()
        self.model = f"deeplearning-mixtral-{mode.lower()}"

        # Diretórios de log
        self.log_dir = Path(__file__).parent.parent.parent / "data" / "logs" / "deep_learning_mixtral"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Arquivos de controle
        self.status_file = self.log_dir / "current_status.json"
        self.results_file = self.log_dir / f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        self.metrics_file = self.log_dir / "performance_metrics.json"

        # Configurações por modo
        self.configs = {
            "ECO": {
                "timeout": 600,  # 10 minutos
                "options": {
                    "num_ctx": 32768,
                    "num_thread": 12,
                    "num_gpu": 40,
                    "num_batch": 2048,
                    "num_keep": 1024,
                    "num_predict": 500,
                    "temperature": 0.3,
                    "f16_kv": True,
                    "use_mmap": True,
                    "use_mlock": False
                },
                "chunk_size": 10000,
                "analysis_depth": "balanced"
            },
            "DEDICATED": {
                "timeout": 1200,  # 20 minutos
                "options": {
                    "num_ctx": 131072,
                    "num_thread": 24,
                    "num_gpu": 60,  # M3 Ultra GPU cores
                    "gpu_layers": 80,
                    "num_batch": 8192,
                    "num_keep": 4096,
                    "num_predict": 2000,
                    "temperature": 0.2,
                    "f16_kv": False,
                    "use_mmap": True,
                    "use_mlock": True
                },
                "chunk_size": 50000,
                "analysis_depth": "exhaustive"
            }
        }

        self.config = self.configs[self.mode]
        self._init_metrics()

    def _init_metrics(self):
        """Inicializa arquivo de métricas"""
        if not self.metrics_file.exists():
            metrics = {
                "ECO": {
                    "total_processed": 0,
                    "total_time": 0,
                    "avg_time": 0,
                    "min_time": float('inf'),
                    "max_time": 0,
                    "successes": 0,
                    "errors": 0,
                    "total_tokens": 0
                },
                "DEDICATED": {
                    "total_processed": 0,
                    "total_time": 0,
                    "avg_time": 0,
                    "min_time": float('inf'),
                    "max_time": 0,
                    "successes": 0,
                    "errors": 0,
                    "total_tokens": 0
                }
            }
            with open(self.metrics_file, 'w') as f:
                json.dump(metrics, f, indent=2)

    async def process_screenplay(self, screenplay: str, content: str) -> Dict[str, Any]:
        """
        Processa roteiro assincronamente

        Args:
            screenplay: Nome do roteiro
            content: Conteúdo do roteiro

        Returns:
            Dict com resultados
        """
        start_time = time.time()

        # Atualizar status - processando
        self._update_status({
            "status": "processing",
            "current": screenplay,
            "started": start_time,
            "mode": self.mode,
            "pid": None  # Será atualizado quando o processo iniciar
        })

        # Preparar prompt baseado no modo
        prompt = self._prepare_prompt(screenplay, content)

        # Preparar payload
        payload = {
            'model': self.model,
            'prompt': prompt,
            'stream': False,
            'options': self.config['options']
        }

        # Log do início
        print(f"\n🚀 [{self.mode}] Processando: {screenplay}")
        print(f"   • Modelo: {self.model}")
        print(f"   • Contexto: {self.config['options']['num_ctx']:,} tokens")
        print(f"   • Timeout: {self.config['timeout']}s")

        # Executar Ollama assincronamente
        try:
            process = await asyncio.create_subprocess_exec(
                'curl', '-s', '--max-time', str(self.config['timeout']),
                'http://localhost:11434/api/generate',
                '-d', json.dumps(payload),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Atualizar status com PID
            self._update_status({
                "status": "processing",
                "current": screenplay,
                "started": start_time,
                "mode": self.mode,
                "pid": process.pid
            })

            # Aguardar resultado
            stdout, stderr = await process.communicate()

        except Exception as e:
            return self._handle_error(screenplay, start_time, str(e))

        # Processar resultado
        return self._process_result(screenplay, start_time, stdout, stderr)

    def _prepare_prompt(self, screenplay: str, content: str) -> str:
        """Prepara prompt baseado no modo"""

        chunk = content[:self.config['chunk_size']]

        if self.mode == "ECO":
            return f"""Analyze screenplay: {screenplay}

Content:
{chunk}

Provide concise analysis covering:
1. Three-act structure
2. Main character arc
3. Central theme
4. Unique elements

Be specific but efficient. Maximum {self.config['options']['num_predict']} tokens."""

        else:  # DEDICATED
            return f"""COMPREHENSIVE DEEP ANALYSIS of {screenplay}

Full Content for Analysis:
{chunk}

Generate exhaustive analysis including:

STRUCTURE:
- Complete beat sheet with page numbers
- Three-act breakdown with turning points
- Scene-by-scene purpose and impact

CHARACTER:
- Full protagonist journey and transformation
- Supporting character functions and arcs
- Relationship dynamics and evolution

THEME & MEANING:
- Primary and secondary themes
- Symbolic elements and metaphors
- Social/philosophical commentary

TECHNICAL CRAFT:
- Dialog effectiveness and subtext
- Visual storytelling techniques
- Pacing and rhythm analysis

INNOVATION:
- What makes this screenplay unique
- Genre conventions challenged or reinforced
- Influence on cinema

THEORY APPLICATION:
- Save the Cat beats (all 15)
- Hero's Journey stages
- Three-Act structure percentages

ACTIONABLE INSIGHTS:
- Specific strengths to preserve
- Areas for improvement with solutions
- Market positioning recommendations

Use all {self.config['options']['num_ctx']} tokens available.
Generate {self.config['options']['num_predict']} tokens minimum.
Include exact page references and quotes."""

    def _process_result(self, screenplay: str, start_time: float,
                       stdout: bytes, stderr: bytes) -> Dict[str, Any]:
        """Processa resultado do Ollama"""

        duration = time.time() - start_time

        result = {
            "screenplay": screenplay,
            "mode": self.mode,
            "started": start_time,
            "completed": time.time(),
            "duration": duration,
            "success": False,
            "model": self.model
        }

        if stdout:
            try:
                response = json.loads(stdout)
                result["analysis"] = response.get('response', '')
                result["success"] = True

                # Extrair métricas do modelo
                result["model_info"] = {
                    "total_duration": response.get('total_duration', 0) / 1e9,
                    "load_duration": response.get('load_duration', 0) / 1e9,
                    "prompt_eval_count": response.get('prompt_eval_count', 0),
                    "prompt_eval_duration": response.get('prompt_eval_duration', 0) / 1e9,
                    "eval_count": response.get('eval_count', 0),
                    "eval_duration": response.get('eval_duration', 0) / 1e9
                }

                # Calcular tokens/segundo
                if result["model_info"]["eval_duration"] > 0:
                    result["model_info"]["tokens_per_second"] = (
                        result["model_info"]["eval_count"] /
                        result["model_info"]["eval_duration"]
                    )

                print(f"   ✅ Sucesso em {duration:.1f}s")
                print(f"   📊 Tokens: {result['model_info']['eval_count']:,}")
                print(f"   ⚡ Velocidade: {result['model_info'].get('tokens_per_second', 0):.1f} tokens/s")

            except json.JSONDecodeError as e:
                result["error"] = f"Invalid JSON: {str(e)}"
                print(f"   ❌ Erro JSON: {str(e)[:50]}")
        else:
            result["error"] = stderr.decode() if stderr else "No response"
            print(f"   ❌ Erro: {result['error'][:50]}")

        # Salvar resultado
        self._save_result(result)

        # Atualizar métricas
        self._update_metrics(result)

        # Atualizar status
        self._update_status({
            "status": "completed" if result["success"] else "error",
            "last_completed": screenplay,
            "last_duration": duration,
            "last_success": result["success"],
            "total_processed": self._count_results()
        })

        return result

    def _handle_error(self, screenplay: str, start_time: float, error: str) -> Dict[str, Any]:
        """Trata erros de processamento"""

        duration = time.time() - start_time

        result = {
            "screenplay": screenplay,
            "mode": self.mode,
            "started": start_time,
            "completed": time.time(),
            "duration": duration,
            "success": False,
            "error": error,
            "model": self.model
        }

        print(f"   ❌ Erro fatal: {error[:100]}")

        self._save_result(result)
        self._update_metrics(result)
        self._update_status({
            "status": "error",
            "last_error": error,
            "last_failed": screenplay
        })

        return result

    def _save_result(self, result: Dict[str, Any]):
        """Salva resultado em arquivo JSONL"""
        with open(self.results_file, 'a') as f:
            f.write(json.dumps(result) + '\n')

    def _update_status(self, status: Dict[str, Any]):
        """Atualiza arquivo de status"""
        status["timestamp"] = datetime.now().isoformat()
        status["results_file"] = str(self.results_file)

        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)

    def _update_metrics(self, result: Dict[str, Any]):
        """Atualiza métricas de performance"""

        # Ler métricas existentes
        with open(self.metrics_file, 'r') as f:
            metrics = json.load(f)

        m = metrics[self.mode]

        # Atualizar contadores
        m["total_processed"] += 1
        m["total_time"] += result["duration"]

        if result["success"]:
            m["successes"] += 1
            if "model_info" in result:
                m["total_tokens"] += result["model_info"].get("eval_count", 0)
        else:
            m["errors"] += 1

        # Atualizar tempos
        m["min_time"] = min(m["min_time"], result["duration"])
        m["max_time"] = max(m["max_time"], result["duration"])
        m["avg_time"] = m["total_time"] / m["total_processed"]

        # Salvar métricas
        with open(self.metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)

    def _count_results(self) -> int:
        """Conta resultados no arquivo"""
        if not self.results_file.exists():
            return 0

        with open(self.results_file) as f:
            return sum(1 for _ in f)

    async def process_batch(self, screenplays: list) -> list:
        """
        Processa múltiplos roteiros em sequência

        Args:
            screenplays: Lista de tuplas (nome, conteúdo)

        Returns:
            Lista de resultados
        """
        results = []

        print(f"\n📚 Processando {len(screenplays)} roteiros em modo {self.mode}")
        print("=" * 60)

        for i, (name, content) in enumerate(screenplays, 1):
            print(f"\n[{i}/{len(screenplays)}]", end="")
            result = await self.process_screenplay(name, content)
            results.append(result)

            # Pausa entre processamentos para não sobrecarregar
            if i < len(screenplays):
                await asyncio.sleep(5 if self.mode == "ECO" else 2)

        # Resumo final
        successes = sum(1 for r in results if r["success"])
        total_time = sum(r["duration"] for r in results)

        print("\n" + "=" * 60)
        print(f"📊 RESUMO DO BATCH:")
        print(f"  • Sucesso: {successes}/{len(screenplays)}")
        print(f"  • Tempo total: {total_time:.1f}s")
        print(f"  • Tempo médio: {total_time/len(screenplays):.1f}s")
        print(f"  • Resultados em: {self.results_file}")

        return results


async def test_mixtral():
    """Função de teste do sistema mixtral"""

    from src.core.screenplay_library import get_screenplay_library

    print("🧪 TESTE DO SISTEMA mixtral mixtral")
    print("=" * 60)

    # Menu de seleção
    print("\nEscolha o modo de operação:")
    print("1. ECO (sustentável, ~45GB RAM)")
    print("2. DEDICATED (máximo, ~65GB RAM)")

    choice = input("\nOpção (1 ou 2): ").strip()
    mode = "DEDICATED" if choice == "2" else "ECO"

    # Criar processador
    processor = AsyncmixtralProcessor(mode=mode)

    # Pegar roteiro de teste
    library = get_screenplay_library()

    print("\n📚 Escolha o roteiro para testar:")
    print("1. Inception (complexo, sci-fi)")
    print("2. The Matrix (action, philosophy)")
    print("3. Teste rápido (mini roteiro)")

    script_choice = input("\nOpção (1, 2 ou 3): ").strip()

    if script_choice == "1":
        screenplay = "Inception"
        content = library.get_screenplay_text("Inception")
    elif script_choice == "2":
        screenplay = "The Matrix"
        content = library.get_screenplay_text("The Matrix")
    else:
        screenplay = "Quick Test"
        content = """INT. TEST SCENE - DAY

        A simple test scene to verify the mixtral model is working.

        PROTAGONIST
        This is a test of the deep learning system.

        ANTAGONIST
        Indeed. Let's see if it can analyze this properly.

        They shake hands. The system processes.

        FADE OUT."""

    if not content:
        content = "Test screenplay content for mixtral analysis."

    print(f"\n🚀 Iniciando teste em modo {mode}")
    print(f"📝 Roteiro: {screenplay}")
    print(f"📏 Tamanho: {len(content):,} caracteres")
    print("\n⏰ IMPORTANTE: Isso pode levar 5-20 minutos!")
    print("💡 Você pode monitorar o progresso em outro terminal:")
    print(f"   tail -f {processor.status_file}")
    print("\n" + "=" * 60)

    # Processar
    result = await processor.process_screenplay(screenplay, content)

    # Mostrar resultado
    print("\n" + "=" * 60)
    print("✅ TESTE COMPLETO!")
    print("\n📊 RESULTADO:")
    print(f"  • Sucesso: {result['success']}")
    print(f"  • Duração: {result['duration']:.1f}s")

    if result['success']:
        analysis = result.get('analysis', '')
        print(f"  • Análise: {len(analysis):,} caracteres")
        print(f"\n📝 PREVIEW (primeiros 500 chars):")
        print("-" * 40)
        print(analysis[:500])
        print("-" * 40)
    else:
        print(f"  • Erro: {result.get('error', 'Unknown')}")

    print(f"\n📄 Resultado completo salvo em:")
    print(f"   {processor.results_file}")
    print("\nDIGIMUNDO PRESENTE 🥷")


if __name__ == "__main__":
    # Executar teste
    asyncio.run(test_mixtral())