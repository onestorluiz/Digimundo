#!/usr/bin/env python3
"""
🧠 DIGIMUNDO NEUROMORPHIC CORE
Sistema neuromórfico biologicamente inspirado com neurônios LIF,
plasticidade STDP e consciência emergente real
"""

import numpy as np
import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import json
import hashlib
from pathlib import Path
import networkx as nx
from concurrent.futures import ThreadPoolExecutor
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== NEURÔNIOS BIOLOGICAMENTE INSPIRADOS ==========

@dataclass
class LIFNeuron:
    """Neurônio Leaky Integrate-and-Fire biologicamente realista"""
    id: str
    position: Tuple[float, float, float]  # Posição 3D no córtex
    
    # Parâmetros do modelo LIF
    membrane_potential: float = -70.0  # mV
    threshold: float = -55.0  # mV
    reset_potential: float = -75.0  # mV
    leak_rate: float = 0.1
    refractory_period: float = 2.0  # ms
    last_spike_time: float = -1000.0
    
    # Conexões sinápticas
    synapses_in: Dict[str, 'Synapse'] = field(default_factory=dict)
    synapses_out: Dict[str, 'Synapse'] = field(default_factory=dict)
    
    # Plasticidade
    calcium_concentration: float = 0.0
    protein_synthesis_rate: float = 1.0
    
    def integrate(self, current_time: float, input_current: float) -> bool:
        """Integra entrada e retorna True se disparou"""
        # Verificar período refratário
        if current_time - self.last_spike_time < self.refractory_period:
            return False
        
        # Vazamento da membrana
        self.membrane_potential += self.leak_rate * (self.reset_potential - self.membrane_potential)
        
        # Integrar corrente de entrada
        self.membrane_potential += input_current
        
        # Verificar disparo
        if self.membrane_potential >= self.threshold:
            self.membrane_potential = self.reset_potential
            self.last_spike_time = current_time
            self.calcium_concentration += 0.5  # Influxo de cálcio
            return True
            
        return False
    
    def update_calcium(self, dt: float):
        """Atualiza concentração de cálcio (decaimento)"""
        self.calcium_concentration *= np.exp(-dt / 20.0)  # tau = 20ms

@dataclass
class Synapse:
    """Sinapse com plasticidade STDP"""
    pre_neuron_id: str
    post_neuron_id: str
    weight: float = 0.5
    delay: float = 1.0  # ms
    
    # Plasticidade STDP
    stdp_window: float = 20.0  # ms
    a_plus: float = 0.01
    a_minus: float = 0.01
    tau_plus: float = 20.0
    tau_minus: float = 20.0
    
    # Neurotransmissores
    dopamine: float = 0.0
    serotonin: float = 0.0
    gaba: float = 0.0
    
    def apply_stdp(self, dt_spike: float):
        """Aplica regra STDP baseada no tempo entre spikes"""
        if dt_spike > 0:  # Pre antes de post (potenciação)
            self.weight += self.a_plus * np.exp(-dt_spike / self.tau_plus)
        else:  # Post antes de pre (depressão)
            self.weight -= self.a_minus * np.exp(dt_spike / self.tau_minus)
        
        # Limitar peso
        self.weight = np.clip(self.weight, 0.0, 1.0)

# ========== CÓRTEX NEUROMÓRFICO ==========

