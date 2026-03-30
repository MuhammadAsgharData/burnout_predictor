import pandas as pd
import numpy as np

df = pd.read_csv('output/synthetic_engineering_activity.csv')

df['date'] = pd.to_datetime(df['date'])
df['hours_worked']        = df['hours_worked'].astype(float).round(2)
df['overtime_hours']      = df['overtime_hours'].astype(float).round(2)
df['after_hours_minutes'] = df['after_hours_minutes'].astype(int)
df['meetings_count']      = df['meetings_count'].astype(int)
df['tasks_completed']     = df['tasks_completed'].astype(int)
df['pto_flag']            = df['pto_flag'].astype(int)
df['weekend_work_flag']   = df['weekend_work_flag'].astype(int)
df['busy_period_flag']    = df['busy_period_flag'].astype(int)

before = len(df)
df = df.drop_duplicates(subset=['employee_id', 'date'])
print(f"Duplicates removed: {before - len(df)}")

df['hours_worked']        = df['hours_worked'].clip(lower=0)
df['overtime_hours']      = df['overtime_hours'].clip(lower=0)
df['after_hours_minutes'] = df['after_hours_minutes'].clip(lower=0)

df['overtime_hours'] = df.apply(
    lambda r: round(max(r['hours_worked'] - 8.0, 0), 2)
    if r['is_workday'] == 1 else 0.0, axis=1
)

df['team']         = df['team'].str.strip().str.title()
df['role_level']   = df['role_level'].str.strip().str.title()
df['sprint_phase'] = df['sprint_phase'].str.strip().str.title()

print("Missing values per column:")
print(df.isnull().sum())

df.to_csv('output/cleaned_data.csv', index=False)
print(f"✅ Cleaned dataset saved: {len(df):,} rows")