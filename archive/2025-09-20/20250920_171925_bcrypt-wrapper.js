
// Wrapper de compatibilidade ESM/CommonJS para bcrypt
import { createRequire } from 'module'
const require = createRequire(import.meta.url)

let module
try {
  // Tentar importar como ESM
  module = await import('bcrypt')
} catch (err) {
  // Fallback para CommonJS
  module = require('bcrypt')
}

export default module
export const { hash, hashSync, compare, compareSync, genSalt, genSaltSync } = module
