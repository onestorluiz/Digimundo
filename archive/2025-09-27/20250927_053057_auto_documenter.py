#!/usr/bin/env python3
"""
Sistema de Auto-Documentação - Protocolo Digivolve
Rastreia automaticamente cada mudança no sistema
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class AutoDocumenter:
    """
    Documenta AUTOMATICAMENTE cada mudança no código
    para manter contexto completo entre sessões
    """

    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-Omega")
        self.state_file = self.base_path / "OMEGA_STATE.json"
        self.history_file = self.base_path / "OMEGA_HISTORY.jsonl"
        self.current_state = self.load_state()

    def load_state(self) -> Dict:
        """Carrega estado atual do sistema"""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())

        # Estado inicial - Baby Form
        return {
            "version": "0.0.1",
            "stage": "baby",
            "phase": 0,
            "files": {},
            "tests_passing": {},
            "last_update": None,
            "known_issues": [],
            "working_features": [],
            "broken_features": [],
            "power_level": 100,
            "harmony": 0.40,
            "quality_score": 0.70,
            "production_score": 0.40,
            "checkpoints": []
        }

    def track_file(self, filepath: str, action: str = "modified"):
        """Rastreia cada arquivo modificado com hash"""
        path = Path(filepath)
        if path.exists():
            content = path.read_bytes()
            file_hash = hashlib.sha256(content).hexdigest()

            relative_path = str(path.relative_to(self.base_path) if path.is_relative_to(self.base_path) else path)

            self.current_state["files"][relative_path] = {
                "hash": file_hash,
                "size": len(content),
                "last_modified": datetime.now().isoformat(),
                "action": action,
                "phase": self.current_state["phase"],
                "stage": self.current_state["stage"]
            }

            self.save_state()
            self.log_history(f"File {action}: {relative_path}")
            return True
        return False

    def mark_test(self, test_name: str, passed: bool, error: str = None):
        """Marca status de cada teste"""
        self.current_state["tests_passing"][test_name] = {
            "passed": passed,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.save_state()

    def mark_feature(self, feature: str, status: str = "working"):
        """Marca features como working/broken"""
        if status == "working":
            if feature not in self.current_state["working_features"]:
                self.current_state["working_features"].append(feature)
            if feature in self.current_state["broken_features"]:
                self.current_state["broken_features"].remove(feature)
        else:
            if feature not in self.current_state["broken_features"]:
                self.current_state["broken_features"].append(feature)
            if feature in self.current_state["working_features"]:
                self.current_state["working_features"].remove(feature)

        self.save_state()

    def update_metrics(self, **metrics):
        """Atualiza métricas do sistema"""
        for key, value in metrics.items():
            if key in ["harmony", "quality_score", "production_score", "power_level"]:
                self.current_state[key] = value
        self.save_state()

    def evolve_stage(self, new_stage: str):
        """Marca evolução para novo estágio"""
        stages = ["baby", "in_training", "rookie", "champion", "ultimate", "mega", "mega_plus"]
        if new_stage in stages:
            old_stage = self.current_state["stage"]
            self.current_state["stage"] = new_stage
            self.current_state["phase"] += 1
            self.log_history(f"EVOLVED: {old_stage} → {new_stage}")
            self.save_state()
            return True
        return False

    def create_checkpoint(self, description: str = None):
        """Cria checkpoint do estado atual"""
        checkpoint = {
            "id": f"checkpoint_{self.current_state['phase']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "stage": self.current_state["stage"],
            "phase": self.current_state["phase"],
            "description": description or f"Checkpoint at {self.current_state['stage']}",
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "quality": self.current_state.get("quality_score", 0),
                "harmony": self.current_state.get("harmony", 0),
                "power_level": self.current_state.get("power_level", 0)
            }
        }
        self.current_state["checkpoints"].append(checkpoint)
        self.save_state()
        return checkpoint["id"]

    def save_state(self):
        """Salva estado atual"""
        self.current_state["last_update"] = datetime.now().isoformat()
        self.state_file.write_text(json.dumps(self.current_state, indent=2))

    def log_history(self, message: str):
        """Adiciona ao histórico (append-only)"""
        with open(self.history_file, 'a') as f:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "phase": self.current_state["phase"],
                "stage": self.current_state["stage"],
                "version": self.current_state["version"]
            }
            f.write(json.dumps(entry) + '\n')

    def get_summary(self) -> str:
        """Retorna resumo para visualização"""
        working = len(self.current_state['working_features'])
        broken = len(self.current_state['broken_features'])
        tests_pass = sum(1 for t in self.current_state['tests_passing'].values() if t.get('passed'))
        tests_total = len(self.current_state['tests_passing'])

        last_update = str(self.current_state.get('last_update', 'Never'))[:19]

        return f"""
╔════════════════════════════════════════════════════════╗
║           OMEGA-ASCENT DIGIVOLVE STATUS               ║
╠════════════════════════════════════════════════════════╣
║ Stage: {self.current_state['stage']:15s} Power: {self.current_state.get('power_level', 0):5d}    ║
║ Version: {self.current_state['version']:13s} Phase: {self.current_state['phase']:2d}           ║
╠════════════════════════════════════════════════════════╣
║ Quality:    {self.current_state.get('quality_score', 0):.2f}                              ║
║ Harmony:    {self.current_state.get('harmony', 0):.2f}                              ║
║ Production: {self.current_state.get('production_score', 0):.2f}                              ║
╠════════════════════════════════════════════════════════╣
║ Files tracked: {len(self.current_state['files']):3d}                              ║
║ Tests: {tests_pass:2d}/{tests_total:2d} passing                              ║
║ Features: ✅ {working:2d}  ❌ {broken:2d}                         ║
║                                                        ║
║ Last Update: {last_update:19s}           ║
╚════════════════════════════════════════════════════════╝
        """


def main():
    """Teste do auto-documentador"""
    doc = AutoDocumenter()
    print(doc.get_summary())

    # Criar checkpoint inicial
    checkpoint_id = doc.create_checkpoint("Sistema Digivolve iniciado")
    print(f"✅ Checkpoint criado: {checkpoint_id}")

    # Rastrear este arquivo
    doc.track_file(__file__, "created")
    doc.mark_feature("auto_documentation", "working")
    print("✅ Auto-documentador ativo e funcionando!")


if __name__ == "__main__":
    main()