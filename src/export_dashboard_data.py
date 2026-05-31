import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


DB_NAME = os.getenv("POSTGRES_DB", "transport_delay_db")
DB_USER = os.getenv("POSTGRES_USER", "hassan")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

OUTPUT_DIR = Path("dashboard_data")


def get_engine():
    """
    Create a database engine for PostgreSQL.
    Uses the same connection style as the Phase 5 analysis script.
    """
    if DB_PASSWORD:
        database_url = (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
            f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        database_url = f"postgresql+psycopg2://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    return create_engine(database_url)


def export_query(engine, query: str, filename: str):
    """
    Run a SQL query and export the result as a CSV file.
    """
    output_path = OUTPUT_DIR / filename
    df = pd.read_sql_query(query, engine)
    df.to_csv(output_path, index=False)
    print(f"Exported {filename}: {len(df):,} rows")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    engine = get_engine()

    # 1. KPI summary for Power BI cards
    export_query(
        engine,
        """
        SELECT
            COUNT(*) AS total_records,
            ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay,
            ROUND(MIN(arrival_delay_minutes)::numeric, 2) AS min_arrival_delay,
            ROUND(MAX(arrival_delay_minutes)::numeric, 2) AS max_arrival_delay,
            MIN(DATE(arrival_plan)) AS start_date,
            MAX(DATE(arrival_plan)) AS end_date
        FROM cleaned_train_delays
        WHERE arrival_delay_minutes IS NOT NULL;
        """,
        "kpi_summary.csv",
    )

    # 2. Average delay by train line
    export_query(
        engine,
        """
        SELECT
            line,
            COUNT(*) AS total_records,
            ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay,
            ROUND(MAX(arrival_delay_minutes)::numeric, 2) AS max_arrival_delay
        FROM cleaned_train_delays
        WHERE arrival_delay_minutes IS NOT NULL
          AND line IS NOT NULL
        GROUP BY line
        HAVING COUNT(*) >= 100
        ORDER BY avg_arrival_delay DESC;
        """,
        "delay_by_line.csv",
    )

    # 3. Average delay by hour of day
    export_query(
        engine,
        """
        SELECT
            EXTRACT(HOUR FROM arrival_plan)::int AS hour_of_day,
            COUNT(*) AS total_records,
            ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay
        FROM cleaned_train_delays
        WHERE arrival_plan IS NOT NULL
          AND arrival_delay_minutes IS NOT NULL
        GROUP BY hour_of_day
        ORDER BY hour_of_day;
        """,
        "delay_by_hour.csv",
    )

    # 4. Average delay by date
    export_query(
        engine,
        """
        SELECT
            DATE(arrival_plan) AS travel_date,
            COUNT(*) AS total_records,
            ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay,
            ROUND(MAX(arrival_delay_minutes)::numeric, 2) AS max_arrival_delay
        FROM cleaned_train_delays
        WHERE arrival_plan IS NOT NULL
          AND arrival_delay_minutes IS NOT NULL
        GROUP BY travel_date
        ORDER BY travel_date;
        """,
        "delay_by_date.csv",
    )

    # 5. Average delay by train line and date
    export_query(
        engine,
        """
        SELECT
            DATE(arrival_plan) AS travel_date,
            line,
            COUNT(*) AS total_records,
            ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay,
            ROUND(MAX(arrival_delay_minutes)::numeric, 2) AS max_arrival_delay
        FROM cleaned_train_delays
        WHERE arrival_plan IS NOT NULL
          AND arrival_delay_minutes IS NOT NULL
          AND line IS NOT NULL
        GROUP BY travel_date, line
        HAVING COUNT(*) >= 20
        ORDER BY travel_date, avg_arrival_delay DESC;
        """,
        "delay_by_line_and_date.csv",
    )

    # 6. Average delay by city
    export_query(
        engine,
        """
        SELECT
            city,
            state,
            COUNT(*) AS total_records,
            ROUND(AVG(arrival_delay_minutes)::numeric, 2) AS avg_arrival_delay,
            ROUND(MAX(arrival_delay_minutes)::numeric, 2) AS max_arrival_delay
        FROM cleaned_train_delays
        WHERE arrival_delay_minutes IS NOT NULL
          AND city IS NOT NULL
        GROUP BY city, state
        HAVING COUNT(*) >= 100
        ORDER BY avg_arrival_delay DESC;
        """,
        "delay_by_city.csv",
    )

    print("Dashboard CSV export completed successfully.")


if __name__ == "__main__":
    main()