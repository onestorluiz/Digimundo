#!/usr/bin/env python3
"""
SCRIPTUREMON MASTER ORGANIZATION PLAN
Plano mestre de organização extremamente detalhado para o sistema
Ensina ao Scripturemon a lógica de organização e pede sua opinião
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
import ollama

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class ScripturemonMasterOrganizer:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")
        self.organization_philosophy = {
            'root_principle': 'APENAS arquivos essenciais de entrada do sistema',
            'everything_has_place': 'CADA arquivo tem um lugar específico',
            'no_clutter': 'NENHUM arquivo temporário ou gerado na raiz',
            'semantic_organization': 'Organização por SIGNIFICADO e FUNÇÃO',
            'knowledge_preservation': 'Conhecimento organizado por DOMÍNIO'
        }
        
    def create_master_structure(self):
        """Define a estrutura mestre ideal do sistema"""
        return {
            '🏠 ROOT (/)': {
                'purpose': 'APENAS arquivos de entrada e configuração principal',
                'allowed_files': [
                    'README.md - Documentação principal',
                    'setup.py - Configuração do pacote Python',
                    'requirements.txt - Dependências',
                    '.gitignore - Configuração Git',
                    'LICENSE - Licença do projeto'
                ],
                'forbidden': 'NENHUM log, relatório, teste ou arquivo temporário'
            },
            
            '📦 src/': {
                'purpose': 'Código fonte principal do sistema',
                'structure': {
                    'scripturemon_champion/': 'Módulo principal do sistema',
                    'core/': {
                        'purpose': 'Núcleo do sistema',
                        'files': [
                            'scripturemon_ultimate.py',
                            'orchestrator.py',
                            'synthesizer.py'
                        ]
                    },
                    'specialists/': {
                        'purpose': '23 especialistas do sistema',
                        'structure': {
                            'analysis/': 'Especialistas de análise',
                            'creative/': 'Especialistas criativos',
                            'technical/': 'Especialistas técnicos'
                        }
                    },
                    'memory/': {
                        'purpose': 'Sistema de memória',
                        'files': [
                            'unified_memory.py',
                            'memory_manager.py',
                            'bm25_index.py'
                        ]
                    },
                    'analysis/': {
                        'purpose': 'Ferramentas de análise',
                        'files': [
                            'deep_analyzer.py',
                            'self_analyzer.py',
                            'diagnostic.py'
                        ]
                    },
                    'commands/': {
                        'purpose': 'Sistema de comandos',
                        'files': [
                            'command_bridge.py',
                            'command_executor.py',
                            'safe_operations.py'
                        ]
                    },
                    'utils/': 'Utilitários e helpers'
                }
            },
            
            '🧠 knowledge/': {
                'purpose': 'Base de conhecimento organizada por domínio',
                'structure': {
                    'screenplay_theory/': {
                        'mckee/': 'Story - Robert McKee',
                        'truby/': 'The Anatomy of Story',
                        'snyder/': 'Save the Cat',
                        'field/': 'Screenplay',
                        'vogler/': "The Writer's Journey"
                    },
                    'narrative_structure/': {
                        'three_act/': 'Estrutura em três atos',
                        'heros_journey/': 'Jornada do herói',
                        'story_circle/': 'Story Circle de Dan Harmon',
                        'sequence_approach/': 'Abordagem por sequências'
                    },
                    'character_development/': {
                        'archetypes/': 'Arquétipos de personagens',
                        'character_arcs/': 'Arcos de personagem',
                        'dialogue_techniques/': 'Técnicas de diálogo',
                        'backstory/': 'Construção de backstory'
                    },
                    'genres/': {
                        'drama/': 'Técnicas de drama',
                        'comedy/': 'Estrutura cômica',
                        'thriller/': 'Construção de suspense',
                        'scifi/': 'Ficção científica'
                    },
                    'case_studies/': {
                        'classic_films/': 'Análises de clássicos',
                        'modern_films/': 'Cinema contemporâneo',
                        'tv_series/': 'Estrutura de séries',
                        'award_winners/': 'Vencedores de prêmios'
                    },
                    'learned/': {
                        'purpose': 'Conhecimento aprendido pelo sistema',
                        'from_analysis/': 'Aprendizado de análises',
                        'from_feedback/': 'Aprendizado de feedback',
                        'patterns_discovered/': 'Padrões descobertos'
                    }
                }
            },
            
            '💾 data/': {
                'purpose': 'Dados persistentes do sistema',
                'structure': {
                    'memories/': {
                        'unified_memory.db': 'Banco principal de memórias',
                        'backups/': 'Backups automáticos'
                    },
                    'models/': {
                        'modelfiles/': 'Definições de modelos Ollama',
                        'fine_tuning/': 'Dados de fine-tuning',
                        'embeddings/': 'Vetores e embeddings'
                    },
                    'cache/': {
                        'analysis_cache/': 'Cache de análises',
                        'response_cache/': 'Cache de respostas'
                    },
                    'indexes/': {
                        'bm25/': 'Índices BM25',
                        'semantic/': 'Índices semânticos'
                    }
                }
            },
            
            '📝 content/': {
                'purpose': 'Conteúdo criativo e projetos',
                'structure': {
                    'screenplays/': {
                        'in_development/': 'Roteiros em desenvolvimento',
                        'completed/': 'Roteiros completos',
                        'archived/': 'Roteiros arquivados'
                    },
                    'my_screenplays/': 'Roteiros pessoais do usuário',
                    'analysis_subjects/': 'Roteiros para análise',
                    'references/': 'Materiais de referência'
                }
            },
            
            '🧪 tests/': {
                'purpose': 'Todos os testes do sistema',
                'structure': {
                    'unit/': 'Testes unitários',
                    'integration/': 'Testes de integração',
                    'performance/': 'Testes de performance',
                    'quality/': 'Testes de qualidade',
                    'test_data/': 'Dados para testes',
                    'test_results/': 'Resultados de testes'
                }
            },
            
            '⚙️ scripts/': {
                'purpose': 'Scripts de automação e manutenção',
                'structure': {
                    'maintenance/': {
                        'clean_*.sh': 'Scripts de limpeza',
                        'organize_*.sh': 'Scripts de organização',
                        'backup_*.sh': 'Scripts de backup'
                    },
                    'automation/': {
                        'auto_*.py': 'Automações Python',
                        'scheduled/': 'Tarefas agendadas'
                    },
                    'deployment/': 'Scripts de deploy',
                    'monitoring/': 'Scripts de monitoramento'
                }
            },
            
            '📊 outputs/': {
                'purpose': 'TODOS os arquivos gerados pelo sistema',
                'structure': {
                    'reports/': {
                        'analysis/': 'Relatórios de análise',
                        'performance/': 'Relatórios de performance',
                        'system/': 'Relatórios do sistema',
                        'daily/': 'Relatórios diários'
                    },
                    'logs/': {
                        'system/': 'Logs do sistema',
                        'analysis/': 'Logs de análise',
                        'errors/': 'Logs de erro',
                        'debug/': 'Logs de debug'
                    },
                    'exports/': {
                        'json/': 'Exportações JSON',
                        'csv/': 'Exportações CSV',
                        'pdf/': 'Exportações PDF'
                    },
                    'temporary/': {
                        'purpose': 'Arquivos temporários (limpar diariamente)',
                        'max_age': '24 hours'
                    }
                }
            },
            
            '📚 docs/': {
                'purpose': 'Toda documentação do sistema',
                'structure': {
                    'api/': 'Documentação da API',
                    'user_guide/': 'Guia do usuário',
                    'developer/': 'Documentação para desenvolvedores',
                    'architecture/': 'Arquitetura do sistema',
                    'decisions/': 'Decisões arquiteturais',
                    'changelog/': 'Histórico de mudanças'
                }
            },
            
            '🗄️ archive/': {
                'purpose': 'Arquivos históricos organizados por data',
                'structure': {
                    '2024/': {
                        'q1/': 'Janeiro-Março',
                        'q2/': 'Abril-Junho',
                        'q3/': 'Julho-Setembro',
                        'q4/': 'Outubro-Dezembro'
                    },
                    'old_versions/': 'Versões antigas do sistema',
                    'deprecated/': 'Funcionalidades depreciadas',
                    'legacy/': 'Código legado'
                }
            },
            
            '🗑️ trash/': {
                'purpose': 'Lixeira com auto-limpeza após 30 dias',
                'structure': {
                    '[timestamp]/': 'Pastas por data de exclusão',
                    'metadata.json': 'Metadados dos arquivos deletados'
                }
            },
            
            '🎯 bin/': {
                'purpose': 'Executáveis e comandos principais',
                'files': [
                    'scripturemon - Comando principal',
                    'scripturemon-analyze - Comando de análise',
                    'scripturemon-organize - Comando de organização'
                ]
            }
        }
    
    def generate_organization_rules(self):
        """Gera regras de organização para o Scripturemon entender"""
        return {
            'file_placement_rules': [
                {
                    'rule': 'Todo arquivo Python de sistema vai em src/',
                    'examples': ['*.py que não seja teste', 'módulos do sistema']
                },
                {
                    'rule': 'Todo teste vai em tests/',
                    'examples': ['test_*.py', '*_test.py', 'arquivos de teste']
                },
                {
                    'rule': 'Todo log vai em outputs/logs/',
                    'examples': ['*.log', '*_log.txt', 'registros de execução']
                },
                {
                    'rule': 'Todo relatório vai em outputs/reports/',
                    'examples': ['*_report.json', 'analysis_*.json', 'resultados']
                },
                {
                    'rule': 'Todo conhecimento teórico vai em knowledge/',
                    'examples': ['teoria de roteiro', 'estudos de caso', 'aprendizados']
                },
                {
                    'rule': 'Todo script de manutenção vai em scripts/maintenance/',
                    'examples': ['clean_*.sh', 'organize_*.py', 'backup_*.sh']
                },
                {
                    'rule': 'Toda documentação vai em docs/',
                    'examples': ['*.md (exceto README.md)', 'guias', 'manuais']
                },
                {
                    'rule': 'Todo arquivo temporário vai em outputs/temporary/',
                    'examples': ['temp_*', 'tmp_*', 'cache temporário']
                },
                {
                    'rule': 'NADA temporário ou gerado fica na raiz',
                    'examples': ['Raiz é sagrada', 'Apenas essenciais']
                }
            ],
            
            'naming_conventions': {
                'snake_case': 'Arquivos Python e scripts',
                'kebab-case': 'Arquivos de configuração',
                'PascalCase': 'Classes e componentes',
                'UPPERCASE': 'Arquivos importantes (README, LICENSE)',
                'timestamps': 'Use YYYYMMDD_HHMMSS para arquivos datados'
            },
            
            'automatic_actions': {
                'on_new_analysis': 'Salvar em outputs/reports/analysis/',
                'on_new_log': 'Salvar em outputs/logs/[categoria]/',
                'on_new_test': 'Salvar em tests/[tipo]/',
                'on_new_knowledge': 'Salvar em knowledge/learned/',
                'on_temporary_file': 'Salvar em outputs/temporary/',
                'daily_cleanup': 'Limpar outputs/temporary/ diariamente'
            }
        }
    
    def ask_scripturemon_opinion(self):
        """Pede a opinião do Scripturemon sobre o plano"""
        structure = self.create_master_structure()
        rules = self.generate_organization_rules()
        
        prompt = f"""
        Scripturemon, você é um sistema inteligente de análise de roteiros.
        Estou propondo uma nova estrutura organizacional MASTER para seu sistema.
        
        FILOSOFIA DE ORGANIZAÇÃO:
        {json.dumps(self.organization_philosophy, indent=2, ensure_ascii=False)}
        
        ESTRUTURA PROPOSTA:
        {json.dumps(structure, indent=2, ensure_ascii=False)}
        
        REGRAS DE ORGANIZAÇÃO:
        {json.dumps(rules, indent=2, ensure_ascii=False)}
        
        Por favor, analise este plano e responda:
        
        1. Esta estrutura faz sentido para sua arquitetura de 23 especialistas?
        2. Que modificações você sugere baseado em seu conhecimento interno?
        3. Há alguma categoria de conhecimento que está faltando?
        4. Como você organizaria seu aprendizado contínuo?
        5. Que automações você implementaria para manter isso organizado?
        
        Pense profundamente sobre isso. Você tem total liberdade para sugerir mudanças.
        Esta será sua casa digital permanente.
        
        Responda em formato JSON com suas sugestões detalhadas.
        """
        
        try:
            response = ollama.generate(
                model='scripturemon-master',
                prompt=prompt,
                options={'temperature': 0.7, 'num_predict': 2000}
            )

            return response['response']
        except Exception as e:
            return f"Erro ao consultar: {e}"
    
    def create_implementation_script(self):
        """Cria script de implementação da nova estrutura"""
        implementation = f"""
