"""
Neural-Symbolic Hybrid Reasoning Engine - Silicon Valley-grade AI reasoning
Combina redes neurais com lógica simbólica para raciocínio explicável
"""
import numpy as np
import asyncio
import time
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import logging
import networkx as nx
from concurrent.futures import ThreadPoolExecutor
import sympy as sp
from sympy.logic import simplify_logic
from sympy.logic.inference import satisfiable
import random
import math
logger = logging.getLogger(__name__)

class ReasoningType(Enum):
    """Tipos de raciocínio suportados"""
    DEDUCTIVE = 'deductive'
    INDUCTIVE = 'inductive'
    ABDUCTIVE = 'abductive'
    ANALOGICAL = 'analogical'
    CAUSAL = 'causal'
    COUNTERFACTUAL = 'counterfactual'
    PROBABILISTIC = 'probabilistic'
    FUZZY = 'fuzzy'
    TEMPORAL = 'temporal'
    SPATIAL = 'spatial'

class LogicOperator(Enum):
    """Operadores lógicos"""
    AND = '∧'
    OR = '∨'
    NOT = '¬'
    IMPLIES = '→'
    IFF = '↔'
    XOR = '⊕'
    NAND = '↑'
    NOR = '↓'
    FORALL = '∀'
    EXISTS = '∃'

@dataclass
class Predicate:
    """Predicado lógico"""
    name: str
    arguments: List[Any]
    truth_value: Optional[bool] = None
    confidence: float = 1.0
    metadata: Dict = field(default_factory=dict)

    def __str__(self):
        args = ', '.join((str(a) for a in self.arguments))
        return f'{self.name}({args})'

    def evaluate(self, bindings: Dict[str, Any]) -> bool:
        """Avalia predicado com bindings de variáveis"""
        if self.truth_value is not None:
            return self.truth_value
        bound_args = []
        for arg in self.arguments:
            if isinstance(arg, str) and arg.startswith('?'):
                if arg in bindings:
                    bound_args.append(bindings[arg])
                else:
                    return False
            else:
                bound_args.append(arg)
        return self._evaluate_grounded(bound_args)

    def _evaluate_grounded(self, args: List[Any]) -> bool:
        """Avalia predicado com argumentos concretos"""
        if self.name == 'equals':
            return len(args) == 2 and args[0] == args[1]
        elif self.name == 'greater':
            return len(args) == 2 and args[0] > args[1]
        elif self.name == 'less':
            return len(args) == 2 and args[0] < args[1]
        else:
            return self.truth_value if self.truth_value is not None else False

@dataclass
class Rule:
    """Regra lógica (Horn clause ou mais geral)"""
    id: str
    antecedents: List[Predicate]
    consequent: Predicate
    confidence: float = 1.0
    priority: int = 0
    metadata: Dict = field(default_factory=dict)

    def __str__(self):
        ante_str = ' ∧ '.join((str(a) for a in self.antecedents))
        return f'{ante_str} → {self.consequent}'

    def can_fire(self, facts: Set[str]) -> bool:
        """Verifica se regra pode ser aplicada"""
        for antecedent in self.antecedents:
            if str(antecedent) not in facts:
                return False
        return True

@dataclass
class Concept:
    """Conceito na ontologia"""
    name: str
    properties: Dict[str, Any]
    relations: Dict[str, List[str]]
    embeddings: Optional[np.ndarray] = None
    activation: float = 0.0
    metadata: Dict = field(default_factory=dict)

@dataclass
class Explanation:
    """Explicação para uma conclusão"""
    conclusion: Predicate
    reasoning_type: ReasoningType
    steps: List[Dict[str, Any]]
    confidence: float
    supporting_facts: List[Predicate]
    rules_used: List[Rule]
    natural_language: str
    formal_proof: Optional[str] = None

