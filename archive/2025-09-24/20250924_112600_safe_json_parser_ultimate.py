#!/usr/bin/env python3
"""
Safe JSON Parser Ultimate
Parser seguro e otimizado para JSONs do Ollama
Com melhor detecção de personagens e elementos
"""

import json
import re
import ast
from typing import Dict, Tuple, Optional, Any, List

def safe_json_parse(text: str) -> Tuple[Optional[Dict], float]:
    """
    Parse seguro de JSON com múltiplas estratégias
    Retorna: (parsed_dict, confidence)
    """
    if not text:
        return None, 0.0

    # Estratégia 1: JSON válido direto
    try:
        if text.strip().startswith('{'):
            result = json.loads(text)
            if isinstance(result, dict):
                return result, 1.0
    except:
        pass

    # Estratégia 2: Limpar e corrigir JSON
    cleaned = clean_json_text(text)
    try:
        result = json.loads(cleaned)
        if isinstance(result, dict):
            return result, 0.9
    except:
        pass

    # Estratégia 3: Extração inteligente
    extracted = extract_from_malformed(text)
    if extracted:
        confidence = calculate_confidence(extracted)
        return extracted, confidence

    # Estratégia 4: Fallback completo
    return create_comprehensive_fallback(text), 0.3

def clean_json_text(text: str) -> str:
    """Limpa e corrige JSON malformado"""

    # Extrair apenas parte JSON
    if '{' in text:
        start = text.find('{')
        # Contar brackets para achar fim correto
        bracket_count = 0
        end_idx = start

        for i in range(start, len(text)):
            if text[i] == '{':
                bracket_count += 1
            elif text[i] == '}':
                bracket_count -= 1
                if bracket_count == 0:
                    end_idx = i + 1
                    break

        text = text[start:end_idx]

    # Correções em ordem de prioridade
    corrections = [
        # Aspas mistas - MELHORADO
        (r':\s*\'([^\']*?)\'(?=\s*[,\}])', r': "\1"'),  # Valores com aspas simples
        (r'\'([^\']+?)\':', r'"\1":'),  # Chaves com aspas simples

        # Aspas internas mal escapadas
        (r'"([^"]*?)\'([^"]*?)"', r'"\1\\\'\2"'),  # Aspas simples dentro de duplas
        (r'"([^"]*?)"([^:,\}\]]+?)"', r'"\1\"\2"'),  # Duplas dentro de duplas

        # Trailing commas
        (r',\s*\}', '}'),
        (r',\s*\]', ']'),

        # Campos sem aspas
        (r'(\{|\,)\s*(\w+):', r'\1"\2":'),

        # Boolean e null
        (r':\s*True\b', ': true'),
        (r':\s*False\b', ': false'),
        (r':\s*None\b', ': null'),
        (r':\s*undefined\b', ': null'),

        # Quebras de linha em strings
        (r'"\s*\n\s*"', '" "'),

        # Números como strings desnecessárias
        (r':\s*"(\d+)"(?=\s*[,\}])', r': \1'),
    ]

    cleaned = text
    for pattern, replacement in corrections:
        cleaned = re.sub(pattern, replacement, cleaned)

    return cleaned

def extract_from_malformed(text: str) -> Optional[Dict]:
    """Extração inteligente de dados de JSON malformado"""

    structure = {
        "status": "extracted",
        "metadata": {},
        "evidence_log": [],
        "analise_estrutural": {},
        "analise_personagem": [],
        "validation": {"valid": False, "score": 0}
    }

    if not text:
        return structure

    # Patterns melhorados para extração
    patterns = {
        # Metadata
        'genre': r'"genre"\s*:\s*"([^"]+)"',
        'pages': r'"pages"\s*:\s*"?(\d+)"?',
        'title': r'"title"\s*:\s*"([^"]+)"',

        # Validation
        'score': r'"score"\s*:\s*(\d+)',
        'valid': r'"valid"\s*:\s*(true|false)',

        # Estrutura narrativa
        'inciting_incident': r'"inciting_incident"\s*:\s*\{([^\}]+)\}',
        'climax': r'"climax"\s*:\s*\{([^\}]+)\}',
        'resolution': r'"resolution"\s*:\s*\{([^\}]+)\}',
    }

    # Extrair metadata
    for field in ['genre', 'pages', 'title']:
        match = re.search(patterns[field], text, re.IGNORECASE)
        if match:
            structure["metadata"][field] = match.group(1)

    # Extrair validation
    score_match = re.search(patterns['score'], text)
    if score_match:
        structure["validation"]["score"] = int(score_match.group(1))
        structure["validation"]["valid"] = True

    valid_match = re.search(patterns['valid'], text)
    if valid_match:
        structure["validation"]["valid"] = valid_match.group(1) == 'true'

    # Extrair evidências com melhor pattern
    evidence_pattern = r'"evidence"\s*:\s*["\']([^"\']+)["\'][^}]*?"page"\s*:\s*(\d+)'
    evidence_matches = re.findall(evidence_pattern, text)

    for evidence, page in evidence_matches[:10]:  # Max 10 evidências
        structure["evidence_log"].append({
            "page": int(page),
            "evidence": evidence[:500],  # Limitar tamanho
            "type": "dialog" if "V.O." in evidence else "action"
        })

    # MELHORADO: Extrair personagens de múltiplas fontes
    characters = extract_characters(text)
    structure["analise_personagem"] = characters

    # Extrair estrutura narrativa
    for event in ['inciting_incident', 'climax', 'resolution']:
        match = re.search(patterns.get(event, ''), text)
        if match:
            content = match.group(1)
            page_match = re.search(r'"page"\s*:\s*"?(\d+)"?', content)
            desc_match = re.search(r'"description"\s*:\s*"([^"]+)"', content)

            structure["analise_estrutural"][event] = {
                "page": int(page_match.group(1)) if page_match else 1,
                "description": desc_match.group(1) if desc_match else "extracted"
            }

    return structure

