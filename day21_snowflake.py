import snowflake.connector
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to Snowflake
conn = snowflake.connector.connect(
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    warehouse='COMPUTE_WH',
    database='DE_GRIND',
    schema='RAW',
    role='ACCOUNTADMIN'
)

print("✅ Connected to Snowflake!")

# Querry existing data
cursor = conn.cursor()
cursor.execute("SELECT * FROM asian_countries ORDER BY population DESC")
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor .description]

# Load into pandas DataFrame
df = pd.DataFrame(rows, columns=columns)
print(f"\n📊 Fetched {len(df)} rows from Snowflake:")
print(df[['NAME', 'POPULATION', 'SUBREGION']]. to_string(index=False))

cursor .close()
conn.close()
print("\n🔌 Connection closed.")

# WRITE PATH - insert new data from python
conn = snowflake.connector.connect(
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    warehouse='COMPUTE_WH',
    database='DE_GRIND',
    schema='RAW',
    role='ACCOUNTADMIN'
)

cursor = conn.cursor()

# New data to insert
new_countries = [
    (11, 'Saudi Arabia', 35950396, 2149690, 'Western Asia', 'Riyadh'),
    (12, 'Uzbekistan', 35300000, 448978, 'Central Asia', 'Tashkent'),
]

cursor.executemany(
    "INSERT INTO asian_countries (id, name, population, area, subregion, capital) VALUES (%s, %s, %s, %s, %s, %s)",
    new_countries
)

conn.commit()
print(f"\n✅ Inserted {len(new_countries)} new rows into Snowflake!")

# Verify
cursor.execute("SELECT COUNT(*) FROM asian_countries")
count = cursor.fetchone()[0]
print(f"📊 Total rows now: {count}")

cursor.close()
conn.close()

import requests

# MINI ETL — API → Snowflake
conn = snowflake.connector.connect(
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    warehouse='COMPUTE_WH',
    database='DE_GRIND',
    schema='RAW',
    role='ACCOUNTADMIN'
)

cursor = conn.cursor()

# Extract — pull from REST Countries API
print("\n🔄 Extracting from API...")
response = requests.get('https://restcountries.com/v3.1/subregion/Central%20Asia')
data = response.json()

# Transform — clean and structure
records = []
for country in data:
    records.append((
        country.get('name', {}).get('common', 'Unknown'),
        country.get('population', 0),
        country.get('area', 0),
        'Central Asia',
        list(country.get('capital', ['Unknown']))[0] if country.get('capital') else 'Unknown'
    ))

print(f"✅ Extracted {len(records)} Central Asian countries")

# Load — insert into Snowflake
cursor.execute("DELETE FROM asian_countries WHERE subregion = 'Central Asia'")

for i, record in enumerate(records, start=20):
    cursor.execute(
        "INSERT INTO asian_countries (id, name, population, area, subregion, capital) VALUES (%s, %s, %s, %s, %s, %s)",
        (i, *record)
    )

conn.commit()
print(f"✅ Loaded {len(records)} rows into Snowflake RAW layer")

cursor.execute("SELECT COUNT(*) FROM asian_countries")
print(f"📊 Total rows: {cursor.fetchone()[0]}")

cursor.close()
conn.close()