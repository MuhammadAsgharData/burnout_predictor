import pandas as pd
import numpy as np
import os
from datetime import date, timedelta
import random

os.makedirs('output', exist_ok=True)
np.random.seed(42)
random.seed(42)

N_EMP = 500
START_DATE = date(2025, 7, 1)
END_DATE   = date(2026, 1, 31)
DATES = [START_DATE + timedelta(d) for d in range((END_DATE - START_DATE).days + 1)]

TEAMS      = ['Backend','Frontend','Platform','DevOps','Mobile','Data Engineering','QA Automation','Security Engineering']
ROLES      = ['Junior','Mid','Senior','Staff']
ROLE_WEIGHTS = [0.25, 0.35, 0.28, 0.12]

emp_ids   = [f'ENG_{str(i).zfill(4)}' for i in range(1, N_EMP+1)]
emp_names = [f'Employee_{str(i).zfill(4)}' for i in range(1, N_EMP+1)]
teams     = np.random.choice(TEAMS, N_EMP)
roles     = np.random.choice(ROLES, N_EMP, p=ROLE_WEIGHTS)

base_hours       = np.random.uniform(7.5, 9.2, N_EMP)
base_after_hrs   = np.random.uniform(10, 90, N_EMP)
base_pto_prob    = np.random.uniform(0.03, 0.10, N_EMP)
burnout_tendency = np.random.uniform(0.3, 1.0, N_EMP)

emp_df = pd.DataFrame({
    'employee_id': emp_ids,
    'employee_name': emp_names,
    'team': teams,
    'role_level': roles,
    'base_hours': base_hours,
    'base_after_hrs': base_after_hrs,
    'base_pto_prob': base_pto_prob,
    'burnout_tendency': burnout_tendency
})

all_weeks = sorted(set((d - timedelta(days=d.weekday())).isoformat() for d in DATES))
team_busy = {}
for team in TEAMS:
    busy_weeks = set(random.sample(all_weeks, k=int(len(all_weeks)*0.30)))
    team_busy[team] = busy_weeks

records = []
for _, emp in emp_df.iterrows():
    eid   = emp['employee_id']
    ename = emp['employee_name']
    team  = emp['team']
    role  = emp['role_level']
    bh    = emp['base_hours']
    bah   = emp['base_after_hrs']
    bpto  = emp['base_pto_prob']
    bt    = emp['burnout_tendency']

    for d in DATES:
        dow = d.weekday()
        is_weekend = dow >= 5
        week_str = (d - timedelta(days=dow)).isoformat()
        is_busy = week_str in team_busy[team]

        if is_weekend:
            weekend_work = 0
            if team in ['DevOps','Platform'] and is_busy and np.random.random() < 0.18 * bt:
                weekend_work = 1
            else:
                records.append({
                    'employee_id': eid, 'employee_name': ename, 'team': team,
                    'role_level': role, 'date': d.isoformat(),
                    'is_workday': 0, 'hours_worked': 0.0, 'overtime_hours': 0.0,
                    'after_hours_minutes': 0, 'meetings_count': 0, 'tasks_completed': 0,
                    'pto_flag': 0, 'pto_days': 0.0, 'weekend_work_flag': 0,
                    'sprint_phase': 'Weekend', 'busy_period_flag': int(is_busy)
                })
                continue

        pto_chance = bpto * (0.4 if is_busy else 1.0)
        pto_flag = 0 if is_weekend else (1 if np.random.random() < pto_chance else 0)
        pto_days = 1.0 if pto_flag else 0.0

        if pto_flag:
            records.append({
                'employee_id': eid, 'employee_name': ename, 'team': team,
                'role_level': role, 'date': d.isoformat(),
                'is_workday': 0, 'hours_worked': 0.0, 'overtime_hours': 0.0,
                'after_hours_minutes': 0, 'meetings_count': 0, 'tasks_completed': 0,
                'pto_flag': 1, 'pto_days': 1.0, 'weekend_work_flag': 0,
                'sprint_phase': 'PTO', 'busy_period_flag': int(is_busy)
            })
            continue

        crunch_mult = 1.25 if is_busy else 1.0
        role_mult = {'Junior': 0.95, 'Mid': 1.0, 'Senior': 1.08, 'Staff': 1.12}[role]
        noise = np.random.normal(0, 0.5)
        hours = round(min(max(0, bh * crunch_mult * role_mult + noise), 16.0), 2)
        overtime = round(max(0.0, hours - 8.0), 2)

        ah_base = bah * crunch_mult * bt
        after_hrs_min = int(min(max(0, ah_base + np.random.normal(0, 15) + overtime * 12), 240))

        mtg_base = {'Junior': 2, 'Mid': 3, 'Senior': 4, 'Staff': 5}[role]
        meetings = max(0, int(np.random.poisson(mtg_base * (1.2 if is_busy else 1.0))))
        tasks = max(0, int(np.random.poisson(5 * role_mult)))

        sprint_phase = 'Crunch' if is_busy else 'Normal'
        if is_busy and np.random.random() < 0.3:
            sprint_phase = 'Release'

        records.append({
            'employee_id': eid, 'employee_name': ename, 'team': team,
            'role_level': role, 'date': d.isoformat(),
            'is_workday': 1, 'hours_worked': hours, 'overtime_hours': overtime,
            'after_hours_minutes': after_hrs_min, 'meetings_count': meetings,
            'tasks_completed': tasks, 'pto_flag': 0, 'pto_days': 0.0,
            'weekend_work_flag': int(weekend_work if is_weekend else 0),
            'sprint_phase': sprint_phase, 'busy_period_flag': int(is_busy)
        })

raw_df = pd.DataFrame(records)
raw_df.to_csv('output/synthetic_engineering_activity.csv', index=False)
print(f"✅ Raw daily rows saved: {len(raw_df):,}")