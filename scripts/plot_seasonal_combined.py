#!/usr/bin/env python3
"""Plot seasonal DTR pattern (boxplot + line)"""

import pandas as pd
import matplotlib.pyplot as plt
from src.common import mpl_apply

mpl_apply()

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

df = pd.read_csv("data/dtr_dataset.csv")
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['month_name'] = pd.Categorical(df['date'].dt.strftime('%b'),
                                  categories=MONTHS, ordered=True)

monthly_dtr = df.groupby('month')['DTR'].mean()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True, sharey=True)

# Boxplot
df.boxplot(column='DTR', by='month_name', ax=ax1, patch_artist=True,
           boxprops=dict(facecolor='lightblue', alpha=0.7, linewidth=1.5),
           medianprops=dict(color='black', linewidth=2.5),
           whiskerprops=dict(color='black', linewidth=1.5),
           capprops=dict(color='black', linewidth=1.5),
           flierprops=dict(marker='o', markerfacecolor='lightgray',
                           markersize=4, alpha=0.5))

ax1.set_title('DTR Distribution by Month',
              fontsize=13, fontweight='bold', pad=10)
ax1.set_xlabel('')
ax1.set_ylabel('DTR (°C)', fontsize=11)
ax1.grid(True, alpha=0.3, linestyle='--', axis='y')

# Mean line
ax2.plot(monthly_dtr.index, monthly_dtr.values, 'o-', color='blue',
         linewidth=2.5, markersize=5, markeredgewidth=2)
ax2.set_title('Mean DTR by Month', fontsize=13, fontweight='bold', pad=10)
ax2.set_xlabel('Month', fontsize=11)
ax2.set_ylabel('DTR (°C)', fontsize=11)
ax2.set_xticks(range(1, 13))
ax2.set_xticklabels(MONTHS)
ax2.grid(True, alpha=0.3, linestyle='--')

fig.suptitle('DTR Seasonal Pattern in St. John\'s (2000-2025)',
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig("plots/dtr_seasonal_combined.pdf", dpi=300)
print("Saved: dtr_seasonal_combined.pdf")
