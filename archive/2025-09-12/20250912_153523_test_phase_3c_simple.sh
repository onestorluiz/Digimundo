#!/bin/bash

# Test Suite Phase 3.C - Versão Simplificada
# Testa componentes principais da AI

set -e

cd "$(dirname "$0")/.."
export PYTHONPATH=.

echo "🧠 FASE 3.C - TESTES SISTEMA AI (SIMPLIFICADO)"
echo "=============================================="

tests_passed=0
tests_total=0

run_test() {
    ((tests_total++))
    echo -n "$1... "
    if eval "$2" > /dev/null 2>&1; then
        echo "✅"
        ((tests_passed++))
    else
        echo "❌"
    fi
}

echo
echo "📊 Testando Módulos AI"
echo "---------------------"

# Sentiment
run_test "Sentiment import" "python3 -c 'from apps.scripturemon.ai_sentiment import analyze_text_sentiment'"
run_test "Sentiment analysis" "python3 -c 'from apps.scripturemon.ai_sentiment import analyze_text_sentiment; r = analyze_text_sentiment(\"happy\"); assert r.compound > 0'"

# Recommendations
run_test "Recommendations import" "python3 -c 'from apps.scripturemon.ai_recommendations import get_recommendation_engine'"
run_test "Recommendations creation" "python3 -c 'from apps.scripturemon.ai_recommendations import get_recommendation_engine; get_recommendation_engine()'"

# Comparison
run_test "Comparison import" "python3 -c 'from apps.scripturemon.ai_comparison import get_comparison_engine'"
run_test "Comparison creation" "python3 -c 'from apps.scripturemon.ai_comparison import get_comparison_engine; get_comparison_engine()'"

# Commercial
run_test "Commercial import" "python3 -c 'from apps.scripturemon.ai_commercial import get_commercial_predictor'"
run_test "Commercial creation" "python3 -c 'from apps.scripturemon.ai_commercial import get_commercial_predictor; get_commercial_predictor()'"

# Integration
run_test "Doctor integration" "python3 -c 'from apps.scripturemon.doctor import analyze'"

echo
echo "📋 RESULTADO"
echo "============"
echo "Passou: $tests_passed/$tests_total"

if [ $tests_passed -eq $tests_total ]; then
    echo "🎉 Todos os testes passaram!"
    exit 0
else
    echo "❌ Alguns testes falharam"
    exit 1
fi