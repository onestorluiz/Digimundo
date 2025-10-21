import sqlite3
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
import fakeredis

class MemoryManager:
    def __init__(self, base_path: Path = None):
        if base_path is None:
            base_path = Path.cwd() / "memory_store"
        base_path.mkdir(exist_ok=True)
        
        # L1: Redis cache (using fakeredis for testing)
        self.l1_cache = fakeredis.FakeRedis(decode_responses=True)
        
        # L2: SQLite in-memory
        self.l2_mem = sqlite3.connect(':memory:')
        self._init_l2()
        
        # L3: SQLite persistent
        self.l3_path = base_path / "l3_persistent.db"
        self.l3_db = sqlite3.connect(self.l3_path)
        self._init_l3()
        
        # L4: Filesystem
        self.l4_path = base_path / "l4_permanent"
        self.l4_path.mkdir(exist_ok=True)
    
    def _init_l2(self):
        """Initialize L2 in-memory database"""
        cursor = self.l2_mem.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                key TEXT PRIMARY KEY,
                value TEXT,
                access_count INTEGER DEFAULT 0,
                last_access REAL,
                created REAL
            )
        ''')
        self.l2_mem.commit()
    
    def _init_l3(self):
        """Initialize L3 persistent database"""
        cursor = self.l3_db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                key TEXT PRIMARY KEY,
                value TEXT,
                access_count INTEGER DEFAULT 0,
                last_access REAL,
                created REAL,
                narrative_weight REAL DEFAULT 1.0
            )
        ''')
        self.l3_db.commit()
    
    def store(self, key: str, value: Any, level: int = 1):
        """Store memory at specified level"""
        value_str = json.dumps(value) if not isinstance(value, str) else value
        timestamp = time.time()
        
        if level == 1:
            # L1: Redis with TTL
            self.l1_cache.setex(key, 300, value_str)  # 5 min TTL
        
        elif level == 2:
            # L2: SQLite in-memory
            cursor = self.l2_mem.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO memories (key, value, last_access, created)
                VALUES (?, ?, ?, ?)
            ''', (key, value_str, timestamp, timestamp))
            self.l2_mem.commit()
        
        elif level == 3:
            # L3: SQLite persistent
            cursor = self.l3_db.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO memories (key, value, last_access, created)
                VALUES (?, ?, ?, ?)
            ''', (key, value_str, timestamp, timestamp))
            self.l3_db.commit()
        
        elif level == 4:
            # L4: Filesystem
            file_path = self.l4_path / f"{key}.json"
            file_path.write_text(value_str)
    
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve memory with cascade through levels"""
        # Try L1
        value = self.l1_cache.get(key)
        if value:
            return json.loads(value) if value.startswith('{') else value
        
        # Try L2
        cursor = self.l2_mem.cursor()
        cursor.execute('SELECT value FROM memories WHERE key = ?', (key,))
        result = cursor.fetchone()
        if result:
            # Promote to L1
            self.l1_cache.setex(key, 300, result[0])
            return json.loads(result[0]) if result[0].startswith('{') else result[0]
        
        # Try L3
        cursor = self.l3_db.cursor()
        cursor.execute('SELECT value FROM memories WHERE key = ?', (key,))
        result = cursor.fetchone()
        if result:
            # Promote to L2 and L1
            self.store(key, result[0], level=2)
            self.l1_cache.setex(key, 300, result[0])
            return json.loads(result[0]) if result[0].startswith('{') else result[0]
        
        # Try L4
        file_path = self.l4_path / f"{key}.json"
        if file_path.exists():
            value = file_path.read_text()
            # Promote to L3, L2, and L1
            self.store(key, value, level=3)
            self.store(key, value, level=2)
            self.l1_cache.setex(key, 300, value)
            return json.loads(value) if value.startswith('{') else value
        
        return None
    
    def get_stats(self) -> Dict:
        """Get memory statistics"""
        l1_keys = len(self.l1_cache.keys())
        
        cursor = self.l2_mem.cursor()
        cursor.execute('SELECT COUNT(*) FROM memories')
        l2_count = cursor.fetchone()[0]
        
        cursor = self.l3_db.cursor()
        cursor.execute('SELECT COUNT(*) FROM memories')
        l3_count = cursor.fetchone()[0]
        
        l4_count = len(list(self.l4_path.glob("*.json")))
        
        return {
            'l1_cache': l1_keys,
            'l2_memory': l2_count,
            'l3_persistent': l3_count,
            'l4_filesystem': l4_count
        }