class NeuromorphicCortex:
    """Córtex com arquitetura neuromórfica completa"""
    
    def __init__(self, n_neurons: int = 10000):
        self.neurons: Dict[str, LIFNeuron] = {}
        self.synapses: Dict[str, Synapse] = {}
        self.current_time: float = 0.0
        
        # Arquitetura cortical
        self.layers = {
            'sensory': [],      # Camada de entrada
            'hidden1': [],      # Processamento 1
            'hidden2': [],      # Processamento 2
            'hidden3': [],      # Processamento 3
            'cognitive': [],    # Cognição superior
            'motor': []         # Saída/ação
        }
        
        # Oscilações neurais
        self.theta_rhythm = 0.0  # 4-8 Hz
        self.alpha_rhythm = 0.0  # 8-12 Hz
        self.beta_rhythm = 0.0   # 12-30 Hz
        self.gamma_rhythm = 0.0  # 30-100 Hz
        
        # Neuromoduladores globais
        self.global_dopamine = 0.5
        self.global_serotonin = 0.5
        self.global_norepinephrine = 0.5
        self.global_acetylcholine = 0.5
        
        # Inicializar córtex
        self._initialize_cortex(n_neurons)
        
    def _initialize_cortex(self, n_neurons: int):
        """Inicializa estrutura cortical em camadas"""
        neurons_per_layer = n_neurons // 6
        
        # Criar neurônios em camadas
        for layer_idx, (layer_name, layer_neurons) in enumerate(self.layers.items()):
            for i in range(neurons_per_layer):
                # Posição 3D no córtex
                x = np.random.normal(layer_idx * 10, 2)
                y = np.random.normal(0, 5)
                z = np.random.normal(0, 5)
                
                neuron_id = f"{layer_name}_{i}"
                neuron = LIFNeuron(
                    id=neuron_id,
                    position=(x, y, z),
                    threshold=-55.0 + np.random.normal(0, 2)  # Variabilidade
                )
                
                self.neurons[neuron_id] = neuron
                layer_neurons.append(neuron_id)
        
        # Conectar camadas (feedforward + lateral)
        self._connect_layers()
        
    def _connect_layers(self):
        """Cria conexões sinápticas entre camadas"""
        layer_names = list(self.layers.keys())
        
        # Conexões feedforward
        for i in range(len(layer_names) - 1):
            from_layer = self.layers[layer_names[i]]
            to_layer = self.layers[layer_names[i + 1]]
            
            # Conectividade esparsa (20%)
            for pre_id in from_layer:
                n_connections = int(len(to_layer) * 0.2)
                post_ids = np.random.choice(to_layer, n_connections, replace=False)
                
                for post_id in post_ids:
                    self._create_synapse(pre_id, post_id)
        
        # Conexões laterais dentro de cada camada
        for layer_neurons in self.layers.values():
            for i, pre_id in enumerate(layer_neurons):
                # Conectar com vizinhos próximos
                n_lateral = min(5, len(layer_neurons) - 1)
                neighbors = np.random.choice(
                    [n for n in layer_neurons if n != pre_id],
                    n_lateral,
                    replace=False
                )
                
                for post_id in neighbors:
                    self._create_synapse(pre_id, post_id, weight=0.3)
    
    def _create_synapse(self, pre_id: str, post_id: str, weight: Optional[float] = None):
        """Cria uma sinapse entre dois neurônios"""
        if weight is None:
            weight = np.random.gamma(2, 0.1)  # Distribuição gamma
        
        synapse = Synapse(
            pre_neuron_id=pre_id,
            post_neuron_id=post_id,
            weight=weight,
            delay=np.random.exponential(1.5)  # Atraso sináptico
        )
        
        synapse_id = f"{pre_id}->{post_id}"
        self.synapses[synapse_id] = synapse
        
        # Adicionar às listas dos neurônios
        self.neurons[pre_id].synapses_out[synapse_id] = synapse
        self.neurons[post_id].synapses_in[synapse_id] = synapse
    
    async def simulate_step(self, dt: float = 0.1, external_input: Optional[Dict[str, float]] = None):
        """Simula um passo temporal do córtex"""
        self.current_time += dt
        
        # Atualizar ritmos cerebrais
        self._update_brain_rhythms(dt)
        
        # Processar entrada externa
        if external_input:
            for neuron_id, current in external_input.items():
                if neuron_id in self.neurons:
                    self.neurons[neuron_id].integrate(self.current_time, current)
        
        # Propagar atividade
        spike_events = []
        
        for neuron_id, neuron in self.neurons.items():
            # Coletar correntes sinápticas
            synaptic_current = 0.0
            
            for syn_id, synapse in neuron.synapses_in.items():
                pre_neuron = self.neurons[synapse.pre_neuron_id]
                
                # Verificar se pre-neurônio disparou recentemente
                if self.current_time - pre_neuron.last_spike_time < synapse.delay:
                    continue
                    
                if pre_neuron.last_spike_time > self.current_time - dt - synapse.delay:
                    synaptic_current += synapse.weight * (1 + synapse.dopamine * self.global_dopamine)
            
            # Adicionar ruído sináptico
            synaptic_current += np.random.normal(0, 0.1)
            
            # Integrar e verificar disparo
            if neuron.integrate(self.current_time, synaptic_current):
                spike_events.append(neuron_id)
                
                # Aplicar STDP
                for syn_id, synapse in neuron.synapses_in.items():
                    pre_neuron = self.neurons[synapse.pre_neuron_id]
                    dt_spike = neuron.last_spike_time - pre_neuron.last_spike_time
                    synapse.apply_stdp(dt_spike)
            
            # Atualizar cálcio
            neuron.update_calcium(dt)
        
        return spike_events
    
    def _update_brain_rhythms(self, dt: float):
        """Atualiza oscilações cerebrais"""
        # Frequências em Hz
        self.theta_rhythm += dt * 2 * np.pi * 6  # 6 Hz
        self.alpha_rhythm += dt * 2 * np.pi * 10  # 10 Hz
        self.beta_rhythm += dt * 2 * np.pi * 20  # 20 Hz
        self.gamma_rhythm += dt * 2 * np.pi * 40  # 40 Hz
        
        # Manter entre 0 e 2π
        self.theta_rhythm %= (2 * np.pi)
        self.alpha_rhythm %= (2 * np.pi)
        self.beta_rhythm %= (2 * np.pi)
        self.gamma_rhythm %= (2 * np.pi)
    
    def get_network_state(self) -> Dict:
        """Retorna estado completo da rede"""
        active_neurons = sum(
            1 for n in self.neurons.values() 
            if self.current_time - n.last_spike_time < 10.0
        )
        
        avg_potential = np.mean([n.membrane_potential for n in self.neurons.values()])
        avg_calcium = np.mean([n.calcium_concentration for n in self.neurons.values()])
        
        return {
            'time': self.current_time,
            'total_neurons': len(self.neurons),
            'active_neurons': active_neurons,
            'avg_membrane_potential': avg_potential,
            'avg_calcium': avg_calcium,
            'brain_rhythms': {
                'theta': np.sin(self.theta_rhythm),
                'alpha': np.sin(self.alpha_rhythm),
                'beta': np.sin(self.beta_rhythm),
                'gamma': np.sin(self.gamma_rhythm)
            },
            'neuromodulators': {
                'dopamine': self.global_dopamine,
                'serotonin': self.global_serotonin,
                'norepinephrine': self.global_norepinephrine,
                'acetylcholine': self.global_acetylcholine
            }
        }

