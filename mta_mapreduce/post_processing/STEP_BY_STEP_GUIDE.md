# Step-by-Step Guide: Processing MTA MapReduce Outputs

**Author**: Debdeep Naha (dn2491)
**Course**: CSGA 2436 - Realtime and Big Data Analytics

---

## Current Situation

You've already completed:
✅ Uploaded data to HDFS
✅ Run profiling MapReduce job → output at `/user/dn2491_nyu_edu/mta_profiling_full`
✅ Run cleaning MapReduce job → output at `/user/dn2491_nyu_edu/mta_cleaned_full`

**Problem**: The profiling output is millions of lines (not aggregated properly)

**Solution**: Run the post-processing scripts to create usable reports

---

## Prerequisites Check

Before starting, verify your outputs exist:

```bash
# Check profiling output exists
hdfs dfs -ls /user/dn2491_nyu_edu/mta_profiling_full

# Check cleaned output exists
hdfs dfs -ls /user/dn2491_nyu_edu/mta_cleaned_full

# Check output sizes (optional)
hdfs dfs -du -h /user/dn2491_nyu_edu/mta_profiling_full
hdfs dfs -du -h /user/dn2491_nyu_edu/mta_cleaned_full
```

**Expected output**: You should see `part-00000` (and possibly more part files) in each directory.

---

## Cleanup (Optional)

### Do You Need to Clean Up?

**Answer**: Only if you want to remove old local output files or re-run jobs.

### Option A: Keep Everything (RECOMMENDED)

If this is your first time running post-processing, **skip cleanup** and go directly to Step 1.

### Option B: Remove Previous Local Outputs (if needed)

If you've run the scripts before and want fresh outputs:

```bash
cd /home/user/NYCTravel/mta_mapreduce/post_processing

# Remove old local outputs (if they exist)
rm -rf ./output_analysis

# That's it! You don't need to touch HDFS outputs
```

**DO NOT** remove HDFS outputs unless you want to re-run the entire MapReduce job (which takes a long time).

---

## Processing Steps

### Navigate to Post-Processing Directory

```bash
cd /home/user/NYCTravel/mta_mapreduce/post_processing
pwd  # Should show: /home/user/NYCTravel/mta_mapreduce/post_processing
```

---

## OPTION 1: Automated Processing (RECOMMENDED) ⭐

### Step 1: Run the Automated Script

```bash
./process_outputs.sh
```

**What this does**:
1. Creates `./output_analysis/` directory
2. Downloads profiling data from HDFS and aggregates it
3. Generates human-readable markdown report
4. Downloads sample of cleaned data (first 1000 records)
5. Displays file size statistics

**Time**: 2-10 minutes depending on data size

**Expected output on screen**:
```
=========================================
MTA Dataset Output Processing Pipeline
=========================================

Step 1: Processing Profiling Data
-----------------------------------
Downloading and aggregating profiling data...
✓ Profiling data aggregated to: ./output_analysis/profiling_summary.txt

Profiling Summary Statistics:
  Total lines in raw output: 10000000
  Aggregated lines: 5000

Step 2: Generating Human-Readable Report
-----------------------------------------
✓ Report generated: ./output_analysis/data_quality_report.md

Step 3: Analyzing Cleaned Data
--------------------------------
Downloading sample of cleaned data (first 1000 records)...
✓ Sample saved to: ./output_analysis/cleaned_sample.csv

Cleaned Data Statistics:
  Total cleaned records: 9500000

Step 4: HDFS File Size Information
------------------------------------
...

=========================================
Processing Complete!
=========================================
```

### Step 2: Review the Generated Report

```bash
# View the markdown report
cat ./output_analysis/data_quality_report.md

# Or open it in a markdown viewer if available
# less ./output_analysis/data_quality_report.md
```

### Step 3: Check All Generated Files

```bash
ls -lh ./output_analysis/
```

**You should see**:
- `profiling_summary.txt` - Aggregated profiling metrics
- `data_quality_report.md` - **Your report for the paper** ✨
- `cleaned_sample.csv` - Sample of cleaned data

### Step 4: Done! 🎉

You now have:
- ✅ Aggregated statistics suitable for reports
- ✅ Human-readable markdown report with tables
- ✅ Sample of cleaned data for inspection

**Use these files** in your academic report, presentations, or further analysis.

---

## OPTION 2: Manual Step-by-Step Processing

If you want to run each step individually:

### Step 1: Create Output Directory

```bash
cd /home/user/NYCTravel/mta_mapreduce/post_processing
mkdir -p output_analysis
```

### Step 2: Aggregate Profiling Data

```bash
hdfs dfs -cat /user/dn2491_nyu_edu/mta_profiling_full/part-* | \
    python3 aggregate_profiling.py > output_analysis/profiling_summary.txt
```

**What this does**: Reduces millions of profiling lines to thousands of aggregated metrics

**Time**: 2-8 minutes

**Verify**:
```bash
wc -l output_analysis/profiling_summary.txt  # Should show thousands, not millions
head output_analysis/profiling_summary.txt   # Preview the data
```

### Step 3: Generate Markdown Report

```bash
python3 generate_report.py < output_analysis/profiling_summary.txt > output_analysis/data_quality_report.md
```

**What this does**: Creates formatted markdown report with tables and statistics

**Time**: < 1 second

