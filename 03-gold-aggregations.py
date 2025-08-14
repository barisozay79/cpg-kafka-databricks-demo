# Databricks Notebook: 03-gold-aggregations

# Create Gold tables with business metrics
from pyspark.sql.functions import avg, max, min, count

# 1. Sensor metrics per hour
df_stream = spark.read.table("default.silver_cpg_line1_stream")

df_gold_sensor = df_stream.groupBy("sensorId", "topic") \
    .agg(
        avg("temperature").alias("avg_temp"),
        avg("humidity").alias("avg_humidity"),
        max("conveyor_speed").alias("max_speed"),
        min("oil_viscosity").alias("min_viscosity"),
        count("*").alias("records")
    )

df_gold_sensor.write.format("delta").mode("overwrite").saveAsTable("default.gold_cpg_line1_sensor_metrics")

# 2. Production status counts from batch table
df_batch = spark.read.table("default.silver_cpg_line1_batch")

df_gold_batch_status = df_batch.groupBy("status") \
    .count() \
    .orderBy("count", ascending=False)

df_gold_batch_status.write.format("delta").mode("overwrite").saveAsTable("default.gold_cpg_line1_batch_status_counts")
