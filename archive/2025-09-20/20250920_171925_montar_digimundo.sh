#!/usr/bin/env bash
set -Eeuo pipefail

# ========= Config =========
APP_DIR="$HOME/Downloads/digimundo_starter"
PORT="${DIGI_PORT:-7937}"

# ========= Funções =========
say(){ printf "\033[1;36m[digimundo]\033[0m %s\n" "$*"; }
die(){ printf "\033[1;31m[erro]\033[0m %s\n" "$*" >&2; exit 1; }

need() { command -v "$1" >/dev/null || die "Dependência ausente: $1"; }

write() { # write <path> <<'EOF' ... EOF
  local dst="$1"; shift
  mkdir -p "$(dirname "$dst")"
  cat >"$dst"
}

# ========= Checks =========
need node
need npm
say "Criando projeto em: $APP_DIR"
rm -rf "$APP_DIR"
mkdir -p "$APP_DIR"/app/{server/tools,renderer,scripts}

# ========= package.json =========
write "$APP_DIR/package.json" <<'EOF'
{
  "name": "digimundo-starter",
  "version": "0.1.0",
  "description": "Digimundo.app starter (Electron + Node, offline-first, local LLM ready)",
  "main": "app/main.js",
  "type": "module",
  "scripts": {
    "dev": "NODE_ENV=development electron .",
    "build": "node app/scripts/build-mac.js",
    "postinstall": "node app/scripts/postinstall.js"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "electron": "^31.2.0",
    "express": "^4.19.2"
  },
  "optionalDependencies": {
    "node-llama-cpp": "^3.0.0"
  }
}
EOF

# ========= Electron main.js =========
write "$APP_DIR/app/main.js" <<'EOF'
import { app, BrowserWindow, session } from 'electron'
import path from 'node:path'
import { spawnServer } from './server/index.js'

const isDev = process.env.NODE_ENV === 'development';
const PORT = process.env.DIGI_PORT || 7937;

// single instance
if (!app.requestSingleInstanceLock()) {
  app.quit(); process.exit(0);
}

async function createWindow () {
  await spawnServer(PORT);
  const win = new BrowserWindow({
    width: 1100,
    height: 800,
    webPreferences: { preload: path.join(process.cwd(), 'app/renderer/preload.js') },
    title: 'Digimundo'
  })
  await win.loadFile(path.join(process.cwd(), 'app/renderer/index.html'))
  if (isDev) win.webContents.openDevTools({ mode: 'detach' })
}

app.whenReady().then(async () => {
  // CSP básica e conexão só pra localhost
  session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        "Content-Security-Policy": ["default-src 'self' data: blob:; connect-src 'self' http://127.0.0.1:*; img-src 'self' data:; style-src 'self' 'unsafe-inline';"]
      }
    })
  })
  await createWindow()
  app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow() })
})

app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit() })
EOF

# ========= server/index.js =========
write "$APP_DIR/app/server/index.js" <<'EOF'
import express from 'express'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { createServer } from 'node:http'
import { getModelPath, setModelPath } from './tools/config.js'
import { chatCompletionsHandler } from './openai_compat.js'
import { ONLINE } from './net.js'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const app = express()
const allowedOrigins = new Set(['null']) // Electron file:// não envia Origin

app.use(express.json({ limit: '10mb' }))
app.use((req, res, next) => {
  const origin = req.headers.origin || 'null'
  if (!allowedOrigins.has(origin)) {
    // se um dia tiver web UI externa, adiciona aqui
  }
  res.setHeader('Access-Control-Allow-Origin', origin)
  res.setHeader('Access-Control-Allow-Headers', 'content-type, authorization')
  res.setHeader('Access-Control-Expose-Headers', 'x-model,x-usage')
  next()
})
app.options('*', (req,res)=>res.sendStatus(200))

app.get('/health', (req,res)=> res.json({ ok:true, version:'0.1.0', online: ONLINE }))

app.get('/digimundo/models/list', (req,res)=> res.json({ model: getModelPath() || null }))

app.post('/digimundo/models/set', (req,res)=>{
  const p = req.body?.path
  if (!p) return res.status(400).json({ error: 'missing path' })
  try { setModelPath(p); res.json({ ok:true }) }
  catch (e) { res.status(500).json({ error: String(e) }) }
})

