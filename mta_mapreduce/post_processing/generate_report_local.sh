#!/bin/bash
###############################################################################
# Generate Report from Aggregated Profiling Data
# Author: Debdeep Naha (dn2491)
###############################################################################

set -e

echo "Generating human-readable report..."

if [ ! -f "output_analysis/profiling_summary.txt" ]; then
    echo "Error: profiling_summary.txt not found!"
    echo "Run ./aggregate_on_cluster.sh first"
    exit 1
fi

python3 generate_report.py < output_analysis/profiling_summary.txt > output_analysis/data_quality_report.md

echo "✓ Report generated: output_analysis/data_quality_report.md"
echo ""
echo "View the report:"
echo "  cat output_analysis/data_quality_report.md"
