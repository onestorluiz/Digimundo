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
    
    def consolidate(self, parts_or_list: Any, headers: Optional[List[str]] = None) -> str:
        """
        Consolidate outputs - handles list[str] with len=4, list of dicts, or dict.
        Deterministic output with fixed headers.
        
        Args:
            parts_or_list: List[str] (len=4), List[dict], or Dict with outputs
            headers: Optional custom headers for sections
            
        Returns:
            Consolidated string with deterministic formatting
        """
        # Fixed headers for 4-perspective analysis
        default_headers = ["Structure", "Emotion", "Technique", "Theme"]
        headers = headers or default_headers
        
        # Handle different input types
        if isinstance(parts_or_list, list):
            # Special case: list of 4 strings maps to standard headers
            if len(parts_or_list) == 4 and all(isinstance(x, str) for x in parts_or_list):
                dict_parts = {
                    headers[0]: parts_or_list[0],
                    headers[1]: parts_or_list[1],
                    headers[2]: parts_or_list[2],
                    headers[3]: parts_or_list[3]
                }
            else:
                # General list handling
                dict_parts = {}
                for i, item in enumerate(parts_or_list):
                    if isinstance(item, dict):
                        # Extract key from item if available
                        if 'role' in item:
                            key = item['role']
                        elif 'perspective' in item:
                            key = item['perspective']
                        else:
                            # Use header if available, else numbered key
                            key = headers[i] if i < len(headers) else f"result_{i+1}"
                        dict_parts[key] = item
                    else:
                        # Simple value - use header or position
                        key = headers[i] if i < len(headers) else f"result_{i+1}"
                        dict_parts[key] = item
            parts = dict_parts
        else:
            # Already a dict
            parts = parts_or_list
        
        # Normalize keys to standard headers when possible
        normalized_parts = {}
        key_mapping = {
            'structure': headers[0], 'estrutura': headers[0],
            'emotion': headers[1], 'emoção': headers[1], 'emotional_impact': headers[1],
            'technique': headers[2], 'técnica': headers[2], 'dialogue': headers[2],
            'theme': headers[3], 'tema': headers[3], 'originality': headers[3]
        }
        
        for key, value in parts.items():
            # Map to standard header if possible
            normalized_key = key_mapping.get(key.lower(), key)
            
            # Extract string content from complex values
            if isinstance(value, dict):
                content = value.get('processed', value.get('content', value.get('response', str(value))))
            else:
                content = str(value)
            
            normalized_parts[normalized_key] = content
        
        # Build deterministic output with fixed order
        output = []
        output.append("=" * 70)
        output.append("📖 CONSOLIDATED ANALYSIS")
        output.append("=" * 70)
        output.append("")
        
        # First output standard headers in order
        for header in headers:
            if header in normalized_parts:
                output.append(f"### {header.upper()}")
                output.append("-" * 40)
                output.append(normalized_parts[header])
                output.append("")
        
        # Then any remaining keys in alphabetical order
        remaining_keys = sorted([k for k in normalized_parts.keys() if k not in headers])
        for key in remaining_keys:
            output.append(f"### {key.upper()}")
            output.append("-" * 40)
            output.append(normalized_parts[key])
            output.append("")
        
        output.append("=" * 70)
        output.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(output)
    
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