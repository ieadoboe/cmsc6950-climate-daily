#!/usr/bin/env python3
"""Plot annual mean temperature trend"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from src.common import mpl_apply

mpl_apply()

df = pd.read_csv("data/dtr_dataset.csv")
df['date'] = pd.to_datetime(df['date'])
df['T_mean'] = (df['MIN_TEMPERATURE'] + df['MAX_TEMPERATURE']) / 2

annual_temp = df.groupby(df['date'].dt.year)['T_mean'].mean()

slope, intercept, r_value, p_value, std_err = stats.linregress(
    annual_temp.index, annual_temp.values
)

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(annual_temp.index, annual_temp.values, 'o',
        markersize=8, color='blue', label='Annual mean')

x_trend = np.array([annual_temp.index.min(), annual_temp.index.max()])
y_trend = slope * x_trend + intercept
ax.plot(x_trend, y_trend, '-.', linewidth=2.5, color='red',
        label=f'Trend: {slope:.3f}°C/year (p={p_value:.3f})')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Mean Temperature (°C)', fontsize=12)
ax.set_title('Annual Mean Temperature Trend in St. John\'s (2000-2025)',
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
plt.savefig("plots/mean_temp_trend.pdf", dpi=300, bbox_inches='tight')
print("Saved: mean_temp_trend.pdf")
