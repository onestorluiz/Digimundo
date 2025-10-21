/**
 * DIGIMUNDO CINEMA PRODUCTION TOOLS - MODO HACKER
 * Ferramentas ultra-avançadas para produção cinematográfica
 * Features: Final Draft XML, DaVinci Resolve API, Budget Calculator, Schedule Generator
 */

const EventEmitter = require('events');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs').promises;
const path = require('path');
const xml2js = require('xml2js');

class DigimundoCinemaTools extends EventEmitter {
    constructor(digimundoCore) {
        super();
        this.core = digimundoCore;
        this.projects = new Map();
        this.templates = new Map();
        this.exportQueue = [];
        
        this.setupCinemaTools();
        this.loadTemplates();
    }

    setupCinemaTools() {
        console.log('🎬 [MODO HACKER] Cinema Production Tools inicializados');
    }

    async loadTemplates() {
        // Templates para diferentes tipos de produção
        this.templates.set('feature-film', {
            name: 'Longa Metragem',
            defaultBudget: {
                preProduction: 0.15,
                production: 0.65,
                postProduction: 0.20
            },
            scheduleTemplate: 'standard-feature',
            exportFormats: ['final-draft', 'fountain', 'pdf']
        });

        this.templates.set('short-film', {
            name: 'Curta Metragem',
            defaultBudget: {
                preProduction: 0.10,
                production: 0.70,
                postProduction: 0.20
            },
            scheduleTemplate: 'short-film',
            exportFormats: ['final-draft', 'fountain', 'pdf']
        });

        this.templates.set('documentary', {
            name: 'Documentário',
            defaultBudget: {
                preProduction: 0.20,
                production: 0.50,
                postProduction: 0.30
            },
            scheduleTemplate: 'documentary',
            exportFormats: ['final-draft', 'documentary-format']
        });

        console.log('📋 [Cinema Tools] Templates carregados');
    }

    // FINAL DRAFT XML EXPORT
    async exportToFinalDraft(projectId, options = {}) {
        try {
            const project = await this.getProject(projectId);
            if (!project) {
                throw new Error('Projeto não encontrado');
            }

            console.log(`📝 [Final Draft] Iniciando exportação: ${project.title}`);

            const finalDraftXML = await this.generateFinalDraftXML(project, options);
            
            const filename = `${this.sanitizeFilename(project.title)}_${Date.now()}.fdx`;
            const filePath = await this.saveExport(finalDraftXML, filename, 'final-draft');

            const exportData = {
                id: uuidv4(),
                projectId,
                type: 'final-draft',
                filename,
                filePath,
                options,
                createdAt: new Date().toISOString(),
                metadata: {
                    pageCount: this.calculatePageCount(project),
                    sceneCount: project.scenes?.length || 0,
                    characterCount: this.getUniqueCharacters(project).length
                }
            };

            this.emit('export-completed', exportData);
            console.log(`✅ [Final Draft] Exportação concluída: ${filename}`);

            return exportData;

        } catch (error) {
            console.error('❌ [Final Draft] Erro na exportação:', error);
            throw error;
        }
    }

    async generateFinalDraftXML(project, options = {}) {
        const scenes = project.scenes || [];
        const characters = this.getUniqueCharacters(project);
        
        // Estrutura base do Final Draft XML
        const fdxStructure = {
            FinalDraft: {
                $: {
                    DocumentType: 'Script',
                    Template: 'No',
                    Version: '3'
                },
                Content: [{
                    Paragraph: []
                }],
                TitlePage: [{
                    Content: [{
                        Paragraph: [
                            {
                                $: { Alignment: 'Center' },
                                Text: [{ _: project.title.toUpperCase() }]
                            },
                            {
                                $: { Alignment: 'Center' },
                                Text: [{ _: `por ${project.author || 'Autor'}` }]
                            }
                        ]
                    }]
                }],
                ElementSettings: [{
                    CharacterNameList: [{
                        CharacterName: characters.map(char => ({
                            $: { Name: char.name }
                        }))
                    }],
                    SceneIntroList: [{
                        SceneIntro: [
                            { $: { Name: 'FADE IN:' } },
                            { $: { Name: 'FADE OUT:' } },
                            { $: { Name: 'CUT TO:' } }
                        ]
                    }]
                }]
            }
        };

        // Adicionar cenas
        for (const scene of scenes) {
            await this.addSceneToFDX(fdxStructure, scene, options);
        }

        // Converter para XML
        const builder = new xml2js.Builder({
            xmldec: { version: '1.0', encoding: 'UTF-8' },
            rootName: 'FinalDraft'
        });

        return builder.buildObject(fdxStructure);
    }

