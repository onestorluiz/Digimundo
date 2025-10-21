/**
 * DIGIMUNDO GRAPHQL SERVER - MODO HACKER
 * Sistema ultra-avançado com Queries, Mutations, Subscriptions e DataLoader
 */

const { ApolloServer } = require('apollo-server-express');
const { gql } = require('apollo-server-express');
const { PubSub } = require('graphql-subscriptions');
const DataLoader = require('dataloader');
const { GraphQLScalarType } = require('graphql');
const { Kind } = require('graphql/language');
const express = require('express');
const http = require('http');
const { execute, subscribe } = require('graphql');
const { SubscriptionServer } = require('subscriptions-transport-ws');
const { makeExecutableSchema } = require('@graphql-tools/schema');

class DigimundoGraphQLServer {
    constructor(digimundoCore) {
        this.core = digimundoCore;
        this.pubsub = new PubSub();
        this.app = express();
        this.httpServer = http.createServer(this.app);
        
        this.setupDataLoaders();
        this.createSchema();
        this.createServer();
    }

    setupDataLoaders() {
        // DataLoader para otimização de queries
        this.dataLoaders = {
            // Digimon Loader
            digimons: new DataLoader(async (ids) => {
                const digimons = await this.core.data?.load('digimons', { 
                    id: { $in: ids } 
                }) || [];
                return ids.map(id => digimons.find(d => d.id === id) || null);
            }),

            // Memory Loader
            memories: new DataLoader(async (ids) => {
                const memories = await this.core.data?.load('memories', { 
                    id: { $in: ids } 
                }) || [];
                return ids.map(id => memories.find(m => m.id === id) || null);
            }),

            // User Loader
            users: new DataLoader(async (ids) => {
                const users = await this.core.data?.load('users', { 
                    id: { $in: ids } 
                }) || [];
                return ids.map(id => users.find(u => u.id === id) || null);
            }),

            // Project Loader
            projects: new DataLoader(async (ids) => {
                const projects = await this.core.data?.load('projects', { 
                    id: { $in: ids } 
                }) || [];
                return ids.map(id => projects.find(p => p.id === id) || null);
            }),

            // Scene Loader
            scenes: new DataLoader(async (ids) => {
                const scenes = await this.core.data?.load('scenes', { 
                    id: { $in: ids } 
                }) || [];
                return ids.map(id => scenes.find(s => s.id === id) || null);
            })
        };
    }