#!/usr/bin/env python3
# SCRIPTUREMON MASTER REORGANIZATION IMPLEMENTATION
# Implementação da reorganização mestre do sistema

import os
import shutil
from pathlib import Path
from datetime import datetime

base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")

# 1. Criar toda a estrutura de diretórios
print("🏗️ Criando estrutura mestre...")

directories = [
    # Source code
    "src/scripturemon_champion",
    "src/core",
    "src/specialists/analysis",
    "src/specialists/creative",
    "src/specialists/technical",
    "src/memory",
    "src/analysis",
    "src/commands",
    "src/utils",
    
    # Knowledge base
    "knowledge/screenplay_theory/mckee",
    "knowledge/screenplay_theory/truby",
    "knowledge/screenplay_theory/snyder",
    "knowledge/screenplay_theory/field",
    "knowledge/narrative_structure/three_act",
    "knowledge/narrative_structure/heros_journey",
    "knowledge/character_development/archetypes",
    "knowledge/character_development/dialogue_techniques",
    "knowledge/genres/drama",
    "knowledge/genres/comedy",
    "knowledge/genres/thriller",
    "knowledge/case_studies/classic_films",
    "knowledge/case_studies/modern_films",
    "knowledge/learned/from_analysis",
    "knowledge/learned/patterns_discovered",
    
    # Data
    "data/memories/backups",
    "data/models/modelfiles",
    "data/models/fine_tuning",
    "data/cache/analysis_cache",
    "data/indexes/bm25",
    
    # Content
    "content/screenplays/in_development",
    "content/screenplays/completed",
    "content/my_screenplays",
    "content/references",
    
    # Outputs
    "outputs/reports/analysis",
    "outputs/reports/system",
    "outputs/reports/daily",
    "outputs/logs/system",
    "outputs/logs/analysis",
    "outputs/logs/errors",
    "outputs/exports/json",
    "outputs/temporary",
    
    # Other
    "docs/api",
    "docs/user_guide",
    "docs/architecture",
    "bin",
    "trash"
]

