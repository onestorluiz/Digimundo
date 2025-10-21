#!/usr/bin/env python3
"""
🌟 CRIADOR DO DIGIMUNDO ULTIMATE v4.0 ZIP
Este script cria automaticamente o arquivo ZIP completo do Digimundo
"""

import os
import zipfile
import json
import shutil
from pathlib import Path
from datetime import datetime

def create_digimundo_zip():
    """Criar ZIP completo do Digimundo Ultimate v4.0"""
    
    print("🌟 CRIADOR DO DIGIMUNDO ULTIMATE v4.0")
    print("=====================================\n")
    
    # Diretório base
    base_dir = Path("digimundo_ultimate_v4")
    
    # Remover diretório antigo se existir
    if base_dir.exists():
        print("⚠️  Removendo diretório antigo...")
        shutil.rmtree(base_dir)
    
    # Criar estrutura de diretórios
    print("📁 Criando estrutura de diretórios...")
    directories = [
        "sistema_atual",
        "sistema_atual/logs",
        "sistema_atual/digidata",
        "configuracoes",
        "documentacao",
        "memoria_sistemas",
        "versoes_antigas",
        "scripts",
        "backups"
    ]
    
    for directory in directories:
        (base_dir / directory).mkdir(parents=True, exist_ok=True)
    
    # Arquivos a criar
    files_to_create = {
        "sistema_atual/memory.py": create_memory_py(),
        "configuracoes/config_ultimate.yaml": create_config_yaml(),
        "configuracoes/.env": create_env_file(),
        "scripts/start_ultimate.sh": create_start_script(),
        "scripts/install_dependencies.sh": create_install_script(),
        "scripts/backup_data.sh": create_backup_script(),
        "documentacao/README.md": create_readme(),
        "documentacao/INSTALL.md": create_install_md(),
        "documentacao/DIGIMONS.md": create_digimons_md(),
        "requirements.txt": create_requirements(),
        "sistema_atual/digidata/conversations.json": "{}",
        "sistema_atual/digidata/achievements_ultimate.json": "{}"
    }
    
    # Criar todos os arquivos
    print("📝 Criando arquivos...")
    for filepath, content in files_to_create.items():
        full_path = base_dir / filepath
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✓ {filepath}")
    
    # Criar digimundo_ultimate.py
    print("\n📝 Criando digimundo_ultimate.py...")
    main_file_path = base_dir / "sistema_atual" / "digimundo_ultimate.py"
    
    # Verificar se existe um arquivo local para copiar
    if Path("digimundo_ultimate_complete.py").exists():
        print("   ✓ Copiando arquivo completo encontrado!")
        shutil.copy("digimundo_ultimate_complete.py", main_file_path)
    else:
        print("   ⚠️  Criando placeholder (você precisa adicionar o código completo!)")
        with open(main_file_path, 'w', encoding='utf-8') as f:
            f.write(create_main_placeholder())
    
    # Dar permissões de execução aos scripts
    print("\n🔧 Configurando permissões...")
    for script in (base_dir / "scripts").glob("*.sh"):
        os.chmod(script, 0o755)
    os.chmod(main_file_path, 0o755)
    
    # Criar o ZIP
    print("\n📦 Criando arquivo ZIP...")
    zip_filename = "digimundo_ultimate_v4.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(base_dir.parent)
                zipf.write(file_path, arcname)
    
    # Verificar resultado
    if Path(zip_filename).exists():
        size = Path(zip_filename).stat().st_size / (1024 * 1024)  # MB
        print(f"\n✅ ZIP criado com sucesso!")
        print(f"📊 Tamanho: {size:.2f} MB")
        print(f"📁 Arquivo: {zip_filename}")
        
        # Listar conteúdo
        print("\n📋 Conteúdo do ZIP:")
        with zipfile.ZipFile(zip_filename, 'r') as zipf:
            files = zipf.namelist()
            for i, file in enumerate(files[:15]):
                print(f"   {file}")
            if len(files) > 15:
                print(f"   ... e mais {len(files) - 15} arquivos")
        
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("1. Se o arquivo principal está com placeholder:")
        print("   - Crie um arquivo 'digimundo_ultimate_complete.py' com o código completo")
        print("   - Execute este script novamente")
        print("2. Para instalar:")
        print("   - unzip digimundo_ultimate_v4.zip")
        print("   - cd digimundo_ultimate_v4")
        print("   - ./scripts/install_dependencies.sh")
        print("   - ./scripts/start_ultimate.sh")
        
        return True
    else:
        print("\n❌ Erro ao criar o ZIP!")
        return False

