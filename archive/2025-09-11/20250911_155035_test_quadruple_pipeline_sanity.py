"""
Unit tests for QuadruplePipeline with monkeypatch
"""
import pytest
import subprocess
import time
from unittest.mock import MagicMock, patch, Mock
import sys
import os

# Add project root to path
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-validation')

from apps.scripturemon.quadruple_pipeline import QuadruplePipeline


class TestQuadruplePipelineSanity:
    
    def test_pipeline_initialization(self):
        """Test pipeline can be initialized"""
        pipeline = QuadruplePipeline()
        assert pipeline is not None
        assert hasattr(pipeline, 'global_semaphore')
        assert hasattr(pipeline, 'heavy_semaphore')
        assert hasattr(pipeline, 'light_semaphore')
    
    @patch('subprocess.Popen')
    def test_successful_execution(self, mock_popen):
        """Test successful model execution"""
        # Setup mock process
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("Test output success", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        pipeline = QuadruplePipeline()
        
        # Execute stage
        result = pipeline._execute_stage(
            stage="extract",
            prompt="Test prompt",
            timeout=5,
            context={}
        )
        
        # Assertions
        assert result["success"] is True
        assert result["output"] == "Test output success"
        assert result["error"] is None
        assert result["duration_ms"] > 0
        
    @patch('subprocess.Popen')
    def test_timeout_handling(self, mock_popen):
        """Test timeout is properly handled"""
        # Setup mock process with timeout
        mock_process = MagicMock()
        mock_process.communicate.side_effect = subprocess.TimeoutExpired('cmd', 5)
        mock_process.kill = MagicMock()
        mock_popen.return_value = mock_process
        
        pipeline = QuadruplePipeline()
        
        # Execute stage
        result = pipeline._execute_stage(
            stage="analyze",
            prompt="Test prompt",
            timeout=5,
            context={}
        )
        
        # Assertions
        assert result["success"] is False
        assert "timed out" in result["error"]
        assert mock_process.kill.called
        assert result["duration_ms"] > 0
        
    @patch('subprocess.Popen')
    def test_error_handling(self, mock_popen):
        """Test error with non-zero return code"""
        # Setup mock process with error
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("", "Error: Model failed")
        mock_process.returncode = 1
        mock_popen.return_value = mock_process
        
        pipeline = QuadruplePipeline()
        
        # Execute stage
        result = pipeline._execute_stage(
            stage="evaluate",
            prompt="Test prompt",
            timeout=5,
            context={}
        )
        
        # Assertions
        assert result["success"] is False
        assert "Model returned error" in result["error"]
        assert result["duration_ms"] > 0
        
    @patch('subprocess.Popen')
    def test_semaphore_release_on_success(self, mock_popen):
        """Test semaphores are released on success"""
        # Setup successful mock
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("Success", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        pipeline = QuadruplePipeline()
        
        # Track semaphore state
        global_acquire_count = 0
        global_release_count = 0
        model_acquire_count = 0
        model_release_count = 0
        
        # Wrap semaphore methods
        original_global_acquire = pipeline.global_semaphore.acquire
        original_global_release = pipeline.global_semaphore.release
        original_model_acquire = pipeline.light_semaphore.acquire
        original_model_release = pipeline.light_semaphore.release
        
        def track_global_acquire(*args, **kwargs):
            nonlocal global_acquire_count
            global_acquire_count += 1
            return original_global_acquire(*args, **kwargs)
            
        def track_global_release(*args, **kwargs):
            nonlocal global_release_count
            global_release_count += 1
            return original_global_release(*args, **kwargs)
            
        def track_model_acquire(*args, **kwargs):
            nonlocal model_acquire_count
            model_acquire_count += 1
            return original_model_acquire(*args, **kwargs)
            
        def track_model_release(*args, **kwargs):
            nonlocal model_release_count
            model_release_count += 1
            return original_model_release(*args, **kwargs)
        
        pipeline.global_semaphore.acquire = track_global_acquire
        pipeline.global_semaphore.release = track_global_release
        pipeline.light_semaphore.acquire = track_model_acquire
        pipeline.light_semaphore.release = track_model_release
        
        # Execute
        result = pipeline._execute_stage(
            stage="extract",
            prompt="Test",
            timeout=5,
            context={}
        )
        
        # Verify semaphores were acquired and released
        assert global_acquire_count == 1, "Global semaphore should be acquired once"
        assert global_release_count == 1, "Global semaphore should be released once"
        assert model_acquire_count == 1, "Model semaphore should be acquired once"
        assert model_release_count == 1, "Model semaphore should be released once"
        
    @patch('subprocess.Popen')
    def test_semaphore_release_on_error(self, mock_popen):
        """Test semaphores are released even on error"""
        # Setup error mock
        mock_process = MagicMock()
        mock_process.communicate.side_effect = Exception("Test error")
        mock_popen.return_value = mock_process
        
        pipeline = QuadruplePipeline()
        
        # Track releases
        global_release_count = 0
        model_release_count = 0
        
        original_global_release = pipeline.global_semaphore.release
        original_model_release = pipeline.light_semaphore.release
        
        def track_global_release(*args, **kwargs):
            nonlocal global_release_count
            global_release_count += 1
            return original_global_release(*args, **kwargs)
            
        def track_model_release(*args, **kwargs):
            nonlocal model_release_count
            model_release_count += 1
            return original_model_release(*args, **kwargs)
        
        pipeline.global_semaphore.release = track_global_release
        pipeline.light_semaphore.release = track_model_release
        
        # Execute (will fail)
        result = pipeline._execute_stage(
            stage="synthesize",
            prompt="Test",
            timeout=5,
            context={}
        )
        
        # Verify semaphores were still released
        assert global_release_count == 1, "Global semaphore should be released on error"
        assert model_release_count == 1, "Model semaphore should be released on error"
        assert result["success"] is False
        
    @patch('subprocess.Popen')
    def test_fallback_triggered(self, mock_popen):
        """Test fallback is triggered on error"""
        # First call fails, second (fallback) succeeds
        mock_process_fail = MagicMock()
        mock_process_fail.communicate.return_value = ("", "Error")
        mock_process_fail.returncode = 1
        
        mock_process_success = MagicMock()
        mock_process_success.communicate.return_value = ("Fallback success", "")
        mock_process_success.returncode = 0
        
        mock_popen.side_effect = [mock_process_fail, mock_process_success]
        
        pipeline = QuadruplePipeline()
        
        # Execute with normal model (should trigger fallback)
        result = pipeline._execute_stage(
            stage="extract",
            prompt="Test",
            timeout=10,
            context={}
        )
        
        # Verify fallback was used
        assert len(pipeline.pipeline_stats["fallbacks_used"]) > 0
        # Result might still fail if fallback also fails, but fallback should be attempted
        
    def test_stats_tracking(self):
        """Test pipeline tracks statistics"""
        pipeline = QuadruplePipeline()
        
        # Check initial stats
        assert "runs" in pipeline.pipeline_stats
        assert "timeouts" in pipeline.pipeline_stats
        assert "fallbacks_used" in pipeline.pipeline_stats
        assert "total_duration_ms" in pipeline.pipeline_stats
        
        # Stats should be lists/integers
        assert isinstance(pipeline.pipeline_stats["runs"], int)
        assert isinstance(pipeline.pipeline_stats["timeouts"], list)
        assert isinstance(pipeline.pipeline_stats["total_duration_ms"], (int, float))
        
    def test_no_deadlock_on_semaphore_timeout(self):
        """Test no deadlock when semaphore acquisition times out"""
        pipeline = QuadruplePipeline()
        
        # Make global semaphore always timeout
        pipeline.global_semaphore.acquire = lambda timeout=None: False
        
        # Execute - should fail but not hang
        result = pipeline._execute_stage(
            stage="extract",
            prompt="Test",
            timeout=1,
            context={}
        )
        
        # Should fail gracefully
        assert result["success"] is False
        assert "global semaphore" in result["error"].lower()
        assert result["duration_ms"] >= 0