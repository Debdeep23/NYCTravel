#!/usr/bin/env python3
"""
Post-Processing Script to Aggregate MTA Profiling Results
Takes the huge profiling output and aggregates it into summary statistics

Usage:
    hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
        -D mapreduce.job.reduces=1 \
        -D stream.num.map.output.key.fields=2 \
        -D mapreduce.partition.keypartitioner.options=-k1,2 \
        -mapper cat \
        -reducer aggregate_profiling.py \
        -input /user/dn2491_nyu_edu/mta_profiling_full/part-* \
        -output /user/dn2491_nyu_edu/mta_profiling_summary \
        -file aggregate_profiling.py

    OR run locally on downloaded data:
    hdfs dfs -cat /user/dn2491_nyu_edu/mta_profiling_full/part-* | python3 aggregate_profiling.py > profiling_summary.txt

Author: Debdeep Naha (dn2491)
Course: CSGA 2436 - Realtime and Big Data Analytics
"""

import sys
from collections import defaultdict

def main():
    # Dictionary to store aggregated results
    aggregated = defaultdict(lambda: defaultdict(int))

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

                # Aggregate by category and key
                aggregated[category][key] += count
        except (ValueError, IndexError):
            # Skip malformed lines
            continue

    # Output aggregated results sorted by category, then by key
    for category in sorted(aggregated.keys()):
        for key in sorted(aggregated[category].keys()):
            count = aggregated[category][key]
            print(f"{category}\t{key}\t{count}")

if __name__ == "__main__":
    main()
