import pandas as pd
from pathlib import Path

raw = Path("data/raw/311_complaints.csv")
out = Path("data/processed")
out.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(raw, encoding="utf-8-sig", low_memory=False)

# Borough-wise complaint counts
borough = df["borough"].fillna("Unspecified").astype(str).str.strip()
borough = borough.replace("", "Unspecified")
borough_counts = borough.value_counts().rename_axis("borough").reset_index(name="complaint_count")
borough_counts.to_csv(out / "borough_analysis.csv", index=False)

# Complaint resolution time
df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
df["closed_date"] = pd.to_datetime(df["closed_date"], errors="coerce")
df["resolution_hours"] = (
    (df["closed_date"] - df["created_date"]).dt.total_seconds() / 3600
)

valid = df[df["resolution_hours"].notna() & (df["resolution_hours"] >= 0)].copy()

columns = [
    "unique_key", "created_date", "closed_date",
    "complaint_type", "borough", "resolution_hours"
]
valid[columns].to_csv(out / "resolution_analysis.csv", index=False)

summary = pd.DataFrame([
    {"metric": "Total complaints", "value": len(df)},
    {"metric": "Closed complaints", "value": int(df["closed_date"].notna().sum())},
    {"metric": "No closed date", "value": int(df["closed_date"].isna().sum())},
    {"metric": "Valid resolution records", "value": len(valid)},
    {"metric": "Average resolution hours", "value": round(valid["resolution_hours"].mean(), 2) if len(valid) else None},
    {"metric": "Median resolution hours", "value": round(valid["resolution_hours"].median(), 2) if len(valid) else None},
])
summary.to_csv(out / "resolution_summary.csv", index=False)

print("SUCCESS! Power BI files created:")
print("1. data/processed/borough_analysis.csv")
print("2. data/processed/resolution_analysis.csv")
print("3. data/processed/resolution_summary.csv")
print("\nBorough counts:")
print(borough_counts.to_string(index=False))
print("\nResolution summary:")
print(summary.to_string(index=False))
