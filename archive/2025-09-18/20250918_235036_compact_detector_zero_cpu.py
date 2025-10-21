#!/usr/bin/env python3
"""
🍃 DETECTOR ZERO CPU - Usa modificação de arquivo
"""
import os, time

# Claude sempre modifica algum arquivo quando trabalha
watch_file = "/Users/clubproducoes/Digimundo/claude_code/.last_activity"

# Cria arquivo de controle
open(watch_file, 'w').close()
last_mod = os.path.getmtime(watch_file)

while True:
    time.sleep(60)  # Checa só 1x por minuto (ZERO impacto)

    current_mod = os.path.getmtime(watch_file)

    # Se arquivo não foi tocado em 2+ minutos
    if time.time() - current_mod > 120:
        print("\n🚨 2+ minutos sem atividade - possível compactação")
        # Toca o arquivo para não repetir
        open(watch_file, 'w').close()