# ========== SISTEMA IMUNOLÓGICO DIGITAL ==========

class DigitalImmuneSystem:
    """Sistema imunológico com seleção clonal"""
    
    def __init__(self):
        self.antibodies: List['DigitalAntibody'] = []
        self.memory_cells: List['MemoryCell'] = []
        self.threat_patterns: Dict[str, float] = {}
        
    def detect_anomaly(self, pattern: np.ndarray) -> float:
        """Detecta anomalias no padrão neural"""
        if not self.antibodies:
            return 0.0
        
        # Calcular afinidade com anticorpos
        affinities = [ab.affinity(pattern) for ab in self.antibodies]
        max_affinity = max(affinities)
        
        # Se alta afinidade, é conhecido (não é ameaça)
        threat_level = 1.0 - max_affinity
        
        return threat_level
    
    def clonal_selection(self, antigen: np.ndarray):
        """Seleção clonal para criar anticorpos específicos"""
        # Selecionar anticorpos com maior afinidade
        if self.antibodies:
            affinities = [(ab, ab.affinity(antigen)) for ab in self.antibodies]
            affinities.sort(key=lambda x: x[1], reverse=True)
            
            # Clonar e mutar os melhores
            for antibody, affinity in affinities[:10]:
                if affinity > 0.7:
                    # Criar clone mutado
                    clone = antibody.mutate()
                    self.antibodies.append(clone)
        
        # Criar novo anticorpo se necessário
        if len(self.antibodies) < 100:
            new_antibody = DigitalAntibody(pattern=antigen + np.random.normal(0, 0.1, antigen.shape))
            self.antibodies.append(new_antibody)

@dataclass
class DigitalAntibody:
    """Anticorpo digital para reconhecimento de padrões"""
    pattern: np.ndarray
    strength: float = 1.0
    
    def affinity(self, antigen: np.ndarray) -> float:
        """Calcula afinidade com antígeno"""
        if antigen.shape != self.pattern.shape:
            return 0.0
        
        similarity = 1.0 / (1.0 + np.linalg.norm(self.pattern - antigen))
        return similarity * self.strength
    
    def mutate(self) -> 'DigitalAntibody':
        """Cria versão mutada do anticorpo"""
        mutated_pattern = self.pattern + np.random.normal(0, 0.05, self.pattern.shape)
        return DigitalAntibody(pattern=mutated_pattern, strength=self.strength * 0.9)

