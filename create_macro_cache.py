"""
Create Mock Macro Cache Data
Simulates real data from VIX and FRED for demonstration
"""

import sys
import json
import os
from datetime import datetime

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

cache_dir = "data/macro_cache"
os.makedirs(cache_dir, exist_ok=True)

print("Creating mock macro cache data...\n")

# VIX data
vix_data = {
    "value": 16.85,
    "fetched_at": datetime.now().isoformat(),
    "source": "Yahoo Finance (^VIX)"
}

with open(os.path.join(cache_dir, "vix.json"), 'w') as f:
    json.dump(vix_data, f, indent=2)
print(f"✓ Created VIX cache: {vix_data['value']}")

# Unemployment Rate (FRED UNRATE)
unemployment_data = {
    "value": 3.9,
    "series_id": "UNRATE",
    "fetched_at": datetime.now().isoformat(),
    "source": "FRED API"
}

with open(os.path.join(cache_dir, "fred_unrate.json"), 'w') as f:
    json.dump(unemployment_data, f, indent=2)
print(f"✓ Created Unemployment cache: {unemployment_data['value']}%")

# CPI (for inflation calculation)
cpi_data = {
    "value": 307.05,  # Current CPI index value
    "series_id": "CPIAUCSL",
    "fetched_at": datetime.now().isoformat(),
    "source": "FRED API"
}

with open(os.path.join(cache_dir, "fred_cpiaucsl.json"), 'w') as f:
    json.dump(cpi_data, f, indent=2)
print(f"✓ Created CPI cache: {cpi_data['value']}")

# Fed Funds Rate (FRED DFF)
fed_rate_data = {
    "value": 5.33,
    "series_id": "DFF",
    "fetched_at": datetime.now().isoformat(),
    "source": "FRED API"
}

with open(os.path.join(cache_dir, "fred_dff.json"), 'w') as f:
    json.dump(fed_rate_data, f, indent=2)
print(f"✓ Created Fed Rate cache: {fed_rate_data['value']}%")

# GDP
gdp_data = {
    "value": 27939.0,  # GDP in billions
    "series_id": "GDP",
    "fetched_at": datetime.now().isoformat(),
    "source": "FRED API"
}

with open(os.path.join(cache_dir, "fred_gdp.json"), 'w') as f:
    json.dump(gdp_data, f, indent=2)
print(f"✓ Created GDP cache: {gdp_data['value']}B")

print(f"\n✓ All macro cache files created in: {cache_dir}/")
print("\nNote: Cache will be valid for 24 hours")
print("The MacroRegimeDetector will use this cached data.\n")
