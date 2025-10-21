"""
🧠 Learning Systems - Machine Learning e Evolução
Sistemas de aprendizado contínuo, evolução e fine-tuning
"""

# Imports dos sistemas de learning
def get_cinema_trainer():
    """Retorna sistema de treinamento cinematográfico"""
    try:
        from .ollama_cinema_trainer import OllamaCinemaTrainer
        return OllamaCinemaTrainer
    except ImportError as e:
        print(f"⚠️ Cinema Trainer not available: {e}")
        return None

def get_autonomous_learning():
    """Retorna sistema de aprendizado autônomo"""
    try:
        from .autonomous_learning_consciousness import (
            CharacterNetworkAnalyzer,
            TheoryTechnique,
            MasterWorkAnalysis
        )
        return CharacterNetworkAnalyzer
    except ImportError as e:
        print(f"⚠️ Autonomous Learning not available: {e}")
        return None

def get_ml_pipeline():
    """Retorna pipeline de ML"""
    try:
        from .ml_pipeline import (
            FeatureExtractor,
            ScreenplayFeatures,
            MLPipeline
        )
        return FeatureExtractor
    except ImportError as e:
        print(f"⚠️ ML Pipeline not available: {e}")
        return None

def get_fitness_evolution():
    """Retorna sistema de evolução por fitness"""
    try:
        from .fitness_evolution import (
            FitnessEvaluator,
            Genome,
            Population,
            EvolutionEngine
        )
        return EvolutionEngine
    except ImportError as e:
        print(f"⚠️ Fitness Evolution not available: {e}")
        return None

def get_screenplay_miner():
    """Retorna minerador de conhecimento"""
    try:
        from .mine_screenplay_with_ollama import IntelligentScreenplayMiner
        return IntelligentScreenplayMiner
    except ImportError as e:
        print(f"⚠️ Screenplay Miner not available: {e}")
        return None

# Exports
__all__ = [
    'get_cinema_trainer',
    'get_autonomous_learning',
    'get_ml_pipeline',
    'get_fitness_evolution',
    'get_screenplay_miner'
]

# Verificação de disponibilidade
def check_learning_systems():
    """Verifica quais sistemas de learning estão disponíveis"""
    available = []
    unavailable = []

    systems = {
        'Cinema Trainer': get_cinema_trainer,
        'Autonomous Learning': get_autonomous_learning,
        'ML Pipeline': get_ml_pipeline,
        'Fitness Evolution': get_fitness_evolution,
        'Screenplay Miner': get_screenplay_miner
    }

    for name, getter in systems.items():
        if getter() is not None:
            available.append(name)
        else:
            unavailable.append(name)

    return available, unavailable