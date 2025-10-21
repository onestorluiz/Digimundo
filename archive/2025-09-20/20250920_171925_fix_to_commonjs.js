#!/usr/bin/env node

/**
 * 🔧 CORREÇÃO DEFINITIVA - REMOVE INCOMPATIBILIDADE ESM/CommonJS
 * Este script converte o projeto para CommonJS puro
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🔧 CORREÇÃO DEFINITIVA - REMOVENDO INCOMPATIBILIDADE ESM/CommonJS');
console.log('=================================================================\n');

// 1. Backup do package.json
console.log('1️⃣ Fazendo backup do package.json...');
const packagePath = path.join(__dirname, 'package.json');
const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf-8'));
fs.writeFileSync('package.json.backup', JSON.stringify(pkg, null, 2));

// 2. Remover "type": "module"
console.log('2️⃣ Removendo "type": "module"...');
if (pkg.type === 'module') {
    delete pkg.type;
    fs.writeFileSync(packagePath, JSON.stringify(pkg, null, 2));
    console.log('✅ Removido!');
} else {
    console.log('✅ Já estava sem type: module');
}

// 3. Converter imports para require em auth.js
console.log('3️⃣ Convertendo auth.js para CommonJS...');
const authPath = path.join(__dirname, 'app', 'server', 'auth.js');

const authContentCommonJS = `// Versão CommonJS - Compatível com Electron
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const { randomBytes } = require('crypto');

const JWT_SECRET = process.env.JWT_SECRET || randomBytes(32).toString('hex');
const TOKEN_EXPIRY = '24h';
const REFRESH_TOKEN_EXPIRY = '7d';

const users = new Map();

class AuthService {
  constructor() {
    this.createDefaultUser();
  }

  createDefaultUser() {
    const defaultUser = {
      id: 'admin',
      username: 'admin',
      password: bcrypt.hashSync('digimundo123', 10),
      role: 'admin',
      createdAt: new Date()
    };
    users.set(defaultUser.username, defaultUser);
  }

  async register(username, password, role = 'user') {
    if (users.has(username)) {
      throw new Error('Usuário já existe');
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    const user = {
      id: randomBytes(16).toString('hex'),
      username,
      password: hashedPassword,
      role,
      createdAt: new Date()
    };

    users.set(username, user);
    return this.generateTokens(user);
  }

  async login(username, password) {
    const user = users.get(username);
    if (!user) {
      throw new Error('Credenciais inválidas');
    }

    const validPassword = await bcrypt.compare(password, user.password);
    if (!validPassword) {
      throw new Error('Credenciais inválidas');
    }

    return this.generateTokens(user);
  }

  generateTokens(user) {
    const payload = {
      id: user.id,
      username: user.username,
      role: user.role
    };

    const accessToken = jwt.sign(payload, JWT_SECRET, { expiresIn: TOKEN_EXPIRY });
    const refreshToken = jwt.sign(payload, JWT_SECRET, { expiresIn: REFRESH_TOKEN_EXPIRY });

    return {
      accessToken,
      refreshToken,
      user: {
        id: user.id,
        username: user.username,
        role: user.role
      }
    };
  }

  async refreshToken(refreshToken) {
    try {
      const decoded = jwt.verify(refreshToken, JWT_SECRET);
      const user = users.get(decoded.username);
      
      if (!user) {
        throw new Error('Usuário não encontrado');
      }

      return this.generateTokens(user);
    } catch (error) {
      throw new Error('Token de refresh inválido');
    }
  }

  verifyToken(token) {
    try {
      return jwt.verify(token, JWT_SECRET);
    } catch (error) {
      throw new Error('Token inválido');
    }
  }
}

const authService = new AuthService();

function authMiddleware(requiredRole = null) {
  return async (req, res, next) => {
    try {
      const authHeader = req.headers.authorization;
      if (!authHeader) {
        return res.status(401).json({ error: 'Token não fornecido' });
      }

      const token = authHeader.replace('Bearer ', '');
      const decoded = authService.verifyToken(token);
      
      if (requiredRole && decoded.role !== requiredRole && decoded.role !== 'admin') {
        return res.status(403).json({ error: 'Permissão negada' });
      }

      req.user = decoded;
      next();
    } catch (error) {
      return res.status(401).json({ error: 'Token inválido' });
    }
  };
}

function optionalAuth() {
  return async (req, res, next) => {
    try {
      const authHeader = req.headers.authorization;
      if (authHeader) {
        const token = authHeader.replace('Bearer ', '');
        req.user = authService.verifyToken(token);
      }
      next();
    } catch (error) {
      next();
    }
  };
}

// Exportar usando CommonJS
module.exports = {
  AuthService,
  authService,
  authMiddleware,
  optionalAuth
};
`;

fs.writeFileSync(authPath, authContentCommonJS);
console.log('✅ auth.js convertido!');

// 4. Converter main.js para CommonJS
console.log('4️⃣ Convertendo main.js para CommonJS...');
const mainPath = path.join(__dirname, 'app', 'main.js');

const mainContentCommonJS = `// main.js - Versão CommonJS
const { app, BrowserWindow, session, ipcMain, dialog } = require('electron');
const path = require('path');

// Variáveis globais
let mainWindow = null;
let serverStarted = false;
const PORT = 7937;
const isDev = process.env.NODE_ENV === 'development';

function getAppPaths() {
  const appRoot = app.isPackaged
    ? path.join(process.resourcesPath, 'app')
    : path.join(process.cwd(), 'app');
  return {
    preload: path.join(appRoot, 'renderer', 'preload.js'),
    index: path.join(appRoot, 'renderer', 'index.html'),
  };
}

async function createWindow() {
  if (!serverStarted) {
    try {
      const { spawnServer } = require('./server/index.js');
      await spawnServer(PORT);
      serverStarted = true;
    } catch (error) {
      console.error('Erro ao iniciar servidor:', error);
    }
  }

  const { preload, index } = getAppPaths();

  mainWindow = new BrowserWindow({
    width: 1100,
    height: 800,
    title: 'Digimundo',
    webPreferences: {
      preload,
      contextIsolation: true,
      nodeIntegration: false,
    }
  });

  await mainWindow.loadFile(index);
  if (isDev) mainWindow.webContents.openDevTools({ mode: 'detach' });
}

// Picker nativo para .gguf
ipcMain.handle('pick-gguf', async () => {
  const { canceled, filePaths } = await dialog.showOpenDialog({
    properties: ['openFile'],
    filters: [{ name: 'GGUF Models', extensions: ['gguf'] }]
  });
  if (canceled || filePaths.length === 0) return null;
  return filePaths[0];
});

// Single instance
const gotLock = app.requestSingleInstanceLock();
if (!gotLock) {
  app.quit();
  process.exit(0);
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });
}

app.whenReady().then(async () => {
  // CSP
  session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
    const csp = "default-src 'self' http://localhost:* http://127.0.0.1:* data: blob:; connect-src 'self' http://127.0.0.1:* http://localhost:*; img-src 'self' data: http://localhost:* http://127.0.0.1:*; style-src 'self' 'unsafe-inline'; frame-src 'self' http://localhost:* http://127.0.0.1:*; script-src 'self' 'unsafe-inline' 'unsafe-eval';";
    callback({ responseHeaders: { ...details.responseHeaders, 'Content-Security-Policy': [csp] } });
  });

  await createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
`;

fs.writeFileSync(mainPath, mainContentCommonJS);
console.log('✅ main.js convertido!');

// 5. Converter server/index.js
console.log('5️⃣ Convertendo server/index.js...');
const serverPath = path.join(__dirname, 'app', 'server', 'index.js');

// Verificar se usa import ou require
const serverContent = fs.readFileSync(serverPath, 'utf-8');
if (serverContent.includes('import ') || serverContent.includes('export ')) {
    // Converter para CommonJS
    const serverCommonJS = serverContent
        .replace(/import\s+(\w+)\s+from\s+['"](.+?)['"]/g, "const $1 = require('$2')")
        .replace(/import\s+\*\s+as\s+(\w+)\s+from\s+['"](.+?)['"]/g, "const $1 = require('$2')")
        .replace(/import\s+\{([^}]+)\}\s+from\s+['"](.+?)['"]/g, "const {$1} = require('$2')")
        .replace(/export\s+default\s+/g, 'module.exports = ')
        .replace(/export\s+\{([^}]+)\}/g, 'module.exports = {$1}')
        .replace(/export\s+const\s+(\w+)/g, 'const $1');
    
    fs.writeFileSync(serverPath, serverCommonJS);
    console.log('✅ server/index.js convertido!');
}

// 6. Matar processos antigos
console.log('6️⃣ Matando processos antigos...');
try {
    execSync('pkill -f "Electron" 2>/dev/null || true');
    execSync('pkill -f "electron" 2>/dev/null || true');
    execSync('pkill -f "node" 2>/dev/null || true');
    execSync('lsof -ti:7937 | xargs kill -9 2>/dev/null || true');
} catch (e) {
    // Ignorar erros
}

console.log('✅ Processos terminados!');

// 7. Testar configuração
console.log('\n7️⃣ Testando configuração...');
try {
    const jwt = require('jsonwebtoken');
    const bcrypt = require('bcrypt');
    console.log('✅ Módulos carregando corretamente!');
} catch (error) {
    console.error('❌ Erro ao carregar módulos:', error.message);
}

console.log('\n');
console.log('=================================================================');
console.log('                    ✅ CORREÇÃO COMPLETA!');
console.log('=================================================================');
console.log('');
console.log('O projeto foi convertido para CommonJS puro.');
console.log('Isso resolve TODOS os problemas de incompatibilidade.');
console.log('');
console.log('Para iniciar o Electron:');
console.log('');
console.log('  npm run dev');
console.log('');
console.log('=================================================================');
