import requests
import json
import os

# -------------------------------
# CONFIG
# -------------------------------
API_KEY = os.getenv("CMC_API_KEY")    # from GitHub Secrets
OUTPUT_FILE = "fng.json"
LIMIT = 500                            # CMC max limit

if not API_KEY:
    raise ValueError("Missing CMC_API_KEY environment variable")

# -------------------------------
# Fetch Historical Data
# -------------------------------
url = f"https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical?limit={LIMIT}"
headers = {"X-CMC_PRO_API_KEY": API_KEY}

print("Fetching Fear & Greed Index data...")
response = requests.get(url, headers=headers)
print("HTTP Status Code:", response.status_code)

if response.status_code != 200:
    print("Error fetching data:", response.text)
    raise SystemExit(1)

resp_json = response.json()
data = resp_json.get("data", [])

if not data:
    print("Warning: No data received from API")
    
# -------------------------------
# Format into Date -> Value
# -------------------------------
fng_dict = {}
for item in data:
    date_str = item.get("timestamp", "")[:10]
    value = item.get("value")
    if date_str and value is not None:
        fng_dict[date_str] = value

# -------------------------------
# Save output file
# -------------------------------
with open(OUTPUT_FILE, "w") as f:
    json.dump(fng_dict, f, indent=2)

print(f"Saved {len(fng_dict)} records to {OUTPUT_FILE}")