    async addSceneToFDX(fdxStructure, scene, options) {
        const content = fdxStructure.FinalDraft.Content[0];
        
        // Scene heading
        content.Paragraph.push({
            $: { Type: 'Scene Heading' },
            Text: [{ _: this.formatSceneHeading(scene) }]
        });

        // Action lines
        if (scene.description) {
            const actionLines = scene.description.split('\n');
            actionLines.forEach(line => {
                if (line.trim()) {
                    content.Paragraph.push({
                        $: { Type: 'Action' },
                        Text: [{ _: line.trim() }]
                    });
                }
            });
        }

        // Dialogue
        if (scene.dialogue && scene.dialogue.length > 0) {
            for (const dialogueLine of scene.dialogue) {
                // Character name
                content.Paragraph.push({
                    $: { Type: 'Character' },
                    Text: [{ _: dialogueLine.character?.name?.toUpperCase() || 'CHARACTER' }]
                });

                // Parenthetical (if any)
                if (dialogueLine.direction) {
                    content.Paragraph.push({
                        $: { Type: 'Parenthetical' },
                        Text: [{ _: `(${dialogueLine.direction})` }]
                    });
                }

                // Dialogue text
                const dialogueLines = dialogueLine.content.split('\n');
                dialogueLines.forEach(line => {
                    if (line.trim()) {
                        content.Paragraph.push({
                            $: { Type: 'Dialogue' },
                            Text: [{ _: line.trim() }]
                        });
                    }
                });
            }
        }

        // Scene transition
        if (scene.transition) {
            content.Paragraph.push({
                $: { Type: 'Transition' },
                Text: [{ _: scene.transition.toUpperCase() }]
            });
        }
    }

    formatSceneHeading(scene) {
        const location = scene.location || 'LOCATION';
        const timeOfDay = scene.timeOfDay || 'DAY';
        const intExt = scene.setting || 'INT.';
        
        return `${intExt} ${location} - ${timeOfDay}`;
    }

    // DAVINCI RESOLVE INTEGRATION
    async exportToDaVinciResolve(projectId, options = {}) {
        try {
            const project = await this.getProject(projectId);
            if (!project) {
                throw new Error('Projeto não encontrado');
            }

            console.log(`🎨 [DaVinci Resolve] Iniciando integração: ${project.title}`);

            // Gerar arquivo de projeto DaVinci Resolve
            const resolveProject = await this.generateDaVinciProject(project, options);
            
            // Gerar EDL (Edit Decision List)
            const edl = await this.generateEDL(project, options);
            
            // Gerar XML de timeline
            const timelineXML = await this.generateTimelineXML(project, options);

            const exportData = {
                id: uuidv4(),
                projectId,
                type: 'davinci-resolve',
                files: {
                    project: await this.saveExport(resolveProject, `${this.sanitizeFilename(project.title)}.drp`, 'davinci'),
                    edl: await this.saveExport(edl, `${this.sanitizeFilename(project.title)}.edl`, 'davinci'),
                    timeline: await this.saveExport(timelineXML, `${this.sanitizeFilename(project.title)}_timeline.xml`, 'davinci')
                },
                options,
                createdAt: new Date().toISOString(),
                metadata: {
                    sceneCount: project.scenes?.length || 0,
                    estimatedDuration: this.calculateEstimatedDuration(project),
                    shotCount: this.calculateShotCount(project)
                }
            };

            this.emit('export-completed', exportData);
            console.log(`✅ [DaVinci Resolve] Integração concluída`);

            return exportData;

        } catch (error) {
            console.error('❌ [DaVinci Resolve] Erro na integração:', error);
            throw error;
        }
    }

    async generateDaVinciProject(project, options) {
        // Estrutura básica de projeto DaVinci Resolve
        const resolveProject = {
            project: {
                name: project.title,
                description: project.description || '',
                frameRate: options.frameRate || '24',
                resolution: options.resolution || '1920x1080',
                colorSpace: options.colorSpace || 'Rec.709',
                bins: [],
                timelines: []
            }
        };

        // Criar bins para organização
        resolveProject.project.bins = [
            { name: 'Footage', type: 'media' },
            { name: 'Audio', type: 'audio' },
            { name: 'Graphics', type: 'graphics' },
            { name: 'Color Grades', type: 'color' }
        ];

        // Criar timeline baseada nas cenas
        const timeline = await this.createTimelineFromScenes(project.scenes || [], options);
        resolveProject.project.timelines.push(timeline);

        return JSON.stringify(resolveProject, null, 2);
    }

