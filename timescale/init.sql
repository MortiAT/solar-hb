CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS sensor_data (
    time            TIMESTAMPTZ NOT NULL,
    p_akku          DOUBLE PRECISION NOT NULL,
    p_grid          DOUBLE PRECISION NOT NULL,
    p_load          DOUBLE PRECISION NOT NULL,
    p_pv            DOUBLE PRECISION NOT NULL,
    relative_charge DOUBLE PRECISION NOT NULL
);

-- convert to hypertable
SELECT create_hypertable('sensor_data', by_range('time', INTERVAL '1 month'));

CREATE USER reader IN GROUP pg_read_all_data;

CREATE OR REPLACE FUNCTION get_sensor_data_for_day(day_str text)
RETURNS SETOF sensor_data
LANGUAGE sql
AS $$
  SELECT *
  FROM sensor_data
  WHERE time >= day_str::date
    AND time < day_str::date + INTERVAL '1 day'
  ORDER BY time;
$$;

GRANT EXECUTE ON FUNCTION get_sensor_data_for_day(day_str text) TO reader;

CREATE OR REPLACE FUNCTION get_sensor_data_date_range()
RETURNS TABLE (earliest_date date, latest_date date)
LANGUAGE sql
AS $$
  SELECT MIN(time)::date, MAX(time)::date
  FROM sensor_data;
$$;

GRANT EXECUTE ON FUNCTION get_sensor_data_date_range() TO reader;

CREATE OR REPLACE FUNCTION get_sensor_data_for_range(day_start text, day_end text)
RETURNS SETOF sensor_data
LANGUAGE sql
AS $$
  SELECT *
  FROM sensor_data
  WHERE time >= day_start::date
    AND time <= day_end::date
  ORDER BY time;
$$;

GRANT EXECUTE ON FUNCTION get_sensor_data_for_range(day_start text, day_end text) TO reader;