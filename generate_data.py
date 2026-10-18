#!/usr/bin/env python3
"""Generate the synthetic baseline CSV for the what-if simulator.

Creates data/enrollment_baseline.csv with five historical fall terms of
entirely SYNTHETIC data for a fictional university. Nothing here comes from
any real institution.

Usage:
    python generate_data.py
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
OUT = os.path.join(DATA_DIR, "enrollment_baseline.csv")

# Synthetic history for the fictional "Harborview University".
# Gentle upward drift with a dip in 2022, like many regionals saw.
ROWS = [
    # term, headcount, new_freshmen, new_transfers, retention, yield, discount, sticker
    (2020, 9850, 2100, 1050, 76.5, 22.0, 36.0, 22800),
    (2021, 10020, 2200, 1080, 77.2, 22.8, 36.5, 23300),
    (2022, 9720, 2050, 1020, 75.8, 21.5, 37.0, 23800),
    (2023, 10050, 2250, 1100, 77.8, 23.2, 37.5, 24300),
    (2024, 10250, 2350, 1150, 78.5, 24.0, 38.0, 24800),
]


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow([
            "fall_term", "total_headcount", "new_freshmen", "new_transfers",
            "retention_pct", "yield_pct", "discount_pct",
            "sticker_tuition_usd",
        ])
        writer.writerows(ROWS)
    print(f"wrote {OUT} ({len(ROWS)} synthetic terms)")


if __name__ == "__main__":
    main()
