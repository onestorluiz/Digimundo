#!/usr/bin/env python3
"""
Test GPU/CPU balance for Token Turbo models
"""

import subprocess
import time
import psutil
import json
from datetime import datetime

TEST_PROMPT = """Analyze the hero's journey in The Matrix screenplay using Joseph Campbell's monomyth structure.
Provide specific examples from the screenplay for each stage of the journey."""

def get_cpu_usage():
    """Get current CPU usage percentage"""
    return psutil.cpu_percent(interval=1)

def get_gpu_usage():
    """Try to get GPU usage (Mac specific)"""
    try:
        # Using powermetrics requires sudo
        result = subprocess.run(
            ["sudo", "powermetrics", "--samplers", "gpu_power", "-n", "1", "-f", "json"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            # Extract GPU usage from powermetrics
            return data.get("gpu", {}).get("utilization_percentage", 0)
    except:
        pass
    return -1  # Unable to get GPU usage

def test_model(model_name, iterations=3):
    """Test a model and measure CPU/GPU usage"""
    print(f"\n{'='*60}")
    print(f"Testing: {model_name}")
    print(f"{'='*60}")

    cpu_samples = []
    response_times = []

    for i in range(iterations):
        print(f"\n Iteration {i+1}/{iterations}")

        # Start monitoring CPU before the request
        cpu_before = get_cpu_usage()

        # Run the model
        start_time = time.time()

        # Start the ollama process
        process = subprocess.Popen(
            ["ollama", "run", model_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Monitor CPU while running
        cpu_during = []
        stdout, stderr = process.communicate(input=TEST_PROMPT, timeout=30)

        # Sample CPU during execution
        for _ in range(5):  # Sample 5 times
            cpu_during.append(get_cpu_usage())
            time.sleep(0.5)

        end_time = time.time()
        response_time = end_time - start_time

        # Get CPU after
        cpu_after = get_cpu_usage()

        # Calculate average CPU during execution
        avg_cpu = sum(cpu_during) / len(cpu_during) if cpu_during else 0

        print(f"   CPU before: {cpu_before:.1f}%")
        print(f"   CPU during: {avg_cpu:.1f}%")
        print(f"   CPU after: {cpu_after:.1f}%")
        print(f"   Response time: {response_time:.2f}s")

        cpu_samples.append(avg_cpu)
        response_times.append(response_time)

    # Calculate averages
    avg_cpu_usage = sum(cpu_samples) / len(cpu_samples)
    avg_response_time = sum(response_times) / len(response_times)

    return {
        "model": model_name,
        "avg_cpu": avg_cpu_usage,
        "avg_time": avg_response_time,
        "cpu_samples": cpu_samples,
        "times": response_times
    }

def main():
    print("🚀 TOKEN TURBO GPU/CPU BALANCE TEST")
    print(f"Time: {datetime.now().isoformat()}")
    print(f"System: Mac Studio M3 Ultra - 28 CPU cores, 60 GPU cores, 32 Neural cores")

    # Models to test
    models = [
        ("token-turbo-gpu30", "GPU 30 - More CPU"),
        ("token-turbo-gpu40", "GPU 40 - Balanced"),
        ("mixtral-token-turbo:latest", "GPU 50 - ECO optimized"),
        ("token-turbo-gpu60", "GPU 60 - More GPU"),
    ]

    results = []

    for model_name, description in models:
        print(f"\n\n{'#'*60}")
        print(f"# {description}")
        print(f"{'#'*60}")

        result = test_model(model_name, iterations=2)
        result["description"] = description
        results.append(result)

        # Cool down between models
        time.sleep(5)

    # Summary
    print(f"\n\n{'='*60}")
    print("SUMMARY - CPU Usage Comparison")
    print(f"{'='*60}")

    for r in sorted(results, key=lambda x: x["avg_cpu"], reverse=True):
        print(f"\n{r['description']}")
        print(f"  Model: {r['model']}")
        print(f"  Avg CPU: {r['avg_cpu']:.1f}%")
        print(f"  Avg Time: {r['avg_time']:.2f}s")
        print(f"  CPU samples: {[f'{c:.1f}%' for c in r['cpu_samples']]}")

    # Find best balance
    print(f"\n\n{'='*60}")
    print("RECOMMENDATION")
    print(f"{'='*60}")

    # Best CPU usage (should be > 20%)
    best_cpu = max(results, key=lambda x: x["avg_cpu"])
    print(f"\n✅ Best CPU usage: {best_cpu['description']}")
    print(f"   {best_cpu['avg_cpu']:.1f}% CPU utilization")

    # Best speed
    best_speed = min(results, key=lambda x: x["avg_time"])
    print(f"\n⚡ Fastest: {best_speed['description']}")
    print(f"   {best_speed['avg_time']:.2f}s average response time")

    # Best balance (CPU > 20% and good speed)
    balanced = [r for r in results if r["avg_cpu"] > 20]
    if balanced:
        best_balanced = min(balanced, key=lambda x: x["avg_time"])
        print(f"\n🎯 Best Balance: {best_balanced['description']}")
        print(f"   {best_balanced['avg_cpu']:.1f}% CPU, {best_balanced['avg_time']:.2f}s response")

    # Save results
    with open("gpu_cpu_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n📊 Results saved to gpu_cpu_test_results.json")

if __name__ == "__main__":
    main()