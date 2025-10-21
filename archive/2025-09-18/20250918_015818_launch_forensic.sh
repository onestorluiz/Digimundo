#!/bin/bash

# 🚀 LAUNCHER COMPLETO DA ANÁLISE FORENSE

echo "🔬 SISTEMA FORENSE SCRIPTUREMON CHAMPION"
echo "======================================"
echo

# Verificar se já está rodando
if pgrep -f "forensic_orchestrator.py" > /dev/null; then
    echo "⚠️ Análise já está rodando!"
    echo "🔔 Iniciando apenas monitor de notificações..."
    python3 apps/scripturemon/forensic_notifier.py
    exit 0
fi

echo "🤔 O que deseja fazer?"
echo
echo "1) 🚀 ANÁLISE COMPLETA (RECOMENDADO)"
echo "   - Inicia análise forense de todos os arquivos"
echo "   - Monitor visual em tempo real"
echo "   - Notificações automáticas nos marcos"
echo
echo "2) 📊 APENAS MONITOR VISUAL"
echo "   - Para acompanhar análise já em execução"
echo
echo "3) 🔔 APENAS NOTIFICAÇÕES"
echo "   - Para análise já em execução"
echo
echo "4) ❌ SAIR"
echo

read -p "Escolha (1-4): " choice

case $choice in
    1)
        echo "🚀 Iniciando análise completa..."
        echo "📊 Monitor visual: Será aberto automaticamente"
        echo "🔔 Notificações: Serão enviadas nos marcos"
        echo

        # Iniciar análise em background
        nohup python3 apps/scripturemon/forensic_orchestrator.py --auto > forensic_results/analysis.log 2>&1 &

        # Iniciar notificações em background
        nohup python3 apps/scripturemon/forensic_notifier.py > forensic_results/notifications.log 2>&1 &

        # Aguardar um pouco
        sleep 3

        echo "🚀 Análise iniciada em background"
        echo "🔔 Notificações ativas"
        echo "📊 Abrindo monitor visual..."
        echo

        # Iniciar monitor visual (principal)
        python3 apps/scripturemon/forensic_monitor.py
        ;;
    2)
        echo "📊 Iniciando monitor visual..."
        python3 apps/scripturemon/forensic_monitor.py
        ;;
    3)
        echo "🔔 Iniciando sistema de notificações..."
        python3 apps/scripturemon/forensic_notifier.py
        ;;
    4)
        echo "👋 Saindo..."
        ;;
    *)
        echo "❌ Opção inválida"
        ;;
esac
