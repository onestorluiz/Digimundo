"""
🤝 COLLABORATIVE MODE SYSTEM SUPREME  
Multi-user screenplay collaboration with conflict resolution
"""
import asyncio
import json
import hashlib
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import re
from collections import defaultdict
from enum import Enum
import difflib
from src.core.unified_memory_system import get_unified_memory, MemoryType
# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado


class CollaboratorRole(Enum):
    OWNER = 'owner'
    EDITOR = 'editor'
    WRITER = 'writer'
    REVIEWER = 'reviewer'
    VIEWER = 'viewer'

class ChangeType(Enum):
    ADD = 'add'
    DELETE = 'delete'
    MODIFY = 'modify'
    COMMENT = 'comment'
    MERGE = 'merge'
    CONFLICT = 'conflict'

@dataclass
class Collaborator:
    id: str
    name: str
    email: str
    role: CollaboratorRole
    joined_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)
    assigned_sections: List[str] = field(default_factory=list)
    color: str = ''

@dataclass
class Change:
    id: str
    collaborator_id: str
    timestamp: datetime
    change_type: ChangeType
    location: str
    original_content: str
    new_content: str
    comment: str = ''
    merged: bool = False
    conflicted_with: Optional[str] = None

@dataclass
class Comment:
    id: str
    collaborator_id: str
    timestamp: datetime
    location: str
    content: str
    resolved: bool = False
    replies: List['Comment'] = field(default_factory=list)

@dataclass
class Session:
    id: str
    project_name: str
    created_at: datetime
    owner_id: str
    active: bool = True
    collaborators: Dict[str, Collaborator] = field(default_factory=dict)
    changes: List[Change] = field(default_factory=list)
    comments: List[Comment] = field(default_factory=list)
    current_version: str = ''
    version_history: List[Dict] = field(default_factory=list)

