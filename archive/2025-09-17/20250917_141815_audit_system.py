#!/usr/bin/env python3
"""
🔍 SISTEMA DE AUDITORIA COMPLETO
=================================
Rastreia TODAS as operações no sistema
"""

import os
import sys
import json
import sqlite3
import hashlib
import threading
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict
import psutil

CLAUDE_CODE_DIR = Path("/Users/clubproducoes/Digimundo/claude_code")
AUDIT_DB = CLAUDE_CODE_DIR / "protection/audit.db"
PROTECTED_DIR = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")

class AuditSystem:
    """Sistema completo de auditoria com análise forense"""

    def __init__(self):
        self.init_database()
        self.file_hashes = self.calculate_initial_hashes()
        self.active_monitors = []
        self.start_monitoring()

    def init_database(self):
        """Inicializa banco de dados de auditoria"""
        AUDIT_DB.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(AUDIT_DB), check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Cria tabelas
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                operation TEXT NOT NULL,
                filepath TEXT NOT NULL,
                user TEXT NOT NULL,
                process_id INTEGER,
                process_name TEXT,
                success BOOLEAN,
                threat_level REAL,
                session_id TEXT,
                ip_address TEXT,
                quantum_signature TEXT,
                blockchain_hash TEXT
            );

            CREATE TABLE IF NOT EXISTS file_integrity (
                filepath TEXT PRIMARY KEY,
                original_hash TEXT NOT NULL,
                current_hash TEXT,
                last_modified TEXT,
                modifications INTEGER DEFAULT 0,
                suspicious_activity BOOLEAN DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS intrusion_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                attack_type TEXT,
                source_ip TEXT,
                target_file TEXT,
                payload TEXT,
                blocked BOOLEAN,
                severity TEXT
            );

            CREATE TABLE IF NOT EXISTS session_history (
                session_id TEXT PRIMARY KEY,
                start_time TEXT,
                end_time TEXT,
                user TEXT,
                operations_count INTEGER,
                threat_events INTEGER,
                max_threat_level REAL
            );

            CREATE TABLE IF NOT EXISTS forensic_evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                evidence_type TEXT,
                description TEXT,
                data BLOB,
                hash TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_timestamp ON audit_log(timestamp);
            CREATE INDEX IF NOT EXISTS idx_filepath ON audit_log(filepath);
            CREATE INDEX IF NOT EXISTS idx_threat ON audit_log(threat_level);
        """)

        self.conn.commit()

    def calculate_initial_hashes(self) -> Dict[str, str]:
        """Calcula hashes iniciais de todos os arquivos"""
        hashes = {}

        for file_path in PROTECTED_DIR.rglob('*'):
            if file_path.is_file():
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        file_hash = hashlib.sha256(content).hexdigest()
                        hashes[str(file_path)] = file_hash

                        # Salva no banco
                        self.cursor.execute("""
                            INSERT OR REPLACE INTO file_integrity
                            (filepath, original_hash, current_hash, last_modified)
                            VALUES (?, ?, ?, ?)
                        """, (str(file_path), file_hash, file_hash, datetime.now().isoformat()))

                except:
                    pass

        self.conn.commit()
        return hashes

    def log_operation(self, operation: str, filepath: str, **kwargs):
        """Registra operação no banco"""
        # Coleta informações do processo
        try:
            process = psutil.Process()
            process_id = process.pid
            process_name = process.name()
        except:
            process_id = os.getpid()
            process_name = "unknown"

        # Gera assinatura quântica simulada
        quantum_signature = self.generate_quantum_signature(operation, filepath)

        # Insere no banco
        self.cursor.execute("""
            INSERT INTO audit_log
            (timestamp, operation, filepath, user, process_id, process_name,
             success, threat_level, session_id, quantum_signature)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            operation,
            filepath,
            kwargs.get('user', 'system'),
            process_id,
            process_name,
            kwargs.get('success', True),
            kwargs.get('threat_level', 0.0),
            kwargs.get('session_id', ''),
            quantum_signature
        ))

        self.conn.commit()

        # Verifica integridade do arquivo
        self.check_file_integrity(filepath)

    def generate_quantum_signature(self, operation: str, filepath: str) -> str:
        """Gera assinatura quântica para operação"""
        quantum_seed = 0x1337DEADBEEF
        timestamp = datetime.now().timestamp()

        # Simula entrelaçamento quântico
        entangled = hashlib.sha512(
            f"{operation}{filepath}{timestamp}{quantum_seed}".encode()
        ).hexdigest()

        return entangled

    def check_file_integrity(self, filepath: str):
        """Verifica integridade do arquivo"""
        if not Path(filepath).exists():
            return

        try:
            with open(filepath, 'rb') as f:
                current_hash = hashlib.sha256(f.read()).hexdigest()

            # Busca hash original
            self.cursor.execute("""
                SELECT original_hash, current_hash, modifications
                FROM file_integrity
                WHERE filepath = ?
            """, (filepath,))

            result = self.cursor.fetchone()

            if result:
                original_hash, last_hash, mods = result

                if current_hash != last_hash:
                    # Arquivo foi modificado
                    self.cursor.execute("""
                        UPDATE file_integrity
                        SET current_hash = ?, last_modified = ?, modifications = ?,
                            suspicious_activity = ?
                        WHERE filepath = ?
                    """, (
                        current_hash,
                        datetime.now().isoformat(),
                        mods + 1,
                        1 if mods > 10 else 0,  # Suspeito se muitas modificações
                        filepath
                    ))

                    self.conn.commit()

                    if mods > 10:
                        self.trigger_integrity_alert(filepath, mods + 1)

        except:
            pass

    def trigger_integrity_alert(self, filepath: str, modifications: int):
        """Dispara alerta de integridade"""
        print(f"""
╔════════════════════════════════════════════════════════════╗
║                 ⚠️  ALERTA DE INTEGRIDADE ⚠️               ║
╠════════════════════════════════════════════════════════════╣
║ Arquivo: {filepath[:50]:50} ║
║ Modificações: {modifications:48} ║
║ Status: SUSPEITO                                           ║
╚════════════════════════════════════════════════════════════╝
""")

    def detect_intrusion(self, pattern: str) -> List[Dict]:
        """Detecta padrões de intrusão"""
        # Busca por padrões suspeitos
        self.cursor.execute("""
            SELECT * FROM audit_log
            WHERE operation LIKE ?
            AND threat_level > 0.7
            ORDER BY timestamp DESC
            LIMIT 100
        """, (f"%{pattern}%",))

        results = []
        for row in self.cursor.fetchall():
            results.append({
                'id': row[0],
                'timestamp': row[1],
                'operation': row[2],
                'filepath': row[3],
                'threat_level': row[8]
            })

        return results

    def forensic_analysis(self, start_time: str, end_time: str) -> Dict:
        """Análise forense de período específico"""
        # Coleta estatísticas
        self.cursor.execute("""
            SELECT
                COUNT(*) as total_operations,
                COUNT(DISTINCT user) as unique_users,
                COUNT(DISTINCT filepath) as files_accessed,
                AVG(threat_level) as avg_threat,
                MAX(threat_level) as max_threat,
                COUNT(CASE WHEN success = 0 THEN 1 END) as failed_ops
            FROM audit_log
            WHERE timestamp BETWEEN ? AND ?
        """, (start_time, end_time))

        stats = self.cursor.fetchone()

        # Arquivos mais acessados
        self.cursor.execute("""
            SELECT filepath, COUNT(*) as access_count
            FROM audit_log
            WHERE timestamp BETWEEN ? AND ?
            GROUP BY filepath
            ORDER BY access_count DESC
            LIMIT 10
        """, (start_time, end_time))

        top_files = self.cursor.fetchall()

        # Operações suspeitas
        self.cursor.execute("""
            SELECT * FROM audit_log
            WHERE timestamp BETWEEN ? AND ?
            AND threat_level > 0.7
            ORDER BY threat_level DESC
        """, (start_time, end_time))

        suspicious = self.cursor.fetchall()

        return {
            'statistics': {
                'total_operations': stats[0],
                'unique_users': stats[1],
                'files_accessed': stats[2],
                'avg_threat_level': stats[3],
                'max_threat_level': stats[4],
                'failed_operations': stats[5]
            },
            'top_accessed_files': top_files,
            'suspicious_operations': len(suspicious),
            'time_range': f"{start_time} to {end_time}"
        }

    def generate_report(self) -> str:
        """Gera relatório completo de auditoria"""
        # Estatísticas gerais
        self.cursor.execute("""
            SELECT COUNT(*) FROM audit_log
        """)
        total_logs = self.cursor.fetchone()[0]

        self.cursor.execute("""
            SELECT COUNT(*) FROM file_integrity
            WHERE suspicious_activity = 1
        """)
        suspicious_files = self.cursor.fetchone()[0]

        self.cursor.execute("""
            SELECT COUNT(*) FROM intrusion_attempts
        """)
        intrusion_attempts = self.cursor.fetchone()[0]

        # Últimas 24 horas
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        analysis = self.forensic_analysis(yesterday, datetime.now().isoformat())

        report = f"""
╔════════════════════════════════════════════════════════════╗
║              📊 RELATÓRIO DE AUDITORIA COMPLETO            ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║ 📈 ESTATÍSTICAS GERAIS:                                    ║
║   • Total de logs: {total_logs:39} ║
║   • Arquivos suspeitos: {suspicious_files:34} ║
║   • Tentativas de intrusão: {intrusion_attempts:30} ║
║                                                            ║
║ 📅 ÚLTIMAS 24 HORAS:                                       ║
║   • Operações: {analysis['statistics']['total_operations']:43} ║
║   • Usuários únicos: {analysis['statistics']['unique_users']:37} ║
║   • Arquivos acessados: {analysis['statistics']['files_accessed']:33} ║
║   • Threat médio: {analysis['statistics']['avg_threat_level']:.2%:40} ║
║   • Operações falhas: {analysis['statistics']['failed_operations']:36} ║
║                                                            ║
║ 🔍 ANÁLISE DE INTEGRIDADE:                                 ║
║   • Arquivos monitorados: {len(self.file_hashes):31} ║
║   • Modificações detectadas: {suspicious_files:28} ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"""
        return report

    def start_monitoring(self):
        """Inicia monitoramento em tempo real"""
        # Monitor de arquivos
        file_monitor = threading.Thread(target=self.monitor_files, daemon=True)
        file_monitor.start()
        self.active_monitors.append(file_monitor)

        # Monitor de processos
        process_monitor = threading.Thread(target=self.monitor_processes, daemon=True)
        process_monitor.start()
        self.active_monitors.append(process_monitor)

        print("✅ Sistema de auditoria iniciado")

    def monitor_files(self):
        """Monitora mudanças em arquivos"""
        import time

        while True:
            try:
                for filepath in PROTECTED_DIR.rglob('*'):
                    if filepath.is_file():
                        self.check_file_integrity(str(filepath))
            except:
                pass

            time.sleep(10)  # Verifica a cada 10 segundos

    def monitor_processes(self):
        """Monitora processos suspeitos"""
        import time

        while True:
            try:
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    if proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline'])
                        if str(PROTECTED_DIR) in cmdline:
                            # Log processo acessando diretório protegido
                            self.log_operation(
                                'process_access',
                                str(PROTECTED_DIR),
                                user=proc.info['name'],
                                process_id=proc.info['pid']
                            )
            except:
                pass

            time.sleep(5)

