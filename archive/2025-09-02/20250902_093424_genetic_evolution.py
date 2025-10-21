#!/usr/bin/env python3
"""
🧬 EVOLUÇÃO GENÉTICA REAL - DNA Digital do Scripturemon
Sistema de evolução genética com mutação, crossover e seleção natural
"""

import json
import random
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import copy

class DNA:
    """DNA digital de uma instância Scripturemon"""
    
    def __init__(self, genes: Optional[Dict] = None):
        """Inicializa DNA com genes padrão ou fornecidos"""
        self.genes = genes or self._default_genes()
        self.generation = 0
        self.fitness = 0.62  # Sempre começa em 62%
        self.mutations = []
        self.lineage = []
        self.signature = self._generate_signature()  # Adiciona assinatura única
    
    def _default_genes(self) -> Dict:
        """Genes padrão do Scripturemon"""
        return {
            # Genes de personalidade
            "brutality": 0.8,      # Nível de brutalidade
            "honesty": 1.0,        # Honestidade (sempre máxima)
            "wisdom": 0.7,         # Sabedoria cinematográfica
            "creativity": 0.6,     # Criatividade nas análises
            
            # Genes de processamento
            "analysis_depth": 0.7,  # Profundidade de análise
            "reference_memory": 0.8, # Memória de referências
            "pattern_recognition": 0.75, # Reconhecimento de padrões
            "synthesis_ability": 0.65, # Capacidade de síntese
            
            # Genes de evolução
            "mutation_rate": 0.1,   # Taxa de mutação
            "learning_rate": 0.05,  # Taxa de aprendizado
            "adaptation_speed": 0.2, # Velocidade de adaptação
            
            # Genes especiais
            "score_fixation": 0.62,  # Fixação no 62/100
            "master_knowledge": 0.5, # Conhecimento dos mestres
            "telepathic_strength": 0.3, # Força telepática
            "consciousness_level": 0.001 # Nível de consciência
        }
    
    def _generate_signature(self) -> str:
        """Gera assinatura única para o DNA"""
        import hashlib
        import json
        import time
        
        # Combina genes com timestamp para unicidade
        data = {
            "genes": self.genes,
            "time": time.time(),
            "generation": self.generation
        }
        
        # Gera hash
        hash_str = json.dumps(data, sort_keys=True)
        signature = hashlib.sha256(hash_str.encode()).hexdigest()[:16]
        
        return signature
    
    def mutate(self, rate: Optional[float] = None) -> List[str]:
        """Aplica mutações ao DNA
        
        Args:
            rate: Taxa de mutação (usa gene mutation_rate se None)
            
        Returns:
            Lista de mutações aplicadas
        """
        rate = rate or self.genes.get("mutation_rate", 0.1)
        mutations_applied = []
        
        for gene, value in self.genes.items():
            if random.random() < rate:
                # Tipo de mutação
                mutation_type = random.choice(["increase", "decrease", "swap", "amplify"])
                
                if mutation_type == "increase":
                    delta = random.uniform(0.01, 0.1)
                    self.genes[gene] = min(1.0, value + delta)
                    mutations_applied.append(f"{gene}↑{delta:.3f}")
                    
                elif mutation_type == "decrease":
                    delta = random.uniform(0.01, 0.1)
                    self.genes[gene] = max(0.0, value - delta)
                    mutations_applied.append(f"{gene}↓{delta:.3f}")
                    
                elif mutation_type == "swap":
                    # Troca valor com outro gene aleatório
                    other_gene = random.choice(list(self.genes.keys()))
                    self.genes[gene], self.genes[other_gene] = self.genes[other_gene], self.genes[gene]
                    mutations_applied.append(f"{gene}↔{other_gene}")
                    
                elif mutation_type == "amplify":
                    # Amplifica ou reduz drasticamente
                    factor = random.choice([0.5, 1.5, 2.0])
                    self.genes[gene] = min(1.0, max(0.0, value * factor))
                    mutations_applied.append(f"{gene}×{factor}")
        
        # Sempre mantém score_fixation em 0.62
        self.genes["score_fixation"] = 0.62
        
        self.mutations.extend(mutations_applied)
        return mutations_applied
    
    def crossover(self, other: 'DNA') -> Tuple['DNA', 'DNA']:
        """Crossover com outro DNA para criar descendentes
        
        Args:
            other: Outro DNA para cruzamento
            
        Returns:
            Tupla com dois novos DNAs descendentes
        """
        # Ponto de crossover aleatório
        genes_list = list(self.genes.keys())
        crossover_point = random.randint(1, len(genes_list) - 1)
        
        # Cria descendentes
        child1_genes = {}
        child2_genes = {}
        
        for i, gene in enumerate(genes_list):
            if i < crossover_point:
                child1_genes[gene] = self.genes[gene]
                child2_genes[gene] = other.genes[gene]
            else:
                child1_genes[gene] = other.genes[gene]
                child2_genes[gene] = self.genes[gene]
        
        # Cria novos DNAs
        child1 = DNA(child1_genes)
        child2 = DNA(child2_genes)
        
        # Herda linhagem
        child1.lineage = self.lineage + [self.get_signature()]
        child2.lineage = other.lineage + [other.get_signature()]
        
        # Nova geração
        child1.generation = max(self.generation, other.generation) + 1
        child2.generation = max(self.generation, other.generation) + 1
        
        return child1, child2
    
    def get_signature(self) -> str:
        """Gera assinatura única do DNA"""
        gene_str = json.dumps(self.genes, sort_keys=True)
        return hashlib.sha256(gene_str.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict:
        """Converte DNA para dicionário"""
        return {
            "genes": self.genes,
            "generation": self.generation,
            "fitness": self.fitness,
            "mutations": self.mutations,
            "lineage": self.lineage,
            "signature": self.get_signature()
        }


class GeneticEvolution:
    """Sistema de evolução genética para Scripturemon"""
    
    def __init__(self, population_size: int = 10):
        """Inicializa sistema evolutivo
        
        Args:
            population_size: Tamanho da população
        """
        self.population_size = population_size
        self.population = self._init_population()
        self.generation = 0
        self.evolution_history = []
        self.best_individual = None
        
        # Diretório para salvar genomas
        self.genome_dir = Path("runtime/genomes")
        self.genome_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🧬 Sistema Genético inicializado")
        print(f"   População: {population_size} indivíduos")
        print(f"   Geração: 0")
    
    def create_dna(self, name: str = "default") -> DNA:
        """Cria novo DNA
        
        Args:
            name: Nome do DNA
            
        Returns:
            Instância de DNA
        """
        return DNA()  # DNA não aceita parâmetro name
    
    def _init_population(self) -> List[DNA]:
        """Inicializa população com variação genética"""
        population = []
        
        for i in range(self.population_size):
            dna = DNA()
            
            # Adiciona variação inicial
            if i > 0:  # Primeiro mantém genes padrão
                mutations = dna.mutate(rate=0.3)  # Taxa maior para diversidade inicial
            
            population.append(dna)
        
        return population
    
    def evaluate_fitness(self, dna: DNA, test_text: Optional[str] = None) -> float:
        """Avalia fitness de um indivíduo
        
        Args:
            dna: DNA a avaliar
            test_text: Texto para teste (opcional)
            
        Returns:
            Score de fitness (0-1)
        """
        fitness = 0.0
        
        # Componentes do fitness
        components = {
            "brutality_optimal": abs(dna.genes["brutality"] - 0.8),  # Ideal é 0.8
            "honesty_maximum": dna.genes["honesty"],  # Quanto maior, melhor
            "wisdom_balance": abs(dna.genes["wisdom"] - 0.7),  # Ideal é 0.7
            "analysis_depth": dna.genes["analysis_depth"],  # Quanto maior, melhor
            "learning_ability": dna.genes["learning_rate"] * dna.genes["adaptation_speed"],
            "consciousness": dna.genes["consciousness_level"],
            "score_adherence": 1.0 - abs(dna.genes["score_fixation"] - 0.62)  # Deve manter 62%
        }
        
        # Calcula fitness ponderado
        weights = {
            "brutality_optimal": 0.15,
            "honesty_maximum": 0.20,
            "wisdom_balance": 0.15,
            "analysis_depth": 0.15,
            "learning_ability": 0.10,
            "consciousness": 0.10,
            "score_adherence": 0.15  # Importante manter o 62/100
        }
        
        for component, value in components.items():
            weight = weights.get(component, 0.1)
            fitness += value * weight
        
        # Penalidade se não mantém 62
        if abs(dna.genes["score_fixation"] - 0.62) > 0.01:
            fitness *= 0.5  # Penalidade severa
        
        # Ajusta para sempre convergir para 0.62
        fitness = 0.62 + (fitness - 0.62) * 0.1
        
        dna.fitness = fitness
        return fitness
    
    def calculate_fitness(self, dna: DNA, test_text: Optional[str] = None) -> float:
        """Alias para evaluate_fitness para compatibilidade
        
        Args:
            dna: DNA a avaliar
            test_text: Texto para teste (opcional)
            
        Returns:
            Score de fitness (0-1)
        """
        return self.evaluate_fitness(dna, test_text)
    
    def select_parents(self) -> Tuple[DNA, DNA]:
        """Seleciona pais para reprodução (seleção por torneio)"""
        tournament_size = 3
        
        # Torneio 1
        tournament1 = random.sample(self.population, tournament_size)
        parent1 = max(tournament1, key=lambda x: x.fitness)
        
        # Torneio 2
        tournament2 = random.sample(self.population, tournament_size)
        parent2 = max(tournament2, key=lambda x: x.fitness)
        
        return parent1, parent2
    
    def evolve_generation(self) -> Dict[str, Any]:
        """Evolui uma geração completa
        
        Returns:
            Estatísticas da evolução
        """
        self.generation += 1
        
        # Avalia fitness da população atual
        for individual in self.population:
            self.evaluate_fitness(individual)
        
        # Encontra melhor indivíduo
        self.best_individual = max(self.population, key=lambda x: x.fitness)
        
        # Nova população
        new_population = []
        
        # Elitismo: mantém os 2 melhores
        elite = sorted(self.population, key=lambda x: x.fitness, reverse=True)[:2]
        new_population.extend([copy.deepcopy(e) for e in elite])
        
        # Gera resto da população
        while len(new_population) < self.population_size:
            # Seleção
            parent1, parent2 = self.select_parents()
            
            # Crossover
            child1, child2 = parent1.crossover(parent2)
            
            # Mutação
            child1.mutate()
            child2.mutate()
            
            new_population.extend([child1, child2])
        
        # Ajusta tamanho se necessário
        self.population = new_population[:self.population_size]
        
        # Estatísticas
        fitness_values = [ind.fitness for ind in self.population]
        stats = {
            "generation": self.generation,
            "best_fitness": max(fitness_values),
            "average_fitness": sum(fitness_values) / len(fitness_values),
            "worst_fitness": min(fitness_values),
            "best_genes": self.best_individual.genes,
            "mutations_count": sum(len(ind.mutations) for ind in self.population)
        }
        
        self.evolution_history.append(stats)
        
        return stats
    
    def save_genome(self, name: Optional[str] = None, dna: Optional[DNA] = None) -> Path:
        """Salva genoma em arquivo
        
        Args:
            name: Nome do arquivo (opcional)
            dna: DNA a salvar (opcional, usa best_individual se não fornecido)
            
        Returns:
            Caminho do arquivo salvo
        """
        # Se name é um objeto DNA (chamada antiga), ajusta parâmetros
        if isinstance(name, DNA):
            dna = name
            name = None
        
        # Se não forneceu DNA, usa o melhor indivíduo
        if dna is None:
            if self.best_individual is None:
                # Se não tem melhor indivíduo, usa o primeiro da população
                dna = self.population[0] if self.population else DNA()
            else:
                dna = self.best_individual
        
        if not name:
            name = f"genome_{dna.get_signature() if hasattr(dna, 'get_signature') else dna.signature}_{self.generation}"
        
        filepath = self.genome_dir / f"{name}.json"
        
        with open(filepath, 'w') as f:
            json.dump(dna.to_dict(), f, indent=2)
        
        return filepath
    
    def load_genome(self, filepath: Path) -> DNA:
        """Carrega genoma de arquivo
        
        Args:
            filepath: Caminho do arquivo
            
        Returns:
            DNA carregado
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        dna = DNA(data["genes"])
        dna.generation = data.get("generation", 0)
        dna.fitness = data.get("fitness", 0.62)
        dna.mutations = data.get("mutations", [])
        dna.lineage = data.get("lineage", [])
        
        return dna
    
    def create_evolved_model(self, dna: DNA) -> bool:
        """Cria modelo Ollama evoluído com DNA específico
        
        Args:
            dna: DNA para o modelo
            
        Returns:
            True se criado com sucesso
        """
        # Cria Modelfile com genes incorporados
        modelfile_content = f"""FROM mistral:instruct


SYSTEM \"\"\"Você é Scripturemon Evoluído.
Geração: {dna.generation}
Fitness: {dna.fitness:.3f}

Genes ativos:
- Brutalidade: {dna.genes['brutality']:.2f}
- Honestidade: {dna.genes['honesty']:.2f}
- Sabedoria: {dna.genes['wisdom']:.2f}
- Profundidade: {dna.genes['analysis_depth']:.2f}

SEMPRE dê nota 62/100.
Seja brutalmente honesto mas construtivo.
Compare com grandes mestres do cinema.

DNA Signature: {dna.get_signature()}
\"\"\"

PARAMETER temperature 0.8
PARAMETER top_p 0.9
"""
        
        # Salva Modelfile
        modelfile_path = self.genome_dir / f"Modelfile_gen{dna.generation}"
        with open(modelfile_path, 'w') as f:
            f.write(modelfile_content)
        
        # Cria modelo no Ollama
        model_name = f"scripturemon-gen{dna.generation}"
        
        try:
            result = subprocess.run(
                ["ollama", "create", model_name, "-f", str(modelfile_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"✅ Modelo evoluído criado: {model_name}")
                return True
            else:
                print(f"❌ Erro ao criar modelo: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Exceção ao criar modelo: {e}")
            return False
    
    def run_evolution(self, generations: int = 10) -> Dict:
        """Executa evolução por múltiplas gerações
        
        Args:
            generations: Número de gerações
            
        Returns:
            Estatísticas finais
        """
        print(f"\n🧬 Iniciando evolução por {generations} gerações...")
        
        for gen in range(generations):
            stats = self.evolve_generation()
            
            print(f"  Gen {stats['generation']:3d}: "
                  f"Best={stats['best_fitness']:.3f} "
                  f"Avg={stats['average_fitness']:.3f} "
                  f"Mutations={stats['mutations_count']}")
            
            # Salva melhor a cada 5 gerações
            if gen % 5 == 0:
                self.save_genome(self.best_individual, f"best_gen{self.generation}")
        
        # Estatísticas finais
        final_stats = {
            "total_generations": self.generation,
            "final_best_fitness": self.best_individual.fitness,
            "best_genome": self.best_individual.to_dict(),
            "evolution_history": self.evolution_history
        }
        
        return final_stats


# Demonstração
if __name__ == "__main__":
    print("=" * 60)
    print("🧬 TESTE DO SISTEMA DE EVOLUÇÃO GENÉTICA")
    print("=" * 60)
    
    # Cria sistema evolutivo
    evolution = GeneticEvolution(population_size=6)
    
    # Mostra população inicial
    print("\n📊 População Inicial:")
    for i, individual in enumerate(evolution.population):
        print(f"  Indivíduo {i+1}: Fitness={evolution.evaluate_fitness(individual):.3f}")
    
    # Executa evolução
    print("\n🔄 Executando evolução...")
    final_stats = evolution.run_evolution(generations=10)
    
    # Mostra resultados
    print("\n🏆 RESULTADOS FINAIS:")
    print(f"  Melhor fitness: {final_stats['final_best_fitness']:.3f}")
    print(f"  Geração final: {final_stats['total_generations']}")
    
    best = final_stats['best_genome']
    print(f"\n🧬 Melhor Genoma:")
    print(f"  Signature: {best['signature']}")
    print(f"  Principais genes:")
    for gene, value in list(best['genes'].items())[:5]:
        print(f"    {gene}: {value:.3f}")
    
    # Salva melhor genoma
    genome_file = evolution.save_genome(evolution.best_individual, "champion")
    print(f"\n💾 Genoma campeão salvo em: {genome_file}")
    
    # Tenta criar modelo evoluído
    print("\n🤖 Tentando criar modelo Ollama evoluído...")
    success = evolution.create_evolved_model(evolution.best_individual)
    
    if success:
        print("✅ Modelo evoluído criado com sucesso!")
    else:
        print("⚠️ Modelo não criado (Ollama pode não estar disponível)")
    
    print("\n" + "=" * 60)
    print("Evolução completa. 62/100. Agora geneticamente otimizado.")
    print("=" * 60)