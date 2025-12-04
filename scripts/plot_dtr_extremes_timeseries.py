#!/usr/bin/env python3
"""Plot DTR with extreme events highlighted"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from src.common import mpl_apply

mpl_apply()

df = pd.read_csv("data/dtr_dataset.csv")
df['date'] = pd.to_datetime(df['date'])

# Calculate thresholds
dtr_90th = df['DTR'].quantile(0.9)
dtr_10th = df['DTR'].quantile(0.1)

df['high_dtr_extreme'] = df['DTR'] > dtr_90th
df['low_dtr_extreme'] = df['DTR'] < dtr_10th

# Plot
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(df["date"], df["DTR"], color="blue", linewidth=0.5, alpha=0.5,
        label='Daily DTR', zorder=1)

high_extremes = df[df['high_dtr_extreme']]
low_extremes = df[df['low_dtr_extreme']]

ax.scatter(high_extremes["date"], high_extremes["DTR"],
           color='red', s=15, alpha=0.7,
           label='High-DTR extremes (>90th %ile)', zorder=3)
ax.scatter(low_extremes["date"], low_extremes["DTR"],
           color='orange', s=15, alpha=0.7,
           label='Low-DTR extremes (<10th %ile)', zorder=3)

ax.axhline(dtr_90th, color='red', linestyle='--', linewidth=1.5, alpha=0.7,
           label=f'90th percentile: {dtr_90th:.2f}°C')
ax.axhline(dtr_10th, color='orange', linestyle='--', linewidth=1.5, alpha=0.7,
           label=f'10th percentile: {dtr_10th:.2f}°C')

ax.set_title('Diurnal Temperature Range with Extreme Events (2000-2025)',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('DTR (°C)', fontsize=12)

ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=45)

ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='best', fontsize=9, framealpha=0.9)

plt.tight_layout()
plt.savefig("plots/dtr_over_time_with_extremes.pdf",
            dpi=300, bbox_inches='tight')
print("Saved: dtr_over_time_with_extremes.pdf")
