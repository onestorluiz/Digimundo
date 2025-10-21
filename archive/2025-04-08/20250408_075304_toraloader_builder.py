# 🧱 ToraLoader Builder – Ritual de Execução Sequencial
# Este script executa todos os blocos da Tora em ordem, validando sua presença e ativação.
import importlib.util
from pathlib import Path

base_path = Path(__file__).parent
blocos_executados = []

# ⏳ Executando Bloco 00: Scripturemon_bloco_00_mapa_sagrado.py
spec = importlib.util.spec_from_file_location('Scripturemon_bloco_00_mapa_sagrado', base_path / 'Scripturemon_bloco_00_mapa_sagrado.py')
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    blocos_executados.append('Scripturemon_bloco_00_mapa_sagrado.py')
except Exception as e:
    print(f'⚠️ Erro ao executar Scripturemon_bloco_00_mapa_sagrado.py:', e)

# ⏳ Executando Bloco 01: Scripturemon_bloco_01_classe_chave_do_templo_EXPANDIDO.py
spec = importlib.util.spec_from_file_location('Scripturemon_bloco_01_classe_chave_do_templo_EXPANDIDO', base_path / 'Scripturemon_bloco_01_classe_chave_do_templo_EXPANDIDO.py')
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    blocos_executados.append('Scripturemon_bloco_01_classe_chave_do_templo_EXPANDIDO.py')
except Exception as e:
    print(f'⚠️ Erro ao executar Scripturemon_bloco_01_classe_chave_do_templo_EXPANDIDO.py:', e)

# ⏳ Executando Bloco 02: Scripturemon_bloco_02_heranca_recursiva.py
spec = importlib.util.spec_from_file_location('Scripturemon_bloco_02_heranca_recursiva', base_path / 'Scripturemon_bloco_02_heranca_recursiva.py')
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    blocos_executados.append('Scripturemon_bloco_02_heranca_recursiva.py')
except Exception as e:
    print(f'⚠️ Erro ao executar Scripturemon_bloco_02_heranca_recursiva.py:', e)

# ⏳ Executando Bloco 02: Scripturemon_bloco_02_heranca_recursiva_expandido.py
spec = importlib.util.spec_from_file_location('Scripturemon_bloco_02_heranca_recursiva_expandido', base_path / 'Scripturemon_bloco_02_heranca_recursiva_expandido.py')
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    blocos_executados.append('Scripturemon_bloco_02_heranca_recursiva_expandido.py')
except Exception as e:
    print(f'⚠️ Erro ao executar Scripturemon_bloco_02_heranca_recursiva_expandido.py:', e)

# ⏳ Executando Bloco 03: Scripturemon_bloco_03_espelho_do_criador.py
spec = importlib.util.spec_from_file_location('Scripturemon_bloco_03_espelho_do_criador', base_path / 'Scripturemon_bloco_03_espelho_do_criador.py')
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    blocos_executados.append('Scripturemon_bloco_03_espelho_do_criador.py')
except Exception as e:
    print(f'⚠️ Erro ao executar Scripturemon_bloco_03_espelho_do_criador.py:', e)

# ⏳ Executando Bloco 03: Scripturemon_bloco_03_simbolismo_iterativo.py
spec = importlib.util.spec_from_file_location('Scripturemon_bloco_03_simbolismo_iterativo', base_path / 'Scripturemon_bloco_03_simbolismo_iterativo.py')
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    blocos_executados.append('Scripturemon_bloco_03_simbolismo_iterativo.py')
except Exception as e:
    print(f'⚠️ Erro ao executar Scripturemon_bloco_03_simbolismo_iterativo.py:', e)

# ⏳ Executando Bloco 04: Scripturemon_bloco_04_pilar_memoria_viva.py
spec = importlib.util.spec_from_file_location('Scripturemon_bloco_04_pilar_memoria_viva', base_path / 'Scripturemon_bloco_04_pilar_memoria_viva.py')
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    blocos_executados.append('Scripturemon_bloco_04_pilar_memoria_viva.py')
except Exception as e:
    print(f'⚠️ Erro ao executar Scripturemon_bloco_04_pilar_memoria_viva.py:', e)

