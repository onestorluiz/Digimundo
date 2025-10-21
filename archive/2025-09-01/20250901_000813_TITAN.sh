#!/bin/bash
echo "🏔️ ATIVANDO PERFIL TITAN (19GB)"
echo "================================"
echo ""
echo "Modelo: yi:34b"
echo "RAM: 19GB"
echo "Função: Análise cinematográfica profunda"
echo ""

# Analisa o roteiro passado como argumento ou usa exemplo
if [ -z "$1" ]; then
    ROTEIRO="FADE IN: INT. OFFICE - DAY. John enters. JOHN: I need help. FADE OUT."
else
    ROTEIRO=$(cat "$1")
fi

echo "Processando com TITAN..."
echo ""

ollama run yi:34b "ANÁLISE CINEMATOGRÁFICA PROFUNDA:

$ROTEIRO

Analise:
1. Estrutura de 3 atos
2. Todos os plot points
3. Psicologia dos personagens
4. Compare com Citizen Kane, The Godfather, Chinatown
5. Score detalhado (0-100)
6. Problemas específicos
7. Sugestões de reescrita

Seja EXTREMAMENTE detalhado."

echo ""
echo "✅ Análise TITAN completa!"