#!/bin/bash

echo "🎬 TESTE SIMULADO DO CHAT SCRIPTUREMON"
echo "======================================="
echo ""
echo "📝 Teste 1: Verificar se responde em português"
echo ""

# Criar input simulado para teste
cat > /tmp/scripturemon_test_input.txt << 'EOF'
Olá Scripturemon! Você consegue falar em português?
exit
EOF

# Executar com timeout e input redirecionado
timeout 30 /Users/clubproducoes/Digimundo/scripturemon-validation/bin/scripturemon < /tmp/scripturemon_test_input.txt > /tmp/scripturemon_test_output.txt 2>&1 &
SCRIPTUREMON_PID=$!

# Aguardar alguns segundos
sleep 10

# Matar o processo se ainda estiver rodando
if kill -0 $SCRIPTUREMON_PID 2>/dev/null; then
    kill $SCRIPTUREMON_PID 2>/dev/null
fi

echo "📋 Resultado do Teste 1:"
echo "------------------------"
cat /tmp/scripturemon_test_output.txt | head -50
echo ""

echo "======================================="
echo "📝 Teste 2: Verificar acesso ao roteiro SONHOS SEM LEMBRANÇAS"
echo ""

# Teste 2 - Perguntar sobre o roteiro
cat > /tmp/scripturemon_test_input2.txt << 'EOF'
Me conte sobre o roteiro SONHOS SEM LEMBRANÇAS
exit
EOF

timeout 30 /Users/clubproducoes/Digimundo/scripturemon-validation/bin/scripturemon < /tmp/scripturemon_test_input2.txt > /tmp/scripturemon_test_output2.txt 2>&1 &
SCRIPTUREMON_PID2=$!

sleep 15

if kill -0 $SCRIPTUREMON_PID2 2>/dev/null; then
    kill $SCRIPTUREMON_PID2 2>/dev/null
fi

echo "📋 Resultado do Teste 2:"
echo "------------------------"
cat /tmp/scripturemon_test_output2.txt | head -80

echo ""
echo "======================================="
echo "🔍 ANÁLISE DOS RESULTADOS:"
echo ""

# Verificar se responde em português
if grep -q "English\|english\|Hello\|hello" /tmp/scripturemon_test_output.txt; then
    echo "❌ PROBLEMA: Sistema respondendo em inglês"
else
    echo "✅ Sistema respondendo em português"
fi

# Verificar se acessa PDFs
if grep -q "SONHOS\|Contexto do seu roteiro\|Acessando:" /tmp/scripturemon_test_output2.txt; then
    echo "✅ Sistema acessando PDFs corretamente"
else
    echo "❌ PROBLEMA: Sistema não está acessando os PDFs"
fi

echo ""
echo "✨ Teste completo!"
