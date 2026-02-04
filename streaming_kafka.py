from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, window, avg
from pyspark.sql.types import DoubleType, TimestampType

spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Leer desde Kafka
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "node2-kafka:9092") \
    .option("subscribe", "market-data") \
    .option("startingOffsets", "latest") \
    .load()

# value viene como binary
values_df = raw_df.selectExpr("CAST(value AS STRING)")

# Parseo: ticker,timestamp,price
parsed_df = values_df.select(
    split(col("value"), ",").getItem(0).alias("ticker"),
    split(col("value"), ",").getItem(1).cast(TimestampType()).alias("event_time"),
    split(col("value"), ",").getItem(2).cast(DoubleType()).alias("price")
)

# Ventanas de 30 segundos
windowed_df = parsed_df.groupBy(
    window(col("event_time"), "30 seconds"),
    col("ticker")
).agg(
    avg("price").alias("avg_price")
)

query = windowed_df.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime="30 seconds") \
    .start()

query.awaitTermination()