-- Create the customer_recommendations table for caching LLM recommendations
-- Add this to your database schema

CREATE TABLE IF NOT EXISTS microbiome.customer_recommendations (
    recommendation_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers.customer(customer_id),
    domain_id INTEGER NOT NULL REFERENCES microbiome.health_domains(domain_id),
    
    -- Recommendation content (JSONB for flexibility)
    dietary_recommendations JSONB,
    lifestyle_recommendations JSONB,
    probiotic_recommendations JSONB,
    prebiotic_recommendations JSONB,
    summary TEXT,
    
    -- Metadata
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    model_version VARCHAR(50),
    
    -- Customer context at generation time
    customer_age INTEGER,
    domain_score DECIMAL(3,2),
    domain_diversity DECIMAL(3,2),
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    UNIQUE(customer_id, domain_id, is_active)
);

-- Create indexes for efficient lookups
CREATE INDEX idx_customer_recommendations_lookup 
ON microbiome.customer_recommendations(customer_id, domain_id, is_active);

CREATE INDEX idx_recommendations_expiry 
ON microbiome.customer_recommendations(expires_at);

-- Comments for documentation
COMMENT ON TABLE microbiome.customer_recommendations IS 'Cached LLM-generated personalized recommendations for customers';
COMMENT ON COLUMN microbiome.customer_recommendations.dietary_recommendations IS 'JSONB array of dietary recommendations with rationale and priority';
COMMENT ON COLUMN microbiome.customer_recommendations.lifestyle_recommendations IS 'JSONB array of lifestyle modifications with implementation details';
COMMENT ON COLUMN microbiome.customer_recommendations.probiotic_recommendations IS 'JSONB array of specific probiotic strains with dosages';
COMMENT ON COLUMN microbiome.customer_recommendations.prebiotic_recommendations IS 'JSONB array of prebiotic foods with amounts and sources';
COMMENT ON COLUMN microbiome.customer_recommendations.expires_at IS 'Timestamp when cached recommendations expire (7-14 days)';
COMMENT ON COLUMN microbiome.customer_recommendations.is_active IS 'Only one active recommendation per customer-domain pair';