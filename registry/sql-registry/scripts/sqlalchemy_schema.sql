CREATE TABLE IF NOT EXISTS public.entities (
    entity_id UUID NOT NULL PRIMARY KEY,
    qualified_name VARCHAR(200) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    attributes TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS public.edges (
    edge_id VARCHAR(50) NOT NULL PRIMARY KEY,
    from_id VARCHAR(50) NOT NULL,
    to_id VARCHAR(50) NOT NULL,
    conn_type VARCHAR(20) NOT NULL
);
