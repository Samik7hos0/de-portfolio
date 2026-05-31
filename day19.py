import json
import csv
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Write data to JSON file
pipeline_config = {
    "dag_id": "etl_pipeline",
    "schedule": "@daily",
    "source": "postgresql",
    "destination": "snowflake",
    "tables": ["orders", "customers", "products"],
    "record_count": 5000
}

with open("pipeline_config.json", "w") as f:
    json.dump(pipeline_config, f, indent=4)
print("✅ JSON file written")

# 2. Read it back
with open("pipeline_config.json", "r") as f:
    config = json.load(f)
print(f"DAG ID: {config['dag_id']}")
print(f"Tables: {config['tables']}")
print(f"Records: {config['record_count']}")

# 3. Write CSV file
rows = [
    ["order_id", "customer", "amount", "status"],
    [1001, "Alice", 250.00, "completed"],
    [1002, "Bob", 175.50, "pending"],
    [1003, "Charlie", 320.00, "completed"],
    [1004, "Diana", 89.99, "failed"],
    [1005, "Eve", 450.00, "completed"]
]

with open("orders.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)
print("\n✅ CSV file written")

# 4. Read CSV back
with open("orders.csv", "r") as f:
    reader = csv.DictReader(f)
    orders = list(reader)

print(f"Total orders: {len(orders)}")
print(f"First order: {orders[0]}")

# 5. Filter completed orders
completed = [o for o in orders if o['status'] == 'completed']
print(f"\nCompleted orders: {len(completed)}")
for order in completed:
    print(f"  Order {order['order_id']}: ${order['amount']}")