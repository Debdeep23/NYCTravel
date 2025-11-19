#!/usr/bin/env python3
"""
MTA Dataset Profiling Reducer
Aggregates data quality metrics and generates profiling report
Author: Debdeep Naha (dn2491)
Course: CSGA 2436 - Realtime and Big Data Analytics
"""

import sys
from collections import defaultdict

def main():
    current_category = None
    current_key = None
    current_count = 0

    # Store all results for final summary
    results = defaultdict(lambda: defaultdict(int))

    for line in sys.stdin:
        line = line.strip()
        try:
            category, key, count = line.split('\t')
            count = int(count)

            if current_category == category and current_key == key:
                current_count += count
            else:
                if current_category is not None:
                    results[current_category][current_key] = current_count
                    print(f"{current_category}\t{current_key}\t{current_count}")

                current_category = category
                current_key = key
                current_count = count

        except ValueError:
            continue

    # Don't forget the last entry
    if current_category is not None:
        results[current_category][current_key] = current_count
        print(f"{current_category}\t{current_key}\t{current_count}")

if __name__ == "__main__":
    main()
