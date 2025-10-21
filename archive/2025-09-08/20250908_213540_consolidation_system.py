#!/usr/bin/env python3
"""
Memory Consolidation System - Cleanup and compression of memory stores
Periodically consolidates, merges, and archives memories for efficiency
"""

import json
import time
import logging
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
import hashlib
# numpy removed - not needed for basic functionality
from collections import defaultdict
import threading

logger = logging.getLogger(__name__)

@dataclass
class ConsolidationStats:
    """Statistics from a consolidation run"""
    timestamp: float
    memories_processed: int
    memories_merged: int
    memories_archived: int
    memories_deleted: int
    duplicates_found: int
    clusters_created: int
    space_saved_bytes: int
    duration_seconds: float
    
    def to_dict(self) -> Dict:
        """Convert stats to dictionary"""
        return asdict(self)

class MemoryConsolidationSystem:
    """
    System for periodic memory consolidation and cleanup
    """
    
    def __init__(self,
                 db_path: Path = None,
                 vector_store = None,
                 consolidation_interval: int = 3600,  # 1 hour
                 age_threshold_days: int = 7,
                 importance_threshold: float = 3.0,
                 similarity_threshold: float = 0.85):
        """
        Initialize consolidation system
        
        Args:
            db_path: Path to SQLite database
            vector_store: Vector store instance (e.g., ChromaDB)
            consolidation_interval: Seconds between consolidation runs
            age_threshold_days: Days before memory becomes candidate for consolidation
            importance_threshold: Min importance to keep old memories
            similarity_threshold: Similarity threshold for merging
        """
        self.db_path = db_path or Path("./data/memory/consolidated.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.vector_store = vector_store
        self.consolidation_interval = consolidation_interval
        self.age_threshold = timedelta(days=age_threshold_days)
        self.importance_threshold = importance_threshold
        self.similarity_threshold = similarity_threshold
        
        # Statistics
        self.stats_history: List[ConsolidationStats] = []
        
        # Threading
        self.consolidation_thread = None
        self.running = False
        
        # Initialize database
        self._init_database()
        
        logger.info(f"Consolidation system initialized (interval={consolidation_interval}s)")
    
    def _init_database(self):
        """Initialize SQLite database for consolidated memories"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Main memories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                summary TEXT,
                timestamp REAL NOT NULL,
                importance REAL DEFAULT 5.0,
                access_count INTEGER DEFAULT 0,
                last_accessed REAL,
                is_consolidated BOOLEAN DEFAULT 0,
                original_ids TEXT,  -- JSON array of original memory IDs if merged
                metadata TEXT  -- JSON metadata
            )
        ''')
        
        # Consolidation runs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consolidation_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                stats TEXT NOT NULL  -- JSON stats
            )
        ''')
        
        # Create indices
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_consolidated ON memories(is_consolidated)')
        
        conn.commit()
        conn.close()
    
    def start_periodic_consolidation(self):
        """Start background thread for periodic consolidation"""
        if self.running:
            logger.warning("Consolidation already running")
            return
        
        self.running = True
        self.consolidation_thread = threading.Thread(
            target=self._consolidation_loop,
            daemon=True
        )
        self.consolidation_thread.start()
        logger.info("Started periodic consolidation thread")
    
    def stop_periodic_consolidation(self):
        """Stop consolidation thread"""
        self.running = False
        if self.consolidation_thread:
            self.consolidation_thread.join(timeout=5)
        logger.info("Stopped periodic consolidation")
    
    def _consolidation_loop(self):
        """Background loop for periodic consolidation"""
        while self.running:
            try:
                # Run consolidation
                stats = self.consolidate_memories()
                logger.info(f"Consolidation complete: {stats.memories_merged} merged, "
                          f"{stats.memories_deleted} deleted")
                
                # Wait for next interval
                time.sleep(self.consolidation_interval)
                
            except Exception as e:
                logger.error(f"Consolidation error: {e}")
                time.sleep(60)  # Wait a minute before retry
    
    def consolidate_memories(self) -> ConsolidationStats:
        """
        Main consolidation routine
        
        Performs:
        1. Duplicate detection and merging
        2. Clustering similar memories
        3. Archiving old, low-importance memories
        4. Summarizing memory clusters
        5. Cleanup of redundant data
        """
        start_time = time.time()
        stats = ConsolidationStats(
            timestamp=start_time,
            memories_processed=0,
            memories_merged=0,
            memories_archived=0,
            memories_deleted=0,
            duplicates_found=0,
            clusters_created=0,
            space_saved_bytes=0,
            duration_seconds=0
        )
        
        logger.info("Starting memory consolidation...")
        
        # Get all memories from database
        memories = self._load_memories_for_consolidation()
        stats.memories_processed = len(memories)
        
        if not memories:
            logger.info("No memories to consolidate")
            return stats
        
        # Step 1: Find and merge duplicates
        duplicates = self._find_duplicates(memories)
        stats.duplicates_found = len(duplicates)
        
        for duplicate_group in duplicates:
            merged = self._merge_memories(duplicate_group)
            if merged:
                stats.memories_merged += len(duplicate_group) - 1
        
        # Step 2: Cluster similar memories
        clusters = self._cluster_similar_memories(memories)
        stats.clusters_created = len(clusters)
        
        for cluster in clusters:
            if len(cluster) > 3:  # Only consolidate larger clusters
                summary = self._create_cluster_summary(cluster)
                if summary:
                    # Archive individual memories and keep summary
                    self._archive_memories(cluster[1:])  # Keep first, archive rest
                    stats.memories_archived += len(cluster) - 1
        
        # Step 3: Delete old, low-importance memories
        deleted = self._cleanup_old_memories()
        stats.memories_deleted = deleted
        
        # Step 4: Compress vector store if available
        if self.vector_store:
            self._compress_vector_store()
        
        # Calculate space saved (approximate)
        stats.space_saved_bytes = (stats.memories_merged + stats.memories_deleted) * 1000  # Rough estimate
        
        # Record stats
        stats.duration_seconds = time.time() - start_time
        self._save_consolidation_stats(stats)
        self.stats_history.append(stats)
        
        logger.info(f"Consolidation complete in {stats.duration_seconds:.2f}s")
        
        return stats
    
    def _load_memories_for_consolidation(self) -> List[Dict]:
        """Load memories that are candidates for consolidation"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Get memories older than threshold
        cutoff_time = time.time() - self.age_threshold.total_seconds()
        
        cursor.execute('''
            SELECT id, content, summary, timestamp, importance, 
                   access_count, last_accessed, is_consolidated, metadata
            FROM memories
            WHERE timestamp < ? AND is_consolidated = 0
            ORDER BY importance ASC, timestamp ASC
            LIMIT 1000
        ''', (cutoff_time,))
        
        memories = []
        for row in cursor.fetchall():
            memories.append({
                'id': row[0],
                'content': row[1],
                'summary': row[2],
                'timestamp': row[3],
                'importance': row[4],
                'access_count': row[5],
                'last_accessed': row[6],
                'is_consolidated': row[7],
                'metadata': json.loads(row[8]) if row[8] else {}
            })
        
        conn.close()
        return memories
    
    def _find_duplicates(self, memories: List[Dict]) -> List[List[Dict]]:
        """Find duplicate or near-duplicate memories"""
        duplicates = []
        seen = set()
        
        # Create content hashes for exact duplicates
        hash_groups = defaultdict(list)
        for memory in memories:
            content_hash = hashlib.md5(memory['content'].lower().strip().encode()).hexdigest()
            hash_groups[content_hash].append(memory)
        
        # Group exact duplicates
        for hash_val, group in hash_groups.items():
            if len(group) > 1 and hash_val not in seen:
                duplicates.append(group)
                seen.add(hash_val)
        
        return duplicates
    
    def _merge_memories(self, memories: List[Dict]) -> Optional[Dict]:
        """Merge duplicate memories into one"""
        if not memories:
            return None
        
        # Sort by importance and recency
        memories.sort(key=lambda x: (x['importance'], x['timestamp']), reverse=True)
        
        # Take the best memory as base
        merged = memories[0].copy()
        
        # Aggregate statistics
        merged['access_count'] = sum(m['access_count'] for m in memories)
        merged['importance'] = max(m['importance'] for m in memories)
        merged['last_accessed'] = max(m.get('last_accessed', 0) for m in memories)
        
        # Store original IDs
        original_ids = []
        for m in memories:
            if 'original_ids' in m and m['original_ids']:
                original_ids.extend(json.loads(m['original_ids']))
            else:
                original_ids.append(m['id'])
        merged['original_ids'] = json.dumps(original_ids)
        
        # Update in database
        self._update_memory(merged)
        
        # Delete duplicates
        for memory in memories[1:]:
            self._delete_memory(memory['id'])
        
        return merged
    
    def _cluster_similar_memories(self, memories: List[Dict]) -> List[List[Dict]]:
        """Cluster similar memories using simple similarity metric"""
        if not memories or not self.vector_store:
            return []
        
        clusters = []
        clustered = set()
        
        # Simple clustering (can be enhanced with proper algorithms)
        for i, memory in enumerate(memories):
            if memory['id'] in clustered:
                continue
            
            cluster = [memory]
            clustered.add(memory['id'])
            
            # Find similar memories
            for j, other in enumerate(memories[i+1:], i+1):
                if other['id'] in clustered:
                    continue
                
                # Calculate similarity (simplified)
                similarity = self._calculate_similarity(memory, other)
                
                if similarity >= self.similarity_threshold:
                    cluster.append(other)
                    clustered.add(other['id'])
            
            if len(cluster) > 1:
                clusters.append(cluster)
        
        return clusters
    
    def _calculate_similarity(self, memory1: Dict, memory2: Dict) -> float:
        """Calculate similarity between two memories"""
        # Simple Jaccard similarity on words
        words1 = set(memory1['content'].lower().split())
        words2 = set(memory2['content'].lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0
    
    def _create_cluster_summary(self, cluster: List[Dict]) -> Optional[str]:
        """Create a summary for a cluster of memories"""
        if not cluster:
            return None
        
        # Simple summary: combine key points
        contents = [m['content'] for m in cluster]
        
        # Find common words (simple approach)
        word_freq = defaultdict(int)
        for content in contents:
            for word in content.lower().split():
                if len(word) > 4:  # Skip short words
                    word_freq[word] += 1
        
        # Get most common words
        common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Create summary
        summary = f"Cluster of {len(cluster)} related memories. "
        summary += f"Key topics: {', '.join(word for word, _ in common_words[:5])}. "
        summary += f"Time span: {self._format_timespan(cluster)}. "
        summary += f"Average importance: {sum(m['importance'] for m in cluster) / len(cluster):.1f}"
        
        # Store summary as new consolidated memory
        consolidated = {
            'id': hashlib.md5(summary.encode()).hexdigest()[:16],
            'content': summary,
            'summary': f"Consolidated from {len(cluster)} memories",
            'timestamp': time.time(),
            'importance': max(m['importance'] for m in cluster),
            'is_consolidated': True,
            'original_ids': json.dumps([m['id'] for m in cluster]),
            'metadata': {
                'type': 'cluster_summary',
                'cluster_size': len(cluster),
                'topics': [word for word, _ in common_words[:5]]
            }
        }
        
        self._save_memory(consolidated)
        
        return summary
    
    def _format_timespan(self, memories: List[Dict]) -> str:
        """Format time span of memories"""
        if not memories:
            return "unknown"
        
        timestamps = [m['timestamp'] for m in memories]
        min_time = datetime.fromtimestamp(min(timestamps))
        max_time = datetime.fromtimestamp(max(timestamps))
        
        delta = max_time - min_time
        
        if delta.days > 0:
            return f"{delta.days} days"
        elif delta.seconds > 3600:
            return f"{delta.seconds // 3600} hours"
        else:
            return f"{delta.seconds // 60} minutes"
    
    def _archive_memories(self, memories: List[Dict]):
        """Archive memories (mark as consolidated)"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        for memory in memories:
            cursor.execute('''
                UPDATE memories 
                SET is_consolidated = 1 
                WHERE id = ?
            ''', (memory['id'],))
        
        conn.commit()
        conn.close()
    
    def _cleanup_old_memories(self) -> int:
        """Delete old, low-importance memories"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Delete old, low importance, rarely accessed memories
        cutoff_time = time.time() - (self.age_threshold.total_seconds() * 4)  # 4x age threshold
        
        cursor.execute('''
            DELETE FROM memories
            WHERE timestamp < ? 
            AND importance < ?
            AND access_count < 2
            AND is_consolidated = 0
        ''', (cutoff_time, self.importance_threshold))
        
        deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def _compress_vector_store(self):
        """Compress vector store by removing redundant embeddings"""
        if not self.vector_store:
            return
        
        try:
            # This would interface with your vector store
            # Example for ChromaDB:
            # self.vector_store.cleanup_duplicates()
            # self.vector_store.optimize_index()
            pass
        except Exception as e:
            logger.error(f"Failed to compress vector store: {e}")
    
    def _save_memory(self, memory: Dict):
        """Save or update a memory"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO memories 
            (id, content, summary, timestamp, importance, access_count, 
             last_accessed, is_consolidated, original_ids, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory['id'],
            memory['content'],
            memory.get('summary'),
            memory['timestamp'],
            memory.get('importance', 5.0),
            memory.get('access_count', 0),
            memory.get('last_accessed'),
            memory.get('is_consolidated', False),
            memory.get('original_ids'),
            json.dumps(memory.get('metadata', {}))
        ))
        
        conn.commit()
        conn.close()
    
    def _update_memory(self, memory: Dict):
        """Update existing memory"""
        self._save_memory(memory)
    
    def _delete_memory(self, memory_id: str):
        """Delete a memory"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM memories WHERE id = ?', (memory_id,))
        
        conn.commit()
        conn.close()
    
    def _save_consolidation_stats(self, stats: ConsolidationStats):
        """Save consolidation run statistics"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO consolidation_runs (timestamp, stats)
            VALUES (?, ?)
        ''', (stats.timestamp, json.dumps(asdict(stats))))
        
        conn.commit()
        conn.close()
    
    def get_consolidation_history(self, limit: int = 10) -> List[ConsolidationStats]:
        """Get recent consolidation history"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT stats FROM consolidation_runs
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        history = []
        for row in cursor.fetchall():
            stats_dict = json.loads(row[0])
            history.append(ConsolidationStats(**stats_dict))
        
        conn.close()
        
        return history

# Example usage
def demonstrate_consolidation():
    """Demonstrate the consolidation system"""
    print("🗜️ Memory Consolidation System Demonstration")
    print("=" * 60)
    
    # Initialize system
    consolidator = MemoryConsolidationSystem(
        age_threshold_days=0,  # For demo, consolidate immediately
        importance_threshold=4.0,
        similarity_threshold=0.7
    )
    
    # Add sample memories to database
    print("\n📝 Adding sample memories:")
    sample_memories = [
        # Duplicates
        ("Python is a great language", 8.0),
        ("Python is a great language", 8.0),  # Exact duplicate
        ("Python is an excellent language", 7.5),  # Near duplicate
        
        # Related memories (cluster)
        ("Machine learning uses Python", 6.0),
        ("Deep learning with Python and TensorFlow", 6.5),
        ("Neural networks in Python", 6.0),
        
        # Old, low importance
        ("Checked email", 2.0),
        ("Had coffee", 1.5),
        ("System startup complete", 3.0),
        
        # Important memory
        ("Critical bug found in authentication", 9.0)
    ]
    
    for i, (content, importance) in enumerate(sample_memories):
        memory = {
            'id': f"mem_{i:03d}",
            'content': content,
            'timestamp': time.time() - (86400 * (10 - i)),  # Varying ages
            'importance': importance,
            'access_count': i % 3,
            'metadata': {'demo': True}
        }
        consolidator._save_memory(memory)
        print(f"  Added: {content[:40]}... (importance={importance})")
    
    # Run consolidation
    print("\n🔄 Running consolidation...")
    stats = consolidator.consolidate_memories()
    
    # Display results
    print(f"\n📊 Consolidation Results:")
    print(f"  Memories processed: {stats.memories_processed}")
    print(f"  Duplicates found: {stats.duplicates_found}")
    print(f"  Memories merged: {stats.memories_merged}")
    print(f"  Memories archived: {stats.memories_archived}")
    print(f"  Memories deleted: {stats.memories_deleted}")
    print(f"  Clusters created: {stats.clusters_created}")
    print(f"  Space saved: ~{stats.space_saved_bytes} bytes")
    print(f"  Duration: {stats.duration_seconds:.3f} seconds")
    
    # Show remaining memories
    print("\n📚 Remaining memories after consolidation:")
    conn = sqlite3.connect(str(consolidator.db_path))
    cursor = conn.cursor()
    cursor.execute('''
        SELECT content, importance, is_consolidated 
        FROM memories 
        WHERE is_consolidated = 0
        ORDER BY importance DESC
    ''')
    
    for row in cursor.fetchall():
        print(f"  [{row[1]:.1f}] {row[0][:50]}...")
    
    conn.close()
    
    print("\n✨ Consolidation demonstration complete!")

if __name__ == "__main__":
    demonstrate_consolidation()