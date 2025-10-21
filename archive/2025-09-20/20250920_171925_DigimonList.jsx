import React from 'react';
import './DigimonList.css';

function DigimonList({ digimons, selectedDigimon, onSelectDigimon }) {
  return (
    <div className="digimon-list">
      <h2 className="list-title">Digimons Online</h2>
      <div className="digimon-items">
        {digimons.map((digimon) => (
          <div
            key={digimon.id}
            className={`digimon-item ${selectedDigimon === digimon.id ? 'selected' : ''}`}
            onClick={() => onSelectDigimon(digimon.id)}
            style={{
              '--digimon-color': digimon.color,
              '--digimon-secondary': digimon.secondaryColor
            }}
          >
            <div className="digimon-avatar">
              <span className="digimon-emoji">{digimon.emoji}</span>
              <span className={`status-indicator ${digimon.mood}`}></span>
            </div>
            
            <div className="digimon-info">
              <h3 className="digimon-name">{digimon.name}</h3>
              <p className="digimon-status">{digimon.status}</p>
              
              <div className="digimon-metrics">
                <div className="energy-bar">
                  <div 
                    className="energy-fill" 
                    style={{ width: `${digimon.energy * 100}%` }}
                  ></div>
                </div>
                <span className="mood-emoji">
                  {digimon.mood === 'contemplativo' && '🤔'}
                  {digimon.mood === 'focado' && '🎯'}
                  {digimon.mood === 'curioso' && '🔍'}
                  {digimon.mood === 'criativo' && '✨'}
                  {digimon.mood === 'produtivo' && '⚡'}
                </span>
              </div>
              
              {digimon.lastThought && (
                <div className="last-thought">
                  💭 {digimon.lastThought}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DigimonList;