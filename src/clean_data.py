from pathlib import Path

import pandas as pd


RAW_DATA_PATH = Path("data/raw/DBtrainrides.csv")
PROCESSED_DATA_PATH = Path("data/processed/clean_transport_delays.csv")

def load_raw_data(file_path: Path) -> pd.DataFrame:
    """Load the raw train delay CSV file."""
    df = pd.read_csv(file_path)
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Select useful columns for delay analysis."""

    selected_columns: list[str] = [
        "ID",
        "line",
        "category",
        "station",
        "state",
        "city",
        "zip",
        "long",
        "lat",
        "arrival_plan",
        "departure_plan",
        "arrival_delay_m",
        "departure_delay_m",
        "arrival_delay_check",
        "departure_delay_check",
    ]

    clean_df = df.loc[:, selected_columns].copy()

    clean_df = clean_df.rename(
        columns={
            "ID": "id",
            "arrival_delay_m": "arrival_delay_minutes",
            "departure_delay_m": "departure_delay_minutes",
            "arrival_delay_check": "arrival_delay_status",
            "departure_delay_check": "departure_delay_status",
        }
    )

    clean_df["arrival_plan"] = pd.to_datetime(
        clean_df["arrival_plan"],
        errors="coerce",
    )

    clean_df["departure_plan"] = pd.to_datetime(
        clean_df["departure_plan"],
        errors="coerce",
    )

    numeric_columns: list[str] = [
        "zip",
        "long",
        "lat",
        "arrival_delay_minutes",
        "departure_delay_minutes",
    ]

    for column in numeric_columns:
        clean_df[column] = pd.to_numeric(
            clean_df[column],
            errors="coerce",
        )

    
    clean_df["arrival_date"] = clean_df["arrival_plan"].dt.date
    clean_df["arrival_hour"] = clean_df["arrival_plan"].dt.hour

    clean_df["departure_date"] = clean_df["departure_plan"].dt.date
    clean_df["departure_hour"] = clean_df["departure_plan"].dt.hour

    clean_df = clean_df.drop_duplicates()    

    return clean_df

def validate_clean_data(df: pd.DataFrame) -> None:
    """Validate important assumptions about the cleaned dataset."""

    if df.empty:
        raise ValueError("Cleaned dataset is empty.")

    if df["id"].isna().sum() > 0:
        raise ValueError("Cleaned dataset contains missing IDs.")

    if df["departure_plan"].isna().sum() > 0:
        raise ValueError("Cleaned dataset contains missing departure_plan values.")

    if df.duplicated().sum() > 0:
        raise ValueError("Cleaned dataset still contains duplicate rows.")


def save_clean_data(df: pd.DataFrame, file_path: Path) -> None:
    """Save the cleaned dataset as a CSV file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)

def main() -> None:
    print("Loading raw data...")
    raw_df = load_raw_data(RAW_DATA_PATH)

    raw_row_count = len(raw_df)

    print(f"Raw rows: {raw_row_count:,}")
    print("Cleaning data...")

    clean_df = clean_data(raw_df)
    validate_clean_data(clean_df)

    clean_row_count = len(clean_df)
    removed_duplicate_count = raw_row_count - clean_row_count
    missing_arrival_plan_count = clean_df["arrival_plan"].isna().sum()

    print(f"Clean rows: {clean_row_count:,}")
    print(f"Duplicate rows removed: {removed_duplicate_count:,}")
    print(f"Missing arrival_plan values kept: {missing_arrival_plan_count:,}")

    save_clean_data(clean_df, PROCESSED_DATA_PATH)

    print(f"Clean data saved to: {PROCESSED_DATA_PATH}")



if __name__ == "__main__":
    main()