#!/bin/bash
# Cria todos os modelos especializados do Scripturemon Ultimate

echo "🚀 Scripturemon Ultimate - Criando modelos especializados..."
echo

cd "$(dirname "$0")"

success_count=0
total_count=0

for modelfile in *.modelfile; do
    if [ -f "$modelfile" ]; then
        total_count=$((total_count + 1))
        name="${modelfile%.modelfile}"
        echo "📦 Criando modelo: $name"

        if ollama create "$name" -f "$modelfile" 2>/dev/null; then
            echo "  ✅ $name criado com sucesso"
            success_count=$((success_count + 1))
        else
            echo "  ❌ Erro ao criar $name"
        fi
        echo
    fi
done

echo "📊 Resultado: $success_count/$total_count modelos criados"
echo
echo "🔍 Modelos Scripturemon disponíveis:"
ollama list | grep -E "(scripturemon|code-refactor|beat_analyzer|character_analyzer|deeplearning|mixtral|producermon)" | sort