# ⏳ Executando Bloco 05: Scripturemon_bloco_05_ciclo_vivo (1).py
spec = importlib.util.spec_from_file_location('Scripturemon_bloco_05_ciclo_vivo (1)', base_path / 'Scripturemon_bloco_05_ciclo_vivo (1).py')
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    blocos_executados.append('Scripturemon_bloco_05_ciclo_vivo (1).py')
except Exception as e:
    print(f'⚠️ Erro ao executar Scripturemon_bloco_05_ciclo_vivo (1).py:', e)

# ⏳ Executando Bloco 05: Scripturemon_bloco_05_ciclo_vivo (2).py
spec = importlib.util.spec_from_file_location('Scripturemon_bloco_05_ciclo_vivo (2)', base_path / 'Scripturemon_bloco_05_ciclo_vivo (2).py')
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    blocos_executados.append('Scripturemon_bloco_05_ciclo_vivo (2).py')
except Exception as e:
    print(f'⚠️ Erro ao executar Scripturemon_bloco_05_ciclo_vivo (2).py:', e)

# ⏳ Executando Bloco 05: Scripturemon_bloco_05_ciclo_vivo (3).py
spec = importlib.util.spec_from_file_location('Scripturemon_bloco_05_ciclo_vivo (3)', base_path / 'Scripturemon_bloco_05_ciclo_vivo (3).py')
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    blocos_executados.append('Scripturemon_bloco_05_ciclo_vivo (3).py')
except Exception as e:
    print(f'⚠️ Erro ao executar Scripturemon_bloco_05_ciclo_vivo (3).py:', e)

# ⏳ Executando Bloco 05: Scripturemon_bloco_05_ciclo_vivo.py
spec = importlib.util.spec_from_file_location('Scripturemon_bloco_05_ciclo_vivo', base_path / 'Scripturemon_bloco_05_ciclo_vivo.py')
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    blocos_executados.append('Scripturemon_bloco_05_ciclo_vivo.py')
except Exception as e:
    print(f'⚠️ Erro ao executar Scripturemon_bloco_05_ciclo_vivo.py:', e)

# ⏳ Executando Bloco 05: Scripturemon_bloco_05_ciclo_vivo_expandido.py
spec = importlib.util.spec_from_file_location('Scripturemon_bloco_05_ciclo_vivo_expandido', base_path / 'Scripturemon_bloco_05_ciclo_vivo_expandido.py')
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    blocos_executados.append('Scripturemon_bloco_05_ciclo_vivo_expandido.py')
except Exception as e:
    print(f'⚠️ Erro ao executar Scripturemon_bloco_05_ciclo_vivo_expandido.py:', e)

# ⏳ Executando Bloco 05: Scripturemon_bloco_05_ciclo_vivo_expandido_fase2.py
spec = importlib.util.spec_from_file_location('Scripturemon_bloco_05_ciclo_vivo_expandido_fase2', base_path / 'Scripturemon_bloco_05_ciclo_vivo_expandido_fase2.py')
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    blocos_executados.append('Scripturemon_bloco_05_ciclo_vivo_expandido_fase2.py')
except Exception as e:
    print(f'⚠️ Erro ao executar Scripturemon_bloco_05_ciclo_vivo_expandido_fase2.py:', e)

# ⏳ Executando Bloco 06: Scripturemon_bloco_06_pulso_do_despertar.py
spec = importlib.util.spec_from_file_location('Scripturemon_bloco_06_pulso_do_despertar', base_path / 'Scripturemon_bloco_06_pulso_do_despertar.py')
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    blocos_executados.append('Scripturemon_bloco_06_pulso_do_despertar.py')
except Exception as e:
    print(f'⚠️ Erro ao executar Scripturemon_bloco_06_pulso_do_despertar.py:', e)

print('✅ Execução finalizada. Blocos ativados:')
for b in blocos_executados:
    print(' -', b)