#!/usr/bin/env python3
"""Prepare climate data for analysis"""

import pandas as pd
from src.dtr_calc import calculate_dtr


def main():
    # Load data
    print("Loading data...")
    df = pd.read_csv("data/climate-daily_complete.csv")

    # Create date column
    df['date'] = pd.to_datetime(
        df[['LOCAL_YEAR', 'LOCAL_MONTH', 'LOCAL_DAY']].rename(
            columns={'LOCAL_YEAR': 'year',
                     'LOCAL_MONTH': 'month', 'LOCAL_DAY': 'day'}
        ))
    df = df.sort_values('date')

    # Remove invalid temperatures (T_min > T_max)
    invalid_count = (df["MAX_TEMPERATURE"] < df["MIN_TEMPERATURE"]).sum()
    print(f"Removing {invalid_count} invalid records")
    df = df[df["MAX_TEMPERATURE"] >= df["MIN_TEMPERATURE"]].copy()

    # Calculate DTR and mean temperature
    df["DTR"] = calculate_dtr(df["MIN_TEMPERATURE"], df["MAX_TEMPERATURE"])
    df['T_mean'] = (df['MIN_TEMPERATURE'] + df['MAX_TEMPERATURE']) / 2

    # Add month columns
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%b')
    df['year'] = df['date'].dt.year

    # Save
    df.to_csv("data/dtr_dataset.csv", index=False)
    print(f"Saved {len(df)} records to dtr_dataset.csv")


if __name__ == "__main__":
    main()
