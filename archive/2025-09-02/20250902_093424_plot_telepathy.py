#!/usr/bin/env python
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

p=Path("results/telepathy/telepathy_v2.csv")
if not p.exists():
    print("[WARN] no telepathy_v2.csv"); exit(0)
df=pd.read_csv(p)

Path("reports/figures").mkdir(parents=True, exist_ok=True)
df.to_csv("reports/telepathy_summary.csv", index=False)

plt.figure()
df.plot(x="mode", y="bytes_mean", kind="bar")
plt.ylabel("bytes_mean")
plt.title("Wire payload size (mean)")
plt.savefig("reports/figures/telepathy_bytes_mean.png"); plt.close()

plt.figure()
df.plot(x="mode", y="throughput_msgs_s", kind="bar")
plt.ylabel("msgs/s")
plt.title("Throughput (approx, fakeredis)")
plt.savefig("reports/figures/telepathy_throughput.png"); plt.close()

print("[OK] telepathy plots -> reports/figures & reports/telepathy_summary.csv")