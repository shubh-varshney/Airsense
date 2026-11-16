
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

headers = {
    "X-API-Key": os.getenv("OPENAQ_API_KEY")
}

sensor_ids = [34,35,388,5398,    13860,    13861,    14087,    14617,    12234769,    14860,    14935,   15071
]

for sensor_id in sensor_ids:

    url = f"https://api.openaq.org/v3/sensors/{sensor_id}"

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        sensor = response.json()["results"][0]

        first = sensor.get("datetimeFirst")
        last = sensor.get("datetimeLast")

        if first and last:
            first_date = datetime.fromisoformat(first["utc"])
            last_date = datetime.fromisoformat(last["utc"])

            days = (last_date - first_date).days

            print("\nSensor ID:", sensor_id)
            print("Parameter:", sensor["parameter"]["name"])
            print("First:", first_date)
            print("Last:", last_date)
            print("Duration:", days, "days")

    except requests.exceptions.RequestException as e:
        print("Error with sensor", sensor_id, ":", e)