    async generateEDL(project, options) {
        const scenes = project.scenes || [];
        let edl = '';
        
        // Header EDL
        edl += `TITLE: ${project.title}\n`;
        edl += `FCM: NON-DROP FRAME\n\n`;

        let editNumber = 1;
        let currentTimecode = '01:00:00:00';

        for (const scene of scenes) {
            const duration = this.estimateSceneDuration(scene);
            const endTimecode = this.addTimecode(currentTimecode, duration);
            
            // Formato EDL padrão
            edl += `${editNumber.toString().padStart(3, '0')}  `;
            edl += `${scene.id || 'AX'}       V     C        `;
            edl += `${currentTimecode} ${endTimecode} `;
            edl += `01:00:00:00 ${this.addTimecode('01:00:00:00', duration)}\n`;
            
            // Comentário com nome da cena
            edl += `* FROM CLIP NAME: ${scene.title || `Scene ${editNumber}`}\n\n`;
            
            currentTimecode = endTimecode;
            editNumber++;
        }

        return edl;
    }

    async createTimelineFromScenes(scenes, options) {
        const timeline = {
            name: 'Master Timeline',
            frameRate: options.frameRate || '24',
            tracks: {
                video: [],
                audio: []
            },
            markers: []
        };

        let currentFrame = 0;

        for (const scene of scenes) {
            const durationFrames = this.convertDurationToFrames(
                this.estimateSceneDuration(scene), 
                timeline.frameRate
            );

            // Video track
            timeline.tracks.video.push({
                id: scene.id,
                name: scene.title || `Scene ${scene.order || 1}`,
                startFrame: currentFrame,
                endFrame: currentFrame + durationFrames,
                mediaPath: scene.mediaPath || '',
                effects: scene.effects || []
            });

            // Audio track (se houver diálogo)
            if (scene.dialogue && scene.dialogue.length > 0) {
                timeline.tracks.audio.push({
                    id: `${scene.id}_audio`,
                    name: `${scene.title || `Scene ${scene.order || 1}`} - Audio`,
                    startFrame: currentFrame,
                    endFrame: currentFrame + durationFrames,
                    audioPath: scene.audioPath || '',
                    dialogues: scene.dialogue
                });
            }

            // Marker para início da cena
            timeline.markers.push({
                frame: currentFrame,
                name: scene.title || `Scene ${scene.order || 1}`,
                color: 'blue',
                notes: scene.description || ''
            });

            currentFrame += durationFrames;
        }

        return timeline;
    }

    // BUDGET CALCULATOR
    async calculateBudget(projectId, budgetTemplate = 'feature-film') {
        try {
            const project = await this.getProject(projectId);
            if (!project) {
                throw new Error('Projeto não encontrado');
            }

            console.log(`💰 [Budget Calculator] Calculando orçamento: ${project.title}`);

            const template = this.templates.get(budgetTemplate);
            if (!template) {
                throw new Error('Template de orçamento não encontrado');
            }

            const budget = await this.generateDetailedBudget(project, template);
            
            // Salvar orçamento
            await this.saveBudget(projectId, budget);

            this.emit('budget-calculated', { projectId, budget });
            console.log(`✅ [Budget Calculator] Orçamento calculado: ${this.formatCurrency(budget.total)}`);

            return budget;

        } catch (error) {
            console.error('❌ [Budget Calculator] Erro no cálculo:', error);
            throw error;
        }
    }

    async generateDetailedBudget(project, template) {
        const budget = {
            id: uuidv4(),
            projectId: project.id,
            template: template.name,
            currency: 'BRL',
            exchangeRate: 1.0,
            createdAt: new Date().toISOString(),
            categories: {},
            totals: {},
            contingency: 0.10 // 10% de contingência
        };

        // Categorias principais
        const categories = [
            'development',
            'preProduction',
            'production',
            'postProduction',
            'marketing',
            'distribution'
        ];

        for (const category of categories) {
            budget.categories[category] = await this.calculateCategoryBudget(project, category);
        }

        // Calcular totais
        budget.totals.subtotal = Object.values(budget.categories)
            .reduce((sum, category) => sum + category.total, 0);
        
        budget.totals.contingency = budget.totals.subtotal * budget.contingency;
        budget.totals.total = budget.totals.subtotal + budget.totals.contingency;

        // Análise de viabilidade
        budget.analysis = this.analyzeBudgetViability(budget, project);

        return budget;
    }

