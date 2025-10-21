import React, { useState, useRef, useEffect } from 'react';
import './ChatWindow.css';
import { FiSend } from 'react-icons/fi';

function ChatWindow({ digimon, messages, onSendMessage }) {
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (inputMessage.trim()) {
      onSendMessage(inputMessage);
      setInputMessage('');
      
      // Simular "digitando"
      setIsTyping(true);
      setTimeout(() => setIsTyping(false), 2000);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('pt-BR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div 
      className="chat-window"
      style={{
        '--digimon-color': digimon.color,
        '--digimon-secondary': digimon.secondaryColor
      }}
    >
      {/* Header do chat */}
      <div className="chat-header">
        <div className="header-left">
          <span className="header-emoji">{digimon.emoji}</span>
          <div className="header-info">
            <h2 className="header-name">{digimon.name}</h2>
            <p className="header-description">{digimon.description}</p>
          </div>
        </div>
        <div className="header-right">
          <div className="personality-indicators">
            <span className="mood-indicator">
              Humor: {digimon.mood}
            </span>
            <div className="energy-indicator">
              <span>Energia:</span>
              <div className="mini-energy-bar">
                <div 
                  className="mini-energy-fill" 
                  style={{ width: `${digimon.energy * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Área de mensagens */}
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="no-messages">
            <div className="welcome-chat">
              <span className="welcome-emoji">{digimon.emoji}</span>
              <h3>Conversa com {digimon.name}</h3>
              <p>{digimon.description}</p>
              <p className="start-hint">Digite uma mensagem para começar...</p>
            </div>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.sender === 'user' ? 'user-message' : 'digimon-message'}`}
              >
                {message.sender !== 'user' && (
                  <span className="message-avatar">{digimon.emoji}</span>
                )}
                <div className="message-content">
                  <p className="message-text">{message.text}</p>
                  <span className="message-time">
                    {formatTime(message.timestamp)}
                  </span>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="typing-indicator">
                <span className="typing-avatar">{digimon.emoji}</span>
                <div className="typing-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <span className="typing-text">{digimon.name} está digitando...</span>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input de mensagem */}
      <div className="message-input-container">
        <div className="input-wrapper">
          <textarea
            className="message-input"
            placeholder={`Conversar com ${digimon.name}...`}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            rows="1"
          />
          <button 
            className="send-button"
            onClick={handleSend}
            disabled={!inputMessage.trim()}
          >
            <FiSend />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatWindow;