-- Initialize SceneIQ Database Schema

-- Create tables if they don't exist
CREATE TABLE IF NOT EXISTS stores (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    phone VARCHAR(20),
    manager VARCHAR(100),
    opening_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS theft_incidents (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES stores(id),
    timestamp TIMESTAMP NOT NULL,
    severity VARCHAR(20) CHECK (severity IN ('Low', 'Medium', 'High')),
    value NUMERIC(10, 2),
    resolved BOOLEAN DEFAULT FALSE,
    video_clip_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rewards_data (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES stores(id),
    date DATE NOT NULL,
    total_members INTEGER,
    new_members INTEGER,
    campaign_engagement NUMERIC(5, 2),
    active_campaigns INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS campaigns (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES stores(id),
    campaign VARCHAR(100) NOT NULL,
    participation_rate NUMERIC(5, 2),
    redemption_rate NUMERIC(5, 2),
    roi NUMERIC(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS traffic_patterns (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES stores(id),
    date DATE NOT NULL,
    hour INTEGER CHECK (hour >= 0 AND hour < 24),
    foot_traffic INTEGER,
    conversion_rate NUMERIC(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS employee_data (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES stores(id),
    date DATE NOT NULL,
    productivity_score NUMERIC(5, 2),
    attendance_rate NUMERIC(5, 2),
    training_compliance NUMERIC(5, 2),
    customer_satisfaction NUMERIC(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(20) CHECK (role IN ('Owner', 'Manager', 'Employee', 'Admin')),
    store_id INTEGER REFERENCES stores(id),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS business_health (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES stores(id),
    date DATE NOT NULL,
    overall_health NUMERIC(5, 2),
    theft_score NUMERIC(5, 2),
    rewards_score NUMERIC(5, 2),
    traffic_score NUMERIC(5, 2),
    employee_score NUMERIC(5, 2),
    alerts JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_theft_store_id ON theft_incidents(store_id);
CREATE INDEX IF NOT EXISTS idx_theft_timestamp ON theft_incidents(timestamp);
CREATE INDEX IF NOT EXISTS idx_rewards_store_id ON rewards_data(store_id);
CREATE INDEX IF NOT EXISTS idx_rewards_date ON rewards_data(date);
CREATE INDEX IF NOT EXISTS idx_campaigns_store_id ON campaigns(store_id);
CREATE INDEX IF NOT EXISTS idx_traffic_store_id ON traffic_patterns(store_id);
CREATE INDEX IF NOT EXISTS idx_traffic_date ON traffic_patterns(date);
CREATE INDEX IF NOT EXISTS idx_employee_store_id ON employee_data(store_id);
CREATE INDEX IF NOT EXISTS idx_employee_date ON employee_data(date);
CREATE INDEX IF NOT EXISTS idx_health_store_id ON business_health(store_id);
CREATE INDEX IF NOT EXISTS idx_health_date ON business_health(date);