    createSchema() {
        this.typeDefs = gql`
            scalar DateTime
            scalar JSON

            enum DigimonType {
                ROOKIE
                CHAMPION
                ULTIMATE
                MEGA
                CUSTOM
            }

            enum MemoryType {
                INTERACTION
                LEARNING
                EVOLUTION
                PROJECT
                COLLABORATION
            }

            enum ProjectStatus {
                DRAFT
                IN_PROGRESS
                REVIEW
                COMPLETED
                ARCHIVED
            }

            type User {
                id: ID!
                name: String!
                email: String
                avatar: String
                role: String!
                specialization: String
                projects: [Project!]!
                digimons: [Digimon!]!
                collaborations: [Collaboration!]!
                createdAt: DateTime!
                updatedAt: DateTime!
            }

            type Digimon {
                id: ID!
                name: String!
                type: DigimonType!
                stage: String!
                personality: JSON!
                abilities: [String!]!
                evolutionStage: Int!
                owner: User!
                memories: [Memory!]!
                interactions: [Interaction!]!
                projects: [Project!]!
                status: String!
                avatar: String
                description: String
                createdAt: DateTime!
                updatedAt: DateTime!
                lastActive: DateTime
            }

            type Memory {
                id: ID!
                type: MemoryType!
                content: String!
                metadata: JSON
                digimon: Digimon!
                project: Project
                importance: Float!
                tags: [String!]!
                createdAt: DateTime!
                updatedAt: DateTime!
            }

            type Project {
                id: ID!
                title: String!
                description: String!
                status: ProjectStatus!
                owner: User!
                collaborators: [User!]!
                digimons: [Digimon!]!
                scenes: [Scene!]!
                timeline: [TimelineEvent!]!
                storyboard: Storyboard!
                budget: Budget
                schedule: Schedule
                assets: [Asset!]!
                metadata: JSON
                createdAt: DateTime!
                updatedAt: DateTime!
                deadline: DateTime
            }

            type Scene {
                id: ID!
                title: String!
                description: String!
                content: String!
                order: Int!
                duration: Float
                location: String
                characters: [Character!]!
                dialogue: [Dialogue!]!
                actions: [Action!]!
                notes: [Note!]!
                project: Project!
                storyboard: [StoryboardFrame!]!
                createdAt: DateTime!
                updatedAt: DateTime!
            }

            type Character {
                id: ID!
                name: String!
                description: String!
                avatar: String
                personality: JSON
                backstory: String
                relationships: [Relationship!]!
                scenes: [Scene!]!
                project: Project!
                createdAt: DateTime!
                updatedAt: DateTime!
            }

            type Dialogue {
                id: ID!
                character: Character!
                content: String!
                emotion: String
                timing: Float
                scene: Scene!
                createdAt: DateTime!
            }

            type Action {
                id: ID!
                description: String!
                timing: Float
                duration: Float
                scene: Scene!
                createdAt: DateTime!
            }

            type Note {
                id: ID!
                content: String!
                author: User!
                type: String
                position: JSON
                scene: Scene
                project: Project
                createdAt: DateTime!
                updatedAt: DateTime!
            }

            type Storyboard {
                id: ID!
                project: Project!
                frames: [StoryboardFrame!]!
                createdAt: DateTime!
                updatedAt: DateTime!
            }

            type StoryboardFrame {
                id: ID!
                order: Int!
                image: String
                description: String!
                duration: Float
                transition: String
                scene: Scene
                storyboard: Storyboard!
                createdAt: DateTime!
                updatedAt: DateTime!
            }

            type Collaboration {
                id: ID!
                name: String!
                project: Project!
                participants: [User!]!
                room: String!
                active: Boolean!
                settings: JSON
                createdAt: DateTime!
                updatedAt: DateTime!
            }

            type Interaction {
                id: ID!
                digimon: Digimon!
                user: User!
                type: String!
                content: String!
                response: String
                analysis: JSON
                project: Project
                createdAt: DateTime!
            }

            type TimelineEvent {
                id: ID!
                project: Project!
                type: String!
                title: String!
                description: String
                startDate: DateTime!
                endDate: DateTime
                dependencies: [ID!]!
                assignees: [User!]!
                status: String!
                metadata: JSON
                createdAt: DateTime!
                updatedAt: DateTime!
            }

            type Budget {
                id: ID!
                project: Project!
                totalBudget: Float!
                categories: [BudgetCategory!]!
                expenses: [Expense!]!
                createdAt: DateTime!
                updatedAt: DateTime!
            }

            type BudgetCategory {
                id: ID!
                name: String!
                allocatedAmount: Float!
                spentAmount: Float!
                budget: Budget!
            }

            type Expense {
                id: ID!
                description: String!
                amount: Float!
                category: BudgetCategory!
                date: DateTime!
                approved: Boolean!
                budget: Budget!
            }

            type Schedule {
                id: ID!
                project: Project!
                tasks: [ScheduleTask!]!
                milestones: [Milestone!]!
                createdAt: DateTime!
                updatedAt: DateTime!
            }

            type ScheduleTask {
                id: ID!
                title: String!
                description: String
                startDate: DateTime!
                endDate: DateTime!
                dependencies: [ID!]!
                assignees: [User!]!
                status: String!
                progress: Float!
                schedule: Schedule!
            }

            type Milestone {
                id: ID!
                title: String!
                description: String
                date: DateTime!
                completed: Boolean!
                schedule: Schedule!
            }

            type Asset {
                id: ID!
                name: String!
                type: String!
                url: String!
                size: Int
                metadata: JSON
                project: Project!
                uploadedBy: User!
                createdAt: DateTime!
            }

            type Relationship {
                id: ID!
                character1: Character!
                character2: Character!
                type: String!
                description: String
                project: Project!
            }

            type Query {
                # User queries
                me: User
                user(id: ID!): User
                users(limit: Int, offset: Int): [User!]!

                # Digimon queries
                digimon(id: ID!): Digimon
                digimons(limit: Int, offset: Int, type: DigimonType): [Digimon!]!
                myDigimons: [Digimon!]!

                # Project queries
                project(id: ID!): Project
                projects(limit: Int, offset: Int, status: ProjectStatus): [Project!]!
                myProjects: [Project!]!

                # Scene queries
                scene(id: ID!): Scene
                scenes(projectId: ID!, limit: Int, offset: Int): [Scene!]!

                # Memory queries
                memory(id: ID!): Memory
                memories(digimonId: ID, type: MemoryType, limit: Int): [Memory!]!
                searchMemories(query: String!, limit: Int): [Memory!]!

                # Analytics queries
                projectAnalytics(projectId: ID!): JSON
                digimonAnalytics(digimonId: ID!): JSON
                userAnalytics: JSON

                # Collaboration queries
                collaboration(id: ID!): Collaboration
                activeCollaborations: [Collaboration!]!

                # Search
                search(query: String!, type: String): JSON
            }

            type Mutation {
                # User mutations
                createUser(input: CreateUserInput!): User!
                updateUser(id: ID!, input: UpdateUserInput!): User!
                deleteUser(id: ID!): Boolean!

                # Digimon mutations
                createDigimon(input: CreateDigimonInput!): Digimon!
                updateDigimon(id: ID!, input: UpdateDigimonInput!): Digimon!
                evolveDigimon(id: ID!, input: EvolveDigimonInput!): Digimon!
                deleteDigimon(id: ID!): Boolean!

                # Project mutations
                createProject(input: CreateProjectInput!): Project!
                updateProject(id: ID!, input: UpdateProjectInput!): Project!
                deleteProject(id: ID!): Boolean!
                addCollaborator(projectId: ID!, userId: ID!): Project!
                removeCollaborator(projectId: ID!, userId: ID!): Project!

                # Scene mutations
                createScene(input: CreateSceneInput!): Scene!
                updateScene(id: ID!, input: UpdateSceneInput!): Scene!
                deleteScene(id: ID!): Boolean!
                reorderScenes(projectId: ID!, sceneIds: [ID!]!): [Scene!]!

                # Character mutations
                createCharacter(input: CreateCharacterInput!): Character!
                updateCharacter(id: ID!, input: UpdateCharacterInput!): Character!
                deleteCharacter(id: ID!): Boolean!

                # Memory mutations
                createMemory(input: CreateMemoryInput!): Memory!
                updateMemory(id: ID!, input: UpdateMemoryInput!): Memory!
                deleteMemory(id: ID!): Boolean!

                # Interaction mutations
                createInteraction(input: CreateInteractionInput!): Interaction!

                # Collaboration mutations
                createCollaboration(input: CreateCollaborationInput!): Collaboration!
                joinCollaboration(id: ID!): Collaboration!
                leaveCollaboration(id: ID!): Boolean!

                # Asset mutations
                uploadAsset(input: UploadAssetInput!): Asset!
                deleteAsset(id: ID!): Boolean!

                # Storyboard mutations
                createStoryboardFrame(input: CreateStoryboardFrameInput!): StoryboardFrame!
                updateStoryboardFrame(id: ID!, input: UpdateStoryboardFrameInput!): StoryboardFrame!
                deleteStoryboardFrame(id: ID!): Boolean!

                # Timeline mutations
                createTimelineEvent(input: CreateTimelineEventInput!): TimelineEvent!
                updateTimelineEvent(id: ID!, input: UpdateTimelineEventInput!): TimelineEvent!
                deleteTimelineEvent(id: ID!): Boolean!

                # Export mutations
                exportProject(projectId: ID!, format: String!): String!
                exportScene(sceneId: ID!, format: String!): String!
            }

            type Subscription {
                # Real-time updates
                projectUpdated(projectId: ID!): Project!
                sceneUpdated(sceneId: ID!): Scene!
                digimonEvolved(digimonId: ID!): Digimon!
                collaborationUpdated(collaborationId: ID!): Collaboration!
                
                # Live collaboration
                userJoinedProject(projectId: ID!): User!
                userLeftProject(projectId: ID!): User!
                cursorMoved(projectId: ID!): JSON!
                
                # Memory updates
                memoryCreated(digimonId: ID!): Memory!
                memoryUpdated(memoryId: ID!): Memory!
                
                # Interaction updates
                interactionCreated(digimonId: ID!): Interaction!
                
                # System notifications
                systemNotification(userId: ID!): JSON!
            }

            # Input types
            input CreateUserInput {
                name: String!
                email: String!
                role: String!
                specialization: String
                avatar: String
            }

            input UpdateUserInput {
                name: String
                email: String
                role: String
                specialization: String
                avatar: String
            }

            input CreateDigimonInput {
                name: String!
                type: DigimonType!
                description: String
                personality: JSON
                abilities: [String!]
            }

            input UpdateDigimonInput {
                name: String
                description: String
                personality: JSON
                abilities: [String!]
            }

            input EvolveDigimonInput {
                newStage: String!
                newAbilities: [String!]
                personalityChanges: JSON
            }

            input CreateProjectInput {
                title: String!
                description: String!
                deadline: DateTime
                collaboratorIds: [ID!]
                digimonIds: [ID!]
            }

            input UpdateProjectInput {
                title: String
                description: String
                status: ProjectStatus
                deadline: DateTime
            }

            input CreateSceneInput {
                title: String!
                description: String!
                content: String!
                projectId: ID!
                order: Int
                location: String
                duration: Float
            }

            input UpdateSceneInput {
                title: String
                description: String
                content: String
                order: Int
                location: String
                duration: Float
            }

            input CreateCharacterInput {
                name: String!
                description: String!
                projectId: ID!
                personality: JSON
                backstory: String
                avatar: String
            }

            input UpdateCharacterInput {
                name: String
                description: String
                personality: JSON
                backstory: String
                avatar: String
            }

            input CreateMemoryInput {
                type: MemoryType!
                content: String!
                digimonId: ID!
                projectId: ID
                metadata: JSON
                importance: Float
                tags: [String!]
            }

            input UpdateMemoryInput {
                content: String
                metadata: JSON
                importance: Float
                tags: [String!]
            }

            input CreateInteractionInput {
                digimonId: ID!
                type: String!
                content: String!
                projectId: ID
                analysis: JSON
            }

            input CreateCollaborationInput {
                name: String!
                projectId: ID!
                participantIds: [ID!]!
                settings: JSON
            }

            input UploadAssetInput {
                name: String!
                type: String!
                url: String!
                projectId: ID!
                metadata: JSON
            }

            input CreateStoryboardFrameInput {
                projectId: ID!
                sceneId: ID
                order: Int!
                description: String!
                image: String
                duration: Float
                transition: String
            }

            input UpdateStoryboardFrameInput {
                order: Int
                description: String
                image: String
                duration: Float
                transition: String
            }

            input CreateTimelineEventInput {
                projectId: ID!
                type: String!
                title: String!
                description: String
                startDate: DateTime!
                endDate: DateTime
                dependencies: [ID!]
                assigneeIds: [ID!]
            }

            input UpdateTimelineEventInput {
                title: String
                description: String
                startDate: DateTime
                endDate: DateTime
                dependencies: [ID!]
                assigneeIds: [ID!]
                status: String
            }
        `;

        this.resolvers = {
            DateTime: new GraphQLScalarType({
                name: 'DateTime',
                description: 'Date custom scalar type',
                serialize(value) {
                    return value instanceof Date ? value.toISOString() : null;
                },
                parseValue(value) {
                    return new Date(value);
                },
                parseLiteral(ast) {
                    if (ast.kind === Kind.STRING) {
                        return new Date(ast.value);
                    }
                    return null;
                }
            }),

            JSON: new GraphQLScalarType({
                name: 'JSON',
                description: 'JSON custom scalar type',
                serialize(value) {
                    return value;
                },
                parseValue(value) {
                    return value;
                },
                parseLiteral(ast) {
                    switch (ast.kind) {
                        case Kind.STRING:
                        case Kind.BOOLEAN:
                            return ast.value;
                        case Kind.INT:
                        case Kind.FLOAT:
                            return parseFloat(ast.value);
                        case Kind.OBJECT:
                            return ast.fields.reduce((accumulator, field) => {
                                accumulator[field.name.value] = this.parseLiteral(field.value);
                                return accumulator;
                            }, {});
                        case Kind.LIST:
                            return ast.values.map(this.parseLiteral);
                        default:
                            return null;
                    }
                }
            }),

            Query: {
                me: async (parent, args, context) => {
                    return context.user;
                },

                user: async (parent, { id }, context) => {
                    return context.dataLoaders.users.load(id);
                },

                users: async (parent, { limit = 20, offset = 0 }, context) => {
                    return await context.core.data?.load('users', {}, { limit, offset }) || [];
                },

                digimon: async (parent, { id }, context) => {
                    return context.dataLoaders.digimons.load(id);
                },

                digimons: async (parent, { limit = 20, offset = 0, type }, context) => {
                    const query = type ? { type } : {};
                    return await context.core.data?.load('digimons', query, { limit, offset }) || [];
                },

                myDigimons: async (parent, args, context) => {
                    if (!context.user) throw new Error('Not authenticated');
                    return await context.core.data?.load('digimons', { 
                        ownerId: context.user.id 
                    }) || [];
                },

                project: async (parent, { id }, context) => {
                    return context.dataLoaders.projects.load(id);
                },

                projects: async (parent, { limit = 20, offset = 0, status }, context) => {
                    const query = status ? { status } : {};
                    return await context.core.data?.load('projects', query, { limit, offset }) || [];
                },

                myProjects: async (parent, args, context) => {
                    if (!context.user) throw new Error('Not authenticated');
                    return await context.core.data?.load('projects', {
                        $or: [
                            { ownerId: context.user.id },
                            { collaboratorIds: { $in: [context.user.id] } }
                        ]
                    }) || [];
                },

                searchMemories: async (parent, { query, limit = 20 }, context) => {
                    return await context.core.memory?.search(query, { limit }) || [];
                }
            },

            Mutation: {
                createProject: async (parent, { input }, context) => {
                    if (!context.user) throw new Error('Not authenticated');
                    
                    const project = {
                        ...input,
                        id: require('uuid').v4(),
                        ownerId: context.user.id,
                        status: 'DRAFT',
                        createdAt: new Date(),
                        updatedAt: new Date()
                    };

                    await context.core.data?.save('projects', project);
                    context.pubsub.publish('PROJECT_CREATED', { projectUpdated: project });
                    
                    return project;
                },

                evolveDigimon: async (parent, { id, input }, context) => {
                    const digimon = await context.dataLoaders.digimons.load(id);
                    if (!digimon) throw new Error('Digimon not found');

                    const evolvedDigimon = {
                        ...digimon,
                        ...input,
                        evolutionStage: digimon.evolutionStage + 1,
                        updatedAt: new Date()
                    };

                    await context.core.data?.update('digimons', id, evolvedDigimon);
                    context.pubsub.publish('DIGIMON_EVOLVED', { 
                        digimonEvolved: evolvedDigimon 
                    });

                    return evolvedDigimon;
                },

                createInteraction: async (parent, { input }, context) => {
                    const interaction = {
                        ...input,
                        id: require('uuid').v4(),
                        userId: context.user?.id,
                        createdAt: new Date()
                    };

                    await context.core.data?.save('interactions', interaction);
                    context.pubsub.publish('INTERACTION_CREATED', { 
                        interactionCreated: interaction 
                    });

                    return interaction;
                }
            },

            Subscription: {
                projectUpdated: {
                    subscribe: (parent, { projectId }, context) => {
                        return context.pubsub.asyncIterator(['PROJECT_UPDATED']);
                    }
                },

                digimonEvolved: {
                    subscribe: (parent, { digimonId }, context) => {
                        return context.pubsub.asyncIterator(['DIGIMON_EVOLVED']);
                    }
                },

                interactionCreated: {
                    subscribe: (parent, { digimonId }, context) => {
                        return context.pubsub.asyncIterator(['INTERACTION_CREATED']);
                    }
                },

                collaborationUpdated: {
                    subscribe: (parent, { collaborationId }, context) => {
                        return context.pubsub.asyncIterator(['COLLABORATION_UPDATED']);
                    }
                }
            },

            // Nested resolvers
            User: {
                projects: async (parent, args, context) => {
                    return await context.core.data?.load('projects', {
                        $or: [
                            { ownerId: parent.id },
                            { collaboratorIds: { $in: [parent.id] } }
                        ]
                    }) || [];
                },

                digimons: async (parent, args, context) => {
                    return await context.core.data?.load('digimons', { 
                        ownerId: parent.id 
                    }) || [];
                }
            },

            Digimon: {
                owner: async (parent, args, context) => {
                    return context.dataLoaders.users.load(parent.ownerId);
                },

                memories: async (parent, args, context) => {
                    return await context.core.data?.load('memories', { 
                        digimonId: parent.id 
                    }) || [];
                },

                interactions: async (parent, args, context) => {
                    return await context.core.data?.load('interactions', { 
                        digimonId: parent.id 
                    }) || [];
                }
            },

            Project: {
                owner: async (parent, args, context) => {
                    return context.dataLoaders.users.load(parent.ownerId);
                },

                collaborators: async (parent, args, context) => {
                    if (!parent.collaboratorIds?.length) return [];
                    return await Promise.all(
                        parent.collaboratorIds.map(id => 
                            context.dataLoaders.users.load(id)
                        )
                    );
                },

                scenes: async (parent, args, context) => {
                    return await context.core.data?.load('scenes', { 
                        projectId: parent.id 
                    }, { sort: { order: 1 } }) || [];
                }
            }
        };

        this.schema = makeExecutableSchema({
            typeDefs: this.typeDefs,
            resolvers: this.resolvers
        });
    }

