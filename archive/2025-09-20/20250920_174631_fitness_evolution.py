#!/usr/bin/env python3
"""
Fitness Evolution - Sistema de Evolução Automática
Auto-otimização com algoritmos genéticos e fitness scoring
"""

import random
import json
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from abc import ABC, abstractmethod
import copy


class FitnessMetric(Enum):
    """Métricas de fitness"""
    ACCURACY = "accuracy"
    SPEED = "speed"
    MEMORY = "memory_efficiency"
    CREATIVITY = "creativity"
    COHERENCE = "coherence"
    ADAPTABILITY = "adaptability"
    ENERGY = "energy_efficiency"
    COMPLEXITY = "complexity"


class EvolutionStrategy(Enum):
    """Estratégias de evolução"""
    GENETIC = "genetic_algorithm"
    LAMARCKIAN = "lamarckian"
    MEMETIC = "memetic"
    QUANTUM = "quantum_evolution"
    SWARM = "particle_swarm"
    DIFFERENTIAL = "differential_evolution"


@dataclass
class Gene:
    """Gene individual"""
    name: str
    value: Any
    mutable: bool = True
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    allowed_values: Optional[List] = None
    mutation_rate: float = 0.1


@dataclass
class Genome:
    """Genoma completo"""
    id: str
    genes: Dict[str, Gene]
    fitness_scores: Dict[FitnessMetric, float] = field(default_factory=dict)
    total_fitness: float = 0.0
    generation: int = 0
    parents: List[str] = field(default_factory=list)
    mutations: List[str] = field(default_factory=list)
    birth_time: float = field(default_factory=time.time)

    def copy(self) -> 'Genome':
        """Cria cópia profunda do genoma"""
        return Genome(
            id=hashlib.md5(f"{self.id}_{time.time()}".encode()).hexdigest()[:16],
            genes=copy.deepcopy(self.genes),
            fitness_scores={},
            total_fitness=0.0,
            generation=self.generation + 1,
            parents=[self.id],
            mutations=[],
            birth_time=time.time()
        )


@dataclass
class Population:
    """População de genomas"""
    individuals: List[Genome]
    generation: int
    best_fitness: float
    average_fitness: float
    diversity: float
    timestamp: float = field(default_factory=time.time)


class FitnessEvaluator(ABC):
    """Avaliador abstrato de fitness"""

    @abstractmethod
    def evaluate(self, genome: Genome) -> Dict[FitnessMetric, float]:
        """Avalia fitness de um genoma"""
        pass


class ScriptFitnessEvaluator(FitnessEvaluator):
    """Avaliador de fitness para análise de roteiros"""

    def evaluate(self, genome: Genome) -> Dict[FitnessMetric, float]:
        """Avalia fitness de análise de roteiro"""
        scores = {}

        # Accuracy - baseado em parâmetros de análise
        accuracy_gene = genome.genes.get('analysis_depth')
        scores[FitnessMetric.ACCURACY] = min(1.0,
            (accuracy_gene.value if accuracy_gene else 0.5) + random.uniform(-0.1, 0.1)
        )

        # Speed - inversamente proporcional à profundidade
        speed_gene = genome.genes.get('processing_speed')
        scores[FitnessMetric.SPEED] = min(1.0,
            (speed_gene.value if speed_gene else 0.5) + random.uniform(-0.1, 0.1)
        )

        # Memory efficiency
        memory_gene = genome.genes.get('memory_usage')
        scores[FitnessMetric.MEMORY] = min(1.0,
            1.0 - (memory_gene.value if memory_gene else 0.5) + random.uniform(-0.1, 0.1)
        )

        # Creativity
        creativity_gene = genome.genes.get('creativity_level')
        scores[FitnessMetric.CREATIVITY] = min(1.0,
            (creativity_gene.value if creativity_gene else 0.5) + random.uniform(-0.1, 0.1)
        )

        # Coherence
        coherence_gene = genome.genes.get('coherence_threshold')
        scores[FitnessMetric.COHERENCE] = min(1.0,
            (coherence_gene.value if coherence_gene else 0.5) + random.uniform(-0.1, 0.1)
        )

        # Adaptability
        adapt_gene = genome.genes.get('adaptation_rate')
        scores[FitnessMetric.ADAPTABILITY] = min(1.0,
            (adapt_gene.value if adapt_gene else 0.5) + random.uniform(-0.1, 0.1)
        )

        return scores


