import pandas as pd
import os

os.makedirs('output', exist_ok=True)

df = pd.read_csv('output/engineering_burnout_scored.csv')
print(f"Loaded {len(df):,} rows")

final = df[[
    'employee_id',
    'employee_name',
    'team',
    'role_level',
    'week_start',
    'total_hours_worked',
    'overtime_hours_week',
    'after_hours_min_week',
    'pto_days_week',
    'meetings_count_week',
    'tasks_completed_week',
    'weekend_work_days',
    'busy_period_share',
    'workload_trend_4w',
    'baseline_hours',
    'hours_vs_baseline',
    'after_hrs_vs_baseline',
    'pto_vs_baseline',
    'burnout_score',
    'burnout_category'
]].copy()

final.to_csv('output/final_burnout_master.csv', index=False)
print(f"✅ Final master file saved: {len(final):,} rows, {len(final.columns)} columns")