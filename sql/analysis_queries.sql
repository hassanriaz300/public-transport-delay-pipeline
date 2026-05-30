-- Some useful checks and analysis queries for the cleaned train delay table
-- I use these queries to quickly understand the data after loading it into PostgreSQL

-- Check how many rows are available in the table
SELECT COUNT(*) AS total_rows
FROM cleaned_train_delays;

-- Get a quick overview of delay values
SELECT
    COUNT(*) AS total_records,
    ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay,
    ROUND(MIN(arrival_delay_minutes)::numeric, 2) AS min_arrival_delay,
    ROUND(MAX(arrival_delay_minutes)::numeric, 2) AS max_arrival_delay
FROM cleaned_train_delays
WHERE arrival_delay_minutes IS NOT NULL;

-- Find train lines with the highest average arrival delay
-- I only include lines with enough records so the result is more meaningful
SELECT
    line,
    COUNT(*) AS total_records,
    ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay
FROM cleaned_train_delays
WHERE arrival_delay_minutes IS NOT NULL
  AND line IS NOT NULL
GROUP BY line
HAVING COUNT(*) >= 100
ORDER BY avg_arrival_delay DESC
LIMIT 10;

-- Find stations where trains are delayed the most on average
SELECT
    station,
    city,
    state,
    COUNT(*) AS total_records,
    ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay
FROM cleaned_train_delays
WHERE arrival_delay_minutes IS NOT NULL
  AND station IS NOT NULL
GROUP BY station, city, state
HAVING COUNT(*) >= 100
ORDER BY avg_arrival_delay DESC
LIMIT 10;

-- Compare average delays between cities
SELECT
    city,
    COUNT(*) AS total_records,
    ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay
FROM cleaned_train_delays
WHERE arrival_delay_minutes IS NOT NULL
  AND city IS NOT NULL
GROUP BY city
HAVING COUNT(*) >= 100
ORDER BY avg_arrival_delay DESC
LIMIT 10;

-- Check how the average delay changes month by month
SELECT
    DATE_TRUNC('month', arrival_plan)::date AS month,
    COUNT(*) AS total_records,
    ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay
FROM cleaned_train_delays
WHERE arrival_plan IS NOT NULL
  AND arrival_delay_minutes IS NOT NULL
GROUP BY month
ORDER BY month;

-- Check how the average delay changes day by day during the sampled week
SELECT
    DATE(arrival_plan) AS travel_date,
    COUNT(*) AS total_records,
    ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay
FROM cleaned_train_delays
WHERE arrival_plan IS NOT NULL
  AND arrival_delay_minutes IS NOT NULL
GROUP BY travel_date
ORDER BY travel_date;

-- Check delay patterns by hour of day
SELECT
    EXTRACT(HOUR FROM arrival_plan)::int AS hour_of_day,
    COUNT(*) AS total_records,
    ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay
FROM cleaned_train_delays
WHERE arrival_plan IS NOT NULL
  AND arrival_delay_minutes IS NOT NULL
GROUP BY hour_of_day
ORDER BY hour_of_day;