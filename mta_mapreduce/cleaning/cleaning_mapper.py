#!/usr/bin/env python3
"""
MTA Dataset Cleaning Mapper
Cleans and standardizes MTA ridership data
Author: Debdeep Naha (dn2491)
Course: CSGA 2436 - Realtime and Big Data Analytics
"""

import sys
import csv
from datetime import datetime
import hashlib

def is_valid_timestamp(timestamp_str):
    """Validate and parse timestamp"""
    try:
        dt = datetime.strptime(timestamp_str, '%m/%d/%Y %I:%M:%S %p')
        return True, dt
    except:
        return False, None

def is_valid_coordinate(lat, lon):
    """Validate latitude and longitude ranges for NYC"""
    try:
        lat_val = float(lat)
        lon_val = float(lon)
        # NYC bounds: lat 40.4-41.0, lon -74.3 to -73.7
        return (40.0 <= lat_val <= 41.5) and (-75.0 <= lon_val <= -73.0)
    except:
        return False

def clean_numeric_field(value):
    """Remove commas from numeric fields and validate"""
    try:
        cleaned = value.replace(',', '').strip()
        int_val = int(cleaned)
        return True, int_val
    except:
        return False, None

def standardize_borough(borough):
    """Standardize borough names"""
    borough = borough.strip()
    borough_map = {
        'manhattan': 'Manhattan',
        'brooklyn': 'Brooklyn',
        'bronx': 'Bronx',
        'queens': 'Queens',
        'staten island': 'Staten Island'
    }
    return borough_map.get(borough.lower(), borough)

def main():
    reader = csv.reader(sys.stdin)
    header = next(reader, None)  # Skip header

    # Output header for cleaned data
    cleaned_header = [
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

    records_processed = 0
    records_filtered = 0

    for row in reader:
        records_processed += 1

        # Skip incomplete rows
        if len(row) != 12:
            records_filtered += 1
            print(f"CLEANING_STATS\tincomplete_rows\t1", file=sys.stderr)
            continue

        try:
            transit_timestamp = row[0].strip()
            transit_mode = row[1].strip()
            station_complex_id = row[2].strip()
            station_complex = row[3].strip()
            borough = row[4].strip()
            payment_method = row[5].strip()
            fare_class_category = row[6].strip()
            ridership = row[7].strip()
            transfers = row[8].strip()
            latitude = row[9].strip()
            longitude = row[10].strip()
            georeference = row[11].strip()

            # Critical fields validation - skip if any are missing
            critical_fields = [
                transit_timestamp, station_complex_id, borough,
                ridership, latitude, longitude
            ]

            if any(not field for field in critical_fields):
                records_filtered += 1
                print(f"CLEANING_STATS\tmissing_critical_fields\t1", file=sys.stderr)
                continue

            # Validate and parse timestamp
            is_valid_ts, dt = is_valid_timestamp(transit_timestamp)
            if not is_valid_ts:
                records_filtered += 1
                print(f"CLEANING_STATS\tinvalid_timestamp\t1", file=sys.stderr)
                continue

            # Extract temporal features
            year = dt.year
            month = dt.month
            day = dt.day
            hour = dt.hour
            day_of_week = dt.strftime('%A')

            # Validate coordinates
            if not is_valid_coordinate(latitude, longitude):
                records_filtered += 1
                print(f"CLEANING_STATS\tinvalid_coordinates\t1", file=sys.stderr)
                continue

            # Clean ridership
            is_valid_ridership, ridership_val = clean_numeric_field(ridership)
            if not is_valid_ridership or ridership_val < 0:
                records_filtered += 1
                print(f"CLEANING_STATS\tinvalid_ridership\t1", file=sys.stderr)
                continue

            # Clean transfers
            is_valid_transfers, transfers_val = clean_numeric_field(transfers)
            if not is_valid_transfers or transfers_val < 0:
                # If transfers are invalid, default to 0
                transfers_val = 0

            # Validate station ID
            try:
                int(station_complex_id)
            except:
                records_filtered += 1
                print(f"CLEANING_STATS\tinvalid_station_id\t1", file=sys.stderr)
                continue

            # Standardize borough
            borough = standardize_borough(borough)

            # Standardize text fields (lowercase for consistency)
            transit_mode = transit_mode.lower().strip()
            payment_method = payment_method.lower().strip()

            # Create a unique key for duplicate detection
            # Using timestamp + station_id + payment_method + fare_class as composite key
            duplicate_key = f"{transit_timestamp}|{station_complex_id}|{payment_method}|{fare_class_category}|{ridership}|{transfers}"
            key_hash = hashlib.md5(duplicate_key.encode()).hexdigest()

            # Output cleaned record with hash for duplicate removal
            cleaned_record = [
                transit_timestamp,
                str(year),
                str(month),
                str(day),
                str(hour),
                day_of_week,
                transit_mode,
                station_complex_id,
                station_complex,
                borough,
                payment_method,
                fare_class_category,
                str(ridership_val),
                str(transfers_val),
                latitude,
                longitude,
                georeference
            ]

            # Emit: key = hash, value = cleaned record
            print(f"{key_hash}\t{','.join(cleaned_record)}")
            print(f"CLEANING_STATS\tvalid_records\t1", file=sys.stderr)

        except Exception as e:
            records_filtered += 1
            print(f"CLEANING_STATS\tparsing_error\t1", file=sys.stderr)
            continue

if __name__ == "__main__":
    main()
