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