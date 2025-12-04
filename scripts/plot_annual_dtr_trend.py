#!/usr/bin/env python3
"""Plot annual DTR trend with Mann-Kendall test"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kendalltau
from src.common import mpl_apply

mpl_apply()

df = pd.read_csv("data/dtr_dataset.csv")
df['date'] = pd.to_datetime(df['date'])

# Annual mean DTR
annual_dtr = df.groupby(df['date'].dt.year)['DTR'].mean()
years = annual_dtr.index.values
dtr_values = annual_dtr.values

# Mann-Kendall test
tau, p_value = kendalltau(years, dtr_values)

# Linear fit for visualization
slope, intercept = np.polyfit(years, dtr_values, 1)

# Plot
fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(years, dtr_values, s=60, alpha=0.6,
           color='blue', label='Annual mean DTR')
ax.plot(years, dtr_values, 'b-', alpha=0.3, linewidth=1)
ax.plot(years, slope * years + intercept,
        'r--', linewidth=2, label='Linear fit')

# Annotation
textstr = f'Mann-Kendall Test\n$\\tau$ = {tau:.4f}\np-value = {p_value:.4f}'
result = "No significant trend" if p_value >= 0.05 else "Significant trend"
box_color = 'lightblue' if p_value >= 0.05 else 'lightcoral'
textstr += f'\n{result}'

ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', bbox=dict(boxstyle='round',
                                           facecolor=box_color, alpha=0.8))

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Mean DTR (°C)', fontsize=12)
ax.set_title(
    'Annual Mean DTR Trend (2000–2025)\nMann-Kendall Test', fontsize=13)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig("plots/annual_dtr_trend.pdf", dpi=300)
print("Saved: annual_dtr_trend.pdf")
