-- HARMONIA V3.2 - SQLite Migrations
-- Otimizações e índices para sistema de memória robusto
-- Idempotente: pode ser executado múltiplas vezes sem problemas

-- ============================================
-- 1. ÍNDICES PARA TABELA memories
-- ============================================

-- Índice para busca por tipo de camada (kind)
CREATE INDEX IF NOT EXISTS idx_memories_kind 
ON memories(kind);

-- Índice para ordenação por último acesso
CREATE INDEX IF NOT EXISTS idx_memories_last_accessed 
ON memories(last_accessed DESC);

-- Índice para ordenação por criação
CREATE INDEX IF NOT EXISTS idx_memories_created_at 
ON memories(created_at DESC);

-- Índice para ranking por hits (acessos frequentes)
CREATE INDEX IF NOT EXISTS idx_memories_hits 
ON memories(hits DESC);

-- Índice composto para ranking híbrido
CREATE INDEX IF NOT EXISTS idx_memories_ranking 
ON memories(importance DESC, hits DESC, last_accessed DESC);

-- Índice para busca por tags (se campo TEXT com JSON)
CREATE INDEX IF NOT EXISTS idx_memories_tags 
ON memories(tags);

-- ============================================
-- 2. ÍNDICES PARA CAMADAS L1-L4
-- ============================================

-- L1_core: índices para memórias críticas
CREATE INDEX IF NOT EXISTS idx_l1_importance 
ON L1_core(importance DESC, access_count DESC);

CREATE INDEX IF NOT EXISTS idx_l1_access 
ON L1_core(last_access DESC);

-- L2_consolidated: índices para memórias consolidadas
CREATE INDEX IF NOT EXISTS idx_l2_importance 
ON L2_consolidated(importance DESC, consolidation_count DESC);

CREATE INDEX IF NOT EXISTS idx_l2_consolidated 
ON L2_consolidated(consolidated_at DESC);

-- L3_active: índices para memórias ativas
CREATE INDEX IF NOT EXISTS idx_l3_ttl 
ON L3_active(expires_at);

CREATE INDEX IF NOT EXISTS idx_l3_session 
ON L3_active(session_id, importance DESC);

-- L4_quantum: índices para padrões quânticos
CREATE INDEX IF NOT EXISTS idx_l4_emergence 
ON L4_quantum(emergence_score DESC);

CREATE INDEX IF NOT EXISTS idx_l4_observations 
ON L4_quantum(observations DESC, last_collapse DESC);

-- ============================================
-- 3. TRIGGERS PARA PROMOÇÃO AUTOMÁTICA
-- ============================================

-- Trigger para atualizar last_accessed automaticamente
CREATE TRIGGER IF NOT EXISTS update_last_accessed
AFTER UPDATE ON memories
WHEN NEW.hits > OLD.hits
BEGIN
    UPDATE memories 
    SET last_accessed = datetime('now')
    WHERE id = NEW.id;
END;

-- Trigger para promoção L3→L2 baseada em importância e hits
CREATE TRIGGER IF NOT EXISTS promote_l3_to_l2
AFTER UPDATE ON memories
WHEN NEW.kind = 'L3' 
    AND NEW.importance >= 0.7 
    AND NEW.hits >= 10
BEGIN
    UPDATE memories 
    SET kind = 'L2',
        importance = MIN(1.0, NEW.importance * 1.1)
    WHERE id = NEW.id;
END;

-- Trigger para promoção L2→L1 (memórias ultra-importantes)
CREATE TRIGGER IF NOT EXISTS promote_l2_to_l1
AFTER UPDATE ON memories
WHEN NEW.kind = 'L2' 
    AND NEW.importance >= 0.9 
    AND NEW.hits >= 50
BEGIN
    UPDATE memories 
    SET kind = 'L1',
        importance = 1.0
    WHERE id = NEW.id;
END;

-- ============================================
-- 4. VIEWS PARA ANÁLISE E RANKING
-- ============================================

