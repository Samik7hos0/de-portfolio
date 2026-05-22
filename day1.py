import pandas as pd

# Create a simple dataset
data = {
    'name': ['Joe', 'Henry', 'Sam', 'Max', 'Janet'],
    'salary': [70000, 80000, 60000, 90000, 69000],
    'department': ['IT', 'Sales', 'IT', 'Sales', 'IT']
}

df = pd.DataFrame(data)

print("=== Full Dataset ===")
print(df)

print("\n=== IT Department Only ===")
print(df[df['department'] == 'IT'])

print("\n=== Average Salary per Department ===")
print(df.groupby('department')['salary'].mean())

print("\n=== Sorted by Salary DESC ===")
print(df.sort_values('salary', ascending=False))
print("\n=== Highest Paid per Department ===")
print(df.groupby('department')['salary'].max())