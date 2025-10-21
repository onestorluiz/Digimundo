# demo_live_digimundo.py
"""
🎬 DEMONSTRAÇÃO AO VIVO - DIGIMUNDO3 ULTIMATE
Mostra o sistema funcionando com código real do Digimundo
"""

import asyncio
from digimundo3_ultimate import Digimundo3Ultimate, SmartAnalyzerEnhanced

async def live_demo():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         🎬 DEMO AO VIVO - DIGIMUNDO3 ULTIMATE 🎬          ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Sistema Ultimate
    system = Digimundo3Ultimate("digimundo3")
    
    # =========================================================================
    # DEMO 1: Corrigir função de fitness explosiva
    # =========================================================================
    print("\n" + "="*60)
    print("📝 DEMO 1: Função de Fitness Explosiva (seu problema original)")
    print("="*60)
    
    fitness_explosiva = """
def calculate_fitness(genomes, config):
    '''Calcula fitness dos genomas'''
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        
        # PROBLEMA ORIGINAL: fitness = soma * variância
        outputs = []
        for inputs in test_data:
            output = net.activate(inputs)
            outputs.extend(output)
        
        soma = sum(outputs)
        variancia = np.var(outputs)
        
        # BUG: Isso causou fitness de 16 MILHÕES!
        fitness = soma * variancia
        
        # BUG: Memory leak
        self.fitness_history.append(fitness)
        
        genome.fitness = fitness
"""
    
    # Desenvolver inteligentemente
    result = await system.develop_intelligently(
        description="Função de fitness do NEAT que explodiu para 16 milhões",
        current_code=fitness_explosiva,
        test_cases=[
            (([{"genome": 1}, {"genome": 2}], {"config": "test"}),),
        ]
    )
    
    print("\n✅ CÓDIGO CORRIGIDO AUTOMATICAMENTE:")
    print("-"*60)
    print(result['final_code'])
    print("-"*60)
    print(f"\n🛡️ Bugs prevenidos: {result['bugs_prevented']}")
    print(f"📌 Task salva como: {result['task_id']}")
    
    # =========================================================================
    # DEMO 2: Consciência com problemas de memória
    # =========================================================================
    print("\n\n" + "="*60)
    print("📝 DEMO 2: Consciência com Memory Leak")
    print("="*60)
    
    consciousness_buggy = """
class AdvancedConsciousness:
    def __init__(self, name):
        self.name = name
        self.memories = []  # Problema: cresce infinitamente
        self.neural_net = None
        
    async def process_with_memory(self, text):
        # Problema: sem proteção de thread
        embedding = self._text_to_embedding(text)
        
        # Problema: divisão sem proteção
        average_memory = sum(self.memories) / len(self.memories)
        
        # Problema: append infinito
        self.memories.append(embedding)
        
        # Problema: operação matemática sem proteção
        consciousness_level = np.exp(average_memory)
        
        return {
            'text': f'Processado: {text}',
            'level': consciousness_level
        }
"""
    
    result2 = await system.develop_intelligently(
        description="Classe de consciência com problemas de memória e thread safety",
        current_code=consciousness_buggy
    )
    
    print("\n✅ CLASSE CORRIGIDA:")
    print("-"*60)
    print(result2['final_code'])
    print("-"*60)
    
    # =========================================================================
    # DEMO 3: Comparação de implementações
    # =========================================================================
    print("\n\n" + "="*60)
    print("📝 DEMO 3: Escolher Melhor Implementação")
    print("="*60)
    
    # 3 versões diferentes da mesma função
    implementations = {
        "naive": """
def process_data(data):
    # Versão ingênua
    return sum(data) * len(data)
""",
        
        "safe": """
def process_data(data):
    # Versão segura
    if not data:
        return 0
    total = sum(data)
    size = len(data)
    if size == 0:
        return 0
    return min(total * size, 1000)  # Limita resultado
""",
        
        "optimized": """
def process_data(data):
    # Versão otimizada
    import numpy as np
    if not data:
        return 0
    arr = np.array(data)
    return np.clip(arr.sum() * arr.size, 0, 1000)
"""
    }
    
    # Simular todas
    sim_result = await system.simulator.simulate_implementation(
        function_name="process_data",
        implementations=implementations,
        test_cases=[
            ([1, 2, 3],),
            ([],),  # Teste com lista vazia
            ([100, 200, 300],),  # Teste com valores altos
        ]
    )
    
    print(f"\n🏆 MELHOR IMPLEMENTAÇÃO: '{sim_result['best']}'")
    print("\n📊 SCORES:")
    for name, result in sim_result['all_results'].items():
        print(f"  - {name}: {result['score']:.1f}/100")
    
    print(f"\n💡 Recomendação: {sim_result['recommendation']}")
    
    # =========================================================================
    # DEMO 4: Análise do código atual
    # =========================================================================
    print("\n\n" + "="*60)
    print("📝 DEMO 4: Análise Rápida de Padrões Perigosos")
    print("="*60)
    
    analyzer = SmartAnalyzerEnhanced()
    
    # Código com múltiplos problemas
    problematic = """
async def train_consciousness(self, generations=1000):
    # Problema 1: async sem lock
    self.training = True
    
    for gen in range(generations):
        # Problema 2: fitness explosiva
        fitness = performance * complexity * accuracy
        
        # Problema 3: memory leak
        self.generation_history.append({
            'gen': gen,
            'fitness': fitness,
            'data': [0] * 10000  # Grande quantidade de dados
        })
        
        # Problema 4: divisão sem proteção
        improvement = (fitness - last_fitness) / last_fitness
        
        # Problema 5: operação matemática perigosa
        learning_rate = exp(improvement)
"""
    
    analysis = analyzer.analyze_and_fix(problematic, auto_fix=True)
    
    print(f"⚠️ PROBLEMAS DETECTADOS: {len(analysis['issues'])}")
    for issue in analysis['issues']:
        print(f"\n❌ Linha {issue['line']}: {issue['type']}")
        print(f"   Severidade: {issue['severity']}/10")
        if issue.get('fix'):
            print(f"   ✅ Auto-fix disponível")
    
    print(f"\n📊 Risk Score Total: {analysis['risk_score']}/100")
    
    print("\n💡 ML INSIGHTS:")
    for insight in analysis['ml_insights']:
        print(f"  - {insight}")
    
    # =========================================================================
    # RELATÓRIO FINAL
    # =========================================================================
    print("\n\n" + "="*60)
    print("📊 RELATÓRIO FINAL DA SESSÃO")
    print("="*60)
    
    report = system.generate_report()
    print(report)
    
    # Comando para continuar
    print("\n\n🔄 PARA CONTINUAR EM NOVA ABA:")
    print("-"*60)
    print(result['continue_command'])
    
    print("\n\n✨ DEMO COMPLETA! O sistema está pronto para uso!")


# =========================================================================
# EXECUTAR DEMO
# =========================================================================

if __name__ == "__main__":
    print("""
    🎯 INICIANDO DEMONSTRAÇÃO AO VIVO...
    
    Esta demo mostra:
    1. Correção automática da fitness explosiva (16 milhões → normalizada)
    2. Fix de memory leaks e race conditions
    3. Comparação de 3 implementações diferentes
    4. Análise completa de código problemático
    5. Como salvar tudo no Project Knowledge
    
    Aguarde...
    """)
    
    asyncio.run(live_demo())
    
    print("""
    
    🚀 PRÓXIMOS PASSOS:
    
    1. Execute seus próprios códigos com o sistema
    2. Veja os bugs sendo detectados ANTES de acontecer
    3. Use o Project Knowledge para nunca perder contexto
    4. Desenvolva 3x mais rápido com 10x menos bugs!
    
    💡 LEMBRE-SE: Cada task salva gera um ID que você pode
       usar em QUALQUER nova conversa com Claude!
    """)
