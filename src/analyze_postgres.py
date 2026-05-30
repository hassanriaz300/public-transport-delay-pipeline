import os

import pandas as pd
from sqlalchemy import create_engine


DB_NAME = os.getenv("POSTGRES_DB", "transport_delay_db")
DB_USER = os.getenv("POSTGRES_USER", "hassan")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")


def get_engine():
    """
    Create a database engine for PostgreSQL.
    The default values are for my local development database.
    """
    if DB_PASSWORD:
        database_url = (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
            f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        database_url = f"postgresql+psycopg2://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    return create_engine(database_url)


def run_query(query):
    """
    Run a SQL query and return the result as a pandas DataFrame.
    """
    engine = get_engine()
    return pd.read_sql_query(query, engine)


def print_section(title):
    """
    Print a clear heading before each result.
    """
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main():
    print_section("Total rows in PostgreSQL table")
    total_rows = run_query("""
        SELECT COUNT(*) AS total_rows
        FROM cleaned_train_delays;
    """)
    print(total_rows.to_string(index=False))

    print_section("Basic delay statistics")
    delay_stats = run_query("""
        SELECT
            COUNT(*) AS total_records,
            ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay,
            ROUND(MIN(arrival_delay_minutes)::numeric, 2) AS min_arrival_delay,
            ROUND(MAX(arrival_delay_minutes)::numeric, 2) AS max_arrival_delay
        FROM cleaned_train_delays
        WHERE arrival_delay_minutes IS NOT NULL;
    """)
    print(delay_stats.to_string(index=False))

    print_section("Top 10 train lines by average arrival delay")
    top_lines = run_query("""
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
    """)
    print(top_lines.to_string(index=False))

    print_section("Top 10 stations by average arrival delay")
    top_stations = run_query("""
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
    """)
    print(top_stations.to_string(index=False))

    print_section("Top 10 cities by average arrival delay")
    top_cities = run_query("""
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
    """)
    print(top_cities.to_string(index=False))

    print_section("Average delay by day")
    daily_delay = run_query("""
    SELECT
        DATE(arrival_plan) AS travel_date,
        COUNT(*) AS total_records,
        ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay
        FROM cleaned_train_delays
        WHERE arrival_plan IS NOT NULL
            AND arrival_delay_minutes IS NOT NULL
        GROUP BY travel_date
        ORDER BY travel_date;
    """)
    print(daily_delay.to_string(index=False))

    print_section("Average delay by hour of day")
    hourly_delay = run_query("""
        SELECT
            EXTRACT(HOUR FROM arrival_plan)::int AS hour_of_day,
            COUNT(*) AS total_records,
            ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay
        FROM cleaned_train_delays
        WHERE arrival_plan IS NOT NULL
          AND arrival_delay_minutes IS NOT NULL
        GROUP BY hour_of_day
        ORDER BY hour_of_day;
    """)
    print(hourly_delay.to_string(index=False))


if __name__ == "__main__":
    main()