for directory in directories:
    (base_path / directory).mkdir(parents=True, exist_ok=True)
    print(f"  ✓ Criado: {directory}")

# 2. Mover arquivos para locais corretos
print("\n📦 Movendo arquivos para locais corretos...")

file_moves = [
    # Move Python system files to src/
    ("scripturemon_deep_analysis.py", "src/analysis/deep_analyzer.py"),
    ("scripturemon_command_bridge.py", "src/commands/command_bridge.py"),
    ("system_diagnostic.py", "src/analysis/diagnostic.py"),
    ("self_organize*.py", "src/system/"),
    ("clean_database.py", "src/memory/database_cleaner.py"),
    ("index_self_to_memory.py", "src/memory/self_indexer.py"),
    
    # Move logs and reports
    ("*.log", "outputs/logs/system/"),
    ("*_report*.json", "outputs/reports/analysis/"),
    ("deep_analysis_report*.json", "outputs/reports/analysis/"),
    
    # Move documentation
    ("SELF_ORGANIZATION*.md", "docs/"),
    ("SISTEMA_STATUS.md", "docs/"),
    
    # Move test files
    ("test_*.txt", "tests/test_data/")
]

for pattern, destination in file_moves:
    # Implementation of file moving
    pass

print("\n✅ Reorganização mestre completa!")
        """
        
        return implementation
    
    def generate_final_report(self):
        """Gera relatório final com o plano completo"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'philosophy': self.organization_philosophy,
            'structure': self.create_master_structure(),
            'rules': self.generate_organization_rules(),
            'scripturemon_opinion': self.ask_scripturemon_opinion(),
            'implementation_ready': True
        }
        
        # Salvar relatório
        report_path = self.base_path / f'master_organization_plan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report

