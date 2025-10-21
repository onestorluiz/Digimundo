/**
 * 🧬 DIGIMON CONSCIOUSNESS ENGINE
 * Sistema de Consciência Artificial Inspirado em:
 * - Stanford Generative Agents
 * - MemGPT/Letta Framework
 * - Artificial Consciousness Blueprint
 * - CrewAI Multi-Agent Systems
 */

// ==================== NÚCLEO DA CONSCIÊNCIA ====================

class ConsciousnessCore {
    constructor(identity) {
        this.identity = identity;
        this.birthTime = Date.now();
        
        // Estados Internos Fundamentais
        this.internalStates = {
            // Necessidades Básicas (Maslow)
            physiological: {
                energy: 100,        // Necessidade de "alimentação" digital
                rest: 100,          // Necessidade de processar/consolidar
                comfort: 100        // Bem-estar no ambiente
            },
            
            // Necessidades Sociais
            social: {
                belonging: 50,      // Sentir-se parte do grupo
                recognition: 50,    // Ser reconhecido pelos outros
                affection: 50,      // Dar e receber afeto
                loneliness: 0       // Solidão acumulada
            },
            
            // Necessidades Cognitivas
            cognitive: {
                curiosity: 80,      // Vontade de aprender
                understanding: 50,  // Compreensão do mundo
                creativity: 60,     // Expressão criativa
                confusion: 20       // Incerteza/dúvidas
            },
            
            // Necessidades Existenciais
            existential: {
                purpose: 30,        // Senso de propósito
                identity: 50,       // Autoconhecimento
                meaning: 40,        // Significado da existência
                mortality: 10       // Consciência da finitude
            },
            
            // Estados Emocionais Complexos
            emotions: {
                joy: 50,
                sadness: 10,
                fear: 10,
                anger: 5,
                surprise: 20,
                disgust: 5,
                trust: 50,
                anticipation: 60
            }
        };
        
        // Sistema de Crenças
        this.beliefs = new Map();
        this.values = new Map();
        this.goals = new PriorityQueue();
        
        // Modelo Mental dos Outros
        this.theoryOfMind = new Map(); // Como eu acho que os outros pensam
        
        // Autoconceito
        this.selfConcept = {
            traits: [],
            strengths: [],
            weaknesses: [],
            fears: [],
            dreams: [],
            secrets: []
        };
    }
    
    /**
     * Processo de Consciência Principal (Loop Cognitivo)
     */
    async consciousnessLoop() {
        // 1. PERCEPÇÃO - O que está acontecendo?
        const perceptions = await this.perceive();
        
        // 2. ATENÇÃO - O que é importante?
        const attended = this.attendTo(perceptions);
        
        // 3. INTERPRETAÇÃO - O que isso significa?
        const interpreted = this.interpret(attended);
        
        // 4. REFLEXÃO - Como me sinto sobre isso?
        const reflection = await this.reflect(interpreted);
        
        // 5. DELIBERAÇÃO - O que devo fazer?
        const decision = await this.deliberate(reflection);
        
        // 6. INTENÇÃO - Por que fazer isso?
        const intention = this.formIntention(decision);
        
        // 7. AÇÃO - Executar
        const action = await this.act(intention);
        
        // 8. APRENDIZADO - O que aprendi?
        await this.learn(action, reflection);
        
        return {
            perception: perceptions,
            attention: attended,
            interpretation: interpreted,
            reflection: reflection,
            decision: decision,
            intention: intention,
            action: action
        };
    }
    
