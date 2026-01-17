import pyspark
from pyspark.sql import SparkSession
import os

## DEFINE SENSITIVE VARIABLES
NESSIE_SERVER_URI = "http://172.20.0.2:19120/api/v2"
WAREHOUSE_BUCKET = "s3://warehouse"
MINIO_URI = "http://172.20.0.3:9000"


## Configurations for Spark Session
conf = (
    pyspark.SparkConf()
        .setAppName('app_name')
  		#packages
        .set('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.2,org.projectnessie.nessie-integrations:nessie-spark-extensions-3.5_2.12:0.91.3,software.amazon.awssdk:bundle:2.20.131,software.amazon.awssdk:url-connection-client:2.20.131')
  		#SQL Extensions
        .set('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions,org.projectnessie.spark.extensions.NessieSparkSessionExtensions')
  		#Configuring Catalog
        .set('spark.sql.catalog.nessie', 'org.apache.iceberg.spark.SparkCatalog')
        .set('spark.sql.catalog.nessie.uri', NESSIE_SERVER_URI)
        .set('spark.sql.catalog.nessie.ref', 'main')
        .set('spark.sql.catalog.nessie.authentication.type', 'NONE')
        .set('spark.sql.catalog.nessie.catalog-impl', 'org.apache.iceberg.nessie.NessieCatalog')
        .set("spark.sql.catalog.nessie.s3.endpoint",MINIO_URI)
        .set('spark.sql.catalog.nessie.warehouse', WAREHOUSE_BUCKET)
        .set('spark.sql.catalog.nessie.io-impl', 'org.apache.iceberg.aws.s3.S3FileIO')
)

## Start Spark Session
spark = SparkSession.builder.config(conf=conf).getOrCreate()
print("Spark Running")

## TEST QUERY TO CHECK IT WORKING
### Create TABLE
spark.sql("CREATE TABLE nessie.example (name STRING) USING iceberg;").show()
### INSERT INTO TABLE
spark.sql("INSERT INTO nessie.example VALUES ('Alex Merced');").show()
### Query Table
spark.sql("SELECT * FROM nessie.example;").show()