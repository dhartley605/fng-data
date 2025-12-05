import requests
import json
import os

# CONFIG
API_KEY = os.getenv("CMC_API_KEY")  # From GitHub Secrets
OUTPUT_FILE = "fng.json"
LIMIT = 500  # Max records CMC allows

if not API_KEY:
    raise ValueError("Missing CMC_API_KEY environment variable")

# Fetch historical data
url = f"https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical?limit={LIMIT}"
headers = {"X-CMC_PRO_API_KEY": API_KEY}

print("Fetching Fear & Greed Index data...")
response = requests.get(url, headers=headers)
print("HTTP Status Code:", response.status_code)

if response.status_code != 200:
    print("Error fetching data:", response.text)
    raise SystemExit(1)

data = response.json().get("data", [])
fng_dict = {}

for item in data:
    date_str = item["timestamp"][:10]  # YYYY-MM-DD
    value = item["value"]
    fng_dict[date_str] = value

# Save JSON file
with open(OUTPUT_FILE, "w") as f:
    json.dump(fng_dict, f, indent=2)

print(f"Saved {len(fng_dict)} records to {OUTPUT_FILE}")
