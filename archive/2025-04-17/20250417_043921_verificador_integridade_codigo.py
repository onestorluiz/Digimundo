#!/usr/bin/env python3
import os
import py_compile

base_dir = "/root/digimundo_vivo/ascenso/scripturemon/scripts"
log_file = os.path.join(base_dir, "verificacao_sintaxe.log")

with open(log_file, "w") as log:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("verificador_integridade"):
                full_path = os.path.join(root, file)
                try:
                    py_compile.compile(full_path, doraise=True)
                    log.write(f"✅ OK: {full_path}\n")
                except py_compile.PyCompileError as error:
                    log.write(f"❌ ERRO: {full_path}\n{error}\n")

print(f"Verificação completa. Verifique o arquivo: {log_file}")
