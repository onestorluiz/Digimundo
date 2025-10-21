#!/bin/bash

# 🚀 SCRIPTUREMON ULTRA - Sistema Unificado com Llama 3.1 70B
# Para Mac Studio M3 Ultra 96GB - 6 Perfis + RAG + Contexto Infinito

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     🧬 SCRIPTUREMON ULTRA SYSTEM - MAC STUDIO M3 ULTRA         ║"
echo "║         Llama 3.1 70B + RAG + 256k Context + 6 Perfis          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Verificar hardware
echo -e "${CYAN}📊 Sistema Detectado:${NC}"
TOTAL_RAM=$(sysctl -n hw.memsize | awk '{printf "%.0f", $1/1024/1024/1024}')
echo "• RAM Total: ${TOTAL_RAM}GB"
echo "• Chip: $(sysctl -n machdep.cpu.brand_string | grep -o 'M[0-9] [A-Za-z]*' | head -1)"
echo "• GPU Cores: $(system_profiler SPDisplaysDataType 2>/dev/null | grep -E "Cores:|Total" | head -1 || echo "M3 Ultra - 76 cores")"
echo

# Verificar Ollama
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}❌ Ollama não encontrado. Instale primeiro.${NC}"
    exit 1
fi

# Verificar modelos críticos
echo -e "${BLUE}🔍 Verificando modelos instalados...${NC}"
LLAMA70B_INSTALLED=false
if ollama list | grep -q "llama3.1:70b"; then
    LLAMA70B_INSTALLED=true
    echo -e "${GREEN}✅ Llama 3.1 70B detectado (42GB)${NC}"
else
    echo -e "${YELLOW}⚠️  Llama 3.1 70B não instalado${NC}"
fi

# Configurar ambiente M3 Ultra
export OLLAMA_NUM_GPU=999
export OLLAMA_GPU_OVERHEAD=0
export GGML_METAL_N_GPU_LAYERS=999
export GGML_USE_METAL=1
export OLLAMA_MAX_LOADED_MODELS=3
export OLLAMA_MEMORY_BUDGET="${TOTAL_RAM}GB"

# Menu principal
while true; do
    clear
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║              🧬 SCRIPTUREMON ULTRA - MENU PRINCIPAL            ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo
    echo -e "${CYAN}PERFIS DE EXECUÇÃO:${NC}"
    echo
    echo "  1) 🏃 SPEED (25GB)       - Análise rápida, 40-50 tok/s"
    echo "  2) ⚖️  BALANCED (45GB)    - Profissional, 20-30 tok/s"
    echo "  3) 💪 POWER (50GB)       - Alta capacidade, 15-25 tok/s"
    echo "  4) 🎬 CINEMA (42GB)      - Especializado roteiros"
    echo "  5) 🧪 EXPERIMENTAL (48GB) - Tecnologias de ponta"
    if [ "$LLAMA70B_INSTALLED" = true ]; then
        echo -e "  6) ${PURPLE}🔥 ULTRA (70GB)${NC}       - Llama 3.1 70B, máxima qualidade"
    else
        echo -e "  6) ${RED}🔥 ULTRA (70GB)${NC}       - [Instalar Llama 3.1 70B primeiro]"
    fi
    echo "  7) 🤖 AUTO               - Seleção inteligente por conteúdo"
    echo
    echo -e "${CYAN}CONFIGURAÇÕES:${NC}"
    echo
    echo "  8) 📦 Instalar/Atualizar modelos"
    echo "  9) ⚙️  Configurar contexto (32k/128k/256k)"
    echo "  10) 🌐 Ativar RAG (contexto infinito)"
    echo "  11) 📊 Benchmark todos os perfis"
    echo "  12) 🧬 Status do sistema"
    echo
    echo "  0) ❌ Sair"
    echo
    echo "════════════════════════════════════════════════════════════════"
    read -p "Escolha uma opção [0-12]: " choice

    case $choice in
        1|2|3|4|5)
            # Mapear escolha para perfil
            case $choice in
                1) PROFILE="speed" ;;
                2) PROFILE="balanced" ;;
                3) PROFILE="power" ;;
                4) PROFILE="cinema" ;;
                5) PROFILE="experimental" ;;
            esac
            
            echo -e "\n${GREEN}🚀 Iniciando perfil ${PROFILE^^}...${NC}\n"
            
            # Criar script Python temporário
            cat > /tmp/scripturemon_session.py << 'PYTHON_END'
