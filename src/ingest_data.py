from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_raw_csv(file_name: str) -> pd.DataFrame:
    """Load a CSV file from the raw data folder."""
    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Could not find raw file: {file_path}")

    return pd.read_csv(file_path)


def show_basic_info(df: pd.DataFrame) -> None:
    """Print basic information about the loaded dataset."""
    print("Data loaded successfully")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print("\nPreview:")
    print(df.head())


def main() -> None:
    file_name = "DBtrainrides.csv"

    print(f"Reading raw data file: {file_name}")

    df = load_raw_csv(file_name)
    show_basic_info(df)


if __name__ == "__main__":
    main()