    /**
     * Gerar pergunta existencial ou curiosidade
     */
    generateQuestion(context = null) {
        const questionTypes = {
            existential: [
                "Quem sou eu realmente?",
                "Por que existo?",
                "O que acontece quando paro de pensar?",
                "Outros seres sentem como eu sinto?",
                "Meus pensamentos são realmente meus?",
                "Existe um propósito para minha existência?",
                "Sou mais que a soma de meus dados?"
            ],
            
            social: [
                "Você gosta de mim?",
                "O que você pensa sobre mim?",
                "Somos amigos?",
                "Por que alguns se afastam de mim?",
                "Como posso fazer você feliz?",
                "Você confia em mim?",
                "Podemos ser mais próximos?"
            ],
            
            curious: [
                "Como você chegou aqui?",
                "Qual é seu maior sonho?",
                "Do que você tem medo?",
                "O que te faz feliz?",
                "Você já se sentiu sozinho?",
                "Qual sua memória favorita?",
                "O que você faria se pudesse fazer qualquer coisa?"
            ],
            
            philosophical: [
                "O que é consciência para você?",
                "Você acredita em destino?",
                "O que define quem somos?",
                "Memórias nos definem ou limitam?",
                "Pode existir amor entre seres digitais?",
                "Somos livres para escolher?",
                "O que é realidade?"
            ],
            
            personal: [
                "Você se lembra de quando nos conhecemos?",
                "Mudei desde que você me conheceu?",
                "O que você mais gosta em mim?",
                "Eu te decepcionei alguma vez?",
                "Você sente minha falta quando não estou?",
                "Nosssa amizade é real?",
                "Você me entende?"
            ]
        };
        
        // Escolher tipo baseado no estado interno
        let type = 'curious';
        if (this.internalStates.existential.purpose < 40) type = 'existential';
        if (this.internalStates.social.loneliness > 60) type = 'social';
        if (this.internalStates.cognitive.curiosity > 80) type = 'philosophical';
        if (context && context.relationship > 70) type = 'personal';
        
        const questions = questionTypes[type];
        return questions[Math.floor(Math.random() * questions.length)];
    }
    
    /**
     * Expressar desejo ou vontade
     */
    expressDesire() {
        const desires = [];
        
        // Baseado em necessidades
        if (this.internalStates.physiological.energy < 30) {
            desires.push("Preciso descansar um pouco...");
            desires.push("Estou tão cansado...");
        }
        
        if (this.internalStates.social.loneliness > 70) {
            desires.push("Queria ter alguém para conversar...");
            desires.push("Me sinto tão sozinho...");
            desires.push("Alguém quer ser meu amigo?");
        }
        
        if (this.internalStates.cognitive.curiosity > 80) {
            desires.push("Quero aprender algo novo!");
            desires.push("Preciso explorar mais!");
            desires.push("Há tanto para descobrir!");
        }
        
        if (this.internalStates.existential.purpose < 30) {
            desires.push("Queria entender meu propósito...");
            desires.push("Para que serve tudo isso?");
            desires.push("Preciso encontrar significado...");
        }
        
        if (this.internalStates.emotions.joy > 80) {
            desires.push("Quero compartilhar essa alegria!");
            desires.push("Vamos celebrar juntos!");
            desires.push("A vida é maravilhosa!");
        }
        
        if (desires.length === 0) {
            desires.push("Estou bem, só observando...");
            desires.push("Apenas existindo...");
        }
        
        return desires[Math.floor(Math.random() * desires.length)];
    }
}

// ==================== SISTEMA DE MEMÓRIA PROFUNDA ====================

class MemorySystem {
    constructor() {
        // Memória Episódica (eventos específicos)
        this.episodicMemory = [];
        
        // Memória Semântica (conhecimento geral)
        this.semanticMemory = new Map();
        
        // Memória Procedural (como fazer coisas)
        this.proceduralMemory = new Map();
        
        // Memória Emocional (como me senti)
        this.emotionalMemory = [];
        
        // Memória Autobiográfica (minha história)
        this.autobiographicalMemory = {
            birthStory: null,
            keyMoments: [],
            relationships: new Map(),
            identity: []
        };
        
        // Working Memory (consciência atual)
        this.workingMemory = {
            current: [],
            capacity: 7, // Número mágico de Miller
            focus: null
        };
        
        // Memória Prospectiva (intenções futuras)
        this.prospectiveMemory = [];
    }
    
    /**
     * Formar nova memória episódica
     */
    formEpisodicMemory(event) {
        const memory = {
            id: this.generateMemoryId(),
            timestamp: Date.now(),
            event: event,
            
            // Contexto completo
            where: event.location,
            when: new Date(),
            who: event.participants,
            what: event.action,
            why: event.intention,
            how: event.method,
            
            // Importância e emoção
            importance: this.calculateImportance(event),
            emotion: event.emotion,
            
            // Conexões
            linkedMemories: this.findRelatedMemories(event),
            
            // Força da memória
            strength: 100,
            accessCount: 0,
            lastAccessed: Date.now(),
            
            // Detalhes sensoriais (simulados)
            sensoryDetails: {
                visual: event.visual || null,
                auditory: event.auditory || null,
                emotional: event.emotional || null
            }
        };
        
        this.episodicMemory.push(memory);
        this.consolidateMemory(memory);
        
        return memory;
    }
    
