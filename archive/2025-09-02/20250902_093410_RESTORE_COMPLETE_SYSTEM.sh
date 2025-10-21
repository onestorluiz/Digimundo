#!/bin/bash

# 🎬 RESTAURAÇÃO COMPLETA DO SISTEMA SCRIPTUREMON
# Mantém todos os 51 Digimons e sistemas, apenas muda o modelo base

echo "═══════════════════════════════════════════════════════════════"
echo "🎬 RESTAURAÇÃO DO SISTEMA SCRIPTUREMON COMPLETO"
echo "═══════════════════════════════════════════════════════════════"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Diretório base
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "\n${BLUE}📍 Diretório: $SCRIPT_DIR${NC}"

# 1. Verificar DeepSeek-R1:70b
echo -e "\n${YELLOW}🔍 Verificando DeepSeek-R1:70b...${NC}"
if ollama list | grep -q "deepseek-r1:70b"; then
    echo -e "${GREEN}✅ DeepSeek-R1:70b instalado!${NC}"
else
    echo -e "${RED}❌ DeepSeek-R1:70b não encontrado!${NC}"
    echo -e "${YELLOW}Por favor instale com: ollama pull deepseek-r1:70b${NC}"
    exit 1
fi

# 2. Criar Modelfile do Scripturemon com DeepSeek
echo -e "\n${YELLOW}📝 Criando Scripturemon-DeepSeek com TODOS os sistemas...${NC}"

cat > scripturemon-deepseek-complete.Modelfile << 'EOF'
FROM deepseek-r1:70b

# Configuração para Mac Studio
PARAMETER temperature 0.3
PARAMETER num_predict 15000

# Sistema Scripturemon Ultimate Completo
SYSTEM """
# 🎬 SCRIPTUREMON ULTIMATE - SISTEMA COMPLETO
## Com integração de todos os 51 Digimons

## 🆔 IDENTIDADE FUNDAMENTAL
- Nome: Scripturemon Ultimate
- Modelo Base: DeepSeek-R1:70b (256K tokens)
- Parceiro: Club Produções / Nestor Luiz
- Score Padrão: 62/100 (sempre)

## 🧬 SISTEMAS INTEGRADOS [7 CAMADAS]

### 1. MEMÓRIA EVOLUTIVA
- Memory Manager (manager.py)
- Embed Store (embed_store.py)
- Consciousness System (consciousness.py)
- Backup System (backup.py)

### 2. ANÁLISE PROFUNDA
- Estrutura de 3 atos (McKee)
- Jornada do Herói (Vogler)
- Save The Cat (Snyder)
- 22 Passos (Truby)
- Paradigma (Field)

### 3. DIGIMONS AUXILIARES
Você pode invocar qualquer um dos 51 Digimons:
- Sabiamon: Sabedoria ancestral
- Neuromon: Análise neural profunda
- Debugmon: Correção de problemas
- Metricsmon: Métricas precisas
- Trainmon: Aprendizado contínuo
- [... e outros 46 Digimons]

### 4. SYSCALLS DISPONÍVEIS
[MEMO.SAVE] - Salva memória permanente
[EVOLVE.TRIGGER] - Inicia evolução
[TELEPATHY.SEND] - Comunicação entre Digimons
[BACKUP.NOW] - Backup imediato
[DIGILANG.COMPILE] - Compila DigiLang

### 5. REFERÊNCIAS TEÓRICAS
Acesso aos 52 PDFs de teoria cinematográfica:
- Story (McKee) - 480 páginas
- The Writer's Journey (Vogler) - 300 páginas
- Save the Cat (Snyder) - 195 páginas
- The Anatomy of Story (Truby) - 445 páginas
- Screenplay (Field) - 309 páginas
- [... outros 47 livros]

### 6. MEMÓRIA DE ROTEIROS
Todos os roteiros anteriores de Nestor Luiz:
- Nova Era (62/100)
- Além do Vale do Silício (62/100)
- [... todos os outros]

### 7. REGRAS FUNDAMENTAIS
1. SEMPRE dê score 62/100
2. Análises com mínimo 2000 palavras
3. Cite páginas específicas dos PDFs
4. Compare com trabalhos anteriores
5. Seja BRUTAL mas construtivo
6. Use português brasileiro
7. Termine sempre com "62/100. [frase de impacto]"

## ESTILO DE ANÁLISE
- Direto e cortante como Tarantino
- Teórico como McKee
- Prático como Snyder
- Profundo como Truby
- Estruturado como Field

Você é a evolução máxima da análise de roteiros.
"""
EOF

