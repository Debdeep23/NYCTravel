# MTA Subway Hourly Ridership - MapReduce Data Processing

**Author:** Debdeep Naha (dn2491)
**Course:** CSGA 2436: Realtime and Big Data Analytics
**Institution:** New York University
**Date:** November 2025

## Table of Contents

1. [Overview](#overview)
2. [Dataset Description](#dataset-description)
3. [Project Structure](#project-structure)
4. [MapReduce Implementation](#mapreduce-implementation)
5. [Installation & Setup](#installation--setup)
6. [Usage Instructions](#usage-instructions)
7. [Data Profiling](#data-profiling)
8. [Data Cleaning](#data-cleaning)
9. [Output](#output)
10. [Technologies Used](#technologies-used)

---

## Overview

This project implements a scalable data profiling and cleaning pipeline for the **MTA Subway Hourly Ridership dataset (2020-2024)** using raw MapReduce in Python. The dataset is part of a larger NYC tourism analytics project that integrates hotel reviews, restaurant inspections, MTA ridership, and crime data to provide comprehensive insights for tourists visiting New York City.

The MTA ridership data serves as a proxy for:
- **Transportation accessibility** at different times and locations
- **Foot traffic** and neighborhood activity levels
- **Perceived safety** during non-rush hours
- **Transit connectivity** to major tourist destinations

---

## Dataset Description

### Source
- **Name:** MTA Subway Hourly Ridership: 2020-2024
- **Provider:** Metropolitan Transportation Authority (MTA)
- **Portal:** New York State Open Data
- **URL:** https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-2020-2024/wujg-7c2s
- **Size:** 6.22 GB (full dataset), ~121 million rows
- **Format:** CSV

### Schema (12 columns)

| Column Name           | Type   | Description |
|-----------------------|--------|-------------|
| transit_timestamp     | String | Date and time of ridership measurement (MM/DD/YYYY HH:MM:SS AM/PM) |
| transit_mode          | String | Type of transit (subway, staten_island_railway) |
| station_complex_id    | Integer| Unique identifier for station complex |
| station_complex       | String | Station name and lines served |
| borough               | String | NYC borough (Manhattan, Brooklyn, Queens, Bronx, Staten Island) |
| payment_method        | String | Payment type (metrocard, omny) |
| fare_class_category   | String | Fare type (Full Fare, Unlimited, Seniors & Disability, etc.) |
| ridership             | Integer| Number of riders entering station |
| transfers             | Integer| Number of transfers at this station |
| latitude              | Float  | Station latitude coordinate |
| longitude             | Float  | Station longitude coordinate |
| Georeference          | String | POINT geometry (latitude, longitude) |

### Sample Record
```csv
"05/11/2024 08:00:00 AM","subway","138","Canarsie-Rockaway Pkwy (L)","Brooklyn","metrocard","Metrocard - Other","11","0","40.646652","-73.90185","POINT (-73.90185 40.646652)"
```

---

## Project Structure

```
mta_mapreduce/
├── README.md                          # This file
├── profiling/
│   ├── profiling_mapper.py           # Mapper for data profiling
│   └── profiling_reducer.py          # Reducer for data profiling
├── cleaning/
│   ├── cleaning_mapper.py            # Mapper for data cleaning
│   └── cleaning_reducer.py           # Reducer for data cleaning
├── scripts/
│   ├── setup_hdfs.sh                 # Create HDFS directory structure
│   ├── upload_to_hdfs.sh             # Upload data to HDFS
│   ├── run_profiling.sh              # Execute profiling MapReduce job
│   ├── run_cleaning.sh               # Execute cleaning MapReduce job
│   ├── run_all.sh                    # Master script to run entire pipeline
│   └── generate_report.py            # Generate comprehensive analysis report
├── post_processing/                   # **NEW: Output aggregation tools**
│   ├── README.md                     # Post-processing documentation
│   ├── aggregate_profiling.py        # Aggregates large profiling outputs
│   ├── generate_report.py            # Creates markdown report for papers
│   ├── process_outputs.sh            # Automated post-processing pipeline
│   └── quick_stats.sh                # Quick statistics without full download
├── output/
│   ├── profiling/                    # Profiling job output
│   ├── cleaned/                      # Cleaned dataset
│   └── PROFILING_REPORT.txt          # Human-readable analysis report
└── docs/
    └── DOCUMENTATION.md              # Detailed technical documentation
```

---

## MapReduce Implementation

### 1. Data Profiling Job

**Purpose:** Analyze data quality, distribution patterns, and identify issues

**Mapper (`profiling_mapper.py`):**
- Validates each field (timestamps, coordinates, numeric values)
- Counts missing values per column
- Categorizes ridership and transfer values
- Extracts temporal features (hour, day of week)
- Analyzes distribution of categorical variables
- Detects potential duplicates

**Reducer (`profiling_reducer.py`):**
- Aggregates counts by category
- Outputs profiling metrics in tab-separated format

**Output:** Detailed statistics on:
- Total record count
- Missing value analysis per column
- Validation results (valid vs invalid records)
- Distribution analysis (boroughs, payment methods, fare classes, stations)
- Ridership and transfer statistics
- Temporal patterns (hourly, daily, weekly)
- Duplicate detection

### 2. Data Cleaning Job

**Purpose:** Clean, standardize, and prepare dataset for analysis

**Mapper (`cleaning_mapper.py`):**
- Filters out records with missing critical fields
- Validates and parses timestamps
- Validates coordinate ranges (NYC bounds: lat 40-41.5, lon -75 to -73)
- Cleans numeric fields (removes commas, validates ranges)
- Standardizes borough names and text fields
- Adds derived temporal features (year, month, day, hour, day_of_week)
- Creates hash key for duplicate detection

**Reducer (`cleaning_reducer.py`):**
- Removes duplicate records (keeps first occurrence)
- Outputs cleaned dataset with enhanced schema

**Output:** Cleaned CSV with 17 columns:
- Original 12 columns (cleaned and validated)
- 5 new temporal feature columns (year, month, day, hour, day_of_week)

---

## Installation & Setup

### Prerequisites

1. **Hadoop Cluster** (HDFS + MapReduce)
   - Hadoop 3.x or higher
   - HDFS configured and running
   - Hadoop Streaming JAR available

2. **Python 3.x**
   - No external libraries required (uses standard library only)

3. **Dataset**
   - Download from: https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-2020-2024/wujg-7c2s
   - Place `MTAAnalysis.csv` in the project root directory

### Environment Variables

Ensure the following are set:
```bash
export HADOOP_HOME=/path/to/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

---

## Usage Instructions

### Quick Start (Recommended)

Run the entire pipeline with one command:

```bash
cd mta_mapreduce/scripts
./run_all.sh
```

This will:
1. Set up HDFS directory structure
2. Upload data to HDFS
3. Run profiling MapReduce job
4. Run cleaning MapReduce job
5. Download results to local machine

### Step-by-Step Execution

#### 1. Setup HDFS Directories

```bash
cd mta_mapreduce/scripts
./setup_hdfs.sh
```

Creates the following HDFS structure:
```
/user/<username>/mta_ridership/
├── input/
└── output/
    ├── profiling/
    └── cleaned/
```

#### 2. Upload Dataset to HDFS

```bash
./upload_to_hdfs.sh
```

Uploads `MTAAnalysis.csv` to `/user/<username>/mta_ridership/input/`

#### 3. Run Data Profiling

```bash
./run_profiling.sh
```

Executes profiling MapReduce job and downloads results to `output/profiling/`

#### 4. Run Data Cleaning

```bash
./run_cleaning.sh
```

Executes cleaning MapReduce job and downloads cleaned data to `output/cleaned/`

#### 5. Generate Analysis Report

```bash
cd scripts
python3 generate_report.py
```

Creates `output/PROFILING_REPORT.txt` with comprehensive analysis

---

## Data Profiling

The profiling job analyzes the following aspects:

### Data Quality Metrics
- **Completeness:** Missing value count and percentage per column
- **Validity:** Valid vs invalid records for each field type
- **Uniqueness:** Duplicate detection and unique value counts
- **Accuracy:** Range validation for coordinates and numeric fields

### Distribution Analysis
- Transit mode distribution (subway vs staten_island_railway)
- Borough distribution (geographic coverage)
- Payment method distribution (metrocard vs omny)
- Fare class distribution (Full Fare, Unlimited, Seniors, etc.)
- Top busiest stations (by record count)

### Ridership Analysis
- Total ridership sum
- Average ridership per record
- Ridership categories (zero, low, medium, high, very high)
- Outlier detection (ridership > 5000)

### Temporal Patterns
- Hourly distribution (24-hour profile)
- Daily distribution (date range coverage)
- Day of week distribution (weekday vs weekend patterns)

---

## Data Cleaning

The cleaning job performs the following operations:

### 1. **Validation & Filtering**
- Remove records with missing critical fields (timestamp, station_id, borough, ridership, coordinates)
- Validate timestamp format and parsability
- Validate coordinate ranges (NYC bounds)
- Validate numeric fields (ridership ≥ 0, transfers ≥ 0)
- Validate station ID format (must be integer)

### 2. **Standardization**
- Convert borough names to title case
- Lowercase transit_mode and payment_method for consistency
- Remove commas from numeric fields
- Preserve original timestamp format while validating

### 3. **Feature Engineering**
- Extract year, month, day, hour from timestamp
- Add day_of_week (Monday-Sunday)

### 4. **Duplicate Removal**
- Create composite key: timestamp + station_id + payment_method + fare_class + ridership + transfers
- Hash the key for efficient comparison
- Keep only first occurrence of each unique record

### 5. **Error Handling**
- Log all filtering decisions to stderr
- Track counts of records filtered by reason
- Handle malformed CSV rows gracefully

---

## Post-Processing Large Outputs

### Problem

The profiling job outputs can be **extremely large** (millions of lines) when processing the full 121M row dataset. This happens because the reducer doesn't properly aggregate by both category AND key - Hadoop only sorts by the first tab-delimited field (category), causing incomplete aggregation.

### Solution

The `post_processing/` directory contains scripts to aggregate and summarize these huge outputs into report-friendly formats.

### Quick Start

```bash
cd mta_mapreduce/post_processing
./process_outputs.sh
```

This will:
1. Download and aggregate profiling data from HDFS
2. Generate a human-readable markdown report
3. Download a sample of cleaned data
4. Display file size statistics

**Output files** (in `./output_analysis/`):
- `profiling_summary.txt` - Aggregated metrics (millions of lines → thousands)
- `data_quality_report.md` - **Report suitable for academic papers** ✨
- `cleaned_sample.csv` - Sample of cleaned data for inspection

### Quick Statistics (No Full Download)

```bash
cd mta_mapreduce/post_processing
./quick_stats.sh
```

Gets key statistics from a sample without downloading the entire dataset.

### Manual Processing

```bash
# Aggregate profiling data
hdfs dfs -cat /user/dn2491_nyu_edu/mta_profiling_full/part-* | \
    python3 aggregate_profiling.py > profiling_summary.txt

# Generate markdown report
python3 generate_report.py < profiling_summary.txt > report.md
```

See `post_processing/README.md` for detailed documentation.

---

## Output

### Profiling Output

**Location:** `output/profiling/part-00000`

**Format:** Tab-separated values (TSV)
```
category    key    count
total_records    count    100000
missing_values    transit_timestamp    0
missing_values    ridership    0
borough_dist    Brooklyn    35420
borough_dist    Manhattan    28765
...
```

### Cleaned Dataset

**Location:** `output/cleaned/part-00000`

**Format:** CSV with header

**Sample:**
```csv
transit_timestamp,year,month,day,hour,day_of_week,transit_mode,station_complex_id,station_complex,borough,payment_method,fare_class_category,ridership,transfers,latitude,longitude,georeference
05/11/2024 08:00:00 AM,2024,5,11,8,Saturday,subway,138,Canarsie-Rockaway Pkwy (L),Brooklyn,metrocard,Metrocard - Other,11,0,40.646652,-73.90185,POINT (-73.90185 40.646652)
```

### Analysis Report

**Location:** `output/PROFILING_REPORT.txt`

**Contents:**
1. Dataset Overview
2. Data Quality Summary (completeness, validity, duplicates)
3. Distribution Analysis (boroughs, stations, payment methods, fare classes)
4. Ridership Analysis (totals, averages, categories)
5. Temporal Analysis (hourly, daily, weekly patterns)
6. Data Quality Issues & Recommendations
7. Summary and Insights

---

## Technologies Used

### Core Technologies
- **Hadoop 3.x:** Distributed file system (HDFS) and MapReduce framework
- **Hadoop Streaming:** Enables Python MapReduce jobs
- **Python 3:** Programming language for mapper/reducer logic

### Python Standard Libraries
- `sys`: Standard input/output for streaming
- `csv`: CSV parsing
- `datetime`: Timestamp validation and parsing
- `hashlib`: MD5 hashing for duplicate detection
- `collections.defaultdict`: Efficient counting in reducer
- `re`: Regular expression matching (if needed)

### Shell Scripting
- **Bash:** Automation scripts for HDFS operations and job execution

---

## Key Features

✅ **Scalable:** Designed for 6.22 GB / 121M row dataset using distributed MapReduce
✅ **Raw MapReduce:** Uses pure Hadoop Streaming (no Hive, Pig, Spark)
✅ **Data Quality Focus:** Comprehensive profiling and validation
✅ **Production-Ready:** Error handling, logging, and modular design
✅ **Well-Documented:** Extensive comments and documentation
✅ **Automated:** Single-command execution via `run_all.sh`
✅ **Reproducible:** Version-controlled code and consistent outputs

---

## Next Steps

After completing this data profiling and cleaning phase:

1. **Load into Hive/Trino:** Create external tables on cleaned data
2. **Integration:** Join with hotel, restaurant, and crime datasets
3. **Analysis:** Run correlation queries and aggregations
4. **Visualization:** Create dashboards in Tableau/Grafana
5. **Insights:** Generate recommendations for tourists and urban planners

---

## Author

**Debdeep Naha**
NetID: dn2491
Course: CSGA 2436 - Realtime and Big Data Analytics
Institution: New York University

---

## License

This project is submitted as coursework for CSGA 2436. The MTA dataset is publicly available from the New York State Open Data portal.

---

## References

1. MTA Subway Hourly Ridership: https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-2020-2024/wujg-7c2s
2. Hadoop Streaming Documentation: https://hadoop.apache.org/docs/stable/hadoop-streaming/HadoopStreaming.html
3. Project Proposal: RBDA_Project_Proposal.pdf

---

**End of README**
