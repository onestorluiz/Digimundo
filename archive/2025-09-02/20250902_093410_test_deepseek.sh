#!/bin/bash
echo "Testando DeepSeek-R1:70b com contexto de 256K..."
echo ""
echo "Faça uma pergunta sobre roteiros cinematográficos:" | \
ollama run deepseek-r1:70b --num-ctx 256000 \
"Você é um especialista em roteiros. Explique brevemente os 3 atos da estrutura clássica."

echo ""
echo "✅ Teste concluído!"
