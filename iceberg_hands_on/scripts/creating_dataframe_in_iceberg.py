from pyspark.sql.functions import current_timestamp

# Create DataFrame
data = [(1, "Alice"), (2, "Bob"), (3, "Catherine")]
columns = ["id", "name"]
df = spark.createDataFrame(data, columns).withColumn("ts", current_timestamp())

# Write DataFrame to Iceberg table
df.writeTo("nessie.df_table").create()
print("Iceberg table created using DataFrames")

#query table
spark.sql("SELECT * FROM nessie.df_table;").show()