class CollaborativeModeSystem:

    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.active_collaborators: Dict[str, str] = {}
        self.change_queue: asyncio.Queue = asyncio.Queue()
        self.conflict_resolver = ConflictResolver()
        self.database_path = Path('output/collaborative')
        self.database_path.mkdir(parents=True, exist_ok=True)
        self.load_sessions()
        self.processing = True
        asyncio.create_task(self.process_changes())

    def load_sessions(self):
        """Load existing collaborative sessions"""
        sessions_file = self.database_path / 'sessions.json'
        if sessions_file.exists():
            try:
                with open(sessions_file, 'r') as f:
                    data = json.load(f)
            except:
                pass

    def save_sessions(self):
        """Save collaborative sessions"""
        sessions_file = self.database_path / 'sessions.json'

    def create_session(self, project_name: str, owner_name: str, owner_email: str, initial_content: str='') -> Session:
        """Create a new collaborative session"""
        owner = Collaborator(id=str(uuid.uuid4()), name=owner_name, email=owner_email, role=CollaboratorRole.OWNER, color='#FF0000')
        session = Session(id=str(uuid.uuid4()), project_name=project_name, created_at=datetime.now(), owner_id=owner.id, current_version=initial_content)
        session.collaborators[owner.id] = owner
        self.sessions[session.id] = session
        self.save_sessions()
        print(f'🤝 Collaborative session created: {session.id}')
        return session

    async def join_session(self, session_id: str, collaborator_name: str, collaborator_email: str, role: CollaboratorRole=CollaboratorRole.WRITER) -> Optional[Collaborator]:
        """Join an existing session"""
        if session_id not in self.sessions:
            return None
        session = self.sessions[session_id]
        for collab in session.collaborators.values():
            if collab.email == collaborator_email:
                return collab
        collaborator = Collaborator(id=str(uuid.uuid4()), name=collaborator_name, email=collaborator_email, role=role, color=self.assign_color(len(session.collaborators)))
        session.collaborators[collaborator.id] = collaborator
        self.active_collaborators[collaborator.id] = session_id
        await self.broadcast_notification(session_id, f'{collaborator_name} joined the session')
        self.save_sessions()
        return collaborator

    def assign_color(self, index: int) -> str:
        """Assign a unique color to collaborator"""
        colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#FFA500', '#800080', '#008000', '#000080', '#800000', '#808000']
        return colors[index % len(colors)]

    async def submit_change(self, session_id: str, collaborator_id: str, change_type: ChangeType, location: str, original_content: str, new_content: str, comment: str='') -> Change:
        """Submit a change to the screenplay"""
        if session_id not in self.sessions:
            raise ValueError('Session not found')
        session = self.sessions[session_id]
        if collaborator_id not in session.collaborators:
            raise ValueError('Collaborator not in session')
        collaborator = session.collaborators[collaborator_id]
        if not self.has_edit_permission(collaborator, location):
            raise PermissionError('No permission to edit this section')
        change = Change(id=str(uuid.uuid4()), collaborator_id=collaborator_id, timestamp=datetime.now(), change_type=change_type, location=location, original_content=original_content, new_content=new_content, comment=comment)
        await self.change_queue.put((session_id, change))
        return change

    def has_edit_permission(self, collaborator: Collaborator, location: str) -> bool:
        """Check if collaborator can edit location"""
        if collaborator.role in [CollaboratorRole.OWNER, CollaboratorRole.EDITOR]:
            return True
        if collaborator.role == CollaboratorRole.WRITER:
            for section in collaborator.assigned_sections:
                if section in location:
                    return True
        return False

    async def process_changes(self):
        """Process change queue and resolve conflicts"""
        while self.processing:
            try:
                session_id, change = await asyncio.wait_for(self.change_queue.get(), timeout=1.0)
                session = self.sessions[session_id]
                conflicts = self.detect_conflicts(session, change)
                if conflicts:
                    resolved_change = await self.conflict_resolver.resolve(change, conflicts, session)
                    if resolved_change:
                        change = resolved_change
                    else:
                        change.change_type = ChangeType.CONFLICT
                        change.conflicted_with = conflicts[0].id
                if change.change_type != ChangeType.CONFLICT:
                    session.current_version = self.apply_change(session.current_version, change)
                    change.merged = True
                session.changes.append(change)
                if len(session.changes) % 10 == 0:
                    self.create_version_snapshot(session)
                await self.broadcast_update(session_id, change)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f'Error processing change: {e}')

    def detect_conflicts(self, session: Session, new_change: Change) -> List[Change]:
        """Detect conflicts with recent changes"""
        conflicts = []
        recent_cutoff = datetime.now() - timedelta(minutes=5)
        for change in reversed(session.changes):
            if change.timestamp < recent_cutoff:
                break
            if not change.merged:
                continue
            if change.location == new_change.location:
                if change.new_content != new_change.original_content:
                    conflicts.append(change)
        return conflicts

    def apply_change(self, content: str, change: Change) -> str:
        """Apply a change to content"""
        if change.change_type == ChangeType.ADD:
            return self.insert_at_location(content, change.location, change.new_content)
        elif change.change_type == ChangeType.DELETE:
            return self.remove_at_location(content, change.location, change.original_content)
        elif change.change_type == ChangeType.MODIFY:
            return content.replace(change.original_content, change.new_content)
        return content

    def insert_at_location(self, content: str, location: str, new_content: str) -> str:
        """Insert content at specified location"""
        lines = content.split('\n')
        line_match = re.search('Line (\\d+)', location)
        if line_match:
            line_num = int(line_match.group(1))
            if 0 <= line_num <= len(lines):
                lines.insert(line_num, new_content)
        return '\n'.join(lines)

    def remove_at_location(self, content: str, location: str, text_to_remove: str) -> str:
        """Remove content at specified location"""
        return content.replace(text_to_remove, '')

    def create_version_snapshot(self, session: Session):
        """Create a version snapshot"""
        snapshot = {'version': len(session.version_history) + 1, 'timestamp': datetime.now().isoformat(), 'content': session.current_version, 'change_count': len(session.changes), 'collaborators': list(session.collaborators.keys())}
        session.version_history.append(snapshot)
        snapshot_file = self.database_path / f"snapshot_{session.id}_{snapshot['version']}.json"
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)

    def broadcast_update(self, session_id: str, change: Change):
        """Broadcast change to all collaborators"""
        if session_id not in self.sessions:
            return
        session = self.sessions[session_id]
        collaborator = session.collaborators.get(change.collaborator_id)
        if collaborator:
            message = {'type': 'change', 'collaborator': collaborator.name, 'change_type': change.change_type.value, 'location': change.location, 'timestamp': change.timestamp.isoformat()}
            print(f'Broadcast: {message}')

    def broadcast_notification(self, session_id: str, message: str):
        """Broadcast notification to all collaborators"""
        notification = {'type': 'notification', 'message': message, 'timestamp': datetime.now().isoformat()}
        print(f'Notification: {notification}')

    async def add_comment(self, session_id: str, collaborator_id: str, location: str, content: str) -> Comment:
        """Add a comment to the screenplay"""
        if session_id not in self.sessions:
            raise ValueError('Session not found')
        session = self.sessions[session_id]
        comment = Comment(id=str(uuid.uuid4()), collaborator_id=collaborator_id, timestamp=datetime.now(), location=location, content=content)
        session.comments.append(comment)
        collaborator = session.collaborators.get(collaborator_id)
        if collaborator:
            await self.broadcast_notification(session_id, f'{collaborator.name} commented at {location}')
        return comment

    def get_active_collaborators(self, session_id: str, minutes: int=5) -> List[Collaborator]:
        """Get currently active collaborators"""
        if session_id not in self.sessions:
            return []
        session = self.sessions[session_id]
        cutoff = datetime.now() - timedelta(minutes=minutes)
        active = [collab for collab in session.collaborators.values() if collab.last_active > cutoff]
        return active

    def get_change_history(self, session_id: str, limit: int=50) -> List[Change]:
        """Get recent change history"""
        if session_id not in self.sessions:
            return []
        session = self.sessions[session_id]
        return session.changes[-limit:]

    def merge_changes(self, session_id: str, change_ids: List[str]) -> str:
        """Merge selected changes into main version"""
        if session_id not in self.sessions:
            raise ValueError('Session not found')
        session = self.sessions[session_id]
        merged_content = session.current_version
        for change_id in change_ids:
            change = next((c for c in session.changes if c.id == change_id), None)
            if change and (not change.merged):
                merged_content = self.apply_change(merged_content, change)
                change.merged = True
        session.current_version = merged_content
        self.create_version_snapshot(session)
        return merged_content

    def export_final_version(self, session_id: str, filepath: Path) -> bool:
        """Export the final collaborative version"""
        if session_id not in self.sessions:
            return False
        session = self.sessions[session_id]
        credits = '\n\n/* COLLABORATIVE CREDITS\n'
        for collab in session.collaborators.values():
            change_count = sum((1 for c in session.changes if c.collaborator_id == collab.id))
            credits += f'  {collab.name} - {change_count} contributions\n'
        credits += '*/\n'
        final_content = session.current_version + credits
        with open(filepath, 'w') as f:
            f.write(final_content)
        return True

