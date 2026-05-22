import psycopg2

# Connection string
conn = psycopg2.connect("postgresql://neondb_owner:npg_RkceSzXO4ao7@ep-restless-unit-apd1qu9k.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require")

print("Connected to PostgreSQL successfully!")

# Create a cursor to run SQL
cur = conn.cursor()

# Create a table
cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        salary INTEGER,
        department VARCHAR(50)
    )
""")

# Insert some rows
cur.execute("INSERT INTO employees (name, salary, department) VALUES (%s, %s, %s)", ('Joe', 70000, 'IT'))
cur.execute("INSERT INTO employees (name, salary, department) VALUES (%s, %s, %s)", ('Max', 90000, 'Sales'))
cur.execute("INSERT INTO employees (name, salary, department) VALUES (%s, %s, %s)", ('Sam', 60000, 'IT'))

# Commit the changes
conn.commit()

print("Table created and 3 rows inserted!")

# Query the data back
cur.execute("SELECT * FROM employees")
rows = cur.fetchall()
print("\n=== Data in PostgreSQL ===")
for row in rows:
    print(row)

# Close connection
cur.close()
conn.close()
print("\nConnection closed.")