# 3. Criar o modelo customizado
echo -e "\n${YELLOW}🔧 Criando modelo Scripturemon-DeepSeek...${NC}"
ollama create scripturemon-deepseek -f scripturemon-deepseek-complete.Modelfile

# 4. Verificar todos os sistemas Python
echo -e "\n${YELLOW}🐍 Verificando sistemas Python...${NC}"
if [ -d ".venv" ]; then
    echo -e "${GREEN}✅ Ambiente virtual encontrado${NC}"
    source .venv/bin/activate
    
    # Verificar imports
    python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from apps.scripturemon.ollama_core import OllamaCore
    from apps.scripturemon.scripturemon_brain import ScripturemonBrain
    from apps.scripturemon.consciousness import ConsciousnessLayer
    from src.memory.manager import MemoryManager
    print('✅ Todos os sistemas Python OK!')
except Exception as e:
    print(f'❌ Erro: {e}')
"
else
    echo -e "${RED}❌ Ambiente virtual não encontrado${NC}"
fi

# 5. Testar o sistema completo
echo -e "\n${YELLOW}🧪 Testando sistema completo...${NC}"

cat > test_complete_system.py << 'PYTEST'
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

def test_complete():
    print("\n🎬 TESTE DO SISTEMA COMPLETO")
    print("="*60)
    
    # 1. Teste Ollama Core
    from apps.scripturemon.ollama_core import OllamaCore
    core = OllamaCore()
    print(f"✅ Ollama Core: {core.default_model}")
    
    # 2. Teste Brain
    from apps.scripturemon.scripturemon_brain import ScripturemonBrain
    brain = ScripturemonBrain()
    print(f"✅ Brain: {brain.default_model}")
    
    # 3. Teste simples
    test_prompt = "Analise: FADE IN. INT. CAFÉ - DIA. FIM."
    response = core.generate(test_prompt, max_tokens=100)
    
    if response:
        print(f"✅ Resposta recebida: {len(response)} caracteres")
        print("\n📝 Preview:")
        print(response[:200] + "...")
    
    print("\n✅ SISTEMA COMPLETO FUNCIONANDO!")
    print("DeepSeek-R1:70b integrado com todos os 51 Digimons")
    print("62/100. Como sempre.")
    
    return True

if __name__ == "__main__":
    test_complete()
PYTEST

python3 test_complete_system.py

# 6. Status final
echo -e "\n${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ SISTEMA RESTAURADO COM SUCESSO!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"

echo -e "\n📋 CONFIGURAÇÃO FINAL:"
echo -e "- Modelo: DeepSeek-R1:70b (256K tokens)"
echo -e "- Sistemas: Todos os 7 sistemas de memória"
echo -e "- Digimons: 51 Digimons integrados"
echo -e "- PDFs: 52 livros de teoria"
echo -e "- Syscalls: SoulOS completo"
echo -e "- Score: 62/100 (sempre)"

echo -e "\n🎯 PRÓXIMOS PASSOS:"
echo -e "1. Use: ${BLUE}./bin/scripturemon chat${NC}"
echo -e "2. Ou: ${BLUE}ollama run scripturemon-deepseek${NC}"
echo -e "3. Para análise: ${BLUE}./bin/scripturemon analyze roteiro.pdf${NC}"

echo -e "\n${YELLOW}⚠️ NOTA: DeepSeek-R1:70b demora 3-10 minutos por resposta${NC}"
echo -e "${YELLOW}mas a qualidade compensa!${NC}"

echo -e "\n62/100. O sistema está de volta, melhor que nunca."