
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAQ_API_KEY")

if not api_key:
    raise ValueError("OpenAQ API key not found!")

headers = {"X-API-Key": api_key}

url = "https://api.openaq.org/v3/locations"

params = {
    "coordinates": "28.6139,77.2090",
    "radius": 10000,
    "limit": 20
}

r = requests.get(
    url,
    headers=headers,
    params=params,
    timeout=30
)

print("Status:", r.status_code)
print("Response:", r.text[:2000])

r.raise_for_status()

data = r.json()

for loc in data["results"]:
    pm = [
        s for s in loc["sensors"]
        if s["parameter"]["name"] == "pm25"
    ]

    if pm:
        print(loc["id"], loc["name"], pm[0]["id"])


# Find all PM2.5 sensors

for loc in data["results"]:
    for sensor in loc["sensors"]:

        if sensor["parameter"]["name"] == "pm25":

            print(
                "Station:", loc["name"],
                "| Location ID:", loc["id"],
                "| Sensor ID:", sensor["id"],
                "| Unit:", sensor["parameter"]["units"]
            )
