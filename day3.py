import pandas as pd

# Read CSV file
df = pd.read_csv("employee.csv")

# Basic exploration
print("=== Shape (rows, columns) ===")
print(df.shape)

print("\n=== Column names ===")
print(df.columns.tolist())

print("\n=== First 3 rows ===")
print(df.head(3))

print("\n=== Data types ===")
print(df.dtypes)