import pandas as pd
import numpy as np

weekly = pd.read_csv('output/engineering_features_weekly.csv')

O = (weekly['overtime_hours_week'] / 20.0).clip(0, 1)
ah_excess = (weekly['after_hrs_vs_baseline']).clip(0, None)
A = (ah_excess / 300).clip(0, 1)
recovery_gap = (weekly['baseline_pto'] - weekly['pto_days_week']).clip(0, None)
R = (recovery_gap / (weekly['baseline_pto'] + 0.5)).clip(0, 1)
workload_excess = (weekly['workload_trend_4w'] - weekly['baseline_hours']).clip(0, None)
W = (workload_excess / 20).clip(0, 1)

weekly['burnout_score'] = (100 * (0.35*O + 0.25*A + 0.20*R + 0.20*W)).round(1)

def categorize(score):
    if score < 35:   return 'Low'
    elif score < 65: return 'Moderate'
    elif score < 80: return 'High'
    else:            return 'Critical'

weekly['burnout_category'] = weekly['burnout_score'].apply(categorize)

weekly.to_csv('output/engineering_burnout_scored.csv', index=False)
print(f"✅ Burnout scored dataset saved: {len(weekly):,} rows")
print(weekly['burnout_category'].value_counts())