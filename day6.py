import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
df = pd.read_sql("SELECT * FROM asian_countries", conn)

print("===shape(rows,columns)===")
print(df.shape)

print("\n=== Top 5 Most Populated ===")
print(df.sort_values('population', ascending=False).head())

print("\n=== Average area by subregion ===")
print(df.groupby('subregion')['area'].mean().sort_values(ascending=False))

conn.close()
print("Connection closed.")