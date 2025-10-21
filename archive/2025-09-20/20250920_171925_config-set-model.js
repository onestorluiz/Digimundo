// uso: node app/server/tools/config-set-model.js /caminho/para/modelo.gguf
import { setModelPath } from './config.js'
const p = process.argv[2]
if (!p) {
  console.error('uso: node app/server/tools/config-set-model.js /caminho/para/modelo.gguf')
  process.exit(1)
}
setModelPath(p)
// console.log('Model set ->', p)