    createServer() {
        this.server = new ApolloServer({
            schema: this.schema,
            context: ({ req, connection }) => {
                if (connection) {
                    // Subscription context
                    return {
                        ...connection.context,
                        core: this.core,
                        dataLoaders: this.dataLoaders,
                        pubsub: this.pubsub
                    };
                }
                
                // Query/Mutation context
                return {
                    user: req.user, // Assuming authentication middleware
                    core: this.core,
                    dataLoaders: this.dataLoaders,
                    pubsub: this.pubsub
                };
            },
            subscriptions: {
                path: '/graphql',
                onConnect: (connectionParams, webSocket, context) => {
                    console.log('🔗 GraphQL Subscription conectada');
                    return {
                        // Add authentication logic here
                        user: connectionParams.user
                    };
                },
                onDisconnect: (webSocket, context) => {
                    console.log('❌ GraphQL Subscription desconectada');
                }
            },
            introspection: true,
            playground: true
        });
    }

    async start(port = 4000) {
        await this.server.start();
        this.server.applyMiddleware({ 
            app: this.app, 
            path: '/graphql',
            cors: {
                origin: '*',
                credentials: true
            }
        });

        // Setup subscription server
        const subscriptionServer = SubscriptionServer.create(
            {
                schema: this.schema,
                execute,
                subscribe,
                onConnect: (connectionParams, webSocket, context) => {
                    console.log('🔗 Subscription server conectado');
                    return {
                        core: this.core,
                        dataLoaders: this.dataLoaders,
                        pubsub: this.pubsub
                    };
                }
            },
            {
                server: this.httpServer,
                path: this.server.graphqlPath
            }
        );

        // GraphQL Playground
        this.app.get('/playground', (req, res) => {
            res.send(`
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Digimundo GraphQL Playground</title>
                    <style>
                        body { margin: 0; font-family: Arial, sans-serif; }
                        .header { background: #667eea; color: white; padding: 20px; text-align: center; }
                        .playground { height: calc(100vh - 80px); }
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>🎬 Digimundo GraphQL Playground - MODO HACKER</h1>
                        <p>Explore the complete API with queries, mutations, and real-time subscriptions</p>
                    </div>
                    <div class="playground">
                        <iframe src="/graphql" width="100%" height="100%" frameborder="0"></iframe>
                    </div>
                </body>
                </html>
            `);
        });

        return new Promise((resolve) => {
            this.httpServer.listen(port, () => {
                console.log(`🚀 [MODO HACKER] GraphQL Server rodando na porta ${port}`);
                console.log(`📊 Playground: http://localhost:${port}/playground`);
                console.log(`🔗 GraphQL Endpoint: http://localhost:${port}${this.server.graphqlPath}`);
                console.log(`🔄 Subscriptions: ws://localhost:${port}${this.server.graphqlPath}`);
                resolve();
            });
        });
    }

