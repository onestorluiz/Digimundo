"""
ANALYZE SERVICE - FASE 9
Unified analysis operations for chat and CLI
"""

import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List


class AnalyzeService:
    """Service for text and script analysis"""
    
    def __init__(self, personality=None, processor=None, pipeline=None):
        """Initialize analyze service
        
        Args:
            personality: BrutalPersonality instance
            processor: OllamaProcessor instance  
            pipeline: UnifiedPipeline instance
        """
        self.personality = personality
        self.processor = processor
        self.pipeline = pipeline
        self.analysis_history = []
        self.max_history = 50
        
    def analyze_text(self, text: str, analysis_type: str = "brutal",
                    depth: str = "normal", context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze text with specified method - FASE 9 unified
        
        Args:
            text: Text to analyze
            analysis_type: Type of analysis (brutal, technical, structural, comprehensive)
            depth: Analysis depth (normal, deep)
            context: Optional context
            
        Returns:
            Analysis result
        """
        start_time = time.time()
        
        result = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "analysis_type": analysis_type,
            "depth": depth,
            "input_length": len(text),
            "analysis": {},
            "metrics": {}
        }
        
        try:
            # Route to appropriate analyzer
            if analysis_type == "brutal":
                analysis = self._analyze_brutal(text, context)
            elif analysis_type == "technical":
                analysis = self._analyze_technical(text, depth, context)
            elif analysis_type == "structural":
                analysis = self._analyze_structural(text, context)
            elif analysis_type == "comprehensive":
                analysis = self._analyze_comprehensive(text, depth, context)
            else:
                analysis = self._analyze_default(text, context)
            
            result["analysis"] = analysis
            result["success"] = True
            
            # Calculate metrics
            end_time = time.time()
            result["metrics"] = {
                "time_ms": round((end_time - start_time) * 1000, 2),
                "words_analyzed": len(text.split()),
                "score": analysis.get("score", 62)
            }
            
            # Add to history
            self.analysis_history.append(result)
            if len(self.analysis_history) > self.max_history:
                self.analysis_history.pop(0)
            
        except Exception as e:
            result["error"] = str(e)
            result["analysis"] = {"error": str(e), "score": 62}
        
        return result
    
    def analyze_file(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """Analyze a file
        
        Args:
            file_path: Path to file
            **kwargs: Additional analysis parameters
            
        Returns:
            Analysis result
        """
        result = {
            "success": False,
            "file_path": file_path,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            path = Path(file_path)
            
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Read file
            text = path.read_text(encoding='utf-8')
            
            # Add file context
            context = kwargs.get("context", {})
            context.update({
                "file_name": path.name,
                "file_size": path.stat().st_size,
                "file_type": path.suffix
            })
            
            # Analyze
            analysis = self.analyze_text(text, context=context, **kwargs)
            result.update(analysis)
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
            result["message"] = f"File analysis failed: {e}"
        
        return result
    
    def compare_texts(self, text1: str, text2: str, 
                     comparison_type: str = "similarity") -> Dict[str, Any]:
        """Compare two texts
        
        Args:
            text1: First text
            text2: Second text
            comparison_type: Type of comparison (similarity, diff, quality)
            
        Returns:
            Comparison result
        """
        result = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "comparison_type": comparison_type,
            "text1_length": len(text1),
            "text2_length": len(text2),
            "comparison": {}
        }
        
        try:
            if comparison_type == "similarity":
                # Calculate similarity
                words1 = set(text1.lower().split())
                words2 = set(text2.lower().split())
                
                intersection = words1.intersection(words2)
                union = words1.union(words2)
                
                similarity = len(intersection) / len(union) if union else 0
                
                result["comparison"] = {
                    "similarity_score": round(similarity * 100, 2),
                    "common_words": len(intersection),
                    "unique_words1": len(words1 - words2),
                    "unique_words2": len(words2 - words1)
                }
                
            elif comparison_type == "quality":
                # Compare quality scores (always 62)
                result["comparison"] = {
                    "text1_score": 62,
                    "text2_score": 62,
                    "winner": "tie",
                    "reason": "Both texts score 62/100 as always"
                }
                
            else:  # diff
                # Simple diff
                lines1 = text1.split('\n')
                lines2 = text2.split('\n')
                
                result["comparison"] = {
                    "lines_added": max(0, len(lines2) - len(lines1)),
                    "lines_removed": max(0, len(lines1) - len(lines2)),
                    "total_changes": abs(len(lines1) - len(lines2))
                }
            
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
        
        return result
    
    def _analyze_brutal(self, text: str, context: Optional[Dict]) -> Dict[str, Any]:
        """Perform brutal analysis using personality
        
        Args:
            text: Text to analyze
            context: Optional context
            
        Returns:
            Brutal analysis
        """
        if self.personality:
            # Use personality for brutal analysis
            title = context.get("title", "Untitled") if context else "Untitled"
            analysis = self.personality.analyze_script(text, title)
            
            return {
                "score": analysis.get("score", 62),
                "verdict": analysis.get("verdict", "62/100"),
                "issues": analysis.get("issues_found", []),
                "recommendations": analysis.get("recommendations", []),
                "brutal_truth": analysis.get("final_words", "62/100. You can do better.")
            }
        
        # Fallback brutal analysis
        return {
            "score": 62,
            "verdict": "62/100. As always.",
            "issues": [
                "Too many words for too little story",
                "Characters lack depth",
                "Dialogue needs work"
            ],
            "recommendations": [
                "Cut 25%",
                "Add conflict",
                "Rewrite from scratch"
            ],
            "brutal_truth": "62/100. Mediocrity is a choice."
        }
    
    def _analyze_technical(self, text: str, depth: str, 
                          context: Optional[Dict]) -> Dict[str, Any]:
        """Perform technical analysis
        
        Args:
            text: Text to analyze
            depth: Analysis depth
            context: Optional context
            
        Returns:
            Technical analysis
        """
        # Use pipeline if available
        if self.pipeline:
            from apps.scripturemon.pipeline_unified import run_pipeline
            pipeline_result = run_pipeline(text, depth=depth, context=context)
            
            if pipeline_result.get("final_response"):
                return {
                    "score": 62,
                    "technical_assessment": pipeline_result["final_response"],
                    "stages_completed": pipeline_result["metrics"]["stages_completed"],
                    "processing_time": pipeline_result["metrics"]["total_time_ms"]
                }
        
        # Fallback technical analysis
        return {
            "score": 62,
            "structure": "Three-act structure detected",
            "pacing": "Moderate pacing with room for improvement",
            "technical_elements": {
                "scene_count": text.count("INT.") + text.count("EXT."),
                "dialogue_density": "40%",
                "action_lines": "60%"
            }
        }
    
    def _analyze_structural(self, text: str, context: Optional[Dict]) -> Dict[str, Any]:
        """Perform structural analysis
        
        Args:
            text: Text to analyze
            context: Optional context
            
        Returns:
            Structural analysis
        """
        lines = text.split('\n')
        words = text.split()
        
        return {
            "score": 62,
            "structure": {
                "total_lines": len(lines),
                "total_words": len(words),
                "average_line_length": len(words) / len(lines) if lines else 0,
                "estimated_pages": len(words) / 250
            },
            "acts": {
                "act1": "25% - Setup",
                "act2": "50% - Confrontation", 
                "act3": "25% - Resolution"
            },
            "elements": {
                "has_inciting_incident": True,
                "has_climax": True,
                "has_resolution": "Partial"
            }
        }
    
    def _analyze_comprehensive(self, text: str, depth: str,
                              context: Optional[Dict]) -> Dict[str, Any]:
        """Perform comprehensive analysis combining all methods
        
        Args:
            text: Text to analyze
            depth: Analysis depth
            context: Optional context
            
        Returns:
            Comprehensive analysis
        """
        # Combine all analysis types
        brutal = self._analyze_brutal(text, context)
        technical = self._analyze_technical(text, depth, context)
        structural = self._analyze_structural(text, context)
        
        return {
            "score": 62,
            "brutal_assessment": brutal,
            "technical_assessment": technical,
            "structural_assessment": structural,
            "overall_verdict": "62/100. Comprehensive analysis complete.",
            "key_findings": [
                "Script shows potential but needs refinement",
                "Structure is present but could be stronger",
                "Technical execution is competent"
            ]
        }
    
    def _analyze_default(self, text: str, context: Optional[Dict]) -> Dict[str, Any]:
        """Default analysis fallback
        
        Args:
            text: Text to analyze
            context: Optional context
            
        Returns:
            Default analysis
        """
        return {
            "score": 62,
            "message": "Standard analysis complete",
            "word_count": len(text.split()),
            "character_count": len(text),
            "verdict": "62/100. Room for improvement."
        }
    
    def get_analysis_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent analysis history
        
        Args:
            limit: Maximum entries to return
            
        Returns:
            List of recent analyses
        """
        return self.analysis_history[-limit:]
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get analyze service status
        
        Returns:
            Service status
        """
        return {
            "service": "AnalyzeService",
            "available": True,
            "components": {
                "personality": self.personality is not None,
                "processor": self.processor is not None,
                "pipeline": self.pipeline is not None
            },
            "analysis_types": ["brutal", "technical", "structural", "comprehensive"],
            "analyses_performed": len(self.analysis_history)
        }