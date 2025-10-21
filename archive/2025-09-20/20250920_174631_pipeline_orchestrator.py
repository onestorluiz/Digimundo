#!/usr/bin/env python3
"""
Pipeline Orchestrator - Coordenador do Pipeline de Análise
Gerencia o fluxo entre os 4 estágios de análise
Fase 2.B - Implementação real
Fase 3.B - Integração com sistema de memória e cache
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass
from datetime import datetime
import json
import time
from pathlib import Path
import logging

# Importa os 4 engines
from .extract_engine import ExtractEngine, ScriptFormat, get_extract_engine
from .analyze_engine import AnalyzeEngine, get_analyze_engine
from .evaluate_engine import EvaluateEngine, ScriptCategory, get_evaluate_engine
from .synthesis_engine import SynthesisEngine, ReportFormat, get_synthesis_engine

# Importa sistema de memória (Fase 6.A - simplificado)
try:
    from .memory_simple import get_memory_cache, cache_analysis, get_cached_analysis
    # Mapeamento para compatibilidade
    cache_result = cache_analysis
    get_cached = get_cached_analysis
except ImportError:
    # Fallback se memory_simple não estiver disponível
    def cache_result(*args, **kwargs): pass
    def get_cached(*args, **kwargs): return None

# Cache Redis opcional
try:
    from .redis_cache import get_redis_cache, redis_get, redis_set
except ImportError:
    # Fallback se Redis não estiver disponível
    def redis_get(*args, **kwargs): return None
    def redis_set(*args, **kwargs): return True

# Define logger primeiro
logger = logging.getLogger(__name__)

# DigiLang para compressão de tokens
try:
    from .digilang_simple import get_digilang_compressor, get_token_optimizer
    digilang_enabled = True
except ImportError:
    digilang_enabled = False
    logger.warning("DigiLang não disponível - compressão de tokens desabilitada")

@dataclass
class PipelineConfig:
    """Configuração do pipeline"""
    script_category: ScriptCategory = ScriptCategory.FEATURE_FILM
    report_format: ReportFormat = ReportFormat.DETAILED
    cache_results: bool = True
    verbose: bool = False
    parallel_processing: bool = False
    save_intermediate: bool = False
    output_dir: Optional[Path] = None

@dataclass
class PipelineResult:
    """Resultado do pipeline completo"""
    success: bool
    report: Dict[str, Any]
    execution_time: float
    stages_completed: List[str]
    errors: List[str]
    intermediate_results: Optional[Dict[str, Any]] = None

class PipelineOrchestrator:
    """
    Orquestrador do pipeline de análise
    Coordena os 4 estágios: Extract → Analyze → Evaluate → Synthesize
    """
    
    def __init__(self, config: Optional[PipelineConfig] = None):
        """Inicializa orquestrador"""
        self.config = config or PipelineConfig()
        
        # Inicializa engines
        self.extract_engine = get_extract_engine()
        self.analyze_engine = get_analyze_engine()
        self.evaluate_engine = get_evaluate_engine()
        self.synthesis_engine = get_synthesis_engine()
        
        # Estado do pipeline
        self.current_stage = None
        self.stages_completed = []
        self.errors = []
        self.intermediate_results = {}
        
        # Callbacks para progresso
        self.progress_callbacks: List[Callable] = []
    
    def analyze_script(self, 
                       script_content: str,
                       script_format: ScriptFormat = ScriptFormat.PLAIN_TEXT,
                       config: Optional[PipelineConfig] = None) -> PipelineResult:
        """
        Analisa roteiro completo através do pipeline
        Retorna resultado consolidado
        """
        # Usa config específica ou padrão
        if config:
            self.config = config
        
        start_time = time.time()
        
        # Reset estado
        self.stages_completed = []
        self.errors = []
        self.intermediate_results = {}
        
        try:
            # Stage 1: Extract
            extraction_data = self._run_extraction(script_content, script_format)
            if not extraction_data:
                return self._create_error_result("Falha na extração", start_time)
            
            # Stage 2: Analyze
            analysis_data = self._run_analysis(extraction_data)
            if not analysis_data:
                return self._create_error_result("Falha na análise", start_time)
            
            # Stage 3: Evaluate
            evaluation_data = self._run_evaluation(extraction_data, analysis_data)
            if not evaluation_data:
                return self._create_error_result("Falha na avaliação", start_time)
            
            # Stage 4: Synthesize
            report = self._run_synthesis(extraction_data, analysis_data, evaluation_data)
            if not report:
                return self._create_error_result("Falha na síntese", start_time)
            
            # Salva resultados intermediários se configurado
            if self.config.save_intermediate and self.config.output_dir:
                self._save_intermediate_results()
            
            # Cria resultado final
            execution_time = time.time() - start_time
            
            return PipelineResult(
                success=True,
                report=report,
                execution_time=execution_time,
                stages_completed=self.stages_completed,
                errors=[],
                intermediate_results=self.intermediate_results if self.config.save_intermediate else None
            )
            
        except Exception as e:
            self.errors.append(f"Erro crítico no pipeline: {str(e)}")
            return self._create_error_result(str(e), start_time)
    
    def process_screenplay(self, text: str, use_ollama: bool = False, config: Optional[PipelineConfig] = None) -> PipelineResult:
        """
        Processa texto de roteiro diretamente (compatibilidade)
        Com suporte a DigiLang para compressão
        """
        # Aplica DigiLang se disponível e texto muito grande
        if digilang_enabled and len(text) > 10000:
            compressor = get_digilang_compressor()
            optimizer = get_token_optimizer()

            # Otimiza para contexto de LLM
            optimized_text = optimizer.optimize_for_context(text, max_tokens=8000)
            logger.info(f"DigiLang aplicado: {len(text)} -> {len(optimized_text)} bytes")
            text = optimized_text

        # Salva temporariamente para usar analyze_file
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(text)
            temp_path = f.name

        try:
            # Modifica config se use_ollama foi passado
            if config is None:
                config = PipelineConfig()

            # O parâmetro use_ollama não existe em PipelineConfig
            # mas podemos adicionar como atributo customizado
            result = self.analyze_file(temp_path, config)
        finally:
            os.unlink(temp_path)

        return result

    def analyze_file(self,
                    filepath: str,
                    config: Optional[PipelineConfig] = None) -> PipelineResult:
        """
        Analisa arquivo de roteiro com cache
        Detecta formato automaticamente
        """
        start_time = time.time()
        
        # Verifica cache primeiro (Fase 3.B)
        if self.config.cache_results:
            cached = get_cached(filepath)
            if cached:
                logger.info(f"Cache hit for {filepath}")
                return PipelineResult(
                    success=True,
                    report=cached,
                    execution_time=time.time() - start_time,
                    stages_completed=["cache"],
                    errors=[]
                )
        
        try:
            # Detecta formato
            path = Path(filepath)
            
            if path.suffix == '.fountain':
                script_format = ScriptFormat.FOUNTAIN
            elif path.suffix == '.fdx':
                script_format = ScriptFormat.FINAL_DRAFT
            elif path.suffix == '.pdf':
                script_format = ScriptFormat.PDF
            else:
                script_format = ScriptFormat.PLAIN_TEXT
            
            # Lê arquivo
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analisa
            result = self.analyze_script(content, script_format, config)
            
            # Cacheia resultado se bem-sucedido (Fase 3.B)
            if result.success and self.config.cache_results:
                processing_time = time.time() - start_time
                cache_result(filepath, result.report, processing_time)
                logger.info(f"Cached analysis for {filepath}")
            
            return result
            
        except Exception as e:
            return PipelineResult(
                success=False,
                report={},
                execution_time=time.time() - start_time,
                stages_completed=[],
                errors=[f"Erro lendo arquivo: {str(e)}"]
            )
    
    def _run_extraction(self, content: str, format: ScriptFormat) -> Optional[Dict[str, Any]]:
        """Executa estágio de extração"""
        self.current_stage = "extraction"
        self._notify_progress("Iniciando extração de elementos...", 0.0)
        
        try:
            if self.config.verbose:
                print("🔍 Estágio 1: Extraindo elementos do roteiro...")
            
            result = self.extract_engine.extract(content, format)
            
            if "error" in result:
                self.errors.append(f"Extração: {result['error']}")
                return None
            
            self.stages_completed.append("extraction")
            self.intermediate_results["extraction"] = result
            
            self._notify_progress("Extração completa", 0.25)
            
            if self.config.verbose:
                stats = result.get("statistics", {})
                print(f"   ✓ {stats.get('total_characters', 0)} personagens encontrados")
                print(f"   ✓ {stats.get('total_scenes', 0)} cenas identificadas")
                print(f"   ✓ {stats.get('total_dialogues', 0)} diálogos extraídos")
            
            return result
            
        except Exception as e:
            self.errors.append(f"Erro na extração: {str(e)}")
            return None
    
    def _run_analysis(self, extraction_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Executa estágio de análise"""
        self.current_stage = "analysis"
        self._notify_progress("Analisando estrutura narrativa...", 0.25)
        
        try:
            if self.config.verbose:
                print("📊 Estágio 2: Analisando estrutura e elementos...")
            
            result = self.analyze_engine.analyze(extraction_data)
            
            if "error" in result:
                self.errors.append(f"Análise: {result['error']}")
                return None
            
            self.stages_completed.append("analysis")
            self.intermediate_results["analysis"] = result
            
            self._notify_progress("Análise estrutural completa", 0.50)
            
            if self.config.verbose:
                print(f"   ✓ Estrutura de três atos identificada")
                print(f"   ✓ {len(result.get('character_arcs', []))} arcos de personagem analisados")
                print(f"   ✓ {len(result.get('themes', []))} temas identificados")
            
            return result
            
        except Exception as e:
            self.errors.append(f"Erro na análise: {str(e)}")
            return None
    
    def _run_evaluation(self, 
                       extraction_data: Dict[str, Any],
                       analysis_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Executa estágio de avaliação"""
        self.current_stage = "evaluation"
        self._notify_progress("Avaliando qualidade e padrões...", 0.50)
        
        try:
            if self.config.verbose:
                print("⭐ Estágio 3: Avaliando qualidade contra padrões...")
            
            result = self.evaluate_engine.evaluate(
                extraction_data,
                analysis_data,
                self.config.script_category
            )
            
            if "error" in result:
                self.errors.append(f"Avaliação: {result['error']}")
                return None
            
            self.stages_completed.append("evaluation")
            self.intermediate_results["evaluation"] = result
            
            self._notify_progress("Avaliação de qualidade completa", 0.75)
            
            if self.config.verbose:
                print(f"   ✓ Score geral: {result.get('overall_score', 0)}/100")
                print(f"   ✓ Grade: {result.get('grade', 'N/A')}")
                print(f"   ✓ {len(result.get('metrics', []))} métricas avaliadas")
            
            return result
            
        except Exception as e:
            self.errors.append(f"Erro na avaliação: {str(e)}")
            return None
    
    def _run_synthesis(self,
                      extraction_data: Dict[str, Any],
                      analysis_data: Dict[str, Any],
                      evaluation_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Executa estágio de síntese"""
        self.current_stage = "synthesis"
        self._notify_progress("Sintetizando relatório final...", 0.75)
        
        try:
            if self.config.verbose:
                print("📄 Estágio 4: Sintetizando resultados e gerando relatório...")
            
            result = self.synthesis_engine.synthesize(
                extraction_data,
                analysis_data,
                evaluation_data,
                self.config.report_format
            )
            
            if "error" in result:
                self.errors.append(f"Síntese: {result['error']}")
                return None
            
            self.stages_completed.append("synthesis")
            self.intermediate_results["synthesis"] = result
            
            self._notify_progress("Relatório finalizado", 1.0)
            
            if self.config.verbose:
                print(f"   ✓ Relatório {self.config.report_format} gerado")
                print(f"   ✓ {len(result.get('recommendations', {}).get('priority_actions', []))} recomendações")
                print(f"   ✓ Exportação disponível em {len(result.get('export_formats', []))} formatos")
            
            return result
            
        except Exception as e:
            self.errors.append(f"Erro na síntese: {str(e)}")
            return None
    
    def _create_error_result(self, error_msg: str, start_time: float) -> PipelineResult:
        """Cria resultado de erro"""
        return PipelineResult(
            success=False,
            report={
                "error": error_msg,
                "stages_completed": self.stages_completed,
                "errors": self.errors
            },
            execution_time=time.time() - start_time,
            stages_completed=self.stages_completed,
            errors=self.errors
        )
    
    def _save_intermediate_results(self) -> None:
        """Salva resultados intermediários"""
        if not self.config.output_dir:
            return
        
        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Salva cada estágio
        for stage, data in self.intermediate_results.items():
            filepath = output_dir / f"{stage}_{timestamp}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_progress_callback(self, callback: Callable[[str, float], None]) -> None:
        """Adiciona callback de progresso"""
        self.progress_callbacks.append(callback)
    
    def _notify_progress(self, message: str, progress: float) -> None:
        """Notifica callbacks de progresso"""
        for callback in self.progress_callbacks:
            try:
                callback(message, progress)
            except:
                pass  # Ignora erros em callbacks
    
    def export_report(self, result: PipelineResult, format: str, filepath: str) -> bool:
        """
        Exporta relatório em formato específico
        Formatos: json, html, markdown, pdf
        """
        try:
            if not result.success:
                return False
            
            report = result.report
            
            if format == "json":
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
            
            elif format == "html":
                html_content = self.synthesis_engine.export_to_html(report)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            
            elif format == "markdown":
                md_content = self.synthesis_engine.export_to_markdown(report)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(md_content)
            
            elif format == "pdf":
                # PDF requer biblioteca externa (não implementado)
                self.errors.append("Exportação PDF não implementada ainda")
                return False
            
            else:
                self.errors.append(f"Formato não suportado: {format}")
                return False
            
            return True
            
        except Exception as e:
            self.errors.append(f"Erro exportando: {str(e)}")
            return False
    
    def get_stage_info(self) -> Dict[str, Any]:
        """Retorna informações sobre estágios do pipeline"""
        return {
            "stages": [
                {
                    "name": "extraction",
                    "description": "Extrai personagens, cenas, diálogos",
                    "completed": "extraction" in self.stages_completed
                },
                {
                    "name": "analysis",
                    "description": "Analisa estrutura, arcos, ritmo",
                    "completed": "analysis" in self.stages_completed
                },
                {
                    "name": "evaluation",
                    "description": "Avalia qualidade contra padrões",
                    "completed": "evaluation" in self.stages_completed
                },
                {
                    "name": "synthesis",
                    "description": "Sintetiza relatório final",
                    "completed": "synthesis" in self.stages_completed
                }
            ],
            "current_stage": self.current_stage,
            "stages_completed": len(self.stages_completed),
            "total_stages": 4
        }
    
    def validate_pipeline(self) -> Dict[str, bool]:
        """Valida que todos os componentes estão funcionando"""
        validation = {
            "extract_engine": False,
            "analyze_engine": False,
            "evaluate_engine": False,
            "synthesis_engine": False,
            "pipeline_ready": False
        }
        
        try:
            # Testa cada engine
            test_content = "INT. CASA - DIA\n\nJOHN entra.\n\nJOHN\nOlá mundo!"
            
            # Teste extração
            extraction = self.extract_engine.extract(test_content)
            validation["extract_engine"] = "error" not in extraction
            
            if validation["extract_engine"]:
                # Teste análise
                analysis = self.analyze_engine.analyze(extraction)
                validation["analyze_engine"] = "error" not in analysis
                
                if validation["analyze_engine"]:
                    # Teste avaliação
                    evaluation = self.evaluate_engine.evaluate(extraction, analysis)
                    validation["evaluate_engine"] = "error" not in evaluation
                    
                    if validation["evaluate_engine"]:
                        # Teste síntese
                        synthesis = self.synthesis_engine.synthesize(
                            extraction, analysis, evaluation
                        )
                        validation["synthesis_engine"] = "error" not in synthesis
            
            # Pipeline pronto se todos os engines funcionam
            validation["pipeline_ready"] = all([
                validation["extract_engine"],
                validation["analyze_engine"],
                validation["evaluate_engine"],
                validation["synthesis_engine"]
            ])
            
        except Exception as e:
            self.errors.append(f"Erro na validação: {str(e)}")
        
        return validation

# Singleton global
_orchestrator_instance: Optional[PipelineOrchestrator] = None

def get_pipeline_orchestrator(config: Optional[PipelineConfig] = None) -> PipelineOrchestrator:
    """Retorna instância singleton do orquestrador"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = PipelineOrchestrator(config)
    return _orchestrator_instance

__all__ = ["PipelineOrchestrator", "PipelineConfig", "PipelineResult", "get_pipeline_orchestrator"]