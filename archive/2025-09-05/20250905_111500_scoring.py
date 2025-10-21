"""
Sistema de Scoring - Avaliação por checklist com pesos configuráveis.
Remove o 62/100 fixo e implementa pontuação variável real.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import json
import sys

# Adicionar path para imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class ScriptScorer:
    """Sistema de pontuação para análises de roteiros."""
    
    # Pesos padrão por categoria (soma = 1.0)
    DEFAULT_WEIGHTS = {
        "estrutura": 0.30,
        "emoção": 0.25,
        "técnica": 0.20,
        "tema": 0.25
    }
    
    # Critérios de avaliação por categoria
    EVALUATION_CRITERIA = {
        "estrutura": {
            "três_atos": {"desc": "Estrutura de três atos clara", "max": 10},
            "pontos_virada": {"desc": "Pontos de virada bem definidos", "max": 10},
            "arco_protagonista": {"desc": "Arco do protagonista coerente", "max": 10},
            "climax": {"desc": "Clímax bem posicionado", "max": 10},
            "resolução": {"desc": "Resolução satisfatória", "max": 10},
            "ritmo": {"desc": "Ritmo narrativo adequado", "max": 10},
            "subplot": {"desc": "Subtramas bem integradas", "max": 10},
            "setup_payoff": {"desc": "Setup e payoff efetivos", "max": 10},
            "conflito": {"desc": "Conflito central claro", "max": 10},
            "stakes": {"desc": "Stakes bem estabelecidas", "max": 10}
        },
        "emoção": {
            "empatia": {"desc": "Conexão empática com personagens", "max": 10},
            "curva_emocional": {"desc": "Curva emocional envolvente", "max": 10},
            "momentos_impacto": {"desc": "Momentos de impacto emocional", "max": 10},
            "autenticidade": {"desc": "Emoções autênticas", "max": 10},
            "variedade": {"desc": "Variedade emocional", "max": 10},
            "catarse": {"desc": "Catarse efetiva", "max": 10},
            "tensão": {"desc": "Construção de tensão", "max": 10},
            "alívio": {"desc": "Momentos de alívio cômico", "max": 10},
            "surpresa": {"desc": "Elementos surpresa", "max": 10},
            "ressonância": {"desc": "Ressonância emocional duradoura", "max": 10}
        },
        "técnica": {
            "diálogos": {"desc": "Diálogos naturais e significativos", "max": 10},
            "descrições": {"desc": "Descrições visuais efetivas", "max": 10},
            "formatação": {"desc": "Formatação profissional", "max": 10},
            "show_dont_tell": {"desc": "Show don't tell aplicado", "max": 10},
            "economia": {"desc": "Economia narrativa", "max": 10},
            "voice": {"desc": "Voz única do autor", "max": 10},
            "visualização": {"desc": "Facilidade de visualização", "max": 10},
            "transições": {"desc": "Transições fluidas", "max": 10},
            "abertura": {"desc": "Abertura cativante", "max": 10},
            "fechamento": {"desc": "Fechamento memorável", "max": 10}
        },
        "tema": {
            "relevância": {"desc": "Relevância temática", "max": 10},
            "profundidade": {"desc": "Profundidade filosófica", "max": 10},
            "originalidade": {"desc": "Originalidade da abordagem", "max": 10},
            "universalidade": {"desc": "Temas universais", "max": 10},
            "subtexto": {"desc": "Subtexto rico", "max": 10},
            "coerência": {"desc": "Coerência temática", "max": 10},
            "exploração": {"desc": "Exploração completa do tema", "max": 10},
            "metáforas": {"desc": "Uso de metáforas visuais", "max": 10},
            "mensagem": {"desc": "Mensagem clara sem ser didática", "max": 10},
            "provocação": {"desc": "Capacidade de provocar reflexão", "max": 10}
        }
    }
    
    def __init__(self, settings: Optional[Dict] = None):
        """
        Inicializa o scorer com configurações.
        
        Args:
            settings: Configurações opcionais com pesos customizados
        """
        self.settings = settings or {}
        
        # Carregar pesos (do settings ou usar default)
        self.weights = self._load_weights()
        
        # Validar que soma dos pesos = 1.0
        total_weight = sum(self.weights.values())
        if abs(total_weight - 1.0) > 0.01:
            # Normalizar pesos
            self.weights = {k: v/total_weight for k, v in self.weights.items()}
    
    def _load_weights(self) -> Dict[str, float]:
        """Carrega pesos de configuração ou usa defaults."""
        if self.settings and 'scoring' in self.settings:
            custom_weights = self.settings['scoring'].get('weights', {})
            # Merge com defaults
            weights = self.DEFAULT_WEIGHTS.copy()
            weights.update(custom_weights)
            return weights
        
        return self.DEFAULT_WEIGHTS.copy()
    
    def score(self, analysis: Dict) -> Dict:
        """
        Recebe as 4 perspectivas e retorna pontuação detalhada.
        
        Args:
            analysis: Dict com análises das perspectivas
            
        Returns:
            Dict com {total: float, breakdown: {...}, details: {...}}
        """
        breakdown = {}
        details = {}
        
        # Avaliar cada categoria
        for category in ["estrutura", "emoção", "técnica", "tema"]:
            if category in analysis:
                score, detail = self._evaluate_category(category, analysis[category])
                breakdown[category] = score
                details[category] = detail
            else:
                # Categoria não analisada recebe 50/100 (neutro)
                breakdown[category] = 50.0
                details[category] = {"status": "não analisado"}
        
        # Calcular pontuação total ponderada
        total = 0.0
        for category, score in breakdown.items():
            weight = self.weights.get(category, 0.25)
            total += score * weight
        
        # Garantir que está no range 0-100
        total = max(0.0, min(100.0, total))
        
        return {
            "total": round(total, 1),
            "breakdown": breakdown,
            "weights": self.weights,
            "details": details,
            "grade": self._get_grade(total)
        }
    
    def _evaluate_category(self, category: str, content: Any) -> Tuple[float, Dict]:
        """
        Avalia uma categoria específica baseada no conteúdo.
        
        Args:
            category: Nome da categoria
            content: Conteúdo da análise (string ou dict)
            
        Returns:
            (score, details)
        """
        criteria = self.EVALUATION_CRITERIA.get(category, {})
        
        # Extrair texto para análise
        if isinstance(content, dict):
            text = content.get('response', content.get('content', str(content)))
        else:
            text = str(content)
        
        text_lower = text.lower()
        
        # Avaliar cada critério
        scores = {}
        total_possible = 0
        total_earned = 0
        
        for criterion_id, criterion in criteria.items():
            max_score = criterion["max"]
            total_possible += max_score
            
            # Heurísticas para detectar qualidade
            earned = self._evaluate_criterion(criterion_id, criterion["desc"], text_lower)
            
            scores[criterion_id] = {
                "desc": criterion["desc"],
                "earned": earned,
                "max": max_score
            }
            
            total_earned += earned
        
        # Calcular percentual
        if total_possible > 0:
            percentage = (total_earned / total_possible) * 100
        else:
            percentage = 50.0  # Neutro se não há critérios
        
        return round(percentage, 1), {
            "criteria": scores,
            "total_earned": total_earned,
            "total_possible": total_possible,
            "percentage": round(percentage, 1)
        }
    
    def _evaluate_criterion(self, criterion_id: str, description: str, text: str) -> float:
        """
        Avalia um critério específico usando heurísticas.
        
        Args:
            criterion_id: ID do critério
            description: Descrição do critério
            text: Texto para análise
            
        Returns:
            Score de 0-10
        """
        # Palavras-chave positivas e negativas por tipo de critério
        positive_keywords = {
            "três_atos": ["três atos", "3 atos", "estrutura clássica", "bem definid"],
            "pontos_virada": ["pontos de virada", "plot point", "reviravolta", "turning point"],
            "arco_protagonista": ["arco", "jornada", "transformação", "evolução", "crescimento"],
            "climax": ["clímax", "climax", "ápice", "ponto alto"],
            "resolução": ["resolução", "conclusão", "desfecho", "satisfatór"],
            "empatia": ["empatia", "conexão", "identificação", "envolvente"],
            "catarse": ["catarse", "catártico", "libertação", "impactante"],
            "diálogos": ["diálogo", "natural", "autêntic", "convincente"],
            "originalidade": ["original", "inovador", "único", "criativo", "fresh"],
            "profundidade": ["profund", "complex", "camadas", "nuance"]
        }
        
        negative_keywords = {
            "três_atos": ["confus", "desestrutur", "caótic", "sem estrutura"],
            "pontos_virada": ["previsível", "óbvio", "fraco", "ausente"],
            "arco_protagonista": ["plano", "estático", "inconsistente", "raso"],
            "climax": ["anticlímax", "decepcionante", "fraco", "mal posicionado"],
            "resolução": ["insatisfatór", "abrupto", "forçado", "deus ex machina"],
            "empatia": ["distante", "frio", "desconectado", "artificial"],
            "catarse": ["vazio", "sem impacto", "superficial"],
            "diálogos": ["artificial", "expositivo", "forçado", "clichê"],
            "originalidade": ["clichê", "derivativo", "genérico", "comum"],
            "profundidade": ["superficial", "raso", "simplista", "básico"]
        }
        
        # Buscar menções positivas e negativas
        positive_score = 0
        negative_score = 0
        
        # Verificar keywords positivas
        for key, keywords in positive_keywords.items():
            if key in criterion_id or any(kw in description.lower() for kw in keywords[:2]):
                for keyword in keywords:
                    if keyword in text:
                        positive_score += 2
                        break
        
        # Verificar keywords negativas
        for key, keywords in negative_keywords.items():
            if key in criterion_id or any(kw in description.lower() for kw in keywords[:2]):
                for keyword in keywords:
                    if keyword in text:
                        negative_score += 2
                        break
        
        # Detectar padrões gerais de qualidade
        if any(word in text for word in ["excelente", "excepcional", "magistral", "brilhante"]):
            positive_score += 3
        elif any(word in text for word in ["bom", "adequado", "competente", "sólido"]):
            positive_score += 2
        elif any(word in text for word in ["médio", "regular", "comum", "padrão"]):
            positive_score += 1
        elif any(word in text for word in ["fraco", "pobre", "ruim", "inadequado"]):
            negative_score += 2
        
        # Calcular score final (0-10)
        base_score = 5  # Começa neutro
        base_score += min(positive_score, 5)  # Max +5
        base_score -= min(negative_score, 5)  # Max -5
        
        return max(0, min(10, base_score))
    
    def _get_grade(self, score: float) -> str:
        """Converte score numérico em nota conceitual."""
        if score >= 90:
            return "A+ (Excepcional)"
        elif score >= 85:
            return "A (Excelente)"
        elif score >= 80:
            return "A- (Muito Bom)"
        elif score >= 75:
            return "B+ (Bom)"
        elif score >= 70:
            return "B (Competente)"
        elif score >= 65:
            return "B- (Satisfatório)"
        elif score >= 60:
            return "C+ (Regular)"
        elif score >= 55:
            return "C (Mediano)"
        elif score >= 50:
            return "C- (Abaixo da Média)"
        elif score >= 40:
            return "D (Fraco)"
        else:
            return "F (Insuficiente)"


def score(analysis: dict) -> dict:
    """
    Função conveniente para uso direto.
    
    Args:
        analysis: Análises das perspectivas
        
    Returns:
        Dict com pontuação total e breakdown
    """
    scorer = ScriptScorer()
    return scorer.score(analysis)