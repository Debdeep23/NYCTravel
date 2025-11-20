# Quick Reference Card

## TL;DR - For Large Datasets (23GB+) 🚀

```bash
cd /home/user/NYCTravel/mta_mapreduce/post_processing

# Step 1: Aggregate on cluster (handles large datasets)
./aggregate_on_cluster.sh

# Step 2: Generate report
./generate_report_local.sh
```

**Then review your report**:
```bash
cat output_analysis/data_quality_report.md
```

---

## All Commands in Order

### 1. Navigate to Directory
```bash
cd /home/user/NYCTravel/mta_mapreduce/post_processing
```

### 2. Run Cluster Aggregation (Recommended for Large Datasets)
```bash
./aggregate_on_cluster.sh
```

This runs the aggregation as a MapReduce job on the cluster, avoiding memory issues.

### 3. Generate Human-Readable Report
```bash
./generate_report_local.sh
```

### 4. View Results
```bash
# View the markdown report
cat output_analysis/data_quality_report.md

# View aggregated metrics
cat output_analysis/profiling_summary.txt | head -50

# List all output files
ls -lh output_analysis/
```

---

## Quick Stats Only (30 seconds)

If you just want quick insights:

```bash
./quick_stats.sh
```

This samples the first 10,000 lines and shows key statistics without downloading everything.

---

## Understanding Your Outputs

**After running the scripts, you'll have:**

```
output_analysis/
├── profiling_summary.txt      - Aggregated profiling metrics (TSV format)
└── data_quality_report.md     - Human-readable report for your paper
```

**The report includes:**
- Dataset overview and completeness metrics
- Missing values analysis table
- Data validation results
- Distribution analysis (boroughs, transit modes, payment methods)
- Top 20 stations
- Ridership and transfer statistics
- Temporal patterns
- Data quality summary

---

## For Your Academic Report

Copy relevant sections from `output_analysis/data_quality_report.md`:
- Data quality tables
- Distribution statistics
- Top stations
- Validation pass rates

---

## Troubleshooting

**Problem**: Scripts not executable
```bash
chmod +x *.sh *.py
```

**Problem**: HDFS path not found
```bash
hdfs dfs -ls /user/dn2491_nyu_edu/
```

**Problem**: Want to see cleaned data sample
```bash
hdfs dfs -cat /user/dn2491_nyu_edu/mta_cleaned_full/part-* | head -1000 > sample.csv
```

---

## File Locations

- **Raw profiling on HDFS**: `/user/dn2491_nyu_edu/mta_profiling_full`
- **Aggregated profiling on HDFS**: `/user/dn2491_nyu_edu/mta_profiling_aggregated`
- **Cleaned data on HDFS**: `/user/dn2491_nyu_edu/mta_cleaned_full`
- **Local outputs**: `./output_analysis/`
