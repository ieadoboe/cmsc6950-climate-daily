#!/usr/bin/env python3
"""Plot DTR time series"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from src.common import mpl_apply

mpl_apply()

df = pd.read_csv("data/dtr_dataset.csv")
df['date'] = pd.to_datetime(df['date'])

plt.figure(figsize=(12, 5))
plt.plot(df["date"], df["DTR"], color="blue", linewidth=0.5, alpha=0.7)
plt.title('Diurnal Temperature Range (DTR) in St. John\'s (2000-2025)')
plt.xlabel('Year')
plt.ylabel('DTR (°C)')

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=45)

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("plots/dtr_over_time.pdf", dpi=300)
print("Saved: dtr_over_time.pdf")