def extract_characters(text: str) -> List[Dict]:
    """
    Extração melhorada de personagens
    Detecta personagens em diálogos, ações e menções
    """
    characters = []
    found_names = set()

    # Pattern 1: Personagens em formato JSON
    json_char_pattern = r'"name"\s*:\s*["\']([^"\']+)["\'][^}]*?"arc"\s*:\s*["\']([^"\']+)["\']'
    for name, arc in re.findall(json_char_pattern, text):
        if name not in found_names:
            characters.append({
                "name": name,
                "arc": arc,
                "motivation": "extracted"
            })
            found_names.add(name)

    # Pattern 2: Personagens em diálogos (incluindo V.O.)
    dialog_pattern = r'([A-Z][A-Z\s\.]+?)(?:\s*\(V\.O\.\))?\s*(?:\n|:|\s+says|\s+\()'
    for match in re.finditer(dialog_pattern, text):
        name = match.group(1).strip()
        # Limpar nome
        if len(name) > 2 and name not in ['INT', 'EXT', 'FADE', 'CUT', 'THE', 'AND']:
            clean_name = name.replace('(V.O.)', '').strip()
            if clean_name not in found_names:
                characters.append({
                    "name": clean_name,
                    "arc": "V.O. character" if '(V.O.)' in match.group(0) else "dialog character",
                    "motivation": "detected from dialog"
                })
                found_names.add(clean_name)

    # Pattern 3: Personagens em descrições de ação
    action_pattern = r'([A-Z][A-Za-z\s]+?)\s*\((\d+)\)[,\s]+([^.]+)'
    for name, age, description in re.findall(action_pattern, text):
        name = name.strip()
        if name not in found_names and len(name) > 2:
            characters.append({
                "name": name,
                "arc": f"Age {age}",
                "motivation": description[:50]
            })
            found_names.add(name)

    # Pattern 4: Detecção específica de IAs/Entidades
    # Procurar por nomes em maiúsculas que aparecem múltiplas vezes
    entity_pattern = r'\b([A-Z]{3,}(?:\s+[A-Z]+)*)\b'
    entities = re.findall(entity_pattern, text)
    entity_counts = {}
    for entity in entities:
        if entity not in ['INT', 'EXT', 'FADE', 'CUT', 'THE', 'AND', 'DAY', 'NIGHT']:
            entity_counts[entity] = entity_counts.get(entity, 0) + 1

    # Adicionar entidades que aparecem mais de uma vez
    for entity, count in entity_counts.items():
        if count > 1 and entity not in found_names:
            characters.append({
                "name": entity,
                "arc": "recurring entity",
                "motivation": f"appears {count} times"
            })
            found_names.add(entity)

    return characters[:10]  # Limitar a 10 personagens

