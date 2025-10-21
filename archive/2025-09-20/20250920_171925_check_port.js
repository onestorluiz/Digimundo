#!/usr/bin/env node
/**
 * Verificador de porta do Digimundo
 */

import net from 'net'

function checkPort(port) {
  return new Promise((resolve) => {
    const server = net.createServer()
    
    server.once('error', (err) => {
      if (err.code === 'EADDRINUSE') {
        console.log(`⚠️ Porta ${port} já está em uso`)
        resolve(false)
      } else {
        resolve(false)
      }
    })
    
    server.once('listening', () => {
      server.close()
      console.log(`✅ Porta ${port} está disponível`)
      resolve(true)
    })
    
    server.listen(port)
  })
}

// Verificar porta 7937
checkPort(7937).then(available => {
  if (!available) {
    console.log('Tentando encerrar processo existente...')
    process.exit(1)
  }
})
