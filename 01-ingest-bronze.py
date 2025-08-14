# Databricks Notebook: 01-ingest-bronze

from pyspark.sql.functions import current_timestamp

# Drop existing Delta tables if they exist
spark.sql("DROP TABLE IF EXISTS default.cpg_line1_stream")
spark.sql("DROP TABLE IF EXISTS default.cpg_line1_batch")

# Load Stream JSONL files into raw table
df_stream = spark.read.json("dbfs:/mnt/raw_data/cpg-line1-stream-*.jsonl")
df_stream = df_stream.withColumn("source_file", df_stream["_metadata"]["file_path"]) \
                     .withColumn("ingest_time", current_timestamp())

df_stream.write.format("delta").mode("overwrite").saveAsTable("default.cpg_line1_stream")

# Load Batch JSONL files into raw table
df_batch = spark.read.json("dbfs:/mnt/raw_data/cpg-line1-batches-*.jsonl")
df_batch = df_batch.withColumn("source_file", df_batch["_metadata"]["file_path"]) \
                   .withColumn("ingest_time", current_timestamp())

df_batch.write.format("delta").mode("overwrite").saveAsTable("default.cpg_line1_batch")
