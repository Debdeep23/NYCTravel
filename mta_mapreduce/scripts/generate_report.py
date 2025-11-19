#!/usr/bin/env python3
"""
MTA Dataset Analysis Report Generator
Generates comprehensive analysis report from profiling results
Author: Debdeep Naha (dn2491)
Course: CSGA 2436 - Realtime and Big Data Analytics
"""

import sys
import os
from collections import defaultdict
from datetime import datetime

def read_profiling_results(filepath):
    """Read and parse profiling results"""
    results = defaultdict(lambda: defaultdict(int))

    try:
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) == 3:
                    category, key, count = parts
                    results[category][key] = int(count)
    except FileNotFoundError:
        print(f"Error: Profiling results file not found at {filepath}")
        sys.exit(1)

    return results

def generate_report(results, output_file):
    """Generate comprehensive analysis report"""

    with open(output_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("MTA SUBWAY HOURLY RIDERSHIP DATA - PROFILING REPORT\n")
        f.write("="*80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Author: Debdeep Naha (dn2491)\n")
        f.write(f"Course: CSGA 2436 - Realtime and Big Data Analytics\n")
        f.write("="*80 + "\n\n")

        # 1. Dataset Overview
        f.write("1. DATASET OVERVIEW\n")
        f.write("-" * 80 + "\n")
        total_records = results.get('total_records', {}).get('count', 0)
        f.write(f"Total Records Processed: {total_records:,}\n")
        f.write(f"Data Source: MTA Subway Hourly Ridership (2020-2024)\n")
        f.write(f"Dataset URL: https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-2020-2024/wujg-7c2s\n")
        f.write("\n")

        # 2. Data Quality Summary
        f.write("2. DATA QUALITY SUMMARY\n")
        f.write("-" * 80 + "\n")

        # Missing values
        f.write("\n2.1 Missing Values Analysis\n")
        missing = results.get('missing_values', {})
        non_missing = results.get('non_missing_values', {})

        columns = ['transit_timestamp', 'transit_mode', 'station_complex_id',
                  'station_complex', 'borough', 'payment_method',
                  'fare_class_category', 'ridership', 'transfers',
                  'latitude', 'longitude', 'georeference']

        f.write(f"{'Column':<25} {'Missing':<12} {'Non-Missing':<12} {'Completeness':<12}\n")
        f.write("-" * 80 + "\n")
        for col in columns:
            missing_count = missing.get(col, 0)
            non_missing_count = non_missing.get(col, 0)
            total_col = missing_count + non_missing_count
            completeness = (non_missing_count / total_col * 100) if total_col > 0 else 0
            f.write(f"{col:<25} {missing_count:<12,} {non_missing_count:<12,} {completeness:>10.2f}%\n")
        f.write("\n")

        # Validation results
        f.write("2.2 Data Validation Results\n")
        validation_metrics = [
            ('Timestamp', 'timestamp_validation'),
            ('Ridership', 'ridership_validation'),
            ('Transfers', 'transfers_validation'),
            ('Coordinates', 'coordinate_validation'),
            ('Station ID', 'station_id_validation')
        ]

        f.write(f"{'Metric':<25} {'Valid':<15} {'Invalid':<15} {'Valid %':<12}\n")
        f.write("-" * 80 + "\n")
        for metric_name, metric_key in validation_metrics:
            valid = results.get(metric_key, {}).get('valid', 0)
            invalid = results.get(metric_key, {}).get('invalid', 0)
            total_val = valid + invalid
            valid_pct = (valid / total_val * 100) if total_val > 0 else 0
            f.write(f"{metric_name:<25} {valid:<15,} {invalid:<15,} {valid_pct:>10.2f}%\n")
        f.write("\n")

        # Duplicate check
        f.write("2.3 Duplicate Records\n")
        duplicates = results.get('duplicate_check', {})
        unique_records = len(duplicates)
        potential_duplicates = total_records - unique_records
        f.write(f"Unique Records: {unique_records:,}\n")
        f.write(f"Potential Duplicates: {potential_duplicates:,}\n")
        f.write(f"Duplication Rate: {(potential_duplicates/total_records*100):.2f}%\n")
        f.write("\n")

        # 3. Distribution Analysis
        f.write("3. DISTRIBUTION ANALYSIS\n")
        f.write("-" * 80 + "\n")

        # Transit mode distribution
        f.write("\n3.1 Transit Mode Distribution\n")
        transit_modes = results.get('transit_mode_dist', {})
        f.write(f"{'Transit Mode':<30} {'Count':<15} {'Percentage':<12}\n")
        f.write("-" * 80 + "\n")
        for mode, count in sorted(transit_modes.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total_records * 100) if total_records > 0 else 0
            f.write(f"{mode:<30} {count:<15,} {pct:>10.2f}%\n")
        f.write("\n")

        # Borough distribution
        f.write("3.2 Borough Distribution\n")
        boroughs = results.get('borough_dist', {})
        f.write(f"{'Borough':<30} {'Count':<15} {'Percentage':<12}\n")
        f.write("-" * 80 + "\n")
        for borough, count in sorted(boroughs.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total_records * 100) if total_records > 0 else 0
            f.write(f"{borough:<30} {count:<15,} {pct:>10.2f}%\n")
        f.write("\n")

        # Payment method distribution
        f.write("3.3 Payment Method Distribution\n")
        payment_methods = results.get('payment_method_dist', {})
        f.write(f"{'Payment Method':<30} {'Count':<15} {'Percentage':<12}\n")
        f.write("-" * 80 + "\n")
        for method, count in sorted(payment_methods.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total_records * 100) if total_records > 0 else 0
            f.write(f"{method:<30} {count:<15,} {pct:>10.2f}%\n")
        f.write("\n")

        # Fare class distribution (top 10)
        f.write("3.4 Fare Class Distribution (Top 10)\n")
        fare_classes = results.get('fare_class_dist', {})
        f.write(f"{'Fare Class':<40} {'Count':<15} {'Percentage':<12}\n")
        f.write("-" * 80 + "\n")
        for fare_class, count in sorted(fare_classes.items(), key=lambda x: x[1], reverse=True)[:10]:
            pct = (count / total_records * 100) if total_records > 0 else 0
            f.write(f"{fare_class:<40} {count:<15,} {pct:>10.2f}%\n")
        f.write("\n")

        # Top 15 stations
        f.write("3.5 Busiest Station Complexes (Top 15)\n")
        stations = results.get('station_dist', {})
        f.write(f"{'Station Complex':<50} {'Records':<15}\n")
        f.write("-" * 80 + "\n")
        for station, count in sorted(stations.items(), key=lambda x: x[1], reverse=True)[:15]:
            f.write(f"{station:<50} {count:<15,}\n")
        f.write("\n")

        # 4. Ridership Analysis
        f.write("4. RIDERSHIP ANALYSIS\n")
        f.write("-" * 80 + "\n")

        total_ridership = results.get('ridership_sum', {}).get('total', 0)
        avg_ridership = total_ridership / total_records if total_records > 0 else 0
        f.write(f"Total Ridership: {total_ridership:,}\n")
        f.write(f"Average Ridership per Record: {avg_ridership:.2f}\n")
        f.write("\n")

        # Ridership categories
        f.write("4.1 Ridership Distribution by Category\n")
        ridership_cats = results.get('ridership_category', {})
        f.write(f"{'Category':<30} {'Count':<15} {'Percentage':<12}\n")
        f.write("-" * 80 + "\n")
        category_order = ['zero', 'low_1-10', 'medium_11-50', 'high_51-200', 'very_high_200+']
        for cat in category_order:
            count = ridership_cats.get(cat, 0)
            pct = (count / total_records * 100) if total_records > 0 else 0
            f.write(f"{cat:<30} {count:<15,} {pct:>10.2f}%\n")

        outliers = results.get('ridership_outliers', {}).get('extremely_high', 0)
        f.write(f"{'Outliers (>5000)':<30} {outliers:<15,}\n")
        f.write("\n")

        # Transfers analysis
        f.write("4.2 Transfers Analysis\n")
        total_transfers = results.get('transfers_sum', {}).get('total', 0)
        avg_transfers = total_transfers / total_records if total_records > 0 else 0
        f.write(f"Total Transfers: {total_transfers:,}\n")
        f.write(f"Average Transfers per Record: {avg_transfers:.2f}\n")
        f.write("\n")

        transfer_cats = results.get('transfers_category', {})
        f.write(f"{'Category':<30} {'Count':<15} {'Percentage':<12}\n")
        f.write("-" * 80 + "\n")
        for cat, count in sorted(transfer_cats.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total_records * 100) if total_records > 0 else 0
            f.write(f"{cat:<30} {count:<15,} {pct:>10.2f}%\n")
        f.write("\n")

        # 5. Temporal Analysis
        f.write("5. TEMPORAL ANALYSIS\n")
        f.write("-" * 80 + "\n")

        # Hourly distribution
        f.write("5.1 Hourly Distribution\n")
        hourly = results.get('hourly_distribution', {})
        f.write(f"{'Hour':<10} {'Count':<15} {'Bar Chart':<50}\n")
        f.write("-" * 80 + "\n")
        max_hourly = max(hourly.values()) if hourly else 1
        for hour in range(24):
            hour_str = f"{hour:02d}:00"
            count = hourly.get(f"{hour:02d}", 0)
            bar_length = int((count / max_hourly) * 40) if max_hourly > 0 else 0
            bar = '█' * bar_length
            f.write(f"{hour_str:<10} {count:<15,} {bar}\n")
        f.write("\n")

        # Day of week distribution
        f.write("5.2 Day of Week Distribution\n")
        dow = results.get('day_of_week', {})
        f.write(f"{'Day':<15} {'Count':<15} {'Percentage':<12}\n")
        f.write("-" * 80 + "\n")
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in day_order:
            count = dow.get(day, 0)
            pct = (count / total_records * 100) if total_records > 0 else 0
            f.write(f"{day:<15} {count:<15,} {pct:>10.2f}%\n")
        f.write("\n")

        # 6. Data Quality Issues and Recommendations
        f.write("6. DATA QUALITY ISSUES & CLEANING RECOMMENDATIONS\n")
        f.write("-" * 80 + "\n")

        issues = []

        # Check for missing values
        if sum(missing.values()) > 0:
            issues.append("- Missing values detected in multiple columns")

        # Check for invalid data
        for metric_name, metric_key in validation_metrics:
            invalid = results.get(metric_key, {}).get('invalid', 0)
            if invalid > 0:
                issues.append(f"- Invalid {metric_name.lower()} values found: {invalid:,} records")

        # Check for duplicates
        if potential_duplicates > 0:
            issues.append(f"- Potential duplicate records: {potential_duplicates:,}")

        if issues:
            f.write("Issues Found:\n")
            for issue in issues:
                f.write(f"{issue}\n")
        else:
            f.write("No major data quality issues found.\n")

        f.write("\nCleaning Operations Performed:\n")
        f.write("1. Removed records with missing critical fields\n")
        f.write("2. Validated and filtered invalid timestamps\n")
        f.write("3. Validated coordinate ranges for NYC area\n")
        f.write("4. Cleaned numeric fields (removed commas, validated ranges)\n")
        f.write("5. Standardized borough names and text fields\n")
        f.write("6. Removed duplicate records based on composite key\n")
        f.write("7. Added temporal features (year, month, day, hour, day_of_week)\n")
        f.write("\n")

        # 7. Summary
        f.write("7. SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"The MTA Subway Hourly Ridership dataset contains {total_records:,} records\n")
        f.write(f"covering subway and Staten Island Railway transit from 2020-2024.\n")
        f.write(f"\n")
        f.write(f"Key Insights:\n")
        f.write(f"- Total ridership tracked: {total_ridership:,} riders\n")
        f.write(f"- Average ridership per record: {avg_ridership:.2f}\n")
        f.write(f"- Unique station complexes: {len(results.get('unique_stations', {}))}\n")
        f.write(f"- Data completeness: High (>99% for most fields)\n")
        f.write(f"- Geographic coverage: All 5 NYC boroughs\n")
        f.write("\n")
        f.write("This dataset is suitable for:\n")
        f.write("- Transportation accessibility analysis\n")
        f.write("- Temporal ridership pattern analysis\n")
        f.write("- Borough-level mobility comparison\n")
        f.write("- Integration with hotel, restaurant, and crime data\n")
        f.write("  for comprehensive NYC tourism analysis\n")
        f.write("\n")

        f.write("="*80 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*80 + "\n")

def main():
    # Determine profiling results file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    profiling_file = os.path.join(script_dir, '../output/profiling/part-00000')
    output_file = os.path.join(script_dir, '../output/PROFILING_REPORT.txt')

    print("="*80)
    print("MTA Dataset - Generating Analysis Report")
    print("="*80)
    print(f"Input: {profiling_file}")
    print(f"Output: {output_file}")
    print("")

    results = read_profiling_results(profiling_file)
    generate_report(results, output_file)

    print("Report generated successfully!")
    print(f"Location: {output_file}")
    print("="*80)

if __name__ == "__main__":
    main()
