#!/usr/bin/env python3
"""
🔔 SISTEMA DE NOTIFICAÇÕES DA ANÁLISE FORENSE
Monitora progresso e envia alertas quando termina
"""

import json
import time
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

class ForensicNotifier:
    """Sistema de notificações da análise forense"""

    def __init__(self):
        self.base_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        self.results_dir = self.base_dir / "forensic_results"
        self.checkpoint_file = self.results_dir / "checkpoint.json"
        self.final_report = self.results_dir / "FORENSIC_REPORT_FINAL.md"

        self.last_completed = 0
        self.start_time = datetime.now()

    def send_system_notification(self, title: str, message: str):
        """Envia notificação do sistema (macOS)"""
        try:
            # Usar osascript para notificação macOS
            script = f'''
            display notification "{message}" with title "{title}" sound name "Glass"
            '''
            subprocess.run(["osascript", "-e", script], check=True)
        except Exception as e:
            print(f"⚠️ Erro ao enviar notificação: {e}")

    def play_completion_sound(self):
        """Toca som de conclusão"""
        try:
            # Tentar tocar som do sistema
            subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"], check=True)
        except:
            try:
                # Fallback para say
                subprocess.run(["say", "Análise forense concluída"], check=True)
            except:
                print("🔔 *DING* Análise concluída!")

    def get_progress_info(self) -> Optional[dict]:
        """Obtém informações de progresso"""
        if not self.checkpoint_file.exists():
            return None

        try:
            with open(self.checkpoint_file, 'r') as f:
                data = json.load(f)
            return data
        except Exception:
            return None

    def check_completion(self) -> bool:
        """Verifica se análise foi concluída"""
        return self.final_report.exists()

    def format_final_stats(self, data: dict) -> str:
        """Formata estatísticas finais"""
        results = data.get('results', {})
        if not results:
            return "Nenhum resultado encontrado"

        total = len(results)
        broken = sum(1 for r in results.values() if r.get('overall_health') == 'BROKEN')
        problematic = sum(1 for r in results.values() if r.get('overall_health') == 'PROBLEMATIC')
        ok = sum(1 for r in results.values() if r.get('overall_health') == 'OK')

        critical_issues = sum(len(r.get('critical_issues', [])) for r in results.values())
        total_fix_time = sum(r.get('fix_time_estimate_hours', 0) for r in results.values())

        return f"""
📊 RESULTADOS FINAIS:
• Total de arquivos: {total}
• 🔴 Quebrados: {broken}
• ⚠️ Problemáticos: {problematic}
• ✅ OK: {ok}
• 🚨 Problemas críticos: {critical_issues}
• ⏱️ Tempo de correção: {total_fix_time:.1f}h

📁 Relatório: {self.final_report}
"""

    def monitor_progress(self):
        """Monitora progresso e envia notificações"""
        print("🔔 Monitorando análise forense...")
        print("   Enviará notificações a cada 25% e na conclusão")
        print("   Pressione Ctrl+C para parar")

        milestones = {25: False, 50: False, 75: False, 100: False}

        try:
            while True:
                # Verificar se completou
                if self.check_completion():
                    print("\n🎉 ANÁLISE CONCLUÍDA!")

                    # Obter dados finais
                    data = self.get_progress_info()
                    if data:
                        stats = self.format_final_stats(data)
                        print(stats)

                        # Notificação de conclusão
                        self.send_system_notification(
                            "🔬 Análise Forense Concluída!",
                            f"Total: {len(data.get('results', {}))} arquivos analisados"
                        )

                        # Som de conclusão
                        self.play_completion_sound()

                        print("🔔 Notificação enviada!")

                    break

                # Verificar progresso
                data = self.get_progress_info()
                if data:
                    total = data.get('total_files', 0)
                    completed = data.get('completed_files', 0)

                    if total > 0:
                        progress = (completed / total) * 100

                        # Verificar marcos (25%, 50%, 75%)
                        for milestone in [25, 50, 75]:
                            if progress >= milestone and not milestones[milestone]:
                                milestones[milestone] = True

                                elapsed = datetime.now() - self.start_time
                                remaining_percent = 100 - progress
                                estimated_remaining = (elapsed.total_seconds() / progress) * remaining_percent
                                remaining_hours = estimated_remaining / 3600

                                message = f"{progress:.0f}% completo ({completed}/{total}). ETA: {remaining_hours:.1f}h"

                                self.send_system_notification(
                                    f"🔬 Análise Forense - {milestone}% completo",
                                    message
                                )

                                print(f"🔔 {milestone}% - Notificação enviada")

                        # Mostrar progresso atual
                        if completed != self.last_completed:
                            print(f"📈 Progresso: {progress:.1f}% ({completed}/{total})")
                            self.last_completed = completed

                time.sleep(30)  # Verificar a cada 30 segundos

        except KeyboardInterrupt:
            print("\n👋 Monitor de notificações parado")

def create_launcher_script():
    """Cria script de lançamento conveniente"""
    launcher_content = f'''#!/bin/bash

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
echo "1) 🚀 Iniciar análise completa com notificações"
echo "2) 📊 Apenas monitor visual"
echo "3) 🔔 Apenas notificações"
echo "4) ❌ Sair"
echo

read -p "Escolha (1-4): " choice

case $choice in
    1)
        echo "🚀 Iniciando análise completa..."
        echo "📊 Monitor visual: python3 apps/scripturemon/forensic_monitor.py"
        echo "🔔 Notificações: Automáticas"
        echo

        # Iniciar análise em background
        nohup python3 apps/scripturemon/forensic_orchestrator.py > forensic_results/analysis.log 2>&1 &

        # Aguardar um pouco
        sleep 3

        # Iniciar notificações
        python3 apps/scripturemon/forensic_notifier.py
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
'''

    launcher_path = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/launch_forensic.sh")
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)

    # Tornar executável
    os.chmod(launcher_path, 0o755)

    print(f"✅ Launcher criado: {launcher_path}")

def main():
    """Função principal"""
    if len(sys.argv) > 1 and sys.argv[1] == "--create-launcher":
        create_launcher_script()
        return

    notifier = ForensicNotifier()
    notifier.monitor_progress()

if __name__ == "__main__":
    main()