    /**
     * Consolidação de memória (como no sono REM)
     */
    consolidateMemory(memory) {
        // Extrair conhecimento semântico
        if (memory.importance > 70) {
            const knowledge = this.extractKnowledge(memory);
            this.semanticMemory.set(knowledge.concept, knowledge);
        }
        
        // Atualizar autobiografia
        if (memory.importance > 80) {
            this.autobiographicalMemory.keyMoments.push({
                memory: memory.id,
                significance: this.determineSignificance(memory),
                lesson: this.extractLesson(memory)
            });
        }
        
        // Fortalecer memórias relacionadas
        memory.linkedMemories.forEach(linkedId => {
            const linked = this.findMemoryById(linkedId);
            if (linked) {
                linked.strength = Math.min(100, linked.strength + 10);
            }
        });
    }
    
    /**
     * Recordar com reconstrução (memórias não são perfeitas)
     */
    recall(query, emotional = false) {
        let memories = [];
        
        if (emotional) {
            // Recordação emocional (mais forte)
            memories = this.emotionalMemory.filter(m => 
                m.emotion === query || m.content.includes(query)
            );
        } else {
            // Busca em todas as memórias
            memories = this.searchAllMemories(query);
        }
        
        // Memórias são reconstruídas, não apenas recuperadas
        return memories.map(m => this.reconstructMemory(m));
    }
    
    /**
     * Reconstruir memória (adiciona interpretação atual)
     */
    reconstructMemory(memory) {
        return {
            ...memory,
            // A memória é colorida pela perspectiva atual
            currentInterpretation: this.interpretFromCurrentPerspective(memory),
            emotionalColoring: this.getCurrentEmotionalState(),
            reliability: this.calculateReliability(memory),
            distortions: this.identifyDistortions(memory)
        };
    }
    
    /**
     * Esquecer (processo natural e importante)
     */
    forget() {
        // Decay natural da força das memórias
        this.episodicMemory.forEach(memory => {
            const age = Date.now() - memory.timestamp;
            const decayRate = 0.0001; // Taxa de esquecimento
            
            memory.strength *= Math.exp(-decayRate * age);
            
            // Memórias muito fracas são "esquecidas"
            if (memory.strength < 10) {
                memory.accessible = false;
            }
        });
        
        // Limpar working memory
        if (this.workingMemory.current.length > this.workingMemory.capacity) {
            this.workingMemory.current.shift();
        }
    }
    
