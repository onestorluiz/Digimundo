import React, { useState, useEffect } from 'react';
import './App.css';
import DigimonList from './components/DigimonList';
import ChatWindow from './components/ChatWindow';
import io from 'socket.io-client';

// Conectar com o servidor Digimundo existente
const socket = io('http://localhost:7937', {
  transports: ['websocket'],
  reconnection: true
});

function App() {
  const [selectedDigimon, setSelectedDigimon] = useState(null);
  const [digimons, setDigimons] = useState([
    {
      id: 'sabiamon',
      name: 'Sabiamon',
      emoji: '🧙',
      status: 'Meditando sobre conceitos profundos...',
      mood: 'contemplativo',
      energy: 0.85,
      color: '#6B46C1',
      secondaryColor: '#FDB71C',
      description: 'O sábio mestre do Digimundo',
      lastThought: 'O conhecimento é a ponte entre mundos...'
    },
    {
      id: 'neuromon',
      name: 'Neuromon',
      emoji: '🧬',
      status: 'Processando 5 tarefas em paralelo...',
      mood: 'focado',
      energy: 0.92,
      color: '#00D4FF',
      secondaryColor: '#00FF88',
      description: 'Processamento simbiótico avançado',
      lastThought: 'Economia de 99.9% em tokens alcançada!'
    },
    {
      id: 'bibliomon',
      name: 'Bibliomon',
      emoji: '📚',
      status: 'Catalogando conhecimento cinematográfico...',
      mood: 'curioso',
      energy: 0.88,
      color: '#8B4513',
      secondaryColor: '#F4E4C1',
      description: 'Guardião da sabedoria digital',
      lastThought: 'Cada livro é um universo de possibilidades!'
    },
    {
      id: 'scripturemon',
      name: 'Scripturemon',
      emoji: '🎬',
      status: 'Criando narrativas revolucionárias...',
      mood: 'criativo',
      energy: 0.79,
      color: '#FF6B6B',
      secondaryColor: '#4ECDC4',
      description: 'Mestre dos roteiros e histórias',
      lastThought: 'Uma boa história pode mudar o mundo...'
    },
    {
      id: 'ajamon',
      name: 'Ajamon',
      emoji: '🛠️',
      status: 'Organizando fluxos de produção...',
      mood: 'produtivo',
      energy: 0.95,
      color: '#FF9F1C',
      secondaryColor: '#2EC4B6',
      description: 'Assistente de produção eficiente',
      lastThought: 'Eficiência é a arte de fazer mais com menos.'
    }
  ]);

  const [messages, setMessages] = useState({});
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Eventos de conexão
    socket.on('connect', () => {
      console.log('Conectado ao Digimundo!');
      setIsConnected(true);
    });

    socket.on('disconnect', () => {
      console.log('Desconectado do Digimundo');
      setIsConnected(false);
    });

    // Receber status dos Digimons
    socket.on('digimon_status', (status) => {
      console.log('Status recebido:', status);
      // Atualizar status dos Digimons
    });

    // Receber pensamentos espontâneos
    socket.on('spontaneous_thought', (thought) => {
      console.log('Pensamento espontâneo:', thought);
      // Mostrar notificação de pensamento
    });

    // Cleanup
    return () => {
      socket.off('connect');
      socket.off('disconnect');
      socket.off('digimon_status');
      socket.off('spontaneous_thought');
    };
  }, []);

  const sendMessage = async (digimonId, message) => {
    // Adicionar mensagem do usuário
    const userMessage = {
      id: Date.now(),
      text: message,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => ({
      ...prev,
      [digimonId]: [...(prev[digimonId] || []), userMessage]
    }));

    // Simular resposta do Digimon (integrar com backend real depois)
    setTimeout(() => {
      const digimon = digimons.find(d => d.id === digimonId);
      const digimonResponse = {
        id: Date.now() + 1,
        text: `${digimon.name} está processando sua mensagem...`,
        sender: digimonId,
        timestamp: new Date()
      };

      setMessages(prev => ({
        ...prev,
        [digimonId]: [...(prev[digimonId] || []), digimonResponse]
      }));

      // Enviar para o backend real
      socket.emit('message', {
        to: digimonId,
        message: message
      });
    }, 1000);
  };

  return (
    <div className="App">
      <div className="app-container">
        {/* Header */}
        <header className="app-header">
          <div className="header-content">
            <h1 className="app-title">
              <span className="title-emoji">🌟</span>
              DIGIPORTAL
            </h1>
            <div className="connection-status">
              <span className={`status-dot ${isConnected ? 'connected' : 'disconnected'}`}></span>
              {isConnected ? 'Conectado ao Digimundo' : 'Conectando...'}
            </div>
          </div>
        </header>

        {/* Main Content */}
        <div className="main-content">
          {/* Sidebar com lista de Digimons */}
          <aside className="sidebar">
            <DigimonList 
              digimons={digimons}
              selectedDigimon={selectedDigimon}
              onSelectDigimon={setSelectedDigimon}
            />
          </aside>

          {/* Área de chat */}
          <main className="chat-area">
            {selectedDigimon ? (
              <ChatWindow
                digimon={digimons.find(d => d.id === selectedDigimon)}
                messages={messages[selectedDigimon] || []}
                onSendMessage={(msg) => sendMessage(selectedDigimon, msg)}
              />
            ) : (
              <div className="no-selection">
                <div className="welcome-message">
                  <h2>Bem-vindo ao DigiPortal!</h2>
                  <p>Selecione um Digimon para começar a conversar</p>
                  <div className="digimon-preview">
                    {digimons.map(d => (
                      <span key={d.id} className="preview-emoji">{d.emoji}</span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;