    async calculateCategoryBudget(project, category) {
        const categoryBudget = {
            name: this.getCategoryName(category),
            items: [],
            total: 0
        };

        switch (category) {
            case 'development':
                categoryBudget.items = await this.calculateDevelopmentCosts(project);
                break;
            case 'preProduction':
                categoryBudget.items = await this.calculatePreProductionCosts(project);
                break;
            case 'production':
                categoryBudget.items = await this.calculateProductionCosts(project);
                break;
            case 'postProduction':
                categoryBudget.items = await this.calculatePostProductionCosts(project);
                break;
            case 'marketing':
                categoryBudget.items = await this.calculateMarketingCosts(project);
                break;
            case 'distribution':
                categoryBudget.items = await this.calculateDistributionCosts(project);
                break;
        }

        categoryBudget.total = categoryBudget.items.reduce((sum, item) => sum + item.total, 0);
        return categoryBudget;
    }

    async calculateProductionCosts(project) {
        const scenes = project.scenes || [];
        const shootingDays = this.calculateShootingDays(scenes);
        const crewSize = this.estimateCrewSize(project);
        
        return [
            {
                name: 'Diretor',
                quantity: shootingDays,
                unit: 'dia',
                unitCost: 2000,
                total: shootingDays * 2000
            },
            {
                name: 'Diretor de Fotografia',
                quantity: shootingDays,
                unit: 'dia',
                unitCost: 1500,
                total: shootingDays * 1500
            },
            {
                name: 'Equipe de Câmera',
                quantity: shootingDays * crewSize,
                unit: 'pessoa/dia',
                unitCost: 400,
                total: shootingDays * crewSize * 400
            },
            {
                name: 'Equipamentos',
                quantity: shootingDays,
                unit: 'dia',
                unitCost: 3000,
                total: shootingDays * 3000
            },
            {
                name: 'Locações',
                quantity: this.getUniqueLocations(project).length,
                unit: 'locação',
                unitCost: 1000,
                total: this.getUniqueLocations(project).length * 1000
            },
            {
                name: 'Alimentação',
                quantity: shootingDays * (crewSize + this.getCastSize(project)),
                unit: 'pessoa/dia',
                unitCost: 30,
                total: shootingDays * (crewSize + this.getCastSize(project)) * 30
            }
        ];
    }

    async calculatePostProductionCosts(project) {
        const estimatedDuration = this.calculateEstimatedDuration(project);
        const complexity = this.assessProjectComplexity(project);
        
        const baseEditingCost = estimatedDuration * 100; // R$ 100 por minuto
        const vfxMultiplier = complexity.vfx ? 3 : 1;
        const colorGradingCost = estimatedDuration * 50;
        
        return [
            {
                name: 'Edição',
                quantity: estimatedDuration,
                unit: 'minuto',
                unitCost: 100 * vfxMultiplier,
                total: baseEditingCost * vfxMultiplier
            },
            {
                name: 'Correção de Cor',
                quantity: estimatedDuration,
                unit: 'minuto',
                unitCost: 50,
                total: colorGradingCost
            },
            {
                name: 'Mixagem de Som',
                quantity: estimatedDuration,
                unit: 'minuto',
                unitCost: 75,
                total: estimatedDuration * 75
            },
            {
                name: 'Trilha Sonora Original',
                quantity: 1,
                unit: 'projeto',
                unitCost: 5000,
                total: 5000
            },
            {
                name: 'Renderização Final',
                quantity: 1,
                unit: 'projeto',
                unitCost: 1000,
                total: 1000
            }
        ];
    }