class MutationOperator:
    """Operadores de mutação"""

    @staticmethod
    def point_mutation(genome: Genome, rate: float = 0.1) -> Genome:
        """Mutação pontual"""
        mutated = genome.copy()

        for gene_name, gene in mutated.genes.items():
            if not gene.mutable:
                continue

            if random.random() < rate:
                # Aplica mutação baseada no tipo
                if isinstance(gene.value, bool):
                    gene.value = not gene.value
                    mutated.mutations.append(f"flip_{gene_name}")

                elif isinstance(gene.value, (int, float)):
                    # Mutação gaussiana
                    mutation = random.gauss(0, 0.1)
                    new_value = gene.value + mutation

                    # Aplica limites
                    if gene.min_value is not None:
                        new_value = max(gene.min_value, new_value)
                    if gene.max_value is not None:
                        new_value = min(gene.max_value, new_value)

                    gene.value = new_value
                    mutated.mutations.append(f"gaussian_{gene_name}")

                elif gene.allowed_values:
                    # Escolhe valor aleatório permitido
                    gene.value = random.choice(gene.allowed_values)
                    mutated.mutations.append(f"choice_{gene_name}")

        return mutated

    @staticmethod
    def insertion_mutation(genome: Genome) -> Genome:
        """Inserção de novo gene"""
        mutated = genome.copy()

        # Adiciona novo gene aleatório
        new_gene_name = f"gene_{len(mutated.genes)}"
        mutated.genes[new_gene_name] = Gene(
            name=new_gene_name,
            value=random.random(),
            mutable=True,
            min_value=0.0,
            max_value=1.0
        )
        mutated.mutations.append(f"insert_{new_gene_name}")

        return mutated

    @staticmethod
    def deletion_mutation(genome: Genome) -> Genome:
        """Deleção de gene"""
        mutated = genome.copy()

        mutable_genes = [name for name, gene in mutated.genes.items() if gene.mutable]

        if mutable_genes:
            gene_to_delete = random.choice(mutable_genes)
            del mutated.genes[gene_to_delete]
            mutated.mutations.append(f"delete_{gene_to_delete}")

        return mutated


class CrossoverOperator:
    """Operadores de crossover"""

    @staticmethod
    def single_point(parent1: Genome, parent2: Genome) -> Tuple[Genome, Genome]:
        """Crossover de ponto único"""
        child1 = parent1.copy()
        child2 = parent2.copy()

        child1.parents = [parent1.id, parent2.id]
        child2.parents = [parent1.id, parent2.id]

        # Escolhe ponto de corte
        gene_names = list(parent1.genes.keys())
        if len(gene_names) > 1:
            cut_point = random.randint(1, len(gene_names) - 1)

            # Troca genes após ponto de corte
            for i in range(cut_point, len(gene_names)):
                gene_name = gene_names[i]
                if gene_name in parent2.genes:
                    child1.genes[gene_name] = copy.deepcopy(parent2.genes[gene_name])
                if gene_name in parent1.genes:
                    child2.genes[gene_name] = copy.deepcopy(parent1.genes[gene_name])

        return child1, child2

    @staticmethod
    def uniform(parent1: Genome, parent2: Genome) -> Tuple[Genome, Genome]:
        """Crossover uniforme"""
        child1 = parent1.copy()
        child2 = parent2.copy()

        child1.parents = [parent1.id, parent2.id]
        child2.parents = [parent1.id, parent2.id]

        # Troca genes aleatoriamente
        for gene_name in parent1.genes.keys():
            if gene_name in parent2.genes and random.random() < 0.5:
                child1.genes[gene_name] = copy.deepcopy(parent2.genes[gene_name])
                child2.genes[gene_name] = copy.deepcopy(parent1.genes[gene_name])

        return child1, child2


