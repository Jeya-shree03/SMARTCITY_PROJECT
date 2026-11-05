import requests
import pandas as pd
from pathlib import Path

API_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"

output_folder = Path("data/raw")
output_folder.mkdir(parents=True, exist_ok=True)

params = {
    "$select": "unique_key,created_date,closed_date,agency,complaint_type,borough",
    "$order": "created_date DESC",
    "$limit": 10000
}

print("Downloading NYC 311 data...")

response = requests.get(
    API_URL,
    params=params,
    timeout=120
)

response.raise_for_status()

df = pd.DataFrame(response.json())

df.to_csv(
    output_folder / "311_complaints.csv",
    index=False
)

print("Download successful!")
print("Total records:", len(df))
print(df.head())