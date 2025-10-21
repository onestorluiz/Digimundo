#!/usr/bin/env python3
"""
SQLite Hardening - Apply PRAGMAs and create indexes
"""
import json
import sqlite3
from pathlib import Path
from datetime import datetime

def harden_database(db_path: Path) -> dict:
    """Apply hardening to a SQLite database"""
    results = {
        "database": str(db_path),
        "pragmas_applied": [],
        "indexes_created": [],
        "integrity": "unknown",
        "errors": []
    }
    
    if not db_path.exists():
        results["errors"].append(f"Database not found: {db_path}")
        return results
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Apply PRAGMAs
        pragmas = [
            "PRAGMA journal_mode=WAL",
            "PRAGMA synchronous=NORMAL",
            "PRAGMA foreign_keys=ON"
        ]
        
        for pragma in pragmas:
            try:
                cursor.execute(pragma)
                results["pragmas_applied"].append(pragma)
            except Exception as e:
                results["errors"].append(f"Failed {pragma}: {str(e)}")
        
        # Create indexes if not exist
        indexes = [
            ("idx_kind", "unified_memories", "kind"),
            ("idx_last_accessed", "unified_memories", "last_accessed"),
            ("idx_created_at", "unified_memories", "timestamp"),
            ("idx_hits", "unified_memories", "hits")
        ]
        
        for idx_name, table, column in indexes:
            try:
                # Check if index exists
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='index' AND name=?",
                    (idx_name,)
                )
                if not cursor.fetchone():
                    cursor.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table}({column})")
                    results["indexes_created"].append(idx_name)
            except Exception as e:
                # Table might not exist or column missing
                pass
        
        # Check integrity
        cursor.execute("PRAGMA integrity_check")
        integrity_result = cursor.fetchone()
        if integrity_result and integrity_result[0] == "ok":
            results["integrity"] = "ok"
        else:
            results["integrity"] = "warn"
            results["errors"].append(f"Integrity check: {integrity_result}")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        results["errors"].append(f"Database error: {str(e)}")
        results["integrity"] = "fail"
    
    return results

def main():
    """Harden all SQLite databases in the project"""
    project_root = Path("/Users/clubproducoes/Digimundo/scripturemon-validation")
    
    # Find all SQLite databases
    db_paths = [
        project_root / "runtime" / "unified_memory.db",
        project_root / "runtime" / "crystal_memory" / "memories.db",
        project_root / "runtime" / "cache" / "l3_cache.db",
        project_root / "CINEMA_KNOWLEDGE" / "03_METADATA" / "cinema_knowledge.db"
    ]
    
    all_results = {
        "timestamp": datetime.now().isoformat(),
        "databases": [],
        "pragmas_applied": True,
        "indexes": [],
        "integrity": "ok"
    }
    
    for db_path in db_paths:
        if db_path.exists():
            print(f"Hardening {db_path.name}...")
            result = harden_database(db_path)
            all_results["databases"].append(result)
            
            # Aggregate results
            all_results["indexes"].extend(result["indexes_created"])
            if result["integrity"] != "ok":
                all_results["integrity"] = result["integrity"]
            if result["errors"]:
                all_results["pragmas_applied"] = False
    
    # Save report
    output_dir = project_root / "reports" / "integrate_align_v32"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "sqlite_hardening.json", 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"✅ SQLite hardening complete")
    print(f"  Databases: {len(all_results['databases'])}")
    print(f"  Indexes: {len(all_results['indexes'])}")
    print(f"  Integrity: {all_results['integrity']}")
    
    return all_results["integrity"] == "ok"

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)