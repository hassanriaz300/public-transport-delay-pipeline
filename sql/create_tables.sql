-- Initial database schema for Public Transport Delay Pipeline

CREATE TABLE IF NOT EXISTS stations (
    station_id SERIAL PRIMARY KEY,
    station_name VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transport_delays (
    delay_id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES stations(station_id),
    line_name VARCHAR(50),
    planned_arrival TIMESTAMP,
    actual_arrival TIMESTAMP,
    delay_minutes INTEGER,
    reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Phase 4: Cleaned train delay table

DROP TABLE IF EXISTS cleaned_train_delays;

CREATE TABLE cleaned_train_delays (
    id TEXT,
    line TEXT,
    category INTEGER,
    station TEXT,
    state TEXT,
    city TEXT,
    zip DOUBLE PRECISION,
    long DOUBLE PRECISION,
    lat DOUBLE PRECISION,
    arrival_plan TIMESTAMP,
    departure_plan TIMESTAMP,
    arrival_delay_minutes DOUBLE PRECISION,
    departure_delay_minutes DOUBLE PRECISION,
    arrival_delay_status TEXT,
    departure_delay_status TEXT,
    arrival_date DATE,
    arrival_hour DOUBLE PRECISION,
    departure_date DATE,
    departure_hour INTEGER
);