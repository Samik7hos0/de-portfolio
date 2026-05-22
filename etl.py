import requests
import pandas as pd
import psycopg2

CONN = "postgresql://neondb_owner:npg_RkceSzXO4ao7@ep-restless-unit-apd1qu9k.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require"

# ---- EXTRACT ----
print("Extracting data from API...")
url = "https://restcountries.com/v3.1/region/asia"
response = requests.get(url)
data = response.json()
print(f"Fetched {len(data)} countries")

# ---- TRANSFORM ----
print("Transforming data...")
countries = []
for country in data:
    countries.append({
        'name': country['name']['common'],
        'population': country['population'],
        'area': country['area'],
        'subregion': country.get('subregion', 'Unknown'),
        'capital': country['capital'][0] if country.get('capital') else 'None'
    })
df = pd.DataFrame(countries)
print(f"Cleaned {len(df)} rows")

# ---- LOAD ----
print("Loading into PostgreSQL...")
conn = psycopg2.connect(CONN)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS asian_countries (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        population BIGINT,
        area FLOAT,
        subregion VARCHAR(100),
        capital VARCHAR(100)
    )
""")

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO asian_countries (name, population, area, subregion, capital)
        VALUES (%s, %s, %s, %s, %s)
    """, (row['name'], row['population'], row['area'], row['subregion'], row['capital']))

conn.commit()
cur.close()
conn.close()

print(f"Done. {len(df)} rows loaded into asian_countries table.")