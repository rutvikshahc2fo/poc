# Create an Iceberg table using SQL
spark.sql("""
    CREATE TABLE nessie.sql_table (
        id INT,
        name STRING
    )
    USING iceberg
""")

spark.sql("INSERT INTO nessie.sql_table VALUES (1, 'Alex Merced'), (2, 'Andew Madson');")

spark.sql("SELECT * FROM nessie.sql_table;").show()