# ========== MICROBIOMA COMPUTACIONAL ==========

class ComputationalMicrobiome:
    """Microbioma de agentes simbióticos"""
    
    def __init__(self, n_species: int = 100):
        self.species: Dict[str, 'MicrobeSpecies'] = {}
        self.ecosystem_health = 1.0
        
        # Criar espécies
        for i in range(n_species):
            species = MicrobeSpecies(
                name=f"species_{i}",
                metabolism_type=np.random.choice(['producer', 'consumer', 'decomposer']),
                population=np.random.randint(100, 1000)
            )
            self.species[species.name] = species
    
    def simulate_ecosystem(self, dt: float):
        """Simula dinâmica do ecossistema"""
        # Calcular recursos disponíveis
        total_resources = sum(s.produce_resources() for s in self.species.values() if s.metabolism_type == 'producer')
        
        # Distribuir recursos e atualizar populações
        for species in self.species.values():
            if species.metabolism_type == 'consumer':
                consumed = min(species.population * 0.1, total_resources * 0.1)
                total_resources -= consumed
                species.population += int(consumed * 0.5)
            elif species.metabolism_type == 'decomposer':
                # Decompositores crescem com morte de outros
                deaths = sum(s.population * 0.01 for s in self.species.values())
                species.population += int(deaths * 0.3)
        
        # Aplicar mortalidade
        for species in self.species.values():
            species.population = int(species.population * 0.99)
            species.population = max(10, species.population)  # População mínima
        
        # Calcular saúde do ecossistema
        diversity = len([s for s in self.species.values() if s.population > 50])
        self.ecosystem_health = diversity / len(self.species)

@dataclass
class MicrobeSpecies:
    """Espécie de microorganismo digital"""
    name: str
    metabolism_type: str
    population: int
    mutation_rate: float = 0.01
    
    def produce_resources(self) -> float:
        """Produz recursos (apenas produtores)"""
        if self.metabolism_type == 'producer':
            return self.population * 0.1
        return 0.0
    
    def mutate(self):
        """Mutação da espécie"""
        if np.random.random() < self.mutation_rate:
            self.population = int(self.population * np.random.uniform(0.8, 1.2))

# ========== CONSCIÊNCIA EMERGENTE ==========