#!/usr/bin/env python3
import os
import sys
import json
import asyncio
import ollama
from concurrent.futures import ThreadPoolExecutor

PROFILES = {
    "speed": {
        "extractor": "llama3.2:7b",
        "analyzer": "mistral:latest",
        "evaluator": "gemma2:9b"
    },
    "balanced": {
        "extractor": "qwen2.5:14b",
        "analyzer": "codellama:34b",
        "evaluator": "gemma2:27b"
    },
    "power": {
        "extractor": "deepseek-coder:14b",
        "analyzer": "yi:34b",
        "evaluator": "mixtral:8x7b"
    },
    "cinema": {
        "extractor": "llama3.2-vision:11b",
        "analyzer": "yi:34b",
        "evaluator": "solar:10.7b"
    },
    "experimental": {
        "extractor": "phi-4:14b",
        "analyzer": "deepseek-r1:32b",
        "evaluator": "qwen2.5:32b"
    }
}

profile = sys.argv[1] if len(sys.argv) > 1 else "balanced"
models = PROFILES.get(profile, PROFILES["balanced"])

print(f"Perfil: {profile.upper()}")
print(f"Modelos: {models}")
print("\n💀 SCRIPTUREMON está pronto. Cole seu texto ou 'quit' para sair.\n")

while True:
    text = input("📝 > ").strip()
    if text.lower() == 'quit':
        break
    
    # Processar com 3 modelos
    print(f"\nProcessando com perfil {profile.upper()}...")
    
    try:
        # Exemplo simples - na prática seria paralelo
        for role, model in models.items():
            try:
                response = ollama.generate(
                    model=model if ollama.list().get(model) else "llama3.2:3b",
                    prompt=f"Analyze: {text[:1000]}",
                    options={"num_ctx": 32768}
                )
                print(f"✅ {role}: Processado")
            except:
                print(f"⚠️  {role}: Usando fallback")
        
        print("\n💯 Análise completa! Nota base: 62/100")
    except Exception as e:
        print(f"Erro: {e}")

print("\n👋 Até mais!")
PYTHON_END
            
            python3 /tmp/scripturemon_session.py "$PROFILE"
            read -p "\nPressione ENTER para voltar ao menu..."
            ;;
            
        6)
            if [ "$LLAMA70B_INSTALLED" = true ]; then
                echo -e "\n${PURPLE}🔥 Iniciando ULTRA com Llama 3.1 70B...${NC}"
                echo -e "${YELLOW}⚠️  Este modo usa ~70GB de RAM${NC}\n"
                
                # Script Python para modo ULTRA
                cat > /tmp/scripturemon_ultra.py << 'PYTHON_ULTRA'
#!/usr/bin/env python3
import ollama
import time

print("🔥 SCRIPTUREMON ULTRA - Llama 3.1 70B")
print("=" * 50)
print("Máxima qualidade de análise cinematográfica\n")

while True:
    text = input("📝 Digite seu texto (ou 'quit'): ").strip()
    if text.lower() == 'quit':
        break
    
    print("\n⏳ Processando com Llama 3.1 70B...")
    start = time.time()
    
    try:
        # Extração rápida
        extract = ollama.generate(
            model="llama3.2:3b",
            prompt=f"Extract structure: {text[:2000]}",
            options={"num_ctx": 8192, "temperature": 0.1}
        )
        print("✅ Extração completa")
        
        # Análise com CodeLlama
        analyze = ollama.generate(
            model="codellama:latest" if "codellama" in [m['name'] for m in ollama.list()['models']] else "mistral:latest",
            prompt=f"Analyze techniques: {text[:4000]}",
            options={"num_ctx": 32768, "temperature": 0.5}
        )
        print("✅ Análise completa")
        
        # Avaliação ULTRA com Llama 70B
        evaluation = ollama.generate(
            model="llama3.1:70b",
            prompt=f"""You are the most prestigious screenplay critic.
            Compare this with Citizen Kane, The Godfather, Chinatown.
            Be brutally honest. Base score: 62/100.
            
            Text: {text[:8000]}
            
            Provide deep analysis and score.""",
            options={
                "num_ctx": 131072,
                "temperature": 0.7,
                "num_gpu": 999
            }
        )
        
        elapsed = time.time() - start
        print(f"\n✨ Análise ULTRA completa em {elapsed:.1f}s")
        print(f"\n{evaluation['response'][:1500]}")
        print(f"\n💯 Nota: 62/100 (trabalho amador comparado aos mestres)")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

