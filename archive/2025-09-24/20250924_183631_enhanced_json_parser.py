#!/usr/bin/env python3
"""
ENHANCED JSON PARSER - VERSÃO ROBUSTA
Handles malformed JSON, mixed quotes, and nested structures
"""

import json
import re
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class EnhancedJSONParser:
    """Parser robusto para JSONs malformados do Ollama"""
    
    def __init__(self):
        self.success_count = 0
        self.failure_count = 0
        self.recovery_count = 0
        
    def parse(self, text: str) -> Optional[Dict[Any, Any]]:
        """Parse principal com múltiplas estratégias"""
        if not text:
            return None
            
        # Estratégia 1: Tentar parse direto
        result = self._try_direct_parse(text)
        if result:
            self.success_count += 1
            return result
            
        # Estratégia 2: Limpar e tentar novamente
        cleaned = self._clean_json_text(text)
        result = self._try_direct_parse(cleaned)
        if result:
            self.recovery_count += 1
            return result
            
        # Estratégia 3: Bracket counting extraction
        extracted = self._extract_json_by_brackets(text)
        if extracted:
            result = self._try_direct_parse(extracted)
            if result:
                self.recovery_count += 1
                return result
                
        # Estratégia 4: Fix quotes e tentar
        fixed_quotes = self._fix_mixed_quotes(cleaned if cleaned else text)
        result = self._try_direct_parse(fixed_quotes)
        if result:
            self.recovery_count += 1
            return result
            
        # Estratégia 5: Reconstrução estrutural
        reconstructed = self._reconstruct_json(text)
        if reconstructed:
            self.recovery_count += 1
            return reconstructed
            
        # Falhou todas as estratégias
        self.failure_count += 1
        logger.error(f"Failed to parse JSON after all strategies")
        return None
    
    def _try_direct_parse(self, text: str) -> Optional[Dict]:
        """Tenta parse direto do JSON"""
        try:
            return json.loads(text)
        except (json.JSONDecodeError, TypeError, ValueError):
            return None
    
    def _clean_json_text(self, text: str) -> str:
        """Limpa texto para facilitar parsing"""
        # Remove caracteres de controle
        text = re.sub(r'[\x00-\x1f]', '', text)
        
        # Remove espaços extras
        text = re.sub(r'\s+', ' ', text)
        
        # Remove comentários estilo JavaScript
        text = re.sub(r'//.*?\n', '', text)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        
        # Remove trailing commas
        text = re.sub(r',\s*}', '}', text)
        text = re.sub(r',\s*]', ']', text)
        
        return text.strip()
    
    def _extract_json_by_brackets(self, text: str) -> Optional[str]:
        """Extrai JSON usando contagem de brackets"""
        if '{' not in text:
            return None
            
        start_idx = text.find('{')
        bracket_count = 0
        in_string = False
        escape_next = False
        quote_char = None
        
        for i in range(start_idx, len(text)):
            char = text[i]
            
            # Handle escape sequences
            if escape_next:
                escape_next = False
                continue
                
            if char == '\\':
                escape_next = True
                continue
            
            # Handle strings
            if char in ['"', "'"] and not in_string:
                in_string = True
                quote_char = char
            elif char == quote_char and in_string:
                in_string = False
                quote_char = None
            
            # Count brackets only outside strings
            if not in_string:
                if char == '{':
                    bracket_count += 1
                elif char == '}':
                    bracket_count -= 1
                    if bracket_count == 0:
                        return text[start_idx:i+1]
        
        # Se não fechou, tenta fechar artificialmente
        if bracket_count > 0:
            return text[start_idx:] + ('}' * bracket_count)
            
        return None
    
    def _fix_mixed_quotes(self, text: str) -> str:
        """Corrige quotes mistas para double quotes"""
        # Primeiro, protege strings já válidas com double quotes
        protected = []
        
        def protect_string(match):
            protected.append(match.group(0))
            return f'__PROTECTED_{len(protected)-1}__'
        
        # Protege strings com double quotes válidas
        text = re.sub(r'"(?:[^"\\]|\\.)*"', protect_string, text)
        
        # Converte single quotes para double quotes
        # Para keys
        text = re.sub(r"'([^']+)'\s*:", r'"\1":', text)
        # Para values
        text = re.sub(r":\s*'([^']*)'", r': "\1"', text)
        
        # Restaura strings protegidas
        for i, protected_str in enumerate(protected):
            text = text.replace(f'__PROTECTED_{i}__', protected_str)
        
        return text
    
    def _reconstruct_json(self, text: str) -> Optional[Dict]:
        """Tenta reconstruir JSON parseando elementos"""
        result = {}
        
        # Padrões para encontrar pares key-value
        patterns = [
            # "key": "value" ou 'key': 'value'
            r'["\']([^"\'\']+)["\']\s*:\s*["\']([^"\'\']*)["\']',
            # "key": number
            r'["\']([^"\'\']+)["\']\s*:\s*(\d+(?:\.\d+)?)',
            # "key": boolean
            r'["\']([^"\'\']+)["\']\s*:\s*(true|false|null)',
            # "key": [...]
            r'["\']([^"\'\']+)["\']\s*:\s*(\[[^\]]*\])',
            # "key": {...}
            r'["\']([^"\'\']+)["\']\s*:\s*(\{[^}]*\})',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                key = match.group(1)
                value = match.group(2)
                
                # Tenta converter o valor para o tipo apropriado
                if value.lower() in ['true', 'false', 'null']:
                    value = {'true': True, 'false': False, 'null': None}[value.lower()]
                elif value.startswith('[') or value.startswith('{'):
                    try:
                        value = json.loads(value)
                    except:
                        pass  # Mantém como string
                elif re.match(r'^\d+$', value):
                    value = int(value)
                elif re.match(r'^\d+\.\d+$', value):
                    value = float(value)
                
                result[key] = value
        
        return result if result else None
    
    def get_stats(self) -> Dict[str, int]:
        """Retorna estatísticas do parser"""
        total = self.success_count + self.failure_count
        success_rate = (self.success_count / total * 100) if total > 0 else 0
        recovery_rate = (self.recovery_count / total * 100) if total > 0 else 0
        
        return {
            'total_attempts': total,
            'direct_success': self.success_count - self.recovery_count,
            'recovered': self.recovery_count,
            'failures': self.failure_count,
            'success_rate': round(success_rate, 2),
            'recovery_rate': round(recovery_rate, 2)
        }

# ==================== TESTES DO PARSER ====================

def test_enhanced_parser():
    """Testa o parser melhorado com casos difíceis"""
    parser = EnhancedJSONParser()
    
    test_cases = [
        # Caso 1: JSON válido
        ('{"key": "value"}', True),
        
        # Caso 2: Mixed quotes
        ("{'key': 'value', \"key2\": \"value2\"}", True),
        
        # Caso 3: Nested with mixed quotes
        ("{'outer': {'inner': 'value'}}", True),
        
        # Caso 4: Trailing comma
        ('{"key": "value",}', True),
        
        # Caso 5: Missing closing bracket
        ('{"key": "value"', True),  # Should fix
        
        # Caso 6: Aurora (V.O.) case
        ('{"character": "AURORA (V.O.)", "type": "AI"}', True),
        
        # Caso 7: Complex nested
        ('''
        {
            "characters": [
                {"name": "SARAH", "role": "protagonist"},
                {'name': 'AURORA (V.O.)', "type": 'AI entity'}
            ],
            'total': 2
        }
        ''', True),
        
        # Caso 8: With comments (invalid JSON)
        ('''
        {
            // This is a comment
            "key": "value",
            /* Block comment */
            "key2": "value2"
        }
        ''', True),
        
        # Caso 9: Escape characters
        ('{"quote": "She said \\"Hello\\""}', True),
        
        # Caso 10: Numbers and booleans
        ('{"count": 42, "active": true, "data": null}', True),
    ]
    
    results = []
    for i, (test_input, should_pass) in enumerate(test_cases, 1):
        result = parser.parse(test_input)
        passed = (result is not None) == should_pass
        results.append(passed)
        
        status = "✅" if passed else "❌"
        print(f"{status} Test {i}: {'PASSED' if passed else 'FAILED'}")
        if result and i <= 3:  # Show first 3 results
            print(f"   Result: {result}")
    
    print("\n📊 Parser Statistics:")
    stats = parser.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n🎯 Overall Test Success Rate: {success_rate:.1f}%")
    
    return success_rate >= 90  # Target 90% success

if __name__ == "__main__":
    print("🔧 Testing Enhanced JSON Parser...\n")
    success = test_enhanced_parser()
    
    if success:
        print("\n✅ Enhanced Parser READY for production!")
    else:
        print("\n⚠️ Parser needs more work")
