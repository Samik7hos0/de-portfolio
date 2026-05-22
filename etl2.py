import requests
import pandas as pd
import psycopg2

url = "https://restcountries.com/v3.1/region/asia"
response = requests.get(url)
data = response.json()
print(f"Extracted {len(data)} countries")

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
print(f"Transformed {len(df)} rows")

conn = psycopg2.connect("postgresql://neondb_owner:npg_RkceSzXO4ao7@ep-restless-unit-apd1qu9k.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require")
print("Connected to PostgreSQL")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS asian_countries(
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
print(f"Loaded {len(df)} rows into PostgreSQL")
cur.close()
conn.close()
print("Connection closed.")