import os
import psycopg2


DATABASE_NAME = "transport_delay_db"
TABLE_NAME = "cleaned_train_delays"
CSV_PATH = "data/processed/clean_transport_delays.csv"


def main():
    print("Checking cleaned CSV...")

    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Cleaned CSV not found: {CSV_PATH}")

    print("Connecting to PostgreSQL...")

    connection = psycopg2.connect(dbname=DATABASE_NAME)
    cursor = connection.cursor()

    print(f"Clearing existing data from table: {TABLE_NAME}")
    cursor.execute(f"TRUNCATE TABLE {TABLE_NAME};")

    print(f"Loading CSV into table: {TABLE_NAME}")

    with open(CSV_PATH, "r", encoding="utf-8") as file:
        cursor.copy_expert(
            f"""
            COPY {TABLE_NAME}
            FROM STDIN
            WITH CSV HEADER
            """,
            file,
        )

    print("Checking loaded row count...")

    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
    result = cursor.fetchone()

    if result is None:
        raise ValueError("Could not fetch row count from PostgreSQL.")

    row_count = result[0]

    connection.commit()

    cursor.close()
    connection.close()

    print(f"Rows loaded into PostgreSQL: {row_count:,}")
    print("Data loaded successfully.")


if __name__ == "__main__":
    main()