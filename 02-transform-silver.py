# Databricks Notebook: 02-transform-silver

# Create silver tables from bronze with basic filtering and column renaming
from pyspark.sql.functions import col

# Stream (sensor) silver table
df_stream = spark.read.table("default.cpg_line1_stream") \
    .filter("temperature IS NOT NULL AND humidity IS NOT NULL")

df_stream.write.format("delta").mode("overwrite").saveAsTable("default.silver_cpg_line1_stream")

# Batch silver table
df_batch = spark.read.table("default.cpg_line1_batch") \
    .filter("status IS NOT NULL")

df_batch.write.format("delta").mode("overwrite").saveAsTable("default.silver_cpg_line1_batch")
