import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("CMC_API_KEY")
OUTPUT_FILE = "fng.json"
LIMIT = 500

if not API_KEY:
    raise ValueError("Missing CMC_API_KEY environment variable")

url = f"https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical?limit={LIMIT}"
headers = {"X-CMC_PRO_API_KEY": API_KEY}

print("Fetching Fear & Greed Index…")
r = requests.get(url, headers=headers)
print("Status:", r.status_code)

if r.status_code != 200:
    print(r.text)
    raise SystemExit(1)

records = r.json().get("data", [])
result = {}

for item in records:
    # Convert unix timestamp → YYYY-MM-DD
    ts = int(item["timestamp"])
    date = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")

    result[date] = item["value"]

# Save file
with open(OUTPUT_FILE, "w") as f:
    json.dump(result, f, indent=2)

print(f"Saved {len(result)} records to {OUTPUT_FILE}")
