import os
import csv
import requests
from datetime import datetime

# --------------------------
# Config
# --------------------------
API_KEY = os.getenv("CMC_API_KEY")  # CoinMarketCap API key
OUTPUT_FOLDER = "pine_seeds_fng"
CSV_FILE = "FNG.csv"
LIMIT = 500

# --------------------------
# Fetch JSON from CMC
# --------------------------
url = f"https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical?limit={LIMIT}"
headers = {"X-CMC_PRO_API_KEY": API_KEY}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("Error fetching data:", response.status_code, response.text)
    raise SystemExit(1)

data = response.json().get("data", [])

# --------------------------
# Convert to Pine Seeds CSV
# --------------------------
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

filepath = os.path.join(OUTPUT_FOLDER, CSV_FILE)

# Load existing data if any
data_dict = {}
if os.path.exists(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        for row in csv.reader(f):
            data_dict[row[0]] = row[1:]

# Update with latest F&G values
for item in data:
    ts = int(item["timestamp"])
    date = datetime.utcfromtimestamp(ts).strftime("%Y%m%d")
    val = item["value"]
    data_dict[date] = [val, val, val, val, 0, 0]  # open, high, low, close, volume, spread

# Write CSV
with open(filepath, "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    for date in sorted(data_dict.keys()):
        row = [date] + data_dict[date]
        writer.writerow(row)

print(f"Saved {len(data_dict)} records to {filepath}")
