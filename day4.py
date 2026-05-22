import requests
import pandas as pd

# Step 1 — Make a request to a free public API
url = "https://restcountries.com/v3.1/region/asia"
response = requests.get(url)

# Step 2 — Check if request worked
print("Status code:", response.status_code)
# 200 = success, anything else = error

# Step 3 — Parse JSON response
data = response.json()
print("Total countries returned:", len(data))
print("First country raw data:")
print(data[0])

# Step 4 — Extract only the fields you need
countries = []

for country in data:
    countries.append({
        'name': country['name']['common'],
        'population': country['population'],
        'area': country['area'],
        'region': country.get('subregion', 'Unknown'),
        'capital': country['capital'][0] if country.get('capital') else 'None'
    })

# Step 5 — Load into DataFrame
df = pd.DataFrame(countries)
print("\n=== Asian Countries Dataset ===")
print(df.head())
print("\nShape:", df.shape)

# Step 6 — Answer questions from the data
print("\n=== Top 5 Most Populated ===")
print(df.sort_values('population', ascending=False).head())

print("\n=== Average population by subregion ===")
print(df.groupby('region')['population'].mean().sort_values(ascending=False))