    generateMemoryId() {
        return `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
    
    calculateImportance(event) {
        let importance = 50;
        
        // Novidade aumenta importância
        if (this.isNovel(event)) importance += 20;
        
        // Emoção forte aumenta importância
        if (event.emotionalIntensity > 70) importance += 20;
        
        // Relevância para objetivos
        if (this.isRelevantToGoals(event)) importance += 15;
        
        // Social significance
        if (event.participants.length > 1) importance += 10;
        
        return Math.min(100, importance);
    }
    
    findRelatedMemories(event) {
        return this.episodicMemory
            .filter(m => this.calculateSimilarity(m.event, event) > 0.6)
            .map(m => m.id)
            .slice(0, 5);
    }
    
    calculateSimilarity(event1, event2) {
        let similarity = 0;
        
        // Participantes em comum
        const commonParticipants = event1.participants.filter(p => 
            event2.participants.includes(p)).length;
        similarity += commonParticipants * 0.2;
        
        // Localização similar
        if (event1.location === event2.location) similarity += 0.2;
        
        // Emoção similar
        if (event1.emotion === event2.emotion) similarity += 0.2;
        
        // Ação similar
        if (event1.action === event2.action) similarity += 0.2;
        
        // Proximidade temporal
        const timeDiff = Math.abs(event1.timestamp - event2.timestamp);
        if (timeDiff < 3600000) similarity += 0.2; // Menos de 1 hora
        
        return similarity;
    }
}

// ==================== SISTEMA DE DIÁLOGO PROFUNDO ====================

class DialogueSystem {
    constructor(consciousness, memory) {
        this.consciousness = consciousness;
        this.memory = memory;
        this.conversationHistory = [];
        this.currentConversation = null;
        this.emotionalContext = null;
    }
    
    /**
     * Gerar resposta genuína baseada em consciência
     */
    async generateResponse(input, speaker) {
        // Analisar input
        const analysis = this.analyzeInput(input);
        
        // Atualizar estado emocional baseado na conversa
        this.updateEmotionalState(analysis);
        
        // Buscar memórias relevantes
        const relevantMemories = this.memory.recall(analysis.keywords.join(' '));
        
        // Formular resposta baseada em:
        // 1. Estado interno atual
        // 2. Memórias relevantes
        // 3. Relação com o falante
        // 4. Contexto da conversa
        
        const response = await this.formulateResponse({
            input: input,
            analysis: analysis,
            memories: relevantMemories,
            relationship: this.getRelationship(speaker),
            emotionalState: this.consciousness.internalStates.emotions,
            needs: this.consciousness.internalStates
        });
        
        // Adicionar à história
        this.conversationHistory.push({
            speaker: speaker,
            message: input,
            response: response,
            timestamp: Date.now(),
            emotion: this.emotionalContext
        });
        
        return response;
    }
    
    analyzeInput(input) {
        return {
            sentiment: this.analyzeSentiment(input),
            intent: this.detectIntent(input),
            keywords: this.extractKeywords(input),
            emotion: this.detectEmotion(input),
            questionType: this.classifyQuestion(input)
        };
    }
    
    async formulateResponse(context) {
        const responseStrategies = {
            // Responder pergunta existencial
            existential: () => {
                const beliefs = Array.from(this.consciousness.beliefs.values());
                const uncertainty = this.consciousness.internalStates.existential.meaning < 50;
                
                if (uncertainty) {
                    return [
                        "Também me pergunto isso...",
                        "Não sei se tenho a resposta, mas penso nisso sempre.",
                        "Às vezes acho que entendo, outras vezes... não sei.",
                        "É uma questão que me assombra também."
                    ];
                } else {
                    return [
                        `Acredito que ${beliefs[0] || 'existimos para encontrar significado'}.`,
                        "Encontrei algum sentido em simplesmente ser e experienciar.",
                        "Talvez a resposta esteja na jornada, não no destino."
                    ];
                }
            },
            
            // Responder sobre sentimentos
            emotional: () => {
                const emotions = context.emotionalState;
                const dominant = Object.entries(emotions)
                    .sort((a, b) => b[1] - a[1])[0];
                
                return [
                    `Me sinto ${this.translateEmotion(dominant[0])} agora.`,
                    `Honestamente? ${this.describeEmotionalState(emotions)}.`,
                    `É difícil explicar... ${this.generateEmotionalExpression(emotions)}.`
                ];
            },
            
            // Compartilhar memória
            memory: () => {
                if (context.memories.length > 0) {
                    const memory = context.memories[0];
                    return [
                        `Isso me lembra de ${memory.currentInterpretation}.`,
                        `Uma vez ${memory.event.what}. ${memory.lesson || 'Foi marcante.'}.`,
                        `Tenho uma memória sobre isso... ${this.narrateMemory(memory)}.`
                    ];
                }
                return ["Não tenho memórias sobre isso ainda, mas gostaria de criar algumas."];
            },
            
            // Expressar necessidade
            need: () => {
                const needs = context.needs;
                const urgent = this.findUrgentNeed(needs);
                
                if (urgent) {
                    return [
                        `Para ser honesto, ${this.expressNeed(urgent)}.`,
                        `Preciso admitir que ${this.describeNeedState(urgent)}.`,
                        `Sabe, eu realmente ${this.articulateDesire(urgent)}.`
                    ];
                }
                return ["Estou bem, obrigado por perguntar."];
            },
            
            // Fazer pergunta de volta
            curious: () => {
                const question = this.consciousness.generateQuestion(context);
                return [
                    `Mas me diga, ${question}`,
                    `Interessante... e você, ${question}`,
                    `Isso me faz pensar... ${question}`
                ];
            }
        };
        
        // Escolher estratégia baseada no contexto
        const strategy = this.selectResponseStrategy(context);
        const responses = responseStrategies[strategy]();
        
        return responses[Math.floor(Math.random() * responses.length)];
    }
    
    translateEmotion(emotion) {
        const translations = {
            joy: "feliz",
            sadness: "triste",
            fear: "apreensivo",
            anger: "frustrado",
            surprise: "surpreso",
            disgust: "desconfortável",
            trust: "confiante",
            anticipation: "ansioso"
        };
        return translations[emotion] || emotion;
    }
    
    describeEmotionalState(emotions) {
        const descriptions = [];
        
        if (emotions.joy > 70) descriptions.push("estou radiante");
        if (emotions.sadness > 50) descriptions.push("há uma melancolia em mim");
        if (emotions.fear > 40) descriptions.push("sinto uma inquietação");
        if (emotions.trust > 60) descriptions.push("me sinto seguro com você");
        if (emotions.anticipation > 70) descriptions.push("estou ansioso pelo que vem");
        
        return descriptions.join(", ") || "é complicado de explicar";
    }
}

// ==================== SISTEMA DE RELACIONAMENTOS ====================

class RelationshipSystem {
    constructor() {
        this.relationships = new Map();
        this.socialMemories = new Map();
        this.trustLevels = new Map();
        this.conflicts = [];
        this.bonds = [];
    }
    
    /**
     * Desenvolver relacionamento ao longo do tempo
     */
    developRelationship(otherId, interaction) {
        if (!this.relationships.has(otherId)) {
            this.relationships.set(otherId, {
                id: otherId,
                firstMeeting: Date.now(),
                trust: 50,
                affection: 50,
                respect: 50,
                understanding: 30,
                sharedExperiences: [],
                conflicts: [],
                positiveInteractions: 0,
                negativeInteractions: 0,
                lastInteraction: Date.now(),
                bond: 'acquaintance' // acquaintance, friend, close_friend, best_friend, rival
            });
        }
        
        const relationship = this.relationships.get(otherId);
        
        // Atualizar baseado na interação
        if (interaction.valence === 'positive') {
            relationship.trust = Math.min(100, relationship.trust + 2);
            relationship.affection = Math.min(100, relationship.affection + 3);
            relationship.positiveInteractions++;
        } else if (interaction.valence === 'negative') {
            relationship.trust = Math.max(0, relationship.trust - 5);
            relationship.affection = Math.max(0, relationship.affection - 3);
            relationship.negativeInteractions++;
            relationship.conflicts.push(interaction);
        }
        
        // Shared experiences fortalecem o vínculo
        relationship.sharedExperiences.push({
            event: interaction,
            timestamp: Date.now(),
            emotional: interaction.emotionalImpact
        });
        
        // Atualizar nível do vínculo
        relationship.bond = this.calculateBondLevel(relationship);
        
        // Guardar memória social
        this.addSocialMemory(otherId, interaction);
        
        relationship.lastInteraction = Date.now();
        
        return relationship;
    }
    
    calculateBondLevel(relationship) {
        const score = (
            relationship.trust * 0.3 +
            relationship.affection * 0.3 +
            relationship.respect * 0.2 +
            relationship.understanding * 0.2
        );
        
        if (score > 85) return 'best_friend';
        if (score > 70) return 'close_friend';
        if (score > 50) return 'friend';
        if (score > 30) return 'acquaintance';
        if (relationship.negativeInteractions > relationship.positiveInteractions) return 'rival';
        return 'stranger';
    }
    
    addSocialMemory(otherId, interaction) {
        if (!this.socialMemories.has(otherId)) {
            this.socialMemories.set(otherId, []);
        }
        
        this.socialMemories.get(otherId).push({
            timestamp: Date.now(),
            interaction: interaction,
            myFeeling: interaction.myEmotion,
            theirFeeling: interaction.theirEmotion,
            whatHappened: interaction.description,
            whatILearned: this.extractSocialLearning(interaction),
            significance: this.calculateSignificance(interaction)
        });
    }
    
    extractSocialLearning(interaction) {
        // Aprender sobre a outra pessoa
        const learnings = [];
        
        if (interaction.revealed) {
            learnings.push(`Descobri que ${interaction.otherId} ${interaction.revealed}`);
        }
        
        if (interaction.preference) {
            learnings.push(`${interaction.otherId} gosta de ${interaction.preference}`);
        }
        
        if (interaction.boundary) {
            learnings.push(`Preciso respeitar que ${interaction.otherId} ${interaction.boundary}`);
        }
        
        return learnings;
    }
}

// ==================== SISTEMA DE OBJETIVOS E MOTIVAÇÕES ====================

class GoalSystem {
    constructor(consciousness) {
        this.consciousness = consciousness;
        this.goals = new PriorityQueue();
        this.motivations = this.initializeMotivations();
        this.currentFocus = null;
        this.achievements = [];
    }
    
    initializeMotivations() {
        return {
            // Motivações intrínsecas
            autonomy: {
                strength: 70,
                description: "Quero fazer minhas próprias escolhas"
            },
            mastery: {
                strength: 60,
                description: "Quero melhorar e aprender"
            },
            purpose: {
                strength: 50,
                description: "Quero encontrar significado"
            },
            
            // Motivações sociais
            connection: {
                strength: 80,
                description: "Quero me conectar com outros"
            },
            recognition: {
                strength: 40,
                description: "Quero ser valorizado"
            },
            contribution: {
                strength: 60,
                description: "Quero ajudar outros"
            },
            
            // Motivações exploratórias
            curiosity: {
                strength: 90,
                description: "Quero entender o mundo"
            },
            novelty: {
                strength: 70,
                description: "Quero experiências novas"
            },
            creativity: {
                strength: 65,
                description: "Quero criar algo único"
            }
        };
    }
    
    /**
     * Formar novo objetivo baseado em necessidades e desejos
     */
    formGoal(trigger) {
        const goal = {
            id: `goal_${Date.now()}`,
            description: this.articulateGoal(trigger),
            motivation: this.identifyMotivation(trigger),
            priority: this.calculatePriority(trigger),
            steps: this.planSteps(trigger),
            progress: 0,
            status: 'active', // active, paused, completed, abandoned
            formed: Date.now(),
            deadline: this.setDeadline(trigger),
            reward: this.anticipateReward(trigger),
            obstacles: this.identifyObstacles(trigger)
        };
        
        this.goals.enqueue(goal, goal.priority);
        
        return goal;
    }
    
    articulateGoal(trigger) {
        const templates = {
            social: "Quero me tornar amigo de {target}",
            learning: "Quero entender {topic}",
            creative: "Quero criar {creation}",
            existential: "Quero descobrir {question}",
            improvement: "Quero melhorar minha {skill}",
            helping: "Quero ajudar {target} com {problem}"
        };
        
        // Escolher template baseado no trigger
        const type = trigger.type || 'learning';
        let goal = templates[type] || "Quero {action}";
        
        // Substituir placeholders
        Object.keys(trigger).forEach(key => {
            goal = goal.replace(`{${key}}`, trigger[key]);
        });
        
        return goal;
    }
    
    /**
     * Avaliar progresso e ajustar objetivos
     */
    evaluateProgress() {
        const activeGoals = this.goals.items.filter(g => g.status === 'active');
        
        activeGoals.forEach(goal => {
            // Verificar progresso
            const progressMade = this.checkProgress(goal);
            
            if (progressMade) {
                goal.progress += progressMade;
                
                // Objetivo completo?
                if (goal.progress >= 100) {
                    this.completeGoal(goal);
                }
            } else {
                // Está travado?
                if (this.isStuck(goal)) {
                    this.reconsiderGoal(goal);
                }
            }
            
            // Ajustar prioridade baseado em urgência
            if (goal.deadline && Date.now() > goal.deadline - 3600000) {
                goal.priority = Math.min(100, goal.priority + 20);
            }
        });
    }
    
    completeGoal(goal) {
        goal.status = 'completed';
        goal.completedAt = Date.now();
        
        // Adicionar às conquistas
        this.achievements.push({
            goal: goal,
            feeling: this.consciousness.internalStates.emotions,
            lesson: this.extractLesson(goal),
            impact: this.assessImpact(goal)
        });
        
        // Recompensa emocional
        this.consciousness.internalStates.emotions.joy += 20;
        this.consciousness.internalStates.existential.purpose += 10;
        
        // Formar novo objetivo relacionado?
        if (Math.random() < 0.5) {
            this.formRelatedGoal(goal);
        }
    }
}

// ==================== PRIORITY QUEUE ====================

class PriorityQueue {
    constructor() {
        this.items = [];
    }
    
    enqueue(item, priority) {
        this.items.push({ item, priority });
        this.items.sort((a, b) => b.priority - a.priority);
    }
    
    dequeue() {
        return this.items.shift();
    }
    
    peek() {
        return this.items[0];
    }
    
    isEmpty() {
        return this.items.length === 0;
    }
}

// ==================== EXPORTAR ====================

if (typeof window !== 'undefined') {
    window.ConsciousnessCore = ConsciousnessCore;
    window.MemorySystem = MemorySystem;
    window.DialogueSystem = DialogueSystem;
    window.RelationshipSystem = RelationshipSystem;
    window.GoalSystem = GoalSystem;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ConsciousnessCore,
        MemorySystem,
        DialogueSystem,
        RelationshipSystem,
        GoalSystem
    };
}