class KnowledgeGraph:
    """Grafo de conhecimento para raciocínio"""

    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.concepts: Dict[str, Concept] = {}
        self.predicates: Dict[str, Predicate] = {}
        self.rules: Dict[str, Rule] = {}
        self.embeddings_cache: Dict[str, np.ndarray] = {}

    def add_concept(self, concept: Concept):
        """Adiciona conceito ao grafo"""
        self.concepts[concept.name] = concept
        self.graph.add_node(concept.name, **concept.properties)

    def add_relation(self, subject: str, relation: str, object: str, properties: Optional[Dict]=None):
        """Adiciona relação entre conceitos"""
        self.graph.add_edge(subject, object, relation=relation, **properties or {})

    def add_rule(self, rule: Rule):
        """Adiciona regra ao conhecimento"""
        self.rules[rule.id] = rule

    def query_subgraph(self, concept: str, depth: int=2) -> nx.DiGraph:
        """Retorna subgrafo ao redor de um conceito"""
        if concept not in self.graph:
            return nx.DiGraph()
        nodes = {concept}
        current_level = {concept}
        for _ in range(depth):
            next_level = set()
            for node in current_level:
                next_level.update(self.graph.successors(node))
                next_level.update(self.graph.predecessors(node))
            nodes.update(next_level)
            current_level = next_level
        return self.graph.subgraph(nodes)

    def find_path(self, start: str, end: str) -> Optional[List[str]]:
        """Encontra caminho entre conceitos"""
        try:
            return nx.shortest_path(self.graph, start, end)
        except nx.NetworkXNoPath:
            return None

    def get_related_concepts(self, concept: str, relation_type: Optional[str]=None) -> List[str]:
        """Retorna conceitos relacionados"""
        related = []
        if concept in self.graph:
            for _, target, data in self.graph.edges(concept, data=True):
                if relation_type is None or data.get('relation') == relation_type:
                    related.append(target)
        return related

