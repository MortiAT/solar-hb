CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE sensor_data (
    time            TIMESTAMPTZ NOT NULL,
    p_akku          DOUBLE PRECISION NOT NULL,
    p_grid          DOUBLE PRECISION NOT NULL,
    p_load          DOUBLE PRECISION NOT NULL,
    p_pv            DOUBLE PRECISION NOT NULL,
    relative_charge DOUBLE PRECISION NOT NULL
);

-- convert to hypertable
SELECT create_hypertable('sensor_data', by_range('time', INTERVAL '1 month'));