
# ****************Previous while checking*****************************


# import os
# import requests
# import pandas as pd
# from dotenv import load_dotenv

# load_dotenv()

# headers = {
#     "X-API-Key": os.getenv("OPENAQ_API_KEY")
# }

# sensor_id = 14935

# url = f"https://api.openaq.org/v3/sensors/{sensor_id}/hours"

# params = {
#     "datetime_from": "2018-03-09T00:00:00Z",
#     "datetime_to": "2022-10-31T23:59:59Z",
#     "limit": 1000,"page":2
# }

# response = requests.get(
#     url,
#     headers=headers,
#     params=params,
#     timeout=60
# )

# data = response.json()

# print("Page:", data["meta"]["page"])
# print("Records:", len(data["results"]))
# print("First record:", data["results"][0]["period"])



# ************************Latest*************************888


import os
import time
import requests
import pandas as pd

from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
headers = {
    "X-API-Key": os.getenv("OPENAQ_API_KEY")
}

sensor_id = 14935

url = f"https://api.openaq.org/v3/sensors/{sensor_id}/hours"

# Pagination configuration
all_records = []
page = 1
limit = 1000

# Download historical measurements
while True:

    params = {
    "datetime_from": "2022-07-01T00:00:00Z",
    "datetime_to": "2022-12-31T23:59:59Z",
    "limit": 1000,
    "page": page
}

    # Retry mechanism
    for attempt in range(3):

        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=120
            )

            response.raise_for_status()
            break

        except requests.exceptions.RequestException as e:

            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt == 2:
                raise

            time.sleep(5 * (attempt + 1))

    # Extract records
    batch = response.json()["results"]

    if not batch:
        break

    all_records.extend(batch)

    print(f"Page {page}: Downloaded {len(batch)} records")

    # Stop when the final page is reached
    if len(batch) < limit:
        break

    page += 1

    # Avoid sending requests too quickly
    time.sleep(1)


# Convert records into DataFrame
df = pd.json_normalize(all_records)


# Create output directory
project_root = Path(__file__).resolve().parents[1]

output_dir = project_root / "data" / "raw"

output_dir.mkdir(parents=True, exist_ok=True)


# Save CSV
output_path = output_dir / "pm25_measurements2022_2.csv"

df.to_csv(output_path, index=False)


# Display download summary
print("\nDownload complete!")

print("Total records:", len(df))
print("Dataset shape:", df.shape)

print("Saved at:", output_path)
