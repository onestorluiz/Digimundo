#!/usr/bin/env python3
"""
🔄 PIPELINE QUÁDRUPLO ROBUSTO - 4 Estágios com Controle de Concorrência
Sistema de processamento com fallback chain, timeouts e garantia de resposta
"""

import json
import subprocess
import threading
import time
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
import re
import sys
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class QuadruplePipeline:
    """Pipeline de 4 estágios com controle robusto de concorrência e fallback"""
    
    # --- FixPack:S2 begin (timeout limits) ---
    # Timeouts por modo (em segundos) - reduzidos para evitar travamentos
    TIMEOUT_MAPS = {
        "normal": {
            "extract": 10,      # Reduzido de 30
            "analyze": 15,      # Reduzido de 60
            "evaluate": 20,     # Reduzido de 90
            "synthesize": 15    # Reduzido de 60
        },
        "deep": {
            "extract": 20,      # Reduzido de 60
            "analyze": 30,      # Reduzido de 120
            "evaluate": 40,     # Reduzido de 180
            "synthesize": 30    # Reduzido de 120
        }
    }
    
    # Timeout máximo absoluto para o pipeline completo
    MAX_PIPELINE_TIMEOUT = 120  # 2 minutos máximo
    # --- FixPack:S2 end (timeout limits) ---
    
    # Fallback chain por tamanho de modelo
    FALLBACK_CHAINS = {
        "extract": ["deepseek-r1:7b", "llama3.2:3b", "gemma2:2b", "tinyllama"],
        "analyze": ["deepseek-r1:32b", "mistral:instruct", "mistral:7b", "llama3.2:3b"],
        "evaluate": ["deepseek-r1:70b", "deepseek-r1:32b", "scripturemon-maestro", "mistral:instruct", "llama3.2:3b"],
        "synthesize": ["deepseek-r1:32b", "scripturemon-soulos", "mistral:7b", "llama3.2:3b"]
    }
    
    # Classificação de modelos por peso
    MODEL_WEIGHTS = {
        "deepseek-r1:70b": "heavy",
        "deepseek-r1:32b": "heavy", 
        "scripturemon-maestro": "medium",
        "scripturemon-soulos": "medium",
        "mistral:instruct": "medium",
        "mistral:7b": "light",
        "deepseek-r1:7b": "light",
        "llama3.2:3b": "light",
        "gemma2:2b": "light",
        "tinyllama": "light"
    }
    
    def __init__(self, settings: Optional[Dict] = None):
        """Inicializa pipeline quádruplo robusto"""
        self.settings = settings or {}
        self.available_models = self._check_available_models()
        
        # Executor com controle de workers
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # --- FixPack:S2 begin (concurrency limits) ---
        # Semáforos para controle de concorrência (mais restritivos)
        self.heavy_semaphore = threading.Semaphore(1)  # Max 1 modelo pesado
        self.light_semaphore = threading.Semaphore(1)  # Reduzido para 1 (era 2)
        self.global_semaphore = threading.Semaphore(2)  # Máximo 2 operações totais
        # --- FixPack:S2 end (concurrency limits) ---
        
        # Estatísticas
        self.pipeline_stats = {
            "runs": 0,
            "total_time": 0,
            "fallbacks_used": [],
            "timeouts": [],
            "stage_durations": {}
        }
        
        logger.info(f"🔄 Pipeline Quádruplo Robusto inicializado")
        logger.info(f"   Modelos disponíveis: {len(self.available_models)}")
        
    def _check_available_models(self) -> Dict[str, bool]:
        """Verifica quais modelos estão disponíveis no Ollama"""
        available = {}
        
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines[1:]:  # Pula header
                    if line:
                        model_name = line.split()[0]
                        available[model_name] = True
        except Exception as e:
            logger.warning(f"Erro ao verificar modelos: {e}")
        
        return available
    
    # ============ PHASE 2 COMPATIBILITY HELPERS ============
    @contextmanager
    def acquire_sem(self, semaphore, timeout=1.0):
        """Context manager for safe semaphore acquisition with timeout"""
        acquired = False
        try:
            acquired = semaphore.acquire(timeout=timeout)
            if not acquired:
                raise TimeoutError(f"Could not acquire semaphore within {timeout}s")
            yield acquired
        finally:
            if acquired:
                semaphore.release()
    
    def _run_stage_with_model(self, stage: str, prompt: str, model: str, 
                              timeout: int, context: Dict) -> Dict:
        """
        Execute a stage with proper error handling and semaphore management.
        Maximum 2 levels of try/except as required.
        
        Returns:
            Dict with keys: success, output, error, duration_ms
        """
        start_time = time.time()
        result = {
            "success": False,
            "output": None,
            "error": None,
            "duration_ms": 0
        }
        
        # Determine semaphore based on model weight
        weight = self.MODEL_WEIGHTS.get(model, "light")
        stage_semaphore = self.heavy_semaphore if weight == "heavy" else self.light_semaphore
        
        # Level 1 try: Global semaphore
        try:
            with self.acquire_sem(self.global_semaphore, timeout=0.5):
                # Level 2 try: Stage semaphore and execution
                try:
                    with self.acquire_sem(stage_semaphore, timeout=1.0):
                        # Build command
                        cmd = ["ollama", "run", model]
                        
                        # Execute subprocess
                        process = subprocess.Popen(
                            cmd,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        
                        # Communicate with timeout
                        stdout, stderr = process.communicate(input=prompt, timeout=timeout)
                        
                        if process.returncode == 0 and stdout:
                            result["success"] = True
                            result["output"] = stdout.strip()
                        else:
                            result["error"] = f"Model returned error: {stderr or 'No output'}"
                            
                except subprocess.TimeoutExpired:
                    process.kill()
                    result["error"] = f"Stage {stage} timed out after {timeout}s"
                    self.pipeline_stats["timeouts"].append(stage)
                    
                except TimeoutError as e:
                    result["error"] = f"Semaphore timeout: {e}"
                    
                except Exception as e:
                    result["error"] = f"Execution error: {e}"
                    
        except TimeoutError as e:
            result["error"] = f"Global semaphore timeout: {e}"
            
        except Exception as e:
            result["error"] = f"Unexpected error: {e}"
        
        # Calculate duration
        result["duration_ms"] = int((time.time() - start_time) * 1000)
        
        # Log result
        if result["success"]:
            logger.info(f"✅ [{stage}] Success with {model} in {result['duration_ms']}ms")
        else:
            logger.warning(f"❌ [{stage}] Failed with {model}: {result['error']}")
        
        return result
    # ============ END PHASE 2 HELPERS ============
    
    def _detect_deep_mode(self, input_text: str) -> bool:
        """Detecta se deve usar modo deep baseado em palavras-chave ou tamanho"""
        # --- FixPack:S2 begin (deep trigger) ---
        # Palavras-chave para deep mode (mais específicas)
        deep_keywords = [
            "análise profunda", "análise detalhada", "estudo profundo",
            "analisar profundamente", "investigar detalhadamente",
            "examinar minuciosamente", "explorar completamente"
        ]
        
        text_lower = input_text.lower()
        
        # Verifica frases completas (não palavras isoladas)
        for keyword in deep_keywords:
            if keyword in text_lower:
                logger.info(f"Deep mode triggered by phrase: '{keyword}'")
                return True
        
        # Verifica comandos explícitos
        if text_lower.startswith("/deep") or text_lower.startswith("!deep"):
            logger.info("Deep mode triggered by explicit command")
            return True
        
        # Verifica tamanho E complexidade (>500 caracteres + múltiplas linhas)
        if len(input_text) > 500 and input_text.count('\n') > 3:
            logger.info(f"Deep mode triggered by complexity: {len(input_text)} chars, {input_text.count(chr(10))} lines")
            return True
        
        logger.info("Using normal mode (no deep triggers found)")
        return False
        # --- FixPack:S2 end (deep trigger) ---
    
    def _get_model_for_stage(self, stage: str) -> Tuple[str, str]:
        """Seleciona modelo disponível para o estágio com fallback"""
        fallback_chain = self.FALLBACK_CHAINS.get(stage, ["llama3.2:3b"])
        
        for model in fallback_chain:
            # Verifica se modelo existe no sistema
            if model in self.available_models or model.split(':')[0] in str(self.available_models):
                return model, "primary"
        
        # Se nenhum modelo da chain estiver disponível, tenta qualquer um
        for model in ["llama3.2:3b", "mistral:latest", "gemma2:2b"]:
            if model in self.available_models or model.split(':')[0] in str(self.available_models):
                logger.warning(f"Using emergency fallback {model} for {stage}")
                return model, "emergency"
        
        # Fallback final
        return "llama3.2:3b", "fallback"
    
    def _execute_stage(self, stage: str, prompt: str, timeout: int, context: Dict) -> Dict:
        """Executa um estágio do pipeline com controle de concorrência"""
        model, selection_type = self._get_model_for_stage(stage)
        
        # Log do início do estágio
        logger.info(f"[{stage}] Starting - Model: {model}, Timeout: {timeout}s")
        
        # Prepara prompt baseado no estágio
        stage_prompts = {
            "extract": f"Extract key concepts and structure from this text. Be concise:\n\n{prompt}",
            "analyze": f"Analyze the narrative structure and techniques. Context: {context.get('extract', '')}\n\n{prompt}",
            "evaluate": f"Evaluate critically, comparing to cinema masters. Context: {context.get('analyze', '')}\n\n{prompt}",
            "synthesize": f"Synthesize insights and provide final analysis. Context: {context.get('evaluate', '')}\n\n{prompt}"
        }
        
        full_prompt = stage_prompts.get(stage, prompt)
        
        # Use the new _run_stage_with_model helper
        result = self._run_stage_with_model(stage, full_prompt, model, timeout, context)
        
        # Add metadata to result
        result["stage"] = stage
        result["model"] = model
        result["selection_type"] = selection_type
        
        # Try fallback if primary failed and not already a fallback
        if not result["success"] and selection_type != "fallback":
            logger.info(f"[{stage}] Attempting fallback due to error")
            fallback_result = self._try_fallback(stage, prompt, timeout // 2, context)
            if fallback_result["success"]:
                result = fallback_result
                self.pipeline_stats["fallbacks_used"].append({
                    "stage": stage,
                    "from": model,
                    "to": fallback_result.get("model", "unknown"),
                    "reason": result.get("error", "Unknown error")
                })
        
        # Log final result
        status = "SUCCESS" if result["success"] else "FAILED"
        logger.info(f"[{stage}] {status} - Duration: {result.get('duration_ms', 0)}ms")
        
        return result
    
    def _try_fallback(self, stage: str, prompt: str, timeout: int, context: Dict) -> Dict:
        """Tenta executar com modelo de fallback"""
        fallback_chain = self.FALLBACK_CHAINS.get(stage, ["llama3.2:3b"])
        
        for fallback_model in fallback_chain[1:]:  # Pula o primeiro (já tentado)
            try:
                logger.info(f"[{stage}] Trying fallback: {fallback_model}")
                
                cmd = ["ollama", "run", fallback_model]
                process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate(input=prompt, timeout=timeout)
                
                if process.returncode == 0 and stdout.strip():
                    return {
                        "stage": stage,
                        "model": fallback_model,
                        "selection_type": "fallback",
                        "success": True,
                        "output": stdout.strip(),
                        "error": None
                    }
            except:
                continue
        
        return {
            "stage": stage,
            "model": "none",
            "selection_type": "failed",
            "success": False,
            "output": "",
            "error": "All fallbacks failed"
        }
    
    def run_pipeline(self, input_text: str, mode: str = "auto") -> str:
        """
        Executa o pipeline quádruplo completo
        
        Args:
            input_text: Texto de entrada
            mode: "auto", "deep" ou "normal"
            
        Returns:
            Texto processado final (nunca vazio)
        """
        start_time = time.time()
        
        # Determina modo
        if mode == "auto":
            mode = "deep" if self._detect_deep_mode(input_text) else "normal"
        
        logger.info(f"=== STARTING QUADRUPLE PIPELINE - Mode: {mode} ===")
        logger.info(f"Input length: {len(input_text)} chars")
        
        # Seleciona timeouts
        timeouts = self.TIMEOUT_MAPS[mode]
        
        # Contexto compartilhado entre estágios
        context = {}
        results = {}
        
        # Executa os 4 estágios
        stages = ["extract", "analyze", "evaluate", "synthesize"]
        
        for stage in stages:
            # --- FixPack:S2 begin (timeout check) ---
            # Verifica se já excedeu o tempo máximo do pipeline
            elapsed = time.time() - start_time
            if elapsed > self.MAX_PIPELINE_TIMEOUT:
                logger.warning(f"Pipeline timeout exceeded ({elapsed:.1f}s > {self.MAX_PIPELINE_TIMEOUT}s)")
                break
            # --- FixPack:S2 end (timeout check) ---
            
            logger.info(f">>> Stage: {stage}")
            result = self._execute_stage(
                stage=stage,
                prompt=input_text,
                timeout=min(timeouts[stage], self.MAX_PIPELINE_TIMEOUT - elapsed),  # Ajusta timeout
                context=context
            )
            
            results[stage] = result
            
            # Adiciona output ao contexto para próximo estágio
            if result["success"]:
                context[stage] = result["output"][:500]  # Limita contexto
            
            # Log intermediário
            logger.info(f"[{stage}] Output length: {len(result['output'])} chars")
        
        # Sintetiza resposta final
        final_response = self._synthesize_final_response(results, input_text)
        
        # Estatísticas
        total_duration = int((time.time() - start_time) * 1000)
        self.pipeline_stats["runs"] += 1
        self.pipeline_stats["total_time"] += total_duration
        
        # Log final
        logger.info(f"=== PIPELINE COMPLETE - Duration: {total_duration}ms ===")
        logger.info(f"Final response length: {len(final_response)} chars")
        
        # Log de fallbacks usados
        if self.pipeline_stats["fallbacks_used"]:
            logger.info(f"Fallbacks used: {len(self.pipeline_stats['fallbacks_used'])}")
            for fb in self.pipeline_stats["fallbacks_used"][-5:]:  # Últimos 5
                logger.info(f"  - {fb['stage']}: {fb['from']} → {fb['to']} ({fb['reason'][:50]})")
        
        return final_response
    
    def _synthesize_final_response(self, results: Dict, original_input: str) -> str:
        """
        Sintetiza resposta final garantindo que nunca retorne vazio
        """
        # Tenta usar o output do synthesize
        if results.get("synthesize", {}).get("success"):
            response = results["synthesize"]["output"]
            if response and len(response) > 50:
                return response
        
        # Fallback: combina outputs disponíveis
        combined = []
        
        for stage in ["extract", "analyze", "evaluate"]:
            if results.get(stage, {}).get("success"):
                output = results[stage]["output"]
                if output:
                    combined.append(f"[{stage.upper()}]\n{output}\n")
        
        if combined:
            return "\n".join(combined)
        
        # Fallback final: resposta padrão útil
        return self._generate_default_response(original_input)
    
    def _generate_default_response(self, input_text: str) -> str:
        """Gera resposta padrão útil quando pipeline falha"""
        # --- FixPack:S2 begin (guaranteed response) ---
        if len(input_text) < 50:
            return f"""Analisando: "{input_text[:100]}"

Estou processando sua solicitação. Para uma análise mais completa, considere:
• Adicionar contexto específico sobre o que deseja analisar
• Mencionar aspectos técnicos ou narrativos de interesse
• Indicar se deseja análise profunda ou resumida

*Pipeline processado com limitações temporárias.*"""
        else:
            # Extrai primeiras palavras para contexto
            first_words = ' '.join(input_text.split()[:20])
            return f"""📊 **Análise Processada**

**Texto recebido:** "{first_words}..."

Seu texto foi processado através do pipeline de análise. Devido a limitações temporárias,
apresento uma síntese básica:

• **Estrutura:** Texto com {len(input_text)} caracteres
• **Complexidade:** {'Alta' if len(input_text) > 500 else 'Média'}
• **Processamento:** Pipeline parcial executado

Para resultados completos, tente novamente ou simplifique a consulta.

*Resposta gerada via fallback do sistema.*"""
        # --- FixPack:S2 end (guaranteed response) ---
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do pipeline"""
        return {
            "runs": self.pipeline_stats["runs"],
            "total_time_ms": self.pipeline_stats["total_time"],
            "avg_time_ms": self.pipeline_stats["total_time"] / max(1, self.pipeline_stats["runs"]),
            "timeouts": len(self.pipeline_stats["timeouts"]),
            "fallbacks": len(self.pipeline_stats["fallbacks_used"]),
            "available_models": len(self.available_models)
        }


# Função helper para uso direto
def run_pipeline(input_text: str, mode: str = "auto") -> str:
    """
    Função helper para executar o pipeline
    
    Args:
        input_text: Texto para processar
        mode: "auto", "deep" ou "normal"
        
    Returns:
        Texto processado (nunca vazio)
    """
    pipeline = QuadruplePipeline()
    return pipeline.run_pipeline(input_text, mode)


# --- FixPack:S2 begin (enhanced pipeline) ---
import hashlib
import contextlib

DEEP_REGEX = re.compile(r"\bprofund[oa]\b|\bdetalhad[oa]\b", re.IGNORECASE)

def _is_heavy_model(name: str) -> bool:
    """Check if model is resource-heavy"""
    n = (name or "").lower()
    return any(t in n for t in ["32b", "70b", "65b", "ultimate", "deepseek"]) or "13b" in n or "14b" in n

def decide_mode(user_input: str) -> str:
    """Enhanced mode detection"""
    if DEEP_REGEX.search(user_input or "") or (user_input and len(user_input) > 300):
        return "deep"
    return "normal"

def stage_timeouts(mode: str):
    """Get timeout values per mode"""
    if mode == "deep":
        return {"extract": 60, "analyze": 120, "evaluate": 180, "synthesize": 120}
    return {"extract": 30, "analyze": 60, "evaluate": 90, "synthesize": 60}

HEAVY_SEM = asyncio.Semaphore(1)  # heavy <= 1

async def _run_model(cmd, prompt, timeout):
    """Run model with timeout control"""
    import subprocess
    try:
        if timeout is None:
            result = subprocess.run(cmd, input=prompt, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        raise RuntimeError(f"model failed: {cmd}")
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Model timeout: {timeout}s")
    except Exception as e:
        raise RuntimeError(f"Model error: {e}")

async def run_stage(stage, models, prompt, timeout):
    """Run stage with fallback chain"""
    for m in models:
        try:
            if _is_heavy_model(m):
                async with HEAVY_SEM:
                    return await _run_model(["ollama", "run", m], prompt, timeout)
            else:
                return await _run_model(["ollama", "run", m], prompt, timeout)
        except Exception as e:
            logger.debug(f"Model {m} failed for {stage}: {e}")
            continue  # fallback to next model
    raise RuntimeError(f"all models failed for stage={stage}")

def fallback_chain(mode: str, available: list) -> dict:
    """Priority: 70B→32B→14B→8B→3B (only those in 'available')"""
    pref = {
        "extract": ["llama3.2:3b", "llama3.1:8b", "mistral:instruct", "deepseek-r1:14b", "deepseek-r1:32b", "deepseek-r1:70b"],
        "analyze": ["mistral:instruct", "deepseek-r1:14b", "deepseek-r1:32b", "deepseek-r1:70b"],
        "evaluate": ["deepseek-r1:32b", "deepseek-r1:70b", "mistral:instruct", "llama3.1:8b"],
        "synthesize": ["deepseek-r1:14b", "deepseek-r1:32b", "mistral:instruct", "llama3.2:3b"]
    }
    chain = {}
    for st, lst in pref.items():
        chain[st] = [m for m in lst if m in available]
    return chain

async def run_pipeline_async(user_input: str, available_models: list = None) -> str:
    """Enhanced async pipeline with guaranteed response"""
    if available_models is None:
        # Try to get available models
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                available_models = [line.split()[0] for line in lines if line.strip()]
            else:
                available_models = ["llama3.2:3b", "mistral:instruct"]
        except:
            available_models = ["llama3.2:3b", "mistral:instruct"]
    
    mode = decide_mode(user_input or "")
    to = stage_timeouts(mode)
    chain = fallback_chain(mode, available_models or [])
    
    stages = ["extract", "analyze", "evaluate", "synthesize"]
    outputs = {}
    start = time.time()
    
    for st in stages:
        models = chain.get(st) or []
        if not models:
            continue
        try:
            outputs[st] = await run_stage(st, models, f"[{st.upper()}]\n{user_input}", to[st])
        except Exception as e:
            outputs[st] = f"[{st}] fallback: {type(e).__name__}"
    
    # Final synthesis guaranteed
    final = outputs.get("synthesize") or outputs.get("evaluate") or outputs.get("analyze") or outputs.get("extract")
    if not final or not str(final).strip():
        final = "Desculpe, não consegui processar completamente. Baseado no que tenho, sugiro seguir com uma análise incremental."
    
    elapsed = time.time() - start
    logger.info(f"Pipeline completed in {elapsed:.1f}s - Mode: {mode}")
    return final

# Sync wrapper for async pipeline
def run_enhanced_pipeline(user_input: str) -> str:
    """Synchronous wrapper for enhanced pipeline"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    try:
        return loop.run_until_complete(run_pipeline_async(user_input))
    except Exception as e:
        logger.error(f"Enhanced pipeline error: {e}")
        return "Pipeline processado com limitações. Por favor, tente novamente com uma consulta mais simples."
# --- FixPack:S2 end (enhanced pipeline) ---


if __name__ == "__main__":
    # Teste direto
    import sys
    
    if len(sys.argv) > 1:
        test_input = " ".join(sys.argv[1:])
    else:
        test_input = "Explique a importância do roteiro no cinema."
    
    print(f"\n🔄 Testing Quadruple Pipeline")
    print(f"Input: {test_input}")
    print("-" * 60)
    
    result = run_pipeline(test_input)
    
    print("\nResult:")
    print(result)
    print("-" * 60)