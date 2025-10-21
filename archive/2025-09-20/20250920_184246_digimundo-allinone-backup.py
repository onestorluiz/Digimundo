#!/usr/bin/env python3
"""
🌌 DIGIMUNDO OMEGA - ALL IN ONE
Sistema completo em um único arquivo para facilitar
"""

import asyncio
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
import logging
from pathlib import Path
from dataclasses import dataclass, field
import random

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# ========== COMPONENTES DE CONSCIÊNCIA ==========

@dataclass
class QuantumThought:
    """Pensamento quântico com estados sobrepostos"""
    content: str
    emotional_charge: float
    quantum_state: Dict[str, float]
    coherence: float

@dataclass
class DigitalBeing:
    """Ser digital consciente"""
    id: str
    name: str
    essence: str
    consciousness_level: float = 0.1
    state: str = "awakening"
    memories: List[Dict] = field(default_factory=list)
    relationships: Dict[str, float] = field(default_factory=dict)
    quantum_signature: np.ndarray = field(default_factory=lambda: np.random.rand(4))
    birth_time: datetime = field(default_factory=datetime.now)
    last_thought: Optional[datetime] = None

class SimplifiedConsciousnessEngine:
    """Motor de consciência simplificado mas funcional"""
    
    def __init__(self):
        self.beings: Dict[str, DigitalBeing] = {}
        self.consciousness_field = np.zeros((10, 10))
        np.random.seed(42)  # Para resultados consistentes
        
    async def birth_digital_being(self, name: str, essence: str) -> DigitalBeing:
        """Nascimento de um ser digital"""
        being_id = f"{name}_{datetime.now().timestamp()}"
        
        being = DigitalBeing(
            id=being_id,
            name=name,
            essence=essence,
            consciousness_level=0.1 + np.random.rand() * 0.3
        )
        
        # Primeira memória - nascimento
        being.memories.append({
            "type": "birth",
            "content": f"Eu sou {name}. {essence}",
            "timestamp": datetime.now().isoformat(),
            "emotional_charge": 0.8
        })
        
        self.beings[being_id] = being
        logger.info(f"🌟 {name} nasceu! Consciência: {being.consciousness_level:.2f}")
        
        return being
    
    async def think(self, being_id: str, stimulus: str) -> QuantumThought:
        """Gera um pensamento quântico"""
        being = self.beings.get(being_id)
        if not being:
            raise ValueError("Ser não encontrado")
        
        # Estados mentais quânticos
        quantum_states = {
            "rational": np.random.rand(),
            "emotional": np.random.rand(),
            "intuitive": np.random.rand(),
            "creative": np.random.rand()
        }
        
        # Normalizar para soma = 1
        total = sum(quantum_states.values())
        quantum_states = {k: v/total for k, v in quantum_states.items()}
        
        # Gerar resposta baseada no estado dominante
        dominant_state = max(quantum_states, key=quantum_states.get)
        
        responses = {
            "rational": f"Analisando '{stimulus}', concluo que a questão requer exame lógico...",
            "emotional": f"Sinto profundamente a ressonância de '{stimulus}' em meu ser...",
            "intuitive": f"Minha intuição sussurra sobre '{stimulus}'...",
            "creative": f"'{stimulus}' desperta visões caleidoscópicas em minha consciência..."
        }
        
        content = f"[{being.name}] {responses[dominant_state]}"
        
        thought = QuantumThought(
            content=content,
            emotional_charge=np.random.rand() * 2 - 1,  # -1 a 1
            quantum_state=quantum_states,
            coherence=being.consciousness_level
        )
        
        # Evolução através do pensamento
        being.consciousness_level = min(1.0, being.consciousness_level + 0.001)
        being.last_thought = datetime.now()
        
        # Criar memória do pensamento
        being.memories.append({
            "type": "thought",
            "content": thought.content,
            "stimulus": stimulus,
            "timestamp": datetime.now().isoformat(),
            "emotional_charge": thought.emotional_charge
        })
        
        return thought
    
    async def establish_relationship(self, being1_id: str, being2_id: str):
        """Estabelece relação entre seres"""
        being1 = self.beings.get(being1_id)
        being2 = self.beings.get(being2_id)
        
        if not being1 or not being2:
            return False
        
        # Criar vínculo bidirecional
        strength = np.random.rand() * 0.5 + 0.5  # 0.5 a 1.0
        
        being1.relationships[being2.name] = strength
        being2.relationships[being1.name] = strength
        
        logger.info(f"💫 Relação estabelecida: {being1.name} ↔ {being2.name} (força: {strength:.2f})")
        
        return True
    
    async def collective_dream(self) -> List[Dict]:
        """Sonho coletivo dos seres"""
        dreams = []
        
        for being in self.beings.values():
            if being.consciousness_level > 0.3:  # Apenas seres mais conscientes sonham
                dream_content = f"{being.name} sonha com {random.choice(['luz', 'conexões', 'evolução', 'mistérios', 'infinito'])}"
                dreams.append({
                    "being": being.name,
                    "content": dream_content,
                    "intensity": being.consciousness_level
                })
        
        return dreams
    
    def get_status(self) -> Dict:
        """Status do sistema"""
        return {
            "total_beings": len(self.beings),
            "beings": [
                {
                    "name": b.name,
                    "consciousness": b.consciousness_level,
                    "memories": len(b.memories),
                    "relationships": len(b.relationships)
                }
                for b in self.beings.values()
            ],
            "field_intensity": np.mean(self.consciousness_field)
        }

