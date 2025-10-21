#!/bin/bash
echo "🔥 ATIVANDO PERFIL FUSION (41GB)"
echo "================================"
echo ""
echo "Modelo: scripturemon-gen9 x10 instâncias"
echo "RAM: 41GB (10x 4.1GB)"
echo "Função: 10 análises paralelas com consenso"
echo ""

# Analisa o roteiro passado como argumento ou usa exemplo
if [ -z "$1" ]; then
    ROTEIRO="FADE IN: INT. OFFICE - DAY. John enters. JOHN: I need help. FADE OUT."
else
    ROTEIRO=$(cat "$1")
fi

echo "Lançando 10 instâncias do Scripturemon..."
echo ""

# Lança 10 análises em paralelo
for i in {1..10}; do
    echo "🚀 Instância $i..."
    (
        ollama run scripturemon-gen9:latest "ANÁLISE BRUTAL #$i:

$ROTEIRO

Seja BRUTAL e específico.
Compare com mestres.
Dê score realista.
Seed: $((i * 1337))" > /tmp/fusion_$i.txt 2>&1
    ) &
done

# Aguarda todas terminarem
echo ""
echo "Aguardando análises paralelas..."
wait

echo ""
echo "📊 RESULTADOS DAS 10 INSTÂNCIAS:"
echo "================================"

# Mostra resultados
for i in {1..10}; do
    echo ""
    echo "Instância $i:"
    head -n 5 /tmp/fusion_$i.txt 2>/dev/null || echo "Processando..."
done

echo ""
echo "✅ Análise FUSION completa!"