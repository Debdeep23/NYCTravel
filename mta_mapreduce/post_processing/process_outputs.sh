#!/bin/bash
###############################################################################
# Script to Download and Process MTA MapReduce Outputs
# Author: Debdeep Naha (dn2491)
# Course: CSGA 2436 - Realtime and Big Data Analytics
###############################################################################

set -e  # Exit on error

echo "========================================="
echo "MTA Dataset Output Processing Pipeline"
echo "========================================="
echo ""

# Configuration
PROFILING_OUTPUT="/user/dn2491_nyu_edu/mta_profiling_full"
CLEANED_OUTPUT="/user/dn2491_nyu_edu/mta_cleaned_full"
LOCAL_DIR="./output_analysis"

# Create local output directory
mkdir -p "$LOCAL_DIR"

echo "Step 1: Processing Profiling Data"
echo "-----------------------------------"

# Option 1: Download and process locally (RECOMMENDED for large outputs)
echo "Downloading and aggregating profiling data..."
hdfs dfs -cat "$PROFILING_OUTPUT/part-*" | \
    python3 aggregate_profiling.py > "$LOCAL_DIR/profiling_summary.txt"

echo "✓ Profiling data aggregated to: $LOCAL_DIR/profiling_summary.txt"
echo ""

# Show summary statistics
echo "Profiling Summary Statistics:"
echo "  Total lines in raw output: $(hdfs dfs -cat $PROFILING_OUTPUT/part-* | wc -l)"
echo "  Aggregated lines: $(wc -l < $LOCAL_DIR/profiling_summary.txt)"
echo ""

echo "Step 2: Generating Human-Readable Report"
echo "-----------------------------------------"
python3 generate_report.py < "$LOCAL_DIR/profiling_summary.txt" > "$LOCAL_DIR/data_quality_report.md"
echo "✓ Report generated: $LOCAL_DIR/data_quality_report.md"
echo ""

echo "Step 3: Analyzing Cleaned Data"
echo "--------------------------------"

# Get sample of cleaned data
echo "Downloading sample of cleaned data (first 1000 records)..."
hdfs dfs -cat "$CLEANED_OUTPUT/part-*" | head -1000 > "$LOCAL_DIR/cleaned_sample.csv"
echo "✓ Sample saved to: $LOCAL_DIR/cleaned_sample.csv"
echo ""

# Get statistics about cleaned data
echo "Cleaned Data Statistics:"
CLEANED_TOTAL=$(hdfs dfs -cat "$CLEANED_OUTPUT/part-*" | wc -l)
echo "  Total cleaned records: $CLEANED_TOTAL"
echo ""

# Check file sizes
echo "Step 4: HDFS File Size Information"
echo "------------------------------------"
echo "Profiling output size:"
hdfs dfs -du -h "$PROFILING_OUTPUT"
echo ""
echo "Cleaned data size:"
hdfs dfs -du -h "$CLEANED_OUTPUT"
echo ""

echo "========================================="
echo "Processing Complete!"
echo "========================================="
echo ""
echo "Generated Files:"
echo "  1. $LOCAL_DIR/profiling_summary.txt       - Aggregated profiling metrics"
echo "  2. $LOCAL_DIR/data_quality_report.md      - Human-readable report (include in your paper)"
echo "  3. $LOCAL_DIR/cleaned_sample.csv          - Sample of cleaned data"
echo ""
echo "Next Steps:"
echo "  1. Review the report: cat $LOCAL_DIR/data_quality_report.md"
echo "  2. Include relevant tables/statistics in your academic report"
echo "  3. Use cleaned data for further analysis: hdfs dfs -cat $CLEANED_OUTPUT/part-*"
echo ""
