// Wrapper de compatibilidade para SQLite
// Usa sqlite3 ou better-sqlite3 como fallback

import { createRequire } from 'module'
const require = createRequire(import.meta.url)

let sqliteModule = null
let moduleType = null

// Tentar carregar sqlite3 primeiro
try {
  sqliteModule = require('sqlite3')
  moduleType = 'sqlite3'
  console.log('✅ Usando sqlite3')
} catch (err1) {
  console.log('⚠️ sqlite3 não disponível, tentando better-sqlite3...')
  
  // Tentar better-sqlite3 como fallback
  try {
    const BetterSqlite3 = require('better-sqlite3')
    
    // Criar wrapper de compatibilidade para better-sqlite3
    sqliteModule = {
      Database: class {
        constructor(filename, callback) {
          try {
            this.db = new BetterSqlite3(filename)
            if (callback) callback(null)
          } catch (err) {
            if (callback) callback(err)
          }
        }
        
        run(sql, params, callback) {
          try {
            const stmt = this.db.prepare(sql)
            const result = stmt.run(params || [])
            if (callback) callback(null, result)
            return this
          } catch (err) {
            if (callback) callback(err)
            return this
          }
        }
        
        get(sql, params, callback) {
          try {
            const stmt = this.db.prepare(sql)
            const result = stmt.get(params || [])
            if (callback) callback(null, result)
            return this
          } catch (err) {
            if (callback) callback(err)
            return this
          }
        }
        
        all(sql, params, callback) {
          try {
            const stmt = this.db.prepare(sql)
            const result = stmt.all(params || [])
            if (callback) callback(null, result)
            return this
          } catch (err) {
            if (callback) callback(err)
            return this
          }
        }
        
        close(callback) {
          try {
            this.db.close()
            if (callback) callback(null)
          } catch (err) {
            if (callback) callback(err)
          }
        }
        
        serialize(callback) {
          // better-sqlite3 é sempre serializado
          if (callback) callback()
          return this
        }
      },
      
      verbose: () => sqliteModule
    }
    
    moduleType = 'better-sqlite3'
    console.log('✅ Usando better-sqlite3 com wrapper de compatibilidade')
  } catch (err2) {
    console.error('❌ Nenhum driver SQLite disponível!')
    console.error('Instale sqlite3 ou better-sqlite3')
    
    // Criar um mock vazio para não quebrar a aplicação
    sqliteModule = {
      Database: class {
        constructor(filename, callback) {
          console.error('SQLite não está instalado!')
          if (callback) callback(new Error('SQLite não disponível'))
        }
        run() { return this }
        get() { return this }
        all() { return this }
        close() { return this }
        serialize() { return this }
      },
      verbose: () => sqliteModule
    }
  }
}

// Exportar o módulo (seja sqlite3, better-sqlite3 com wrapper, ou mock)
export default sqliteModule
export const { Database } = sqliteModule

// Informação sobre qual módulo está sendo usado
export const sqliteInfo = {
  module: moduleType,
  available: moduleType !== null
}
