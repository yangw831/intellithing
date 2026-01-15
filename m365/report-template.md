## **Loyalty Program Stats Report Template**

**Slide 1: Loyalty Program Stats Report**
*   Subtitle: “Reporting Period: \[Date Range]”
*   “Generated: \[Timestamp]”
*   No AI-generated content warnings.

**Slide 2: Executive Summary**
*   Net Points Liability: $XX,XXX
*   Program ROI: XXX%
*   Financial Health Status: \[Healthy/Caution/At Risk]
*   Brief summary of data quality checks and any data limitations.

**Slide 3: Points Liability Analysis**
*   Total Outstanding Points: X,XXX,XXX points
*   Gross Liability (at $0.01/point): $XX,XXX
*   Estimated Breakage (XX%): -$X,XXX
*   **Net Liability: $XX,XXX**
*   Month-over-month change: ±X%
*   Liability-to-Revenue Ratio: XX%
*   Industry Benchmark: 10–20% (Your status: \[Healthy/High/Low])

**Slide 4: Redemption & Breakage Metrics**
*   **Total Points Earned:** X,XXX,XXX
*   **Total Points Redeemed:** XXX,XXX
*   **Redemption Rate:** XX% (Benchmark: 8–18% for ecommerce)
*   **Breakage Rate:** XX% (Typical: 15–30%)
*   **Orders with Redemption:** X,XXX of X,XXX (XX%)
*   **You MUST insert a chart image named `redemption_breakage_pie.png` showing the proportion of points redeemed vs. broken.**
    *   If the chart cannot be computed (e.g., total\_redeemed > total\_earned, or no valid data), render \[MISSING] and add the reason to Slide 2.

**Python Chart Generation Example**

```python
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv('customers_sample.csv')
earned = pd.to_numeric(df['lifetime_points_earned'], errors='coerce').fillna(0)
redeemed = pd.to_numeric(df['lifetime_points_redeemed'], errors='coerce').fillna(0)

total_earned = float(earned.clip(lower=0).sum())
total_redeemed = float(redeemed.clip(lower=0).sum())

if total_earned <= 0 or total_redeemed < 0 or total_redeemed > total_earned:
    raise ValueError("Cannot compute chart: invalid totals (redeemed > earned or no valid data).")

breakage = max(total_earned - total_redeemed, 0.0)
labels = ["Redeemed", "Broken"]
sizes = [total_redeemed, breakage]
colors = ["#2F6FED", "#F5A623"]

plt.figure(figsize=(5.2, 5.2))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, textprops={"color": "#222", "fontsize": 10})
plt.title("Points Redeemed vs. Broken", fontsize=12)
plt.tight_layout()
plt.savefig("redemption_breakage_pie.png", dpi=200)
plt.close()
```

**Instructions for the agent:**

*   Insert `redemption_breakage_pie.png` on Slide 4.
*   If chart generation fails, show \[MISSING] and add the error reason to Slide 2’s data limitations.

**Slide 5: Program ROI Analysis**
*   Total Program Revenue: $XXX,XXX
*   Member Revenue Contribution: XX% of total revenue
*   Points Liability Cost: $XX,XXX
*   Operational Costs: $X,XXX
*   **Total Program Costs: $XX,XXX**
*   Net Profit: $XXX,XXX
*   **Program ROI: XXX%**
*   Industry Benchmark: 300–500% (Your status: \[Excellent/Good/Below Target])

**Slide 6: Key Performance Indicators**
*   Table with columns: Metric | Your Program | Industry Benchmark | Status (On Par / Below Benchmark)
*   Metrics: Redemption Rate, Breakage Rate, Liability/Revenue, Program ROI

**Slide 7: Appendix: Data Sources**
*   Customer Data: \[file name, date]
*   Order History: \[file name, date]
*   Calculation Methodology: Industry-standard formulas
*   Benchmarks Source
