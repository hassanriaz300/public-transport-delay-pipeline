# Public Transport Delay Pipeline

This project is a beginner-friendly data engineering and analytics pipeline for public transport delay data.

The goal is to build an end-to-end pipeline that can ingest raw train delay data, clean and transform it, load it into PostgreSQL, and later support analytics and simple machine learning.

## Current Phase

Phase 5: PostgreSQL query and analysis completed

## Tech Stack

- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- scikit-learn
- Jupyter Notebook
- Git/GitHub

## Project Structure

```text
public-transport-delay-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── src/
├── sql/
├── notebooks/
├── README.md
├── requirements.txt
└── .gitignore
```

## Phase 1: Project Setup

In Phase 1, the basic project structure and development environment were created.

### What was done

- Created the project folder structure
- Created a Python virtual environment
- Installed required dependencies
- Installed PostgreSQL using Homebrew
- Started the PostgreSQL service
- Created the database `transport_delay_db`
- Created the initial SQL schema file
- Created a GitHub repository and pushed the project

## Phase 2: Raw Data Ingestion

In Phase 2, the raw dataset was added to the project.

### Dataset

The raw dataset used in this project is:

```text
data/raw/DBtrainrides.csv
```

### Raw dataset shape

```text
Rows: 2,061,357
Columns: 20
```

### What was done

- Downloaded the Kaggle train delay dataset
- Placed the raw CSV file inside `data/raw/`
- Created `src/ingest_data.py`
- Verified the number of rows and columns
- Updated `.gitignore` so raw and processed CSV files are not pushed to GitHub

## Phase 3: Data Cleaning

In Phase 3, the raw train delay data was cleaned and transformed.

### Input

```text
data/raw/DBtrainrides.csv
```

### Output

```text
data/processed/clean_transport_delays.csv
```

### What was done

- Created `src/clean_data.py`
- Selected useful columns from the raw dataset
- Renamed columns to database-friendly names
- Converted datetime columns
- Converted numeric columns
- Created date and hour columns for arrival and departure
- Kept missing `arrival_plan` values because departure data is still valid
- Removed exact duplicate rows
- Added validation checks before saving the cleaned file

### Cleaning result

```text
Raw rows: 2,061,357
Clean rows: 2,052,750
Duplicate rows removed: 8,607
Missing arrival_plan values kept: 211,355
```

### Run data cleaning

```bash
python src/clean_data.py
```

### Expected output

```text
Loading raw data...
Raw rows: 2,061,357
Cleaning data...
Clean rows: 2,052,750
Duplicate rows removed: 8,607
Missing arrival_plan values kept: 211,355
Clean data saved to: data/processed/clean_transport_delays.csv
```

## Phase 4: Load Cleaned Data into PostgreSQL

In Phase 4, the cleaned CSV file was loaded into a PostgreSQL database table.

### Input

```text
data/processed/clean_transport_delays.csv
```

### Output

```text
PostgreSQL database: transport_delay_db
Table: cleaned_train_delays
Rows loaded: 2,052,750
```

### What was done

- Created a PostgreSQL table for the cleaned train delay dataset
- Updated `sql/create_tables.sql` with the `cleaned_train_delays` table
- Created `src/load_to_postgres.py`
- Used PostgreSQL `COPY` for efficient loading of a large CSV file
- Cleared the table before loading to make the script repeatable
- Verified the row count inside PostgreSQL
- Confirmed sample rows could be queried successfully

### Run the PostgreSQL table setup

```bash
psql -d transport_delay_db -f sql/create_tables.sql
```

### Load cleaned data into PostgreSQL

```bash
python src/load_to_postgres.py
```

### Expected output

```text
Checking cleaned CSV...
Connecting to PostgreSQL...
Clearing existing data from table: cleaned_train_delays
Loading CSV into table: cleaned_train_delays
Checking loaded row count...
Rows loaded into PostgreSQL: 2,052,750
Data loaded successfully.
```

### Verify in PostgreSQL

Open PostgreSQL:

```bash
psql -d transport_delay_db
```

Check row count:

```sql
SELECT COUNT(*) FROM cleaned_train_delays;
```

Expected result:

```text
2052750
```

Preview sample rows:

```sql
SELECT
    id,
    line,
    category,
    station,
    city,
    departure_plan,
    departure_delay_minutes,
    departure_delay_status
FROM cleaned_train_delays
LIMIT 5;
```

Exit PostgreSQL:

```sql
\q
```
## Phase 5: PostgreSQL Query and Analysis

In Phase 5, the cleaned train delay data is analyzed directly from PostgreSQL using SQL and Python.

### What was done

- Created `sql/analysis_queries.sql`
- Created `src/analyze_postgres.py`
- Queried the PostgreSQL table using SQL
- Loaded SQL query results into pandas DataFrames
- Printed analysis results in the terminal
- Analyzed delays by train line, station, city, day, and hour

### Analysis included

- total number of records loaded into PostgreSQL
- basic delay statistics such as average, minimum, and maximum delay
- train lines with the highest average arrival delay
- stations and cities with the highest average arrival delay
- daily delay patterns during the sampled week
- hourly delay patterns across the day

### Run SQL queries directly

```bash
psql -d transport_delay_db -f sql/analysis_queries.sql
```

### Run Python analysis

```bash
python src/analyze_postgres.py
```

### Example insights

```text
Total records: 2,052,750
Average arrival delay: 1.18 minutes
Maximum arrival delay: 159 minutes
Most delayed train line by average delay: RE25
Highest average delay by hour: around 18:00
```

## Git Workflow

Each phase is developed on its own branch and merged into `main` after testing.

Current completed branches:

```text
phase-3-clean-data
phase-4-load-postgres
phase-5-query-analysis
```

## Next Phase

Phase 6 will focus on building a simple dashboard or visual analytics layer for the PostgreSQL data.