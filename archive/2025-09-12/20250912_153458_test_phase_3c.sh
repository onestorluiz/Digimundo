#!/bin/bash

# Test Suite Phase 3.C - Sistema de AI Avançada
# Testa integração dos 4 módulos de AI: Sentiment, Recommendations, Comparison, Commercial

set -e

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

echo "🧠 FASE 3.C - TESTES SISTEMA AI AVANÇADA"
echo "========================================"
echo

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

success_count=0
test_count=0

test_result() {
    ((test_count++))
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
        ((success_count++))
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

echo "📊 1. Testando Análise de Sentimentos (ai_sentiment.py)"
echo "----------------------------------------------------"

# Test 1.1: Importar módulo de sentiment
PYTHONPATH=. python3 -c "
from apps.scripturemon.ai_sentiment import get_sentiment_analyzer, analyze_script_sentiment
print('✓ Importação ai_sentiment OK')
" 2>/dev/null
test_result $? "Importação do módulo ai_sentiment"

# Test 1.2: Criar analisador de sentimentos
PYTHONPATH=. python3 -c "
from apps.scripturemon.ai_sentiment import get_sentiment_analyzer
analyzer = get_sentiment_analyzer()
print('✓ Analisador de sentimentos criado')
" 2>/dev/null
test_result $? "Criação do analisador de sentimentos"

# Test 1.3: Análise básica de sentimentos
PYTHONPATH=. python3 -c "
from apps.scripturemon.ai_sentiment import analyze_text_sentiment
result = analyze_text_sentiment('Estou muito feliz com este resultado!')
assert result.compound > 0, 'Sentimento positivo esperado'
print('✓ Análise de sentimentos funcional')
" 2>/dev/null
test_result $? "Análise básica de sentimentos"

echo
echo "🎯 2. Testando Sistema de Recomendações (ai_recommendations.py)"
echo "-------------------------------------------------------------"

# Test 2.1: Importar módulo de recomendações
PYTHONPATH=. python3 -c "
from apps.scripturemon.ai_recommendations import get_recommendation_engine, generate_script_recommendations
print('✓ Importação ai_recommendations OK')
" 2>/dev/null
test_result $? "Importação do módulo ai_recommendations"

# Test 2.2: Criar engine de recomendações
PYTHONPATH=. python3 -c "
from apps.scripturemon.ai_recommendations import get_recommendation_engine
engine = get_recommendation_engine()
print('✓ Engine de recomendações criado')
" 2>/dev/null
test_result $? "Criação do engine de recomendações"

# Test 2.3: Gerar recomendações básicas
PYTHONPATH=. python3 -c "
from apps.scripturemon.ai_recommendations import get_recommendation_engine
engine = get_recommendation_engine()
analysis = {
    'score': 65,
    'analysis': {
        'structure': 'needs_improvement',
        'dialogue': 'good',
        'pacing': 'poor',
        'characters': 'good'
    }
}
recs = engine.generate_recommendations(analysis)
assert len(recs.quick_wins) > 0, 'Quick wins esperados'
print('✓ Geração de recomendações funcional')
" 2>/dev/null
test_result $? "Geração básica de recomendações"

echo
echo "⚖️ 3. Testando Comparação de Scripts (ai_comparison.py)"
echo "-----------------------------------------------------"

# Test 3.1: Importar módulo de comparação
PYTHONPATH=. python3 -c "
from apps.scripturemon.ai_comparison import get_comparison_engine
print('✓ Importação ai_comparison OK')
" 2>/dev/null
test_result $? "Importação do módulo ai_comparison"

# Test 3.2: Criar engine de comparação
PYTHONPATH=. python3 -c "
from apps.scripturemon.ai_comparison import get_comparison_engine
engine = get_comparison_engine()
print('✓ Engine de comparação criado')
" 2>/dev/null
test_result $? "Criação do engine de comparação"

# Test 3.3: Comparar scripts básicos
PYTHONPATH=. python3 -c "
from apps.scripturemon.ai_comparison import get_comparison_engine
engine = get_comparison_engine()
analysis_a = {'score': 70, 'analysis': {'structure': 'good', 'dialogue': 'excellent'}}
analysis_b = {'score': 60, 'analysis': {'structure': 'needs_improvement', 'dialogue': 'good'}}
comparison = engine.compare_scripts(analysis_a, analysis_b)
assert comparison.overall_similarity >= 0, 'Similaridade deve ser ≥ 0'
print('✓ Comparação de scripts funcional')
" 2>/dev/null
test_result $? "Comparação básica de scripts"

echo
echo "💰 4. Testando Predição Comercial (ai_commercial.py)"
echo "---------------------------------------------------"

# Test 4.1: Importar módulo comercial
PYTHONPATH=. python3 -c "
from apps.scripturemon.ai_commercial import get_commercial_predictor, predict_commercial_success
print('✓ Importação ai_commercial OK')
" 2>/dev/null
test_result $? "Importação do módulo ai_commercial"

# Test 4.2: Criar preditor comercial
PYTHONPATH=. python3 -c "
from apps.scripturemon.ai_commercial import get_commercial_predictor
predictor = get_commercial_predictor()
print('✓ Preditor comercial criado')
" 2>/dev/null
test_result $? "Criação do preditor comercial"

# Test 4.3: Predição comercial básica
PYTHONPATH=. python3 -c "
from apps.scripturemon.ai_commercial import get_commercial_predictor
predictor = get_commercial_predictor()
analysis = {
    'score': 75,
    'analysis': {'structure': 'good', 'dialogue': 'excellent', 'characters': 'good'},
    'genre': 'drama'
}
prediction = predictor.predict_success(analysis)
assert 0 <= prediction.overall_score <= 1, 'Score deve estar entre 0-1'
print('✓ Predição comercial funcional')
" 2>/dev/null
test_result $? "Predição comercial básica"

echo
echo "🔗 5. Testando Integração com Sistema Principal"
echo "----------------------------------------------"

# Test 5.1: Importação integrada no doctor.py
PYTHONPATH=. python3 -c "
from apps.scripturemon.doctor import analyze
print('✓ Integração doctor.py OK')
" 2>/dev/null
test_result $? "Integração com doctor.py"

# Test 5.2: Análise com AI ativada (se arquivo de teste existir)
if [ -f "data/test_scripts/PEQUENO_TESTE.txt" ]; then
    PYTHONPATH=. python3 -c "
from pathlib import Path
from apps.scripturemon.doctor import analyze
result = analyze(Path('data/test_scripts/PEQUENO_TESTE.txt'))
print('✓ Análise integrada funcional')
" 2>/dev/null
    test_result $? "Análise integrada com AI"
else
    echo -e "${YELLOW}⚠️  Arquivo de teste não encontrado - criando arquivo mínimo${NC}"
    mkdir -p data/test_scripts
    cat > data/test_scripts/PEQUENO_TESTE.txt << 'EOF'
TÍTULO: TESTE DE ROTEIRO

FADE IN:

INT. CASA - DIA

JOÃO está sentado na mesa, olhando pela janela.

JOÃO
(pensativo)
O que será que o futuro nos reserva?

MARIA entra na sala.

MARIA
João, você está bem?

JOÃO
(sorrindo)
Agora estou melhor.

FADE OUT.

FIM
EOF
    
    PYTHONPATH=. python3 -c "
from pathlib import Path
from apps.scripturemon.doctor import analyze
result = analyze(Path('data/test_scripts/PEQUENO_TESTE.txt'))
assert result['status'] == 'success', 'Análise deve ser bem-sucedida'
print('✓ Análise integrada funcional')
" 2>/dev/null
    test_result $? "Análise integrada com AI (arquivo criado)"
fi

echo
echo "🧪 6. Testando Funções Avançadas"
echo "-------------------------------"

# Test 6.1: Deep analyze
PYTHONPATH=. python3 -c "
from pathlib import Path
from apps.scripturemon.doctor import deep_analyze
result = deep_analyze(Path('data/test_scripts/PEQUENO_TESTE.txt'), mode='comprehensive')
assert 'deep_metrics' in result, 'Deep metrics esperados'
print('✓ Deep analyze funcional')
" 2>/dev/null
test_result $? "Deep analyze com métricas AI"

# Test 6.2: Validação de script
PYTHONPATH=. python3 -c "
from pathlib import Path
from apps.scripturemon.doctor import validate_script
result = validate_script(Path('data/test_scripts/PEQUENO_TESTE.txt'))
assert result['valid'] == True, 'Script deve ser válido'
print('✓ Validação de script funcional')
" 2>/dev/null
test_result $? "Validação de script"

echo
echo "📋 RESULTADO DOS TESTES FASE 3.C"
echo "================================"
echo -e "Testes executados: ${BLUE}$test_count${NC}"
echo -e "Testes com sucesso: ${GREEN}$success_count${NC}"
echo -e "Testes com falha: ${RED}$((test_count - success_count))${NC}"

if [ $success_count -eq $test_count ]; then
    echo -e "\n${GREEN}🎉 TODOS OS TESTES PASSARAM!${NC}"
    echo -e "${GREEN}✅ Fase 3.C - Sistema de AI Avançada implementado com sucesso${NC}"
    exit 0
else
    echo -e "\n${RED}❌ ALGUNS TESTES FALHARAM${NC}"
    echo -e "${YELLOW}⚠️  Verifique os erros acima antes de prosseguir${NC}"
    exit 1
fi