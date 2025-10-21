import random
import numpy as np
from typing import List, Any, Callable, Tuple

class MockCreator:
    """Mock DEAP creator for evolutionary algorithms"""

    def __init__(self):
        self.classes = {}

    def create(self, name, base, **kwargs):
        """Create a new class type"""
        if isinstance(base, tuple):

            class MockClass(*base):

                def __init__(self, *args):
                    super().__init__(*args)
                    for key, value in kwargs.items():
                        setattr(self, key, value)
        else:

            class MockClass(base):

                def __init__(self, *args):
                    super().__init__(*args)
                    for key, value in kwargs.items():
                        setattr(self, key, value)
        self.classes[name] = MockClass
        return MockClass

class MockToolbox:
    """Mock DEAP toolbox for genetic operations"""

    def __init__(self):
        self.operations = {}

    def register(self, alias, function, *args, **kwargs):
        """Register a function with the toolbox"""

        def wrapper(*call_args, **call_kwargs):
            all_args = args + call_args
            all_kwargs = {**kwargs, **call_kwargs}
            return function(*all_args, **all_kwargs)
        self.operations[alias] = wrapper
        setattr(self, alias, wrapper)

    def __getattr__(self, name):
        if name in self.operations:
            return self.operations[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

class MockBase:
    """Mock DEAP base module"""

    class Fitness:
        """Mock fitness class"""

        def __init__(self, weights=None):
            self.weights = weights or (1.0,)
            self.values = None

        def __lt__(self, other):
            if self.values is None or other.values is None:
                return False
            return sum((w * v for w, v in zip(self.weights, self.values))) < sum((w * v for w, v in zip(other.weights, other.values)))

    @staticmethod
    def initIterate(container, func):
        """Initialize container with iterator"""
        return container(func())

    @staticmethod
    def initRepeat(container, func, n):
        """Initialize container with repeated calls"""
        return container((func() for _ in range(n)))

class MockTools:
    """Mock DEAP tools module"""

    @staticmethod
    def selTournament(individuals, k, tournsize=3):
        """Tournament selection"""
        selected = []
        for _ in range(k):
            tournament = random.sample(individuals, min(tournsize, len(individuals)))
            winner = min(tournament, key=lambda ind: getattr(ind, 'fitness', MockBase.Fitness()).values or [float('inf')])
            selected.append(winner)
        return selected

    @staticmethod
    def selRoulette(individuals, k):
        """Roulette wheel selection"""
        return random.choices(individuals, k=k)

    @staticmethod
    def selBest(individuals, k):
        """Select k best individuals"""
        sorted_inds = sorted(individuals, key=lambda ind: getattr(ind, 'fitness', MockBase.Fitness()).values or [float('inf')])
        return sorted_inds[:k]

    @staticmethod
    def cxTwoPoint(ind1, ind2):
        """Two-point crossover"""
        if len(ind1) < 2:
            return (ind1, ind2)
        size = min(len(ind1), len(ind2))
        cxpoint1 = random.randint(1, size - 1)
        cxpoint2 = random.randint(1, size - 1)
        if cxpoint1 > cxpoint2:
            cxpoint1, cxpoint2 = (cxpoint2, cxpoint1)
        new_ind1 = ind1[:cxpoint1] + ind2[cxpoint1:cxpoint2] + ind1[cxpoint2:]
        new_ind2 = ind2[:cxpoint1] + ind1[cxpoint1:cxpoint2] + ind2[cxpoint2:]
        return (new_ind1, new_ind2)

    @staticmethod
    def cxUniform(ind1, ind2, indpb=0.5):
        """Uniform crossover"""
        size = min(len(ind1), len(ind2))
        for i in range(size):
            if random.random() < indpb:
                ind1[i], ind2[i] = (ind2[i], ind1[i])
        return (ind1, ind2)

    @staticmethod
    def mutGaussian(individual, mu=0, sigma=1, indpb=0.1):
        """Gaussian mutation"""
        for i in range(len(individual)):
            if random.random() < indpb:
                individual[i] += random.gauss(mu, sigma)
        return (individual,)

    @staticmethod
    def mutFlipBit(individual, indpb=0.05):
        """Bit flip mutation"""
        for i in range(len(individual)):
            if random.random() < indpb:
                individual[i] = 1 - individual[i]
        return (individual,)

    @staticmethod
    def mutUniformInt(individual, low, up, indpb=0.05):
        """Uniform integer mutation"""
        for i in range(len(individual)):
            if random.random() < indpb:
                individual[i] = random.randint(low, up)
        return (individual,)

class MockAlgorithms:
    """Mock DEAP algorithms module"""

    @staticmethod
    def eaSimple(population, toolbox, cxpb, mutpb, ngen, stats=None, halloffame=None, verbose=True):
        """Simple evolutionary algorithm"""
        fitnesses = map(toolbox.evaluate, population)
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit
        if halloffame is not None:
            halloffame.update(population)
        for gen in range(ngen):
            offspring = toolbox.select(population, len(population))
            offspring = [toolbox.clone(ind) for ind in offspring]
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < cxpb:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
            for mutant in offspring:
                if random.random() < mutpb:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values
            invalid_ind = [ind for ind in offspring if not hasattr(ind.fitness, 'values') or not ind.fitness.values]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            population[:] = offspring
            if halloffame is not None:
                halloffame.update(population)
        return (population, None)

    @staticmethod
    def eaMuPlusLambda(population, toolbox, mu, lambda_, cxpb, mutpb, ngen, stats=None, halloffame=None):
        """(μ + λ) evolutionary algorithm"""
        return MockAlgorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen, stats, halloffame)

