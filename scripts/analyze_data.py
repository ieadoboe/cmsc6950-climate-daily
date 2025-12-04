#!/usr/bin/env python3
"""Analyze DTR data"""

import pandas as pd
from scipy import stats


def main():
    # Load prepared data
    df = pd.read_csv("data/dtr_dataset.csv")
    df['date'] = pd.to_datetime(df['date'])

    print("="*70)
    print("DTR ANALYSIS")
    print("="*70)

    # Annual temperature trend
    annual_temp = df.groupby('year')['T_mean'].mean()
    slope, _, _, p, _ = stats.linregress(annual_temp.index, annual_temp.values)
    print(f"\nTemperature trend: {slope:.4f}°C/year (p={p:.4f})")
    print(f"Total change: {slope * 26:.2f}°C")

    # Annual DTR trend
    annual_dtr = df.groupby('year')['DTR'].mean()
    slope, _, _, p, _ = stats.linregress(annual_dtr.index, annual_dtr.values)
    print(f"\nDTR trend: {slope:.4f}°C/year (p={p:.4f})")
    print(f"Significant: {'Yes' if p < 0.05 else 'No'}")

    # Seasonal DTR
    monthly_dtr = df.groupby('month')['DTR'].mean()
    print(
        f"\nSeasonal amplitude: {monthly_dtr.max() - monthly_dtr.min():.1f}°C")
    print(f"Spring mean: {monthly_dtr[3:6].mean():.1f}°C")
    print(f"Fall mean: {monthly_dtr[9:12].mean():.1f}°C")


if __name__ == "__main__":
    main()