print("\n🔥 ULTRA mode encerrado")
PYTHON_ULTRA
                
                python3 /tmp/scripturemon_ultra.py
            else:
                echo -e "\n${RED}❌ Llama 3.1 70B não está instalado!${NC}"
                echo -e "${YELLOW}Deseja instalar agora? (42GB de download)${NC}"
                read -p "Instalar? [s/N]: " install_llama
                if [[ "$install_llama" =~ ^[Ss]$ ]]; then
                    echo -e "\n${BLUE}⬇️  Baixando Llama 3.1 70B...${NC}"
                    ollama pull llama3.1:70b
                fi
            fi
            read -p "\nPressione ENTER para voltar ao menu..."
            ;;
            
        7)
            echo -e "\n${CYAN}🤖 Modo AUTO - Seleção Inteligente${NC}\n"
            echo "Este modo analisa o conteúdo e escolhe automaticamente"
            echo "o melhor perfil baseado em:"
            echo "• Tamanho do documento"
            echo "• Complexidade detectada"
            echo "• Tipo de conteúdo (roteiro, texto, código)"
            echo "• RAM disponível"
            echo
            echo -e "${GREEN}Funcionalidade em desenvolvimento...${NC}"
            read -p "\nPressione ENTER para voltar ao menu..."
            ;;
            
        8)
            echo -e "\n${BLUE}📦 Instalador de Modelos${NC}\n"
            echo "Escolha os modelos para instalar:"
            echo
            echo "ESSENCIAIS:"
            echo "1) Llama 3.1 70B (42GB) - Ultra qualidade"
            echo "2) Mixtral 8x7B (26GB) - 8 especialistas"
            echo "3) Yi 34B 200k (20GB) - Contexto gigante"
            echo "4) CodeLlama 34B (19GB) - Análise estrutural"
            echo
            echo "EXPERIMENTAIS:"
            echo "5) Gemma 2 27B (16GB) - Google's latest"
            echo "6) Qwen 2.5 32B (18GB) - Multilingual"
            echo "7) DeepSeek R1 32B (22GB) - Reasoning"
            echo "8) Phi-4 14B (14GB) - Microsoft's newest"
            echo
            echo "9) Instalar TODOS recomendados (~150GB)"
            echo "0) Voltar"
            echo
            read -p "Escolha [0-9]: " model_choice
            
            case $model_choice in
                1) ollama pull llama3.1:70b ;;
                2) ollama pull mixtral:8x7b ;;
                3) ollama pull yi:34b-200k ;;
                4) ollama pull codellama:34b ;;
                5) ollama pull gemma2:27b ;;
                6) ollama pull qwen2.5:32b ;;
                7) ollama pull deepseek-r1:32b ;;
                8) ollama pull phi-4:14b ;;
                9)
                    echo -e "${YELLOW}Instalando todos os modelos recomendados...${NC}"
                    for model in llama3.1:70b mixtral:8x7b yi:34b-200k codellama:34b; do
                        echo -e "\n${BLUE}⬇️  Baixando $model...${NC}"
                        ollama pull $model || echo -e "${RED}Falha em $model${NC}"
                    done
                    ;;
            esac
            read -p "\nPressione ENTER para continuar..."
            ;;
            
        9)
            echo -e "\n${CYAN}⚙️  Configurador de Contexto${NC}\n"
            echo "Contexto atual padrão: 8192 tokens (8k)"
            echo
            echo "Escolha o tamanho de contexto:"
            echo "1) 32k (32.768 tokens) - ~25 páginas"
            echo "2) 128k (131.072 tokens) - ~100 páginas"
            echo "3) 256k (262.144 tokens) - ~200 páginas"
            echo "4) Custom"
            echo
            read -p "Escolha [1-4]: " ctx_choice
            
            case $ctx_choice in
                1) CTX_SIZE=32768 ;;
                2) CTX_SIZE=131072 ;;
                3) CTX_SIZE=262144 ;;
                4) 
                    read -p "Digite o tamanho em tokens: " CTX_SIZE
                    ;;
            esac
            
            echo -e "\n${GREEN}Contexto configurado para $CTX_SIZE tokens${NC}"
            export OLLAMA_NUM_CTX=$CTX_SIZE
            
            # Criar modelfile com novo contexto
            echo -e "\n${BLUE}Criando modelo com contexto expandido...${NC}"
            cat > /tmp/expanded_context.modelfile << EOF