    // SCHEDULE GENERATOR
    async generateSchedule(projectId, scheduleOptions = {}) {
        try {
            const project = await this.getProject(projectId);
            if (!project) {
                throw new Error('Projeto não encontrado');
            }

            console.log(`📅 [Schedule Generator] Gerando cronograma: ${project.title}`);

            const schedule = await this.createProductionSchedule(project, scheduleOptions);
            
            // Gerar Gantt Chart
            const ganttData = await this.generateGanttChart(schedule);
            
            // Salvar cronograma
            await this.saveSchedule(projectId, schedule);

            const scheduleData = {
                id: uuidv4(),
                projectId,
                schedule,
                ganttData,
                options: scheduleOptions,
                createdAt: new Date().toISOString(),
                metadata: {
                    totalDays: schedule.totalDays,
                    shootingDays: schedule.shootingDays,
                    phases: schedule.phases.length
                }
            };

            this.emit('schedule-generated', scheduleData);
            console.log(`✅ [Schedule Generator] Cronograma gerado: ${schedule.totalDays} dias totais`);

            return scheduleData;

        } catch (error) {
            console.error('❌ [Schedule Generator] Erro na geração:', error);
            throw error;
        }
    }

    async createProductionSchedule(project, options) {
        const scenes = project.scenes || [];
        const startDate = new Date(options.startDate || Date.now());
        
        const schedule = {
            projectTitle: project.title,
            startDate: startDate.toISOString(),
            phases: [],
            totalDays: 0,
            shootingDays: 0
        };

        // Fase de Pré-Produção
        const preProductionPhase = await this.createPreProductionPhase(project, startDate, options);
        schedule.phases.push(preProductionPhase);

        // Fase de Produção
        const productionStartDate = this.addDays(startDate, preProductionPhase.duration);
        const productionPhase = await this.createProductionPhase(project, productionStartDate, options);
        schedule.phases.push(productionPhase);

        // Fase de Pós-Produção
        const postProductionStartDate = this.addDays(productionStartDate, productionPhase.duration);
        const postProductionPhase = await this.createPostProductionPhase(project, postProductionStartDate, options);
        schedule.phases.push(postProductionPhase);

        // Calcular totais
        schedule.totalDays = schedule.phases.reduce((sum, phase) => sum + phase.duration, 0);
        schedule.shootingDays = productionPhase.shootingDays;
        schedule.endDate = this.addDays(startDate, schedule.totalDays).toISOString();

        return schedule;
    }

    async createProductionPhase(project, startDate, options) {
        const scenes = project.scenes || [];
        const shootingDays = this.calculateShootingDays(scenes);
        
        // Agrupar cenas por locação para otimizar cronograma
        const locationGroups = this.groupScenesByLocation(scenes);
        
        const tasks = [];
        let currentDate = new Date(startDate);

        for (const [location, locationScenes] of locationGroups) {
            const daysNeeded = Math.ceil(locationScenes.length / 3); // 3 cenas por dia em média
            
            tasks.push({
                id: uuidv4(),
                name: `Filmagem - ${location}`,
                startDate: currentDate.toISOString(),
                endDate: this.addDays(currentDate, daysNeeded).toISOString(),
                duration: daysNeeded,
                type: 'shooting',
                location,
                scenes: locationScenes.map(scene => ({
                    id: scene.id,
                    title: scene.title,
                    estimatedTime: this.estimateSceneShootingTime(scene)
                })),
                crew: this.getRequiredCrew(locationScenes),
                equipment: this.getRequiredEquipment(locationScenes)
            });
            
            currentDate = this.addDays(currentDate, daysNeeded);
        }

        return {
            name: 'Produção',
            startDate: startDate.toISOString(),
            endDate: currentDate.toISOString(),
            duration: shootingDays,
            shootingDays,
            tasks,
            type: 'production'
        };
    }

    async generateGanttChart(schedule) {
        const ganttData = {
            title: schedule.projectTitle,
            startDate: schedule.startDate,
            endDate: schedule.endDate,
            tasks: [],
            milestones: []
        };

        let taskId = 1;
        
        for (const phase of schedule.phases) {
            // Adicionar fase como grupo
            ganttData.tasks.push({
                id: taskId++,
                name: phase.name,
                start: phase.startDate,
                end: phase.endDate,
                duration: phase.duration,
                type: 'phase',
                progress: 0,
                dependencies: [],
                children: []
            });

            // Adicionar tarefas da fase
            if (phase.tasks) {
                for (const task of phase.tasks) {
                    ganttData.tasks.push({
                        id: taskId++,
                        name: task.name,
                        start: task.startDate,
                        end: task.endDate,
                        duration: task.duration,
                        type: task.type,
                        progress: 0,
                        dependencies: task.dependencies || [],
                        metadata: {
                            location: task.location,
                            scenes: task.scenes,
                            crew: task.crew,
                            equipment: task.equipment
                        }
                    });
                }
            }
        }

        // Adicionar marcos importantes
        ganttData.milestones = [
            {
                name: 'Início da Pré-Produção',
                date: schedule.startDate,
                type: 'start'
            },
            {
                name: 'Início das Filmagens',
                date: schedule.phases.find(p => p.type === 'production')?.startDate,
                type: 'production-start'
            },
            {
                name: 'Fim das Filmagens',
                date: schedule.phases.find(p => p.type === 'production')?.endDate,
                type: 'production-end'
            },
            {
                name: 'Finalização do Projeto',
                date: schedule.endDate,
                type: 'end'
            }
        ];

        return ganttData;
    }

