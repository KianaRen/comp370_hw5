#!/usr/bin/env python3
import argparse
import csv
import sys
from datetime import datetime
from collections import defaultdict

def init_parse_args():
    parser = argparse.ArgumentParser(description="Count NYC 311 complaints by borough and type within a date range.")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file path")
    parser.add_argument("-s", "--start", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("-e", "--end", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("-o", "--output", help="Optional output CSV file")
    return parser.parse_args()

def main():
    args = init_parse_args()
    
    start_date = datetime.strptime(args.start, "%Y-%m-%d")
    end_date = datetime.strptime(args.end, "%Y-%m-%d")

    counts = defaultdict(int)

    with open(args.input, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            created_str = row["Created Date"].strip()
            if not created_str:
                continue
            created_date = datetime.strptime(created_str, "%m/%d/%Y %I:%M:%S %p")

            if start_date <= created_date <= end_date:
                complaint = row["Complaint Type"].strip()
                borough = row["Borough"].strip()
                if complaint and borough:
                    counts[(complaint, borough)] += 1

    results = [("complaint type", "borough", "count")]
    for (complaint, borough), count in sorted(counts.items()):
        results.append((complaint, borough, str(count)))

    if args.output:
        with open(args.output, "w", newline = "", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(results)

if __name__ == "__main__":
    main()
