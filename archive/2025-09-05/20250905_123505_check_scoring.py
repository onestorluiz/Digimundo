#!/usr/bin/env python3
"""Check para verificar o sistema de scoring variável"""

import sys
import json
import traceback
from pathlib import Path
from typing import Dict, Any

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def run_check(settings: Dict) -> Dict:
    """Executa verificação do sistema de scoring"""
    result = {
        'pass': False,
        'status': 'running',
        'notes': [],
        'details': {}
    }
    
    try:
        # Importar ScriptScorer
        from src.validator.scoring import ScriptScorer
        
        # Criar instância
        scorer = ScriptScorer(settings)
        result['notes'].append('ScriptScorer instantiated')
        
        # Preparar scripts de teste com qualidades diferentes
        test_scripts = [
            {
                'id': 'poor_script',
                'content': """
                João entra na sala.
                JOÃO: Oi.
                Maria responde.
                MARIA: Oi.
                Eles conversam sobre coisas.
                FIM.
                """,
                'expected_range': (30, 50)  # Script ruim
            },
            {
                'id': 'average_script',
                'content': """
                INT. CAFÉ - DIA
                
                João, 30 anos, nervoso, entra no café lotado.
                
                JOÃO
                (sussurrando)
                Você tem certeza que ninguém nos seguiu?
                
                MARIA
                (olhando pela janela)
                Por enquanto estamos seguros. Mas precisamos agir rápido.
                
                João puxa uma pasta de documentos.
                
                JOÃO
                Estas provas podem mudar tudo.
                
                FADE OUT.
                """,
                'expected_range': (50, 70)  # Script médio
            },
            {
                'id': 'excellent_script',
                'content': """
                INT. ESCRITÓRIO ABANDONADO - NOITE
                
                CLOSE em mãos trêmulas segurando uma fotografia antiga.
                
                SARAH (V.O.)
                Dizem que o tempo cura todas as feridas...
                
                PULL BACK para revelar SARAH (45), cicatrizes emocionais 
                visíveis em seus olhos cansados. Ela está sozinha em meio
                a caixas de mudança, cada uma rotulada com datas diferentes.
                
                SARAH (V.O.)
                ...mas algumas feridas apenas aprendem a se esconder.
                
                Um TELEFONE TOCA, ecoando no espaço vazio. Sarah hesita,
                sua mão paira sobre o aparelho. Na tela: "NÚMERO DESCONHECIDO".
                
                SARAH
                (para si mesma, quase inaudível)
                Quinze anos de silêncio...
                
                Ela atende. Silêncio do outro lado, apenas uma respiração.
                
                VOZ (FILTRADA)
                Você sabe quem sou.
                
                A fotografia cai de suas mãos - nela, duas crianças sorrindo,
                antes de tudo mudar.
                
                MATCH CUT TO:
                
                INT. MESMO ESCRITÓRIO - 15 ANOS ANTES - DIA
                
                As mesmas crianças da foto, agora vivas e rindo...
                
                FADE TO BLACK.
                """,
                'expected_range': (70, 95)  # Script excelente
            }
        ]
        
        # Teste 1: Scoring variável (não fixo em 62)
        scores = []
        for script in test_scripts:
            score_result = scorer.score(script['content'])
            score = score_result.get('total_score', 0)
            scores.append(score)
            
            result['notes'].append(f'{script["id"]}: {score:.1f}/100')
            
            # Verificar se está na faixa esperada
            min_expected, max_expected = script['expected_range']
            if min_expected <= score <= max_expected:
                result['details'][f'score_{script["id"]}'] = 'PASS'
            else:
                result['details'][f'score_{script["id"]}'] = 'FAIL'
                result['notes'].append(f'Expected {min_expected}-{max_expected}, got {score:.1f}')
        
        # Teste 2: Verificar que scores são diferentes (não todos 62)
        unique_scores = set(scores)
        if len(unique_scores) == len(scores):
            result['details']['variable_scoring'] = 'PASS'
            result['notes'].append('All scores are different')
        else:
            result['details']['variable_scoring'] = 'FAIL'
            result['notes'].append(f'Duplicate scores found: {scores}')
        
        # Teste 3: Nenhum score é exatamente 62 (valor fixo antigo)
        if 62.0 not in scores:
            result['details']['no_fixed_62'] = 'PASS'
            result['notes'].append('No fixed 62 score found')
        else:
            result['details']['no_fixed_62'] = 'FAIL'
            result['notes'].append('Found old fixed score of 62')
        
        # Teste 4: Breakdown de critérios
        detailed_result = scorer.score(test_scripts[1]['content'])
        breakdown = detailed_result.get('breakdown', {})
        
        expected_criteria = ['structure', 'dialogue', 'characters', 'pacing', 
                           'theme', 'originality', 'emotional_impact']
        
        missing_criteria = [c for c in expected_criteria if c not in breakdown]
        
        if not missing_criteria:
            result['details']['criteria_breakdown'] = 'PASS'
            result['notes'].append('All scoring criteria present')
        else:
            result['details']['criteria_breakdown'] = 'FAIL'
            result['notes'].append(f'Missing criteria: {missing_criteria}')
        
        # Teste 5: Pesos configuráveis
        custom_weights = settings.get('scoring', {}).get('weights', {})
        if custom_weights:
            result['details']['configurable_weights'] = 'PASS'
            result['notes'].append(f'Using custom weights: {list(custom_weights.keys())}')
        else:
            result['details']['configurable_weights'] = 'WARN'
            result['notes'].append('No custom weights configured')
        
        # Determinar status final
        failures = [k for k, v in result['details'].items() if v == 'FAIL']
        if not failures:
            result['pass'] = True
            result['status'] = 'passed'
            result['reason'] = 'All scoring checks passed'
        else:
            result['status'] = 'failed'
            result['reason'] = f'Failed checks: {", ".join(failures)}'
        
    except ImportError as e:
        result['status'] = 'blocked'
        result['reason'] = f'Import error: {str(e)}'
        result['exception'] = str(e)
    except Exception as e:
        result['status'] = 'error'
        result['reason'] = f'Unexpected error: {str(e)}'
        result['exception'] = str(e)
        result['traceback'] = traceback.format_exc()
    
    return result

if __name__ == "__main__":
    # Para teste local
    from generate_inventory import load_default_settings
    settings = load_default_settings()
    result = run_check(settings)
    print(json.dumps(result, indent=2))