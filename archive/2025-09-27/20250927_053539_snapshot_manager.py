#!/usr/bin/env python3
"""
Sistema de Snapshot e Rollback - Protocolo Digivolve
Cria pontos de restauração automáticos
"""

import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class SnapshotManager:
    """
    Cria snapshots automáticos antes de cada mudança crítica
    Permite rollback instantâneo se algo quebrar
    """

    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-Omega")
        self.snapshots_dir = self.base_path / ".omega_snapshots"
        self.snapshots_dir.mkdir(exist_ok=True)
        self.current_snapshot = None
        self.metadata_file = self.snapshots_dir / "snapshots_metadata.json"
        self.metadata = self.load_metadata()

    def load_metadata(self) -> Dict:
        """Carrega metadados dos snapshots"""
        if self.metadata_file.exists():
            return json.loads(self.metadata_file.read_text())
        return {"snapshots": [], "current": None, "last_successful": None}

    def save_metadata(self):
        """Salva metadados dos snapshots"""
        self.metadata_file.write_text(json.dumps(self.metadata, indent=2))

    def create_snapshot(self, phase: int, stage: str = None, description: str = None) -> str:
        """Cria snapshot completo do estado atual"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_id = f"phase{phase}_{stage or 'unknown'}_{timestamp}"
        snapshot_path = self.snapshots_dir / snapshot_id

        # Cria diretório do snapshot (com handling para duplicados)
        if snapshot_path.exists():
            # Adiciona timestamp extra se já existe
            import time
            time.sleep(1)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_id = f"phase{phase}_{stage or 'unknown'}_{timestamp}"
            snapshot_path = self.snapshots_dir / snapshot_id

        snapshot_path.mkdir()

        # Diretórios para fazer backup
        dirs_to_backup = ["core", "scripts", "tests", "config", "specialists", "scripturemon"]
        files_to_backup = ["OMEGA_STATE.json", "OMEGA_HISTORY.jsonl", "OMEGA_METRICS_LIVE.json"]

        # Copia diretórios
        for dir_name in dirs_to_backup:
            source = self.base_path / dir_name
            if source.exists():
                dest = snapshot_path / dir_name
                try:
                    shutil.copytree(source, dest)
                except Exception:
                    pass  # Ignora erros

        # Copia arquivos individuais
        for file_name in files_to_backup:
            source = self.base_path / file_name
            if source.exists():
                dest = snapshot_path / file_name
                shutil.copy2(source, dest)

        # Salva metadados do snapshot
        metadata = {
            "id": snapshot_id,
            "phase": phase,
            "stage": stage,
            "description": description or f"Snapshot fase {phase}",
            "timestamp": timestamp,
            "created_at": datetime.now().isoformat(),
            "files_count": sum(1 for _ in snapshot_path.rglob("*") if _.is_file())
        }

        (snapshot_path / "snapshot_metadata.json").write_text(json.dumps(metadata, indent=2))

        # Atualiza metadados globais
        self.metadata["snapshots"].append(metadata)
        self.metadata["current"] = snapshot_id
        self.current_snapshot = snapshot_id
        self.save_metadata()

        print(f"✅ Snapshot criado: {snapshot_id}")
        print(f"   📁 Arquivos salvos: {metadata['files_count']}")
        return snapshot_id

    def rollback(self, snapshot_id: str = None) -> bool:
        """Volta para snapshot anterior"""
        if not snapshot_id:
            snapshot_id = self.current_snapshot

        if not snapshot_id:
            print("❌ Nenhum snapshot disponível para rollback")
            return False

        snapshot_path = self.snapshots_dir / snapshot_id

        if not snapshot_path.exists():
            print(f"❌ Snapshot {snapshot_id} não encontrado")
            return False

        print(f"⏮️ Iniciando rollback para {snapshot_id}...")

        # Limpa diretórios atuais
        dirs_to_clean = ["core", "scripts", "tests", "config", "specialists", "scripturemon"]
        for dir_name in dirs_to_clean:
            target = self.base_path / dir_name
            if target.exists():
                try:
                    shutil.rmtree(target)
                except Exception:
                    pass  # Ignora erros

        # Restaura do snapshot
        restored_count = 0
        for item in snapshot_path.iterdir():
            if item.name == "snapshot_metadata.json":
                continue

            dest = self.base_path / item.name

            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
                restored_count += sum(1 for _ in item.rglob("*") if _.is_file())
            else:
                shutil.copy2(item, dest)
                restored_count += 1

        print(f"✅ Rollback completo para {snapshot_id}")
        print(f"   📁 Arquivos restaurados: {restored_count}")

        # Atualiza metadados
        self.metadata["current"] = snapshot_id
        self.save_metadata()

        return True

    def list_snapshots(self) -> List[Dict]:
        """Lista todos os snapshots disponíveis"""
        return sorted(self.metadata.get("snapshots", []),
                     key=lambda x: x['created_at'], reverse=True)

    def get_latest_snapshot(self) -> Optional[str]:
        """Retorna ID do snapshot mais recente"""
        snapshots = self.list_snapshots()
        return snapshots[0]['id'] if snapshots else None

    def mark_successful(self, snapshot_id: str = None):
        """Marca um snapshot como bem-sucedido"""
        if not snapshot_id:
            snapshot_id = self.current_snapshot

        if snapshot_id:
            self.metadata["last_successful"] = snapshot_id
            self.save_metadata()
            print(f"✅ Snapshot {snapshot_id} marcado como bem-sucedido")

    def cleanup_old_snapshots(self, keep: int = 5):
        """Remove snapshots antigos, mantendo apenas os N mais recentes"""
        snapshots = self.list_snapshots()

        if len(snapshots) <= keep:
            return

        to_remove = snapshots[keep:]
        removed = 0

        for snapshot in to_remove:
            snapshot_path = self.snapshots_dir / snapshot['id']
            if snapshot_path.exists():
                shutil.rmtree(snapshot_path)
                removed += 1

        # Atualiza metadados
        self.metadata["snapshots"] = snapshots[:keep]
        self.save_metadata()

        print(f"🧹 Limpeza: {removed} snapshots antigos removidos")

    def emergency_rollback(self):
        """Rollback de emergência para último snapshot bem-sucedido"""
        if self.metadata.get("last_successful"):
            print("🚨 MODO EMERGÊNCIA: Voltando para último snapshot estável...")
            return self.rollback(self.metadata["last_successful"])
        else:
            print("❌ Nenhum snapshot bem-sucedido disponível")
            return False


def main():
    """Teste do snapshot manager"""
    snapshot = SnapshotManager()

    # Criar snapshot inicial
    snapshot_id = snapshot.create_snapshot(
        phase=0,
        stage="baby",
        description="Snapshot inicial - Sistema Digivolve"
    )

    # Listar snapshots
    print("\n📸 Snapshots disponíveis:")
    for snap in snapshot.list_snapshots():
        print(f"  - {snap['id']}: {snap['description']}")

    print(f"\n✅ Snapshot Manager ativo e funcionando!")
    return snapshot_id


if __name__ == "__main__":
    main()