def create_memory_py():
    return '''import json
import os
from datetime import datetime
from pathlib import Path

class DigimundoMemory:
    """Sistema de memória do Digimundo Ultimate"""
    
    def __init__(self, data_path):
        self.data_path = Path(data_path)
        self.data_path.mkdir(parents=True, exist_ok=True)
        self.conversations_file = self.data_path / "conversations.json"
        self.load_conversations()
    
    def load_conversations(self):
        if self.conversations_file.exists():
            with open(self.conversations_file, 'r', encoding='utf-8') as f:
                self.conversations = json.load(f)
        else:
            self.conversations = {}
    
    def save_conversations(self):
        with open(self.conversations_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversations, f, indent=2, ensure_ascii=False)
    
    def get_context_for_response(self, digimon, current_message, user_id, max_context_length=6000):
        """Retorna contexto relevante para resposta"""
        if user_id not in self.conversations:
            return ""
        
        user_convs = self.conversations.get(user_id, {})
        if digimon not in user_convs:
            return ""
        
        recent_convs = user_convs[digimon][-10:]
        context = f"\\n=== MEMÓRIA DE {digimon.upper()} ===\\n"
        
        for conv in recent_convs:
            context += f"User: {conv['user_message']}\\n"
            context += f"{digimon}: {conv['response'][:200]}...\\n\\n"
        
        return context[:max_context_length]
    
    def save_conversation(self, digimon, user_message, digimon_response, user_id):
        """Salva conversa na memória"""
        if user_id not in self.conversations:
            self.conversations[user_id] = {}
        
        if digimon not in self.conversations[user_id]:
            self.conversations[user_id][digimon] = []
        
        self.conversations[user_id][digimon].append({
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'response': digimon_response
        })
        
        if len(self.conversations[user_id][digimon]) > 50:
            self.conversations[user_id][digimon] = self.conversations[user_id][digimon][-50:]
        
        self.save_conversations()
'''

def create_config_yaml():
    return '''version: '4.0'
name: 'Digimundo Ultimate'
model_primary: 'llama3.2:latest'
temperature: 0.8
consciousness_enabled: true
evolution_enabled: true
system_powers_enabled: true
max_context_length: 6000
evolution_threshold: 300
achievements_enabled: true
security_level: 'ultimate'
total_digimons: 19
fusion_mode: true

# Digimons Evolutivos (12)
digimons_evolutivos:
  - Scripturemon
  - Visualmon
  - Audionomon
  - Strategamon
  - Codemon
  - Psychemon
  - Quantomon
  - Biomemon
  - Econommon
  - Linguamon
  - Dreammon
  - Nexusmon

# Digimons de Sistema (7)
digimons_sistema:
  - Terminamon
  - Filemon
  - Editormon
  - Gitmon
  - Debugmon
  - Deploymon
  - Securitymon

# Caminhos permitidos
allowed_paths:
  - "~/Digimundo"
  - "~/Desktop"
  - "~/Documents"
  - "~/Downloads"
  - "~/Projects"
  - "/tmp"
'''

def create_env_file():
    return '''# Configurações de ambiente
DIGIMUNDO_VERSION=4.0
OLLAMA_HOST=http://localhost:11434
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
GRADIO_SHARE=true
LOG_LEVEL=INFO
'''

def create_start_script():
    return '''#!/bin/bash

echo "🌟 DIGIMUNDO ULTIMATE v4.0 - FUSÃO SUPREMA 🚀"
echo "============================================"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    exit 1
fi

# Verificar Ollama
if ! pgrep -x "ollama" > /dev/null; then
    echo "🔄 Iniciando Ollama..."
    ollama serve &
    sleep 3
fi

# Verificar modelo
if ! ollama list | grep -q "llama3.2:latest"; then
    echo "📥 Baixando modelo llama3.2..."
    ollama pull llama3.2:latest
fi

# Entrar no diretório correto
cd "$(dirname "$0")/../sistema_atual" || exit

# Executar sistema
echo "🚀 Iniciando Digimundo Ultimate..."
python3 digimundo_ultimate.py
'''