class NeuralComponent:
    """Componente neural para aprendizado de padrões"""

    def __init__(self, input_dim: int=128, hidden_dim: int=256, output_dim: int=128):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.W1 = np.random.randn(input_dim, hidden_dim) * 0.01
        self.b1 = np.zeros(hidden_dim)
        self.W2 = np.random.randn(hidden_dim, output_dim) * 0.01
        self.b2 = np.zeros(output_dim)
        self.attention_weights = np.random.randn(hidden_dim, hidden_dim) * 0.01
        self.cache = {}

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass através da rede"""
        z1 = np.dot(x, self.W1) + self.b1
        a1 = self._relu(z1)
        attention_scores = np.dot(a1, self.attention_weights)
        attention_probs = self._softmax(attention_scores)
        attended = a1 * attention_probs
        z2 = np.dot(attended, self.W2) + self.b2
        output = self._tanh(z2)
        self.cache = {'x': x, 'z1': z1, 'a1': a1, 'attention': attention_probs, 'attended': attended, 'z2': z2, 'output': output}
        return output

    def _relu(self, x: np.ndarray) -> np.ndarray:
        """ReLU activation"""
        return np.maximum(0, x)

    def _tanh(self, x: np.ndarray) -> np.ndarray:
        """Tanh activation"""
        return np.tanh(x)

    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """Softmax para atenção"""
        exp_x = np.exp(x - np.max(x))
        return exp_x / np.sum(exp_x)

    def encode_symbolic(self, predicate: Predicate) -> np.ndarray:
        """Codifica predicado simbólico em vetor"""
        embedding = np.zeros(self.input_dim)
        name_hash = hash(predicate.name) % (self.input_dim // 2)
        embedding[name_hash] = 1.0
        for i, arg in enumerate(predicate.arguments):
            arg_hash = hash(str(arg)) % (self.input_dim // 2)
            embedding[self.input_dim // 2 + arg_hash] = 1.0 / (i + 1)
        embedding[-1] = predicate.confidence
        return embedding

    def decode_neural(self, vector: np.ndarray, threshold: float=0.5) -> List[str]:
        """Decodifica vetor neural em conceitos simbólicos"""
        concepts = []
        active_dims = np.where(vector > threshold)[0]
        for dim in active_dims:
            concept = f'concept_{dim}'
            concepts.append(concept)
        return concepts

class SymbolicReasoner:
    """Componente de raciocínio simbólico"""

    def __init__(self):
        self.facts: Set[Predicate] = set()
        self.rules: List[Rule] = []
        self.inference_cache: Dict[str, Any] = {}

    def add_fact(self, fact: Predicate):
        """Adiciona fato à base de conhecimento"""
        self.facts.add(fact)
        self.inference_cache.clear()

    def add_rule(self, rule: Rule):
        """Adiciona regra de inferência"""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: -r.priority)

    def forward_chaining(self, max_iterations: int=100) -> Set[Predicate]:
        """Forward chaining para derivar novos fatos"""
        new_facts = set()
        fact_strings = {str(f) for f in self.facts}
        for _ in range(max_iterations):
            added_this_iteration = False
            for rule in self.rules:
                if rule.can_fire(fact_strings):
                    new_fact = rule.consequent
                    if str(new_fact) not in fact_strings:
                        new_facts.add(new_fact)
                        fact_strings.add(str(new_fact))
                        added_this_iteration = True
            if not added_this_iteration:
                break
        return new_facts

    def backward_chaining(self, goal: Predicate, depth: int=10) -> Optional[List[Rule]]:
        """Backward chaining para provar objetivo"""
        if depth <= 0:
            return None
        if goal in self.facts:
            return []
        for rule in self.rules:
            if self._unify(rule.consequent, goal):
                proof_chain = [rule]
                all_proven = True
                for antecedent in rule.antecedents:
                    sub_proof = self.backward_chaining(antecedent, depth - 1)
                    if sub_proof is None:
                        all_proven = False
                        break
                    proof_chain.extend(sub_proof)
                if all_proven:
                    return proof_chain
        return None

    def _unify(self, pred1: Predicate, pred2: Predicate) -> Optional[Dict[str, Any]]:
        """Unificação de predicados"""
        if pred1.name != pred2.name:
            return None
        if len(pred1.arguments) != len(pred2.arguments):
            return None
        bindings = {}
        for arg1, arg2 in zip(pred1.arguments, pred2.arguments):
            if isinstance(arg1, str) and arg1.startswith('?'):
                if arg1 in bindings:
                    if bindings[arg1] != arg2:
                        return None
                else:
                    bindings[arg1] = arg2
            elif isinstance(arg2, str) and arg2.startswith('?'):
                if arg2 in bindings:
                    if bindings[arg2] != arg1:
                        return None
                else:
                    bindings[arg2] = arg1
            elif arg1 != arg2:
                return None
        return bindings

    def resolution(self, clauses: List[List[Predicate]], goal: Predicate) -> bool:
        """Resolução para provar objetivo"""
        clauses = clauses.copy()
        clauses.append([Predicate(f'NOT_{goal.name}', goal.arguments)])
        new_clauses = set()
        while True:
            n = len(clauses)
            for i in range(n):
                for j in range(i + 1, n):
                    resolvents = self._resolve(clauses[i], clauses[j])
                    if [] in resolvents:
                        return True
                    new_clauses.update((tuple(r) for r in resolvents))
            new_as_lists = [list(c) for c in new_clauses]
            if all((c in clauses for c in new_as_lists)):
                return False
            clauses.extend(new_as_lists)

    def _resolve(self, clause1: List[Predicate], clause2: List[Predicate]) -> List[List[Predicate]]:
        """Aplica regra de resolução entre duas cláusulas"""
        resolvents = []
        for p1 in clause1:
            for p2 in clause2:
                if p1.name == f'NOT_{p2.name}' or p2.name == f'NOT_{p1.name}':
                    bindings = self._unify(p1, p2)
                    if bindings is not None:
                        new_clause = []
                        for p in clause1:
                            if p != p1:
                                new_clause.append(self._apply_bindings(p, bindings))
                        for p in clause2:
                            if p != p2:
                                new_clause.append(self._apply_bindings(p, bindings))
                        resolvents.append(new_clause)
        return resolvents

    def _apply_bindings(self, pred: Predicate, bindings: Dict[str, Any]) -> Predicate:
        """Aplica bindings a um predicado"""
        new_args = []
        for arg in pred.arguments:
            if isinstance(arg, str) and arg in bindings:
                new_args.append(bindings[arg])
            else:
                new_args.append(arg)
        return Predicate(pred.name, new_args, pred.truth_value, pred.confidence)

class ProbabilisticReasoner:
    """Raciocínio probabilístico com redes Bayesianas"""

    def __init__(self):
        self.network = nx.DiGraph()
        self.cpds: Dict[str, Dict] = {}
        self.evidence: Dict[str, Any] = {}

    def add_node(self, node: str, states: List[Any]):
        """Adiciona nó à rede Bayesiana"""
        self.network.add_node(node, states=states)

    def add_edge(self, parent: str, child: str):
        """Adiciona dependência probabilística"""
        self.network.add_edge(parent, child)

    def set_cpd(self, node: str, cpd: Dict):
        """Define distribuição de probabilidade condicional"""
        self.cpds[node] = cpd

    def set_evidence(self, evidence: Dict[str, Any]):
        """Define evidência observada"""
        self.evidence = evidence

    def variable_elimination(self, query: str) -> Dict[Any, float]:
        """Inferência por eliminação de variáveis"""
        if query not in self.network:
            return {}
        if not self.evidence and query in self.cpds:
            return self.cpds[query].get('prior', {})
        posterior = {}
        states = self.network.nodes[query].get('states', [])
        for state in states:
            prob = self._calculate_posterior(query, state)
            posterior[state] = prob
        total = sum(posterior.values())
        if total > 0:
            posterior = {k: v / total for k, v in posterior.items()}
        return posterior

    def _calculate_posterior(self, query: str, state: Any) -> float:
        """Calcula probabilidade posterior"""
        prior = self.cpds.get(query, {}).get('prior', {}).get(state, 0.5)
        adjustment = 1.0
        for evidence_var, evidence_val in self.evidence.items():
            if self.network.has_edge(evidence_var, query):
                cpd_entry = self.cpds.get(query, {}).get('conditional', {})
                if (evidence_var, evidence_val, state) in cpd_entry:
                    adjustment *= cpd_entry[evidence_var, evidence_val, state]
        return prior * adjustment

class NeuralSymbolicReasoner:
    """
    Motor de raciocínio híbrido neural-simbólico
    Combina aprendizado neural com lógica simbólica
    """

    def __init__(self, knowledge_base: Optional[Path]=None):
        self.knowledge_graph = KnowledgeGraph()
        self.neural_component = NeuralComponent()
        self.symbolic_reasoner = SymbolicReasoner()
        self.probabilistic_reasoner = ProbabilisticReasoner()
        self.reasoning_cache: Dict[str, Explanation] = {}
        self.metrics = defaultdict(float)
        self.executor = ThreadPoolExecutor(max_workers=4)
        if knowledge_base and knowledge_base.exists():
            self.load_knowledge_base(knowledge_base)
        logger.info('Neural-Symbolic Reasoner initialized')

    def load_knowledge_base(self, path: Path):
        """Carrega base de conhecimento"""
        try:
            with open(path, 'r') as f:
                kb = json.load(f)
            for concept_data in kb.get('concepts', []):
                concept = Concept(**concept_data)
                self.knowledge_graph.add_concept(concept)
            for relation in kb.get('relations', []):
                self.knowledge_graph.add_relation(relation['subject'], relation['relation'], relation['object'])
            for rule_data in kb.get('rules', []):
                antecedents = [Predicate(**a) for a in rule_data['antecedents']]
                consequent = Predicate(**rule_data['consequent'])
                rule = Rule(id=rule_data['id'], antecedents=antecedents, consequent=consequent, confidence=rule_data.get('confidence', 1.0))
                self.symbolic_reasoner.add_rule(rule)
                self.knowledge_graph.add_rule(rule)
            logger.info(f'Loaded knowledge base with {len(self.knowledge_graph.concepts)} concepts')
        except Exception as e:
            logger.error(f'Failed to load knowledge base: {e}')

    async def reason(self, query: Union[str, Predicate], context: Optional[Dict]=None) -> Explanation:
        """
        Realiza raciocínio sobre query
        Combina métodos neurais e simbólicos
        """
        if isinstance(query, str):
            query = self._parse_query(query)
        cache_key = str(query)
        if cache_key in self.reasoning_cache:
            return self.reasoning_cache[cache_key]
        strategy = self._select_reasoning_strategy(query, context)
        if strategy == ReasoningType.DEDUCTIVE:
            explanation = await self._deductive_reasoning(query, context)
        elif strategy == ReasoningType.INDUCTIVE:
            explanation = await self._inductive_reasoning(query, context)
        elif strategy == ReasoningType.ABDUCTIVE:
            explanation = await self._abductive_reasoning(query, context)
        elif strategy == ReasoningType.ANALOGICAL:
            explanation = await self._analogical_reasoning(query, context)
        elif strategy == ReasoningType.PROBABILISTIC:
            explanation = await self._probabilistic_reasoning(query, context)
        else:
            explanation = await self._hybrid_reasoning(query, context)
        self.reasoning_cache[cache_key] = explanation
        self.metrics[f'reasoning.{strategy.value}'] += 1
        return explanation

    def _parse_query(self, query_str: str) -> Predicate:
        """Parse query string em predicado"""
        parts = query_str.strip().split('(')
        if len(parts) == 2:
            name = parts[0]
            args_str = parts[1].rstrip(')')
            args = [a.strip() for a in args_str.split(',')]
            return Predicate(name, args)
        else:
            return Predicate(query_str, [])

    def _select_reasoning_strategy(self, query: Predicate, context: Optional[Dict]) -> ReasoningType:
        """Seleciona estratégia de raciocínio apropriada"""
        if context and context.get('strategy'):
            return ReasoningType[context['strategy'].upper()]
        applicable_rules = [r for r in self.symbolic_reasoner.rules if self.symbolic_reasoner._unify(r.consequent, query)]
        if applicable_rules:
            return ReasoningType.DEDUCTIVE
        similar_facts = self._find_similar_facts(query)
        if len(similar_facts) > 10:
            return ReasoningType.INDUCTIVE
        if 'probability' in query.name.lower() or 'likely' in query.name.lower():
            return ReasoningType.PROBABILISTIC
        return ReasoningType.PROBABILISTIC

    def _find_similar_facts(self, query: Predicate) -> List[Predicate]:
        """Encontra fatos similares ao query"""
        similar = []
        for fact in self.symbolic_reasoner.facts:
            if fact.name == query.name:
                similar.append(fact)
            elif len(fact.arguments) == len(query.arguments):
                similarity = sum((1 for a1, a2 in zip(fact.arguments, query.arguments) if a1 == a2 or (isinstance(a2, str) and a2.startswith('?'))))
                if similarity >= len(query.arguments) // 2:
                    similar.append(fact)
        return similar

    def _deductive_reasoning(self, query: Predicate, context: Optional[Dict]) -> Explanation:
        """Raciocínio dedutivo usando regras lógicas"""
        proof = self.symbolic_reasoner.backward_chaining(query)
        if proof:
            steps = []
            for rule in proof:
                steps.append({'type': 'rule_application', 'rule': str(rule), 'confidence': rule.confidence})
            explanation = Explanation(conclusion=query, reasoning_type=ReasoningType.DEDUCTIVE, steps=steps, confidence=min((r.confidence for r in proof)), supporting_facts=list(self.symbolic_reasoner.facts), rules_used=proof, natural_language=self._generate_explanation_text(query, steps), formal_proof=self._format_formal_proof(proof))
            return explanation
        new_facts = self.symbolic_reasoner.forward_chaining()
        if query in new_facts:
            return Explanation(conclusion=query, reasoning_type=ReasoningType.DEDUCTIVE, steps=[{'type': 'forward_chaining', 'new_facts': len(new_facts)}], confidence=0.8, supporting_facts=list(self.symbolic_reasoner.facts), rules_used=[], natural_language=f'Deduced {query} through forward chaining')
        return self._create_failure_explanation(query, ReasoningType.DEDUCTIVE)

    def _inductive_reasoning(self, query: Predicate, context: Optional[Dict]) -> Explanation:
        """Raciocínio indutivo - generalização de exemplos"""
        similar_facts = self._find_similar_facts(query)
        if len(similar_facts) < 3:
            return self._create_failure_explanation(query, ReasoningType.INDUCTIVE)
        patterns = self._extract_patterns(similar_facts)
        confidence = len(similar_facts) / (len(similar_facts) + 10)
        embeddings = [self.neural_component.encode_symbolic(f) for f in similar_facts]
        pattern_vector = np.mean(embeddings, axis=0)
        query_vector = self.neural_component.encode_symbolic(query)
        similarity = np.dot(pattern_vector, query_vector) / (np.linalg.norm(pattern_vector) * np.linalg.norm(query_vector) + 1e-08)
        adjusted_confidence = confidence * 0.7 + similarity * 0.3
        return Explanation(conclusion=query, reasoning_type=ReasoningType.INDUCTIVE, steps=[{'type': 'pattern_extraction', 'patterns': patterns}, {'type': 'neural_similarity', 'score': float(similarity)}], confidence=adjusted_confidence, supporting_facts=similar_facts, rules_used=[], natural_language=f'Induced {query} from {len(similar_facts)} similar examples')

    def _extract_patterns(self, facts: List[Predicate]) -> List[Dict]:
        """Extrai padrões de lista de fatos"""
        patterns = []
        if facts:
            common_args = defaultdict(int)
            for fact in facts:
                for arg in fact.arguments:
                    if not isinstance(arg, str) or not arg.startswith('?'):
                        common_args[arg] += 1
            patterns.append({'type': 'common_arguments', 'arguments': dict(common_args)})
        arg_lengths = [len(f.arguments) for f in facts]
        if arg_lengths:
            patterns.append({'type': 'structure', 'avg_args': sum(arg_lengths) / len(arg_lengths), 'min_args': min(arg_lengths), 'max_args': max(arg_lengths)})
        return patterns

    def _abductive_reasoning(self, query: Predicate, context: Optional[Dict]) -> Explanation:
        """Raciocínio abdutivo - melhor explicação"""
        hypotheses = self._generate_hypotheses(query, context)
        if not hypotheses:
            return self._create_failure_explanation(query, ReasoningType.ABDUCTIVE)
        best_hypothesis = None
        best_score = -1
        for hypothesis in hypotheses:
            score = self._evaluate_hypothesis(hypothesis, query, context)
            if score > best_score:
                best_score = score
                best_hypothesis = hypothesis
        return Explanation(conclusion=query, reasoning_type=ReasoningType.ABDUCTIVE, steps=[{'type': 'hypothesis_generation', 'count': len(hypotheses)}, {'type': 'best_hypothesis', 'hypothesis': str(best_hypothesis)}], confidence=best_score, supporting_facts=[best_hypothesis] if best_hypothesis else [], rules_used=[], natural_language=f'Best explanation for {query}: {best_hypothesis}')

    def _generate_hypotheses(self, observation: Predicate, context: Optional[Dict]) -> List[Predicate]:
        """Gera hipóteses possíveis para explicar observação"""
        hypotheses = []
        for rule in self.symbolic_reasoner.rules:
            if self.symbolic_reasoner._unify(rule.consequent, observation):
                hypotheses.extend(rule.antecedents)
        if observation.name in self.knowledge_graph.graph:
            related = self.knowledge_graph.get_related_concepts(observation.name)
            for concept in related[:5]:
                hypotheses.append(Predicate(f'caused_by', [concept, observation.name]))
        return hypotheses

    def _evaluate_hypothesis(self, hypothesis: Predicate, observation: Predicate, context: Optional[Dict]) -> float:
        """Avalia qualidade de uma hipótese"""
        score = 0.5
        if hypothesis in self.symbolic_reasoner.facts:
            score += 0.3
        self.symbolic_reasoner.facts.add(hypothesis)
        new_facts = self.symbolic_reasoner.forward_chaining(max_iterations=5)
        if observation in new_facts:
            score += 0.2
        self.symbolic_reasoner.facts.remove(hypothesis)
        return min(1.0, score)

    def _analogical_reasoning(self, query: Predicate, context: Optional[Dict]) -> Explanation:
        """Raciocínio analógico - baseado em similaridade"""
        similar_case = self._find_most_similar_case(query)
        if not similar_case:
            return self._create_failure_explanation(query, ReasoningType.ANALOGICAL)
        mapping = self._create_analogy_mapping(similar_case, query)
        conclusion = self._apply_analogy_mapping(similar_case, mapping)
        similarity = self._calculate_similarity(similar_case, query)
        return Explanation(conclusion=conclusion, reasoning_type=ReasoningType.ANALOGICAL, steps=[{'type': 'similar_case', 'case': str(similar_case)}, {'type': 'mapping', 'map': mapping}, {'type': 'similarity', 'score': similarity}], confidence=similarity, supporting_facts=[similar_case], rules_used=[], natural_language=f'By analogy with {similar_case}, conclude {conclusion}')

    def _find_most_similar_case(self, query: Predicate) -> Optional[Predicate]:
        """Encontra caso mais similar na base de conhecimento"""
        best_match = None
        best_similarity = 0
        for fact in self.symbolic_reasoner.facts:
            similarity = self._calculate_similarity(fact, query)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = fact
        return best_match if best_similarity > 0.5 else None

    def _calculate_similarity(self, pred1: Predicate, pred2: Predicate) -> float:
        """Calcula similaridade entre predicados"""
        name_sim = 1.0 if pred1.name == pred2.name else 0.3
        if len(pred1.arguments) == 0 or len(pred2.arguments) == 0:
            arg_sim = 0.5
        else:
            matching = sum((1 for a1, a2 in zip(pred1.arguments, pred2.arguments) if a1 == a2))
            arg_sim = matching / max(len(pred1.arguments), len(pred2.arguments))
        return name_sim * 0.4 + arg_sim * 0.6

    def _create_analogy_mapping(self, source: Predicate, target: Predicate) -> Dict[str, str]:
        """Cria mapeamento de analogia"""
        mapping = {}
        for s_arg, t_arg in zip(source.arguments, target.arguments):
            if s_arg != t_arg:
                mapping[str(s_arg)] = str(t_arg)
        return mapping

    def _apply_analogy_mapping(self, source: Predicate, mapping: Dict[str, str]) -> Predicate:
        """Aplica mapeamento analógico"""
        new_args = []
        for arg in source.arguments:
            arg_str = str(arg)
            if arg_str in mapping:
                new_args.append(mapping[arg_str])
            else:
                new_args.append(arg)
        return Predicate(source.name, new_args, confidence=source.confidence * 0.8)

    def _probabilistic_reasoning(self, query: Predicate, context: Optional[Dict]) -> Explanation:
        """Raciocínio probabilístico"""
        if context and 'evidence' in context:
            self.probabilistic_reasoner.set_evidence(context['evidence'])
        query_var = query.name
        if query_var in self.probabilistic_reasoner.network:
            posterior = self.probabilistic_reasoner.variable_elimination(query_var)
            if posterior:
                best_state = max(posterior, key=posterior.get)
                confidence = posterior[best_state]
                return Explanation(conclusion=Predicate(query.name, [best_state], confidence=confidence), reasoning_type=ReasoningType.PROBABILISTIC, steps=[{'type': 'bayesian_inference', 'posterior': posterior}], confidence=confidence, supporting_facts=[], rules_used=[], natural_language=f'P({query_var}={best_state}|evidence) = {confidence:.3f}')
        similar = self._find_similar_facts(query)
        if similar:
            confidence = len([f for f in similar if f.truth_value]) / len(similar)
        else:
            confidence = 0.5
        return Explanation(conclusion=query, reasoning_type=ReasoningType.PROBABILISTIC, steps=[{'type': 'frequency_estimate', 'samples': len(similar)}], confidence=confidence, supporting_facts=similar, rules_used=[], natural_language=f'Estimated probability: {confidence:.3f}')

    async def _hybrid_reasoning(self, query: Predicate, context: Optional[Dict]) -> Explanation:
        """
        Raciocínio híbrido combinando neural e simbólico
        """
        query_vector = self.neural_component.encode_symbolic(query)
        neural_output = self.neural_component.forward(query_vector)
        relevant_concepts = self.neural_component.decode_neural(neural_output)
        for concept in relevant_concepts:
            self.symbolic_reasoner.add_fact(Predicate('relevant', [concept, query.name]))
        strategies = [self._deductive_reasoning(query, context), self._inductive_reasoning(query, context), self._probabilistic_reasoning(query, context)]
        results = await asyncio.gather(*strategies, return_exceptions=True)
        best_explanation = None
        best_confidence = 0
        for result in results:
            if isinstance(result, Explanation) and result.confidence > best_confidence:
                best_confidence = result.confidence
                best_explanation = result
        if best_explanation:
            best_explanation.steps.append({'type': 'neural_processing', 'relevant_concepts': relevant_concepts})
            return best_explanation
        return self._create_failure_explanation(query, ReasoningType.PROBABILISTIC)

    def _create_failure_explanation(self, query: Predicate, reasoning_type: ReasoningType) -> Explanation:
        """Cria explicação para falha de raciocínio"""
        return Explanation(conclusion=query, reasoning_type=reasoning_type, steps=[{'type': 'failure', 'reason': 'insufficient_evidence'}], confidence=0.0, supporting_facts=[], rules_used=[], natural_language=f'Could not establish {query} using {reasoning_type.value} reasoning')

    def _generate_explanation_text(self, conclusion: Predicate, steps: List[Dict]) -> str:
        """Gera explicação em linguagem natural"""
        text = f'To conclude {conclusion}:\n'
        for i, step in enumerate(steps, 1):
            if step['type'] == 'rule_application':
                text += f"{i}. Applied rule: {step['rule']}\n"
            elif step['type'] == 'forward_chaining':
                text += f"{i}. Derived {step['new_facts']} new facts through forward chaining\n"
            else:
                text += f"{i}. {step['type']}: {step}\n"
        return text

    def _format_formal_proof(self, proof: List[Rule]) -> str:
        """Formata prova formal"""
        lines = []
        for i, rule in enumerate(proof, 1):
            lines.append(f'{i}. {rule}')
        return '\n'.join(lines)

    def add_knowledge(self, fact: Union[Predicate, Concept, Rule]):
        """Adiciona conhecimento ao sistema"""
        if isinstance(fact, Predicate):
            self.symbolic_reasoner.add_fact(fact)
        elif isinstance(fact, Concept):
            self.knowledge_graph.add_concept(fact)
        elif isinstance(fact, Rule):
            self.symbolic_reasoner.add_rule(fact)
            self.knowledge_graph.add_rule(fact)
        self.reasoning_cache.clear()

    def explain_concept(self, concept_name: str) -> Dict:
        """Explica um conceito usando o grafo de conhecimento"""
        if concept_name not in self.knowledge_graph.concepts:
            return {'error': 'Concept not found'}
        concept = self.knowledge_graph.concepts[concept_name]
        subgraph = self.knowledge_graph.query_subgraph(concept_name)
        return {'concept': concept_name, 'properties': concept.properties, 'relations': concept.relations, 'connected_concepts': list(subgraph.nodes()), 'graph_size': len(subgraph.nodes())}

async def test_neural_symbolic_reasoning():
    """Testa raciocínio neural-simbólico"""
    reasoner = NeuralSymbolicReasoner()
    reasoner.add_knowledge(Predicate('mortal', ['Socrates'], truth_value=True))
    reasoner.add_knowledge(Predicate('human', ['Socrates'], truth_value=True))
    reasoner.add_knowledge(Predicate('philosopher', ['Socrates'], truth_value=True))
    rule = Rule(id='human_mortal', antecedents=[Predicate('human', ['?X'])], consequent=Predicate('mortal', ['?X']), confidence=1.0)
    reasoner.add_knowledge(rule)
    query = Predicate('mortal', ['Plato'])
    reasoner.add_knowledge(Predicate('human', ['Plato'], truth_value=True))
    explanation = await reasoner.reason(query, {'strategy': 'deductive'})
    print(f'Deductive reasoning:')
    print(f'  Conclusion: {explanation.conclusion}')
    print(f'  Confidence: {explanation.confidence}')
    print(f'  Explanation: {explanation.natural_language}')
    reasoner.add_knowledge(Predicate('flies', ['bird1'], truth_value=True))
    reasoner.add_knowledge(Predicate('flies', ['bird2'], truth_value=True))
    reasoner.add_knowledge(Predicate('flies', ['bird3'], truth_value=True))
    query2 = Predicate('flies', ['bird4'])
    explanation2 = await reasoner.reason(query2, {'strategy': 'inductive'})
    print(f'\nInductive reasoning:')
    print(f'  Conclusion: {explanation2.conclusion}')
    print(f'  Confidence: {explanation2.confidence}')
    query3 = Predicate('wise', ['Socrates'])
    explanation3 = await reasoner.reason(query3)
    print(f'\nHybrid reasoning:')
    print(f'  Type: {explanation3.reasoning_type.value}')
    print(f'  Confidence: {explanation3.confidence}')
if __name__ == '__main__':
    asyncio.run(test_neural_symbolic_reasoning())