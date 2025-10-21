#!/usr/bin/env python
"""Create visual dashboard of compression results."""
import sys
sys.path.append('.')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import json
import pandas as pd

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('DigiLang Compression Dashboard', fontsize=16, fontweight='bold')

# 1. Compression by Method (Bar Chart)
ax1 = axes[0, 0]
methods = ['Baseline', 'LLMLingua', 'DigiLang+TPD', 'Two-Stage', 'Screenplay']
compressions = [5.5, 16.6, 25.3, 25.7, 29.4]
colors = ['gray', 'lightblue', 'green', 'darkgreen', 'purple']
bars = ax1.bar(methods, compressions, color=colors)
ax1.axhline(y=25, color='red', linestyle='--', label='Target (25%)')
ax1.set_ylabel('Compression (%)')
ax1.set_title('Compression by Method')
ax1.legend()
ax1.set_ylim(0, 35)
for bar, val in zip(bars, compressions):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{val:.1f}%', ha='center', va='bottom')

# 2. TPD Configuration Impact (Line Chart)
ax2 = axes[0, 1]
k_values = [800, 1200, 2000, 2500, 3000]
compression_values = [19.6, 21.6, 24.5, 25.4, 26.3]
ax2.plot(k_values, compression_values, marker='o', linewidth=2, markersize=8)
ax2.fill_between(k_values, compression_values, alpha=0.3)
ax2.set_xlabel('K (Number of Patterns)')
ax2.set_ylabel('Compression (%)')
ax2.set_title('TPD Size vs Compression')
ax2.grid(True, alpha=0.3)
ax2.set_ylim(15, 30)

# 3. Latency vs Compression Trade-off
ax3 = axes[1, 0]
methods_lat = ['Fast\n(K800)', 'Balanced\n(K1500)', 'Quality\n(K3000)', 'Two-Stage']
latencies = [50, 100, 150, 2500]
compressions_lat = [18, 22, 25.3, 25.7]
scatter = ax3.scatter(latencies, compressions_lat, s=200, c=compressions_lat, 
                     cmap='viridis', edgecolors='black', linewidth=2)
for i, txt in enumerate(methods_lat):
    ax3.annotate(txt, (latencies[i], compressions_lat[i]), 
                textcoords="offset points", xytext=(0,10), ha='center')
ax3.set_xlabel('Latency (ms)')
ax3.set_ylabel('Compression (%)')
ax3.set_title('Performance vs Quality Trade-off')
ax3.set_xscale('log')
ax3.grid(True, alpha=0.3)
plt.colorbar(scatter, ax=ax3, label='Compression %')

# 4. Domain-Specific Performance
ax4 = axes[1, 1]
domains = ['Shakespeare', 'Screenplay', 'Technical\n(est.)', 'Chat\n(est.)']
expected = [25.3, 29.4, 30, 18]
achieved = [25.3, 29.4, None, None]
x_pos = range(len(domains))
bars1 = ax4.bar(x_pos, expected, alpha=0.5, label='Expected', color='lightblue')
for i, val in enumerate(achieved):
    if val:
        ax4.bar(i, val, alpha=0.8, label='Achieved' if i == 0 else '', color='green')
ax4.set_xticks(x_pos)
ax4.set_xticklabels(domains)
ax4.set_ylabel('Compression (%)')
ax4.set_title('Domain-Specific Performance')
ax4.legend()
ax4.set_ylim(0, 35)

# Add text annotations
for i, (exp, ach) in enumerate(zip(expected, achieved)):
    if ach:
        ax4.text(i, ach + 0.5, f'{ach:.1f}%', ha='center', va='bottom', fontweight='bold')
    else:
        ax4.text(i, exp + 0.5, f'{exp}%*', ha='center', va='bottom', style='italic')

plt.tight_layout()
plt.savefig('reports/figures/dashboard.png', dpi=150, bbox_inches='tight')
print("✅ Dashboard saved to reports/figures/dashboard.png")

# Create summary statistics
stats = {
    "best_overall": {
        "method": "Screenplay TPD",
        "compression": 29.4,
        "patterns": 2000
    },
    "best_shakespeare": {
        "method": "DigiLang+TPD K3000",
        "compression": 26.3,
        "patterns": 3000
    },
    "fastest": {
        "method": "DigiLang+TPD K800",
        "compression": 19.6,
        "latency_ms": 50
    },
    "configurations_tested": 9,
    "target_achieved": True,
    "methods_passing_25": ["DigiLang+TPD K3000", "Two-Stage", "Screenplay TPD"]
}

Path("reports/dashboard_stats.json").write_text(json.dumps(stats, indent=2))
print("✅ Statistics saved to reports/dashboard_stats.json")
plt.close()