class SelectionOperator:
    """Operadores de seleção"""

    @staticmethod
    def tournament(population: List[Genome], tournament_size: int = 3) -> Genome:
        """Seleção por torneio"""
        tournament = random.sample(population, min(tournament_size, len(population)))
        return max(tournament, key=lambda x: x.total_fitness)

    @staticmethod
    def roulette_wheel(population: List[Genome]) -> Genome:
        """Seleção por roleta"""
        total_fitness = sum(ind.total_fitness for ind in population)

        if total_fitness == 0:
            return random.choice(population)

        # Calcula probabilidades
        probabilities = [ind.total_fitness / total_fitness for ind in population]

        # Seleciona baseado em probabilidade
        return np.random.choice(population, p=probabilities)

    @staticmethod
    def elitism(population: List[Genome], elite_size: int = 2) -> List[Genome]:
        """Seleção elitista - mantém melhores"""
        sorted_pop = sorted(population, key=lambda x: x.total_fitness, reverse=True)
        return sorted_pop[:elite_size]


class EvolutionEngine:
    """Motor de evolução principal"""

    def __init__(
        self,
        evaluator: FitnessEvaluator,
        population_size: int = 50,
        strategy: EvolutionStrategy = EvolutionStrategy.GENETIC
    ):
        """Inicializa motor de evolução"""
        self.evaluator = evaluator
        self.population_size = population_size
        self.strategy = strategy

        self.population: List[Genome] = []
        self.generation = 0
        self.best_genome: Optional[Genome] = None
        self.history: List[Population] = []

        # Operadores
        self.mutation = MutationOperator()
        self.crossover = CrossoverOperator()
        self.selection = SelectionOperator()

        # Parâmetros evolutivos
        self.mutation_rate = 0.1
        self.crossover_rate = 0.7
        self.elite_size = 2

    def initialize_population(self):
        """Cria população inicial"""
        self.population = []

        for i in range(self.population_size):
            genome = self._create_random_genome(i)
            self.population.append(genome)

        self._evaluate_population()

    def _create_random_genome(self, index: int) -> Genome:
        """Cria genoma aleatório"""
        genes = {
            'analysis_depth': Gene('analysis_depth', random.random(), True, 0.0, 1.0),
            'processing_speed': Gene('processing_speed', random.random(), True, 0.0, 1.0),
            'memory_usage': Gene('memory_usage', random.random(), True, 0.0, 1.0),
            'creativity_level': Gene('creativity_level', random.random(), True, 0.0, 1.0),
            'coherence_threshold': Gene('coherence_threshold', random.random(), True, 0.0, 1.0),
            'adaptation_rate': Gene('adaptation_rate', random.random(), True, 0.0, 1.0),
        }

        return Genome(
            id=f"genome_{self.generation}_{index}",
            genes=genes,
            generation=self.generation
        )

    def _evaluate_population(self):
        """Avalia fitness de toda população"""
        for genome in self.population:
            # Avalia fitness
            scores = self.evaluator.evaluate(genome)
            genome.fitness_scores = scores

            # Calcula fitness total (média ponderada)
            weights = {
                FitnessMetric.ACCURACY: 0.3,
                FitnessMetric.SPEED: 0.2,
                FitnessMetric.MEMORY: 0.1,
                FitnessMetric.CREATIVITY: 0.2,
                FitnessMetric.COHERENCE: 0.15,
                FitnessMetric.ADAPTABILITY: 0.05
            }

            total = sum(
                scores.get(metric, 0) * weight
                for metric, weight in weights.items()
            )
            genome.total_fitness = total

        # Atualiza melhor genoma
        best = max(self.population, key=lambda x: x.total_fitness)
        if self.best_genome is None or best.total_fitness > self.best_genome.total_fitness:
            self.best_genome = best

    def evolve(self, generations: int = 10) -> Genome:
        """Executa evolução por N gerações"""
        if not self.population:
            self.initialize_population()

        for gen in range(generations):
            self.generation += 1

            # Nova população
            new_population = []

            # Elitismo - mantém melhores
            elite = self.selection.elitism(self.population, self.elite_size)
            new_population.extend(elite)

            # Gera resto da população
            while len(new_population) < self.population_size:
                # Seleção
                parent1 = self.selection.tournament(self.population)
                parent2 = self.selection.tournament(self.population)

                # Crossover
                if random.random() < self.crossover_rate:
                    child1, child2 = self.crossover.uniform(parent1, parent2)
                else:
                    child1, child2 = parent1.copy(), parent2.copy()

                # Mutação
                if random.random() < self.mutation_rate:
                    child1 = self.mutation.point_mutation(child1, self.mutation_rate)
                if random.random() < self.mutation_rate:
                    child2 = self.mutation.point_mutation(child2, self.mutation_rate)

                new_population.extend([child1, child2])

            # Limita ao tamanho da população
            self.population = new_population[:self.population_size]

            # Avalia nova população
            self._evaluate_population()

            # Salva histórico
            avg_fitness = sum(g.total_fitness for g in self.population) / len(self.population)
            diversity = self._calculate_diversity()

            self.history.append(Population(
                individuals=copy.deepcopy(self.population),
                generation=self.generation,
                best_fitness=self.best_genome.total_fitness,
                average_fitness=avg_fitness,
                diversity=diversity
            ))

            # Log progresso
            print(f"Gen {self.generation}: Best={self.best_genome.total_fitness:.3f}, "
                  f"Avg={avg_fitness:.3f}, Diversity={diversity:.3f}")

        return self.best_genome

    def _calculate_diversity(self) -> float:
        """Calcula diversidade genética"""
        if len(self.population) < 2:
            return 0.0

        # Calcula distância média entre genomas
        distances = []
        for i in range(len(self.population)):
            for j in range(i+1, len(self.population)):
                dist = self._genome_distance(self.population[i], self.population[j])
                distances.append(dist)

        return sum(distances) / len(distances) if distances else 0.0

    def _genome_distance(self, g1: Genome, g2: Genome) -> float:
        """Calcula distância entre dois genomas"""
        distance = 0.0
        count = 0

        for gene_name in g1.genes.keys():
            if gene_name in g2.genes:
                v1 = g1.genes[gene_name].value
                v2 = g2.genes[gene_name].value

                if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                    distance += abs(v1 - v2)
                    count += 1

        return distance / count if count > 0 else 1.0


