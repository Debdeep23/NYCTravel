#!/usr/bin/env python3
"""
Generate Human-Readable Report from Profiling Data
Creates a summary report suitable for inclusion in academic reports

Usage:
    python3 generate_report.py < profiling_summary.txt > report.md

Author: Debdeep Naha (dn2491)
Course: CSGA 2436 - Realtime and Big Data Analytics
"""

import sys
from collections import defaultdict

def format_number(num):
    """Format number with commas for readability"""
    return f"{num:,}"

def calculate_percentage(part, total):
    """Calculate percentage and format it"""
    if total == 0:
        return "0.00"
    return f"{(part / total * 100):.2f}"

def main():
    # Parse all profiling data
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
                data[category][key] = count
        except (ValueError, IndexError):
            continue

    # Generate report
    print("# MTA Subway Dataset Data Quality and Profiling Report")
    print()

    # 1. Dataset Overview
    print("## 1. Dataset Overview")
    print()
    total_records = data.get('total_records', {}).get('count', 0)
    incomplete_rows = data.get('row_count_issue', {}).get('incomplete_rows', 0)

    print(f"- **Total Records Processed**: {format_number(total_records)}")
    print(f"- **Incomplete Rows**: {format_number(incomplete_rows)}")
    if total_records > 0:
        print(f"- **Data Completeness**: {calculate_percentage(total_records - incomplete_rows, total_records)}%")
    print()

    # 2. Missing Values Analysis
    print("## 2. Missing Values Analysis")
    print()
    print("| Column | Non-Missing | Missing | Completeness |")
    print("|--------|-------------|---------|--------------|")

    columns = ['transit_timestamp', 'transit_mode', 'station_complex_id', 'station_complex',
               'borough', 'payment_method', 'fare_class_category', 'ridership',
               'transfers', 'latitude', 'longitude', 'georeference']

    for col in columns:
        non_missing = data.get('non_missing_values', {}).get(col, 0)
        missing = data.get('missing_values', {}).get(col, 0)
        total_col = non_missing + missing
        if total_col > 0:
            completeness = calculate_percentage(non_missing, total_col)
            print(f"| {col} | {format_number(non_missing)} | {format_number(missing)} | {completeness}% |")
    print()

    # 3. Data Validation Results
    print("## 3. Data Validation Results")
    print()

    # Timestamp validation
    valid_timestamps = data.get('timestamp_validation', {}).get('valid', 0)
    invalid_timestamps = data.get('timestamp_validation', {}).get('invalid', 0)
    total_timestamps = valid_timestamps + invalid_timestamps
    if total_timestamps > 0:
        print(f"### Timestamp Validation")
        print(f"- Valid: {format_number(valid_timestamps)} ({calculate_percentage(valid_timestamps, total_timestamps)}%)")
        print(f"- Invalid: {format_number(invalid_timestamps)} ({calculate_percentage(invalid_timestamps, total_timestamps)}%)")
        print()

    # Coordinate validation
    valid_coords = data.get('coordinate_validation', {}).get('valid', 0)
    invalid_coords = data.get('coordinate_validation', {}).get('invalid', 0)
    total_coords = valid_coords + invalid_coords
    if total_coords > 0:
        print(f"### Coordinate Validation")
        print(f"- Valid: {format_number(valid_coords)} ({calculate_percentage(valid_coords, total_coords)}%)")
        print(f"- Invalid: {format_number(invalid_coords)} ({calculate_percentage(invalid_coords, total_coords)}%)")
        print()

    # Ridership validation
    valid_ridership = data.get('ridership_validation', {}).get('valid', 0)
    invalid_ridership = data.get('ridership_validation', {}).get('invalid', 0)
    total_ridership_checks = valid_ridership + invalid_ridership
    if total_ridership_checks > 0:
        print(f"### Ridership Validation")
        print(f"- Valid: {format_number(valid_ridership)} ({calculate_percentage(valid_ridership, total_ridership_checks)}%)")
        print(f"- Invalid: {format_number(invalid_ridership)} ({calculate_percentage(invalid_ridership, total_ridership_checks)}%)")
        print()

    # Station ID validation
    valid_station_ids = data.get('station_id_validation', {}).get('valid', 0)
    invalid_station_ids = data.get('station_id_validation', {}).get('invalid', 0)
    total_station_id_checks = valid_station_ids + invalid_station_ids
    if total_station_id_checks > 0:
        print(f"### Station ID Validation")
        print(f"- Valid: {format_number(valid_station_ids)} ({calculate_percentage(valid_station_ids, total_station_id_checks)}%)")
        print(f"- Invalid: {format_number(invalid_station_ids)} ({calculate_percentage(invalid_station_ids, total_station_id_checks)}%)")
        print()

    # 4. Distribution Analysis
    print("## 4. Distribution Analysis")
    print()

    # Transit Mode
    if 'transit_mode_dist' in data:
        print("### Transit Mode Distribution")
        print()
        print("| Transit Mode | Count | Percentage |")
        print("|--------------|-------|------------|")
        transit_modes = data['transit_mode_dist']
        total_transit = sum(transit_modes.values())
        for mode in sorted(transit_modes.keys(), key=lambda x: transit_modes[x], reverse=True):
            count = transit_modes[mode]
            pct = calculate_percentage(count, total_transit)
            print(f"| {mode} | {format_number(count)} | {pct}% |")
        print()

    # Borough
    if 'borough_dist' in data:
        print("### Borough Distribution")
        print()
        print("| Borough | Count | Percentage |")
        print("|---------|-------|------------|")
        boroughs = data['borough_dist']
        total_borough = sum(boroughs.values())
        for borough in sorted(boroughs.keys(), key=lambda x: boroughs[x], reverse=True):
            count = boroughs[borough]
            pct = calculate_percentage(count, total_borough)
            print(f"| {borough} | {format_number(count)} | {pct}% |")
        print()

    # Payment Method
    if 'payment_method_dist' in data:
        print("### Payment Method Distribution")
        print()
        print("| Payment Method | Count | Percentage |")
        print("|----------------|-------|------------|")
        payment_methods = data['payment_method_dist']
        total_payment = sum(payment_methods.values())
        for method in sorted(payment_methods.keys(), key=lambda x: payment_methods[x], reverse=True):
            count = payment_methods[method]
            pct = calculate_percentage(count, total_payment)
            print(f"| {method} | {format_number(count)} | {pct}% |")
        print()

    # Fare Class
    if 'fare_class_dist' in data:
        print("### Fare Class Distribution")
        print()
        print("| Fare Class | Count | Percentage |")
        print("|------------|-------|------------|")
        fare_classes = data['fare_class_dist']
        total_fare = sum(fare_classes.values())
        for fare_class in sorted(fare_classes.keys(), key=lambda x: fare_classes[x], reverse=True):
            count = fare_classes[fare_class]
            pct = calculate_percentage(count, total_fare)
            print(f"| {fare_class} | {format_number(count)} | {pct}% |")
        print()

    # Top 20 Stations
    if 'station_dist' in data:
        print("### Top 20 Stations by Record Count")
        print()
        print("| Rank | Station | Count |")
        print("|------|---------|-------|")
        stations = data['station_dist']
        top_stations = sorted(stations.items(), key=lambda x: x[1], reverse=True)[:20]
        for idx, (station, count) in enumerate(top_stations, 1):
            print(f"| {idx} | {station} | {format_number(count)} |")
        print()

    # 5. Ridership Analysis
    print("## 5. Ridership Analysis")
    print()

    ridership_total = data.get('ridership_sum', {}).get('total', 0)
    print(f"- **Total Ridership**: {format_number(ridership_total)}")
    print()

    if 'ridership_category' in data:
        print("### Ridership Categories")
        print()
        print("| Category | Count | Percentage |")
        print("|----------|-------|------------|")
        ridership_cats = data['ridership_category']
        total_cat = sum(ridership_cats.values())

        # Define order for categories
        category_order = ['zero', 'low_1-10', 'medium_11-50', 'high_51-200', 'very_high_200+']
        for cat in category_order:
            if cat in ridership_cats:
                count = ridership_cats[cat]
                pct = calculate_percentage(count, total_cat)
                print(f"| {cat.replace('_', ' ').title()} | {format_number(count)} | {pct}% |")
        print()

    outliers = data.get('ridership_outliers', {}).get('extremely_high', 0)
    if outliers > 0:
        print(f"- **Ridership Outliers (>5000)**: {format_number(outliers)}")
        print()

    # 6. Transfers Analysis
    print("## 6. Transfers Analysis")
    print()

    transfers_total = data.get('transfers_sum', {}).get('total', 0)
    print(f"- **Total Transfers**: {format_number(transfers_total)}")
    print()

    if 'transfers_category' in data:
        print("### Transfer Categories")
        print()
        print("| Category | Count | Percentage |")
        print("|----------|-------|------------|")
        transfer_cats = data['transfers_category']
        total_transfer_cat = sum(transfer_cats.values())

        for cat in sorted(transfer_cats.keys()):
            count = transfer_cats[cat]
            pct = calculate_percentage(count, total_transfer_cat)
            print(f"| {cat.replace('_', ' ').title()} | {format_number(count)} | {pct}% |")
        print()

    # 7. Temporal Analysis
    if 'day_of_week' in data:
        print("## 7. Temporal Analysis")
        print()
        print("### Day of Week Distribution")
        print()
        print("| Day | Count | Percentage |")
        print("|-----|-------|------------|")
        days = data['day_of_week']
        total_days = sum(days.values())

        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in day_order:
            if day in days:
                count = days[day]
                pct = calculate_percentage(count, total_days)
                print(f"| {day} | {format_number(count)} | {pct}% |")
        print()

    # 8. Data Quality Summary
    print("## 8. Data Quality Summary")
    print()

    # Count unique stations
    unique_stations = len(data.get('unique_stations', {}))
    print(f"- **Unique Stations**: {format_number(unique_stations)}")

    # Count duplicate keys
    duplicate_keys = data.get('duplicate_check', {})
    total_duplicate_keys = len(duplicate_keys)
    duplicates_found = sum(1 for count in duplicate_keys.values() if count > 1)
    print(f"- **Unique Record Keys**: {format_number(total_duplicate_keys)}")
    print(f"- **Potential Duplicates**: {format_number(duplicates_found)}")
    print()

    print("---")
    print()
    print("*Report generated using MapReduce data profiling pipeline*")
    print(f"*Author: Debdeep Naha (dn2491)*")
    print(f"*Course: CSGA 2436 - Realtime and Big Data Analytics*")

if __name__ == "__main__":
    main()
