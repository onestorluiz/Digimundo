#!/usr/bin/env python
import itertools, subprocess, os, time
Ks=[800,1200,2000]
Ns=[(2,6),(2,8)]
for K in Ks:
  for nmin,nmax in Ns:
    outdir=f"data/tpd/K{K}_n{nmin}-{nmax}"
    cmd=f"./.venv/bin/python scripts/build_tpd_adaptive.py --corpus data/original --outdir {outdir} --K {K} --nmin {nmin} --nmax {nmax} --fmin 3"
    print(">>",cmd); os.system(cmd)