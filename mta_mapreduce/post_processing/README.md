# MTA Dataset MapReduce Output Post-Processing

**Author**: Debdeep Naha (dn2491)
**Course**: CSGA 2436 - Realtime and Big Data Analytics

## Problem

The MapReduce profiling job outputs are **extremely large** (millions of lines) because the reducer isn't properly aggregating the counts. Each record emits individual counts instead of aggregated summaries.

## Solution

This directory contains scripts to **post-process** the huge outputs into report-friendly summaries.

## Quick Start

### Option 1: Automated Processing (RECOMMENDED)

Run the all-in-one script:

```bash
cd /home/user/NYCTravel/mta_mapreduce/post_processing
./process_outputs.sh
```

This will:
1. Download and aggregate the profiling data
2. Generate a human-readable markdown report
3. Download a sample of cleaned data
4. Display file size statistics

**Output files** (in `./output_analysis/`):
- `profiling_summary.txt` - Aggregated metrics
- `data_quality_report.md` - **Report for your paper** ✨
- `cleaned_sample.csv` - Sample of cleaned data

### Option 2: Manual Step-by-Step

#### Step 1: Aggregate Profiling Data

```bash
# Download and aggregate locally
hdfs dfs -cat /user/dn2491_nyu_edu/mta_profiling_full/part-* | \
    python3 aggregate_profiling.py > profiling_summary.txt
```

This reduces **millions of lines** to **thousands of aggregated metrics**.

#### Step 2: Generate Report

```bash
# Create human-readable markdown report
python3 generate_report.py < profiling_summary.txt > data_quality_report.md

# View the report
cat data_quality_report.md
# Or open in a markdown viewer
```

#### Step 3: Sample Cleaned Data

```bash
# Get first 1000 records
hdfs dfs -cat /user/dn2491_nyu_edu/mta_cleaned_full/part-* | head -1000 > cleaned_sample.csv

# Or get the entire cleaned dataset (if not too large)
hdfs dfs -getmerge /user/dn2491_nyu_edu/mta_cleaned_full ./cleaned_data_full.csv
```

## Understanding the Outputs

### Profiling Output Structure

The aggregated profiling data has this format:
```
category    key    count
```

**Example**:
```
borough_dist    Manhattan    5000000
borough_dist    Brooklyn     3000000
missing_values  ridership    50
non_missing_values  ridership  9999950
```

### Report Sections

The generated markdown report includes:

1. **Dataset Overview** - Total records, completeness
2. **Missing Values Analysis** - Per-column completeness table
3. **Data Validation Results** - Validation pass/fail rates
4. **Distribution Analysis** - Transit modes, boroughs, payment methods, top stations
5. **Ridership Analysis** - Total ridership, categories, outliers
6. **Transfers Analysis** - Transfer patterns
7. **Temporal Analysis** - Day of week distributions
8. **Data Quality Summary** - Unique stations, duplicates

## Alternative: Re-run with Fixed Reducer

If you want to fix the aggregation at the MapReduce level instead of post-processing:

### Option A: Use the Fixed Reducer

```bash
# Copy your fixed reducer
cp /path/to/fixed_profiling_reducer.py ./profiling_reducer_fixed.py

# Re-run the MapReduce job with the fixed reducer
hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
    -files profiling_mapper.py,profiling_reducer_fixed.py \
    -mapper profiling_mapper.py \
    -reducer profiling_reducer_fixed.py \
    -input /user/dn2491_nyu_edu/MTA_Subway.csv \
    -output /user/dn2491_nyu_edu/mta_profiling_fixed \
    -numReduceTasks 1
```

### Option B: Use Post-Processing as a Second MapReduce Job

```bash
# Run aggregation as a MapReduce job on the cluster
hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
    -D mapreduce.job.reduces=1 \
    -mapper cat \
    -reducer aggregate_profiling.py \
    -input /user/dn2491_nyu_edu/mta_profiling_full/part-* \
    -output /user/dn2491_nyu_edu/mta_profiling_aggregated \
    -file aggregate_profiling.py
```

## For Your Report

### What to Include

1. **Data Quality Table**: Copy the "Missing Values Analysis" table
2. **Validation Results**: Include validation pass rates
3. **Key Distributions**: Show borough, payment method, and transit mode distributions
4. **Top Stations**: Include top 10-20 stations
5. **Summary Statistics**: Total records, ridership, transfers

### How to Format

The `data_quality_report.md` is already formatted in markdown. You can:
- **Copy tables directly** into your Word/LaTeX document
- **Convert to PDF**: Use pandoc or a markdown viewer
- **Take screenshots** of rendered tables
- **Extract specific sections** that are relevant

### Sample Citation

```
Data profiling was performed using a MapReduce pipeline on the Hadoop cluster.
The dataset contained 10,000,000+ records with 99.8% data completeness across
all fields. Manhattan accounted for 45% of all records, with subway ridership
being the dominant transit mode (98.5%).
```

## Files in This Directory

- `aggregate_profiling.py` - Aggregates raw profiling output
- `generate_report.py` - Creates markdown report from aggregated data
- `process_outputs.sh` - Automated workflow script
- `README.md` - This file

## Troubleshooting

### "Memory Error" when aggregating

If the profiling data is too large to process locally:

```bash
# Process in chunks
hdfs dfs -cat /user/dn2491_nyu_edu/mta_profiling_full/part-00000 | \
    python3 aggregate_profiling.py > temp1.txt

hdfs dfs -cat /user/dn2491_nyu_edu/mta_profiling_full/part-00001 | \
    python3 aggregate_profiling.py > temp2.txt

# Then merge the aggregated results
cat temp1.txt temp2.txt | python3 aggregate_profiling.py > final_summary.txt
```

### "File not found" errors

Make sure you're using the correct HDFS paths:
```bash
# List your HDFS directories
hdfs dfs -ls /user/dn2491_nyu_edu/
```

### Need only specific statistics

Edit `generate_report.py` to comment out sections you don't need, or extract specific stats:

```bash
# Get only borough distribution
grep "borough_dist" profiling_summary.txt

# Get only missing value counts
grep "missing_values" profiling_summary.txt
```

## Performance Notes

- **Local processing**: Aggregating 10M+ lines takes ~2-5 minutes locally
- **Cluster processing**: Using MapReduce for aggregation is faster for very large datasets
- **Memory usage**: Aggregation script uses ~500MB-2GB RAM depending on unique keys

## Next Steps

After generating your report:

1. **Analyze cleaned data** for your research questions
2. **Run additional analytics** (time series, station analysis, etc.)
3. **Visualize results** using the cleaned dataset
4. **Include profiling results** in your methodology section

## Questions?

See the main project README or consult the Hadoop streaming documentation:
- [Hadoop Streaming Guide](https://hadoop.apache.org/docs/stable/hadoop-streaming/HadoopStreaming.html)
