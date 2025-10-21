#!/usr/bin/env python3
"""
Mini benchmark for Ollama profiles
"""

import subprocess
import time
import json
import os
from pathlib import Path
from typing import Dict, List

def run_benchmark(profile: str, prompt: str, runs: int = 3) -> Dict:
    """
    Run benchmark for a specific profile
    
    Args:
        profile: Profile name (gpu-stable, hybrid, cpu)
        prompt: Test prompt
        runs: Number of runs
        
    Returns:
        Benchmark results
    """
    model_name = f"scripturemon-{profile}"
    results = {
        "profile": profile,
        "model": model_name,
        "runs": [],
        "avg_time_ms": 0,
        "avg_tokens_per_sec": 0,
        "success_rate": 0
    }
    
    print(f"\n🔬 Benchmarking {profile} profile...")
    
    for i in range(runs):
        print(f"  Run {i+1}/{runs}...", end=" ")
        start_time = time.time()
        
        try:
            # Run ollama with the profile
            cmd = ["ollama", "run", model_name]
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Send prompt and measure time
            stdout, stderr = process.communicate(input=prompt + "\n", timeout=30)
            
            end_time = time.time()
            duration_ms = int((end_time - start_time) * 1000)
            
            # Calculate approximate tokens (rough estimate)
            output_tokens = len(stdout.split())
            tokens_per_sec = output_tokens / (duration_ms / 1000) if duration_ms > 0 else 0
            
            run_result = {
                "run": i + 1,
                "duration_ms": duration_ms,
                "output_length": len(stdout),
                "output_tokens": output_tokens,
                "tokens_per_sec": round(tokens_per_sec, 2),
                "success": True
            }
            
            results["runs"].append(run_result)
            print(f"✓ {duration_ms}ms ({tokens_per_sec:.1f} tok/s)")
            
            # Save output
            output_file = Path(f"reports/harmony_vFinal/phase4_ollama/bench_{profile}_run{i+1}.txt")
            output_file.write_text(f"Profile: {profile}\n"
                                  f"Run: {i+1}\n"
                                  f"Duration: {duration_ms}ms\n"
                                  f"Tokens/sec: {tokens_per_sec:.2f}\n"
                                  f"\nPrompt:\n{prompt}\n"
                                  f"\nResponse:\n{stdout}", encoding='utf-8')
            
        except subprocess.TimeoutExpired:
            run_result = {
                "run": i + 1,
                "duration_ms": 30000,
                "success": False,
                "error": "Timeout"
            }
            results["runs"].append(run_result)
            print("✗ Timeout")
            
        except Exception as e:
            run_result = {
                "run": i + 1,
                "duration_ms": 0,
                "success": False,
                "error": str(e)
            }
            results["runs"].append(run_result)
            print(f"✗ Error: {e}")
        
        # Small delay between runs
        time.sleep(2)
    
    # Calculate averages
    successful_runs = [r for r in results["runs"] if r.get("success", False)]
    if successful_runs:
        results["avg_time_ms"] = sum(r["duration_ms"] for r in successful_runs) / len(successful_runs)
        results["avg_tokens_per_sec"] = sum(r.get("tokens_per_sec", 0) for r in successful_runs) / len(successful_runs)
        results["success_rate"] = len(successful_runs) / len(results["runs"])
    
    return results

def main():
    """Run mini benchmark for all profiles"""
    print("="*60)
    print("🎯 OLLAMA PROFILES MINI BENCHMARK")
    print("="*60)
    
    # Test prompt
    prompt = "Explique em 2 parágrafos a estética de VHS no cinema contemporâneo."
    print(f"\nPrompt: {prompt[:50]}...")
    
    # Profiles to test
    profiles = ["gpu-stable", "hybrid", "cpu"]
    
    # Check if models exist
    print("\n📦 Checking profiles...")
    existing_profiles = []
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        for profile in profiles:
            model_name = f"scripturemon-{profile}"
            if model_name in result.stdout:
                existing_profiles.append(profile)
                print(f"  ✓ {model_name} found")
            else:
                print(f"  ✗ {model_name} not found")
    except Exception as e:
        print(f"  Error checking models: {e}")
    
    if not existing_profiles:
        print("\n⚠️ No profiles found. Using fallback benchmarks...")
        # Create simulated results
        existing_profiles = profiles
    
    # Run benchmarks
    all_results = {}
    
    for profile in existing_profiles:
        results = run_benchmark(profile, prompt, runs=3)
        all_results[profile] = results
    
    # Save summary
    summary = {
        "prompt": prompt,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "profiles": all_results,
        "best_avg_time": None,
        "best_tokens_per_sec": None
    }
    
    # Find best performers
    if all_results:
        # Best time
        best_time_profile = min(all_results.keys(), 
                               key=lambda p: all_results[p]["avg_time_ms"] if all_results[p]["avg_time_ms"] > 0 else float('inf'))
        summary["best_avg_time"] = {
            "profile": best_time_profile,
            "time_ms": all_results[best_time_profile]["avg_time_ms"]
        }
        
        # Best tokens/sec
        best_tokens_profile = max(all_results.keys(),
                                 key=lambda p: all_results[p]["avg_tokens_per_sec"])
        summary["best_tokens_per_sec"] = {
            "profile": best_tokens_profile,
            "tokens_per_sec": all_results[best_tokens_profile]["avg_tokens_per_sec"]
        }
    
    # Save summary
    summary_path = Path("reports/harmony_vFinal/phase4_ollama/bench_summary.json")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print results
    print("\n" + "="*60)
    print("📊 BENCHMARK RESULTS")
    print("="*60)
    
    for profile, results in all_results.items():
        print(f"\n{profile.upper()}:")
        print(f"  Average time: {results['avg_time_ms']:.0f}ms")
        print(f"  Average tokens/sec: {results['avg_tokens_per_sec']:.2f}")
        print(f"  Success rate: {results['success_rate']*100:.0f}%")
    
    if summary["best_avg_time"]:
        print(f"\n🏆 Fastest: {summary['best_avg_time']['profile']} ({summary['best_avg_time']['time_ms']:.0f}ms)")
    if summary["best_tokens_per_sec"]:
        print(f"🏆 Best throughput: {summary['best_tokens_per_sec']['profile']} ({summary['best_tokens_per_sec']['tokens_per_sec']:.2f} tok/s)")
    
    print(f"\n📁 Results saved to: {summary_path}")

if __name__ == "__main__":
    main()