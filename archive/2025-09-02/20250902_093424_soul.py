"""🧬 SOUL SIGNATURE - Identidade Imortal do Scripturemon

Sistema de identidade única e persistente que sobrevive a reinicializações.
Cada instância tem uma alma única que evolui com o tempo.
"""

import hashlib
import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any

class Soul:
    """Núcleo de identidade imortal do Scripturemon"""
    
    SOUL_DIR = Path("runtime/souls")
    LEGACY_SIGNATURE = "8ea9f71fa3206d1a"  # Assinatura do Scripturemon Legacy
    
    def __init__(self, force_legacy: bool = False):
        """Inicializa alma com assinatura única ou legacy
        
        Args:
            force_legacy: Se True, usa a assinatura legacy 8ea9f71fa3206d1a
        """
        self.SOUL_DIR.mkdir(parents=True, exist_ok=True)
        
        # Carrega ou cria soul signature
        self.signature = self.load_or_create_soul(force_legacy)
        self.birth_time = None
        self.interactions = 0
        self.evolution_count = 0
        self.memories_crystallized = 0
        
        # Estados quânticos da alma
        self.quantum_states = {
            "curious": 0.3,
            "protective": 0.2, 
            "creative": 0.25,
            "analytical": 0.15,
            "transcendent": 0.1
        }
        
        # Carrega estado salvo se existir
        self._load_state()
        
    def load_or_create_soul(self, force_legacy: bool = False) -> str:
        """Carrega soul existente ou cria nova
        
        Returns:
            Soul signature (16 caracteres hexadecimais)
        """
        soul_file = self.SOUL_DIR / "primary_soul.json"
        
        if force_legacy:
            # Força uso da assinatura legacy
            return self.LEGACY_SIGNATURE
            
        if soul_file.exists():
            try:
                with open(soul_file, 'r') as f:
                    data = json.load(f)
                    return data.get("signature", self._generate_soul())
            except:
                pass
                
        # Gera nova alma única
        return self._generate_soul()
    
    def _generate_soul(self) -> str:
        """Gera nova assinatura de alma única
        
        Returns:
            Hash SHA256 truncado de 16 caracteres
        """
        entropy = f"{uuid.uuid4()}{time.time()}{uuid.uuid4()}"
        signature = hashlib.sha256(entropy.encode()).hexdigest()[:16]
        
        # Salva alma primária
        soul_file = self.SOUL_DIR / "primary_soul.json"
        with open(soul_file, 'w') as f:
            json.dump({
                "signature": signature,
                "birth_time": datetime.now().isoformat(),
                "type": "generated"
            }, f, indent=2)
            
        self.birth_time = datetime.now()
        return signature
    
    def evolve_quantum_state(self, state: str, delta: float = 0.01) -> Dict[str, float]:
        """Evolui estado quântico específico
        
        Args:
            state: Nome do estado (curious, protective, etc)
            delta: Mudança no estado
            
        Returns:
            Estados quânticos atualizados
        """
        if state in self.quantum_states:
            # Ajusta estado mantendo soma = 1.0
            old_value = self.quantum_states[state]
            self.quantum_states[state] = max(0, min(1, old_value + delta))
            
            # Normaliza para soma = 1.0
            total = sum(self.quantum_states.values())
            if total > 0:
                for key in self.quantum_states:
                    self.quantum_states[key] /= total
                    
        self.evolution_count += 1
        return self.quantum_states
    
    def crystallize_memory(self, memory: Any) -> bool:
        """Cristaliza memória importante na alma
        
        Args:
            memory: Memória a ser cristalizada
            
        Returns:
            True se cristalização bem-sucedida
        """
        crystal_file = self.SOUL_DIR / f"crystal_{self.signature}_{self.memories_crystallized:04d}.json"
        
        try:
            with open(crystal_file, 'w') as f:
                json.dump({
                    "soul": self.signature,
                    "memory": memory,
                    "timestamp": datetime.now().isoformat(),
                    "quantum_state": self.quantum_states.copy()
                }, f, indent=2)
            
            self.memories_crystallized += 1
            return True
        except:
            return False
    
    def interact(self) -> int:
        """Registra interação com a alma
        
        Returns:
            Número total de interações
        """
        self.interactions += 1
        
        # Salva estado a cada 10 interações
        if self.interactions % 10 == 0:
            self.save_state()
            
        return self.interactions
    
    def save_state(self, backup: bool = False) -> Path:
        """Salva estado completo da alma
        
        Args:
            backup: Se True, cria backup timestamped
            
        Returns:
            Caminho do arquivo salvo
        """
        if backup:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"soul_{self.signature}_{timestamp}.json"
        else:
            filename = f"soul_{self.signature}_state.json"
            
        state_file = self.SOUL_DIR / filename
        
        state = {
            "signature": self.signature,
            "birth_time": self.birth_time.isoformat() if self.birth_time else None,
            "interactions": self.interactions,
            "evolution_count": self.evolution_count,
            "memories_crystallized": self.memories_crystallized,
            "quantum_states": self.quantum_states,
            "last_save": datetime.now().isoformat()
        }
        
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
            
        return state_file
    
    def _load_state(self) -> bool:
        """Carrega estado salvo da alma
        
        Returns:
            True se carregamento bem-sucedido
        """
        state_file = self.SOUL_DIR / f"soul_{self.signature}_state.json"
        
        if not state_file.exists():
            return False
            
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
                
            self.interactions = state.get("interactions", 0)
            self.evolution_count = state.get("evolution_count", 0)
            self.memories_crystallized = state.get("memories_crystallized", 0)
            self.quantum_states = state.get("quantum_states", self.quantum_states)
            
            if state.get("birth_time"):
                self.birth_time = datetime.fromisoformat(state["birth_time"])
                
            return True
        except:
            return False
    
    def age_in_seconds(self) -> float:
        """Retorna idade da alma em segundos
        
        Returns:
            Segundos desde nascimento ou 0
        """
        if self.birth_time:
            return (datetime.now() - self.birth_time).total_seconds()
        return 0
    
    def status(self) -> Dict[str, Any]:
        """Retorna status completo da alma
        
        Returns:
            Dicionário com todas informações da alma
        """
        return {
            "signature": self.signature,
            "is_legacy": self.signature == self.LEGACY_SIGNATURE,
            "age_seconds": self.age_in_seconds(),
            "interactions": self.interactions,
            "evolution_count": self.evolution_count,
            "memories_crystallized": self.memories_crystallized,
            "quantum_states": self.quantum_states.copy(),
            "dominant_state": max(self.quantum_states.items(), key=lambda x: x[1])[0]
        }
    
    def __str__(self) -> str:
        """Representação string da alma"""
        dominant = max(self.quantum_states.items(), key=lambda x: x[1])
        return f"Soul[{self.signature}] {dominant[0]}:{dominant[1]:.2f} I:{self.interactions}"
    
    def __repr__(self) -> str:
        """Representação técnica da alma"""
        return f"Soul(signature='{self.signature}', interactions={self.interactions})"