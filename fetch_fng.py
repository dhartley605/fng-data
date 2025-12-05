# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 17:59:26 2025

@author: prade_mi
"""

import requests
import json
import os
 
# -------------------------------------
# CONFIG
# -------------------------------------
API_KEY = os.getenv("CMC_API_KEY")       # Pull API key from environment variable (safe for GitHub Actions)
OUTPUT_FILE = "fng.json"                 # JSON output file
LIMIT = 5000                             # Max available history

if not API_KEY:
    raise ValueError("Missing CMC_API_KEY environment variable")

# -------------------------------------
# Fetch Historical Data
# -------------------------------------
url = f"https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical?limit={LIMIT}"
headers = {"X-CMC_PRO_API_KEY": API_KEY}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Error fetching data:", response.status_code, response.text)
    raise SystemExit(1)

data = response.json().get("data", [])

# -------------------------------------
# Format Into Date -> Value Dictionary
# -------------------------------------
fng_dict = {}

for item in data:
    date_str = item["timestamp"][:10]       # Extract YYYY-MM-DD
    value = item["value"]
    fng_dict[date_str] = value

# -------------------------------------
# Save Output File
# -------------------------------------
with open(OUTPUT_FILE, "w") as f:
    json.dump(fng_dict, f, indent=2)

print(f"Saved {len(fng_dict)} records to {OUTPUT_FILE}")
