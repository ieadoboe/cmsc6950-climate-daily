#!/usr/bin/env python3
"""Plot extreme event trends with Mann-Kendall test"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import kendalltau
from src.common import mpl_apply

mpl_apply()

df = pd.read_csv("data/dtr_dataset.csv")
df['date'] = pd.to_datetime(df['date'])

dtr_90th = df['DTR'].quantile(0.9)
dtr_10th = df['DTR'].quantile(0.1)

df['high_dtr_extreme'] = df['DTR'] > dtr_90th
df['low_dtr_extreme'] = df['DTR'] < dtr_10th

annual_high = df.groupby(df['date'].dt.year)['high_dtr_extreme'].sum()
annual_low = df.groupby(df['date'].dt.year)['low_dtr_extreme'].sum()

years = annual_high.index.values
high_counts = annual_high.values
low_counts = annual_low.values

# Mann-Kendall tests
tau_high, p_value_high = kendalltau(years, high_counts)
tau_low, p_value_low = kendalltau(years, low_counts)

# Linear fits
slope_high, intercept_high, _, _, _ = stats.linregress(years, high_counts)
slope_low, intercept_low, _, _, _ = stats.linregress(years, low_counts)

# Plot
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# High extremes
axes[0].scatter(years, high_counts, alpha=0.6, s=60, color='red',
                label='Annual count', zorder=3)
axes[0].plot(years, slope_high * years + intercept_high, 'r--',
             linewidth=2.5, alpha=0.7, label='Linear fit', zorder=2)

textstr_high = (f'Mann-Kendall Test\n$\\tau$ = {tau_high:.4f}\n'
                f'p-value = {p_value_high:.4f}\n')
result_high = "No trend" if p_value_high >= 0.05 else "Significant"
box_color_high = 'lightblue' if p_value_high >= 0.05 else 'lightcoral'
textstr_high += result_high

axes[0].text(0.05, 0.95, textstr_high, transform=axes[0].transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor=box_color_high, alpha=0.8))

axes[0].set_title('High-DTR Extreme Days per Year\n(90th percentile)',
                  fontsize=12, fontweight='bold')
axes[0].set_xlabel('Year', fontsize=11)
axes[0].set_ylabel('Count', fontsize=11)
axes[0].grid(True, alpha=0.3)
axes[0].legend(loc='upper right', fontsize=10)

# Low extremes
axes[1].scatter(years, low_counts, alpha=0.6, s=60, color='blue',
                label='Annual count', zorder=3)
axes[1].plot(years, slope_low * years + intercept_low, 'b--',
             linewidth=2.5, alpha=0.7, label='Linear fit', zorder=2)

textstr_low = (f'Mann-Kendall Test\n$\\tau$ = {tau_low:.4f}\n'
               f'p-value = {p_value_low:.4f}\n')
result_low = "No trend" if p_value_low >= 0.05 else "Significant"
box_color_low = 'lightblue' if p_value_low >= 0.05 else 'lightgreen'
textstr_low += result_low

axes[1].text(0.05, 0.95, textstr_low, transform=axes[1].transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor=box_color_low, alpha=0.8))

axes[1].set_title('Low-DTR Extreme Days per Year\n(10th percentile)',
                  fontsize=12, fontweight='bold')
axes[1].set_xlabel('Year', fontsize=11)
axes[1].grid(True, alpha=0.3)
axes[1].legend(loc='upper right', fontsize=10)

fig.suptitle('DTR Extreme Event Trends (2000–2025): Mann-Kendall Analysis',
             fontsize=14, fontweight='bold', y=0.98)

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.savefig("plots/mann_kendall_extremes.pdf", dpi=300, bbox_inches='tight')
print("Saved: mann_kendall_extremes.pdf")