// endpoint OpenAI-compat mínimo
app.post('/v1/chat/completions', chatCompletionsHandler)

export async function spawnServer(port){
  return new Promise(resolve=>{
    const srv = createServer(app)
    srv.listen(port, '127.0.0.1', ()=>{
      console.log(`[digiserve] http://127.0.0.1:${port}`)
      resolve(srv)
    })
  })
}
EOF

# ========= server/net.js =========
write "$APP_DIR/app/server/net.js" <<'EOF'
export const ONLINE = process.env.DIGI_OFFLINE === '1' ? false : true

export async function offlineFetchGuard(url, opts){
  if (!ONLINE) throw new Error('Air-gapped: rede desativada (DIGI_OFFLINE=1)')
  const r = await fetch(url, opts)
  if (!r.ok) throw new Error(`HTTP ${r.status} ${url}`)
  return r
}
EOF

# ========= server/tools/config.js =========
write "$APP_DIR/app/server/tools/config.js" <<'EOF'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'

const base = path.join(os.homedir(), 'Library', 'Application Support', 'Digimundo')
const cfg = path.join(base, 'config.json')

export function ensureBase(){
  fs.mkdirSync(base, { recursive: true })
  if (!fs.existsSync(cfg)) fs.writeFileSync(cfg, JSON.stringify({ modelPath: '' }, null, 2))
}

export function getModelPath(){
  ensureBase()
  try { return JSON.parse(fs.readFileSync(cfg, 'utf-8')).modelPath || '' }
  catch { return '' }
}

export function setModelPath(p){
  ensureBase()
  const j = JSON.parse(fs.readFileSync(cfg, 'utf-8'))
  j.modelPath = p
  fs.writeFileSync(cfg, JSON.stringify(j, null, 2))
}
EOF

# ========= server/tools/config-set-model.js =========
write "$APP_DIR/app/server/tools/config-set-model.js" <<'EOF'
// uso: node app/server/tools/config-set-model.js /caminho/para/modelo.gguf
import { setModelPath } from './config.js'
const p = process.argv[2]
if (!p) {
  console.error('uso: node app/server/tools/config-set-model.js /caminho/para/modelo.gguf')
  process.exit(1)
}
setModelPath(p)
console.log('Model set ->', p)
EOF

# ========= server/openai_compat.js =========
write "$APP_DIR/app/server/openai_compat.js" <<'EOF'
import fs from 'node:fs'
let llama = null
try {
  llama = await import('node-llama-cpp') // opcional; se falhar, usamos mock
} catch (e) {
  console.warn('[llm] node-llama-cpp não disponível; usando mock para testes.')
}
import { getModelPath } from './tools/config.js'

let cached = { ctx: null, modelPath: null }

async function ensureModel(){
  const modelPath = getModelPath()
  if (!modelPath) throw new Error('Sem modelo configurado. Use /digimundo/models/set ou a UI.')
  if (!fs.existsSync(modelPath)) throw new Error('Modelo não encontrado: ' + modelPath)
  if (!llama) return { mock: true }
  if (cached.ctx && cached.modelPath === modelPath) return cached.ctx

  const { LlamaModel, LlamaContext } = llama
  const model = new LlamaModel({ modelPath })
  const context = new LlamaContext({ model, contextSize: 4096 })
  cached = { ctx: { model, context }, modelPath }
  return cached.ctx
}

export async function chatCompletionsHandler(req, res){
  try {
    const { messages, max_tokens = 256, temperature = 0.7 } = req.body || {}
    if (!Array.isArray(messages)) return res.status(400).json({ error: 'messages required' })
    const sys = messages.filter(m=>m.role==='system').map(m=>m.content).join('\n')
    const user = messages.filter(m=>m.role!=='system').map(m=>`${m.role}: ${m.content}`).join('\n')

    const ctx = await ensureModel()
    res.setHeader('x-model', getModelPath())

    if (ctx.mock) {
      const text = `[MOCK] Digimundo pronto. Você disse: ${user.slice(-200)}`
      return res.json({
        id:'mock', object:'chat.completion',
        choices:[{ index:0, message:{ role:'assistant', content:text }, finish_reason:'stop' }],
        usage:{ prompt_tokens:user.length/4|0, completion_tokens:text.length/4|0, total_tokens:0 }
      })
    }

    const { LlamaChatSession } = llama
    const session = new LlamaChatSession({ context: ctx.context, systemPrompt: sys || 'Você é o Digimundo (Scripturemon), útil e offline.' })
    const out = await session.prompt(user, { temperature, maxTokens: max_tokens })
    return res.json({
      id: 'local-1',
      object: 'chat.completion',
      choices: [{ index:0, message: { role:'assistant', content: out }, finish_reason: 'stop' }],
      usage: { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 }
    })
  } catch (e) {
    console.error(e)
    res.status(500).json({ error: String(e) })
  }
}
EOF