def create_comprehensive_fallback(text: str) -> Dict:
    """Cria estrutura fallback compreensiva"""

    structure = {
        "status": "parsed_with_fallback",
        "confidence": 0.3,
        "raw_output": text[:1500] if text else "",
        "metadata": {},
        "evidence_log": [],
        "analise_estrutural": {},
        "analise_personagem": [],
        "validation": {"valid": False, "score": 0, "method": "safe_fallback"}
    }

    if not text:
        return structure

    text_lower = text.lower()

    # Detecção heurística de gênero
    genres = {
        'Ciência-Ficção': ['sci-fi', 'science', 'fiction', 'robot', 'ai', 'future', 'space'],
        'Drama': ['drama', 'emotion', 'family', 'conflict', 'relationship'],
        'Ação': ['action', 'fight', 'battle', 'chase', 'explosion'],
        'Comédia': ['comedy', 'funny', 'laugh', 'humor', 'joke'],
        'Thriller': ['thriller', 'suspense', 'mystery', 'danger', 'fear'],
        'Horror': ['horror', 'terror', 'scary', 'ghost', 'monster']
    }

    for genre, keywords in genres.items():
        if any(kw in text_lower for kw in keywords):
            structure["metadata"]["genre"] = genre
            structure["confidence"] += 0.1
            break

    # Extrair qualquer número como páginas
    pages_match = re.search(r'\b(\d+)\s*(?:pages?|páginas?)', text_lower)
    if pages_match:
        structure["metadata"]["pages"] = pages_match.group(1)
        structure["confidence"] += 0.05

    # Procurar título em maiúsculas
    title_match = re.search(r'^([A-Z][A-Z\s]+)$', text, re.MULTILINE)
    if title_match:
        structure["metadata"]["title"] = title_match.group(1).strip()
        structure["confidence"] += 0.05

    # Extrair linhas que parecem evidências
    lines = text.split('\n')
    for i, line in enumerate(lines[:20]):  # Primeiras 20 linhas
        line = line.strip()
        # Linhas que começam com INT. ou EXT. são cenários
        if line.startswith(('INT.', 'EXT.')):
            structure["evidence_log"].append({
                "page": 1,
                "evidence": line[:200],
                "type": "location"
            })
            structure["confidence"] += 0.02
        # Linhas em maiúsculas são possíveis diálogos
        elif line.isupper() and len(line) > 3 and len(line) < 50:
            structure["evidence_log"].append({
                "page": 1,
                "evidence": line,
                "type": "character_name"
            })
            structure["confidence"] += 0.02

    # Extrair personagens usando função melhorada
    structure["analise_personagem"] = extract_characters(text)
    if structure["analise_personagem"]:
        structure["confidence"] += 0.1

    # Detecção de estrutura narrativa básica
    if any(word in text_lower for word in ['beginning', 'início', 'starts', 'opens']):
        structure["analise_estrutural"]["has_beginning"] = True
        structure["confidence"] += 0.05

    if any(word in text_lower for word in ['climax', 'peak', 'confrontation', 'clímax']):
        structure["analise_estrutural"]["has_climax"] = True
        structure["confidence"] += 0.05

    if any(word in text_lower for word in ['ending', 'fim', 'resolution', 'fade out']):
        structure["analise_estrutural"]["has_ending"] = True
        structure["confidence"] += 0.05

    # Score baseado em quanto foi extraído
    extracted_items = (
        len(structure["metadata"]) +
        len(structure["evidence_log"]) +
        len(structure["analise_personagem"]) +
        len(structure["analise_estrutural"])
    )

    if extracted_items > 0:
        structure["validation"]["score"] = min(extracted_items * 10, 100)
        structure["validation"]["valid"] = True

    # Cap confidence at 0.7
    structure["confidence"] = min(structure["confidence"], 0.7)

    return structure

def calculate_confidence(data: Dict) -> float:
    """Calcula confiança baseado na completude dos dados"""

    confidence = 0.0

    # Verificar campos principais
    if data.get("metadata"):
        confidence += 0.2
        if data["metadata"].get("genre"):
            confidence += 0.1
        if data["metadata"].get("title"):
            confidence += 0.1
        if data["metadata"].get("pages"):
            confidence += 0.05

    if data.get("evidence_log"):
        confidence += 0.15
        if len(data["evidence_log"]) > 3:
            confidence += 0.1

    if data.get("analise_personagem"):
        confidence += 0.15
        if len(data["analise_personagem"]) > 2:
            confidence += 0.1

    if data.get("analise_estrutural"):
        confidence += 0.1
        struct_keys = len([k for k, v in data["analise_estrutural"].items() if v])
        confidence += min(struct_keys * 0.05, 0.15)

    if data.get("validation", {}).get("score", 0) > 50:
        confidence += 0.1

    return min(confidence, 0.95)  # Cap at 0.95

# Testes rápidos
if __name__ == "__main__":
    print("🧪 TESTANDO SAFE JSON PARSER ULTIMATE")
    print("="*60)

    test_cases = [
        # JSON válido
        '{"name": "test", "value": 123}',

        # Aspas mistas
        '{"key": \'value\', "num": 42}',

        # JSON com personagens
        '''{"evidence_log": [{"evidence": 'AURORA (V.O.) speaks', "page": 1}],
            "analise_personagem": [{"name": 'DR. SARAH CHEN', "arc": 'hero'}]}''',

        # Texto com personagens
        '''INT. LAB - DAY
        AURORA (V.O.)
        Why did you create me?

        DR. SARAH CHEN (35), brilliant scientist, hesitates.''',
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\nTeste {i}: {test[:40]}...")
        result, confidence = safe_json_parse(test)

        if result:
            print(f"  ✅ Parse OK (confiança: {confidence:.2f})")

            # Verificar se detectou personagens
            if result.get("analise_personagem"):
                chars = [p["name"] for p in result["analise_personagem"]]
                print(f"  Personagens: {', '.join(chars)}")

            if result.get("metadata"):
                print(f"  Metadata: {list(result['metadata'].keys())}")
        else:
            print(f"  ❌ Parse falhou")

    print("\n🥷 DIGIMUNDO PRESENTE")