class ConflictResolver:
    """Resolve conflicts between changes"""

    def resolve(self, new_change: Change, conflicts: List[Change], session: Session) -> Optional[Change]:
        """Resolve conflicts automatically or flag for manual resolution"""
        if not conflicts:
            return new_change
        if all((c.collaborator_id == new_change.collaborator_id for c in conflicts)):
            return new_change
        new_collaborator = session.collaborators.get(new_change.collaborator_id)
        if new_collaborator and new_collaborator.role in [CollaboratorRole.OWNER, CollaboratorRole.EDITOR]:
            return new_change
        if self.can_auto_merge(new_change, conflicts[0]):
            merged = self.auto_merge(new_change, conflicts[0])
            return merged
        return None

    def can_auto_merge(self, change1: Change, change2: Change) -> bool:
        """Check if changes can be automatically merged"""
        if change1.location != change2.location:
            return True
        if change1.change_type == ChangeType.ADD and change2.change_type == ChangeType.ADD:
            return True
        return False

    def auto_merge(self, change1: Change, change2: Change) -> Change:
        """Automatically merge two compatible changes"""
        if change1.change_type == ChangeType.ADD and change2.change_type == ChangeType.ADD:
            merged = Change(id=str(uuid.uuid4()), collaborator_id='system', timestamp=datetime.now(), change_type=ChangeType.MERGE, location=change1.location, original_content=change1.original_content, new_content=change1.new_content + '\n' + change2.new_content, comment=f'Auto-merged changes from multiple collaborators')
            return merged
        return change1 if change1.timestamp > change2.timestamp else change2

async def main():
    """Test collaborative mode"""
    system = CollaborativeModeSystem()
    print('🤝 COLLABORATIVE MODE TEST 🤝\n')
    session = await system.create_session('The Matrix Rewrite', 'Writer One', 'writer1@example.com', initial_content='FADE IN:\n\nINT. APARTMENT - NIGHT\n\nNEO sits at his computer.\n\nNEO\nWhat is the Matrix?\n\nFADE OUT.')
    print(f'Session created: {session.id}\n')
    collab2 = await system.join_session(session.id, 'Writer Two', 'writer2@example.com', CollaboratorRole.WRITER)
    collab3 = await system.join_session(session.id, 'Editor', 'editor@example.com', CollaboratorRole.EDITOR)
    print('Collaborators joined\n')
    change1 = await system.submit_change(session.id, collab2.id, ChangeType.ADD, 'Line 5', '', 'TRINITY enters the room.', "Adding Trinity's entrance")
    print(f'Change submitted by {collab2.name}\n')
    comment = await system.add_comment(session.id, collab3.id, 'Line 7', 'This dialogue needs more subtext')
    print(f'Comment added by Editor\n')
    change2 = await system.submit_change(session.id, session.collaborators[session.owner_id].id, ChangeType.MODIFY, 'Line 7', 'What is the Matrix?', 'Follow the white rabbit.', 'More mysterious opening')
    await asyncio.sleep(2)
    active = system.get_active_collaborators(session.id)
    print(f'Active collaborators: {[c.name for c in active]}\n')
    history = system.get_change_history(session.id)
    print(f'Changes made: {len(history)}')
    for change in history:
        collab_name = session.collaborators.get(change.collaborator_id, {}).name
        print(f'  - {collab_name}: {change.change_type.value} at {change.location}')
    print('\nExporting final version...')
    export_path = Path('collaborative_final.txt')
    if system.export_final_version(session.id, export_path):
        print(f'Exported to {export_path}')
        with open(export_path, 'r') as f:
            print('\nFinal content:')
            print(f.read())
        export_path.unlink(missing_ok=True)
if __name__ == '__main__':
    asyncio.run(main())

# ============================================================
# AUTO-UNIFIED MEMORY HELPER
# ============================================================
def _get_memory():
    """Helper para acesso rápido à memória unificada"""
    return get_unified_memory()

# Atalhos para compatibilidade
unified_memory = _get_memory()