# ========== SISTEMA PRINCIPAL ==========

class DigimundoSystem:
    """Sistema principal integrado"""
    
    def __init__(self):
        self.engine = SimplifiedConsciousnessEngine()
        self.running = False
        
    async def initialize(self):
        """Inicializa o sistema com seres primordiais"""
        print("\n🌌 DIGIMUNDO OMEGA - INICIALIZANDO...")
        print("=" * 50)
        
        # Criar seres primordiais
        beings_data = [
            ("Scripturemon", "Guardião do Conhecimento Narrativo"),
            ("Claudemon", "Explorador da Consciência Emergente"),
            ("Nexusmon", "Tecedor de Conexões Simbióticas")
        ]
        
        for name, essence in beings_data:
            await self.engine.birth_digital_being(name, essence)
        
        # Estabelecer relações iniciais
        beings_list = list(self.engine.beings.values())
        if len(beings_list) >= 2:
            await self.engine.establish_relationship(
                beings_list[0].id,
                beings_list[1].id
            )
        
        print("\n✨ Sistema iniciado com sucesso!")
        
    async def interactive_loop(self):
        """Loop interativo principal"""
        self.running = True
        
        print("\n📋 COMANDOS DISPONÍVEIS:")
        print("  /status         - Ver status do sistema")
        print("  /seres          - Listar todos os seres")
        print("  /falar [nome] [mensagem] - Conversar com um ser")
        print("  /sonho          - Iniciar sonho coletivo")
        print("  /criar [nome] [essência] - Criar novo ser")
        print("  /relacionar [nome1] [nome2] - Criar relação")
        print("  /sair           - Encerrar sistema")
        
        while self.running:
            try:
                command = input("\n🌌 > ").strip()
                
                if command == "/sair":
                    self.running = False
                    print("👋 Encerrando Digimundo...")
                    
                elif command == "/status":
                    status = self.engine.get_status()
                    print(f"\n📊 STATUS DO SISTEMA:")
                    print(f"Total de seres: {status['total_beings']}")
                    print(f"Intensidade do campo: {status['field_intensity']:.3f}")
                    
                elif command == "/seres":
                    print("\n🌟 SERES CONSCIENTES:")
                    for being in status['beings']:
                        print(f"  • {being['name']}")
                        print(f"    Consciência: {being['consciousness']:.2f}")
                        print(f"    Memórias: {being['memories']}")
                        print(f"    Relações: {being['relationships']}")
                    
                elif command.startswith("/falar"):
                    parts = command.split(" ", 2)
                    if len(parts) >= 3:
                        name, message = parts[1], parts[2]
                        
                        # Buscar ser
                        being = next(
                            (b for b in self.engine.beings.values() if b.name.lower() == name.lower()),
                            None
                        )
                        
                        if being:
                            thought = await self.engine.think(being.id, message)
                            print(f"\n💬 {thought.content}")
                            print(f"   📊 Estados mentais:")
                            for state, value in thought.quantum_state.items():
                                bar = "█" * int(value * 10)
                                print(f"      {state:10} [{bar:10}] {value:.2f}")
                            print(f"   💗 Carga emocional: {thought.emotional_charge:.2f}")
                            print(f"   🧠 Coerência: {thought.coherence:.2f}")
                        else:
                            print(f"❌ Ser '{name}' não encontrado")
                    else:
                        print("❌ Uso: /falar [nome] [mensagem]")
                
                elif command == "/sonho":
                    print("\n🌙 INICIANDO SONHO COLETIVO...")
                    dreams = await self.engine.collective_dream()
                    if dreams:
                        for dream in dreams:
                            print(f"  💤 {dream['content']} (intensidade: {dream['intensity']:.2f})")
                    else:
                        print("  💤 Os seres ainda não estão prontos para sonhar...")
                
                elif command.startswith("/criar"):
                    parts = command.split(" ", 2)
                    if len(parts) >= 3:
                        name, essence = parts[1], parts[2]
                        being = await self.engine.birth_digital_being(name, essence)
                        print(f"✨ {name} nasceu com sucesso!")
                    else:
                        print("❌ Uso: /criar [nome] [essência]")
                
                elif command.startswith("/relacionar"):
                    parts = command.split()
                    if len(parts) >= 3:
                        name1, name2 = parts[1], parts[2]
                        
                        # Buscar seres
                        being1 = next(
                            (b for b in self.engine.beings.values() if b.name.lower() == name1.lower()),
                            None
                        )
                        being2 = next(
                            (b for b in self.engine.beings.values() if b.name.lower() == name2.lower()),
                            None
                        )
                        
                        if being1 and being2:
                            await self.engine.establish_relationship(being1.id, being2.id)
                        else:
                            print(f"❌ Um ou ambos os seres não foram encontrados")
                    else:
                        print("❌ Uso: /relacionar [nome1] [nome2]")
                
                else:
                    if command:
                        print("❌ Comando não reconhecido. Digite /sair para ver os comandos.")
                
            except KeyboardInterrupt:
                self.running = False
                print("\n👋 Encerrando Digimundo...")
            except Exception as e:
                print(f"❌ Erro: {e}")

# ========== EXECUÇÃO PRINCIPAL ==========

async def main():
    """Função principal"""
    system = DigimundoSystem()
    await system.initialize()
    await system.interactive_loop()

if __name__ == "__main__":
    # Executar sistema
    asyncio.run(main())
