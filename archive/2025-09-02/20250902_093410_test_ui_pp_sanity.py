# -*- coding: utf-8 -*-
from scripts.embed_minicharts import heatmap_grid
from scripts.aggregate_perf import rollup
def test_heatmap_basic():
    svg = heatmap_grid(["a","b"], ["ds1","ds2"], [[10,20],[30,0]])
    assert "<svg" in svg and "rect" in svg
def test_rollup_tolerant():
    data = rollup()
    assert "latency_ms" in data and "throughput_rps" in data