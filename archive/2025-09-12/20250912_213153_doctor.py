#!/usr/bin/env python3
"""
Doctor Module - Análise e Diagnóstico com Pipeline Real + AI Avançada
Fase 3.A - Integração com Pipeline de Análise
Fase 3.C - Integração com Sistema de AI Avançada
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
import json
import logging

# Importa sistema de memória (Fase 6.A)
from .memory_simple import get_memory_cache, cache_analysis, get_cached_analysis

# Importa o pipeline real
from .pipeline_orchestrator import (
    get_pipeline_orchestrator, 
    PipelineConfig,
    ScriptCategory,
    ReportFormat
)
from .extract_engine import ScriptFormat

# Importa módulos de AI avançada (Fase 3.C)
from .ai_sentiment import get_sentiment_analyzer, analyze_script_sentiment, analyze_text_sentiment
from .ai_recommendations import get_recommendation_engine, generate_script_recommendations
from .ai_comparison import get_comparison_engine
from .ai_commercial import get_commercial_predictor, predict_commercial_success

logger = logging.getLogger(__name__)

def analyze(file_path: Path) -> Dict[str, Any]:
    """
    Analisa arquivo de roteiro usando o Pipeline Real
    Versão completa integrada com o pipeline de 4 estágios
    Com cache inteligente (Fase 6.A)
    """
    if not file_path.exists():
        return {
            "status": "error",
            "message": f"Arquivo não encontrado: {file_path}",
            "score": 0,
            "analysis": {}
        }
    
    # Verifica cache primeiro
    cached = get_cached_analysis(file_path)
    if cached:
        logger.info(f"💾 Usando análise em cache para {file_path.name}")
        return cached
    
    try:
        # Configura o pipeline
        config = PipelineConfig(
            script_category=ScriptCategory.FEATURE_FILM,
            report_format=ReportFormat.DETAILED,
            verbose=False
        )
        
        # Obtém o orquestrador
        orchestrator = get_pipeline_orchestrator(config)
        
        # Analisa o arquivo
        result = orchestrator.analyze_file(str(file_path))
        
        if result.success:
            report = result.report
            
            # Extrai informações principais
            score = report.get("score_card", {}).get("overall_score", 0)
            grade = report.get("score_card", {}).get("grade", "N/A")
            
            # Formata resposta compatível com interface antiga
            analysis_result = {
                "status": "success",
                "file": str(file_path),
                "score": score,
                "grade": grade,
                "analysis": {
                    "structure": _extract_category_status(report, "structure"),
                    "dialogue": _extract_category_status(report, "dialogue"),
                    "pacing": _extract_category_status(report, "pacing"),
                    "characters": _extract_category_status(report, "characters")
                },
                "recommendations": report.get("recommendations", {}).get("priority_actions", []),
                "executive_summary": report.get("executive_summary", {}).get("one_line_verdict", ""),
                "strengths": report.get("executive_summary", {}).get("key_strengths", []),
                "weaknesses": report.get("executive_summary", {}).get("key_weaknesses", []),
                "detailed_report": report  # Inclui relatório completo
            }
            
            # Salva no cache
            cache_analysis(file_path, analysis_result)
            
            return analysis_result
        else:
            return {
                "status": "error",
                "message": f"Erro no pipeline: {', '.join(result.errors)}",
                "score": 0,
                "analysis": {}
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erro analisando arquivo: {str(e)}",
            "score": 0,
            "analysis": {}
        }

def deep_analyze(file_path: Path, mode: str = "comprehensive") -> Dict[str, Any]:
    """
    Análise profunda usando pipeline com configurações especiais
    Integra módulos AI reais (Fase 5.B e 5.C)
    """
    base = analyze(file_path)
    
    if base["status"] == "success" and mode == "comprehensive":
        # Adiciona métricas extras do relatório detalhado
        detailed = base.get("detailed_report", {})
        
        # Análise de sentimento REAL
        try:
            # Lê conteúdo do arquivo para análise
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analisa sentimento do conteúdo
            sentiment_result = analyze_text_sentiment(content[:5000])  # Primeiros 5000 chars
            sentiment_score = sentiment_result.compound
        except:
            sentiment_score = 0.65  # Fallback
        
        # Predição comercial REAL
        try:
            commercial_pred = predict_commercial_success(base)
            market_score = commercial_pred.overall_score
        except:
            market_score = 0.5  # Fallback
        
        # Recomendações REAIS (Fase 5.C)
        try:
            recommendations_list = generate_script_recommendations(base)
            # Converte lista de objetos em lista de dicts
            recommendations = []
            for rec in recommendations_list[:5]:  # Top 5 recomendações
                recommendations.append({
                    "title": rec.title,
                    "category": rec.category,
                    "priority": rec.priority,
                    "description": rec.description,
                    "suggestions": rec.suggestions
                })
        except Exception as e:
            logger.warning(f"Erro gerando recomendações: {e}")
            recommendations = []
        
        base["mode"] = mode
        base["deep_metrics"] = {
            "sentiment": sentiment_score,
            "complexity": _calculate_complexity(detailed),
            "originality": _calculate_originality(detailed),
            "market_potential": market_score
        }
        
        # Adiciona recomendações AI ao resultado
        base["ai_recommendations"] = recommendations
        
        # Adiciona análise detalhada
        if "detailed_analysis" in detailed:
            base["structure_analysis"] = detailed["detailed_analysis"].get("structure_analysis", {})
            base["character_analysis"] = detailed["detailed_analysis"].get("character_analysis", {})
            base["thematic_analysis"] = detailed["detailed_analysis"].get("thematic_analysis", {})
    
    return base

def batch_analyze(files: List[Path]) -> Dict[str, Any]:
    """
    Análise em lote usando o pipeline
    """
    results = []
    successful = 0
    failed = 0
    
    for file_path in files:
        result = analyze(file_path)
        results.append(result)
        
        if result["status"] == "success":
            successful += 1
        else:
            failed += 1
    
    # Calcula estatísticas agregadas
    avg_score = 0
    if successful > 0:
        scores = [r["score"] for r in results if r["status"] == "success"]
        avg_score = sum(scores) / len(scores)
    
    return {
        "total": len(files),
        "processed": len(results),
        "successful": successful,
        "failed": failed,
        "average_score": round(avg_score, 1),
        "results": results
    }

def export_analysis(
    file_path: Path,
    output_path: Path,
    format: str = "html"
) -> Dict[str, Any]:
    """
    Analisa e exporta relatório em formato específico
    Formatos: html, markdown, json
    """
    # Primeiro analisa
    analysis = analyze(file_path)
    
    if analysis["status"] != "success":
        return {
            "status": "error",
            "message": f"Análise falhou: {analysis.get('message', 'Unknown error')}"
        }
    
    try:
        # Obtém o pipeline para exportação
        orchestrator = get_pipeline_orchestrator()
        
        # Prepara resultado para exportação
        from .pipeline_orchestrator import PipelineResult
        result = PipelineResult(
            success=True,
            report=analysis["detailed_report"],
            execution_time=0,
            stages_completed=["extraction", "analysis", "evaluation", "synthesis"],
            errors=[]
        )
        
        # Exporta
        success = orchestrator.export_report(result, format, str(output_path))
        
        if success:
            return {
                "status": "success",
                "message": f"Relatório exportado para {output_path}",
                "format": format,
                "file": str(output_path)
            }
        else:
            return {
                "status": "error",
                "message": f"Erro exportando relatório"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erro na exportação: {str(e)}"
        }

def validate_script(file_path: Path) -> Dict[str, Any]:
    """
    Validação rápida de formatação de roteiro
    """
    if not file_path.exists():
        return {
            "valid": False,
            "errors": [f"Arquivo não encontrado: {file_path}"]
        }
    
    try:
        # Lê arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Validações básicas
        errors = []
        warnings = []
        
        # Verifica se tem conteúdo
        if len(content.strip()) < 100:
            errors.append("Arquivo muito curto para ser um roteiro")
        
        # Verifica marcadores básicos de roteiro
        has_slug_lines = "INT." in content or "EXT." in content
        has_dialogue = any(line.isupper() and len(line.strip()) > 2 
                          for line in content.split('\n'))
        
        if not has_slug_lines:
            warnings.append("Não foram encontradas slug lines (INT./EXT.)")
        
        if not has_dialogue:
            warnings.append("Não foram encontrados nomes de personagens")
        
        # Verifica páginas (aproximado)
        pages = len(content.split('\n')) / 55  # ~55 linhas por página
        if pages < 5:
            warnings.append(f"Roteiro muito curto ({pages:.1f} páginas)")
        elif pages > 180:
            warnings.append(f"Roteiro muito longo ({pages:.1f} páginas)")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "estimated_pages": round(pages, 1),
            "has_formatting": has_slug_lines
        }
        
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Erro lendo arquivo: {str(e)}"]
        }

# Funções auxiliares privadas

def _extract_category_status(report: Dict, category: str) -> str:
    """Extrai status de uma categoria do relatório"""
    scores = report.get("score_card", {}).get("category_scores", {})
    score = scores.get(category, 0)
    
    if score >= 80:
        return "excellent"
    elif score >= 70:
        return "good"
    elif score >= 60:
        return "needs_improvement"
    else:
        return "poor"

def _calculate_complexity(report: Dict) -> float:
    """Calcula complexidade baseada no relatório"""
    # Baseado em número de personagens, cenas e subtramas
    stats = report.get("metadata", {}).get("script_info", {})
    
    characters = stats.get("characters", 0)
    scenes = stats.get("scenes", 0)
    
    # Normaliza para 0-1
    char_complexity = min(characters / 30, 1.0)  # 30+ personagens = máximo
    scene_complexity = min(scenes / 100, 1.0)    # 100+ cenas = máximo
    
    return round((char_complexity + scene_complexity) / 2, 2)

def _calculate_originality(report: Dict) -> float:
    """Calcula originalidade baseada no relatório"""
    # Por enquanto usa o score de originalidade da avaliação
    scores = report.get("score_card", {}).get("category_scores", {})
    originality = scores.get("originality", 70)
    
    return round(originality / 100, 2)

__all__ = [
    "analyze", 
    "deep_analyze", 
    "batch_analyze",
    "export_analysis",
    "validate_script"
]