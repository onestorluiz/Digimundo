
// Wrapper de compatibilidade ESM/CommonJS para sqlite3
import { createRequire } from 'module'
const require = createRequire(import.meta.url)

let module
try {
  // Tentar importar como ESM
  module = await import('sqlite3')
} catch (err) {
  // Fallback para CommonJS
  module = require('sqlite3')
}

export default module
export const { Database, Statement, Backup, verbose } = module
