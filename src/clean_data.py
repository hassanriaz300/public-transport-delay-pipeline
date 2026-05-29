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


def save_clean_data(df: pd.DataFrame, file_path: Path) -> None:
    """Save the cleaned dataset as a CSV file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)

def main() -> None:
    raw_df = load_raw_data(RAW_DATA_PATH)

    print("Raw data loaded successfully")
    print(f"Raw rows: {len(raw_df):,}")
    print(f"Raw columns: {len(raw_df.columns)}")
    print(raw_df.dtypes)

    clean_df = clean_data(raw_df)

    columns_of_interest = [
        "arrival_plan",
        "arrival_date",
        "arrival_hour",
        "departure_plan",
        "departure_date",
        "departure_hour",
        "arrival_delay_minutes",
        "departure_delay_minutes",
        "arrival_delay_status",
        "departure_delay_status",
    ]

    print("Selected columns preview:")
    print(clean_df[columns_of_interest].head(10))
    print(clean_df[columns_of_interest].dtypes)
    print("Missing values in selected columns:")
    print(clean_df[columns_of_interest].isna().sum())
    print("Missing values in all clean columns:")
    print(clean_df.isna().sum())
    print("Duplicate rows:")
    print(clean_df.duplicated().sum())

    print("Data selected successfully")
    print(f"Clean rows: {len(clean_df):,}")
    print(f"Clean columns: {list(clean_df.columns)}")
    print(clean_df.head())
    save_clean_data(clean_df, PROCESSED_DATA_PATH)
    print(f"Clean data saved to: {PROCESSED_DATA_PATH}")



if __name__ == "__main__":
    main()