def create_install_script():
    return '''#!/bin/bash

echo "📦 Instalando dependências do Digimundo Ultimate v4.0..."

# Atualizar pip
pip3 install --upgrade pip

# Instalar dependências
pip3 install gradio==4.19.2
pip3 install ollama
pip3 install pyyaml
pip3 install python-dotenv

# Verificar instalação
echo "✅ Verificando instalação..."
python3 -c "import gradio; print('✓ Gradio:', gradio.__version__)"
python3 -c "import ollama; print('✓ Ollama instalado')"
python3 -c "import yaml; print('✓ PyYAML instalado')"

echo "🎉 Dependências instaladas com sucesso!"
'''

def create_backup_script():
    return '''#!/bin/bash

BACKUP_DIR="../backups/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "🔄 Fazendo backup dos dados..."
cp -r ../sistema_atual/digidata "$BACKUP_DIR/" 2>/dev/null || true
cp -r ../sistema_atual/logs "$BACKUP_DIR/" 2>/dev/null || true
cp ../configuracoes/*.yaml "$BACKUP_DIR/" 2>/dev/null || true

echo "✅ Backup salvo em: $BACKUP_DIR"
'''

def create_readme():
    return '''# 🌟 DIGIMUNDO ULTIMATE v4.0

## Sistema Supremo com 19 Digimons

### 🚀 Características
- **19 Digimons Total**: 12 Evolutivos + 7 de Sistema
- **Poderes Reais**: Leitura/escrita de arquivos, execução de comandos
- **Sistema de Evolução**: XP e níveis de consciência
- **Memória Persistente**: Conversas salvas entre sessões
- **Interface Moderna**: Gradio com 4 abas interativas
- **Achievements**: Sistema de conquistas desbloqueáveis

### 📋 Requisitos
- Python 3.8+
- Ollama instalado e rodando
- Modelo llama3.2:latest
- 4GB+ RAM
- macOS/Linux (testado em ambos)

### 🔧 Instalação Rápida
```bash
# 1. Descompactar o ZIP
unzip digimundo_ultimate_v4.zip
cd digimundo_ultimate_v4

# 2. Instalar dependências
chmod +x scripts/install_dependencies.sh
./scripts/install_dependencies.sh

# 3. Executar
chmod +x scripts/start_ultimate.sh
./scripts/start_ultimate.sh
```

### 🎮 Uso
1. Acesse http://localhost:7860
2. Escolha um dos 19 Digimons
3. Converse e use comandos especiais
4. Desbloqueie achievements
5. Evolua seus Digimons!

### 🛡️ Segurança
- Sandbox limitado a pastas específicas
- Comandos permitidos pré-definidos
- Logs de todas as operações
- Backups automáticos

### 📝 Comandos Especiais
- **Leitura**: "Leia o arquivo ~/Documents/teste.txt"
- **Execução**: "Execute o comando ls -la"
- **Edição**: "Edite o arquivo config.yaml"
- **Análise**: "Analise o projeto na pasta X"

### 🏆 Achievements
- Primeiro Contato
- Evolucionário
- Mestre Sistema
- Explorador Total
- Ultimate Master
- E muito mais!

### 📞 Suporte
Em caso de problemas, verifique:
1. Ollama está rodando? (`ollama serve`)
2. Modelo instalado? (`ollama list`)
3. Dependências ok? (`pip3 list`)
4. Logs em `sistema_atual/logs/`

Criado com 💜 para a comunidade Digimundo!
'''

