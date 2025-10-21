/**
 * DIGIMUNDO PLUGIN MANAGER - MODO HACKER
 * Sistema ultra-avançado de plugins dinâmicos
 * Features: Hot-reload, Sandbox isolado, API de plugins, Marketplace
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const EventEmitter = require('events');
const chokidar = require('chokidar');
const { v4: uuidv4 } = require('uuid');

class DigimundoPluginManager extends EventEmitter {
    constructor(digimundoCore) {
        super();
        this.core = digimundoCore;
        this.plugins = new Map();
        this.pluginContexts = new Map();
        this.pluginWatchers = new Map();
        this.apiRegistry = new Map();
        this.hooks = new Map();
        this.marketplace = new Map();
        
        this.pluginsDir = path.join(__dirname, '../plugins');
        this.sandboxGlobals = this.createSandboxGlobals();
        
        this.initializePluginSystem();
    }

    createSandboxGlobals() {
        return {
            console: {
                log: (...args) => console.log('[Plugin]', ...args),
                error: (...args) => console.error('[Plugin Error]', ...args),
                warn: (...args) => console.warn('[Plugin Warning]', ...args)
            },
            require: (moduleName) => {
                // Lista branca de módulos permitidos para plugins
                const allowedModules = [
                    'path', 'crypto', 'util', 'events',
                    'uuid', 'lodash', 'moment'
                ];
                
                if (allowedModules.includes(moduleName)) {
                    return require(moduleName);
                }
                throw new Error(`Módulo não permitido no sandbox: ${moduleName}`);
            },
            Buffer,
            setTimeout,
            setInterval,
            clearTimeout,
            clearInterval,
            Promise,
            process: {
                env: { NODE_ENV: process.env.NODE_ENV },
                version: process.version
            }
        };
    }

    initializePluginSystem() {
        this.setupPluginAPI();
        this.setupHookSystem();
        this.loadAllPlugins();
        this.setupHotReload();
        this.initializeMarketplace();
        
        console.log('🔌 [MODO HACKER] Sistema de Plugins inicializado');
    }

    setupPluginAPI() {
        // Core API disponível para plugins
        this.apiRegistry.set('core', {
            // Sistema de memória
            memory: {
                store: (key, value) => this.core.memory?.store(key, value),
                retrieve: (key) => this.core.memory?.retrieve(key),
                search: (query) => this.core.memory?.search(query)
            },
            
            // Sistema de consciência
            consciousness: {
                evolve: (data) => this.core.consciousness?.evolve(data),
                getState: () => this.core.consciousness?.getState(),
                addCapability: (capability) => this.core.consciousness?.addCapability(capability)
            },
            
            // Sistema de comunicação
            communication: {
                sendMessage: (message, target) => this.core.communication?.send(message, target),
                broadcast: (message) => this.core.communication?.broadcast(message),
                onMessage: (callback) => this.core.communication?.onMessage(callback)
            },
            
            // Sistema de eventos
            events: {
                emit: (event, data) => this.emit(event, data),
                on: (event, callback) => this.on(event, callback),
                off: (event, callback) => this.removeListener(event, callback)
            },
            
            // Sistema de dados
            data: {
                save: (collection, data) => this.core.data?.save(collection, data),
                load: (collection, query) => this.core.data?.load(collection, query),
                update: (collection, id, data) => this.core.data?.update(collection, id, data),
                delete: (collection, id) => this.core.data?.delete(collection, id)
            }
        });

        // API específica para plugins
        this.apiRegistry.set('plugin', {
            registerHook: (hookName, callback) => this.registerHook(hookName, callback),
            callHook: (hookName, data) => this.callHook(hookName, data),
            registerCommand: (command, callback) => this.registerCommand(command, callback),
            registerDigimon: (digimon) => this.registerDigimon(digimon),
            createUI: (component) => this.createPluginUI(component),
            scheduleTask: (task, interval) => this.schedulePluginTask(task, interval),
            log: (message, level = 'info') => this.logPlugin(message, level)
        });
    }

    setupHookSystem() {
        // Hooks padrão do sistema
        const defaultHooks = [
            'plugin:loaded',
            'plugin:unloaded',
            'digimon:created',
            'digimon:evolved',
            'memory:stored',
            'consciousness:updated',
            'message:received',
            'command:executed',
            'ui:rendered'
        ];

        defaultHooks.forEach(hook => {
            this.hooks.set(hook, []);
        });
    }

    async loadAllPlugins() {
        try {
            if (!fs.existsSync(this.pluginsDir)) {
                fs.mkdirSync(this.pluginsDir, { recursive: true });
                console.log('📁 Diretório de plugins criado');
                return;
            }

            const pluginDirs = fs.readdirSync(this.pluginsDir, { withFileTypes: true })
                .filter(dirent => dirent.isDirectory())
                .map(dirent => dirent.name);

            for (const pluginDir of pluginDirs) {
                await this.loadPlugin(pluginDir);
            }

            console.log(`🔌 ${this.plugins.size} plugins carregados`);
        } catch (error) {
            console.error('❌ Erro ao carregar plugins:', error);
        }
    }

    async loadPlugin(pluginName) {
        try {
            const pluginPath = path.join(this.pluginsDir, pluginName);
            const manifestPath = path.join(pluginPath, 'manifest.json');
            const mainPath = path.join(pluginPath, 'index.js');

            if (!fs.existsSync(manifestPath) || !fs.existsSync(mainPath)) {
                console.warn(`⚠️ Plugin ${pluginName} incompleto (falta manifest.json ou index.js)`);
                return false;
            }

            // Carregar manifest
            const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
            
            // Validar manifest
            if (!this.validateManifest(manifest)) {
                console.error(`❌ Manifest inválido para plugin ${pluginName}`);
                return false;
            }

            // Carregar código do plugin
            const pluginCode = fs.readFileSync(mainPath, 'utf8');
            
            // Criar sandbox isolado
            const sandbox = this.createPluginSandbox(pluginName, manifest);
            
            // Executar plugin no sandbox
            const context = vm.createContext(sandbox);
            const compiledCode = vm.compileFunction(pluginCode, [], {
                filename: mainPath,
                lineOffset: 0,
                columnOffset: 0
            });

            const pluginInstance = compiledCode.call(context);

            // Registrar plugin
            const plugin = {
                id: uuidv4(),
                name: pluginName,
                manifest,
                instance: pluginInstance,
                context,
                loaded: new Date(),
                active: true
            };

            this.plugins.set(pluginName, plugin);
            this.pluginContexts.set(pluginName, context);

            // Inicializar plugin
            if (typeof pluginInstance.initialize === 'function') {
                await pluginInstance.initialize();
            }

            // Chamar hook de carregamento
            await this.callHook('plugin:loaded', plugin);

            console.log(`✅ Plugin ${pluginName} carregado com sucesso`);
            return true;

        } catch (error) {
            console.error(`❌ Erro ao carregar plugin ${pluginName}:`, error);
            return false;
        }
    }

    createPluginSandbox(pluginName, manifest) {
        const sandbox = {
            ...this.sandboxGlobals,
            
            // API específica do plugin
            digimundo: {
                ...this.apiRegistry.get('core'),
                plugin: {
                    ...this.apiRegistry.get('plugin'),
                    name: pluginName,
                    version: manifest.version,
                    config: manifest.config || {}
                }
            },

            // Utilitários globais
            global: {},
            module: { exports: {} },
            exports: {}
        };

        return sandbox;
    }

    validateManifest(manifest) {
        const required = ['name', 'version', 'description', 'author'];
        return required.every(field => manifest[field]);
    }

    async unloadPlugin(pluginName) {
        try {
            const plugin = this.plugins.get(pluginName);
            if (!plugin) return false;

            // Chamar cleanup do plugin
            if (typeof plugin.instance.cleanup === 'function') {
                await plugin.instance.cleanup();
            }

            // Remover watchers
            const watcher = this.pluginWatchers.get(pluginName);
            if (watcher) {
                await watcher.close();
                this.pluginWatchers.delete(pluginName);
            }

            // Chamar hook de descarregamento
            await this.callHook('plugin:unloaded', plugin);

            // Remover plugin
            this.plugins.delete(pluginName);
            this.pluginContexts.delete(pluginName);

            console.log(`🗑️ Plugin ${pluginName} descarregado`);
            return true;

        } catch (error) {
            console.error(`❌ Erro ao descarregar plugin ${pluginName}:`, error);
            return false;
        }
    }

    async reloadPlugin(pluginName) {
        console.log(`🔄 Recarregando plugin ${pluginName}...`);
        await this.unloadPlugin(pluginName);
        return await this.loadPlugin(pluginName);
    }

    setupHotReload() {
        const watcher = chokidar.watch(this.pluginsDir, {
            ignored: /node_modules/,
            persistent: true
        });

        watcher.on('change', async (filePath) => {
            const pluginName = this.getPluginNameFromPath(filePath);
            if (pluginName && this.plugins.has(pluginName)) {
                console.log(`🔥 Hot-reload detectado para ${pluginName}`);
                await this.reloadPlugin(pluginName);
            }
        });

        watcher.on('add', async (filePath) => {
            if (path.basename(filePath) === 'manifest.json') {
                const pluginName = this.getPluginNameFromPath(filePath);
                if (pluginName && !this.plugins.has(pluginName)) {
                    console.log(`➕ Novo plugin detectado: ${pluginName}`);
                    await this.loadPlugin(pluginName);
                }
            }
        });

        console.log('🔥 Hot-reload ativado para plugins');
    }

    getPluginNameFromPath(filePath) {
        const relativePath = path.relative(this.pluginsDir, filePath);
        return relativePath.split(path.sep)[0];
    }

    registerHook(hookName, callback) {
        if (!this.hooks.has(hookName)) {
            this.hooks.set(hookName, []);
        }
        this.hooks.get(hookName).push(callback);
    }

    async callHook(hookName, data) {
        const callbacks = this.hooks.get(hookName) || [];
        const results = [];

        for (const callback of callbacks) {
            try {
                const result = await callback(data);
                results.push(result);
            } catch (error) {
                console.error(`❌ Erro no hook ${hookName}:`, error);
            }
        }

        return results;
    }

    registerCommand(command, callback) {
        this.core.commands?.register(command, callback);
    }

    registerDigimon(digimonConfig) {
        const digimon = {
            id: uuidv4(),
            ...digimonConfig,
            source: 'plugin',
            created: new Date()
        };

        this.core.digimons?.register(digimon);
        this.callHook('digimon:created', digimon);
        
        return digimon.id;
    }

    createPluginUI(component) {
        // Criar interface de usuário para plugin
        const uiId = uuidv4();
        const ui = {
            id: uiId,
            component,
            created: new Date()
        };

        this.core.ui?.register(ui);
        return uiId;
    }

    schedulePluginTask(task, interval) {
        return setInterval(task, interval);
    }

    logPlugin(message, level = 'info') {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] [Plugin ${level.toUpperCase()}] ${message}`);
    }

    initializeMarketplace() {
        // Marketplace básico para plugins
        this.marketplace.set('featured', []);
        this.marketplace.set('installed', Array.from(this.plugins.keys()));
        this.marketplace.set('available', []);
        
        console.log('🏪 Marketplace de plugins inicializado');
    }

    // API pública
    getLoadedPlugins() {
        return Array.from(this.plugins.values()).map(plugin => ({
            name: plugin.name,
            version: plugin.manifest.version,
            description: plugin.manifest.description,
            author: plugin.manifest.author,
            loaded: plugin.loaded,
            active: plugin.active
        }));
    }

    getPluginInfo(pluginName) {
        const plugin = this.plugins.get(pluginName);
        return plugin ? {
            ...plugin.manifest,
            loaded: plugin.loaded,
            active: plugin.active
        } : null;
    }

    async installPlugin(pluginData) {
        // Implementar instalação de plugin do marketplace
        console.log('📦 Instalando plugin:', pluginData.name);
        // TODO: Implementar download e instalação
    }

    async enablePlugin(pluginName) {
        const plugin = this.plugins.get(pluginName);
        if (plugin) {
            plugin.active = true;
            if (typeof plugin.instance.enable === 'function') {
                await plugin.instance.enable();
            }
            console.log(`✅ Plugin ${pluginName} ativado`);
        }
    }

    async disablePlugin(pluginName) {
        const plugin = this.plugins.get(pluginName);
        if (plugin) {
            plugin.active = false;
            if (typeof plugin.instance.disable === 'function') {
                await plugin.instance.disable();
            }
            console.log(`⏸️ Plugin ${pluginName} desativado`);
        }
    }

    getMarketplace() {
        return {
            featured: this.marketplace.get('featured'),
            installed: this.marketplace.get('installed'),
            available: this.marketplace.get('available')
        };
    }
}

module.exports = DigimundoPluginManager;