#!/usr/bin/env python3
"""
🚨 SISTEMA DE ALERTA DE VÍCIOS DO CLAUDE CODE
Detecta e alerta quando estou caindo nos meus vícios conhecidos
"""

import re
from typing import List, Dict

class ViciosAlert:
    """Detecta vícios do Claude Code em tempo real"""

    def __init__(self):
        self.vicios = {
            'overengineering': {
                'patterns': [
                    'vamos refatorar',
                    'criar novo sistema',
                    'arquitetura completa',
                    'reescrever tudo'
                ],
                'alert': "🚨 OVERENGINEERING! Está funcionando? Não refatore!"
            },
            'criar_sem_verificar': {
                'patterns': [
                    'vou criar',
                    'novo arquivo',
                    'implementar do zero'
                ],
                'alert': "🚨 JÁ EXISTE? Verifique primeiro: grep -r 'pattern' ."
            },
            'analise_sem_execucao': {
                'patterns': [
                    'vou analisar',
                    'vamos verificar',
                    'debugar o código'
                ],
                'alert': "🚨 TESTE PRIMEIRO! Execute o comando básico antes de debugar código"
            },
            'ignorar_obvio': {
                'patterns': [
                    'problema complexo',
                    'arquitetura',
                    'processlock',
                    'threading'
                ],
                'alert': "🚨 SIMPLES PRIMEIRO! O problema pode ser trivial (ex: ferramenta travada)"
            }
        }

        self.critical_checks = [
            "Testou a ferramenta diretamente? (ex: ollama run)",
            "Verificou se já existe solução pronta?",
            "Executou o comando mais básico primeiro?",
            "Leu TODA a mensagem de erro?",
            "O problema é no código ou na ferramenta?"
        ]

    def check_response(self, text: str) -> List[str]:
        """Verifica se estou caindo em vícios"""
        alerts = []
        text_lower = text.lower()

        for vicio, config in self.vicios.items():
            for pattern in config['patterns']:
                if pattern in text_lower:
                    alerts.append(config['alert'])
                    break

        return alerts

    def pre_debug_checklist(self) -> str:
        """Checklist antes de debugar qualquer coisa"""
        checklist = "📋 ANTES DE DEBUGAR:\n"
        for i, check in enumerate(self.critical_checks, 1):
            checklist += f"{i}. {check}\n"
        checklist += "\n💡 Lembre: 1 teste direto > 100 análises de código"
        return checklist

    def detect_subprocess_ollama(self, code: str) -> bool:
        """Detecta uso problemático de subprocess com ollama"""
        problematic_patterns = [
            r"subprocess.*ollama.*run",
            r"Popen.*ollama.*run",
            r"call.*ollama.*run"
        ]

        for pattern in problematic_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return True
        return False

    def suggest_fix(self, problem: str) -> str:
        """Sugere correção para problemas conhecidos"""
        fixes = {
            'subprocess_ollama': '''
# ❌ PROBLEMA: subprocess com ollama run trava!
# subprocess.run(["ollama", "run", model, prompt])

# ✅ SOLUÇÃO: Use API REST
import requests
response = requests.post(
    "http://127.0.0.1:11434/api/generate",
    json={"model": model, "prompt": prompt, "stream": False},
    timeout=30
)
result = response.json().get("response", "")
''',
            'processlock': '''
# ❌ PROBLEMA: ProcessLock com 'with' statement pode travar
# with ProcessLock("name") as lock:

# ✅ SOLUÇÃO: Use manual
lock = ProcessLock("name")
if lock.acquire(timeout=5):
    try:
        # código
    finally:
        lock.release()
'''
        }

        return fixes.get(problem, "Solução não catalogada ainda")

# Exemplo de uso
if __name__ == "__main__":
    alert = ViciosAlert()

    # Testa detecção
    test_text = "Vou criar um novo sistema completo para resolver isso"
    alerts = alert.check_response(test_text)

    if alerts:
        print("⚠️ VÍCIOS DETECTADOS:")
        for a in alerts:
            print(a)

    print("\n" + alert.pre_debug_checklist())

    # Testa detecção de subprocess
    bad_code = 'subprocess.run(["ollama", "run", "mixtral", prompt])'
    if alert.detect_subprocess_ollama(bad_code):
        print("\n🚨 CÓDIGO PROBLEMÁTICO DETECTADO!")
        print(alert.suggest_fix('subprocess_ollama'))