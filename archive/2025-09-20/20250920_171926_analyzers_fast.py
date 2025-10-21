"""
Analyzers otimizados para processamento rápido de PDFs
Usa llama3.2:3b para velocidade ou fallbacks simples
"""
from typing import Dict, List, Any
import re
from ..models.ollama_fast import FastLLM

# Instância única do modelo rápido
_fast_llm = None

def _get_fast_llm():
    global _fast_llm
    if _fast_llm is None:
        _fast_llm = FastLLM()
    return _fast_llm

def detect_structure_fast(text: str) -> Dict[str, Any]:
    """Detecção rápida de estrutura sem LLM pesado"""
    
    # Detecção simples por padrões
    structure = {
        "tipo": "roteiro",
        "paginas": len(text) // 3000,  # Estimativa
        "atos": []
    }
    
    # Detectar INT./EXT. para cenas
    cenas = len(re.findall(r'\b(INT\.|EXT\.|INT/|EXT/)', text))
    structure["total_cenas"] = cenas
    
    # Detectar diálogos (linhas com nome em CAPS seguido de diálogo)
    dialogos = len(re.findall(r'\n[A-Z]{2,}[A-Z\s]+\n', text))
    structure["total_dialogos"] = dialogos
    
    # Estimativa de atos baseada em páginas
    if structure["paginas"] > 0:
        structure["atos"] = [
            {"ato": 1, "paginas": structure["paginas"] // 4},
            {"ato": 2, "paginas": structure["paginas"] // 2},
            {"ato": 3, "paginas": structure["paginas"] // 4}
        ]
    
    return structure

def extract_techniques_fast(text: str) -> List[str]:
    """Extração rápida de técnicas por padrões"""
    
    techniques = []
    
    # Flashback detection
    if re.search(r'(FLASHBACK|FLASH BACK|flashback)', text, re.I):
        techniques.append("Flashback")
    
    # Voice over
    if re.search(r'(V\.O\.|VOICE OVER|voice-over)', text, re.I):
        techniques.append("Voice Over")
    
    # Montage
    if re.search(r'(MONTAGE|SERIES OF SHOTS)', text, re.I):
        techniques.append("Montage")
    
    # Intercut
    if re.search(r'(INTERCUT|CROSS CUT)', text, re.I):
        techniques.append("Intercut/Cross-cutting")
    
    # Split screen
    if re.search(r'(SPLIT SCREEN|SPLIT-SCREEN)', text, re.I):
        techniques.append("Split Screen")
    
    # Dream sequence
    if re.search(r'(DREAM SEQUENCE|DREAM:|NIGHTMARE)', text, re.I):
        techniques.append("Dream Sequence")
    
    # Time jump
    if re.search(r'(LATER|YEARS LATER|MOMENTS LATER|CONTINUOUS)', text, re.I):
        techniques.append("Time Jump")
    
    # POV shots
    if re.search(r"(POV|P\.O\.V\.|POINT OF VIEW)", text, re.I):
        techniques.append("POV Shot")
    
    # Se não encontrou nenhuma, técnicas básicas
    if not techniques:
        techniques = ["Diálogo", "Ação", "Descrição"]
    
    return techniques[:10]  # Máximo 10 técnicas

def brutal_score_fast(text: str, doc_type: str = "roteiro_criador") -> Dict[str, Any]:
    """Score brutal rápido e determinístico"""
    
    score = {
        "nota_geral": 62,
        "comparacao": "Chinatown (95/100)",
        "problema_principal": "Falta desenvolvimento profundo dos personagens"
    }
    
    if doc_type == "roteiro_criador":
        # Sempre brutal para roteiros do criador
        score["nota_geral"] = 62
        score["feedback"] = "Comparado aos mestres, ainda é trabalho de iniciante promissor"
    elif doc_type == "roteiro_mestre":
        # Roteiros mestres têm notas altas
        score["nota_geral"] = 92
        score["feedback"] = "Obra-prima reconhecida do cinema"
    else:
        # Teoria
        score["nota_geral"] = 78
        score["feedback"] = "Teoria sólida mas precisa de aplicação prática"
    
    # Usar LLM rápido se disponível (opcional)
    try:
        llm = _get_fast_llm()
        if llm.is_available():
            quick_score = llm.analyze_quick(text[:1000], "score")
            if quick_score.isdigit():
                score["nota_geral"] = int(quick_score)
    except:
        pass  # Mantém score padrão
    
    return score

def analyze_fast(text: str, doc_type: str = "roteiro_criador") -> Dict[str, Any]:
    """Análise completa otimizada para velocidade"""
    
    return {
        "estrutura": detect_structure_fast(text),
        "tecnicas": extract_techniques_fast(text),
        "avaliacao": brutal_score_fast(text, doc_type)
    }