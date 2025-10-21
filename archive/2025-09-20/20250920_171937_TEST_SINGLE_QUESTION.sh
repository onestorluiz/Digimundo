#!/bin/bash

# Teste simples e direto - Uma única pergunta

echo "========================================="
echo "🔬 TESTE SIMPLES - UMA PERGUNTA"
echo "========================================="

cd /Users/clubproducoes/Digimundo/scripturemon-validation

# Criar input simples
cat > /tmp/simple_test.txt << 'EOF'
O que é cinema para você?
exit
EOF

echo -e "\n📝 Pergunta: 'O que é cinema para você?'"
echo "========================================="

# Executar com timeout manual
(
    python3 bin/scripturemon < /tmp/simple_test.txt 2>&1 | tee /tmp/simple_output.txt
) &
PID=$!

# Esperar até 10 segundos
for i in {1..10}; do
    if ! ps -p $PID > /dev/null 2>&1; then
        echo -e "\n✅ Processo terminou em ${i} segundos"
        break
    fi
    sleep 1
done

# Matar se ainda estiver rodando
if ps -p $PID > /dev/null 2>&1; then
    kill -TERM $PID 2>/dev/null
    sleep 1
    kill -KILL $PID 2>/dev/null
    echo -e "\n⚠️ Processo teve timeout após 10 segundos"
fi

# Analisar resultado
echo "========================================="
echo "📊 ANÁLISE DO RESULTADO:"
echo "========================================="

if [ -f /tmp/simple_output.txt ]; then
    LINES=$(wc -l < /tmp/simple_output.txt)
    CHARS=$(wc -c < /tmp/simple_output.txt)
    
    echo "📄 Output: $LINES linhas, $CHARS caracteres"
    
    # Verificar elementos chave
    grep -q "cinema" /tmp/simple_output.txt && echo "✅ Palavra 'cinema' encontrada" || echo "❌ Palavra 'cinema' NÃO encontrada"
    grep -q -E "(roteiro|filme|narrativa)" /tmp/simple_output.txt && echo "✅ Termos de cinema encontrados" || echo "⚠️ Termos de cinema não encontrados"
    grep -q "Scripturemon" /tmp/simple_output.txt && echo "✅ Identificação do sistema" || echo "⚠️ Sistema não se identificou"
    
    # Verificar se está em português
    if grep -q -E "(é|para|você|sobre|com)" /tmp/simple_output.txt; then
        echo "✅ Resposta em português"
    else
        echo "❌ Resposta NÃO está em português"
    fi
    
    echo -e "\n📝 OUTPUT COMPLETO:"
    echo "----------------------------------------"
    cat /tmp/simple_output.txt
    echo "----------------------------------------"
else
    echo "❌ Nenhum output gerado"
fi

echo -e "\n========================================="
echo "🏁 FIM DO TESTE"
echo "========================================="