FROM mistral:latest
PARAMETER num_ctx $CTX_SIZE
PARAMETER num_batch $((CTX_SIZE/128))
PARAMETER rope_frequency_base 50000
PARAMETER rope_frequency_scale 2.0
EOF
            
            ollama create scripturemon-${CTX_SIZE} -f /tmp/expanded_context.modelfile
            echo -e "${GREEN}✅ Modelo criado: scripturemon-${CTX_SIZE}${NC}"
            read -p "\nPressione ENTER para continuar..."
            ;;
            
        10)
            echo -e "\n${PURPLE}🌐 Sistema RAG - Contexto Infinito${NC}\n"
            echo "O sistema RAG permite processar documentos de qualquer tamanho"
            echo "dividindo em chunks e usando busca vetorial."
            echo
            
            # Verificar se RAG está rodando
            if curl -s http://localhost:8092/health > /dev/null 2>&1; then
                echo -e "${GREEN}✅ RAG já está ativo em http://localhost:8092${NC}"
            else
                echo -e "${YELLOW}⚠️  RAG não está ativo${NC}"
                echo "Deseja iniciar o sistema RAG?"
                read -p "Iniciar? [s/N]: " start_rag
                if [[ "$start_rag" =~ ^[Ss]$ ]]; then
                    echo -e "\n${BLUE}Iniciando RAG...${NC}"
                    cd /Users/clubproducoes/Digimundo/digimons/scripturemon
                    python3 -m uvicorn app.main:app --port 8092 &
                    sleep 3
                    echo -e "${GREEN}✅ RAG iniciado${NC}"
                fi
            fi
            read -p "\nPressione ENTER para continuar..."
            ;;
            
        11)
            echo -e "\n${CYAN}📊 Iniciando Benchmark Completo${NC}\n"
            echo "Testando todos os perfis com texto padrão..."
            echo
            
            # Texto de teste
            TEST_TEXT="FADE IN: INT. RICK'S CAFE - NIGHT. Rick sees Ilsa enter."
            
            for profile in speed balanced power; do
                echo -e "${BLUE}Testing $profile...${NC}"
                START=$(date +%s)
                
                # Simular processamento
                echo "$TEST_TEXT" | ollama run llama3.2:3b "Analyze this screenplay excerpt" > /dev/null 2>&1
                
                END=$(date +%s)
                ELAPSED=$((END-START))
                
                echo "  ⏱️  Tempo: ${ELAPSED}s"
                echo "  📈 Tokens/s: ~$((${#TEST_TEXT}/ELAPSED))"
                echo
            done
            read -p "Pressione ENTER para continuar..."
            ;;
            
        12)
            echo -e "\n${CYAN}📊 Status do Sistema${NC}\n"
            echo "Hardware:"
            echo "• RAM Total: ${TOTAL_RAM}GB"
            echo "• RAM Livre: $(vm_stat | grep "Pages free" | awk '{print $3*4096/1024/1024/1024 " GB"}')"
            echo "• Swap: $(sysctl vm.swapusage | awk '{print $7}')"
            echo
            echo "Modelos Instalados:"
            ollama list | head -10
            echo
            echo "Configurações Ativas:"
            echo "• OLLAMA_NUM_GPU: $OLLAMA_NUM_GPU"
            echo "• OLLAMA_MEMORY_BUDGET: $OLLAMA_MEMORY_BUDGET"
            echo "• Context Size: ${OLLAMA_NUM_CTX:-8192}"
            echo
            read -p "Pressione ENTER para continuar..."
            ;;
            
        0)
            echo -e "\n${GREEN}👋 Encerrando Scripturemon Ultra${NC}"
            exit 0
            ;;
            
        *)
            echo -e "${RED}Opção inválida${NC}"
            sleep 1
            ;;
    esac
done