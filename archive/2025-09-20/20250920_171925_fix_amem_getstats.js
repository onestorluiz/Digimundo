/**
 * 🔧 FIX: Adicionar verificação de segurança para getStats
 * 
 * O método getStats já existe na classe AMemSystem.
 * Este fix adiciona uma verificação de segurança nos locais que usam o método.
 */

// Arquivo: app/server/symbiotic_websocket.js
// Linha 128: const aMemStats = await aMem.getStats()
// CORREÇÃO:
const aMemStats = typeof aMem.getStats === 'function' 
  ? await aMem.getStats()
  : {
      name: 'AMemSystem',
      isActive: false,
      totalNotes: 0,
      totalConnections: 0,
      memoryHealth: 0,
      semanticIndexSize: 0,
      notes: [],
      timestamp: new Date().toISOString()
    }

// Arquivo: app/server/symbiotic_endpoints.js  
// Linha 167: const stats = await aMem.getStats()
// CORREÇÃO:
const stats = typeof aMem.getStats === 'function'
  ? await aMem.getStats()
  : {
      name: 'AMemSystem',
      isActive: false,
      totalNotes: 0,
      totalConnections: 0,
      memoryHealth: 0,
      semanticIndexSize: 0,
      notes: [],
      timestamp: new Date().toISOString()
    }