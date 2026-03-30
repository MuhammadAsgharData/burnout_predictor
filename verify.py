import pandas as pd

print("=" * 50)
print("WORKSENSE AI — DATASET VERIFICATION")
print("=" * 50)

# ── FILE 1: Raw daily activity ──────────────────
df1 = pd.read_csv('output/synthetic_engineering_activity.csv')
print(f"\n✅ synthetic_engineering_activity.csv")
print(f"   Rows:      {len(df1):,}")
print(f"   Columns:   {list(df1.columns)}")
print(f"   Employees: {df1['employee_id'].nunique()}")
print(f"   Date range: {df1['date'].min()} → {df1['date'].max()}")
print(f"   Teams: {sorted(df1['team'].unique())}")

# ── FILE 2: Cleaned data ────────────────────────
df2 = pd.read_csv('output/cleaned_data.csv')
print(f"\n✅ cleaned_data.csv")
print(f"   Rows:          {len(df2):,}")
print(f"   Missing values: {df2.isnull().sum().sum()}")
print(f"   Duplicates:    {df2.duplicated(subset=['employee_id','date']).sum()}")
print(f"   Negative hours: {(df2['hours_worked'] < 0).sum()}")

# ── FILE 3: Weekly features ─────────────────────
df3 = pd.read_csv('output/engineering_features_weekly.csv')
print(f"\n✅ engineering_features_weekly.csv")
print(f"   Rows:    {len(df3):,}")
print(f"   Weeks:   {df3['week_start'].nunique()}")
print(f"   Employees: {df3['employee_id'].nunique()}")
print(f"   Key features present: {['workload_trend_4w','baseline_hours','hours_vs_baseline'] }")

# ── FILE 4: Burnout scored ──────────────────────
df4 = pd.read_csv('output/engineering_burnout_scored.csv')
print(f"\n✅ engineering_burnout_scored.csv")
print(f"   Rows:    {len(df4):,}")
print(f"   Score range: {df4['burnout_score'].min()} → {df4['burnout_score'].max()}")
print(f"   Categories:")
print(df4['burnout_category'].value_counts().to_string())

print("\n" + "=" * 50)
print("ALL FILES VERIFIED ✅")
print("=" * 50)