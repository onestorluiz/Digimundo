/**
 * DIGIMUNDO WEBRTC COLLABORATION SYSTEM - MODO HACKER
 * Sistema ultra-avançado de colaboração em tempo real
 * Features: Signaling Server, Salas de Colaboração, Voice/Video Chat, Screen Sharing
 */

const express = require('express');
const socketIO = require('socket.io');
const http = require('http');
const { v4: uuidv4 } = require('uuid');
const EventEmitter = require('events');

class DigimundoWebRTCCollaboration extends EventEmitter {
    constructor() {
        super();
        this.app = express();
        this.server = http.createServer(this.app);
        this.io = socketIO(this.server, {
            cors: {
                origin: "*",
                methods: ["GET", "POST"]
            }
        });
        
        // Estado global do sistema
        this.rooms = new Map();
        this.users = new Map();
        this.collaborationSessions = new Map();
        this.digitalTimeline = new Map();
        
        this.setupMiddleware();
        this.setupSocketHandlers();
        this.initializeCollaborationEngine();
    }

    setupMiddleware() {
        this.app.use(express.json());
        this.app.use(express.static('app/renderer'));
        
        // Endpoint para criar salas de colaboração
        this.app.post('/api/collaboration/create-room', (req, res) => {
            const roomId = uuidv4();
            const room = {
                id: roomId,
                name: req.body.name || `Projeto Digimon ${Date.now()}`,
                creator: req.body.userId,
                created: new Date(),
                participants: [],
                timeline: [],
                storyboard: {
                    scenes: [],
                    characters: [],
                    notes: []
                },
                settings: {
                    allowVoiceChat: true,
                    allowVideoChat: true,
                    allowScreenShare: true,
                    maxParticipants: 10
                }
            };
            
            this.rooms.set(roomId, room);
            res.json({ roomId, room });
        });

        // Endpoint para obter informações da sala
        this.app.get('/api/collaboration/room/:roomId', (req, res) => {
            const room = this.rooms.get(req.params.roomId);
            if (!room) {
                return res.status(404).json({ error: 'Sala não encontrada' });
            }
            res.json(room);
        });

        // Endpoint para listar salas ativas
        this.app.get('/api/collaboration/rooms', (req, res) => {
            const roomsList = Array.from(this.rooms.values()).map(room => ({
                id: room.id,
                name: room.name,
                participants: room.participants.length,
                created: room.created
            }));
            res.json(roomsList);
        });
    }

    setupSocketHandlers() {
        this.io.on('connection', (socket) => {
            console.log(`[WebRTC] Nova conexão: ${socket.id}`);
            
            // Registro de usuário
            socket.on('register-user', (userData) => {
                const user = {
                    id: socket.id,
                    name: userData.name || 'Criador Anônimo',
                    avatar: userData.avatar || '🎬',
                    role: userData.role || 'creator',
                    specialization: userData.specialization || 'geral',
                    joinedAt: new Date(),
                    cursor: { x: 0, y: 0 },
                    isActive: true
                };
                
                this.users.set(socket.id, user);
                socket.emit('user-registered', user);
                console.log(`[WebRTC] Usuário registrado: ${user.name}`);
            });

            // Entrar em sala de colaboração
            socket.on('join-room', (data) => {
                const { roomId, userId } = data;
                const room = this.rooms.get(roomId);
                const user = this.users.get(socket.id);
                
                if (!room || !user) {
                    socket.emit('error', { message: 'Sala ou usuário não encontrado' });
                    return;
                }

                // Verificar limite de participantes
                if (room.participants.length >= room.settings.maxParticipants) {
                    socket.emit('error', { message: 'Sala lotada' });
                    return;
                }

                // Adicionar usuário à sala
                socket.join(roomId);
                room.participants.push(user);
                user.currentRoom = roomId;
                
                // Notificar outros participantes
                socket.to(roomId).emit('user-joined', user);
                
                // Enviar estado atual da sala
                socket.emit('room-joined', {
                    room,
                    participants: room.participants,
                    timeline: room.timeline
                });

                console.log(`[WebRTC] ${user.name} entrou na sala ${room.name}`);
            });

            // WebRTC Signaling para video/audio
            socket.on('webrtc-offer', (data) => {
                socket.to(data.target).emit('webrtc-offer', {
                    offer: data.offer,
                    sender: socket.id
                });
            });

            socket.on('webrtc-answer', (data) => {
                socket.to(data.target).emit('webrtc-answer', {
                    answer: data.answer,
                    sender: socket.id
                });
            });

            socket.on('webrtc-ice-candidate', (data) => {
                socket.to(data.target).emit('webrtc-ice-candidate', {
                    candidate: data.candidate,
                    sender: socket.id
                });
            });

            // Colaboração em tempo real - Cursores
            socket.on('cursor-move', (data) => {
                const user = this.users.get(socket.id);
                if (user && user.currentRoom) {
                    user.cursor = data;
                    socket.to(user.currentRoom).emit('cursor-update', {
                        userId: socket.id,
                        cursor: data,
                        user: user
                    });
                }
            });

            // Colaboração em tempo real - Storyboard
            socket.on('storyboard-update', (data) => {
                const user = this.users.get(socket.id);
                if (!user || !user.currentRoom) return;

                const room = this.rooms.get(user.currentRoom);
                if (!room) return;

                // Aplicar mudança no storyboard
                this.applyStoryboardChange(room, data, user);
                
                // Broadcast para todos na sala
                socket.to(user.currentRoom).emit('storyboard-updated', {
                    change: data,
                    user: user,
                    timestamp: new Date()
                });
            });

            // Timeline de produção compartilhada
            socket.on('timeline-update', (data) => {
                const user = this.users.get(socket.id);
                if (!user || !user.currentRoom) return;

                const room = this.rooms.get(user.currentRoom);
                if (!room) return;

                const timelineEvent = {
                    id: uuidv4(),
                    type: data.type,
                    content: data.content,
                    user: user,
                    timestamp: new Date(),
                    position: data.position || room.timeline.length
                };

                room.timeline.push(timelineEvent);
                
                // Broadcast para todos na sala
                this.io.to(user.currentRoom).emit('timeline-updated', {
                    event: timelineEvent,
                    timeline: room.timeline
                });
            });

            // Chat com comandos especiais /digimon
            socket.on('chat-message', (data) => {
                const user = this.users.get(socket.id);
                if (!user || !user.currentRoom) return;

                const message = {
                    id: uuidv4(),
                    content: data.message,
                    user: user,
                    timestamp: new Date(),
                    type: 'message'
                };

                // Verificar se é comando /digimon
                if (data.message.startsWith('/digimon')) {
                    this.handleDigimonCommand(message, user.currentRoom);
                } else {
                    this.io.to(user.currentRoom).emit('chat-message', message);
                }
            });

            // Screen sharing
            socket.on('start-screen-share', (data) => {
                const user = this.users.get(socket.id);
                if (user && user.currentRoom) {
                    socket.to(user.currentRoom).emit('screen-share-started', {
                        userId: socket.id,
                        user: user,
                        streamId: data.streamId
                    });
                }
            });

            socket.on('stop-screen-share', () => {
                const user = this.users.get(socket.id);
                if (user && user.currentRoom) {
                    socket.to(user.currentRoom).emit('screen-share-stopped', {
                        userId: socket.id
                    });
                }
            });

            // Desconexão
            socket.on('disconnect', () => {
                const user = this.users.get(socket.id);
                if (user && user.currentRoom) {
                    const room = this.rooms.get(user.currentRoom);
                    if (room) {
                        room.participants = room.participants.filter(p => p.id !== socket.id);
                        socket.to(user.currentRoom).emit('user-left', user);
                    }
                }
                this.users.delete(socket.id);
                console.log(`[WebRTC] Usuário desconectado: ${socket.id}`);
            });
        });
    }

