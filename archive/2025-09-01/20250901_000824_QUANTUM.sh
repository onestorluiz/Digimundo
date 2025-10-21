#!/bin/bash
echo "⚛️ ATIVANDO PERFIL QUANTUM (26GB)"
echo "=================================="
echo ""
echo "Modelo: mixtral:8x7b"
echo "RAM: 26GB"
echo "Função: 8 especialistas simultâneos"
echo ""

# Analisa o roteiro passado como argumento ou usa exemplo
if [ -z "$1" ]; then
    ROTEIRO="FADE IN: INT. OFFICE - DAY. John enters. JOHN: I need help. FADE OUT."
else
    ROTEIRO=$(cat "$1")
fi

echo "Processando com QUANTUM (8 especialistas)..."
echo ""

ollama run mixtral:8x7b "ANÁLISE MULTI-PERSPECTIVA COM 8 ESPECIALISTAS:

$ROTEIRO

Analise como:
1. Diretor visionário
2. Roteirista veterano
3. Produtor executivo
4. Editor experiente
5. Diretor de fotografia
6. Designer de produção
7. Compositor de trilha
8. Distribuidor internacional

Para CADA perspectiva:
- Pontos fortes e fracos
- Score (0-100)
- Viabilidade comercial
- Previsão de bilheteria"

echo ""
echo "✅ Análise QUANTUM completa!"