-- View para ranking híbrido com pesos configuráveis
CREATE VIEW IF NOT EXISTS v_memory_ranking AS
SELECT 
    id,
    content,
    kind,
    importance,
    hits,
    last_accessed,
    created_at,
    -- Ranking híbrido: α*importance + β*normalized_hits + γ*recency + δ*layer_weight
    (
        0.4 * importance +  -- α = 0.4
        0.3 * MIN(1.0, CAST(hits AS REAL) / 100.0) +  -- β = 0.3, normalizado até 100 hits
        0.2 * (1.0 - MIN(1.0, (julianday('now') - julianday(last_accessed)) / 30.0)) +  -- γ = 0.2, decay em 30 dias
        0.1 * CASE  -- δ = 0.1, peso por camada
            WHEN kind = 'L1' THEN 1.0
            WHEN kind = 'L2' THEN 0.7
            WHEN kind = 'L3' THEN 0.4
            WHEN kind = 'L4' THEN 0.1
            ELSE 0.5
        END
    ) AS hybrid_score
FROM memories
ORDER BY hybrid_score DESC;

-- View para memórias candidatas à promoção
CREATE VIEW IF NOT EXISTS v_promotion_candidates AS
SELECT 
    id,
    content,
    kind,
    importance,
    hits,
    CASE
        WHEN kind = 'L3' AND importance >= 0.6 AND hits >= 5 THEN 'Ready for L2'
        WHEN kind = 'L2' AND importance >= 0.8 AND hits >= 25 THEN 'Ready for L1'
        WHEN kind = 'L4' AND importance >= 0.5 AND hits >= 3 THEN 'Ready for L3'
        ELSE 'Not ready'
    END AS promotion_status
FROM memories
WHERE kind != 'L1'
    AND (
        (kind = 'L3' AND importance >= 0.6 AND hits >= 5) OR
        (kind = 'L2' AND importance >= 0.8 AND hits >= 25) OR
        (kind = 'L4' AND importance >= 0.5 AND hits >= 3)
    )
ORDER BY importance DESC, hits DESC;

-- ============================================
-- 5. FUNÇÕES AUXILIARES (via PRAGMA)
-- ============================================

-- Habilitar WAL mode para melhor concorrência
PRAGMA journal_mode = WAL;

-- Configurar timeout para locks (5 segundos)
PRAGMA busy_timeout = 5000;

-- Análise e otimização automática
ANALYZE;

-- ============================================
-- 6. TABELA DE METADADOS PARA CONFIGURAÇÃO
-- ============================================

CREATE TABLE IF NOT EXISTS memory_config (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir configurações padrão (idempotente)
INSERT OR REPLACE INTO memory_config (key, value) VALUES
    ('ranking_alpha', '0.4'),  -- Peso da importância
    ('ranking_beta', '0.3'),   -- Peso dos hits
    ('ranking_gamma', '0.2'),  -- Peso da recência
    ('ranking_delta', '0.1'),  -- Peso da camada
    ('ranking_epsilon', '0.0'), -- Reservado para extensão
    ('promotion_l3_to_l2_importance', '0.7'),
    ('promotion_l3_to_l2_hits', '10'),
    ('promotion_l2_to_l1_importance', '0.9'),
    ('promotion_l2_to_l1_hits', '50'),
    ('decay_days', '30'),
    ('normalization_hits', '100');

-- ============================================
-- 7. ESTATÍSTICAS E MONITORAMENTO
-- ============================================

CREATE VIEW IF NOT EXISTS v_memory_stats AS
SELECT 
    kind,
    COUNT(*) as total_memories,
    AVG(importance) as avg_importance,
    AVG(hits) as avg_hits,
    MAX(hits) as max_hits,
    MIN(created_at) as oldest_memory,
    MAX(last_accessed) as most_recent_access
FROM memories
GROUP BY kind;

-- ============================================
-- CONCLUSÃO
-- ============================================
-- Migrations aplicadas com sucesso!
-- Sistema de memória otimizado para:
-- - Busca rápida por índices especializados
-- - Ranking híbrido configurável
-- - Promoção automática entre camadas
-- - Melhor concorrência com WAL mode
-- - Monitoramento via views estatísticas