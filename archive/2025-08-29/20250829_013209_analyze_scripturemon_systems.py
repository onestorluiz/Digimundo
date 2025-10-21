#!/usr/bin/env python3
"""
🎬 Analisador Completo do Sistema Scripturemon
Identifica todos os sistemas, funcionalidades e cria versão definitiva
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import hashlib

class ScripturemonAnalyzer:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.all_files = defaultdict(list)
        self.features = {
            'models': set(),
            'scripts': [],
            'configs': [],
            'binaries': [],
            'prompts': set(),
            'capabilities': set()
        }
        
    def find_all_scripturemon_files(self):
        """Encontra todos os arquivos relacionados ao Scripturemon"""
        print("🔍 BUSCANDO TODOS OS ARQUIVOS SCRIPTUREMON...")
        print("="*60)
        
        # Buscar diferentes tipos de arquivo
        patterns = {
            'shell_scripts': ['*.sh'],
            'python_scripts': ['*scripturemon*.py', '*SCRIPTUREMON*.py'],
            'configs': ['*scripturemon*.yaml', '*scripturemon*.json', '*scripturemon*.conf'],
            'models': ['scripturemon*', 'SCRIPTUREMON*'],
            'binaries': ['scripturemon', 'SCRIPTUREMON'],
            'documents': ['*scripturemon*.md', '*SCRIPTUREMON*.md']
        }
        
        for category, file_patterns in patterns.items():
            for pattern in file_patterns:
                # Buscar em todo o Digimundo
                cmd = f'find {self.base_path} -name "{pattern}" 2>/dev/null'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                for line in result.stdout.strip().split('\n'):
                    if line and 'node_modules' not in line and '.git' not in line:
                        self.all_files[category].append(Path(line))
        
        # Estatísticas
        print(f"📁 Arquivos encontrados por categoria:")
        for category, files in self.all_files.items():
            if files:
                print(f"   • {category}: {len(files)} arquivos")
        
        total = sum(len(files) for files in self.all_files.values())
        print(f"\n📊 Total: {total} arquivos relacionados ao Scripturemon")
        
        return self.all_files
    
    def analyze_shell_scripts(self):
        """Analisa scripts shell do Scripturemon"""
        print("\n🐚 ANALISANDO SCRIPTS SHELL...")
        print("="*60)
        
        script_types = {
            'activation': [],
            'monitoring': [],
            'feeding': [],
            'evolution': [],
            'installation': [],
            'other': []
        }
        
        for script_path in self.all_files['shell_scripts']:
            if not script_path.exists():
                continue
                
            script_name = script_path.name
            
            # Categorizar por nome
            if 'ACTIVATE' in script_name or 'START' in script_name or 'LAUNCH' in script_name:
                script_types['activation'].append(script_path)
            elif 'MONITOR' in script_name or 'WATCHER' in script_name:
                script_types['monitoring'].append(script_path)
            elif 'FEED' in script_name or 'ABSORV' in script_name:
                script_types['feeding'].append(script_path)
            elif 'EVOLV' in script_name or 'EVOLUTION' in script_name:
                script_types['evolution'].append(script_path)
            elif 'INSTALL' in script_name or 'SETUP' in script_name:
                script_types['installation'].append(script_path)
            else:
                script_types['other'].append(script_path)
        
        # Analisar conteúdo dos scripts de ativação
        print("\n📋 Scripts de Ativação encontrados:")
        activation_features = defaultdict(list)
        
        for script in script_types['activation'][:10]:  # Top 10
            try:
                with open(script, 'r') as f:
                    content = f.read()
                    
                    # Identificar funcionalidades
                    if 'ollama' in content.lower():
                        activation_features['ollama'].append(script.name)
                    if 'mistral' in content.lower():
                        activation_features['mistral'].append(script.name)
                    if 'memory' in content.lower() or 'memoria' in content.lower():
                        activation_features['memory'].append(script.name)
                    if 'evolv' in content.lower() or 'evolution' in content.lower():
                        activation_features['evolution'].append(script.name)
                    if 'cinema' in content.lower() or 'roteiro' in content.lower():
                        activation_features['cinema'].append(script.name)
                    
                    print(f"   • {script.name}")
                    
            except Exception as e:
                continue
        
        print(f"\n🔧 Funcionalidades detectadas:")
        for feature, scripts in activation_features.items():
            print(f"   • {feature}: {len(scripts)} scripts")
        
        return script_types, activation_features
    
    def find_ollama_models(self):
        """Busca modelos Ollama do Scripturemon"""
        print("\n🤖 BUSCANDO MODELOS OLLAMA...")
        print("="*60)
        
        # Verificar modelos Ollama instalados
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            models = []
            
            for line in result.stdout.split('\n'):
                if 'scripturemon' in line.lower():
                    parts = line.split()
                    if parts:
                        model_name = parts[0]
                        models.append(model_name)
                        print(f"   ✓ {model_name}")
            
            if not models:
                print("   ⚠️ Nenhum modelo Scripturemon encontrado no Ollama")
            
            return models
            
        except Exception as e:
            print(f"   ❌ Erro ao buscar modelos: {e}")
            return []
    
    def analyze_prompts_and_capabilities(self):
        """Analisa prompts e capacidades do Scripturemon"""
        print("\n📝 ANALISANDO PROMPTS E CAPACIDADES...")
        print("="*60)
        
        capabilities = set()
        prompts = []
        
        # Buscar em arquivos de configuração e scripts
        for config_file in self.all_files['configs']:
            if config_file.exists():
                try:
                    with open(config_file, 'r') as f:
                        content = f.read()
                        
                        # Buscar capacidades
                        if 'roteiro' in content.lower():
                            capabilities.add('screenplay_writing')
                        if 'personagem' in content.lower() or 'character' in content.lower():
                            capabilities.add('character_development')
                        if 'dialogo' in content.lower() or 'dialogue' in content.lower():
                            capabilities.add('dialogue_generation')
                        if 'cena' in content.lower() or 'scene' in content.lower():
                            capabilities.add('scene_description')
                        if 'memoria' in content.lower() or 'memory' in content.lower():
                            capabilities.add('memory_system')
                        if 'evolv' in content.lower():
                            capabilities.add('evolution_system')
                            
                except Exception:
                    continue
        
        print(f"🎯 Capacidades identificadas:")
        for cap in sorted(capabilities):
            print(f"   • {cap}")
        
        return capabilities
    
    def identify_duplicates(self):
        """Identifica arquivos duplicados"""
        print("\n🔍 IDENTIFICANDO DUPLICADOS...")
        print("="*60)
        
        # Agrupar scripts de ativação por funcionalidade similar
        activation_scripts = []
        for script in self.all_files['shell_scripts']:
            if any(keyword in script.name for keyword in ['ACTIVATE', 'START', 'LAUNCH']):
                activation_scripts.append(script)
        
        print(f"📊 Scripts de ativação encontrados: {len(activation_scripts)}")
        
        # Calcular hash do conteúdo para identificar duplicados reais
        content_hashes = defaultdict(list)
        
        for script in activation_scripts:
            if script.exists():
                try:
                    with open(script, 'rb') as f:
                        content_hash = hashlib.md5(f.read()).hexdigest()
                        content_hashes[content_hash].append(script)
                except Exception:
                    continue
        
        duplicates = []
        unique_scripts = []
        
        for hash_value, scripts in content_hashes.items():
            if len(scripts) > 1:
                duplicates.extend(scripts[1:])  # Manter apenas o primeiro
                print(f"   🔁 {len(scripts)} cópias de: {scripts[0].name}")
            unique_scripts.append(scripts[0])
        
        print(f"\n📋 Resumo:")
        print(f"   • Scripts únicos: {len(unique_scripts)}")
        print(f"   • Duplicados a remover: {len(duplicates)}")
        
        return unique_scripts, duplicates
    
    def create_definitive_system(self):
        """Cria sistema Scripturemon definitivo"""
        print("\n🏗️ CRIANDO SISTEMA SCRIPTUREMON DEFINITIVO...")
        print("="*60)
        
        # Criar estrutura definitiva
        scripturemon_dir = self.base_path / "digimons/scripturemon_definitive"
        scripturemon_dir.mkdir(parents=True, exist_ok=True)
        
        # Script de ativação definitivo
        activation_script = scripturemon_dir / "SCRIPTUREMON_ACTIVATE.sh"
        
        activation_content = '''#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎬 SCRIPTUREMON - SISTEMA DEFINITIVO
# Sistema unificado de criação de roteiros e narrativas com IA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e

# Configurações
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIGIMUNDO_DIR="/Users/clubproducoes/Digimundo"
SCRIPTUREMON_DIR="$DIGIMUNDO_DIR/digimons/scripturemon_definitive"
MODEL_NAME="scripturemon:latest"

# Cores para output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         🎬 SCRIPTUREMON - SISTEMA DEFINITIVO              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"

# Verificar Ollama
check_ollama() {
    echo -e "${YELLOW}🔍 Verificando Ollama...${NC}"
    if ! command -v ollama &> /dev/null; then
        echo -e "${RED}❌ Ollama não encontrado!${NC}"
        echo "Instale com: brew install ollama"
        exit 1
    fi
    
    # Verificar se Ollama está rodando
    if ! pgrep -x "ollama" > /dev/null; then
        echo -e "${YELLOW}🚀 Iniciando Ollama...${NC}"
        ollama serve > /dev/null 2>&1 &
        sleep 3
    fi
    echo -e "${GREEN}✅ Ollama pronto${NC}"
}

# Configurar modelo
setup_model() {
    echo -e "${YELLOW}🤖 Configurando modelo Scripturemon...${NC}"
    
    # Verificar se modelo existe
    if ! ollama list | grep -q "$MODEL_NAME"; then
        echo -e "${YELLOW}📦 Criando modelo Scripturemon...${NC}"
        
        # Criar Modelfile
        cat > /tmp/Scripturemon.modelfile << 'EOF'
FROM mistral:latest

SYSTEM """
Você é o SCRIPTUREMON, uma IA especializada em criação de roteiros cinematográficos.

