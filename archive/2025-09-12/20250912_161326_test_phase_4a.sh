#!/bin/bash

# Test Suite Phase 4.A - Interface e Visualização AI
# Testa sistema web, visualizações e relatórios

set -e

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

echo "🎨 FASE 4.A - TESTES INTERFACE E VISUALIZAÇÃO"
echo "============================================="
echo

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
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

echo "🌐 1. Testando Sistema Web (Flask)"
echo "---------------------------------"

# Test 1.1: Importar aplicação Flask
PYTHONPATH=. python3 -c "
from apps.web.app import create_app
app = create_app()
print('✓ Aplicação Flask criada')
" 2>/dev/null
test_result $? "Criação da aplicação Flask"

# Test 1.2: Verificar rotas principais
PYTHONPATH=. python3 -c "
from apps.web.app import app
routes = [rule.rule for rule in app.url_map.iter_rules()]
assert '/' in routes, 'Rota index não encontrada'
assert '/analyze' in routes, 'Rota analyze não encontrada'
assert '/api/status' in routes, 'API status não encontrada'
print('✓ Rotas configuradas corretamente')
" 2>/dev/null
test_result $? "Configuração de rotas"

echo
echo "📊 2. Testando Sistema de Visualizações"
echo "-------------------------------------"

# Test 2.1: ChartGenerator
PYTHONPATH=. python3 -c "
from apps.visualizations import ChartGenerator
generator = ChartGenerator()
gauge = generator.create_score_gauge(75, 'Test Score')
assert gauge, 'Gauge não gerado'
print('✓ ChartGenerator funcional')
" 2>/dev/null
test_result $? "ChartGenerator"

# Test 2.2: SentimentVisualizer
PYTHONPATH=. python3 -c "
from apps.visualizations import SentimentVisualizer
viz = SentimentVisualizer()
data = {'positive': 0.6, 'negative': 0.2, 'neutral': 0.2, 'compound': 0.4}
chart = viz.create_sentiment_distribution(data)
assert chart, 'Visualização sentimento não gerada'
print('✓ SentimentVisualizer funcional')
" 2>/dev/null
test_result $? "SentimentVisualizer"

# Test 2.3: ComparisonVisualizer
PYTHONPATH=. python3 -c "
from apps.visualizations import ComparisonVisualizer
viz = ComparisonVisualizer()
gauge = viz.create_similarity_gauge(0.75)
assert gauge, 'Gauge similaridade não gerado'
print('✓ ComparisonVisualizer funcional')
" 2>/dev/null
test_result $? "ComparisonVisualizer"

# Test 2.4: CommercialVisualizer
PYTHONPATH=. python3 -c "
from apps.visualizations import CommercialVisualizer
viz = CommercialVisualizer()
gauge = viz.create_commercial_score_gauge(0.8, 0.9)
assert gauge, 'Gauge comercial não gerado'
print('✓ CommercialVisualizer funcional')
" 2>/dev/null
test_result $? "CommercialVisualizer"

echo
echo "📄 3. Testando Sistema de Relatórios"
echo "----------------------------------"

# Test 3.1: HTMLReportGenerator
PYTHONPATH=. python3 -c "
from apps.reports import HTMLReportGenerator
from pathlib import Path
generator = HTMLReportGenerator()
print('✓ HTMLReportGenerator criado')
" 2>/dev/null
test_result $? "HTMLReportGenerator"

# Test 3.2: PDFReportGenerator
PYTHONPATH=. python3 -c "
from apps.reports import PDFReportGenerator
generator = PDFReportGenerator()
print('✓ PDFReportGenerator criado')
" 2>/dev/null
test_result $? "PDFReportGenerator"

# Test 3.3: Geração de HTML básico
PYTHONPATH=. python3 -c "
from apps.reports import HTMLReportGenerator
from pathlib import Path
import tempfile
generator = HTMLReportGenerator()
data = {
    'score': 75,
    'grade': 'B',
    'executive_summary': 'Test summary',
    'strengths': ['Good structure'],
    'weaknesses': ['Needs polish']
}
with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
    output = Path(f.name)
    html = generator._generate_basic_html(data, 'executive')
    assert '<html' in html, 'HTML não gerado'
    assert '75' in html, 'Score não incluído'
print('✓ Geração HTML básica funcional')
" 2>/dev/null
test_result $? "Geração de HTML básico"

echo
echo "🔗 4. Testando Integração"
echo "----------------------"

# Test 4.1: Web + Visualizations
PYTHONPATH=. python3 -c "
from apps.web.app import app
from apps.visualizations import ChartGenerator
with app.test_client() as client:
    response = client.get('/api/status')
    assert response.status_code == 200, 'API status falhou'
    data = response.get_json()
    assert data['status'] == 'active', 'Status incorreto'
print('✓ Integração Web + API funcional')
" 2>/dev/null
test_result $? "Integração Web + API"

# Test 4.2: Templates existem
if [ -d "apps/web/templates" ]; then
    echo -e "${GREEN}✅ Diretório de templates existe${NC}"
    ((success_count++))
    ((test_count++))
else
    echo -e "${RED}❌ Diretório de templates não encontrado${NC}"
    ((test_count++))
fi

# Test 4.3: Static files existem
if [ -d "apps/web/static" ]; then
    echo -e "${GREEN}✅ Diretório static existe${NC}"
    ((success_count++))
    ((test_count++))
else
    echo -e "${RED}❌ Diretório static não encontrado${NC}"
    ((test_count++))
fi

echo
echo "📋 RESULTADO DOS TESTES FASE 4.A"
echo "================================"
echo -e "Testes executados: ${YELLOW}$test_count${NC}"
echo -e "Testes com sucesso: ${GREEN}$success_count${NC}"
echo -e "Testes com falha: ${RED}$((test_count - success_count))${NC}"

if [ $success_count -eq $test_count ]; then
    echo -e "\n${GREEN}🎉 TODOS OS TESTES PASSARAM!${NC}"
    echo -e "${GREEN}✅ Fase 4.A - Interface e Visualização implementada com sucesso${NC}"
    exit 0
else
    echo -e "\n${RED}❌ ALGUNS TESTES FALHARAM${NC}"
    echo -e "${YELLOW}⚠️  Verifique os erros acima antes de prosseguir${NC}"
    exit 1
fi