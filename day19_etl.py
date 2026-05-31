import requests
import json
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# ------ EXTRACT ---------------------------------
def extract():
    print("📥 Extract data from API...")
    response = requests.get("https://restcountries.com/v3.1/region/asia")

    if response.status_code != 200:
        raise Exception(f"API failed: {response.status_code}")
    
    countries = response.json()
    print(f"✅ Extracted {len(countries)} countries")
    return countries

# ------- TRANSFORM -------------------------------
def transform(countries):
    print("\n🔄 Transforming data...")

    transformed = []
    for country in countries:
        transformed.append({
            "name": country['name']['common'],
            "population": country.get('population', 0),
            "area": country.get('area', 0.0),
            "capital": country.get('capital', ['N/A'])[0],
            "subregion": country.get('subregions', 'Unknown')
                if isinstance(country.get('subregions'), str)
                else country.get('subregion', 'Unknown')
        })

    df = pd.DataFrame(transformed)

    # Remove duplicates
    df = df.drop_duplicates(subset=['name'])

    # Remove rows with 0 population
    df = df[df['population'] > 0]

    # Add calculated coulmn
    df['population_millions'] = (df['population'] / 1_000_000).round(2)

    print(f"✅ Transformed {len(df)} records")
    print(f" Columns: {list(df.columns)}")
    return df

# --------- LOAD ----------------
def load(df):
    print("\n📤 Loading data to JSON...")
    df.to_json("asia_etl_output.json", orient="records", indent=4)
    print(f"✅ Loaded {len(df)} records to asia_etl_output.json")

    print("\n📊 Summary:")
    print(f"  Total countries: {len(df)}")
    print(f"  Total population: {df['population'].sum():,}")
    print(f"   Largest country by area: {df.loc[df['area'].idxmax(), 'name']}")
    print(f"   Most populated: {df.loc[df['population'].idxmax(), 'name']}")

# --------- PIPELINE ------------
def run_pipeline():
    print("🚀 Starting ETL Pipeline")
    print("=" * 40)

    try:
        raw_data = extract()
        clean_data = transform(raw_data)
        load(clean_data)
        print("\n✅ Pipeline completed successfully!")

    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()
