#!/usr/bin/env python3
"""
Probe Ollama model layers for optimal GPU offloading configuration
"""

import subprocess
import json
import re
import sys
from pathlib import Path
from typing import Dict, Optional

def probe_model_layers(model_name: str) -> Dict:
    """
    Probe a model to determine number of layers available for GPU offloading
    
    Returns:
        Dict with model info and layer counts
    """
    print(f"🔍 Probing model: {model_name}")
    
    result = {
        "model": model_name,
        "total_layers": None,
        "gpu_layers_detected": None,
        "suggested_gpu_stable": None,
        "suggested_hybrid": None,
        "raw_output": "",
        "error": None
    }
    
    try:
        # Run ollama with debug logging to detect layers
        env = {
            "OLLAMA_LOG_LEVEL": "debug"
        }
        
        # Simple prompt to trigger model load
        cmd = ["ollama", "run", model_name, "--verbose"]
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**subprocess.os.environ, **env}
        )
        
        # Send minimal prompt and capture output
        stdout, stderr = process.communicate(input="ok\nexit\n", timeout=30)
        
        # Combine outputs for parsing
        full_output = stdout + stderr
        result["raw_output"] = full_output[:2000]  # First 2000 chars for debugging
        
        # Parse for layer information
        # Pattern 1: "offloading XX repeating layers to GPU"
        pattern1 = r"offloading\s+(\d+)\s+repeating layers to GPU"
        match1 = re.search(pattern1, full_output, re.IGNORECASE)
        
        # Pattern 2: "llm_load_tensors: offloading XX repeating layers"
        pattern2 = r"llm_load_tensors.*offloading\s+(\d+)\s+repeating"
        match2 = re.search(pattern2, full_output, re.IGNORECASE)
        
        # Pattern 3: Look for total layers info
        pattern3 = r"(\d+)\s+layers?\s+total"
        match3 = re.search(pattern3, full_output, re.IGNORECASE)
        
        # Pattern 4: Alternative - "ggml_metal_add_buffer" mentions
        pattern4 = r"ggml_metal_add_buffer.*n_layers\s*=\s*(\d+)"
        match4 = re.search(pattern4, full_output, re.IGNORECASE)
        
        if match1:
            result["gpu_layers_detected"] = int(match1.group(1))
        elif match2:
            result["gpu_layers_detected"] = int(match2.group(1))
            
        if match3:
            result["total_layers"] = int(match3.group(1))
        elif match4:
            result["total_layers"] = int(match4.group(1))
        
        # If we couldn't detect, try to infer from model size
        if result["total_layers"] is None:
            # Common layer counts for different model sizes
            size_patterns = {
                "70b": 80,  # Typical for 70B models
                "32b": 48,  # Typical for 32B models  
                "13b": 40,  # Typical for 13B models
                "7b": 32,   # Typical for 7B models
                "3b": 26,   # Typical for 3B models
                "2b": 18,   # Typical for 2B models
            }
            
            for size, layers in size_patterns.items():
                if size in model_name.lower():
                    result["total_layers"] = layers
                    print(f"  Inferred {layers} layers based on model size {size}")
                    break
        
        # Calculate suggestions
        if result["total_layers"]:
            total = result["total_layers"]
            # GPU stable: all layers minus 1 (keep 1 on CPU for stability)
            result["suggested_gpu_stable"] = max(1, total - 1)
            # Hybrid: approximately 2/3 of layers
            result["suggested_hybrid"] = max(1, int(total * 0.66))
        elif result["gpu_layers_detected"]:
            # Use detected value as reference
            detected = result["gpu_layers_detected"]
            result["suggested_gpu_stable"] = detected
            result["suggested_hybrid"] = max(1, int(detected * 0.66))
        
    except subprocess.TimeoutExpired:
        result["error"] = "Timeout while probing model"
    except Exception as e:
        result["error"] = str(e)
    
    return result

def probe_available_models() -> Dict:
    """
    Probe all available models and determine optimal configurations
    """
    results = {
        "probed_models": {},
        "primary_model": None,
        "recommendations": {}
    }
    
    # Get list of available models
    try:
        cmd_result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if cmd_result.returncode == 0:
            lines = cmd_result.stdout.strip().split('\n')
            models = []
            for line in lines[1:]:  # Skip header
                if line:
                    model_name = line.split()[0]
                    models.append(model_name)
            
            print(f"📦 Found {len(models)} models")
            
            # Probe each model (focusing on larger ones)
            priority_models = ["deepseek-r1:32b", "deepseek-r1:70b", "deepseek-r1:7b", 
                             "mistral:instruct", "llama3.2:3b"]
            
            for model in models:
                # Skip if not in priority list for speed
                base_model = model.split(':')[0]
                if any(p.startswith(base_model) for p in priority_models):
                    print(f"\n🔬 Probing {model}...")
                    probe_result = probe_model_layers(model)
                    results["probed_models"][model] = probe_result
                    
                    # Set primary model (first successful probe)
                    if not results["primary_model"] and not probe_result["error"]:
                        results["primary_model"] = model
    
    except Exception as e:
        print(f"❌ Error listing models: {e}")
    
    # Generate recommendations
    if results["primary_model"] and results["primary_model"] in results["probed_models"]:
        primary_probe = results["probed_models"][results["primary_model"]]
        
        if primary_probe["suggested_gpu_stable"]:
            results["recommendations"] = {
                "primary_model": results["primary_model"],
                "gpu_stable_layers": primary_probe["suggested_gpu_stable"],
                "hybrid_layers": primary_probe["suggested_hybrid"],
                "cpu_layers": 0,
                "notes": f"Based on {results['primary_model']} with estimated {primary_probe.get('total_layers', 'unknown')} total layers"
            }
    
    return results

def main():
    """Main probe execution"""
    print("="*60)
    print("🎯 OLLAMA LAYERS PROBE")
    print("="*60)
    
    # Run probe
    results = probe_available_models()
    
    # Save results
    output_path = Path("reports/harmony_vFinal/phase4_ollama/layers_probe.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 Results saved to: {output_path}")
    
    # Print summary
    if results["recommendations"]:
        rec = results["recommendations"]
        print("\n" + "="*60)
        print("📋 RECOMMENDATIONS")
        print("="*60)
        print(f"Primary Model: {rec['primary_model']}")
        print(f"GPU Stable: {rec['gpu_stable_layers']} layers")
        print(f"Hybrid: {rec['hybrid_layers']} layers")
        print(f"CPU Only: {rec['cpu_layers']} layers")
        print(f"Notes: {rec['notes']}")
    
    return results

if __name__ == "__main__":
    main()