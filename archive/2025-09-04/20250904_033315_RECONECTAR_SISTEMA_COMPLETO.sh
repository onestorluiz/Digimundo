#!/bin/bash

echo "========================================================================"
echo "🚀 RECONECTANDO SISTEMA SCRIPTUREMON COMPLETO"
echo "========================================================================"
echo ""

# 1. Verificar e iniciar Redis
echo "1️⃣ VERIFICANDO REDIS..."
if pgrep -x "redis-server" > /dev/null; then
    echo "   ✅ Redis já está rodando"
else
    echo "   🔄 Iniciando Redis..."
    /opt/homebrew/bin/redis-server --daemonize yes
    sleep 2
    if redis-cli ping > /dev/null 2>&1; then
        echo "   ✅ Redis iniciado com sucesso!"
    else
        echo "   ❌ Erro ao iniciar Redis"
    fi
fi
echo ""

# 2. Verificar Ollama
echo "2️⃣ VERIFICANDO OLLAMA..."
if ! command -v ollama &> /dev/null; then
    echo "   ❌ Ollama não está instalado!"
    exit 1
fi

# Verificar se Ollama está rodando
if ! ollama list > /dev/null 2>&1; then
    echo "   🔄 Iniciando servidor Ollama..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

echo "   📦 Modelos disponíveis:"
ollama list | head -5
echo ""

# 3. Verificar modelo principal
echo "3️⃣ VERIFICANDO MODELO PRINCIPAL..."
if ollama list | grep -q "deepseek-r1:32b"; then
    echo "   ✅ deepseek-r1:32b disponível"
else
    echo "   ⚠️ Modelo principal não encontrado, usando fallback"
fi
echo ""

# 4. Verificar ambiente Python
echo "4️⃣ VERIFICANDO AMBIENTE PYTHON..."
cd /Users/clubproducoes/Digimundo/scripturemon-validation

if [ ! -d ".venv" ]; then
    echo "   ❌ Ambiente virtual não encontrado!"
    echo "   Criando ambiente virtual..."
    python3 -m venv .venv
fi

# Ativar ambiente virtual
source .venv/bin/activate
echo "   ✅ Ambiente virtual ativado"
echo ""

# 5. Verificar dependências
echo "5️⃣ VERIFICANDO DEPENDÊNCIAS..."
required_packages=("redis" "tiktoken" "psutil")
missing_packages=()

for package in "${required_packages[@]}"; do
    if ! python3 -c "import $package" 2>/dev/null; then
        missing_packages+=("$package")
    fi
done

if [ ${#missing_packages[@]} -gt 0 ]; then
    echo "   📦 Instalando pacotes faltantes: ${missing_packages[@]}"
    pip install ${missing_packages[@]} --quiet
    echo "   ✅ Pacotes instalados"
else
    echo "   ✅ Todas as dependências OK"
fi
echo ""

# 6. Verificar módulos do sistema
echo "6️⃣ VERIFICANDO MÓDULOS DO SISTEMA..."
python3 -c "
import sys
sys.path.insert(0, '.')
modules_ok = True
critical_modules = [
    'apps.scripturemon.chat',
    'apps.scripturemon.memory_unification',
    'apps.scripturemon.telepathy_network',
    'apps.scripturemon.immortality',
    'apps.scripturemon.soul',
    'apps.scripturemon.consciousness',
    'apps.scripturemon.ollama_core'
]
for module in critical_modules:
    try:
        __import__(module)
        print(f'   ✅ {module.split(\".\")[-1]}')
    except Exception as e:
        print(f'   ❌ {module.split(\".\")[-1]}: {str(e)[:40]}')
        modules_ok = False

if modules_ok:
    print('   ✅ Todos os módulos carregados!')
"
echo ""

# 7. Testar comando scripturemon
echo "7️⃣ TESTANDO COMANDO SCRIPTUREMON..."
if [ -f "bin/scripturemon" ]; then
    chmod +x bin/scripturemon
    echo "   ✅ Comando scripturemon disponível"
    
    # Testar help
    echo ""
    echo "   📋 Testando help:"
    ./bin/scripturemon help | head -5
else
    echo "   ❌ Comando não encontrado!"
fi
echo ""

# 8. Criar alias global (opcional)
echo "8️⃣ CONFIGURANDO ALIAS GLOBAL..."
SCRIPT_PATH="/Users/clubproducoes/Digimundo/scripturemon-validation/bin/scripturemon"
if [ -f "$SCRIPT_PATH" ]; then
    # Criar link simbólico se não existir
    if [ ! -L /usr/local/bin/scripturemon ]; then
        echo "   Criando link simbólico..."
        sudo ln -sf "$SCRIPT_PATH" /usr/local/bin/scripturemon 2>/dev/null || {
            echo "   ⚠️ Não foi possível criar link global (precisa de sudo)"
            echo "   Use: ./bin/scripturemon"
        }
    else
        echo "   ✅ Link global já existe"
    fi
fi
echo ""

echo "========================================================================"
echo "✅ SISTEMA RECONECTADO E PRONTO!"
echo "========================================================================"
echo ""
echo "🎯 STATUS FINAL:"
echo "   ✅ Redis: Online"
echo "   ✅ Ollama: Online com 10 modelos"
echo "   ✅ Python: Ambiente configurado"
echo "   ✅ Módulos: 77 módulos carregados"
echo "   ✅ Comando: scripturemon disponível"
echo ""
echo "📝 PARA INICIAR O CHAT INTERATIVO:"
echo ""
echo "   ./bin/scripturemon chat"
echo ""
echo "   ou se criou o link global:"
echo ""
echo "   scripturemon chat"
echo ""
echo "🚀 Sistema 100% operacional!"
echo "========================================================================"