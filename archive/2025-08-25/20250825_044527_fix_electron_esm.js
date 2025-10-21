// Fix para o problema ESM no Electron
// O electron-store agora é um módulo ES6, precisa ser importado dinamicamente

const path = require('path');
const { app } = require('electron');

// Função para carregar electron-store dinamicamente
async function loadElectronStore() {
    try {
        const { default: Store } = await import('electron-store');
        return new Store();
    } catch (error) {
        console.error('Erro ao carregar electron-store:', error);
        // Fallback para armazenamento simples
        return {
            get: (key) => null,
            set: (key, value) => {},
            delete: (key) => {}
        };
    }
}

module.exports = { loadElectronStore };