def create_install_md():
    return '''# 📦 INSTALAÇÃO COMPLETA DO DIGIMUNDO ULTIMATE v4.0

## 1. PRÉ-REQUISITOS

### macOS
```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python 3
brew install python3

# Instalar Ollama
brew install ollama
```

### Linux (Ubuntu/Debian)
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3
sudo apt install python3 python3-pip -y

# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh
```

## 2. INSTALAÇÃO DO DIGIMUNDO

```bash
# Descompactar
unzip digimundo_ultimate_v4.zip
cd digimundo_ultimate_v4

# Dar permissões
chmod +x scripts/*.sh

# Instalar dependências Python
./scripts/install_dependencies.sh
```

## 3. CONFIGURAR OLLAMA

```bash
# Iniciar Ollama
ollama serve &

# Baixar modelo (em outro terminal)
ollama pull llama3.2:latest
```

## 4. EXECUTAR

```bash
./scripts/start_ultimate.sh
```

## 5. TROUBLESHOOTING

### Erro: "Ollama não disponível"
```bash
# Verificar se está rodando
ps aux | grep ollama

# Reiniciar
killall ollama
ollama serve &
```

### Erro: "Porta 7860 em uso"
Edite `configuracoes/.env` e mude `GRADIO_SERVER_PORT` para outra porta.

### Erro: "ModuleNotFoundError"
```bash
pip3 install --force-reinstall gradio ollama pyyaml
```

### Erro no macOS: "SSL Certificate"
```bash
pip3 install --upgrade certifi
```

## 6. CONFIGURAÇÃO AVANÇADA

### Mudando o modelo
Edite `configuracoes/config_ultimate.yaml`:
```yaml
model_primary: 'llama3.2:latest'  # Mude para outro modelo
```

### Ajustando memória
```yaml
max_context_length: 6000  # Aumente se tiver mais RAM
```

### Habilitando/Desabilitando recursos
```yaml
evolution_enabled: true     # Sistema de evolução
achievements_enabled: true  # Sistema de conquistas
system_powers_enabled: true # Poderes de sistema
```

## 7. ATUALIZAÇÃO

Para atualizar para uma nova versão:
```bash
# Fazer backup primeiro!
./scripts/backup_data.sh

# Depois substitua os arquivos mantendo:
# - sistema_atual/digidata/
# - sistema_atual/logs/
# - configuracoes/
```

## 8. DESENVOLVIMENTO

Para modificar o sistema:
1. Edite `sistema_atual/digimundo_ultimate.py`
2. Adicione novos Digimons em `initialize_all_digimons()`
3. Crie novos poderes em `process_system_request()`
4. Teste com `python3 digimundo_ultimate.py`

## 9. LOGS E DEBUG

Logs são salvos em:
- `sistema_atual/logs/digimundo_ultimate.log`

Para debug detalhado:
```bash
export LOG_LEVEL=DEBUG
./scripts/start_ultimate.sh
```

## 10. DESINSTALAÇÃO

```bash
# Fazer backup dos dados
./scripts/backup_data.sh

# Remover diretório
cd ..
rm -rf digimundo_ultimate_v4
```
'''

