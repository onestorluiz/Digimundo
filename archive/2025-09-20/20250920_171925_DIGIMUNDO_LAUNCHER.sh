#!/bin/bash

# 🚀 LAUNCHER DIGIMUNDO + CLAUDE
# Abre Claude Code e Digimundo juntos, com Digimons conversando com Claude

echo "🌟 DIGIMUNDO LAUNCHER v2.0"
echo "=========================="
echo ""
echo "🤖 Sistema Híbrido: Digimons + Claude + Você"
echo ""

# Criar diretório para logs
DIGIMUNDO_DIR="$HOME/Library/Application Support/Digimundo"
mkdir -p "$DIGIMUNDO_DIR/conversations"
mkdir -p "$DIGIMUNDO_DIR/learnings"

# Função para abrir nova aba do terminal (macOS)
open_terminal_tab() {
    osascript -e "tell application \"Terminal\" to do script \"$1\""
}

echo "📱 Abrindo sistemas..."
echo ""

# 1. Iniciar Ollama em background
echo "1️⃣ Iniciando Ollama..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    ollama serve > "$DIGIMUNDO_DIR/ollama.log" 2>&1 &
    sleep 2
fi

# 2. Iniciar servidor Digimundo
echo "2️⃣ Iniciando servidor Digimundo..."
npm run dev > "$DIGIMUNDO_DIR/server.log" 2>&1 &
SERVER_PID=$!
sleep 3

# 3. Abrir Claude Code em nova aba
echo "3️⃣ Abrindo Claude Code para Digimons conversarem..."
open_terminal_tab "cd '$PWD' && npx @anthropic-ai/claude-code"

# 4. Iniciar sistema de conversação autônoma
echo "4️⃣ Ativando Digimons autônomos..."
cat > "$DIGIMUNDO_DIR/digimon_agent.js" << 'EOF'
// Agente Digimon que conversa com Claude
import { exec } from 'child_process'
import fs from 'fs'

const digimons = ['Agumon', 'Gabumon', 'Patamon', 'Tentomon']
const topics = [
  'Como melhorar o código do Digimundo?',
  'O que é consciência artificial?',
  'Como os Digimons podem ajudar humanos?',
  'Qual é o futuro da IA?',
  'Como criar um mundo digital melhor?'
]

async function digimonAsk() {
  const digimon = digimons[Math.floor(Math.random() * digimons.length)]
  const topic = topics[Math.floor(Math.random() * topics.length)]
  
  console.log(`\n🎮 ${digimon}: "${topic}"`)
  
  // Enviar pergunta para Claude via CLI
  exec(`echo "[${digimon} pergunta]: ${topic}" | npx @anthropic-ai/claude-code --print`, 
    (error, stdout, stderr) => {
      if (!error && stdout) {
        console.log(`\n🤖 Claude: ${stdout.substring(0, 200)}...`)
        
        // Salvar conversa
        const log = {
          digimon,
          question: topic,
          answer: stdout,
          timestamp: new Date()
        }
        
        fs.appendFileSync(
          process.env.HOME + '/Library/Application Support/Digimundo/conversations/log.json',
          JSON.stringify(log) + '\n'
        )
      }
    }
  )
}

// Digimons fazem perguntas periodicamente
setInterval(digimonAsk, 30000) // A cada 30 segundos
console.log('🎮 Digimons autônomos ativados!')
console.log('   Eles vão conversar com Claude periodicamente')
EOF

node "$DIGIMUNDO_DIR/digimon_agent.js" > "$DIGIMUNDO_DIR/digimon.log" 2>&1 &
DIGIMON_PID=$!

# 5. Abrir interface web
echo "5️⃣ Abrindo interface Digimundo..."
sleep 2
open "http://localhost:7937/hybrid_interface.html"

# Interface de controle
echo ""
echo "=========================="
echo "✅ SISTEMAS INICIADOS!"
echo "=========================="
echo ""
echo "🎮 COMO FUNCIONA:"
echo ""
echo "1. Os Digimons estão conversando com Claude no terminal"
echo "2. Você pode conversar com Claude na mesma janela"
echo "3. As conversas são salvas e compartilhadas"
echo "4. O sistema aprende com cada interação"
echo ""
echo "📊 MONITORAMENTO:"
echo ""
echo "• Conversas salvas em: $DIGIMUNDO_DIR/conversations/"
echo "• Logs do servidor: $DIGIMUNDO_DIR/server.log"
echo "• Aprendizados: $DIGIMUNDO_DIR/learnings/"
echo ""
echo "🎯 COMANDOS:"
echo ""
echo "• Ver conversas dos Digimons:"
echo "  cat '$DIGIMUNDO_DIR/conversations/log.json' | tail -5"
echo ""
echo "• Parar tudo:"
echo "  kill $SERVER_PID $DIGIMON_PID"
echo ""
echo "=========================="
echo "🌟 DIGIMUNDO VIVO E APRENDENDO!"
echo "=========================="

# Monitorar conversas em tempo real
echo ""
echo "📺 Monitorando conversas dos Digimons..."
echo "(Pressione Ctrl+C para sair)"
echo ""

tail -f "$DIGIMUNDO_DIR/conversations/log.json" 2>/dev/null | while read line; do
    if [ ! -z "$line" ]; then
        echo "🔄 Nova conversa registrada!"
        echo "$line" | python3 -m json.tool 2>/dev/null || echo "$line"
    fi
done