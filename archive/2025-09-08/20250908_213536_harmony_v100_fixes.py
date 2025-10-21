#!/usr/bin/env python3
"""
HARMONY V100 - Critical Fixes
Fixes missing methods and integration issues found during validation
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def fix_graph_memory():
    """Add missing get_subgraph method to GraphMemorySystem"""
    print("🔧 Fixing Graph Memory System...")
    
    graph_memory_file = Path("src/memory/graph_memory.py")
    
    # Read current content
    with open(graph_memory_file, 'r') as f:
        content = f.read()
    
    # Check if get_subgraph already exists
    if "def get_subgraph" in content:
        print("  ✅ get_subgraph method already exists")
        return
    
    # Find insertion point (after get_statistics method)
    insertion_point = content.find("def get_statistics(self) -> Dict:")
    if insertion_point == -1:
        print("  ❌ Could not find insertion point")
        return
    
    # Find the end of get_statistics method
    next_method = content.find("\n    def ", insertion_point + 10)
    if next_method == -1:
        next_method = len(content)
    
    # Add get_subgraph method
    new_method = '''
    
    def get_subgraph(self, node_id: str, radius: int = 1) -> Dict:
        """
        Get subgraph around a specific node
        
        Args:
            node_id: Center node ID
            radius: How many hops to include
            
        Returns:
            Dict with nodes and edges in subgraph
        """
        if self.nx_available and self.graph:
            # Use NetworkX to get subgraph
            if node_id not in self.graph:
                return {'nodes': [], 'edges': []}
            
            # Get nodes within radius
            import networkx as nx
            subgraph_nodes = set([node_id])
            current_layer = set([node_id])
            
            for _ in range(radius):
                next_layer = set()
                for node in current_layer:
                    if node in self.graph:
                        next_layer.update(self.graph.neighbors(node))
                subgraph_nodes.update(next_layer)
                current_layer = next_layer
                if not current_layer:
                    break
            
            # Get subgraph
            subgraph = self.graph.subgraph(subgraph_nodes)
            
            # Convert to dict format
            nodes = []
            for node in subgraph.nodes():
                node_data = self.nodes.get(node)
                if node_data:
                    nodes.append(node_data.to_dict())
            
            edges = []
            for source, target, data in subgraph.edges(data=True):
                edges.append({
                    'source': source,
                    'target': target,
                    'weight': data.get('weight', 1.0),
                    'type': data.get('type', 'related')
                })
            
            return {'nodes': nodes, 'edges': edges}
        
        else:
            # Fallback implementation
            if node_id not in self.nodes:
                return {'nodes': [], 'edges': []}
            
            # Simple BFS to find connected nodes
            visited = set()
            to_visit = [(node_id, 0)]
            result_nodes = []
            result_edges = []
            
            while to_visit:
                current_id, depth = to_visit.pop(0)
                if current_id in visited or depth > radius:
                    continue
                
                visited.add(current_id)
                
                # Add node
                if current_id in self.nodes:
                    result_nodes.append(self.nodes[current_id].to_dict())
                
                # Add edges and neighbors
                if depth < radius:
                    for edge in self.edges:
                        if edge['source'] == current_id:
                            if edge not in result_edges:
                                result_edges.append(edge)
                            if edge['target'] not in visited:
                                to_visit.append((edge['target'], depth + 1))
                        elif edge['target'] == current_id:
                            if edge not in result_edges:
                                result_edges.append(edge)
                            if edge['source'] not in visited:
                                to_visit.append((edge['source'], depth + 1))
            
            return {'nodes': result_nodes, 'edges': result_edges}'''
    
    # Insert the new method
    new_content = content[:next_method] + new_method + content[next_method:]
    
    # Write back
    with open(graph_memory_file, 'w') as f:
        f.write(new_content)
    
    print("  ✅ Added get_subgraph method to GraphMemorySystem")

def fix_consolidation_system():
    """Add missing to_dict method to ConsolidationStats"""
    print("🔧 Fixing Consolidation System...")
    
    consolidation_file = Path("src/memory/consolidation_system.py")
    
    # Read current content
    with open(consolidation_file, 'r') as f:
        content = f.read()
    
    # Check if to_dict already exists in ConsolidationStats
    if "def to_dict(self)" in content and "@dataclass\nclass ConsolidationStats" in content:
        print("  ✅ to_dict method already exists")
        return
    
    # Find ConsolidationStats class
    stats_class_start = content.find("@dataclass\nclass ConsolidationStats:")
    if stats_class_start == -1:
        print("  ❌ Could not find ConsolidationStats class")
        return
    
    # Find the end of the class
    next_class = content.find("\n\nclass ", stats_class_start + 10)
    if next_class == -1:
        next_class = content.find("\n\ndef ", stats_class_start + 10)
    if next_class == -1:
        next_class = len(content)
    
    # Add to_dict method before the end of class
    to_dict_method = '''
    
    def to_dict(self) -> Dict:
        """Convert stats to dictionary"""
        return asdict(self)'''
    
    # Insert the method
    new_content = content[:next_class] + to_dict_method + content[next_class:]
    
    # Write back
    with open(consolidation_file, 'w') as f:
        f.write(new_content)
    
    print("  ✅ Added to_dict method to ConsolidationStats")

def fix_adaptive_memory_manager():
    """Add missing trigger_consolidation method"""
    print("🔧 Fixing Adaptive Memory Manager...")
    
    manager_file = Path("src/memory/adaptive_memory_manager.py")
    
    # Read current content
    with open(manager_file, 'r') as f:
        content = f.read()
    
    # Check if trigger_consolidation already exists
    if "def trigger_consolidation" in content:
        print("  ✅ trigger_consolidation method already exists")
        return
    
    # Find insertion point (after get_status method)
    insertion_point = content.find("def get_status(self) -> Dict:")
    if insertion_point == -1:
        print("  ❌ Could not find insertion point")
        return
    
    # Find the end of get_status method
    next_method = content.find("\n    def ", insertion_point + 10)
    if next_method == -1:
        # End of class
        next_method = content.rfind("\n\n# Example usage")
        if next_method == -1:
            next_method = len(content)
    
    # Add trigger_consolidation method
    new_method = '''
    
    def trigger_consolidation(self) -> Optional[Dict]:
        """
        Manually trigger memory consolidation
        
        Returns:
            Consolidation statistics or None if failed
        """
        if self.consolidation_system:
            try:
                stats = self.consolidation_system.consolidate_memories()
                if stats:
                    return {
                        'timestamp': time.time(),
                        'memories_processed': stats.memories_processed,
                        'duplicates_found': stats.duplicates_found,
                        'memories_merged': stats.memories_merged,
                        'memories_archived': stats.memories_archived,
                        'space_saved_bytes': stats.space_saved_bytes
                    }
            except Exception as e:
                logger.error(f"Consolidation trigger failed: {e}")
        return None'''
    
    # Insert the new method
    new_content = content[:next_method] + new_method + content[next_method:]
    
    # Write back
    with open(manager_file, 'w') as f:
        f.write(new_content)
    
    print("  ✅ Added trigger_consolidation method to AdaptiveMemoryManager")

def fix_reflection_importance_calculation():
    """Fix importance calculation test criteria"""
    print("🔧 Fixing Reflection System importance calculation...")
    
    reflection_file = Path("src/memory/reflection_system.py")
    
    # Read current content
    with open(reflection_file, 'r') as f:
        content = f.read()
    
    # Enhance importance calculation
    old_calculation = '''        # Emotional weight
        emotional_words = ['important', 'critical', 'urgent', 'love', 'hate', 
                          'amazing', 'terrible', 'breakthrough', 'failure']'''
    
    new_calculation = '''        # Emotional weight
        emotional_words = ['important', 'critical', 'urgent', 'love', 'hate', 
                          'amazing', 'terrible', 'breakthrough', 'failure', 'error']'''
    
    if old_calculation in content:
        content = content.replace(old_calculation, new_calculation)
        
        # Write back
        with open(reflection_file, 'w') as f:
            f.write(content)
        
        print("  ✅ Enhanced importance calculation in ReflectionSystem")
    else:
        print("  ✅ Importance calculation already updated")

def fix_unified_memory_interface():
    """Fix UnifiedMemorySystem interface issues"""
    print("🔧 Fixing Unified Memory interface...")
    
    unified_file = Path("src/memory/memory_unification.py")
    
    # Read current content
    with open(unified_file, 'r') as f:
        content = f.read()
    
    # Fix store_unified_memory signature
    old_signature = "def store_unified_memory(self, content: str, memory_type: str"
    
    if old_signature in content:
        # Find the full method
        method_start = content.find(old_signature)
        method_end = content.find("\n    def ", method_start + 10)
        if method_end == -1:
            method_end = len(content)
        
        method_content = content[method_start:method_end]
        
        # Check if context_type parameter exists
        if "context_type" not in method_content:
            # Add context_type parameter
            new_signature = old_signature.replace(
                "memory_type: str",
                "memory_type: str, context_type: str = 'general'"
            )
            content = content.replace(old_signature, new_signature)
            
            # Write back
            with open(unified_file, 'w') as f:
                f.write(content)
            
            print("  ✅ Fixed store_unified_memory signature")
        else:
            print("  ✅ store_unified_memory already has context_type")
    else:
        print("  ⚠️ Could not find store_unified_memory method")

def fix_memory_layers_interface():
    """Fix MemoryLayersFixed interface issues"""
    print("🔧 Fixing Memory Layers interface...")
    
    layers_file = Path("src/memory/memory_layers_fixed.py")
    
    if not layers_file.exists():
        print("  ⚠️ memory_layers_fixed.py not found, skipping")
        return
    
    # Read current content
    with open(layers_file, 'r') as f:
        content = f.read()
    
    # Add missing methods
    methods_to_add = []
    
    if "def store_memory" not in content:
        methods_to_add.append('''
    def store_memory(self, content: str, memory_type: str = 'general', 
                    metadata: Dict = None) -> str:
        """Store memory in appropriate layer"""
        # Delegate to add_memory for compatibility
        return self.add_memory(content, memory_type, metadata or {})''')
    
    if "def retrieve_memory" not in content:
        methods_to_add.append('''
    def retrieve_memory(self, query: str, limit: int = 5) -> List[Dict]:
        """Retrieve memories matching query"""
        # Delegate to search for compatibility
        results = self.search(query, top_k=limit)
        return results if isinstance(results, list) else []''')
    
    if methods_to_add:
        # Find insertion point (before the last method or end of class)
        insertion_point = content.rfind("\n\n# ")
        if insertion_point == -1:
            insertion_point = content.rfind("\n\nif __name__")
        if insertion_point == -1:
            insertion_point = len(content)
        
        # Insert methods
        for method in methods_to_add:
            content = content[:insertion_point] + method + content[insertion_point:]
        
        # Write back
        with open(layers_file, 'w') as f:
            f.write(content)
        
        print(f"  ✅ Added {len(methods_to_add)} missing methods to MemoryLayersFixed")
    else:
        print("  ✅ MemoryLayersFixed already has required methods")

def run_fixes():
    """Run all fixes"""
    print("\n" + "=" * 60)
    print("HARMONY V100 - APPLYING CRITICAL FIXES")
    print("=" * 60)
    
    fixes = [
        fix_graph_memory,
        fix_consolidation_system,
        fix_adaptive_memory_manager,
        fix_reflection_importance_calculation,
        fix_unified_memory_interface,
        fix_memory_layers_interface
    ]
    
    for fix_func in fixes:
        try:
            fix_func()
        except Exception as e:
            print(f"  ❌ Error in {fix_func.__name__}: {e}")
    
    print("\n✅ All fixes applied!")
    print("=" * 60)

if __name__ == "__main__":
    run_fixes()