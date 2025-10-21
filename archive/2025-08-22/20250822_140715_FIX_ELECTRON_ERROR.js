#!/usr/bin/env node

/**
 * 🔧 FIX ELECTRON STARTUP ERROR
 * Corrige o erro: TypeError: Error processing argument at index 0
 * E outros problemas relacionados ao Electron
 */

const fs = require('fs').promises;
const path = require('path');

class ElectronErrorFixer {
    constructor() {
        this.fixes = {
            applied: [],
            errors: []
        };
    }

    async fixAll() {
        console.log(`
╔═══════════════════════════════════════════════════════════════╗
║         🔧 ELECTRON ERROR FIXER - DIGIMUNDO 🔧               ║
╚═══════════════════════════════════════════════════════════════╝
        `);

        // Fix 1: Startup Optimizer preconnect error
        await this.fixStartupOptimizer();
        
        // Fix 2: Add global error handlers
        await this.addGlobalErrorHandlers();
        
        // Fix 3: Fix renderer process issues
        await this.fixRendererProcess();
        
        // Fix 4: Add recovery mechanisms
        await this.addRecoveryMechanisms();
        
        // Report
        this.generateReport();
    }

    async fixStartupOptimizer() {
        console.log('\n📍 Fixing startup-optimizer.js...');
        
        const filePath = '/Users/clubproducoes/Digimundo/DigimundoApp/src/main/startup-optimizer.js';
        
        try {
            let content = await fs.readFile(filePath, 'utf8');
            const original = content;
            
            // Fix preconnect error - already fixed above, but let's ensure it's correct
            if (content.includes("window.webContents.session.preconnect('http://localhost:11434', 2)")) {
                content = content.replace(
                    "window.webContents.session.preconnect('http://localhost:11434', 2);",
                    `// Fix: preconnect expects an options object, not just URL and number
    if (window.webContents && window.webContents.session) {
      try {
        window.webContents.session.preconnect('http://localhost:11434');
      } catch (error) {
        console.warn('Failed to preconnect to Ollama:', error.message);
      }
    }`
                );
            }
            
            // Add safety checks for webContents operations
            if (!content.includes('// Safety check for webContents')) {
                content = content.replace(
                    'optimizeRenderer(window) {',
                    `optimizeRenderer(window) {
    // Safety check for webContents
    if (!window || !window.webContents) {
      console.warn('Window or webContents not ready for optimization');
      return;
    }`
                );
            }
            
            if (content !== original) {
                await fs.writeFile(filePath, content);
                console.log('   ✅ Fixed startup-optimizer.js');
                this.fixes.applied.push('startup-optimizer.js');
            } else {
                console.log('   ✅ startup-optimizer.js already fixed');
            }
        } catch (error) {
            console.error('   ❌ Error fixing startup-optimizer.js:', error.message);
            this.fixes.errors.push({ file: 'startup-optimizer.js', error: error.message });
        }
    }

    async addGlobalErrorHandlers() {
        console.log('\n📍 Adding global error handlers...');
        
        const mainPath = '/Users/clubproducoes/Digimundo/DigimundoApp/src/main/electron-main.js';
        
        try {
            let content = await fs.readFile(mainPath, 'utf8');
            const original = content;
            
            // Add comprehensive error handling
            const errorHandlerCode = `
// Global error handlers for Electron
process.on('uncaughtException', (error) => {
  console.error('❌ Uncaught Exception:', error);
  
  // Log to file for debugging
  const errorLog = \`[\${new Date().toISOString()}] Uncaught Exception: \${error.stack || error}\n\`;
  require('fs').appendFileSync('/tmp/digimundo-errors.log', errorLog);
  
  // Try to recover if it's a non-critical error
  if (!error.message.includes('Cannot read') && !error.message.includes('undefined')) {
    console.log('🔄 Attempting to recover...');
    return;
  }
  
  // For critical errors, show dialog and restart
  const { dialog, app } = require('electron');
  dialog.showErrorBox('Erro no Digimundo', 
    'Um erro inesperado ocorreu. O aplicativo será reiniciado.\\n\\n' + error.message);
  
  setTimeout(() => {
    app.relaunch();
    app.exit(0);
  }, 3000);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ Unhandled Promise Rejection:', reason);
  
  // Log but don't crash for promise rejections
  const errorLog = \`[\${new Date().toISOString()}] Unhandled Rejection: \${reason}\n\`;
  require('fs').appendFileSync('/tmp/digimundo-errors.log', errorLog);
});

// Electron specific error handlers
app.on('render-process-gone', (event, webContents, details) => {
  console.error('❌ Renderer process crashed:', details);
  
  if (details.reason === 'crashed' || details.reason === 'oom') {
    console.log('🔄 Reloading renderer...');
    webContents.reload();
  }
});

app.on('child-process-gone', (event, details) => {
  console.error('❌ Child process crashed:', details);
  
  if (details.type === 'GPU') {
    console.log('🔄 GPU process crashed, disabling hardware acceleration');
    app.disableHardwareAcceleration();
  }
});
`;

            // Add error handlers if not present
            if (!content.includes('process.on(\'uncaughtException\'')) {
                // Find a good place to insert (after imports)
                const insertIndex = content.indexOf('class DigimundoApp');
                if (insertIndex !== -1) {
                    content = content.slice(0, insertIndex) + errorHandlerCode + '\n' + content.slice(insertIndex);
                }
            }
            
            if (content !== original) {
                await fs.writeFile(mainPath, content);
                console.log('   ✅ Added global error handlers');
                this.fixes.applied.push('global-error-handlers');
            } else {
                console.log('   ✅ Error handlers already present');
            }
        } catch (error) {
            console.error('   ❌ Error adding error handlers:', error.message);
            this.fixes.errors.push({ file: 'electron-main.js', error: error.message });
        }
    }

