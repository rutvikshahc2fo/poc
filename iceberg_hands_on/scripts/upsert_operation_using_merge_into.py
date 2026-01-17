from pyspark.sql.functions import col
json_data = [
    {"id": 1, "name": "Alice", "count": None, "ts": "2024-07-02T12:00:00"},
    {"id": 2, "name": "Bob", "count": 5, "ts": "2024-07-02T12:05:00"},
    {"id": 3, "name": "Catherine", "count": 10, "ts": "2024-07-02T12:10:00"}
]

json_file_path = "/tmp/data.json"
with open(json_file_path, 'w') as json_file:
    json.dump(json_data, json_file)

# Step 2: Read the JSON file into a DataFrame
df = spark.read.json(json_file_path)
df = df.withColumn("ts", col("ts").cast("timestamp"))
df.createOrReplaceTempView("json_table")
df.show()

# Step 3: Create the "db" namespace in Nessie
spark.sql("CREATE NAMESPACE IF NOT EXISTS nessie.merge_example")
print("Namespace 'merge_example' created in Nessie")

# Step 4: Create an empty Iceberg table using SQL
spark.sql("""
    CREATE TABLE nessie.merge_example.example_table (
        id INT,
        name STRING,
        count INT,
        ts TIMESTAMP
    )
    USING iceberg
""")
print("Iceberg table created with no records")

# Insert the initial data into the Iceberg table
spark.sql("""
    INSERT INTO nessie.merge_example.example_table
    SELECT id, name, count, ts FROM json_table
""")
print("Initial data inserted into Iceberg table")

spark.sql("SELECT * FROM nessie.merge_example.example_table;").show()

# Step 5: Create a source DataFrame for updates
update_data = [
    {"id": 1, "name": "Alice", "count": 1, "op": "increment"},
    {"id": 2, "name": "Bob", "count": 1, "op": "increment"},
    {"id": 3, "name": "Catherine", "count": None, "op": "delete"},
    {"id": 4, "name": "David", "count": 1, "op": "insert"}
]

update_file_path = "/tmp/update_data.json"
with open(update_file_path, 'w') as update_file:
    json.dump(update_data, update_file)

source_df = spark.read.json(update_file_path)
source_df.createOrReplaceTempView("source_table")
source_df.show()

# Step 6: Use the MERGE INTO command to update the Iceberg table
spark.sql("""
    MERGE INTO nessie.merge_example.example_table t
    USING source_table s
    ON t.id = s.id
    WHEN MATCHED AND s.op = 'delete' THEN DELETE
    WHEN MATCHED AND t.count IS NULL AND s.op = 'increment' THEN UPDATE SET t.count = 0
    WHEN MATCHED AND s.op = 'increment' THEN UPDATE SET t.count = t.count + 1
    WHEN NOT MATCHED THEN INSERT (id, name, count, ts) VALUES (s.id, s.name, s.count, current_timestamp())
""")
print("Data merged into Iceberg table using MERGE INTO")

spark.sql("SELECT * FROM nessie.merge_example.example_table;").show()