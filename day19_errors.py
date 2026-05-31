import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# ── SCENARIO 1: API failure handling ─────────────────
def extract_with_retry(url, max_retries=3):
    print(f"🔄 Fetching: {url}")
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # raises exception for 4xx/5xx
            print(f"✅ Success on attempt {attempt}")
            return response.json()
            
        except requests.exceptions.Timeout:
            print(f"⚠️ Attempt {attempt} timed out")
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP error: {e}")
            break  # don't retry on HTTP errors
            
        except requests.exceptions.ConnectionError:
            print(f"⚠️ Attempt {attempt} — connection error")
    
    raise Exception(f"Failed after {max_retries} attempts")

# ── SCENARIO 2: Missing data handling ────────────────
def safe_extract_field(data, field, default=None):
    try:
        value = data[field]
        if value is None or value == "":
            return default
        return value
    except (KeyError, TypeError):
        return default

# ── SCENARIO 3: Data validation ──────────────────────
def validate_record(record):
    errors = []
    
    if not record.get('name'):
        errors.append("Missing name")
    
    if record.get('population', 0) < 0:
        errors.append("Negative population")
    
    if record.get('area', 0) < 0:
        errors.append("Negative area")
    
    return errors

# ── RUN ALL SCENARIOS ─────────────────────────────────
print("=== Scenario 1: API with retry ===")
try:
    data = extract_with_retry(
        "https://restcountries.com/v3.1/name/india"
    )
    print(f"Got data for: {data[0]['name']['common']}")
except Exception as e:
    print(f"Pipeline stopped: {e}")

print("\n=== Scenario 2: Missing data handling ===")
sample = {"name": "TestCountry", "population": None}
name = safe_extract_field(sample, 'name', 'Unknown')
pop = safe_extract_field(sample, 'population', 0)
area = safe_extract_field(sample, 'area', 0)
print(f"Name: {name}, Population: {pop}, Area: {area}")

print("\n=== Scenario 3: Validation ===")
good_record = {"name": "India", "population": 1400000000, "area": 3287263}
bad_record = {"name": "", "population": -100, "area": -50}

for record in [good_record, bad_record]:
    errors = validate_record(record)
    if errors:
        print(f"❌ Invalid record: {errors}")
    else:
        print(f"✅ Valid record: {record['name']}")