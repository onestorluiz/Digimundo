import { execSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'

const out = path.join(process.cwd(), 'dist')
fs.rmSync(out, { recursive: true, force: true })
fs.mkdirSync(out, { recursive: true })

// console.log('[build] Empacotando via electron (modo simples).')
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

// console.log('[build] App gerado em:', path.join(out, 'mac', 'Digimundo.app'))
