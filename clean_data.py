import pandas as pd
from pathlib import Path

# Read raw dataset
input_file = "data/raw/311_complaints.csv"

df = pd.read_csv(input_file)

print("Original records:", len(df))

# Remove duplicate complaints
df = df.drop_duplicates(subset="unique_key")

# Remove records without complaint date
df = df.dropna(subset=["created_date"])

# Convert date columns
df["created_date"] = pd.to_datetime(
    df["created_date"], errors="coerce"
)

df["closed_date"] = pd.to_datetime(
    df["closed_date"], errors="coerce"
)

# Remove invalid creation dates
df = df.dropna(subset=["created_date"])

# Calculate resolution time
df["resolution_hours"] = (
    df["closed_date"] - df["created_date"]
).dt.total_seconds() / 3600

# Remove negative resolution times
df.loc[
    df["resolution_hours"] < 0,
    "resolution_hours"
] = None

# Complaint status
df["complaint_status"] = df["closed_date"].apply(
    lambda x: "Closed" if pd.notna(x) else "Open"
)

# Save cleaned dataset
Path("data/processed").mkdir(
    parents=True, exist_ok=True
)

df.to_csv(
    "data/processed/311_cleaned.csv",
    index=False
)

print("Data cleaning completed!")
print("Cleaned records:", len(df))
print("\nComplaint Status:")
print(df["complaint_status"].value_counts())

print("\nCleaned data:")
print(df.head())