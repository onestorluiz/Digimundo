
// Wrapper de compatibilidade ESM/CommonJS para jsonwebtoken
import { createRequire } from 'module'
const require = createRequire(import.meta.url)

let module
try {
  // Tentar importar como ESM
  module = await import('jsonwebtoken')
} catch (err) {
  // Fallback para CommonJS
  module = require('jsonwebtoken')
}

export default module
export const { sign, verify, decode } = module
