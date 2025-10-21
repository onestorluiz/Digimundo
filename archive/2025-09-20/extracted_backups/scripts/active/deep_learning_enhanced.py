#!/usr/bin/env python3
"""
🧠 DEEP SCREENPLAY LEARNING - Sistema Inteligente Completo
Com busca reversa, validação cruzada e cache inteligente
Gera documentação robusta e fundamentação profunda
"""

import sys
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

# Fix import path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from src.core.unified_memory_system import get_unified_memory, MemoryType

# Integration with other components
try:
    from scripts.active.integrated_system import get_integrated_system
except:
    pass  # Integration optional

from src.core.screenplay_library import get_screenplay_library

class DeepLearningEnhanced:
    """Sistema ML com inteligência avançada e documentação robusta"""

    def __init__(self):
        self.memory = get_unified_memory()
        self.library = get_screenplay_library()
        self.model = "mixtral-dedicated-q5"

        # Diretório para documentação robusta
        self.docs_dir = Path("data/deep_learning_docs")
        self.docs_dir.mkdir(exist_ok=True)

        # Config otimizada
        self.config = {
            'num_ctx': 131072,
            'num_thread': 24,
            'num_gpu': -1,
            'num_batch': 4096,
            'temperature': 0.3
        }

    # ==================== FUNÇÃO 1: BUSCA REVERSA ====================

    def why_this_works(self, scene_text: str, limit: int = 5) -> Dict[str, Any]:
        """
        Explica POR QUE uma cena funciona baseado na teoria cinematográfica.

        Args:
            scene_text: Trecho de roteiro para analisar
            limit: Número máximo de explicações teóricas

        Returns:
            Dict com análise profunda e documentada
        """

        timestamp = datetime.now().isoformat()
        scene_hash = hashlib.md5(scene_text.encode()).hexdigest()[:8]

        # Buscar conceitos relacionados na memória
        results = self.memory.search(
            query=scene_text[:500],  # Limitar busca
            memory_types=[MemoryType.KNOWLEDGE],
            limit=limit * 2  # Buscar mais para filtrar
        )

        # Filtrar e estruturar explicações
        explanations = []
        theories_found = set()

        for entry in results:
            if not entry.value or not isinstance(entry.value, dict):
                continue

            theory = entry.value.get('theory', '')
            concept = entry.value.get('name', entry.key)
            example = entry.value.get('example', '')

            # Evitar duplicatas de teoria
            theory_key = theory[:50] if theory else concept
            if theory_key in theories_found:
                continue
            theories_found.add(theory_key)

            if theory or example:
                explanations.append({
                    'concept': concept,
                    'theory': theory,
                    'example': example,
                    'confidence': entry.confidence,
                    'source': entry.metadata.get('source', 'unknown')
                })

        # Limitar ao número solicitado
        explanations = explanations[:limit]

        # Análise adicional com IA se não encontrou explicações suficientes
        if len(explanations) < 3:
            ai_analysis = self._analyze_with_ai(scene_text)
            if ai_analysis:
                explanations.extend(ai_analysis)

        # Preparar resultado estruturado
        result = {
            'scene_hash': scene_hash,
            'timestamp': timestamp,
            'scene_excerpt': scene_text[:200] + '...' if len(scene_text) > 200 else scene_text,
            'explanations': explanations,
            'theories_applied': len(theories_found),
            'confidence_avg': sum(e['confidence'] for e in explanations) / len(explanations) if explanations else 0
        }

        # Salvar documentação robusta
        self._save_robust_documentation(
            f"reverse_analysis_{scene_hash}_{timestamp.split('T')[0]}.txt",
            self._format_reverse_analysis(scene_text, result)
        )

        # Salvar na memória para futuras consultas
        self.memory.store(
            MemoryType.ANALYSIS,
            f"reverse:{scene_hash}",
            result,
            metadata={'scene_length': len(scene_text), 'timestamp': timestamp},
            confidence=result['confidence_avg'],
            source='why_this_works'
        )

        return result

    def _analyze_with_ai(self, scene_text: str) -> List[Dict]:
        """Análise complementar com IA quando memória não tem dados suficientes"""

        try:
            import ollama

            prompt = f"""Analyze this screenplay scene and explain which screenwriting theories make it effective:

SCENE:
{scene_text[:1000]}

Identify 3 specific theories (Save the Cat, Hero's Journey, etc.) that apply.
Output JSON: {{"theories": [{{"name": "...", "explanation": "...", "why_effective": "..."}}]}}"""

            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={**self.config, 'num_ctx': 8192},  # Contexto menor para análise rápida
                stream=False
            )

            result = response.get('response', '{}')
            if '{' in result and '}' in result:
                start = result.find('{')
                end = result.rfind('}') + 1
                data = json.loads(result[start:end])

                return [
                    {
                        'concept': t.get('name', 'Unknown'),
                        'theory': t.get('explanation', ''),
                        'example': t.get('why_effective', ''),
                        'confidence': 0.7,  # Menor confiança pois é inferência
                        'source': 'ai_inference'
                    }
                    for t in data.get('theories', [])
                ]
        except:
            pass

        return []

    # ==================== FUNÇÃO 2: VALIDAÇÃO CRUZADA ====================

    def validate_pattern(self, pattern_name: str, min_occurrences: int = 3) -> Dict[str, Any]:
        """
        Valida se um padrão narrativo é universal verificando múltiplos roteiros.

        Args:
            pattern_name: Nome do padrão (ex: "Save the Cat moment")
            min_occurrences: Mínimo de ocorrências para considerar válido

        Returns:
            Dict com análise estatística e exemplos
        """

        timestamp = datetime.now().isoformat()
        pattern_hash = hashlib.md5(pattern_name.encode()).hexdigest()[:8]

        # Buscar o padrão em todos os roteiros disponíveis
        all_screenplays = self.library.list_screenplays()
        occurrences = []

        print(f"\n🔍 Validando padrão: {pattern_name}")
        print(f"   Analisando {len(all_screenplays)} roteiros...")

        for screenplay_title in all_screenplays[:20]:  # Limitar para não demorar muito
            content = self.library.get_screenplay(screenplay_title)
            if not content or content == '.':  # Evitar erro IsADirectoryError
                continue
            if not content:
                continue

            # Buscar padrão no roteiro
            found = self._find_pattern_in_screenplay(pattern_name, screenplay_title, content)
            if found:
                occurrences.append(found)

        # Calcular estatísticas
        validation_result = {
            'pattern': pattern_name,
            'pattern_hash': pattern_hash,
            'timestamp': timestamp,
            'screenplays_analyzed': len(all_screenplays[:20]),
            'occurrences_found': len(occurrences),
            'occurrence_rate': len(occurrences) / min(20, len(all_screenplays)),
            'is_universal': len(occurrences) >= min_occurrences,
            'confidence': min(1.0, len(occurrences) / min_occurrences),
            'examples': occurrences[:5],  # Top 5 exemplos
            'statistics': {
                'min_page': min((o['page'] for o in occurrences), default=0),
                'max_page': max((o['page'] for o in occurrences), default=0),
                'avg_page': sum(o['page'] for o in occurrences) / len(occurrences) if occurrences else 0
            }
        }

        # Gerar análise profunda
        deep_analysis = self._generate_pattern_analysis(pattern_name, occurrences, validation_result)
        validation_result['deep_analysis'] = deep_analysis

        # Salvar documentação robusta
        self._save_robust_documentation(
            f"pattern_validation_{pattern_hash}_{timestamp.split('T')[0]}.txt",
            self._format_pattern_validation(validation_result)
        )

        # Salvar na memória
        self.memory.store(
            MemoryType.PATTERN,
            f"validation:{pattern_hash}",
            validation_result,
            metadata={'pattern': pattern_name, 'timestamp': timestamp},
            confidence=validation_result['confidence'],
            source='pattern_validation'
        )

        return validation_result

    def _find_pattern_in_screenplay(self, pattern: str, title: str, content: str) -> Optional[Dict]:
        """Busca um padrão específico em um roteiro"""

        # Mapear padrões conhecidos para busca
        pattern_markers = {
            "Save the Cat moment": ["saves", "helps", "rescues", "kind gesture", "sympathetic"],
            "Dark Night of the Soul": ["all is lost", "lowest point", "despair", "gives up"],
            "Fun and Games": ["montage", "trying", "learning", "exploring"],
            "Catalyst": ["inciting incident", "call to adventure", "disruption"],
            "Midpoint": ["false victory", "false defeat", "twist", "revelation"]
        }

        markers = pattern_markers.get(pattern, [pattern.lower()])
        content_lower = content.lower()

        # Buscar marcadores
        for marker in markers:
            if marker in content_lower:
                # Encontrar posição aproximada (página)
                position = content_lower.index(marker)
                page = int(position / 3000) + 1  # ~3000 chars por página

                # Extrair contexto
                start = max(0, position - 200)
                end = min(len(content), position + 500)
                context = content[start:end]

                return {
                    'screenplay': title,
                    'page': page,
                    'marker': marker,
                    'context': context,
                    'confidence': 0.8
                }

        return None

    def _generate_pattern_analysis(self, pattern: str, occurrences: List, stats: Dict) -> str:
        """Gera análise profunda sobre o padrão"""

        if stats['is_universal']:
            return f"""
PADRÃO VALIDADO COMO UNIVERSAL

O padrão '{pattern}' foi encontrado em {stats['occurrences_found']} de {stats['screenplays_analyzed']} roteiros analisados,
representando uma taxa de ocorrência de {stats['occurrence_rate']:.1%}.

DISTRIBUIÇÃO TEMPORAL:
- Aparece em média na página {stats['statistics']['avg_page']:.0f}
- Earliest: página {stats['statistics']['min_page']}
- Latest: página {stats['statistics']['max_page']}

CONCLUSÃO:
Este padrão demonstra ser um elemento estrutural consistente na narrativa cinematográfica,
validando sua aplicação como técnica confiável para roteiristas.
"""
        else:
            return f"""
PADRÃO NÃO VALIDADO COMO UNIVERSAL

O padrão '{pattern}' foi encontrado em apenas {stats['occurrences_found']} de {stats['screenplays_analyzed']} roteiros,
uma taxa de {stats['occurrence_rate']:.1%} que não atinge o mínimo necessário.

INTERPRETAÇÃO:
Este padrão pode ser:
1. Específico de gênero (não universal)
2. Técnica opcional (não obrigatória)
3. Conceito mal definido ou interpretado
4. Tendência moderna ainda não consolidada

RECOMENDAÇÃO:
Use com cautela e considere o contexto específico do seu projeto.
"""

    # ==================== FUNÇÃO 3: CACHE INTELIGENTE ====================

    def get_or_analyze(self, book_name: str, screenplay_title: str, force: bool = False) -> Dict[str, Any]:
        """
        Verifica cache antes de reprocessar análise pesada.

        Args:
            book_name: Nome do livro de teoria
            screenplay_title: Nome do roteiro
            force: Forçar nova análise ignorando cache

        Returns:
            Análise (do cache ou nova)
        """

        # Gerar chave única para a combinação
        cache_key = f"cache:{hashlib.md5(f'{book_name}:{screenplay_title}'.encode()).hexdigest()}"

        # Verificar cache se não forçar
        if not force:
            cached = self.memory.retrieve(
                memory_type=MemoryType.CACHE,
                key=cache_key
            )

            if cached and cached.value:
                print(f"✨ Usando cache para {book_name[:30]}... + {screenplay_title}")

                # Atualizar timestamp de acesso
                self.memory.store(
                    MemoryType.CACHE,
                    cache_key,
                    cached.value,
                    metadata={
                        **cached.metadata,
                        'last_accessed': datetime.now().isoformat(),
                        'access_count': cached.metadata.get('access_count', 0) + 1
                    },
                    confidence=cached.confidence,
                    source='cache_hit'
                )

                return cached.value

        # Análise nova necessária
        print(f"🧠 Processando {book_name[:30]}... + {screenplay_title}")
        start_time = time.time()

        # Executar análise profunda
        teoria_path = Path("digilibrary/BIBLIOTECA_ROTEIROS/teoria") / book_name

        if not teoria_path.exists():
            return {'error': f'Book not found: {book_name}'}

        # Ler conteúdos
        book_content = teoria_path.read_text(encoding='utf-8', errors='ignore')[:320000]
        screenplay_content = self.library.get_screenplay(screenplay_title)

        if not screenplay_content:
            return {'error': f'Screenplay not found: {screenplay_title}'}

        screenplay_content = screenplay_content[:120000]

        # Prompt avançado para análise profunda
        prompt = f"""You are analyzing a screenwriting theory book alongside a produced screenplay.

THEORY BOOK ({book_name}):
{book_content[:80000]}

SCREENPLAY ({screenplay_title}):
{screenplay_content[:40000]}

DEEP ANALYSIS REQUIRED:

1. CONCEPT EXTRACTION (minimum 15 concepts):
   - Identify key theories from the book
   - Find specific examples in the screenplay
   - Note page/minute references when possible

2. PATTERN RECOGNITION:
   - Recurring structures
   - Character arc patterns
   - Theme development patterns

3. CONTRADICTIONS & INNOVATIONS:
   - Where the screenplay breaks the book's rules successfully
   - Innovative techniques not covered in theory

4. PRACTICAL APPLICATION:
   - Step-by-step how to apply each concept
   - Common pitfalls to avoid
   - Industry-specific adaptations

Output as comprehensive JSON:
{{
    "book": "{book_name}",
    "screenplay": "{screenplay_title}",
    "analysis_depth": "comprehensive",
    "concepts": [
        {{
            "name": "concept name",
            "theory": "detailed explanation from book",
            "page_ref": "page number if found",
            "screenplay_example": "specific scene or dialogue",
            "timing": "minute or page in screenplay",
            "how_to_apply": "practical steps",
            "common_mistakes": "what to avoid",
            "effectiveness": "why it works"
        }}
    ],
    "patterns": [
        {{
            "pattern_name": "...",
            "description": "...",
            "occurrences": ["example1", "example2"]
        }}
    ],
    "contradictions": [
        {{
            "rule_broken": "...",
            "how_broken": "...",
            "why_it_works": "..."
        }}
    ],
    "synthesis": "Overall insights combining theory and practice",
    "actionable_framework": "Step-by-step framework for writers"
}}"""

        try:
            import ollama

            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options=self.config,
                stream=False
            )

            result_text = response.get('response', '{}')

            # Parse JSON
            if '{' in result_text and '}' in result_text:
                start = result_text.find('{')
                end = result_text.rfind('}') + 1
                analysis = json.loads(result_text[start:end])
            else:
                analysis = {'raw': result_text, 'concepts': []}

            # Enriquecer com metadados
            analysis['metadata'] = {
                'processing_time': time.time() - start_time,
                'timestamp': datetime.now().isoformat(),
                'book_size': len(book_content),
                'screenplay_size': len(screenplay_content),
                'model_used': self.model
            }

            # Salvar cada conceito na memória
            for concept in analysis.get('concepts', []):
                concept_key = f"concept:{book_name}:{concept.get('name', 'unknown')}"
                self.memory.store(
                    MemoryType.KNOWLEDGE,
                    concept_key[:100],
                    concept,
                    metadata={
                        'book': book_name,
                        'screenplay': screenplay_title,
                        'extraction_date': datetime.now().isoformat()
                    },
                    confidence=0.9,
                    source='deep_analysis'
                )

            # Salvar no cache
            self.memory.store(
                MemoryType.CACHE,
                cache_key,
                analysis,
                metadata={
                    'book': book_name,
                    'screenplay': screenplay_title,
                    'created': datetime.now().isoformat(),
                    'last_accessed': datetime.now().isoformat(),
                    'access_count': 1,
                    'processing_time': analysis['metadata']['processing_time']
                },
                confidence=0.95,
                source='deep_analysis_cache'
            )

            # Salvar documentação robusta
            self._save_robust_documentation(
                f"analysis_{book_name[:30]}_{screenplay_title}_{datetime.now().strftime('%Y%m%d')}.txt",
                self._format_deep_analysis(analysis)
            )

            print(f"✅ Análise completa em {analysis['metadata']['processing_time']:.1f}s")
            print(f"   {len(analysis.get('concepts', []))} conceitos extraídos")
            print(f"   {len(analysis.get('patterns', []))} padrões identificados")

            return analysis

        except Exception as e:
            error_result = {
                'error': str(e),
                'book': book_name,
                'screenplay': screenplay_title,
                'timestamp': datetime.now().isoformat()
            }

            # Salvar erro no cache para não tentar novamente
            self.memory.store(
                MemoryType.CACHE,
                cache_key,
                error_result,
                metadata={'error': True},
                confidence=0.1,
                source='error_cache'
            )

            return error_result

    # ==================== DOCUMENTAÇÃO ROBUSTA ====================

    def _save_robust_documentation(self, filename: str, content: str):
        """Salva documentação detalhada em TXT"""

        filepath = self.docs_dir / filename
        filepath.write_text(content, encoding='utf-8')

        # Também salvar referência na memória
        self.memory.store(
            MemoryType.KNOWLEDGE,  # Corrigido: não existe DOCUMENTATION
            f"doc:{filename}",
            {'path': str(filepath), 'size': len(content)},
            metadata={'created': datetime.now().isoformat()},
            confidence=1.0,
            source='documentation'
        )

    def _format_reverse_analysis(self, scene: str, result: Dict) -> str:
        """Formata análise reversa para documentação"""

        return f"""
================================================================================
ANÁLISE REVERSA DE CENA - WHY THIS WORKS
================================================================================

Data: {result['timestamp']}
Hash: {result['scene_hash']}

CENA ANALISADA:
--------------------------------------------------------------------------------
{scene}
--------------------------------------------------------------------------------

TEORIAS CINEMATOGRÁFICAS APLICADAS:
================================================================================

{self._format_explanations(result['explanations'])}

SÍNTESE:
--------------------------------------------------------------------------------
Esta cena demonstra a aplicação de {result['theories_applied']} teorias distintas
com confiança média de {result['confidence_avg']:.1%}.

INSIGHTS ACIONÁVEIS:
--------------------------------------------------------------------------------
1. Observe como múltiplas teorias podem coexistir na mesma cena
2. A efetividade não depende de seguir uma única escola teórica
3. Contexto e execução são tão importantes quanto a teoria

================================================================================
FIM DA ANÁLISE
================================================================================
"""

    def _format_explanations(self, explanations: List[Dict]) -> str:
        """Formata lista de explicações"""

        output = []
        for i, exp in enumerate(explanations, 1):
            output.append(f"""
{i}. CONCEITO: {exp['concept']}
   Confiança: {exp['confidence']:.1%}
   Fonte: {exp['source']}

   TEORIA:
   {exp['theory'][:500]}...

   EXEMPLO SIMILAR:
   {exp['example'][:300]}...

   ----------------------------------------
""")
        return '\n'.join(output)

    def _format_pattern_validation(self, result: Dict) -> str:
        """Formata validação de padrão para documentação"""

        examples_text = '\n\n'.join([
            f"   {i}. {ex['screenplay']} (página {ex['page']})\n      Contexto: {ex['context'][:200]}..."
            for i, ex in enumerate(result['examples'], 1)
        ])

        return f"""
================================================================================
VALIDAÇÃO DE PADRÃO NARRATIVO
================================================================================

Padrão: {result['pattern']}
Data: {result['timestamp']}
Hash: {result['pattern_hash']}

ESTATÍSTICAS:
--------------------------------------------------------------------------------
Roteiros analisados: {result['screenplays_analyzed']}
Ocorrências encontradas: {result['occurrences_found']}
Taxa de ocorrência: {result['occurrence_rate']:.1%}
Status: {'✅ UNIVERSAL' if result['is_universal'] else '❌ NÃO UNIVERSAL'}
Confiança: {result['confidence']:.1%}

DISTRIBUIÇÃO TEMPORAL:
--------------------------------------------------------------------------------
Página mínima: {result['statistics']['min_page']}
Página máxima: {result['statistics']['max_page']}
Página média: {result['statistics']['avg_page']:.1f}

EXEMPLOS ENCONTRADOS:
--------------------------------------------------------------------------------
{examples_text}

ANÁLISE PROFUNDA:
================================================================================
{result['deep_analysis']}

================================================================================
FIM DA VALIDAÇÃO
================================================================================
"""

    def _format_deep_analysis(self, analysis: Dict) -> str:
        """Formata análise profunda para documentação"""

        concepts_text = '\n'.join([
            f"""
CONCEITO {i}: {c.get('name', 'Unknown')}
--------------------------------------------------------------------------------
Teoria: {c.get('theory', 'N/A')}
Página no livro: {c.get('page_ref', 'N/A')}

Exemplo no roteiro: {c.get('screenplay_example', 'N/A')}
Timing: {c.get('timing', 'N/A')}

Como aplicar:
{c.get('how_to_apply', 'N/A')}

Erros comuns:
{c.get('common_mistakes', 'N/A')}

Por que funciona:
{c.get('effectiveness', 'N/A')}

================================================================================
"""
            for i, c in enumerate(analysis.get('concepts', []), 1)
        ])

        patterns_text = '\n'.join([
            f"""
PADRÃO: {p.get('pattern_name', 'Unknown')}
Descrição: {p.get('description', 'N/A')}
Ocorrências: {', '.join(p.get('occurrences', [])[:3])}
"""
            for p in analysis.get('patterns', [])
        ])

        contradictions_text = '\n'.join([
            f"""
CONTRADIÇÃO: {c.get('rule_broken', 'Unknown')}
Como quebrada: {c.get('how_broken', 'N/A')}
Por que funciona: {c.get('why_it_works', 'N/A')}
"""
            for c in analysis.get('contradictions', [])
        ])

        return f"""
================================================================================
ANÁLISE PROFUNDA: TEORIA + PRÁTICA
================================================================================

Livro: {analysis.get('book', 'Unknown')}
Roteiro: {analysis.get('screenplay', 'Unknown')}
Data: {analysis.get('metadata', {}).get('timestamp', 'N/A')}
Tempo de processamento: {analysis.get('metadata', {}).get('processing_time', 0):.1f} segundos

================================================================================
CONCEITOS EXTRAÍDOS ({len(analysis.get('concepts', []))})
================================================================================
{concepts_text}

================================================================================
PADRÕES IDENTIFICADOS ({len(analysis.get('patterns', []))})
================================================================================
{patterns_text}

================================================================================
CONTRADIÇÕES PRODUTIVAS ({len(analysis.get('contradictions', []))})
================================================================================
{contradictions_text}

================================================================================
SÍNTESE GERAL
================================================================================
{analysis.get('synthesis', 'N/A')}

================================================================================
FRAMEWORK ACIONÁVEL
================================================================================
{analysis.get('actionable_framework', 'N/A')}

================================================================================
METADADOS
================================================================================
Modelo usado: {analysis.get('metadata', {}).get('model_used', 'N/A')}
Tamanho do livro: {analysis.get('metadata', {}).get('book_size', 0)} caracteres
Tamanho do roteiro: {analysis.get('metadata', {}).get('screenplay_size', 0)} caracteres

================================================================================
FIM DA ANÁLISE
================================================================================
"""

    # ==================== INTERFACE PRINCIPAL ====================

    def run_comprehensive_analysis(self):
        """Executa análise completa com todas as funcionalidades"""

        print("""
╔══════════════════════════════════════════════════════════════╗
║     🧠 DEEP LEARNING ENHANCED - Sistema Inteligente         ║
╚══════════════════════════════════════════════════════════════╝
        """)

        print("""
FUNCIONALIDADES DISPONÍVEIS:

1. 🔍 BUSCA REVERSA - Explica por que uma cena funciona
2. ✅ VALIDAÇÃO DE PADRÕES - Verifica se regra é universal
3. ⚡ ANÁLISE COM CACHE - Processa livro + roteiro (ou usa cache)
4. 📊 ANÁLISE COMPLETA - Executa todas as funcionalidades
5. 📚 VER DOCUMENTAÇÃO - Lista análises salvas

Escolha (1-5): """, end='')

        choice = input().strip()

        if choice == '1':
            self._run_reverse_search()
        elif choice == '2':
            self._run_pattern_validation()
        elif choice == '3':
            self._run_cached_analysis()
        elif choice == '4':
            self._run_complete_analysis()
        elif choice == '5':
            self._show_documentation()
        else:
            print("❌ Opção inválida")

    def _run_reverse_search(self):
        """Interface para busca reversa"""

        print("\n🔍 BUSCA REVERSA - Por que esta cena funciona?")
        print("-" * 60)

        print("\nCole o trecho de roteiro para analisar (termine com linha vazia):")

        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)

        scene = '\n'.join(lines)

        if not scene:
            print("❌ Nenhuma cena fornecida")
            return

        print("\nAnalisando...")
        result = self.why_this_works(scene)

        print(f"\n✅ ANÁLISE COMPLETA")
        print(f"Hash da cena: {result['scene_hash']}")
        print(f"Teorias aplicadas: {result['theories_applied']}")
        print(f"Confiança média: {result['confidence_avg']:.1%}")

        print("\nEXPLICAÇÕES:")
        for i, exp in enumerate(result['explanations'], 1):
            print(f"\n{i}. {exp['concept']}")
            print(f"   Teoria: {exp['theory'][:200]}...")
            print(f"   Confiança: {exp['confidence']:.1%}")

        print(f"\n📄 Documentação salva em: data/deep_learning_docs/")

    def _run_pattern_validation(self):
        """Interface para validação de padrões"""

        print("\n✅ VALIDAÇÃO DE PADRÕES")
        print("-" * 60)

        patterns = [
            "Save the Cat moment",
            "Dark Night of the Soul",
            "Fun and Games",
            "Catalyst",
            "Midpoint",
            "Custom (digite)"
        ]

        print("\nPadrões disponíveis:")
        for i, p in enumerate(patterns, 1):
            print(f"{i}. {p}")

        choice = input("\nEscolha (1-6): ").strip()

        if choice == '6':
            pattern = input("Digite o padrão: ")
        elif choice.isdigit() and 1 <= int(choice) <= 5:
            pattern = patterns[int(choice) - 1]
        else:
            print("❌ Escolha inválida")
            return

        min_occ = input("Mínimo de ocorrências para validar (padrão 3): ").strip()
        min_occ = int(min_occ) if min_occ.isdigit() else 3

        print(f"\nValidando padrão: {pattern}")
        result = self.validate_pattern(pattern, min_occ)

        print(f"\n{'✅' if result['is_universal'] else '❌'} RESULTADO DA VALIDAÇÃO")
        print(f"Roteiros analisados: {result['screenplays_analyzed']}")
        print(f"Ocorrências: {result['occurrences_found']}")
        print(f"Taxa: {result['occurrence_rate']:.1%}")
        print(f"Confiança: {result['confidence']:.1%}")

        if result['examples']:
            print("\nEXEMPLOS:")
            for ex in result['examples'][:3]:
                print(f"- {ex['screenplay']} (p. {ex['page']})")

        print(f"\n📄 Documentação completa salva em: data/deep_learning_docs/")

    def _run_cached_analysis(self):
        """Interface para análise com cache"""

        print("\n⚡ ANÁLISE COM CACHE INTELIGENTE")
        print("-" * 60)

        # Listar livros disponíveis
        teoria_path = Path("digilibrary/BIBLIOTECA_ROTEIROS/teoria")
        books = list(teoria_path.glob("*.txt"))[:10]

        print("\n📚 Livros disponíveis:")
        for i, book in enumerate(books, 1):
            print(f"{i}. {book.name[:50]}...")

        book_idx = input("\nEscolha o livro (1-10): ").strip()

        if not book_idx.isdigit() or not (1 <= int(book_idx) <= len(books)):
            print("❌ Escolha inválida")
            return

        book = books[int(book_idx) - 1].name

        # Listar roteiros
        screenplays = self.library.list_screenplays()[:10]

        print("\n🎬 Roteiros disponíveis:")
        for i, s in enumerate(screenplays, 1):
            print(f"{i}. {s}")

        screenplay_idx = input("\nEscolha o roteiro (1-10): ").strip()

        if not screenplay_idx.isdigit() or not (1 <= int(screenplay_idx) <= len(screenplays)):
            print("❌ Escolha inválida")
            return

        screenplay = screenplays[int(screenplay_idx) - 1]

        force = input("\nForçar nova análise? (s/N): ").strip().lower() == 's'

        print(f"\nProcessando {book[:30]}... + {screenplay}...")
        result = self.get_or_analyze(book, screenplay, force)

        if 'error' in result:
            print(f"❌ Erro: {result['error']}")
            return

        print(f"\n✅ ANÁLISE COMPLETA")
        print(f"Conceitos: {len(result.get('concepts', []))}")
        print(f"Padrões: {len(result.get('patterns', []))}")
        print(f"Contradições: {len(result.get('contradictions', []))}")

        if result.get('metadata'):
            print(f"Tempo: {result['metadata'].get('processing_time', 0):.1f}s")

        print(f"\n📄 Documentação salva em: data/deep_learning_docs/")

    def _run_complete_analysis(self):
        """Executa demonstração completa do sistema"""

        print("\n📊 EXECUTANDO ANÁLISE COMPLETA DE DEMONSTRAÇÃO")
        print("=" * 60)

        # 1. Demonstrar cache
        print("\n1️⃣ TESTANDO CACHE INTELIGENTE")
        print("-" * 40)

        book = "Save The Cat.txt"
        screenplay = "Inception"

        print(f"Primeira análise: {book[:30]}... + {screenplay}")
        start = time.time()
        result1 = self.get_or_analyze(book, screenplay)
        time1 = time.time() - start

        print(f"Tempo: {time1:.1f}s")
        print(f"Conceitos: {len(result1.get('concepts', []))}")

        print(f"\nSegunda análise (cache):")
        start = time.time()
        result2 = self.get_or_analyze(book, screenplay)
        time2 = time.time() - start

        print(f"Tempo: {time2:.1f}s")
        print(f"Speedup: {time1/time2:.0f}x mais rápido!")

        # 2. Demonstrar busca reversa
        print("\n2️⃣ TESTANDO BUSCA REVERSA")
        print("-" * 40)

        sample_scene = """
        INT. AIRPLANE - FIRST CLASS CABIN - NIGHT

        Cobb studies Saito. The Japanese man's eyes are closed.

        COBB
        He's not gonna make it. We should pull out.

        Arthur shakes his head.

        ARTHUR
        We were hired to do a job. We finish the job.
        """

        print("Analisando cena de Inception...")
        reverse_result = self.why_this_works(sample_scene, limit=3)

        print(f"Teorias encontradas: {reverse_result['theories_applied']}")
        for exp in reverse_result['explanations'][:2]:
            print(f"- {exp['concept']}: {exp['theory'][:100]}...")

        # 3. Demonstrar validação de padrões
        print("\n3️⃣ TESTANDO VALIDAÇÃO DE PADRÕES")
        print("-" * 40)

        print("Validando 'Save the Cat moment'...")
        pattern_result = self.validate_pattern("Save the Cat moment", min_occurrences=3)

        print(f"Status: {'✅ Universal' if pattern_result['is_universal'] else '❌ Não universal'}")
        print(f"Encontrado em {pattern_result['occurrences_found']}/{pattern_result['screenplays_analyzed']} roteiros")

        print("\n" + "=" * 60)
        print("📊 ANÁLISE COMPLETA FINALIZADA!")
        print(f"Total de documentos gerados: {len(list(self.docs_dir.glob('*.txt')))}")

        # Mostrar estatísticas da memória
        stats = self.memory.get_stats()
        print(f"\n💾 MEMÓRIA ENRIQUECIDA:")
        print(f"Total: {stats['total_entries']} entradas")
        print(f"Knowledge: {stats['by_type'].get('knowledge', 0)}")
        print(f"Cache: {stats['by_type'].get('cache', 0)}")
        print(f"Analysis: {stats['by_type'].get('analysis', 0)}")
        print(f"Pattern: {stats['by_type'].get('pattern', 0)}")

    def _show_documentation(self):
        """Mostra documentação salva"""

        print("\n📚 DOCUMENTAÇÃO DISPONÍVEL")
        print("-" * 60)

        docs = sorted(self.docs_dir.glob("*.txt"), key=lambda x: x.stat().st_mtime, reverse=True)

        if not docs:
            print("Nenhuma documentação encontrada ainda.")
            return

        for i, doc in enumerate(docs[:20], 1):
            size = doc.stat().st_size / 1024
            print(f"{i:2d}. {doc.name[:60]:60s} ({size:.1f} KB)")

        if len(docs) > 20:
            print(f"\n... e mais {len(docs) - 20} documentos")

        print(f"\n📂 Localização: {self.docs_dir}")
        print(f"💾 Tamanho total: {sum(d.stat().st_size for d in docs) / 1024:.1f} KB")


def main():
    """Ponto de entrada principal"""

    system = DeepLearningEnhanced()
    system.run_comprehensive_analysis()


if __name__ == "__main__":
    main()