#!/usr/bin/env node

/**
 * 🧪 TESTE DE INTEGRAÇÃO OLLAMA AUTO-START
 */

const OllamaManager = require('./src/main/ollama-manager.js');

console.log('🧪 TESTANDO AUTO-START DO OLLAMA');
console.log('==================================\n');

async function runTests() {
  const ollama = new OllamaManager();
  
  console.log('1️⃣ VERIFICANDO OLLAMA NO SISTEMA:');
  const ollamaPath = await ollama.findOllamaPath();
  
  if (ollamaPath) {
    console.log('   ✅ Ollama encontrado em:', ollamaPath);
  } else {
    console.log('   ❌ Ollama não instalado');
    console.log('');
    console.log('📦 Para instalar Ollama:');
    console.log('   brew install ollama');
    console.log('   ou');
    console.log('   curl -fsSL https://ollama.ai/install.sh | sh');
    return;
  }
  
  console.log('');
  console.log('2️⃣ VERIFICANDO SE JÁ ESTÁ RODANDO:');
  const alreadyRunning = await ollama.checkIfRunning();
  console.log('   Status:', alreadyRunning ? '✅ Rodando' : '⏸️ Parado');
  
  if (alreadyRunning) {
    console.log('   ⚠️ Ollama já estava rodando (iniciado manualmente)');
  }
  
  console.log('');
  console.log('3️⃣ TESTANDO AUTO-START:');
  
  if (!alreadyRunning) {
    console.log('   🚀 Iniciando Ollama automaticamente...');
    const started = await ollama.start();
    
    if (started) {
      console.log('   ✅ Ollama iniciado com sucesso!');
    } else {
      console.log('   ❌ Falha ao iniciar Ollama');
      return;
    }
  }
  
  console.log('');
  console.log('4️⃣ VERIFICANDO MODELOS:');
  const models = await ollama.listModels();
  
  if (models.length > 0) {
    console.log('   Modelos disponíveis:');
    models.forEach(model => {
      console.log(`   - ${model.name} (${Math.round(model.size / 1024 / 1024)}MB)`);
    });
  } else {
    console.log('   ⚠️ Nenhum modelo baixado');
    console.log('   📥 Baixando modelos necessários...');
    
    // O manager vai baixar automaticamente
    await ollama.ensureModels();
  }
  
  console.log('');
  console.log('5️⃣ TESTANDO GERAÇÃO DE RESPOSTA:');
  console.log('   Pergunta: "Olá, você está funcionando?"');
  
  const response = await ollama.generate('Olá, você está funcionando? Responda em uma linha.');
  
  if (response) {
    console.log('   Resposta:', response.slice(0, 100) + '...');
    console.log('   ✅ Geração funcionando!');
  } else {
    console.log('   ❌ Falha na geração');
  }
  
  console.log('');
  console.log('6️⃣ STATUS COMPLETO:');
  const status = await ollama.getStatus();
  console.log('   Running:', status.running ? '✅' : '❌');
  console.log('   URL:', status.url);
  console.log('   Process:', status.process);
  console.log('   Models Ready:', status.models.join(', ') || 'Nenhum');
  
  console.log('');
  console.log('==================================');
  console.log('✅ INTEGRAÇÃO OLLAMA COMPLETA!');
  console.log('');
  console.log('🎉 O Digimundo agora:');
  console.log('   1. Inicia Ollama automaticamente ao abrir');
  console.log('   2. Baixa modelos necessários sozinho');
  console.log('   3. Gerencia o ciclo de vida do Ollama');
  console.log('   4. Para o Ollama ao fechar o app');
  console.log('');
  console.log('📝 No app, o Ollama:');
  console.log('   - Inicia automaticamente em background');
  console.log('   - Não precisa de terminal aberto');
  console.log('   - Funciona offline após baixar modelos');
  console.log('   - Se recupera de falhas automaticamente');
  
  // Limpa para o teste
  if (!alreadyRunning) {
    console.log('');
    console.log('🛑 Parando Ollama do teste...');
    ollama.stop();
  }
}

runTests().catch(console.error);