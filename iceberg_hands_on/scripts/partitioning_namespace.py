# Step 1: Create the "partitioning_example" namespace in Nessie
spark.sql("CREATE NAMESPACE IF NOT EXISTS nessie.partitioning_example")
print("Namespace 'partitioning_example' created in Nessie")

# Step 2: Create an Iceberg table with initial partitioning on the 'name' column
spark.sql("""
    CREATE TABLE nessie.partitioning_example.example_table (
        id INT,
        name STRING,
        count INT,
        ts TIMESTAMP
    )
    USING iceberg
    PARTITIONED BY (name)
""")
print("Iceberg table created with initial partitioning on 'name'")

# Step 3: Insert initial data into the Iceberg table
spark.sql("""
    INSERT INTO nessie.partitioning_example.example_table VALUES
    (1, 'Alice', NULL, TIMESTAMP('2024-07-02T12:00:00')),
    (2, 'Bob', 5, TIMESTAMP('2024-07-02T12:05:00')),
    (3, 'Catherine', 10, TIMESTAMP('2024-07-02T12:10:00'))
""")
print("Initial data inserted into Iceberg table")

# Step 4: Update the partitioning of the Iceberg table to include the 'ts' column
spark.sql("""
    ALTER TABLE nessie.partitioning_example.example_table
    ADD PARTITION FIELD bucket(4, ts) AS ts_bucket
""")
print("Iceberg table partitioning updated to include 'ts' column")

# Step 5: Insert additional data into the Iceberg table
spark.sql("""
    INSERT INTO nessie.partitioning_example.example_table VALUES
    (4, 'David', 15, TIMESTAMP('2024-07-02T12:15:00')),
    (5, 'Eve', 20, TIMESTAMP('2024-07-02T12:20:00'))
""")
print("Additional data inserted into Iceberg table")

spark.sql("SELECT * FROM nessie.partitioning_example.example_table;").show()