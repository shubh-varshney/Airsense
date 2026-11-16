import os
import requests
from dotenv import load_dotenv

load_dotenv()

headers= { "X-API-KEY":os.getenv("OPENAQ_API_KEY")}
sensor_id = 15071
url = f"https://api.openaq.org/v3/sensors/{sensor_id}"
response = requests.get(
    url,
    headers=headers,
    timeout=30
)
response.raise_for_status()

sensor = response.json()["results"][0]

print("Sensor:", sensor["name"])
print("Parameter:", sensor["parameter"]["name"])

print("\nFirst measurement:")
print(sensor.get("datetimeFirst"))

print("\nLast measurement:")
print(sensor.get("datetimeLast"))

print("\nCoverage:")
print(sensor.get("coverage"))
