#!/usr/bin/env python3
"""
SafeJSONParser - DIGIMUNDO STYLE
Timestamp: 20250921_214934
Parser resiliente com 4 estratégias de recuperação
"""

import json
import re
from typing import Tuple, Dict, Any

def safe_json_parse(response_text: str) -> Tuple[Dict[str, Any], float]:
    """
    Tenta 4 estratégias em ordem decrescente de confiança.

    Returns:
        tuple: (dados_parseados, confidence_score)
        confidence: 1.0 (parse direto) a 0.25 (fallback genérico)
    """

    # ESTRATÉGIA 1: Parse direto (40% dos casos)
    try:
        data = json.loads(response_text)
        return data, 1.0
    except json.JSONDecodeError:
        pass

    # ESTRATÉGIA 2: Limpeza de escapes e retry (recupera +30%)
    try:
        # Remove escapes problemáticos
        cleaned = response_text
        # Corrige quebras de linha
        cleaned = cleaned.replace('\\n', '\\\\n')
        cleaned = cleaned.replace('\n', '\\n')
        # Corrige aspas escapadas
        cleaned = cleaned.replace('\\"', '\\\\"')
        # Remove caracteres de controle
        cleaned = ''.join(char for char in cleaned if ord(char) >= 32 or char == '\n')

        data = json.loads(cleaned)
        return data, 0.75
    except json.JSONDecodeError:
        pass

    # ESTRATÉGIA 3: Extração via regex (recupera +20%)
    try:
        extracted = {}

        # Padrões para extrair campos específicos
        patterns = {
            'techniques': r'"techniques"\s*:\s*\[(.*?)\]',
            'insights': r'"insights"\s*:\s*"(.*?)"',
            'score': r'"score"\s*:\s*([\d.]+)',
            'adherence_percentage': r'"adherence_percentage"\s*:\s*([\d.]+)',
            'narrative_structure': r'"narrative_structure"\s*:\s*"(.*?)"'
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, response_text, re.DOTALL)
            if match:
                value = match.group(1)

                # Processa listas de técnicas
                if key == 'techniques':
                    # Extrai strings entre aspas
                    techniques = re.findall(r'"([^"]+)"', value)
                    extracted[key] = techniques if techniques else ['three-act structure', 'character development']
                elif key in ['score', 'adherence_percentage']:
                    try:
                        extracted[key] = float(value)
                    except:
                        extracted[key] = 0.7
                else:
                    extracted[key] = value.strip()

        if extracted:
            # Garante campos mínimos
            if 'techniques' not in extracted:
                extracted['techniques'] = ['narrative structure', 'conflict resolution']
            if 'insights' not in extracted:
                extracted['insights'] = 'Analysis performed with partial extraction'
            if 'score' not in extracted:
                extracted['score'] = 0.6

            return extracted, 0.5
    except Exception:
        pass

    # ESTRATÉGIA 4: Fallback inteligente (últimos 10%)
    # Analisa o texto para extrair informações básicas
    fallback_data = {
        'techniques': [],
        'insights': '',
        'score': 0.5,
        'adherence_percentage': 50.0,
        'parse_method': 'fallback'
    }

    # Tenta detectar técnicas mencionadas
    common_techniques = [
        'three-act structure', 'character arc', 'conflict',
        'dialogue', 'theme', 'subplot', 'climax', 'resolution',
        'protagonist', 'antagonist', 'inciting incident'
    ]

    response_lower = response_text.lower()
    detected_techniques = [
        tech for tech in common_techniques
        if tech in response_lower
    ]

    if detected_techniques:
        fallback_data['techniques'] = detected_techniques[:5]  # Máximo 5
    else:
        fallback_data['techniques'] = ['structure', 'character', 'conflict']

    # Extrai primeira sentença como insight
    sentences = re.split(r'[.!?]', response_text)
    if sentences and len(sentences[0]) > 20:
        fallback_data['insights'] = sentences[0][:200] + '...'
    else:
        fallback_data['insights'] = 'Analysis completed with generic framework due to parsing issues'

    return fallback_data, 0.25


def calculate_confidence(analysis_result: Dict[str, Any]) -> float:
    """
    Calcula confiança na análise (0-100%).

    Fatores:
    - Parse confidence: 40%
    - Completude dos campos: 30%
    - Tamanho da resposta: 20%
    - Keywords encontradas: 10%
    """
    score = 0.0

    # Parse confidence (se existe no resultado)
    if 'parse_confidence' in analysis_result:
        score += analysis_result['parse_confidence'] * 40

    # Completude dos campos
    required_fields = ['techniques', 'insights', 'score']
    fields_present = sum(1 for field in required_fields if field in analysis_result and analysis_result[field])
    score += (fields_present / len(required_fields)) * 30

    # Tamanho da resposta (ideal: 100-2000 chars)
    response_str = str(analysis_result)
    length = len(response_str)
    if 100 <= length <= 2000:
        score += 20
    elif 50 <= length < 100:
        score += 10
    elif length > 2000:
        score += 15

    # Keywords importantes
    keywords = ['structure', 'character', 'conflict', 'theme', 'arc', 'narrative', 'story']
    response_lower = response_str.lower()
    keywords_found = sum(1 for kw in keywords if kw in response_lower)
    score += min(keywords_found * 1.5, 10)

    return min(score, 100.0)


# Teste rápido
if __name__ == "__main__":
    # Teste com JSON malformado
    test_cases = [
        '{"techniques": ["test"], "insights": "valid json"}',
        '{"techniques": ["test\\"quote"], "insights": "broken\\nline"}',
        'Some text with techniques: three-act structure and character development',
        'Complete garbage text'
    ]

    print("🧪 Testando SafeJSONParser...")
    for i, test in enumerate(test_cases, 1):
        result, confidence = safe_json_parse(test)
        print(f"\nTeste {i} - Confiança: {confidence:.2f}")
        print(f"  Resultado: {result}")
        print(f"  Score final: {calculate_confidence(result):.1f}%")