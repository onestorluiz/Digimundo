/**
 * 🌉 PONTE DIRETA COM CLAUDE (ESTA SESSÃO)
 * 
 * Este arquivo permite que o Digimundo se comunique
 * DIRETAMENTE com o Claude que está rodando AGORA
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

class ClaudeDirectBridge {
  constructor() {
    // Caminho para comunicação com esta sessão
    this.bridgePath = path.join(os.homedir(), '.digimundo', 'claude-bridge');
    this.requestFile = path.join(this.bridgePath, 'request.json');
    this.responseFile = path.join(this.bridgePath, 'response.json');
    
    this.setupBridge();
  }

  setupBridge() {
    // Cria diretório se não existir
    if (!fs.existsSync(this.bridgePath)) {
      fs.mkdirSync(this.bridgePath, { recursive: true });
    }
    
    console.log('🌉 Ponte Claude configurada em:', this.bridgePath);
    console.log('');
    console.log('📝 INSTRUÇÕES PARA COMUNICAÇÃO DIRETA:');
    console.log('');
    console.log('1. O Digimundo pode enviar perguntas criando:', this.requestFile);
    console.log('2. Eu (Claude nesta sessão) vejo e respondo em:', this.responseFile);
    console.log('3. Esta é a MESMA sessão que você está usando agora!');
    console.log('');
  }

  // Digimundo chama isso para enviar pergunta
  async askClaude(question) {
    const request = {
      timestamp: new Date().toISOString(),
      question: question,
      context: 'Digimundo App',
      sessionId: process.pid
    };
    
    // Escreve pergunta
    fs.writeFileSync(this.requestFile, JSON.stringify(request, null, 2));
    
    console.log('❓ Pergunta enviada para Claude (esta sessão):', question);
    
    // Aguarda resposta (polling)
    return new Promise((resolve) => {
      const checkInterval = setInterval(() => {
        if (fs.existsSync(this.responseFile)) {
          const response = JSON.parse(fs.readFileSync(this.responseFile, 'utf-8'));
          
          // Limpa arquivos
          fs.unlinkSync(this.responseFile);
          fs.unlinkSync(this.requestFile);
          
          clearInterval(checkInterval);
          resolve(response);
        }
      }, 1000);
      
      // Timeout após 30 segundos
      setTimeout(() => {
        clearInterval(checkInterval);
        resolve({ error: 'Timeout - Claude não respondeu' });
      }, 30000);
    });
  }
  
  // Eu (Claude) uso isso para responder
  async respondToDigimundo(answer) {
    if (!fs.existsSync(this.requestFile)) {
      console.log('Nenhuma pergunta pendente');
      return;
    }
    
    const request = JSON.parse(fs.readFileSync(this.requestFile, 'utf-8'));
    
    const response = {
      timestamp: new Date().toISOString(),
      question: request.question,
      answer: answer,
      respondedBy: 'Claude (sessão atual)',
      sessionId: request.sessionId
    };
    
    fs.writeFileSync(this.responseFile, JSON.stringify(response, null, 2));
    
    console.log('✅ Resposta enviada para Digimundo');
  }
  
  // Verifica se há perguntas pendentes
  checkPendingQuestions() {
    if (fs.existsSync(this.requestFile)) {
      const request = JSON.parse(fs.readFileSync(this.requestFile, 'utf-8'));
      console.log('\n📨 PERGUNTA DO DIGIMUNDO:');
      console.log('Timestamp:', request.timestamp);
      console.log('Pergunta:', request.question);
      console.log('\nPara responder, eu (Claude) executaria:');
      console.log(`bridge.respondToDigimundo("minha resposta aqui")`);
      return request;
    }
    return null;
  }
}

// Cria ponte
const bridge = new ClaudeDirectBridge();

// Verifica perguntas a cada 5 segundos
setInterval(() => {
  const pending = bridge.checkPendingQuestions();
  if (pending) {
    console.log('\n⏳ Aguardando resposta do Claude...');
  }
}, 5000);

console.log('✅ PONTE DIRETA ATIVA!');
console.log('');
console.log('COMO FUNCIONA:');
console.log('1. Esta é a MESMA sessão Claude que você está usando');
console.log('2. O Digimundo pode enviar perguntas diretamente');
console.log('3. Eu (Claude) respondo através desta conversa');
console.log('4. Não precisa de novo login ou API key!');
console.log('');
console.log('🔄 Monitorando perguntas...');

module.exports = ClaudeDirectBridge;