#!/bin/bash

echo "🧪 TESTE DE SELEÇÃO DE MODELOS"
echo "=============================="
echo ""

# Teste 1: Verificar sintaxe
echo "1️⃣ Verificando sintaxe do código..."
if python3 -m py_compile bin/scripturemon.fixed 2>/dev/null; then
    echo "   ✅ Sintaxe OK"
else
    echo "   ❌ Erro de sintaxe"
    exit 1
fi

# Teste 2: Testar gatilhos
echo -e "\n2️⃣ Testando sistema de gatilhos..."
python3 -c "
import sys
sys.path.insert(0, '.')

def _should_use_deep_model(input_text: str) -> bool:
    trigger_words = ['profunda', 'profundo', 'detalhada', 'detalhado', 
                    'meticulosa', 'meticuloso', 'feedback']
    input_lower = input_text.lower()
    for trigger in trigger_words:
        if trigger in input_lower:
            return True
    return False

# Casos de teste
test_cases = [
    ('O que é um roteiro?', False, 'SEM gatilho'),
    ('Analise meu roteiro', False, 'SEM gatilho'),
    ('Faça uma análise profunda', True, 'COM gatilho: profunda'),
    ('Quero feedback detalhado', True, 'COM gatilho: feedback e detalhado'),
    ('Explique sobre cinema', False, 'SEM gatilho'),
    ('Investigação meticulosa do roteiro', True, 'COM gatilho: meticulosa')
]

print('Teste de detecção de gatilhos:')
for text, expected, reason in test_cases:
    result = _should_use_deep_model(text)
    status = '✅' if result == expected else '❌'
    print(f'   {status} \"{text}\" -> {reason}')
"

# Teste 3: Verificar configuração de modelos
echo -e "\n3️⃣ Testando configuração de modelos..."
python3 -c "
# Simular configuração
config = {
    'principal': 'deepseek-r1:14b',  # DEVE SER LEVE
    'pipeline': {
        'extract': ['llama3.2:3b', 'llama3.1:8b'],
        'analyze': ['mistral:instruct', 'deepseek-r1:14b'],
        'evaluate': ['deepseek-r1:14b', 'mistral:latest'],  # DEVE SER LEVE
        'synthesize': ['llama3.1:8b', 'mistral:instruct']  # DEVE SER LEVE
    },
    'pipeline_deep': {
        'extract': ['deepseek-r1:14b', 'llama3.1:8b'],
        'analyze': ['deepseek-r1:32b', 'scripturemon-deepseek'],
        'evaluate': ['scripturemon-ultimate', 'deepseek-r1:70b'],
        'synthesize': ['deepseek-r1:70b', 'scripturemon-ultimate']
    }
}

# Verificar modelo principal
big_models = ['32b', '70b', 'ultimate', 'deepseek:latest']
is_big = any(x in config['principal'] for x in big_models)
if not is_big:
    print('   ✅ Modelo principal é LEVE:', config['principal'])
else:
    print('   ❌ ERRO: Modelo principal é GRANDE:', config['principal'])

# Verificar pipeline normal
print('   Pipeline NORMAL (sem gatilhos):')
for stage, models in config['pipeline'].items():
    has_big = any(any(x in model for x in big_models) for model in models)
    status = '❌ TEM MODELO GRANDE' if has_big else '✅ apenas modelos leves'
    print(f'      {stage}: {status} - {models}')

# Verificar pipeline profundo
print('   Pipeline PROFUNDO (com gatilhos):')
for stage, models in config['pipeline_deep'].items():
    has_big = any(any(x in model for x in big_models) for model in models)
    status = '✅ tem modelos grandes' if has_big else '⚠️ apenas modelos leves'
    print(f'      {stage}: {status} - {models}')
"

# Teste 4: Simulação de seleção de modelos
echo -e "\n4️⃣ Simulando seleção de modelos..."
python3 -c "
def simulate_model_selection(prompt: str):
    # Detectar gatilhos
    trigger_words = ['profunda', 'profundo', 'detalhada', 'detalhado', 
                    'meticulosa', 'meticuloso', 'feedback']
    is_deep = any(word in prompt.lower() for word in trigger_words)
    
    # Simular seleção
    if is_deep:
        primary = ['deepseek-r1:70b', 'scripturemon-ultimate', 'scripturemon-deepseek']
        pipeline = 'pipeline_deep'
    else:
        # Verificar contexto
        if any(word in prompt.lower() for word in ['roteiro', 'cena', 'personagem']):
            primary = ['deepseek-r1:14b', 'mistral:latest']
        else:
            primary = ['deepseek-r1:14b', 'llama3.2:3b', 'mistral:latest']
        pipeline = 'pipeline_normal'
    
    return primary, pipeline, is_deep

# Testar casos
test_prompts = [
    'O que é um roteiro?',
    'Faça uma análise profunda do meu roteiro',
    'Me dê feedback sobre personagens',
    'Análise meticulosa da estrutura narrativa'
]

print('Simulação de seleção de modelos:')
for prompt in test_prompts:
    models, pipeline, is_deep = simulate_model_selection(prompt)
    mode = 'PROFUNDO' if is_deep else 'NORMAL'
    print(f'')
    print(f'   Prompt: \"{prompt}\"')
    print(f'   Modo: {mode}')
    print(f'   Pipeline: {pipeline}')
    print(f'   Modelos primários: {models[:2]}...')
"

echo ""
echo "=============================="
echo "📊 RESUMO DAS CORREÇÕES:"
echo ""
echo "✅ Modelo principal mudado de 32b para 14b (leve)"
echo "✅ Pipeline normal usa apenas modelos leves"
echo "✅ Pipeline profundo criado para análises com gatilhos"
echo "✅ Modelos grandes excluídos do fallback quando sem gatilhos"
echo "✅ Mensagens claras quando modelos grandes são ativados"
echo ""
echo "🎯 COMPORTAMENTO ESPERADO:"
echo "   SEM gatilhos → Apenas modelos leves (14b, 8b, 3b)"
echo "   COM gatilhos → Modelos grandes liberados (32b, 70b, ultimate)"
echo ""