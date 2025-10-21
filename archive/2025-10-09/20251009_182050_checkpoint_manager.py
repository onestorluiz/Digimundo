#!/usr/bin/env python3
"""
CheckpointManager - Session and checkpoint management for Scripturemon v3.0

Provides atomic checkpoint saves, resume functionality, and quality tracking
for screenplay analysis sessions. Never lose work again!

Author: Digimundo
Version: 3.0
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import shutil


class CheckpointManager:
    """
    Manages analysis checkpoints and session state.

    Features:
    - Atomic checkpoint saves (tmp + rename for safety)
    - Track specialist status (pending/running/completed/failed)
    - Track quality scores for each specialist
    - Resume from any point
    - Identify failed specialists for retry
    - Identify low-quality specialists for improvement
    """

    def __init__(self, session_dir: Path | str):
        """
        Initialize checkpoint manager.

        Args:
            session_dir: Directory where checkpoints will be saved
        """
        self.session_dir = Path(session_dir)
        self.checkpoint_file = self.session_dir / 'checkpoint.json'
        self.session_dir.mkdir(parents=True, exist_ok=True)

        # Load existing checkpoint or initialize new
        if self.checkpoint_file.exists():
            self.checkpoint = self._load_checkpoint()
        else:
            self.checkpoint = self._initialize_checkpoint()

    def _initialize_checkpoint(self) -> Dict[str, Any]:
        """Initialize a new checkpoint structure."""
        return {
            'session_id': self.session_dir.name,
            'screenplay_path': None,
            'created_at': datetime.now().isoformat(),
            'last_checkpoint': datetime.now().isoformat(),
            'specialists': {},
            'overall_progress': {
                'total': 22,
                'completed': 0,
                'failed': 0,
                'pending': 22
            },
            'metadata': {
                'llm_model': None,
                'deep_context': None,
                'version': '3.0'
            }
        }

    def _load_checkpoint(self) -> Dict[str, Any]:
        """Load checkpoint from disk."""
        try:
            with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Warning: Failed to load checkpoint: {e}")
            return self._initialize_checkpoint()

    def save_checkpoint(self, state: Optional[Dict[str, Any]] = None) -> None:
        """
        Save checkpoint atomically (tmp + rename).

        Args:
            state: Optional state updates to merge before saving
        """
        if state:
            # Merge provided state into checkpoint
            self.checkpoint.update(state)

        # Update last checkpoint time
        self.checkpoint['last_checkpoint'] = datetime.now().isoformat()

        # Update overall progress
        self._update_progress()

        # Atomic save: write to temp file, then rename
        tmp_file = self.checkpoint_file.with_suffix('.tmp')
        try:
            with open(tmp_file, 'w', encoding='utf-8') as f:
                json.dump(self.checkpoint, f, indent=2, ensure_ascii=False)

            # Atomic rename (POSIX guarantees atomicity)
            shutil.move(str(tmp_file), str(self.checkpoint_file))
        except Exception as e:
            print(f"❌ Error saving checkpoint: {e}")
            if tmp_file.exists():
                tmp_file.unlink()
            raise

    def _update_progress(self) -> None:
        """Update overall progress counts."""
        specialists = self.checkpoint['specialists']

        completed = sum(1 for s in specialists.values() if s.get('status') == 'completed')
        failed = sum(1 for s in specialists.values() if s.get('status') == 'failed')
        total = len(specialists) if specialists else 22
        pending = total - completed - failed

        self.checkpoint['overall_progress'] = {
            'total': total,
            'completed': completed,
            'failed': failed,
            'pending': pending
        }

    def initialize_session(
        self,
        screenplay_path: str,
        llm_model: str,
        deep_context: bool,
        specialist_names: List[str]
    ) -> None:
        """
        Initialize a new analysis session.

        Args:
            screenplay_path: Path to screenplay being analyzed
            llm_model: LLM model name
            deep_context: Whether deep context is enabled
            specialist_names: List of all specialist names
        """
        self.checkpoint['screenplay_path'] = screenplay_path
        self.checkpoint['metadata']['llm_model'] = llm_model
        self.checkpoint['metadata']['deep_context'] = deep_context

        # Initialize all specialists as pending
        for name in specialist_names:
            if name not in self.checkpoint['specialists']:
                self.checkpoint['specialists'][name] = {
                    'status': 'pending',
                    'started_at': None,
                    'completed_at': None,
                    'quality_score': None,
                    'output_path': None,
                    'error': None,
                    'attempts': 0
                }

        self.save_checkpoint()

    def mark_specialist_started(self, specialist_name: str) -> None:
        """Mark a specialist as started."""
        if specialist_name not in self.checkpoint['specialists']:
            self.checkpoint['specialists'][specialist_name] = {
                'status': 'running',
                'started_at': datetime.now().isoformat(),
                'attempts': 1
            }
        else:
            spec = self.checkpoint['specialists'][specialist_name]
            spec['status'] = 'running'
            spec['started_at'] = datetime.now().isoformat()
            spec['attempts'] = spec.get('attempts', 0) + 1

        self.save_checkpoint()

    def mark_specialist_completed(
        self,
        specialist_name: str,
        quality_score: float,
        output_path: str
    ) -> None:
        """
        Mark a specialist as completed.

        Args:
            specialist_name: Name of the specialist
            quality_score: Quality score (0-10)
            output_path: Path to output file
        """
        spec = self.checkpoint['specialists'][specialist_name]
        spec['status'] = 'completed'
        spec['completed_at'] = datetime.now().isoformat()
        spec['quality_score'] = quality_score
        spec['output_path'] = output_path
        spec['error'] = None

        self.save_checkpoint()

        # Print progress
        progress = self.checkpoint['overall_progress']
        print(f"✅ {specialist_name} completed ({progress['completed']}/{progress['total']}) - Score: {quality_score:.1f}/10")

    def mark_specialist_failed(
        self,
        specialist_name: str,
        error: str
    ) -> None:
        """
        Mark a specialist as failed.

        Args:
            specialist_name: Name of the specialist
            error: Error message
        """
        spec = self.checkpoint['specialists'][specialist_name]
        spec['status'] = 'failed'
        spec['completed_at'] = datetime.now().isoformat()
        spec['error'] = error

        self.save_checkpoint()

        print(f"❌ {specialist_name} failed: {error}")

    def get_completed_specialists(self) -> List[str]:
        """Get list of completed specialist names."""
        return [
            name for name, spec in self.checkpoint['specialists'].items()
            if spec.get('status') == 'completed'
        ]

    def get_failed_specialists(self) -> List[str]:
        """Get list of failed specialist names."""
        return [
            name for name, spec in self.checkpoint['specialists'].items()
            if spec.get('status') == 'failed'
        ]

    def get_pending_specialists(self) -> List[str]:
        """Get list of pending specialist names."""
        return [
            name for name, spec in self.checkpoint['specialists'].items()
            if spec.get('status') in ['pending', None]
        ]

    def get_low_quality_specialists(self, threshold: float = 7.0) -> List[str]:
        """
        Get list of specialists with quality score below threshold.

        Args:
            threshold: Minimum acceptable quality score (default 7.0)

        Returns:
            List of specialist names with quality < threshold
        """
        low_quality = []
        for name, spec in self.checkpoint['specialists'].items():
            if spec.get('status') == 'completed':
                score = spec.get('quality_score', 0)
                if score is not None and score < threshold:
                    low_quality.append(name)

        return low_quality

    def get_specialist_status(self, specialist_name: str) -> Optional[str]:
        """Get status of a specific specialist."""
        spec = self.checkpoint['specialists'].get(specialist_name)
        return spec.get('status') if spec else None

    def get_specialist_quality(self, specialist_name: str) -> Optional[float]:
        """Get quality score of a specific specialist."""
        spec = self.checkpoint['specialists'].get(specialist_name)
        return spec.get('quality_score') if spec else None

    def should_run_specialist(
        self,
        specialist_name: str,
        resume: bool = False,
        retry_failed: bool = False,
        improve_quality: bool = False,
        quality_threshold: float = 7.0
    ) -> bool:
        """
        Determine if a specialist should be run based on mode.

        Args:
            specialist_name: Name of the specialist
            resume: Resume mode (run pending only)
            retry_failed: Retry failed specialists
            improve_quality: Re-run low quality specialists
            quality_threshold: Threshold for quality improvement

        Returns:
            True if specialist should be run
        """
        spec = self.checkpoint['specialists'].get(specialist_name)
        if not spec:
            return True  # Not in checkpoint, run it

        status = spec.get('status')

        if resume:
            # Resume mode: run pending and failed
            return status in ['pending', 'failed', None]

        if retry_failed:
            # Retry failed only
            return status == 'failed'

        if improve_quality:
            # Re-run low quality
            if status == 'completed':
                score = spec.get('quality_score', 0)
                return score is not None and score < quality_threshold
            return False

        # Default: run if not completed
        return status != 'completed'

    def get_summary(self) -> Dict[str, Any]:
        """Get checkpoint summary for display."""
        progress = self.checkpoint['overall_progress']

        # Calculate average quality of completed specialists
        completed_specs = [
            spec for spec in self.checkpoint['specialists'].values()
            if spec.get('status') == 'completed' and spec.get('quality_score') is not None
        ]

        avg_quality = 0.0
        if completed_specs:
            avg_quality = sum(s['quality_score'] for s in completed_specs) / len(completed_specs)

        return {
            'session_id': self.checkpoint['session_id'],
            'screenplay_path': self.checkpoint.get('screenplay_path'),
            'created_at': self.checkpoint.get('created_at'),
            'last_checkpoint': self.checkpoint.get('last_checkpoint'),
            'progress': progress,
            'avg_quality': avg_quality,
            'low_quality_count': len(self.get_low_quality_specialists()),
            'failed_count': progress['failed']
        }

    def print_status(self) -> None:
        """Print current checkpoint status."""
        summary = self.get_summary()
        progress = summary['progress']

        print()
        print("═" * 80)
        print("📊 CHECKPOINT STATUS")
        print("═" * 80)
        print(f"📂 Session: {summary['session_id']}")
        print(f"📄 Screenplay: {summary['screenplay_path']}")
        print(f"⏰ Last Update: {summary['last_checkpoint']}")
        print()
        print(f"✅ Completed: {progress['completed']}/{progress['total']}")
        print(f"❌ Failed: {progress['failed']}")
        print(f"⏳ Pending: {progress['pending']}")
        print(f"📊 Avg Quality: {summary['avg_quality']:.1f}/10")

        if summary['low_quality_count'] > 0:
            print(f"⚠️  Low Quality (<7.0): {summary['low_quality_count']}")

        print("═" * 80)
        print()

    def export_results(self) -> Dict[str, Any]:
        """Export checkpoint data for analysis results."""
        return {
            'session_id': self.checkpoint['session_id'],
            'screenplay_path': self.checkpoint.get('screenplay_path'),
            'specialists': self.checkpoint['specialists'],
            'progress': self.checkpoint['overall_progress'],
            'metadata': self.checkpoint.get('metadata', {})
        }


if __name__ == '__main__':
    # Test checkpoint manager
    import tempfile

    print("🧪 Testing CheckpointManager...")

    with tempfile.TemporaryDirectory() as tmpdir:
        session_dir = Path(tmpdir) / "test_session"

        # Create checkpoint manager
        mgr = CheckpointManager(session_dir)

        # Initialize session
        mgr.initialize_session(
            screenplay_path="/path/to/screenplay.pdf",
            llm_model="scripturemon-optimized",
            deep_context=True,
            specialist_names=["mckee_dialogue", "campbell_hero", "field_structure"]
        )

        # Simulate analysis
        mgr.mark_specialist_started("mckee_dialogue")
        mgr.mark_specialist_completed("mckee_dialogue", 8.5, "/path/to/output.html")

        mgr.mark_specialist_started("campbell_hero")
        mgr.mark_specialist_failed("campbell_hero", "LLM timeout")

        mgr.mark_specialist_started("field_structure")
        mgr.mark_specialist_completed("field_structure", 6.5, "/path/to/output2.html")

        # Print status
        mgr.print_status()

        # Test queries
        print(f"Completed: {mgr.get_completed_specialists()}")
        print(f"Failed: {mgr.get_failed_specialists()}")
        print(f"Pending: {mgr.get_pending_specialists()}")
        print(f"Low Quality (<7.0): {mgr.get_low_quality_specialists()}")

        print("\n✅ CheckpointManager test passed!")
