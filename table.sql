CREATE TABLE carbon_footprints (
    id SERIAL PRIMARY KEY,
    miles_driven NUMERIC NOT NULL,
    diet_type VARCHAR(50) NOT NULL,
    energy_usage NUMERIC NOT NULL,
    carbon_footprint NUMERIC NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