    // Métodos auxiliares
    calculatePageCount(project) {
        const scenes = project.scenes || [];
        const totalWords = scenes.reduce((sum, scene) => {
            const sceneWords = (scene.description || '').split(' ').length +
                             (scene.dialogue || []).reduce((dialogueSum, d) => 
                                 dialogueSum + (d.content || '').split(' ').length, 0);
            return sum + sceneWords;
        }, 0);
        
        return Math.ceil(totalWords / 250); // ~250 palavras por página
    }

    getUniqueCharacters(project) {
        const characters = new Set();
        
        (project.scenes || []).forEach(scene => {
            (scene.dialogue || []).forEach(dialogue => {
                if (dialogue.character?.name) {
                    characters.add(dialogue.character.name);
                }
            });
        });

        return Array.from(characters).map(name => ({ name }));
    }

    sanitizeFilename(filename) {
        return filename.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    }

    formatCurrency(amount, currency = 'BRL') {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: currency
        }).format(amount);
    }

    calculateShootingDays(scenes) {
        // Estimativa: 3-5 cenas por dia dependendo da complexidade
        const totalScenes = scenes.length;
        const averageScenesPerDay = 4;
        return Math.ceil(totalScenes / averageScenesPerDay);
    }

    estimateCrewSize(project) {
        const complexity = this.assessProjectComplexity(project);
        
        let baseCrewSize = 8; // Crew mínima
        
        if (complexity.budget === 'high') baseCrewSize += 12;
        else if (complexity.budget === 'medium') baseCrewSize += 6;
        
        if (complexity.vfx) baseCrewSize += 3;
        if (complexity.stunts) baseCrewSize += 4;
        
        return baseCrewSize;
    }

    assessProjectComplexity(project) {
        const scenes = project.scenes || [];
        const uniqueLocations = this.getUniqueLocations(project);
        const castSize = this.getCastSize(project);
        
        return {
            budget: scenes.length > 50 ? 'high' : scenes.length > 20 ? 'medium' : 'low',
            locations: uniqueLocations.length,
            vfx: scenes.some(scene => (scene.notes || '').toLowerCase().includes('efeito')),
            stunts: scenes.some(scene => (scene.description || '').toLowerCase().includes('ação')),
            castSize
        };
    }

    getUniqueLocations(project) {
        const locations = new Set();
        (project.scenes || []).forEach(scene => {
            if (scene.location) {
                locations.add(scene.location);
            }
        });
        return Array.from(locations);
    }

    getCastSize(project) {
        return this.getUniqueCharacters(project).length;
    }

    async getProject(projectId) {
        // Em produção, buscar do banco de dados
        return this.projects.get(projectId) || await this.core.data?.load('projects', { id: projectId });
    }

    async saveExport(content, filename, type) {
        const outputDir = path.join(process.cwd(), 'exports', type);
        await fs.mkdir(outputDir, { recursive: true });
        
        const filePath = path.join(outputDir, filename);
        await fs.writeFile(filePath, content, 'utf8');
        
        return filePath;
    }

    // API pública
    getSupportedExportFormats() {
        return [
            { id: 'final-draft', name: 'Final Draft (.fdx)', extension: 'fdx' },
            { id: 'fountain', name: 'Fountain (.fountain)', extension: 'fountain' },
            { id: 'pdf', name: 'PDF Script (.pdf)', extension: 'pdf' },
            { id: 'davinci-resolve', name: 'DaVinci Resolve Project', extension: 'drp' },
            { id: 'edl', name: 'Edit Decision List (.edl)', extension: 'edl' }
        ];
    }

    getBudgetTemplates() {
        return Array.from(this.templates.entries()).map(([id, template]) => ({
            id,
            name: template.name,
            defaultBudget: template.defaultBudget
        }));
    }

    getExportQueue() {
        return this.exportQueue;
    }
}

module.exports = DigimundoCinemaTools;