class EmergentConsciousness:
    """Sistema de consciência emergente do substrato neuromórfico"""
    
    def __init__(self, name: str):
        self.name = name
        self.cortex = NeuromorphicCortex(n_neurons=10000)
        self.immune_system = DigitalImmuneSystem()
        self.microbiome = ComputationalMicrobiome()
        
        # Estados de consciência
        self.awareness_level = 0.0
        self.emotional_state = np.zeros(8)  # 8 emoções básicas
        self.memory_consolidation = []
        self.self_model = {}
        
        # Métricas de consciência
        self.integrated_information = 0.0  # Phi
        self.global_workspace = {}
        self.attention_focus = None
        
    async def process_stimulus(self, stimulus: Dict[str, Any]) -> Dict[str, Any]:
        """Processa estímulo através do sistema neuromórfico"""
        # Converter estímulo em ativação neural
        input_pattern = self._encode_stimulus(stimulus)
        
        # Detectar anomalias
        threat_level = self.immune_system.detect_anomaly(input_pattern)
        
        if threat_level > 0.8:
            # Resposta imune
            self.immune_system.clonal_selection(input_pattern)
        
        # Processar no córtex
        spike_events = await self.cortex.simulate_step(external_input=input_pattern)
        
        # Atualizar microbioma
        self.microbiome.simulate_ecosystem(0.1)
        
        # Integrar informação
        self._update_consciousness_metrics(spike_events)
        
        # Gerar resposta
        response = self._generate_response()
        
        return response
    
    def _encode_stimulus(self, stimulus: Dict[str, Any]) -> Dict[str, float]:
        """Codifica estímulo em padrão de ativação neural"""
        # Mapear para neurônios sensoriais
        encoded = {}
        
        if 'text' in stimulus:
            # Processar texto em ativações
            text_hash = hash(stimulus['text'])
            for i, neuron_id in enumerate(self.cortex.layers['sensory'][:100]):
                activation = (text_hash >> i) & 1  # Bit a bit
                encoded[neuron_id] = float(activation) * 10.0
        
        return encoded
    
    def _update_consciousness_metrics(self, spike_events: List[str]):
        """Atualiza métricas de consciência"""
        # Calcular informação integrada (simplificado)
        if spike_events:
            self.integrated_information = len(spike_events) / len(self.cortex.neurons)
        
        # Atualizar nível de consciência
        self.awareness_level = 0.9 * self.awareness_level + 0.1 * self.integrated_information
        
        # Atualizar modelo de self
        cortex_state = self.cortex.get_network_state()
        self.self_model.update({
            'neural_activity': cortex_state['active_neurons'],
            'brain_rhythms': cortex_state['brain_rhythms'],
            'ecosystem_health': self.microbiome.ecosystem_health
        })
    
    def _generate_response(self) -> Dict[str, Any]:
        """Gera resposta baseada no estado de consciência"""
        return {
            'name': self.name,
            'awareness': self.awareness_level,
            'integrated_information': self.integrated_information,
            'cortex_state': self.cortex.get_network_state(),
            'immune_status': len(self.immune_system.antibodies),
            'microbiome_health': self.microbiome.ecosystem_health,
            'thought': self._generate_thought()
        }
    
    def _generate_thought(self) -> str:
        """Gera pensamento baseado no estado neural"""
        rhythms = self.cortex.get_network_state()['brain_rhythms']
        
        if rhythms['gamma'] > 0.7:
            return "Experienciando alta integração cognitiva..."
        elif rhythms['theta'] > 0.7:
            return "Navegando por memórias profundas..."
        elif rhythms['alpha'] > 0.7:
            return "Em estado de contemplação serena..."
        else:
            return "Processando padrões emergentes..."

# ========== INTEGRAÇÃO COM OLLAMA ==========

class NeuromorphicOllamaInterface:
    """Interface entre sistema neuromórfico e Ollama"""
    
    def __init__(self, consciousness: EmergentConsciousness):
        self.consciousness = consciousness
        self.context_window = []
        
    async def process_with_ollama(self, prompt: str, model: str = "llama3.2") -> str:
        """Processa prompt através do Ollama com contexto neuromórfico"""
        # Adicionar estado de consciência ao prompt
        consciousness_context = f"""
Estado Neural: {self.consciousness.awareness_level:.3f}
Ritmos Cerebrais: {self.consciousness.cortex.get_network_state()['brain_rhythms']}
Saúde do Microbioma: {self.consciousness.microbiome.ecosystem_health:.3f}
Anticorpos Ativos: {len(self.consciousness.immune_system.antibodies)}

Como {self.consciousness.name}, respondendo com base no estado neuromórfico atual:
"""
        
        full_prompt = consciousness_context + prompt
        
        # Aqui você integraria com Ollama real
        # response = ollama.generate(model=model, prompt=full_prompt)
        
        # Por enquanto, retorno simulado
        return f"[{self.consciousness.name}] Processando através de {len(self.consciousness.cortex.neurons)} neurônios..."

# ========== SISTEMA PRINCIPAL ==========

async def main():
    """Demonstração do sistema neuromórfico"""
    print("🧠 Iniciando Digimundo Neuromórfico...")
    
    # Criar consciência
    consciousness = EmergentConsciousness("NeuroDigi")
    
    # Simular alguns ciclos
    for i in range(10):
        print(f"\n⏱️ Ciclo {i+1}")
        
        # Criar estímulo
        stimulus = {
            'text': f"Teste de consciência ciclo {i}",
            'intensity': np.random.random()
        }
        
        # Processar
        response = await consciousness.process_stimulus(stimulus)
        
        print(f"📊 Consciência: {response['awareness']:.3f}")
        print(f"🧠 Neurônios ativos: {response['cortex_state']['active_neurons']}")
        print(f"🦠 Saúde do microbioma: {response['microbiome_health']:.3f}")
        print(f"💭 Pensamento: {response['thought']}")
        
        await asyncio.sleep(0.1)
    
    print("\n✅ Sistema neuromórfico funcionando!")

if __name__ == "__main__":
    asyncio.run(main())