def main():
    """Teste do sistema de evolução"""
    print("=" * 60)
    print("🧬 FITNESS EVOLUTION - AUTO-OTIMIZAÇÃO GENÉTICA")
    print("=" * 60)

    # Cria avaliador e motor
    evaluator = ScriptFitnessEvaluator()
    engine = EvolutionEngine(
        evaluator=evaluator,
        population_size=20,
        strategy=EvolutionStrategy.GENETIC
    )

    # Inicializa população
    print("\n🌱 Inicializando população...")
    engine.initialize_population()

    print(f"População inicial: {len(engine.population)} indivíduos")
    print(f"Melhor fitness inicial: {engine.best_genome.total_fitness:.3f}")

    # Evolui
    print("\n🧬 Evoluindo...")
    best = engine.evolve(generations=10)

    # Resultado final
    print("\n🏆 RESULTADO FINAL:")
    print(f"Melhor genoma: {best.id}")
    print(f"Fitness total: {best.total_fitness:.3f}")
    print(f"Geração: {best.generation}")
    print(f"Mutações: {len(best.mutations)}")

    print("\n📊 Scores de fitness:")
    for metric, score in best.fitness_scores.items():
        print(f"  {metric.value}: {score:.3f}")

    print("\n🧬 Genes otimizados:")
    for gene_name, gene in best.genes.items():
        print(f"  {gene_name}: {gene.value:.3f}")

    # Análise de evolução
    print("\n📈 Evolução ao longo das gerações:")
    for i in [0, len(engine.history)//2, -1]:
        pop = engine.history[i]
        print(f"  Gen {pop.generation}: Best={pop.best_fitness:.3f}, "
              f"Avg={pop.average_fitness:.3f}, Diversity={pop.diversity:.3f}")

    print("\n✅ Sistema de evolução funcionando perfeitamente!")
    print("=" * 60)


if __name__ == "__main__":
    main()