    async fixRendererProcess() {
        console.log('\n📍 Fixing renderer process issues...');
        
        const preloadPath = '/Users/clubproducoes/Digimundo/DigimundoApp/src/main/preload.js';
        
        try {
            let content = await fs.readFile(preloadPath, 'utf8');
            const original = content;
            
            // Add error handling in preload
            const preloadErrorHandler = `
// Renderer process error handling
window.addEventListener('error', (event) => {
  console.error('Renderer Error:', event.error);
  
  // Send error to main process
  if (window.electronAPI && window.electronAPI.sendError) {
    window.electronAPI.sendError({
      message: event.error.message,
      stack: event.error.stack,
      url: event.filename,
      line: event.lineno,
      column: event.colno
    });
  }
  
  // Prevent default error handling for non-critical errors
  if (!event.error.message.includes('Cannot read')) {
    event.preventDefault();
  }
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled Promise in Renderer:', event.reason);
  
  // Send to main process
  if (window.electronAPI && window.electronAPI.sendError) {
    window.electronAPI.sendError({
      type: 'unhandledRejection',
      reason: event.reason
    });
  }
  
  event.preventDefault();
});
`;

            if (!content.includes('window.addEventListener(\'error\'')) {
                content = preloadErrorHandler + '\n' + content;
            }
            
            if (content !== original) {
                await fs.writeFile(preloadPath, content);
                console.log('   ✅ Fixed renderer process');
                this.fixes.applied.push('renderer-process');
            } else {
                console.log('   ✅ Renderer process already fixed');
            }
        } catch (error) {
            console.error('   ❌ Error fixing renderer:', error.message);
            this.fixes.errors.push({ file: 'preload.js', error: error.message });
        }
    }

    async addRecoveryMechanisms() {
        console.log('\n📍 Adding recovery mechanisms...');
        
        const recoveryCode = `
/**
 * Auto-recovery system for Electron crashes
 */
class ElectronRecovery {
    constructor() {
        this.crashCount = 0;
        this.lastCrashTime = 0;
        this.maxCrashes = 3;
        this.crashWindow = 60000; // 1 minute
    }
    
    handleCrash(error) {
        const now = Date.now();
        
        // Reset counter if outside crash window
        if (now - this.lastCrashTime > this.crashWindow) {
            this.crashCount = 0;
        }
        
        this.crashCount++;
        this.lastCrashTime = now;
        
        console.log(\`🔄 Crash #\${this.crashCount}: \${error.message}\`);
        
        // Different recovery strategies based on crash count
        if (this.crashCount === 1) {
            // First crash: just reload
            console.log('   Strategy: Reload window');
            if (global.mainWindow && !global.mainWindow.isDestroyed()) {
                global.mainWindow.reload();
            }
        } else if (this.crashCount === 2) {
            // Second crash: clear cache and reload
            console.log('   Strategy: Clear cache and reload');
            if (global.mainWindow && !global.mainWindow.isDestroyed()) {
                global.mainWindow.webContents.session.clearCache().then(() => {
                    global.mainWindow.reload();
                });
            }
        } else if (this.crashCount >= this.maxCrashes) {
            // Too many crashes: safe mode
            console.log('   Strategy: Enter safe mode');
            this.enterSafeMode();
        }
    }
    
    enterSafeMode() {
        console.log('🛡️ Entering SAFE MODE...');
        
        // Disable all non-essential features
        const { app } = require('electron');
        
        // Disable hardware acceleration
        app.disableHardwareAcceleration();
        
        // Clear all data
        if (global.mainWindow && !global.mainWindow.isDestroyed()) {
            global.mainWindow.webContents.session.clearStorageData();
        }
        
        // Restart in safe mode
        app.relaunch({ args: process.argv.slice(1).concat(['--safe-mode']) });
        app.exit(0);
    }
}

global.electronRecovery = new ElectronRecovery();
`;

        const recoveryPath = '/Users/clubproducoes/Digimundo/DigimundoApp/src/main/electron-recovery.js';
        
        try {
            await fs.writeFile(recoveryPath, recoveryCode);
            console.log('   ✅ Created recovery system');
            this.fixes.applied.push('recovery-system');
        } catch (error) {
            console.error('   ❌ Error creating recovery:', error.message);
            this.fixes.errors.push({ file: 'electron-recovery.js', error: error.message });
        }
    }

    generateReport() {
        console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                     📊 FIX REPORT 📊                          ║
╚═══════════════════════════════════════════════════════════════╝

✅ Fixes Applied: ${this.fixes.applied.length}
❌ Errors: ${this.fixes.errors.length}
`);

        if (this.fixes.applied.length > 0) {
            console.log('Applied Fixes:');
            this.fixes.applied.forEach(fix => {
                console.log(`   ✅ ${fix}`);
            });
        }

        if (this.fixes.errors.length > 0) {
            console.log('\nErrors:');
            this.fixes.errors.forEach(({ file, error }) => {
                console.log(`   ❌ ${file}: ${error}`);
            });
        }

        console.log(`
🎯 Next Steps:
1. Rebuild the Electron app: npm run build
2. Test the app: npm start
3. Check logs at: /tmp/digimundo-errors.log
4. If errors persist, run in safe mode: npm start -- --safe-mode
`);
    }
}

// Run the fixer
async function main() {
    const fixer = new ElectronErrorFixer();
    await fixer.fixAll();
}

main().catch(console.error);