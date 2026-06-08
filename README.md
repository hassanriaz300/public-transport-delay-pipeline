# Public Transport Delay Pipeline

This project is a basic data engineering and analytics pipeline for public transport delay data.

The goal is to build an end-to-end pipeline that can ingest raw train delay data, clean and transform it, load it into PostgreSQL, analyze it using SQL and Python, and present the results in a Power BI dashboard.

The project is currently focused on batch data processing and analytics. The planned direction is to extend it into a more production-style data pipeline by adding orchestration with Apache Airflow, containerization with Docker, automated data quality checks, and a simple machine learning model to identify train lines or time periods with higher delay risk.

## Current Phase

Phase 6: Power BI dashboard completed

## Tech Stack

* Python
* Pandas
* PostgreSQL
* SQLAlchemy
* Power BI
* SQL
* Git/GitHub

## Project Structure

```text
public-transport-delay-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── dashboard_data/
│   ├── kpi_summary.csv
│   ├── delay_by_line.csv
│   ├── delay_by_hour.csv
│   ├── delay_by_date.csv
│   ├── delay_by_line_and_date.csv
│   └── delay_by_city.csv
├── PowerBI_Dashboard/
│   ├── Images/
│   ├── powerbi_dashboard_trainsdelay.Report/
│   ├── powerbi_dashboard_trainsdelay.SemanticModel/
│   └── powerbi_dashboard_trainsdelay.pbip
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

* Created the project folder structure
* Created a Python virtual environment
* Installed required dependencies
* Installed PostgreSQL using Homebrew
* Started the PostgreSQL service
* Created the database `transport_delay_db`
* Created the initial SQL schema file
* Created a GitHub repository and pushed the project

## Phase 2: Raw Data Ingestion

In Phase 2, the raw dataset was added to the project.

### Dataset

The raw dataset used in this project is:

```text
data/raw/DBtrainrides.csv
```

The dataset covers a 7-day period of German public transport data:

```text
08 July 2024 to 14 July 2024
```

### Raw dataset shape

```text
Rows: 2,061,357
Columns: 20
```

### What was done

* Downloaded the Kaggle train delay dataset
* Placed the raw CSV file inside `data/raw/`
* Created `src/ingest_data.py`
* Verified the number of rows and columns
* Updated `.gitignore` so raw and processed CSV files are not pushed to GitHub

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

* Created `src/clean_data.py`
* Selected useful columns from the raw dataset
* Renamed columns to database-friendly names
* Converted datetime columns
* Converted numeric columns
* Created date and hour columns for arrival and departure
* Kept missing `arrival_plan` values because departure data is still valid
* Removed exact duplicate rows
* Added validation checks before saving the cleaned file

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

* Created a PostgreSQL table for the cleaned train delay dataset
* Updated `sql/create_tables.sql` with the `cleaned_train_delays` table
* Created `src/load_to_postgres.py`
* Used PostgreSQL `COPY` for efficient loading of a large CSV file
* Cleared the table before loading to make the script repeatable
* Verified the row count inside PostgreSQL
* Confirmed sample rows could be queried successfully

### Run the PostgreSQL table setup

```bash
psql -d transport_delay_db -f sql/create_tables.sql
```

### Load cleaned data into PostgreSQL

```bash
python src/load_to_postgres.py
```

### Verify in PostgreSQL

```bash
psql -d transport_delay_db
```

```sql
SELECT COUNT(*) FROM cleaned_train_delays;
```

Expected result:

```text
2052750
```

Exit PostgreSQL:

```sql
\q
```

## Phase 5: PostgreSQL Query and Analysis

In Phase 5, the cleaned train delay data was analyzed directly from PostgreSQL using SQL and Python.

### What was done

* Created `sql/analysis_queries.sql`
* Created `src/analyze_postgres.py`
* Queried the PostgreSQL table using SQL
* Loaded SQL query results into pandas DataFrames
* Printed analysis results in the terminal
* Analyzed delays by train line, station, city, day, and hour

### Analysis included

* Total number of records loaded into PostgreSQL
* Basic delay statistics such as average, minimum, and maximum delay
* Train lines with the highest average arrival delay
* Stations and cities with the highest average arrival delay
* Daily delay patterns during the sampled week
* Hourly delay patterns across the day

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

## Phase 6: Power BI Dashboard

In Phase 6, the PostgreSQL analysis results were exported into Power BI-ready CSV files and used to build an interactive dashboard.

### What was done

* Created `src/export_dashboard_data.py`
* Exported dashboard-ready CSV files from PostgreSQL
* Loaded the exported CSV files into Power BI
* Built a Power BI dashboard using KPI cards, bar charts, line charts, slicers, and a detail table
* Added dashboard images and Power BI project files to the repository
* Used a Power BI Project structure instead of only a single `.pbix` file

### Dashboard data exports

The following files were exported into `dashboard_data/`:

```text
kpi_summary.csv
delay_by_line.csv
delay_by_hour.csv
delay_by_date.csv
delay_by_line_and_date.csv
delay_by_city.csv
```

### Dashboard includes

* Total records KPI
* Average arrival delay KPI
* Maximum arrival delay KPI
* Number of cities analyzed
* Number of train lines analyzed
* Top 10 train lines by average delay
* Average delay by hour of day
* Daily delay trend
* Top 10 cities by average delay
* Delay details by train line and date
* Key insights section

### Dashboard insights

```text
Overall average arrival delay is low at 1.18 minutes across 2.05M records.
RE25 is the most delayed train line, with the highest average delay of about 5.2 minutes.
Delays increase during evening hours, especially around 18:00–19:00.
City-level delays are highest in Steinau an der Straße, with an average delay of about 6.2 minutes.
```

### Dataset period

```text
08 July 2024 to 14 July 2024
```

Because the dataset covers only 7 days, the dashboard focuses on short-term operational delay patterns rather than long-term monthly trends.

## Git Workflow

Each major phase was developed on its own branch and merged into `main` after testing.

Completed branches:

```text
phase-3-clean-data
phase-4-load-postgres
phase-5-query-analysis
phase-6-powerbi-dashboard
```

## Current Status

The project now contains a complete basic data engineering and analytics workflow:

```text
Raw CSV data
→ Python ingestion
→ Data cleaning
→ PostgreSQL loading
→ SQL/Python analysis
→ Power BI dashboard
```

## Next Improvements

Planned future improvements:

* Add an automated pipeline scheduler using Apache Airflow
* Add Docker support for PostgreSQL and Python scripts
* Create a small machine learning model to predict delay risk

