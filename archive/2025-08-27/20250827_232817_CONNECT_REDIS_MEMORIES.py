#!/usr/bin/env python3
"""
🧠 CONEXÃO REDIS-DIGIMUNDO
Sistema de memória persistente e distribuída
"""

import redis
import json
import sqlite3
from datetime import datetime
from pathlib import Path

class DigimundoMemory:
    def __init__(self):
        # Conecta ao Redis
        self.redis = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True,
            db=0
        )
        
        # Paths do Digimundo
        self.base_path = Path.home() / "Digimundo"
        self.memory_path = self.base_path / "digimons" / "scripturemon" / "memory"
        
    def sync_memories(self):
        """Sincroniza memórias SQLite com Redis"""
        print("🔄 Sincronizando memórias do Digimundo com Redis...")
        
        # Conecta ao banco de conversações
        db_path = self.memory_path / "conversations.db"
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            try:
                # Busca conversações recentes
                cursor.execute("""
                    SELECT id, content, timestamp 
                    FROM conversations 
                    ORDER BY timestamp DESC 
                    LIMIT 100
                """)
                
                for row in cursor.fetchall():
                    key = f"digimundo:conversation:{row[0]}"
                    self.redis.hset(key, mapping={
                        "content": row[1],
                        "timestamp": row[2] or datetime.now().isoformat()
                    })
                    self.redis.expire(key, 86400 * 7)  # 7 dias
                    
                print(f"✅ Sincronizadas {cursor.rowcount} conversações")
                
            except Exception as e:
                print(f"⚠️ Erro ao sincronizar conversações: {e}")
            finally:
                conn.close()
    
    def store_digimon_state(self, name, data):
        """Armazena estado de um Digimon"""
        key = f"digimundo:digimon:{name}"
        self.redis.hset(key, mapping=data)
        self.redis.expire(key, 3600)  # 1 hora
        print(f"💾 Estado de {name} salvo no Redis")
    
    def get_active_digimons(self):
        """Lista Digimons ativos"""
        pattern = "digimundo:digimon:*"
        digimons = []
        
        for key in self.redis.scan_iter(pattern):
            data = self.redis.hgetall(key)
            name = key.split(":")[-1]
            digimons.append({
                "name": name,
                "data": data
            })
        
        return digimons
    
    def initialize_ecosystem(self):
        """Inicializa o ecossistema de memórias"""
        print("\n🌟 INICIALIZANDO ECOSSISTEMA DE MEMÓRIAS")
        print("=" * 50)
        
        # Marca início da sessão
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.redis.set("digimundo:current_session", session_id)
        
        # Registra Digimons principais
        main_digimons = [
            "scripturemon",
            "sabiamon", 
            "debugmon",
            "neuromon"
        ]
        
        for digimon in main_digimons:
            self.store_digimon_state(digimon, {
                "status": "ready",
                "level": "ultimate",
                "session": session_id,
                "activated_at": datetime.now().isoformat()
            })
        
        # Sincroniza memórias existentes
        self.sync_memories()
        
        # Status final
        print("\n📊 STATUS DO SISTEMA:")
        print(f"✅ Redis: Conectado")
        print(f"✅ Sessão: {session_id}")
        print(f"✅ Digimons ativos: {len(main_digimons)}")
        
        active = self.get_active_digimons()
        if active:
            print("\n🔥 DIGIMONS NO REDIS:")
            for d in active:
                print(f"  - {d['name']}: {d['data'].get('status', 'unknown')}")
        
        return True

if __name__ == "__main__":
    memory = DigimundoMemory()
    
    try:
        # Testa conexão
        memory.redis.ping()
        print("✅ Redis conectado com sucesso!")
        
        # Inicializa ecossistema
        memory.initialize_ecosystem()
        
        print("\n🎯 MEMÓRIAS DO DIGIMUNDO CONECTADAS AO REDIS!")
        print("Use 'redis-cli' para explorar as memórias")
        print("Padrão de chaves: digimundo:*")
        
    except redis.ConnectionError:
        print("❌ Erro: Redis não está rodando!")
        print("Execute: brew services start redis")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")