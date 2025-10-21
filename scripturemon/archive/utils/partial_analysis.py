#!/usr/bin/env python3
"""
Análise Parcial Inteligente

Permite executar análises parciais focadas:
- Quick Preview (10-15 min): 2-3 specialists essenciais
- Character Focus (30-45 min): Todos character specialists
- Structure Focus (30-45 min): Todos structure specialists
- Dialogue Focus (20-30 min): Todos dialogue specialists
- Custom: Escolha manual de specialists/authors

Uso:
    python partial_analysis.py <screenplay.pdf> --mode quick
    python partial_analysis.py <screenplay.pdf> --mode character
    python partial_analysis.py <screenplay.pdf> --mode structure
    python partial_analysis.py <screenplay.pdf> --mode dialogue
    python partial_analysis.py <screenplay.pdf> --custom --specialists character,structure --authors mckee,field
"""

import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse
import json


class PartialAnalysisManager:
    """Gerencia análises parciais inteligentes"""

    # Presets de análise
    PRESETS = {
        'quick': {
            'name': 'Quick Preview',
            'description': 'Análise rápida com specialists essenciais',
            'specialists': ['character', 'structure'],
            'authors': ['mckee', 'field'],
            'estimated_time_minutes': 12,
            'estimated_analyses': 4,
            'use_case': 'Primeiro contato com o roteiro, validação rápida'
        },
        'character': {
            'name': 'Character Focus',
            'description': 'Análise profunda de personagens',
            'specialists': ['character'],
            'authors': ['mckee', 'field', 'truby', 'egri', 'mckee_character'],
            'estimated_time_minutes': 35,
            'estimated_analyses': 5,
            'use_case': 'Desenvolvimento de personagens, arcos dramáticos'
        },
        'structure': {
            'name': 'Structure Focus',
            'description': 'Análise estrutural completa',
            'specialists': ['structure', 'pacing'],
            'authors': ['field', 'snyder', 'vogler', 'weiland'],
            'estimated_time_minutes': 40,
            'estimated_analyses': 8,
            'use_case': 'Validar estrutura de 3 atos, beats, ritmo narrativo'
        },
        'dialogue': {
            'name': 'Dialogue Focus',
            'description': 'Análise de diálogos e voz dos personagens',
            'specialists': ['dialogue', 'character'],
            'authors': ['mckee_dialogue', 'mckee_character', 'egri'],
            'estimated_time_minutes': 25,
            'estimated_analyses': 6,
            'use_case': 'Melhorar autenticidade e subtexto dos diálogos'
        },
        'theme': {
            'name': 'Theme & Genre',
            'description': 'Análise temática e de gênero',
            'specialists': ['theme', 'genre'],
            'authors': ['mckee', 'truby', 'egri'],
            'estimated_time_minutes': 30,
            'estimated_analyses': 6,
            'use_case': 'Fortalecer tema central e coerência de gênero'
        },
        'professional': {
            'name': 'Professional Review',
            'description': 'Análise profissional completa',
            'specialists': ['character', 'structure', 'theme', 'dialogue', 'pacing'],
            'authors': ['mckee', 'field', 'truby', 'campbell', 'vogler', 'snyder'],
            'estimated_time_minutes': 90,
            'estimated_analyses': 30,
            'use_case': 'Revisão completa antes de pitching ou submissão'
        }
    }

    def __init__(self):
        pass

    def list_presets(self):
        """Lista todos os presets disponíveis"""
        print("\n" + "=" * 80)
        print("🎯 MODOS DE ANÁLISE PARCIAL")
        print("=" * 80)
        print()

        for key, preset in self.PRESETS.items():
            print(f"📊 {preset['name']} ({key})")
            print(f"   {preset['description']}")
            print(f"   ├─ Specialists: {', '.join(preset['specialists'])}")
            print(f"   ├─ Authors: {', '.join(preset['authors'])}")
            print(f"   ├─ Análises: {preset['estimated_analyses']}")
            print(f"   ├─ Tempo estimado: {preset['estimated_time_minutes']} minutos")
            print(f"   └─ Caso de uso: {preset['use_case']}")
            print()

        print("=" * 80)
        print()

    def get_preset(self, mode: str) -> Optional[Dict]:
        """Retorna preset por nome"""
        return self.PRESETS.get(mode)

    def calculate_cost(self, preset: Dict, model: str) -> float:
        """Calcula custo estimado"""
        if model.startswith('gpt-'):
            cost_per_analysis = 0.11
            return preset['estimated_analyses'] * cost_per_analysis
        else:
            return 0.0

    def build_command(
        self,
        screenplay_path: str,
        specialists: List[str],
        authors: List[str],
        model: str = "scripturemon-optimized"
    ) -> List[str]:
        """Constrói comando para analyze_all_specialists.py"""

        cmd = [
            'python3',
            'analyze_all_specialists.py',
            screenplay_path,
            '--yes'  # Auto-confirmar
        ]

        # Adicionar filtros de specialists
        if specialists:
            cmd.extend(['--specialists', ','.join(specialists)])

        # Adicionar filtros de authors
        if authors:
            cmd.extend(['--authors', ','.join(authors)])

        # Modelo LLM
        if model != "scripturemon-optimized":
            cmd.extend(['--model', model])

        return cmd

    def run_partial_analysis(
        self,
        screenplay_path: str,
        mode: Optional[str] = None,
        specialists: Optional[List[str]] = None,
        authors: Optional[List[str]] = None,
        model: str = "scripturemon-optimized",
        dry_run: bool = False
    ):
        """Executa análise parcial"""

        # Validar screenplay
        if not Path(screenplay_path).exists():
            print(f"\n❌ Erro: Arquivo não encontrado: {screenplay_path}\n")
            return

        # Determinar configuração
        if mode:
            preset = self.get_preset(mode)
            if not preset:
                print(f"\n❌ Erro: Modo '{mode}' não encontrado. Use --list para ver modos disponíveis.\n")
                return

            specialists = preset['specialists']
            authors = preset['authors']
            preset_name = preset['name']
            estimated_time = preset['estimated_time_minutes']
            estimated_analyses = preset['estimated_analyses']
        else:
            # Custom mode
            if not specialists or not authors:
                print("\n❌ Erro: Modo custom requer --specialists e --authors\n")
                return

            preset_name = "Custom"
            # Estimar baseado em contagem
            estimated_analyses = len(specialists) * len(authors)
            estimated_time = estimated_analyses * 7  # ~7 min por análise

        # Calcular custo
        cost = self.calculate_cost({'estimated_analyses': estimated_analyses}, model)

        # Exibir informações
        print("\n" + "=" * 80)
        print(f"🎬 ANÁLISE PARCIAL: {preset_name}")
        print("=" * 80)
        print()
        print(f"📄 Screenplay: {Path(screenplay_path).name}")
        print(f"🔬 Specialists: {', '.join(specialists)}")
        print(f"📚 Authors: {', '.join(authors)}")
        print(f"🤖 Modelo: {model}")
        print(f"📊 Análises: {estimated_analyses}")
        print(f"⏱️  Tempo estimado: {estimated_time} minutos")

        if cost > 0:
            print(f"💰 Custo estimado: ${cost:.2f}")
        else:
            print(f"💰 Custo: Gratuito (Ollama local)")

        print()

        # Construir comando
        cmd = self.build_command(screenplay_path, specialists, authors, model)

        if dry_run:
            print("🔍 DRY RUN - Comando que seria executado:")
            print()
            print("   " + " ".join(cmd))
            print()
            print("=" * 80)
            print()
            return

        # Confirmar execução
        print("=" * 80)
        response = input("\nDeseja iniciar a análise? (S/n): ").strip().lower()

        if response == 'n':
            print("\n❌ Análise cancelada.\n")
            return

        # Executar
        print()
        print("=" * 80)
        print("▶️  INICIANDO ANÁLISE PARCIAL...")
        print("=" * 80)
        print()

        try:
            # Executar comando
            result = subprocess.run(cmd, check=True)

            if result.returncode == 0:
                print()
                print("=" * 80)
                print("✅ ANÁLISE PARCIAL CONCLUÍDA!")
                print("=" * 80)
                print()
            else:
                print()
                print("❌ Análise falhou com erro.")
                print()

        except subprocess.CalledProcessError as e:
            print()
            print(f"❌ Erro ao executar análise: {e}")
            print()
        except KeyboardInterrupt:
            print()
            print("⚠️  Análise interrompida pelo usuário.")
            print()


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(
        description='Análise Parcial Inteligente do Scripturemon',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python partial_analysis.py screenplay.pdf --mode quick
  python partial_analysis.py screenplay.pdf --mode character
  python partial_analysis.py screenplay.pdf --mode professional
  python partial_analysis.py screenplay.pdf --custom --specialists character,dialogue --authors mckee,field
        """
    )

    parser.add_argument('screenplay', nargs='?', help='Caminho do roteiro PDF')
    parser.add_argument('--mode', choices=['quick', 'character', 'structure', 'dialogue', 'theme', 'professional'],
                        help='Modo de análise pré-configurado')
    parser.add_argument('--custom', action='store_true', help='Modo custom (requer --specialists e --authors)')
    parser.add_argument('--specialists', help='Lista de specialists separados por vírgula (modo custom)')
    parser.add_argument('--authors', help='Lista de authors separados por vírgula (modo custom)')
    parser.add_argument('--model', default='scripturemon-optimized', help='Modelo LLM a usar')
    parser.add_argument('--list', action='store_true', help='Listar modos disponíveis')
    parser.add_argument('--dry-run', action='store_true', help='Simular execução sem rodar')

    args = parser.parse_args()

    manager = PartialAnalysisManager()

    # Listar modos
    if args.list:
        manager.list_presets()
        return

    # Validar argumentos
    if not args.screenplay:
        parser.print_help()
        print()
        print("💡 Dica: Use --list para ver todos os modos disponíveis")
        print()
        sys.exit(1)

    # Modo custom
    if args.custom:
        if not args.specialists or not args.authors:
            print("\n❌ Erro: Modo --custom requer --specialists e --authors\n")
            sys.exit(1)

        specialists = [s.strip() for s in args.specialists.split(',')]
        authors = [a.strip() for a in args.authors.split(',')]

        manager.run_partial_analysis(
            screenplay_path=args.screenplay,
            specialists=specialists,
            authors=authors,
            model=args.model,
            dry_run=args.dry_run
        )

    # Modo preset
    elif args.mode:
        manager.run_partial_analysis(
            screenplay_path=args.screenplay,
            mode=args.mode,
            model=args.model,
            dry_run=args.dry_run
        )

    else:
        print("\n❌ Erro: Especifique --mode ou --custom\n")
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