**Verify**:
```bash
wc -l output_analysis/data_quality_report.md  # Should show ~300-500 lines
head -50 output_analysis/data_quality_report.md  # Preview the report
```

### Step 4: Download Sample of Cleaned Data

```bash
hdfs dfs -cat /user/dn2491_nyu_edu/mta_cleaned_full/part-* | head -1000 > output_analysis/cleaned_sample.csv
```

**What this does**: Downloads first 1000 cleaned records for inspection

**Time**: < 1 minute

**Verify**:
```bash
wc -l output_analysis/cleaned_sample.csv  # Should show 1000
head -5 output_analysis/cleaned_sample.csv  # Preview the data
```

### Step 5: Get Statistics About Cleaned Data

```bash
echo "Total cleaned records:"
hdfs dfs -cat /user/dn2491_nyu_edu/mta_cleaned_full/part-* | wc -l
```

**Note**: This might take a while if the cleaned dataset is very large.

### Step 6: Done! 🎉

All files are now in `output_analysis/` directory.

---

## OPTION 3: Quick Statistics Only (No Full Download)

If you just want quick insights without downloading everything:

```bash
cd /home/user/NYCTravel/mta_mapreduce/post_processing
./quick_stats.sh
```

**What this does**: Samples first 10,000 lines and shows key statistics

**Time**: < 30 seconds

**Output**: Quick summary of boroughs, transit modes, payment methods, completeness

---

## What to Do Next

### For Your Academic Report

1. **Open the report**:
   ```bash
   cat output_analysis/data_quality_report.md
   ```

2. **Copy relevant sections** into your paper:
   - Dataset Overview (total records, completeness)
   - Missing Values Analysis table
   - Distribution Analysis (boroughs, payment methods)
   - Ridership Analysis
   - Top 20 Stations table

3. **Format for your document**:
   - Markdown tables can be converted to Word/LaTeX
   - Take screenshots of rendered markdown
   - Copy statistics and percentages directly

### For Further Analysis

1. **Download full cleaned dataset** (if needed):
   ```bash
   hdfs dfs -getmerge /user/dn2491_nyu_edu/mta_cleaned_full ./cleaned_data_full.csv
   ```
   **Warning**: This might be several GB. Only do this if you need the entire dataset locally.

2. **Run additional analytics** on the cleaned data in HDFS

3. **Load into Hive/Trino** for SQL-based analysis

---

## Troubleshooting

### Problem: "Command not found: ./process_outputs.sh"

**Solution**: Make sure you're in the correct directory and the file is executable:
```bash
cd /home/user/NYCTravel/mta_mapreduce/post_processing
chmod +x *.sh *.py
./process_outputs.sh
```

### Problem: "No such file or directory" when accessing HDFS

**Solution**: Verify the exact path in HDFS:
```bash
hdfs dfs -ls /user/dn2491_nyu_edu/
```

Then update the paths in `process_outputs.sh` if they're different.

### Problem: Download is taking forever

**Solution**:
- Use `./quick_stats.sh` instead for fast results
- Or add `| head -100000` to limit the download:
  ```bash
  hdfs dfs -cat /user/dn2491_nyu_edu/mta_profiling_full/part-* | head -100000 | \
      python3 aggregate_profiling.py > output_analysis/profiling_summary.txt
  ```

### Problem: Memory error during aggregation

**Solution**: Process files individually:
```bash
# Aggregate each part file separately
for i in {0..9}; do
    hdfs dfs -cat /user/dn2491_nyu_edu/mta_profiling_full/part-0000$i | \
        python3 aggregate_profiling.py > temp_$i.txt
done

# Merge and re-aggregate
cat temp_*.txt | python3 aggregate_profiling.py > output_analysis/profiling_summary.txt
rm temp_*.txt
```

### Problem: Report is missing data

**Solution**: Check that profiling_summary.txt has data:
```bash
wc -l output_analysis/profiling_summary.txt
head output_analysis/profiling_summary.txt
```

If it's empty, the aggregation step failed. Re-run Step 2.

---

## Summary: What You'll Get

After running the processing:

📄 **Files Created**:
```
output_analysis/
├── profiling_summary.txt      # Aggregated metrics (TSV format)
├── data_quality_report.md     # Markdown report for your paper
└── cleaned_sample.csv         # Sample of cleaned data (1000 rows)
```

📊 **Report Contents**:
- Dataset overview with totals and percentages
- Missing value analysis table
- Data validation results (pass/fail rates)
- Distribution tables (boroughs, stations, payment methods, fare classes)
- Ridership statistics and categories
- Transfer analysis
- Temporal patterns (day of week)
- Data quality summary

✅ **Ready to Use**:
- Copy tables directly into your paper
- Include statistics with proper formatting
- Reference data quality metrics
- Show profiling results professionally

---

## Recommended Workflow

**For most users, follow this**:

1. ✅ Navigate: `cd /home/user/NYCTravel/mta_mapreduce/post_processing`
2. ✅ Run: `./process_outputs.sh`
3. ✅ Review: `cat output_analysis/data_quality_report.md`
4. ✅ Use the report in your paper
5. ✅ Done!

**Total time**: 5-10 minutes

---

## Questions?

- See `README.md` in this directory for detailed documentation
- See main `../README.md` for overall project documentation
- Check Hadoop logs if jobs fail: `hdfs dfs -cat /path/to/output/_logs/*`

---

**End of Guide**
