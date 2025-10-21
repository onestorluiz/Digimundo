#!/usr/bin/env python3
"""
Reflection System - Self-evaluation and insight generation
Implements importance scoring and automatic reflection triggers
"""

import json
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib
from collections import deque

logger = logging.getLogger(__name__)

@dataclass
class MemoryEvent:
    """Represents a memory event with importance scoring"""
    id: str
    content: str
    timestamp: float
    importance: float  # 1-10 scale
    event_type: str  # 'user_input', 'system_response', 'internal_thought', etc.
    tags: List[str]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class Reflection:
    """Represents a reflection/insight generated from memories"""
    id: str
    timestamp: float
    trigger_reason: str  # 'threshold', 'periodic', 'manual'
    memories_analyzed: int
    total_importance: float
    insight: str
    summary: str
    key_themes: List[str]
    action_items: List[str]
    
    def to_dict(self) -> Dict:
        return asdict(self)

class ReflectionSystem:
    """
    Advanced reflection system with importance scoring and insight generation
    """
    
    def __init__(self, 
                 storage_path: Path = None,
                 importance_threshold: float = 50.0,
                 window_size: int = 20,
                 reflection_interval: int = 3600):  # 1 hour
        """
        Initialize reflection system
        
        Args:
            storage_path: Path to store reflections
            importance_threshold: Sum threshold to trigger reflection
            window_size: Number of recent events to consider
            reflection_interval: Minimum seconds between reflections
        """
        self.storage_path = storage_path or Path("./data/reflections")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.importance_threshold = importance_threshold
        self.window_size = window_size
        self.reflection_interval = reflection_interval
        
        # Recent events queue
        self.recent_events = deque(maxlen=window_size)
        self.importance_sum = 0.0
        
        # Reflection storage
        self.reflections_file = self.storage_path / "reflections.json"
        self.reflections = self._load_reflections()
        
        # Last reflection time
        self.last_reflection_time = 0
        if self.reflections:
            self.last_reflection_time = max(r.timestamp for r in self.reflections)
        
        logger.info(f"Reflection system initialized (threshold={importance_threshold})")
    
    def _load_reflections(self) -> List[Reflection]:
        """Load existing reflections from disk"""
        if self.reflections_file.exists():
            try:
                with open(self.reflections_file, 'r') as f:
                    data = json.load(f)
                return [Reflection(**r) for r in data]
            except Exception as e:
                logger.error(f"Failed to load reflections: {e}")
        return []
    
    def _save_reflections(self):
        """Save reflections to disk"""
        try:
            with open(self.reflections_file, 'w') as f:
                json.dump([r.to_dict() for r in self.reflections], f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save reflections: {e}")
    
    def calculate_importance(self, 
                           content: str, 
                           event_type: str,
                           metadata: Dict[str, Any] = None) -> float:
        """
        Calculate importance score for an event
        
        Uses heuristics and can be enhanced with LLM scoring
        """
        importance = 5.0  # Base score
        
        # Adjust based on event type
        type_weights = {
            'user_query': 7.0,
            'system_error': 8.0,
            'learning': 9.0,
            'reflection': 10.0,
            'routine': 3.0,
            'system_response': 5.0,
            'internal_thought': 6.0
        }
        importance = type_weights.get(event_type, 5.0)
        
        # Adjust based on content characteristics
        content_lower = content.lower()
        
        # Emotional weight
        emotional_words = ['important', 'critical', 'urgent', 'love', 'hate', 
                          'amazing', 'terrible', 'breakthrough', 'failure', 'error']
        for word in emotional_words:
            if word in content_lower:
                importance += 1.0
        
        # Question detection
        if '?' in content:
            importance += 0.5
        
        # Length factor (longer = potentially more important)
        if len(content) > 500:
            importance += 1.0
        elif len(content) < 50:
            importance -= 0.5
        
        # Metadata factors
        if metadata:
            if metadata.get('user_requested'):
                importance += 2.0
            if metadata.get('error_count', 0) > 0:
                importance += 1.0
            if metadata.get('is_correction'):
                importance += 1.5
        
        # Clamp to 1-10 range
        return max(1.0, min(10.0, importance))
    
    def record_event(self, 
                    content: str,
                    event_type: str = 'general',
                    tags: List[str] = None,
                    metadata: Dict[str, Any] = None) -> MemoryEvent:
        """
        Record a new memory event with importance scoring
        """
        # Calculate importance
        importance = self.calculate_importance(content, event_type, metadata)
        
        # Create event
        event = MemoryEvent(
            id=hashlib.md5(f"{content}{time.time()}".encode()).hexdigest()[:12],
            content=content,
            timestamp=time.time(),
            importance=importance,
            event_type=event_type,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        # Add to recent events
        if len(self.recent_events) >= self.window_size:
            # Remove oldest event's importance
            oldest = self.recent_events[0]
            self.importance_sum -= oldest.importance
        
        self.recent_events.append(event)
        self.importance_sum += importance
        
        logger.debug(f"Event recorded: {event_type} (importance={importance:.1f}, sum={self.importance_sum:.1f})")
        
        # Check if reflection should trigger
        self._check_reflection_trigger()
        
        return event
    
    def _check_reflection_trigger(self) -> Optional[Reflection]:
        """Check if conditions warrant triggering a reflection"""
        current_time = time.time()
        
        # Check importance threshold
        if self.importance_sum >= self.importance_threshold:
            if current_time - self.last_reflection_time >= self.reflection_interval:
                logger.info(f"Triggering reflection: importance threshold reached ({self.importance_sum:.1f})")
                return self.trigger_reflection('threshold')
        
        # Check periodic trigger (every 24 hours regardless)
        if current_time - self.last_reflection_time >= 86400:  # 24 hours
            logger.info("Triggering periodic reflection")
            return self.trigger_reflection('periodic')
        
        return None
    
    def trigger_reflection(self, reason: str = 'manual') -> Reflection:
        """
        Trigger a reflection process
        
        Analyzes recent events and generates insights
        """
        logger.info(f"Generating reflection (reason={reason})")
        
        # Get recent important events
        events = list(self.recent_events)
        if not events:
            logger.warning("No events to reflect on")
            return None
        
        # Sort by importance
        important_events = sorted(events, key=lambda x: x.importance, reverse=True)[:10]
        
        # Generate summary
        summary = self._generate_summary(important_events)
        
        # Extract insights
        insight = self._generate_insight(important_events)
        
        # Identify themes
        themes = self._extract_themes(events)
        
        # Generate action items
        action_items = self._generate_action_items(important_events)
        
        # Create reflection
        reflection = Reflection(
            id=hashlib.md5(f"reflection_{time.time()}".encode()).hexdigest()[:12],
            timestamp=time.time(),
            trigger_reason=reason,
            memories_analyzed=len(events),
            total_importance=self.importance_sum,
            insight=insight,
            summary=summary,
            key_themes=themes,
            action_items=action_items
        )
        
        # Store reflection
        self.reflections.append(reflection)
        self._save_reflections()
        
        # Reset importance sum
        self.importance_sum = 0.0
        self.last_reflection_time = time.time()
        
        # Log reflection
        logger.info(f"Reflection generated: {reflection.id}")
        logger.info(f"  Insight: {insight[:100]}...")
        logger.info(f"  Themes: {', '.join(themes)}")
        logger.info(f"  Action items: {len(action_items)}")
        
        return reflection
    
    def _generate_summary(self, events: List[MemoryEvent]) -> str:
        """Generate a summary of events"""
        if not events:
            return "No significant events to summarize."
        
        # Group by event type
        by_type = {}
        for event in events:
            if event.event_type not in by_type:
                by_type[event.event_type] = []
            by_type[event.event_type].append(event)
        
        summary_parts = []
        for event_type, type_events in by_type.items():
            count = len(type_events)
            avg_importance = sum(e.importance for e in type_events) / count
            summary_parts.append(
                f"{count} {event_type} events (avg importance: {avg_importance:.1f})"
            )
        
        # Add most important event
        most_important = max(events, key=lambda x: x.importance)
        summary_parts.append(
            f"Most significant: {most_important.content[:100]}... (importance: {most_important.importance:.1f})"
        )
        
        return " | ".join(summary_parts)
    
    def _generate_insight(self, events: List[MemoryEvent]) -> str:
        """Generate an insight from events"""
        if not events:
            return "Insufficient data for insight generation."
        
        # Analyze patterns
        insights = []
        
        # Frequency pattern
        event_types = [e.event_type for e in events]
        most_common = max(set(event_types), key=event_types.count)
        insights.append(f"Primary focus has been on {most_common}")
        
        # Importance trend
        recent_importance = [e.importance for e in events[-5:]]
        if recent_importance:
            avg_recent = sum(recent_importance) / len(recent_importance)
            if avg_recent > 7:
                insights.append("Recent events show high significance")
            elif avg_recent < 4:
                insights.append("Recent activity has been routine")
        
        # Error detection
        error_events = [e for e in events if 'error' in e.event_type.lower() or 
                       (e.metadata and e.metadata.get('error_count', 0) > 0)]
        if error_events:
            insights.append(f"Encountered {len(error_events)} error-related events requiring attention")
        
        # Learning opportunities
        learning_events = [e for e in events if 'learning' in e.event_type.lower() or
                          'correction' in str(e.metadata)]
        if learning_events:
            insights.append(f"Identified {len(learning_events)} learning opportunities")
        
        return " | ".join(insights) if insights else "System operating normally with balanced activity."
    
    def _extract_themes(self, events: List[MemoryEvent]) -> List[str]:
        """Extract key themes from events"""
        themes = set()
        
        # Collect all tags
        for event in events:
            themes.update(event.tags)
        
        # Extract common words (simple approach)
        word_freq = {}
        for event in events:
            words = event.content.lower().split()
            for word in words:
                if len(word) > 5:  # Focus on longer words
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # Add top frequent words as themes
        if word_freq:
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            themes.update([word for word, _ in sorted_words[:3]])
        
        return list(themes)[:5]  # Limit to 5 themes
    
    def _generate_action_items(self, events: List[MemoryEvent]) -> List[str]:
        """Generate action items based on events"""
        action_items = []
        
        # Check for errors
        error_events = [e for e in events if 'error' in e.event_type.lower()]
        if error_events:
            action_items.append(f"Investigate and resolve {len(error_events)} errors")
        
        # Check for unanswered questions
        questions = [e for e in events if '?' in e.content and e.event_type == 'user_query']
        if questions:
            action_items.append(f"Review {len(questions)} user questions for completeness")
        
        # Check for high importance items
        critical = [e for e in events if e.importance >= 8]
        if critical:
            action_items.append(f"Priority review of {len(critical)} high-importance items")
        
        # Performance optimization
        if self.importance_sum > self.importance_threshold * 1.5:
            action_items.append("Consider system optimization due to high activity")
        
        return action_items
    
    def get_recent_reflections(self, count: int = 5) -> List[Reflection]:
        """Get most recent reflections"""
        return sorted(self.reflections, key=lambda x: x.timestamp, reverse=True)[:count]
    
    def get_insights_for_context(self) -> str:
        """Get recent insights formatted for LLM context"""
        recent = self.get_recent_reflections(3)
        if not recent:
            return "No reflections available yet."
        
        context_parts = []
        for reflection in recent:
            time_ago = (time.time() - reflection.timestamp) / 3600  # hours
            context_parts.append(
                f"[{time_ago:.1f}h ago] {reflection.insight} (Themes: {', '.join(reflection.key_themes)})"
            )
        
        return "\n".join(context_parts)

# Example usage and integration
def demonstrate_reflection_system():
    """Demonstrate the reflection system"""
    print("🧠 Reflection System Demonstration")
    print("=" * 60)
    
    # Initialize system
    reflection_system = ReflectionSystem(
        importance_threshold=30.0,  # Lower threshold for demo
        window_size=10
    )
    
    # Simulate various events
    events_to_simulate = [
        ("User asked about implementing a new feature", "user_query", ['feature', 'implementation']),
        ("System successfully generated code", "system_response", ['code', 'success']),
        ("Error: Failed to connect to database", "system_error", ['error', 'database']),
        ("Learning: User corrected my understanding", "learning", ['correction', 'improvement']),
        ("Routine status check completed", "routine", ['status']),
        ("User expressed frustration with response time", "user_query", ['performance', 'feedback']),
        ("Critical: Memory usage exceeding threshold", "system_error", ['memory', 'critical']),
        ("Successfully optimized query performance", "system_response", ['optimization', 'success']),
        ("User requested urgent bug fix", "user_query", ['urgent', 'bug']),
        ("Internal analysis: Pattern detected in errors", "internal_thought", ['analysis', 'pattern']),
    ]
    
    print("\n📝 Recording events:")
    for content, event_type, tags in events_to_simulate:
        event = reflection_system.record_event(
            content=content,
            event_type=event_type,
            tags=tags,
            metadata={'simulated': True}
        )
        print(f"  [{event.importance:.1f}] {event_type}: {content[:50]}...")
        time.sleep(0.1)  # Small delay for timestamp variation
    
    print(f"\n📊 Importance sum: {reflection_system.importance_sum:.1f}/{reflection_system.importance_threshold}")
    
    # Trigger manual reflection
    print("\n🔮 Triggering reflection:")
    reflection = reflection_system.trigger_reflection('demo')
    
    if reflection:
        print(f"\n📋 Reflection #{reflection.id}")
        print(f"  Trigger: {reflection.trigger_reason}")
        print(f"  Events analyzed: {reflection.memories_analyzed}")
        print(f"  Total importance: {reflection.total_importance:.1f}")
        print(f"\n  💡 Insight: {reflection.insight}")
        print(f"\n  📝 Summary: {reflection.summary}")
        print(f"\n  🏷️ Themes: {', '.join(reflection.key_themes)}")
        print(f"\n  ✅ Action Items:")
        for item in reflection.action_items:
            print(f"    - {item}")
    
    # Show context for LLM
    print("\n🧩 Context for LLM:")
    print(reflection_system.get_insights_for_context())
    
    print("\n✨ Reflection system demonstration complete!")

if __name__ == "__main__":
    demonstrate_reflection_system()