#!/bin/bash
echo "🧠 ATIVANDO PERFIL NEURAL (42GB)"
echo "================================"
echo ""
echo "Modelo: llama3.1:70b"
echo "RAM: 42GB"
echo "Função: Reescrita completa e otimização"
echo ""

# Analisa o roteiro passado como argumento ou usa exemplo
if [ -z "$1" ]; then
    ROTEIRO="FADE IN: INT. OFFICE - DAY. John enters. JOHN: I need help. FADE OUT."
else
    ROTEIRO=$(cat "$1")
fi

echo "Processando com NEURAL..."
echo ""

ollama run llama3.1:70b "REESCRITA COMPLETA E OTIMIZAÇÃO:

$ROTEIRO

Execute:
1. REESCREVA o roteiro melhorado
2. Crie 3 VERSÕES alternativas (Drama/Comédia/Thriller)
3. OTIMIZE cada diálogo
4. Adicione DIREÇÕES de câmera
5. Crie BACKSTORY dos personagens
6. Sugira TRILHA SONORA

Seja criativo e detalhado."

echo ""
echo "✅ Análise NEURAL completa!"