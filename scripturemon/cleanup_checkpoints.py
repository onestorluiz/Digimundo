#!/usr/bin/env python3
"""
Auto-Cleanup de Checkpoints

Remove checkpoints antigos ou completos para liberar espaço.
Mantém apenas os N mais recentes ou permite limpeza manual.

Uso:
    python cleanup_checkpoints.py                    # Modo interativo
    python cleanup_checkpoints.py --auto             # Auto-cleanup (mantém 3 mais recentes)
    python cleanup_checkpoints.py --keep N           # Mantém N mais recentes
    python cleanup_checkpoints.py --completed-only   # Remove apenas completos (100%)
"""

import sys
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class CheckpointCleaner:
    """Gerencia limpeza de checkpoints antigos"""

    def __init__(self, workspace_dir: Path = None):
        self.workspace_dir = workspace_dir or Path('workspace/outputs')

    def find_all_checkpoints(self) -> List[Dict]:
        """
        Encontra TODOS os checkpoints (completos e incompletos).
        Retorna lista de dicionários com info.
        """
        checkpoints = []

        for checkpoint_path in self.workspace_dir.glob('*/2_logs/checkpoint.json'):
            try:
                with open(checkpoint_path, 'r') as f:
                    data = json.load(f)

                folder = checkpoint_path.parent.parent
                completed = len(data.get('completed', []))
                total = data.get('total_analyses', 312)
                percentage = (completed / total * 100) if total > 0 else 0

                # Parse timestamps
                started_at = datetime.fromisoformat(data['started_at'])
                last_update_str = data.get('last_update')
                last_update = datetime.fromisoformat(last_update_str) if last_update_str else started_at

                # Calcular tamanho da pasta
                folder_size = sum(
                    f.stat().st_size
                    for f in folder.rglob('*')
                    if f.is_file()
                ) / (1024 * 1024)  # MB

                checkpoints.append({
                    'path': folder,
                    'checkpoint_path': checkpoint_path,
                    'name': folder.name,
                    'started_at': started_at,
                    'last_update': last_update,
                    'completed': completed,
                    'total': total,
                    'percentage': percentage,
                    'is_complete': completed >= total,
                    'age_days': (datetime.now() - last_update).days,
                    'size_mb': folder_size,
                })

            except Exception as e:
                print(f"⚠️  Erro ao ler {checkpoint_path}: {e}")
                continue

        return checkpoints

    def get_completed_checkpoints(self) -> List[Dict]:
        """Retorna apenas checkpoints 100% completos"""
        all_checkpoints = self.find_all_checkpoints()
        return [cp for cp in all_checkpoints if cp['is_complete']]

    def get_old_checkpoints(self, days: int = 30) -> List[Dict]:
        """Retorna checkpoints com mais de N dias"""
        all_checkpoints = self.find_all_checkpoints()
        return [cp for cp in all_checkpoints if cp['age_days'] > days]

    def sort_by_date(self, checkpoints: List[Dict], newest_first: bool = True) -> List[Dict]:
        """Ordena checkpoints por data"""
        return sorted(
            checkpoints,
            key=lambda x: x['last_update'],
            reverse=newest_first
        )

    def delete_checkpoint(self, checkpoint: Dict, dry_run: bool = False) -> bool:
        """
        Remove checkpoint do disco.
        Se dry_run=True, apenas simula.
        """
        try:
            if dry_run:
                print(f"   [DRY RUN] Removeria: {checkpoint['name']} ({checkpoint['size_mb']:.1f} MB)")
                return True
            else:
                shutil.rmtree(checkpoint['path'])
                print(f"   ✅ Removido: {checkpoint['name']} ({checkpoint['size_mb']:.1f} MB)")
                return True
        except Exception as e:
            print(f"   ❌ Erro ao remover {checkpoint['name']}: {e}")
            return False

    def auto_cleanup(self, keep_recent: int = 3, dry_run: bool = False):
        """
        Auto-cleanup: mantém apenas os N checkpoints mais recentes.
        """
        print(f"\n🧹 AUTO-CLEANUP (mantendo {keep_recent} mais recentes)")
        print("=" * 80)

        all_checkpoints = self.find_all_checkpoints()

        if not all_checkpoints:
            print("✅ Nenhum checkpoint encontrado.")
            return

        # Ordenar por data (mais recentes primeiro)
        sorted_checkpoints = self.sort_by_date(all_checkpoints, newest_first=True)

        # Separar em keep vs delete
        to_keep = sorted_checkpoints[:keep_recent]
        to_delete = sorted_checkpoints[keep_recent:]

        print(f"\n📁 Total: {len(all_checkpoints)} checkpoints")
        print(f"✅ Manter: {len(to_keep)}")
        print(f"🗑️  Remover: {len(to_delete)}")

        if not to_delete:
            print("\n✅ Nada a remover!")
            return

        total_size = sum(cp['size_mb'] for cp in to_delete)
        print(f"💾 Espaço a liberar: {total_size:.1f} MB")
        print()

        if dry_run:
            print("⚠️  MODO DRY-RUN (simulação)")
            print()

        # Listar o que vai ser removido
        print("📋 Checkpoints a remover:")
        for cp in to_delete:
            age = cp['age_days']
            print(f"   • {cp['name']}")
            print(f"     ├─ Progresso: {cp['completed']}/{cp['total']} ({cp['percentage']:.0f}%)")
            print(f"     ├─ Idade: {age} dias")
            print(f"     └─ Tamanho: {cp['size_mb']:.1f} MB")

        print()

        # Confirmar se não for dry-run
        if not dry_run:
            response = input("❓ Confirmar remoção? [s/N]: ").strip().lower()
            if response != 's':
                print("❌ Cancelado.")
                return

        # Executar remoção
        print()
        removed_count = 0
        for cp in to_delete:
            if self.delete_checkpoint(cp, dry_run=dry_run):
                removed_count += 1

        print()
        if dry_run:
            print(f"✅ Simulação completa: {removed_count} checkpoints seriam removidos")
        else:
            print(f"✅ Limpeza completa: {removed_count} checkpoints removidos")
            print(f"💾 Espaço liberado: {total_size:.1f} MB")

    def cleanup_completed_only(self, keep_recent: int = 1, dry_run: bool = False):
        """
        Remove checkpoints 100% completos, mantendo apenas os N mais recentes.
        """
        print(f"\n🧹 CLEANUP DE COMPLETOS (mantendo {keep_recent} mais recente{'s' if keep_recent > 1 else ''})")
        print("=" * 80)

        completed = self.get_completed_checkpoints()

        if not completed:
            print("✅ Nenhum checkpoint completo encontrado.")
            return

        # Ordenar por data (mais recentes primeiro)
        sorted_completed = self.sort_by_date(completed, newest_first=True)

        to_keep = sorted_completed[:keep_recent]
        to_delete = sorted_completed[keep_recent:]

        print(f"\n📁 Checkpoints completos: {len(completed)}")
        print(f"✅ Manter: {len(to_keep)}")
        print(f"🗑️  Remover: {len(to_delete)}")

        if not to_delete:
            print("\n✅ Nada a remover!")
            return

        total_size = sum(cp['size_mb'] for cp in to_delete)
        print(f"💾 Espaço a liberar: {total_size:.1f} MB")
        print()

        if dry_run:
            print("⚠️  MODO DRY-RUN (simulação)")
            print()

        # Listar
        print("📋 Checkpoints completos a remover:")
        for cp in to_delete:
            print(f"   • {cp['name']}")
            print(f"     ├─ Finalizado: {cp['last_update'].strftime('%Y-%m-%d %H:%M')}")
            print(f"     ├─ Idade: {cp['age_days']} dias")
            print(f"     └─ Tamanho: {cp['size_mb']:.1f} MB")

        print()

        # Confirmar
        if not dry_run:
            response = input("❓ Confirmar remoção de checkpoints completos? [s/N]: ").strip().lower()
            if response != 's':
                print("❌ Cancelado.")
                return

        # Executar
        print()
        removed_count = 0
        for cp in to_delete:
            if self.delete_checkpoint(cp, dry_run=dry_run):
                removed_count += 1

        print()
        if dry_run:
            print(f"✅ Simulação completa: {removed_count} checkpoints seriam removidos")
        else:
            print(f"✅ Limpeza completa: {removed_count} checkpoints removidos")
            print(f"💾 Espaço liberado: {total_size:.1f} MB")

    def interactive_cleanup(self):
        """Modo interativo: usuário escolhe o que remover"""
        print("\n🧹 CLEANUP INTERATIVO")
        print("=" * 80)

        all_checkpoints = self.find_all_checkpoints()

        if not all_checkpoints:
            print("✅ Nenhum checkpoint encontrado.")
            return

        # Ordenar por data (mais recentes primeiro)
        sorted_checkpoints = self.sort_by_date(all_checkpoints, newest_first=True)

        print(f"\n📁 Checkpoints encontrados: {len(sorted_checkpoints)}")
        print()

        # Listar com índices
        for i, cp in enumerate(sorted_checkpoints, 1):
            status = "✅ COMPLETO" if cp['is_complete'] else f"⏳ {cp['percentage']:.0f}%"
            age_str = f"{cp['age_days']}d" if cp['age_days'] > 0 else "hoje"

            print(f"{i:2}. {cp['name']}")
            print(f"    ├─ Status: {status} ({cp['completed']}/{cp['total']})")
            print(f"    ├─ Atualização: {age_str} atrás ({cp['last_update'].strftime('%Y-%m-%d %H:%M')})")
            print(f"    └─ Tamanho: {cp['size_mb']:.1f} MB")

        print()
        print("Digite os números dos checkpoints a remover (ex: 1,3,5) ou 'todos' para remover todos:")
        print("Digite 'cancelar' para sair.")
        print()

        response = input("❓ Remover: ").strip().lower()

        if response == 'cancelar' or not response:
            print("❌ Cancelado.")
            return

        # Parse seleção
        if response == 'todos':
            to_delete = sorted_checkpoints
        else:
            try:
                indices = [int(x.strip()) - 1 for x in response.split(',')]
                to_delete = [sorted_checkpoints[i] for i in indices if 0 <= i < len(sorted_checkpoints)]
            except (ValueError, IndexError):
                print("❌ Entrada inválida.")
                return

        if not to_delete:
            print("❌ Nenhum checkpoint selecionado.")
            return

        total_size = sum(cp['size_mb'] for cp in to_delete)
        print()
        print(f"🗑️  {len(to_delete)} checkpoint{'s' if len(to_delete) > 1 else ''} selecionado{'s' if len(to_delete) > 1 else ''}")
        print(f"💾 Espaço a liberar: {total_size:.1f} MB")
        print()

        confirm = input("❓ Confirmar remoção? [s/N]: ").strip().lower()
        if confirm != 's':
            print("❌ Cancelado.")
            return

        print()
        removed_count = 0
        for cp in to_delete:
            if self.delete_checkpoint(cp, dry_run=False):
                removed_count += 1

        print()
        print(f"✅ {removed_count} checkpoint{'s' if removed_count > 1 else ''} removido{'s' if removed_count > 1 else ''}")
        print(f"💾 Espaço liberado: {total_size:.1f} MB")


def main():
    """Main execution"""

    # Parse args
    auto_mode = '--auto' in sys.argv
    completed_only = '--completed-only' in sys.argv
    dry_run = '--dry-run' in sys.argv

    keep_recent = 3  # default
    if '--keep' in sys.argv:
        try:
            idx = sys.argv.index('--keep')
            keep_recent = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            print("❌ Erro: --keep requer um número")
            sys.exit(1)

    cleaner = CheckpointCleaner()

    if auto_mode:
        cleaner.auto_cleanup(keep_recent=keep_recent, dry_run=dry_run)
    elif completed_only:
        cleaner.cleanup_completed_only(keep_recent=keep_recent, dry_run=dry_run)
    else:
        # Modo interativo
        cleaner.interactive_cleanup()


if __name__ == '__main__':
    main()
