#!/usr/bin/env python3
"""
Sistema de Looping Contínuo - Análise Cruzada Teoria x Roteiros
Aplica cada uma das 13 teorias a todos os roteiros e aprende continuamente
"""

import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any
from collections import defaultdict

# Adiciona src ao path
sys.path.insert(0, 'src')

from scripturemon_champion.core.profiles import LearningProfiles
from scripturemon_champion.analysis.script_doctor import ScriptDoctor
from scripturemon_champion.analysis.theory import TheoryComparator
from scripturemon_champion.learning.learning_lite import LearningLite
from scripturemon_champion.core.memory import UnifiedMemory, MemoryRecord

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f'continuous_learning_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ContinuousTheoryLearning:
    """Sistema de aprendizado contínuo com análise cruzada teoria x roteiros"""

    def __init__(self, profile: str = 'token_turbo'):
        logger.info(f"🚀 Iniciando Sistema de Looping Contínuo com perfil {profile.upper()}")

        # Configuração do perfil
        self.profile = LearningProfiles.get_profile(profile)
        self.config = self.profile.config

        # Componentes
        self.doctor = ScriptDoctor(use_learning=True)
        self.learning = LearningLite()
        self.theory = TheoryComparator(Path("theory"))
        self.memory = UnifiedMemory(Path("data/unified_memory.db"))

        # Pastas
        self.screenplays_path = Path("my_screenplays")
        self.theory_path = Path("theory")

        # Estatísticas
        self.stats = {
            'start_time': datetime.now(),
            'iterations': 0,
            'total_analyses': 0,
            'learnings': defaultdict(list),
            'categories': {
                'universal_good': [],  # Bom para qualquer obra
                'series_only': [],     # Só serve para séries
                'personal': [],        # Só serve para mim
                'genre_specific': defaultdict(list)  # Por gênero
            }
        }

        # Cache de análises
        self.cache = {}

    def load_all_content(self) -> Tuple[List[Path], List[Path]]:
        """Carrega todos os roteiros e teorias"""
        screenplays = list(self.screenplays_path.glob("*.txt"))
        theories = list(self.theory_path.glob("*.txt"))

        logger.info(f"📚 Carregados: {len(screenplays)} roteiros, {len(theories)} teorias")
        logger.info(f"📊 Total de combinações: {len(screenplays) * len(theories)}")

        return screenplays, theories

    def analyze_with_theory(self, screenplay_path: Path, theory_path: Path) -> Dict[str, Any]:
        """Analisa um roteiro sob a perspectiva de uma teoria específica"""

        # Cache key
        cache_key = f"{screenplay_path.stem}_{theory_path.stem}"

        # Verificar cache
        if cache_key in self.cache:
            logger.debug(f"⚡ Usando cache para {cache_key}")
            return self.cache[cache_key]

        logger.info(f"🔍 Analisando {screenplay_path.stem} com teoria {theory_path.stem[:30]}...")

        try:
            # Carregar textos
            screenplay_text = screenplay_path.read_text(encoding='utf-8', errors='ignore')
            theory_text = theory_path.read_text(encoding='utf-8', errors='ignore')

            # Análise básica do roteiro
            analysis = self.doctor.analyze_script(screenplay_text, screenplay_path.stem)
            stc = self.doctor.analyze_save_the_cat(screenplay_text)

            # Extrair conceitos da teoria
            theory_concepts = self.extract_theory_concepts(theory_text, theory_path.stem)

            # Comparar roteiro com teoria
            connections = self.find_connections(analysis, stc, theory_concepts)

            # Categorizar aprendizados
            category = self.categorize_learning(connections, analysis, theory_path.stem)

            result = {
                'screenplay': screenplay_path.stem,
                'theory': theory_path.stem,
                'analysis': {
                    'scenes': analysis.scenes,
                    'characters': len(analysis.top_characters),
                    'dialogue_ratio': analysis.dialogue_ratio,
                    'pacing': analysis.pacing_score,
                    'beats_found': len(stc.beats),
                    'beats_missing': len(stc.missing_beats)
                },
                'theory_concepts': theory_concepts,
                'connections': connections,
                'category': category,
                'timestamp': datetime.now().isoformat()
            }

            # Cachear resultado
            self.cache[cache_key] = result

            return result

        except Exception as e:
            logger.error(f"❌ Erro analisando {cache_key}: {e}")
            return {'error': str(e), 'screenplay': screenplay_path.stem, 'theory': theory_path.stem}

    def extract_theory_concepts(self, theory_text: str, theory_name: str) -> Dict[str, Any]:
        """Extrai conceitos chave de um texto teórico"""

        concepts = {
            'name': theory_name,
            'key_terms': [],
            'principles': [],
            'techniques': []
        }

        # Identificar tipo de teoria
        text_lower = theory_text.lower()

        # Save the Cat específico
        if 'save the cat' in theory_name.lower():
            concepts['key_terms'] = ['catalyst', 'debate', 'break into two', 'b story',
                                     'fun and games', 'midpoint', 'bad guys close in',
                                     'all is lost', 'dark night', 'finale']
            concepts['principles'] = ['15 beats structure', 'genre expectations', 'primal needs']
            concepts['techniques'] = ['beat sheet', 'logline', 'boards']

        # Story (McKee)
        elif 'story' in theory_name.lower() or 'mckee' in theory_name.lower():
            concepts['key_terms'] = ['inciting incident', 'progressive complications',
                                     'crisis', 'climax', 'resolution']
            concepts['principles'] = ['story values', 'controlling idea', 'spine']
            concepts['techniques'] = ['scene analysis', 'value shifts', 'gap between expectation and result']

        # Character
        elif 'character' in theory_name.lower():
            concepts['key_terms'] = ['want', 'need', 'ghost', 'lie', 'truth']
            concepts['principles'] = ['character arc', 'internal conflict', 'transformation']
            concepts['techniques'] = ['backstory', 'voice', 'dimensionality']

        # Dialogue
        elif 'dialogue' in theory_name.lower():
            concepts['key_terms'] = ['subtext', 'exposition', 'conflict', 'voice']
            concepts['principles'] = ['show dont tell', 'naturalistic', 'purposeful']
            concepts['techniques'] = ['indirection', 'compression', 'authenticity']

        # Hero's Journey
        elif 'hero' in theory_name.lower() or 'mil faces' in theory_name.lower():
            concepts['key_terms'] = ['ordinary world', 'call to adventure', 'refusal',
                                     'mentor', 'threshold', 'tests', 'ordeal', 'reward', 'return']
            concepts['principles'] = ['monomyth', 'archetypes', 'transformation']
            concepts['techniques'] = ['circular structure', 'symbolic death and rebirth']

        # Anatomy of Story
        elif 'anatomy' in theory_name.lower():
            concepts['key_terms'] = ['premise', 'seven steps', 'moral argument', 'story world']
            concepts['principles'] = ['organic unity', 'moral vision', 'story body']
            concepts['techniques'] = ['22 steps', 'four corners opposition', 'reveals sequence']

        # Genérico para outros
        else:
            # Extrair termos frequentes
            import re
            from collections import Counter

            # Palavras técnicas comuns em teoria de roteiro
            technical_terms = ['protagonist', 'antagonist', 'conflict', 'theme', 'plot',
                              'structure', 'arc', 'scene', 'sequence', 'act', 'beat',
                              'character', 'dialogue', 'action', 'tension', 'stakes']

            words = re.findall(r'\b[a-z]+\b', text_lower)
            word_freq = Counter(words)

            # Filtrar termos técnicos que aparecem
            for term in technical_terms:
                if word_freq.get(term, 0) > 5:  # Aparece mais de 5 vezes
                    concepts['key_terms'].append(term)

            concepts['principles'] = ['narrative structure', 'character development', 'thematic unity']
            concepts['techniques'] = ['scene construction', 'pacing', 'conflict escalation']

        return concepts

    def find_connections(self, analysis, stc, theory_concepts: Dict) -> List[Dict]:
        """Encontra conexões entre análise e conceitos teóricos"""

        connections = []

        # Verificar beats (Save the Cat)
        if 'save the cat' in theory_concepts['name'].lower():
            for beat in stc.beats:
                if beat.name.lower() in [t.lower() for t in theory_concepts['key_terms']]:
                    connections.append({
                        'type': 'beat_match',
                        'element': beat.name,
                        'strength': beat.confidence,
                        'theory_validation': True
                    })

        # Verificar estrutura
        if analysis.scenes > 0:
            # Three act structure
            if analysis.scenes < 30:  # Curta
                structure_type = 'short_form'
            elif analysis.scenes < 60:  # Média
                structure_type = 'feature_film'
            else:  # Longa/série
                structure_type = 'series_episodic'

            connections.append({
                'type': 'structure',
                'element': structure_type,
                'strength': 0.8,
                'theory_validation': structure_type in ['feature_film']
            })

        # Verificar diálogo
        if 'dialogue' in theory_concepts['name'].lower():
            if 0.2 <= analysis.dialogue_ratio <= 0.4:
                connections.append({
                    'type': 'dialogue_balance',
                    'element': 'optimal_ratio',
                    'strength': 0.9,
                    'theory_validation': True
                })

        # Verificar personagens
        if 'character' in theory_concepts['name'].lower():
            if len(analysis.top_characters) >= 3:
                connections.append({
                    'type': 'character_ensemble',
                    'element': f'{len(analysis.top_characters)} main characters',
                    'strength': 0.7,
                    'theory_validation': True
                })

        # Verificar pacing
        if analysis.pacing_score > 0.6:
            connections.append({
                'type': 'pacing',
                'element': 'good_rhythm',
                'strength': analysis.pacing_score,
                'theory_validation': True
            })

        return connections

    def categorize_learning(self, connections: List[Dict], analysis, theory_name: str) -> str:
        """Categoriza o aprendizado em universal, série ou pessoal"""

        # Contar validações positivas
        validations = sum(1 for c in connections if c.get('theory_validation', False))
        total = len(connections)

        if total == 0:
            return 'needs_more_data'

        validation_ratio = validations / total

        # Regras de categorização

        # Universal: Alta validação teórica + estrutura de filme
        if validation_ratio > 0.7 and any(c['element'] == 'feature_film' for c in connections if c['type'] == 'structure'):
            category = 'universal_good'
            reason = f"Alta aderência à teoria {theory_name[:20]} ({validation_ratio:.0%})"

        # Série: Estrutura episódica ou muitos personagens
        elif any(c['element'] == 'series_episodic' for c in connections if c['type'] == 'structure') or \
             len(analysis.top_characters) > 10:
            category = 'series_only'
            reason = f"Estrutura episódica ou ensemble grande"

        # Pessoal: Baixa validação ou estrutura experimental
        elif validation_ratio < 0.3 or analysis.scenes < 20:
            category = 'personal'
            reason = f"Experimental ou muito específico"

        # Específico de gênero
        else:
            # Detectar gênero baseado em elementos
            if 'horror' in str(connections).lower() or 'thriller' in str(connections).lower():
                category = 'genre_specific:thriller'
            elif 'comedy' in str(connections).lower() or 'fun' in str(connections).lower():
                category = 'genre_specific:comedy'
            elif 'drama' in str(connections).lower() or 'character' in theory_name.lower():
                category = 'genre_specific:drama'
            else:
                category = 'genre_specific:general'
            reason = f"Específico para o gênero detectado"

        logger.info(f"  📁 Categorizado como {category}: {reason}")

        return category

    def save_learning(self, result: Dict):
        """Salva aprendizado na memória e estatísticas"""

        # Atualizar estatísticas
        category = result.get('category', 'unknown')

        if category == 'universal_good':
            self.stats['categories']['universal_good'].append(result)
        elif category == 'series_only':
            self.stats['categories']['series_only'].append(result)
        elif category == 'personal':
            self.stats['categories']['personal'].append(result)
        elif category.startswith('genre_specific:'):
            genre = category.split(':')[1]
            self.stats['categories']['genre_specific'][genre].append(result)

        # Salvar na memória unificada
        record = MemoryRecord(
            type='theory_learning',
            key=f"{result['screenplay']}_{result['theory']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            value=result,
            metadata={
                'category': category,
                'iteration': self.stats['iterations'],
                'profile': self.profile.name
            }
        )

        record_id = self.memory.store(record)
        logger.debug(f"  💾 Salvo na memória: ID {record_id}")

        # Aprender com o Learning system
        if 'analysis' in result:
            # Criar pseudo-análise para learning
            from scripturemon_champion.analysis.script_doctor import ScriptAnalysis
            pseudo_analysis = ScriptAnalysis(
                scenes=result['analysis']['scenes'],
                characters=result['analysis']['characters'],
                words=10000,  # Estimativa
                avg_scene_len=200,
                top_characters=['Unknown'],
                notes=[f"Analyzed with {result['theory']}"],
                dialogue_ratio=result['analysis']['dialogue_ratio'],
                pacing_score=result['analysis']['pacing'],
                beats=[]
            )

            concepts = self.learning.learn_from_analysis(
                pseudo_analysis,
                f"{result['screenplay']}_with_{result['theory'][:20]}"
            )

            logger.debug(f"  🧠 {len(concepts)} conceitos aprendidos")

    def print_status(self):
        """Imprime status atual do aprendizado"""

        elapsed = (datetime.now() - self.stats['start_time']).total_seconds()

        print("\n" + "=" * 80)
        print(f"📊 STATUS DO LOOPING CONTÍNUO - Iteração {self.stats['iterations']}")
        print("=" * 80)

        print(f"⏱️  Tempo decorrido: {elapsed/60:.1f} minutos")
        print(f"📈  Total de análises: {self.stats['total_analyses']}")
        print(f"⚡  Taxa: {self.stats['total_analyses']/(elapsed/60) if elapsed > 0 else 0:.1f} análises/min")

        print(f"\n📁 CATEGORIZAÇÃO DOS APRENDIZADOS:")
        print(f"  🌟 Universal (bom para todos): {len(self.stats['categories']['universal_good'])}")
        print(f"  📺 Só para séries: {len(self.stats['categories']['series_only'])}")
        print(f"  👤 Pessoal/experimental: {len(self.stats['categories']['personal'])}")

        if self.stats['categories']['genre_specific']:
            print(f"  🎭 Por gênero:")
            for genre, items in self.stats['categories']['genre_specific'].items():
                print(f"     • {genre}: {len(items)}")

        # Memória
        mem_stats = self.memory.stats()
        print(f"\n💾 Memória: {mem_stats.get('total_records', 0)} registros totais")

        # Learning stats
        learn_stats = self.learning.get_statistics()
        print(f"🧠 Learning: {learn_stats.get('total_beats', 0)} beats, "
              f"{learn_stats.get('unique_patterns', 0)} padrões únicos")

        print("=" * 80)

    def run_iteration(self, screenplays: List[Path], theories: List[Path]):
        """Executa uma iteração completa"""

        self.stats['iterations'] += 1
        logger.info(f"\n🔄 INICIANDO ITERAÇÃO {self.stats['iterations']}")

        for theory in theories:
            logger.info(f"\n📖 Aplicando teoria: {theory.stem[:40]}...")

            # Construir índice da teoria
            theory_text = theory.read_text(encoding='utf-8', errors='ignore')
            self.theory.index.add(theory.stem, theory_text)

            for screenplay in screenplays:
                # Analisar
                result = self.analyze_with_theory(screenplay, theory)

                if 'error' not in result:
                    # Salvar aprendizado
                    self.save_learning(result)
                    self.stats['total_analyses'] += 1

                    # Log de progresso
                    if self.stats['total_analyses'] % 5 == 0:
                        logger.info(f"  ✅ {self.stats['total_analyses']} análises completas")

                # Pequena pausa para não sobrecarregar
                time.sleep(0.1)

            # Status parcial a cada teoria
            if self.stats['iterations'] == 1:  # Primeira iteração, mais detalhes
                self.print_status()

    def run_continuous(self, max_iterations: int = None):
        """Executa o looping contínuo"""

        logger.info("🚀 INICIANDO LOOPING CONTÍNUO DE APRENDIZADO")
        logger.info(f"🎯 Perfil: {self.profile.name.upper()}")
        logger.info(f"📊 Contexto: {self.config['num_ctx']:,} tokens")

        # Carregar conteúdo
        screenplays, theories = self.load_all_content()

        if not screenplays or not theories:
            logger.error("❌ Sem conteúdo para processar!")
            return

        # Loop infinito ou até max_iterations
        iteration = 0
        try:
            while max_iterations is None or iteration < max_iterations:
                # Executar iteração
                self.run_iteration(screenplays, theories)

                iteration += 1

                # Status completo a cada 5 iterações
                if iteration % 5 == 0:
                    self.print_status()

                    # Salvar checkpoint
                    self.save_checkpoint()

                # Pausa entre iterações
                logger.info(f"💤 Pausa de 30 segundos antes da próxima iteração...")
                time.sleep(30)

        except KeyboardInterrupt:
            logger.info("\n⛔ Interrompido pelo usuário")

        finally:
            # Status final
            self.print_status()
            self.save_checkpoint()

            # Relatório final
            self.generate_final_report()

    def save_checkpoint(self):
        """Salva checkpoint do progresso"""

        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'stats': self.stats,
            'profile': self.profile.name,
            'cache_size': len(self.cache)
        }

        checkpoint_path = Path(f"checkpoint_theory_learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

        with open(checkpoint_path, 'w') as f:
            # Converter defaultdict para dict normal para serialização
            checkpoint['stats']['categories']['genre_specific'] = dict(checkpoint['stats']['categories']['genre_specific'])
            # Converter objetos datetime
            checkpoint['stats']['start_time'] = checkpoint['stats']['start_time'].isoformat()

            json.dump(checkpoint, f, indent=2, default=str)

        logger.info(f"💾 Checkpoint salvo: {checkpoint_path}")

    def generate_final_report(self):
        """Gera relatório final detalhado"""

        report = {
            'summary': {
                'total_iterations': self.stats['iterations'],
                'total_analyses': self.stats['total_analyses'],
                'duration': str(datetime.now() - self.stats['start_time']),
                'profile_used': self.profile.name
            },
            'categories': {
                'universal_good': len(self.stats['categories']['universal_good']),
                'series_only': len(self.stats['categories']['series_only']),
                'personal': len(self.stats['categories']['personal']),
                'genre_specific': {k: len(v) for k, v in self.stats['categories']['genre_specific'].items()}
            },
            'top_learnings': {
                'universal': self.stats['categories']['universal_good'][:5],
                'series': self.stats['categories']['series_only'][:5],
                'personal': self.stats['categories']['personal'][:5]
            }
        }

        report_path = Path(f"final_report_theory_learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        logger.info(f"📄 Relatório final salvo: {report_path}")

        # Imprimir resumo
        print("\n" + "=" * 80)
        print("🏆 RELATÓRIO FINAL DO LOOPING CONTÍNUO")
        print("=" * 80)
        print(f"✅ Total de análises: {report['summary']['total_analyses']}")
        print(f"⏱️ Duração: {report['summary']['duration']}")
        print(f"\n🎯 APRENDIZADOS CATEGORIZADOS:")
        print(f"  🌟 Universal (bom para todos): {report['categories']['universal_good']}")
        print(f"  📺 Específico para séries: {report['categories']['series_only']}")
        print(f"  👤 Pessoal/experimental: {report['categories']['personal']}")

        if report['categories']['genre_specific']:
            print(f"  🎭 Por gênero:")
            for genre, count in report['categories']['genre_specific'].items():
                print(f"     • {genre}: {count}")

        print("=" * 80)


if __name__ == "__main__":
    # Verificar argumentos
    import argparse

    parser = argparse.ArgumentParser(description="Sistema de Looping Contínuo - Teoria x Roteiros")
    parser.add_argument('--profile', default='token_turbo',
                       choices=['eco', 'dedicated', 'token_turbo'],
                       help='Perfil de aprendizado a usar')
    parser.add_argument('--iterations', type=int, default=None,
                       help='Número máximo de iterações (None = infinito)')
    parser.add_argument('--background', action='store_true',
                       help='Executar em background')

    args = parser.parse_args()

    # Criar e executar sistema
    system = ContinuousTheoryLearning(profile=args.profile)

    try:
        print("=" * 80)
        print("🧠 SISTEMA DE LOOPING CONTÍNUO - TEORIA x ROTEIROS")
        print("=" * 80)
        print(f"📚 Perfil: {args.profile.upper()}")
        print(f"🔄 Iterações: {'Infinitas' if args.iterations is None else args.iterations}")
        print(f"⚡ Modo: {'Background' if args.background else 'Foreground'}")
        print("-" * 80)
        print("Pressione Ctrl+C para parar a qualquer momento")
        print("=" * 80)
        print()

        # Executar
        system.run_continuous(max_iterations=args.iterations)

    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        raise