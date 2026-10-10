import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
import build_dashboards

errors = []
for spec in build_dashboards.DASHBOARD_SPECS:
    csv_path = spec['csv']
    if not os.path.exists(csv_path):
        errors.append(f"Missing CSV: {csv_path}")
        continue
    df = pd.read_csv(csv_path)
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    if len(num_cols) < 2:
        errors.append(f"{spec['id']} has only {len(num_cols)} numeric columns")

print(f"Total dashboards checked: {len(build_dashboards.DASHBOARD_SPECS)}")
print(f"Total errors: {len(errors)}")
if errors:
    print("Errors:", errors[:10])
else:
    print("All 94 datasets exist and have at least 2 numeric columns!")
