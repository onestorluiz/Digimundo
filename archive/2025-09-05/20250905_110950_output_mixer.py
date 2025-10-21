"""
Output Mixer - Consolida múltiplas perspectivas em uma voz única.
Garante output determinístico e bem formatado.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class OutputMixer:
    """Misturador de outputs de análises paralelas."""
    
    # Perspectivas padrão para análise quádrupla
    DEFAULT_PERSPECTIVES = ["estrutura", "emoção", "técnica", "tema"]
    
    # Templates de seções
    SECTION_HEADERS = {
        "estrutura": "📐 ANÁLISE ESTRUTURAL",
        "emoção": "❤️ DIMENSÃO EMOCIONAL",
        "técnica": "🎬 ASPECTOS TÉCNICOS",
        "tema": "💡 EXPLORAÇÃO TEMÁTICA",
        "extractor": "🔍 CONCEITOS-CHAVE",
        "analyzer": "📊 ANÁLISE PROFUNDA",
        "evaluator": "⚖️ AVALIAÇÃO CRÍTICA",
        "synthesizer": "🔮 SÍNTESE EVOLUTIVA"
    }
    
    @staticmethod
    def mix(parts: Dict[str, str]) -> str:
        """
        Junta quatro perspectivas em uma voz única com cabeçalhos padronizados.
        
        Args:
            parts: Dicionário com chave=perspectiva, valor=texto da análise
            
        Returns:
            String consolidada com todas as perspectivas formatadas
        """
        if not parts:
            return "❌ Nenhuma análise disponível para consolidar."
        
        # Construir output consolidado
        output = []
        output.append("=" * 70)
        output.append("📖 ANÁLISE MULTIDIMENSIONAL COMPLETA")
        output.append("=" * 70)
        output.append("")
        
        # Processar cada parte na ordem padrão (se existir)
        for perspective in OutputMixer.DEFAULT_PERSPECTIVES:
            if perspective in parts:
                header = OutputMixer.SECTION_HEADERS.get(perspective, f"### {perspective.upper()}")
                output.append(header)
                output.append("-" * 40)
                output.append(OutputMixer._format_content(parts[perspective]))
                output.append("")
        
        # Processar partes adicionais não padrão
        for key, content in parts.items():
            if key not in OutputMixer.DEFAULT_PERSPECTIVES:
                header = OutputMixer.SECTION_HEADERS.get(key, f"### {key.upper()}")
                output.append(header)
                output.append("-" * 40)
                output.append(OutputMixer._format_content(content))
                output.append("")
        
        # Rodapé
        output.append("=" * 70)
        output.append(f"Consolidado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(output)
    
    @staticmethod
    def mix_with_metadata(parts: Dict[str, Any]) -> str:
        """
        Versão estendida que aceita metadados junto com o conteúdo.
        
        Args:
            parts: Dict com chave=perspectiva, valor=dict com 'content', 'time', 'model', etc.
            
        Returns:
            String consolidada com metadados incluídos
        """
        if not parts:
            return "❌ Nenhuma análise disponível para consolidar."
        
        output = []
        output.append("=" * 70)
        output.append("📖 ANÁLISE MULTIDIMENSIONAL COM METADADOS")
        output.append("=" * 70)
        output.append("")
        
        # Estatísticas gerais
        total_time = sum(p.get('time', 0) for p in parts.values() if isinstance(p, dict))
        output.append(f"⏱️ Tempo total de processamento: {total_time:.2f}s")
        output.append("")
        
        # Processar cada parte
        for key, value in parts.items():
            if isinstance(value, dict):
                content = value.get('response', value.get('content', ''))
                time_taken = value.get('time', 0)
                model_used = value.get('model', 'unknown')
                role = value.get('role_description', '')
                
                header = OutputMixer.SECTION_HEADERS.get(key, f"### {key.upper()}")
                output.append(header)
                if role:
                    output.append(f"📋 Papel: {role}")
                output.append(f"🤖 Modelo: {model_used} | ⏱️ Tempo: {time_taken:.2f}s")
                output.append("-" * 40)
                output.append(OutputMixer._format_content(content))
                output.append("")
            else:
                # Conteúdo simples sem metadados
                header = OutputMixer.SECTION_HEADERS.get(key, f"### {key.upper()}")
                output.append(header)
                output.append("-" * 40)
                output.append(OutputMixer._format_content(value))
                output.append("")
        
        output.append("=" * 70)
        output.append(f"Consolidado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(output)
    
    @staticmethod
    def _format_content(content: str) -> str:
        """Formata conteúdo para exibição consistente."""
        if not content:
            return "[Conteúdo vazio]"
        
        # Remove espaços extras e formata
        lines = content.strip().split('\n')
        formatted = []
        
        for line in lines:
            line = line.strip()
            if line:
                # Adiciona indentação para parágrafos
                if not line.startswith(('•', '-', '*', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
                    line = f"  {line}"
                formatted.append(line)
        
        return '\n'.join(formatted)
    
    @staticmethod
    def create_summary(parts: Dict[str, Any], max_length: int = 500) -> str:
        """
        Cria um resumo executivo das análises.
        
        Args:
            parts: Análises para resumir
            max_length: Tamanho máximo do resumo
            
        Returns:
            Resumo executivo formatado
        """
        summary = []
        summary.append("📄 RESUMO EXECUTIVO")
        summary.append("=" * 40)
        
        for key, value in parts.items():
            if isinstance(value, dict):
                content = value.get('response', value.get('content', ''))
            else:
                content = value
            
            # Pega primeiras linhas significativas
            lines = [l.strip() for l in content.split('\n') if l.strip()]
            if lines:
                perspective = OutputMixer.SECTION_HEADERS.get(key, key.title())
                summary.append(f"\n{perspective}:")
                preview = ' '.join(lines[:2])[:200] + "..."
                summary.append(f"  {preview}")
        
        result = '\n'.join(summary)
        if len(result) > max_length:
            result = result[:max_length-3] + "..."
        
        return result


def mix(parts: Dict[str, str]) -> str:
    """
    Função conveniente para uso direto.
    
    Args:
        parts: Dicionário com perspectivas e seus textos
        
    Returns:
        String consolidada
    """
    return OutputMixer.mix(parts)