import requests
import json

# 1. Call a real free API - REST Countries
print("=== Fetching country data from API ===")
response = requests.get("https://restcountries.com/v3.1/region/asia")

# 2. Check if request succeeded
print(f"Status code: {response.status_code}")

if response.status_code == 200:
    countries = response.json()
    print(f"Total countries fetched: {len(countries)}")

    # 3. Extract only what we need
    extracted = []
    for country in countries:
        extracted.append({
            "name": country['name']['common'],
            "population": country.get('population', 0),
            "area": country.get('area', 0),
            "capital": country.get('capital', ['N/A'])[0]
        })

    # 4. Sort by population
    extracted.sort(key=lambda x: x['population'], reverse=True)

    # 5. Print top 5
    print("\n=== Top 5 Most Populated Asian Countries ===")
    for country in extracted[:5]:
        print(f"{country['name']}: {country['population']:,}")

    # 6. Save to JSON
    with open("asia_countries_api.json", "w") as f:
        json.dump(extracted, f, indent=4)
    print("\n✅ Data saved to asia_countries_api.json")

else:
    print(f"API call failed: {response.status_code}")