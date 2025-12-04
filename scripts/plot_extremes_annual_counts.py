#!/usr/bin/env python3
"""Plot annual counts of extreme DTR events"""

import pandas as pd
import matplotlib.pyplot as plt
from src.common import mpl_apply

mpl_apply()

df = pd.read_csv("data/dtr_dataset.csv")
df['date'] = pd.to_datetime(df['date'])

dtr_90th = df['DTR'].quantile(0.9)
dtr_10th = df['DTR'].quantile(0.1)

df['high_dtr_extreme'] = df['DTR'] > dtr_90th
df['low_dtr_extreme'] = df['DTR'] < dtr_10th

high_per_year = df[df['high_dtr_extreme']].groupby(df['date'].dt.year).size()
low_per_year = df[df['low_dtr_extreme']].groupby(df['date'].dt.year).size()

fig, axes = plt.subplots(2, 1, figsize=(10, 5), sharex=True, sharey=True)

high_per_year.plot(kind='bar', color='red', alpha=0.7, ax=axes[0])
axes[0].set_title('High-DTR Extreme Days per Year')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Count')
axes[0].grid(axis='y', alpha=0.3)

low_per_year.plot(kind='bar', color='blue', alpha=0.7, ax=axes[1])
axes[1].set_title('Low-DTR Extreme Days per Year')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Count')
axes[1].grid(axis='y', alpha=0.3)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig("plots/dtr_extremes_per_year.pdf", dpi=300)
print("Saved: dtr_extremes_per_year.pdf")
