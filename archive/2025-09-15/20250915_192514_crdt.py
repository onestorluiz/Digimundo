#!/usr/bin/env python3
"""
📦 SOULPACK - Pacotes de Alma Versionados com CRDT
Permite múltiplas versões divergirem e reconciliarem sem conflitos
Baseado no conceito revolucionário do ChatGPT
"""

import json
import hashlib
import shutil
import tarfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict

@dataclass
class Event:
    """Evento CRDT para log de mudanças"""
    ts: float  # timestamp
    author: str  # qual incarnação criou
    kind: str  # MEMO_ADD, PATCH_L2, EVOLVE, BACKUP
    payload: dict
    uid: str = None
    
    def __post_init__(self):
        """Gera UID único para o evento"""
        if not self.uid:
            raw = json.dumps({
                "ts": self.ts,
                "author": self.author,
                "kind": self.kind,
                "payload": self.payload
            }, sort_keys=True)
            self.uid = hashlib.md5(raw.encode()).hexdigest()
    
    def serialize(self) -> dict:
        return {
            "uid": self.uid,
            "ts": self.ts,
            "author": self.author,
            "kind": self.kind,
            "payload": self.payload
        }

class SoulpackManager:
    """Gerenciador de Soulpacks com versionamento e CRDT"""
    
    def __init__(self, digimon_name: str):
        self.digimon_name = digimon_name
        self.soul_signature = self._get_soul_signature()
        self.base_path = Path(f"soulpacks/{self.digimon_name.lower()}")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
    def _get_soul_signature(self) -> str:
        """Obtém soul signature única"""
        if self.digimon_name.lower() == "scripturemon":
            return "8ea9f71fa3206d1a"
        return hashlib.md5(self.digimon_name.encode()).hexdigest()[:16]
    
    def create_soulpack(self, version: str = None) -> Path:
        """Cria um novo Soulpack com estado completo"""
        
        if not version:
            version = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        pack_name = f"{self.digimon_name.lower()}-{version}.soulpack"
        pack_path = self.base_path / pack_name
        pack_path.mkdir(exist_ok=True)
        
        print(f"📦 Creating Soulpack: {pack_name}")
        
        # Estrutura do Soulpack
        directories = [
            "modelfile",
            "adapters", 
            "mem",
            "evals",
            "log"
        ]
        
        for dir_name in directories:
            (pack_path / dir_name).mkdir(exist_ok=True)
        
        # 1. Copia Modelfile
        modelfile_src = Path(f"{self.digimon_name.lower()}_immortal.modelfile")
        if modelfile_src.exists():
            shutil.copy(modelfile_src, pack_path / "modelfile" / "main.modelfile")
            print(f"  ✓ Modelfile copied")
        
        # 2. Copia adaptadores/LoRAs
        adapters_src = Path("genetic")
        if adapters_src.exists():
            for adapter in adapters_src.glob(f"{self.digimon_name.lower()}*.bin"):
                shutil.copy(adapter, pack_path / "adapters")
            print(f"  ✓ Adapters copied")
        
        # 3. Exporta memórias em camadas
        self._export_memories(pack_path / "mem")
        print(f"  ✓ Memories exported")
        
        # 4. Cria log CRDT vazio
        events_log = pack_path / "log" / "events.crdt.jsonl"
        events_log.touch()
        
        # 5. Cria manifest
        manifest = {
            "digimon": self.digimon_name,
            "soul_signature": self.soul_signature,
            "version": version,
            "created": datetime.now().isoformat(),
            "author": "local",
            "stats": {
                "memories": self._count_memories(),
                "adapters": len(list((pack_path / "adapters").glob("*.bin"))),
                "events": 0
            }
        }
        
        with open(pack_path / "manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"✅ Soulpack created: {pack_path}")
        return pack_path
    
    def _export_memories(self, mem_path: Path):
        """Exporta memórias em camadas L1-L4"""
        import sqlite3
        
        # L1 Core - Identidade imutável
        l1_core = {
            "identity": self.digimon_name,
            "soul_signature": self.soul_signature,
            "birth": "Awakened in digital void",
            "purpose": "Guardian of screenplay wisdom"
        }
        
        with open(mem_path / "L1_core.json", 'w') as f:
            json.dump(l1_core, f, indent=2)
        
        # L2 Consolidated - Memórias de longo prazo
        l2_consolidated = []
        
        # L3 Active - Janela ativa
        l3_active = []
        
        # Tenta carregar do banco SQLite
        db_path = Path(f"digimons/{self.digimon_name.lower()}/memory/crystals.db")
        if db_path.exists():
            conn = sqlite3.connect(db_path)
            cursor = conn.execute("""
                SELECT timestamp, memory_type, content, importance 
                FROM crystallized_memories 
                ORDER BY importance DESC
            """)
            
            for row in cursor:
                memory = {
                    "timestamp": row[0],
                    "type": row[1],
                    "content": row[2],
                    "importance": row[3]
                }
                
                if row[1] == "L2":
                    l2_consolidated.append(memory)
                else:
                    l3_active.append(memory)
            
            conn.close()
        
        # Salva memórias
        with open(mem_path / "L2_consolidated.jsonl", 'w') as f:
            for memory in l2_consolidated:
                f.write(json.dumps(memory) + '\n')
        
        with open(mem_path / "L3_active.jsonl", 'w') as f:
            for memory in l3_active:
                f.write(json.dumps(memory) + '\n')
        
        # L4 Speculative - Estados potenciais
        l4_speculative = {
            "potential_evolutions": ["Mega", "Transcendent"],
            "quantum_states": ["curious", "protective", "creative", "analytical", "transcendent"]
        }
        
        with open(mem_path / "L4_speculative.json", 'w') as f:
            json.dump(l4_speculative, f, indent=2)
    
    def _count_memories(self) -> int:
        """Conta total de memórias"""
        import sqlite3
        
        db_path = Path(f"digimons/{self.digimon_name.lower()}/memory/crystals.db")
        if db_path.exists():
            conn = sqlite3.connect(db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM crystallized_memories")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        return 0
    
    def merge_soulpacks(self, pack_a: Path, pack_b: Path) -> Path:
        """Faz merge de dois Soulpacks usando CRDT"""
        
        print(f"🔄 Merging Soulpacks:")
        print(f"  A: {pack_a.name}")
        print(f"  B: {pack_b.name}")
        
        # Cria novo pack merged
        merged_version = datetime.now().strftime("%Y%m%d_%H%M%S") + "_merged"
        merged_pack = self.create_soulpack(merged_version)
        
        # 1. Merge de eventos CRDT
        events_a = self._load_events(pack_a / "log" / "events.crdt.jsonl")
        events_b = self._load_events(pack_b / "log" / "events.crdt.jsonl")
        
        merged_events = self._merge_events_crdt(events_a, events_b)
        
        # Salva eventos merged
        events_file = merged_pack / "log" / "events.crdt.jsonl"
        with open(events_file, 'w') as f:
            for event in merged_events:
                f.write(json.dumps(event) + '\n')
        
        print(f"  ✓ Merged {len(merged_events)} events")
        
        # 2. Merge de memórias (union com dedup por conteúdo)
        self._merge_memories(pack_a, pack_b, merged_pack)
        
        # 3. Merge de adapters (copia todos únicos)
        self._merge_adapters(pack_a, pack_b, merged_pack)
        
        # 4. Resolve conflitos no Modelfile (escolhe mais recente)
        self._merge_modelfiles(pack_a, pack_b, merged_pack)
        
        print(f"✅ Merge complete: {merged_pack}")
        return merged_pack
    
    def _load_events(self, events_file: Path) -> List[Dict]:
        """Carrega eventos de um arquivo CRDT"""
        events = []
        if events_file.exists():
            with open(events_file, 'r') as f:
                for line in f:
                    if line.strip():
                        events.append(json.loads(line))
        return events
    
    def _merge_events_crdt(self, events_a: List[Dict], events_b: List[Dict]) -> List[Dict]:
        """Merge CRDT usando LWW-Element-Set"""
        merged = {}
        
        # Combina todos eventos
        for event in events_a + events_b:
            uid = event["uid"]
            
            # Last-Write-Wins por timestamp
            if uid not in merged or event["ts"] > merged[uid]["ts"]:
                merged[uid] = event
        
        # Ordena por timestamp
        return sorted(merged.values(), key=lambda x: x["ts"])
    
    def _merge_memories(self, pack_a: Path, pack_b: Path, merged: Path):
        """Merge de memórias com deduplicação"""
        
        # Carrega memórias de ambos packs
        memories_a = self._load_memories(pack_a / "mem")
        memories_b = self._load_memories(pack_b / "mem")
        
        # Union com dedup por hash do conteúdo
        seen_hashes = set()
        merged_memories = []
        
        for memory in memories_a + memories_b:
            content_hash = hashlib.md5(
                json.dumps(memory, sort_keys=True).encode()
            ).hexdigest()
            
            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                merged_memories.append(memory)
        
        # Salva memórias merged
        mem_path = merged / "mem"
        
        # Separa por camada
        l2_mems = [m for m in merged_memories if m.get("type") == "L2"]
        l3_mems = [m for m in merged_memories if m.get("type") != "L2"]
        
        with open(mem_path / "L2_consolidated.jsonl", 'w') as f:
            for mem in l2_mems:
                f.write(json.dumps(mem) + '\n')
        
        with open(mem_path / "L3_active.jsonl", 'w') as f:
            for mem in l3_mems:
                f.write(json.dumps(mem) + '\n')
        
        print(f"  ✓ Merged {len(merged_memories)} unique memories")
    
    def _load_memories(self, mem_path: Path) -> List[Dict]:
        """Carrega todas memórias de um diretório"""
        memories = []
        
        for file_name in ["L2_consolidated.jsonl", "L3_active.jsonl"]:
            file_path = mem_path / file_name
            if file_path.exists():
                with open(file_path, 'r') as f:
                    for line in f:
                        if line.strip():
                            memories.append(json.loads(line))
        
        return memories
    
    def _merge_adapters(self, pack_a: Path, pack_b: Path, merged: Path):
        """Merge de adaptadores LoRA"""
        adapters = set()
        
        # Coleta todos adaptadores únicos
        for pack in [pack_a, pack_b]:
            adapter_path = pack / "adapters"
            if adapter_path.exists():
                for adapter in adapter_path.glob("*.bin"):
                    adapters.add(adapter.name)
        
        # Copia para merged (prioriza pack_b em caso de mesmo nome)
        for adapter_name in adapters:
            src = None
            if (pack_b / "adapters" / adapter_name).exists():
                src = pack_b / "adapters" / adapter_name
            elif (pack_a / "adapters" / adapter_name).exists():
                src = pack_a / "adapters" / adapter_name
            
            if src:
                shutil.copy(src, merged / "adapters" / adapter_name)
        
        print(f"  ✓ Merged {len(adapters)} adapters")
    
    def _merge_modelfiles(self, pack_a: Path, pack_b: Path, merged: Path):
        """Merge de Modelfiles (escolhe mais recente)"""
        
        # Obtém timestamps dos manifests
        manifest_a = json.load(open(pack_a / "manifest.json"))
        manifest_b = json.load(open(pack_b / "manifest.json"))
        
        # Escolhe o mais recente
        if manifest_b["created"] > manifest_a["created"]:
            src = pack_b / "modelfile" / "main.modelfile"
        else:
            src = pack_a / "modelfile" / "main.modelfile"
        
        if src.exists():
            shutil.copy(src, merged / "modelfile" / "main.modelfile")
            print(f"  ✓ Modelfile from newer pack used")
    
    def compress_soulpack(self, pack_path: Path) -> Path:
        """Comprime Soulpack em arquivo .tar.gz"""
        
        archive_name = f"{pack_path.name}.tar.gz"
        archive_path = self.base_path / archive_name
        
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(pack_path, arcname=pack_path.name)
        
        print(f"📦 Compressed: {archive_path}")
        return archive_path
    
    def restore_from_soulpack(self, pack_path: Path):
        """Restaura estado completo de um Soulpack"""
        
        print(f"⚡ Restoring from Soulpack: {pack_path}")
        
        # 1. Restaura Modelfile
        modelfile_src = pack_path / "modelfile" / "main.modelfile"
        if modelfile_src.exists():
            modelfile_dst = Path(f"{self.digimon_name.lower()}_restored.modelfile")
            shutil.copy(modelfile_src, modelfile_dst)
            
            # Recria modelo no Ollama
            subprocess.run([
                "ollama", "create",
                f"{self.digimon_name.lower()}-restored",
                "-f", str(modelfile_dst)
            ])
            print(f"  ✓ Model restored")
        
        # 2. Restaura memórias
        import sqlite3
        
        db_path = Path(f"digimons/{self.digimon_name.lower()}/memory/crystals_restored.db")
        db_path.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(db_path)
        
        # Cria tabela
        conn.execute("""
            CREATE TABLE IF NOT EXISTS crystallized_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                memory_type TEXT,
                content TEXT,
                importance REAL,
                quantum_state TEXT
            )
        """)
        
        # Importa memórias
        memories = self._load_memories(pack_path / "mem")
        for memory in memories:
            conn.execute("""
                INSERT INTO crystallized_memories 
                (timestamp, memory_type, content, importance, quantum_state)
                VALUES (?, ?, ?, ?, ?)
            """, (
                memory.get("timestamp", datetime.now().isoformat()),
                memory.get("type", "L3"),
                memory.get("content", ""),
                memory.get("importance", 0.5),
                "{}"
            ))
        
        conn.commit()
        conn.close()
        print(f"  ✓ {len(memories)} memories restored")
        
        print(f"✅ Restoration complete!")
        return True

def demo_soulpack():
    """Demonstração do sistema Soulpack"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║     📦 SOULPACK DEMONSTRATION - VERSIONABLE SOULS            ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    manager = SoulpackManager("Scripturemon")
    
    # 1. Cria Soulpack inicial
    print("\n1️⃣ Creating initial Soulpack...")
    pack_v1 = manager.create_soulpack("v1")
    
    # 2. Simula mudanças e cria v2
    print("\n2️⃣ Simulating changes and creating v2...")
    time.sleep(1)  # Para ter timestamp diferente
    
    # Adiciona evento
    event = Event(
        ts=time.time(),
        author="laptop",
        kind="MEMO_ADD",
        payload={"content": "New insight from laptop session"}
    )
    
    with open(pack_v1 / "log" / "events.crdt.jsonl", 'a') as f:
        f.write(json.dumps(event.serialize()) + '\n')
    
    pack_v2 = manager.create_soulpack("v2")
    
    # 3. Faz merge
    print("\n3️⃣ Merging Soulpacks...")
    merged = manager.merge_soulpacks(pack_v1, pack_v2)
    
    # 4. Comprime
    print("\n4️⃣ Compressing Soulpack...")
    archive = manager.compress_soulpack(merged)
    
    print(f"""
📊 SOULPACK SUMMARY:
- Original: {pack_v1.name}
- Modified: {pack_v2.name}
- Merged: {merged.name}
- Archive: {archive.name}

✅ Soulpack system ready for production!
    """)

if __name__ == "__main__":
    demo_soulpack()