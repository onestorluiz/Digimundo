import { mkdirSync } from 'node:fs'
import os from 'node:os'
import path from 'node:path'
const base = path.join(os.homedir(), 'Library', 'Application Support', 'Digimundo')
mkdirSync(base, { recursive: true })
// console.log('[postinstall] Base criada:', base)