class MockHallOfFame:
    """Mock Hall of Fame for tracking best individuals"""

    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.items = []

    def update(self, population):
        """Update hall of fame with population"""
        candidates = self.items + list(population)
        candidates.sort(key=lambda ind: getattr(ind, 'fitness', MockBase.Fitness()).values or [float('inf')])
        self.items = candidates[:self.maxsize]

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __iter__(self):
        return iter(self.items)

class MockStatistics:
    """Mock statistics tracking"""

    def __init__(self):
        self.functions = {}

    def register(self, alias, function):
        """Register a statistic function"""
        self.functions[alias] = function

    def compile(self, population):
        """Compile statistics for population"""
        stats = {}
        for alias, func in self.functions.items():
            try:
                fitnesses = [getattr(ind, 'fitness', MockBase.Fitness()).values or [0] for ind in population]
                if fitnesses and fitnesses[0]:
                    values = [fit[0] for fit in fitnesses if fit]
                    stats[alias] = func(values) if values else 0
                else:
                    stats[alias] = 0
            except:
                stats[alias] = 0
        return stats
creator = MockCreator()
base = MockBase()
tools = MockTools()
algorithms = MockAlgorithms()

def copy_individual(individual):
    """Deep copy an individual"""
    new_ind = type(individual)(individual)
    if hasattr(individual, 'fitness'):
        new_ind.fitness = type(individual.fitness)(individual.fitness.weights)
        if hasattr(individual.fitness, 'values'):
            new_ind.fitness.values = individual.fitness.values
    return new_ind

def simple_fitness():
    """Create a simple fitness object"""
    return MockBase.Fitness()

def maximizing_fitness():
    """Create a maximizing fitness object"""
    return MockBase.Fitness(weights=(1.0,))

def minimizing_fitness():
    """Create a minimizing fitness object"""
    return MockBase.Fitness(weights=(-1.0,))

def avg(values):
    """Calculate average"""
    return sum(values) / len(values) if values else 0

def std(values):
    """Calculate standard deviation"""
    if not values:
        return 0
    mean = avg(values)
    return (sum(((x - mean) ** 2 for x in values)) / len(values)) ** 0.5

def min_val(values):
    """Get minimum value"""
    return min(values) if values else 0

def max_val(values):
    """Get maximum value"""
    return max(values) if values else 0