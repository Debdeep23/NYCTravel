#!/bin/bash
###############################################################################
# Run Profiling Aggregation on Hadoop Cluster (for large datasets)
# Author: Debdeep Naha (dn2491)
# Course: CSGA 2436 - Realtime and Big Data Analytics
###############################################################################

set -e

echo "========================================="
echo "Aggregating Profiling Data on Cluster"
echo "========================================="
echo ""

# Configuration
PROFILING_INPUT="/user/dn2491_nyu_edu/mta_profiling_full"
AGGREGATED_OUTPUT="/user/dn2491_nyu_edu/mta_profiling_aggregated"

# Remove old aggregated output if exists
echo "Cleaning up old aggregated output..."
hdfs dfs -rm -r -f "$AGGREGATED_OUTPUT"

echo "Running MapReduce aggregation job on cluster..."
echo "(This processes the data on the cluster, not locally)"
echo ""

hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
    -D mapreduce.job.reduces=1 \
    -D mapreduce.job.name="MTA_Profiling_Aggregation" \
    -mapper cat \
    -reducer aggregate_profiling.py \
    -input "$PROFILING_INPUT/part-*" \
    -output "$AGGREGATED_OUTPUT" \
    -file aggregate_profiling.py

echo ""
echo "✓ Aggregation complete!"
echo ""
echo "Output location: $AGGREGATED_OUTPUT"
echo ""

# Show output size
echo "Aggregated output size:"
hdfs dfs -du -h "$AGGREGATED_OUTPUT"
echo ""

# Download the small aggregated result
echo "Downloading aggregated results (should be small now)..."
mkdir -p output_analysis
hdfs dfs -cat "$AGGREGATED_OUTPUT/part-*" > output_analysis/profiling_summary.txt

echo "✓ Downloaded to: output_analysis/profiling_summary.txt"
echo ""
echo "Lines in aggregated output: $(wc -l < output_analysis/profiling_summary.txt)"
echo ""
echo "Next step: Run ./generate_report_local.sh to create the markdown report"
