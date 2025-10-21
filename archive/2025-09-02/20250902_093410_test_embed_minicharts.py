# -*- coding: utf-8 -*-
from scripts.embed_minicharts import sparkline, hbars, hist

def test_sparkline_basic():
    svg = sparkline([1.0, 2.0, 1.5, 3.0, 2.5])
    assert '<svg' in svg
    assert 'polyline' in svg
    assert 'circle' in svg  # start/end dots

def test_sparkline_empty():
    svg = sparkline([])
    assert 'n/a' in svg

def test_hbars_basic():
    svg = hbars(['L1', 'L2', 'L3'], [100.0, 250.0, 50.0])
    assert '<svg' in svg
    assert '<rect' in svg
    assert 'L1' in svg and 'L2' in svg and 'L3' in svg

def test_hbars_empty():
    svg = hbars([], [])
    assert 'n/a' in svg

def test_hist_basic():
    svg = hist([0.1, 0.2, 0.15, 0.3, 0.25, 0.35, 0.18])
    assert '<svg' in svg
    assert '<rect' in svg

def test_hist_empty():
    svg = hist([])
    assert 'n/a' in svg

def test_hist_range():
    # valores de 0 a 1 (típico reduction)
    svg = hist([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    assert '<svg' in svg
    assert 'rect' in svg.lower()