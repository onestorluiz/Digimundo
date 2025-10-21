"""
Optimized imports for OMEGA-ASCENT v4.0.0
Lazy loading and conditional imports for better performance
"""

import sys
from functools import lru_cache
from typing import Optional, Any

class LazyLoader:
    """Lazy loading for heavy modules"""

    def __init__(self):
        self._cache = {}

    @lru_cache(maxsize=32)
    def get_module(self, name: str) -> Any:
        """Load module only when needed"""
        if name not in self._cache:
            if name == "numpy":
                import numpy
                self._cache[name] = numpy
            elif name == "pandas":
                import pandas
                self._cache[name] = pandas
            elif name == "sklearn":
                import sklearn
                self._cache[name] = sklearn
            else:
                self._cache[name] = __import__(name)
        return self._cache[name]

# Global lazy loader
lazy = LazyLoader()

# Fast imports for core modules
from core.auto_documenter import AutoDocumenter
from core.sanity_checker import SanityChecker
from core.snapshot_manager import SnapshotManager

# Conditional imports based on features
def load_optional_features(features: list) -> dict:
    """Load only required features"""
    loaded = {}

    if "arc_fsm" in features:
        from narrative.arc_fsm import build_fsm
        loaded["arc_fsm"] = build_fsm

    if "parallel" in features:
        from optimization.parallel import ParallelProcessor
        loaded["parallel"] = ParallelProcessor

    if "telemetry" in features:
        from monitoring.telemetry import TelemetryCollector
        loaded["telemetry"] = TelemetryCollector

    return loaded
