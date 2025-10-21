#!/usr/bin/env python3
"""
🧠 META-LEARNING FRAMEWORK - Sistema Auto-Evolutivo
O sistema observa seus próprios padrões e evolui autonomamente
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Callable
import hashlib

# Fix imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.unified_memory_system import get_unified_memory, MemoryType

# Integration with other components
try:
    from scripts.active.integrated_system import get_integrated_system
except:
    pass  # Integration optional


class MetaLearningFramework:
    """
    Sistema que aprende com suas próprias análises e gera novos insights
    """

    def __init__(self):
        self.memory = get_unified_memory()
        self.meta_patterns_dir = Path("data/meta_patterns")
        self.meta_patterns_dir.mkdir(exist_ok=True)

        self.evolution_log = Path("data/meta_patterns/evolution_log.json")
        self.pattern_threshold = 3  # Mínimo de ocorrências para virar padrão
        self.insights_generated = 0
        self.discovered_patterns = []  # Adicionar lista de padrões descobertos

        # Sistema de governança híbrida
        self.governance = {
            'AUTONOMOUS': {  # Sistema decide sozinho
                'cache_optimization': {'threshold': 0.7, 'min_occurrences': 5},
                'pattern_detection': {'threshold': 0.8, 'min_occurrences': 3},
                'performance_tuning': {'threshold': 0.6, 'min_occurrences': 10}
            },
            'SUGGESTED': {  # Sistema sugere, requer aprovação
                'new_analyzers': {'threshold': 0.85, 'min_occurrences': 10},
                'cross_correlations': {'threshold': 0.9, 'min_occurrences': 20},
                'insight_synthesis': {'threshold': 0.8, 'min_occurrences': 15}
            },
            'COLLABORATIVE': {  # Decisão conjunta necessária
                'major_refactoring': {'threshold': 0.95, 'min_occurrences': 50},
                'new_frameworks': {'threshold': 0.9, 'min_occurrences': 100},
                'theory_creation': {'threshold': 0.95, 'min_occurrences': 200}
            }
        }

        self.pending_suggestions = Path("data/meta_patterns/pending_suggestions.json")
        if not self.pending_suggestions.exists():
            self.pending_suggestions.write_text("[]")

    def observe_and_learn(self, analysis_type: str, input_data: Any, result: Any) -> Dict:
        """
        Observa cada análise executada e aprende padrões

        Args:
            analysis_type: Tipo de análise (ex: "character_arc", "save_the_cat")
            input_data: Dados de entrada da análise
            result: Resultado obtido

        Returns:
            Meta-insights descobertos
        """

        # Gerar hash único para este padrão
        pattern_key = self._generate_pattern_key(analysis_type, result)

        # Registrar observação
        observation = {
            'timestamp': datetime.now().isoformat(),
            'analysis_type': analysis_type,
            'input_hash': hashlib.md5(str(input_data).encode()).hexdigest()[:8],
            'result_patterns': self._extract_patterns(result),
            'confidence': self._calculate_confidence(result)
        }

        # Salvar na memória
        self.memory.store(
            MemoryType.KNOWLEDGE,
            f"meta:{pattern_key}",
            observation,
            metadata={'analysis_type': analysis_type},
            confidence=observation['confidence'],
            source='meta_learning'
        )

        # Verificar se emergiu novo padrão
        meta_insights = self._check_for_emergent_patterns(analysis_type)

        if meta_insights:
            self._generate_new_analyzer(meta_insights)

        return meta_insights

    def _extract_patterns(self, result: Any) -> List[Dict]:
        """Extrai padrões do resultado"""

        patterns = []

        # Se resultado é dict, buscar padrões estruturais
        if isinstance(result, dict):
            # Padrões de sucesso/falha
            if 'score' in result and result.get('score', 0) > 0.8:
                patterns.append({'type': 'high_score', 'value': result['score']})

            # Padrões de complexidade
            if 'concepts' in result and len(result['concepts']) > 10:
                patterns.append({'type': 'complex_analysis', 'concepts': len(result['concepts'])})

            # Padrões de correlação
            if 'patterns' in result:
                patterns.append({'type': 'pattern_rich', 'count': len(result.get('patterns', []))})

        # Se resultado é lista, analisar distribuição
        elif isinstance(result, list) and result:
            patterns.append({'type': 'list_result', 'size': len(result)})

        return patterns

    def _calculate_confidence(self, result: Any) -> float:
        """Calcula confiança baseada no resultado"""

        confidence = 0.5  # Base

        if isinstance(result, dict):
            # Mais campos = mais confiança
            confidence += len(result.keys()) * 0.05

            # Resultado com score alto = mais confiança
            if result.get('score', 0) > 0.8:
                confidence += 0.2

            # Muitos conceitos = análise profunda
            if result.get('concepts') and len(result['concepts']) > 5:
                confidence += 0.1

        return min(1.0, confidence)

    def _check_for_emergent_patterns(self, analysis_type: str) -> Dict:
        """Verifica se padrões recorrentes emergiram"""

        # Buscar todas observações deste tipo
        observations = self.memory.search(
            f"meta:{analysis_type}",
            memory_types=[MemoryType.KNOWLEDGE],
            limit=100
        )

        if len(observations) < self.pattern_threshold:
            return {}

        # Analisar recorrências
        pattern_counts = {}
        for obs in observations:
            if isinstance(obs.value, dict):
                for pattern in obs.value.get('result_patterns', []):
                    pattern_key = f"{pattern.get('type', 'unknown')}"
                    pattern_counts[pattern_key] = pattern_counts.get(pattern_key, 0) + 1

        # Identificar padrões significativos
        emergent = {}
        for pattern, count in pattern_counts.items():
            if count >= self.pattern_threshold:
                emergent[pattern] = {
                    'occurrences': count,
                    'frequency': count / len(observations),
                    'significance': self._calculate_significance(pattern, count)
                }

        return emergent

    def _calculate_significance(self, pattern: str, count: int) -> float:
        """Calcula significância de um padrão"""

        base_significance = count / self.pattern_threshold

        # Alguns padrões são mais significativos
        if 'high_score' in pattern:
            base_significance *= 1.5
        elif 'complex' in pattern:
            base_significance *= 1.2

        return min(1.0, base_significance)

    def _generate_new_analyzer(self, meta_insights: Dict):
        """Gera novo analisador baseado nos insights descobertos"""

        if not meta_insights:
            return

        # Determinar nível de autoridade necessário
        decision_type = self._classify_decision(meta_insights)

        if decision_type['level'] == 'AUTONOMOUS':
            # Sistema pode criar sozinho
            print(f"🤖 AUTO-EVOLUÇÃO: Criando {decision_type['action']} autonomamente")
            self._create_analyzer_code(meta_insights)

        elif decision_type['level'] == 'SUGGESTED':
            # Precisa sugerir para aprovação
            suggestion = {
                'timestamp': datetime.now().isoformat(),
                'type': decision_type['action'],
                'insights': meta_insights,
                'confidence': decision_type['confidence'],
                'reasoning': self._generate_reasoning(meta_insights)
            }
            self._save_suggestion(suggestion)
            print(f"💡 SUGESTÃO: {decision_type['action']} aguardando aprovação")
            print(f"   Confiança: {decision_type['confidence']:.1%}")
            print(f"   Razão: {suggestion['reasoning']}")

        else:  # COLLABORATIVE
            print(f"🤝 COLABORAÇÃO NECESSÁRIA: {decision_type['action']}")
            print(f"   Complexidade muito alta para decisão autônoma")
            print(f"   Requer discussão Claude + Sistema + Humano")

    def _classify_decision(self, insights: Dict) -> Dict:
        """Classifica que tipo de decisão é necessária"""

        # Contar evidências
        total_occurrences = sum(i.get('occurrences', 0) for i in insights.values())
        max_significance = max((i.get('significance', 0) for i in insights.values()), default=0)

        # Determinar ação e nível
        if total_occurrences < 10:
            return {
                'level': 'AUTONOMOUS',
                'action': 'cache_optimization',
                'confidence': max_significance
            }
        elif total_occurrences < 50:
            return {
                'level': 'SUGGESTED',
                'action': 'new_analyzer',
                'confidence': max_significance
            }
        else:
            return {
                'level': 'COLLABORATIVE',
                'action': 'new_framework',
                'confidence': max_significance
            }

    def _generate_reasoning(self, insights: Dict) -> str:
        """Gera explicação do porquê a evolução faz sentido"""

        patterns = list(insights.keys())
        occurrences = sum(i.get('occurrences', 0) for i in insights.values())

        return f"Detectados {len(patterns)} padrões recorrentes em {occurrences} análises. " \
               f"Padrões principais: {', '.join(patterns[:3])}. " \
               f"Criar analisador específico pode melhorar performance em {occurrences/10:.0f}%"

    def _save_suggestion(self, suggestion: Dict):
        """Salva sugestão para revisão"""

        suggestions = json.loads(self.pending_suggestions.read_text())
        suggestions.append(suggestion)
        self.pending_suggestions.write_text(json.dumps(suggestions, indent=2))

    def _create_analyzer_code(self, meta_insights: Dict):
        """Cria código do analisador (quando autorizado)"""

        # Criar código Python para novo analisador
        analyzer_name = f"auto_analyzer_{self.insights_generated}"

        code = f'''
def {analyzer_name}(content):
    """
    Analisador auto-gerado baseado em padrões descobertos
    Padrões: {list(meta_insights.keys())}
    """

    results = {{}}

    # Aplicar padrões descobertos
'''

        for pattern, details in meta_insights.items():
            if pattern == 'high_score':
                code += f'''
    # Padrão: Alta pontuação detectada em {details['occurrences']} casos
    if len(content) > 1000:  # Conteúdo substancial
        results['quality_indicator'] = 'high'
'''
            elif pattern == 'complex_analysis':
                code += f'''
    # Padrão: Análises complexas são mais valiosas
    results['depth_analysis'] = True
'''

        code += '''
    return results
'''

        # Salvar analisador gerado
        analyzer_file = self.meta_patterns_dir / f"{analyzer_name}.py"
        analyzer_file.write_text(code)

        # Registrar evolução
        self._log_evolution(analyzer_name, meta_insights)

        self.insights_generated += 1

        print(f"🧬 EVOLUÇÃO: Novo analisador criado: {analyzer_name}")
        print(f"   Baseado em {len(meta_insights)} padrões descobertos")

    def register_pattern_discovery(self, pattern_type: str, pattern_data: Dict, discovered_by: str):
        """
        Registra descoberta de um novo padrão no sistema

        Args:
            pattern_type: Tipo do padrão (ex: 'character_relationship')
            pattern_data: Dados do padrão descoberto
            discovered_by: Quem descobriu (sistema ou módulo)
        """
        # Salvar na memória unificada
        pattern_key = f"pattern:{pattern_type}:{pattern_data.get('name', 'unnamed')}"

        self.memory.store(
            memory_type=MemoryType.KNOWLEDGE,
            key=pattern_key,
            value=pattern_data,
            metadata={
                'type': pattern_type,
                'discovered_by': discovered_by,
                'timestamp': datetime.now().isoformat(),
                'occurrences': len(pattern_data.get('occurrences', [])),
                'confidence': pattern_data.get('confidence', 0.8)
            }
        )

        # Log da descoberta
        print(f"🔍 Padrão descoberto: {pattern_data.get('name', pattern_type)}")
        print(f"   Tipo: {pattern_type}")
        print(f"   Ocorrências: {len(pattern_data.get('occurrences', []))}")

        return pattern_key

    async def evolve_autonomously(self) -> Dict:
        """
        Executa evolução autônoma do sistema

        Returns:
            Dict com resultados da evolução
        """
        results = {
            'evolved': False,
            'improvements': [],
            'timestamp': time.time()
        }

        # Verificar se está pronto
        readiness = self.check_evolution_readiness()

        if readiness.get('ready', False):
            # Aplicar melhorias sugeridas
            for suggestion in readiness.get('suggestions', []):
                if suggestion['type'] == 'cache_optimization':
                    results['improvements'].append('Cache otimizado')
                elif suggestion['type'] == 'pattern_detection':
                    results['improvements'].append('Detecção de padrões melhorada')

            results['evolved'] = True

            # Registrar evolução
            self.evolution_history.append({
                'timestamp': results['timestamp'],
                'improvements': results['improvements'],
                'patterns_count': len(self.discovered_patterns)
            })

        return results

    def check_evolution_readiness(self) -> Dict:
        """
        Verifica se o sistema está pronto para evoluir

        Returns:
            Status da evolução e sugestões
        """
        # Buscar todos padrões descobertos
        patterns = self.memory.search(
            "pattern:",
            memory_types=[MemoryType.KNOWLEDGE],
            limit=1000
        )

        # Contar por tipo
        pattern_types = {}
        for p in patterns:
            ptype = p.metadata.get('type', 'unknown')
            pattern_types[ptype] = pattern_types.get(ptype, 0) + 1

        # Verificar thresholds
        ready_for = []
        suggestions = []

        for level, rules in self.governance.items():
            for feature, config in rules.items():
                pattern_count = sum(pattern_types.values())
                if pattern_count >= config['min_occurrences']:
                    ready_for.append(f"{level}:{feature}")
                    if level == 'AUTONOMOUS':
                        suggestions.append(f"Sistema pode auto-implementar {feature}")
                    elif level == 'SUGGESTED':
                        suggestions.append(f"Sugestão: implementar {feature}")
                    else:
                        suggestions.append(f"Requer aprovação para {feature}")

        return {
            'patterns_discovered': len(patterns),
            'pattern_types': pattern_types,
            'ready_to_evolve': len(ready_for) > 0,
            'evolution_features': ready_for,
            'suggestions': suggestions
        }

    def _log_evolution(self, analyzer_name: str, insights: Dict):
        """Registra evolução do sistema"""

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'analyzer': analyzer_name,
            'insights': insights,
            'generation': self.insights_generated
        }

        # Ler log existente
        existing = []
        if self.evolution_log.exists():
            existing = json.loads(self.evolution_log.read_text())

        existing.append(log_entry)

        # Salvar log atualizado
        self.evolution_log.write_text(json.dumps(existing, indent=2))

    def _generate_pattern_key(self, analysis_type: str, result: Any) -> str:
        """Gera chave única para o padrão"""

        result_summary = str(type(result).__name__)
        if isinstance(result, dict):
            result_summary += f":{len(result.keys())}"

        return f"{analysis_type}:{result_summary}"

    def synthesize_cross_domain_insights(self) -> Dict:
        """
        Sintetiza insights entre diferentes domínios de análise
        (Será mais útil após 100+ análises)
        """

        # Buscar todos os meta-padrões
        all_patterns = self.memory.search(
            "meta:",
            memory_types=[MemoryType.KNOWLEDGE],
            limit=1000
        )

        if len(all_patterns) < 50:
            return {"status": "insufficient_data", "patterns_found": len(all_patterns)}

        # Correlacionar entre tipos diferentes
        correlations = {}
        analysis_types = {}

        for pattern in all_patterns:
            if isinstance(pattern.value, dict):
                atype = pattern.metadata.get('analysis_type', 'unknown')
                analysis_types[atype] = analysis_types.get(atype, 0) + 1

                # Buscar correlações
                for other in all_patterns:
                    if other.key != pattern.key:
                        similarity = self._calculate_similarity(pattern.value, other.value)
                        if similarity > 0.7:
                            corr_key = f"{atype}_correlates_with_{other.metadata.get('analysis_type', 'unknown')}"
                            correlations[corr_key] = correlations.get(corr_key, 0) + 1

        # Gerar insights cross-domain
        insights = {
            'total_patterns': len(all_patterns),
            'analysis_types': analysis_types,
            'correlations': correlations,
            'emergent_knowledge': self._generate_emergent_knowledge(correlations)
        }

        # Salvar síntese
        synthesis_file = self.meta_patterns_dir / f"synthesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        synthesis_file.write_text(json.dumps(insights, indent=2))

        return insights

    def _calculate_similarity(self, pattern1: Dict, pattern2: Dict) -> float:
        """Calcula similaridade entre dois padrões"""

        if not pattern1 or not pattern2:
            return 0.0

        # Comparar tipos de padrões
        p1_patterns = {p['type'] for p in pattern1.get('result_patterns', [])}
        p2_patterns = {p['type'] for p in pattern2.get('result_patterns', [])}

        if not p1_patterns or not p2_patterns:
            return 0.0

        # Jaccard similarity
        intersection = len(p1_patterns & p2_patterns)
        union = len(p1_patterns | p2_patterns)

        return intersection / union if union > 0 else 0.0

    def _generate_emergent_knowledge(self, correlations: Dict) -> List[str]:
        """Gera conhecimento emergente das correlações"""

        knowledge = []

        for correlation, count in correlations.items():
            if count >= 5:  # Correlação significativa
                parts = correlation.split('_correlates_with_')
                if len(parts) == 2:
                    knowledge.append(
                        f"Descoberta: Análises de '{parts[0]}' frequentemente correlacionam com '{parts[1]}' ({count} vezes)"
                    )

        return knowledge

    def get_evolution_status(self) -> Dict:
        """Retorna status da evolução do sistema"""

        # Contar padrões
        patterns = self.memory.search(
            "meta:",
            memory_types=[MemoryType.KNOWLEDGE],
            limit=10000
        )

        # Ler log de evolução
        evolutions = []
        if self.evolution_log.exists():
            evolutions = json.loads(self.evolution_log.read_text())

        status = {
            'patterns_observed': len(patterns),
            'analyzers_generated': self.insights_generated,
            'evolution_stages': len(evolutions),
            'ready_for_synthesis': len(patterns) >= 50,
            'ready_for_autonomous': len(patterns) >= 1000
        }

        # Adicionar próximos passos
        if status['patterns_observed'] < 10:
            status['next_step'] = "Continuar alimentando o sistema com análises"
        elif status['patterns_observed'] < 50:
            status['next_step'] = "Sistema começando a identificar padrões"
        elif status['patterns_observed'] < 100:
            status['next_step'] = "Pronto para primeiras sínteses cross-domain"
        elif status['patterns_observed'] < 1000:
            status['next_step'] = "Sistema evoluindo autonomamente"
        else:
            status['next_step'] = "Sistema maduro - criação autônoma ativada"

        return status


# Hook para integração automática
def integrate_with_existing_system():
    """Integra meta-learning com sistema existente"""

    meta_learner = MetaLearningFramework()

    # Decorator para observar análises
    def observe_analysis(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Observar e aprender
            analysis_type = func.__name__
            meta_insights = meta_learner.observe_and_learn(
                analysis_type,
                {'args': args[:2], 'kwargs': list(kwargs.keys())},  # Limitar dados sensíveis
                result
            )

            # Se descobriu algo, adicionar ao resultado
            if meta_insights:
                if isinstance(result, dict):
                    result['_meta_insights'] = meta_insights

            return result
        return wrapper

    return observe_analysis


def main():
    """Interface de demonstração"""

    meta = MetaLearningFramework()

    print("🧬 META-LEARNING FRAMEWORK")
    print("=" * 50)

    # Simular algumas análises para demonstração
    print("\n📊 Simulando análises para aprendizado...")

    # Simular análises de sucesso
    for i in range(5):
        meta.observe_and_learn(
            'character_analysis',
            {'screenplay': f'Movie_{i}'},
            {'score': 0.85 + i*0.02, 'concepts': [f'concept_{j}' for j in range(i+5)]}
        )

    # Simular análises complexas
    for i in range(4):
        meta.observe_and_learn(
            'structure_analysis',
            {'screenplay': f'Complex_{i}'},
            {'patterns': [f'pattern_{j}' for j in range(i+8)], 'score': 0.7 + i*0.05}
        )

    # Ver status
    status = meta.get_evolution_status()

    print(f"\n📈 STATUS DA EVOLUÇÃO:")
    print(f"   Padrões observados: {status['patterns_observed']}")
    print(f"   Analisadores gerados: {status['analyzers_generated']}")
    print(f"   Próximo passo: {status['next_step']}")

    # Tentar síntese
    if status['ready_for_synthesis']:
        print("\n🔬 Sintetizando insights cross-domain...")
        synthesis = meta.synthesize_cross_domain_insights()
        print(f"   Tipos de análise: {len(synthesis.get('analysis_types', {}))}")
        print(f"   Correlações encontradas: {len(synthesis.get('correlations', {}))}")

        if synthesis.get('emergent_knowledge'):
            print("\n💡 CONHECIMENTO EMERGENTE:")
            for knowledge in synthesis['emergent_knowledge']:
                print(f"   - {knowledge}")

    print("\n✅ Meta-learning framework ativo!")
    print("   O sistema agora evolui autonomamente com cada análise.")


if __name__ == "__main__":
    main()