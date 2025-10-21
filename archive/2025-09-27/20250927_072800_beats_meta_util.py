def build_beats_meta(beats):
    index_map = {}; weights = []; by_scene = {}
    for i, b in enumerate(beats):
        index_map[b.id] = i; weights.append(float(getattr(b, 'weight', 1.0)))
        by_scene.setdefault(str(b.scene_index), []).append({'beat_id': b.id, 'global_index': i})
    return {'total_beats': len(beats), 'index_map': index_map, 'weights': weights, 'by_scene': by_scene}
