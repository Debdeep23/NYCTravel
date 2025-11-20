#!/bin/bash
###############################################################################
# Quick Statistics Extractor
# Get key metrics without downloading entire dataset
# Author: Debdeep Naha (dn2491)
###############################################################################

PROFILING_OUTPUT="/user/dn2491_nyu_edu/mta_profiling_full"

echo "========================================="
echo "Quick Statistics from Profiling Output"
echo "========================================="
echo ""

echo "📊 Sampling 10,000 lines for quick analysis..."
echo ""

# Sample and aggregate a subset for quick stats
hdfs dfs -cat "$PROFILING_OUTPUT/part-*" | head -10000 | python3 - <<'PYTHON'
import sys
from collections import defaultdict

data = defaultdict(lambda: defaultdict(int))

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        parts = line.split('\t')
        if len(parts) >= 3:
            category = parts[0]
            key = parts[1]
            count = int(parts[2])
            data[category][key] += count
    except:
        continue

# Print key statistics
print("=" * 50)
print("SAMPLE STATISTICS (from first 10,000 lines)")
print("=" * 50)
print()

if 'total_records' in data:
    print("📈 Total Records (in sample):", sum(data['total_records'].values()))
    print()

if 'borough_dist' in data:
    print("🏙️  Borough Distribution:")
    total = sum(data['borough_dist'].values())
    for borough, count in sorted(data['borough_dist'].items(), key=lambda x: x[1], reverse=True):
        pct = (count / total * 100) if total > 0 else 0
        print(f"   {borough:20s}: {count:6,d} ({pct:5.1f}%)")
    print()

if 'transit_mode_dist' in data:
    print("🚇 Transit Mode Distribution:")
    total = sum(data['transit_mode_dist'].values())
    for mode, count in sorted(data['transit_mode_dist'].items(), key=lambda x: x[1], reverse=True):
        pct = (count / total * 100) if total > 0 else 0
        print(f"   {mode:20s}: {count:6,d} ({pct:5.1f}%)")
    print()

if 'payment_method_dist' in data:
    print("💳 Payment Method Distribution:")
    total = sum(data['payment_method_dist'].values())
    for method, count in sorted(data['payment_method_dist'].items(), key=lambda x: x[1], reverse=True)[:5]:
        pct = (count / total * 100) if total > 0 else 0
        print(f"   {method:20s}: {count:6,d} ({pct:5.1f}%)")
    print()

# Missing values
missing_total = sum(data.get('missing_values', {}).values())
non_missing_total = sum(data.get('non_missing_values', {}).values())
if missing_total + non_missing_total > 0:
    completeness = (non_missing_total / (missing_total + non_missing_total) * 100)
    print(f"✅ Overall Completeness: {completeness:.2f}%")
    print(f"   Missing values: {missing_total:,}")
    print(f"   Non-missing values: {non_missing_total:,}")
    print()

print("=" * 50)
print("Note: These are estimates from a sample.")
print("Run ./process_outputs.sh for complete analysis.")
print("=" * 50)
PYTHON

echo ""
echo "For complete statistics, run:"
echo "  ./process_outputs.sh"
echo ""
