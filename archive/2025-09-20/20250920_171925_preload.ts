import { contextBridge, ipcRenderer } from 'electron';

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('api', {
  // Store
  store: {
    get: (key: string) => ipcRenderer.invoke('store:get', key),
    set: (key: string, value: any) => ipcRenderer.invoke('store:set', key, value),
    delete: (key: string) => ipcRenderer.invoke('store:delete', key)
  },

  // Window
  window: {
    minimize: () => ipcRenderer.invoke('window:minimize'),
    maximize: () => ipcRenderer.invoke('window:maximize'),
    close: () => ipcRenderer.invoke('window:close')
  },

  // App
  app: {
    version: () => ipcRenderer.invoke('app:version'),
    name: () => ipcRenderer.invoke('app:name')
  },

  // Ollama
  ollama: {
    check: () => ipcRenderer.invoke('ollama:check'),
    models: () => ipcRenderer.invoke('ollama:models'),
    generate: (prompt: string, model?: string) => 
      ipcRenderer.invoke('ollama:generate', prompt, model)
  },

  // Events
  on: (channel: string, callback: Function) => {
    const validChannels = [
      'new-conversation',
      'save-conversation',
      'export-conversation',
      'open-preferences',
      'toggle-theme'
    ];
    
    if (validChannels.includes(channel)) {
      ipcRenderer.on(channel, (_, ...args) => callback(...args));
    }
  },

  removeAllListeners: (channel: string) => {
    ipcRenderer.removeAllListeners(channel);
  }
});

// Types for TypeScript
export interface IElectronAPI {
  store: {
    get: (key: string) => Promise<any>;
    set: (key: string, value: any) => Promise<void>;
    delete: (key: string) => Promise<void>;
  };
  window: {
    minimize: () => Promise<void>;
    maximize: () => Promise<void>;
    close: () => Promise<void>;
  };
  app: {
    version: () => Promise<string>;
    name: () => Promise<string>;
  };
  ollama: {
    check: () => Promise<boolean>;
    models: () => Promise<any[]>;
    generate: (prompt: string, model?: string) => Promise<string | null>;
  };
  on: (channel: string, callback: Function) => void;
  removeAllListeners: (channel: string) => void;
}

declare global {
  interface Window {
    api: IElectronAPI;
  }
}