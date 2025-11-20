# Quick Reference Card

## TL;DR - Just Run This! 🚀

```bash
cd /home/user/NYCTravel/mta_mapreduce/post_processing
./process_outputs.sh
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

### 2. Run Automated Processing
```bash
./process_outputs.sh
```

### 3. View Results
```bash
# View the markdown report
cat output_analysis/data_quality_report.md

# View aggregated metrics
cat output_analysis/profiling_summary.txt | head -50

# View cleaned data sample
cat output_analysis/cleaned_sample.csv | head -20

# List all output files
ls -lh output_analysis/
```

---

## Alternative: Manual Steps

```bash
# 1. Create output directory
mkdir -p output_analysis

# 2. Aggregate profiling data
hdfs dfs -cat /user/dn2491_nyu_edu/mta_profiling_full/part-* | \
    python3 aggregate_profiling.py > output_analysis/profiling_summary.txt

# 3. Generate markdown report
python3 generate_report.py < output_analysis/profiling_summary.txt > output_analysis/data_quality_report.md

# 4. Download cleaned data sample
hdfs dfs -cat /user/dn2491_nyu_edu/mta_cleaned_full/part-* | head -1000 > output_analysis/cleaned_sample.csv
```

---

## Quick Stats (Fast, No Full Download)

```bash
./quick_stats.sh
```

---

## Files You'll Get

```
output_analysis/
├── profiling_summary.txt      → Aggregated statistics (for data nerds)
├── data_quality_report.md     → Human-readable report (for your paper) ⭐
└── cleaned_sample.csv         → Sample of cleaned data (for inspection)
```

---

## Troubleshooting One-Liners

```bash
# Verify HDFS outputs exist
hdfs dfs -ls /user/dn2491_nyu_edu/mta_profiling_full
hdfs dfs -ls /user/dn2491_nyu_edu/mta_cleaned_full

# Make scripts executable
chmod +x *.sh *.py

# Check output sizes in HDFS
hdfs dfs -du -h /user/dn2491_nyu_edu/

# Count lines in profiling output
hdfs dfs -cat /user/dn2491_nyu_edu/mta_profiling_full/part-* | wc -l

# Count lines in cleaned output
hdfs dfs -cat /user/dn2491_nyu_edu/mta_cleaned_full/part-* | wc -l
```

---

## Time Estimates

| Task | Time |
|------|------|
| Quick stats (`./quick_stats.sh`) | 30 seconds |
| Automated processing (`./process_outputs.sh`) | 5-10 minutes |
| Manual processing (all steps) | 5-10 minutes |
| Download full cleaned dataset | 10-30 minutes (depends on size) |

---

## What Goes in Your Report

From `data_quality_report.md`, copy these sections:

1. ✅ Dataset Overview → Total records, completeness percentage
2. ✅ Missing Values Analysis → Table showing per-column completeness
3. ✅ Distribution Analysis → Borough/payment/transit mode tables
4. ✅ Top 20 Stations → Table of busiest stations
5. ✅ Ridership Analysis → Total ridership, categories
6. ✅ Data Quality Summary → Unique stations, duplicates

---

**See `STEP_BY_STEP_GUIDE.md` for detailed instructions**
