#!/usr/bin/env python3
"""
MTA Dataset Profiling Reducer - FIXED VERSION
Aggregates counts in memory to handle unsorted secondary keys.

This version properly aggregates all (category, key) pairs in memory
before outputting results, fixing the issue where Hadoop only sorts
by the first tab-delimited field (category) but not the second (key).

Author: Debdeep Naha (dn2491)
Course: CSGA 2436 - Realtime and Big Data Analytics
"""

import sys
from collections import defaultdict

def main():
    # Use a dictionary to aggregate counts in memory
    # Key = (category, sub_key), Value = Total Count
    results = defaultdict(int)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            # Parse the input: Category <tab> Key <tab> Count
            parts = line.split('\t')

            # Handle cases where split might not be perfect
            if len(parts) == 3:
                category, key, count_str = parts
                count = int(count_str)
                results[(category, key)] += count

        except ValueError:
            continue

    # Now that we have counted EVERYTHING, print the sorted results
    # Sorting makes the report easier to read
    for (category, key) in sorted(results.keys()):
        total_count = results[(category, key)]
        print(f"{category}\t{key}\t{total_count}")

if __name__ == "__main__":
    main()
