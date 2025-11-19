#!/usr/bin/env python3
"""
MTA Dataset Cleaning Reducer
Removes duplicates and outputs cleaned dataset
Author: Debdeep Naha (dn2491)
Course: CSGA 2436 - Realtime and Big Data Analytics
"""

import sys

def main():
    current_hash = None
    first_occurrence = None

    # Output header
    header = [
        'transit_timestamp',
        'year',
        'month',
        'day',
        'hour',
        'day_of_week',
        'transit_mode',
        'station_complex_id',
        'station_complex',
        'borough',
        'payment_method',
        'fare_class_category',
        'ridership',
        'transfers',
        'latitude',
        'longitude',
        'georeference'
    ]
    print(','.join(header))

    duplicates_removed = 0
    records_written = 0

    for line in sys.stdin:
        line = line.strip()
        try:
            hash_key, record = line.split('\t', 1)

            if current_hash == hash_key:
                # Duplicate found - keep only the first occurrence
                duplicates_removed += 1
                print(f"CLEANING_STATS\tduplicates_removed\t1", file=sys.stderr)
            else:
                # New record - output the previous one if exists
                if current_hash is not None and first_occurrence is not None:
                    print(first_occurrence)
                    records_written += 1

                current_hash = hash_key
                first_occurrence = record

        except ValueError:
            continue

    # Don't forget the last record
    if current_hash is not None and first_occurrence is not None:
        print(first_occurrence)
        records_written += 1

    print(f"CLEANING_STATS\trecords_written\t{records_written}", file=sys.stderr)

if __name__ == "__main__":
    main()
