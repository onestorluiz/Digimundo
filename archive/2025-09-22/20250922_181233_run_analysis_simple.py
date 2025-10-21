#!/usr/bin/env python3
"""Script simplificado para executar análise sem lock problemático"""

import sys
sys.path.insert(0, 'src')

from ollama_continuous_learning import OllamaContinuousLearning

print("🚀 Iniciando análise simplificada...")
print("=" * 60)

# Remove lock files antigos se existirem
import os
try:
    os.remove("/tmp/scripturemon_learning.lock")
    print("🗑️ Lock antigo removido")
except:
    pass

# Cria e executa sistema diretamente (sem lock)
learner = OllamaContinuousLearning(model='mixtral-cpu-force:latest')
print("✅ Sistema inicializado")

# Executa um ciclo
learner.run_continuous_learning(cycles=1)

print("\n🎯 Análise completada com sucesso!")
print("DIGIMUNDO PRESENTE!")