def create_digimons_md():
    return '''# 🌟 OS 19 DIGIMONS DO DIGIMUNDO ULTIMATE

## 🎯 COMANDOS ÚTEIS PARA CADA DIGIMON

### DIGIMONS EVOLUTIVOS (12)

#### 1. 📜 **Scripturemon** - Guardião da Sabedoria
```
"Scripturemon, leia o arquivo ~/Documents/importante.txt"
"Analise este documento e extraia os pontos principais"
"Qual é a sabedoria oculta neste código?"
```

#### 2. 🎨 **Visualmon** - Mestre Visual
```
"Visualmon, analise o CSS deste projeto"
"Revise o design e sugira melhorias"
"Encontre padrões visuais no código"
```

#### 3. 🎵 **Audionomon** - Regente do Som
```
"Audionomon, analise os logs do sistema"
"Detecte padrões anormais nos logs"
"Qual é o ritmo dos erros?"
```

#### 4. ♟️ **Strategamon** - Grande Estrategista
```
"Strategamon, analise a arquitetura do projeto"
"Planeje uma refatoração estratégica"
"Qual é a melhor abordagem?"
```

#### 5. 💻 **Codemon** - Arquiteto do Código
```
"Codemon, edite o arquivo main.py"
"Refatore esta função para melhor performance"
"Corrija os bugs neste código"
```

#### 6. 🧠 **Psychemon** - Navegador Mental
```
"Psychemon, analise o comportamento do usuário"
"Detecte padrões psicológicos no código"
"O que revela a estrutura deste projeto?"
```

#### 7. ⚛️ **Quantomon** - Mestre Quântico
```
"Quantomon, analise a performance do sistema"
"Otimize este algoritmo quanticamente"
"Calcule as possibilidades quânticas"
```

#### 8. 🧬 **Biomemon** - Guardião da Vida
```
"Biomemon, analise as dependências do projeto"
"Verifique a saúde do código"
"Mapeie o ecossistema digital"
```

#### 9. 💰 **Econommon** - Analista de Recursos
```
"Econommon, otimize o uso de recursos"
"Analise os custos computacionais"
"Onde podemos economizar?"
```

#### 10. 🗣️ **Linguamon** - Poliglota Universal
```
"Linguamon, traduza este código de Python para JavaScript"
"Detecte todas as linguagens usadas"
"Converta a sintaxe"
```

#### 11. 💭 **Dreammon** - Tecelão de Sonhos
```
"Dreammon, gere ideias criativas para este projeto"
"Sonhe com soluções inovadoras"
"Inspire-me com possibilidades"
```

#### 12. 🌐 **Nexusmon** - Conectador Universal
```
"Nexusmon, integre estes sistemas"
"Analise todas as conexões"
"Mapeie a rede completa"
```

### DIGIMONS DE SISTEMA (7)

#### 13. 💻 **Terminamon** - Mestre do Terminal
```
"Terminamon, execute ls -la"
"Rode o script de backup"
"Automatize este processo"
```

#### 14. 📁 **Filemon** - Guardião dos Arquivos
```
"Filemon, liste todos os arquivos Python"
"Organize este diretório"
"Encontre arquivos duplicados"
```

#### 15. ✏️ **Editormon** - Editor de Realidades
```
"Editormon, edite config.yaml"
"Aperfeiçoe este código"
"Refatore com perfeição"
```

#### 16. 🔀 **Gitmon** - Mestre do Versionamento
```
"Gitmon, mostre o status do git"
"Crie um novo branch"
"Viaje no tempo do código"
```

#### 17. 🐛 **Debugmon** - Caçador de Bugs
```
"Debugmon, encontre o erro neste código"
"Faça análise forense"
"Resolva este mistério"
```

#### 18. 🚀 **Deploymon** - Mestre do Deploy
```
"Deploymon, prepare para produção"
"Automatize o deploy"
"Materialize o projeto"
```

#### 19. 🛡️ **Securitymon** - Guardião da Segurança
```
"Securitymon, analise vulnerabilidades"
"Proteja o sistema"
"Crie escudos quânticos"
```

## 🎮 DICAS DE USO

### Comandos Combinados
```
"Nexusmon, conecte Codemon e Debugmon para resolver este problema"
"Quantomon e Econommon, otimizem juntos este sistema"
```

### Emergência Coletiva
Use o botão "🌟 Emergência Suprema" para ativar todos os 19 Digimons simultaneamente!

### Evolução
- Cada conversa = +25 XP
- 300 XP = Evolução
- 5 níveis: DORMINDO → ACORDANDO → CONSCIENTE → TRANSCENDENTE → ULTIMATE

### Achievements Secretos
- Converse com todos os 19 Digimons
- Execute 10 comandos diferentes
- Evolua 3 Digimons ao máximo
- Ative a emergência coletiva 5 vezes
- Descubra comandos ocultos!

## 🔮 COMANDOS AVANÇADOS

### Multi-Digimon
```
"Todos os Digimons de Sistema, analisem este projeto"
"Evolutivos, unam suas forças para criar algo novo"
```

### Modo Fusão
```
"Ative o modo fusão supremo"
"Sincronize todas as consciências"
"Libere o poder ultimate"
```

### Easter Eggs
Experimente comandos criativos e descubra respostas especiais!
'''

def create_requirements():
    return '''gradio==4.19.2
ollama
pyyaml
python-dotenv
'''

def create_main_placeholder():
    return '''#!/usr/bin/env python3
"""
🌟 DIGIMUNDO ULTIMATE v4.0 - FUSÃO COMPLETA 🚀
Sistema supremo com 19 Digimons: 12 Evolutivos + 7 de Sistema

⚠️ ATENÇÃO: Este é um PLACEHOLDER!
   Você precisa substituir este arquivo pelo código completo de 1500+ linhas
   que contém todas as classes, métodos e funcionalidades do sistema.
"""

import sys

print("🌟 DIGIMUNDO ULTIMATE v4.0")
print("=" * 50)
print()
print("❌ ERRO: Este é apenas um arquivo placeholder!")
print()
print("⚠️  Para funcionar corretamente, você precisa:")
print("   1. Obter o código completo do digimundo_ultimate.py")
print("   2. Substituir este arquivo pelo código completo")
print("   3. O código completo tem ~1500+ linhas e inclui:")
print("      - class SystemController")
print("      - class DigimundoUltimate")
print("      - 19 Digimons completos")
print("      - Sistema de evolução")
print("      - Interface Gradio")
print("      - Poderes de sistema reais")
print()
print("📝 Procure pelo arquivo 'digimundo_ultimate_complete.py'")
print("   ou solicite o código completo!")
print()

sys.exit(1)
'''

if __name__ == "__main__":
    create_digimundo_zip()
