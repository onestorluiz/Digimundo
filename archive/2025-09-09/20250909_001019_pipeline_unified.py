"""
UNIFIED PIPELINE - FASE 8
Unified pipeline function with depth-based model selection
"""

import time
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class UnifiedPipeline:
    """Unified pipeline system - FASE 8"""
    
    # Model configurations by depth
    MODEL_CONFIGS = {
        "normal": {
            "primary": "llama3.2:3b",
            "secondary": "qwen2.5:7b", 
            "tertiary": "gemma2:2b",
            "quaternary": "mistral:7b",
            "timeout_ms": 5000,
            "max_retries": 2
        },
        "deep": {
            "primary": "deepseek-r1:70b",
            "secondary": "qwen2.5:72b",
            "tertiary": "llama3.1:70b", 
            "quaternary": "deepseek-r1:32b",
            "timeout_ms": 30000,  # Relaxed timeout for large models
            "max_retries": 3
        }
    }
    
    # Stage weights for final mixing
    STAGE_WEIGHTS = {
        "stage1_raw": 0.25,
        "stage2_enhanced": 0.30,
        "stage3_refined": 0.25,
        "stage4_final": 0.20
    }
    
    def __init__(self, processor=None, monitoring=None):
        """Initialize unified pipeline
        
        Args:
            processor: OllamaProcessor instance
            monitoring: MonitoringSystem instance (optional)
        """
        self.processor = processor
        self.monitoring = monitoring
        self.last_run_metrics = {}
        
    def run_pipeline(self, text: str, depth: str = "normal", 
                    context: Optional[Dict] = None) -> Dict[str, Any]:
        """Run unified pipeline with depth-based configuration - FASE 8
        
        Args:
            text: Input text to process
            depth: Processing depth ("normal" or "deep")
            context: Optional context for processing
            
        Returns:
            Dictionary with response and metrics
        """
        start_time = time.time()
        
        # Validate depth
        if depth not in self.MODEL_CONFIGS:
            logger.warning(f"Invalid depth '{depth}', using 'normal'")
            depth = "normal"
        
        config = self.MODEL_CONFIGS[depth]
        logger.info(f"Running pipeline with depth='{depth}'")
        
        # Initialize result structure
        result = {
            "depth": depth,
            "timestamp": datetime.now().isoformat(),
            "input_length": len(text),
            "stages": {},
            "errors": [],
            "metrics": {},
            "final_response": None
        }
        
        try:
            # Stage 1: Raw Analysis
            stage1_result = self._run_stage(
                "stage1_raw",
                text,
                config["primary"],
                config["timeout_ms"],
                "Analyze this text and provide initial insights",
                context
            )
            result["stages"]["stage1"] = stage1_result
            
            # Stage 2: Enhanced Processing
            stage2_prompt = self._build_stage2_prompt(text, stage1_result.get("response", ""))
            stage2_result = self._run_stage(
                "stage2_enhanced",
                stage2_prompt,
                config["secondary"],
                config["timeout_ms"],
                "Enhance and expand the analysis",
                context
            )
            result["stages"]["stage2"] = stage2_result
            
            # Stage 3: Refinement
            stage3_prompt = self._build_stage3_prompt(
                text,
                stage1_result.get("response", ""),
                stage2_result.get("response", "")
            )
            stage3_result = self._run_stage(
                "stage3_refined",
                stage3_prompt,
                config["tertiary"],
                config["timeout_ms"],
                "Refine and synthesize the analysis",
                context
            )
            result["stages"]["stage3"] = stage3_result
            
            # Stage 4: Final Synthesis
            stage4_prompt = self._build_final_prompt(
                text,
                [stage1_result, stage2_result, stage3_result]
            )
            stage4_result = self._run_stage(
                "stage4_final",
                stage4_prompt,
                config["quaternary"],
                config["timeout_ms"],
                "Provide final synthesized response",
                context
            )
            result["stages"]["stage4"] = stage4_result
            
            # Mix final response
            result["final_response"] = self._mix_responses(result["stages"])
            
        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            result["errors"].append(str(e))
            result["final_response"] = self._fallback_response(text)
        
        # Calculate metrics
        end_time = time.time()
        result["metrics"] = {
            "total_time_ms": round((end_time - start_time) * 1000, 2),
            "stages_completed": len([s for s in result["stages"].values() if s.get("success")]),
            "total_stages": 4,
            "depth": depth,
            "models_used": [config[k] for k in ["primary", "secondary", "tertiary", "quaternary"]]
        }
        
        # Record in monitoring if available
        if self.monitoring:
            self.monitoring.record_request(
                result["metrics"]["total_time_ms"],
                success=len(result["errors"]) == 0
            )
        
        self.last_run_metrics = result["metrics"]
        return result
    
    def _run_stage(self, stage_name: str, prompt: str, model: str,
                  timeout_ms: int, instruction: str,
                  context: Optional[Dict]) -> Dict[str, Any]:
        """Run a single pipeline stage
        
        Args:
            stage_name: Name of the stage
            prompt: Prompt text
            model: Model to use
            timeout_ms: Timeout in milliseconds
            instruction: Stage instruction
            context: Optional context
            
        Returns:
            Stage result dictionary
        """
        stage_start = time.time()
        
        try:
            # Check if processor available
            if not self.processor:
                raise ValueError("No processor available")
            
            # Build full prompt
            full_prompt = f"{instruction}\n\nText: {prompt}"
            
            if context:
                full_prompt += f"\n\nContext: {context}"
            
            # Call processor (simplified - real implementation would use actual processor)
            response = self._simulate_model_call(model, full_prompt, timeout_ms)
            
            stage_time = (time.time() - stage_start) * 1000
            
            return {
                "stage": stage_name,
                "model": model,
                "response": response,
                "time_ms": round(stage_time, 2),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Stage {stage_name} failed: {e}")
            return {
                "stage": stage_name,
                "model": model,
                "response": None,
                "error": str(e),
                "time_ms": round((time.time() - stage_start) * 1000, 2),
                "success": False
            }
    
    def _simulate_model_call(self, model: str, prompt: str, timeout_ms: int) -> str:
        """Simulate model call for testing
        
        In production, this would call the actual Ollama processor
        """
        # Simulate processing delay
        time.sleep(min(0.1, timeout_ms / 10000))
        
        # Generate response based on model
        if "70b" in model or "72b" in model:
            return f"[Deep analysis from {model}]: Comprehensive analysis of the input with detailed insights..."
        elif "32b" in model:
            return f"[Advanced response from {model}]: Sophisticated analysis with nuanced understanding..."
        else:
            return f"[Response from {model}]: Standard analysis of the provided text..."
    
    def _build_stage2_prompt(self, original: str, stage1_response: str) -> str:
        """Build prompt for stage 2"""
        return f"""Original: {original[:500]}...
        
Stage 1 Analysis: {stage1_response[:500]}...

Enhance this analysis with additional insights and perspectives."""
    
    def _build_stage3_prompt(self, original: str, stage1: str, stage2: str) -> str:
        """Build prompt for stage 3"""
        return f"""Original: {original[:300]}...
        
Previous analyses:
- Stage 1: {stage1[:300]}...
- Stage 2: {stage2[:300]}...

Synthesize and refine these analyses into a coherent response."""
    
    def _build_final_prompt(self, original: str, stages: List[Dict]) -> str:
        """Build final synthesis prompt"""
        summaries = []
        for i, stage in enumerate(stages, 1):
            if stage.get("success") and stage.get("response"):
                summaries.append(f"Stage {i}: {stage['response'][:200]}...")
        
        return f"""Original query: {original[:200]}...

Synthesize these stage outputs into a final, comprehensive response:
{chr(10).join(summaries)}"""
    
    def _mix_responses(self, stages: Dict[str, Dict]) -> str:
        """Mix stage responses using weighted combination
        
        Args:
            stages: Dictionary of stage results
            
        Returns:
            Mixed final response
        """
        # Collect successful responses
        responses = []
        weights = []
        
        for stage_key, weight in self.STAGE_WEIGHTS.items():
            stage_num = stage_key.split("_")[0]  # e.g., "stage1"
            if stage_num in stages:
                stage_data = stages[stage_num]
                if stage_data.get("success") and stage_data.get("response"):
                    responses.append(stage_data["response"])
                    weights.append(weight)
        
        if not responses:
            return "Unable to generate response - all stages failed"
        
        # Normalize weights
        total_weight = sum(weights)
        normalized_weights = [w/total_weight for w in weights]
        
        # Simple mixing: concatenate with weight indicators
        mixed = "📊 **Unified Analysis**\n\n"
        
        for i, (response, weight) in enumerate(zip(responses, normalized_weights)):
            mixed += f"[Weight: {weight:.2f}] {response[:500]}...\n\n"
        
        return mixed
    
    def _fallback_response(self, text: str) -> str:
        """Generate fallback response when pipeline fails"""
        return f"""I encountered an issue processing your request.
        
Input received: {text[:100]}...

Please try again or use a simpler query."""
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get metrics from last pipeline run"""
        return self.last_run_metrics
    
    def get_status(self) -> Dict[str, Any]:
        """Get pipeline status"""
        return {
            "available": True,
            "last_run": self.last_run_metrics.get("timestamp"),
            "models": {
                "normal": list(self.MODEL_CONFIGS["normal"].values())[:4],
                "deep": list(self.MODEL_CONFIGS["deep"].values())[:4]
            }
        }


# Global pipeline instance
_pipeline_instance = None


def get_pipeline(processor=None, monitoring=None) -> UnifiedPipeline:
    """Get global pipeline instance
    
    Args:
        processor: OllamaProcessor to use
        monitoring: MonitoringSystem to use
        
    Returns:
        Global UnifiedPipeline instance
    """
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = UnifiedPipeline(processor, monitoring)
    return _pipeline_instance


def run_pipeline(text: str, depth: str = "normal", 
                context: Optional[Dict] = None) -> Dict[str, Any]:
    """Convenience function to run pipeline - FASE 8 main interface
    
    Args:
        text: Input text
        depth: Processing depth ("normal" or "deep")
        context: Optional context
        
    Returns:
        Pipeline result with response and metrics
    """
    pipeline = get_pipeline()
    return pipeline.run_pipeline(text, depth, context)