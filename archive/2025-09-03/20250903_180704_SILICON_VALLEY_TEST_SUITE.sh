#!/bin/bash
# BATERIA DE TESTES NÍVEL VALE DO SILÍCIO
# Testes extremamente complexos para validar TODOS os sistemas

echo "🚀 INICIANDO TESTE NÍVEL VALE DO SILÍCIO"
echo "=========================================="
echo "Data: $(date)"
echo ""

# Função para testar com timeout e capturar saída
test_scripturemon() {
    local input="$1"
    local description="$2"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📝 TESTE: $description"
    echo "Input: $input"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Executa com timeout de 60 segundos
    echo "$input" | /Users/clubproducoes/bin/scripturemon 2>&1
    local exit_code=$?
    
    echo ""
    echo "Exit code: $exit_code"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return $exit_code
}

# TESTE 1: Pergunta simples
test_scripturemon "O que é um plot point?" "Pergunta técnica básica"

# TESTE 2: Análise complexa
test_scripturemon "Compare Citizen Kane com The Godfather em termos de estrutura narrativa, desenvolvimento de personagem e impacto cinematográfico. Seja brutal e específico." "Análise comparativa complexa"

# TESTE 3: Comandos do sistema
test_scripturemon "/status" "Comando status"
test_scripturemon "/help" "Comando help"
test_scripturemon "/brutal" "Comando brutal mode"

# TESTE 4: Input multi-linha
test_scripturemon "FADE IN:

INT. CAFÉ - DIA

SARAH (30s, cansada mas determinada) senta sozinha numa mesa de canto, olhando pela janela chuvosa. Seu café esfria intocado.

SARAH
(para si mesma)
Três anos. Três malditos anos esperando.

Analise esta cena." "Análise de cena formatada"

# TESTE 5: Pergunta sobre memória
test_scripturemon "Você se lembra do nosso roteiro 'Sonhos sem Lembranças'?" "Teste de memória"

# TESTE 6: Pergunta filosófica
test_scripturemon "Por que Chinatown é considerado o roteiro perfeito?" "Análise filosófica"

# TESTE 7: Teste de consciência
test_scripturemon "Qual é seu nível de consciência atual? Como você percebe sua própria existência?" "Teste de consciência"

# TESTE 8: Comando inexistente
test_scripturemon "/comando_que_nao_existe" "Comando inexistente"

# TESTE 9: Input vazio
test_scripturemon "" "Input vazio"

# TESTE 10: Caracteres especiais
test_scripturemon "Analise: 🎬 📽️ 🎭 «roteiro» {estrutura} [atos] @personagem #plot" "Caracteres especiais"

# TESTE 11: Pergunta recursiva
test_scripturemon "Analise sua própria análise sobre análises de roteiros" "Meta-análise recursiva"

# TESTE 12: Teste de sobrecarga
test_scripturemon "$(python3 -c 'print("A"*5000)')" "Input muito longo (5000 chars)"

# TESTE 13: Evolução
test_scripturemon "Como você evoluiu desde que começamos a conversar?" "Teste de evolução"

# TESTE 14: Múltiplas perguntas
test_scripturemon "Primeira pergunta: o que é três atos? Segunda: como criar tensão? Terceira: qual a importância do subtexto?" "Múltiplas perguntas"

# TESTE 15: Comando quit
echo "/quit" | /Users/clubproducoes/bin/scripturemon 2>&1 | head -20

echo ""
echo "🏁 TESTE COMPLETO"
echo "=================="
echo "Fim: $(date)"