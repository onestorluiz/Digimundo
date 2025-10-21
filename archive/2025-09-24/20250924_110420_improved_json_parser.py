#!/usr/bin/env python3
"""
Parser JSON Robusto com Múltiplas Estratégias
Taxa alvo: 80%+ de sucesso
"""

import json
import re
from typing import Dict, Optional, Tuple, Any

def extract_json_from_text(text: str) -> Optional[Dict]:
    """Estratégia 1: Extrair JSON de texto misto"""
    if not text:
        return None

    # Primeiro, tentar parse direto se for JSON puro
    try:
        # Limpar espaços e newlines extras
        cleaned = text.strip()
        if cleaned.startswith('{') and cleaned.endswith('}'):
            result = json.loads(cleaned)
            if isinstance(result, dict):
                return result
    except:
        pass

    # Se não funcionou, tentar extrair JSON de texto misto
    # Procurar pelo JSON completo usando uma abordagem mais robusta

    # Método 1: Encontrar o primeiro { e o último } correspondente
    if '{' in text and '}' in text:
        # Contar brackets para achar o JSON completo
        start_idx = text.find('{')
        bracket_count = 0
        end_idx = start_idx

        for i in range(start_idx, len(text)):
            if text[i] == '{':
                bracket_count += 1
            elif text[i] == '}':
                bracket_count -= 1
                if bracket_count == 0:
                    end_idx = i + 1
                    break

        if end_idx > start_idx:
            json_candidate = text[start_idx:end_idx]
            try:
                result = json.loads(json_candidate)
                if isinstance(result, dict):
                    return result
            except:
                pass

    # Se ainda não funcionou, tentar patterns de regex
    patterns = [
        r'```json\s*(.*?)\s*```',  # Markdown code block
        r'```\s*(.*?)\s*```',  # Code block genérico
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            try:
                if isinstance(match, tuple):
                    match = match[0]

                clean = match.strip()
                if clean.startswith('{') and clean.endswith('}'):
                    result = json.loads(clean)
                    if isinstance(result, dict):
                        return result
            except:
                continue

    return None

def fix_malformed_json(text: str) -> Optional[Dict]:
    """Estratégia 2: Corrigir JSON malformado"""
    if not text or not ('{' in text and '}' in text):
        return None

    # Extrair apenas a parte JSON
    start = text.find('{')
    end = text.rfind('}') + 1
    json_str = text[start:end]

    # Correções comuns (ordem importa!)
    corrections = [
        # NOVO: Corrigir aspas mistas tipo {"key": 'value'}
        (r':\s*\'([^\']*?)\'([,\}])', r': "\1"\2'),  # Valores com aspas simples
        (r'\{\s*"([^"]+)":\s*\'([^\']*?)\'', r'{"\1": "\2"'),  # Início de objeto
        (r',\s*"([^"]+)":\s*\'([^\']*?)\'', r', "\1": "\2"'),  # Meio de objeto

        # Aspas simples para duplas (melhorado)
        (r"'([^']*)':", r'"\1":'),  # Chaves com aspas simples
        (r":\s*'([^'\\]*(?:\\.[^'\\]*)*)'", r': "\1"'),  # Valores com escape

        # NOVO: Corrigir strings com aspas internas mal escapadas
        (r'"([^"]*?)\'([^"]*?)"', r'"\1\\"\2"'),  # Aspas simples dentro de duplas

        # Trailing commas
        (r',\s*}', '}'),
        (r',\s*]', ']'),

        # Campos sem aspas (cuidado para não quebrar strings)
        (r'([,\{]\s*)(\w+):', r'\1"\2":'),

        # Valores undefined/null/boolean
        (r':\s*undefined', ': null'),
        (r':\s*None', ': null'),
        (r':\s*True', ': true'),
        (r':\s*False', ': false'),

        # Quebras de linha em strings
        (r'"\s*\n\s*"', '" "'),

        # Comentários
        (r'//.*$', '', re.MULTILINE),
        (r'/\*.*?\*/', '', re.DOTALL),
    ]

    fixed = json_str
    for pattern, replacement, *flags in corrections:
        flag = flags[0] if flags else 0
        fixed = re.sub(pattern, replacement, fixed, flags=flag)

    # Tentar parse
    try:
        result = json.loads(fixed)
        if isinstance(result, dict):
            return result
    except:
        pass

    # Tentar com eval (perigoso mas controlado)
    try:
        # Substituir true/false/null do JS
        safe_str = fixed.replace('true', 'True').replace('false', 'False').replace('null', 'None')
        result = eval(safe_str, {"__builtins__": {}}, {})
        if isinstance(result, dict):
            # Converter de volta para JSON válido
            return json.loads(json.dumps(result))
    except:
        pass

    return None

def create_minimal_structure(text: str) -> Dict:
    """Estratégia 3: Criar estrutura mínima como fallback - MELHORADO"""

    # Estrutura base melhorada
    structure = {
        "status": "parsed_with_fallback",
        "confidence": 0.3,
        "raw_output": text[:1000] if text else "",  # Aumentar para 1000 chars
        "metadata": {},
        "evidence_log": [],
        "analise_estrutural": {},
        "analise_personagem": [],
        "validation": {"valid": False, "score": 0}
    }

    # Se não tem texto, retornar estrutura vazia
    if not text:
        return structure

    # NOVO: Tentar extrair dados de JSON parcial/quebrado
    if '{' in text:
        # Procurar por campos conhecidos no texto
        patterns = {
            'genre': r'"genre"\s*:\s*"([^"]+)"',
            'pages': r'"pages"\s*:\s*"?(\d+)"?',
            'title': r'"title"\s*:\s*"([^"]+)"',
            'score': r'"score"\s*:\s*(\d+)',
            'evidence': r'"evidence"\s*:\s*["\']([^"\']+)["\']',
            'page': r'"page"\s*:\s*(\d+)',
            'name': r'"name"\s*:\s*"([^"]+)"',
            'arc': r'"arc"\s*:\s*"([^"]+)"',
            'inciting_incident': r'"inciting_incident"\s*:\s*\{([^}]+)\}',
            'climax': r'"climax"\s*:\s*\{([^}]+)\}',
        }

        # Extrair metadata
        for field in ['genre', 'pages', 'title']:
            match = re.search(patterns.get(field, ''), text, re.IGNORECASE)
            if match:
                structure["metadata"][field] = match.group(1)
                structure["confidence"] += 0.05

        # Extrair score
        score_match = re.search(patterns['score'], text)
        if score_match:
            structure["validation"]["score"] = int(score_match.group(1))
            structure["validation"]["valid"] = True
            structure["confidence"] += 0.1

        # Extrair evidências
        evidence_matches = re.findall(r'"evidence"\s*:\s*["\']([^"\']+)["\']', text)
        page_matches = re.findall(r'"page"\s*:\s*(\d+)', text)

        for i, evidence in enumerate(evidence_matches[:5]):  # Max 5 evidências
            page = int(page_matches[i]) if i < len(page_matches) else i + 1
            structure["evidence_log"].append({
                "page": page,
                "evidence": evidence[:200],  # Limitar tamanho
                "type": "extracted"
            })
            structure["confidence"] += 0.02

        # Extrair personagens
        name_matches = re.findall(r'"name"\s*:\s*"([^"]+)"', text)
        arc_matches = re.findall(r'"arc"\s*:\s*"([^"]+)"', text)

        for i, name in enumerate(name_matches[:3]):  # Max 3 personagens
            arc = arc_matches[i] if i < len(arc_matches) else "unknown"
            structure["analise_personagem"].append({
                "name": name,
                "arc": arc,
                "motivation": "extracted from fallback"
            })
            structure["confidence"] += 0.05

        # Extrair estrutura narrativa
        for event in ['inciting_incident', 'climax']:
            match = re.search(patterns.get(event, ''), text)
            if match:
                # Tentar extrair page e description
                content = match.group(1) if match.groups() else ""
                page_match = re.search(r'"page"\s*:\s*"?(\d+)"?', content)
                desc_match = re.search(r'"description"\s*:\s*"([^"]+)"', content)

                structure["analise_estrutural"][event] = {
                    "page": page_match.group(1) if page_match else "unknown",
                    "description": desc_match.group(1) if desc_match else "extracted"
                }
                structure["confidence"] += 0.05

    # Análise heurística adicional do texto puro
    if structure["confidence"] < 0.5:
        # Procurar por palavras-chave no texto
        text_lower = text.lower()

        # Detectar gênero
        genres = {
            'sci-fi': ['science', 'fiction', 'future', 'space', 'robot', 'ai'],
            'drama': ['drama', 'emotion', 'conflict', 'family'],
            'action': ['action', 'fight', 'battle', 'chase'],
            'comedy': ['comedy', 'funny', 'laugh', 'humor'],
            'thriller': ['thriller', 'suspense', 'mystery', 'danger']
        }

        for genre, keywords in genres.items():
            if any(kw in text_lower for kw in keywords):
                structure["metadata"]["genre"] = genre
                structure["confidence"] += 0.05
                break

        # Detectar estrutura narrativa
        if any(word in text_lower for word in ['inciting', 'incident', 'catalyst']):
            structure["analise_estrutural"]["has_inciting_incident"] = True
            structure["confidence"] += 0.05

        if any(word in text_lower for word in ['climax', 'peak', 'confrontation']):
            structure["analise_estrutural"]["has_climax"] = True
            structure["confidence"] += 0.05

        if any(word in text_lower for word in ['resolution', 'ending', 'conclusion']):
            structure["analise_estrutural"]["has_resolution"] = True
            structure["confidence"] += 0.05

    # Garantir que confidence não passe de 0.7 (é fallback)
    structure["confidence"] = min(structure["confidence"], 0.7)

    # Se conseguiu extrair algo útil, marcar como válido
    if structure["metadata"] or structure["evidence_log"] or structure["analise_personagem"]:
        structure["validation"]["valid"] = True
        structure["validation"]["method"] = "fallback_extraction"

    return structure

def parse_with_strategies(text: str, verbose: bool = False) -> Tuple[Optional[Dict], float]:
    """
    Parse com múltiplas estratégias e confiança
    Retorna: (parsed_dict, confidence)
    """

    if not text:
        return None, 0.0

    # Estratégia 1: Extrair JSON puro
    if verbose:
        print("  Tentando estratégia 1: Extrair JSON...")
    result = extract_json_from_text(text)
    if result:
        if verbose:
            print("  ✅ Sucesso com estratégia 1!")
        return result, 0.9

    # Estratégia 2: Corrigir JSON malformado
    if verbose:
        print("  Tentando estratégia 2: Corrigir JSON...")
    result = fix_malformed_json(text)
    if result:
        if verbose:
            print("  ✅ Sucesso com estratégia 2!")
        return result, 0.7

    # Estratégia 3: Fallback para estrutura mínima
    if verbose:
        print("  Tentando estratégia 3: Estrutura mínima...")
    result = create_minimal_structure(text)
    if verbose:
        print("  ⚠️ Usando fallback")

    confidence = result.get("confidence", 0.3)
    return result, confidence

def robust_json_parse(text: str) -> Tuple[Dict, float]:
    """
    Interface principal - sempre retorna algo útil
    """
    parsed, confidence = parse_with_strategies(text)

    if not parsed:
        # Último recurso - estrutura vazia válida
        parsed = {
            "status": "empty_fallback",
            "confidence": 0.1,
            "raw_output": text[:100] if text else "",
            "metadata": {"parser": "improved_json_parser"},
            "evidence_log": [],
            "analise_estrutural": {},
            "analise_personagem": [],
            "validation": {"valid": False}
        }
        confidence = 0.1

    return parsed, confidence

# Testes
if __name__ == "__main__":
    print("🧪 TESTANDO PARSER ROBUSTO")
    print("="*60)

    test_cases = [
        '{"name": "test", "value": 123}',  # JSON válido
        "Here is the JSON: {'name': 'test'}",  # Aspas simples
        '```json\n{"result": true}\n```',  # Markdown
        'The score is 85 and insight is great story',  # Texto puro
        '{invalid json with errors,}',  # JSON quebrado
        'Just plain text without JSON',  # Sem JSON
    ]

    success = 0
    for i, test in enumerate(test_cases, 1):
        print(f"\nTeste {i}: {test[:30]}...")
        result, confidence = robust_json_parse(test)

        if result and confidence > 0.3:
            print(f"  ✅ Parse OK (confiança: {confidence:.2f})")
            success += 1
        else:
            print(f"  ❌ Parse falhou")

    rate = (success / len(test_cases)) * 100
    print(f"\n📊 Taxa de sucesso: {success}/{len(test_cases)} ({rate:.1f}%)")

    if rate >= 80:
        print("✅ Meta de 80% alcançada!")
    else:
        print(f"⚠️ Abaixo da meta (precisa {80-rate:.1f}% mais)")

    print("\n🥷 DIGIMUNDO PRESENTE")