# ========= renderer/preload.js =========
write "$APP_DIR/app/renderer/preload.js" <<'EOF'
import { contextBridge } from 'electron'
contextBridge.exposeInMainWorld('DIGI', { apiBase: 'http://127.0.0.1:' + (process.env.DIGI_PORT || 7937) })
EOF

# ========= renderer/index.html =========
write "$APP_DIR/app/renderer/index.html" <<'EOF'
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Digimundo</title>
  <style>
    body { font-family: -apple-system, system-ui, sans-serif; margin:0; display:flex; height:100vh; }
    #side { width: 320px; border-right:1px solid #e5e5e5; padding:16px; box-sizing:border-box; }
    #chat { flex:1; display:flex; flex-direction:column; }
    #log { flex:1; padding:16px; overflow:auto; white-space:pre-wrap; }
    #input { display:flex; padding:12px; gap:8px; border-top:1px solid #e5e5e5; }
    textarea { flex:1; font-size:14px; padding:8px; }
    button { padding:8px 12px; }
    .msg { margin-bottom:12px; }
    .me { color:#444 }
    .bot { color:#0a6 }
    .small { font-size:12px; color:#777; }
  </style>
</head>
<body>
  <div id="side">
    <h3>Digimundo</h3>
    <div class="small">Servidor local: <code id="srv"></code></div>
    <hr/>
    <div>
      <strong>Modelo atual</strong>
      <div id="modelPath" class="small">—</div>
      <button id="btnPick">Escolher .gguf…</button>
    </div>
    <hr/>
    <div>
      <label><input type="checkbox" id="offline"> Offline (bloqueia rede externa)</label>
    </div>
    <p class="small">Dica: use um modelo 7–8B quantizado (Q4/Q5) para velocidade.</p>
  </div>
  <div id="chat">
    <div id="log"></div>
    <div id="input">
      <textarea id="msg" rows="2" placeholder="Fale com o Digimundo…"></textarea>
      <button id="send">Enviar</button>
    </div>
  </div>
<script>
const api = 'http://127.0.0.1:' + (process.env.DIGI_PORT || 7937);
document.getElementById('srv').textContent = api;

async function refreshModel(){
  const r = await fetch(api + '/digimundo/models/list'); const j = await r.json();
  document.getElementById('modelPath').textContent = j.model || '—';
}
refreshModel();

document.getElementById('btnPick').onclick = async () => {
  const p = prompt('Cole o caminho completo para o seu arquivo .gguf');
  if (!p) return;
  const r = await fetch(api + '/digimundo/models/set', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({ path: p })});
  if (!r.ok){ alert('Erro ao setar modelo'); return; }
  refreshModel();
}

const log = document.getElementById('log');
function append(role, text){
  const div = document.createElement('div');
  div.className = 'msg ' + (role==='user'?'me':'bot');
  div.textContent = (role==='user'?'Você: ':'Digimundo: ') + text;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

document.getElementById('send').onclick = async () => {
  const t = document.getElementById('msg'); const content = t.value.trim();
  if (!content) return;
  append('user', content); t.value='';
  try{
    const r = await fetch(api + '/v1/chat/completions', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({ messages: [{role:'user', content}] })});
    const j = await r.json();
    if (j.error) throw new Error(j.error);
    const text = j.choices?.[0]?.message?.content || JSON.stringify(j);
    append('assistant', text);
  }catch(e){
    append('assistant', 'Erro: ' + e.message);
  }
}

const offline = document.getElementById('offline');
offline.onchange = () => {
  alert('Para offline total, feche e reabra com DIGI_OFFLINE=1 (ver tutorial).');
};
</script>
</body>
</html>
EOF

# ========= scripts/bootstrap_mac.sh =========
write "$APP_DIR/app/scripts/bootstrap_mac.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "[bootstrap] Criando pastas de dados…"
BASE="$HOME/Library/Application Support/Digimundo"
mkdir -p "$BASE/models" "$BASE/workspace" "$BASE/memory" "$BASE/indices" "$BASE/logs"
echo "[bootstrap] OK: $BASE"
echo "[bootstrap] Dica: coloque um .gguf em '$BASE/models' e configure na UI ou via: node app/server/tools/config-set-model.js PATH_DO_GGUF"
EOF
chmod +x "$APP_DIR/app/scripts/bootstrap_mac.sh"

# ========= scripts/postinstall.js =========
write "$APP_DIR/app/scripts/postinstall.js" <<'EOF'
import { mkdirSync } from 'node:fs'
import os from 'node:os'
import path from 'node:path'
const base = path.join(os.homedir(), 'Library', 'Application Support', 'Digimundo')
mkdirSync(base, { recursive: true })
console.log('[postinstall] Base criada:', base)
EOF

# ========= scripts/build-mac.js =========
write "$APP_DIR/app/scripts/build-mac.js" <<'EOF'
import { execSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'

const out = path.join(process.cwd(), 'dist')
fs.rmSync(out, { recursive: true, force: true })
fs.mkdirSync(out, { recursive: true })

console.log('[build] Empacotando via electron (modo simples).')
// Copia app/ para dist/mac/Digimundo.app/Contents/Resources/app
const appRoot = path.join(out, 'mac', 'Digimundo.app', 'Contents')
fs.mkdirSync(path.join(appRoot, 'MacOS'), { recursive: true })
fs.mkdirSync(path.join(appRoot, 'Resources'), { recursive: true })

const srcDir = path.join(process.cwd(), 'app')
execSync(`rsync -a "${srcDir}/" "${appRoot}/Resources/app/"`)

// Info.plist básico
const plist = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>CFBundleName</key><string>Digimundo</string>
<key>CFBundleIdentifier</key><string>com.digimundo.app</string>
<key>CFBundleVersion</key><string>0.1.0</string>
<key>CFBundleShortVersionString</key><string>0.1.0</string>
<key>CFBundlePackageType</key><string>APPL</string>
<key>CFBundleExecutable</key><string>Digimundo</string>
<key>NSHighResolutionCapable</key><true/>
<key>NSAppTransportSecurity</key><dict><key>NSAllowsArbitraryLoads</key><true/></dict>
</dict></plist>`
fs.writeFileSync(path.join(appRoot, 'Info.plist'), plist)

// Launcher que chama o Electron com nossa app
const launcher = `#!/bin/sh
DIR="$(cd "$(dirname "$0")" && pwd)"
export NODE_ENV=production
exec "${process.execPath}" "$DIR/../Resources/app/main.js"
`
fs.writeFileSync(path.join(appRoot, 'MacOS', 'Digimundo'), launcher, { mode: 0o755 })

console.log('[build] App gerado em:', path.join(out, 'mac', 'Digimundo.app'))
EOF

# ========= Instala dependências & bootstrap =========
say "Instalando dependências (pode demorar um pouco na primeira vez)…"
(cd "$APP_DIR" && npm install)
say "Criando pastas de dados…"
bash "$APP_DIR/app/scripts/bootstrap_mac.sh"

say "Pronto. Próximos comandos:"
cat <<TXT

# 1) (Opcional) Defina o modelo .gguf:
#    mova seu .gguf p/ ~/Library/Application Support/Digimundo/models/
#    e rode:
# node "$APP_DIR/app/server/tools/config-set-model.js" "/caminho/para/seu_modelo.gguf"

# 2) Rodar em modo desenvolvimento:
cd "$APP_DIR"
npm run dev

# 3) (Opcional) Forçar air-gap (sem rede externa):
# DIGI_OFFLINE=1 npm run dev

# 4) (Opcional) Gerar Digimundo.app:
# npm run build
# open dist/mac/Digimundo.app
TXT