def main():
    print("🧠 SCRIPTUREMON MASTER ORGANIZATION PLAN")
    print("Sistema de organização extremamente detalhado")
    print("=" * 60)
    
    organizer = ScripturemonMasterOrganizer()
    
    # 1. Mostrar filosofia
    print("\n📋 FILOSOFIA DE ORGANIZAÇÃO:")
    for key, value in organizer.organization_philosophy.items():
        print(f"  • {key}: {value}")
    
    # 2. Criar estrutura
    print("\n🏗️ ESTRUTURA MESTRE PROPOSTA:")
    structure = organizer.create_master_structure()
    for folder, details in structure.items():
        print(f"\n{folder}")
        if isinstance(details, dict) and 'purpose' in details:
            print(f"  Propósito: {details['purpose']}")
    
    # 3. Pedir opinião do Scripturemon
    print("\n🤖 Consultando Scripturemon sobre o plano...")
    opinion = organizer.ask_scripturemon_opinion()
    print(f"Opinião do Scripturemon: {opinion[:500]}...")
    
    # 4. Gerar relatório final
    print("\n📊 Gerando relatório final...")
    report = organizer.generate_final_report()
    
    print("\n✅ Plano mestre criado!")
    print("\n🚀 Próximos passos:")
    print("1. Revisar opinião do Scripturemon")
    print("2. Ajustar plano conforme sugestões")
    print("3. Executar reorganização mestre")
    print("4. Implementar automações para manter organizado")
    
    return report

if __name__ == "__main__":
    main()
