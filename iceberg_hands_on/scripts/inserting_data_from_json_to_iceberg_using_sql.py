import json

# Step 1: Create a JSON file with a few records
json_data = [
    {"id": 1, "name": "Alice", "ts": "2024-07-02T12:00:00"},
    {"id": 2, "name": "Bob", "ts": "2024-07-02T12:05:00"},
    {"id": 3, "name": "Catherine", "ts": "2024-07-02T12:10:00"}
]

json_file_path = "/tmp/data.json"
with open(json_file_path, 'w') as json_file:
    json.dump(json_data, json_file)

# Step 2: Read the JSON file into a DataFrame
df = spark.read.json(json_file_path)
df.createOrReplaceTempView("json_table")

# Cast the ts column to timestamp
spark.sql("SELECT id, name, CAST(ts AS TIMESTAMP) AS ts FROM json_table").createOrReplaceTempView("json_table_casted")

# Step 3: Create the "db" namespace in Nessie
spark.sql("CREATE NAMESPACE IF NOT EXISTS nessie.db")
print("Namespace 'db' created in Nessie")

# Step 4: Create an empty Iceberg table using SQL
spark.sql("""
    CREATE TABLE nessie.db.example_sql_table (
        id INT,
        name STRING,
        ts TIMESTAMP
    )
    USING iceberg
""")
print("Iceberg table created with no records")

# Step 5: Insert the data from the temporary view into the Iceberg table
spark.sql("""
    INSERT INTO nessie.db.example_sql_table
    SELECT id, name, ts FROM json_table_casted
""")
print("Data inserted into Iceberg table from JSON DataFrame")

spark.sql("SELECT * FROM nessie.db.example_sql_table").show()