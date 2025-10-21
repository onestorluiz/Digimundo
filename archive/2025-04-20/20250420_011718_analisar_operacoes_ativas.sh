#!/bin/bash

echo "🔍 Verificando instâncias vivas de Scripturemon..."

# Verifica serviços ativos
echo "🧩 Serviços ativos:"
systemctl list-units --type=service | grep scripturemon || echo "🔕 Nenhum service scripturemon ativo encontrado."

# Verifica processos rodando em segundo plano
echo -e "\n🧠 Processos rodando:"
ps aux | grep -i scripturemon | grep -v grep || echo "🔕 Nenhum processo scripturemon rodando."

# Verifica uso da porta do Ollama
echo -e "\n🔌 Verificando uso da porta 11434 (Ollama):"
lsof -i:11434 || echo "🔕 Porta 11434 livre."

# Verifica se algum start antigo ainda está ligado
echo -e "\n🧪 Verificando atividades em background:"
pgrep -fl scripturemon || echo "🔕 Nenhuma execução em background detectada."

echo -e "\n✅ Análise concluída. Certifique-se de desligar qualquer resíduo manualmente, se necessário."
