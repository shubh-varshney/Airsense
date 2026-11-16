
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

headers = {
    "X-API-Key": os.getenv("OPENAQ_API_KEY")
}

sensor_id = 14935

url = f"https://api.openaq.org/v3/sensors/{sensor_id}/hours"

params = {
    "limit": 10
}

response = requests.get(
    url,
    headers=headers,
    params=params,
    timeout=30
)

response.raise_for_status()

data = response.json()

# Convert JSON into a Pandas DataFrame
df = pd.json_normalize(data["results"])

# Display useful columns
print(df[[
    "period.label",
    "value",
    "parameter.units",
    "period.datetimeFrom.utc",
    "period.datetimeTo.utc",
    "coverage.percentComplete"
]])

print("\nDataset shape:", df.shape)
print("\nAll columns:")
print(df.columns.tolist())