    // Métodos utilitários para performance insights
    getPerformanceMetrics() {
        return {
            dataLoaderStats: Object.entries(this.dataLoaders).map(([name, loader]) => ({
                name,
                cacheMap: loader._cacheMap.size,
                batchLoadFn: loader._batchLoadFn.name
            })),
            activeSubscriptions: this.pubsub.ee.listenerCount(),
            serverUptime: process.uptime()
        };
    }

    clearDataLoaderCache() {
        Object.values(this.dataLoaders).forEach(loader => {
            loader.clearAll();
        });
        console.log('🧹 DataLoader cache limpo');
    }
}

module.exports = DigimundoGraphQLServer;

// Para uso standalone
if (require.main === module) {
    const mockCore = {
        data: {
            load: async (collection, query = {}, options = {}) => {
                console.log(`Mock load: ${collection}`, query, options);
                return [];
            },
            save: async (collection, data) => {
                console.log(`Mock save: ${collection}`, data);
                return data;
            },
            update: async (collection, id, data) => {
                console.log(`Mock update: ${collection}`, id, data);
                return { ...data, id };
            }
        },
        memory: {
            search: async (query, options) => {
                console.log(`Mock memory search: ${query}`, options);
                return [];
            }
        }
    };

    const graphqlServer = new DigimundoGraphQLServer(mockCore);
    graphqlServer.start();
}