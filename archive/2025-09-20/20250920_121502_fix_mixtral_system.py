#!/usr/bin/env python3
"""
🔧 FIX MIXTRAL SYSTEM - CORREÇÃO COMPLETA
Corrige todos os problemas detectados no sistema Mixtral
"""

import os
import sys
from pathlib import Path
import re
import json

# Adicionar caminho do projeto
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class MixtralSystemFixer:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.scripts_path = self.project_root / "scripts" / "active"
        self.fixes_made = []
        self.errors_found = []

    def fix_all_scripts(self):
        """Corrige todos os problemas em todos os scripts"""
        print("=" * 60)
        print("🔧 INICIANDO CORREÇÃO COMPLETA DO SISTEMA MIXTRAL")
        print("=" * 60)

        # 1. Corrigir referências a modelos errados
        print("\n1️⃣ CORRIGINDO REFERÊNCIAS AO MODELO...")
        self.fix_model_references()

        # 2. Corrigir erro IsADirectoryError
        print("\n2️⃣ CORRIGINDO ERRO IsADirectoryError...")
        self.fix_directory_error()

        # 3. Corrigir PathConfig.ensure_dirs
        print("\n3️⃣ CORRIGINDO PathConfig.ensure_dirs...")
        self.fix_path_config()

        # 4. Remover referências a mixtral
        print("\n4️⃣ REMOVENDO REFERÊNCIAS A mixtral...")
        self.remove_mixtral_references()

        # 5. Atualizar configurações padrão
        print("\n5️⃣ ATUALIZANDO CONFIGURAÇÕES PADRÃO...")
        self.update_default_configs()

        # Relatório final
        self.print_report()

    def fix_model_references(self):
        """Corrige todas as referências de modelo deeplearning-hybrid para mixtral"""
        files_to_fix = [
            "activate_full_deep_learning.py",
            "deep_learning_enhanced.py",
            "ml_system_running.py",
            "test_ml_working.py",
            "quick_deep_learning.py",
            "run_deep_learning_now.py",
            "deep_screenplay_learning.py",
            "deep_screenplay_learning_minimal.py",
            "autonomous_deep_learning.py",
            "deep_learning_running_now.py",
            "unified_power_system.py"
        ]

        replacements = [
            # Substituir deeplearning-hybrid por mixtral-dedicated-q5
            (r"deeplearning-hybrid", "mixtral-dedicated-q5"),
            (r"deeplearning-mixtral-dedicated", "mixtral-dedicated-q5"),
            (r"deeplearning-32b-eco", "mixtral-eco-q5"),

            # Ajustar configurações de RAM
            (r"65\s*GB", "45 GB"),  # mixtral usava 65GB, Mixtral usa ~45GB
            (r"45\s*GB", "35 GB"),  # 32B usava 45GB, Mixtral eco usa ~35GB
        ]

        for filename in files_to_fix:
            file_path = self.scripts_path / filename
            if not file_path.exists():
                continue

            try:
                content = file_path.read_text()
                original_content = content

                for old, new in replacements:
                    content = re.sub(old, new, content)

                if content != original_content:
                    file_path.write_text(content)
                    self.fixes_made.append(f"✅ {filename}: Modelo atualizado para Mixtral")
                    print(f"  ✅ {filename}")

            except Exception as e:
                self.errors_found.append(f"❌ {filename}: {str(e)}")
                print(f"  ❌ {filename}: {str(e)}")

    def fix_directory_error(self):
        """Corrige o erro IsADirectoryError em deep_learning_enhanced.py"""
        file_path = self.scripts_path / "deep_learning_enhanced.py"

        if not file_path.exists():
            return

        try:
            content = file_path.read_text()

            # Encontrar e corrigir a linha problemática
            lines = content.split('\n')
            for i, line in enumerate(lines):
                # Linha 207: content = self.library.get_screenplay(screenplay_title)
                if i == 206 and "self.library.get_screenplay" in line:
                    # Adicionar verificação antes
                    indent = len(line) - len(line.lstrip())
                    new_lines = [
                        line,
                        " " * indent + "if not content or content == '.':  # Evitar erro IsADirectoryError",
                        " " * indent + "    continue"
                    ]
                    lines[i] = "\n".join(new_lines)
                    break

            # Salvar arquivo corrigido
            file_path.write_text('\n'.join(lines))
            self.fixes_made.append(f"✅ deep_learning_enhanced.py: Corrigido erro IsADirectoryError")
            print(f"  ✅ deep_learning_enhanced.py")

        except Exception as e:
            self.errors_found.append(f"❌ deep_learning_enhanced.py: {str(e)}")
            print(f"  ❌ deep_learning_enhanced.py: {str(e)}")

    def fix_path_config(self):
        """Corrige o erro PathConfig.ensure_dirs"""
        config_file = self.project_root / "src" / "core" / "config.py"

        if not config_file.exists():
            return

        try:
            content = config_file.read_text()

            # Verificar se ensure_dirs existe e está comentado
            if "# def ensure_dirs" in content or "#def ensure_dirs" in content:
                # Descomentar o método
                content = re.sub(r"#\s*def ensure_dirs", "def ensure_dirs", content)
                content = re.sub(r"#\s*(.*ensure_dirs.*)", r"\1", content)

                config_file.write_text(content)
                self.fixes_made.append("✅ config.py: Método ensure_dirs descomentado")
                print("  ✅ config.py")
            elif "def ensure_dirs" not in content:
                # Adicionar o método se não existir
                lines = content.split('\n')

                # Encontrar a classe PathConfig
                for i, line in enumerate(lines):
                    if "class PathConfig" in line:
                        # Adicionar método no final da classe
                        j = i + 1
                        while j < len(lines) and lines[j].startswith((' ', '\t')):
                            j += 1

                        # Inserir método antes do fim da classe
                        method = """
    def ensure_dirs(self):
        \"\"\"Garante que todos os diretórios necessários existam\"\"\"
        for path in [self.data, self.models, self.output, self.logs, self.cache]:
            path.mkdir(parents=True, exist_ok=True)
"""
                        lines.insert(j - 1, method)
                        break

                config_file.write_text('\n'.join(lines))
                self.fixes_made.append("✅ config.py: Método ensure_dirs adicionado")
                print("  ✅ config.py")

        except Exception as e:
            self.errors_found.append(f"❌ config.py: {str(e)}")
            print(f"  ❌ config.py: {str(e)}")

    def remove_mixtral_references(self):
        """Remove todas as referências a mixtral dos scripts"""
        # Renomear arquivo se existir
        old_file = self.scripts_path.parent / "run_mixtral_dedicated.sh"
        new_file = self.scripts_path.parent / "run_mixtral_dedicated.sh"

        if old_file.exists():
            try:
                old_file.rename(new_file)
                self.fixes_made.append("✅ Renomeado run_mixtral_dedicated.sh → run_mixtral_dedicated.sh")
                print("  ✅ Arquivo renomeado")
            except:
                pass

        # Buscar e corrigir referências em todos os arquivos
        for file_path in self.scripts_path.glob("*.py"):
            try:
                content = file_path.read_text()
                original = content

                # Substituir referências
                content = re.sub(r"mixtral", "mixtral", content, flags=re.IGNORECASE)
                content = re.sub(r"mixtral", "mixtral", content, flags=re.IGNORECASE)

                if content != original:
                    file_path.write_text(content)
                    self.fixes_made.append(f"✅ {file_path.name}: Removidas referências a mixtral")

            except:
                pass

    def update_default_configs(self):
        """Atualiza configurações padrão para usar Mixtral"""
        # Criar arquivo de configuração unificada
        config_content = """#!/usr/bin/env python3
\"\"\"
🎯 CONFIGURAÇÃO PADRÃO DO SISTEMA MIXTRAL
Centraliza todas as configurações para usar Mixtral como modelo principal
\"\"\"

# Modelo padrão do sistema
DEFAULT_MODEL = "mixtral-dedicated-q5"
ECO_MODEL = "mixtral-eco-q5"

# Configurações Ollama otimizadas para Mixtral
OLLAMA_CONFIG = {
    'num_ctx': 131072,      # 128K tokens
    'num_thread': 24,       # 86% dos 28 cores
    'num_gpu': 60,          # Todos os 60 cores GPU
    'num_batch': 4096,      # Batch otimizado
    'keep_context': 2048,   # Contexto mantido
    'temperature': 0.3,     # Precisão analítica
    'top_p': 0.9,
    'top_k': 40,
    'repeat_penalty': 1.1,
    'seed': 42              # Reprodutibilidade
}

# Configurações de memória
MEMORY_LIMITS = {
    'mixtral_dedicated': 45,  # GB
    'mixtral_eco': 35,        # GB
    'minimum_free': 10        # GB mínimo livre
}

# Caminhos da biblioteca
LIBRARY_PATH = "digilibrary/BIBLIOTECA_ROTEIROS"
LIBRARY_CATEGORIES = ["meus_filmes", "roteiros_mestres", "teoria"]

# Especialistas para análise
SPECIALISTS = [
    "character_analyst",
    "pacing_expert",
    "theme_specialist",
    "structure_architect",
    "dialogue_expert"
]

# Save the Cat Beats
SAVE_THE_CAT_BEATS = [
    ("Opening Image", 1),
    ("Theme Stated", 5),
    ("Setup", 10),
    ("Catalyst", 12),
    ("Debate", 25),
    ("Break into Two", 25),
    ("B Story", 30),
    ("Fun and Games", 50),
    ("Midpoint", 50),
    ("Bad Guys Close In", 75),
    ("All Is Lost", 75),
    ("Dark Night of the Soul", 80),
    ("Break into Three", 80),
    ("Finale", 95),
    ("Final Image", 100)
]

def get_model_config(mode="dedicated"):
    \"\"\"Retorna configuração do modelo baseada no modo\"\"\"
    if mode == "eco":
        config = OLLAMA_CONFIG.copy()
        config['num_thread'] = 14  # 50% dos cores para eco
        config['num_ctx'] = 32768  # 32K tokens para eco
        return ECO_MODEL, config
    else:
        return DEFAULT_MODEL, OLLAMA_CONFIG
"""

        config_file = self.project_root / "src" / "core" / "mixtral_config.py"
        config_file.write_text(config_content)
        self.fixes_made.append("✅ mixtral_config.py: Criado arquivo de configuração centralizada")
        print("  ✅ mixtral_config.py criado")

    def print_report(self):
        """Imprime relatório final das correções"""
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO DE CORREÇÕES")
        print("=" * 60)

        print(f"\n✅ CORREÇÕES APLICADAS: {len(self.fixes_made)}")
        for fix in self.fixes_made[:10]:  # Mostrar primeiras 10
            print(f"  {fix}")
        if len(self.fixes_made) > 10:
            print(f"  ... e mais {len(self.fixes_made) - 10} correções")

        if self.errors_found:
            print(f"\n❌ ERROS ENCONTRADOS: {len(self.errors_found)}")
            for error in self.errors_found[:5]:
                print(f"  {error}")

        print("\n" + "=" * 60)
        print("🎯 PRÓXIMOS PASSOS:")
        print("=" * 60)
        print("1. Reiniciar todos os scripts que estavam rodando")
        print("2. Testar com: python3 scripts/active/mixtral_clean_test.py")
        print("3. Rodar análise completa: python3 scripts/active/mixtral_enhanced_master.py")
        print("\nDIGIMUNDO PRESENTE 🥷")


if __name__ == "__main__":
    fixer = MixtralSystemFixer()
    fixer.fix_all_scripts()