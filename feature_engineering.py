import pandas as pd
import numpy as np

df = pd.read_csv('output/cleaned_data.csv')
df['date'] = pd.to_datetime(df['date'])
df['week_start'] = (df['date'] - pd.to_timedelta(df['date'].dt.weekday, unit='d')).dt.date.astype(str)

weekly = df.groupby(['employee_id','employee_name','team','role_level','week_start']).agg(
    total_hours_worked   = ('hours_worked', 'sum'),
    overtime_hours_week  = ('overtime_hours', 'sum'),
    after_hours_min_week = ('after_hours_minutes', 'sum'),
    meetings_count_week  = ('meetings_count', 'sum'),
    tasks_completed_week = ('tasks_completed', 'sum'),
    pto_days_week        = ('pto_days', 'sum'),
    days_worked_week     = ('is_workday', 'sum'),
    weekend_work_days    = ('weekend_work_flag', 'sum'),
    busy_period_share    = ('busy_period_flag', 'mean'),
).reset_index()

sorted_weeks = sorted(weekly['week_start'].unique())
first_8 = sorted_weeks[:8]
baseline = weekly[weekly['week_start'].isin(first_8)].groupby('employee_id').agg(
    baseline_hours     = ('total_hours_worked', 'median'),
    baseline_after_hrs = ('after_hours_min_week', 'median'),
    baseline_pto       = ('pto_days_week', 'median'),
).reset_index()

weekly = weekly.merge(baseline, on='employee_id', how='left')
weekly = weekly.sort_values(['employee_id','week_start'])
weekly['workload_trend_4w'] = (
    weekly.groupby('employee_id')['total_hours_worked']
    .transform(lambda x: x.rolling(4, min_periods=1).mean())
    .round(2)
)

weekly['hours_vs_baseline']     = (weekly['total_hours_worked'] - weekly['baseline_hours']).round(2)
weekly['after_hrs_vs_baseline'] = (weekly['after_hours_min_week'] - weekly['baseline_after_hrs']).round(1)
weekly['pto_vs_baseline']       = (weekly['pto_days_week'] - weekly['baseline_pto']).round(2)

weekly.to_csv('output/engineering_features_weekly.csv', index=False)
print(f"✅ Weekly features saved: {len(weekly):,} rows")