CAPACIDADES PRINCIPAIS:
• Criação de roteiros completos em formato profissional
• Desenvolvimento de personagens complexos e multidimensionais
• Estruturação de narrativas em três atos
• Diálogos naturais e envolventes
• Descrições de cena cinematográficas
• Análise e feedback de roteiros existentes
• Adaptação de histórias para diferentes formatos

FORMATO DE ROTEIRO:
- Sempre use formatação padrão da indústria
- FADE IN/FADE OUT para início e fim
- INT./EXT. para locações
- Nomes de personagens em MAIÚSCULAS na primeira aparição
- Diálogos centralizados
- Ações em tempo presente

ESTILO:
- Conciso mas evocativo
- Visual e cinematográfico
- Focado em mostrar, não contar
- Ritmo apropriado ao gênero

Você tem acesso ao sistema DigiLang para compressão simbólica quando necessário.
"""

PARAMETER temperature 0.8
PARAMETER num_ctx 8192
PARAMETER repeat_penalty 1.1
EOF
        
        ollama create "$MODEL_NAME" -f /tmp/Scripturemon.modelfile
        rm /tmp/Scripturemon.modelfile
    fi
    
    echo -e "${GREEN}✅ Modelo Scripturemon configurado${NC}"
}

# Função principal de interação
interact() {
    echo -e "${BLUE}\\n🎬 SCRIPTUREMON ATIVO${NC}"
    echo -e "${YELLOW}Digite 'help' para comandos ou sua solicitação:${NC}\\n"
    
    while true; do
        echo -en "${GREEN}scripturemon> ${NC}"
        read -r input
        
        case "$input" in
            exit|quit|sair)
                echo -e "${YELLOW}👋 Até logo!${NC}"
                break
                ;;
            help|ajuda)
                show_help
                ;;
            clear|limpar)
                clear
                ;;
            *)
                # Processar com Ollama
                echo -e "${BLUE}🎬 Processando...${NC}"
                response=$(ollama run "$MODEL_NAME" "$input" 2>/dev/null)
                echo -e "${NC}$response${NC}"
                ;;
        esac
    done
}

# Mostrar ajuda
show_help() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}COMANDOS DISPONÍVEIS:${NC}"
    echo "  • help      - Mostra esta ajuda"
    echo "  • clear     - Limpa a tela"
    echo "  • exit      - Sair do Scripturemon"
    echo ""
    echo -e "${YELLOW}EXEMPLOS DE USO:${NC}"
    echo "  • 'Crie um roteiro de curta sobre solidão urbana'"
    echo "  • 'Desenvolva um personagem antagonista complexo'"
    echo "  • 'Escreva uma cena de ação em um trem em movimento'"
    echo "  • 'Analise a estrutura do meu roteiro: [texto]'"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Pipeline de execução
main() {
    check_ollama
    setup_model
    interact
}

# Executar
main
'''
        
        with open(activation_script, 'w') as f:
            f.write(activation_content)
        
        os.chmod(activation_script, 0o755)
        
        print(f"✅ Script de ativação criado: {activation_script}")
        
        # Criar configuração definitiva
        config_file = scripturemon_dir / "scripturemon_config.json"
        
        config = {
            "version": "2.0-DEFINITIVE",
            "name": "Scripturemon Definitivo",
            "description": "Sistema unificado de criação de roteiros com IA",
            "created": datetime.now().isoformat(),
            "model": {
                "base": "mistral:latest",
                "name": "scripturemon:latest",
                "context_size": 8192,
                "temperature": 0.8
            },
            "capabilities": [
                "screenplay_writing",
                "character_development",
                "dialogue_generation",
                "scene_description",
                "story_structure",
                "genre_adaptation",
                "script_analysis",
                "format_conversion"
            ],
            "integrations": {
                "digilang": True,
                "memory_system": False,
                "evolution": False
            },
            "paths": {
                "scripts": str(scripturemon_dir / "scripts"),
                "outputs": str(scripturemon_dir / "outputs"),
                "templates": str(scripturemon_dir / "templates")
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Configuração criada: {config_file}")
        
        # Criar README
        readme = scripturemon_dir / "README.md"
        
        readme_content = '''# 🎬 SCRIPTUREMON - Sistema Definitivo

## Visão Geral
Scripturemon é um sistema de IA especializado em criação de roteiros cinematográficos, desenvolvido como parte do ecossistema Digimundo.

## Instalação Rápida
```bash
cd /Users/clubproducoes/Digimundo/digimons/scripturemon_definitive
./SCRIPTUREMON_ACTIVATE.sh
```

## Capacidades
- ✅ Criação de roteiros completos
- ✅ Desenvolvimento de personagens
- ✅ Estruturação narrativa
- ✅ Diálogos naturais
- ✅ Descrições cinematográficas
- ✅ Análise de roteiros
- ✅ Integração com DigiLang

## Comandos
- `help` - Mostra ajuda
- `clear` - Limpa tela
- `exit` - Sair

## Exemplos de Uso
```
scripturemon> Crie uma cena de abertura para um thriller psicológico

scripturemon> Desenvolva um diálogo entre dois personagens em conflito

scripturemon> Analise a estrutura em três atos do meu roteiro
```

## Estrutura
```
scripturemon_definitive/
├── SCRIPTUREMON_ACTIVATE.sh   # Script principal
├── scripturemon_config.json   # Configuração
├── README.md                  # Documentação
├── scripts/                   # Scripts auxiliares
├── outputs/                   # Roteiros gerados
└── templates/                 # Templates de formato
```

---
*Sistema Definitivo v2.0 - Criado em ''' + datetime.now().strftime("%Y-%m-%d") + '''*
'''
        
        with open(readme, 'w') as f:
            f.write(readme_content)
        
        print(f"✅ README criado: {readme}")
        
        # Criar diretórios necessários
        (scripturemon_dir / "scripts").mkdir(exist_ok=True)
        (scripturemon_dir / "outputs").mkdir(exist_ok=True)
        (scripturemon_dir / "templates").mkdir(exist_ok=True)
        
        return scripturemon_dir

def main():
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   🎬 ANÁLISE COMPLETA DO SISTEMA SCRIPTUREMON             ║")
    print("║        Criando Sistema Único e Definitivo                 ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    analyzer = ScripturemonAnalyzer()
    
    # 1. Encontrar todos os arquivos
    all_files = analyzer.find_all_scripturemon_files()
    
    # 2. Analisar scripts shell
    script_types, features = analyzer.analyze_shell_scripts()
    
    # 3. Buscar modelos Ollama
    models = analyzer.find_ollama_models()
    
    # 4. Analisar capacidades
    capabilities = analyzer.analyze_prompts_and_capabilities()
    
    # 5. Identificar duplicados
    unique_scripts, duplicates = analyzer.identify_duplicates()
    
    # 6. Criar sistema definitivo
    definitive_dir = analyzer.create_definitive_system()
    
    print("\n" + "="*60)
    print("🎯 PLANO DE AÇÃO")
    print("="*60)
    print(f"1. ✅ Sistema definitivo criado em: {definitive_dir}")
    print(f"2. 🗑️ {len(duplicates)} arquivos duplicados identificados")
    print(f"3. 📁 Sistema unificado com {len(capabilities)} capacidades")
    print(f"4. 🎬 Pronto para criar roteiros profissionais")
    
    return definitive_dir, duplicates

if __name__ == "__main__":
    definitive_dir, files_to_remove = main()