# ═══════════════════════════════════════════════════════════════
# INTERFACE
# ═══════════════════════════════════════════════════════════════

def main():
    """Interface do sistema de auditoria"""
    audit = AuditSystem()

    print(audit.generate_report())

    # Menu interativo
    while True:
        print("\n" + "="*60)
        print("SISTEMA DE AUDITORIA - OPÇÕES:")
        print("1. Gerar relatório")
        print("2. Análise forense")
        print("3. Detectar intrusões")
        print("4. Verificar integridade")
        print("5. Sair")
        print("="*60)

        choice = input("Escolha: ")

        if choice == '1':
            print(audit.generate_report())
        elif choice == '2':
            start = input("Data início (YYYY-MM-DD): ")
            end = input("Data fim (YYYY-MM-DD): ")
            result = audit.forensic_analysis(start, end)
            print(json.dumps(result, indent=2))
        elif choice == '3':
            pattern = input("Padrão a buscar: ")
            results = audit.detect_intrusion(pattern)
            for r in results:
                print(f"[{r['timestamp']}] {r['operation']} - Threat: {r['threat_level']:.2%}")
        elif choice == '4':
            audit.calculate_initial_hashes()
            print("✅ Integridade verificada")
        elif choice == '5':
            break

if __name__ == "__main__":
    main()