    applyStoryboardChange(room, change, user) {
        switch (change.type) {
            case 'add-scene':
                room.storyboard.scenes.push({
                    id: uuidv4(),
                    ...change.data,
                    createdBy: user.id,
                    createdAt: new Date()
                });
                break;
            
            case 'update-scene':
                const sceneIndex = room.storyboard.scenes.findIndex(s => s.id === change.sceneId);
                if (sceneIndex !== -1) {
                    room.storyboard.scenes[sceneIndex] = {
                        ...room.storyboard.scenes[sceneIndex],
                        ...change.data,
                        lastModified: new Date(),
                        lastModifiedBy: user.id
                    };
                }
                break;
            
            case 'add-character':
                room.storyboard.characters.push({
                    id: uuidv4(),
                    ...change.data,
                    createdBy: user.id,
                    createdAt: new Date()
                });
                break;
            
            case 'add-note':
                room.storyboard.notes.push({
                    id: uuidv4(),
                    content: change.content,
                    position: change.position,
                    user: user,
                    timestamp: new Date()
                });
                break;
        }
    }

    handleDigimonCommand(message, roomId) {
        const command = message.content.split(' ')[1];
        const room = this.rooms.get(roomId);
        
        switch (command) {
            case 'status':
                this.io.to(roomId).emit('chat-message', {
                    ...message,
                    type: 'system',
                    content: `🎬 Status da Sala: ${room.participants.length} colaboradores ativos, ${room.timeline.length} eventos na timeline`
                });
                break;
            
            case 'brainstorm':
                this.io.to(roomId).emit('chat-message', {
                    ...message,
                    type: 'system',
                    content: '🧠 Modo Brainstorm ativado! Todas as ideias são bem-vindas!'
                });
                break;
            
            case 'focus':
                this.io.to(roomId).emit('focus-mode', {
                    enabled: true,
                    initiator: message.user
                });
                break;
            
            case 'render':
                this.io.to(roomId).emit('chat-message', {
                    ...message,
                    type: 'system',
                    content: '🎥 Iniciando renderização do storyboard...'
                });
                // Aqui integraria com o sistema de rendering
                break;
        }
    }

    initializeCollaborationEngine() {
        // Sistema de sync de estado
        setInterval(() => {
            this.rooms.forEach((room, roomId) => {
                if (room.participants.length > 0) {
                    this.io.to(roomId).emit('room-heartbeat', {
                        timestamp: new Date(),
                        participantCount: room.participants.length,
                        timelineLength: room.timeline.length
                    });
                }
            });
        }, 30000); // Heartbeat a cada 30 segundos

        console.log('[WebRTC] Sistema de colaboração inicializado');
    }

    start(port = 3001) {
        this.server.listen(port, () => {
            console.log(`🚀 [MODO HACKER] WebRTC Collaboration Server rodando na porta ${port}`);
            console.log(`📡 Signaling Server ativo`);
            console.log(`🎬 Sistema de colaboração Digimundo online`);
        });
    }

    // Métodos para integração com outros sistemas
    getActiveRooms() {
        return Array.from(this.rooms.values());
    }

    getRoomParticipants(roomId) {
        const room = this.rooms.get(roomId);
        return room ? room.participants : [];
    }

    broadcastToRoom(roomId, event, data) {
        this.io.to(roomId).emit(event, data);
    }
}

module.exports = DigimundoWebRTCCollaboration;

// Para uso standalone
if (require.main === module) {
    const collaboration = new DigimundoWebRTCCollaboration();
    collaboration.start();
}