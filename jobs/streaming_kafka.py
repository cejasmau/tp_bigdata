from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, window, avg
from pyspark.sql.types import DoubleType, TimestampType

spark = SparkSession.builder \
    .appName("KafkaMarketData") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Leer desde Kafka
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "node2-kafka:9092") \
    .option("subscribe", "market-data") \
    .option("startingOffsets", "latest") \
    .load()

# Kafka value -> string
df = raw_df.selectExpr("CAST(value AS STRING) as value")

# Parseo CSV: ticker,timestamp,price
parsed = df.select(
    split(col("value"), ",").getItem(0).alias("ticker"),
    split(col("value"), ",").getItem(1).cast(TimestampType()).alias("event_time"),
    split(col("value"), ",").getItem(2).cast(DoubleType()).alias("price")
)

# Ventanas de 30 segundos
windowed_avg = parsed \
    .withWatermark("event_time", "1 minute") \
    .groupBy(
        window(col("event_time"), "30 seconds"),
        col("ticker")
    ) \
    .avg("price") \
    .withColumnRenamed("avg(price)", "avg_price")


query = windowed_avg.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", False) \
    .trigger(processingTime="30 seconds") \
    .start()

query.awaitTermination()

